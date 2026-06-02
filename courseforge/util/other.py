import pathlib as p

from ..type import PathLike


def mkdir(path: PathLike, parent: bool = False) -> p.Path:
    path = p.Path(path)
    (path.parent if parent else path).mkdir(parents=True, exist_ok=True)
    return path
