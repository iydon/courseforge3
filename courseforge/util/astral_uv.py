import functools as f
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

    @f.cached_property
    def lock(self) -> dict:
        with open("uv.lock", "r") as file:
            return tomllib.loads(file.read())

    @f.cached_property
    def members(self) -> Strings:
        return self.lock["manifest"]["members"]

    @f.cached_property
    def pkg2pkgs(self) -> Str2Strs:
        ans = {}
        for package in self.lock["package"]:
            deps = dict(package).get("dependencies", [])
            if not deps:
                continue
            ans[package["name"]] = [x["name"] for x in deps]
        return ans

    @f.cached_property
    def grp2pkgs(self) -> Str2Strs:
        return {member: self.pkg2pkgs.get(member, []) for member in self.members}

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

    def get_redundants(self, root: str = "courseforge") -> Str2StrSet:
        ans: Str2StrSet = {}
        closure: StrSet = set()
        for dep in self.grp2pkgs.get(root, []):
            closure.add(dep)
            closure.update(self._transitive(self.pkg2pkgs, dep))
        for name, pkgs in sorted(self.grp2pkgs.items()):
            mapper = {pkg: self._transitive(self.pkg2pkgs, pkg) for pkg in pkgs}
            ans[name] = set()
            for lhs in pkgs:
                for rhs in pkgs:
                    if lhs != rhs and lhs in mapper.get(rhs, set()):
                        ans[name].add(lhs)
                        break
            if name != root:
                ans[name].update(
                    pkg for pkg in pkgs if pkg not in self.members and pkg in closure
                )
        return ans

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
