#!/usr/bin/env python3
"""
一级市场估值模型构建器
Phase 2: Model Building — VC Method + Scorecard + Comps + DCF + PWERM

用法:
  python3 build_valuation.py --config config.json --outdir output/

从 config.json 读取参数，执行所有选定的估值方法，输出：
- valuation_results.json  （结构化估值结果）
- 12张 matplotlib 图表（PNG）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import os
import sys
import json
import argparse
from pathlib import Path


# ============================================================
# Font Setup (Cross-platform, load by file path)
# ============================================================
def setup_fonts():
    """跨平台中文字体加载"""
    song_paths = [
        '/System/Library/Fonts/Supplemental/Songti.ttc',  # macOS
        '/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc',  # Linux
        'C:/Windows/Fonts/simsun.ttc'  # Windows
    ]
    hei_paths = [
        '/System/Library/Fonts/STHeiti Medium.ttc',  # macOS
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',  # Linux
        'C:/Windows/Fonts/simhei.ttf'  # Windows
    ]

    song_file = None
    hei_file = None
    for p in song_paths:
        if os.path.exists(p):
            song_file = p
            break
    for p in hei_paths:
        if os.path.exists(p):
            hei_file = p
            break

    if song_file:
        fm.fontManager.addfont(song_file)
    if hei_file:
        fm.fontManager.addfont(hei_file)

    fm._load_fontmanager(try_read_cache=False)

    hei_name = None
    song_name = None
    for f in fm.fontManager.ttflist:
        if 'eiti' in f.name and 'TC' in f.name:
            hei_name = f.name
        if 'Songti' in f.name and 'SC' in f.name:
            song_name = f.name
        # Windows fallback
        if 'SimHei' in f.name:
            hei_name = hei_name or f.name
        if 'SimSun' in f.name:
            song_name = song_name or f.name
        # Linux fallback
        if 'Noto Sans CJK' in f.name and 'Bold' in f.name:
            hei_name = hei_name or f.name
        if 'Noto Serif CJK' in f.name:
            song_name = song_name or f.name

    if not hei_name:
        hei_name = 'sans-serif'
    if not song_name:
        song_name = 'serif'

    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [hei_name, song_name, 'Arial Unicode MS', 'DejaVu Sans'],
        'axes.unicode_minus': False,
    })
    return hei_name, song_name


HEI_NAME, SONG_NAME = setup_fonts()

# Color palette
DARK_BLUE = '#1F4E79'
MED_BLUE = '#2E86AB'
LIGHT_BLUE = '#A8DADC'
ACCENT_ORANGE = '#E07A5F'
ACCENT_GREEN = '#81B29A'
ACCENT_PURPLE = '#9B5DE5'
WARM_GOLD = '#F4A261'
BG_LIGHT = '#F5F7FA'
DARK_GREY = '#4A4A4A'


# ============================================================
# 0. Config Loading
# ============================================================
def load_config(config_path):
    """加载并验证 config.json"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


def validate_config(config):
    """验证必填字段"""
    errors = []
    # Meta
    if 'meta' not in config:
        errors.append("缺少 meta 字段")
    # Company
    if 'company' not in config:
        errors.append("缺少 company 字段")
    # Round
    if 'round' not in config:
        errors.append("缺少 round 字段")
    else:
        r = config['round']
        for k in ['stage', 'round_amount', 'equity_offered']:
            if k not in r:
                errors.append(f"round 缺少 {k}")
    # Financials
    if 'financials' not in config:
        errors.append("缺少 financials 字段")
    else:
        fin = config['financials']
        if 'forecast_years' not in fin:
            errors.append("financials 缺少 forecast_years")
        if 'revenue_forecast' not in fin:
            errors.append("financials 缺少 revenue_forecast")
    # Valuation params
    if 'valuation_params' not in config:
        errors.append("缺少 valuation_params 字段")

    if errors:
        print("❌ Config 验证失败:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("✅ Config 验证通过")
    return True


# ============================================================
# 1. VC Method
# ============================================================
def vc_method(config):
    """
    VC Method 计算
    返回: list of dicts, 每个情景一个 dict
    """
    vp = config['valuation_params']['vc_method']
    round_amount = config['round']['round_amount']
    exit_value_mid = vp['exit_metric_value'] * vp['exit_multiple_range']['mid']

    # 三种退出倍数情景
    exit_values = {
        '保守': vp['exit_metric_value'] * vp['exit_multiple_range']['low'],
        '基准': vp['exit_metric_value'] * vp['exit_multiple_range']['mid'],
        '乐观': vp['exit_metric_value'] * vp['exit_multiple_range']['high'],
    }

    results = []
    for moic_label, target_moic in zip(
        ['保守', '基准', '乐观'],
        vp['target_moic_scenarios']
    ):
        for ev_label, exit_value in exit_values.items():
            required_proceeds = round_amount * target_moic
            required_ownership = required_proceeds / exit_value

            if required_ownership > 0.50:
                note = "⚠️ 所需持股超过50%，该情景不可投"
                post_money = None
                pre_money = None
            else:
                note = ""
                post_money = round_amount / required_ownership
                pre_money = post_money - round_amount

            results.append({
                'exit_scenario': ev_label,
                'moic_scenario': f'{moic_label} ({target_moic}x)',
                'target_moic': target_moic,
                'exit_value': round(exit_value, 2),
                'required_proceeds': round(required_proceeds, 2),
                'required_ownership': round(required_ownership * 100, 1),
                'required_ownership_decimal': round(required_ownership, 4),
                'post_money': round(post_money, 2) if post_money else None,
                'pre_money': round(pre_money, 2) if pre_money else None,
                'investable': required_ownership <= 0.50,
                'note': note,
            })

    # 选择基准情景（基准退出倍数 × 基准 MOIC）
    base_case = [r for r in results
                 if '基准' in r['exit_scenario'] and '基准' in r['moic_scenario']][0]

    return {
        'all_scenarios': results,
        'base_case': base_case,
        'summary': f"VC Method: {vp['exit_metric_type']}倍数法, "
                   f"退出年份 {vp['exit_year']}, "
                   f"基准退出价值 ¥{exit_value_mid:,.0f}万, "
                   f"基准投前估值 ¥{base_case['pre_money']:,.0f}万"
    }


# ============================================================
# 2. Scorecard Method
# ============================================================
def scorecard_method(config):
    """
    Scorecard 计分卡法
    """
    sc = config['valuation_params']['scorecard']
    baseline = sc['baseline_valuation']
    scores = sc['scores']

    weights = {
        'team': 0.30,
        'market': 0.25,
        'product_tech': 0.15,
        'competition': 0.10,
        'sales_marketing': 0.10,
        'other': 0.10,
    }

    weighted_score = sum(scores[k] * weights[k] for k in weights)
    pre_money = baseline * weighted_score

    return {
        'baseline_valuation': baseline,
        'baseline_source': sc['baseline_source'],
        'dimension_scores': scores,
        'dimension_weights': weights,
        'weighted_score': round(weighted_score, 3),
        'weighted_score_pct': f'{weighted_score*100:.0f}%',
        'pre_money': round(pre_money, 2),
        'premium_discount': f"{'溢价' if weighted_score > 1.0 else '折价'} {abs(weighted_score-1.0)*100:.0f}% vs 行业基准",
        'summary': f"Scorecard: 行业基准 ¥{baseline:,.0f}万, "
                   f"加权得分 {weighted_score*100:.0f}%, "
                   f"投前估值 ¥{pre_money:,.0f}万"
    }


# ============================================================
# 3. Precedent Transaction Analysis
# ============================================================
def precedent_transactions(config):
    """
    可比交易法
    """
    comps = config['valuation_params'].get('comps', {})
    transactions = comps.get('transaction_comps', [])

    if not transactions:
        return {
            'available': False,
            'note': '未提供可比交易数据'
        }

    amounts = [t['amount'] for t in transactions]
    post_moneys = [t.get('post_money', 0) for t in transactions if t.get('post_money')]

    result = {
        'available': True,
        'transaction_count': len(transactions),
        'transactions': transactions,
        'amount_range': f"¥{min(amounts):,}万 - ¥{max(amounts):,}万",
        'amount_median': round(np.median(amounts), 2),
        'amount_mean': round(np.mean(amounts), 2),
    }

    if post_moneys:
        result['post_money_median'] = round(np.median(post_moneys), 2)
        result['post_money_mean'] = round(np.mean(post_moneys), 2)
        result['post_money_range'] = f"¥{min(post_moneys):,}万 - ¥{max(post_moneys):,}万"

    if all(t.get('revenue_multiple') for t in transactions):
        multiples = [t['revenue_multiple'] for t in transactions]
        result['revenue_multiple_median'] = round(np.median(multiples), 1)
        result['revenue_multiple_range'] = f"{min(multiples):.1f}x - {max(multiples):.1f}x"

    return result


# ============================================================
# 4. DCF (简化版，用于中后期公司)
# ============================================================
def dcf_valuation(config):
    """
    简化 DCF + 风险调整（RA-NPV）
    仅在有 DCF 参数时才执行
    """
    dcf_params = config['valuation_params'].get('dcf')
    if not dcf_params:
        return {'available': False, 'note': '未配置 DCF 参数（早期阶段通常不适用）'}

    fin = config['financials']
    years = fin['forecast_years']
    revenues = [fin['revenue_forecast'][str(y)] for y in years]

    wacc = dcf_params['wacc']
    terminal_g = dcf_params['terminal_growth']
    tax_rate = dcf_params['tax_rate']
    dep_pct = dcf_params.get('depreciation_pct', 0.02)
    capex_pct = dcf_params.get('capex_pct', 0.05)
    nwc_pct = dcf_params.get('nwc_pct', 0.08)
    failure_rates = dcf_params.get('failure_rates', {})

    gross_margin = fin.get('gross_margin', 0.5)
    ebit_margins = {}
    net_margins = {}
    if isinstance(fin.get('ebit_margin'), dict):
        ebit_margins = {int(k): v for k, v in fin['ebit_margin'].items()}

    # 计算 FCF
    fcfs = []
    survival_probs = []
    cumulative_survival = 1.0

    for i, year in enumerate(years):
        revenue = revenues[i]
        yr_idx = i + 1  # 1-based

        # 确定 EBIT 利润率
        if year in ebit_margins:
            ebit_margin = ebit_margins[year]
        elif str(year) in fin.get('ebit_margin', {}):
            ebit_margin = fin['ebit_margin'][str(year)]
        else:
            # 用最近年份或插值
            ebit_margin = list(ebit_margins.values())[-1] if ebit_margins else 0.15

        ebit = revenue * ebit_margin
        nopat = ebit * (1 - tax_rate)
        depreciation = revenue * dep_pct
        capex = revenue * capex_pct
        nwc_change = revenue * nwc_pct

        fcf = nopat + depreciation - capex - nwc_change
        fcfs.append(fcf)

        # 生存概率
        fail_rate = failure_rates.get(str(yr_idx), failure_rates.get(yr_idx, 0.05))
        cumulative_survival *= (1 - fail_rate)
        survival_probs.append(cumulative_survival)

    # Terminal Value (Gordon Growth)
    last_fcf = fcfs[-1]
    terminal_value = last_fcf * (1 + terminal_g) / (wacc - terminal_g)

    # DCF (unadjusted)
    pv_fcfs = []
    for i, fcf in enumerate(fcfs):
        pv = fcf / (1 + wacc) ** (i + 1)
        pv_fcfs.append(pv)

    pv_terminal = terminal_value / (1 + wacc) ** len(years)
    enterprise_value_unadj = sum(pv_fcfs) + pv_terminal

    # Risk-adjusted (RA-NPV)
    pv_fcfs_ra = []
    for i, fcf in enumerate(fcfs):
        pv_ra = fcf * survival_probs[i] / (1 + wacc) ** (i + 1)
        pv_fcfs_ra.append(pv_ra)

    pv_terminal_ra = terminal_value * survival_probs[-1] / (1 + wacc) ** len(years)
    enterprise_value_ra = sum(pv_fcfs_ra) + pv_terminal_ra

    return {
        'available': True,
        'wacc': wacc,
        'terminal_growth': terminal_g,
        'tax_rate': tax_rate,
        'fcfs': [round(f, 2) for f in fcfs],
        'survival_probs': [round(s, 4) for s in survival_probs],
        'terminal_value': round(terminal_value, 2),
        'enterprise_value_unadj': round(enterprise_value_unadj, 2),
        'enterprise_value_ra': round(enterprise_value_ra, 2),
        'pv_terminal_pct': round(pv_terminal_ra / enterprise_value_ra * 100, 1) if enterprise_value_ra > 0 else 0,
        'summary': f"DCF: WACC={wacc*100:.0f}%, g={terminal_g*100:.1f}%, "
                   f"RA-NPV=¥{enterprise_value_ra:,.0f}万, "
                   f"未调整NPV=¥{enterprise_value_unadj:,.0f}万"
    }


# ============================================================
# 5. PWERM (Probability-Weighted Expected Return)
# ============================================================
def pwerm_analysis(config):
    """
    概率加权情景分析
    """
    pwerm = config['valuation_params'].get('pwerm')
    if not pwerm or not pwerm.get('scenarios'):
        return {'available': False, 'note': '未配置 PWERM 情景'}

    scenarios = pwerm['scenarios']
    total_prob = sum(s['probability'] for s in scenarios)

    if abs(total_prob - 1.0) > 0.01:
        print(f"⚠️ PWERM 情景概率之和 = {total_prob:.2f}，不等于 1.0")

    expected_value = sum(s['exit_value'] * s['probability'] for s in scenarios)
    weighted_exit_year = sum(s['exit_year'] * s['probability'] for s in scenarios)

    scenario_details = []
    for s in scenarios:
        contribution = s['exit_value'] * s['probability']
        scenario_details.append({
            'name': s['name'],
            'probability': s['probability'],
            'probability_pct': f"{s['probability']*100:.0f}%",
            'exit_year': s['exit_year'],
            'exit_value': s['exit_value'],
            'contribution': round(contribution, 2),
            'rationale': s.get('rationale', ''),
        })

    return {
        'available': True,
        'scenarios': scenario_details,
        'total_probability': round(total_prob, 3),
        'expected_value': round(expected_value, 2),
        'weighted_exit_year': round(weighted_exit_year, 1),
        'summary': f"PWERM: {len(scenarios)} 情景, "
                   f"概率加权预期退出价值 ¥{expected_value:,.0f}万, "
                   f"加权退出年份 {weighted_exit_year:.1f}年"
    }


# ============================================================
# 6. Weighted Valuation Synthesis
# ============================================================
def synthesize_valuation(config, vc_result, scorecard_result,
                         transactions_result, dcf_result, pwerm_result):
    """
    多方法加权综合
    """
    weights = config['valuation_params'].get('method_weights', {})
    methods = config['valuation_params'].get('methods', [])

    valuations = {}
    sources = {}

    # VC Method → pre-money
    if 'vc_method' in methods and vc_result['base_case']['pre_money']:
        valuations['VC Method'] = vc_result['base_case']['pre_money']
        sources['VC Method'] = f"退出PS倍数 {vc_result['base_case']['exit_value']/config['valuation_params']['vc_method']['exit_metric_value']:.1f}x × {vc_result['base_case']['moic_scenario']}"

    # Scorecard → pre-money
    if 'scorecard' in methods:
        valuations['Scorecard'] = scorecard_result['pre_money']
        sources['Scorecard'] = f"行业基准 {scorecard_result['baseline_valuation']:,.0f}万 × {scorecard_result['weighted_score_pct']}"

    # Precedent Transactions → post-money median
    if 'precedent_transactions' in methods and transactions_result.get('available'):
        if transactions_result.get('post_money_median'):
            post_m = transactions_result['post_money_median']
            pre_m = post_m - config['round']['round_amount']
            valuations['可比交易法'] = pre_m
            sources['可比交易法'] = f"{transactions_result['transaction_count']}笔可比交易投后中位数 ¥{post_m:,.0f}万"

    # DCF → enterprise value (RA-NPV)
    if 'dcf' in methods and dcf_result.get('available'):
        valuations['DCF (RA-NPV)'] = dcf_result['enterprise_value_ra']
        sources['DCF (RA-NPV)'] = f"WACC={dcf_result['wacc']*100:.0f}%, g={dcf_result['terminal_growth']*100:.1f}%"

    # PWERM → expected exit value, discounted
    if 'pwerm' in methods and pwerm_result.get('available'):
        # 将预期退出价值折现回当前（简化：用 DCF WACC 或默认 20%）
        disc_rate = config['valuation_params'].get('dcf', {}).get('wacc', 0.20)
        exit_years = pwerm_result['weighted_exit_year']
        pv = pwerm_result['expected_value'] / (1 + disc_rate) ** exit_years
        valuations['PWERM'] = pv
        sources['PWERM'] = f"预期退出价值 ¥{pwerm_result['expected_value']:,.0f}万 / (1+{disc_rate*100:.0f}%)^{exit_years:.1f}"

    # 加权计算
    weighted_sum = 0
    total_weight = 0
    detail_lines = []

    for method_name, val in valuations.items():
        # Map method name to weight key
        weight_key_map = {
            'VC Method': 'vc_method',
            'Scorecard': 'scorecard',
            '可比交易法': 'precedent_transactions',
            'DCF (RA-NPV)': 'dcf',
            'PWERM': 'pwerm',
        }
        wk = weight_key_map.get(method_name, '')
        w = weights.get(wk, 0)

        if w > 0:
            weighted_sum += val * w
            total_weight += w
            detail_lines.append({
                'method': method_name,
                'valuation': round(val, 2),
                'weight': w,
                'weighted_contribution': round(val * w, 2),
                'source': sources.get(method_name, ''),
            })

    if total_weight > 0:
        weighted_pre_money = weighted_sum / total_weight
    else:
        weighted_pre_money = None

    # 估值范围
    vals_list = list(valuations.values())
    if vals_list:
        val_min = min(vals_list)
        val_max = max(vals_list)
        val_median = np.median(vals_list)
    else:
        val_min = val_max = val_median = None

    # vs BP implied
    bp_pre = config['round'].get('bp_implied_pre_money')
    vs_bp = None
    if bp_pre and weighted_pre_money:
        premium = (weighted_pre_money / bp_pre - 1) * 100
        direction = '溢价' if premium > 0 else '折价'
        vs_bp = f"分析师估值加权中位数 vs BP隐含投前: {direction} {abs(premium):.0f}%"

    return {
        'individual_valuations': detail_lines,
        'valuation_range': {
            'min': round(val_min, 2) if val_min else None,
            'max': round(val_max, 2) if val_max else None,
            'median': round(val_median, 2) if val_median else None,
        },
        'weighted_pre_money': round(weighted_pre_money, 2) if weighted_pre_money else None,
        'weighted_post_money': round(weighted_pre_money + config['round']['round_amount'], 2) if weighted_pre_money else None,
        'bp_implied_pre_money': bp_pre,
        'bp_implied_post_money': config['round'].get('bp_implied_post_money'),
        'vs_bp': vs_bp,
        'total_weight': round(total_weight, 3),
        'summary': f"加权投前估值: ¥{weighted_pre_money:,.0f}万 (范围 ¥{val_min:,.0f}万 - ¥{val_max:,.0f}万)"
            if weighted_pre_money else "无法计算加权估值"
    }


# ============================================================
# 7. Chart Generation
# ============================================================
def make_charts(config, vc_result, synthesis, dcf_result, outdir):
    """生成 12 张 matplotlib 图表"""
    chart_dir = os.path.join(outdir, 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    fin = config['financials']
    years = fin['forecast_years']
    revenues = [fin['revenue_forecast'][str(y)] for y in years]

    # Chart 1: 收入预测
    fig, ax1 = plt.subplots(figsize=(10, 5))
    growth_rates = []
    for i in range(1, len(revenues)):
        growth_rates.append(revenues[i] / revenues[i-1] - 1)

    bars = ax1.bar(years, revenues, color=DARK_BLUE, alpha=0.85, label='收入（万元）')
    for bar, val in zip(bars, revenues):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenues)*0.02,
                 f'{val:,}', ha='center', va='bottom', fontsize=9)
    ax1.set_ylabel('收入（万元）', fontsize=11)
    ax1.set_title(f'{config["company"]["name"]} 收入预测', fontsize=14, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(years[1:], [g*100 for g in growth_rates], color=ACCENT_ORANGE, marker='o',
             linewidth=2, markersize=8, label='同比增长率 (%)')
    ax2.set_ylabel('同比增长率 (%)', fontsize=11, color=ACCENT_ORANGE)
    ax2.tick_params(axis='y', labelcolor=ACCENT_ORANGE)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    plt.tight_layout()
    fig.savefig(os.path.join(chart_dir, '01_revenue_forecast.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Chart 2: 盈利能力趋势
    fig, ax = plt.subplots(figsize=(10, 5))
    ebit_margins_data = []
    net_margins_data = []
    for y in years:
        ys = str(y)
        em = fin.get('ebit_margin', {}).get(ys, 0.15)
        nm = fin.get('net_margin', {}).get(ys, 0.10)
        ebit_margins_data.append(em * 100)
        net_margins_data.append(nm * 100)

    ax.plot(years, ebit_margins_data, color=MED_BLUE, marker='s', linewidth=2, markersize=8, label='EBIT利润率')
    ax.plot(years, net_margins_data, color=ACCENT_GREEN, marker='^', linewidth=2, markersize=8, label='净利润率')
    ax.fill_between(years, ebit_margins_data, alpha=0.1, color=MED_BLUE)
    ax.fill_between(years, net_margins_data, alpha=0.1, color=ACCENT_GREEN)
    ax.axhline(y=fin['gross_margin']*100, color=WARM_GOLD, linestyle='--', linewidth=1.5,
               label=f"毛利率 ({fin['gross_margin']*100:.0f}%)")
    ax.set_ylabel('利润率 (%)', fontsize=11)
    ax.set_title(f'{config["company"]["name"]} 盈利能力趋势', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(chart_dir, '02_profitability_trend.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Chart 3: VC Method 估值桥
    fig, ax = plt.subplots(figsize=(10, 6))
    bp_pre = config['round'].get('bp_implied_pre_money', 0)
    scenarios = vc_result['all_scenarios']
    investable_scenarios = [s for s in scenarios if s['investable']]

    labels = []
    values = []
    colors = []
    for s in investable_scenarios:
        label = f"{s['exit_scenario']}\n{s['moic_scenario']}"
        labels.append(label)
        values.append(s['pre_money'])
        if '保守' in s['exit_scenario']:
            colors.append(ACCENT_GREEN)
        elif '乐观' in s['exit_scenario']:
            colors.append(ACCENT_ORANGE)
        else:
            colors.append(DARK_BLUE)

    if bp_pre:
        labels.insert(0, 'BP隐含')
        values.insert(0, bp_pre)
        colors.insert(0, DARK_GREY)

    bars = ax.barh(labels, values, color=colors, height=0.6)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                f'¥{val:,.0f}万', va='center', fontsize=9)
    ax.set_xlabel('投前估值（万元）', fontsize=11)
    ax.set_title(f'{config["company"]["name"]} VC Method 估值桥', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(os.path.join(chart_dir, '03_vc_valuation_bridge.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Chart 4: 退出情景分析
    pwerm = config['valuation_params'].get('pwerm', {})
    if pwerm.get('scenarios'):
        fig, ax1 = plt.subplots(figsize=(10, 6))
        sc_names = [s['name'] for s in pwerm['scenarios']]
        sc_vals = [s['exit_value'] for s in pwerm['scenarios']]
        sc_probs = [s['probability'] for s in pwerm['scenarios']]
        sc_colors = [ACCENT_GREEN if n == 'IPO' else MED_BLUE if n == 'M&A'
                     else DARK_BLUE if n == '继续运营' else DARK_GREY for n in sc_names]

        bars = ax1.bar(sc_names, sc_vals, color=sc_colors, alpha=0.85)
        for bar, val, prob in zip(bars, sc_vals, sc_probs):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sc_vals)*0.02,
                     f'¥{val:,.0f}万\n({prob*100:.0f}%)', ha='center', fontsize=9)
        ax1.set_ylabel('退出价值（万元）', fontsize=11)
        ax1.set_title(f'{config["company"]["name"]} 退出情景分析 (PWERM)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '04_exit_scenarios.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 5: MOIC 敏感性热力图
    fig, ax = plt.subplots(figsize=(9, 7))
    moic_range = [5, 6, 7, 8, 10, 12, 15]
    ps_range = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]

    exit_metric = config['valuation_params']['vc_method']['exit_metric_value']
    round_amt = config['round']['round_amount']
    heatmap_data = np.zeros((len(moic_range), len(ps_range)))

    for i, moic in enumerate(moic_range):
        for j, ps in enumerate(ps_range):
            exit_val = exit_metric * ps
            required_own = (round_amt * moic) / exit_val
            if required_own <= 0.50:
                pre_money = round_amt / required_own - round_amt
                heatmap_data[i, j] = pre_money
            else:
                heatmap_data[i, j] = np.nan

    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    cbar = plt.colorbar(im, ax=ax, label='投前估值（万元）')
    ax.set_xticks(range(len(ps_range)))
    ax.set_xticklabels([f'{p:.1f}x' for p in ps_range])
    ax.set_yticks(range(len(moic_range)))
    ax.set_yticklabels([f'{m}x' for m in moic_range])
    ax.set_xlabel('退出PS倍数', fontsize=11)
    ax.set_ylabel('目标MOIC', fontsize=11)
    ax.set_title(f'{config["company"]["name"]} 投前估值敏感性: PS × MOIC', fontsize=14, fontweight='bold')

    for i in range(len(moic_range)):
        for j in range(len(ps_range)):
            if not np.isnan(heatmap_data[i, j]):
                text = ax.text(j, i, f'¥{heatmap_data[i,j]/10000:.1f}亿',
                              ha='center', va='center', fontsize=8,
                              color='white' if heatmap_data[i,j] > np.nanmedian(heatmap_data) else 'black')

    plt.tight_layout()
    fig.savefig(os.path.join(chart_dir, '05_moic_sensitivity.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Chart 6: 资金用途饼图
    usage = config.get('fund_usage', {})
    if usage:
        fig, ax = plt.subplots(figsize=(8, 8))
        labels = list(usage.keys())
        sizes = [v['pct'] * 100 for v in usage.values()]
        colors_pie = [DARK_BLUE, MED_BLUE, LIGHT_BLUE, ACCENT_ORANGE, ACCENT_GREEN]
        explode = [0.03] * len(labels)

        wedges, texts, autotexts = ax.pie(
            sizes, explode=explode, labels=labels, colors=colors_pie[:len(labels)],
            autopct='%1.0f%%', startangle=90, pctdistance=0.6
        )
        for t in autotexts:
            t.set_fontsize(10)
            t.set_fontweight('bold')
        ax.set_title(f'{config["company"]["name"]} 本轮融资用途\n'
                     f'(总额 ¥{config["round"]["round_amount"]:,.0f}万)',
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '06_fund_usage.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 7: 市场空间 (TAM/SAM/SOM)
    market = config.get('market_context', {})
    if market:
        fig, ax = plt.subplots(figsize=(10, 5))
        tam = market.get('tam', {})
        sam = market.get('sam', {})
        som = market.get('som', {})

        tam_val = tam.get('value', 0)
        sam_val = sam.get('value', 0)
        som_val = som.get('value', 0)

        levels = ['TAM\n(总可寻址市场)', 'SAM\n(可服务市场)', 'SOM\n(可获取市场)']
        values_mkt = [tam_val, sam_val, som_val]
        colors_mkt = [LIGHT_BLUE, MED_BLUE, DARK_BLUE]

        bars = ax.barh(levels, values_mkt, color=colors_mkt, height=0.5)
        for bar, val, level in zip(bars, values_mkt, [tam, sam, som]):
            yr = level.get('year', '')
            unit = '万亿' if val > 100000000 else '亿' if val > 10000 else '万'
            divisor = 100000000 if val > 100000000 else 10000 if val > 10000 else 1
            ax.text(bar.get_width() + max(values_mkt)*0.01, bar.get_y() + bar.get_height()/2,
                    f'¥{val/divisor:.1f}{unit} ({yr})', va='center', fontsize=10)
        ax.set_xlabel('市场规模', fontsize=11)
        ax.set_title(f'{config["company"]["name"]} 市场空间分析', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '07_market_size.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 8: 估值方法对比（估值桥）
    if synthesis.get('individual_valuations'):
        fig, ax = plt.subplots(figsize=(10, 5))
        methods_list = [d['method'] for d in synthesis['individual_valuations']]
        vals_list = [d['valuation'] for d in synthesis['individual_valuations']]
        weights_list = [d['weight'] for d in synthesis['individual_valuations']]

        colors_bridge = [DARK_BLUE, MED_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE][:len(methods_list)]
        bars = ax.barh(methods_list, vals_list, color=colors_bridge, height=0.5)
        for bar, val, w in zip(bars, vals_list, weights_list):
            ax.text(bar.get_width() + max(vals_list)*0.01, bar.get_y() + bar.get_height()/2,
                    f'¥{val:,.0f}万 (权重 {w*100:.0f}%)', va='center', fontsize=9)

        if synthesis.get('weighted_pre_money'):
            ax.axvline(x=synthesis['weighted_pre_money'], color=DARK_GREY, linestyle='--', linewidth=2,
                      label=f"加权投前: ¥{synthesis['weighted_pre_money']:,.0f}万")
        if synthesis.get('bp_implied_pre_money'):
            ax.axvline(x=synthesis['bp_implied_pre_money'], color=ACCENT_ORANGE, linestyle=':', linewidth=2,
                      label=f"BP隐含: ¥{synthesis['bp_implied_pre_money']:,.0f}万")

        ax.set_xlabel('投前估值（万元）', fontsize=11)
        ax.set_title(f'{config["company"]["name"]} 多方法估值对比', fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)
        ax.invert_yaxis()
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '08_valuation_bridge.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 9: 情景概率分布
    if pwerm.get('scenarios'):
        fig, ax = plt.subplots(figsize=(9, 6))
        sc_names = [s['name'] for s in pwerm['scenarios']]
        sc_probs = [s['probability'] * 100 for s in pwerm['scenarios']]
        sc_colors = [ACCENT_GREEN, MED_BLUE, DARK_BLUE, DARK_GREY][:len(sc_names)]

        bars = ax.bar(sc_names, sc_probs, color=sc_colors, alpha=0.85)
        for bar, prob in zip(bars, sc_probs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{prob:.0f}%', ha='center', fontsize=11, fontweight='bold')
        ax.set_ylabel('概率 (%)', fontsize=11)
        ax.set_ylim(0, max(sc_probs) * 1.3)
        ax.set_title(f'{config["company"]["name"]} 情景概率分布', fontsize=14, fontweight='bold')
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '09_scenario_probability.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 10: 稀释路径（简化版）
    fig, ax = plt.subplots(figsize=(10, 5))
    rounds = ['创始人', 'ESOP']
    ownership = [90, 10]  # simplified for Angel round only
    colors_dilution = [DARK_BLUE, ACCENT_ORANGE]

    # Project future rounds
    future_rounds = []
    if config['round']['stage'] == 'Angel':
        future_rounds = [
            ('A轮', 15),
            ('B轮', 12),
            ('C轮', 10),
            ('IPO', 8),
        ]

    for r_name, r_pct in future_rounds:
        rounds.append(r_name)
        # Dilute existing holders
        for i in range(len(ownership)):
            ownership[i] = ownership[i] * (1 - r_pct / 100)
        ownership.append(r_pct)

    bottom = np.zeros(1)
    all_rounds = rounds
    all_colors = [DARK_BLUE, ACCENT_ORANGE, MED_BLUE, ACCENT_GREEN, ACCENT_PURPLE, WARM_GOLD]

    for i, (name, pct) in enumerate(zip(rounds, ownership)):
        color_idx = min(i, len(all_colors) - 1)
        ax.bar(0, pct, bottom=bottom, color=all_colors[color_idx], label=name, alpha=0.85)
        bottom += pct

    ax.set_xlim(-0.5, len(future_rounds) + 0.5)
    ax.set_ylabel('持股比例 (%)', fontsize=11)
    ax.set_title(f'{config["company"]["name"]} 稀释路径预测', fontsize=14, fontweight='bold')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    ax.set_xticks([])
    plt.tight_layout()
    fig.savefig(os.path.join(chart_dir, '10_dilution_path.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Chart 11: 可比交易对比
    transactions = config['valuation_params'].get('comps', {}).get('transaction_comps', [])
    if transactions:
        fig, ax = plt.subplots(figsize=(10, 5))
        t_names = [t['target_name'][:10] for t in transactions]
        t_amounts = [t['amount'] for t in transactions]
        t_post = [t.get('post_money', 0) for t in transactions]

        x = np.arange(len(t_names))
        width = 0.35
        bars1 = ax.bar(x - width/2, t_amounts, width, color=MED_BLUE, alpha=0.85, label='融资金额（万元）')
        bars2 = ax.bar(x + width/2, t_post, width, color=ACCENT_ORANGE, alpha=0.85, label='投后估值（万元）')
        ax.set_xticks(x)
        ax.set_xticklabels(t_names, fontsize=9)
        ax.set_ylabel('金额（万元）', fontsize=11)
        ax.set_title(f'{config["company"]["name"]} vs 可比天使轮交易', fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '11_comparable_rounds.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # Chart 12: 增长 vs 利润率散点图（vs 可比公司）
    public_comps = config['valuation_params'].get('comps', {}).get('public_comps', [])
    if public_comps:
        fig, ax = plt.subplots(figsize=(10, 7))
        # 可比公司
        comp_names = [c['name'] for c in public_comps]
        comp_growth = [c['growth_rate'] * 100 for c in public_comps]
        comp_margin = [c['gross_margin'] * 100 for c in public_comps]
        comp_sizes = [c['revenue_ttm'] / 10000 for c in public_comps]  # 转为亿

        scatter = ax.scatter(comp_growth, comp_margin, s=[s*2 for s in comp_sizes],
                            c=comp_sizes, cmap='Blues', alpha=0.7, edgecolors='white', linewidth=1)

        for i, name in enumerate(comp_names):
            ax.annotate(name, (comp_growth[i], comp_margin[i]),
                       textcoords="offset points", xytext=(5, 5), fontsize=8)

        # 岁锦科技
        sujin_growth = (revenues[-1] / revenues[0]) ** (1/len(revenues)) - 1
        sujin_margin = fin['gross_margin'] * 100
        ax.scatter([sujin_growth*100], [sujin_margin], s=300, color=ACCENT_ORANGE,
                  edgecolors=DARK_BLUE, linewidth=2, marker='*', zorder=5,
                  label=f'{config["company"]["name"]} (预测均值)')

        cbar = plt.colorbar(scatter, ax=ax, label='收入规模（亿元 TTM）')
        ax.set_xlabel('收入增长率 (%)', fontsize=11)
        ax.set_ylabel('毛利率 (%)', fontsize=11)
        ax.set_title(f'{config["company"]["name"]} vs 可比公司: 增长 vs 利润率', fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        fig.savefig(os.path.join(chart_dir, '12_growth_margin_scatter.png'), dpi=150, bbox_inches='tight')
        plt.close()

    print(f"✅ 图表已生成至 {chart_dir}/ (共12张)")


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='一级市场估值模型构建器 - VC Method + Scorecard + Comps + DCF + PWERM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 build_valuation.py --config example-config.json --outdir output/
  python3 build_valuation.py --config config.json --outdir . --no-charts
        """
    )
    parser.add_argument('--config', required=True, help='config.json 文件路径')
    parser.add_argument('--outdir', default='.', help='输出目录 (默认: 当前目录)')
    parser.add_argument('--no-charts', action='store_true', help='跳过图表生成')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # Load & validate config
    print(f"📂 加载配置文件: {args.config}")
    config = load_config(args.config)
    validate_config(config)

    company = config['company']['name']
    stage = config['round']['stage']
    methods = config['valuation_params']['methods']
    print(f"\n{'='*60}")
    print(f"  {company} | {stage} | 估值方法: {', '.join(methods)}")
    print(f"{'='*60}\n")

    # Execute methods
    results = {}

    # 1. VC Method (always for early-stage)
    if 'vc_method' in methods:
        print("🔢 执行 VC Method...")
        vc_result = vc_method(config)
        results['vc_method'] = vc_result
        print(f"  {vc_result['summary']}")

    # 2. Scorecard
    if 'scorecard' in methods:
        print("📊 执行 Scorecard Method...")
        scorecard_result = scorecard_method(config)
        results['scorecard'] = scorecard_result
        print(f"  {scorecard_result['summary']}")

    # 3. Precedent Transactions
    if 'precedent_transactions' in methods:
        print("📋 执行可比交易分析...")
        transactions_result = precedent_transactions(config)
        results['precedent_transactions'] = transactions_result
        if transactions_result['available']:
            print(f"  {transactions_result['transaction_count']}笔可比交易, "
                  f"投后中位数 ¥{transactions_result.get('post_money_median', 'N/A')}万")

    # 4. DCF
    if 'dcf' in methods:
        print("💰 执行 DCF 估值...")
        dcf_result = dcf_valuation(config)
        results['dcf'] = dcf_result
        if dcf_result['available']:
            print(f"  {dcf_result['summary']}")

    # 5. PWERM
    if 'pwerm' in methods:
        print("🎲 执行 PWERM 情景分析...")
        pwerm_result = pwerm_analysis(config)
        results['pwerm'] = pwerm_result
        if pwerm_result['available']:
            print(f"  {pwerm_result['summary']}")

    # Synthesize
    print("\n🔗 综合多方法估值...")
    synthesis = synthesize_valuation(
        config,
        results.get('vc_method', {'base_case': {'pre_money': None}}),
        results.get('scorecard', {'pre_money': None}),
        results.get('precedent_transactions', {'available': False}),
        results.get('dcf', {'available': False}),
        results.get('pwerm', {'available': False}),
    )
    results['synthesis'] = synthesis

    print(f"\n{'='*60}")
    if synthesis.get('summary'):
        print(f"  {synthesis['summary']}")
    if synthesis.get('vs_bp'):
        print(f"  {synthesis['vs_bp']}")
    print(f"{'='*60}")

    # Generate charts
    if not args.no_charts:
        print("\n📈 生成图表...")
        make_charts(config, results.get('vc_method', {'all_scenarios': []}),
                   synthesis, results.get('dcf', {}), args.outdir)

    # Save results JSON
    output_file = os.path.join(args.outdir, 'valuation_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 估值结果已保存至 {output_file}")

    # Print summary table
    print(f"\n{'─'*50}")
    print(f"  {company} | {stage} | {config['meta']['valuation_date']}")
    print(f"{'─'*50}")
    if synthesis.get('individual_valuations'):
        for d in synthesis['individual_valuations']:
            print(f"  {d['method']:20s}  ¥{d['valuation']:>12,.0f}万  (权重 {d['weight']*100:.0f}%)")
        print(f"  {'─'*50}")
        print(f"  {'加权投前估值':20s}  ¥{synthesis['weighted_pre_money']:>12,.0f}万")
        print(f"  {'估值范围':20s}  ¥{synthesis['valuation_range']['min']:,.0f}万 - ¥{synthesis['valuation_range']['max']:,.0f}万")

    return results


if __name__ == '__main__':
    main()
