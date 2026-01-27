# Java 软件开发规范 (Agent-Ready Edition)

本规范基于 **阿里巴巴 Java 开发手册 (Alibaba Java Coding Guidelines)** 和 **Google Java Style Guide**，旨在为 Agent 提供生成高质量、企业级 Java 代码的标准。

## 1. 命名规范 (Naming Conventions)

### 1.1 基础规则
- **类名 (Class)**: `UpperCamelCase` (PascalCase)。
    - ✅ `UserLoginController`
    - ❌ `userLoginController`
- **方法名 (Method)**: `lowerCamelCase`。
    - ✅ `getUserId()`
    - ❌ `GetUserId()`
- **变量名 (Variable)**: `lowerCamelCase`。
- **常量 (Constant)**: `UPPER_CASE_UNDERSCORE`。
    - ✅ `MAX_STOCK_COUNT`
- **包名 (Package)**: 全小写，点分隔，单数形式。
    - ✅ `com.alibaba.mop.user.dto`
- **实现类**: 接口名 + `Impl` 后缀。
    - ✅ `UserServiceImpl` 实现 `UserService`

### 1.2 阿里规范特例
- **POJO 类**: 布尔类型变量 **不要** 加 `is` 前缀，否则部分框架序列化会出错。
    - ✅ `Boolean success;`
    - ❌ `Boolean isSuccess;`
- **Service/DAO 方法命名**:
    - 获取单个对象: `get` / `find`
    - 获取列表: `list`
    - 统计: `count`
    - 插入: `save` / `insert`
    - 删除: `remove` / `delete`
    - 修改: `update`

---

## 2. OOP 规约 (Object Oriented Programming)

### 2.1 封装与继承
- **组合优于继承**: 优先通过组合 (Composition) 复用代码，避免过深的继承链。
- **接口编程**: 依赖于接口而非具体实现类 (Dependency Inversion Principle)。
- **工具类**: 工具类构造函数必须私有化，禁止实例化。

### 2.2 实体类 (POJO)
- 必须重写 `toString()` 方法（推荐使用 Lombok `@ToString`），便于日志排查。
- 相同属性的拷贝必须使用 `BeanUtils` 或 MapStruct，禁止大量 Getter/Setter 手写赋值。

---

## 3. 集合处理 (Collections)

### 3.1 泛型与初始化
- 严禁使用原生类型 (Raw Types)，必须指定泛型。
    - ✅ `List<String> list = new ArrayList<>();`
    - ❌ `List list = new ArrayList();`
- 集合初始化时，如果可预估大小，必须指定容量，减少扩容开销。
    - `Map<String, Object> map = new HashMap<>(16);`

### 3.2 空指针保护 (NPE)
- 此规约极其重要：**返回列表的方法，禁止返回 null，必须返回空集合** (`Collections.emptyList()`)。
- 判空推荐使用 `Optional` 或 `org.apache.commons.lang3.StringUtils`。

---

## 4. 异常与日志 (Exception & Logging)

### 4.1 异常处理
- **Checked vs Unchecked**: 推荐优先使用 RuntimeException (Unchecked)，避免代码中充斥大量的 try-catch 样板代码。
- **分层异常**: DAO 层异常不应抛给 Web 层，应在 Service 层转换为业务异常 (BusinessException)。
- **禁止吞掉异常**: catch 块中必须处理或 log 异常，严禁 `catch (Exception e) {}`。

### 4.2 日志规约 (SLF4J)
- 必须使用 SLF4J 接口，禁止直接使用 Log4j/Logback API。
- 日志通过 Lombok `@Slf4j` 注解获取。
- **格式**: `log.error("Processing failed, id: {}", id, e);`（注意 e 在最后，不需要占位符）。

---

## 5. 控制语句 (Control Statements)

### 5.1 卫语句 (Guard Clauses)
- 优先判断非法条件并 return，减少 `else` 嵌套。

```java
// ✅ Good
if (param == null) {
    return;
}
doSomething();

// ❌ Bad
if (param != null) {
    doSomething();
}
```

### 5.2 魔法值
- 代码中禁止出现从未预定义的常量（魔法值）。必须提取为 `static final` 常量或 `Enum`。

---

## 6. Agent 专属规范 (Agent-Specific)

### 6.1 工具接口设计
- **DTO 模式**: Agent 调用的工具方法，入参建议封装为 DTO (Data Transfer Object)，而不是长参数列表。
- **JSON 序列化**: 确保所有 DTO 都有默认构造函数，且字段名与 JSON key 一致，方便 LLM 理解和构造。

### 6.2 注释与 Prompt
- 核心业务逻辑必须有 Javadoc (`/** ... */`)。
- 接口方法的 Javadoc 应当清晰描述 "What it does" 和 "Side Effects"，因为这些描述会被提取为 Tool Definitions 给 LLM 看。

---

## 7. 自我审查清单 (Self-Review Checklist)

Agent 在提交 Java 代码前，必须检查：
- [ ] 命名符合驼峰式，POJO 布尔值无 is 前缀？
- [ ] 集合无论何时都不返回 null？
- [ ] 是否消灭了魔法值？
- [ ] 异常是否被正确记录或抛出？
- [ ] 是否使用了 SLF4J 占位符记录日志？
- [ ] 核心类和接口是否有清晰的 Javadoc？
