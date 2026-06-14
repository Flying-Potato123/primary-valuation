# Pri Valuation

Pri Valuation 是一个一级市场估值工作流，用于创业公司、私募融资、成长股权投资和 Pre-IPO 项目的估值分析。项目将公司故事、关键假设、VC Method、Scorecard、可比交易、Cap Table/Waterfall 和报告交付物组织成一套可复跑的脚本流水线。

本仓库由 `primary-market-valuation` 整理而来，当前定位是脚本型研究工具包，不是 Web 应用，也不是已发布的 Python package。

## 功能

- 使用 JSON 配置描述公司、轮次、预测、资本结构和估值参数。
- 生成 VC Method、Scorecard、可比交易、DCF/PWERM 等估值结果。
- 生成 Cap Table、期权池扩容、稀释路径和优先股瀑布分配分析。
- 生成图表、Word 估值报告、PPT 展示文档、Excel 模型和辅助文件。
- 内置 Damodaran 叙事到数字、VC 方法论、Cap Table 和报告模板参考资料。

## 项目结构

```text
pri-valuation/
├── README.md
├── requirements.txt
├── SKILL.md
├── agents/
├── assets/
│   ├── config-schema-vc.json
│   └── example-config-sujin.json
├── references/
└── scripts/
    ├── build_charts.py
    ├── build_valuation.py
    ├── build_cap_table.py
    └── build_report.py
```

## 快速开始

```bash
git clone <your-repo-url>
cd pri-valuation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

使用内置示例配置跑完整流水线：

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

生成结果位于：

```text
output/charts/        图表 PNG
output/data/          valuation_results.json、cap_table.json、CSV
output/deliverables/  Word、PPT、Excel、摘要和来源日志
```

## 配置文件

估值输入由一个 JSON 文件驱动。推荐从示例开始复制并修改：

```bash
cp assets/example-config-sujin.json output/config.json
```

配置结构参考：

- `assets/config-schema-vc.json`：字段结构和必填项。
- `assets/example-config-sujin.json`：示例项目，不应直接用于真实投资结论。

真实项目中至少需要替换：

- `meta`：估值日期、币种、报告类型和保密级别。
- `company`：公司名称、行业、商业模式和基本描述。
- `round`：融资阶段、融资金额、出让股权和证券类型。
- `financials`：历史数据、预测收入、利润率、净利润和关键驱动。
- `capital_structure`：创始人股本、ESOP、历史轮次、可转债和权证。
- `valuation_params`：估值方法、权重、退出假设、可比公司和可比交易。
- `market_context`、`risks`、`report_narrative`：报告叙事、市场背景和风险。

## 方法论

项目遵循“文字故事 → 关键经营假设 → 数字模型 → 估值结论 → 回到故事验证”的结构。具体参考：

- `references/damodaran-method.md`
- `references/damodaran-primary-synthesis.md`
- `references/vc-methodology-reference.md`
- `references/cap-table-waterfall.md`
- `references/report-template-guide.md`

## 数据与免责声明

本项目不会自动保证输入数据真实、完整或最新。公开市场利率、可比公司、融资交易、行业规模和 Damodaran 数据在正式报告中应重新核验并标注日期。

生成结果仅供研究、教学和内部分析使用，不构成证券投资咨询、融资建议、估值意见书或任何受监管投资建议。

## License

MIT许可证协议，开源项目。
