import pathlib as p

from courseforge.util.astral_uv import AstralUv
from courseforge.util.notebook import Notebook
from courseforge.util.statistics import Statistics


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dsts = {
    "README.md": [],
    "verbatim.txt": [],
    "slides/main.pdf": ["slides.pdf"],
    "case/.cache/1.ipynb.time": [
        "case/.cache/1_basic.ipynb.time",
        "case/.cache/1_extra.ipynb.time",
    ],
    "case/.cache/2.ipynb.time": [
        "case/.cache/2_basic.ipynb.time",
        "case/.cache/2_extra.ipynb.time",
    ],
    "case/_1.ipynb": ["case/1_basic.ipynb", "case/1_extra.ipynb"],
    "case/_2.ipynb": ["case/2_basic.ipynb", "case/2_extra.ipynb"],
}
old = Statistics.fromDirectory(dir_src)
new = old.clone(dir_dst, src2dsts, skip_missing=True)
for path in new.directory.rglob("*_basic.ipynb"):
    Notebook.fromPath(path).remove_comments().to_path(path)
print(new.summary())
AstralUv.fromDefault().export(dir_dst / "requirements.txt", extra=["--no-hashes"])
