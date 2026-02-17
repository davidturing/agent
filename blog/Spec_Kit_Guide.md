# GitHub Spec Kit 使用指南：开启 Spec 驱动编程新时代

![Spec-Driven Development Concept](https://image.pollinations.ai/prompt/A%20futuristic%20developer%20workspace%20with%20holographic%20specifications%20transforming%20into%20clean%20code%20blocks,%20blue%20and%20purple%20neon%20lighting,%20cyberpunk%20style?width=1024&height=576&nologo=true)

**发布时间**：2026年2月4日
**来源**：[GitHub - spec-kit](https://github.com/github/spec-kit)

---

## 1. 什么是 Spec？为什么我们需要 Spec 驱动编程？

### 核心概念
**Spec (Specification，规格说明书)** 在传统软件开发中往往是一份被束之高阁的文档。但在 AI 辅助编程时代，**Spec 是连接人类意图与 AI 执行力的桥梁**。

**Spec-Driven Development (SDD, 规格驱动开发)** 是一种反直觉的开发模式。它不再让你直接跳进代码的海洋里“凭感觉编程” (Vibe Coding)，而是要求你先写下**可执行的规格说明**。

### 为什么选择 Spec 驱动？
在没有 Spec 的情况下，直接让 AI 写代码就像让建筑工人在没有蓝图的情况下盖房子——即使每一块砖都砌得很直，最后的大楼也可能是歪的。

**Spec 驱动的优势：**
1.  **意图对齐**：通过自然语言清晰定义“做什么” (What) 和“为什么做” (Why)，而不是陷入“怎么实现” (How) 的细节泥潭。
2.  **减少幻觉**：详细的 Spec 为 AI 提供了上下文围栏，大幅减少 AI 生成无用或错误代码的概率。
3.  **可迭代性**：Spec 是活的文档。当需求变更时，你修改 Spec，AI 重新生成代码，而不是手动去修补千疮百孔的代码库。

> *"Don't vibe code. Spec code." —— 告别随性编程，拥抱规格驱动。*

---

## 2. Spec Kit 快速上手指南

GitHub 推出的 `spec-kit` 是一个开源工具包，旨在帮助开发者快速实践 Spec 驱动开发。它提供了一套 CLI 工具和标准化的工作流。

### 🛠️ 安装步骤

首先，确保你的环境中安装了 `uv` (Python 包管理器) 和 `git`。

**推荐安装方式（持久化安装）：**
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

安装完成后，你可以通过 `specify` 命令来调用工具。

### 🚀 常用命令 (Command)

Spec Kit 的工作流分为几个标准阶段，每个阶段都有对应的 Slash Command（在 AI 助手如 Claude Code, Cursor 中使用）：

#### 1. 初始化项目
在你的项目根目录下运行：
```bash
# 初始化并指定 AI 助手（例如 Claude）
specify init . --ai claude
```
这将生成 `.specify` 目录，包含必要的模板和脚本。

#### 2. 制定宪法 (Constitution)
这是项目的“最高法则”。定义代码风格、测试标准和架构原则。
```bash
/speckit.constitution 创建一个专注于高性能、TypeScript 严格模式和 100% 测试覆盖率的宪法。
```

#### 3. 编写规格 (Specify)
描述你要构建的功能，专注于业务逻辑。
```bash
/speckit.specify 构建一个基于 React 的看板应用，支持拖拽排序，数据存储在本地 SQLite 中。
```

#### 4. 技术规划 (Plan)
制定技术实现方案，选择技术栈。
```bash
/speckit.plan 使用 Vite + React + TailwindCSS 实现前端，后端使用 Python FastAPI。
```

#### 5. 任务拆解 (Tasks)
将计划自动拆解为可执行的步骤。
```bash
/speckit.tasks
```

#### 6. 执行实现 (Implement)
AI 自动执行上述任务，生成代码。
```bash
/speckit.implement
```

---

## 3. 总结

Spec Kit 不是要取代开发者，而是要升级开发者。它将我们从“代码工人”升级为“软件架构师”。通过掌握 Spec 驱动编程，你将能以惊人的速度构建高质量、易维护的软件系统。

---
*本文由 Spec Kit 爱好者整理发布。*
