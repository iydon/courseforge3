import functools as f
import pathlib as p
import typing as t

from ..type import PathLike, Strings


class Statistics:
    def __init__(self, directory: PathLike) -> None:
        self._dir = p.Path(directory)

    @classmethod
    def fromDirectory(cls, directory: PathLike) -> t.Self:
        return cls(directory)

    @property
    def directory(self) -> p.Path:
        return self._dir

    @property
    def minutes(self) -> float:
        return self.seconds / 60.0

    @f.cached_property
    def seconds(self) -> float:
        ans = 0.0
        for path in self._dir.rglob("*.time"):
            ans += float(path.read_text())
        return ans

    @f.cached_property
    def pages(self) -> int:
        import PyPDF2

        ans = 0
        for path in self._dir.rglob("slides/main.pdf"):
            with open(path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                ans += len(reader.pages)
        return ans

    @f.lru_cache
    def lines(self, suffix: str) -> int:
        ans = 0
        for path in self._dir.rglob(f"*.{suffix}"):
            with path.open("r") as file:
                ans += sum(1 for _ in file)
        return ans

    def summary(self, suffixes: Strings = ["py", "md"]) -> str:
        lines = [
            f"pdf = {self.pages} pages",
            f"run = {self.minutes:.1f} minutes",
        ]
        for suffix in suffixes:
            lines.append(f"lines@{suffix} = {self.lines(suffix)}")
        return "\n".join(lines)
