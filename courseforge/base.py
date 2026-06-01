import functools as f
import pathlib as p
import typing as t

import yaml

from .type import Gen, PathLike


type Outline = dict[str, Info | Outline]


class Info(t.TypedDict):
    detail: str
    duration: float


class Course:
    sep = "__"

    def __init__(self, outline: Outline) -> None:
        self._outline: Outline = outline

    @classmethod
    def fromYaml(cls, path: PathLike) -> t.Self:
        with open(path, "r") as file:
            return cls(yaml.safe_load(file))

    @f.cached_property
    def lessons(self) -> dict[str, Info]:
        name2info = list(self._lessons(self._outline, ""))
        width = len(str(len(name2info)))
        return {
            f"{ith:0{width}}{self.sep}{name}": info
            for ith, (name, info) in enumerate(name2info, start=1)
        }

    def iter_lessons(self, directory: PathLike = "") -> Gen[tuple[p.Path, Info]]:
        directory = p.Path(directory).resolve()
        for name, info in self.lessons.items():
            cwd = directory / name
            cwd.mkdir(parents=True, exist_ok=True)
            yield cwd, info

    def _lessons(self, outline: Outline, name: str) -> Gen[tuple[str, Info]]:
        for key, value in outline.items():
            temp = f"{name}{self.sep}{key}" if name else key
            if self._is_lesson(value):
                yield temp, value
            else:
                value = t.cast(Outline, value)
                yield from self._lessons(value, temp)

    def _is_lesson(self, data: Info | Outline) -> t.TypeGuard[Info]:
        return "detail" in data and "duration" in data
