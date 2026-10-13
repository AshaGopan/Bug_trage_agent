import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import os

os.makedirs('report_assets/diagrams', exist_ok=True)

# Common styling constants
BG_COLOR = '#FFFFFF'
BOX_BG = '#F1F5F9'
BOX_BORDER = '#334155'
PRIMARY_COLOR = '#1E3A8A'
ACCENT_COLOR = '#2563EB'
LIGHT_ACCENT = '#DBEAFE'
TEXT_COLOR = '#0F172A'
FONT_FAMILY = 'sans-serif'

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def draw_fancy_box(ax, x, y, w, h, text, title='', bg='#EFF6FF', border='#2563EB', text_color='#1E293B', title_color='#1E3A8A', fs=9, radius=0.03):
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}", fc=bg, ec=border, lw=1.5, zorder=2)
    ax.add_patch(box)
    if title:
        ax.text(x + w/2, y + h - 0.04, title, ha='center', va='top', fontsize=fs+1, fontweight='bold', color=title_color, zorder=3)
        ax.text(x + w/2, y + (h - 0.05)/2, text, ha='center', va='center', fontsize=fs, color=text_color, zorder=3, multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, color=text_color, zorder=3, multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, label='', label_pos=0.5, color='#475569', lw=1.5, fs=8, offset=(0, 0.02)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12, shrinkA=3, shrinkB=3),
                zorder=4)
    if label:
        lx = x1 + (x2 - x1) * label_pos + offset[0]
        ly = y1 + (y2 - y1) * label_pos + offset[1]
        ax.text(lx, ly, label, ha='center', va='bottom', fontsize=fs, color='#334155', fontweight='semibold',
                bbox=dict(boxstyle="round,pad=0.2", fc='#FFFFFF', ec='none', alpha=0.85), zorder=5)

# ==============================================================================
# Figure 5.1: Context Diagram
# ==============================================================================
def make_context_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Central System
    draw_fancy_box(ax, 3.6, 2.3, 2.8, 1.9, "Bug Triage AI\nSystem\n(Multi-Modal LangGraph Core)",
                   title="0.0 CENTRAL SYSTEM", bg='#EFF6FF', border='#1D4ED8', text_color='#1E3A8A', fs=10, radius=0.04)

    # External Entities
    # Left: Maintainer / Contributor
    draw_fancy_box(ax, 0.4, 2.5, 2.2, 1.5, "GitHub Maintainer /\nContributor\n(Browser Workspace)",
                   title="ENTITY 1", bg='#F8FAFC', border='#475569', fs=9)
    
    # Top: GitHub REST API
    draw_fancy_box(ax, 3.8, 4.8, 2.4, 1.3, "GitHub REST API\n(kubernetes/kubernetes)",
                   title="ENTITY 2", bg='#F8FAFC', border='#475569', fs=9)
    
    # Right Top: SQLite Database
    draw_fancy_box(ax, 7.3, 4.2, 2.3, 1.4, "SQLite Database\n(triage.db - Issues, Edges,\nPR Files, Vectors)",
                   title="DATA STORE 1", bg='#ECFDF5', border='#059669', fs=8.5)
    
    # Right Bottom: ChromaDB Vector Store
    draw_fancy_box(ax, 7.3, 2.1, 2.3, 1.4, "ChromaDB Vector Store\n(384d Dense Embeddings\nK=5 Semantic Search)",
                   title="DATA STORE 2", bg='#FEF3C7', border='#D97706', fs=8.5)
    
    # Bottom: Machine Learning Models & LLM Engine
    draw_fancy_box(ax, 3.5, 0.3, 3.0, 1.4, "ML Models & LLM Engine\n(GraphSAGE, LightGBM,\nGemini / LLM Synthesizer)",
                   title="AI INFERENCE ENGINES", bg='#F5F3FF', border='#7C3AED', fs=8.5)

    # Arrows with flows
    # Maintainer <-> System
    draw_arrow(ax, 2.6, 3.5, 3.6, 3.5, "Bug Report (Title, Body)", 0.5, offset=(0, 0.04))
    draw_arrow(ax, 3.6, 3.0, 2.6, 3.0, "SIG, Draft Comment, History", 0.5, offset=(0, -0.07))

    # GitHub API <-> System
    draw_arrow(ax, 4.6, 4.8, 4.6, 4.2, "Raw Issues, PRs, Comments", 0.5, offset=(-0.25, 0))
    draw_arrow(ax, 5.4, 4.2, 5.4, 4.8, "Label Assignment (/sig)", 0.5, offset=(0.25, 0))

    # System <-> SQLite
    draw_arrow(ax, 6.4, 3.7, 7.3, 4.5, "Read Issues & Edges", 0.5, offset=(-0.15, 0.05))
    draw_arrow(ax, 7.3, 4.2, 6.4, 3.4, "Persist Splits & Vectors", 0.5, offset=(0.15, -0.05))

    # System <-> ChromaDB
    draw_arrow(ax, 6.4, 2.8, 7.3, 2.8, "Query Top-K Similar", 0.5, offset=(0, 0.04))
    draw_arrow(ax, 7.3, 2.5, 6.4, 2.5, "Cosine Nearest Neighbors", 0.5, offset=(0, -0.07))

    # System <-> ML/LLM
    draw_arrow(ax, 4.7, 2.3, 4.7, 1.7, "Features Vector (519d)", 0.5, offset=(-0.25, 0))
    draw_arrow(ax, 5.3, 1.7, 5.3, 2.3, "Class Preds & Draft Text", 0.5, offset=(0.25, 0))

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_1_context.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.1 Context Diagram")

# ==============================================================================
# Figure 5.2: Use Case Diagram
# ==============================================================================
def make_usecase_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Boundary Box
    rect = patches.Rectangle((2.3, 0.3), 5.4, 7.4, linewidth=2, edgecolor='#1E3A8A', facecolor='#F8FAFC', zorder=1)
    ax.add_patch(rect)
    ax.text(5.0, 7.45, "Bug Triage AI System Boundary", ha='center', va='center', fontsize=12, fontweight='bold', color='#1E3A8A', zorder=2)

    # Actor Left: Maintainer / Contributor
    ax.plot([0.9, 0.9], [4.6, 5.2], color='#0F172A', lw=2.5, zorder=3) # body
    ax.plot([0.5, 1.3], [4.9, 4.9], color='#0F172A', lw=2.5, zorder=3) # arms
    ax.plot([0.9, 0.6], [4.6, 4.0], color='#0F172A', lw=2.5, zorder=3) # left leg
    ax.plot([0.9, 1.2], [4.6, 4.0], color='#0F172A', lw=2.5, zorder=3) # right leg
    circle = patches.Circle((0.9, 5.5), 0.3, facecolor='#E2E8F0', edgecolor='#0F172A', lw=2, zorder=3)
    ax.add_patch(circle)
    ax.text(0.9, 3.6, "Open-Source\nMaintainer /\nContributor", ha='center', va='top', fontsize=9, fontweight='bold', color='#0F172A')

    # Actor Right: External Services (GitHub & AI Backends)
    ax.plot([9.1, 9.1], [4.6, 5.2], color='#0F172A', lw=2.5, zorder=3) # body
    ax.plot([8.7, 9.5], [4.9, 4.9], color='#0F172A', lw=2.5, zorder=3) # arms
    ax.plot([9.1, 8.8], [4.6, 4.0], color='#0F172A', lw=2.5, zorder=3) # left leg
    ax.plot([9.1, 9.4], [4.6, 4.0], color='#0F172A', lw=2.5, zorder=3) # right leg
    circle2 = patches.Circle((9.1, 5.5), 0.3, facecolor='#E2E8F0', edgecolor='#0F172A', lw=2, zorder=3)
    ax.add_patch(circle2)
    ax.text(9.1, 3.6, "GitHub API &\nAI Inference\nServices", ha='center', va='top', fontsize=9, fontweight='bold', color='#0F172A')

    # Use Cases (Ellipses)
    use_cases = [
        ("Submit Bug Report / Fetch URL", 6.8, True, True),
        ("Select Rotating SIG Sample Issue", 6.1, True, False),
        ("Audit Diagnostic Completeness", 5.4, True, True),
        ("Query Top-K Semantic Neighbors", 4.7, False, True),
        ("Compute Inductive GraphSAGE Vectors", 4.0, False, True),
        ("Predict Target SIG & Confidence Score", 3.3, True, True),
        ("Review & Toggle Missing Info Checkboxes", 2.6, True, False),
        ("Edit & Copy Suggested Maintainer Draft", 1.9, True, False),
        ("Browse Triage Audit History & Search", 1.2, True, False),
        ("Manage Maintainer Account & Dark/Light Theme", 0.5, True, False),
    ]

    for text, y, link_left, link_right in use_cases:
        ellipse = patches.Ellipse((5.0, y), 4.2, 0.52, facecolor='#EFF6FF', edgecolor='#2563EB', lw=1.5, zorder=2)
        ax.add_patch(ellipse)
        ax.text(5.0, y, text, ha='center', va='center', fontsize=8.5, fontweight='semibold', color='#1E293B', zorder=3)
        if link_left:
            ax.plot([1.25, 2.9], [4.7, y], color='#64748B', lw=1.2, linestyle='-', zorder=2)
        if link_right:
            ax.plot([7.1, 8.75], [y, 4.7], color='#64748B', lw=1.2, linestyle='-', zorder=2)

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_2_usecase.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.2 Use Case Diagram")

# ==============================================================================
# Figure 5.3: Activity Diagram
# ==============================================================================
def make_activity_diagram():
    fig, ax = plt.subplots(figsize=(9, 8.5), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Start Node
    start_c = patches.Circle((4.5, 9.1), 0.18, facecolor='#0F172A', edgecolor='#0F172A', zorder=3)
    ax.add_patch(start_c)
    ax.text(4.5, 9.4, "Start Triage Session", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    draw_arrow(ax, 4.5, 8.92, 4.5, 8.45)

    # 1. Input Box
    draw_fancy_box(ax, 2.2, 7.8, 4.6, 0.65, "Submit GitHub Issue Title & Markdown Body\n(or Fetch Live via REST URL)", fs=8.5)
    draw_arrow(ax, 4.5, 7.8, 4.5, 7.3)

    # 2. Intake Node
    draw_fancy_box(ax, 2.2, 6.65, 4.6, 0.65, "Intake Node: Clean Markdown, Strip Boilerplate &\nTemplates (features/clean_text.py)", fs=8.5)
    draw_arrow(ax, 4.5, 6.65, 4.5, 6.15)

    # 3. Missing Info Node
    draw_fancy_box(ax, 2.2, 5.5, 4.6, 0.65, "Missing Info Node: Audit Reproduction Steps,\nEnvironment Details & Log Snippets", fs=8.5)
    draw_arrow(ax, 4.5, 5.5, 4.5, 5.0)

    # 4. Cold-Start Node
    draw_fancy_box(ax, 1.8, 4.25, 5.4, 0.75, "Cold-Start Node: Compute MiniLM Text Embedding (384d),\nQuery ChromaDB Top-5, Form Dynamic Subgraph &\nCompute GraphSAGE Inductive Vectors (128d)", fs=8.5)
    draw_arrow(ax, 4.5, 4.25, 4.5, 3.75)

    # 5. Classifier Node
    draw_fancy_box(ax, 2.0, 3.0, 5.0, 0.75, "Classifier Node: Multi-Modal Concatenation\n[v_text (384d) || v_graph (128d) || v_label (7d)] (519d)\nLightGBM GBDT Multi-Class Inference", fs=8.5)
    draw_arrow(ax, 4.5, 3.0, 4.5, 2.45)

    # Decision Diamond
    diamond = patches.Polygon([[4.5, 2.4], [5.6, 1.95], [4.5, 1.5], [3.4, 1.95]],
                              closed=True, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.5, zorder=3)
    ax.add_patch(diamond)
    ax.text(4.5, 1.95, "Confidence\n>= 60%?", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400E', zorder=4)

    # High Branch (Left)
    draw_arrow(ax, 3.4, 1.95, 1.8, 1.95, "Yes (>=60%)", 0.5, offset=(0, 0.08))
    draw_arrow(ax, 1.8, 1.95, 1.8, 1.25)
    draw_fancy_box(ax, 0.4, 0.55, 2.8, 0.7, "Writer High Node:\nSuggest /sig Label,\nCite Similar Issues, Format Missing Info", fs=7.5, bg='#ECFDF5', border='#059669')

    # Low Branch (Right)
    draw_arrow(ax, 5.6, 1.95, 7.2, 1.95, "No (<60%)", 0.5, offset=(0, 0.08))
    draw_arrow(ax, 7.2, 1.95, 7.2, 1.25)
    draw_fancy_box(ax, 5.8, 0.55, 2.8, 0.7, "Writer Low Node:\nRequest Clarifications\nWithout Automated SIG Assignment", fs=7.5, bg='#FEF2F2', border='#DC2626')

    # Merge to end
    draw_arrow(ax, 1.8, 0.55, 1.8, 0.25)
    draw_arrow(ax, 7.2, 0.55, 7.2, 0.25)
    ax.plot([1.8, 7.2], [0.25, 0.25], color='#475569', lw=1.5)
    draw_arrow(ax, 4.5, 0.25, 4.5, 0.08)

    # Final Node
    final_out = patches.Circle((4.5, -0.06), 0.16, facecolor='none', edgecolor='#0F172A', lw=1.5, zorder=3)
    final_in = patches.Circle((4.5, -0.06), 0.10, facecolor='#0F172A', edgecolor='#0F172A', zorder=4)
    ax.add_patch(final_out)
    ax.add_patch(final_in)

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_3_activity.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.3 Activity Diagram")

# ==============================================================================
# Figure 5.4: State Diagram
# ==============================================================================
def make_state_diagram():
    fig, ax = plt.subplots(figsize=(9.5, 7.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Start Node
    ax.add_patch(patches.Circle((1.0, 5.8), 0.15, facecolor='#0F172A', edgecolor='#0F172A', zorder=3))
    draw_arrow(ax, 1.15, 5.8, 2.0, 5.8)

    # State 1: IDLE / WAITING
    draw_fancy_box(ax, 2.0, 5.2, 2.4, 1.2, "Maintainer Dashboard Ready;\nRotating Sample Issues Loaded",
                   title="1. IDLE / WAITING", fs=8.5)

    # State 2: INTAKE & PREPROCESSING
    draw_fancy_box(ax, 5.8, 5.2, 2.6, 1.2, "Clean Markdown, Remove\nHTML & Template Boilerplate",
                   title="2. INTAKE & PREPROCESS", fs=8.5)
    draw_arrow(ax, 4.4, 5.8, 5.8, 5.8, "Issue Submitted / URL Fetched", offset=(0, 0.06))

    # State 3: DIAGNOSTIC AUDITING
    draw_fancy_box(ax, 5.8, 3.2, 2.6, 1.2, "Verify Steps to Reproduce,\nLogs, Environment Specs",
                   title="3. DIAGNOSTIC AUDIT", fs=8.5)
    draw_arrow(ax, 7.1, 5.2, 7.1, 4.4, "Text Sanitized", offset=(0.18, 0))

    # State 4: GRAPH COLD-START & EMBEDDING
    draw_fancy_box(ax, 2.0, 3.2, 2.6, 1.2, "MiniLM 384d, ChromaDB K=5,\nInductive GraphSAGE 128d",
                   title="4. TOPOLOGICAL INFERENCE", fs=8.5)
    draw_arrow(ax, 5.8, 3.8, 4.6, 3.8, "Missing Info Checked", offset=(0, 0.06))

    # State 5: MULTI-MODAL CLASSIFICATION
    draw_fancy_box(ax, 2.0, 1.2, 2.6, 1.2, "Concatenate 519d Features;\nLightGBM Predicts SIG & Conf",
                   title="5. CLASSIFICATION", fs=8.5)
    draw_arrow(ax, 3.3, 3.2, 3.3, 2.4, "Features Assembled", offset=(-0.25, 0))

    # Branch 6A: HIGH CONFIDENCE TRIAGED
    draw_fancy_box(ax, 5.8, 1.7, 2.6, 1.0, "Auto-assign /sig Label;\nDraft Maintainer Response",
                   title="6A. TRIAGED (>=60%)", fs=8, bg='#ECFDF5', border='#059669')
    draw_arrow(ax, 4.6, 2.0, 5.8, 2.1, "Confidence >= 60%", offset=(0, 0.06))

    # Branch 6B: LOW CONFIDENCE CLARIFICATION
    draw_fancy_box(ax, 5.8, 0.4, 2.6, 1.0, "Draft Clarification Request;\nNo Automated SIG Assignment",
                   title="6B. NEEDS INFO (<60%)", fs=8, bg='#FEF2F2', border='#DC2626')
    draw_arrow(ax, 4.6, 1.5, 5.8, 0.8, "Confidence < 60%", offset=(0, -0.08))

    # Final Node (Dispatched / Saved)
    ax.add_patch(patches.Circle((9.2, 1.4), 0.16, facecolor='none', edgecolor='#0F172A', lw=1.5, zorder=3))
    ax.add_patch(patches.Circle((9.2, 1.4), 0.10, facecolor='#0F172A', edgecolor='#0F172A', zorder=4))
    ax.text(9.2, 1.8, "Dispatched /\nArchived", ha='center', va='center', fontsize=8, fontweight='bold')
    draw_arrow(ax, 8.4, 2.1, 9.04, 1.45)
    draw_arrow(ax, 8.4, 0.8, 9.04, 1.35)

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_4_state.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.4 State Diagram")

# ==============================================================================
# Figure 5.5: Sequence Diagram
# ==============================================================================
def make_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 8.0)
    ax.axis('off')

    lifelines = [
        ("Maintainer UI", 1.0),
        ("FastAPI /triage", 2.6),
        ("LangGraph Core", 4.2),
        ("ChromaDB Index", 5.8),
        ("GraphSAGE Engine", 7.4),
        ("LightGBM Model", 9.0),
    ]

    for name, x in lifelines:
        draw_fancy_box(ax, x - 0.7, 7.3, 1.4, 0.55, name, fs=8, bg='#EFF6FF', border='#2563EB')
        ax.plot([x, x], [0.6, 7.3], color='#94A3B8', linestyle='--', lw=1.2, zorder=1)

    steps = [
        (1.0, 2.6, 6.7, "1: POST /triage {title, body}", '#2563EB'),
        (2.6, 4.2, 6.2, "2: invoke(initial_state)", '#2563EB'),
        (4.2, 4.2, 5.7, "3: intake_node & clean_text()", '#475569', True),
        (4.2, 4.2, 5.2, "4: missing_info_node audit", '#475569', True),
        (4.2, 5.8, 4.7, "5: query_similar(dense_emb, k=5)", '#2563EB'),
        (5.8, 4.2, 4.3, "6: return top-5 similar issues", '#059669', False, '--'),
        (4.2, 7.4, 3.8, "7: compute_cold_start(subgraph)", '#2563EB'),
        (7.4, 4.2, 3.4, "8: return graph_embedding (128d)", '#059669', False, '--'),
        (4.2, 9.0, 2.9, "9: predict_proba(519d features)", '#2563EB'),
        (9.0, 4.2, 2.5, "10: predicted_sig, confidence", '#059669', False, '--'),
        (4.2, 4.2, 2.0, "11: writer_node(draft_comment)", '#475569', True),
        (4.2, 2.6, 1.5, "12: return final_state", '#059669', False, '--'),
        (2.6, 1.0, 1.0, "13: 200 OK (TriageResponse JSON)", '#059669', False, '--'),
    ]

    for item in steps:
        if len(item) == 5:
            x1, x2, y, label, color = item
            is_self = False
            style = '-'
        else:
            x1, x2, y, label, color, is_self = item[:6]
            style = item[6] if len(item) > 6 else '-'

        if is_self:
            # Self call loop
            ax.plot([x1, x1 + 0.35, x1 + 0.35, x1], [y, y, y - 0.25, y - 0.25], color=color, lw=1.3)
            ax.annotate('', xy=(x1, y - 0.25), xytext=(x1 + 0.1, y - 0.25),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=10))
            ax.text(x1 + 0.4, y - 0.12, label, ha='left', va='center', fontsize=7.5, color='#334155', fontweight='semibold')
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, linestyle=style, mutation_scale=10))
            ax.text((x1 + x2)/2, y + 0.08, label, ha='center', va='bottom', fontsize=7.5, color='#334155', fontweight='semibold')

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_5_sequence.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.5 Sequence Diagram")

# ==============================================================================
# Figure 5.6: Data Flow Diagram (DFD Level 1)
# ==============================================================================
def make_dfd_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # External Entities
    draw_fancy_box(ax, 0.4, 4.6, 1.8, 1.2, "Maintainer /\nContributor", title="ENTITY", bg='#F8FAFC', border='#475569', fs=8.5)
    draw_fancy_box(ax, 7.8, 4.6, 1.8, 1.2, "GitHub Cloud\nRepository", title="ENTITY", bg='#F8FAFC', border='#475569', fs=8.5)

    # Processes (Circles or Rounded Boxes)
    draw_fancy_box(ax, 2.9, 4.8, 1.8, 1.1, "1.0 Ingest &\nClean Text", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)
    draw_fancy_box(ax, 5.3, 4.8, 1.8, 1.1, "2.0 Diagnostic\nCompleteness Audit", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)
    draw_fancy_box(ax, 2.9, 2.7, 1.8, 1.1, "3.0 Cold-Start\nGraph & Retrieval", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)
    draw_fancy_box(ax, 5.3, 2.7, 1.8, 1.1, "4.0 Hybrid LightGBM\nClassification", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)
    draw_fancy_box(ax, 2.9, 0.6, 1.8, 1.1, "5.0 Generate Draft\nResponse Comment", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)
    draw_fancy_box(ax, 5.3, 0.6, 1.8, 1.1, "6.0 Audit Logging\n& History Store", title="PROCESS", bg='#EFF6FF', border='#2563EB', fs=8, radius=0.04)

    # Data Stores
    draw_fancy_box(ax, 0.4, 2.7, 1.8, 1.1, "D1: triage.db\n(Issues, Edges, PRs)", title="DATA STORE", bg='#ECFDF5', border='#059669', fs=7.5)
    draw_fancy_box(ax, 7.8, 2.7, 1.8, 1.1, "D2: ChromaDB\n(Dense Index)", title="DATA STORE", bg='#FEF3C7', border='#D97706', fs=7.5)
    draw_fancy_box(ax, 7.8, 0.6, 1.8, 1.1, "D3: Model Weights\n(LGBM + GNN)", title="DATA STORE", bg='#F5F3FF', border='#7C3AED', fs=7.5)

    # Connecting Arrows
    draw_arrow(ax, 2.2, 5.3, 2.9, 5.3, "Issue Text", offset=(0, 0.05))
    draw_arrow(ax, 4.7, 5.3, 5.3, 5.3, "Clean Text", offset=(0, 0.05))
    draw_arrow(ax, 6.2, 4.8, 3.8, 3.8, "Audit Flags", offset=(-0.1, 0.05))
    draw_arrow(ax, 2.9, 3.2, 2.2, 3.2, "Read Edges", offset=(0, 0.05))
    draw_arrow(ax, 4.7, 3.2, 5.3, 3.2, "Features (519d)", offset=(0, 0.05))
    draw_arrow(ax, 7.1, 3.2, 7.8, 3.2, "Query K=5", offset=(0, 0.05))
    draw_arrow(ax, 6.2, 2.7, 6.2, 1.7, "Predictions", offset=(0.2, 0))
    draw_arrow(ax, 4.7, 1.1, 5.3, 1.1, "Draft Text", offset=(0, 0.05))
    draw_arrow(ax, 2.9, 1.1, 1.3, 4.6, "Triage Output", offset=(-0.25, -0.2))
    draw_arrow(ax, 7.1, 1.1, 7.8, 1.1, "Weights", offset=(0, 0.05))

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_6_dfd.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.6 Data Flow Diagram")

# ==============================================================================
# Figure 5.7: ER Diagram
# ==============================================================================
def make_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Entity 1: ISSUES
    issues_text = "+ issue_id : INTEGER [PK]\n  title : TEXT\n  body_clean : TEXT\n  created_at : TEXT\n  state : TEXT\n  label : TEXT\n  linked_pr_ids : TEXT\n  split : TEXT (train/val/test)"
    draw_fancy_box(ax, 0.5, 3.5, 2.8, 2.6, issues_text, title="ISSUES", bg='#EFF6FF', border='#1D4ED8', fs=8, radius=0.03)

    # Entity 2: EDGES
    edges_text = "+ id : INTEGER [PK]\n  src_issue : INTEGER [FK]\n  dst_issue : INTEGER [FK]\n  edge_type : TEXT"
    draw_fancy_box(ax, 4.2, 4.3, 2.6, 1.8, edges_text, title="EDGES", bg='#ECFDF5', border='#059669', fs=8, radius=0.03)

    # Entity 3: PR_FILES
    pr_text = "+ id : INTEGER [PK]\n  pr_id : INTEGER\n  file_path : TEXT"
    draw_fancy_box(ax, 4.2, 2.0, 2.6, 1.6, pr_text, title="PR_FILES", bg='#FEF3C7', border='#D97706', fs=8, radius=0.03)

    # Entity 4: EMBEDDINGS
    emb_text = "+ issue_id : INTEGER [PK, FK]\n  text_vec : BLOB (384d)\n  graph_vec : BLOB (128d)\n  label_aware_vec : BLOB (7d)"
    draw_fancy_box(ax, 0.5, 0.4, 2.8, 2.2, emb_text, title="EMBEDDINGS", bg='#F5F3FF', border='#7C3AED', fs=8, radius=0.03)

    # Entity 5: TRIAGE_HISTORY (Frontend / LocalStorage)
    hist_text = "+ id : TEXT [PK]\n  title : TEXT\n  repository : TEXT\n  suggestedTeam : TEXT\n  confidence : REAL\n  status : TEXT\n  dateAnalyzed : TEXT\n  whyThisTeam : TEXT\n  suggestedResponse : TEXT"
    draw_fancy_box(ax, 7.3, 1.5, 2.5, 3.8, hist_text, title="TRIAGE_HISTORY", bg='#F8FAFC', border='#475569', fs=7.5, radius=0.03)

    # Relationships
    # ISSUES -> EDGES (1 to N)
    ax.plot([3.3, 4.2], [4.9, 4.9], color='#1E3A8A', lw=2)
    ax.text(3.4, 5.0, "1", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(4.0, 5.0, "N", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(3.75, 5.15, "connects", fontsize=7.5, color='#475569', ha='center')

    # ISSUES -> PR_FILES (1 to N)
    ax.plot([3.3, 4.2], [3.8, 2.8], color='#1E3A8A', lw=2)
    ax.text(3.4, 3.6, "1", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(4.0, 2.7, "N", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(3.7, 3.3, "modifies", fontsize=7.5, color='#475569', ha='center')

    # ISSUES -> EMBEDDINGS (1 to 1)
    ax.plot([1.9, 1.9], [3.5, 2.6], color='#1E3A8A', lw=2)
    ax.text(2.0, 3.3, "1", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(2.0, 2.7, "1", fontsize=9, fontweight='bold', color='#1E3A8A')
    ax.text(2.3, 3.0, "generates", fontsize=7.5, color='#475569', ha='center')

    # ISSUES -> TRIAGE_HISTORY (1 to N conceptual)
    ax.plot([6.8, 7.3], [3.4, 3.4], color='#64748B', lw=1.5, linestyle=':')
    ax.text(7.05, 3.55, "audits", fontsize=7.5, color='#475569', ha='center')

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_7_er.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.7 ER Diagram")

# ==============================================================================
# Figure 5.8: Class Diagram
# ==============================================================================
def make_class_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 8.0)
    ax.axis('off')

    # Class 1: TriageState
    triage_state_text = "+ title : str\n+ body : str\n+ clean_title : str\n+ clean_body : str\n+ missing_fields : list[str]\n+ query_embedding : list[float]\n+ similar_issues : list[dict]\n+ graph_embedding : list[float]\n+ label_aware_vec : list[float]\n+ predicted_label : str\n+ confidence : float\n+ draft_comment : str"
    draw_fancy_box(ax, 0.4, 3.8, 2.7, 3.8, triage_state_text, title="«TypedDict»\nTriageState", bg='#EFF6FF', border='#2563EB', fs=7.5)

    # Class 2: TriageWorkflow (LangGraph)
    workflow_text = "- graph : StateGraph\n- compiled_app : CompiledGraph\n+ __init__()\n+ build_graph() : StateGraph\n+ route_confidence(state) : str\n+ run(title, body) : dict"
    draw_fancy_box(ax, 3.6, 5.0, 3.0, 2.6, workflow_text, title="TriageWorkflow", bg='#F8FAFC', border='#1E3A8A', fs=7.5)

    # Class 3: IntakeService
    intake_text = "+ clean_markdown(text: str) : str\n+ strip_boilerplate(body: str) : str\n+ extract_keywords(text: str) : list"
    draw_fancy_box(ax, 7.1, 5.4, 3.0, 2.2, intake_text, title="IntakeService", bg='#F8FAFC', border='#475569', fs=7.5)

    # Class 4: GraphSAGENet
    gnn_text = "- conv1 : SAGEConv(384, 128)\n- conv2 : SAGEConv(128, 128)\n+ forward(x, edge_index) : Tensor\n+ compute_cold_start(subgraph) : Tensor"
    draw_fancy_box(ax, 3.6, 2.5, 3.0, 2.1, gnn_text, title="«nn.Module»\nGraphSAGENet", bg='#ECFDF5', border='#059669', fs=7.5)

    # Class 5: HybridClassifier
    clf_text = "- model : LGBMClassifier\n- label_encoder : LabelEncoder\n+ load(model_path: str)\n+ predict_proba(X: Tensor) : ndarray\n+ format_recommendation() : dict"
    draw_fancy_box(ax, 7.1, 2.5, 3.0, 2.1, clf_text, title="HybridClassifier", bg='#FEF3C7', border='#D97706', fs=7.5)

    # Class 6: FastAPIServer
    api_text = "+ app : FastAPI\n+ post_triage(req: TriageRequest) : TriageResponse\n+ health_check() : dict"
    draw_fancy_box(ax, 0.4, 0.5, 2.7, 2.4, api_text, title="FastAPIServer", bg='#F5F3FF', border='#7C3AED', fs=7.5)

    # Class 7: ReactFrontendController
    react_text = "- state : ReactState\n+ handleStartAnalysis(input)\n+ handleToggleMissingInfo(field)\n+ handleCopyResponse()\n+ toggleTheme()"
    draw_fancy_box(ax, 3.6, 0.4, 3.0, 1.8, react_text, title="ReactFrontendController", bg='#F8FAFC', border='#475569', fs=7.5)

    # Class 8: VectorStore
    vec_text = "- client : PersistentClient\n- collection : Collection\n+ query_similar(vec, k=5) : list\n+ add_documents(texts, metas)"
    draw_fancy_box(ax, 7.1, 0.4, 3.0, 1.8, vec_text, title="VectorStore", bg='#EFF6FF', border='#2563EB', fs=7.5)

    # Relationships
    ax.plot([3.1, 3.6], [6.0, 6.0], color='#1E3A8A', lw=1.5) # State -> Workflow
    ax.plot([6.6, 7.1], [6.0, 6.0], color='#1E3A8A', lw=1.5) # Workflow -> Intake
    ax.plot([5.1, 5.1], [5.0, 4.6], color='#1E3A8A', lw=1.5) # Workflow -> GNN
    ax.plot([6.6, 7.1], [3.5, 3.5], color='#1E3A8A', lw=1.5) # GNN -> Classifier
    ax.plot([1.7, 1.7], [3.8, 2.9], color='#1E3A8A', lw=1.5) # State -> API
    ax.plot([3.1, 3.6], [1.3, 1.3], color='#1E3A8A', lw=1.5) # API -> React
    ax.plot([6.6, 7.1], [1.3, 1.3], color='#1E3A8A', lw=1.5) # React -> VectorStore

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_8_class.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.8 Class Diagram")

# ==============================================================================
# Figure 5.9: ML Workflow Diagram
# ==============================================================================
def make_ml_workflow_diagram():
    fig, ax = plt.subplots(figsize=(9.5, 8.5), dpi=300)
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Start Node
    ax.add_patch(patches.Circle((4.75, 9.1), 0.16, facecolor='#0F172A', edgecolor='#0F172A', zorder=3))
    ax.text(4.75, 9.38, "GitHub Data Collection (kubernetes/kubernetes)", ha='center', va='center', fontsize=9, fontweight='bold')
    draw_arrow(ax, 4.75, 8.94, 4.75, 8.4)

    # Step 1: Temporal Splitting
    draw_fancy_box(ax, 2.0, 7.7, 5.5, 0.7, "Strict Temporal Split (Zero Data Leakage):\nTrain (<= T_train) | Val (<= T_val) | Test (> T_val)", fs=8.5)
    draw_arrow(ax, 4.75, 7.7, 4.75, 7.15)

    # Step 2: Text Preprocessing
    draw_fancy_box(ax, 2.0, 6.45, 5.5, 0.7, "Text Preprocessing & Markdown Sanitization:\nRegex Cleansing, Template Stripping, Token Normalization", fs=8.5)
    draw_arrow(ax, 4.75, 6.45, 4.75, 5.9)

    # Step 3: Multi-Modal Feature Extraction
    draw_fancy_box(ax, 0.4, 4.7, 2.6, 1.2, "Modality A:\nDense Semantic\nall-MiniLM-L6-v2\n(384 dimensions)", title="TEXT DENSE", bg='#EFF6FF', border='#2563EB', fs=8)
    draw_fancy_box(ax, 3.45, 4.7, 2.6, 1.2, "Modality B:\nInductive GraphSAGE\n2-Layer PyTorch GNN\n(128 dimensions)", title="GRAPH SAGE", bg='#ECFDF5', border='#059669', fs=8)
    draw_fancy_box(ax, 6.5, 4.7, 2.6, 1.2, "Modality C:\nTraining-Neighbor\nLabel Awareness Prior\n(7 dimensions)", title="LABEL AWARE", bg='#FEF3C7', border='#D97706', fs=8)

    draw_arrow(ax, 4.75, 5.9, 1.7, 5.9)
    draw_arrow(ax, 1.7, 5.9, 1.7, 5.9 - 0.0) # line
    draw_arrow(ax, 4.75, 5.9, 4.75, 5.9)
    draw_arrow(ax, 4.75, 5.9, 7.8, 5.9)
    draw_arrow(ax, 1.7, 5.9, 1.7, 5.25)
    draw_arrow(ax, 4.75, 5.9, 4.75, 5.25)
    draw_arrow(ax, 7.8, 5.9, 7.8, 5.25)

    # Merge Arrows
    draw_arrow(ax, 1.7, 4.7, 3.5, 3.8)
    draw_arrow(ax, 4.75, 4.7, 4.75, 3.8)
    draw_arrow(ax, 7.8, 4.7, 6.0, 3.8)

    # Step 4: Multi-Modal Fusion
    draw_fancy_box(ax, 2.0, 3.1, 5.5, 0.7, "Multi-Modal Feature Concatenation:\nx = [v_text || v_graph || v_label] (519 dimensions)", fs=8.5, bg='#F5F3FF', border='#7C3AED')
    draw_arrow(ax, 4.75, 3.1, 4.75, 2.5)

    # Step 5: LightGBM Multi-Class Training
    draw_fancy_box(ax, 2.0, 1.8, 5.5, 0.7, "LightGBM Gradient Boosted Decision Tree Training\nHyperparameter Optimization & Early Stopping on Validation Split", fs=8.5)
    draw_arrow(ax, 4.75, 1.8, 4.75, 1.2)

    # Step 6: Evaluation & Export
    draw_fancy_box(ax, 1.8, 0.5, 5.9, 0.7, "Chronological Test Evaluation (Macro-F1: 0.7485) &\nModel Serialization (hybrid_model.joblib, graphsage.pt, ChromaDB)", fs=8.5, bg='#ECFDF5', border='#059669')
    draw_arrow(ax, 4.75, 0.5, 4.75, 0.18)

    # Final Node
    ax.add_patch(patches.Circle((4.75, 0.05), 0.14, facecolor='none', edgecolor='#0F172A', lw=1.5, zorder=3))
    ax.add_patch(patches.Circle((4.75, 0.05), 0.08, facecolor='#0F172A', edgecolor='#0F172A', zorder=4))

    plt.tight_layout()
    plt.savefig('report_assets/diagrams/diagram_5_9_ml_workflow.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated 5.9 ML Workflow Diagram")

if __name__ == '__main__':
    make_context_diagram()
    make_usecase_diagram()
    make_activity_diagram()
    make_state_diagram()
    make_sequence_diagram()
    make_dfd_diagram()
    make_er_diagram()
    make_class_diagram()
    make_ml_workflow_diagram()
    print("All 9 diagrams generated successfully!")
