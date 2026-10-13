"""Pydantic data schemas for Bug Triage FastAPI backend."""

from typing import Any
from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    """Input payload representing an incoming GitHub bug report."""

    title: str = Field(..., description="The title of the bug report")
    body: str = Field(..., description="The markdown or plain text description of the bug report")


class TriageResponse(BaseModel):
    """Output payload returned by the LangGraph triage workflow."""

    predicted_label: str = Field(..., description="Recommended Special Interest Group (SIG) category")
    confidence: float = Field(..., description="Classification model confidence score (0.0 to 1.0)")
    missing_fields: list[str] = Field(default_factory=list, description="Diagnostic fields missing from the report")
    similar_issues: list[dict[str, Any]] = Field(default_factory=list, description="Top retrieved similar historical issues")
    draft_comment: str = Field(..., description="Automated professional triage comment ready for GitHub")
