"""FastAPI application for Bug-Report Triage Agent.

Provides REST API endpoints to process incoming GitHub bug reports through
the LangGraph triage agent workflow.
"""

from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException

# Support running directly or via uvicorn
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.graph import build_triage_graph
from backend.schemas import TriageRequest, TriageResponse

# Initialize the FastAPI application
app = FastAPI(
    title="Bug Triage API",
    description="Multi-modal Bug Report Triage and Routing Agent for kubernetes/kubernetes",
    version="1.0.0",
)

# Initialize compiled LangGraph agent
triage_agent = build_triage_graph()


@app.get("/")
def read_root():
    """Health check and service status."""
    return {
        "status": "online",
        "service": "Bug Triage API",
        "docs_url": "/docs",
    }


@app.post("/triage", response_model=TriageResponse)
def triage_issue(request: TriageRequest):
    """Triage an incoming bug report using the LangGraph state graph.

    Cleans text, assesses diagnostic completeness, performs vector retrieval,
    computes cold-start GraphSAGE & label awareness representations, runs
    LightGBM classification, and drafts a tailored GitHub comment.
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Issue title cannot be empty.")

    input_payload = {
        "raw_title": request.title,
        "raw_body": request.body,
    }

    try:
        final_state = triage_agent.invoke(input_payload)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing triage workflow: {str(exc)}",
        ) from exc

    missing_info = final_state.get("missing_info", {})
    missing_fields = missing_info.get("missing_fields", []) if isinstance(missing_info, dict) else []

    return TriageResponse(
        predicted_label=final_state.get("predicted_label", "sig/node"),
        confidence=round(float(final_state.get("confidence", 0.0)), 4),
        missing_fields=missing_fields,
        similar_issues=final_state.get("similar_issues", []),
        draft_comment=final_state.get("draft_comment", ""),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
