import pathlib as p
import shutil
import string
import subprocess as sp
import typing as t

from ..type import Maybe, PathLike, PathLikes


class LaTeX:
    exe = "latexmk"

    def __init__(self, cwd: PathLike) -> None:
        self._cwd = p.Path(cwd)

    @classmethod
    def fromDirectory(cls, cwd: PathLike) -> t.Self:
        return cls(cwd)

    def copy(
        self, src: PathLike, dst: Maybe[PathLike] = None, force: bool = False
    ) -> t.Self:
        path_src = p.Path(src)
        path_dst = self._cwd / (dst or path_src.name)
        if force or not path_dst.exists():
            path_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path_src, path_dst)
        return self

    def copy_template(
        self,
        src: PathLike,
        dst: Maybe[PathLike] = None,
        force: bool = False,
        /,
        **kwargs,
    ) -> t.Self:
        path_src = p.Path(src)
        path_dst = self._cwd / (dst or path_src.name)
        if force or not path_dst.exists():
            path_dst.parent.mkdir(parents=True, exist_ok=True)
            text = string.Template(path_src.read_text()).substitute(**kwargs)
            path_dst.write_text(text)
        return self

    def make(self, *args: str) -> None:
        cp = sp.run([self.exe, *args], cwd=self._cwd, capture_output=True)
        assert cp.returncode == 0, cp.stderr.decode()
