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

    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "heading": heading_style,
        "body": body_style,
        "small": small_style,
        "label": label_style,
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