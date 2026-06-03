请根据 `README.md` 和 `case/` 目录下的案例代码，在 `slides/` 目录下生成一套 LaTeX beamer 课件，面向本科生教学。必须严格按以下工作流执行，不得跳过编译验证环节：

## 工作流

1. **编写内容**：仅修改 `slides/section.tex`（参考其中的示例样式），不要新建其他文件，不要修改 `slides/main.tex`
2. **编译验证**：在 `slides/` 目录内执行 `latexmk`（无其他参数），目录下已有 `.latexmkrc` 配置文件
3. **修复重试**：若编译失败，根据报错信息修正 `slides/section.tex`，重新执行步骤 2，直至编译通过且无 error

所有文件读写和命令执行均以 `slides/` 目录为工作目录，禁止在 `slides/` 上级目录执行 `latexmk`。

## 内容规范

- 内容详尽、结构清晰，适合授课及零基础自学；每页代码均需附带详细讲解，不可单独放置代码
- 课件中的代码示例优先引用 `case/` 目录下的案例代码，保持理论与实战结合
- 必要时使用 tikz 绘制图形，所需库在 `slides/main.tex` 导言区引入
- 使用 `columns` 环境时，总宽度 ≤0.98\textwidth，并添加 `[T]` 选项实现顶对齐
- 允许长页面自动分页（`allowframebreaks`），包含代码的帧需添加 `fragile` 选项
- 非代码抄录环境，下划线、美元符在 LaTeX 中需要转义，即 `\_`、`\$$`
- 使用 `\section` 和 `\subsection` 组织章节，最少 $page 页
