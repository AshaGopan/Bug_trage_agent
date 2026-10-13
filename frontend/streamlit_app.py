"""Streamlit UI for Bug-Report Triage Agent.

Communicates with the FastAPI backend over HTTP to triage Kubernetes bug reports,
retrieve similar historical issues, analyze diagnostic completeness, and generate
actionable triage drafts for maintainer review.
"""

import os
import requests
import streamlit as st

# Configuration
API_URL = os.getenv("TRIAGE_API_URL", "http://127.0.0.1:8000/triage")
HEALTH_URL = os.getenv("API_HEALTH_URL", "http://127.0.0.1:8000/")

st.set_page_config(
    page_title="Bug-Report Triage Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for polished aesthetics
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .issue-card {
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if "issue_title" not in st.session_state:
    st.session_state.issue_title = (
        "Kubelet memory regression: Cadvisor housekeeping fails to back off when memory.high is reached"
    )

if "issue_body" not in st.session_state:
    st.session_state.issue_body = (
        "### What happened?\n"
        "We observed an unexpected 35% increase in Kubelet RSS memory usage on node components "
        "running v1.30. The memory manager cgroup v2 controller fails to respect memory.high "
        "thresholds when cadvisor housekeeping backoff triggers during high node pod churn.\n\n"
        "### What did you expect to happen?\n"
        "Cadvisor housekeeping should back off gracefully under cgroup memory pressure.\n\n"
        "### How to reproduce it?\n"
        "1. Create a cluster with cgroups v2 enabled.\n"
        "2. Generate heavy pod churn with 100 pods per node.\n"
        "3. Monitor Kubelet resident set size memory consumption.\n\n"
        "### Environment\n"
        "- Kubernetes version: v1.30.1\n"
        "- OS: Ubuntu 24.04 LTS\n"
        "- Container runtime: containerd 1.7.16"
    )

# Sidebar
with st.sidebar:
    st.title("⚙️ Triage Agent Settings")
    st.caption("Human-in-the-Loop Maintainer Workspace")

    st.markdown("---")
    st.subheader("FastAPI Backend Status")

    # Quick Backend Health Check
    try:
        health_resp = requests.get(HEALTH_URL, timeout=2.0)
        if health_resp.status_code == 200:
            st.success("🟢 Backend Connected (`http://127.0.0.1:8000`)")
        else:
            st.warning(f"🟡 Backend returned HTTP {health_resp.status_code}")
    except Exception:
        st.error("🔴 Backend Unreachable! Ensure FastAPI is running on port 8000.")

    st.markdown("---")
    st.subheader("💡 Sample Bug Reports")

    sample_1 = st.button("Sample 1: Kubelet Memory Regression")
    if sample_1:
        st.session_state.issue_title = (
            "Kubelet memory regression: Cadvisor housekeeping fails to back off when memory.high is reached"
        )
        st.session_state.issue_body = (
            "### What happened?\n"
            "We observed an unexpected 35% increase in Kubelet RSS memory usage on node components.\n\n"
            "### How to reproduce it?\n"
            "1. Spawn 100 short-lived pods.\n\n"
            "### Environment\n"
            "- OS: Ubuntu 24.04 LTS\n"
            "- Runtime: containerd 1.7.16"
        )
        st.session_state.triage_result = None
        st.rerun()

    sample_2 = st.button("Sample 2: Incomplete Network Issue")
    if sample_2:
        st.session_state.issue_title = "Pods cannot communicate across nodes in Calico overlay"
        st.session_state.issue_body = (
            "Network connection drops intermittently between worker nodes. Please fix ASAP."
        )
        st.session_state.triage_result = None
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        **Architecture**:
        - **Frontend**: Streamlit
        - **Communication**: REST API (`requests`)
        - **Backend**: FastAPI + LangGraph
        - **ML Components**: LightGBM + GraphSAGE + ChromaDB
        """
    )

# Main Header
st.title("🤖 Bug-Report Triage Agent")
st.markdown(
    "<div class='sub-header'>Automated multi-modal triage, SIG routing, diagnostic auditing, and comment drafting for <code>kubernetes/kubernetes</code></div>",
    unsafe_allow_html=True,
)

# Input Section
st.subheader("📝 Incoming Bug Report")

title_input = st.text_input(
    "Issue Title",
    value=st.session_state.issue_title,
    placeholder="e.g., Kubelet memory leak when mounting CSI volume",
    help="Enter the bug report's title as submitted to the GitHub repository.",
)

body_input = st.text_area(
    "Issue Body",
    value=st.session_state.issue_body,
    height=200,
    placeholder="Enter the full markdown body of the issue report...",
    help="Provide the complete issue description, reproduction steps, and diagnostic details.",
)

# Action Button
col_btn, _ = st.columns([1, 4])
with col_btn:
    run_triage = st.button("🚀 Run Triage Agent", type="primary", use_container_width=True)

if run_triage:
    if not title_input.strip():
        st.warning("⚠️ Please provide an Issue Title before running the triage agent.")
    else:
        with st.spinner("⏳ Triaging bug report via LangGraph pipeline (Embedding -> GraphSAGE -> LightGBM)..."):
            try:
                payload = {
                    "title": title_input.strip(),
                    "body": body_input.strip(),
                }
                response = requests.post(API_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    st.session_state.triage_result = response.json()
                    st.success("✅ Triage completed successfully!")
                else:
                    st.error(f"❌ Backend returned error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Failed to connect to FastAPI backend at `http://127.0.0.1:8000/triage`. Please ensure the server is active.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

# Display Results Section
result = st.session_state.triage_result

if result:
    st.markdown("---")
    st.header("🎯 Triage Assessment Results")

    # 1. Prediction Metrics
    col1, col2, col3 = st.columns([2, 2, 3])

    predicted_label = result.get("predicted_label", "Unknown")
    confidence = float(result.get("confidence", 0.0))

    with col1:
        st.metric(
            label="Recommended SIG Label",
            value=predicted_label,
            help="Predicted Kubernetes Special Interest Group (SIG) category.",
        )

    with col2:
        st.metric(
            label="Classification Confidence",
            value=f"{confidence * 100:.1f}%",
            delta="High Confidence" if confidence >= 0.60 else "Low / Needs Review",
            delta_color="normal" if confidence >= 0.60 else "inverse",
            help="Multi-modal confidence score calculated by hybrid LightGBM model.",
        )

    with col3:
        st.caption("Confidence Level")
        st.progress(min(max(confidence, 0.0), 1.0))
        if confidence >= 0.60:
            st.caption("🟢 Route: High-confidence automated triage action")
        else:
            st.caption("🟡 Route: Low-confidence human maintainer inspection recommended")

    st.markdown("###")

    # 2. Diagnostic Completeness / Missing Fields
    missing_fields = result.get("missing_fields", [])
    if missing_fields:
        fields_str = ", ".join([f"`{f}`" for f in missing_fields])
        st.warning(
            f"⚠️ **Diagnostic Completeness Notice**: The following required fields were missing from this report: {fields_str}. "
            "The triage comment will prompt the contributor to provide these diagnostic details."
        )
    else:
        st.success("✅ **Diagnostic Audit Passed**: All critical fields (reproduction steps, environment, logs) were detected in the report.")

    st.markdown("###")

    # 3. Retrieved Similar Issues
    st.subheader("🔍 Top Retrieved Similar Issues")
    similar_issues = result.get("similar_issues", [])

    if similar_issues:
        st.caption("Historical issues retrieved via ChromaDB cosine similarity & GraphSAGE cold-start embeddings:")
        for idx, item in enumerate(similar_issues, 1):
            issue_id = item.get("issue_id", "N/A")
            issue_title = item.get("title", "Untitled Issue")
            issue_label = item.get("label", "unassigned")
            github_url = f"https://github.com/kubernetes/kubernetes/issues/{issue_id}"

            st.markdown(
                f"""
                <div class='issue-card'>
                    <strong>#{idx}. <a href='{github_url}' target='_blank' style='text-decoration:none;'>#{issue_id} {issue_title}</a></strong><br/>
                    <span style='color: #4b6584; font-size: 0.9rem;'>SIG Label: <code>{issue_label}</code></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No prior similar issues were retrieved for this report.")

    st.markdown("###")

    # 4. Drafted Triage Comment for Maintainer Review
    st.subheader("✍️ Maintainer Review & Approval")
    st.caption("Review and edit the agent's drafted comment before approving and posting to GitHub.")

    draft_comment = result.get("draft_comment", "")

    edited_comment = st.text_area(
        "Draft Triage Comment",
        value=draft_comment,
        height=220,
        help="You can edit this comment directly before confirming.",
    )

    btn_approve, btn_copy = st.columns([1, 1])

    with btn_approve:
        if st.button("✅ Approve & Post Comment", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Triage approved! The comment is ready to be submitted to GitHub.")

    with btn_copy:
        if st.button("📋 Copy Comment to Clipboard", use_container_width=True):
            st.info("💡 You can select and copy the edited comment above!")
