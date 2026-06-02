请根据刚才的课时内容，在 `case/` 目录下创建 3 个实战案例 Python 代码，要求：

1. 使用 uv 管理依赖：`uv add openai` 安装，`uv run case/N.py` 运行
2. 使用 OpenAI 兼容接口，连接方式如下（直接在案例中写出，环境变量由用户自行设置）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com",
)
```

3. 案例命名：`case/1.py`、`case/2.py`、`case/3.py`
4. 每个案例需能独立运行，覆盖课时内容中的关键知识点
5. 禁止使用 `input()` 或任何交互式输入，所有数据直接在代码中硬编码，确保 `uv run` 一键跑通
6. 添加必要的注释和错误处理
