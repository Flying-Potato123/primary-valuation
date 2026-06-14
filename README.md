# Primary Valuation / 一级市场估值

**English**  
Primary Valuation is a specialized valuation workflow designed for the primary market, comprehensively covering scenarios such as startups, private financing, VC/growth equity investments, and Pre-IPO stages. It transforms complex valuations into an analytical framework that integrates "quantitative digital models" with "qualitative narrative storytelling." Supporting mainstream methodologies such as Discounted Cash Flow (DCF), Comparable Transaction Analysis, Venture Capital Valuation, Scorecard analysis, and Cap Table / Waterfall modeling, it automatically generates standardized deliverables, including Word valuation reports, PPT presentations, and Excel templates.

You may refer to the Example folder, where a virtually generated "SuiJin Tech valuation report" is provided for previewing the final deliverable format.

**中文**  
Primary Valuation 是专为一级市场打造的专业估值工作流，全面覆盖初创企业、私募融资、VC/成长型股权投资及 Pre-IPO 等核心场景。该工作流将复杂的估值过程转化为“量化数字模型”与“定性文字故事”深度结合的分析体系。Primary Valuation 内置了现金流折现（DCF）、可比交易分析、风险投资估值、Scorecard 分析以及 Cap Table / Waterfall 建模等多种主流方法，并能自动生成 Word 估值报告、PPT 演示文稿及 Excel 数据模板等标准化交付物。

您可以前往 Example 文件夹，下载虚拟生成的“岁锦科技公司估值报告”示例，以便对最终的交付文档进行预览。

---

## Repository Structure / 仓库结构

**English**

```text
pri-valuation/
├── README.md
├── readme2.md
├── requirements.txt
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── config-schema-vc.json
│   └── example-config-sujin.json
├── references/
│   ├── damodaran-method.md
│   ├── damodaran-primary-synthesis.md
│   ├── vc-methodology-reference.md
│   ├── cap-table-waterfall.md
│   ├── industry-benchmarks.md
│   └── report-template-guide.md
└── scripts/
    ├── build_charts.py
    ├── build_valuation.py
    ├── build_cap_table.py
    └── build_report.py
```

**中文**

```text
pri-valuation/
├── README.md              项目说明
├── readme2.md             双语 README 文档
├── requirements.txt       Python 依赖
├── SKILL.md               Codex skill 定义文件
├── agents/                Agent 配置
├── assets/                JSON schema 与示例配置
├── references/            方法论与报告模板参考资料
└── scripts/               核心生成脚本
```

---

## Valuation Logic / 估值逻辑

**English**  
For startups, the answer is rarely a single valuation figure. Early-stage companies typically have limited historical data, unvalidated product-market fit, high future dilution risks, and value realization that is highly dependent on exit pathways. Therefore, Primary Valuation's valuation philosophy draws upon Aswath Damodaran's "Narrative to Numbers" framework, while also incorporating methodologies specific to the primary market:

| Valuation Lens | Financial Meaning |
|---|---|
| VC Method | What valuation allows the investor to reach the required MOIC or IRR? |
| Scorecard | How does the company compare with other early-stage companies on team, market, product, traction, and risk? |
| Comparable Financing | How is the private market pricing similar companies or similar rounds? |
| DCF / Narrative Value | What intrinsic value is implied by the business story, growth, margin, reinvestment, and risk? |
| PWERM / Scenario Analysis | How do IPO, M&A, continued operation, or failure scenarios affect value? |
| Cap Table / Waterfall | How much of the exit value actually flows to each shareholder class? |

**中文**  
对于创业公司，答案通常不是一个单一的估值数字。早期公司历史数据有限，产品市场匹配尚未完全验证，未来稀释风险高，价值实现也高度依赖退出路径。因此，Primary Valuation 的估值思想借鉴了 Aswath Damodaran 的“叙事到数字”框架，同时结合一级市场特有方法。

Primary Valuation 不依赖单一估值方法，而是对多个估值视角进行交叉验证：

| 估值视角 | 金融含义 |
|---|---|
| VC Method | 在目标 MOIC 或 IRR 下，投资人能够接受的估值是多少？ |
| Scorecard | 公司在团队、市场、产品、牵引力和风险方面相对同阶段公司如何？ |
| 可比融资 | 私募市场如何给类似公司或类似轮次定价？ |
| DCF / 叙事价值 | 商业故事、增长、利润率、再投资和风险隐含的内在价值是多少？ |
| PWERM / 情景分析 | IPO、并购、继续经营或失败等路径如何影响价值？ |
| Cap Table / 瀑布分配 | 退出价值最终如何分配到不同股东和证券类别？ |

---

## Install Locally / 本地安装

**English**  
Method 1 (Recommended): Ask an AI agent to install.  
Copy the repository URL and ask an AI agent to download and install the skill for you.

```text
Please help me download and install the Codex skill from this repository:
https://github.com/Flying-Potato123/primary-valuation
```

Method 2: Manual copy or symlink.  
Clone or download this repository, then place the skill directory into your Codex skills folder.

```bash
git clone https://github.com/Flying-Potato123/eprimary-valuation.git
mkdir -p ~/.codex/skills
ln -s /path/to/eprimary-valuation ~/.codex/skills/primary-market-valuation
```

If you prefer copying instead of symlinking:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/eprimary-valuation ~/.codex/skills/primary-market-valuation
```

Restart Codex or open a new session after installation.

**中文**  
方法 1（推荐）：让 AI agent 帮你安装。  
复制这个仓库链接，让 AI agent 帮你下载并安装 skill。

```text
请帮我下载并安装这个仓库里的 Codex skill：
https://github.com/Flying-Potato123/primary-valuation
```

方法 2：手动复制或软链接。  
克隆或下载本仓库，然后把 skill 目录放入 Codex skills 文件夹。

```bash
git clone https://github.com/Flying-Potato123/eprimary-valuation.git
mkdir -p ~/.codex/skills
ln -s /path/to/eprimary-valuation ~/.codex/skills/primary-market-valuation
```

如果您更希望复制文件而不是创建软链接：

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/eprimary-valuation ~/.codex/skills/primary-market-valuation
```

安装后，重启 Codex 或开启新的 Codex 会话即可。

---

## Usage / 使用方法

**English**  
After installation, you can invoke the skill by explicitly asking Codex to use `primary-market-valuation`. A good prompt should briefly state the company, financing stage, available materials, and desired outputs.

General prompt:

```text
Use the primary-market-valuation skill to value this company.

Company: [company name and short description]
Stage: [Angel / Seed / Pre-A / A / Growth / Pre-IPO]
Available materials: [BP, pitch deck, financial forecast, cap table, term sheet]
Deliverables: [valuation range, Word report, PPT, Excel model, cap table analysis]
Please use a narrative-to-numbers framework and clearly label assumptions and sources.
```

Common task prompts:

```text
Use the primary-market-valuation skill to generate a full valuation report, PPT, and Excel model for this Angel round financing.
```

```text
Use the primary-market-valuation skill to provide only a quick pre-money valuation range and the key assumptions behind it.
```

```text
Use the primary-market-valuation skill to analyze the cap table, ESOP expansion, dilution path, and waterfall distribution for this financing round.
```

```text
Use the primary-market-valuation skill to review this investment memo and identify valuation assumptions, missing sources, method mismatches, and key risks.
```

**中文**  
安装后，您可以在提示词中明确要求 Codex 使用 `primary-market-valuation`。一个好的提示词应简要说明公司、融资阶段、已有资料和希望生成的交付物。

通用提示词：

```text
请使用 primary-market-valuation skill 对这家公司进行估值。

公司：[公司名称和简要介绍]
阶段：[天使轮 / 种子轮 / Pre-A / A轮 / 成长期 / Pre-IPO]
已有资料：[BP、Pitch Deck、财务预测、Cap Table、Term Sheet]
需要交付：[估值区间、Word 报告、PPT、Excel 模型]
请使用“叙事到数字”的框架，并清楚标注关键假设和数据来源。
```

常见任务提示词：

```text
请使用 primary-market-valuation skill，为这个天使轮融资项目生成完整估值报告、PPT 和 Excel 模型。
```

```text
请使用 primary-market-valuation skill，请你对项目进行DCF估值，并说明关键假设。
```

```text
请使用 primary-market-valuation skill，分析本轮融资的 Cap Table、期权池扩容、稀释路径和瀑布分配。
```

```text
请使用 primary-market-valuation skill，复核这份投资报告，识别估值假设、缺失来源、方法不匹配和关键风险。
```

---

## Data and Source Discipline / 数据与来源规范

**English**  
Primary Valuation does not automatically guarantee that input data is accurate, complete, or current. Public market data, financing transactions, industry benchmarks, Damodaran data, and company-provided forecasts should be independently verified before being used in formal investment materials.

Every important assumption should be labeled as one of the following:

- Observed / observed data
- Company-provided / company-provided data
- Public source / public market or industry source
- Private transaction / private financing or transaction data
- Analyst judgment / analyst judgment
- Sensitivity / sensitivity assumption

**中文**  
Primary Valuation 不会自动保证输入数据真实、完整或最新。公开市场数据、融资交易、行业基准、Damodaran 数据和公司提供的预测，在用于正式投资材料前都应独立核验。

每一个重要假设都应标注为以下类型之一：

- Observed / 已观察数据
- Company-provided / 公司提供
- Public source / 公开来源
- Private transaction / 私募交易
- Analyst judgment / 分析师判断
- Sensitivity / 敏感性假设

---

## Disclaimer / 免责声明

**English**  
This project is for research, education, and internal analytical use only. It does not constitute investment advice, valuation opinion, financing advice, legal advice, accounting advice, or any regulated financial recommendation.

**中文**  
本项目仅用于研究、教学和内部分析，不构成投资建议、估值意见书、融资建议、法律建议、会计建议或任何受监管金融建议。

---

## License / 许可证

**English**  
This project uses the MIT open-source license. Please refer to the repository license file for details.

**中文**  
本项目采用 MIT 开源许可证。具体授权条款请以仓库中的 License 文件为准。
