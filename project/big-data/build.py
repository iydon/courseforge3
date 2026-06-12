getattr(getattr(__import__("sys"), "path"), "append")("../..")


import pathlib as p

import tqdm

from courseforge.base import Course
from courseforge.util.astral_uv import AstralUv
from courseforge.util.opencode import OpenCode
from courseforge.util.other import mkdir
from courseforge.util.statistics import Statistics


root = p.Path(__file__).parent
course = Course.fromYaml("outline.yaml")
stat = Statistics.fromDirectory("build")
uv = AstralUv.fromDefault()
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
    paths = [dir_02 / f"{ith + 1}.py" for ith in range(3)]
    if not all(path.exists() for path in paths):
        oc.run_template("prompt/02-case.md").consume()
        uv.format(dir_02)
    assert all(path.exists() for path in paths)
    uv.runs(dir_02)
print(f"# {stat.directory}")
print(stat.summary())
