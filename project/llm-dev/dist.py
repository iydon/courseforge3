import pathlib as p

from courseforge.util.astral_uv import AstralUv
from courseforge.util.statistics import Statistics


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dsts = {
    "README.md": [],
    # "verbatim.txt": [],
    "slides/main.pdf": ["slides.pdf"],
    "case/.cache/1.py.time": [],
    "case/.cache/2.py.time": [],
    "case/.cache/3.py.time": [],
    "case/1.py": [],
    "case/2.py": [],
    "case/3.py": [],
}
old = Statistics.fromDirectory(dir_src)
new = old.clone(dir_dst, src2dsts)
print(new.summary())
AstralUv.fromDefault().export(dir_dst / "requirements.txt", extra=["--no-hashes"])
