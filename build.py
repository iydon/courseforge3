import itertools as it
import pathlib as p

import tqdm

from courseforge.base import Course
from courseforge.util.astral_uv import AstralUv
from courseforge.util.latex import LaTeX
from courseforge.util.opencode import OpenCode
from courseforge.util.other import mkdir
from courseforge.util.statistics import Statistics


root = p.Path(__file__).parent
for yaml in p.Path("static/outline").iterdir():
    course = Course.fromYaml(yaml)
    stat = Statistics.fromDirectory(f"build/{yaml.stem}")
    uv = AstralUv.fromDefault()
    for cwd, info in tqdm.tqdm(list(course.iter_lessons(stat.directory))):
        oc = OpenCode.fromDeepSeek("pro", cwd)
        # 0x01 教师讲义
        path_01 = cwd / "README.md"
        if not path_01.exists():
            oc.run_template(
                "static/prompt/01-lesson.md",
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
            oc.run_template("static/prompt/02-case.md").consume()
            uv.format(dir_02)
        assert all(path.exists() for path in paths)
        uv.runs(dir_02)
        # # 0x03 教学课件
        # dir_03 = mkdir(cwd / "slides")
        # path = dir_03 / "main.pdf"
        # minute = 2  # minute per page
        # if not path.exists():
        #     latex = LaTeX.fromDirectory(dir_03)
        #     level = len(dir_03.relative_to(root).parts)
        #     iroot = p.Path(*it.repeat("..", level), "static")
        #     _, title, *parts = cwd.name.split(Course.sep)
        #     (
        #         latex.copy("static/slides/.latexmkrc")
        #         .copy("static/slides/section.tex")
        #         .copy_template(
        #             "static/slides/main.tex",
        #             iroot=iroot,
        #             title=title,
        #             part="/".join(parts),
        #         )
        #     )
        #     page = 60 * info["duration"] // minute
        #     oc.run_template("static/prompt/03-slides.md", page=page).consume()
        #     latex.make()
        # assert path.exists()
        # # 0x04 逐字稿
        # path_04 = cwd / "verbatim.txt"
        # if path_04.exists() and not path_04.read_bytes().strip():
        #     oc.run_template("static/prompt/04-verbatim.md", duration=minute).consume()
    print(f"# {stat.directory}")
    print(stat.summary())
