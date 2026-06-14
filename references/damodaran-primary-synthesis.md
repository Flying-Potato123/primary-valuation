# Damodaran + Primary-Market Valuation Synthesis

Use this reference when combining intrinsic valuation discipline with VC, growth-equity, or financing-round analysis.

## Core Reconciliation

Primary-market valuation has four related but different lenses:

| Lens | Question answered | Common output |
|---|---|---|
| Financing terms | What price are the parties transacting at? | Pre-money, post-money, ownership sold |
| VC return math | What entry valuation supports the investor's required return after dilution? | Implied current value from exit value / target MOIC |
| Intrinsic value | What is the business worth based on cash flows, growth, risk, and reinvestment? | Enterprise/equity value range |
| Pricing comps | How are similar companies priced by current markets or private rounds? | Multiple-based range |

The final recommendation should explain why these lenses converge or diverge. A round can be investable even if the negotiated headline valuation is above a simple VC Method output, but only if rights, downside protection, strategic value, or a stronger intrinsic story justifies the gap.

## Stage Weighting

### Angel / Seed

Use financing terms, VC Method, Scorecard/Berkus, and comparable financing as the main evidence. Treat DCF as a narrative discipline rather than a precision engine.

Damodaran layer:
- Define the business story and the adoption path.
- Test whether the target market, unit economics, retention, and margin story can support the exit revenue.
- Make survival probability and dilution explicit.
- Avoid terminal-value theatrics: the useful output is usually driver plausibility, not a precise present value.

### Pre-A / A

Use VC Method and comparable financing as anchors; add revenue/ARR multiples and unit economics if early commercial traction exists.

Damodaran layer:
- Convert pipeline, contracts, pilots, or usage into measurable revenue drivers.
- Tie revenue growth to sales capacity, implementation capacity, working capital, and R&D/product investment.
- Distinguish GMV, bookings, ARR, recognized revenue, and cash collection.

### B / C / Growth

Use a multi-method range: VC Method, public comps, private transactions, and DCF/PWERM when forecasts and KPI history are credible.

Damodaran layer:
- Normalize current financials and adjust accounting where needed.
- Test margin expansion, reinvestment intensity, operating leverage, and risk fade.
- Use WACC/cost of equity only when cash-flow forecasts are meaningful enough to justify discounting.

### Pre-IPO

Use DCF, public comps, IPO discount, and PWERM as primary methods. VC Method becomes a return-check rather than the center of gravity.

Damodaran layer:
- Match cash flow type, currency, and discount rate.
- Set terminal growth below or near long-run nominal economic growth in the valuation currency.
- Reconcile intrinsic value with IPO-market pricing and liquidity discounts.

## Method Integration Rules

- Start with the company story, not the formula.
- Convert every optimistic claim into a driver: revenue growth, margin, reinvestment, risk, survival, exit multiple, or dilution.
- Use financing terms as observed price, not automatically fair value.
- Use VC Method as investor-entry math, not company intrinsic value.
- Use DCF as intrinsic value only when the business has a credible forecast path; otherwise use it to expose what must become true.
- Use public comps as pricing evidence; adjust for scale, liquidity, growth, profitability, geography, and timing.
- Use cap table waterfall to estimate investor proceeds; company value and investor economics are not the same thing.

## Damodaran Checks For VC Inputs

| VC input | Damodaran-style check |
|---|---|
| Exit revenue | Is it consistent with market size, share, pricing, capacity, and sales cycle? |
| Exit multiple | Is it consistent with growth, margin, reinvestment, ROIC, risk, and public/private liquidity? |
| Target MOIC / IRR | Does it reflect stage risk, illiquidity, fund return needs, and downside protection? |
| Dilution | Does it reflect future capital needs implied by growth and cash burn? |
| Success probability | Is failure risk captured here, in cash flows, or in discount rate, but not all three? |
| Terminal value | Does the terminal business look mature, or does it still assume venture-scale excess growth? |

## Output Reconciliation

Use a reconciliation table in reports:

| Method | Value basis | Range | Weight | Why it matters | Key weakness |
|---|---|---:|---:|---|---|
| Terms backsolve | Observed round price | | | Actual transaction anchor | May include strategic or bargaining effects |
| VC Method | Investor return requirement | | | Captures exit and dilution economics | Sensitive to exit multiple and target MOIC |
| Intrinsic DCF / narrative DCF | Cash flow, growth, risk, reinvestment | | | Tests business fundamentals | Weak for thin histories |
| Comparable financing | Private-market pricing | | | Stage-relevant market evidence | Sparse and rumor-prone data |
| Public comps | Market pricing | | | Transparent multiples | Needs liquidity/scale adjustment |
| Cap table waterfall | Investor proceeds | | | Converts company value to security value | Term details may be incomplete |

Conclude with a value range, base-case value, method weights, and the two or three assumptions that would change the decision.
