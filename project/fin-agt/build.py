import pathlib as p
import shutil

import tqdm

from courseforge.base import Course
from courseforge.util.astral_uv import AstralUv
from courseforge.util.opencode import OpenCode
from courseforge.util.other import mkdir
from courseforge.util.statistics import Statistics


root = p.Path(__file__).parent
script = root / "../../script"
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
    # 0x02 教学课件
    path_02 = mkdir(cwd / "slides/main.pdf", parent=True)
    minute = 2  # minute per page
    page = 60 * info["duration"] // minute
    if not path_02.exists():
        shutil.copyfile(script / "gpt_image.py", path_02.parent / "gpt_image.py")
        oc.run_template(
            "prompt/02-slides.md",
            page=page,
            name=cwd.name,
            detail=info["detail"],
            duration=info["duration"],
        ).consume()
    assert path_02.exists()
    # 0x03 逐字稿
    path_03 = cwd / "verbatim.txt"
    if not path_03.exists():
        oc.run_template(
            "prompt/03-verbatim.md",
            duration=minute,
            page=page,
            name=cwd.name,
        ).consume()
    assert path_03.exists()
print(f"# {stat.directory}")
print(stat.summary())
