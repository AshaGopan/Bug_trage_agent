"""LangGraph workflow definition for Bug-Report Triage Agent (Phase 10).

Constructs the complete state machine orchestrating:
  START -> intake_node -> missing_info_node -> cold_start_node -> classifier_node
       -> conditional branch (confidence >= 0.60)
            -> writer_high_node -> END
            -> writer_low_node  -> END
"""

from pathlib import Path
import sys

# Ensure UTF-8 output encoding for Windows terminal
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langgraph.graph import END, START, StateGraph

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.nodes import (
    classifier_node,
    cold_start_node,
    intake_node,
    missing_info_node,
    writer_high_node,
    writer_low_node,
)
from agents.state import TriageState


def route_confidence(state: TriageState) -> str:
    """Conditional router based on classification confidence threshold (0.60)."""
    confidence = state.get("confidence", 0.0)
    if confidence >= 0.60:
        return "writer_high_node"
    return "writer_low_node"


def build_triage_graph():
    """Build and compile the LangGraph StateGraph workflow."""
    builder = StateGraph(TriageState)

    # Add all agent processing nodes
    builder.add_node("intake_node", intake_node)
    builder.add_node("missing_info_node", missing_info_node)
    builder.add_node("cold_start_node", cold_start_node)
    builder.add_node("classifier_node", classifier_node)
    builder.add_node("writer_high_node", writer_high_node)
    builder.add_node("writer_low_node", writer_low_node)

    # Define execution graph sequence
    builder.add_edge(START, "intake_node")
    builder.add_edge("intake_node", "missing_info_node")
    builder.add_edge("missing_info_node", "cold_start_node")
    builder.add_edge("cold_start_node", "classifier_node")

    # Conditional edge: branch based on confidence
    builder.add_conditional_edges(
        "classifier_node",
        route_confidence,
        {
            "writer_high_node": "writer_high_node",
            "writer_low_node": "writer_low_node",
        },
    )

    builder.add_edge("writer_high_node", END)
    builder.add_edge("writer_low_node", END)

    app = builder.compile()
    return app


if __name__ == "__main__":
    print("=" * 70)
    print("Phase 10: Executing LangGraph Triage Agent Workflow")
    print("=" * 70)

    # 1. Compile workflow
    agent = build_triage_graph()
    print("Compiled LangGraph StateGraph workflow successfully.")

    # 2. Dummy bug report for testing
    dummy_issue = {
        "raw_title": "Kubelet memory regression: Cadvisor housekeeping fails to back off when memory.high is reached",
        "raw_body": (
            "<!-- Please use this bug template -->\n"
            "### What happened?\n"
            "We observed a 30% increase in Kubelet RSS memory usage on node components. "
            "The memory manager cgroup v2 controller fails to respect memory.high thresholds "
            "when cadvisor housekeeping backoff triggers.\n\n"
            "### Environment\n"
            "- Node OS: Ubuntu 24.04 LTS\n"
            "- Container runtime: containerd 1.7.15"
        ),
    }

    print("\nSimulating triage for new bug report:")
    print(f"  Title: {dummy_issue['raw_title']}")
    print("-" * 70)

    # 3. Execute graph via .invoke()
    final_state = agent.invoke(dummy_issue)

    # 4. Display internal agent state
    print("\n" + "=" * 70)
    print("Agent Reasoning Results:")
    print("=" * 70)
    print(f"Predicted SIG Label : {final_state.get('predicted_label')}")
    print(f"Confidence Score    : {final_state.get('confidence', 0.0)*100:.2f}%")

    missing = final_state.get("missing_info", {})
    print(f"Missing Information : {missing.get('missing_fields')}")

    sim_issues = final_state.get("similar_issues", [])
    print(f"Similar Issues Found: {len(sim_issues)} issues")
    for s in sim_issues[:3]:
        print(f"  - #{s['issue_id']}: {s['title'][:55]}... ({s['label']})")

    # 5. Output final drafted triage comment
    print("\n" + "=" * 70)
    print("Final Drafted Triage Comment:")
    print("=" * 70)
    print(final_state.get("draft_comment"))
    print("=" * 70)
