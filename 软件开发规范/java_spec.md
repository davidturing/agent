# Java 软件开发规范 (Enterprise Agent Edition)

**版本**: 2.0  
**生效日期**: 2026-01-27  
**基准**: Alibaba Java Coding Guidelines + Google Java Style  

本规范旨在定义 Java 项目在架构设计、并发处理、数据库交互及异常与日志方面的严格标准。

---

## 1. 命名与代码风格 (Naming & Style)

### 1.1 命名规约
| 类型 | 规则 | 示例 | 说明 |
| :--- | :--- | :--- | :--- |
| **Class** | `UpperCamelCase` | `UserLoginController` | 名词，领域模型清晰 |
| **Method** | `lowerCamelCase` | `listActiveUsers` | 动词开头 |
| **Constant** | `UPPER_CASE` | `MAX_RETRY_COUNT` | 必须 `static final` |
| **Package** | `lowercase` | `com.company.module.biz` | 单数形式，点分隔 |
| **Enum** | `UpperCamelCase` | `PaymentStatusEnum` | 必须以 Enum 后缀结尾 |
| **Impl** | `Impl` Suffix | `UserServiceImpl` | 接口实现类 |

### 1.2 POJO 规范 (Data Objects)
-   **DO/DTO/VO**: 严格区分各层数据对象。
    -   `DO (Data Object)`: 与数据库表一一对应。
    -   `DTO (Data Transfer Object)`: RPC/Service 层传输。
    -   `VO (View Object)`: 前端展示。
-   **No `is` Prefix**: Boolean 类型的属性名禁止加 `is` 前缀 (如 `isSuccess`)，防止 RPC 框架序列化异常。
-   **Lombok**: 推荐使用 `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor` 减少样板代码。

---

## 2. 并发处理 (Concurrency)

### 2.1 线程池 (Thread Pools)
-   **严禁显式创建线程**: 禁止 `new Thread()`。必须通过线程池管理并发。
-   **自定义线程池**: 严禁使用 `Executors.newFixedThreadPool` 等静态方法（避免 OOM）。必须使用 `ThreadPoolExecutor` 构造函数，明确指定：
    -   `corePoolSize` / `maximumPoolSize`
    -   `ArrayBlockingQueue` (有界队列)
    -   `ThreadFactory` (必须给线程命名，如 "order-process-pool-%d")
    -   `RejectedExecutionHandler` (拒绝策略)

### 2.2 线程安全
-   **SimpleDateFormat**: 线程不安全，禁止定义为 static 变量。推荐使用 Java 8 的 `DateTimeFormatter`。
-   **ThreadLocal**:以此传递上下文时，必须遵循 **try-finally** 模式，在 `finally` 块中调用 `remove()` 清理，防止内存泄漏。

---

## 3. 数据库规约 (Database & MySQL)

### 3.1 建表规范
-   **主键**: 必须有 `id` (bigint unsigned)，自增或雪花算法。
-   **必填字段**: `gmt_create` (datetime), `gmt_modified` (datetime).
-   **字段类型**:
    -   **Boolean**: 使用 `tinyint(1)`，0 为 false，1 为 true。
    -   **Money**: 使用 `decimal(10, 2)` 或存储 `bigint` (分)，严禁使用 `double/float`。
-   **索引**:
    -   主键索引: `pk_字段名`
    -   唯一索引: `uk_字段名`
    -   普通索引: `idx_字段名`

### 3.2 SQL 规约
-   **禁止 `SELECT *`**: 必须明确指定列名。
-   **禁止隐式转换**: 字符型字段查询时必须加单引号，避免索引失效。
-   **分页查询**: `LIMIT` 偏移量过大时，必须使用 "延迟关联" 或 "ID > X" 的方式优化。

---

## 4. 异常与日志 (Error Handling & Logging)

### 4.1 异常处理体系
-   **分层异常**:
    -   DAO 层抛出框架异常 (SQLException)。
    -   Service 层捕获并抛出 `BusinessException` (包含 ErrorCode)。
    -   Web/Controller 层统一捕获，封装为 `Result<T>` 返回。
-   **禁止吞异常**: `catch` 块中必须处理或记录日志 (`log.error("msg", e)`), 严禁空 `catch`。

### 4.2 日志规范 (SLF4J)
-   **日志对象**: 使用 `@Slf4j` 或 `private static final Logger log = LoggerFactory.getLogger(Clazz.class);`
-   **占位符**: 使用 `{}` 占位，避免字符串拼接。
    -   ✅ `log.info("Order processed: id={}", orderId);`
-   **日志级别**:
    -   `DEBUG`: 调试信息，生产关闭。
    -   `INFO`: 关键业务状态流转（入参、出参、状态变更）。
    -   `WARN`: 可自愈的异常（如重试）。
    -   `ERROR`: 需要人工介入的系统故障。

---

## 5. 单元测试 (Unit Testing)

### 5.1 准则
-   **AIR 原则**:
    -   **A**utomatic: 全自动运行，无人工干预。
    -   **I**ndependent: 测试用例相互独立，无依赖。
    -   **R**epeatable: 任何环境、任何时间执行结果一致。
-   **Mock**: 外部依赖（DB, Redis, RPC）必须使用 `Mockito` 进行 Mock，只测试核心业务逻辑。

---

## 6. 自我审查清单 (Self-Review Checklist)

Agent 在生成/提交代码前，必须回答：
- [ ] 线程池是否使用了有界队列并自定义了名称？
- [ ] 数据库查询是否避免了 `SELECT *` 和全表扫描？
- [ ] 所有的 Money 类型是否避免了浮点数精度问题？
- [ ] 所有的 DTO/POJO 是否区分明确？
- [ ] 是否处理了所有的 Checked Exception？
- [ ] 日志是否包含了上下文 ID (TraceId) 和异常堆栈？
