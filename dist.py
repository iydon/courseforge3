import pathlib as p
import shutil
import subprocess as sp


root_src = p.Path("build")
root_dst = p.Path("dist")
src2dst = {
    "README.md": "README.md",
    "verbatim.txt": "verbatim.txt",
    "slides/main.pdf": "slides.pdf",
    "case/": "case/",
}

for dir_src in root_src.iterdir():
    dir_dst = root_dst / dir_src.relative_to(root_src)
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
        shutil.rmtree(cache)
    sp.run(
        ["uv", "export", "--only-group=case", "--output-file=requirements.txt"],
        cwd=dir_dst,
        capture_output=True,
        check=True,
    )
