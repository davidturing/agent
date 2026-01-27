# Java 软件开发规范 (Enterprise Agent Edition)

**版本**: 3.0 (Deep Dive)  
**生效日期**: 2026-01-27  
**基准**: Alibaba Java Guide + Google Style + Spring Boot Best Practices  

本规范适用于构建**高并发、高可用**的企业级 Java 应用，特别是基于 Spring Boot 生态的微服务和 Agent 后端。

---

## 1. 架构分层规约 (Architecture Layering)

### 1.1 分层模型
严禁跨层调用，必须遵循单向依赖：
1.  **Web 层 (Controller)**: 参数校验、异常捕获、DTO/VO 转换。
2.  **Service 层 (Biz Logic)**: 核心业务逻辑，事务控制，原子服务编排。
3.  **Manager 层 (Option)**: 通用业务处理，对第三方平台 (LLM API) 的封装。
4.  **DAO 层 (Repository)**: 仅负责与存储交互 (CRUD)。

### 1.2 对象模型 (DTO/DO/VO)
-   **DO (Data Object)**: 数据库表映射，字段与 DB 完全一致。
-   **DTO (Data Transfer Object)**: 服务间传输，不暴露 DB 结构，必须实现 `Serializable`。
-   **VO (View Object)**: 返回给前端，隐藏敏感字段 (如 masking 手机号)。
-   **Converter**: 必须使用 `MapStruct` 或 `BeanUtils` 进行对象转换，禁止在业务代码中手动 set 数十个字段。

---

## 2. Spring Boot 最佳实践

### 2.1 依赖注入 (DI)
-   **构造器注入**: 优先使用构造器注入 (Constructor Injection) 而非 `@Autowired` 字段注入。
-   **Lombok**: 配合 `@RequiredArgsConstructor` 实现简洁的构造器注入。

```java
// ✅ Good
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserMapper userMapper; // 自动生成构造函数注入
}
```

### 2.2 统一响应与异常
-   **Global Exception Handler**: 使用 `@RestControllerAdvice` 统一处理异常，返回标准 JSON 结构 (`code`, `msg`, `data`)。
-   **Pre-conditions**: 使用 `Assert` 类进行参数卫语句检查。

```java
Assert.notNull(req.getUserId(), "UserId cannot be null");
```

---

## 3. 并发与分布式 (Concurrency & Distributed)

### 3.1 锁机制
-   **JVM 锁**: 单机环境使用 `ReentrantLock` 或 `synchronized`，但在微服务下几乎无用。
-   **分布式锁**: 必须使用 Redis (Redisson) 或 ZooKeeper。
    -   **锁超时**: 必须设置 Lease Time，防止服务宕机导致死锁。
    -   **加锁粒度**: 仅锁定必要的资源 (e.g., `lock_order_{orderId}`)，禁止锁定全局。

### 3.2 缓存策略 (Cache)
-   **Cache-Aside**: 读：先查缓存，hit 则返回，miss 则查库并回填；写：先更新库，再**删除**缓存 (Double Delete 或 延迟双删)。
-   **穿透/击穿/雪花**: 必须配置 BloomFilter 防止穿透，设置随机过期时间防止雪崩。

### 3.3 异步执行
-   **@Async**: 仅用于非核心路径 (如发送邮件)。必须配置自定义 `TaskExecutor`，禁止使用默认线程池。
-   **MQ**: 核心业务解耦必须使用消息队列 (RocketMQ/Kafka)。发送方必须保证"事务消息"或"本地消息表"以确保最终一致性。

---

## 4. 数据库与事务 (Database & Transaction)

### 4.1 SQL 性能优化
-   **禁止**: `SELECT *`，`COUNT(column)` (使用 `COUNT(*)`), 在索引列上做函数运算。
-   **批量操作**: 插入/更新大量数据时，使用 MyBatis 的 Batch 模式，禁止循环单条插入。
-   **深分页**: 使用 `id > lastId limit N` 替代 `offset M limit N`。

### 4.2 事务控制
-   **@Transactional**: 仅加在 Service 层 public 方法上。
-   **事务粒度**: 事务中严禁进行远程 RPC 调用 (HTTP/Dubbo) 或 复杂耗时计算。这会占用连接池链接。
    -   ✅ 方案: 先做 RPC 获取数据，再开启事务保存数据。
-   **回滚**: 默认只回滚 `RuntimeException`。如需回滚 Check Exception，必须指定 `rollbackFor = Exception.class`。

---

## 5. 稳定性与可观测性 (Reliability & Observability)

### 5.1 熔断与降级
-   调用外部 LLM 或第三方 API 时，必须配置 **Circuit Breaker** (Resilience4j / Sentinel)。
-   超时时间 (Timeout) 必须显式设置，连接超时 (Connect) 通常 < 3s，读取超时 (Read) 视业务而定。

### 5.2 日志规约 (MDC)
-   **TraceId**: 在 Web 过滤器 (Filter) 中生成 UUID 放入 `MDC`，并在所有日志中通过 `%X{traceId}` 输出，实现全链路追踪。
-   **脱敏**: 手机号、身份证、密码在打印日志时必须 Masking (如 `138****0000`)。

---

## 6. JVM 调优简述 (Tuning)
-   **内存**: 堆内存大小 `-Xms` 和 `-Xmx` 设为相同值，避免运行时抖动。
-   **GC**: 推荐使用 G1 GC (JDK 8+) 或 ZGC (JDK 17+)，针对低延迟场景优化。
-   **OOM Dump**: 必须配置 `-XX:+HeapDumpOnOutOfMemoryError`，现场保留证据。

---

## 7. 自我审查清单 (Self-Review Checklist)

Agent 在提交 Java 代码前，必须检查：
- [ ] 事务方法内是否有 RPC 调用？(性能杀手)
- [ ] 分布式锁是否设置了超时时间？
- [ ] Controller 层是否捕获了所有异常并标准化返回？
- [ ] 缓存更新是否采用了"先更库后删缓存"的策略？
- [ ] SQL 是否存在全表扫描风险？
- [ ] 线程池是否自定义了参数，没有使用默认方案？
