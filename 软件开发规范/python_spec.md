# Python 软件开发规范 (Agent-Ready Edition)

本规范基于 **PEP 8** 和 **Google Python Style Guide**，并结合智能体 (Agent) 代码生成的特性进行了优化。旨在作为 Agent 自我审查 (Self-Review) 的核心依据。

## 1. 命名规范 (Naming Conventions)

### 1.1 基础规则
- **模块 (Module)**: `lowercase_underscore.py` (e.g., `data_loader.py`)
- **类 (Class)**: `CapWords` (PascalCase) (e.g., `DataProcessor`)
- **函数/方法 (Function/Method)**: `lowercase_underscore` (snake_case) (e.g., `process_data`)
- **变量 (Variable)**: `lowercase_underscore` (e.g., `user_input`)
- **常量 (Constant)**: `UPPER_CASE_UNDERSCORE` (e.g., `MAX_RETRIES = 3`)
- **私有成员**: `_single_leading_underscore` (e.g., `_internal_helper`)

### 1.2 特殊命名
- **Agent 工具函数**: 必须具有描述性的名称，动词开头，清晰表达意图。
    - ✅ `search_knowledge_base(query: str)`
    - ❌ `search(q: str)`
- **布尔变量**: 使用 `is_`, `has_`, `can_` 前缀。
    - ✅ `is_valid`, `has_permission`
    - ❌ `valid`, `permission`

---

## 2. 代码布局与格式 (Layout & Formatting)

### 2.1 缩进与行宽
- **缩进**: 必须使用 **4 个空格**，严禁使用 Tab。
- **行宽**: 建议 **80-100 字符**。Agent 生成的代码应避免过长行，以提升可读性和 Token 效率。

### 2.2 导入 (Imports)
- **顺序**: 标准库 -> 第三方库 -> 本地模块。
- **避免**: `from module import *` (污染命名空间)。
- **推荐**: `import numpy as np` (使用标准别名)。

```python
# ✅ Good
import os
import sys
import pandas as pd
from my_module import MyClass

# ❌ Bad
from my_module import *
```

### 2.3 空行
- 顶级定义（类、函数）之间空 **2 行**。
- 类内部方法之间空 **1 行**。

---

## 3. 类型提示 (Type Hints)

### 3.1 强制要求
- **所有公共函数/方法**必须包含类型提示 (Type Hints)。这对于 Agent 理解函数签名至关重要。
- 使用 `typing` 模块 (如 `List`, `Dict`, `Optional`, `Union`) 或 Python 3.9+ 的原生泛型。

```python
# ✅ Good
def calculate_metrics(data: List[float], threshold: float = 0.5) -> Dict[str, float]:
    ...
```

### 3.2 复杂类型
- 对于复杂的字典结构，建议使用 `TypedDict` 或 `dataclass` 定义，而非裸 `Dict`。

```python
from typing import TypedDict

class UserProfile(TypedDict):
    id: int
    name: str
    roles: List[str]

def get_user(user_id: int) -> UserProfile:
    ...
```

---

## 4. 文档字符串 (Docstrings)

### 4.1 Google Style
- 所有公共模块、类、函数必须包含 Docstring。
- 采用 **Google Style** 格式，因为它被 LLM 理解得最好。

```python
def fetch_data(url: str, retry: int = 3) -> Optional[bytes]:
    """Fetches data from a URL with retries.

    Args:
        url: The target URL string.
        retry: Max number of retries. Defaults to 3.

    Returns:
        The raw bytes content if successful, None otherwise.

    Raises:
        ConnectionError: If the network is unreachable.
    """
    ...
```

---

## 5. 异常处理 (Error Handling)

### 5.1 精确捕获
- 严禁使用裸 `except:`。
- 捕获特定的异常类型。

```python
# ✅ Good
try:
    result = 1 / x
except ZeroDivisionError:
    logging.error("Cannot divide by zero")

# ❌ Bad
try:
    result = 1 / x
except:
    pass
```

### 5.2 Fail Fast
- 在函数开头进行参数校验（Guard Clauses），尽早返回或报错，减少缩进层级。

---

## 6. Agent 专属规范 (Agent-Specific)

### 6.1 工具函数设计
- **单一职责**: 一个工具函数只做一件事。
- **JSON 友好**: 输入输出尽量使用 JSON 可序列化的类型 (str, int, float, list, dict)，避免返回复杂的对象实例，除非是为了内部传递。
- **幂等性**: 如果可能，设计成幂等的（重复调用不产生副作用）。

### 6.2 解释性代码
- 关键逻辑步骤必须添加注释。
- 不要写显而易见的注释 (e.g., `i += 1 # Increment i`)。
- **Rationale**: 解释 "为什么" 这样做，而不仅仅是 "做了什么"。

---

## 7. 自我审查清单 (Self-Review Checklist)

Agent 在提交 Python 代码前，必须检查：
- [ ] 命名是否符合 PEP 8？
- [ ] 是否添加了 Type Hints？
- [ ] Docstring 是否完整（包含 Args, Returns）？
- [ ] 异常处理是否安全（无 bare except）？
- [ ] 是否有多余的 print 语句（应使用 logging）？
- [ ] 复杂逻辑是否有注释解释 "Why"？
