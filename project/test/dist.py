import pathlib as p

from courseforge.util.astral_uv import AstralUv
from courseforge.util.notebook import Notebook
from courseforge.util.statistics import Statistics


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dsts = {
    "README.md": [],
    "case/1.py": [],
    "case/2.py": [],
    "case/3.py": [],
    "case/.cache/1.py.time": [],
    "case/.cache/2.py.time": [],
    "case/.cache/3.py.time": [],
    "note/_1.ipynb": ["note/1.ipynb"],
    "note/_2.ipynb": ["note/2.ipynb"],
    "note/_3.ipynb": ["note/3.ipynb"],
    "note/.cache/1.ipynb.time": [],
    "note/.cache/2.ipynb.time": [],
    "note/.cache/3.ipynb.time": [],
}

old = Statistics.fromDirectory(dir_src)
new = old.clone(dir_dst, src2dsts)
for path in new.directory.rglob("*_basic.ipynb"):
    Notebook.fromPath(path).remove_comments().to_path(path)
print(new.summary())
AstralUv.fromDefault().export(dir_dst / "requirements.txt")
