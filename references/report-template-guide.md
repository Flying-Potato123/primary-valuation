# 一级市场估值报告模板指南（v3风格）

> 本文档定义了一级市场估值报告的标准结构、数据组织方式、图表设计规范和PPT制作标准。
> AI 在生成估值报告时必须遵循本文档的规范。参照案例：岁锦科技天使轮估值报告 v3。

---

## 目录

1. [报告结构](#1-报告结构)
2. [数据组织方式](#2-数据组织方式)
3. [图表设计规范](#3-图表设计规范)
4. [PPT制作标准](#4-ppt制作标准)
5. [交付物清单](#5-交付物清单)
6. [质量检查清单](#6-质量检查清单)

---

## 1. 报告结构

### 1.1 核心原则：结论先行

**执行摘要必须在报告第1-2页给出完整的估值结论**。读者不需要读完整个报告才能知道估值结果。

报告结构应当：
- **封面**（1页）：公司名 + 报告标题 + 标语 + KPI卡片 + 日期/机密
- **执行摘要**（1-2页）：估值结论 → 本轮条款 → 方法选择 → 关键发现 → 估值摘要表
- **正文分析**（逐层展开论证）

### 1.2 完整结构

```
封面
执行摘要
  估值结论
  本轮交易条款
  估值方法选择与依据
  关键发现（6条，编号列表）
  估值摘要表（4-5种方法 × 低/中/高估值）
  [图表] 估值方法交叉验证桥图

一、融资背景与估值目的
  1.1 公司发展阶段
  1.2 融资概况与条款（⚠ 标注未提供的关键条款）
  1.3 估值目的与范围
  [图表] 资金用途饼图

二、公司分析
  2.1 公司概况
  2.2 产品矩阵（全宽表格）
  2.3 商业模式与收入结构
  [图表] 收入构成预测
  2.4 竞争壁垒（4点）
  2.5 核心团队

三、行业与市场分析
  3.1 不可逆的老龄化浪潮
  3.2 智慧养老市场规模
  [图表] 市场规模面积图 + 数据表
  3.3 政策环境与红利（政策文件表格）
  3.4 竞争格局分析（三足鼎立表格 + 岁锦差异化定位）

四、财务预测分析
  4.1 BP财务预测概览（⚠ 重要前提标注）
  [图表] 营收预测+利润率趋势
  4.2 收入驱动因素拆解（4个层面：产品线/客户数/ARPU/区域）
  4.3 毛利率与盈利路径
  4.4 关键假设审阅与压力测试
  [图表] 简化DCF现金流（辅助参考）

五、估值分析
  5.1 方法选择说明（四层估值体系）
  5.2 融资条款反推法
  5.3 VC Method（风险资本法）— 核心方法
      - 核心参数设置
      - 三种情景分析表
      [图表] VC Method退出回报分析
      [图表] 情景概率加权估值
      - 概率加权计算
  5.4 可比天使轮/Pre-A融资分析
      [图表] 可比融资散点图
  5.5 可比上市公司PS倍数参考
      [图表] 可比上市公司PS对比
  5.6 估值方法交叉验证与结论
      [图表] 估值桥图（复用）
  5.7 综合估值建议（加粗，结论性段落）

六、退出分析与股权稀释
  6.1 退出路径分析
  6.2 后续稀释路径（稀释表格 + 推演）
  [图表] 股权稀释路径堆叠柱状图

七、敏感性分析
  7.1 MOIC敏感性热力图
  [图表] MOIC热力图
  7.2 关键变量敏感性排序（4个变量从高到低）
  7.3 下行情景压力测试

八、风险提示
  8.1-8.8 按严重程度分级（高风险→中高风险→中风险）
  每个风险：标题 + 详细情境描述 + 影响分析

九、关键尽调建议
  9.1-9.8 8大方向，每个有具体验证动作
  （非泛泛列表，而是可执行的验证步骤）

附录
  附录A：估值模型核心假设汇总表
  附录B：数据来源与可靠性说明
  附录C：假设追溯表

免责声明（7条标准条款）
```

---

## 2. 数据组织方式

### 2.1 数据定义模式（v3推荐）

将核心数据直接组织在脚本的全局常量中，减少对 config.json 的过度依赖：

```python
COMPANY = {
    "name": "岁锦科技（AgeTech）",
    "slogan": "AI × 智慧养老设备，用 AI 守护每一个暮年时光",
    "stage": "天使轮",
    "round_amount": 1500,  # 万元
    "equity_offered": "10%",
    "pre_money_base": 1.35,  # 亿元
    "post_money_base": 1.50,  # 亿元
    "post_money_range": "1.00-1.85亿元",
    "valuation_date": "2026年6月10日",
}

FORECAST = [
    # (年份, 营收万, YoY, 毛利率, 净利率, 里程碑, 发展阶段)
    (2026, 2000, "-", "52%", "负", "MVP上线，5家机构试点", "产品研发期"),
    (2027, 9000, "+350%", "52%", "~2%", "月活5,000，30家机构", "商业验证期"),
    ...
]

VC_SCENARIOS = [
    # (情景名, 退出营收亿, PS倍数, 退出估值亿, 天使保留股权%, MOIC, 概率%)
    ("乐观情景", 25.0, 2.8, 70.0, 0.45, 25.7, 0.20),
    ("基准情景", 20.0, 1.8, 36.0, 0.55, 10.8, 0.55),
    ("悲观情景", 12.0, 1.0, 12.0, 0.65, 2.8, 0.25),
]
```

### 2.2 表格后必须紧跟分析段落

```markdown
❌ 错误做法：
[表格]
[表格]
[表格]
[分析段落]  ← 读者已经忘了第一个表格的内容

✅ v3正确做法：
[表格1]
[分析段落1：解读表格1的关键发现]
[图表1]
[分析段落2：图表1的takeaway]
[表格2]
[分析段落2：解读表格2的关键发现]
```

### 2.3 数据-叙事融合模式

每个数据模块遵循四步叙事：

```
市场背景（1-2句）→ 核心数字（量化）→ 驱动解释（为什么）→ 估值含义（so what）
```

示例：
> 中国60岁以上人口已突破3亿，占总人口超过21%。智慧养老市场2025年预计达7.21万亿元，
> 年复合增长率12.34%。岁锦科技主攻的平台整合型子赛道CAGR高达41%，是增速最快的子赛道。
> **估值含义**：公司定位在超级赛道的最快增长子领域，TAM天花板极高，为长期高增长提供了结构性支撑。

---

## 3. 图表设计规范

### 3.1 图表清单（12张标准图表）

| # | 文件名 | 类型 | 尺寸 | 核心信息 |
|---|--------|------|------|---------|
| 01 | `chart01_revenue_forecast.png` | 柱状图+双折线 | 10×6 | 营收预测+毛利率/净利率趋势，里程碑标注 |
| 02 | `chart02_vc_method.png` | 分组柱+折线 | 10×6 | 三种情景退出估值+MOIC，情景参数标注 |
| 03 | `chart03_valuation_bridge.png` | 水平区间条 | 11×6 | 4种方法估值区间+综合区间红色高亮框 |
| 04 | `chart04_comparable_financing.png` | 气泡散点图 | 10×6 | 5个可比案例（气泡=融资额），岁锦★红色标注 |
| 05 | `chart05_fund_usage_pie.png` | 饼图 | 8×7 | 5项资金用途，中心标注总额，右侧图例带金额 |
| 06 | `chart06_market_size.png` | 面积图 | 10×6 | 市场规模趋势+增速标注，历史/预测分界线 |
| 07 | `chart07_comparable_ps.png` | 水平柱状图 | 10×6 | 5-6家公司PS对比，行业均值虚线，岁锦红色高亮 |
| 08 | `chart08_scenario_probability.png` | 分组柱 | 10×6 | 3种情景MOIC+概率加权期望，概率标注 |
| 09 | `chart09_dilution_path.png` | 堆叠柱状图 | 10×6 | 天使→IPO各轮次持股变化，累计稀释%标注 |
| 10 | `chart10_revenue_mix.png` | 饼图 | 8×7 | 2030E收入构成，右侧图例带金额 |
| 11 | `chart11_dcf_cashflow.png` | 柱+折线 | 10×6 | 简化DCF（附注：辅助参考，非主估值方法） |
| 12 | `chart12_moic_heatmap.png` | 热力图 | 9×7 | 退出倍数×稀释率→MOIC，Base Case★标注 |

### 3.2 全局样式

```python
plt.rcParams.update({
    'font.family': 'Arial Unicode MS',  # 中英文混排首选
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
```

### 3.3 配色

```python
DARK_BLUE   = '#1F4E79'   # 主色（柱状图、标题；与 Word/PPT 表头、PPT 装饰条统一）
ACCENT_RED  = '#c0392b'   # 悲观情景、风险标注
ACCENT_GREEN = '#27ae60'  # 乐观情景、正向指标
ORANGE      = '#e67e22'   # 折线、关键标注
PURPLE      = '#8e44ad'   # PS倍数法
TEAL        = '#1abc9c'   # 辅助色
LIGHT_BLUE  = '#3498db'   # 辅助色
GREY        = '#7f8c8d'   # 网格线、辅助元素
DARK_GREY   = '#2c3e50'   # 轴标签

# 分情景色板
SCENARIO_COLORS = {
    '乐观': '#27ae60',  # 绿色
    '基准': '#1F4E79',  # 深蓝
    '悲观': '#c0392b',  # 红色
}
```

### 3.4 每张图表必备元素

1. **结论导向标题**：如"图表3：估值方法交叉验证"，不是"各方法估值对比"
2. **右下角来源标注**：`fig.text(0.98, 0.02, f'来源：{公司名}BP，项目组分析', fontsize=7, color='#999999', ha='right', va='bottom', style='italic')`（公司名从 config 读取）
3. **清晰图例**：位置不遮挡数据
4. **Grid线**：浅灰色虚线，透明度0.3

### 3.5 标题与标签辅助函数

```python
def set_title_and_labels(ax, title, xlabel='', ylabel=''):
    ax.set_title(title, fontsize=14, fontweight='bold', color=DARK_BLUE, pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=DARK_GREY, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=DARK_GREY, labelpad=8)
    ax.tick_params(colors=DARK_GREY, labelsize=10)

def add_logo_watermark(fig, company_name, x=0.98, y=0.02):
    fig.text(x, y, f'来源：{company_name}BP，项目组分析', fontsize=7,
             color='#999999', ha='right', va='bottom', style='italic')
```

---

## 4. PPT制作标准

### 4.1 全局设置

```python
prs = Presentation()
prs.slide_width = PptInches(13.333)  # 16:9 宽屏
prs.slide_height = PptInches(7.5)

# 字体
FONT_NAME_CN = "微软雅黑"  # 中文首选
FONT_NAME_EN = "Arial"     # 英文/数字

# 配色
HEADER_BG = "1F4E79"       # 表头背景
ALT_ROW_BG = "D6E4F0"      # 交替行背景
```

### 4.2 17页标准结构

| Slide | 标题 | 核心元素 | 特殊说明 |
|-------|------|---------|---------|
| 1 | 封面 | 蓝色装饰条 + 公司名(40pt) + 报告标题(26pt) + 标语 + 日期/机密 | 白底+蓝色横条 |
| 2 | 执行摘要 | 5条要点列表 + 估值摘要表 | 最核心信息 |
| 3 | 公司概览 | 左栏要点 + 右栏资金用途饼图 | 左右分栏 |
| 4 | 产品矩阵 | 全宽四线产品表格 | 信息密度高 |
| 5 | 商业模式 | 左栏三级变现+优势 + 右栏收入构成图 | 左右分栏 |
| 6 | 行业市场 | 市场规模表 + 面积图 + 驱动要点 | 数据丰富 |
| 7 | 竞争格局 | 三足鼎立表 + 岁锦定位(红色加粗) + 可比PS图 | 竞争分析 |
| 8 | 财务预测 | 预测表 + 营收图 + 红色警示文字 | ⚠标注不确定性 |
| 9 | 估值方法 | 四重方法概述 + 估值桥图 + 摘要表 | 方法论概览 |
| 10 | VC Method | 情景表 + 退出回报图 + 关键发现 | 核心方法详解 |
| 11 | 情景概率 | 三种情景详情 + 概率加权结论 + 概率图 | 数学计算呈现 |
| 12 | 可比分析 | 可比融资表 + 散点图 + PS说明 | 双维度对标 |
| 13 | MOIC敏感性 | 热力图(左) + 排序解读(右) | 左右分栏 |
| 14 | 稀释路径 | 稀释表 + 堆叠柱状图 + 投资人退出分析 | 退出分析 |
| 15 | 风险提示 | 左栏：高风险+中高 / 右栏：中风险 | 分级呈现 |
| 16 | 尽调建议 | 8个方向分两栏 | 可执行验证 |
| 17 | 免责声明 | 7条标准条款 | 合规要求 |

### 4.3 PPT辅助函数规范

```python
def add_ppt_title(slide, text):
    """统一标题样式：28pt 深蓝加粗"""
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(28); p.font.bold = True
    p.font.color.rgb = RGBColor(31, 78, 121)
    p.font.name = FONT_NAME_CN

def add_ppt_divider(slide, left, top, width):
    """分隔线：深蓝色细线"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(31, 78, 121)
    shape.line.fill.background()

def add_ppt_footer(slide, text="公司名 估值报告 | 机密 | 2026年6月"):
    """页脚：8pt 灰色"""
    add_ppt_text(slide, text, Inches(0.5), Inches(7.1), Inches(12), Inches(0.3),
                 font_size=Pt(8), color=RGBColor(150, 150, 150))
```

### 4.4 PPT表格样式

```python
# 表头：深蓝背景 + 白色加粗文字(9pt) + 居中对齐
# 数据行：8pt，交替行浅蓝背景(D6E4F0)
# 使用 parse_xml 设置单元格背景色（兼容性好）
```

---

## 5. 交付物清单

每次估值报告生成后，必须输出以下文件：

| # | 交付物 | 格式 | 必需 |
|---|--------|------|------|
| 1 | 估值报告 | `.docx` | ✅ |
| 2 | PPT展示 | `.pptx`（16:9） | ✅ |
| 3 | 估值模型 | `.xlsx` | ✅ |
| 4 | 图表集（12张） | `.png`（150dpi） | ✅ |
| 5 | 配置参数 | `config.json` | ✅ |
| 6 | 估值结果 | `valuation_results.json` | ✅ |
| 7 | Cap Table数据 | `cap_table.json` + `cap_table.csv` | ✅ |
| 8 | 假设追溯表 | `assumption_traceability.csv` | ✅ |
| 9 | 数据来源日志 | `source_log.csv` | ✅ |
| 10 | 一页摘要 | `one_page_summary.md` | ✅ |
| 11 | 尽调问题清单 | `open_questions.md` | ✅ |
| 12 | 交付清单 | `manifest.json` | ✅ |

### manifest.json 格式

```json
{
  "valuation_date": "2026-06-10",
  "currency": "人民币",
  "outputs": ["所有文件路径列表"],
  "conclusion": {
    "post_money_base_rmb_yi": 1.50,
    "pre_money_base_rmb_yi": 1.35,
    "post_money_range_rmb_yi": [1.00, 1.85],
    "round_amount_rmb_wan": 1500,
    "equity_offered": "10%",
    "primary_method": "VC Method（风险资本法）",
    "base_case_moic": 10.8,
    "probability_weighted_moic": 12.1
  },
  "report_version": "v3"
}
```

---

## 6. 质量检查清单

### Word报告检查

- [ ] 封面含公司名、报告标题、标语、KPI、日期、机密标记
- [ ] 执行摘要在前2页给出完整估值结论
- [ ] 每章有明确的标题层次（一、二、三... → 1.1, 1.2... → 5.1, 5.2...）
- [ ] 每个表格后紧跟分析段落
- [ ] 每个图表后紧跟takeaway解读
- [ ] 所有BP数据加 ⚠ 标注不确定性
- [ ] 风险按严重程度分级（高→中高→中）
- [ ] 尽调建议有具体验证动作
- [ ] 估值结论先给区间再给基准情景
- [ ] 附录含假设汇总+数据来源+假设追溯
- [ ] 免责声明完整（7条）
- [ ] 全文字体统一（微软雅黑/Arial）
- [ ] 表格表头深蓝白字，交替行浅蓝

### PPT检查

- [ ] 16:9 宽屏比例
- [ ] 17页标准结构
- [ ] 封面有设计感（非纯白底黑字）
- [ ] 每页有标题+分隔线
- [ ] 除封面外每页有页脚
- [ ] 图表嵌入正确路径
- [ ] 表格格式统一（表头深蓝+交替行）
- [ ] 信息密度合适（不太空不太挤）

### 图表检查

- [ ] 12张图表全部生成
- [ ] 每张图表有结论导向标题
- [ ] 右下方有来源标注
- [ ] 配色统一（深蓝主色+红绿情景色）
- [ ] 分辨率150dpi
- [ ] 中文字符正常渲染（无方框乱码）

### 交付物检查

- [ ] 所有12项交付物全部存在
- [ ] manifest.json 包含完整结论摘要
- [ ] 估值结果JSON与其他交付物数据一致
