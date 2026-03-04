"""
AI 投資日報 PDF 生成器 v2
修復：嵌入 Noto Sans TC 字體，完整支援繁體中文渲染
適用市場：台股 / 美股 / 日股
"""

import os
import subprocess
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# ─────────────────────────────────────────
#  字體安裝與註冊（支援繁體中文）
# ─────────────────────────────────────────

FONT_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJKtc-Regular.otf",
    "/home/user/fonts/NotoSansTC-Regular.ttf",
    "/tmp/NotoSansTC-Regular.ttf",
]

FONT_BOLD_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/home/user/fonts/NotoSansTC-Bold.ttf",
    "/tmp/NotoSansTC-Bold.ttf",
]

FONT_DOWNLOAD_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/TC/NotoSansTC-Regular.otf"
FONT_BOLD_DOWNLOAD_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/TC/NotoSansTC-Bold.otf"


def _download_font(url: str, dest: str) -> bool:
    """下載字體到本地，失敗回傳 False。"""
    try:
        import urllib.request
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        urllib.request.urlretrieve(url, dest)
        return os.path.exists(dest)
    except Exception as e:
        print(f"[font] download failed: {e}")
        return False


def _register_fonts() -> tuple[str, str]:
    """
    嘗試以優先順序找到並註冊中文字體。
    回傳 (regular_name, bold_name)，找不到時 fallback 到 Helvetica。
    """
    reg_path = None
    bold_path = None

    # 找 Regular
    for p in FONT_PATHS:
        if os.path.exists(p):
            reg_path = p
            break

    # 找 Bold
    for p in FONT_BOLD_PATHS:
        if os.path.exists(p):
            bold_path = p
            break

    # 找不到就下載
    if not reg_path:
        dest = "/tmp/NotoSansTC-Regular.otf"
        if _download_font(FONT_DOWNLOAD_URL, dest):
            reg_path = dest
        else:
            print("[font] WARNING: Cannot load Chinese font. Text may render as boxes.")
            return "Helvetica", "Helvetica-Bold"

    if not bold_path:
        dest = "/tmp/NotoSansTC-Bold.otf"
        if _download_font(FONT_BOLD_DOWNLOAD_URL, dest):
            bold_path = dest
        else:
            bold_path = reg_path  # fallback: bold 用 regular

    try:
        pdfmetrics.registerFont(TTFont("NotoSansTC", reg_path))
        pdfmetrics.registerFont(TTFont("NotoSansTC-Bold", bold_path))
        print(f"[font] Registered NotoSansTC from {reg_path}")
        return "NotoSansTC", "NotoSansTC-Bold"
    except Exception as e:
        print(f"[font] Registration failed: {e}")
        return "Helvetica", "Helvetica-Bold"


# 全域字體名稱（模組載入時即執行）
_FONT_REG, _FONT_BOLD = _register_fonts()


# ─────────────────────────────────────────
#  樣式工廠
# ─────────────────────────────────────────

def _build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CTitle",
        parent=base["Heading1"],
        fontSize=22,
        textColor=colors.HexColor("#1a5490"),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName=_FONT_BOLD,
        leading=28,
        wordWrap="CJK",
    )

    subtitle_style = ParagraphStyle(
        "CSubtitle",
        parent=base["BodyText"],
        fontSize=11,
        textColor=colors.HexColor("#555555"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName=_FONT_REG,
        leading=16,
        wordWrap="CJK",
    )

    heading_style = ParagraphStyle(
        "CHeading",
        parent=base["Heading2"],
        fontSize=15,
        textColor=colors.HexColor("#2c5aa0"),
        spaceAfter=10,
        spaceBefore=18,
        fontName=_FONT_BOLD,
        leading=20,
        wordWrap="CJK",
    )

    body_style = ParagraphStyle(
        "CBody",
        parent=base["BodyText"],
        fontSize=10,
        leading=16,
        fontName=_FONT_REG,
        spaceAfter=4,
        wordWrap="CJK",
    )

    small_style = ParagraphStyle(
        "CSmall",
        parent=base["BodyText"],
        fontSize=8,
        leading=12,
        fontName=_FONT_REG,
        textColor=colors.grey,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )

    label_style = ParagraphStyle(
        "CLabel",
        parent=base["BodyText"],
        fontSize=9,
        leading=13,
        fontName=_FONT_BOLD,
        textColor=colors.HexColor("#333333"),
        wordWrap="CJK",
    )

    gp_header_style = ParagraphStyle(
        "gp_header",
        fontName=_FONT_BOLD,
        fontSize=10,
        textColor=colors.white,
        backColor=colors.HexColor("#34495e"),
        leading=16,
        spaceBefore=10,
        spaceAfter=4,
        leftIndent=6,
        rightIndent=6,
        wordWrap="CJK",
    )
    gp_body_style = ParagraphStyle(
        "gp_body",
        fontName=_FONT_REG,
        fontSize=8,
        textColor=colors.HexColor("#2c3e50"),
        backColor=colors.HexColor("#f4f6f7"),
        leading=13,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=8,
        rightIndent=8,
        wordWrap="CJK",
    )
    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "heading": heading_style,
        "body": body_style,
        "small": small_style,
        "label": label_style,
        "gp_header": gp_header_style,
        "gp_body": gp_body_style,
    }


# ─────────────────────────────────────────
#  工具函式
# ─────────────────────────────────────────

def _safe_str(val, fallback="N/A") -> str:
    """安全轉字串，避免 None 造成 PDF 建構失敗。"""
    if val is None:
        return fallback
    return str(val)


def _make_header_table(report_data: dict, s: dict):
    """封面資訊卡片。"""
    title = report_data.get("report_title", "AI 投資日報")
    date_str = report_data.get("report_date", datetime.now().strftime("%Y-%m-%d"))
    version = report_data.get("pipeline_version", "v5")

    story = []
    story.append(Paragraph(_safe_str(title), s["title"]))
    story.append(Paragraph(
        f"報告日期：{date_str}　　Pipeline {version}",
        s["subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2c5aa0")))
    story.append(Spacer(1, 0.4 * cm))
    return story


def _make_summary_table(report_data: dict, s: dict):
    """執行摘要評分表。"""
    macro = report_data.get("macro", {})
    sc = report_data.get("supply_chain", {})
    senti = report_data.get("sentiment", {})
    tech = report_data.get("technical", {})
    fund = report_data.get("fundamental", {})

    rows = [
        ["指標", "評分 (0-10)", "體制 / 信號"],
    ]

    def row(label, score, regime):
        return [_safe_str(label), _safe_str(score), _safe_str(regime)]

    # 台股有供應鏈溫度
    if sc:
        rows.append(row("總體環境 (Macro)", f"{macro.get('score', 'N/A')}/10", macro.get("regime", "N/A")))
        rows.append(row("供應鏈溫度 (SC)", f"{sc.get('score', 'N/A')}/10", sc.get("regime", "N/A")))
    else:
        rows.append(row("總體環境 (Macro)", f"{macro.get('score', 'N/A')}/10", macro.get("regime", "N/A")))

    rows.append(row("市場情緒 (Sentiment)", f"{senti.get('score', 'N/A')}/10", senti.get("regime", "N/A")))
    rows.append(row("技術分析 (Technical)", f"{tech.get('avg_score', 'N/A')}/10", f"{tech.get('bull_count', 0)} BULL"))
    rows.append(row("基本面 (Fundamental)", f"{fund.get('avg_score', 'N/A')}/10", f"{fund.get('buy_count', 0)} BUY"))

    col_widths = [7 * cm, 3.5 * cm, 4.5 * cm]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5490")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), _FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTNAME", (0, 1), (-1, -1), _FONT_REG),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
    ]))
    return t


def _make_position_table(final_positions: list, s: dict):
    """最終倉位表格。"""
    rows = [["代碼", "名稱", "倉位 %", "CVaR 95%", "決策"]]
    for pos in (final_positions or [])[:12]:
        verdict = _safe_str(pos.get("decision", pos.get("verdict", "N/A")))
        color_map = {"APPROVED": "#27ae60", "REDUCED": "#f39c12", "REJECTED": "#e74c3c"}
        rows.append([
            _safe_str(pos.get("ticker")),
            _safe_str(pos.get("name")),
            f"{pos.get('weight', pos.get('final_pct', 0)):.1f}%",
            f"{pos.get('cvar_95', 0):.1f}%",
            verdict,
        ])

    col_widths = [2 * cm, 3.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5aa0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), _FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), _FONT_REG),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    return t


def _embed_chart(path: str, width_cm=14, height_cm=10):
    """安全嵌入圖表 PNG，找不到時回傳 None。"""
    if path and os.path.exists(path):
        return Image(path, width=width_cm * cm, height=height_cm * cm)
    return None


# ─────────────────────────────────────────
#  Global Perspective (EN) 區塊渲染
# ─────────────────────────────────────────

def _make_global_perspective_block(gp_data: dict, ticker: str, s: dict) -> list:
    """
    為單一股票渲染 Global Perspective (EN) 灰底卡片。
    gp_data: en_global_perspective dict，任何欄位可選。
    回傳 Flowable list。
    """
    if not gp_data:
        return []

    flowables = []

    # 欄位標籤 → 顯示名稱映射（涵蓋台股/美股/日股所有欄位）
    field_labels = {
        # 台股 Stage 1
        "institutional_flows":       "Institutional Flows",
        "analyst_calls":             "Analyst Calls",
        "global_catalyst":           "Global Catalyst",
        "supply_chain_en":           "Supply Chain (Global View)",
        # 台股 Stage 2
        "foreign_flow":              "Foreign Flow",
        "global_peers_comparison":   "Global Peers Comparison",
        "smart_money_signal":        "Smart Money Signal",
        # 台股 Stage 3
        "foreign_institutional_rating": "Foreign Institutional Rating",
        "consensus_eps_usd":         "Consensus EPS (USD)",
        "peer_valuation_gap":        "Peer Valuation Gap",
        "key_risk_en":               "Key Risk (EN)",
        # 台股 Stage 4
        "foreign_ownership_pct":     "Foreign Ownership %",
        "etf_inclusion":             "ETF Inclusion",
        "global_demand_driver":      "Global Demand Driver",
        "institutional_consensus":   "Institutional Consensus",
        # 台股 Stage 5
        "macro_risk_en":             "Macro Risk (EN)",
        "geopolitical_risk_en":      "Geopolitical Risk",
        "portfolio_var_usd":         "Portfolio VaR (USD)",
        "hedge_suggestion_en":       "Hedge Suggestion",
        # 美股 Stage 1
        "global_macro_en":           "Global Macro",
        "key_catalyst_en":           "Key Catalyst",
        # 美股 Stage 2
        "options_flow":              "Options Flow",
        "short_interest":            "Short Interest",
        "sector_rotation_en":        "Sector Rotation",
        "technical_vs_peers":        "Technical vs Peers",
        # 美股 Stage 3
        "wall_street_consensus":     "Wall Street Consensus",
        "consensus_pt_usd":          "Consensus Price Target",
        "earnings_revision_trend":   "Earnings Revision Trend",
        "competitive_moat_en":       "Competitive Moat",
        # 美股 Stage 4
        "index_weight":              "Index Weight",
        "etf_flow":                  "ETF Flow",
        "global_ai_positioning":     "Global AI Positioning",
        "institutional_ownership_change": "Institutional Ownership Change",
        # 美股 Stage 5
        "macro_tail_risk_en":        "Macro Tail Risk",
        "sector_correlation_en":     "Sector Correlation",
        "usd_impact_en":             "USD Impact",
        "hedge_tools_en":            "Hedge Tools",
        # 日股 Stage 1
        "foreign_net_buying":        "Foreign Net Buying (TSE)",
        "global_supply_chain_en":    "Global Supply Chain Role",
        "boj_impact_en":             "BOJ Policy Impact",
        # 日股 Stage 2
        "foreign_flow_en":           "Foreign Flow (TSE)",
        "jpy_technical_impact":      "JPY Technical Impact",
        "nikkei_relative_strength":  "Nikkei Relative Strength",
        "options_market_en":         "Options Market Signal",
        # 日股 Stage 3
        "foreign_broker_rating":     "Foreign Broker Rating",
        "consensus_eps_jpy":         "Consensus EPS (JPY)",
        "jpy_earnings_sensitivity":  "JPY Earnings Sensitivity",
        "global_peer_comparison_en": "Global Peer Comparison",
        # 日股 Stage 4
        "msci_japan_weight":         "MSCI Japan Weight",
        "global_ai_theme_fit":       "Global AI Theme Fit",
        "carry_trade_risk_en":       "Carry Trade Risk",
        # 日股 Stage 5
        "jpy_tail_risk_en":          "JPY Tail Risk",
        "boj_policy_risk_en":        "BOJ Policy Risk",
        "china_demand_risk_en":      "China Demand Risk",
    }

    # 標頭
    header_text = f"Global Perspective (EN) — {ticker}" if ticker else "Global Perspective (EN)"
    flowables.append(Paragraph(header_text, s["gp_header"]))

    # 每個非空欄位渲染為一行
    for key, label in field_labels.items():
        val = gp_data.get(key)
        if not val:
            continue
        # analyst_calls 是 list，特殊處理
        if isinstance(val, list):
            lines = "; ".join(
                f"{item.get('firm','?')} {item.get('action','?')} {item.get('ticker', item.get('ticker',''))} "
                f"PT={item.get('target_price', item.get('target_price_jpy','N/A'))}"
                for item in val
            )
            val = lines if lines else "N/A"
        flowables.append(Paragraph(
            f"<b>{label}:</b> {_safe_str(val)}",
            s["gp_body"]
        ))

    flowables.append(Spacer(1, 0.3 * cm))
    return flowables


# ─────────────────────────────────────────
#  主建構函式
# ─────────────────────────────────────────

def build_report(report_data: dict, output_path: str) -> str:
    """
    生成 AI 投資日報 PDF（支援台股 / 美股 / 日股）。

    Args:
        report_data: 包含所有 Stage 資料和 charts 路徑的 dict
        output_path: PDF 輸出完整路徑

    Returns:
        生成的 PDF 路徑字串
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=report_data.get("report_title", "AI Investment Report"),
        author="Nebula AI Pipeline",
    )

    s = _build_styles()
    story = []
    charts = report_data.get("charts", {})

    # ── 封面 ──────────────────────────────
    story.extend(_make_header_table(report_data, s))

    # ── 執行摘要 ─────────────────────────
    story.append(Paragraph("執行摘要", s["heading"]))
    story.append(_make_summary_table(report_data, s))
    story.append(Spacer(1, 0.5 * cm))

    # 總體環境文字摘要
    macro_summary = report_data.get("macro", {}).get("summary", "")
    if macro_summary:
        story.append(Paragraph(_safe_str(macro_summary), s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    # ── Chapter 1: 五維度雷達圖 ────────────
    story.append(PageBreak())
    story.append(Paragraph("Chapter 1：五維度綜合評分", s["heading"]))
    sc_summary = report_data.get("supply_chain", {}).get("summary", "")
    if sc_summary:
        story.append(Paragraph(_safe_str(sc_summary), s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    chart = _embed_chart(charts.get("radar"), 14, 10)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ 雷達圖尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 2: Kelly 倉位 ──────────────
    story.append(PageBreak())
    story.append(Paragraph("Chapter 2：Kelly Criterion 倉位配置", s["heading"]))
    story.append(Spacer(1, 0.3 * cm))

    chart = _embed_chart(charts.get("kelly_pie"), 12, 9)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ Kelly 圓餅圖尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("最終核准倉位（CVaR 調整後）", s["heading"]))
    final_positions = report_data.get("final_positions", [])
    if final_positions:
        story.append(_make_position_table(final_positions, s))
    else:
        story.append(Paragraph("（本次無核准倉位資料）", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 3: CVaR 風險 ───────────────
    story.append(PageBreak())
    story.append(Paragraph("Chapter 3：CVaR 風險管理", s["heading"]))

    pr = report_data.get("portfolio_risk", {})
    risk_text = (
        f"組合 CVaR 95%：{_safe_str(pr.get('cvar_95'))}%　"
        f"CVaR 99%：{_safe_str(pr.get('cvar_99'))}%　"
        f"最大回撤：{_safe_str(pr.get('max_drawdown'))}%　"
        f"裁決：{_safe_str(pr.get('verdict'))}"
    )
    story.append(Paragraph(risk_text, s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    chart = _embed_chart(charts.get("cvar_bar"), 14, 10)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ CVaR 長條圖尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 4: 市場特色圖（台股=供應鏈熱圖；美股=動能排行；日股=JPY 敏感度）──
    story.append(PageBreak())
    chart4_title = report_data.get("chart4_title", "Chapter 4：市場特色分析")
    story.append(Paragraph(chart4_title, s["heading"]))
    senti_summary = report_data.get("sentiment", {}).get("summary", "")
    if senti_summary:
        story.append(Paragraph(_safe_str(senti_summary), s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    # 台股用 sc_heatmap，美股用 momentum_bar，日股用 jpy_matrix，通用 fallback
    chart4_key = report_data.get("chart4_key", "sc_heatmap")
    chart = _embed_chart(charts.get(chart4_key) or charts.get("sc_heatmap") or charts.get("momentum_bar"), 14, 10)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ Chapter 4 圖表尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 5: 技術分析 ────────────────
    story.append(PageBreak())
    story.append(Paragraph("Chapter 5：技術分析趨勢圖", s["heading"]))
    tech_summary = report_data.get("technical", {}).get("summary", "")
    if tech_summary:
        story.append(Paragraph(_safe_str(tech_summary), s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    chart = _embed_chart(charts.get("technical"), 14, 10)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ 技術分析圖尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 6: 情緒散佈圖 ──────────────
    story.append(PageBreak())
    story.append(Paragraph("Chapter 6：市場情緒散點圖", s["heading"]))
    fund_summary = report_data.get("fundamental", {}).get("summary", "")
    if fund_summary:
        story.append(Paragraph(_safe_str(fund_summary), s["body"]))
    story.append(Spacer(1, 0.3 * cm))

    chart = _embed_chart(charts.get("sentiment_scatter"), 14, 10)
    if chart:
        story.append(chart)
    else:
        story.append(Paragraph("⚠ 情緒散點圖尚未生成或路徑不存在", s["body"]))
    story.append(Spacer(1, 0.5 * cm))

    # ── Chapter 7: Global Perspective (EN) ──
    # 從各 Stage 的 stocks 陣列中收集 en_global_perspective，每股渲染一個灰底卡片
    story.append(PageBreak())
    story.append(Paragraph("Chapter 7：Global Perspective (EN)", s["heading"]))
    story.append(Paragraph(
        "The following insights are sourced directly from English-language institutional research, "
        "foreign broker ratings, and global market data — supplementing the Chinese analysis above "
        "with an international investor perspective.",
        s["body"]
    ))
    story.append(Spacer(1, 0.4 * cm))

    # 收集所有股票的 en_global_perspective（從 Stage 1~5 各層合併，ticker 為 key）
    gp_by_ticker: dict = {}
    for stage_key in ["market_research", "technical", "fundamental", "portfolio", "risk"]:
        stage_data = report_data.get(stage_key, {})
        stocks = stage_data.get("stocks", [])
        if isinstance(stocks, list):
            for stock in stocks:
                ticker = _safe_str(stock.get("ticker", ""))
                gp = stock.get("en_global_perspective", {})
                if gp and isinstance(gp, dict):
                    if ticker not in gp_by_ticker:
                        gp_by_ticker[ticker] = {}
                    gp_by_ticker[ticker].update(gp)

    # 也嘗試從頂層 en_global_perspective 取市場級別資料
    market_gp = report_data.get("en_global_perspective", {})
    if market_gp:
        story.extend(_make_global_perspective_block(market_gp, "Market Overview", s))

    if gp_by_ticker:
        for ticker, gp_data in gp_by_ticker.items():
            story.extend(_make_global_perspective_block(gp_data, ticker, s))
    else:
        story.append(Paragraph(
            "（Global Perspective data not available for this report — "
            "ensure Stage 1-5 format_guide includes en_global_perspective fields.）",
            s["body"]
        ))
    story.append(Spacer(1, 0.5 * cm))

    # ── 關鍵發現 ──────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("關鍵發現", s["heading"]))
    for i, finding in enumerate(report_data.get("key_findings", []), 1):
        story.append(Paragraph(f"{i}. {_safe_str(finding)}", s["body"]))
        story.append(Spacer(1, 0.15 * cm))

    story.append(Spacer(1, 0.4 * cm))

    # ── 風險警示 ──────────────────────────
    story.append(Paragraph("風險警示", s["heading"]))
    for i, warning in enumerate(report_data.get("risk_warnings", []), 1):
        story.append(Paragraph(f"{i}. {_safe_str(warning)}", s["body"]))
        story.append(Spacer(1, 0.15 * cm))

    # ── 頁尾 ──────────────────────────────
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        f"Powered by Nebula AI Pipeline　|　Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (CST)",
        s["small"]
    ))

    # ── 建構 PDF ──────────────────────────
    doc.build(story)
    print(f"[pdf] Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("AI Investment PDF Generator v2 — supports Traditional Chinese")
    print("Usage: build_report(report_data, output_path)")
