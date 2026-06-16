import pathlib as p
import warnings

from tabulate import tabulate

from courseforge.type import Number
from courseforge.util.statistics import Statistics


warnings.filterwarnings("ignore")

root = p.Path("project")
headers = ["Project", "Value"]

m2p2v: dict[str, dict[str, Number]] = {}
for directory in root.iterdir():
    name = directory.name
    stat = Statistics.fromDirectory(directory / "dist")
    for metric, value, _ in stat.metrics():
        m2p2v.setdefault(metric, {}).setdefault(name, value)

for metric, p2v in m2p2v.items():
    print("#", metric)
    print(tabulate(p2v.items(), headers, tablefmt="github"))
    print()
