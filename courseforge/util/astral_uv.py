import itertools as it
import pathlib as p
import subprocess as sp
import time
import tomllib
import typing as t

from ..type import PathLike, Str2StrSet, Str2Strs, StrSet, Strings


class AstralUv:
    exe = "uv"

    def __init__(self) -> None:
        pass

    @classmethod
    def fromDefault(cls) -> t.Self:
        return cls()

    def run(self, path: PathLike, force: bool = False, extra: Strings = []) -> t.Self:
        path = p.Path(path)
        return self.runs(path.parent, [path.name], force, extra)

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

    def export(self, path: PathLike = "requirements.txt", extra: Strings = []) -> None:
        path = p.Path(path)
        args = [self.exe, "export", f"--output-file={path.name}", *extra]
        sp.run(args, cwd=path.parent, check=True, capture_output=True)

    def format(self, directory: PathLike, extra: Strings = []) -> None:
        args = [self.exe, "format", *extra]
        sp.run(args, cwd=directory, check=True, capture_output=True)

    def get_redundants(self, path_lock: PathLike) -> Str2StrSet:
        with open(path_lock, "r") as file:
            lock = tomllib.loads(file.read())
        pkg2pkgs: Str2Strs = {}
        for package in lock["package"]:
            package: dict
            dependencies = package.get("dependencies", [])
            if not dependencies:
                continue
            name = package["name"]
            deps = self._get_names(dependencies)
            pkg2pkgs[name] = deps
        grp2pkgs: Str2Strs = {
            member: pkg2pkgs[member] for member in lock["manifest"]["members"]
        }
        ans: Str2StrSet = {}
        for name, pkgs in sorted(grp2pkgs.items()):
            mapper = {pkg: self._transitive(pkg2pkgs, pkg) for pkg in pkgs}
            ans[name] = set()
            for lhs, rhs in it.product(pkgs, pkgs):
                if lhs != rhs and lhs in mapper[rhs]:
                    ans[name].add(lhs)
                    break
        return ans

    def _get_names(self, xs: list[dict]) -> Strings:
        return [x["name"] for x in xs]

    def _transitive(self, graph: Str2Strs, pkg: str) -> StrSet:
        ans: StrSet = set()
        stack = [pkg]
        while stack:
            current = stack.pop()
            for pkg in graph.get(current, []):
                if pkg in ans:
                    continue
                ans.add(pkg)
                stack.append(pkg)
        return ans
