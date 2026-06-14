# Cap Table 瀑布分配完整规则

> 本文档定义了在退出情景下，投资条款如何影响各类股东的实际收益分配。AI 在执行 Cap Table 建模时必须严格遵循本文档的计算顺序。

---

## 目录

1. [基础概念](#1-基础概念)
2. [Cap Table 建模步骤](#2-cap-table-建模步骤)
3. [瀑布分配（Waterfall）计算](#3-瀑布分配waterfall计算)
4. [期权池（Option Pool）处理](#4-期权池option-pool处理)
5. [反稀释条款（Anti-dilution）](#5-反稀释条款anti-dilution)
6. [执行示例：天使轮 + A 轮 + 期权池](#6-执行示例天使轮--a-轮--期权池)
7. [常见错误](#7-常见错误)

---

## 1. 基础概念

### 1.1 关键术语

| 术语 | 英文 | 定义 |
|------|------|------|
| 投前估值 | Pre-money Valuation | 本轮投资前的公司股权价值 |
| 投后估值 | Post-money Valuation | Pre-money + 本轮投资额 |
| 清算优先权 | Liquidation Preference | 退出时优先股股东优先收回的金额 |
| 参与分配权 | Participation Rights | 优先股股东收回 LP 后是否还参与剩余分配 |
| 完全棘轮 | Full Ratchet | 反稀释：后轮价格 < 前轮价格 → 前轮价格无条件调至后轮价格 |
| 加权平均 | Weighted Average | 反稀释：根据后轮发行量和价格重新计算调整价格 |
| 期权池 | Option Pool (ESOP) | 为员工激励预留的股份，通常由创始人稀释提供 |
| MOIC | Multiple on Invested Capital | 退出收益 / 投资本金 |

### 1.2 中国一级市场常见条款

中国市场（特别是人民币基金）的典型条款组合：

| 条款 | 常见约定 | 说明 |
|------|---------|------|
| 清算优先权 | 1x, non-participating | 最常见；收回本金后不参与剩余分配 |
| 清算优先权 | 1x, participating (capped 2x-3x) | 参与分配但有上限，增长期企业常见 |
| 清算优先权 | 1.5x-2x, non-participating | 高倍数，用于高风险项目 |
| 反稀释 | 加权平均（broad-based） | 中国市场最常用 |
| 期权池 | 10%-15%（投后） | 天使/A 轮常见比例 |
| 赎回权 | 5-7 年触发 | 人民币基金常见 |

---

## 2. Cap Table 建模步骤

### Step 1: 确定估值参数

```
Input:
- 本轮投资额 = I
- 投前估值 = V_pre
- 期权池比例（投后）= ESOP%
- 现存期权池比例 = ESOP_existing%
```

### Step 2: 计算投后估值和持股比例

```
投后估值 V_post = V_pre + I

投资人持股 = I / V_post
期权池新增 = ESOP% - ESOP_existing%（如需扩容）
创始人持股 = 1 - 投资人持股 - ESOP%（投后）
```

### Step 3: 构建各轮次持股表

```
| 股东 | 股份数 | 持股比例 | 投资金额 | 每股价格 | LP 倍数 |
|------|--------|---------|---------|---------|--------|
| 创始人 | ... | ... | — | — | — |
| ESOP | ... | ... | — | — | — |
| 天使轮 | ... | ... | I_angel | P_angel | LPx_angel |
| A 轮 | ... | ... | I_A | P_A | LPx_A |
| 完全稀释总股数 | ... | 100% | ... | — | — |
```

### Step 4: 计算各轮次的每股价格

```
天使轮每股价格 = V_pre_angel / 天使轮前总股数
A 轮每股价格 = V_pre_A / A 轮前总股数（含天使轮 + ESOP）
```

---

## 3. 瀑布分配（Waterfall）计算

### 3.1 分配顺序

在退出事件中，收益按以下顺序分配：

```
优先级 1: 债务偿还（如有可转债/借款）
优先级 2: 最高优先级优先股 LP（如 B 轮优于 A 轮）
优先级 3: 次高优先级优先股 LP
优先级 4: 最低优先级优先股 LP
优先级 5: 普通股（创始人 + ESOP）

注：如果各轮次都是 pari passu（同等优先级），则按 LP 金额比例同时分配。
```

### 3.2 Non-Participating Preferred（不参与分配）

最常见的中国一级市场结构：

```
对每个优先股股东 i：
  选项 A: 收回 LP_i = Investment_i × LP_multiple_i
  选项 B: 转为普通股，按持股比例分配
  
  实际收益 = max(选项 A, 选项 B)
```

```python
def waterfall_non_participating(exit_value, investors, common_holders):
    """
    investors: list of {name, investment, lp_multiple, ownership_pct}
    common_holders: list of {name, ownership_pct}
    
    Returns: dict of {name: proceeds}
    """
    results = {}
    remaining = exit_value
    
    # Step 1: 计算每个优先股股东选择 LP 还是转股
    decisions = {}
    for inv in investors:
        lp_proceeds = inv['investment'] * inv['lp_multiple']
        convert_proceeds = exit_value * inv['ownership_pct']
        decisions[inv['name']] = 'lp' if lp_proceeds > convert_proceeds else 'convert'
    
    # Step 2: 收集选择 LP 的股东，优先分配
    lp_total = sum(inv['investment'] * inv['lp_multiple'] 
                   for inv in investors if decisions[inv['name']] == 'lp')
    
    if lp_total > exit_value:
        # 退出价值不足以覆盖所有 LP，按比例分配
        for inv in investors:
            if decisions[inv['name']] == 'lp':
                results[inv['name']] = exit_value * (inv['investment'] * inv['lp_multiple']) / lp_total
        # 普通股股东 = 0
        for c in common_holders:
            results[c['name']] = 0
        return results
    
    # 分配给选择 LP 的股东
    for inv in investors:
        if decisions[inv['name']] == 'lp':
            results[inv['name']] = inv['investment'] * inv['lp_multiple']
            remaining -= results[inv['name']]
    
    # Step 3: 剩余价值按持股比例分给转股股东 + 普通股
    convert_total_pct = sum(inv['ownership_pct'] for inv in investors 
                           if decisions[inv['name']] == 'convert')
    convert_total_pct += sum(c['ownership_pct'] for c in common_holders)
    
    for inv in investors:
        if decisions[inv['name']] == 'convert':
            results[inv['name']] = remaining * inv['ownership_pct'] / convert_total_pct
    
    for c in common_holders:
        pct = c['ownership_pct'] / convert_total_pct
        results[c['name']] = remaining * pct
    
    return results
```

### 3.3 Participating Preferred（参与分配）

优先股先收回 LP，然后**仍按持股比例**参与剩余分配：

```python
def waterfall_participating(exit_value, investors, common_holders, cap=None):
    """
    cap: 参与分配的上限倍数（如 2x 或 3x），None = 无上限
    """
    results = {}
    
    # Step 1: 所有优先股先收回 LP
    lp_paid = {}
    for inv in investors:
        lp_paid[inv['name']] = min(
            inv['investment'] * inv['lp_multiple'],
            exit_value  # 不够分时按比例
        )
    
    total_lp = sum(lp_paid.values())
    if total_lp > exit_value:
        # 按比例缩减
        for inv in investors:
            results[inv['name']] = exit_value * lp_paid[inv['name']] / total_lp
        for c in common_holders:
            results[c['name']] = 0
        return results
    
    remaining = exit_value - total_lp
    
    # Step 2: 所有股东（含优先股）按持股比例分剩余部分
    all_holders = investors + common_holders
    total_pct = sum(h['ownership_pct'] for h in all_holders)
    
    for h in all_holders:
        share = remaining * h['ownership_pct'] / total_pct
        
        if h['name'] in lp_paid:
            # 检查是否触发参与上限
            total_to_inv = lp_paid[h['name']] + share
            if cap is not None:
                max_proceeds = h['investment'] * cap
                if total_to_inv > max_proceeds:
                    share = max(0, max_proceeds - lp_paid[h['name']])
            results[h['name']] = lp_paid[h['name']] + share
        else:
            results[h['name']] = share
    
    return results
```

### 3.4 多轮次不同 LP 倍数的处理

当不同轮次有不同 LP 倍数时（如天使轮 1x、A 轮 1.5x），按**后轮优先原则**分配：

```
分配顺序：
1. A 轮投资者 LP (1.5x)
2. 天使轮投资者 LP (1x)
3. 剩余按持股比例分配
```

---

## 4. 期权池（Option Pool）处理

### 4.1 期权池对估值的影响

期权池扩容直接影响**投前估值**的经济含义：

```
情景 A: 期权池在投前扩容
  投资人投后持股 = I / V_post
  创始人（稀释后）= 1 - 投资人持股 - ESOP_new%
  创始人承担全部稀释

情景 B: 期权池在投后扩容
  投资人投后持股 = I / V_post（含期权池）
  创始人和投资人都被稀释
  → 中国市场通常为投前扩容（创始人承担稀释）
```

### 4.2 完全稀释股数计算

```python
# 计算完全稀释后的每股价值
fully_diluted_shares = (
    founder_shares 
    + sum(round['investor_shares'] for round in rounds)
    + total_esop_pool
    + outstanding_warrants
    + convertible_notes_as_if_converted
)

price_per_share = post_money_valuation / fully_diluted_shares
```

---

## 5. 反稀释条款（Anti-dilution）

### 5.1 加权平均反稀释（中国市场最常见）

```python
# Broad-based weighted average
def weighted_average_anti_dilution(
    original_price,      # 原始购买价
    new_price,           # 下轮发行价
    total_pre,           # 下轮前完全稀释总股数
    new_shares_issued    # 下轮新发行股数
):
    """
    调整价格 = 原始价格 × (total_pre + new_money / original_price) 
                        / (total_pre + new_shares_issued)
    
    其中 new_money = new_price × new_shares_issued
    """
    new_money = new_price * new_shares_issued
    adjusted_price = original_price * (
        (total_pre + new_money / original_price) 
        / (total_pre + new_shares_issued)
    )
    return adjusted_price

# 调整后的股数
# adjusted_shares = original_investment / adjusted_price
```

### 5.2 完全棘轮（Full Ratchet，较少见）

```python
# Full ratchet: 原始价格直接降到新价格
adjusted_price = min(original_price, new_price)
adjusted_shares = original_investment / adjusted_price
additional_shares = adjusted_shares - original_shares
# 额外股份通常由创始人无偿转让
```

---

## 6. 执行示例：天使轮 + A 轮 + 期权池

### 场景设定

```
初始状态：
- 创始人 1000 万股

天使轮（2024年）：
- 投资额：¥1,500 万
- 投前估值：¥13,500 万
- 投后估值：¥15,000 万
- LP 倍数：1x, non-participating
- 期权池：10%（投后新建）
- 天使轮每股价格 = 13,500 / 1,000万 = ¥1.35/股 (pre-esop)
  实际: 创始人的 1,000 万股 = 90%（因为 10% ESOP）
  所以: 总股数 = 1,000万 / 0.90 = 1,111.11 万股
  天使轮股份 = 1,111.11万 × 0.10 = 111.11 万股
  天使轮每股价格 = ¥15,000万 / 111.11万股 = ¥135/股 ? 不对...
  
正确计算：
  投后总股数 = 创始人股数 / (1 - 10% - 10%) = 1,000万 / 0.80 = 1,250万股
  ESOP = 1,250万 × 10% = 125万股
  天使轮 = 1,250万 × 10% = 125万股
  每股价格 = ¥1,500万 / 125万股 = ¥12/股
  验证: 投后估值 = 1,250万股 × ¥12/股 = ¥15,000万 ✓

A 轮（2026年）：
- 投资额：¥5,000 万
- 投前估值：¥50,000 万
- LP 倍数：1.5x, non-participating
- 期权池扩容至 15%（投后）
- A 轮前完全稀释总股数 = 1,250万股
- A 轮每股价格 = ¥50,000万 / 1,250万股 = ¥40/股
- A 轮新股 = ¥5,000万 / ¥40/股 = 125万股
- A 轮后总股数 = 1,250万 + 125万 + ESOP扩容部分
- 设 ESOP 扩容后目标 = 15% of post-A fully diluted
- post-A fully diluted = 1,375万股 / (1 - 15% - A轮比例)
- A 轮比例 = ¥5,000万 / ¥55,000万 = 9.09%

更简单的计算方法：
  A 轮投后估值 = ¥55,000万
  A 轮持股 = ¥5,000万 / ¥55,000万 = 9.09%
  ESOP 目标 = 15%
  创始人 + 天使轮 = 1 - 9.09% - 15% = 75.91%
  
  ESOP 已有 125万股 = 10%（投后）
  post-A 总股数: 
    创始人(1,000万) + 天使(125万) = 1,125万股 = 75.91%
    post-A 总 = 1,125万 / 0.7591 = 1,482万股
    A 轮新股 = 1,482万 × 9.09% = 135万股
    ESOP 总数 = 1,482万 × 15% = 222万股
    ESOP 新增 = 222万 - 125万 = 97万股（由创始人 + 天使轮按比例承担）
```

### 退出情景（2030年，IPO）

```
退出价值 = ¥70,000 万（假设）

瀑布分配（天使轮 1x non-participating, A 轮 1.5x non-participating）：

A 轮 LP 选项：
  LP: ¥5,000万 × 1.5 = ¥7,500万
  转股: ¥70,000万 × 9.09% = ¥6,363万
  → 选择 LP（¥7,500万 > ¥6,363万）

天使轮 LP 选项：
  LP: ¥1,500万 × 1.0 = ¥1,500万
  转股: (¥70,000万 - ¥7,500万) × [10% / (75.91% + 10%)] 
      = ¥62,500万 × 11.64% = ¥7,275万
  → 选择转股（¥7,275万 > ¥1,500万）

最终分配：
- A 轮投资者：¥7,500万（MOIC = 1.50x）
- 天使轮投资者：¥62,500万 × 10% / 85.91% = ¥7,275万（MOIC = 4.85x）
- 创始人：¥62,500万 × 64% / 85.91% = ¥46,553万
- ESOP：¥62,500万 × 11.87% / 85.91% = ¥8,672万
```

---

## 7. 常见错误

❌ **忽略 ESOP 扩容的稀释效应**——期权池扩容由谁承担会显著影响最终分配
❌ **混淆 non-participating 和 participating**——中国一级市场多为 non-participating
❌ **LP 倍数在退出价值不足时直接全额计入**——应该按比例分配
❌ **忽略不同轮次的 LP 优先级**——后轮通常优先于前轮
❌ **不检查转股选择**——每个优先股股东都会在 LP 和转股之间选择最优
❌ **Anti-dilution 调整后的股数不重新计算持股比例**——会影响后续所有人的百分比
