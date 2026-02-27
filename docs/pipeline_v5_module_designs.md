# Pipeline v5 — 三大新模組設計規格

> 設計日期:2026-02-26 | 基於 v4 架構升級

---

## MODULE A:Stage 0.3 — 台廠月營收供應鏈追蹤

### 定位
- **插入位置**:Stage 0.5(Macro Score)之後、Stage 1(市場研究)之前
- **核心邏輯**:台廠月營收是比 PMI 領先 2-3 週的即時信號,每月 10 日前強制公告
- **數據來源**:完全免費(公開資訊觀測站 MOPS)

### 監控標的矩陣(三層供應鏈)

#### 上游層(原材料/設備)— 信號領先 2-4 個月
| 公司 | 代號 | 追蹤意義 | 參考閾值 |
|------|------|----------|----------|
| 環球晶 | 6488 | 矽晶圓需求先行指標 | YoY > +10% = 強 |
| 嘉晶 | 3016 | 化合物半導體材料 | YoY > +15% = 強 |
| 家登 | 3680 | 光罩基板/光罩盒 | QoQ > +5% = 擴張 |
| 帆宣 | 6196 | 半導體廠務工程 | YoY > +20% = 擴張 |
| 漢唐 | 2404 | 無塵室工程(建廠指標) | 新接單金額 |

#### 中游層(晶圓代工/封裝)— 信號領先 1-2 個月
| 公司 | 代號 | 追蹤意義 | 參考閾值 |
|------|------|----------|----------|
| 聯電 | 2303 | 成熟製程景氣溫度計 | YoY > +5% = 回溫 |
| 日月光 | 3711 | 封裝測試需求現況 | YoY > +10% = 強 |
| 京元電 | 2449 | HBM/先進封裝測試 | QoQ > +8% = 爆發 |
| 欣銓 | 3264 | 記憶體測試景氣 | YoY > +15% = 強 |
| 南茂 | 8150 | IC 封裝需求 | QoQ > +5% = 正常 |

#### 下游層(AI 伺服器/系統整合)— 即時需求溫度計
| 公司 | 代號 | 追蹤意義 | 參考閾值 |
|------|------|----------|----------|
| 緯穎 | 6669 | AI 伺服器 ODM 龍頭 | YoY > +50% = 超強 |
| 英業達 | 2356 | AI 伺服器 + 傳統伺服器 | YoY > +30% = 強 |
| 廣達 | 2382 | 雲端伺服器/AI 系統 | YoY > +20% = 強 |
| 緯創 | 3231 | 伺服器 + NB 雙線 | YoY > +15% = 正常 |
| 川湖 | 2059 | 機架/滑軌(資料中心指標) | YoY > +20% = 強 |

### 計算邏輯:Supply Chain Temperature Score

```python
def calculate_supply_chain_temp(monthly_revenues):
    # 分層加權
    upstream_score   = weighted_avg(upstream_companies,   weight=0.25)
    midstream_score  = weighted_avg(midstream_companies,  weight=0.40)
    downstream_score = weighted_avg(downstream_companies, weight=0.35)
    
    # 趨勢加成:連續 2 個月改善 +0.5,連續 3 個月改善 +1.0
    trend_bonus = calculate_trend_bonus(3_month_history)
    
    base_score = upstream_score + midstream_score + downstream_score
    final_score = min(10, base_score + trend_bonus)
    
    if final_score >= 7.5:
        regime = "SUPPLY_EXPANSION"
    elif final_score >= 5.5:
        regime = "SUPPLY_STABLE"
    elif final_score >= 3.5:
        regime = "SUPPLY_CAUTIOUS"
    else:
        regime = "SUPPLY_CONTRACTION"
    
    return {"sc_temp_score": final_score, "sc_regime": regime, ...}
```

### 數據抓取方式(免費,無需 API Key)

```python
# 方法 1:MOPS 公開資訊觀測站(每月 10 日前強制公告)
url = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}_0.html"

# 方法 2:HiStock 財經網(月營收彙整頁面)
url = "https://histock.tw/stock/financial.aspx?no={ticker}&data=4"
```

### 對下游 Stage 的影響

| SC Regime | Stage 1 指示 | Stage 4 權重調整 |
|-----------|-------------|------------------|
| SUPPLY_EXPANSION | 積極篩選 AI 伺服器/CoWoS 標的 | SC Score 權重 +5% |
| SUPPLY_STABLE | 正常篩選流程 | 標準權重 |
| SUPPLY_CAUTIOUS | 提高基本面門檻,降低技術面權重 | SC Score 權重 -5% |
| SUPPLY_CONTRACTION | 縮短標的清單,加強風控 | Stage 5 CVaR 門檻收緊 |

---

## MODULE B:法說逐字稿 NLP 信號萃取(加入 Stage 1)

### NLP 信號字典

```python
BULLISH_SIGNALS = {
    "strong demand": +2, "robust demand": +2, "customer pull-in": +2,
    "CoWoS capacity expansion": +2, "advanced packaging ramp": +2,
    "capacity utilization above": +1.5, "price increase": +1,
}
BEARISH_SIGNALS = {
    "demand softness": -2, "inventory digestion": -2,
    "customer push-out": -2, "oversupply": -1.5,
    "pricing pressure": -1, "export restriction": -2,
}
```

### 處理流程

```
Step 1: web_scrape(TSMC IR / Seeking Alpha) → 法說逐字稿全文
Step 2: 按段落分割 → 管理層陳述 / Q&A(Q&A 權重 x1.3)
Step 3: 關鍵詞掃描 → 計算原始信號分數
Step 4: 正規化 → NLP Transcript Score (0-10),5.0 = 中性
Step 5: 萃取前 5 個最重要信號(含原文引述)
```

---

## MODULE C:供應鏈上下游評分框架(Supply Chain Score)

### 五維度評分矩陣(v5 vs v4)

| 維度 | v4 權重 | v5 權重 | 變化 |
|------|---------|---------|------|
| Macro Score | 25% | 20% | ↓5% |
| SC Chain Score | — | 20% | 新增 |
| Sentiment Score | 20% | 20% | 持平 |
| Technical Score | 30% | 25% | ↓5% |
| Fundamental Score | 25% | 15% | ↓10% |

### SC Score 五子指標計算

| 子指標 | 滿分 | 數據來源 |
|--------|------|----------|
| 供應鏈位置評分 | 2.0 | 固定分類(CoWoS=2.0, ODM=1.8...) |
| 上游景氣傳導分數 | 2.0 | Stage 0.3 上游層溫度 |
| 下游需求能見度分數 | 2.0 | Stage 0.3 下游層溫度 |
| 法說NLP提及分數 | 2.0 | Module B NLP 分析結果 |
| 客戶集中度評分(反向) | 2.0 | Stage 3 基本面分析 |

### SC Score 分級

| 分數 | 標籤 | 含義 |
|------|------|------|
| 8.5 - 10 | CORE_AI | 核心 AI 受益者,最高優先 |
| 7.0 - 8.4 | HIGH_EXPOSURE | 高度暴露 AI 景氣,積極布局 |
| 5.5 - 6.9 | MODERATE | 中度受益,等待更好訊號 |
| 4.0 - 5.4 | LOW_EXPOSURE | 低度受益,非優先標的 |
| < 4.0 | AVOID | 供應鏈邏輯不支撐,建議迴避 |

---

## 三模組整合時序圖

```
Stage 0.5 → Macro Score (RISK-ON/NEUTRAL/RISK-OFF)
Stage 0.3 → SC Temperature Score (SUPPLY_EXPANSION/STABLE/CAUTIOUS/CONTRACTION)
Stage 1   → 市場研究 + NLP 法說分析 (NLP Transcript Score)
Stage 1.5 → Sentiment Score per stock
Stage 2   → Technical Score + Regime Detection
Stage 3   → Fundamental Score + Customer Concentration
Stage 4   → 五維度整合 (Macro 20% + SC 20% + Sentiment 20% + Tech 25% + Fund 15%) + Kelly
Stage 5   → CVaR 風控 + 最終裁決 (APPROVED/REDUCED/REJECTED)
```

---

## 數據品質保護機制(Fallback Rules)

| 故障情境 | 降級處理 | 警告訊息 |
|----------|----------|----------|
| MOPS 月營收數據不可用 | 使用前一月數據,打折係數 0.8 | SC Score 準確度降低 |
| 法說逐字稿找不到 | transcript_score 設為 1.0(中性) | NLP 子模組跳過 |
| SC Score 計算失敗 | Stage 4 回退至 v4 四維度模式 | 使用 v4 相容模式 |