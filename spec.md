# 项目核心规约 (Project Specifications)

本文件汇总了 **智能体** 项目的核心开发与文档规范。所有贡献者在提交代码或文档前，必须阅读并遵循以下规约。

## 1. 文档编写规约
*   **适用范围**: 项目内所有 Markdown (`.md`) 文档。
*   **执行标准**: [doc-spec.md](./spec/doc-spec.md)
*   **关键要求**:
    *   严禁使用 MDN 风格，必须遵循 **Google Markdown Style**。
    *   必须使用 **4 空格** 进行列表缩进。
    *   必须使用 ATX 标题 (`#`) 且前后保留空行。
    *   概念词汇使用 `**Bold**`，注意项使用 `_Italic_`。

## 2. Java 代码规约
*   **适用范围**: 所有 Java (`.java`) 源代码。
*   **执行标准**: [java-spec.md](./spec/java-spec.md)
*   **关键要求**:
    *   严格遵循 Google Java Style Guide。
    *   必须包含 Javadoc。

## 3. Python 代码规约
*   **适用范围**: 所有 Python (`.py`) 源代码。
*   **执行标准**: [python-spec.md](./spec/python-spec.md)
*   **关键要求**:
    *   遵循 PEP 8 标准。
    *   必须使用 Type Hints (类型提示)。
    *   使用 `reformat_docs.py` 等工具维持代码格式。
