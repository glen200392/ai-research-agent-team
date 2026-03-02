# AI Investment Pipeline — Self-Hosted Architecture Design
# 自架版 AI 投資日報系統：完整架構設計文件

> **Version**: 2.0  
> **Date**: 2026-03-02  
> **Author**: Glennn  
> **Status**: Design Specification (Pre-Implementation)

---

## Table of Contents

1. [系統概述](#1-系統概述)
2. [與 Nebula 版本對比](#2-與-nebula-版本對比)
3. [三層系統架構](#3-三層系統架構)
4. [多模型多層次 LLM 策略](#4-多模型多層次-llm-策略)
5. [LangGraph StateGraph 設計](#5-langgraph-stategraph-設計)
6. [Prefect 排程與編排](#6-prefect-排程與編排)
7. [圖表視覺化設計](#7-圖表視覺化設計)
8. [Streamlit Dashboard 設計](#8-streamlit-dashboard-設計)
9. [GCP 雲端部署架構](#9-gcp-雲端部署架構)
10. [本地開發環境](#10-本地開發環境)
11. [Repo 結構設計](#11-repo-結構設計)
12. [Cost Estimation](#12-cost-estimation)

---

## 1. 系統概述

### 1.1 目標

建立一套完全脫離 Nebula 封閉環境、可自主部署的 AI 投資日報自動化系統，涵蓋：

- **台股 AI 投資 Pipeline**（每日 07:00 TST）
- **美股 AI 投資 Pipeline**（每日 22:00 TST）
- **日股 AI 投資 Pipeline**（每日 22:00 TST）

每條 Pipeline 執行 9 個分析 Stage，最終產出：
1. 結構化 JSON 分析資料
2. 專業排版 PDF 報告
3. Email 自動寄送
4. Streamlit 互動儀表板即時更新

### 1.2 核心設計原則

```
Modularity    → 每個 Stage 獨立可測試、可替換
Resilience    → 每個 Stage 支援 retry + fallback model
Observability → 全 Stage LLM trace、token 成本、延遲監控
Cost-Aware    → 開源模型為主、商業模型為輔，降低 90% API 成本
Portability   → Docker 化，本地/GCP 皆可部署
```

---

## 2. 與 Nebula 版本對比

| 面向 | Nebula 版本 | 自架版本 v2.0 | 改善幅度 |
|------|------------|--------------|---------|
| **LLM 成本** | 全商業 API（$80-150/月） | 開源主力 + 商業補充（$8-20/月） | ↓ 87% |
| **狀態管理** | JSON 檔案 pass-through（臨時） | PostgreSQL + Redis checkpoint | 永久可回溯 |
| **Stage 執行** | 完全依序（等待型） | Stage 2+3 真正非同步平行 | ↓ 35% 執行時間 |
| **PDF 品質** | Markdown → 基本 PDF | Jinja2 HTML + WeasyPrint（含圖表） | 專業排版品質 |
| **圖表數量** | 純文字表格 | 12+ 種互動圖表嵌入 PDF | 全新視覺化層 |
| **可觀測性** | 無 trace | Langfuse 全 Stage trace + 成本記錄 | 完整可觀測 |
| **錯誤恢復** | Pipeline 中斷即全失敗 | Prefect retry + partial state 恢復 | 高可用 |
| **模型彈性** | 固定 Nebula 內建 LLM | 任意切換 GPT/Claude/Qwen/DeepSeek | 完全控制 |
| **Dashboard** | 無 | Streamlit 互動儀表板（GCP Cloud Run） | 全新功能 |
| **部署環境** | Nebula 封閉 | Docker + 本地 / GCP Cloud Run | 完全可攜 |

---

## 3. 三層系統架構

```
╔══════════════════════════════════════════════════════════════════════╗
║  LAYER 1: ORCHESTRATION LAYER（排程與編排層）                         ║
║                                                                      ║
║  ┌─────────────────────────────────────────────────────────────┐     ║
║  │  Prefect Server / Prefect Cloud                             │     ║
║  │                                                             │     ║
║  │  @flow: master_daily_flow()                                 │     ║
║  │      ├── 07:00 TST → taiwan_pipeline_flow()                 │     ║
║  │      ├── 22:00 TST → us_pipeline_flow()      (parallel)     │     ║
║  │      └── 22:00 TST → japan_pipeline_flow()   (parallel)     │     ║
║  │                                                             │     ║
║  │  Features: retry, scheduling, deployment, monitoring        │     ║
║  └─────────────────────────────────────────────────────────────┘     ║
╠══════════════════════════════════════════════════════════════════════╣
║  LAYER 2: AGENT EXECUTION LAYER（Agent 執行層）                       ║
║                                                                      ║
║  ┌─────────────────────────────────────────────────────────────┐     ║
║  │  LangGraph StateGraph（每條 Pipeline 一個獨立 Graph）          │     ║
║  │                                                             │     ║
║  │  [Stage 0.5 Macro]──►[Stage 0.3 SupplyChain]               │     ║
║  │         │                      │                           │     ║
║  │         └──────────►[Stage 1 MarketResearch]               │     ║
║  │                              │                             │     ║
║  │                     [Stage 1.5 Sentiment]                  │     ║
║  │                              │                             │     ║
║  │              ┌───────────────┴──────────────┐              │     ║
║  │              ▼                              ▼              │     ║
║  │   [Stage 2 Technical]           [Stage 3 Fundamental]      │     ║
║  │   (async parallel)              (async parallel)           │     ║
║  │              └───────────────┬──────────────┘              │     ║
║  │                              ▼                             │     ║
║  │                  [Stage 4 Composite Score]                 │     ║
║  │                              │                             │     ║
║  │                    [Stage 5 CVaR + Risk]                   │     ║
║  │                              │                             │     ║
║  │              ┌───────────────┴──────────────┐              │     ║
║  │              ▼                              ▼              │     ║
║  │    [Stage 6a PDF Report]       [Stage 6b Dashboard Update] │     ║
║  │    (WeasyPrint + Charts)       (PostgreSQL write)          │     ║
║  │              │                                             │     ║
║  │    [Stage 7 Email Send]                                    │     ║
║  └─────────────────────────────────────────────────────────────┘     ║
╠══════════════════════════════════════════════════════════════════════╣
║  LAYER 3: INFRASTRUCTURE LAYER（基礎設施層）                          ║
║                                                                      ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐   ║
║  │PostgreSQL│  │  Redis   │  │ Langfuse │  │  Streamlit App    │   ║
║  │(state +  │  │(cache +  │  │(LLM trace│  │  (Dashboard +     │   ║
║  │ history) │  │ checkpoint│  │ + cost)  │  │   PDF viewer)     │   ║
║  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 4. 多模型多層次 LLM 策略

### 4.1 設計哲學：任務匹配模型，而非單一模型

不同 Stage 的任務性質截然不同，應使用最適合該任務的模型：

```
數值計算密集型  → 小模型即可，優先開源
長文理解分析型  → 需要大 context，考慮商業模型
多語言混合型    → Qwen3 多語言優勢
高頻調用型      → 開源/本地部署，零 API 成本
最終整合報告型  → 品質優先，使用最強模型
```

### 4.2 完整多模型路由表

| Stage | 任務類型 | 主力模型（開源） | 備援模型 1 | 備援模型 2（商業） | 部署方式 |
|-------|---------|----------------|-----------|-----------------|---------|
| **0.5 Macro Score** | 數值計算 + 指標正規化 | **DeepSeek-V3** (API) | Qwen3-8B (本地) | GPT-4o-mini | API |
| **0.3 Supply Chain** | 結構化資訊抽取 | **Qwen3-14B** (本地) | DeepSeek-V3 | GPT-4o-mini | Ollama local |
| **1 Market Research** | 長文閱讀 + 摘要 | **Qwen3-32B** (本地/API) | DeepSeek-V3 | Claude 3.5 Sonnet | Ollama / API |
| **1.5 Sentiment** | 情緒分類（高頻） | **FinGPT** (fine-tuned Llama3-8B) | Qwen3-8B | GPT-4o-mini | 本地 Ollama |
| **2 Technical** | 指標計算 + 信號判讀 | **DeepSeek-R1-Distill-8B** | Qwen3-14B | GPT-4o | 本地 / API |
| **3 Fundamental** | 財報分析 + DCF 建模 | **Qwen3-32B** | DeepSeek-V3 | Claude 3.5 Sonnet | API |
| **4 Composite Score** | 多維度加權整合 | **DeepSeek-V3** | Qwen3-32B | Claude 3.5 Sonnet | API |
| **5 CVaR + Risk** | 統計計算 + 情境分析 | **DeepSeek-R1** (推理強化) | Qwen3-32B | GPT-4o | API |
| **6 Report Gen** | 繁體中文長文寫作 | **Qwen3-32B** (中文最強) | DeepSeek-V3 | Claude 3.5 Sonnet | API |
| **7 Email** | 簡短摘要 | **Qwen3-8B** (本地) | — | — | 本地 Ollama |

### 4.3 三層 Fallback 機制

```python
# LLM Router with 3-tier fallback
class LLMRouter:
    """
    Tier 1: 本地 Ollama（零成本，較慢）
    Tier 2: 開源 API（DeepSeek / Qwen API，低成本）
    Tier 3: 商業 API（GPT / Claude，高品質保底）
    """

    async def invoke_with_fallback(
        self,
        stage: str,
        prompt: str,
        require_quality: QualityLevel = QualityLevel.STANDARD
    ) -> LLMResponse:

        tiers = self.get_tier_config(stage, require_quality)

        for tier_idx, model_config in enumerate(tiers):
            try:
                response = await self._invoke_model(model_config, prompt)
                if self._quality_check(response, stage):
                    return response
                # 品質不足 → 升級到下一層
                logger.warning(f"[{stage}] Tier {tier_idx} quality insufficient, escalating...")
            except (APIError, TimeoutError) as e:
                logger.error(f"[{stage}] Tier {tier_idx} failed: {e}, trying next tier")

        raise PipelineStageError(f"All tiers exhausted for {stage}")
```

### 4.4 開源模型本地部署（Ollama）

```yaml
# docker-compose.yml 中的 Ollama 服務
ollama:
  image: ollama/ollama:latest
  volumes:
    - ollama_data:/root/.ollama
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
  ports:
    - "11434:11434"
```

預拉取的模型清單：
```bash
# Stage 0.3, 1.5, 7 使用（輕量高頻）
ollama pull qwen3:8b

# Stage 0.3, 2 使用（推理強化）
ollama pull deepseek-r1:8b

# Stage 1, 3, 6 使用（長文品質）
ollama pull qwen3:32b  # 需要 20GB+ VRAM 或 CPU 推理

# Stage 1.5 專用（金融情緒微調）
# FinGPT fine-tuned model → 自訂 Modelfile 載入
```

### 4.5 FinGPT 情緒分析專用模型

```python
# Stage 1.5: 使用 FinGPT fine-tuned 模型
# 基於 Llama-3.1-8B 在金融情緒資料集上微調
# 訓練成本 < $300，準確率接近 GPT-4o

from transformers import AutoTokenizer, AutoModelForCausalLM

class FinGPTSentimentAnalyzer:
    MODEL_ID = "FinGPT/fingpt-sentiment_llama3.1-8b_lora"

    def analyze_sentiment(self, text: str) -> SentimentResult:
        """
        輸入：新聞標題或財報段落
        輸出：{sentiment: "positive/negative/neutral", score: 0.0-1.0, confidence: float}
        """
        prompt = f"""Analyze the sentiment of the following financial text.
Output ONLY: {{"sentiment": "positive|negative|neutral", "score": 0.0-1.0}}

Text: {text}"""
        # ... inference logic
```

### 4.6 月度成本估算（三條 Pipeline）

| 模型層 | 用途 | 預估月費 |
|--------|------|---------|
| Ollama 本地（Qwen3-8B, DeepSeek-R1-8B） | Stage 0.3, 1.5, 7 | $0（電費忽略） |
| DeepSeek API（V3, R1） | Stage 0.5, 2, 4, 5 | ~$3-5 |
| Qwen API（32B） | Stage 1, 3, 6 | ~$5-8 |
| Claude/GPT（fallback only） | 品質保底，約 10% 調用 | ~$2-5 |
| **總計** | | **~$10-18/月** |

---

## 5. LangGraph StateGraph 設計

### 5.1 統一 PipelineState Schema

```python
from typing import TypedDict, Annotated
from pydantic import BaseModel
import operator

# ── Sub-state models ──────────────────────────────────────────────────

class MacroState(BaseModel):
    score: float              # 0-10
    regime: str               # "expansion|contraction|stagflation|recession"
    yield_spread: float       # 10Y-2Y
    fed_rate_direction: str   # "hiking|cutting|neutral"
    usd_index: float
    tw_pmi: float
    computed_at: str

class SupplyChainState(BaseModel):
    temperature: float        # 0-10, 供應鏈熱度
    bottleneck_nodes: list[str]
    opportunity_nodes: list[str]
    raw_data: dict

class SentimentState(BaseModel):
    market_sentiment: float   # 0-10
    per_stock_scores: dict[str, float]
    fear_greed_index: float
    news_volume_signal: str

class TechnicalState(BaseModel):
    signals: dict[str, StockTechnicalSignal]
    market_breadth: float
    sector_rotation: dict[str, str]

class FundamentalState(BaseModel):
    valuations: dict[str, FundamentalMetrics]
    dcf_targets: dict[str, float]
    quality_scores: dict[str, float]

class CompositeState(BaseModel):
    scores: dict[str, float]           # 最終 0-100 分
    buy_list: list[str]                # Top 5 買入
    watch_list: list[str]              # 觀察名單
    sell_list: list[str]               # 賣出信號

class RiskState(BaseModel):
    portfolio_var: float
    portfolio_cvar: float
    kelly_positions: dict[str, float]  # Kelly 建議倉位
    stress_test_results: dict[str, float]
    max_drawdown_estimate: float

# ── Master PipelineState ──────────────────────────────────────────────

class PipelineState(TypedDict):
    # Pipeline metadata
    market: str                              # "TW" | "US" | "JP"
    execution_date: str
    pipeline_version: str

    # Stage outputs (immutable once written)
    macro: MacroState | None
    supply_chain: SupplyChainState | None    # TW only
    market_research: dict | None
    sentiment: SentimentState | None
    technical: TechnicalState | None
    fundamental: FundamentalState | None
    composite: CompositeState | None
    risk: RiskState | None

    # Parallel stage aggregation (using reducer)
    parallel_results: Annotated[list, operator.add]

    # Artifacts
    charts_paths: Annotated[list[str], operator.add]
    pdf_path: str | None
    email_sent: bool

    # Observability
    stage_timings: Annotated[dict, lambda a, b: {**a, **b}]
    total_tokens: Annotated[int, operator.add]
    errors: Annotated[list[str], operator.add]
```

### 5.2 Graph 建構（以台股為例）

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.redis import AsyncRedisSaver

def build_taiwan_pipeline() -> CompiledGraph:
    graph = StateGraph(PipelineState)

    # ── 節點註冊 ──────────────────────────────────────────────────────
    graph.add_node("macro",         MacroScoringAgent().run)
    graph.add_node("supply_chain",  SupplyChainAgent().run)
    graph.add_node("market_research", MarketResearchAgent().run)
    graph.add_node("sentiment",     SentimentAgent().run)
    graph.add_node("technical",     TechnicalAnalysisAgent().run)    # async
    graph.add_node("fundamental",   FundamentalAnalysisAgent().run)  # async
    graph.add_node("composite",     CompositeScoreAgent().run,  defer=True)  # 等待平行完成
    graph.add_node("risk",          RiskManagementAgent().run)
    graph.add_node("report",        ReportGeneratorAgent().run)
    graph.add_node("email",         EmailSenderAgent().run)

    # ── 邊連接 ────────────────────────────────────────────────────────
    graph.set_entry_point("macro")
    graph.add_edge("macro",          "supply_chain")
    graph.add_edge("supply_chain",   "market_research")
    graph.add_edge("market_research","sentiment")

    # 平行分叉：Stage 2 + 3 同時執行
    graph.add_edge("sentiment",      "technical")
    graph.add_edge("sentiment",      "fundamental")

    # 平行收束：兩者完成後才進 composite（defer=True 保證等待）
    graph.add_edge("technical",      "composite")
    graph.add_edge("fundamental",    "composite")

    graph.add_edge("composite",      "risk")
    graph.add_edge("risk",           "report")
    graph.add_edge("report",         "email")
    graph.add_edge("email",          END)

    # ── Redis Checkpoint（支援跨 worker 狀態恢復）─────────────────────
    checkpointer = AsyncRedisSaver.from_conn_string(
        os.environ["REDIS_URL"],
        ttl={"default_ttl": 86400}  # 24hr TTL
    )

    return graph.compile(checkpointer=checkpointer)
```

---

## 6. Prefect 排程與編排

### 6.1 三條 Pipeline 的 Prefect Flow 設計

```python
import asyncio
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta

# ── 單一市場 Task（可 retry）────────────────────────────────────────

@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=6),
    timeout_seconds=3600
)
async def run_market_pipeline(market: str, execution_date: str) -> dict:
    logger = get_run_logger()
    logger.info(f"Starting {market} pipeline for {execution_date}")

    graph = get_pipeline_graph(market)  # TW / US / JP

    initial_state = PipelineState(
        market=market,
        execution_date=execution_date,
        pipeline_version="2.0"
    )

    config = {"configurable": {"thread_id": f"{market}-{execution_date}"}}
    final_state = await graph.ainvoke(initial_state, config=config)

    logger.info(f"{market} pipeline completed. PDF: {final_state['pdf_path']}")
    return {"market": market, "status": "success", "pdf_path": final_state["pdf_path"]}

# ── 主排程 Flow ─────────────────────────────────────────────────────

@flow(name="daily-investment-report", log_prints=True)
async def master_daily_flow(execution_date: str | None = None):
    """每日執行兩個時間點：07:00 台股、22:00 美股+日股（Asia/Taipei）"""
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone("Asia/Taipei")
    now = datetime.now(tz)
    exec_date = execution_date or now.strftime("%Y-%m-%d")
    current_hour = now.hour

    if 6 <= current_hour < 8:
        # 07:00 → 執行台股
        await run_market_pipeline("TW", exec_date)

    elif 21 <= current_hour < 23:
        # 22:00 → 美股 + 日股平行執行
        us_task = run_market_pipeline.submit("US", exec_date)
        jp_task = run_market_pipeline.submit("JP", exec_date)
        await asyncio.gather(us_task, jp_task)

# ── Prefect Deployment 設定 ─────────────────────────────────────────

# prefect.yaml (部署設定)
# deployments:
#   - name: taiwan-07h
#     flow: master_daily_flow
#     schedule:
#       cron: "0 7 * * *"
#       timezone: "Asia/Taipei"
#     parameters:
#       execution_date: null
#
#   - name: us-japan-22h
#     flow: master_daily_flow
#     schedule:
#       cron: "0 22 * * *"
#       timezone: "Asia/Taipei"
```

---

## 7. 圖表視覺化設計

### 7.1 完整圖表清單（12 種，分市場）

#### 所有市場共用圖表

| # | 圖表名稱 | 類型 | 技術庫 | 說明 |
|---|---------|------|--------|------|
| 1 | **K 線圖 + 均線 + 成交量** | OHLCV Candlestick | mplfinance | 每支標的過去 60 日 K 線 + MA5/20/60 + 布林帶 + 成交量柱 |
| 2 | **RSI + MACD 雙指標** | Subplot indicator | mplfinance | RSI(14) 超買超賣線 + MACD/Signal/Histogram |
| 3 | **五維度雷達圖** | Radar / Spider | Plotly Scatterpolar | 總體/情緒/技術/基本面/風險 五軸評分，每支股票一張 |
| 4 | **Composite Score 排行橫條圖** | Horizontal Bar | Plotly | 所有候選股由高到低排行，含 Buy/Watch/Sell 色彩分層 |
| 5 | **相關性熱圖** | Heatmap | Plotly / Seaborn | 標的間 60 日報酬相關係數矩陣 |
| 6 | **CVaR / VaR 長條圖** | Bar + Line | Plotly | 各標的 95%/99% VaR 與 CVaR 視覺化 |
| 7 | **Kelly 倉位建議圓餅圖** | Pie / Donut | Plotly | 建議投資組合倉位分配 |
| 8 | **情緒時序趨勢線** | Time Series Line | Plotly | 過去 30 日 Sentiment Score 走勢，標記重要事件 |

#### 台股專用

| # | 圖表名稱 | 類型 | 技術庫 | 說明 |
|---|---------|------|--------|------|
| 9 | **AI 供應鏈溫度熱圖** | Heatmap（矩陣） | Plotly | 上游/中游/下游 × 各廠商的溫度（0-10），標記瓶頸節點 |
| 10 | **產業鏈資金流向 Sankey 圖** | Sankey | Plotly | 從 AI 伺服器需求 → 晶片 → 封裝 → PCB → 系統整合的資金流 |

#### 美股專用

| # | 圖表名稱 | 類型 | 技術庫 | 說明 |
|---|---------|------|--------|------|
| 11 | **AI CapEx 曝險泡泡圖** | Bubble Scatter | Plotly | X=EV/EBITDA, Y=營收成長率, Size=AI CapEx 比例 |

#### 日股專用

| # | 圖表名稱 | 類型 | 技術庫 | 說明 |
|---|---------|------|--------|------|
| 12 | **日圓敏感度矩陣** | Annotated Heatmap | Plotly | 各標的在不同日圓匯率情境下的預估盈餘變動 |

### 7.2 圖表技術實作模式

```python
import plotly.graph_objects as go
import plotly.io as pio
import mplfinance as mpf
import base64
from pathlib import Path

class ChartFactory:
    """統一圖表生成工廠，輸出 base64 PNG 供 HTML 模板嵌入"""

    def candlestick_with_indicators(
        self,
        df: pd.DataFrame,      # OHLCV DataFrame，index 為日期
        ticker: str,
        output_path: Path
    ) -> str:
        """生成 K 線圖（mplfinance）→ 儲存 PNG → 回傳 base64"""
        fig, axes = mpf.plot(
            df, type='candle',
            style='charles',
            title=f'{ticker} — 60日 K 線圖',
            volume=True,
            mav=(5, 20, 60),
            bollinger_bands=True,
            returnfig=True,
            figsize=(14, 8)
        )
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        return self._to_base64(output_path)

    def radar_chart(
        self,
        scores: dict[str, float],  # {"macro": 7.2, "sentiment": 6.8, ...}
        ticker: str
    ) -> str:
        """生成五維度雷達圖（Plotly）→ Kaleido 轉 PNG → base64"""
        categories = list(scores.keys())
        values = list(scores.values()) + [list(scores.values())[0]]  # 閉合多邊形

        fig = go.Figure(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(99, 110, 250, 0.2)',
            line=dict(color='rgb(99, 110, 250)', width=2),
            name=ticker
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            title=f'{ticker} 五維度評分雷達圖',
            showlegend=False,
            width=600, height=500
        )
        return self._plotly_to_base64(fig)

    def supply_chain_heatmap(self, sc_data: dict) -> str:
        """台股 AI 供應鏈溫度熱圖"""
        # 建構矩陣：rows=層級（上/中/下游）, cols=廠商
        fig = go.Figure(go.Heatmap(
            z=sc_data["temperature_matrix"],
            x=sc_data["companies"],
            y=["上游", "中游", "下游"],
            colorscale='RdYlGn',
            zmin=0, zmax=10,
            text=sc_data["temperature_matrix"],
            texttemplate="%{text:.1f}",
            hoverongaps=False
        ))
        fig.update_layout(
            title='AI 供應鏈溫度熱圖',
            width=900, height=400
        )
        return self._plotly_to_base64(fig)

    def correlation_heatmap(self, returns_df: pd.DataFrame) -> str:
        """標的相關係數矩陣熱圖"""
        corr = returns_df.corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale='RdBu_r',
            zmid=0,
            text=corr.round(2).values,
            texttemplate="%{text}",
        ))
        return self._plotly_to_base64(fig)

    def cvar_bar_chart(self, risk_data: dict) -> str:
        """VaR / CVaR 長條比較圖"""
        tickers = list(risk_data.keys())
        var_95 = [risk_data[t]["var_95"] for t in tickers]
        cvar_95 = [risk_data[t]["cvar_95"] for t in tickers]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='VaR 95%', x=tickers, y=var_95,
                             marker_color='orange'))
        fig.add_trace(go.Bar(name='CVaR 95%', x=tickers, y=cvar_95,
                             marker_color='red'))
        fig.update_layout(
            barmode='group',
            title='各標的 VaR / CVaR 風險比較',
            yaxis_title='損失比例 (%)'
        )
        return self._plotly_to_base64(fig)

    def sankey_supply_chain(self, flow_data: dict) -> str:
        """產業鏈資金流向 Sankey 圖（台股專用）"""
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15, thickness=20,
                label=flow_data["nodes"],
                color=flow_data["node_colors"]
            ),
            link=dict(
                source=flow_data["sources"],
                target=flow_data["targets"],
                value=flow_data["values"],
                color=flow_data["link_colors"]
            )
        ))
        fig.update_layout(title='AI 產業鏈資金流向', width=1000, height=500)
        return self._plotly_to_base64(fig)

    def _plotly_to_base64(self, fig: go.Figure) -> str:
        img_bytes = pio.to_image(fig, format="png", engine="kaleido")
        return base64.b64encode(img_bytes).decode("utf-8")

    def _to_base64(self, path: Path) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
```

### 7.3 PDF HTML 模板結構（WeasyPrint）

```html
<!-- templates/tw_report_body.html.j2 -->
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <style>
    /* 專業金融報告版面 */
    body { font-family: 'Noto Sans TC', sans-serif; }
    .cover { page-break-after: always; text-align: center; }
    .section { page-break-inside: avoid; margin: 20px 0; }
    .chart-container { text-align: center; margin: 15px 0; }
    .score-card { 
      display: grid; grid-template-columns: repeat(5, 1fr);
      gap: 10px; background: #f5f5f5; padding: 15px; border-radius: 8px;
    }
    .buy-signal { color: #00aa00; font-weight: bold; }
    .sell-signal { color: #cc0000; font-weight: bold; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #1a237e; color: white; padding: 8px; }
    td { padding: 6px; border-bottom: 1px solid #ddd; }
    @page { margin: 2cm; size: A4; }
  </style>
</head>
<body>
  <!-- 封面 -->
  <div class="cover">
    <h1>台股 AI 投資日報</h1>
    <h2>{{ execution_date }}</h2>
    <p>Macro 評分: {{ macro.score }}/10 | 市場態勢: {{ macro.regime }}</p>
  </div>

  <!-- 總體環境 -->
  <div class="section">
    <h2>1. 總體環境評估</h2>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.macro_gauge }}" width="600"/>
    </div>
    <!-- ... 宏觀指標表格 ... -->
  </div>

  <!-- 供應鏈溫度 -->
  <div class="section">
    <h2>2. AI 供應鏈溫度圖</h2>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.supply_chain_heatmap }}" width="900"/>
    </div>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.sankey }}" width="900"/>
    </div>
  </div>

  <!-- 個股技術分析（迴圈每支股票）-->
  {% for ticker, data in technical.signals.items() %}
  <div class="section">
    <h3>{{ ticker }} — 技術分析</h3>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.candlestick[ticker] }}" width="900"/>
    </div>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.radar[ticker] }}" width="600"/>
    </div>
  </div>
  {% endfor %}

  <!-- 風險矩陣 -->
  <div class="section">
    <h2>6. 風險評估</h2>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.cvar_bar }}" width="800"/>
    </div>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.correlation_heatmap }}" width="700"/>
    </div>
    <div class="chart-container">
      <img src="data:image/png;base64,{{ charts.kelly_pie }}" width="600"/>
    </div>
  </div>

</body>
</html>
```

---

## 8. Streamlit Dashboard 設計

### 8.1 頁面結構

```
Dashboard
├── 📊 總覽（Overview）
│   ├── 三市場 Macro Score 卡片（即時）
│   ├── 當日 Top Buy 清單
│   └── 全球市場情緒儀表板
│
├── 🇹🇼 台股 AI Pipeline
│   ├── Composite Score 排行榜
│   ├── 供應鏈溫度熱圖（互動）
│   ├── Sankey 資金流向圖（互動）
│   ├── 個股雷達圖（下拉選擇）
│   ├── K 線圖（互動，含技術指標）
│   └── PDF 報告下載按鈕
│
├── 🇺🇸 美股 AI Pipeline
│   ├── Composite Score 排行榜
│   ├── AI CapEx 泡泡圖（互動）
│   ├── 動能篩選表
│   └── PDF 報告下載
│
├── 🇯🇵 日股 AI Pipeline
│   ├── Composite Score 排行榜
│   ├── 日圓敏感度矩陣（互動）
│   └── PDF 報告下載
│
└── 📈 歷史趨勢
    ├── 三市場 Composite Score 30 日走勢
    ├── Macro Score 時序圖
    └── 月績效回顧表
```

### 8.2 Streamlit App 核心程式碼結構

```python
# dashboard/app.py
import streamlit as st
import plotly.graph_objects as go
from db import get_latest_pipeline_results, get_historical_scores

st.set_page_config(
    page_title="AI Investment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 側邊欄導航 ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("AI Investment Pipeline")
    page = st.radio("選擇市場", ["總覽", "台股", "美股", "日股", "歷史趨勢"])
    exec_date = st.date_input("查詢日期", value=datetime.today())

# ── 總覽頁 ──────────────────────────────────────────────────────────
if page == "總覽":
    st.title("📊 三市場即時總覽")

    col1, col2, col3 = st.columns(3)
    for col, market in zip([col1, col2, col3], ["TW", "US", "JP"]):
        data = get_latest_pipeline_results(market, exec_date)
        with col:
            st.metric(
                label=f"{'台股' if market=='TW' else '美股' if market=='US' else '日股'} Macro Score",
                value=f"{data['macro_score']:.1f} / 10",
                delta=f"{data['macro_score_delta']:+.1f} vs 昨日"
            )
            st.caption(f"市場態勢：{data['regime']}")

    # Top Buy 清單
    st.subheader("🔥 當日 Top 5 Buy 訊號")
    st.dataframe(get_top_buys(exec_date), use_container_width=True)

# ── 台股頁 ──────────────────────────────────────────────────────────
elif page == "台股":
    data = get_latest_pipeline_results("TW", exec_date)

    st.title(f"🇹🇼 台股 AI Pipeline — {exec_date}")

    # Composite Score 排行
    st.subheader("Composite Score 排行")
    fig = create_composite_bar_chart(data["composite"])
    st.plotly_chart(fig, use_container_width=True)

    # 供應鏈溫度熱圖（互動版）
    st.subheader("AI 供應鏈溫度熱圖")
    fig = create_supply_chain_heatmap(data["supply_chain"])
    st.plotly_chart(fig, use_container_width=True)

    # 個股深度分析（下拉選擇）
    st.subheader("個股深度分析")
    selected = st.selectbox("選擇標的", options=data["tickers"])
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = create_candlestick(data["technical"][selected])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = create_radar_chart(data["scores"][selected])
        st.plotly_chart(fig, use_container_width=True)

    # PDF 下載
    if data.get("pdf_path"):
        with open(data["pdf_path"], "rb") as f:
            st.download_button(
                "📥 下載 PDF 報告",
                data=f.read(),
                file_name=f"tw_report_{exec_date}.pdf",
                mime="application/pdf"
            )
```

---

## 9. GCP 雲端部署架構

### 9.1 GCP 服務配置

```
GCP Project: ai-investment-pipeline
Region: asia-east1 (台灣最近)

┌──────────────────────────────────────────────────────────────┐
│  Cloud Scheduler                                              │
│  ├── job: taiwan-07h  → Pub/Sub → Cloud Run (Prefect worker) │
│  └── job: us-jp-22h   → Pub/Sub → Cloud Run (Prefect worker) │
├──────────────────────────────────────────────────────────────┤
│  Cloud Run Services                                           │
│  ├── prefect-worker  (Pipeline 執行，min=0, max=3)            │
│  └── streamlit-app   (Dashboard，min=1, max=5)                │
├──────────────────────────────────────────────────────────────┤
│  Cloud SQL (PostgreSQL 15)                                    │
│  ├── db: pipeline_state  (Stage 狀態持久化)                   │
│  └── db: dashboard_data  (Dashboard 查詢用)                   │
├──────────────────────────────────────────────────────────────┤
│  Memorystore (Redis 7.2)                                      │
│  └── LangGraph checkpoint + Stage cache                       │
├──────────────────────────────────────────────────────────────┤
│  Artifact Registry                                            │
│  ├── pipeline-worker:latest                                   │
│  └── streamlit-app:latest                                     │
├──────────────────────────────────────────────────────────────┤
│  Secret Manager                                               │
│  ├── OPENAI_API_KEY, ANTHROPIC_API_KEY                        │
│  ├── DEEPSEEK_API_KEY, QWEN_API_KEY                           │
│  ├── FRED_API_KEY, LANGFUSE_SECRET_KEY                        │
│  └── DATABASE_URL, REDIS_URL, SMTP_PASSWORD                   │
├──────────────────────────────────────────────────────────────┤
│  Cloud Storage                                                │
│  └── bucket: ai-investment-reports (PDF 永久存儲)             │
└──────────────────────────────────────────────────────────────┘
```

### 9.2 月費估算（GCP）

| 服務 | 規格 | 月費估算 |
|------|------|---------|
| Cloud Run (pipeline worker) | 2 vCPU, 4GB, 每日 2 次各 ~30min | ~$5 |
| Cloud Run (Streamlit) | 1 vCPU, 2GB, min=1 | ~$15 |
| Cloud SQL (PostgreSQL) | db-f1-micro | ~$10 |
| Memorystore (Redis) | 1GB Basic | ~$16 |
| Cloud Storage | PDF 存儲 ~1GB/月 | ~$0.02 |
| Secret Manager | < 10 secrets | ~$0.06 |
| **GCP 總計** | | **~$46/月** |

---

## 10. 本地開發環境

### 10.1 docker-compose.yml

```yaml
version: "3.9"

services:
  # ── 資料庫 ──────────────────────────────────────────────────────
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ai_pipeline
      POSTGRES_USER: pipeline_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infra/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7.2-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  # ── LLM 本地推理 ────────────────────────────────────────────────
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    # GPU 支援（需安裝 nvidia-container-toolkit）
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  # ── Prefect 編排 ────────────────────────────────────────────────
  prefect-server:
    image: prefecthq/prefect:3-latest
    command: prefect server start
    environment:
      PREFECT_SERVER_API_HOST: 0.0.0.0
      PREFECT_API_DATABASE_CONNECTION_URL: postgresql+asyncpg://pipeline_user:${POSTGRES_PASSWORD}@postgres:5432/ai_pipeline
    ports:
      - "4200:4200"
    depends_on:
      - postgres

  prefect-worker:
    build:
      context: .
      dockerfile: Dockerfile.pipeline
    command: prefect worker start --pool default-agent-pool
    environment:
      PREFECT_API_URL: http://prefect-server:4200/api
      REDIS_URL: redis://redis:6379
      DATABASE_URL: postgresql://pipeline_user:${POSTGRES_PASSWORD}@postgres:5432/ai_pipeline
    env_file: .env
    depends_on:
      - prefect-server
      - redis
      - ollama
    volumes:
      - ./reports:/app/reports  # PDF 輸出目錄

  # ── Observability ────────────────────────────────────────────────
  langfuse:
    image: langfuse/langfuse:latest
    environment:
      DATABASE_URL: postgresql://pipeline_user:${POSTGRES_PASSWORD}@postgres:5432/ai_pipeline
      NEXTAUTH_SECRET: ${LANGFUSE_SECRET}
      NEXTAUTH_URL: http://localhost:3000
    ports:
      - "3000:3000"
    depends_on:
      - postgres

  # ── Streamlit Dashboard ─────────────────────────────────────────
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.dashboard
    ports:
      - "8501:8501"
    environment:
      DATABASE_URL: postgresql://pipeline_user:${POSTGRES_PASSWORD}@postgres:5432/ai_pipeline
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

---

## 11. Repo 結構設計

```
ai-research-agent-team/
│
├── pipelines/                          # Prefect Flow 定義
│   ├── __init__.py
│   ├── master_flow.py                  # 主排程 Flow
│   ├── taiwan_pipeline.py
│   ├── us_pipeline.py
│   └── japan_pipeline.py
│
├── agents/                             # LangGraph Agent 節點
│   ├── __init__.py
│   ├── base_agent.py                   # 抽象基類 + LLM router
│   ├── macro_scoring.py                # Stage 0.5
│   ├── supply_chain.py                 # Stage 0.3 (TW only)
│   ├── market_research.py              # Stage 1
│   ├── sentiment.py                    # Stage 1.5 (FinGPT)
│   ├── technical_analysis.py           # Stage 2
│   ├── fundamental_analysis.py         # Stage 3
│   ├── composite_scoring.py            # Stage 4
│   ├── risk_management.py              # Stage 5
│   ├── report_generator.py             # Stage 6
│   └── email_sender.py                 # Stage 7
│
├── llm/                                # 多模型 LLM 路由層
│   ├── __init__.py
│   ├── router.py                       # 三層 Fallback Router
│   ├── models.py                       # 模型配置清單
│   ├── quality_checker.py              # 輸出品質檢核
│   └── cost_tracker.py                 # Token 費用追蹤
│
├── state/                              # Pydantic State Schemas
│   ├── __init__.py
│   ├── pipeline_state.py               # PipelineState TypedDict
│   └── sub_states.py                   # MacroState, RiskState, etc.
│
├── charts/                             # 圖表生成工廠
│   ├── __init__.py
│   ├── factory.py                      # ChartFactory 主類
│   ├── candlestick.py                  # K 線圖
│   ├── radar.py                        # 五維度雷達圖
│   ├── heatmaps.py                     # 熱圖系列
│   ├── risk_charts.py                  # VaR/CVaR/Kelly
│   └── sankey.py                       # 供應鏈 Sankey（TW only）
│
├── templates/                          # Jinja2 HTML 報告模板
│   ├── base_report.html.j2
│   ├── tw_report_body.html.j2
│   ├── us_report_body.html.j2
│   ├── jp_report_body.html.j2
│   └── email_summary.html.j2
│
├── dashboard/                          # Streamlit Dashboard
│   ├── app.py                          # 主入口
│   ├── pages/
│   │   ├── overview.py
│   │   ├── taiwan.py
│   │   ├── us.py
│   │   ├── japan.py
│   │   └── history.py
│   ├── components/                     # 可複用 UI 元件
│   │   ├── score_cards.py
│   │   ├── chart_widgets.py
│   │   └── pdf_viewer.py
│   └── db.py                           # Dashboard DB 查詢層
│
├── infra/                              # 基礎設施設定
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml         # GCP 生產設定覆蓋
│   ├── Dockerfile.pipeline
│   ├── Dockerfile.dashboard
│   ├── init.sql                        # PostgreSQL 初始化 Schema
│   └── prefect.yaml                    # Prefect 部署設定
│
├── deploy/                             # GCP 部署腳本
│   ├── gcp_setup.sh                    # 一鍵建立 GCP 資源
│   ├── deploy_pipeline.sh
│   └── deploy_dashboard.sh
│
├── tests/                              # 測試套件
│   ├── unit/
│   │   ├── test_macro_agent.py
│   │   ├── test_llm_router.py
│   │   └── test_chart_factory.py
│   └── integration/
│       └── test_tw_pipeline_e2e.py
│
├── docs/
│   ├── architecture_design.md          # 本文件
│   ├── llm_model_selection.md          # 模型選型詳細說明
│   ├── gcp_deployment_guide.md         # GCP 部署手冊
│   └── local_dev_guide.md              # 本地開發指南
│
├── .env.example                        # 環境變數範本（不含真實 key）
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md                           # 完整系統說明
```

---

## 12. Cost Estimation

### 完整月費總覽

| 類別 | 項目 | 月費 |
|------|------|------|
| **LLM API** | DeepSeek V3/R1 | $3-5 |
| **LLM API** | Qwen API | $5-8 |
| **LLM API** | GPT/Claude fallback | $2-5 |
| **GCP** | Cloud Run (2 services) | $20 |
| **GCP** | Cloud SQL PostgreSQL | $10 |
| **GCP** | Memorystore Redis | $16 |
| **GCP** | 其他（Storage, Scheduler） | $1 |
| **總計** | | **~$57-65/月** |

### 本地部署月費（僅電費）

| 項目 | 說明 | 月費 |
|------|------|------|
| 本機電費 | GPU 推理 + 每日 2 次執行 | ~$2-5 |
| LLM API | DeepSeek + Qwen（開源優先） | $8-15 |
| **總計** | | **~$10-20/月** |

---

*文件版本：2.0 | 最後更新：2026-03-02*
