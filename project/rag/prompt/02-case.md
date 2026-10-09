请根据当前目录下的 `README.md`（本课时教师讲义）的内容，创建 2 个实战案例 Jupyter Notebook。必须严格按以下工作流逐文件完成，不得跳过验证环节：

## 环境与依赖约束（必须遵守）

- 本仓库是 uv 工作空间的子工作区：添加依赖只能执行 `uv add <包名>`（会自动写入正确的 pyproject.toml 并更新锁文件），运行程序只能执行 `uv run ...`。
- 严禁新建、删除或手工编辑 pyproject.toml / uv.lock；严禁使用 pip、conda；严禁 `uv init`、`uv venv` 等会破坏本仓库环境的命令。
- 所有命令一律在课时根目录（当前目录）下执行；Notebook 内的相对路径以课时根目录为基准，持久化数据统一写入 `case/.cache/`。
- 缺少依赖时现装现用，例如 `uv add faiss-cpu`（向量库课时）、`uv add llama-index-retrievers-bm25`（检索课时），安装后必须重新运行验证。

## 模型与密钥约束

- 大模型统一使用 `deepseek-flash`，接入信息只从环境变量读取，禁止硬编码、占位符或虚构变量名：

```python
import os

from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    model="deepseek-flash",
    api_base=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    is_chat_model=True,
)
```

- 向量化统一使用 `BAAI/bge-small-zh-v1.5`（本地已缓存）；禁止换用其他 Embedding 模型，禁止下载大模型权重；重排优先使用 sentence-transformers 的小尺寸 CrossEncoder。
- 调用 DeepSeek 的示例保持最小化（短输入、短输出），不要编写多轮长对话压测。

## 可执行性约束

- 案例必须能全程无人值守自动执行：禁止启动常驻或阻塞进程（`streamlit run`、web 服务、死循环、轮询等待等），涉及交互界面的内容只写代码和讲解，不要真的启动服务。
- 单个 cell 执行时间不得超过 10 分钟（执行器超时 600 秒）。
- 样本文档使用文本格式（Markdown / TXT / CSV / HTML）或带文字层的极小 PDF；禁止依赖 OCR、语音识别、大模型下载类重流程（Docling 模型已缓存，可直接使用）。

## 风格约束（必须遵守）

- 去 AI 味：Markdown 说明文字避免使用破折号（——）、引号、括号、箭头（→、->）、单横杠等非必要符号（对话的引号可以保留，代码、命令、列表标记等其他特殊情形也可以酌情保留）。
- 小节标题禁用 A 与 B 式并列结构，此类结构易显机械且导致主题分散。
- 不布置作业、课后练习或思考题，案例 Notebook 即本课全部产出。
- 不出现课时时长、课时序号等课程元信息。
- 案例必须自成体系，单独使用即可上课：不引用其他课时的文件、数据或产物，不假设读者学过其他课时。

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

- 案例尽量简洁，聚焦课时核心流程，避免过度复杂的代码
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
