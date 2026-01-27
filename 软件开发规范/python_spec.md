# Python 软件开发规范 (Enterprise Agent Edition)

**版本**: 2.0  
**生效日期**: 2026-01-27  
**基准**: Google Python Style Guide + PEP 8  

本规范旨在建立一套**严格、清晰、可自动化检查**的 Python 代码标准。适用于所有由 Agent 生成或人工编写的 Python 项目。

---

## 1. 代码风格与布局 (Style & Layout)

### 1.1 缩进与断行
-   **缩进**: 强制使用 **4 个空格**。严禁使用 Tab。
-   **行宽**: 限制为 **88 字符** (遵循 `Black` 格式化标准)。超过时必须换行。
-   **断行策略**:
    -   优先在二元运算符**之前**换行。
    -   参数列表过长时，采用"垂直挂起"格式（Vertical Hanging Indent）。

```python
# ✅ Good
def long_function_name(
    var_one: int,
    var_two: str,
    var_three: float,
) -> None:
    result = (
        some_very_long_variable_name
        + another_variable_name
        - third_variable_name
    )
```

### 1.2 导入规范 (Imports)
-   **分区顺序**:
    1.  标准库 (Standard Library)
    2.  第三方库 (Third Party)
    3.  本地应用/库 (Local Application)
-   **组内排序**: 按字母顺序排列。
-   **禁止**: `from module import *` (通配符导入)。
-   **别名**: 仅对通用库使用标准别名 (`numpy as np`, `pandas as pd`, `tensorflow as tf`)。

### 1.3 字符串 (Strings)
-   **F-Strings**: 优先使用 f-string (`f"{name}"`) 进行字符串拼接，性能和可读性最佳。
-   **Docstrings**: 使用**双引号三引号** (`"""`)。

---

## 2. 命名规约 (Naming Conventions)

| 类型 | 规则 | 示例 | 说明 |
| :--- | :--- | :--- | :--- |
| **Module** | `snake_case` | `data_loader.py` | 全小写，下划线分隔 |
| **Package** | `snake_case` | `utils` | 不建议使用下划线，除非必要 |
| **Class** | `PascalCase` | `DataProcessor` | 首字母大写驼峰 |
| **Function** | `snake_case` | `calculate_metrics` | 动词开头 |
| **Variable** | `snake_case` | `user_id` | 名词 |
| **Constant** | `UPPER_CASE` | `MAX_RETRIES` | 全大写，下划线分隔 |
| **Private** | `_snake_case` | `_internal_helper` | 单下划线开头 |

### 2.1 特殊命名规则
-   **布尔值**: 必须以 `is_`, `has_`, `should_`, `can_` 开头。
    -   ✅ `is_valid`
    -   ❌ `valid` (名词混淆)
-   **集合变量**: 使用复数或后缀。
    -   ✅ `users`, `user_list`
    -   ❌ `user` (当它是一个列表时)

---

## 3. 类型系统 (Type System)

### 3.1 强制类型提示 (Mandatory Type Hints)
-   **所有**函数/方法的参数和返回值必须标注类型。
-   使用 Python 3.9+ 原生泛型 (`list[]`, `dict[]`, `tuple[]`)，不再导入 `typing.List` 等。

```python
# ✅ Good (Python 3.10+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

### 3.2 复杂类型定义
-   对于嵌套字典或复杂结构，**禁止**直接使用 `dict`。必须定义 `TypedDict` 或 `dataclass`。

```python
from typing import TypedDict

class UserConfig(TypedDict):
    api_key: str
    timeout: int
    features: list[str]

def configure(config: UserConfig) -> None:
    ...
```

---

## 4. 文档与注释 (Documentation)

### 4.1 Google Style Docstrings
-   **必须**为所有公共模块、类、函数编写 Docstring。
-   包含 `Args`, `Returns`, `Raises` 三个部分。
-   **Rationale**: 不仅描述"做什么"，还要描述"为什么"以及"副作用"。

```python
def connect_db(connection_string: str) -> None:
    """Establishes a connection to the database.

    This function initializes the connection pool. It is not thread-safe 
    and should only be called during startup.

    Args:
        connection_string: The JDBC-style URL for the database.

    Raises:
        ConnectionError: If the server is unreachable.
        ValueError: If the connection string format is invalid.
    """
    ...
```

---

## 5. 工程实践与安全性 (Engineering & Safety)

### 5.1 异常处理
-   **Fail Fast**: 在函数入口进行 Guards Check。
-   **No Bare Except**: 严禁 `except:` 或 `except Exception:`，除非在最顶层入口记录日志。

### 5.2 日志 (Logging)
-   **禁止 print**: 生产代码中严禁出现 `print()`。
-   **使用 logging**:
    -   `logging.info()`: 正常流程关键点。
    -   `logging.warning()`: 预期外的非阻断问题。
    -   `logging.error()`: 导致功能失败的错误 (务必包含 `exc_info=True`)。

### 5.3 资源管理
-   必须使用 Context Managers (`with` 语句) 管理文件、锁、网络连接。

```python
# ✅ Good
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

### 5.4 依赖管理
-   项目根目录必须包含 `requirements.txt` 或 `pyproject.toml`。
-   版本号必须固定 (`pandas==2.2.0`)，避免隐式升级导致的不兼容。

---

## 6. 工具函数设计规范 (Agent-Specific)

### 6.1 接口设计
-   **原子性**: 一个函数只做一件事。
-   **JSON 友好**: 入参和返回值尽量限制在 JSON 数据类型 (str, int, float, bool, list, dict)。
-   **无状态**: 尽量设计为纯函数 (Pure Function)，不依赖全局变量。

### 6.2 错误返回
-   对于工具调用，如果失败，**不要抛出异常**导致 Agent 崩溃。
-   应该捕获异常并返回包含错误信息的结构化结果。

```python
def safe_search(query: str) -> dict[str, str]:
    try:
        # ... logic ...
        return {"status": "success", "data": "..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```
