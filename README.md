# Primary Valuation / 一级市场估值

**English**  
Primary Valuation is a specialized valuation workflow designed for the primary market, comprehensively covering scenarios such as startups, private financing, VC/growth equity investments, and Pre-IPO stages. It transforms complex valuations into an analytical framework that seamlessly integrates "quantitative digital models" with "qualitative narrative storytelling." Supporting mainstream methodologies like Discounted Cash Flow (DCF), Comparable Transaction Analysis, and Venture Capital Valuation, it automatically generates standardized deliverables, including Word valuation reports, PPT presentations, and Excel templates.

**中文**  
Primary Valuation是专为一级市场打造的专业估值工作流，全面覆盖初创企业、私募融资、VC/成长型股权投资及 Pre-IPO 等核心场景。该工作流将复杂的估值过程转化为“量化数字模型”与“定性文字故事”深度结合的分析体系。Primary Valuation内置了现金流折现（DCF）、可比交易分析以及风险投资估值等多种主流方法，并能一键自动生成 Word 估值报告、PPT 演示文稿及 Excel 数据模板等标准化交付物。
您可以前往 Example 文件夹，下载虚拟生成的“岁锦科技公司估值报告”示例，以便对最终的交付文档进行预览。

---

## Repository Structure / 仓库结构

**English**

```text
pri-valuation/
├── README.md
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
├── readme2.md             专业双语 README 草案
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
For startups, the answer is rarely a single valuation figure. Early-stage companies typically have limited historical data, unvalidated product-market fit, high future dilution risks, and value realization that is highly dependent on exit pathways. Therefore, Primary Valuation's valuation philosophy draws upon Aswath Damodaran’s "Narrative to Numbers" framework, while also incorporating methodologies specific to the primary market:

| Valuation Lens | Financial Meaning |
|---|---|
| VC Method | What valuation allows the investor to reach the required MOIC or IRR? |
| Scorecard | How does the company compare with other early-stage companies on team, market, product, traction, and risk? |
| Comparable Financing | How is the private market pricing similar companies or similar rounds? |
| DCF / Narrative Value | What intrinsic value is implied by the business story, growth, margin, reinvestment, and risk? |
| PWERM / Scenario Analysis | How do IPO, M&A, continued operation, or failure scenarios affect value? |
| Cap Table / Waterfall | How much of the exit value actually flows to each shareholder class? |

**中文**  
对于创业公司，答案通常不是一个单一的估值数字。早期公司历史数据有限，产品市场匹配尚未完全验证，未来稀释风险高，价值实现也高度依赖退出路径。因此，Primary Valuation 的估值思想借鉴了 Aswath Damodaran 的“叙事到数字”框架，同时结合一级市场特有方法：

Pri Valuation 不依赖单一估值方法，而是对多个估值视角进行交叉验证：

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
This repository can also be used as a local Codex skill. The skill definition is stored in `SKILL.md`, and the skill name is:

```text
primary-market-valuation
```

For local installation, copy or symlink this project into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

Restart Codex or open a new session after installation.

**中文**  
本仓库也可以作为 Codex 本地 skill 使用。Skill 定义文件位于 `SKILL.md`，skill 名称为：

```text
primary-market-valuation
```

本地安装时，将本项目复制或软链接到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

安装后，重启 Codex 或开启新的 Codex 会话即可。

Example prompt:

示例 prompt：

```text
Use the primary-market-valuation skill to value this startup and generate a Word report, PPT, and Excel model.
```

```text
请使用 primary-market-valuation skill 对这个创业项目进行估值，并生成 Word 报告、PPT 和 Excel 模型。
```
---

## Data and Source Discipline / 数据与来源规范

**English**  
Primary Valuation does not automatically guarantee that input data is accurate, complete, or current. Public market data, financing transactions, industry benchmarks, Damodaran data, and company-provided forecasts should be independently verified before being used in formal investment materials.

**中文**  
Primary Valuation 不会自动保证输入数据真实、完整或最新。公开市场数据、融资交易、行业基准、Damodaran 数据和公司提供的预测，在用于正式投资材料前都应独立核验。

Every important assumption should be labeled as one of the following:

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
This project choose the MIT open-source license, please feel free to use it.

**中文**  
本项目选择MIT开源许可证，请放心使用。
