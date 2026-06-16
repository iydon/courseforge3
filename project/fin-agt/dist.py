import pathlib as p

from courseforge.util.statistics import Statistics


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dsts = {
    "README.md": [],
    "verbatim.txt": [],
    "slides/main.pdf": ["slides.pdf"],
}
old = Statistics.fromDirectory(dir_src)
new = old.clone(dir_dst, src2dsts)
print(new.summary())
