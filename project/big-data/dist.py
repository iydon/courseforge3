import pathlib as p
import shutil
import subprocess as sp


dir_src = p.Path("build")
dir_dst = p.Path("dist")
src2dst = {
    "README.md": "README.md",
    "verbatim.txt": "verbatim.txt",
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
        file_src, file_dst = path_src / src, path_dst / dst
        if not file_src.exists():
            continue
        copy = shutil.copytree if src.endswith("/") else shutil.copyfile
        copy(file_src, file_dst)
for cache in dir_dst.rglob(".cache"):
    for path in cache.iterdir():
        if path.is_file() and path.suffix != ".time":
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
group = f"case-{dir_src.name}"
sp.run(
    ["uv", "export", "--output-file=requirements.txt"],
    cwd=dir_dst,
    capture_output=True,
    check=True,
)
