import tqdm

from courseforge.base import Course
from courseforge.util.opencode import OpenCode


if __name__ == "__main__":
    course = Course.fromYaml("outline.yaml")
    for cwd, info in tqdm.tqdm(list(course.iter_lessons("build"))):
        oc = OpenCode.fromDeepSeek("pro", cwd)
        # 0x01
        path_01 = cwd / "README.md"
        if not path_01.exists():
            kwargs = {
                "path": path_01,
                "outline": repr(course.lessons),
                "name": cwd.name,
                "detail": info["detail"],
                "duration": str(info["duration"]),
            }
            oc.run_template("prompt/01-lesson.md", **kwargs).consume()
        assert path_01.exists()
