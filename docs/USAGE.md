# Usage Guide

本文档说明如何用 `pri-valuation` 生成一套一级市场估值交付物。

## 1. 准备环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 2. 准备配置

```bash
mkdir -p output
cp assets/example-config-sujin.json output/config.json
```

打开 `output/config.json`，替换公司、轮次、财务预测、可比公司、可比交易、资本结构和风险因素。

正式项目中不要直接沿用示例里的公司名称、行业数据、融资案例或估值参数。

## 3. 生成图表

```bash
mkdir -p output/charts
python scripts/build_charts.py \
  --config output/config.json \
  --outdir output/charts
```

输出：`output/charts/*.png`

## 4. 生成估值结果

```bash
mkdir -p output/data
python scripts/build_valuation.py \
  --config output/config.json \
  --outdir output/data
```

输出：

- `output/data/valuation_results.json`
- `output/data/charts/*.png`

## 5. 生成 Cap Table 和瀑布分配

`--exit-value` 使用万元口径。比如 `360000` 表示 36 亿元人民币。

```bash
python scripts/build_cap_table.py \
  --config output/config.json \
  --exit-value 360000 \
  --outdir output/data
```

输出：

- `output/data/cap_table.json`
- `output/data/cap_table.csv`

## 6. 生成报告和展示文档

```bash
mkdir -p output/deliverables
python scripts/build_report.py \
  --config output/config.json \
  --data output/data \
  --charts output/charts \
  --outdir output/deliverables
```

输出：

- Word 估值报告 `.docx`
- PPT 展示文档 `.pptx`
- Excel 估值模型 `.xlsx`
- `manifest.json`
- `one_page_summary.md`
- `source_log.csv`
- `assumption_traceability.csv`
- `open_questions.md`

## 7. 交付前检查

至少检查：

- 估值日期、币种和金额单位是否一致。
- Pre-money、Post-money、Equity Value、Enterprise Value 是否混用。
- VC Method 的退出价值、退出倍数、目标 MOIC 和未来稀释是否一致。
- Cap Table 持股比例是否合计为 100%。
- Word/PPT 中是否还有示例公司名称、占位符或无来源假设。
- 所有 analyst judgment 是否在报告或来源日志中可见。
