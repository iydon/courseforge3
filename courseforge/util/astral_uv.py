import pathlib as p
import subprocess as sp
import time
import traceback
import typing as t

from ..type import PathLike, Strings


class AstralUv:
    exe = "uv"

    def __init__(self) -> None:
        pass

    @classmethod
    def fromDefault(cls) -> t.Self:
        return cls()

    def run(self, path: PathLike, force: bool = False) -> t.Self:
        path = p.Path(path)
        return self.runs(path.parent, [path.name], force)

    def runs(
        self,
        directory: PathLike,
        names: Strings = [],
        force: bool = False,
        extra: Strings = [],
    ) -> t.Self:
        directory = p.Path(directory)
        dir_cache = directory / ".cache"
        dir_cache.mkdir(parents=True, exist_ok=True)
        names = names or [path.name for path in directory.glob("*.py")]
        for name in names:
            path_cache = dir_cache / f"{name}.time"
            if not force and path_cache.exists():
                continue
            elapsed = -time.perf_counter()
            args = [self.exe, "run", name, *extra]
            cp = sp.run(args, cwd=directory, capture_output=True, text=True)
            elapsed += time.perf_counter()
            if cp.returncode != 0:
                raise sp.CalledProcessError(
                    cp.returncode, cp.args, output=cp.stdout, stderr=cp.stderr
                )
            path_cache.write_text(str(elapsed))
        return self

    def format(self, directory: PathLike) -> None:
        sp.run([self.exe, "format"], cwd=directory, check=True, capture_output=True)
