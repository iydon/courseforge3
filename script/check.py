"""Validate and execute Jupyter Notebooks using courseforge.

Usage: uv run check.py <notebook.ipynb> [<notebook2.ipynb> ...]

Performs two stages for each notebook:
  1. Validate  —— JSON structure / nbformat compliance
  2. Execute   —— run all cells, output to _<original-name>.ipynb

Exit code 0 = all notebooks passed both stages.
"""

import pathlib as p
import sys

from courseforge.type import PathLike
from courseforge.util.notebook import Notebook


def check(path: PathLike) -> bool:
    path_src = p.Path(path)
    note = Notebook.fromPath(path_src)
    # Stage 1: validation
    if not note.is_valid:
        return False
    # Stage 2: execution (output → _xxx.ipynb in same directory)
    path_dst = path_src.with_name(f"_{path_src.name}")
    return note.run(path_dst, force=True)


if __name__ == "__main__":
    code = sum(1 for path in sys.argv[1:] if not check(path))
    raise SystemExit(code)
