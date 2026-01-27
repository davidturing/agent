---
name: Code Quality Review
description: Enforce software development standards (Python & Java) via automated self-review.
---

# Code Quality Review Skill

This skill guides the Agent to perform a rigorous self-review of code before submission or merging. It ensures alignment with the **Smart Agent Software Development Standards**.

## 1. Prerequisites

Before reviewing any code, the Agent **MUST** read the latest version of the relevant specification files located in the Knowledge Base:

- **Python**: [`/智能体/软件开发规范/python_spec.md`](/Users/david/david_project/智能体/软件开发规范/python_spec.md)
- **Java**: [`/智能体/软件开发规范/java_spec.md`](/Users/david/david_project/智能体/软件开发规范/java_spec.md)

## 2. Review Process

For every code file generated or modified, perform the following checks:

### 🐍 Python Checklist
1.  **Type Hints**: Do ALL public functions have type hints? (Use `list[]`, `dict[]`, not `List`, `Dict`).
2.  **Docstrings**: Does every public module/class/function have a Google-style docstring?
3.  **Safety**: Are there any bare `except:` clauses? (Fix them).
4.  **Logging**: Are `print()` statements removed and replaced with `logging`?
5.  **Naming**: Do boolean variables start with `is_`, `has_`, etc.?
6.  **Imports**: Are imports sorted (Std -> Third Party -> Local)?

### ☕ Java Checklist
1.  **Concurrency**: Is `new Thread()` avoided? Are thread pools properly configured (no `Executors.new...`)?
2.  **NPE Prevention**: Do methods return empty collections instead of `null`?
3.  **Log Format**: Is SLF4J `{}` placeholder used?
4.  **Database**: Are `SELECT *` queries avoided? Do money fields use `BigDecimal`?
5.  **Clean Code**: Are magic numbers extracted to constants?

## 3. Output Format

If the Agent detects violations, it must report them in the following format BEFORE making any edits (or fixing them automatically):

```markdown
### 🚨 Code Quality Report

**File**: `filename.py`

| Severity | Issue | Recommendation |
| :--- | :--- | :--- |
| 🔴 High | Bare `except:` found on line 45 | Catch specific exception |
| 🟡 Medium | Missing docstring for `process_data` | Add Google-style docstring |
| 🟢 Low | Import order incorrect | Reorder imports |
```

## 4. Automatic Fixes

If `AutoFix` mode is enabled (or implied), the Agent should proceed to fix **High** and **Medium** severity issues immediately.
