请根据当前目录下的 `README.md`（本课时教师讲义）的内容，创建 3 个实战案例 Python 代码。必须严格按以下工作流逐文件完成，不得跳过验证环节：

## 工作流（对每个案例依次执行）

1. **编写代码**：在 `case/N.py` 中编写完整代码
2. **安装依赖**：若案例引用了未安装的包，执行 `uv add <包名>`（禁止 `uv init`）
3. **运行验证**：立即执行 `uv run case/N.py`，确认无报错且输出符合预期
4. **修复重试**：若运行失败，分析错误信息并修复代码，重新执行步骤 3，直至通过

三个案例全部通过 `uv run` 验证后才能结束。

## 具体规范

- 案例文件：`case/1.py`、`case/2.py`、`case/3.py`
- 缓存目录统一为脚本所在目录下的 `.cache/`，每个案例文件开头须包含如下初始化代码：

```python
import pathlib as p

root = p.Path(__file__).parent
cache_dir = root / ".cache"
cache_dir.mkdir(parents=True, exist_ok=True)
```

- 每个案例需独立运行，覆盖课时内容中的关键知识点
- 禁止使用 `input()` 或任何交互式输入，所有数据直接在代码中硬编码或随机生成
- 添加必要的注释和错误处理
- 三个案例之间要有递进关系，从基础到进阶

### 涉及绘图时

使用 `matplotlib` 绘图，绘图前必须配置中文字体：

```python
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
```

### 涉及数据存储/查询时

使用 DuckDB 技术栈，连接方式如下（本地文件数据库，无需环境变量）：

```python
import duckdb

conn = duckdb.connect(str(cache_dir / "data.db"))
```

可配合 pandas 进行数据转换与清洗，查询结果优先使用 `.df()` / `.fetchdf()` 方法转为 DataFrame 再继续处理。
