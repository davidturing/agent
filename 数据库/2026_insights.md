# 数据库 (Database): 2026 深度洞察

## 1. 2026 技术演进洞察 (Insights)

### 趋势一：数据库变身 AI 平台 (DB4AI)
- 数据库内置向量索引 (Vector Index) 只是标配。
- 更多数据库（如 PostgresML）开始内置 ML 模型推断能力，SQL 语句直接调用 `predict()` 函数，避免数据搬出数据库。

### 趋势二：NewSQL 的全球分布 (Global Distributed)
- 随着出海业务增多，通过 Paxos/Raft 协议实现的全球跨 Region 强一致性数据库成为刚需。
- 业务像使用单机数据库一样使用分布式数据库，无需关心分库分表。

---

## 2. Vendor 与产品能力分析

| Vendor | 核心产品 | 2026 核心能力评价 |
| :--- | :--- | :--- |
| **PostgreSQL** | PG 18 | "数据库界的 Linux"。扩展插件生态 (pgvector, TimescaleDB) 让它能做任何事，从 OLTP 到 OLAP 再到 Vector。 |
| **MongoDB** | MongoDB Atlas | 依然是文档型数据库首选。在非结构化数据激增的 AI 时代，Schema-less 的优势更加明显。 |
| **TiDB (PingCAP)** | TiDB Cloud | HTAP (混合负载) 的佼佼者。Serverless 架构和对 MySQL 的完美兼容性是其杀手锏。 |
| **Redis** | Redis 8 | 不仅仅是缓存。Flash 存储分层让其成为高性能的主数据库。多线程架构大大提升了吞吐。 |

---

## 3. 概念索引 (Index)

- **[HTAP]**: Hybrid Transactional/Analytical Processing，一套系统同时搞定交易和分析。
- **[Vector Database]**: 专为存储和检索向量 Embedding 设计的数据库（如 Pinecone, Milvus），是 LLM 记忆的载体。
- **[ACID]**: 事务的四大特性：原子性、一致性、隔离性、持久性。
- **[Sharding]**: 分片，将大数据集水平切分到多个节点存储。
