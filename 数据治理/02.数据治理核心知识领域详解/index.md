# 📘 02. 数据治理核心知识领域详解 (Key Knowledge Areas)

## 🏙️ 1. 业界背景与领域细分

数据治理并非铁板一块，而是由多个相互依赖的专业领域组成的复杂机器。在 DAMA 定义的 11 个领域中，并非所有领域权重都一样。对于大多数企业而言，存在所谓的“四大金刚”：

1.  **数据架构 (Data Architecture)**: 类似城市的规划图，决定了数据流动的骨架。
2.  **数据质量 (Data Quality)**: 类似城市的水质监测，确保流淌（流动）的是净水而非污水。
3.  **数据安全 (Data Security)**: 类似城市的防御系统，防止数据泄露或被非法访问。
4.  **元数据 (Metadata)**: 类似城市的地图和索引，没有它，谁也找不到数据在哪里。

### 趋势分析
*   **传统视角**: 侧重于“数据建模”和“数据库设计”。
*   **现代视角**: 侧重于 **DataOps (数据开发运营一体化)** 和 **Data Fabric (数据编织)**。架构更加灵活（Schema-on-Read），质量管控更加自动化。

---

## 🎯 2. 本章课题描述 (Chapter Objectives)

本章不追求对 DMBOK 的面面俱到，而是挑选企业实施中**最痛、最难、最关键**的四个领域进行深度剖析。

**核心课题**:
1.  **架构治理**: 如何打破“数据孤岛”？如何设计 Master Data Management (MDM) 主数据系统？
2.  **质量攻坚**: 建立“六性”评估标准（完整性、准确性等），并构建闭环改进机制。
3.  **安全合规**: 在 GDPR/PIPL 严监管环境下，如何做好数据分级分类与隐私保护。
4.  **元数据驱动**: 如何利用 Data Lineage (血缘分析) 自动化追踪数据链路。

---

## 🏗️ 3. 整体知识框架 (Overall Framework)

本章的知识拓扑结构如下：

```mermaid
graph LR
    Core[核心知识领域] --> Arch(2.1 数据架构)
    Core --> Quality(2.2 数据质量)
    Core --> Security(2.3 数据安全)
    Core --> Integration(2.4 集成与互操作)
    
    Arch --> MDM[主数据 MDM]
    Arch --> Model[数据建模]
    
    Quality --> Profile[数据探查]
    Quality --> Clean[清洗规则]
    
    Security --> IAM[身份认证]
    Security --> Encrypt[脱敏加密]
```

### 3.1 关键领域对照表

| 领域 | 核心产出物 (Deliverables) | 典型工具 (Tools) | 常见挑战 |
| :--- | :--- | :--- | :--- |
| **数据架构** | 企业数据模型 (EDM)、数据流图 | PowerDesigner, ER/Studio | 业务变更快，模型跟不上 |
| **数据质量** | 质量检核报告 (DQC Report) | Informatica DQ, Apache Griffin | 发现问题容易，根因解决难 |
| **数据安全** | 分级分类清单、脱敏策略 | Ranger, Kerberos | 业务便利性与安全的平衡 |

---

## 🧭 4. 目录导航 (Section Navigation)

*   [2.1-数据架构管理](./2.1-%E6%95%B0%E6%8D%AE%E6%9E%B6%E6%9E%84%E7%AE%A1%E7%90%86.md)
    *   _Note: 重点掌握纵向的“业务-逻辑-物理”三层架构，以及横向的中台化架构设计。_
*   [2.2-数据质量管理](./2.2-%E6%95%B0%E6%8D%AE%E8%B4%A8%E9%87%8F%E7%AE%A1%E7%90%86.md)
    *   _Note: 所谓“垃圾进垃圾出 (GIGO)”，本节提供了一套完整的“清洗-监控-评估”实战方案。_
*   [2.3-数据安全与合规管理](./2.3-%E6%95%B0%E6%8D%AE%E5%AE%89%E5%85%A8%E4%B8%8E%E5%90%88%E8%A7%84%E7%AE%A1%E7%90%86.md)
    *   _Note: 涉及 GDPR、CCPA 及中国《数据安全法》的合规落地策略。_
*   [2.4-其他关键知识领域](./2.4-%E5%85%B6%E4%BB%96%E5%85%B3%E9%94%AE%E7%9F%A5%E8%AF%86%E9%A2%86%E5%9F%9F.md)
    *   _Note: 涵盖数据集成 (ETL/ELT)、文件与内容管理等补充领域。_

---



## ❓ 5. 常见问题 (FAQ)
### Q1: 到底什么是主数据（MDM）？
**A:** 解决多系统间“共用实体”（如客户、产品）信息不一致的问题。MDM 是企业的“Single Source of Truth”。
### Q2: 质量问题为何难改？
**A:** 通常因为“责权分离”。录入者（如客服）只背“接听量”KPI，不背“地址准确率”KPI，所以没动力改。

---

## 📚 6. 参考文档 (References)

> [!NOTE]
> 本列表收录了该领域的核心文献。您可以点击链接购买书籍或查看原文。

| 标题 (Title) | 作者 (Author) | 日期 (Date) | 链接 (Link) | 简介 (Summary) |
| :--- | :--- | :--- | :--- | :--- |
| Master Data Management | David Loshin | 2008 | [Amazon](https://www.amazon.com/Master-Data-Management-David-Loshin/dp/0123742250) | MDM 经典。 |
| The Data Warehouse Toolkit | Ralph Kimball | 2013 | [Wiley](https://www.wiley.com/en-us/The+Data+Warehouse+Toolkit) | 维度建模圣经。 |
| Apache Atlas | Apache | 2023 | [Official](https://atlas.apache.org/) | 开源元数据治理。 |
| Six Primary Dimensions for DQ | DAMA UK | 2013 | [DAMA UK](https://damauk.org/) | 六大质量维度定义。 |
| Building the Data Warehouse | Inmon | 2005 | [Amazon](https://www.amazon.com/Building-Data-Warehouse-W-Inmon/dp/0764599445) | 范式建模。 |
| Data Lineage Benefits | Octopai | 2021 | [Blog](https://octopai.com/blog/data-lineage/) | 血缘分析价值。 |
| NIST Privacy Framework | NIST | 2020 | [NIST](https://www.nist.gov/privacy-framework) | 隐私框架。 |
| Metadata Maturity | Dataversity | 2018 | [Article](https://www.dataversity.net/) | 元数据成熟度。 |
| Informatica MDM | Informatica | 2023 | [Product](https://www.informatica.com/products/master-data-management.html) | 商业 MDM。 |
| Data Fabric Architecture | Gartner | 2022 | [Gartner](https://www.gartner.com/) | 数据编织报告。 |

## 📝 7. 章节测验 (Quiz)

### 7.1 第一部分：判断题 (True/False)
1. **[判断]** 主数据体量通常远大于交易数据。
    * ( ) 对
    * ( ) 错

2. **[判断]** 质量清洗最好在报表端进行。
    * ( ) 对
    * ( ) 错

3. **[判断]** 元数据也描述业务属性。
    * ( ) 对
    * ( ) 错

4. **[判断]** 维度表通常存储环境上下文。
    * ( ) 对
    * ( ) 错

### 7.2 第二部分：选择题 (Multiple Choice)
5. **[单选]** 哪个最适合做主数据？
    * A. 点击日志
    * B. 员工名录
    * C. 每日库存
    * D. CPU监控

6. **[单选]** 日期为'2月30日'属于？
    * A. 唯一性
    * B. 及时性
    * C. 完整性
    * D. 有效性

7. **[单选]** Kimball 核心模型？
    * A. 星型模型
    * B. 3NF
    * C. Data Vault
    * D. NoSQL

8. **[多选]** 元数据用途？
    * A. 影响性分析
    * B. 搜索资产
    * C. 理解术语
    * D. 自动写代码

9. **[单选]** 脱敏是为了？
    * A. 压缩
    * B. 隐私保护
    * C. 加速
    * D. 纠错

---
<div style="page-break-after: always;"></div>

### 7.3 答案与解析 (Answers & Analysis)

1. **错**。解析：交易数据量大，主数据量小且稳定。
2. **错**。解析：应在源头或数仓层清洗，报表端清洗会导致逻辑不一致。
3. **对**。解析：元数据包含业务、技术、操作三类。
4. **对**。解析：事实表存数据，维度表存环境。
5. **B**。解析：员工是核心实体，高复用。
6. **D**。解析：逻辑无效。
7. **A**。解析：星型模型是 Kimball 标志。
8. **ABC**。解析：D 不是核心用途。
9. **B**。解析：Masking 保护敏感信息。
