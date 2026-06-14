请根据 `case/` 目录下的 3 个 Python 案例代码，在 `note/` 目录下生成对应的 Jupyter Notebook 文件（`case/` 与 `note/` 为同级目录，非嵌套关系）。必须严格按以下工作流逐文件完成，不得跳过验证环节：

## 工作流（对每个案例依次执行）

1. **阅读源码**：阅读 `case/N.py` 的完整内容，理解代码逻辑
2. **编写 Notebook**：在 `note/N.ipynb` 中创建完整的 Jupyter Notebook
3. **结构验证 + 执行**：Notebook 需符合 nbformat 4 规范，每个 cell 可正常执行
4. **修复重试**：若验证失败，根据错误信息修复 Notebook，重新执行步骤 3，直至通过

三个 Notebook 全部通过验证后才能结束。

## Notebook 结构规范

- 案例文件：`note/1.ipynb`、`note/2.ipynb`、`note/3.ipynb`
- 必须严格符合 nbformat 4 规范
- 每个 cell 的 `source` 字段为字符串列表，每行一个元素，行末须保留 `\n`
- code cell 必须包含 `"outputs": []` 和 `"execution_count": null`
- markdown cell 用于详细说明文字、章节标题、知识点讲解，内容尽可能详尽
- code cell 用于可执行的 Python 代码
- 合理的 markdown/code 交替结构，每个逻辑段落前应有 markdown cell 作为说明
- 每个 Notebook 开头需包含一个 markdown cell 作为标题和案例说明
- 代码内容应源自 `case/N.py`，但可按逻辑段落拆分为多个 code cell，每个 code cell 前加 markdown cell 讲解

## JSON 结构示例

```json
{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["# 案例标题\\n", "案例说明，包含知识点覆盖和场景描述\\n"]
    },
    {
      "cell_type": "code",
      "metadata": {},
      "source": ["import numpy as np\\n", "print('Hello World')\\n"],
      "outputs": [],
      "execution_count": null
    }
  ]
}
```

## 具体规范

- 每个案例需独立运行，覆盖对应 .py 文件中的关键知识点
- 禁止使用 `input()` 或任何交互式输入
- 添加充分的注释说明每一步的目的和逻辑
- 涉及本地持久化统一写入 `note/.cache/` 目录，每个 Notebook 的第一个 code cell 须包含如下初始化代码：

```python
import pathlib as p

cache_dir = p.Path(".cache")
cache_dir.mkdir(parents=True, exist_ok=True)
```
- 代码中 matplotlib 已配置中文字体的情况保持不变，所有图表直接使用 `plt.show()` 内联展示，禁止 `plt.savefig()` 保存到本地文件
- 公共 import 可聚合到第一个 code cell，后续 cell 只写核心逻辑
- Notebook 中的注释应比原始 .py 更详细，关键步骤、公式含义、参数选择原因均需注释说明，方便零基础读者理解
