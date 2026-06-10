import itertools as it
import tomllib


type Str2Strs = dict[str, Strings]
type StrSet = set[str]
type Strings = list[str]


def get_names(xs: list[dict]) -> Strings:
    return [x["name"] for x in xs]


def transitive(graph: Str2Strs, pkg: str) -> StrSet:
    ans: StrSet = set()
    stack = [pkg]
    while stack:
        current = stack.pop()
        for pkg in graph.get(current, []):
            if pkg in ans:
                continue
            ans.add(pkg)
            stack.append(pkg)
    return ans


with open("uv.lock", "r") as file:
    lock = tomllib.loads(file.read())
pkg2pkgs: Str2Strs = {}
grp2pkgs: Str2Strs = {}
for package in lock["package"]:
    package: dict
    dependencies = package.get("dependencies", [])
    if not dependencies:
        continue
    name = package["name"]
    deps = get_names(dependencies)
    if name == "courseforge":
        deps_dev: dict = package.get("dev-dependencies", {})
        grp2pkgs = {key: get_names(value) for key, value in deps_dev.items()}
        grp2pkgs[""] = deps
    else:
        pkg2pkgs[name] = deps

for name, pkgs in sorted(grp2pkgs.items()):
    mapper = {pkg: transitive(pkg2pkgs, pkg) for pkg in pkgs}
    redundant: StrSet = set()
    for lhs, rhs in it.product(pkgs, pkgs):
        if lhs != rhs and lhs in mapper[rhs]:
            redundant.add(lhs)
            break
    if redundant:
        cmd = "uv remove {}".format(" ".join(redundant))
        if name:
            cmd += f" --group={name}"
        print(cmd)
