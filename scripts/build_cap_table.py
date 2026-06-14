#!/usr/bin/env python3
"""
Cap Table 构建与瀑布分配分析
Phase 2: Model Building — Cap Table + Waterfall + Dilution Analysis

用法:
  python3 build_cap_table.py --config config.json --outdir output/

功能:
1. 构建当前轮次 Cap Table（含期权池）
2. 模拟多轮融资稀释路径
3. 瀑布分配计算（Non-Participating / Participating Preferred）
4. 反稀释调整（加权平均法）
5. 输出 cap_table.json 和 cap_table.csv
"""

import json
import os
import sys
import argparse
import csv
import copy
from pathlib import Path


# ============================================================
# Helper Functions
# ============================================================
def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def fmt_wan(val):
    """格式化万元金额"""
    if val is None:
        return 'N/A'
    if abs(val) >= 10000:
        return f'¥{val/10000:.2f}亿'
    return f'¥{val:,.0f}万'


def fmt_pct(val):
    """格式化百分比"""
    if val is None:
        return 'N/A'
    return f'{val*100:.1f}%'


# ============================================================
# 1. Build Current Cap Table
# ============================================================
def build_current_cap_table(config):
    """
    构建当前轮次 Cap Table
    返回: dict with shareholders, fully_diluted_shares, price_per_share, etc.
    """
    cap = config.get('capital_structure', {})
    rnd = config['round']

    founder_shares = cap.get('founder_shares', 1000)  # 万股
    target_esop_pct = cap.get('target_esop_pct', 0.10)
    existing_esop_pct = cap.get('existing_esop_pct', 0.0)
    esop_burden = cap.get('esop_expansion_burden', 'pre_money')
    round_amount = rnd['round_amount']
    equity_offered = rnd['equity_offered']

    # Prior rounds
    prior_rounds = cap.get('prior_rounds', [])

    # === Step 1: Calculate total shares pre-round ===
    # Founder shares + ESOP (existing) + prior investors
    total_existing_pct_for_founder = 1.0 - existing_esop_pct - sum(
        r.get('ownership_pct', 0) for r in prior_rounds
    )

    # Founder shares represent this percentage
    if total_existing_pct_for_founder > 0:
        total_existing_shares = founder_shares / total_existing_pct_for_founder
    else:
        total_existing_shares = founder_shares

    existing_esop_shares = total_existing_shares * existing_esop_pct

    # Prior investor shares
    prior_investor_shares = {}
    for r in prior_rounds:
        pct = r.get('ownership_pct', 0)
        shares = total_existing_shares * pct
        prior_investor_shares[r['name']] = {
            'shares': shares,
            'ownership_pct': pct,
            'investment': r.get('investment', 0),
            'lp_multiple': r.get('lp_multiple', 1.0),
            'participating': r.get('participating', False),
            'participation_cap': r.get('participation_cap'),
            'seniority': r.get('seniority', 1),
            'anti_dilution': r.get('anti_dilution', 'none'),
        }

    # === Step 2: ESOP expansion ===
    esop_expansion_needed = max(0, target_esop_pct - existing_esop_pct)

    if esop_burden == 'pre_money':
        # Founder bears the dilution entirely
        # Post-money total shares: founder_shares represents (1 - target_esop - investor_pct)
        investor_pct = equity_offered
        founder_post_pct = 1.0 - target_esop_pct - investor_pct

        if founder_post_pct > 0:
            fully_diluted_shares = founder_shares / founder_post_pct
        else:
            fully_diluted_shares = total_existing_shares / (1.0 - target_esop_pct - investor_pct)

        new_investor_shares = fully_diluted_shares * investor_pct
        total_esop_shares = fully_diluted_shares * target_esop_pct
        esop_new_shares = total_esop_shares - existing_esop_shares

    elif esop_burden == 'post_money':
        # All existing shareholders diluted pro-rata
        investor_pct = equity_offered
        post_money_total = total_existing_shares / (1.0 - target_esop_pct - investor_pct)
        fully_diluted_shares = post_money_total
        new_investor_shares = fully_diluted_shares * investor_pct
        total_esop_shares = fully_diluted_shares * target_esop_pct
        esop_new_shares = total_esop_shares - existing_esop_shares

    else:  # pro_rata
        investor_pct = equity_offered
        post_money_total = total_existing_shares / (1.0 - target_esop_pct - investor_pct)
        fully_diluted_shares = post_money_total
        new_investor_shares = fully_diluted_shares * investor_pct
        total_esop_shares = fully_diluted_shares * target_esop_pct
        esop_new_shares = total_esop_shares - existing_esop_shares

    # === Step 3: Post-money valuation and per-share price ===
    post_money_val = round_amount / equity_offered
    price_per_share = round_amount / new_investor_shares if new_investor_shares > 0 else 0
    pre_money_val = post_money_val - round_amount

    # === Step 4: Build shareholder list ===
    shareholders = []

    # Founder
    founder_pct = founder_shares / fully_diluted_shares
    shareholders.append({
        'name': '创始人',
        'type': 'common',
        'shares': round(founder_shares, 4),
        'ownership_pct': round(founder_pct, 4),
        'investment': 0,
        'price_per_share': 0,
        'lp_multiple': None,
        'participating': False,
        'seniority': 0,
    })

    # Existing ESOP
    shareholders.append({
        'name': 'ESOP',
        'type': 'common',
        'shares': round(total_esop_shares, 4),
        'ownership_pct': round(target_esop_pct, 4),
        'investment': 0,
        'price_per_share': 0,
        'lp_multiple': None,
        'participating': False,
        'seniority': 0,
    })

    # Prior investors (adjusted for dilution)
    for name, info in prior_investor_shares.items():
        diluted_pct = info['shares'] / fully_diluted_shares
        shareholders.append({
            'name': name,
            'type': 'preferred',
            'shares': round(info['shares'], 4),
            'ownership_pct': round(diluted_pct, 4),
            'investment': info['investment'],
            'price_per_share': round(info['investment'] / info['shares'], 4) if info['shares'] > 0 else 0,
            'lp_multiple': info['lp_multiple'],
            'participating': info['participating'],
            'participation_cap': info['participation_cap'],
            'seniority': info['seniority'],
            'anti_dilution': info['anti_dilution'],
        })

    # New investor (current round)
    shareholders.append({
        'name': f"{rnd['stage']}轮投资者",
        'type': 'preferred',
        'shares': round(new_investor_shares, 4),
        'ownership_pct': round(investor_pct, 4),
        'investment': round_amount,
        'price_per_share': round(price_per_share, 4),
        'lp_multiple': 1.0,  # default 1x, can be overridden in config
        'participating': False,
        'participation_cap': None,
        'seniority': len(prior_rounds) + 1,  # latest round = highest seniority
        'anti_dilution': 'weighted_average_broad',
    })

    return {
        'config': {
            'founder_shares_wg': founder_shares,
            'target_esop_pct': target_esop_pct,
            'existing_esop_pct': existing_esop_pct,
            'esop_burden': esop_burden,
            'esop_new_shares': round(esop_new_shares, 4),
            'round_amount': round_amount,
            'equity_offered': equity_offered,
        },
        'pre_money_valuation': round(pre_money_val, 2),
        'post_money_valuation': round(post_money_val, 2),
        'price_per_share': round(price_per_share, 4),
        'fully_diluted_shares': round(fully_diluted_shares, 4),
        'shareholders': shareholders,
        'verification': {
            'total_ownership': round(sum(s['ownership_pct'] for s in shareholders), 4),
            'total_shares': round(sum(s['shares'] for s in shareholders), 4),
        }
    }


# ============================================================
# 2. Dilution Path Simulation
# ============================================================
def simulate_dilution_path(config, cap_table):
    """
    模拟未来多轮融资的稀释路径
    """
    stage = config['round']['stage']
    round_sequence = []

    if stage == 'Angel':
        round_sequence = [
            {'name': 'A轮', 'new_money_pct': 0.15, 'esop_new': 0.05},
            {'name': 'B轮', 'new_money_pct': 0.12, 'esop_new': 0.03},
            {'name': 'C轮', 'new_money_pct': 0.10, 'esop_new': 0.02},
            {'name': 'IPO', 'new_money_pct': 0.08, 'esop_new': 0.0},
        ]
    elif stage == 'A':
        round_sequence = [
            {'name': 'B轮', 'new_money_pct': 0.12, 'esop_new': 0.03},
            {'name': 'C轮', 'new_money_pct': 0.10, 'esop_new': 0.02},
            {'name': 'IPO', 'new_money_pct': 0.08, 'esop_new': 0.0},
        ]
    elif stage == 'B':
        round_sequence = [
            {'name': 'C轮', 'new_money_pct': 0.10, 'esop_new': 0.02},
            {'name': 'IPO', 'new_money_pct': 0.08, 'esop_new': 0.0},
        ]
    else:
        round_sequence = [
            {'name': 'IPO', 'new_money_pct': 0.05, 'esop_new': 0.0},
        ]

    # Start with current ownership
    current = {s['name']: s['ownership_pct'] for s in cap_table['shareholders']}
    path = [{'round': '当前轮次', 'ownership': copy.deepcopy(current)}]

    for r in round_sequence:
        dilution_factor = 1.0 - r['new_money_pct'] - r['esop_new']
        new_current = {}

        # Existing holders diluted
        for name, pct in current.items():
            new_current[name] = pct * dilution_factor

        # New ESOP
        if r['esop_new'] > 0:
            new_current['ESOP'] = new_current.get('ESOP', 0) + r['esop_new']

        # New investor
        new_current[f"{r['name']}投资者"] = r['new_money_pct']

        path.append({'round': r['name'], 'ownership': copy.deepcopy(new_current)})
        current = new_current

    return path


# ============================================================
# 3. Waterfall Distribution
# ============================================================
def waterfall_distribution(exit_value, shareholders):
    """
    瀑布分配计算
    支持 Non-Participating 和 Participating (with cap) Preferred

    exit_value: 退出时的总股权价值（万元）
    shareholders: list of dicts from cap_table

    Returns: dict with per-shareholder proceeds and MOIC
    """
    # Separate preferred (with seniority) and common
    preferred = sorted(
        [s for s in shareholders if s['type'] == 'preferred'],
        key=lambda x: x.get('seniority', 0),
        reverse=True  # higher seniority first
    )
    common = [s for s in shareholders if s['type'] == 'common']

    # === Non-Participating Preferred ===
    # Step 1: Each preferred holder decides: LP or convert?
    decisions_np = {}
    for p in preferred:
        lp_proceeds = p['investment'] * p.get('lp_multiple', 1.0)
        convert_proceeds = exit_value * p['ownership_pct']
        decisions_np[p['name']] = 'lp' if lp_proceeds > convert_proceeds else 'convert'

    # Step 2: Pay LP takers by seniority
    remaining_np = exit_value
    results_np = {}

    # Sort LP takers by seniority
    lp_takers = sorted(
        [p for p in preferred if decisions_np[p['name']] == 'lp'],
        key=lambda x: x.get('seniority', 0),
        reverse=True
    )

    for p in lp_takers:
        lp_due = p['investment'] * p.get('lp_multiple', 1.0)
        if remaining_np >= lp_due:
            results_np[p['name']] = lp_due
            remaining_np -= lp_due
        else:
            results_np[p['name']] = remaining_np
            remaining_np = 0

    # If remaining > 0 but more LP takers unpaid → pro-rata among remaining LP takers
    unpaid_lp = [p for p in lp_takers if p['name'] not in results_np]
    if unpaid_lp and remaining_np > 0:
        total_lp_due = sum(p['investment'] * p.get('lp_multiple', 1.0) for p in unpaid_lp)
        for p in unpaid_lp:
            lp_due = p['investment'] * p.get('lp_multiple', 1.0)
            results_np[p['name']] = remaining_np * lp_due / total_lp_due
        remaining_np = 0

    # Step 3: Remaining distributed to convert-takers + common by ownership
    convert_takers = [p for p in preferred if decisions_np[p['name']] == 'convert']
    all_convert_pct = sum(p['ownership_pct'] for p in convert_takers) + sum(c['ownership_pct'] for c in common)

    if all_convert_pct > 0 and remaining_np > 0:
        for p in convert_takers:
            results_np[p['name']] = remaining_np * p['ownership_pct'] / all_convert_pct
        for c in common:
            results_np[c['name']] = remaining_np * c['ownership_pct'] / all_convert_pct

    # === Participating Preferred ===
    results_p = {}
    remaining_p = exit_value

    # All preferred take LP first (by seniority)
    for p in preferred:
        lp_due = p['investment'] * p.get('lp_multiple', 1.0)
        if remaining_p >= lp_due:
            results_p[p['name']] = lp_due
            remaining_p -= lp_due
        else:
            results_p[p['name']] = remaining_p
            remaining_p = 0

    # Then all shareholders (including preferred) participate pro-rata in remaining
    if remaining_p > 0:
        total_pct_all = sum(s['ownership_pct'] for s in shareholders)
        for s in shareholders:
            share = remaining_p * s['ownership_pct'] / total_pct_all

            if s['type'] == 'preferred' and s['name'] in results_p:
                # Check participation cap
                cap_mult = s.get('participation_cap')
                if cap_mult is not None:
                    max_proceeds = s['investment'] * cap_mult
                    current_total = results_p[s['name']] + share
                    if current_total > max_proceeds:
                        share = max(0, max_proceeds - results_p[s['name']])
                results_p[s['name']] += share
            else:
                results_p[s['name']] = results_p.get(s['name'], 0) + share

    # Calculate MOIC for each
    def calc_moic(results_dict, shareholders):
        moic = {}
        for s in shareholders:
            proceeds = results_dict.get(s['name'], 0)
            if s['investment'] > 0 and proceeds > 0:
                moic[s['name']] = round(proceeds / s['investment'], 2)
            elif s['investment'] > 0:
                moic[s['name']] = 0.0
            else:
                moic[s['name']] = None  # founder/ESOP don't have "MOIC"
        return moic

    return {
        'exit_value': exit_value,
        'non_participating': {
            'description': 'Non-Participating Preferred (不参与分配)',
            'decisions': decisions_np,
            'proceeds': {k: round(v, 2) for k, v in results_np.items()},
            'moic': calc_moic(results_np, shareholders),
            'total_distributed': round(sum(results_np.values()), 2),
            'verification': round(abs(sum(results_np.values()) - exit_value), 2),
        },
        'participating': {
            'description': 'Participating Preferred (参与分配)',
            'proceeds': {k: round(v, 2) for k, v in results_p.items()},
            'moic': calc_moic(results_p, shareholders),
            'total_distributed': round(sum(results_p.values()), 2),
            'verification': round(abs(sum(results_p.values()) - exit_value), 2),
        }
    }


# ============================================================
# 4. Anti-Dilution Adjustment
# ============================================================
def weighted_average_anti_dilution(original_price, new_price, total_pre_shares, new_shares_issued):
    """
    Broad-based Weighted Average Anti-Dilution

    Adjusted Price = Original Price × (A + B) / (A + C)
    where:
      A = total shares before new round (fully diluted)
      B = new investment / original price (= shares that would have been issued at old price)
      C = new shares actually issued
    """
    if new_price >= original_price:
        # No adjustment needed (up round)
        return original_price, 0

    new_investment = new_price * new_shares_issued
    B = new_investment / original_price  # shares at old price
    A = total_pre_shares
    C = new_shares_issued

    adjusted_price = original_price * (A + B) / (A + C)
    additional_shares_pct = (original_price / adjusted_price - 1) * 100

    return adjusted_price, additional_shares_pct


def apply_anti_dilution(config, cap_table, down_round_price):
    """
    对 cap_table 中的所有受保护优先股应用反稀释调整
    down_round_price: 假设的下轮每股价格（低于当前价格即触发）
    """
    current_price = cap_table['price_per_share']
    total_shares = cap_table['fully_diluted_shares']

    adjustments = []
    for s in cap_table['shareholders']:
        if s['type'] != 'preferred':
            continue

        anti_dilution = s.get('anti_dilution', 'none')
        if anti_dilution == 'none':
            continue

        original_price = s['price_per_share']

        if down_round_price >= original_price:
            continue  # not triggered

        # Calculate new shares issued in down round
        new_money = config['round']['round_amount']  # simplified: assume same round size
        new_shares = new_money / down_round_price

        if anti_dilution == 'weighted_average_broad':
            adj_price, extra_pct = weighted_average_anti_dilution(
                original_price, down_round_price, total_shares, new_shares
            )
            adj_shares = s['investment'] / adj_price
            extra_shares = adj_shares - s['shares']
            adjustments.append({
                'shareholder': s['name'],
                'method': '加权平均 (Broad-based)',
                'original_price': round(original_price, 4),
                'down_round_price': round(down_round_price, 4),
                'adjusted_price': round(adj_price, 4),
                'original_shares': round(s['shares'], 4),
                'adjusted_shares': round(adj_shares, 4),
                'extra_shares': round(extra_shares, 4),
                'extra_shares_pct': round(extra_pct, 1),
                'note': f"需创始人补偿 {round(extra_shares, 4)}万股"
            })

        elif anti_dilution == 'full_ratchet':
            adj_price = down_round_price
            adj_shares = s['investment'] / adj_price
            extra_shares = adj_shares - s['shares']
            adjustments.append({
                'shareholder': s['name'],
                'method': '完全棘轮 (Full Ratchet)',
                'original_price': round(original_price, 4),
                'down_round_price': round(down_round_price, 4),
                'adjusted_price': round(adj_price, 4),
                'original_shares': round(s['shares'], 4),
                'adjusted_shares': round(adj_shares, 4),
                'extra_shares': round(extra_shares, 4),
                'extra_shares_pct': round((s['shares'] / adj_shares) * 100, 1),
                'note': f"⚠️ 完全棘轮触发！需创始人补偿 {round(extra_shares, 4)}万股"
            })

    return adjustments


# ============================================================
# 5. Export
# ============================================================
def export_cap_table_csv(cap_table, outdir):
    """导出 Cap Table 为 CSV"""
    path = os.path.join(outdir, 'cap_table.csv')
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['股东', '类型', '股数(万股)', '持股比例', '投资额(万元)',
                        '每股价格(元)', 'LP倍数', '参与分配', '优先级'])
        for s in cap_table['shareholders']:
            writer.writerow([
                s['name'], s['type'], s['shares'], f"{s['ownership_pct']*100:.1f}%",
                s['investment'], s['price_per_share'],
                s.get('lp_multiple', '-'), s.get('participating', '-'),
                s.get('seniority', '-'),
            ])
    print(f"✅ Cap Table CSV 已保存至 {path}")


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='Cap Table 构建与瀑布分配分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 build_cap_table.py --config example-config.json --outdir output/
  python3 build_cap_table.py --config config.json --exit-value 700000 --down-round-price 20
        """
    )
    parser.add_argument('--config', required=True, help='config.json 文件路径')
    parser.add_argument('--outdir', default='.', help='输出目录')
    parser.add_argument('--exit-value', type=float, default=700000,
                       help='退出股权价值（万元），用于瀑布分配分析 (默认: 700000)')
    parser.add_argument('--down-round-price', type=float, default=None,
                       help='假设的下轮每股价格（元），用于反稀释分析。不指定则跳过反稀释分析。')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    print(f"📂 加载配置: {args.config}")
    config = load_config(args.config)

    company = config['company']['name']
    stage = config['round']['stage']

    print(f"\n{'='*60}")
    print(f"  {company} | {stage} | Cap Table & 瀑布分配分析")
    print(f"{'='*60}\n")

    # 1. Build Cap Table
    print("📊 构建当前轮次 Cap Table...")
    cap_table = build_current_cap_table(config)

    print(f"  投前估值:     {fmt_wan(cap_table['pre_money_valuation'])}")
    print(f"  投后估值:     {fmt_wan(cap_table['post_money_valuation'])}")
    print(f"  完全稀释股数: {cap_table['fully_diluted_shares']:,.2f}万股")
    print(f"  每股价格:     ¥{cap_table['price_per_share']:,.2f}/股")
    print(f"  期权池扩容:   {cap_table['config']['esop_new_shares']:,.2f}万股 (新增)")
    print(f"  总持股验证:   {cap_table['verification']['total_ownership']*100:.1f}% "
          f"(应为100%)")

    print(f"\n  股东结构:")
    print(f"  {'股东':20s} {'类型':10s} {'股数(万股)':>12s} {'持股比例':>10s} {'投资额':>12s}")
    print(f"  {'─'*70}")
    for s in cap_table['shareholders']:
        print(f"  {s['name']:20s} {s['type']:10s} {s['shares']:>12.2f} "
              f"{s['ownership_pct']*100:>9.1f}% {fmt_wan(s['investment']):>12s}")

    # 2. Dilution Path
    print(f"\n🔄 模拟稀释路径...")
    dilution_path = simulate_dilution_path(config, cap_table)

    print(f"  {'轮次':12s} ", end='')
    # Print header with shareholder names
    main_holders = [s['name'] for s in cap_table['shareholders'] if s['ownership_pct'] > 0.02]
    for h in main_holders:
        print(f"{h:>10s} ", end='')
    print()
    print(f"  {'─'*12} {'─'*len(main_holders)*11}")

    for step in dilution_path:
        rnd_name = step['round']
        print(f"  {rnd_name:12s} ", end='')
        for h in main_holders:
            pct = step['ownership'].get(h, 0) * 100
            print(f"{pct:>9.1f}% ", end='')
        print()

    # 3. Waterfall
    print(f"\n🌊 瀑布分配分析 (退出价值 = {fmt_wan(args.exit_value)})...")
    waterfall = waterfall_distribution(args.exit_value, cap_table['shareholders'])

    for wp_type in ['non_participating', 'participating']:
        wp = waterfall[wp_type]
        print(f"\n  [{wp['description']}]")
        if wp_type == 'non_participating' and 'decisions' in wp:
            print(f"  优先股选择:")
            for name, decision in wp['decisions'].items():
                print(f"    {name}: {'收回LP' if decision == 'lp' else '转为普通股'}")

        print(f"  {'股东':20s} {'分配金额':>15s} {'MOIC':>8s} {'占总额':>8s}")
        print(f"  {'─'*55}")
        for s in cap_table['shareholders']:
            proceeds = wp['proceeds'].get(s['name'], 0)
            moic = wp['moic'].get(s['name'])
            pct_of_total = proceeds / args.exit_value * 100 if args.exit_value > 0 else 0
            moic_str = f'{moic:.2f}x' if moic is not None else '-'
            print(f"  {s['name']:20s} {fmt_wan(proceeds):>15s} {moic_str:>8s} {pct_of_total:>7.1f}%")

        print(f"  {'总计':20s} {fmt_wan(wp['total_distributed']):>15s}")
        if wp['verification'] > 0.01:
            print(f"  ⚠️ 差额: {fmt_wan(wp['verification'])} (应为0)")

    # 4. Anti-Dilution (if requested)
    if args.down_round_price:
        print(f"\n🛡️ 反稀释分析 (下轮价格 ¥{args.down_round_price:.2f}/股)...")
        adj = apply_anti_dilution(config, cap_table, args.down_round_price)
        if adj:
            for a in adj:
                print(f"  {a['shareholder']}: {a['method']}")
                print(f"    原始价格: ¥{a['original_price']:.2f} → 调整价格: ¥{a['adjusted_price']:.2f}")
                print(f"    原始股数: {a['original_shares']:.2f}万股 → 调整股数: {a['adjusted_shares']:.2f}万股")
                print(f"    需补偿: {a['extra_shares']:.2f}万股 ({a['extra_shares_pct']:.1f}%)")
                print(f"    {a['note']}")
        else:
            print(f"  无反稀释触发（当前价格 ¥{cap_table['price_per_share']:.2f} ≥ "
                  f"下轮价格 ¥{args.down_round_price:.2f}，或无限价保护条款）")

    # 5. Export
    all_results = {
        'cap_table': cap_table,
        'dilution_path': dilution_path,
        'waterfall': waterfall,
    }
    if args.down_round_price:
        all_results['anti_dilution'] = adj

    output_file = os.path.join(args.outdir, 'cap_table.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    export_cap_table_csv(cap_table, args.outdir)

    print(f"\n✅ Cap Table 分析结果已保存至 {output_file}")
    return all_results


if __name__ == '__main__':
    main()
