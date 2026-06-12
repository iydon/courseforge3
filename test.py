import pathlib as p
import shutil
import subprocess as sp

import tqdm

from courseforge.util.astral_uv import AstralUv
from courseforge.util.opencode import OpenCode


path_chk_src = p.Path("static/script/check.py")
prompt = """
请将 {src} 转换为 Jupyter Notebook {dst}，必须符合 nbformat 4 规范。

## 工作流

1. 读取 {src} 的完整内容
2. 按以下规则分割为 notebook cells，写入 {dst}
3. 执行 `uv run check {dst}` 验证，status code 为 0 即为通过
4. 若验证失败，根据错误信息修复 {dst} 并重新验证，直至通过

## 分割规则

- **文件顶部的模块 docstring** → 单独一个 markdown cell
- **连续的 import 语句** → 合并为一个 code cell
- **函数/类定义** → 每个定义单独一个 code cell（定义前的 docstring 转为 markdown cell）
- **顶层的 print / 实验代码块** → 按逻辑段落分割为独立的 code cell
- **`───` / `====` 装饰线和实验分组注释** → 转为描述性 markdown cell
- **代码中的 `#` 行内注释** → 若注释解释后续代码块，转为该 cell 前的 markdown cell
- **汇总/结论部分的 print** → 合并为最终 markdown cell

## JSON 结构要求

```json
{{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {{ "kernelspec": {{ "display_name": "Python 3", "language": "python", "name": "python3" }} }},
  "cells": [
    {{
      "cell_type": "markdown",
      "metadata": {{}},
      "source": ["# 标题\\n", "说明文字\\n"]
    }},
    {{
      "cell_type": "code",
      "metadata": {{}},
      "source": ["import os\\n"],
      "outputs": [],
      "execution_count": null
    }}
  ]
}}
```

注意 source 是字符串列表，每行一个元素，行末须保留 \\n。
""".strip()

uv = AstralUv.fromDefault()
directories = sorted(p.Path("build").rglob("case"))
for dir_src in tqdm.tqdm(directories):
    print(dir_src)
    dir_dst = dir_src.with_name("note")
    dir_dst.mkdir(parents=True, exist_ok=True)
    path_chk_dst = dir_dst / path_chk_src.name
    shutil.copyfile(path_chk_src, path_chk_dst)
    for temp_src in dir_src.glob("*.py"):
        path_dst = dir_dst / f"{temp_src.stem}.ipynb"
        if path_dst.exists():
            continue
        path_src = dir_dst / temp_src.name
        shutil.copyfile(temp_src, path_src)
        # opencode
        oc = OpenCode.fromDeepSeek("flash", cwd=dir_dst)
        oc.run(prompt.format(src=path_src.name, dst=path_dst.name)).consume()
        uv.run(path_chk_dst, force=True, extra=[path_dst])
        sp.run(["uv", "run", path_chk_dst.name, path_dst], cwd=dir_dst, check=True)
        path_src.unlink()
    path_chk_dst.unlink()
