
import os

ROOT_DIR = '/Users/david/david_project/智能体/数据治理'

# Helper to format reference table
def format_ref_table(rows):
    header = "| 标题 (Title) | 作者 (Author) | 日期 (Date) | 链接 (Link) | 简介 (Summary) |\n| :--- | :--- | :--- | :--- | :--- |"
    body = "\n".join([f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows])
    return f"{header}\n{body}"

# Helper to format quiz
def format_quiz(questions, answers):
    return f"""# 章节测验 (Chapter Quiz)

## 第一部分：判断题 (True/False)
{questions['tf']}

## 第二部分：选择题 (Multiple Choice)
{questions['mc']}

---
<div style="page-break-after: always;"></div>

## 答案与解析 (Answers & Analysis)

{answers}
"""

CONTENTS = {
    '01': {
        'faq': """# FAQ: 核心概念与理论框架

## Q1: 数据治理项目通常也是“一把手”工程，具体在企业中如何体现？
**A:** 
*   **理论**: 治理需要跨部门协调（协调 IT、业务、法务），只有高层才有此权力。
*   **场景**: 在某大型商业银行，CEO 亲自担任“数据治理委员会”主席，行长任组长。如果不这样，业务部门（信贷部、吸储部）根本不会配合 IT 部门修改数据录入规范。因为修改规范意味着一线柜员的工作量增加。
*   **结论**: 没有“尚方宝剑”，治理寸步难行。

## Q2: 如何区分“业务数据”和“元数据”，能举个例子吗？
**A:**
*   **场景**: 在淘宝购物。
*   **业务数据**: "订单号: 1001, 金额: 50.00, 用户: ZhangSan"。这是实际发生的交易。
*   **元数据**: "订单表 (Order_Table) 有 3 个字段：OrderId (Int), Amount (Decimal), UserId (String)"。这是描述交易的数据。
*   **价值**: 治理通常是对“元数据”进行管理（定义标准），从而间接控制“业务数据”的质量。

## Q3: 初创公司（0-1阶段）如果不做治理，会有什么后果？
**A:**
*   **场景**: 一家电商创业公司，初期为了快，App 端定义的“用户ID”是手机号，后端 ERP 定义的是“邮箱”，物流系统定义的是“自增整数”。
*   **后果**: 当公司发展到 B 轮融资，想做“用户画像”分析复购率时，发现三个系统的数据根本打不通。此时再想统一 ID，需要重构底层代码，成本可能是初期的 100 倍。这被称为“技术债”。""",
        'refs': [
            ("DAMA-DMBOK2: Data Management Body of Knowledge", "DAMA International", "2017", "[Official Site](https://www.dama.org/)", "全球数据管理领域的权威指南（红宝书），定义了 11 个核心知识领域。"),
            ("Data Governance: The Path of Least Resistance", "Robert S. Seiner", "2014", "[Amazon](https://www.amazon.com/Non-Invasive-Data-Governance-Least-Resistance/dp/1935504851)", "提出了'非入侵式'数据治理理念，主张利用现有流程而非建立新官僚体系。"),
            ("The DGI Data Governance Framework", "Data Governance Institute", "2004", "[DGI](http://www.datagovernance.com/the-dgi-framework/)", "早期的经典治理框架，侧重于组织架构和决策模型。"),
            ("ISO/IEC 38500: Corporate Governance of IT", "ISO", "2015", "[ISO](https://www.iso.org/standard/62816.html)", "国际标准，确立了 IT 治理的 EDP 模型 (Evaluate, Direct, Monitor)。"),
            ("What is Data Governance and Why is it Important?", "Google Cloud", "2023", "[Google Cloud](https://cloud.google.com/learn/what-is-data-governance)", "云厂商视角的定义，强调云环境下的安全与合规。"),
            ("The State of Data Governance 2023", "Gartner", "2023", "[Gartner](https://www.gartner.com/)", "年度行业报告，分析了 AB-DG (主动元数据治理) 等新趋势。"),
            ("Does Your Company Have a Data Strategy?", "Harvard Business Review", "2017-05", "[HBR](https://hbr.org/2017/05/whats-your-data-strategy)", "探讨了防御型与进攻型数据战略的选择。"),
            ("Designing Data Governance", "Khatri & Brown", "2010", "CACM", "学术界引用率极高的论文，定义了治理的五个决策领域。"),
            ("Data Governance for the Digital Age", "McKinsey", "2020", "[McKinsey](https://www.mckinsey.com/)", "麦肯锡视野下的数字化转型与治理。"),
            ("华为数据之道", "华为公司数据管理部", "2020", "机械工业出版社", "中国企业数据治理的最佳实践参考，详解'五维'治理体系。"),
            ("Data Governance Maturity Model", "IBM", "2007", "[IBM](https://www.ibm.com/)", "IBM 提出的成熟度模型，分为初始级到优化级 5 个阶段。"),
            ("Ten Steps to Quality Data", "Danette McGilvray", "2008", "Morgan Kaufmann", "实战派经典，提出了 POSH 框架。")
        ],
        'quiz_q_tf': """
1.  **[判断]** 数据治理的核心目标是限制业务人员访问数据，以确保安全。
    *   ( ) 对
    *   ( ) 错

2.  **[判断]** “非入侵式治理”意味着不需要任何人对数据质量负责。
    *   ( ) 对
    *   ( ) 错

3.  **[判断]** 技术债（Technical Debt）如果早期不处理，后期处理成本会指数级上升。
    *   ( ) 对
    *   ( ) 错

4.  **[判断]** 数据管理（Data Management）包含数据治理（Data Governance）。
    *   ( ) 对
    *   ( ) 错
""",
        'quiz_q_mc': """
5.  **[单选]** 在银行场景中，因反洗钱（AML）失败被罚款，属于数据治理在哪个维度的价值？
    *   A. 增收 (Revenue)
    *   B. 降本 (Cost)
    *   C. 避险 (Risk)
    *   D. 增效 (Efficiency)

6.  **[单选]** 谁最适合担任公司级数据治理委员会的主席？
    *   A. 实习生
    *   B. IT 经理
    *   C. 数据库管理员 (DBA)
    *   D. CEO / COO / 首席战略官

7.  **[单选]** 描述“数据的定义、格式、业务含义”的数据是？
    *   A. 主数据
    *   B. 交易数据
    *   C. 元数据
    *   D. 参考数据

8.  **[多选]** 以下属于“进攻型”数据战略场景的是？
    *   A. 满足 GDPR 合规要求
    *   B. 利用用户数据进行精准营销
    *   C. 将数据打包出售给第三方
    *   D. 防止黑客攻击数据库

9.  **[单选]** DAMA 定义的数据管理核心是？
    *   A. 数据架构
    *   B. 数据治理
    *   C. 数据质量
    *   D. 数据安全
""",
        'quiz_a': """
1.  **错**。解析：核心目标是**平衡**安全与价值。过度限制会导致数据失去价值。
2.  **错**。解析：非入侵式治理是指**正式化**现有的责任，而不是没有责任。
3.  **对**。解析：这是软件工程和数据工程的共识，初期规范缺失由于数据耦合度低可能不明显，但随着系统复杂度增加，修正成本极大。
4.  **错**。解析：DAMA 2.0 中，治理是核心；广义上管理包含治理，但狭义上通常将二者并列或视治理为上层建筑。DAMA 视图中治理指导管理。
5.  **C**。解析：合规免罚属于风险控制（Risk/Compliance）。
6.  **D**。解析：涉及跨部门权力协调，必须由高层挂帅。
7.  **C**。解析：元数据是“关于数据的数据”。
8.  **BC**。解析：A和D属于防御型（守成）；B和C属于利用数据创造新价值（进攻）。
9.  **B**。解析：DAMA Wheel 的圆心是数据治理。
"""
    },
    '02': {
        'faq': """# FAQ: 核心知识领域

## Q1: 到底什么是主数据（MDM），能结合 ERP 系统讲讲吗？
**A:** 
*   **场景**: 一个制造企业，ERP 里有“供应商 A”，SRM（供应链系统）里也有“供应商 A”。
*   **问题**: 如果供应商 A 换了电话号码，采购员在 SRM 里改了，ERP 里的电话号码没变。结果财务打款通知发到了旧手机上，造成业务事故。
*   **定义**: 主数据就是用来解决“跨系统共享的核心实体”一致性问题的。MDM 系统会作为唯一的“真理源头”（Single Source of Truth），分发正确的供应商信息给 ERP 和 SRM。

## Q2: 数据质量（DQ）做不好的主要阻力在哪？
**A:** 
*   **阻力**: **“谁污染，谁治理”难以落地**。
*   **例子**: 客服录入客户地址时偷懒，填了“未知”。这导致物流部门发货失败。由于客服背的是“接听量”KPI，不背“地址准确率”KPI，所以他们没有动力改。
*   **对策**: 必须在制度层面，把物流失败的成本核算一部分给客服部门，或者在系统录入端直接做地址校验（API 校验）。

## Q3: 元数据血缘分析（Lineage）在实际故障排查中怎么用？
**A:**
*   **场景**: CEO 发现 dashboard 上的“昨日营收”突然跌了 50%。
*   **排查**: 在没有血缘图之前，数据分析师要通宵查 SQL 代码。有了血缘图，点击“营收指标”，系统自动高亮上游的依赖——发现是源头 MySQL 的一张订单表结构变更（字段改名）导致 ETL 任务失败。""",
        'refs': [
            ("Master Data Management", "David Loshin", "2008", "Morgan Kaufmann", "MDM 领域的经典入门书籍。"),
            ("The Data Warehouse Toolkit", "Ralph Kimball", "2013", "Wiley", "维度建模权威指南，定义的星型模型是各类数仓的事实标准。"),
            ("Apache Atlas", "Apache Foundation", "2023", "[Atlas](https://atlas.apache.org/)", "开源元数据管理与治理平台，支持 Hadoop 生态的自动血缘采集。"),
            ("Data Quality Dimensions", "DAMA UK", "2013", "Whitepaper", "详细定义了完整性、准确性等 6 大核心质量维度。"),
            ("Informatica MDM Products", "Informatica", "2023", "Official Site", "业界领先的商业 MDM 解决方案介绍。"),
            ("Explaining Data Fabric", "Gartner", "2022", "Trend Report", "分析了 Data Fabric 架构如何利用主动元数据简化集成。"),
            ("Data Lineage: The Foundation of Governance", "Octopai", "2021", "Blog", "通俗解释了数据血缘在合规与排错中的作用。"),
            ("NIST Privacy Framework", "NIST", "2020", "Framework", "美国国家标准技术研究院发布的隐私保护框架。"),
            ("Metadata Management Maturity Model", "Dataversity", "2018", "Article", "评估企业元数据管理能力的层级模型。"),
            ("The Role of Data Stewards", "Plotkin", "2020", "Book Excerpt", "明确了数据管家在 MDM 和 DQ 中的具体操作职责。"),
             ("Building the Data Warehouse", "Inmon", "2005", "Wiley", "范式建模理论体系。"),
             ("Effective Data Storytelling", "Dykes", "2019", "Wiley", "数据可视化与分析领域的参考。")

        ],
        'quiz_q_tf': """
1.  **[判断]** 主数据（Master Data）的体量通常远大于交易数据（Transaction Data）。
    *   ( ) 对
    *   ( ) 错

2.  **[判断]** 数据质量清洗工作最好是在数据展示层（报表端）进行，这样最灵活。
    *   ( ) 对
    *   ( ) 错

3.  **[判断]** 元数据不仅描述技术属性（如字段类型），也描述业务属性（如指标口径）。
    *   ( ) 对
    *   ( ) 错

4.  **[判断]** 维度建模中，事实表（Fact Table）通常存储定量的数值，如金额、次数。
    *   ( ) 对
    *   ( ) 错
""",
        'quiz_q_mc': """
5.  **[单选]** 以下哪项数据最适合被纳入“主数据”管理？
    *   A. 用户的点击日志 (Clickstream)
    *   B. 企业的员工名录
    *   C. 每日的库存变动记录
    *   D. 服务器的 CPU 监控日志

6.  **[单选]** 如果一个字段的值显示为 "2023-02-30"，这违反了数据质量的哪个维度？
    *   A. 唯一性
    *   B. 及时性
    *   C. 完整性
    *   D. 有效性/准确性 (Validity)

7.  **[单选]** 在 Kimball 架构中，数据仓库的核心是？
    *   A. 星型模型 (Star Schema)
    *   B. 雪花模型 (Snowflake Schema) - 归一化
    *   C. 3NF 范式模型
    *   D. Data Vault

8.  **[多选]** 元数据管理的典型应用场景包括？
    *   A. 影响性分析 (Impact Analysis)
    *   B. 快速搜索数据资产
    *   C. 理解业务术语含义
    *   D. 自动生成测试数据

9.  **[单选]** 数据安全中的“脱敏”操作（Masking）主要目的是？
    *   A. 压缩数据体积
    *   B. 防止敏感隐私泄露
    *   C. 提高查询速度
    *   D. 修复错误数据
""",
        'quiz_a': """
1.  **错**。解析：交易数据（如淘宝订单流水）是海量的，而主数据（如用户列表、商品列表）数量相对有限且稳定。
2.  **错**。解析：清洗应尽早进行（最好在源头或 ODS/DW 层），如果在报表端清洗，会导致不同报表逻辑不一致（“报表打架”）。
3.  **对**。解析：元数据分为技术元数据、业务元数据和操作元数据。
4.  **对**。解析：事实表存事实（Measure），维度表存环境（Context）。
5.  **B**。解析：员工是核心实体，具有高共享性、低波动性。日志流水属于交易/流数据。
6.  **D**。解析：2月没有30号，这是逻辑无效的日期，属于有效性或准确性问题。
7.  **A**。解析：Kimball 强烈推崇星型模型，因为易于理解和查询性能好。
8.  **ABC**。解析：D 生成测试数据通常不依赖元数据管理平台的核心功能，尽管可能相关，但ABC是核心用途。
9.  **B**。解析：脱敏（如把手机号中间四位变*）是为了隐私保护。
"""
    }
}
# ... (I would extend this for all 10 chapters in the real execution)
# To save tool output space, I will write specific rich content for 3-10 in the file write call 
# by implementing the script logic to cover them.
# The `CONTENTS` dict in the final file will be fully populated.

def main():
    write_script(CONTENTS)

def write_script(data_dict):
    # This function is a placeholder for the actual tool call which will write the full python script
    pass

