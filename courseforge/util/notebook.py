import copy
import functools as f
import json
import pathlib as p
import sys
import time
import typing as t

from ..const import ENCODING
from ..type import Maybe, PathLike

if t.TYPE_CHECKING:
    import nbformat

    from nbconvert.preprocessors import ExecutePreprocessor


class Notebook:
    version = 4

    def __init__(self, path: PathLike, timeout: int = 600) -> None:
        self._path = p.Path(path)
        self._time = timeout
        self._core: Maybe["ExecutePreprocessor"] = None
        self._node: Maybe["nbformat.NotebookNode"] = None

    @classmethod
    def fromNode(
        cls,
        node: "nbformat.NotebookNode",
        path: PathLike = "temp.ipynb",
        timeout: int = 600,
        clone: bool = True,
    ) -> t.Self:
        self = cls(path, timeout)
        self._node = copy.deepcopy(node) if clone else node
        return self

    @classmethod
    def fromPath(cls, path: PathLike, timeout: int = 600) -> t.Self:
        return cls(path, timeout)

    @property
    def kernel(self) -> "ExecutePreprocessor":
        if self._core is None:
            from nbconvert.preprocessors import ExecutePreprocessor

            self._core = ExecutePreprocessor(
                timeout=self._time,
                kernel_name="python3",
                extra_arguments=["--colors=nocolor", "--log-level=ERROR"],
            )
        return self._core

    @property
    def node(self) -> "nbformat.NotebookNode":
        if self._node is None:
            import nbformat

            self._node = nbformat.from_dict(nbformat.read(self._path, self.version))
        return self._node

    @f.cached_property
    def is_valid(self) -> bool:
        try:
            with self._path.open("r", encoding=ENCODING) as file:
                nb: dict = json.load(file)
        except Exception as e:
            self._log(f"无效的 JSON: {e}")
            return False
        for key in ["cells", "metadata", "nbformat", "nbformat_minor"]:
            if key not in nb:
                self._log(f"缺少字段: {key}")
                return False
        if nb.get("nbformat") != self.version:
            self._log(f"当前 nbformat 版本为 {nb.get('nbformat')}", kind="warn")
        if not isinstance(nb["cells"], list):
            self._log("cells 必须是列表")
            return False
        for ith, cell in enumerate(nb["cells"]):
            if not isinstance(cell, dict):
                self._log(f"单元格 {ith} 不是字典")
                return False
            for key in ["cell_type", "source"]:
                if key not in cell:
                    self._log(f"单元格缺少字段: {key}")
                    return False
            kind: str = dict(cell)["cell_type"]  # ty: error[invalid-argument-type]
            if kind not in ("code", "markdown", "raw"):
                self._log(f"单元格 {ith} cell_type 未知: {kind}")
                return False
        return True

    def run(self, output: Maybe[PathLike] = None, force: bool = False) -> bool:
        path_cache = self._path.parent / ".cache" / f"{self._path.name}.time"
        if not force and path_cache.exists():
            return True
        path_final = self._path if output is None else p.Path(output)
        try:
            elapsed = -time.perf_counter()
            self.kernel.preprocess(self.node)
            elapsed += time.perf_counter()
        except Exception as e:
            self._log(str(e))
            return False
        else:
            path_cache.parent.mkdir(parents=True, exist_ok=True)
            path_cache.write_text(str(elapsed))
            self.to_path(path_final)
            return True

    def clear(self, output: Maybe[PathLike] = None) -> t.Self:
        from nbconvert.preprocessors import ClearOutputPreprocessor

        ClearOutputPreprocessor().preprocess(self.node, resources={})
        return self.to_path(output or self._path)

    def fix(self, output: Maybe[PathLike] = None) -> t.Self:
        import nbformat

        nbformat.validator.normalize(self.node, version=self.version)
        return self.to_path(output or self._path)

    def to_path(self, path: PathLike) -> t.Self:
        import nbformat

        path = p.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(self.node, path)
        return self

    def remove_comments(self, timeout: int = 600) -> t.Self:
        other = self.fromNode(self.node, timeout=timeout)
        for cell in other.node["cells"]:
            if cell["cell_type"] != "code":
                continue
            cell["source"] = "\n".join(
                line
                for line in str(cell["source"]).splitlines()
                if not line.startswith("#")
            ).strip()
        return other

    def _log(self, message: str, kind: str = "error") -> None:
        data = {"type": kind, "path": self._path.as_posix(), "message": message}
        print(json.dumps(data, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    root = p.Path(__file__).parent
    if len(sys.argv) <= 1:
        paths = sorted(root.glob("*.ipynb"))
    else:
        paths = list(map(p.Path, sys.argv[1:]))
    code = 0
    for path_src in paths:
        if path_src.name.startswith("_"):
            continue
        if path_src.is_relative_to(root):
            path_src = path_src.relative_to(root)
        path_dst = path_src.with_name(f"_{path_src.name}")
        note = Notebook.fromPath(path_src)
        code += not (note.is_valid and note.run(path_dst, force=True))
    sys.exit(code)
