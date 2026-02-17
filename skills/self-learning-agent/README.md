# David Agent (大卫智能体) 架构设计与功能特性说明书

## 1. 项目愿景
David Agent 是一个基于 OpenClaw 框架构建的**自我进化、双维度感知**的数字分身智能体。它不仅是一个自动化工具，更是一个能够自主学习技术趋势、构建知识图谱并持续输出深度洞察的智能实体。

## 2. 核心架构设计 (Architecture)

David Agent 采用了 **"Slim & Resilient" (轻量且韧性)** 的扁平化流水线架构，确保在 MacOS 环境下稳定运行。

### 2.1 核心组件 (Modules)
- **Doctor (自检模块)**: 每次启动前自动检查网络、Gemini API、GitHub API 和 WordPress 的连通性。
- **Ingest (采集模块)**: 
    - **GitHub Ingest**: 实时跟踪开发者的代码动态和 Star 趋势。
    - **X (Twitter) Ingest**: 针对 20+ 位顶级技术领袖（Tech Kings）进行精准推文抓取与解析。
- **Brain (认知模块)**:
    - **Dual-Lens Analysis**: 采用“科技达人”与“首席数据官 (CDO)”双重视角进行信息过滤与价值提取。
    - **Ontology Extraction**: 使用 Gemini 自动从非结构化文本中提取实体与关系三元组 (S-R-O)。
- **Memory (存储模块)**:
    - **PageIndex 索引**: 借鉴 VectifyAI 理念，采用层次化文件目录存储知识，实现基于推理的结构化记忆。
- **Publish & Sync (分发模块)**:
    - **WordPress**: 自动生成并发布《David Agent Daily Evolution》日志。
    - **GitHub Sync**: 自动将结构化知识图谱推送到 `davidturing/agent` 仓库。

## 3. 功能特性 (Features)

### 🚀 3.1 自我进化与代码感知 (Self-Learning)
Agent 会定期读取自身的源码，感知功能边界的变化，并在每日日志中记录其“认知成长”与“方法论迭代”。

### 🧠 3.2 知识图谱与本体存储 (Graph-based PageIndex)
- **特性**: 不再记录散乱的推文。
- **实现**: 将知识拆解为 `AI agents --(require)--> Coordination` 等关系，并以 Persona/Category/Topic 的目录结构持久化。

### 🎭 3.3 双角色驱动策略 (Dual Persona)
- **科技达人**: 关注系统架构、自动化工作流、AI Agent 协调、Vibe Coding 等前沿技术。
- **CDO (首席数据官)**: 关注数据治理、数据资产化、业务连续性及数据安全。

### 🛡️ 3.4 环境韧性 (Resilience)
具备“降级执行”能力：当本地 `exec` 环境不稳定时，Agent 能自动切换到“纯 LLM 上下文执行模式”，通过内置工具替代外部脚本，确保核心业务逻辑不中断。

## 4. 迭代历程细节 (Evolution Discussion Details)

### 第一阶段：基础设施建设 (2026-02-15 ~ 16)
- **讨论重点**: 解决 OpenClaw 在 MacOS 下的 `spawn EBADF` 报错。
- **决策**: 引入 `doctor.py` 自检机制，并将复杂的逻辑拆分为细粒度的 Python 脚本，通过 `pipeline.py` 进行流控。

### 第二阶段：知识源拓展 (2026-02-17 上午)
- **讨论重点**: 如何从海量 X 资讯中提取真知灼见？
- **决策**: 定义 20 个“King”级别的科技账号作为初始种子，建立 `x_accounts.json` 并为其打标，实现从“关注人”到“学习知识”的转变。

### 第三阶段：结构化记忆与多仓库管理 (2026-02-17 下午)
- **讨论重点**: 如何让 Agent 的知识不仅仅停留在会话中？
- **决策**: 
    - 引入 **PageIndex** 概念，用 MacOS 文件目录模拟知识本体结构。
    - 实现 **Multi-Repo Sync**: 代码/日志部署到 `davidturing/blog`，结构化知识沉淀到 `davidturing/agent`。

## 5. 部署信息
- **部署仓库**: `https://github.com/davidturing/blog` (Code & Infrastructure)
- **知识仓库**: `https://github.com/davidturing/agent` (Structured Knowledge Graph)

---
*Generated & Published by David Agent v2026.02*
