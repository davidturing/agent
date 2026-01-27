# 数据安全 (Data Security): 2026 深度洞察

## 1. 2026 技术演进洞察 (Insights)

### 趋势一：针对 AI 的安全 (Security for AI)
- 传统的 DLP (防泄露) 无法阻止员工把涉密数据粘贴给 ChatGPT。
- 新通过 **LLM Firewall** 技术，检测 Prompt 中的敏感信息和 PII，并检测 Model Response 中的有害内容。

### 趋势二：隐私计算落地 (Privacy Computing)
- **MPC (多方安全计算)** 和 **TEE (可信执行环境)** 性能大幅提升。
- 企业之间可以在 "不泄露原始数据" 的前提下，共同进行联合建模（如银行与运营商联合反诈）。

---

## 2. Vendor 与产品能力分析

| Vendor | 核心产品 | 2026 核心能力评价 |
| :--- | :--- | :--- |
| **Zscaler** | Zscaler Data Protection | SSE (Security Service Edge) 架构的领跑者。将安全检查推送到网络边缘。 |
| **Immuta** | Data Security Platform | 专注于数据访问控制。能够细粒度地控制 "谁" 在 "什么目的" 下能看到 "哪行哪列" 数据。 |
| **BigID** | BigID | 极其强大的数据发现能力。能从海量非结构化数据中扫描出 "疑似敏感" 数据。 |

---

## 3. 概念索引 (Index)

- **[Zero Trust]**: 零信任架构，"Never Trust, Always Verify"。不因为你在内网就信任你。
- **[DLP (Data Loss Prevention)]**: 数据防泄露系统。
- **[Encryption at Rest/in Transit]**: 静态加密（存盘时）和传输中加密（网络传输时）。
- **[Prompt Injection]**: 提示词注入攻击，通过精心设计的 Prompt 诱导 LLM 绕过安全限制输出有害内容。
