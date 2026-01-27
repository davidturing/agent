# 数据库 (Database): 2026 深度洞察

## 1. 2026 技术演进洞察 (Insights)

### 趋势一：数据库变身 AI 平台 (DB4AI)
- 数据库内置向量索引 (Vector Index) 只是标配。
- 更多数据库（如 PostgresML）开始内置 ML 模型推断能力，SQL 语句直接调用 `predict()` 函数，避免数据搬出数据库。

### 趋势二：NewSQL 的全球分布 (Global Distributed)
- 随着出海业务增多，通过 Paxos/Raft 协议实现的全球跨 Region 强一致性数据库成为刚需。
- 业务像使用单机数据库一样使用分布式数据库，无需关心分库分表。

### 趋势三：Serverless Database 普及
- 数据库不再按实例收费，而是按读写单元 (Request Units) 收费。即使 0 流量时也无需支付费用（Scale to Zero）。

---

## 2. 商业案例分析 (Business Cases)

### 金融与银行
1. **DBS Bank**: 核心账务系统下移，从大型机迁移到分布式数据库，实现 99.999% 可用性和弹性扩容。
2. **Nubank**: 基于 Datomic (不可变数据库) 构建核心银行系统，所有交易历史可追溯，轻松回滚错误状态。
3. **微众银行**: 全行核心系统运行在 TiDB/MySQL 分布式架构上，支撑亿级用户，单账户IT成本极低。
4. **Nasdaq**: 交易后处理系统使用云原生数据库，确保数据实时一致性并满足监管留痕要求。
5. **Coinbase**: 使用 MongoDB 存储海量用户交易日志和账户状态，利用其 Flexible Schema 适应快速变化的加密资产类型。

### 互联网与电商
6. **Amazon Prime Day**: DynamoDB 峰值每秒处理 1.26 亿次请求，且延迟保持在个位数毫秒。
7. **Uber**: 自研 Schemaless 数据库 (基于 MySQL)，支撑全球数百万司机和乘客的实时订单状态更新。
8. **Discord**: 从 MongoDB 迁移到 ScyllaDB (C++ Cassandra)，解决了万亿级消息存储的 GC 延迟问题。
9. **Slack**: 使用 Vitess (MySQL 分库分表中间件) 管理庞大的消息存储，实现无限水平扩展。
10. **Figma**: 使用 Postgres 存储复杂的设计文件元数据，通过 RDS 读写分离支撑协作编辑。

### 游戏与社交
11. **Genshin Impact (原神)**: 全球同服架构，使用分布式KV数据库存储玩家实时状态，确保全球玩家延迟体验一致。
12. **Roblox**: 使用 CockroachDB 确保虚拟货币交易的全球强一致性，防止资产复制 bug。
13. **王者荣耀**: 数据库架构支撑每秒千万级并发写入，战绩数据实时落库。
14. **Twitter (X)**: Manhattan 分布式数据库，支撑每天 5 亿条推文的写入和实时 Timeline 拉取。

### 物联网与工业
15. **Tesla Energy**: 使用 TimescaleDB 存储数百万个 Powerwall 和车辆的时序传感器数据。
16. **Bosch**: 工业 4.0 平台使用 InfluxDB 监控工厂设备运行状态，每秒写入数百万数据点。
17. **Maersk**: 全球集装箱追踪系统，使用 NoSQL 数据库记录每个集装箱在不同港口的状态流转。
18. **Peloton**: 使用 DynamoDB 记录用户骑行时的实时心率和输出功率，生成排行榜。

### AI 与新兴
19. **OpenAI**: 使用 Vector Database (如 Pinecone/Milvus) 作为 ChatGPT 的长期记忆存储，实现 Document Retrieval。
20. **Notion**: 使用 Postgres 分片集群存储几十亿个 Block 数据，支撑 Notion AI 的快速响应。

---

## 3. Vendor 与产品能力分析

### 关系型与 NewSQL (Relational & NewSQL)
1. **Oracle Database**: 23ai 版本。依然是企业核心交易系统的最强守门员，Exadata 硬件软硬结合性能无敌。
2. **PostgreSQL**: 开源界的霸主。社区插件生态极其丰富 (PostGIS, Timescale, pgvector)。
3. **MySQL (Oracle)**: Web 应用的默认选择。HeatWave 引擎让其具备了强大的实时分析能力。
4. **CockroachDB**: 云原生分布式 SQL 数据库。号称 "永不宕机" (Survive disk, machine, rack, and datacenter failures)。
5. **TiDB (PingCAP)**: HTAP 数据库代表。既能跑高并发交易，又能跑实时复杂分析，MySQL 协议兼容。
6. **YugabyteDB**: 基于 PG 协议的分布式数据库。兼容 PostgreSQL 的所有特性，同时具备 Spanner 的水平扩展能力。
7. **OceanBase (Aliyun)**: 金融级分布式数据库。连续多年刷新 TPC-C 测试记录，适合核心账务场景。
8. **Spanner (Google)**: 全球分布式数据库的鼻祖。利用原子钟 (TrueTime) 实现全球外部一致性。
9. **Aurora (AWS)**: 云原生数据库的定义者。存算分离，日志即数据库，1/10 的成本提供商业数据库的性能。
10. **PolarDB (Aliyun)**: 阿里云自研云原生数据库。一写多读，Serverless 极致弹性。

### NoSQL (Document, Key-Value, Wide-Column)
11. **MongoDB**: 文档数据库事实标准。Atlas 平台提供了 Search, Charts, Mobile 同步等全栈数据服务。
12. **Redis**: 内存数据库事实标准。Redis Stack 增加了 Search, JSON, Graph, TimeSeries 等模块。
13. **DynamoDB (AWS)**: 极致的 Serverless KV 数据库。能够处理任何规模的吞吐量，Consistent single-digit millisecond latency。
14. **Cassandra**: 宽表列式数据库。写入性能极强，适合写多读少的日志/IoT 场景。Datastax 提供商业化支持。
15. **ScyllaDB**: C++ 重写的 Cassandra。号称性能是 Cassandra 的 10 倍，延迟更低。
16. **Couchbase**: 结合了 KV 的性能和 Document 的灵活性的分布式数据库，自带缓存层。
17. **HBase**: Hadoop 生态的 KV 数据库。适合存储海量稀疏数据。

### 时序数据库 (Time-Series)
18. **InfluxDB**: 时序数据库最流行的选择。Flux 查询语言专为时序分析设计。
19. **TimescaleDB**: 基于 PG 的时序数据库。让用户用 SQL 就能查询海量时序数据，兼具关系型数据的关联能力。
20. **TDengine**: 国产时序数据库新星。针对物联网场景深度优化，写入压缩比极高。
21. **QuestDB**: 追求极致写入性能的开源时序数据库，适合高频交易场景。

### 向量数据库 (Vector Databases)
22. **Pinecone**: 全托管向量数据库，Serverless 架构，开发者体验极佳，OpenAI 官方 Demo 常客。
23. **Milvus (Zilliz)**: 功能最全面的开源向量数据库。支持混合搜索，标量过滤性能强。
24. **Weaviate**: AI 原生的向量数据库。内置了模块化架构，可以直接在数据库层面集成 LLM。
25. **Qdrant**: Rust 编写的高性能向量搜索引擎，资源占用少，适合边缘侧部署。
26. **Chroma**: 轻量级向量数据库，专为开发者设计，简单易用，Python 生态集成度高。

### 图数据库 (Graph Databases)
27. **Neo4j**: 图数据库的市场领导者。Cypher 查询语言是图查询的事实标准。Graph Data Science 库强大。
28. **TigerGraph**: 原生并行图数据库。能够处理万亿级大图的深度多跳查询。
29. **NebulaGraph**: 针对海量数据设计的高性能开源分布式图数据库。

---

## 4. 概念索引 (Index)

- **[HTAP]**: Hybrid Transactional/Analytical Processing，一套系统同时搞定交易和分析。
- **[Vector Database]**: 专为存储和检索向量 Embedding 设计的数据库（如 Pinecone, Milvus），是 LLM 记忆的载体。
- **[ACID]**: 事务的四大特性：原子性、一致性、隔离性、持久性。
- **[Sharding]**: 分片，将大数据集水平切分到多个节点存储。
- **[Consistency Models]**: 一致性模型，如强一致性、最终一致性、因果一致性。
- **[WAL (Write-Ahead Logging)]**: 预写日志，数据库实现持久性和原子性的关键技术。
- **[MVCC]**: 多版本并发控制，允许读写操作不冲突，提高并发性能。
- **[LSM-Tree]**: Log-Structured Merge-Tree，针对写入优化的数据结构，大多数 NoSQL 数据库的底层存储。
- **[B+ Tree]**: 针对读取优化的数据结构，大多数关系型数据库的底层索引。
