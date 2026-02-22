"""
LangGraph State Schema — Team C: Pedagogy Federation
"""
from typing import TypedDict, Annotated, Optional
import operator


class PedagogyState(TypedDict):
    # Pipeline metadata
    pipeline_run_id: str
    config: dict

    # Inputs
    source_report_path: str       # Path to Team A report
    source_report_content: str    # Raw markdown of the report
    evolution_context: str        # Team B chronicle entry (may be empty string)

    # Stage outputs
    lesson_content: Optional[dict]   # Three-level lesson from lesson_designer
    quiz_content: Optional[dict]     # 10 questions from quiz_generator
    lesson_file_path: Optional[str]  # Where the final lesson was saved

    # Accumulating lists
    errors: Annotated[list, operator.add]
    orchestration_log: Annotated[list, operator.add]
