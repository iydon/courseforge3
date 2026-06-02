import io
import json
import pathlib as p
import string
import subprocess as sp
import threading
import time
import typing as t

from ..const import CACHE
from ..type import Floats, Gen, Maybe, PathLike, Strings


LOG = CACHE / "log" / "opencode"


class OpenCode:
    exe = "opencode"

    def __init__(
        self, cwd: PathLike = ".", model: Maybe[str] = None, pure: bool = False
    ) -> None:
        self._cwd = p.Path(cwd).resolve()
        self._model = model
        self._pure = pure
        self._session: Maybe[str] = None
        self._args = ["--dir", self._cwd, "--format", "json"]
        if self._model is not None:
            self._args += ["--model", self._model]
        if self._pure:
            self._args.append("--pure")
        self._args.append("--dangerously-skip-permissions")

    @classmethod
    def fromDeepSeek(
        cls, kind: t.Literal["flash", "pro"] = "flash", *args, **kwargs
    ) -> t.Self:
        model = f"deepseek/deepseek-v4-{kind}"
        return cls(*args, model=model, **kwargs)

    @property
    def cwd(self) -> p.Path:
        return self._cwd

    @property
    def session(self) -> Maybe[str]:
        return self._session

    def run(self, prompt: str) -> "Result":
        log = LOG / time.strftime("%Y%m%dT%H%M%S")
        log.mkdir(parents=True, exist_ok=True)
        (log / "prompt.md").write_text(prompt)
        args = [self.exe, "run", prompt] + self._args
        if self._session is not None:
            args += ["--session", self._session]
        proc = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE, cwd=self._cwd, text=True)
        stderr: Strings = []
        if proc.stderr is not None:
            func = lambda: stderr.append(t.cast(io.TextIOWrapper, proc.stderr).read())
            threading.Thread(target=func, daemon=True).start()
        return Result(proc, stderr, self, log)

    def run_template(self, path: PathLike, /, **kwargs) -> "Result":
        text = string.Template(p.Path(path).read_text()).substitute(**kwargs)
        return self.run(text)


class Result:
    def __init__(
        self,
        proc: sp.Popen[str],
        stderr: Strings,
        oc: OpenCode,
        log: p.Path,
    ) -> None:
        self._proc = proc
        self._stderr = stderr
        self._oc = oc
        self._log = log
        self._cost: Floats = []
        self._usage: list[dict] = []
        self._stdout: Maybe[list[dict]] = None

    def __iter__(self) -> Gen[dict]:
        if self._stdout is not None:
            yield from self._stdout
            return
        self._stdout = []
        if self._proc.stdout:
            for line in self._proc.stdout:
                line = line.rstrip("\n")
                event = self._parse(line)
                if event is not None:
                    self._stdout.append(event)
                    with (self._log / "stdout.jsonl").open("a") as file:
                        file.write(line + "\n")
                    yield event
        self._finalize()

    @property
    def stdout(self) -> list[dict]:
        self.consume()
        assert self._stdout is not None
        return self._stdout

    @property
    def stderr(self) -> str:
        return "".join(self._stderr)

    @property
    def cost(self) -> Floats:
        return self._cost

    @property
    def usage(self) -> list[dict]:
        self.consume()
        return self._usage

    def consume(self) -> t.Self:
        if self._stdout is None:
            list(self)
        return self

    def _parse(self, line: str) -> Maybe[dict]:
        try:
            ans: dict = json.loads(line)
        except json.JSONDecodeError:
            return
        if not self._oc._session and (session := ans.get("sessionID")):
            self._oc._session = session
        if ans.get("type") == "step_finish":
            part: dict = ans.get("part", {})
            self._cost.append(part.get("cost", 0.0))
            self._usage.append(part.get("tokens", {}))
        return ans

    def _finalize(self) -> None:
        self._proc.wait()
        (self._log / "stderr.txt").write_text(self.stderr)
        meta = {
            "session": self._oc._session,
            "model": self._oc._model,
            "cost": self._cost,
            "usage": self._usage,
        }
        (self._log / "meta.json").write_text(json.dumps(meta, ensure_ascii=False))
        if self._proc.returncode != 0:
            raise sp.CalledProcessError(self._proc.returncode, self._proc.args)
