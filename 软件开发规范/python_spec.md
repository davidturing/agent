# Python 软件开发规范 (Enterprise Agent Edition)

**版本**: 3.0 (Deep Dive)  
**生效日期**: 2026-01-27  
**基准**: Google Python Style Guide + PEP 8 + Anthropic Engineering Practices  

本规范旨在建立一套**工业级**的 Python 代码标准，特别针对 Agentic Workflow、异步并发和高可靠性系统进行了深度定制。

---

## 1. 工程结构与配置 (Project Structure & Config)

### 1.1 项目布局 (Layout)
采用标准的 `src` 布局，避免导入混乱。
```text
project_root/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core/       # 核心业务逻辑
│       ├── api/        # 外部接口/路由
│       └── utils/      # 通用工具
├── tests/
│   ├── unit/           # 单元测试
│   └── integration/    # 集成测试
├── pyproject.toml      # 依赖管理与工具配置
├── README.md
└── .gitignore
```

### 1.2 依赖管理 (Dependency Management)
-   **工具**: 推荐使用 `Poetry` 或 `uv` 进行依赖管理。
-   **版本锁定**: 必须提交 `poetry.lock` 或 `uv.lock` 文件，确保环境一致性。
-   **依赖分组**:
    -   `main`: 生产环境依赖 (e.g., `fastapi`, `pydantic`).
    -   `dev`: 开发工具 (e.g., `ruff`, `mypy`).
    -   `test`: 测试框架 (e.g., `pytest`, `pytest-asyncio`).

### 1.3 代码质量像 (Quality Tools)
所有项目必须配置以下工具，并在 CI 中强制执行：
-   **Formatter**: `Ruff` (兼容 Black 风格)。
-   **Linter**: `Ruff` (替代 flake8, isort)。
-   **Type Checker**: `MyPy` (strict mode)。

---

## 2. 核心编码规范 (Core Coding Standards)

### 2.1 类型系统 (Type System) - Strict
-   **全覆盖**: 所有函数必须标注参数和返回值类型。
-   **泛型**: 使用 `typing.TypeVar` 和 `typing.Generic` 增强复用性。
-   **运行时检查**: 推荐使用 `Pydantic` 或 `TypeGuard` 进行运行时数据验证。

```python
from typing import TypeVar, Iterable
from pydantic import BaseModel

T = TypeVar("T")

class User(BaseModel):
    id: int
    name: str

def first(iterable: Iterable[T]) -> T | None:
    """Return the first element of an iterable or None."""
    for item in iterable:
        return item
    return None
```

### 2.2 异步编程 (Asyncio)
Agent 系统通常是 I/O 密集型的（LLM API 调用），必须拥抱 `asyncio`。

-   **命名**: 异步函数不需要特殊前缀，但必须在 docstring 中注明。
-   **并发控制**: 使用 `asyncio.gather` 或 `asyncio.TaskGroup` (Python 3.11+) 管理并发。
-   **严禁阻塞**: 异步函数中严禁调用同步阻塞 I/O (如 `requests.get`, `time.sleep`)。必须使用 `httpx`, `aiofiles` 或 `asyncio.sleep`。

```python
import asyncio
from httpx import AsyncClient

async def fetch_urls(urls: list[str]) -> list[str]:
    async with AsyncClient() as client:
        # ✅ Good: 使用 TaskGroup 结构化并发
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(client.get(url)) for url in urls]
        
        return [t.result().text for t in tasks]
```

### 2.3 错误处理 (Error Handling) - Defensive
-   **自定义异常**: 业务模块必须定义基类异常 `AppError`。
-   **异常链**: 使用 `raise NewException from e` 保留原始堆栈。
-   **原子性**: 在执行不可逆操作前（如写 DB），确保所有前置检查已通过。

---

## 3. Agent 专属架构模式 (Agent Patterns)

### 3.1 工具接口设计 (Tool Implementation)
Agent 调用的 Tool 必须遵循 "幂等" 和 "容错" 原则。

-   **入参扁平化**: 避免嵌套 JSON，尽量使用扁平参数，减少 LLM 幻觉。
-   **结果结构化**: 返回 `ToolResult` 对象，而非纯字符串。

```python
@dataclass
class ToolResult:
    success: bool
    output: str  # 给 LLM 看的内容
    data: dict   # 给程序读的结构化数据
    error: str | None = None
```

### 3.2 提示词工程代码化 (Prompt as Code)
-   **模版分离**: Prompt 模版应存储在独立文件或配置中，不应硬编码在 Python 逻辑里。
-   **版本控制**: Prompt 的变更等同于代码变更，需要 Git 记录。
-   **动态注入**: 使用 `jinja2` 进行复杂的 Prompt 渲染。

---

## 4. 测试规范 (Testing Guidelines)

### 4.1 Pytest 优先
-   **Fixtures**: 使用 `conftest.py` 管理共享资源（如 Mock DB, Mock LLM）。
-   **Parametrization**: 使用 `@pytest.mark.parametrize` 覆盖边界条件。

### 4.2 Mocking 策略
-   **外部服务**: 严禁在单元测试中调用真实 API (OpenAI, Database)。必须使用 `respx` (HTTP mock) 或 `unittest.mock`。
-   **确定性**: 测试必须是确定性的。对于涉及 LLM 的测试，Mock 其输出或使用 "Evaluation" 层进行语义断言。

```python
import pytest
from unittest.mock import MagicMock

def test_agent_decision(mock_llm):
    mock_llm.return_value = "Order confirmed"
    agent = Agent(llm=mock_llm)
    assert agent.run("Buy it") == "Order confirmed"
```

---

## 5. 安全性 (Security)

### 5.1 敏感信息
-   **ENV**: 密钥必须通过环境变量 (`os.getenv`) 读取，严禁硬编码。
-   **Log Redaction**: 日志中必须脱敏 PII (个人隐私信息) 和 API Keys。

### 5.2 注入防护
-   **SQL**: 使用 ORM (SQLAlchemy) 或参数化查询，严禁 f-string 拼 SQL。
-   **XML/YAML**: 使用 `defusedxml` 和 `yaml.safe_load` 防止反序列化攻击。
-   **Command**: 慎用 `subprocess.run(shell=True)`，尽量使用列表参数形式。
