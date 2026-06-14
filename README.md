# Primary Valuation / 一级市场估值

**English**  
Pri Valuation is a primary-market valuation workflow for startups, private companies, venture rounds, growth equity financings, and Pre-IPO situations. It converts an investment story into traceable assumptions, valuation models, cap table analysis, and professional Word/PPT/Excel deliverables.

**中文**  
Pri Valuation 是一个面向一级市场估值的工作流，适用于创业公司、私募融资、VC/成长股权投资以及 Pre-IPO 场景。它将投资故事转化为可追溯的关键假设、估值模型、股权结构分析，并自动生成 Word、PPT 和 Excel 交付物。

---

## What This Project Does / 项目功能概览

**English**  
This project helps analysts build a structured valuation package from a single JSON configuration file. It supports VC Method, Scorecard, comparable transaction analysis, cap table modeling, waterfall distribution, dilution analysis, and report generation.
You can navigate to the Example folder and download the sample "Suijin Tech Valuation Report" (virtually generated) to preview the final deliverable document.

**中文**  
本项目帮助分析师基于一个 JSON 配置文件生成完整的一级市场估值材料。它支持 VC Method、Scorecard、可比交易分析、Cap Table 建模、瀑布分配、稀释分析，以及估值报告生成。
您可以前往 Example 文件夹，下载虚拟生成的“岁锦科技公司估值报告”示例，以便对最终的交付文档进行预览。

Core outputs:

- Valuation results in JSON format
- Cap table and waterfall analysis
- Professional valuation charts
- Word valuation report
- PowerPoint presentation
- Excel valuation model
- Source log, assumption traceability, one-page summary, and open questions

核心输出包括：

- JSON 格式的估值结果
- Cap Table 与瀑布分配分析
- 专业估值图表
- Word 估值分析报告
- PowerPoint 展示文档
- Excel 估值模型
- 数据来源日志、假设追溯表、一页摘要和待确认问题清单

---

## Financial Valuation Logic / 金融估值构建逻辑

**English**  
The project follows a narrative-to-numbers approach. A valuation should not begin with a multiple or a spreadsheet formula. It should begin with a clear economic story:

```text
Business story
→ Economic drivers
→ Model assumptions
→ Valuation methods
→ Investor economics
→ Final valuation range
```

The key question is not only "what is the company worth?" but also "what must be true for this valuation to be reasonable?"

**中文**  
本项目遵循“叙事到数字”的估值方法。估值不应从一个倍数或一个表格公式开始，而应从清晰的商业经济逻辑开始：

```text
商业故事
→ 经济驱动因素
→ 模型假设
→ 估值方法
→ 投资人经济账
→ 最终估值区间
```

核心问题不只是“这家公司值多少钱”，而是“要让这个估值成立，哪些商业假设必须是真的”。

In primary-market valuation, this means:

- Market size must map to revenue potential.
- Competitive advantage must map to margin, retention, pricing power, or capital efficiency.
- Growth must map to reinvestment needs, burn rate, hiring, sales capacity, or working capital.
- Risk must map to survival probability, discount rate, required return, dilution, and exit path.
- Financing terms must map to ownership, preference stack, investor proceeds, and founder dilution.

在一级市场估值中，这意味着：

- 市场空间必须映射到收入潜力。
- 竞争优势必须映射到利润率、留存率、定价权或资本效率。
- 增长必须映射到再投资需求、现金消耗、人员扩张、销售能力或营运资金。
- 风险必须映射到存活概率、折现率、目标回报、未来稀释和退出路径。
- 融资条款必须映射到持股比例、优先清算权、投资人分配和创始人稀释。

---

## Damodaran-Style Valuation / 达摩达兰式估值逻辑

**English**  
The valuation philosophy in this project is inspired by Aswath Damodaran's narrative-to-numbers framework. In that framework, valuation is not a mechanical exercise. It is a disciplined process for turning a story about a business into a set of financial inputs.

For a private company, the Damodaran-style logic can be summarized as four questions:

1. What cash flows can the company generate if the story works?
2. How much reinvestment is required to create that growth?
3. How risky are those cash flows, especially given failure risk and financing uncertainty?
4. What does the company look like at exit or maturity?

**中文**  
本项目的估值思想借鉴了 Aswath Damodaran 的“叙事到数字”框架。在这个框架下，估值不是机械填表，而是把一个关于企业未来的故事，严谨地转化为一组财务输入。

对于非上市公司，达摩达兰式估值可以归纳为四个问题：

1. 如果商业故事成立，公司未来能产生多少现金流？
2. 为了实现这种增长，公司需要投入多少资本、人员、渠道和营运资金？
3. 这些现金流有多大风险，尤其是失败风险、融资不确定性和退出不确定性？
4. 到退出或成熟阶段时，公司应当呈现什么样的经济特征？

**English**  
For startups, the answer is rarely a single DCF number. Early-stage companies usually have limited historical data, uncertain product-market fit, high dilution risk, and exit-dependent value realization. Therefore, Pri Valuation uses Damodaran's discipline as the foundation, but combines it with venture-specific methods:

- VC Method to test target returns and required ownership.
- Scorecard to benchmark early-stage qualitative risk.
- Comparable financing to test market pricing.
- PWERM-style scenarios to reflect different exit paths.
- Cap table and waterfall analysis to convert enterprise value into actual investor proceeds.

**中文**  
对于创业公司，答案通常不是一个单一的 DCF 数字。早期公司历史数据有限，产品市场匹配尚未完全验证，未来稀释风险高，价值实现也高度依赖退出路径。因此，Pri Valuation 以达摩达兰的估值纪律为基础，同时结合一级市场特有方法：

- 用 VC Method 检验目标回报和所需持股比例。
- 用 Scorecard 对早期项目的定性风险进行基准化。
- 用可比融资检验市场实际定价。
- 用 PWERM 风格情景分析反映不同退出路径。
- 用 Cap Table 和瀑布分配把企业价值转换为投资人真实可获得的收益。

**English**  
The goal is not to make an uncertain company look precise. The goal is to make uncertainty explicit, connect assumptions to value drivers, and show which assumptions would change the investment conclusion.

**中文**  
本项目的目标不是把高度不确定的公司估得看似精确，而是把不确定性显性化，把关键假设与价值驱动因素连接起来，并说明哪些假设会改变投资结论。

---

## Primary-Market Method Stack / 一级市场估值方法体系

**English**  
Pri Valuation does not rely on a single method. It reconciles multiple valuation lenses:

| Valuation Lens | Financial Meaning |
|---|---|
| VC Method | What valuation allows the investor to reach the required MOIC or IRR? |
| Scorecard | How does the company compare with other early-stage companies on team, market, product, traction, and risk? |
| Comparable Financing | How is the private market pricing similar companies or similar rounds? |
| DCF / Narrative Value | What intrinsic value is implied by the business story, growth, margin, reinvestment, and risk? |
| PWERM / Scenario Analysis | How do IPO, M&A, continued operation, or failure scenarios affect value? |
| Cap Table / Waterfall | How much of the exit value actually flows to each shareholder class? |

**中文**  
Pri Valuation 不依赖单一估值方法，而是对多个估值视角进行交叉验证：

| 估值视角 | 金融含义 |
|---|---|
| VC Method | 在目标 MOIC 或 IRR 下，投资人能够接受的估值是多少？ |
| Scorecard | 公司在团队、市场、产品、牵引力和风险方面相对同阶段公司如何？ |
| 可比融资 | 私募市场如何给类似公司或类似轮次定价？ |
| DCF / 叙事价值 | 商业故事、增长、利润率、再投资和风险隐含的内在价值是多少？ |
| PWERM / 情景分析 | IPO、并购、继续经营或失败等路径如何影响价值？ |
| Cap Table / 瀑布分配 | 退出价值最终如何分配到不同股东和证券类别？ |

The final valuation should be a range, not a point estimate. The range should explain both intrinsic value and market pricing.

最终估值应当是一个区间，而不是一个点估值。这个区间既要解释企业内在价值，也要解释市场定价。

---

## Installation / 安装

**English**  
Install the project in a standard Python environment:

```bash
git clone <your-repo-url>
cd pri-valuation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**中文**  
在标准 Python 环境中安装本项目：

```bash
git clone <your-repo-url>
cd pri-valuation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows users can activate the virtual environment with:

Windows 用户可使用以下命令激活虚拟环境：

```powershell
.venv\Scripts\Activate.ps1
```

---

## Local Skill Installation / 本地技能安装

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

## Quick Start / 快速开始

**English**  
Run the included example pipeline:

```bash
mkdir -p output/charts output/data output/deliverables
cp assets/example-config-sujin.json output/config.json

python scripts/build_charts.py --config output/config.json --outdir output/charts
python scripts/build_valuation.py --config output/config.json --outdir output/data
python scripts/build_cap_table.py --config output/config.json --exit-value 360000 --outdir output/data
python scripts/build_report.py --config output/config.json --data output/data --charts output/charts --outdir output/deliverables
```

**中文**  
运行内置示例流水线：

```bash
mkdir -p output/charts output/data output/deliverables
cp assets/example-config-sujin.json output/config.json

python scripts/build_charts.py --config output/config.json --outdir output/charts
python scripts/build_valuation.py --config output/config.json --outdir output/data
python scripts/build_cap_table.py --config output/config.json --exit-value 360000 --outdir output/data
python scripts/build_report.py --config output/config.json --data output/data --charts output/charts --outdir output/deliverables
```

The generated reports and models will be saved under `output/`.

生成的报告和模型会保存在 `output/` 目录下。

---

## Data and Source Discipline / 数据与来源规范

**English**  
Pri Valuation does not automatically guarantee that input data is accurate, complete, or current. Public market data, financing transactions, industry benchmarks, Damodaran data, and company-provided forecasts should be independently verified before being used in formal investment materials.

**中文**  
Pri Valuation 不会自动保证输入数据真实、完整或最新。公开市场数据、融资交易、行业基准、Damodaran 数据和公司提供的预测，在用于正式投资材料前都应独立核验。

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
No open-source license has been selected yet. Before public release, choose a license that matches your intended usage, such as MIT, Apache-2.0, or private/all-rights-reserved distribution.

**中文**  
本项目暂未选择开源许可证。公开发布前，请根据你的使用目标选择合适协议，例如 MIT、Apache-2.0，或保持私有/保留所有权利。
