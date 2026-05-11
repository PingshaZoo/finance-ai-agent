# 代账财务 AI 赋能自动化大项目规划

> 适用角色：小企业代理记账财务人员  
> 文档版本：v1.0 | 2026-05  
> 目标：用 AI Agent + 自动化工具，将重复性财务工作提效 60%+

---

## 一、工作场景全景梳理

| # | 工作场景 | 核心动作 | 数据来源 | 产出物 |
|---|---------|---------|---------|-------|
| 1 | 客户沟通 & 资金录入 | 读微信聊天记录、看转账截图 | 微信PC端、图片 | 收支流水表 |
| 2 | 电商多平台数据采集 | 登录后台、下载订单 | 淘宝/京东/拼多多/抖音/微店 | 订单明细Excel |
| 3 | 数据核对 & 对账 | 两表比对、差异标记 | Excel多文件 | 对账差异报告 |
| 4 | 财务汇总 & 报告 | 汇总收支盈亏、制作Excel/PPT | 各类数据汇总 | 客户汇报材料 |
| 5 | 税务操作 | 开发票、报税 | 国家税务总局网站 | 发票/申报记录 |

---

## 二、推荐技术栈 & Skill 体系

### 2.1 核心 Skill 清单（按优先级排序）

#### 🥇 第一优先级——立即构建（高频 + 高回报）

**Skill 1: `excel_processor`（Excel 读写与对账）**

```
用途：读取多个Excel/CSV，做数据清洗、两表对比、差异标记、汇总
技术：Python + openpyxl/pandas + xlsxwriter
触发词："核对两个表" / "对账" / "汇总收支" / "导出报表"
```

**Skill 2: `ocr_receipt_parser`（图片/截图识别）**

```
用途：识别微信转账截图、银行流水截图、电商发货单图片，提取金额、时间、备注
技术：Claude Vision API / PaddleOCR + 结构化提取 Prompt
触发词："这是转账截图" / "帮我读一下这张图" / "识别金额"
```

**Skill 3: `report_generator`（Excel + PPT 报告生成）**

```
用途：根据汇总数据，自动生成月度财务报告PPT和Excel
技术：python-pptx + openpyxl + Claude 生成文案
触发词："给客户做报告" / "月报" / "汇报材料"
```

#### 🥈 第二优先级——第二阶段构建（中频 + 中等复杂度）

**Skill 4: `ecommerce_scraper`（电商后台数据采集）**

```
用途：自动登录各平台后台，下载订单数据（或解析已下载文件）
技术：Playwright 无头浏览器 + Cookie管理 + 各平台文件格式解析
支持平台：淘宝、京东、拼多多、抖音小店、微信微店
触发词："下载订单" / "拉取平台数据" / "同步电商数据"
⚠️ 注意：各平台反爬策略不同，微信微店最难，优先做淘宝/拼多多
```

**Skill 5: `wechat_bill_parser`（微信聊天账单解析）**

```
用途：解析微信导出的聊天记录文本，提取客户发送的金额、时间、说明信息
技术：正则 + Claude NLP 理解 + 结构化输出
触发词："解析微信记录" / "客户发来的账单"
```

**Skill 6: `invoice_helper`（开票辅助）**

```
用途：根据已有信息，生成开票所需的标准化数据表，并引导操作增值税发票系统
技术：表单数据生成 + 操作指引 + (可选) RPA 辅助填表
触发词："开发票" / "填开票信息"
```

#### 🥉 第三优先级——长期规划（低频 + 高复杂度）

**Skill 7: `tax_filing_assistant`（报税辅助）**

```
用途：根据财务数据，生成申报所需数字，引导或半自动填写税务申报表
技术：Claude + 数据映射规则 + (可选) 浏览器自动化
⚠️ 风险：税务操作涉及合规，建议先做"数据准备"层，人工最终确认
```

**Skill 8: `multi_client_manager`（多客户数据隔离管理）**

```
用途：管理多个客户的数据文件夹、自动路由到正确客户的数据
技术：文件系统管理 + SQLite/本地数据库
```

---

## 三、AI Agent 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    主控 Agent (Orchestrator)              │
│          Claude API / 本地 LLM (可选 Ollama)              │
└──────────┬──────────────────────────────────┬───────────┘
           │                                  │
    ┌──────▼──────┐                   ┌───────▼───────┐
    │  数据采集层   │                   │   处理输出层   │
    │             │                   │               │
    │ • OCR Agent │                   │ • Excel Agent │
    │ • 爬虫 Agent │                   │ • PPT Agent   │
    │ • 文件解析   │                   │ • 报告 Agent  │
    └──────┬──────┘                   └───────┬───────┘
           │                                  │
           └──────────────┬───────────────────┘
                          │
                 ┌────────▼────────┐
                 │   本地数据存储   │
                 │  (SQLite / 文件) │
                 └─────────────────┘
```

### Agent 交互流程示例（月度对账）

```
用户说："帮我做5月份的对账，客户是XX公司"
     ↓
主控 Agent 解析意图
     ↓
① 调用 file_reader → 读取该客户文件夹下的5月数据文件
② 调用 ecommerce_scraper → 抓取/读取电商订单
③ 调用 ocr_receipt_parser → 识别微信截图金额
④ 调用 excel_processor → 两表核对，标记差异
⑤ 调用 report_generator → 生成汇报Excel/PPT
     ↓
输出：差异报告 + 客户汇报材料
```

---

## 四、软硬件条件要求

### 4.1 硬件配置

| 组件 | 最低要求 | 推荐配置 | 用途 |
|------|---------|---------|------|
| CPU | 4核 | 8核 i5/i7 或 AMD R5 | 跑 Python 脚本、LLM 推理 |
| 内存 | 8GB | 16GB+ | pandas 大表处理、浏览器自动化 |
| 存储 | 256GB SSD | 512GB SSD | 客户数据文件存储 |
| 显卡 | 集成显卡 | 可选 GTX1660+ | 本地 OCR 加速（可不用） |
| 网络 | 稳定宽带 | 稳定宽带 | 访问各电商平台、税务网站 |
| 操作系统 | Windows 10 | Windows 11 | 运行微信PC版、Office |

> 💡 **现有 Windows PC 完全够用**，不需要额外购买设备。

### 4.2 软件环境

**必装软件：**

```
Python 3.10+          # 核心运行环境
pip 包：
  - pandas            # 数据处理
  - openpyxl          # Excel读写
  - xlsxwriter        # Excel高级生成
  - python-pptx       # PPT生成
  - playwright        # 浏览器自动化
  - paddleocr         # 本地OCR（可选）
  - requests          # HTTP请求
  - anthropic         # Claude API SDK
  
Node.js 18+           # 部分工具依赖
微信PC版              # 与客户沟通
Microsoft Office      # Excel/PPT操作
```

**可选增强软件：**

```
Ollama               # 本地小模型，处理隐私数据用
Docker Desktop       # 隔离运行环境
VS Code              # 脚本编辑
```

### 4.3 账号 & API 资源

| 资源 | 用途 | 备注 |
|------|------|------|
| Claude API Key | 核心 AI 能力 | 按量计费，月均约 ¥50-200 |
| 各电商平台账号 | 数据下载 | 需要客户授权子账号或共享登录 |
| 国家税务总局账号 | 报税开票 | 客户自己的账号，需授权 |

---

## 五、项目建设路线图

### Phase 1：基础能力搭建（第 1-2 个月）

**目标：解决最高频、最痛的手工操作**

```
Week 1-2: 环境搭建
  ✅ 安装 Python、依赖包
  ✅ 申请 Claude API Key
  ✅ 建立客户数据文件夹规范（按客户/年月组织）

Week 3-4: excel_processor Skill
  ✅ 实现 Excel 读取、数据清洗
  ✅ 实现两表对比（VLOOKUP逻辑 Python化）
  ✅ 自动标红差异行并输出报告

Week 5-6: ocr_receipt_parser Skill
  ✅ 实现微信截图上传 → Claude Vision 识别
  ✅ 提取：金额、时间、付款方/收款方、备注
  ✅ 输出标准化 CSV 行追加到流水表

Week 7-8: report_generator Skill
  ✅ Excel月报模板自动填充
  ✅ PPT 汇报模板自动生成（收入/支出/盈亏/欠款）
```

**Phase 1 预期收益：**
- Excel 对账时间：从 3小时 → 20分钟
- 截图录入：从 1小时 → 5分钟（批量上传识别）
- 月报制作：从 2小时 → 30分钟

---

### Phase 2：数据采集自动化（第 3-4 个月）

**目标：打通电商平台数据获取**

```
Week 9-10: ecommerce_scraper（淘宝/拼多多）
  ✅ Playwright 登录会话管理
  ✅ 订单列表分页抓取
  ✅ 统一输出格式（日期/订单号/金额/状态/平台）

Week 11-12: ecommerce_scraper（京东/抖音）
  ✅ 扩展支持更多平台
  ✅ 广告投流费用单独解析
  ✅ 平台扣费字段提取（技术服务费、退款等）

Week 13-14: wechat_bill_parser
  ✅ 解析微信聊天导出文件
  ✅ 识别金额语句（"转你500"、"收了1200"等）
  ✅ 半自动确认流程（AI 建议 + 人工确认）
```

---

### Phase 3：主控 Agent & 税务辅助（第 5-6 个月）

**目标：串联所有 Skill，实现端到端自动化**

```
Week 15-18: 主控 Orchestrator Agent
  ✅ 统一入口（Web UI 或 命令行）
  ✅ 自然语言任务派发
  ✅ 多客户数据隔离管理
  ✅ 任务日志 & 错误处理

Week 19-22: invoice_helper & tax_filing_assistant
  ✅ 开票数据自动整理
  ✅ 申报表数据预填（人工最终核对）
  ✅ 税务操作步骤引导文档
```

---

## 六、数据安全 & 合规要求

```
⚠️  重要：财务数据属于敏感商业信息，必须注意以下事项

1. 客户数据本地化存储
   - 不要将客户财务数据上传到第三方云服务
   - Claude API 调用时，避免发送客户名称、银行账号等敏感信息
   - OCR 识别截图时，可使用本地 PaddleOCR（离线）替代云API

2. 访问控制
   - 各客户数据文件夹设置独立密码
   - 电商平台登录凭据加密存储（使用 keyring 库）
   - 不在脚本中明文写密码

3. 税务操作
   - 税务申报必须人工最终审核确认
   - AI 只做"数据准备"和"操作引导"，不做自动提交
   - 保留所有操作日志备查

4. 数据备份
   - 每日自动备份到本地外置硬盘
   - 重要报告保存 PDF 不可修改版本
```

---

## 七、推荐项目目录结构

```
ai_accounting_agent/
│
├── README.md                    # 项目说明
├── config/
│   ├── settings.yaml            # 全局配置（API Key等，加密）
│   └── clients.yaml             # 客户信息配置
│
├── skills/                      # 各 Skill 模块
│   ├── excel_processor/
│   │   ├── __init__.py
│   │   ├── reader.py            # Excel读取
│   │   ├── reconcile.py         # 对账核对
│   │   └── reporter.py          # 报告生成
│   ├── ocr_receipt_parser/
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── report_generator/
│   │   ├── __init__.py
│   │   ├── excel_report.py
│   │   └── ppt_report.py
│   ├── ecommerce_scraper/
│   │   ├── __init__.py
│   │   ├── taobao.py
│   │   ├── jd.py
│   │   ├── pdd.py
│   │   └── douyin.py
│   └── invoice_helper/
│       └── __init__.py
│
├── agent/
│   ├── orchestrator.py          # 主控 Agent
│   └── router.py                # 任务路由
│
├── templates/                   # Excel/PPT模板
│   ├── monthly_report.xlsx
│   └── client_ppt.pptx
│
├── data/                        # 客户数据（.gitignore排除）
│   ├── 客户A/
│   │   ├── 2026-05/
│   │   └── 2026-04/
│   └── 客户B/
│
├── logs/                        # 操作日志
└── requirements.txt             # Python依赖
```

---

## 八、快速开始（第一步实操）

### 步骤 1：安装 Python 环境

```bash
# 下载安装 Python 3.11 from python.org
# 然后安装核心依赖
pip install pandas openpyxl xlsxwriter python-pptx anthropic pillow
```

### 步骤 2：测试 Excel 对账（最快见效的起点）

创建 `reconcile.py`，实现两表比对：

```python
import pandas as pd

def reconcile(file_a, file_b, key_col, amount_col):
    """
    对比两个Excel表，找出金额差异
    file_a: 系统账（如电商后台下载）
    file_b: 客户账（如银行流水）
    key_col: 匹配字段（如订单号/日期）
    amount_col: 金额字段
    """
    df_a = pd.read_excel(file_a)
    df_b = pd.read_excel(file_b)
    
    merged = pd.merge(df_a, df_b, on=key_col, suffixes=('_系统', '_客户'), how='outer')
    merged['差异'] = merged[f'{amount_col}_系统'].fillna(0) - merged[f'{amount_col}_客户'].fillna(0)
    merged['状态'] = merged['差异'].apply(
        lambda x: '✅ 一致' if abs(x) < 0.01 else f'❌ 差异 {x:+.2f}'
    )
    
    # 输出结果
    output = '对账结果.xlsx'
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        merged.to_excel(writer, index=False, sheet_name='对账明细')
        # 标红差异行（xlsxwriter格式化）
    
    print(f"✅ 对账完成，共 {len(merged)} 条，差异 {(merged['差异'].abs() > 0.01).sum()} 条")
    return merged

# 使用示例
reconcile('电商订单.xlsx', '银行流水.xlsx', key_col='订单号', amount_col='金额')
```

### 步骤 3：测试 OCR 截图识别

```python
import anthropic, base64
from pathlib import Path

client = anthropic.Anthropic(api_key="你的API_KEY")

def parse_receipt_image(image_path):
    image_data = base64.b64encode(Path(image_path).read_bytes()).decode()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}
                },
                {
                    "type": "text",
                    "text": """请识别这张转账/收款截图，提取以下信息并以JSON格式返回：
                    {
                      "金额": "",
                      "时间": "",
                      "付款方": "",
                      "收款方": "",
                      "备注": "",
                      "交易类型": "收入/支出"
                    }
                    如果某字段无法识别，填null。"""
                }
            ]
        }]
    )
    return response.content[0].text

# 使用
result = parse_receipt_image("微信截图.jpg")
print(result)
```

---

## 九、成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| Claude API | ¥50-300/月 | 按使用量，处理大量OCR时偏高 |
| Python 环境 | 免费 | 开源 |
| 服务器/VPS | 可选，¥30-50/月 | 如需定时自动运行 |
| 总计 | ¥50-350/月 | 视使用量 |

**ROI 估算：**
- 假设每月节省 20 小时手工操作
- 时间价值 ¥50/小时 → 节省 ¥1000/月
- **回报率约 3-20倍**

---

## 十、后续扩展方向

```
📌 短期扩展
  - 微信机器人接入（itchat / WeChatPad）
    → 客户发截图，自动回复"已记录 ✅"
  
  - 定时自动化
    → 每月1号自动拉取上月数据，生成报告草稿

📌 中期扩展  
  - 多客户 Web 管理后台
    → 本地 Flask/FastAPI + 简单前端
    → 每个客户独立看板

📌 长期扩展
  - 接入记账软件 API（如金蝶、用友云）
  - 智能预警（欠款超期、税务申报截止日提醒）
  - 多人协作（助理 + 主管审核流程）
```

---

*文档由 AI 协助生成，建议根据实际业务情况调整优先级和技术选型。*