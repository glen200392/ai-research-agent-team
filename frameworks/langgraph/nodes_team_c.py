"""
LangGraph Node Implementations — Team C: Pedagogy Federation
Agents: Lesson Designer → Quiz Generator → Lesson Packager (file I/O)
"""
import json
from datetime import datetime
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from .state_team_c import PedagogyState
from .nodes import _load_prompt, _extract_json   # reuse shared helpers


def _get_llm_c(config: dict, agent_name: str):
    from core.providers import get_llm
    return get_llm(config, agent_name=agent_name)


def _find_latest_report() -> tuple[str, str]:
    base = Path(__file__).parent.parent.parent
    reports_dir = base / "reports"
    reports = sorted(reports_dir.glob("AI_Tech_Report_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports:
        return "", ""
    path = reports[0]
    return str(path), path.read_text(encoding="utf-8")


def _find_latest_period_chronicle() -> str:
    """Return the latest by-period chronicle entry, or empty string."""
    base = Path(__file__).parent.parent.parent
    period_dir = base / "docs" / "evolution-chronicle" / "by-period"
    if not period_dir.exists():
        return ""
    entries = sorted(period_dir.glob("*.md"), key=lambda p: p.stem, reverse=True)
    if not entries:
        return ""
    return entries[0].read_text(encoding="utf-8")


# ── Node 0: Initialise Team C pipeline ───────────────────────────────────────

def team_c_init(state: PedagogyState) -> dict:
    """Load source report and Team B evolution context into state."""
    run_id = f"teamc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    report_path = state.get("source_report_path", "")
    if report_path and Path(report_path).exists():
        report_content = Path(report_path).read_text(encoding="utf-8")
    else:
        report_path, report_content = _find_latest_report()

    evolution_context = state.get("evolution_context", "") or _find_latest_period_chronicle()

    log_entry = {
        "step": "team_c_init",
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": run_id,
        "report": report_path,
        "has_evolution_context": bool(evolution_context),
    }

    return {
        "pipeline_run_id": run_id,
        "source_report_path": report_path,
        "source_report_content": report_content,
        "evolution_context": evolution_context,
        "errors": [],
        "orchestration_log": [log_entry],
    }


# ── Node 1: Lesson Designer ───────────────────────────────────────────────────

def lesson_designer(state: PedagogyState) -> dict:
    """Generate three-level educational content for the month's key technology."""
    llm = _get_llm_c(state["config"], "lesson_designer")
    system_prompt = _load_prompt("team_c/10_lesson_designer.md")

    evolution_section = ""
    if state.get("evolution_context"):
        evolution_section = f"""
    EVOLUTION CONTEXT (from Team B):
    {state['evolution_context'][:2000]}
    """

    task = f"""
    Design a complete three-level lesson based on this month's AI research report.

    MONTHLY REPORT:
    {state["source_report_content"][:5000]}
    {evolution_section}

    Select the single most important technology to teach.
    Produce lesson JSON with level_1 (beginner), level_2 (practitioner), level_3 (expert).
    All narrative content in Traditional Chinese. Technical terms may be English.
    """

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task)]

    try:
        response = llm.invoke(messages)
        parsed = _extract_json(response.content)
        lesson = parsed if parsed else {"raw": response.content}
    except Exception as e:
        lesson = {"error": str(e)}

    log_entry = {
        "step": "lesson_designer",
        "timestamp": datetime.utcnow().isoformat(),
        "focus_technology": lesson.get("lesson", lesson).get("focus_technology", "unknown"),
    }

    return {
        "lesson_content": lesson,
        "orchestration_log": [log_entry],
    }


# ── Node 2: Quiz Generator ────────────────────────────────────────────────────

def quiz_generator(state: PedagogyState) -> dict:
    """Generate 10 questions (3 L1 / 4 L2 / 3 L3) based on lesson content."""
    llm = _get_llm_c(state["config"], "quiz_generator")
    system_prompt = _load_prompt("team_c/11_quiz_generator.md")

    task = f"""
    Generate exactly 10 quiz questions based on this lesson content.

    LESSON CONTENT:
    {json.dumps(state.get("lesson_content", {}), indent=2, ensure_ascii=False)[:6000]}

    Follow the distribution: Q1-3 Level 1, Q4-7 Level 2, Q8-10 Level 3.
    Each question must have 4 options, a correct_answer, and an explanation.
    All question text in Traditional Chinese.
    """

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task)]

    try:
        response = llm.invoke(messages)
        parsed = _extract_json(response.content)
        quiz = parsed if parsed else {"raw": response.content}
    except Exception as e:
        quiz = {"error": str(e)}

    log_entry = {
        "step": "quiz_generator",
        "timestamp": datetime.utcnow().isoformat(),
        "questions_generated": len(quiz.get("quiz", quiz).get("questions", [])),
    }

    return {
        "quiz_content": quiz,
        "orchestration_log": [log_entry],
    }


# ── Node 3: Lesson Packager (file I/O) ────────────────────────────────────────

def lesson_packager(state: PedagogyState) -> dict:
    """Assemble and save the complete lesson (3 levels + quiz) to disk."""
    base = Path(__file__).parent.parent.parent
    today = datetime.now().strftime("%Y-%m-%d")
    lesson_dir = base / "pedagogy" / "weekly-lessons" / today
    lesson_dir.mkdir(parents=True, exist_ok=True)
    lesson_file = lesson_dir / "complete-lesson.md"

    lesson = state.get("lesson_content", {}).get("lesson", state.get("lesson_content", {}))
    quiz = state.get("quiz_content", {}).get("quiz", state.get("quiz_content", {}))
    focus_tech = lesson.get("focus_technology", "Unknown Technology")
    target_month = lesson.get("target_month", today[:7])

    try:
        sections = [
            f"# AI 學習課程：{focus_tech}",
            f"**生成日期：** {today}  ",
            f"**涵蓋月份：** {target_month}  ",
            f"**焦點技術：** {focus_tech}  ",
            "",
            "---",
            "",
            f"> **選題理由：** {lesson.get('focus_selection_reasoning', '')}",
            "",
            "---",
        ]

        # Level 1
        l1 = lesson.get("level_1", {})
        if l1:
            sections += [
                f"## 🟢 Level 1 — {l1.get('title', '入門')}",
                f"*適合讀者：{l1.get('audience_label', '完全沒概念的朋友')}*",
                "",
                l1.get("content_markdown", "（內容生成中）"),
                "",
                "---",
                "",
            ]

        # Level 2
        l2 = lesson.get("level_2", {})
        if l2:
            sections += [
                f"## 🟡 Level 2 — {l2.get('title', '進階')}",
                f"*適合讀者：{l2.get('audience_label', '有技術背景的工程師')}*",
                "",
                l2.get("content_markdown", "（內容生成中）"),
                "",
                "---",
                "",
            ]

        # Level 3
        l3 = lesson.get("level_3", {})
        if l3:
            sections += [
                f"## 🔴 Level 3 — {l3.get('title', '專業')}",
                f"*適合讀者：{l3.get('audience_label', 'ML研究者與工程師')}*",
                "",
                l3.get("content_markdown", "（內容生成中）"),
                "",
                "---",
                "",
            ]

        # Quiz
        if quiz and quiz.get("questions"):
            sections.append(f"## 📝 理解測驗（{len(quiz['questions'])} 題）")
            sections.append("")
            for q in quiz["questions"]:
                sections.append(f"**Q{q.get('number', '?')}. [{['', 'L1', 'L2', 'L3'][q.get('level', 0)]}] {q.get('question', '')}**")
                for letter, option in q.get("options", {}).items():
                    sections.append(f"- {letter}) {option}")
                sections.append(f"> 正確答案：**{q.get('correct_answer', '?')}**")
                sections.append(f"> {q.get('explanation', '')}")
                sections.append("")

            if quiz.get("scoring_guide"):
                sections.append("### 得分說明")
                for score, desc in quiz["scoring_guide"].items():
                    sections.append(f"- **{score} 分**：{desc}")

        sections.append("\n---\n*本課程由 **AI Research Agent Team — Team C** 自動生成*")

        content = "\n".join(sections)
        lesson_file.write_text(content, encoding="utf-8")

        status = "success"
        error = None

    except Exception as e:
        status = "failed"
        error = str(e)

    log_entry = {
        "step": "lesson_packager",
        "timestamp": datetime.utcnow().isoformat(),
        "file_path": str(lesson_file),
        "status": status,
    }

    errors = [f"lesson_packager: {error}"] if error else []

    return {
        "lesson_file_path": str(lesson_file),
        "errors": errors,
        "orchestration_log": [log_entry],
    }
