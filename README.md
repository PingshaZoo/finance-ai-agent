# 代理记账财务 AI 自动化项目规划（路线原则修正版）

> 适用角色：小企业代理记账财务人员  
> 系统环境：Windows 10/11 桌面 Agent / 本地脚本  
> 文档版本：v2.1  
> 核心目标：把“人工重复点击 + 手工搬运”逐步变成“AI + Skill + Workflow”的自动化工作流。

---

## 0. 路线原则修正（重要补充）

这部分不是推翻原计划，而是给原计划加一个现实约束：

```text
你现在最大的风险
不是“技术不够”
而是：
系统过度设计
```

当前真实业务规模大约是：

```text
10 个左右客户
```

这意味着：现在不是 SaaS，不是企业 ERP，不是万人系统，也不是高并发系统。

所以当前判断标准应该是：

```text
“能稳定替你省时间”
```

而不是：

```text
“架构先进”
```

这个项目现阶段真正应该追求的目标不是“AI Agent”本身，而是：

```text
减少每天的重复劳动
```

更准确地说，它是：

```text
一个增强财务工作能力的系统
```

而不是：

```text
一家 AI 公司
```

### 现阶段不要优先碰的东西

#### 1. 不要优先做 multi-agent

当前规模暂时不需要 planner agent、memory agent、executor agent、reflection agent 这类复杂拆分。

现在更需要的是：

```text
稳定脚本
```

#### 2. 不要优先做本地大模型

核心问题不是推理算力，而是工作流。

Claude / OpenAI API 足够覆盖 OCR 理解、字段抽取、报告草稿、分析文案等需求。

#### 3. 不要优先做复杂数据库

当前阶段：

```text
SQLite 就够了
```

甚至大量场景里：

```text
Excel 都够
```

现在真正重要的是：

```text
先跑通
```

---

## 一、当前工作场景全景拆解

> 6 大工作场景，每个都有核心痛点，是构建 Skill 的直接依据。

| # | 工作场景 | 输入来源 | 核心痛点 | 期望产出 |
|---|---------|---------|---------|---------|
| 1 | 客户沟通 & 资金录入 | 微信 PC、转账截图、Excel 附件、PDF | 非结构化数据量大，手工录入慢 | 标准化流水记录 |
| 2 | 电商多平台数据采集 | 淘宝、京东、拼多多、抖音、微信小店 | 重复登录点击，格式各异 | 统一格式订单表 |
| 3 | Excel 对账 & 数据核对 | 多来源 Excel、银行流水 | 规则型劳动，差异查找费时 | 差异报告、核对结果 |
| 4 | 财务汇总 & 客户汇报 | 各类汇总数据 | 整理耗时，格式要求高 | Excel 月报 + PPT 汇报 |
| 5 | 税务操作 | 国家税务局、电子发票系统 | 强交互，容错率极低 | 发票 / 申报记录 |
| 6 | 历史数据查询 | 分散在各 Excel 文件 | 查询慢，找数难 | 即时查询结果 |

日常工作本质上主要在做两件事：

```text
非结构化 -> 结构化
```

和：

```text
两表核对
```

这也是为什么第一阶段应该优先做 `excel_processor` 和 `ocr_parser`。

---

## 二、系统总体架构

> 这是长期架构图，但实现时不要一次性全部做完。当前应先用脚本把核心流程跑通。

```text
┌──────────────────────────────────────────────────────────┐
│              数据输入层（非结构化）                       │
│   微信PC端  │  电商后台  │  截图/图片  │  Excel/PDF       │
└──────┬───────────┬───────────┬─────────────┬─────────────┘
       │           │           │             │
┌──────▼───────────▼───────────▼─────────────▼─────────────┐
│                    数据采集 Skills 层                    │
│  微信监听Skill │ 爬虫采集Skill │ OCR识别Skill │ 文件解析Skill │
└──────────────────────────┬───────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │   统一数据层     │
                  │ SQLite / Excel   │
                  └────────┬────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                    处理 & 分析 Skills 层                 │
│   Excel对账Skill │ 财务分析Skill │ 发票辅助Skill          │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                   主控 Orchestrator（后期）               │
│         自然语言 -> 任务拆解 -> 调用对应 Skill -> 汇总结果 │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                      输出层                               │
│       Excel月报  │  PPT汇报  │  Word报告  │  微信消息通知 │
└──────────────────────────────────────────────────────────┘
```

### Agent 端到端执行示例（长期目标）

```text
你说：帮我做张总 5 月份的经营汇报
         ↓
主控 Agent 解析意图：客户=张总，月份=5月
         ↓
1. ecommerce_scraper  -> 拉取各平台订单
2. ocr_parser         -> 识别本月上传截图金额
3. excel_processor    -> 两表核对，生成差异报告
4. finance_analyzer   -> 分析盈亏 / 广告ROI / 欠款
5. report_generator   -> 生成 Excel 月报 + PPT 汇报
         ↓
输出：经营汇报 PPT + 对账明细 XLSX
```

注意：这是长期形态，不是第一天就要实现的形态。

---

## 三、核心 Skill 体系

### 第一优先级：立即构建（最高 ROI）

#### Skill 1：`excel_processor`（Excel 对账 & 汇总）

**定位：当前最应该先做的模块。**

解决问题：

- 多来源 Excel / CSV 数据清洗
- 两表核对
- 差异标红
- 查重
- 自动统计摘要

技术方案：

- pandas
- openpyxl
- xlsxwriter

最小可用功能：

```text
两表对账
自动差异标红
自动统计
```

输入示例：

```text
电商订单.xlsx
银行流水.xlsx
客户提供账单.xlsx
```

输出示例：

```text
对账结果.xlsx
差异摘要.json / txt
```

核心收益：

以前：

```text
眼睛找差异
```

以后：

```text
脚本自动标红
```

#### Skill 2：`ocr_parser`（截图 / 票据识别）

解决问题：

- 微信转账截图
- 银行回单图片
- 发票图片
- 支付截图

技术方案：

```text
首选：Claude / OpenAI Vision API
备选：PaddleOCR（本地离线）
```

结构化输出字段：

```json
{
  "amount": 0,
  "time": "YYYY-MM-DD HH:mm",
  "payer": "",
  "payee": "",
  "remark": "",
  "transaction_type": "income/expense/refund",
  "confidence": "high/medium/low",
  "source_file": ""
}
```

核心收益：

以前：

```text
盯着截图手敲金额
```

以后：

```text
批量提取 JSON / CSV
```

#### Skill 3：`report_generator`（Excel 月报 + PPT 汇报）

解决问题：

- 汇总数据后自动生成客户汇报材料
- 固定模板自动填数
- 生成分析说明草稿

技术方案：

- openpyxl
- python-pptx
- python-docx
- Claude / OpenAI API 生成分析文案

适合生成：

- 月度财务报告
- 利润分析
- 经营汇报 PPT
- 客户可读版说明

### 第二优先级：数据采集自动化

#### Skill 4：`ecommerce_scraper`（电商后台数据采集）

目标：

- 下载订单
- 下载退款
- 下载广告投流
- 下载平台费用

技术方案：

- Playwright
- 浏览器持久化上下文
- Cookie 复用
- 下载文件解析

关键原则：

```text
不要追求“全自动登录”
```

更稳定的是：

```text
Cookie 复用
+
人工过验证码
```

否则会陷入：

```text
对抗平台风控
```

平台支持优先级：

| 平台 | 难度 | 建议方案 |
|------|------|---------|
| 拼多多 | 中 | 优先尝试 Playwright 自动导出 |
| 淘宝 / 天猫 | 中高 | Cookie 复用 + 人工验证码 |
| 京东 | 中高 | Cookie 复用 |
| 抖音小店 | 中高 | Playwright + 定期维护 |
| 微信小店 | 高 | 优先手动导出，脚本解析 |

#### Skill 5：`wechat_monitor`（微信文件 / 消息处理）

建议先做低风险方案：

```text
微信文件夹监听
```

而不是一开始就做复杂 GUI 自动化。

实现方式：

- 微信 PC 设置固定文件接收目录
- Python watchdog 监听目录
- 新文件触发分类处理
- 图片 -> OCR
- Excel -> 解析
- PDF -> 提取

GUI 自动化只作为补充：

- pywinauto
- uiautomation

建议只用于读取，不优先模拟大量点击或发送。

### 第三优先级：分析、查询与税务辅助

#### Skill 6：`finance_analyzer`（财务智能分析）

功能：

- 盈亏分析
- 平台 ROI 分析
- 欠款 / 回款预警
- 异常交易检测
- 退款率异常提醒

技术方案：

- pandas 统计
- 固定指标规则
- AI 生成解释文本

#### Skill 7：`invoice_helper`（开票辅助）

定位：

```text
数据准备层，人工最终确认提交
```

功能：

- 整理开票信息
- 生成标准化开票字段
- 输出待填表格
- 可选：Playwright 引导式填写

#### Skill 8：`tax_filing_assistant`（报税辅助）

定位：

```text
数据准备 + 操作引导，不自动最终提交
```

功能：

- 生成申报数据核对表
- 税额计算辅助
- 操作步骤提示
- 截图 / 日志留档

合规红线：

```text
报税 / 开票最终提交必须人工核对确认
```

#### Skill 9：`finance_knowledge_base`（历史数据查询）

解决问题：

- Excel 数据分散
- 历史查询慢
- 客户长期经营数据难复用

初期方案：

```text
SQLite
```

后期客户和数据量增加后，再考虑 PostgreSQL。

---

## 四、工作流调度：n8n（后期）

n8n 适合做可视化定时任务编排，但不应该成为第一阶段的阻塞项。

典型月度流程：

```text
每月 1 日触发
    ↓
拉取 / 导入上月订单
    ↓
扫描微信文件夹新增附件
    ↓
OCR 识别截图
    ↓
运行 Excel 对账
    ↓
生成报告草稿
    ↓
通知人工复核
```

本地安装示例：

```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

---

## 五、软件技术栈

### 核心依赖

```bash
pip install pandas openpyxl xlsxwriter python-pptx python-docx \
            anthropic openai playwright watchdog keyring sqlalchemy click
```

### 可选依赖

```bash
# 本地 OCR
pip install paddleocr

# Windows GUI 自动化
pip install pywinauto
```

### 技术选型总览

| 层级 | 工具 | 用途 | 当前是否必须 |
|------|------|------|-------------|
| 数据处理 | pandas + openpyxl | Excel 清洗、对账、汇总 | 必须 |
| 报告生成 | python-pptx + python-docx | PPT / Word 生成 | 必须 |
| AI 引擎 | Claude / OpenAI API | OCR 理解、报告文案 | 必须 |
| 浏览器自动化 | Playwright | 电商后台 / 税务系统辅助 | 第二阶段 |
| 文件监听 | watchdog | 微信附件目录监听 | 第二阶段 |
| 密钥管理 | keyring | 平台密码 / token 存储 | 推荐 |
| 数据库 | SQLite | 历史数据存储 | 需要时启用 |
| 工作流 | n8n | 定时任务编排 | 后期 |
| 本地 OCR | PaddleOCR | 高保密场景 | 可选 |

---

## 六、硬件配置建议

结论：

```text
现有普通 Windows PC 完全够用
```

因为当前主要跑的是 Python 脚本、Excel 处理和浏览器自动化，AI 推理交给 Claude / OpenAI API。

| 组件 | 实际最低需求 | 推荐配置 | 说明 |
|------|-------------|---------|------|
| CPU | 4 核 | 8 核 | 足够跑脚本和浏览器 |
| 内存 | 16GB | 32GB | pandas 处理大表更舒服 |
| SSD | 256GB | 512GB+ | 存客户数据和报告 |
| GPU | 不需要 | 不需要 | 不优先跑本地大模型 |
| 显示器 | 1 台 | 2 台 | 一台看数据，一台操作 |
| 网络 | 稳定宽带 | 稳定宽带 | 后台下载和 API 调用需要稳定 |

不建议现阶段为了本地大模型购买 RTX 4090 / 64GB 内存级别硬件。

---

## 七、推荐项目目录结构

当前仓库结构已经接近这个方向：

```text
finance-ai-agent/
├── README.md
├── requirements.txt
├── main.py
├── config/
│   └── settings.yaml
├── skills/
│   ├── excel/          # excel_processor
│   ├── ocr/            # ocr_parser
│   ├── ecommerce/      # ecommerce_scraper
│   ├── report/         # report_generator
│   ├── wechat/         # wechat_monitor
│   └── tax/            # tax_filing_assistant
├── agents/
│   ├── finance_agent/
│   └── workflow_agent/
├── data/
│   ├── orders/
│   ├── invoices/
│   ├── bank/
│   └── reports/
├── db/
├── workflows/
├── prompts/
└── logs/
```

当前 CLI 入口：

```bash
python main.py --help
python main.py excel --help
python main.py ocr --help
python main.py ecommerce --help
python main.py report --help
```

---

## 八、数据安全 & 合规要求

财务数据属于敏感商业信息，必须严肃处理。

### 数据本地化

- 客户原始数据默认只存本地
- 不把客户完整账套上传到无关第三方服务
- 调用 AI API 时，尽量只上传必要字段或脱敏数据

### 密码安全

- 电商平台密码使用 keyring 或浏览器安全存储
- API Key 放 `.env`，不提交代码仓库
- 不在脚本里明文写密码

### 税务合规

- AI 只做数据准备和操作引导
- 报税 / 开票最终提交必须人工确认
- 关键操作保留日志和截图

### 数据备份

- 客户数据按客户、月份分目录
- 重要报告保留 PDF 或不可篡改版本
- 定期备份到外置硬盘或可信存储

---

## 九、真实开发路线图

### Phase 1：立刻产生价值（第 1-2 个月）

目标：

```text
先把最重复、最稳定、最高 ROI 的工作自动化
```

优先顺序：

| 顺序 | 模块 | 功能 | 收益 |
|------|------|------|------|
| 1 | excel_processor | 两表对账、差异标红、统计摘要 | 最容易闭环 |
| 2 | ocr_parser | 截图 -> JSON / CSV | 减少手工录入 |
| 3 | excel + OCR 联动 | 截图 -> OCR -> 写入 Excel -> 对账 | 打通真实流程 |

验收标准：

- 能用真实客户的两张表跑出对账结果
- 能批量识别微信转账截图
- 输出结果可以人工快速复核

### Phase 2：减少点击劳动（第 3-4 个月）

模块：

```text
ecommerce_scraper
```

目标：

- 自动或半自动下载订单
- 自动整理平台导出文件
- 统一字段格式

原则：

- Cookie 复用
- 人工过验证码
- 不对抗平台风控

### Phase 3：报告自动化（第 4-5 个月）

模块：

```text
report_generator
finance_analyzer
```

目标：

- 自动生成 Excel 月报
- 自动生成 PPT 草稿
- 自动生成利润分析说明

### Phase 4：税务 / 开票辅助（第 6 个月以后）

模块：

```text
invoice_helper
tax_filing_assistant
```

目标：

- 数据准备
- 操作引导
- 人工最终确认

### Phase 5：全流程 Agent 化（长期）

只有当前面脚本都稳定后，再考虑：

```text
一句话驱动整月工作流
```

这不是第一阶段目标。

---

## 十、成本 & ROI 估算

### 月度运营成本

| 项目 | 费用 | 说明 |
|------|------|------|
| Claude / OpenAI API | ¥80-300 / 月 | OCR 和文案生成使用量决定 |
| n8n 本地部署 | ¥0 | Docker 本地运行 |
| VPS | 可选 ¥30-60 / 月 | 需要定时后台运行时再考虑 |
| Python / 开源库 | ¥0 | 开源 |

### ROI 粗略估算

| 场景 | 当前耗时 | 自动化后 | 每月节省 |
|------|---------|---------|---------|
| Excel 对账 | 15h | 2h | 13h |
| 截图录入 | 8h | 1h | 7h |
| 月报制作 | 10h | 2h | 8h |
| 订单下载整理 | 6h | 0.5h | 5.5h |
| 合计 | 39h / 月 | 5.5h / 月 | 33.5h / 月 |

真正目标不是“系统看起来高级”，而是：

```text
每个月少工作 30 小时
```

---

## 十一、快速开始

### 1. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 查看当前 CLI

```bash
python main.py --help
```

### 4. 第一件真正该做的事

不是继续扩展架构，而是直接开始：

```text
excel_processor
```

最小任务：

```text
输入两张 Excel
-> 按指定字段匹配
-> 输出差异标红 Excel
-> 输出摘要统计
```

---

## 十二、最后的判断

这个项目真正有价值的部分不是：

```text
AI
```

而是：

```text
你对真实财务流程的理解
```

AI 只是：

```text
把这些流程自动化
```

所以这套系统应该保持：

```text
小而强
```

而不是：

```text
大而全
```
