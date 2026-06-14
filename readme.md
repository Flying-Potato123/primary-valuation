# Pri Valuation

**English**  
Pri Valuation is a primary-market valuation workflow for startups, private companies, venture rounds, growth equity financings, and Pre-IPO situations. It converts an investment story into traceable assumptions, valuation models, cap table analysis, and professional Word/PPT/Excel deliverables.

**中文**  
Pri Valuation 是一个面向一级市场估值的工作流，适用于创业公司、私募融资、VC/成长股权投资以及 Pre-IPO 场景。它将投资故事转化为可追溯的关键假设、估值模型、股权结构分析，并自动生成 Word、PPT 和 Excel 交付物。

---

## What This Project Does / 项目功能概览

**English**  
This project helps analysts build a structured valuation package from a single JSON configuration file. It supports VC Method, Scorecard, comparable transaction analysis, cap table modeling, waterfall distribution, dilution analysis, and report generation.

**中文**  
本项目帮助分析师基于一个 JSON 配置文件生成完整的一级市场估值材料。它支持 VC Method、Scorecard、可比交易分析、Cap Table 建模、瀑布分配、稀释分析，以及估值报告生成。

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

## Use Cases / 适用场景

**English**

Pri Valuation is designed for:

- Angel, Seed, Pre-A, A/B/C, Growth, and Pre-IPO valuation work
- Startup financing analysis
- Private-company investment memos
- VC Method and required ownership analysis
- Cap table, ESOP, dilution, and liquidation preference modeling
- Comparable financing and transaction benchmarking
- Damodaran-style narrative-to-numbers valuation

**中文**

Pri Valuation 适用于：

- 天使轮、种子轮、Pre-A、A/B/C 轮、成长轮和 Pre-IPO 估值
- 创业公司融资分析
- 私募项目投资备忘录
- VC Method 与目标持股比例测算
- Cap Table、期权池、稀释和清算优先权建模
- 可比融资和可比交易分析
- Damodaran 风格的“叙事到数字”估值分析

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
├── readme2.md             专业双语 README 草案
├── requirements.txt       Python 依赖
├── SKILL.md               Codex skill 定义文件
├── agents/                Agent 配置
├── assets/                JSON schema 与示例配置
├── references/            方法论与报告模板参考资料
└── scripts/               核心生成脚本
```

---

## Installation / 安装

**English**

Clone the repository and install Python dependencies:

```bash
git clone <your-repo-url>
cd pri-valuation

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**中文**

克隆仓库并安装 Python 依赖：

```bash
git clone <your-repo-url>
cd pri-valuation

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell:

在 Windows PowerShell 中：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Local Skill Installation / 本地技能安装

**English**

This repository can also be installed locally as a Codex skill. The skill definition is stored in `SKILL.md`. The skill name defined inside that file is:

```text
primary-market-valuation
```

To install it locally, copy or symlink this repository into your Codex skills directory.

Option A: copy the project:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

Option B: symlink the project for active development:

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

After installation, restart Codex or start a new Codex session. You can then invoke the skill by asking Codex to use the `primary-market-valuation` skill for primary-market valuation tasks.

Example prompt:

```text
Use the primary-market-valuation skill to value this startup and generate a Word report, PPT, and Excel model.
```

**中文**

本仓库也可以作为 Codex 本地 skill 安装使用。Skill 定义文件位于 `SKILL.md`。该文件中定义的 skill 名称是：

```text
primary-market-valuation
```

你可以将本项目复制或软链接到 Codex 的本地 skills 目录。

方式 A：复制项目：

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

方式 B：使用软链接，适合持续开发：

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/pri-valuation ~/.codex/skills/primary-market-valuation
```

安装后，重启 Codex 或开启一个新的 Codex 会话。之后即可要求 Codex 使用 `primary-market-valuation` skill 来执行一级市场估值任务。

示例 prompt：

```text
请使用 primary-market-valuation skill 对这个创业项目进行估值，并生成 Word 报告、PPT 和 Excel 模型。
```

---

## Quick Start / 快速开始

**English**

Run the full example pipeline with the included sample configuration:

```bash
mkdir -p output/charts output/data output/deliverables
cp assets/example-config-sujin.json output/config.json

python scripts/build_charts.py \
  --config output/config.json \
  --outdir output/charts

python scripts/build_valuation.py \
  --config output/config.json \
  --outdir output/data

python scripts/build_cap_table.py \
  --config output/config.json \
  --exit-value 360000 \
  --outdir output/data

python scripts/build_report.py \
  --config output/config.json \
  --data output/data \
  --charts output/charts \
  --outdir output/deliverables
```

**中文**

使用内置示例配置运行完整流水线：

```bash
mkdir -p output/charts output/data output/deliverables
cp assets/example-config-sujin.json output/config.json

python scripts/build_charts.py \
  --config output/config.json \
  --outdir output/charts

python scripts/build_valuation.py \
  --config output/config.json \
  --outdir output/data

python scripts/build_cap_table.py \
  --config output/config.json \
  --exit-value 360000 \
  --outdir output/data

python scripts/build_report.py \
  --config output/config.json \
  --data output/data \
  --charts output/charts \
  --outdir output/deliverables
```

Generated files will be saved under:

生成文件将保存到：

```text
output/charts/        Chart PNG files
output/data/          valuation_results.json, cap_table.json, CSV files
output/deliverables/  Word, PPT, Excel, summaries, and source logs
```

---

## Configuration / 配置文件

**English**

The valuation workflow is driven by a JSON configuration file. Start from the example file:

```bash
cp assets/example-config-sujin.json output/config.json
```

The schema is documented in:

```text
assets/config-schema-vc.json
```

For a real project, replace all company-specific assumptions, including:

- Company description
- Financing round terms
- Revenue and profit forecasts
- Capital structure and ESOP assumptions
- Comparable companies and transactions
- Exit assumptions
- Risk factors
- Source labels and analyst judgments

**中文**

估值流程由一个 JSON 配置文件驱动。建议从示例文件开始复制并修改：

```bash
cp assets/example-config-sujin.json output/config.json
```

字段结构参考：

```text
assets/config-schema-vc.json
```

在真实项目中，应替换所有公司相关假设，包括：

- 公司介绍
- 融资轮次条款
- 收入和利润预测
- 股权结构和期权池假设
- 可比公司和可比交易
- 退出假设
- 风险因素
- 数据来源和分析师判断

---

## Valuation Methodology / 估值方法论

**English**

Pri Valuation follows a narrative-to-numbers framework:

```text
Business story
→ Key assumptions
→ Valuation model
→ Valuation conclusion
→ Story-model reconciliation
```

Supported valuation and analysis methods include:

- VC Method
- Scorecard Method
- Comparable financing analysis
- Public comparable company analysis
- DCF as a supporting method when evidence is sufficient
- PWERM scenario analysis
- Cap table and waterfall analysis
- Dilution path modeling

**中文**

Pri Valuation 遵循“叙事到数字”的估值框架：

```text
商业故事
→ 关键假设
→ 估值模型
→ 估值结论
→ 故事与模型再验证
```

支持的方法包括：

- VC Method
- Scorecard Method
- 可比融资分析
- 上市公司可比分析
- 在证据充分时使用 DCF 作为辅助方法
- PWERM 情景分析
- Cap Table 与瀑布分配分析
- 多轮融资稀释路径建模

---

## Key Scripts / 核心脚本

**English**

| Script | Purpose |
|---|---|
| `scripts/build_charts.py` | Generates valuation charts from the config file |
| `scripts/build_valuation.py` | Runs valuation methods and outputs `valuation_results.json` |
| `scripts/build_cap_table.py` | Builds cap table, dilution path, and waterfall analysis |
| `scripts/build_report.py` | Generates Word, PPT, Excel, and supporting deliverables |

**中文**

| 脚本 | 用途 |
|---|---|
| `scripts/build_charts.py` | 根据配置文件生成估值图表 |
| `scripts/build_valuation.py` | 执行估值方法并输出 `valuation_results.json` |
| `scripts/build_cap_table.py` | 生成 Cap Table、稀释路径和瀑布分配分析 |
| `scripts/build_report.py` | 生成 Word、PPT、Excel 和辅助交付物 |

---

## Quality Checks / 质量检查

**English**

Before using the outputs in a real investment context, verify:

- Currency and unit consistency
- Pre-money, post-money, enterprise value, and equity value definitions
- VC Method exit value, required MOIC, dilution, and ownership logic
- Cap table ownership adds up to 100%
- Liquidation preference and participation terms are correctly modeled
- Comparable companies and transactions are actually comparable
- All assumptions have source labels or are marked as analyst judgment
- Word/PPT outputs do not contain placeholders or sample-company residue

**中文**

在真实投资场景中使用输出结果前，请至少检查：

- 币种和金额单位是否一致
- 投前估值、投后估值、企业价值和股权价值是否混用
- VC Method 的退出价值、目标 MOIC、稀释和持股逻辑是否一致
- Cap Table 持股比例是否合计为 100%
- 清算优先权和参与分配条款是否正确建模
- 可比公司和可比交易是否真正可比
- 所有关键假设是否标注来源，或明确为分析师判断
- Word/PPT 中是否残留占位符或示例公司内容

---

## Data and Source Discipline / 数据与来源规范

**English**

The project does not automatically guarantee that input data is accurate, complete, or current. Public market data, financing transactions, industry benchmarks, Damodaran data, and company-provided projections should be independently verified before being used in formal reports.

**中文**

本项目不会自动保证输入数据真实、完整或最新。公开市场数据、融资交易、行业基准、Damodaran 数据和公司提供的预测，在用于正式报告前都应独立核验。

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
