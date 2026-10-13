"""State schema for Bug-Report Triage Agent workflow (Phase 10)."""

from typing import Any, Optional, TypedDict


class TriageState(TypedDict, total=False):
    """The central state passed between LangGraph agent nodes."""

    raw_title: str
    raw_body: str
    clean_body: str
    missing_info: dict[str, Any]
    similar_issues: list[dict[str, Any]]
    predicted_label: str
    confidence: float
    draft_comment: str

    # Feature representations for multi-modal classification
    text_vec: Any
    graph_vec: Any
    label_aware_vec: Any
