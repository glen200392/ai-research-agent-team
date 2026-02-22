"""
LangGraph State Schema — Team B: Evolution Chronicle
"""
from typing import TypedDict, Annotated, Optional
import operator


class EvolutionState(TypedDict):
    # Pipeline metadata
    pipeline_run_id: str
    config: dict

    # Inputs
    source_report_path: str        # Path to Team A report to analyse
    source_report_content: str     # Raw markdown content of the report
    evolution_graph: dict          # Loaded evolution-graph.json

    # Stage outputs
    archaeology_results: Optional[dict]   # Tech profiles + proposed new edges
    chronicle_updates: Optional[dict]     # Content ready to write to files

    # Accumulating lists (merged across parallel nodes)
    errors: Annotated[list, operator.add]
    orchestration_log: Annotated[list, operator.add]
