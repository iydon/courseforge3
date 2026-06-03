import pathlib
import typing as t


type Maybe[T] = T | None
type Gen[T] = t.Generator[T, None, None]

type Floats = list[float]
type PathLike = str | pathlib.Path
type PathLikes = list[PathLike]
type Strings = list[str]
