import pathlib as p
import shutil

import tqdm

from courseforge.base import Course
from courseforge.util.astral_uv import AstralUv
from courseforge.util.notebook import Notebook
from courseforge.util.opencode import OpenCode
from courseforge.util.other import mkdir
from courseforge.util.statistics import Statistics


course = Course.fromYaml("outline.yaml")
stat = Statistics.fromDirectory("build")
uv = AstralUv.fromDefault()
path_chk_src = p.Path("script/check.py")
for cwd, info in tqdm.tqdm(list(course.iter_lessons(stat.directory))):
    oc = OpenCode.fromDeepSeek("pro", cwd)
    # 0x01 教师讲义
    path_01 = cwd / "README.md"
    if not path_01.exists():
        oc.run_template(
            "prompt/01-lesson.md",
            path=path_01,
            outline=repr(course.lessons),
            name=cwd.name,
            detail=info["detail"],
            duration=info["duration"],
        ).consume()
    assert path_01.exists()
    # 0x02 实战案例
    dir_02 = mkdir(cwd / "case")
    path_chk_dst = cwd / path_chk_src.name
    shutil.copyfile(path_chk_src, path_chk_dst)
    paths = [dir_02 / f"{ith + 1}.ipynb" for ith in range(2)]
    if not all(path.exists() for path in paths):
        oc.run_template("prompt/02-case.md").consume()
    assert all(path.exists() for path in paths)
    for path_src in paths:
        path_dst = path_src.with_name(f"_{path_src.name}")
        if path_dst.exists():
            continue
        assert Notebook.fromPath(path_src).fix().run(path_dst, force=True)
        uv.format(dir_02)
    path_chk_dst.unlink()
    # 0x03 教学课件 + 逐字稿
    assert (cwd / "slides/main.pdf").exists()
    assert (cwd / "verbatim.txt").exists()
print(f"# {stat.directory}")
print(stat.summary())
