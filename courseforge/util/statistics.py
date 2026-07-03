import functools as f
import pathlib as p
import shutil
import typing as t

from .notebook import Notebook
from ..type import Number, PathLike, Str2Int, Str2Strs


type KeyValueUnit = tuple[str, Number, str]
type Metrics = list[KeyValueUnit]


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
        for path in self._dir.rglob("*.pdf"):
            with open(path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                ans += len(reader.pages)
        return ans

    @f.cached_property
    def notebook(self) -> Str2Int:
        ans = {"code": 0, "markdown": 0}
        for path in self._dir.rglob("*.ipynb"):
            note = Notebook.fromPath(path)
            cells: list[dict] = note.node["cells"]
            for cell in cells:
                kind: str = cell["cell_type"]
                text: str = cell["source"]
                ans[kind] += len(text.splitlines())
        return ans

    @f.lru_cache
    def lines(self, suffix: str) -> int:
        ans = 0
        for path in self._dir.rglob(f"*.{suffix}"):
            with path.open("r") as file:
                ans += sum(1 for _ in file)
        return ans

    def metrics(self) -> Metrics:
        items = [
            ("PDF", self.pages, "pages"),
            ("Runtime", self.minutes, "minutes"),
            ("Python", self.lines("py"), "lines"),
            ("Markdown", self.lines("md"), "lines"),
        ]
        for kind, line in self.notebook.items():
            kind = {"code": "Python", "markdown": "Markdown"}[kind]
            items.append((f"Jupyter > {kind}", line, "lines"))
        return items

    def summary(self, **kwargs) -> str:
        from tabulate import tabulate

        headers = ["Metric", "Value", "Unit"]
        kwargs = {"tablefmt": "github"} | kwargs
        return tabulate(self.metrics(), headers, **kwargs)

    def clone(
        self,
        directory: PathLike,
        src2dsts: Str2Strs = {},
        force: bool = True,
        skip_missing: bool = False,
    ) -> t.Self:
        dir_src, dir_dst = self._dir, p.Path(directory)
        other = self.fromDirectory(dir_dst)
        if dir_dst.exists():
            if force:
                shutil.rmtree(dir_dst)
            else:
                return other
        for path_src in self._dir.iterdir():
            if not path_src.is_dir():
                continue
            path_dst = dir_dst / path_src.relative_to(dir_src)
            for src, dsts in src2dsts.items():
                for dst in dsts or [src]:
                    file_src, file_dst = path_src / src, path_dst / dst
                    if not file_src.exists():
                        if skip_missing:
                            continue
                        else:
                            raise FileNotFoundError(file_src)
                    file_dst.parent.mkdir(parents=True, exist_ok=True)
                    copy = shutil.copytree if src.endswith("/") else shutil.copyfile
                    copy(file_src, file_dst)
        return other
