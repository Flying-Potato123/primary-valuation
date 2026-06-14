---
name: primary-market-valuation
description: Integrated primary-market valuation workflow for startups, private companies, venture/growth equity rounds, pre-IPO financings, private-company investment memos, valuation reports, PPT presentations, cap table/waterfall analysis, VC Method models, Scorecard/Berkus/PWERM/OPM analysis, financing-term backsolves, comparable financing analysis, private-company DCF, and Damodaran-style narrative-to-numbers valuation. Use when Codex needs to value a private project or company, reconcile intrinsic value with pricing, assess round terms, build Word/PPT/Excel valuation deliverables, or critique a primary-market valuation using Aswath Damodaran's framework.
---

# Primary Market Valuation

Use this skill to produce a defensible primary-market valuation: frame the company stage, convert the business story into numeric drivers, select methods that fit the evidence, calculate value and investor economics, and deliver a conclusion-first report with traceable assumptions.

Core principle: do not let a financing price, VC return target, market multiple, or DCF output stand alone. Reconcile them as different lenses on the same company, then state the valuation range and the assumptions that would change it.

## Reference Routing

Load only the files needed for the task:

| Need | Read |
|---|---|
| Damodaran story-to-numbers, cash flow, growth, risk, terminal value, pricing checks | `references/damodaran-method.md` |
| Combining Damodaran with VC/growth-equity valuation | `references/damodaran-primary-synthesis.md` |
| Capital budgeting or project-level incremental cash flow | `references/damodaran-project-analysis.md` |
| Official Damodaran sources, local book corpus, and current-data rules | `references/damodaran-sources.md` |
| VC Method, Scorecard, Berkus, PWERM, scenario formulas | `references/vc-methodology-reference.md` |
| Cap table, dilution, liquidation preference, participation, anti-dilution, waterfall | `references/cap-table-waterfall.md` |
| China primary-market industry and round benchmarks | `references/industry-benchmarks.md` |
| Word/PPT/report structure, chart style, deliverable checklist | `references/report-template-guide.md` |

Use `assets/config-schema-vc.json` to structure model inputs. Use `assets/example-config-sujin.json` as an example only; replace company-specific facts and assumptions.

## Sub-Skill Routing

When a primary-market valuation task needs deeper specialized work, load and follow the relevant sub-skill package before building the final integrated conclusion:

| Specialized need | Use sub-skill |
|---|---|
| Detailed DCF, intrinsic value modeling, WACC, terminal value, sensitivity tables, Monte Carlo, or Excel DCF model | `dcf-model/SKILL.md` |
| Comparable company analysis, trading multiples, operating metric benchmarking, public peer tables, IPO/funding-round pricing support | `comps-analysis/SKILL.md` |
| Competitive landscape, market map, competitor deep-dives, peer positioning, strategic market review, or competitive investment memo deck | `competitive-analysis/SKILL.md` |

Use these sub-skills as specialist modules. Return their outputs to the integrated primary-market valuation workflow, then reconcile them with VC Method, financing terms, cap table economics, scenario analysis, and the final valuation range.

## Workflow

1. Frame the assignment.
   - Define valuation date, currency, jurisdiction, target security, ownership claim, purpose, and audience.
   - Identify stage: Angel/Seed, Pre-A/A, B/C/Growth, Pre-IPO, buyout, project finance, distressed, biotech/deep tech, or other special situation.
   - Inventory user files first: BP, pitch deck, financial statements, forecast model, contracts, KPI exports, cap table, term sheet, and previous round documents.

2. Classify sources and data quality.
   - Separate `Observed`, `Company-provided`, `Public source`, `Private transaction`, `Analyst judgment`, and `Sensitivity`.
   - Browse or otherwise verify current rates, public comps, market prices, Damodaran ERP/CRP/default spreads, and recent financing data when material.
   - Do not invent missing data. Mark it as missing and either ask a targeted question or proceed with an explicit assumption.

3. Build the narrative-to-numbers bridge.
   - Translate market story into revenue drivers, market share, pricing, volume, churn, utilization, or ARR.
   - Translate competitive advantage into target margin, ROIC, retention, pricing power, and fade period.
   - Translate growth into reinvestment: capex, working capital, R&D, sales capacity, acquisitions, or sales-to-capital assumptions.
   - Translate risk into survival probability, required return, discount rate, dilution, and claim seniority.

4. Select methods by stage and evidence.
   - If the assignment explicitly requires DCF, comparable-company analysis, or competitive analysis, first route that portion to the corresponding sub-skill in `dcf-model/`, `comps-analysis/`, or `competitive-analysis/`, then integrate the output into the primary-market valuation conclusion.

| Stage / situation | Primary methods | Secondary checks | Avoid overweighting |
|---|---|---|---|
| Angel / Seed | Financing terms backsolve, VC Method, Scorecard/Berkus, comparable financing | Simple TAM/unit-economics sanity checks, exit multiple cap | Detailed DCF |
| Pre-A / A | VC Method, comparable financing, revenue/ARR multiple, terms backsolve | Scorecard, burn/runway, unit economics | Long-horizon precision DCF |
| B / C / Growth | VC Method, public comps, private transactions, PWERM | DCF if cash-flow path is credible, cap table waterfall | Single-method conclusion |
| Pre-IPO | DCF, public comps, IPO/secondary discount, PWERM | VC Method as return check | Pure seed-style VC Method |
| Biotech / deep tech | rNPV, milestone probability, comparable BD/financing deals | Cash runway, option value | Generic revenue multiple |
| Project / asset | Incremental FCFF, scenario DCF, APV if financing side effects matter | Comparable project metrics | Sunk-cost thinking |

5. Model value and investor economics.
   - Distinguish enterprise value, equity value, pre-money, post-money, per-share value, and investor proceeds.
   - Match cash flows and discount rates: FCFF with WACC, FCFE with cost of equity, nominal with nominal, real with real, RMB with RMB.
   - For VC Method, calculate exit value, ownership needed, future dilution, required MOIC/IRR, and implied current pre/post-money value.
   - For cap table work, model option pool, liquidation preference, participation, conversion, anti-dilution, warrants, SAFE/convertible notes, and waterfall proceeds.
   - Use multiples as pricing cross-checks; test peer definition, distribution, fundamentals, and applicability.

6. Reconcile the valuation range.
   - Present range before point estimate.
   - Reconcile at least four lenses when available: transaction terms, VC return math, intrinsic/narrative value, and pricing comps.
   - Explain disagreements as story differences: market size, margin, reinvestment, risk, survival, liquidity, control, and exit path.
   - Include sensitivities for the few assumptions that move the decision: exit revenue/multiple, dilution, target return, success probability, WACC/terminal growth when DCF is material.

7. Deliver and review.
   - For full reports, read `references/report-template-guide.md` before writing.
   - Generate deliverables with scripts when possible, then review outputs against sources and assumptions.
   - Include a disclaimer that the work is an analytical valuation, not regulated investment advice.

## Script Pipeline

For a full valuation package, create a project working directory and a `config.json` matching `assets/config-schema-vc.json`.

Run from this skill directory or pass absolute paths:

```bash
python3 scripts/build_charts.py --outdir output/charts/
python3 scripts/build_valuation.py --config config.json --outdir output/
python3 scripts/build_cap_table.py --config config.json --exit-value <exit_value_wan_rmb> --outdir output/
python3 scripts/build_report.py --config config.json --outdir output/
```

Use scripts as deterministic helpers, not substitutes for analyst review. Always inspect generated JSON/Word/PPT/Excel outputs for unit consistency, source labels, method fit, and hardcoded assumptions.

## Review Checklist

- Method fit matches company stage, industry, evidence quality, and valuation purpose.
- All important assumptions have source labels and dates.
- Growth is supported by reinvestment or operating capacity.
- Terminal assumptions describe a mature business and do not smuggle in high-growth economics.
- Risk is not double-counted across discount rate, cash flows, survival probability, liquidity discount, and required return.
- EV, equity value, pre-money, post-money, per-share value, and investor proceeds are not mixed.
- Cap table and waterfall terms are modeled when financing terms affect investor economics.
- Public comps and private financing comps are comparable by business model, size, growth, profitability, geography, and timing.
- Report opens with conclusion and valuation range, then supports it with evidence.
- Missing data, low-confidence data, and analyst judgment are visible to the reader.
| Pre-IPO | DCF, public comps, IPO/secondary discount, PWERM | VC Method as return check | Pure seed-style VC Method |
| Biotech / deep tech | rNPV, milestone probability, comparable BD/financing deals | Cash runway, option value | Generic revenue multiple |
| Project / asset | Incremental FCFF, scenario DCF, APV if financing side effects matter | Comparable project metrics | Sunk-cost thinking |

5. Model value and investor economics.
   - Distinguish enterprise value, equity value, pre-money, post-money, per-share value, and investor proceeds.
   - Match cash flows and discount rates: FCFF with WACC, FCFE with cost of equity, nominal with nominal, real with real, RMB with RMB.
   - For VC Method, calculate exit value, ownership needed, future dilution, required MOIC/IRR, and implied current pre/post-money value.
   - For cap table work, model option pool, liquidation preference, participation, conversion, anti-dilution, warrants, SAFE/convertible notes, and waterfall proceeds.
   - Use multiples as pricing cross-checks; test peer definition, distribution, fundamentals, and applicability.

6. Reconcile the valuation range.
   - Present range before point estimate.
   - Reconcile at least four lenses when available: transaction terms, VC return math, intrinsic/narrative value, and pricing comps.
   - Explain disagreements as story differences: market size, margin, reinvestment, risk, survival, liquidity, control, and exit path.
   - Include sensitivities for the few assumptions that move the decision: exit revenue/multiple, dilution, target return, success probability, WACC/terminal growth when DCF is material.

7. Deliver and review.
   - For full reports, read `references/report-template-guide.md` before writing.
   - Generate deliverables with scripts when possible, then review outputs against sources and assumptions.
   - Include a disclaimer that the work is an analytical valuation, not regulated investment advice.

## Script Pipeline

For a full valuation package, create a project working directory and a `config.json` matching `assets/config-schema-vc.json`.

Run from this skill directory or pass absolute paths:

```bash
python3 scripts/build_charts.py --outdir output/charts/
python3 scripts/build_valuation.py --config config.json --outdir output/
python3 scripts/build_cap_table.py --config config.json --exit-value <exit_value_wan_rmb> --outdir output/
python3 scripts/build_report.py --config config.json --outdir output/
```

Use scripts as deterministic helpers, not substitutes for analyst review. Always inspect generated JSON/Word/PPT/Excel outputs for unit consistency, source labels, method fit, and hardcoded assumptions.

## Review Checklist

- Method fit matches company stage, industry, evidence quality, and valuation purpose.
- All important assumptions have source labels and dates.
- Growth is supported by reinvestment or operating capacity.
- Terminal assumptions describe a mature business and do not smuggle in high-growth economics.
- Risk is not double-counted across discount rate, cash flows, survival probability, liquidity discount, and required return.
- EV, equity value, pre-money, post-money, per-share value, and investor proceeds are not mixed.
- Cap table and waterfall terms are modeled when financing terms affect investor economics.
- Public comps and private financing comps are comparable by business model, size, growth, profitability, geography, and timing.
- Report opens with conclusion and valuation range, then supports it with evidence.
- Missing data, low-confidence data, and analyst judgment are visible to the reader.
