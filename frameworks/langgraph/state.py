"""
LangGraph State Schema
Shared state that flows through the entire research pipeline.
"""
from typing import TypedDict, Annotated, Optional
import operator


class ResearchState(TypedDict):
    # Pipeline metadata
    pipeline_run_id: str
    target_month: str           # e.g. "2026-02"
    time_range_start: str       # e.g. "2026-02-01"
    time_range_end: str         # e.g. "2026-02-28"
    config: dict

    # Stage outputs
    intel_collection: Optional[dict]
    tech_analysis: Optional[dict]
    market_analysis: Optional[dict]
    content_package: Optional[dict]
    qa_report: Optional[dict]
    revision_number: int
    delivery_report: Optional[dict]

    # Accumulating lists
    errors: Annotated[list, operator.add]
    orchestration_log: Annotated[list, operator.add]
