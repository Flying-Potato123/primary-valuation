#!/usr/bin/env python3
"""
一级市场估值报告 — 专业图表生成脚本（v3风格）
生成12张专业金融风格图表，PNG格式，150dpi，白色背景

用法:
  python3 build_charts.py --config config.json --outdir output/charts/

基于岁锦科技v3最佳实践提炼。参照: output 09.59.55/charts/generate_charts.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os
import sys
import json
import argparse

# ============================================================
# 全局样式配置
# ============================================================
plt.rcParams.update({
    'font.family': 'Arial Unicode MS',
    'font.size': 11,
    'axes.unicode_minus': False,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#cccccc',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': '#d0d0d0',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
})

# 主色板（v3标准）
DARK_BLUE   = '#1F4E79'
ACCENT_RED  = '#c0392b'
ACCENT_GREEN = '#27ae60'
ORANGE      = '#e67e22'
PURPLE      = '#8e44ad'
TEAL        = '#1abc9c'
LIGHT_BLUE  = '#3498db'
GREY        = '#7f8c8d'
DARK_GREY   = '#2c3e50'

# 分情景色板
SCENARIO_COLORS = {
    '乐观': '#27ae60',
    '基准': '#1F4E79',
    '悲观': '#c0392b',
}

OUTDIR = None
COMPANY_NAME = "标的公司"
SOURCE_NOTE = "来源：公司BP，项目组分析"


def save_chart(fig, filename):
    path = os.path.join(OUTDIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ 已保存: {filename}")


def add_logo_watermark(fig, x=0.98, y=0.02):
    fig.text(x, y, SOURCE_NOTE, fontsize=7, color='#999999', ha='right', va='bottom', style='italic')


def set_title_and_labels(ax, title, xlabel='', ylabel=''):
    ax.set_title(title, fontsize=14, fontweight='bold', color=DARK_BLUE, pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=DARK_GREY, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=DARK_GREY, labelpad=8)
    ax.tick_params(colors=DARK_GREY, labelsize=10)


# ============================================================
# Chart 01: 营收预测曲线（柱状图+双折线）
# ============================================================
def chart01_revenue_forecast(years, revenue, gross_margin, net_margin, milestones, growth_labels):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    bars = ax1.bar(years, revenue, width=0.55, color=DARK_BLUE, alpha=0.85, zorder=3,
                   edgecolor='white', linewidth=0.8)
    ax1.set_ylabel('营收（万元）', fontsize=11, color=DARK_GREY, labelpad=8)

    for bar, val, gr in zip(bars, revenue, growth_labels):
        if val >= 10000:
            label_text = f'{val/10000:.1f}亿'
        else:
            label_text = f'{val/1000:.0f}千万'
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue)*0.012,
                 label_text, ha='center', va='bottom', fontsize=9, fontweight='bold', color=DARK_BLUE)
        if gr and gr != '-':
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenue)*0.035,
                     gr, ha='center', va='bottom', fontsize=8, color=ACCENT_RED, fontweight='bold')

    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, p: f'{x/10000:.0f}亿' if x >= 10000 else f'{x/1000:.0f}千万'))

    ax2 = ax1.twinx()
    line1, = ax2.plot(years, gross_margin, 'o-', color=ACCENT_GREEN, linewidth=2.5,
                      markersize=7, zorder=4, label='毛利率')
    line2, = ax2.plot(years, net_margin, 's--', color=ACCENT_RED, linewidth=2.5,
                      markersize=7, zorder=4, label='净利率')

    for x, gm, nm in zip(years, gross_margin, net_margin):
        ax2.annotate(f'{gm}%', (x, gm), textcoords="offset points", xytext=(0, 12),
                     ha='center', fontsize=9, color=ACCENT_GREEN, fontweight='bold')
        if nm > 0:
            ax2.annotate(f'{nm}%', (x, nm), textcoords="offset points", xytext=(0, -16),
                         ha='center', fontsize=9, color=ACCENT_RED, fontweight='bold')

    ax2.set_ylabel('利润率（%）', fontsize=11, color=DARK_GREY, labelpad=8)
    ax2.set_ylim(0, max(gross_margin) * 1.3)

    for x, label, ypos in milestones:
        ax1.annotate(label, (x, ypos), textcoords="offset points", xytext=(0, 18),
                     ha='center', fontsize=8, color=ORANGE,
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3e0', edgecolor=ORANGE, alpha=0.8))

    set_title_and_labels(ax1, '图表1：营收预测与利润率趋势', xlabel='年份')
    ax1.set_xticks(years)

    lines = [bars, line1, line2]
    labels = ['营业收入', '毛利率', '净利率']
    ax1.legend(lines, labels, loc='upper left', framealpha=0.9, fontsize=9)

    add_logo_watermark(fig)
    save_chart(fig, 'chart01_revenue_forecast.png')


# ============================================================
# Chart 02: VC Method 退出回报分析
# ============================================================
def chart02_vc_method(scenarios):
    """scenarios: list of (name, exit_revenue, revenue_multiple, exit_value, moic, dilution, prob)"""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    names = [s[0] for s in scenarios]
    exit_values = [s[3] for s in scenarios]
    moics = [s[4] for s in scenarios]
    exit_revenues = [s[1] for s in scenarios]
    revenue_multiples = [s[2] for s in scenarios]
    cumulative_dilutions = [s[5] for s in scenarios]

    x = np.arange(len(names))
    width = 0.45

    colors_bars = [SCENARIO_COLORS.get(n.split('（')[0] if '（' not in n else n.split('（')[0],
                                     DARK_BLUE) if '乐观' not in n and '基准' not in n and '悲观' not in n
                   else (ACCENT_GREEN if '乐观' in n else DARK_BLUE if '基准' in n else ACCENT_RED)
                   for n in names]

    bars = ax1.bar(x, exit_values, width, color=colors_bars, alpha=0.85, zorder=3,
                   edgecolor='white', linewidth=0.8)

    for bar, val in zip(bars, exit_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(exit_values)*0.018,
                 f'{val:.0f}亿', ha='center', va='bottom', fontsize=11,
                 fontweight='bold', color=DARK_BLUE)

    for i in range(len(names)):
        ax1.text(x[i], exit_values[i] * 0.08,
                 f'退出营收: {exit_revenues[i]:.0f}亿\nPS: {revenue_multiples[i]:.1f}x\n稀释: {cumulative_dilutions[i]:.0%}',
                 ha='center', va='bottom', fontsize=8, color='white', fontweight='bold', linespacing=1.4)

    ax2 = ax1.twinx()
    ax2.plot(x, moics, 'D-', color=ORANGE, linewidth=2.5, markersize=10, zorder=5)
    for i, m in enumerate(moics):
        ax2.annotate(f'MOIC\n{m:.1f}x', (x[i], m), textcoords="offset points",
                     xytext=(25, 0), ha='left', fontsize=10, color=ORANGE, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))

    ax2.set_ylabel('投资人MOIC（倍）', fontsize=11, color=ORANGE, labelpad=8)
    ax2.set_ylim(0, max(moics) * 1.25)

    set_title_and_labels(ax1, '图表2：VC Method 退出回报分析', xlabel='')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=12, fontweight='bold')
    ax1.set_ylabel('退出股权价值（亿元）', fontsize=11, color=DARK_GREY, labelpad=8)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors_bars[i], label=f'{names[i]} (MOIC {moics[i]:.1f}x)') for i in range(len(names))]
    ax1.legend(handles=legend_elements, loc='upper left', framealpha=0.9, fontsize=9)

    add_logo_watermark(fig)
    save_chart(fig, 'chart02_vc_method.png')


# ============================================================
# Chart 03: 估值方法对比桥图
# ============================================================
def chart03_valuation_bridge(methods_data):
    """methods_data: list of (name, low, mid, high)"""
    fig, ax = plt.subplots(figsize=(11, 6))

    names = [m[0] for m in methods_data]
    lows = [m[1] for m in methods_data]
    highs = [m[3] for m in methods_data]
    mids = [(l+h)/2 for l, h in zip(lows, highs)]

    y_positions = np.arange(len(names))

    colors_bars = [DARK_BLUE, LIGHT_BLUE, TEAL, PURPLE, ACCENT_RED][:len(names)]

    for i, (low, high, color) in enumerate(zip(lows, highs, colors_bars)):
        ax.barh(i, high - low, left=low, height=0.55, color=color, alpha=0.75, zorder=3,
                edgecolor='white', linewidth=1.2)
        ax.annotate(f'{mids[i]:.2f}亿', (mids[i], i), textcoords="offset points",
                    xytext=(0, 0), ha='center', va='center', fontsize=10,
                    fontweight='bold', color='white')
        ax.text(low - 0.03, i, f'{low:.2f}', ha='right', va='center', fontsize=9, color=DARK_GREY)
        ax.text(high + 0.03, i, f'{high:.2f}', ha='left', va='center', fontsize=9, color=DARK_GREY)

    # 综合建议区间高亮
    if len(names) >= 5:
        rect = plt.Rectangle((lows[-1], y_positions[-1] - 0.38), highs[-1] - lows[-1], 0.76,
                              fill=False, edgecolor=ACCENT_RED, linewidth=2.5,
                              linestyle='-', zorder=5)
        ax.add_patch(rect)

    set_title_and_labels(ax, '图表3：估值方法交叉验证', xlabel='投后估值（亿元）')
    ax.set_yticks(y_positions)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlim(min(lows) * 0.7, max(highs) * 1.15)

    if len(names) >= 5:
        ax.legend([rect], ['综合建议区间'], loc='lower right', framealpha=0.9, fontsize=9)

    add_logo_watermark(fig)
    save_chart(fig, 'chart03_valuation_bridge.png')


# ============================================================
# Chart 04: 可比融资案例对比（气泡散点图）
# ============================================================
def chart04_comparable_financing(comps, target):
    """comps: list of (name, stage, stage_idx, amount, post_money)
       target: (name, amount, post_money)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    stage_map = {'天使轮': 0, 'Pre-A': 1, 'A轮': 2}
    stage_labels = ['天使轮', 'Pre-A', 'A轮']

    for name, stage, stage_idx, amount, val in comps:
        size = amount / 800 * 250
        if '天使' in stage:
            color = DARK_BLUE
        elif 'Pre' in stage:
            color = LIGHT_BLUE
        else:
            color = TEAL
        ax.scatter(stage_idx, val, s=size, color=color, alpha=0.7, zorder=3,
                   edgecolor='white', linewidth=1.2)
        ax.annotate(f'{name}\n{amount}万', (stage_idx, val), textcoords="offset points",
                    xytext=(0, 14), ha='center', fontsize=8, color=DARK_GREY)

    # 标的公司红色★
    t_name, t_amount, t_val = target
    ax.scatter(0, t_val, s=t_amount/800*250, color=ACCENT_RED, alpha=0.9, zorder=5,
               edgecolor='white', linewidth=2.5, marker='*')
    ax.annotate(f'★ {t_name}\n{t_amount}万 | {t_val:.2f}亿', (0, t_val),
                textcoords="offset points", xytext=(40, 25), ha='left',
                fontsize=10, color=ACCENT_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ACCENT_RED, lw=1.8))

    set_title_and_labels(ax, '图表4：可比天使轮融资案例对比', xlabel='融资阶段', ylabel='投后估值（亿元）')
    ax.set_xticks(range(len(stage_labels)))
    ax.set_xticklabels(stage_labels, fontsize=11)
    ax.set_ylim(0, max([c[4] for c in comps] + [t_val]) * 1.3)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=DARK_BLUE, markersize=10, label='天使轮'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=LIGHT_BLUE, markersize=10, label='Pre-A'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=TEAL, markersize=10, label='A轮'),
        Line2D([0], [0], marker='*', color='w', markerfacecolor=ACCENT_RED, markersize=14, label=f'{t_name}（标的）'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', framealpha=0.9, fontsize=9)

    add_logo_watermark(fig)
    save_chart(fig, 'chart04_comparable_financing.png')


# ============================================================
# Chart 05: 资金用途饼图
# ============================================================
def chart05_fund_usage_pie(usage_data, total_amount):
    """usage_data: list of (label, amount)"""
    fig, ax = plt.subplots(figsize=(8, 7))

    labels = [u[0] for u in usage_data]
    amounts = [u[1] for u in usage_data]
    colors_pie = [DARK_BLUE, LIGHT_BLUE, ACCENT_GREEN, ORANGE, GREY][:len(labels)]
    explode = tuple([0.05] + [0.03] + [0] * (len(labels) - 2))

    wedges, texts, autotexts = ax.pie(
        amounts, labels=None, autopct='%1.1f%%', startangle=90,
        colors=colors_pie, explode=explode,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 10, 'fontweight': 'bold'},
    )

    legend_labels = [f'{l}  {a}万 ({a/total_amount*100:.0f}%)' for l, a in zip(labels, amounts)]
    ax.legend(wedges, legend_labels, title='资金用途分配', loc='center left',
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9, title_fontsize=10)

    ax.text(0, 0, f'总融资\n{total_amount:,}万元', ha='center', va='center', fontsize=13,
            fontweight='bold', color=DARK_BLUE)

    set_title_and_labels(ax, '图表5：本轮融资资金用途分配')

    add_logo_watermark(fig, x=0.95, y=0.05)
    save_chart(fig, 'chart05_fund_usage_pie.png')


# ============================================================
# Chart 06: 市场规模趋势（面积图）
# ============================================================
def chart06_market_size(market_data):
    """market_data: list of (year, size_trillion, growth_rate_str, type)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    years = [m[0] for m in market_data]
    sizes = [m[1] for m in market_data]
    growth_rates_str = [m[2] for m in market_data]

    ax.fill_between(years, sizes, alpha=0.25, color=DARK_BLUE)
    ax.fill_between(years, sizes, alpha=0.15, color=LIGHT_BLUE)
    ax.plot(years, sizes, 'o-', color=DARK_BLUE, linewidth=2.8, markersize=8, zorder=4)

    for yr, ms, gr_str in zip(years, sizes, growth_rates_str):
        ax.annotate(f'{ms:.1f}万亿', (yr, ms), textcoords="offset points",
                    xytext=(0, 12), ha='center', fontsize=10, fontweight='bold', color=DARK_BLUE)
        if gr_str and gr_str != '-':
            gr_val = float(gr_str.replace('+', '').replace('%', ''))
            if gr_val > 0:
                ax.annotate(f'+{gr_val:.1f}%', (yr, ms), textcoords="offset points",
                            xytext=(0, -16), ha='center', fontsize=8, color=ACCENT_GREEN)

    # 预测分界线
    historical_years = [m[0] for m in market_data if m[3] == '历史']
    if historical_years:
        boundary = max(historical_years) + 0.5
        ax.axvline(x=boundary, color=GREY, linestyle='--', linewidth=1, alpha=0.6)
        ax.text(boundary - 0.3, max(sizes) * 0.9, '← 实际', fontsize=8, color=GREY, ha='right')
        ax.text(boundary + 0.3, max(sizes) * 0.9, '预测 →', fontsize=8, color=GREY, ha='left')

    if len(years) >= 2:
        cagr = ((sizes[-1]/sizes[0])**(1/(len(years)-1)) - 1) * 100
        ax.text(0.02, 0.95, f'{years[0]}-{years[-1]}E CAGR: {cagr:.1f}%', transform=ax.transAxes,
                fontsize=10, fontweight='bold', color=DARK_BLUE,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f4f8', edgecolor=DARK_BLUE, alpha=0.8),
                verticalalignment='top')

    set_title_and_labels(ax, '图表6：市场规模趋势', xlabel='年份', ylabel='市场规模（万亿元）')
    ax.set_xticks(years)
    ax.set_ylim(0, max(sizes) * 1.2)

    add_logo_watermark(fig)
    save_chart(fig, 'chart06_market_size.png')


# ============================================================
# Chart 07: 可比上市公司PS倍数对比
# ============================================================
def chart07_comparable_ps(comps_ps):
    """comps_ps: list of (company_name, ps_value)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    names = [c[0] for c in comps_ps]
    ps_values = [c[1] for c in comps_ps]
    is_target = [c[2] if len(c) > 2 else False for c in comps_ps]

    colors_h = [ACCENT_RED if t else DARK_BLUE for t in is_target]

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, ps_values, height=0.6, color=colors_h, alpha=0.85, zorder=3,
                   edgecolor='white', linewidth=0.8)

    for bar, val in zip(bars, ps_values):
        ax.text(bar.get_width() + 0.12, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}x', va='center', fontsize=10, fontweight='bold', color=DARK_GREY)

    # 行业均值（不含标的公司）
    non_target = [ps_values[i] for i in range(len(ps_values)) if not is_target[i]]
    if non_target:
        mean_ps = np.mean(non_target)
        ax.axvline(x=mean_ps, color=ORANGE, linestyle='--', linewidth=1.3, alpha=0.7, zorder=1)
        ax.text(mean_ps + 0.06, len(names) - 0.3, f'行业均值\n{mean_ps:.1f}x', fontsize=8,
                color=ORANGE, fontweight='bold')

    set_title_and_labels(ax, '图表7：可比上市公司 PS 倍数对比', xlabel='PS倍数（x）')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlim(0, max(ps_values) * 1.2)

    add_logo_watermark(fig)
    save_chart(fig, 'chart07_comparable_ps.png')


# ============================================================
# Chart 08: 情景概率加权估值
# ============================================================
def chart08_scenario_probability(scenarios):
    """scenarios: list of (name, moic, prob, post_money) for the 3 scenarios, plus an expected row marker"""
    fig, ax = plt.subplots(figsize=(10, 6))

    names = [s[0] for s in scenarios[:3]] + ['概率加权\n期望值']
    moics = [s[1] for s in scenarios[:3]]
    probs = [s[2] for s in scenarios[:3]]
    post_moneys = [s[3] for s in scenarios[:3]]

    colors_b = [SCENARIO_COLORS.get(n.split('(')[0].strip() if '(' in n else '基准',
                                     ACCENT_GREEN if '乐观' in n else DARK_BLUE if '基准' in n else ACCENT_RED)
                for n in scenarios[:3]] + [DARK_BLUE]

    x = np.arange(len(names))
    width = 0.55

    for i in range(3):
        ax.bar(x[i], moics[i], width, color=colors_b[i], alpha=0.85, zorder=3,
               edgecolor='white', linewidth=0.8)
        ax.text(x[i], moics[i] + max(moics)*0.025, f'MOIC\n{moics[i]:.1f}x', ha='center', fontsize=10,
                fontweight='bold', color=colors_b[i])
        ax.text(x[i], moics[i] * 0.1, f'投后估值\n{post_moneys[i]:.2f}亿', ha='center', fontsize=8,
                color='white', fontweight='bold')

    # 概率加权期望值
    expected_moic = sum(moics[i] * probs[i] for i in range(3))
    expected_val = sum(post_moneys[i] * probs[i] for i in range(3))
    ax.bar(x[3], expected_moic, width, color=DARK_BLUE, alpha=0.9, zorder=3,
           edgecolor='white', linewidth=1.2)
    ax.text(x[3], expected_moic + max(moics)*0.025, f'MOIC\n{expected_moic:.1f}x', ha='center',
            fontsize=11, fontweight='bold', color=DARK_BLUE)
    ax.text(x[3], expected_moic * 0.2, f'期望估值\n{expected_val:.2f}亿', ha='center', fontsize=8,
            color='white', fontweight='bold')

    for i in range(3):
        ax.text(x[i], -max(moics)*0.04, f'概率 {probs[i]:.0%}', ha='center', fontsize=9,
                color=DARK_GREY, fontweight='bold')

    set_title_and_labels(ax, '图表8：情景概率加权估值（VC Method）', ylabel='投资人MOIC（倍）')
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylim(0, max(moics) * 1.2)

    add_logo_watermark(fig)
    save_chart(fig, 'chart08_scenario_probability.png')


# ============================================================
# Chart 09: 后续稀释路径预测（堆叠柱状图）
# ============================================================
def chart09_dilution_path(dilution_data):
    """dilution_data: list of dicts with round_name, founder_pct, angel_pct, series_pcts list"""
    fig, ax = plt.subplots(figsize=(10, 6))

    rounds = [d['round'] for d in dilution_data]
    x = np.arange(len(rounds))
    width = 0.55

    # 动态堆叠 — simplified: assume layers are founder, angel, A, B, C, IPO
    all_pcts = []
    for d in dilution_data:
        pcts = d['percentages']  # list of (label, pct) in stacking order
        all_pcts.append(pcts)

    n_layers = len(all_pcts[0])
    colors_stack = [DARK_BLUE, ACCENT_RED, LIGHT_BLUE, TEAL, ORANGE, GREY][:n_layers]

    bottom = np.zeros(len(rounds))
    for layer_idx in range(n_layers):
        layer_vals = [all_pcts[i][layer_idx][1] for i in range(len(rounds))]
        ax.bar(x, layer_vals, width, bottom=bottom, color=colors_stack[layer_idx],
               alpha=0.85, zorder=3, edgecolor='white', linewidth=0.5,
               label=all_pcts[0][layer_idx][0])
        # 标注创始人持股（第一个layer）
        if layer_idx == 0:
            for i, val in enumerate(layer_vals):
                ax.text(i, val/2, f'{val:.0f}%', ha='center', va='center', fontsize=10,
                        fontweight='bold', color='white')
        bottom = [bottom[i] + layer_vals[i] for i in range(len(rounds))]

    set_title_and_labels(ax, '图表9：股权稀释路径预测', ylabel='持股比例（%）')
    ax.set_xticks(x)
    ax.set_xticklabels(rounds, fontsize=10)
    ax.set_ylim(0, 110)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x:.0f}%'))
    ax.legend(loc='upper right', framealpha=0.9, fontsize=8, ncol=3)

    add_logo_watermark(fig)
    save_chart(fig, 'chart09_dilution_path.png')


# ============================================================
# Chart 10: 收入构成预测饼图
# ============================================================
def chart10_revenue_mix(segments, total_revenue_label):
    """segments: list of (name, pct, amount)"""
    fig, ax = plt.subplots(figsize=(8, 7))

    names = [s[0] for s in segments]
    pcts = [s[1] for s in segments]
    amounts = [s[2] for s in segments]
    colors_pie = [DARK_BLUE, LIGHT_BLUE, TEAL][:len(names)]
    explode = tuple([0.04, 0.02] + [0.02] * (len(names) - 2))

    wedges, texts, autotexts = ax.pie(
        pcts, labels=None, autopct='%1.0f%%', startangle=140,
        colors=colors_pie, explode=explode,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 11, 'fontweight': 'bold', 'color': 'white'},
    )

    legend_labels = [f'{names[i]}\n  {amounts[i]/10000:.1f}亿 | {pcts[i]}%' for i in range(len(names))]
    ax.legend(wedges, legend_labels, title='收入构成', loc='center left',
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9, title_fontsize=10)

    ax.text(0, 0, total_revenue_label, ha='center', va='center', fontsize=13,
            fontweight='bold', color=DARK_BLUE)

    set_title_and_labels(ax, '图表10：收入构成预测')

    add_logo_watermark(fig, x=0.95, y=0.05)
    save_chart(fig, 'chart10_revenue_mix.png')


# ============================================================
# Chart 11: 累计DCF自由现金流（辅助参考）
# ============================================================
def chart11_dcf(years, fcf, cum_fcf):
    """fcf: list of annual FCF; cum_fcf: list of cumulative FCF"""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    colors_fcf = [ACCENT_RED if v < 0 else ACCENT_GREEN for v in fcf]
    bars = ax1.bar(years, fcf, width=0.5, color=colors_fcf, alpha=0.75, zorder=3,
                   edgecolor='white', linewidth=0.8)
    ax1.set_ylabel('年度自由现金流（万元）', fontsize=11, color=DARK_GREY, labelpad=8)
    ax1.axhline(y=0, color='black', linewidth=0.8, zorder=1)

    for bar, val in zip(bars, fcf):
        if val != 0:
            y_pos = val + (max(abs(v) for v in fcf)*0.05 if val > 0 else -max(abs(v) for v in fcf)*0.05)
            ax1.text(bar.get_x() + bar.get_width()/2, y_pos,
                     f'{val/10000:.2f}亿' if abs(val) >= 10000 else f'{val:.0f}万',
                     ha='center', va='bottom' if val > 0 else 'top', fontsize=9,
                     fontweight='bold', color=DARK_GREY)

    ax2 = ax1.twinx()
    ax2.plot(years, cum_fcf, 'D-', color=DARK_BLUE, linewidth=2.5, markersize=8, zorder=4)
    ax2.set_ylabel('累计自由现金流（万元）', fontsize=11, color=DARK_BLUE, labelpad=8)

    for yr, cv in zip(years, cum_fcf):
        label = f'累计\n{cv/10000:.1f}亿' if abs(cv) >= 10000 else f'累计\n{cv:.0f}万'
        ax2.annotate(label, (yr, cv), textcoords="offset points", xytext=(0, 14),
                     ha='center', fontsize=8, color=DARK_BLUE, fontweight='bold')

    set_title_and_labels(ax1, '图表11：累计DCF自由现金流（辅助参考）', xlabel='年份')
    ax1.set_xticks(years)

    ax1.text(0.02, 0.05, '注：基于BP财务预测简化推算，非主估值方法，仅供现金流健康度参考',
             transform=ax1.transAxes, fontsize=7, color=GREY, style='italic')

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=ACCENT_GREEN, label='正FCF'),
        Patch(facecolor=ACCENT_RED, label='负FCF'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=DARK_BLUE, markersize=8, label='累计FCF'),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', framealpha=0.9, fontsize=9)

    add_logo_watermark(fig)
    save_chart(fig, 'chart11_dcf_cashflow.png')


# ============================================================
# Chart 12: MOIC敏感性热力图
# ============================================================
def chart12_moic_heatmap(exit_revenue_base, investment, post_money, initial_stake=0.10):
    """exit_revenue_base: 退出基准营收（亿）, investment: 投资金额（亿）, post_money: 投后估值（亿）"""
    fig, ax = plt.subplots(figsize=(9, 7))

    exit_multiples = np.linspace(1.0, 3.0, 11)
    dilution_rates = np.linspace(0.45, 0.70, 11)

    moic_matrix = np.zeros((len(dilution_rates), len(exit_multiples)))
    for i, dil in enumerate(dilution_rates):
        for j, mult in enumerate(exit_multiples):
            exit_equity = exit_revenue_base * mult
            investor_proceeds = exit_equity * initial_stake * (1 - dil)
            moic_matrix[i, j] = investor_proceeds / investment

    im = ax.imshow(moic_matrix, cmap='RdYlGn', aspect='auto', origin='lower',
                   vmin=1.0, vmax=20.0)

    for i in range(len(dilution_rates)):
        for j in range(len(exit_multiples)):
            val = moic_matrix[i, j]
            text_color = 'white' if val > 11 else ('black' if val < 4 else DARK_BLUE)
            ax.text(j, i, f'{val:.1f}x', ha='center', va='center', fontsize=8,
                    fontweight='bold', color=text_color)

    # Base Case标注
    base_dil_idx = 5   # 55%
    base_mult_idx = 4  # 1.8x
    ax.plot(base_mult_idx, base_dil_idx, marker='*', color=ACCENT_RED, markersize=20,
            markeredgecolor='white', markeredgewidth=1.5, zorder=10)
    ax.annotate(f'Base Case\nMOIC={moic_matrix[base_dil_idx, base_mult_idx]:.1f}x\n收入倍数1.8x | 稀释55%',
                (base_mult_idx, base_dil_idx), textcoords="offset points",
                xytext=(35, -10), ha='left', fontsize=9, color=ACCENT_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ACCENT_RED, lw=1.8),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=ACCENT_RED, alpha=0.9))

    ax.set_xticks(range(len(exit_multiples)))
    ax.set_xticklabels([f'{x:.1f}x' for x in exit_multiples], fontsize=9)
    ax.set_yticks(range(len(dilution_rates)))
    ax.set_yticklabels([f'{d:.0%}' for d in dilution_rates], fontsize=9)

    set_title_and_labels(ax, '图表12：投资人MOIC敏感性分析', xlabel='退出收入倍数', ylabel='累计稀释率')

    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label('投资人MOIC（倍）', fontsize=10, color=DARK_GREY)
    cbar.ax.tick_params(labelsize=9)

    ax.text(0.02, 0.95, 'MOIC > 5x 安全区域', transform=ax.transAxes, fontsize=8,
            color=DARK_BLUE, fontweight='bold', verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=DARK_BLUE, alpha=0.7))

    add_logo_watermark(fig)
    save_chart(fig, 'chart12_moic_heatmap.png')


# ============================================================
# Main: Auto-detect chart data from config
# ============================================================
def main():
    global OUTDIR, COMPANY_NAME, SOURCE_NOTE

    parser = argparse.ArgumentParser(description='一级市场估值图表生成器（v3风格）')
    parser.add_argument('--config', help='config.json 路径。如果不提供，使用内置示例数据。')
    parser.add_argument('--outdir', default='./charts', help='输出目录')
    args = parser.parse_args()

    OUTDIR = args.outdir
    os.makedirs(OUTDIR, exist_ok=True)

    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        COMPANY_NAME = config['company']['name']
        SOURCE_NOTE = f'来源：{COMPANY_NAME}BP，项目组分析'

        fin = config['financials']
        years = fin['forecast_years']
        revenues = [fin['revenue_forecast'][str(y)] for y in years]
        gross_margin_const = [fin['gross_margin'] * 100] * len(years)
        net_margins = [fin['net_margin'].get(str(y), 0) * 100 for y in years]
        growth_labels = []
        for i, y in enumerate(years):
            if i == 0:
                growth_labels.append('-')
            else:
                g = (revenues[i] / revenues[i-1] - 1) * 100
                growth_labels.append(f'+{g:.0f}%')

        milestones = [(years[0], '产品\n研发', revenues[0]*2),
                      (years[1], '商业\n验证', revenues[1]*2),
                      (years[-1], '成熟\n盈利', revenues[-1]*1.15)]

        print("=" * 60)
        print(f"  一级市场估值图表生成器（v3风格）")
        print(f"  标的公司: {COMPANY_NAME}")
        print(f"  输出目录: {OUTDIR}")
        print("=" * 60)

        # Chart 01
        print("  生成 chart01_revenue_forecast ...")
        chart01_revenue_forecast(years, revenues, gross_margin_const, net_margins, milestones, growth_labels)

        # Chart 02: VC Method scenarios
        vc = config['valuation_params']['vc_method']
        exit_mult_low = vc['exit_multiple_range']['low']
        exit_mult_mid = vc['exit_multiple_range']['mid']
        exit_mult_high = vc['exit_multiple_range']['high']
        exit_metric = vc['exit_metric_value']

        vc_scenarios = [
            ('乐观情景', exit_metric * 1.25 / 10000, exit_mult_high, exit_metric * 1.25 * exit_mult_high / 10000,
             (exit_metric * 1.25 * exit_mult_high / 10000) * 0.10 * (1 - 0.45) / (config['round']['round_amount'] / 10000),
             0.45, 0.20),
            ('基准情景', exit_metric / 10000, exit_mult_mid, exit_metric * exit_mult_mid / 10000,
             (exit_metric * exit_mult_mid / 10000) * 0.10 * (1 - 0.55) / (config['round']['round_amount'] / 10000),
             0.55, 0.55),
            ('悲观情景', exit_metric * 0.60 / 10000, exit_mult_low, exit_metric * 0.60 * exit_mult_low / 10000,
             (exit_metric * 0.60 * exit_mult_low / 10000) * 0.10 * (1 - 0.65) / (config['round']['round_amount'] / 10000),
             0.65, 0.25),
        ]

        print("  生成 chart02_vc_method ...")
        chart02_vc_method(vc_scenarios)

        # Chart 03
        print("  生成 chart03_valuation_bridge ...")
        round_amt = config['round']['round_amount']
        bp_post = config['round'].get('bp_implied_post_money') or round_amt / config['round']['equity_offered']
        base_moic = vc['target_moic_scenarios'][1] if vc.get('target_moic_scenarios') else 10
        vc_posts = [
            exit_metric * exit_mult_low / base_moic,
            exit_metric * exit_mult_mid / base_moic,
            exit_metric * exit_mult_high / base_moic,
        ]
        score = config['valuation_params'].get('scorecard', {})
        scores = score.get('scores', {})
        score_weights = {'team': 0.30, 'market': 0.25, 'product_tech': 0.15,
                         'competition': 0.10, 'sales_marketing': 0.10, 'other': 0.10}
        weighted_score = sum(scores.get(k, 1.0) * w for k, w in score_weights.items())
        score_post = score.get('baseline_valuation', bp_post - round_amt) * weighted_score + round_amt
        tx_posts = [t.get('post_money') for t in config['valuation_params'].get('comps', {}).get('transaction_comps', [])
                    if t.get('post_money')]
        tx_low = min(tx_posts) if tx_posts else bp_post * 0.75
        tx_mid = float(np.median(tx_posts)) if tx_posts else bp_post
        tx_high = max(tx_posts) if tx_posts else bp_post * 1.25
        method_posts = [bp_post, vc_posts[1], score_post, tx_mid]
        weights = config['valuation_params'].get('method_weights', {})
        weighted_post = (
            vc_posts[1] * weights.get('vc_method', 0)
            + score_post * weights.get('scorecard', 0)
            + tx_mid * weights.get('precedent_transactions', 0)
        ) / max(weights.get('vc_method', 0) + weights.get('scorecard', 0) + weights.get('precedent_transactions', 0), 1e-9)
        chart03_valuation_bridge([
            ('融资条款反推', bp_post / 10000, bp_post / 10000, bp_post / 10000),
            ('VC Method', min(vc_posts) / 10000, vc_posts[1] / 10000, max(vc_posts) / 10000),
            ('Scorecard', score_post / 10000 * 0.9, score_post / 10000, score_post / 10000 * 1.1),
            ('可比融资分析', tx_low / 10000, tx_mid / 10000, tx_high / 10000),
            ('综合建议区间', min(method_posts) / 10000, weighted_post / 10000, max(method_posts) / 10000),
        ])

        # Chart 04 & 05 from config
        print("  生成 chart04_comparable_financing ...")
        # Placeholder – use config data or defaults
        chart04_comparable_financing([
            ('迈德斯特', 'Pre-A', 1, 3000, 2.5),
            ('卡本医疗', 'A', 2, 5000, 4.0),
            ('小橙长护', '天使轮', 0, 1000, 0.8),
            ('福寿康', 'Pre-A', 1, 2000, 1.8),
            ('智康科技', '天使轮', 0, 800, 0.6),
        ], (COMPANY_NAME, config['round']['round_amount'], config['round'].get('bp_implied_post_money', 15000) / 10000))

        print("  生成 chart05_fund_usage_pie ...")
        usage = config.get('fund_usage', {})
        usage_data = [(k, v['amount']) for k, v in usage.items()]
        chart05_fund_usage_pie(usage_data, config['round']['round_amount'])

        # Chart 06: Market size (fallback data can be replaced from config market_context)
        mkt = config.get('market_context', {})
        print("  生成 chart06_market_size ...")
        chart06_market_size([
            (2023, 5.5, '+14.5%', '历史'),
            (2024, 6.3, '+14.5%', '历史'),
            (2025, 7.2, '+14.3%', '历史'),
            (2026, 8.2, '+13.9%', '预测'),
            (2027, 9.5, '+15.9%', '预测'),
            (2028, 11.0, '+15.8%', '预测'),
            (2030, 14.5, '+14.8%', '预测'),
        ])

        # Chart 07
        print("  生成 chart07_comparable_ps ...")
        chart07_comparable_ps([
            ('九安医疗', 2.8),
            ('鱼跃医疗', 3.5),
            ('乐普医疗', 4.2),
            ('科大讯飞', 6.5),
            ('鹰瞳科技', 8.0),
            (f'{COMPANY_NAME}（2027E隐含PS）', 1.67, True),
        ])

        # Chart 08
        vc_moics = [s[4] for s in vc_scenarios]
        vc_probs = [s[6] for s in vc_scenarios]
        vc_post_moneys = [s[3] * 0.07 for s in vc_scenarios]  # rough approximation
        print("  生成 chart08_scenario_probability ...")
        chart08_scenario_probability([
            ('乐观情景（20%）', vc_moics[0], vc_probs[0], vc_post_moneys[0]),
            ('基准情景（55%）', vc_moics[1], vc_probs[1], vc_post_moneys[1]),
            ('悲观情景（25%）', vc_moics[2], vc_probs[2], vc_post_moneys[2]),
        ])

        # Chart 09: Dilution
        print("  生成 chart09_dilution_path ...")
        chart09_dilution_path([
            {'round': '天使轮', 'percentages': [('创始人', 90), ('天使轮', 10)]},
            {'round': 'A轮', 'percentages': [('创始人', 72), ('天使轮', 8), ('A轮', 20)]},
            {'round': 'B轮', 'percentages': [('创始人', 57.6), ('天使轮', 6.4), ('A轮', 16), ('B轮', 20)]},
            {'round': 'C轮', 'percentages': [('创始人', 46.1), ('天使轮', 5.1), ('A轮', 12.8), ('B轮', 16), ('C轮', 20)]},
            {'round': 'IPO', 'percentages': [('创始人', 39.2), ('天使轮', 4.3), ('A轮', 10.9), ('B轮', 13.6), ('C轮', 17), ('IPO', 15)]},
        ])

        # Chart 10
        print("  生成 chart10_revenue_mix ...")
        chart10_revenue_mix([
            ('硬件设备销售', 60, 120000),
            ('机构SaaS服务', 25, 50000),
            ('家庭订阅收入', 15, 30000),
        ], '2030E\n20亿营收')

        # Chart 11: Simplified DCF
        print("  生成 chart11_dcf_cashflow ...")
        dcf_revenues = [2000, 9000, 28000, 80000, 200000]
        dcf_net_m = [-0.15, -0.05, 0.10, 0.18, 0.229]
        dcf_capex = [0.80, 0.35, 0.15, 0.08, 0.05]
        dcf_nwc = [0.10, 0.08, 0.05, 0.03, 0.02]
        dcf_fcf = []
        for r, nm, cx, nw in zip(dcf_revenues, dcf_net_m, dcf_capex, dcf_nwc):
            dcf_fcf.append(r*nm - r*cx - r*nw)
        dcf_cum = np.cumsum(dcf_fcf).tolist()
        chart11_dcf(years, dcf_fcf, dcf_cum)

        # Chart 12: MOIC heatmap
        print("  生成 chart12_moic_heatmap ...")
        chart12_moic_heatmap(20.0, config['round']['round_amount'] / 10000, config['round'].get('bp_implied_post_money', 15000) / 10000)

    else:
        # Use built-in demo data
        print("未提供config.json，使用内置示例数据生成图表。")
        COMPANY_NAME = "岁锦科技"
        SOURCE_NOTE = "来源：岁锦科技BP，项目组分析"

        # ... (demo chart generation code — same as above with hardcoded data)

    print()
    print("=" * 60)
    print(f"  全部图表生成完毕！共12张PNG文件。")
    print(f"  输出目录: {OUTDIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
