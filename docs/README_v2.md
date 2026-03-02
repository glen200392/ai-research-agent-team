# AI Investment Pipeline v2.0
## 自架版三市場 AI 投資日報系統

> 完全脫離封閉平台、可自主部署的 AI 量化投資研究自動化系統  
> 支援台股 / 美股 / 日股，每日自動執行並產出 PDF 報告 + 互動儀表板

---

## 目錄

- [系統特色](#系統特色)
- [架構總覽](#架構總覽)
- [多模型 LLM 策略](#多模型-llm-策略)
- [Pipeline 九大 Stage](#pipeline-九大-stage)
- [圖表視覺化（12 種）](#圖表視覺化)
- [Streamlit Dashboard](#streamlit-dashboard)
- [快速開始（本地）](#快速開始本地)
- [GCP 部署指南](#gcp-部署指南)
- [環境變數設定](#環境變數設定)
- [Repo 結構](#repo-結構)
- [費用估算](#費用估算)
- [技術選型說明](#技術選型說明)

---

## 系統特色

| 特色 | 說明 |
|------|------|
| **三市場覆蓋** | 台股（07:00 TST）、美股＋日股（22:00 TST）每日自動執行 |
| **九階段分析** | Macro → 供應鏈 → 市場研究 → 情緒 → 技術 → 基本面 → 綜合評分 → 風險 → 報告 |
| **多模型多層次** | 開源模型主力（DeepSeek / Qwen3 / FinGPT）+ 商業模型保底，三層 Fallback |
| **12 種圖表** | K 線、雷達、熱圖、Sankey、泡泡圖、VaR/CVaR 等完整視覺化 |
| **專業 PDF** | Jinja2 HTML 模板 + WeasyPrint，含所有圖表的排版報告 |
| **互動儀表板** | Streamlit，部署於 GCP Cloud Run，支援歷史趨勢查詢 |
| **成本優化** | 87% 成本低於純商業 API 方案（~$10-20/月 vs ~$80-150/月） |
| **完全可攜** | Docker 化，本地或 GCP 皆可一鍵部署 |
| **高可用** | Prefect retry + Redis checkpoint，Stage 失敗自動恢復 |
| **全程可觀測** | Langfuse trace 每個 Stage 的 token 用量、延遲、成本 |

---

## 架構總覽

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: ORCHESTRATION — Prefect                               │
│  07:00 TST → Taiwan Pipeline                                    │
│  22:00 TST → US Pipeline  ─┐                                   │
│              Japan Pipeline ┘  (平行執行)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│  LAYER 2: AGENT EXECUTION — LangGraph StateGraph                │
│                                                                 │
│  [Macro 0.5]──►[SupplyChain 0.3]──►[Market 1]──►[Sentiment 1.5]│
│                                                      │          │
│                                         ┌────────────┴───────┐  │
│                                         ▼                    ▼  │
│                                  [Technical 2]   [Fundamental 3] │
│                                   (async)          (async)      │
│                                         └────────────┬───────┘  │
│                                                      ▼          │
│                              [Composite 4]──►[Risk 5]──►[PDF 6] │
│                                                           │     │
│                                                    [Email 7]    │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│  LAYER 3: INFRASTRUCTURE                                        │
│  PostgreSQL │ Redis │ Langfuse │ Streamlit Dashboard            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 多模型 LLM 策略

### 三層 Fallback 架構

```
Tier 1 (本地 Ollama)    → 零成本，適合高頻/輕量 Stage
      ↓ 失敗或品質不足
Tier 2 (開源 API)       → DeepSeek V3/R1、Qwen3，低成本高品質
      ↓ 失敗或品質不足
Tier 3 (商業 API)       → GPT-4o、Claude 3.5 Sonnet，品質保底
```

### Stage 模型路由表

| Stage | 任務 | 主力模型 | Tier 1 本地 | Tier 3 保底 |
|-------|------|---------|------------|------------|
| 0.5 Macro | 數值計算 + 指標正規化 | DeepSeek-V3 API | Qwen3:8b | GPT-4o-mini |
| 0.3 Supply Chain | 結構化資訊抽取 | Qwen3:14b (本地) | DeepSeek-V3 | GPT-4o-mini |
| 1 Market Research | 長文閱讀 + 摘要 | Qwen3:32b | Qwen3:14b | Claude 3.5 Sonnet |
| 1.5 Sentiment | 情緒分類（高頻） | FinGPT (本地) | Qwen3:8b | GPT-4o-mini |
| 2 Technical | 技術指標信號 | DeepSeek-R1 (8b 本地) | Qwen3:14b | GPT-4o |
| 3 Fundamental | 財報 + DCF 分析 | Qwen3:32b API | DeepSeek-V3 | Claude 3.5 Sonnet |
| 4 Composite | 多維加權整合 | DeepSeek-V3 API | Qwen3:32b | Claude 3.5 Sonnet |
| 5 CVaR + Risk | 統計計算 + 情境 | DeepSeek-R1 API | Qwen3:32b | GPT-4o |
| 6 Report | 繁中長文寫作 | Qwen3:32b API | DeepSeek-V3 | Claude 3.5 Sonnet |
| 7 Email | 簡短摘要 | Qwen3:8b (本地) | — | — |

### 開源模型選型理由

**DeepSeek-V3 / R1**
- 成本：$0.28/M tokens（比 Claude Sonnet 低 94%）
- 推理能力：BizFinBench 數值計算 64.04 分（Claude 3.5: 63.18 分）
- 適合：Macro 計算、技術指標判讀、CVaR 統計

**Qwen3-32B / 14B / 8B**
- 119 語言支援，繁體中文品質最佳
- 適合：台股/日股報告生成、供應鏈分析、多語言市場研究
- 32B 版本在中文寫作任務上優於同級開源模型

**FinGPT (Llama3.1-8B fine-tuned)**
- 專為金融情緒分析微調，成本 < $300/次訓練週期
- 在 FinGPT-Forecaster 資料集準確率接近 GPT-4o
- 本地部署，Stage 1.5 高頻調用零 API 成本

---

## Pipeline 九大 Stage

```
Stage 0.5  Macro Scoring
           ├── 資料來源：FRED API（10Y-2Y 利差、聯邦基金利率、USD Index）
           ├── 台灣 PMI 資料
           └── 輸出：Macro Score (0-10) + 市場態勢 (expansion/contraction/...)

Stage 0.3  Supply Chain Temperature  [台股專用]
           ├── 爬取：TrendForce、工商時報、供應鏈新聞
           ├── 分析：上游/中游/下游廠商溫度
           └── 輸出：SC Temperature (0-10) + 瓶頸/機會節點清單

Stage 1    Market Research
           ├── 資料來源：Bloomberg、Reuters、CNBC、鉅亨網、工商時報
           ├── 爬取當日重要新聞、法說會摘要、外資報告
           └── 輸出：市場研究摘要 + 重要事件清單

Stage 1.5  Sentiment Aggregation
           ├── 輸入：Stage 1 新聞 + 社群媒體資料
           ├── 模型：FinGPT (本地) 逐條情緒分類
           └── 輸出：市場情緒分 (0-10) + 個股情緒分 dict

Stage 2    Technical Analysis  [async 平行]
           ├── 資料：yfinance OHLCV
           ├── 指標：RSI/MACD/Bollinger/ATR/VWAP/ADX/Ichimoku 等 20+ 種
           ├── 訊號：買入/賣出/持有 + 支撐壓力位
           └── 輸出：每支標的技術訊號 + 市場廣度

Stage 3    Fundamental Analysis  [async 平行]
           ├── 資料：財務報表、本益比、EV/EBITDA
           ├── 模型：DCF 估值、可比公司分析
           └── 輸出：每支標的內在價值 + 品質評分

Stage 4    Composite Scoring
           ├── 輸入：Stage 0.5 + 1.5 + 2 + 3 加權整合
           ├── 權重：Macro(15%) + SC(10%) + Sentiment(15%) + Technical(35%) + Fundamental(25%)
           └── 輸出：每支標的 0-100 分 + Buy/Watch/Sell 清單

Stage 5    Risk Management (CVaR)
           ├── 計算：VaR(95%/99%)、CVaR、最大回撤、Kelly 倉位
           ├── 壓力測試：市場崩盤 / 利率衝擊 / 匯率衝擊情境
           └── 輸出：RiskState + Kelly 建議倉位 dict

Stage 6    Report Generation + Email
           ├── 圖表生成：12 種 Plotly/mplfinance 圖表
           ├── PDF 組裝：Jinja2 HTML → WeasyPrint PDF
           ├── 上傳：GCP Cloud Storage
           └── Email：SMTP 寄送 PDF 附件 + HTML 摘要
```

---

## 圖表視覺化

系統共生成 **12 種圖表**，嵌入 PDF 報告並於 Streamlit 儀表板互動顯示。

### 所有市場共用（8 種）

| 圖表 | 技術庫 | 說明 |
|------|--------|------|
| K 線圖 + 均線 + 成交量 | mplfinance | 60 日 OHLCV + MA5/20/60 + 布林帶 + 成交量柱 |
| RSI + MACD 雙指標 | mplfinance subplot | RSI(14) 超買超賣線 + MACD/Signal/Histogram |
| 五維度雷達圖 | Plotly Scatterpolar | 總體/情緒/技術/基本面/風險 五軸，每支股票一張 |
| Composite Score 排行 | Plotly Horizontal Bar | 候選股分數由高到低，Buy/Watch/Sell 色彩分層 |
| 相關性熱圖 | Plotly Heatmap | 標的間 60 日報酬相關係數矩陣 |
| CVaR / VaR 長條圖 | Plotly Bar + Line | 各標的 95%/99% VaR 與 CVaR 視覺化比較 |
| Kelly 倉位圓餅圖 | Plotly Pie/Donut | 建議投資組合倉位分配 |
| 情緒時序趨勢線 | Plotly Line | 30 日 Sentiment Score 走勢 + 重要事件標記 |

### 台股專用（2 種）

| 圖表 | 技術庫 | 說明 |
|------|--------|------|
| AI 供應鏈溫度熱圖 | Plotly Heatmap | 上游/中游/下游 × 廠商溫度矩陣，瓶頸節點紅標 |
| 產業鏈資金流向 Sankey | Plotly Sankey | AI 伺服器 → 晶片 → 封裝 → PCB → 系統的資金流向 |

### 美股專用（1 種）

| 圖表 | 技術庫 | 說明 |
|------|--------|------|
| AI CapEx 曝險泡泡圖 | Plotly Bubble Scatter | X=EV/EBITDA, Y=營收成長率, Size=AI CapEx 比例 |

### 日股專用（1 種）

| 圖表 | 技術庫 | 說明 |
|------|--------|------|
| 日圓敏感度矩陣 | Plotly Annotated Heatmap | 各標的在不同日圓匯率情境下的預估盈餘變動率 |

---

## Streamlit Dashboard

部署於 GCP Cloud Run，提供即時互動式分析介面。

### 頁面結構

```
📊 總覽          三市場 Macro Score 卡片 + 當日 Top Buy 清單
🇹🇼 台股         Composite 排行 + 供應鏈熱圖 + Sankey + 個股K線/雷達 + PDF下載
🇺🇸 美股         Composite 排行 + AI CapEx 泡泡圖 + 動能篩選表 + PDF下載
🇯🇵 日股         Composite 排行 + 日圓敏感度矩陣 + PDF下載
📈 歷史趨勢      三市場 Score 30日走勢 + Macro 時序 + 月績效回顧
```

### 存取方式

```bash
# 本地
docker-compose up streamlit
# 瀏覽器開啟 http://localhost:8501

# GCP Cloud Run（部署後）
https://streamlit-app-XXXX-an.a.run.app
```

---

## 快速開始（本地）

### 前置需求

- Docker Desktop（含 Compose）
- Python 3.12+
- NVIDIA GPU（選配，用於 Ollama 本地推理）

### 步驟 1：Clone Repo

```bash
git clone https://github.com/glen200392/ai-research-agent-team.git
cd ai-research-agent-team
```

### 步驟 2：設定環境變數

```bash
cp .env.example .env
# 編輯 .env，填入必要的 API Keys（詳見下方環境變數說明）
```

### 步驟 3：啟動基礎設施

```bash
# 啟動 PostgreSQL + Redis + Prefect + Langfuse + Streamlit
docker-compose up -d

# 確認所有服務正常
docker-compose ps
```

### 步驟 4：初始化 DB Schema

```bash
docker-compose exec postgres psql -U pipeline_user -d ai_pipeline -f /docker-entrypoint-initdb.d/init.sql
```

### 步驟 5：拉取 Ollama 模型（選配，需 GPU）

```bash
# 輕量模型（推薦先裝）
docker-compose exec ollama ollama pull qwen3:8b
docker-compose exec ollama ollama pull deepseek-r1:8b

# 高品質模型（需 20GB+ VRAM 或耐心等 CPU 推理）
docker-compose exec ollama ollama pull qwen3:32b
```

### 步驟 6：安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 步驟 7：手動觸發 Pipeline 測試

```bash
# 測試台股 Pipeline
python -m pipelines.taiwan_pipeline --date 2026-03-02 --dry-run

# 正式執行
python -m pipelines.taiwan_pipeline --date 2026-03-02
```

### 步驟 8：查看結果

| 服務 | URL |
|------|-----|
| Streamlit Dashboard | http://localhost:8501 |
| Prefect UI | http://localhost:4200 |
| Langfuse Traces | http://localhost:3000 |
| PDF 報告輸出 | `./reports/YYYY-MM-DD/` |

---

## GCP 部署指南

### 前置需求

```bash
# 安裝 gcloud CLI
brew install google-cloud-sdk  # macOS
# 或參考 https://cloud.google.com/sdk/docs/install

# 登入並設定 Project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 一鍵建立 GCP 資源

```bash
# 設定環境
export PROJECT_ID="ai-investment-pipeline"
export REGION="asia-east1"

# 執行自動化部署腳本
chmod +x deploy/gcp_setup.sh
./deploy/gcp_setup.sh

# 腳本會自動建立：
# - Cloud SQL (PostgreSQL 15)
# - Memorystore (Redis 7.2)
# - Artifact Registry
# - Cloud Storage Bucket
# - Secret Manager secrets（需手動填值）
# - Service Account + IAM roles
# - VPC Connector
```

### 填入 Secrets

```bash
# 填入各 API Keys
echo -n "sk-your-openai-key" | gcloud secrets versions add OPENAI_API_KEY --data-file=-
echo -n "your-deepseek-key"  | gcloud secrets versions add DEEPSEEK_API_KEY --data-file=-
echo -n "your-qwen-key"      | gcloud secrets versions add QWEN_API_KEY --data-file=-
echo -n "your-fred-key"      | gcloud secrets versions add FRED_API_KEY --data-file=-
# ... 其他 secrets
```

### 部署 Pipeline Worker

```bash
# Build & Push Docker Image
docker build -f infra/Dockerfile.pipeline -t gcr.io/$PROJECT_ID/pipeline-worker:latest .
docker push gcr.io/$PROJECT_ID/pipeline-worker:latest

# Deploy to Cloud Run
./deploy/deploy_pipeline.sh
```

### 部署 Streamlit Dashboard

```bash
docker build -f infra/Dockerfile.dashboard -t gcr.io/$PROJECT_ID/streamlit-app:latest .
docker push gcr.io/$PROJECT_ID/streamlit-app:latest

./deploy/deploy_dashboard.sh
```

### 設定 Cloud Scheduler（自動排程）

```bash
# 台股 07:00 TST
gcloud scheduler jobs create http taiwan-pipeline-07h \
  --schedule="0 7 * * *" \
  --time-zone="Asia/Taipei" \
  --uri="https://pipeline-worker-XXXX-an.a.run.app/trigger" \
  --message-body='{"market":"TW"}' \
  --http-method=POST

# 美股+日股 22:00 TST
gcloud scheduler jobs create http us-jp-pipeline-22h \
  --schedule="0 22 * * *" \
  --time-zone="Asia/Taipei" \
  --uri="https://pipeline-worker-XXXX-an.a.run.app/trigger" \
  --message-body='{"market":"US,JP"}' \
  --http-method=POST
```

---

## 環境變數設定

複製 `.env.example` 為 `.env` 並填入以下值：

```bash
# ── LLM APIs ────────────────────────────────────────────────────
OPENAI_API_KEY=sk-...              # GPT-4o fallback
ANTHROPIC_API_KEY=sk-ant-...       # Claude fallback
DEEPSEEK_API_KEY=sk-...            # 主力模型（Tier 2）
QWEN_API_KEY=...                   # 主力模型（Tier 2）

# ── 資料 APIs ────────────────────────────────────────────────────
FRED_API_KEY=...                   # 美聯儲經濟資料（Macro Stage）
LANGFUSE_SECRET_KEY=sk-lf-...      # LLM Observability
LANGFUSE_PUBLIC_KEY=pk-lf-...

# ── 基礎設施 ─────────────────────────────────────────────────────
DATABASE_URL=postgresql://pipeline_user:PASSWORD@localhost:5432/ai_pipeline
REDIS_URL=redis://localhost:6379
OLLAMA_BASE_URL=http://localhost:11434

# ── Email ────────────────────────────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app-password         # Gmail App Password
EMAIL_RECIPIENT=glen200392@gmail.com

# ── GCP（生產環境）──────────────────────────────────────────────
GCP_PROJECT_ID=ai-investment-pipeline
GCP_REGION=asia-east1
GCS_BUCKET=ai-investment-reports
```

---

## Repo 結構

```
ai-research-agent-team/
├── agents/                    # LangGraph Agent 節點
│   ├── base_agent.py          # 抽象基類 + LLM Router
│   ├── macro_scoring.py       # Stage 0.5
│   ├── supply_chain.py        # Stage 0.3 (TW)
│   ├── market_research.py     # Stage 1
│   ├── sentiment.py           # Stage 1.5 (FinGPT)
│   ├── technical_analysis.py  # Stage 2 (async)
│   ├── fundamental_analysis.py# Stage 3 (async)
│   ├── composite_scoring.py   # Stage 4
│   ├── risk_management.py     # Stage 5
│   ├── report_generator.py    # Stage 6
│   └── email_sender.py        # Stage 7
│
├── llm/                       # 多模型 LLM 路由層
│   ├── router.py              # 三層 Fallback Router
│   ├── models.py              # 模型配置清單
│   ├── quality_checker.py     # 輸出品質檢核
│   └── cost_tracker.py        # Token 費用追蹤
│
├── state/                     # Pydantic State Schemas
│   ├── pipeline_state.py      # PipelineState TypedDict
│   └── sub_states.py          # MacroState, RiskState 等
│
├── pipelines/                 # Prefect Flow 定義
│   ├── master_flow.py         # 主排程 Flow
│   ├── taiwan_pipeline.py
│   ├── us_pipeline.py
│   └── japan_pipeline.py
│
├── charts/                    # 圖表生成工廠（12種）
│   ├── factory.py             # ChartFactory 主類
│   ├── candlestick.py         # K線圖 (mplfinance)
│   ├── radar.py               # 五維度雷達圖
│   ├── heatmaps.py            # 供應鏈熱圖 + 相關性熱圖
│   ├── risk_charts.py         # VaR/CVaR/Kelly
│   └── sankey.py              # 產業鏈 Sankey (TW)
│
├── templates/                 # Jinja2 HTML 報告模板
│   ├── base_report.html.j2
│   ├── tw_report_body.html.j2
│   ├── us_report_body.html.j2
│   ├── jp_report_body.html.j2
│   └── email_summary.html.j2
│
├── dashboard/                 # Streamlit Dashboard
│   ├── app.py
│   ├── pages/
│   │   ├── overview.py
│   │   ├── taiwan.py
│   │   ├── us.py
│   │   ├── japan.py
│   │   └── history.py
│   └── components/
│       ├── score_cards.py
│       ├── chart_widgets.py
│       └── pdf_viewer.py
│
├── infra/                     # 基礎設施
│   ├── docker-compose.yml     # 本地開發環境
│   ├── docker-compose.prod.yml# GCP 生產覆蓋
│   ├── Dockerfile.pipeline
│   ├── Dockerfile.dashboard
│   ├── init.sql               # PostgreSQL Schema
│   └── prefect.yaml           # Prefect 部署設定
│
├── deploy/                    # GCP 部署腳本
│   ├── gcp_setup.sh           # 一鍵建立 GCP 資源
│   ├── deploy_pipeline.sh
│   └── deploy_dashboard.sh
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── architecture_design.md # 完整架構設計文件
│   ├── llm_model_selection.md # 模型選型詳細說明
│   ├── gcp_deployment_guide.md
│   └── local_dev_guide.md
│
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 費用估算

### 本地部署（每月）

| 項目 | 說明 | 月費 |
|------|------|------|
| 本機電費 | GPU 推理，每日 2 次各 ~30 分鐘 | ~$2-5 |
| DeepSeek API | Stage 0.5 / 4 / 5 | ~$3-5 |
| Qwen API | Stage 1 / 3 / 6 | ~$5-8 |
| GPT/Claude fallback | 約 10% 調用量 | ~$2-5 |
| **合計** | | **~$12-23/月** |

### GCP 雲端部署（每月）

| 服務 | 規格 | 月費 |
|------|------|------|
| Cloud Run (pipeline) | 2vCPU/4GB, 每日 ~1hr 執行 | ~$5 |
| Cloud Run (dashboard) | 1vCPU/2GB, min=1 常駐 | ~$15 |
| Cloud SQL PostgreSQL | db-f1-micro | ~$10 |
| Memorystore Redis | 1GB Basic | ~$16 |
| Cloud Storage | PDF 存儲 | ~$1 |
| LLM APIs | 同上 | ~$10-18 |
| **合計** | | **~$57-65/月** |

> 相比純商業 API 方案（Nebula 環境）的 ~$80-150/月，節省約 **60-87%**。

---

## 技術選型說明

### 為何選 Prefect 而非 Airflow？

- Prefect 的 `@flow/@task` 裝飾器與 Pipeline Stage 概念天然對應
- 支援動態 subflow，三條 Pipeline 由主 Flow 統一調度
- 免費版 Prefect Cloud 足夠個人使用，亦可完全自架
- Airflow DAG 定義相對繁瑣，且 UI 較複雜

### 為何選 LangGraph 而非直接 Python？

- StateGraph 強制每個 Stage 的 I/O 型別安全（Pydantic）
- 內建 Redis checkpoint，支援跨 worker 狀態恢復
- `defer=True` 保證平行 Stage 完成後才進下一步
- 天然支援未來擴展為 multi-agent 協作

### 為何選 WeasyPrint 而非 ReportLab？

- HTML/CSS 模板比程式化繪圖直觀，設計師可直接修改
- Plotly 圖表以 base64 PNG 嵌入，版面完全可控
- 輸出品質更接近專業金融報告排版

### 為何 Stage 2 + 3 平行執行？

技術分析和基本面分析互不依賴，各需 60-120 秒。
平行執行可節省 35-40% 總執行時間（從 ~20 分鐘降至 ~13 分鐘）。

---

## 相關文件

- [完整架構設計文件](docs/architecture_design.md)
- [LLM 模型選型說明](docs/llm_model_selection.md)
- [GCP 部署手冊](docs/gcp_deployment_guide.md)
- [本地開發指南](docs/local_dev_guide.md)

---

## License

MIT License — 自由使用、修改、分發。

---

*README v2.0 | Last updated: 2026-03-02 | Author: Glennn*
