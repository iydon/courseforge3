请根据当前目录下的 `README.md`（本课时教师讲义）的内容，创建 2 个实战案例 Jupyter Notebook。必须严格按以下工作流逐文件完成，不得跳过验证环节：

## 工作流（对每个案例依次执行）

1. **编写 Notebook**：在 `case/N.ipynb` 中创建完整的 Jupyter Notebook
2. **验证 + 执行**：运行 `uv run check.py case/N.ipynb`
   - `check.py` 会先校验 JSON 结构合法性（nbformat 4 规范）
   - 然后执行所有 cell，将带输出的结果写入 `case/_N.ipynb`
   - exit code 0 = 通过，非 0 = 失败
3. **修复重试**：若步骤 2 失败，根据 `check.py` 输出的错误信息修复 Notebook，重新执行步骤 2，直至通过

两个案例全部通过验证后才能结束。

## Notebook 结构规范

- 案例文件：`case/1.ipynb`、`case/2.ipynb`
- 必须严格符合 nbformat 4 规范
- 每个 cell 的 `source` 字段为字符串列表，每行一个元素，行末须保留 `\n`
- code cell 必须包含 `"outputs": []` 和 `"execution_count": null`
- markdown cell 用于详细说明文字、章节标题、知识点讲解，内容尽可能详尽
- code cell 用于可执行的 Python 代码
- 合理的 markdown/code 交替结构，每个逻辑段落前应有 markdown cell 作为说明

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
      "source": ["import pandas as pd\\n", "print('Hello World')\\n"],
      "outputs": [],
      "execution_count": null
    }
  ]
}
```

## 具体规范

- 案例尽量简洁，聚焦核心数据分析流程，避免过度复杂的代码
- 每个案例需独立运行，覆盖课时内容中的关键知识点
- 禁止使用 `input()` 或任何交互式输入，所有数据直接在代码中硬编码
- 代码中添加充分的注释说明每一步的目的和逻辑
- 案例中如需本地持久化（缓存文件、中间结果、输出数据等），统一写入 `case/.cache/` 目录
- 图表使用 `matplotlib` 绘制，必要时保存到 `case/.cache/` 目录
- 绘图前必须配置中文字体，在 import matplotlib 后添加：
```python
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False
```

### 涉及数据存储/查询时

- 统一使用 pandas 进行数据读取、转换与清洗
- 如需本地持久化，写入 `case/.cache/` 目录（如 CSV、Parquet 等格式）
