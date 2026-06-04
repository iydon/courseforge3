import pathlib as p
import shutil
import subprocess as sp


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dst = {
    "README.md": "README.md",
    "slides/main.pdf": "slides.pdf",
    "case/": "case/",
}

if dir_dst.exists():
    shutil.rmtree(dir_dst)
dir_dst.mkdir(parents=True, exist_ok=True)

for cache in dir_src.rglob("README.md"):
    path_src = cache.parent
    path_dst = dir_dst / path_src.relative_to(dir_src)
    path_dst.mkdir(parents=True, exist_ok=True)
    for src, dst in src2dst.items():
        if src.endswith("/"):
            shutil.copytree(path_src / src, path_dst / dst)
        else:
            shutil.copyfile(path_src / src, path_dst / dst)
for cache in dir_dst.rglob(".cache"):
    shutil.rmtree(cache)
sp.run(
    ["uv", "export", "--only-group=case", "--output-file=requirements.txt"],
    cwd=dir_dst,
    capture_output=True,
    check=True,
)
