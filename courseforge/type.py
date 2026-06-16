import pathlib as p
import typing as t


type Maybe[T] = T | None
type Gen[T] = t.Generator[T, None, None]

type Floats = list[float]
type PathLike = str | p.Path
type PathLikes = list[PathLike]
type Str2Int = dict[str, int]
type Str2StrSet = dict[str, StrSet]
type Str2Strs = dict[str, Strings]
type StrSet = set[str]
type Strings = list[str]
