import pathlib as p
import typing as t


type Maybe[T] = T | None
type Gen[T] = t.Generator[T, None, None]

type Floats = list[float]
type PathLike = str | p.Path
type PathLikes = list[PathLike]
type Strings = list[str]
