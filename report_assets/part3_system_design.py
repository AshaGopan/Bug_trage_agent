"""Part 3: Chapter 5 (System Design, pp. 17-31).
Physical Pages 25 to 39 (15 pages).
Features all 9 UML diagrams embedded as publication-quality figures,
database schemas, dataset designs, and UI design specifications.
"""

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch

def build_part3(styles):
    story = []

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 17 / Physical Page 25)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 5 - SYSTEM DESIGN</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>5.1 System Architecture / Overall Workflow</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    p_arch1 = (
        "The Bug Triage AI system is engineered according to a modular, decoupled <b>Three-Tier Enterprise Architecture</b> "
        "comprising the Presentation Layer (Frontend Workspace), the Application Layer (FastAPI REST Service & LangGraph "
        "Orchestrator), and the Data Layer (Relational SQLite, Vector ChromaDB, and Serialized Model Stores). This separation "
        "of concerns guarantees high scalability, low coupling, and rigorous data integrity."
    )
    story.append(Paragraph(p_arch1, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Presentation Layer (Maintainer Frontend Workspace):</b>", styles['SubSectionHeader']))
    p_ui = (
        "Built using React 18, Vite 5, and Tailwind CSS 3, the frontend provides an interactive, responsive user experience "
        "tailored for open-source maintainers. It features a curated SaaS design system supporting persistent Light Mode "
        "(<code>#F8F9FC</code>) and Dark Mode (<code>#0B0F19</code>) themes, an issue intake dashboard with live GitHub URL "
        "fetching, a split-view session explorer, an automated response editor, and persistent local history auditing."
    )
    story.append(Paragraph(p_ui, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Application Layer (Service & Agentic Inference Core):</b>", styles['SubSectionHeader']))
    p_app = (
        "The backend is driven by FastAPI and Uvicorn, exposing asynchronous REST endpoints validated via strict Pydantic "
        "schemas. Triage requests are processed through a stateful <b>LangGraph Multi-Agent Pipeline</b> that executes "
        "markdown text cleaning, diagnostic completeness checking, dynamic K-NN subgraph projection, multi-modal LightGBM "
        "inference, and confidence-gated response drafting (&ge; 60% threshold)."
    )
    story.append(Paragraph(p_app, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3. Data Layer (Relational, Vector, & Graph Model Stores):</b>", styles['SubSectionHeader']))
    p_data = (
        "The persistence layer utilizes SQLite (<code>data/processed/triage.db</code>) for storing sanitized issue text, "
        "cross-reference edges, PR modified files, and precomputed embedding BLOBs. ChromaDB acts as the dense vector index "
        "for sub-millisecond similarity search over 384-dimensional SentenceTransformer embeddings. Serialized PyTorch "
        "GraphSAGE weights (<code>graphsage.pt</code>) and LightGBM models (<code>hybrid_model.joblib</code>) are loaded "
        "into memory at application startup for instant inference."
    )
    story.append(Paragraph(p_data, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 18 / Physical Page 26) - Figure 5.1
    # =========================================================================
    story.append(Paragraph("<b>5.2 Context Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_ctx = (
        "The Context Diagram (Figure 5.1) defines the external boundaries of the Bug Triage AI system, depicting all "
        "external entities, inbound requests, outbound responses, and external data store interfaces."
    )
    story.append(Paragraph(p_ctx, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_1 = Image('report_assets/diagrams/diagram_5_1_context.png', width=5.6*inch, height=3.6*inch)
        story.append(img_5_1)
    except Exception:
        story.append(Spacer(1, 3.5*inch))

    story.append(Paragraph("<b>Figure 5.1 Context Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    p_ctx_desc = (
        "As illustrated above, the central Bug Triage AI core interacts with the Maintainer/Contributor (submitting bug "
        "descriptions and receiving triage recommendations), the GitHub REST API (fetching live issue bodies and posting "
        "maintainer-approved labels), SQLite triage.db (persisting dataset splits and embeddings), ChromaDB (querying top-K "
        "semantic neighbors), and the ML Model Registry (serving GraphSAGE and LightGBM inference)."
    )
    story.append(Paragraph(p_ctx_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 19 / Physical Page 27) - Figure 5.2
    # =========================================================================
    story.append(Paragraph("<b>5.3 Use Case Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_uc = (
        "The Use Case Diagram (Figure 5.2) maps all primary interactions between human maintainers, external service actors, "
        "and the functional capabilities encapsulated within the Bug Triage AI platform."
    )
    story.append(Paragraph(p_uc, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_2 = Image('report_assets/diagrams/diagram_5_2_usecase.png', width=5.6*inch, height=3.9*inch)
        story.append(img_5_2)
    except Exception:
        story.append(Spacer(1, 3.8*inch))

    story.append(Paragraph("<b>Figure 5.2 Use Case Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    p_uc_desc = (
        "The primary actor (Maintainer) executes ten core use cases including manual issue submission, live GitHub issue URL "
        "fetching, rotating sample selection, diagnostic auditing, missing information inspection, and markdown draft response "
        "review. Secondary actors (GitHub REST API and AI Inference Services) satisfy backend retrieval, vector computation, "
        "and classification use cases."
    )
    story.append(Paragraph(p_uc_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 20 / Physical Page 28) - Figure 5.3
    # =========================================================================
    story.append(Paragraph("<b>5.4 Activity Diagram / State Diagram / UML Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    p_act = (
        "The Activity Diagram (Figure 5.3) models the sequential control flow executed across the multi-agent triage pipeline, "
        "from initial bug intake to conditional comment drafting."
    )
    story.append(Paragraph(p_act, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_3 = Image('report_assets/diagrams/diagram_5_3_activity.png', width=5.2*inch, height=4.2*inch)
        story.append(img_5_3)
    except Exception:
        story.append(Spacer(1, 4.0*inch))

    story.append(Paragraph("<b>Figure 5.3 Activity Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_act_desc = (
        "Control flows sequentially from text intake through diagnostic auditing, dense text encoding, ChromaDB vector retrieval, "
        "dynamic subgraph synthesis, GraphSAGE forward pass, and multi-modal concatenation. The decision diamond evaluates "
        "classification confidence: scores &ge; 60% branch to <code>writer_high_node</code>, while low-confidence scores branch "
        "to <code>writer_low_node</code>."
    )
    story.append(Paragraph(p_act_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 21 / Physical Page 29) - Figure 5.4
    # =========================================================================
    story.append(Paragraph("<b>5.4.1 State Diagram</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_st = (
        "The State Diagram (Figure 5.4) details the operational states and event-driven transitions experienced by an issue "
        "entity during an active triage session."
    )
    story.append(Paragraph(p_st, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_4 = Image('report_assets/diagrams/diagram_5_4_state.png', width=5.6*inch, height=3.8*inch)
        story.append(img_5_4)
    except Exception:
        story.append(Spacer(1, 3.8*inch))

    story.append(Paragraph("<b>Figure 5.4 State Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    p_st_desc = (
        "The issue begins in the <b>IDLE / WAITING</b> state. Upon submission, it transitions to <b>INTAKE & SANITIZATION</b>, "
        "advances to <b>DIAGNOSTIC AUDIT</b>, enters <b>TOPOLOGICAL INFERENCE</b> (MiniLM + ChromaDB + GraphSAGE), and "
        "proceeds to <b>CLASSIFICATION</b>. Depending on the LightGBM confidence guard condition, it terminates in either "
        "<b>HIGH CONFIDENCE TRIAGED</b> or <b>LOW CONFIDENCE CLARIFICATION</b>, culminating in the <b>DISPATCHED / ARCHIVED</b> state."
    )
    story.append(Paragraph(p_st_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 22 / Physical Page 30) - Figure 5.5
    # =========================================================================
    story.append(Paragraph("<b>5.4.2 Sequence Diagram</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_seq = (
        "The Sequence Diagram (Figure 5.5) chronicles the chronological message exchanges and synchronous method invocations "
        "orchestrated across system participants during a triage transaction."
    )
    story.append(Paragraph(p_seq, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_5 = Image('report_assets/diagrams/diagram_5_5_sequence.png', width=5.6*inch, height=4.0*inch)
        story.append(img_5_5)
    except Exception:
        story.append(Spacer(1, 4.0*inch))

    story.append(Paragraph("<b>Figure 5.5 Sequence Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_seq_desc = (
        "The Maintainer UI dispatches an asynchronous HTTP POST to <code>/triage</code>. FastAPI invokes the compiled LangGraph "
        "state machine. Internal messages trigger text cleaning, ChromaDB vector querying, GraphSAGE cold-start projection, "
        "and LightGBM prediction. The resulting <code>TriageResponse</code> payload is returned to the client and rendered."
    )
    story.append(Paragraph(p_seq_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 23 / Physical Page 31) - Figure 5.6
    # =========================================================================
    story.append(Paragraph("<b>5.5 Data Flow Diagram / ER Diagram / Class Diagram / ML Workflow</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>5.5.1 Data Flow Diagram (DFD Level 1)</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    p_dfd = (
        "The DFD Level 1 diagram (Figure 5.6) visualizes the structural transformation of data across six core system "
        "processes, showing inbound streams, transformations, and persistence mechanisms."
    )
    story.append(Paragraph(p_dfd, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_6 = Image('report_assets/diagrams/diagram_5_6_dfd.png', width=5.6*inch, height=3.6*inch)
        story.append(img_5_6)
    except Exception:
        story.append(Spacer(1, 3.5*inch))

    story.append(Paragraph("<b>Figure 5.6 Data Flow Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_dfd_desc = (
        "Data transforms through Process 1.0 (Text Ingestion), Process 2.0 (Diagnostic Audit), Process 3.0 (Vector Retrieval), "
        "Process 4.0 (Hybrid Classification), Process 5.0 (Comment Synthesis), and Process 6.0 (Audit Logging), interfacing "
        "with SQLite triage.db (D1), ChromaDB (D2), and Model Weights (D3)."
    )
    story.append(Paragraph(p_dfd_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 24 / Physical Page 32) - Figure 5.7
    # =========================================================================
    story.append(Paragraph("<b>5.5.2 Entity-Relationship (ER) Diagram</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_er = (
        "The Entity-Relationship Diagram (Figure 5.7) models the relational database architecture supporting dataset "
        "partitioning, structural edges, PR file linkages, and precomputed embeddings."
    )
    story.append(Paragraph(p_er, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_7 = Image('report_assets/diagrams/diagram_5_7_er.png', width=5.6*inch, height=3.6*inch)
        story.append(img_5_7)
    except Exception:
        story.append(Spacer(1, 3.5*inch))

    story.append(Paragraph("<b>Figure 5.7 ER Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_er_desc = (
        "The <b>ISSUES</b> entity acts as the primary relational root (1:N with EDGES, 1:N with PR_FILES, and 1:1 with "
        "EMBEDDINGS). The <b>TRIAGE_HISTORY</b> entity captures client-side audit logs, linking suggested SIG assignments "
        "and diagnostic verification states to persistent storage."
    )
    story.append(Paragraph(p_er_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 25 / Physical Page 33) - Figure 5.8
    # =========================================================================
    story.append(Paragraph("<b>5.5.3 Class Diagram</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_cls = (
        "The Class Diagram (Figure 5.8) illustrates the object-oriented structure of the software engineering codebase, "
        "highlighting core classes, state containers, neural modules, and service controllers."
    )
    story.append(Paragraph(p_cls, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_8 = Image('report_assets/diagrams/diagram_5_8_class.png', width=5.6*inch, height=3.9*inch)
        story.append(img_5_8)
    except Exception:
        story.append(Spacer(1, 3.8*inch))

    story.append(Paragraph("<b>Figure 5.8 Class Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_cls_desc = (
        "The <code>TriageState</code> TypedDict serves as the immutable data contract shared across the <code>TriageWorkflow</code>, "
        "<code>IntakeService</code>, <code>GraphSAGENet</code> (PyG nn.Module), <code>HybridClassifier</code> (LightGBM), and "
        "<code>FastAPIServer</code> endpoints, maintaining strict type safety."
    )
    story.append(Paragraph(p_cls_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 26 / Physical Page 34) - Figure 5.9
    # =========================================================================
    story.append(Paragraph("<b>5.5.4 Machine Learning Workflow Diagram</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_mlw = (
        "The ML Workflow Diagram (Figure 5.9) maps the complete offline training and online inference lifecycle, ensuring strict "
        "temporal ordering and multi-modal feature synergy."
    )
    story.append(Paragraph(p_mlw, styles['ReportBody']))
    story.append(Spacer(1, 4))

    try:
        img_5_9 = Image('report_assets/diagrams/diagram_5_9_ml_workflow.png', width=5.4*inch, height=4.2*inch)
        story.append(img_5_9)
    except Exception:
        story.append(Spacer(1, 4.0*inch))

    story.append(Paragraph("<b>Figure 5.9 ML Workflow</b>", styles['FigureCaption']))
    story.append(Spacer(1, 3))
    p_mlw_desc = (
        "The pipeline commences with raw issue scraping, applies strict temporal splitting (max(T_train) &le; min(T_val) &le; "
        "min(T_test)), extracts three modalities (384d text, 128d graph, 7d label prior), performs 519d feature concatenation, "
        "and trains the LightGBM classifier with early stopping."
    )
    story.append(Paragraph(p_mlw_desc, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 27 / Physical Page 35) - Tables 5.1 & 5.2
    # =========================================================================
    story.append(Paragraph("<b>5.6 Database Design / Dataset Design</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The database architecture is designed to store structured metadata, relational issue citations, and dense "
        "embedding vectors. The relational schema is managed within SQLite (<code>triage.db</code>).", styles['ReportBody']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 5.1: SQLite Issues & Edges Table Schema</b>", styles['TableCaption']))
    t51_data = [
        [Paragraph("<b>Table Name</b>", styles['TableHeader']),
         Paragraph("<b>Column Name</b>", styles['TableHeader']),
         Paragraph("<b>Data Type</b>", styles['TableHeader']),
         Paragraph("<b>Constraints & Description</b>", styles['TableHeader'])],
        
        [Paragraph("issues", styles['TableCellBold']), Paragraph("issue_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY (GitHub Issue Number)", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("title", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Raw and sanitized bug title", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("body_clean", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Boilerplate-cleansed issue description", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("created_at", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("ISO-8601 timestamp for temporal split", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("state", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Issue state ('open' or 'closed')", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("label", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Target SIG category (e.g. 'sig/node')", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("split", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Temporal split ('train', 'val', 'test')", styles['TableCell'])],
        
        [Paragraph("edges", styles['TableCellBold']), Paragraph("id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY AUTOINCREMENT", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("src_issue", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Source issue ID (Foreign Key)", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("dst_issue", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Referenced issue ID (Foreign Key)", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("edge_type", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Citation type ('references', 'duplicate')", styles['TableCell'])],
    ]
    t51 = Table(t51_data, colWidths=[65, 80, 75, 213])
    t51.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t51)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Table 5.2: SQLite PR Files & Embeddings Table Schema</b>", styles['TableCaption']))
    t52_data = [
        [Paragraph("<b>Table Name</b>", styles['TableHeader']),
         Paragraph("<b>Column Name</b>", styles['TableHeader']),
         Paragraph("<b>Data Type</b>", styles['TableHeader']),
         Paragraph("<b>Constraints & Description</b>", styles['TableHeader'])],
        
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY AUTOINCREMENT", styles['TableCell'])],
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("pr_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Linked Pull Request ID", styles['TableCell'])],
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("file_path", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Path to modified repository source file", styles['TableCell'])],
        
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("issue_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY, Foreign Key to issues.issue_id", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("text_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 384d MiniLM vector (float32)", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("graph_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 128d GraphSAGE vector (float32)", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("label_aware_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 7d empirical label prior (float32)", styles['TableCell'])],
    ]
    t52 = Table(t52_data, colWidths=[70, 85, 75, 203])
    t52.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t52)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 28 / Physical Page 36) - Tables 5.3 & 5.4
    # =========================================================================
    story.append(Paragraph("<b>Table 5.3: ChromaDB Vector Collection Schema</b>", styles['TableCaption']))
    story.append(Spacer(1, 3))

    t53_data = [
        [Paragraph("<b>Field Name</b>", styles['TableHeader']),
         Paragraph("<b>Type / Storage</b>", styles['TableHeader']),
         Paragraph("<b>Index / Metric</b>", styles['TableHeader']),
         Paragraph("<b>Description & Operational Function</b>", styles['TableHeader'])],
        
        [Paragraph("id", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Primary Key", styles['TableCellCenter']), Paragraph("Stringified issue ID (e.g. '119402')", styles['TableCell'])],
        [Paragraph("embedding", styles['TableCellBold']), Paragraph("Float32[384]", styles['TableCellCenter']), Paragraph("Cosine Metric", styles['TableCellCenter']), Paragraph("Normalized all-MiniLM-L6-v2 dense semantic text embedding vector", styles['TableCell'])],
        [Paragraph("document", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Full-Text", styles['TableCellCenter']), Paragraph("Cleaned text (Title + Body) used for lexical audit and context fallback", styles['TableCell'])],
        [Paragraph("metadata.label", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Inverted Index", styles['TableCellCenter']), Paragraph("Ground-truth SIG category assigned to training issue", styles['TableCell'])],
        [Paragraph("metadata.split", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Filter Index", styles['TableCellCenter']), Paragraph("Strictly set to 'train'; ensures zero validation/test leakage during search", styles['TableCell'])],
    ]
    t53 = Table(t53_data, colWidths=[90, 85, 80, 178])
    t53.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t53)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Table 5.4: Frontend LocalStorage History Schema</b>", styles['TableCaption']))
    story.append(Spacer(1, 3))

    t54_data = [
        [Paragraph("<b>Field Name</b>", styles['TableHeader']),
         Paragraph("<b>Type</b>", styles['TableHeader']),
         Paragraph("<b>UI Representation</b>", styles['TableHeader']),
         Paragraph("<b>Description & Maintainer Usage</b>", styles['TableHeader'])],
        
        [Paragraph("id", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Record Key", styles['TableCell']), Paragraph("Unique session identifier (e.g. 'k8s-115201')", styles['TableCell'])],
        [Paragraph("title", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("History Row Title", styles['TableCell']), Paragraph("Original bug report title displayed in audit table", styles['TableCell'])],
        [Paragraph("repository", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Repo Badge", styles['TableCell']), Paragraph("Target repository context ('kubernetes/kubernetes')", styles['TableCell'])],
        [Paragraph("suggestedTeam", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Team Pill Badge", styles['TableCell']), Paragraph("Formatted SIG name (e.g. 'SIG Node', 'SIG Network')", styles['TableCell'])],
        [Paragraph("confidence", styles['TableCellBold']), Paragraph("Float", styles['TableCellCenter']), Paragraph("Confidence Gauge", styles['TableCell']), Paragraph("Model confidence percentage (e.g. 94.0%)", styles['TableCell'])],
        [Paragraph("status", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Status Badge", styles['TableCell']), Paragraph("Triage state ('Triaged', 'Needs Clarification')", styles['TableCell'])],
        [Paragraph("dateAnalyzed", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Date Stamp", styles['TableCell']), Paragraph("Formatted human-readable analysis timestamp", styles['TableCell'])],
        [Paragraph("whyThisTeam", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Rationale Card", styles['TableCell']), Paragraph("Architectural explanation justifying SIG selection", styles['TableCell'])],
        [Paragraph("suggestedResponse", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Editor Modal", styles['TableCell']), Paragraph("Generated markdown comment ready for GitHub dispatch", styles['TableCell'])],
    ]
    t54 = Table(t54_data, colWidths=[90, 60, 95, 188])
    t54.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t54)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 29 / Physical Page 37) - Dataset Design
    # =========================================================================
    story.append(Paragraph("<b>5.6.1 Dataset Design & Target Class Stratification</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 4))

    p_ds1 = (
        "The Bug Triage AI dataset was mined from the official <b>kubernetes/kubernetes</b> repository, capturing issues "
        "created between 2020 and 2024. In Kubernetes governance, technical responsibilities are divided into Special Interest "
        "Groups (SIGs). The classification target is stratified across the seven highest-velocity SIG categories:"
    )
    story.append(Paragraph(p_ds1, styles['ReportBody']))
    story.append(Spacer(1, 4))

    sig_descs = [
        ("<b>1. sig/node:</b> ", "Governs node-level daemons including the Kubelet, Container Runtime Interface (CRI/containerd), Proactive Liveness Eviction (PLEG), cgroups v2 resource controllers, and hardware topology."),
        ("<b>2. sig/network:</b> ", "Governs pod network connectivity, kube-proxy packet routing (iptables/IPVS), CoreDNS resolution, EndpointSlices, NetworkPolicies, and CNI plugin integration."),
        ("<b>3. sig/api-machinery:</b> ", "Manages the central control plane architecture, kube-apiserver endpoints, etcd storage compaction, Custom Resource Definition (CRD) registration, and schema conversion webhooks."),
        ("<b>4. sig/scheduling:</b> ", "Responsible for the kube-scheduler daemon, pod topology spread constraints, node affinity/anti-affinity filters, priority queues, and preemption scoring algorithms."),
        ("<b>5. sig/storage:</b> ", "Handles persistent volume claims (PVC), Container Storage Interface (CSI) volume driver attachments, volume resizing, and storage unmount lifecycle controllers."),
        ("<b>6. sig/cli:</b> ", "Focuses on developer command-line utilities, kubectl command parsing, kustomize integration, and terminal output formatting."),
        ("<b>7. sig/auth:</b> ", "Oversees cluster security, RBAC authorization policies, BoundServiceAccountTokenVolume rotation, certificate management, and webhook authentication.")
    ]
    for title, desc in sig_descs:
        story.append(Paragraph(f"{title}{desc}", styles['ReportBody']))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    p_ds2 = (
        "To ensure absolute temporal realism, the dataset enforces a strict <b>chronological 80/10/10 split</b> where "
        "training issues precede validation issues, which in turn precede all test issues. This temporal ordering strictly "
        "prevents lookahead bias and accurately mirrors real-world production deployment."
    )
    story.append(Paragraph(p_ds2, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 30 / Physical Page 38) - UI Design Principles
    # =========================================================================
    story.append(Paragraph("<b>5.7 User Interface Design</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>5.7.1 Design Principles & SaaS Design Tokens</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))

    p_ui_p = (
        "The user interface of Bug Triage AI was designed following modern SaaS design aesthetics, focusing on clarity, "
        "high contrast, ergonomic data density, and seamless maintainer workflows. The visual theme is driven by Tailwind CSS "
        "design tokens supporting instantaneous switching between Light Mode and Dark Mode:"
    )
    story.append(Paragraph(p_ui_p, styles['ReportBody']))
    story.append(Spacer(1, 4))

    ui_tokens = [
        ("<b>Light Mode Background (#F8F9FC):</b> ", "A calm, ultra-light slate background paired with crisp white card containers (<code>#FFFFFF</code>) and subtle neutral borders (<code>#E5E7EB</code>), maximizing text legibility during daytime maintenance."),
        ("<b>Dark Mode Background (#0B0F19):</b> ", "A deep midnight-navy background complemented by dark elevated cards (<code>#111827</code>) and slate dividing lines (<code>#1F2937</code>), preventing eye strain during nocturnal triage shifts."),
        ("<b>Primary Accent Indigo (#2E31E8):</b> ", "A high-visibility electric indigo used for primary action buttons, confidence progress indicators, and active tab states, with <code>#2326C4</code> hover transitions."),
        ("<b>Typography Hierarchy:</b> ", "The interface incorporates the clean, modern <b>Inter</b> typeface across all display headers, badges, and body content, paired with monospace fonts for code snippets and log traces."),
        ("<b>Watermark Branding Graphic:</b> ", "A subtle, low-opacity vector watermark graphic is embedded behind workspace cards to provide a polished, branded look without interfering with reading flow."),
        ("<b>Micro-Animations & Progress Indicators:</b> ", "Smooth 200 ms cubic-bezier transitions for theme switching, interactive hover lifts on scenario cards, and animated pulsing progress bars during multi-modal inference.")
    ]
    for title, desc in ui_tokens:
        story.append(Paragraph(f"• {title}{desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2.5))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These design tokens ensure that the application maintains visual elegance while adhering to strict accessibility "
        "standards (WCAG 2.1 AA contrast ratios across all text and interactive badges).", styles['ReportBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Page 31 / Physical Page 39) - UI Screen Layouts
    # =========================================================================
    story.append(Paragraph("<b>5.7.2 Screen Layout Specifications (All 10 Screens)</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))

    p_screens = (
        "The Bug Triage AI frontend implements a cohesive 10-screen architecture covering the entire maintainer journey:"
    )
    story.append(Paragraph(p_screens, styles['ReportBody']))
    story.append(Spacer(1, 3))

    screen_list = [
        ("Screen 1 — Workspace Landing:", "Centered issue intake hero with live GitHub URL parser, rotating Kubernetes sample issue chips, and Quick Scenario selectors."),
        ("Screen 2 — Analyzing Progress View:", "Real-time 4-step execution view tracking issue parsing, ChromaDB similarity retrieval, GraphSAGE topological inference, and LightGBM classification."),
        ("Screen 3 — Triage Results Dashboard:", "Primary intelligence card displaying predicted SIG (e.g. SIG Node), 94% confidence gauge, 'Why This Team' architectural rationale, similar issue cards, and diagnostic audit checklist."),
        ("Screen 4 — Suggested Response Editor:", "Automated maintainer response synthesizer with live markdown preview, interactive diagnostic inclusion checkboxes, and one-click copy."),
        ("Screen 5 — Split-View Triage Session:", "Side-by-side comparative workspace displaying the original raw issue markdown on the left pane and real-time AI triage intelligence on the right pane."),
        ("Screen 6 — Maintainer History Audit View:", "Searchable, sortable audit table persisting all prior triages in local storage, complete with repository tags, timestamps, and result reload triggers."),
        ("Screen 7 — Maintainer Sign In Screen:", "Secure authentication view featuring credential validation, GitHub SSO options, and theme toggle controls."),
        ("Screen 8 — Create Maintainer Account:", "New maintainer registration view with role assignment, repository scope selection, and GitHub handle verification."),
        ("Screen 9 — Account & Model Settings:", "Maintainer configuration panel managing active model weights, inference confidence thresholds, API keys, and notification preferences."),
        ("Screen 10 — Error & Warning Component States:", "Comprehensive UI component sheet demonstrating all four system exception states: Unidentified Issue, Analysis Failed, Diagnostic Warning, and Empty History.")
    ]
    for title, desc in screen_list:
        story.append(Paragraph(f"<b>{title}</b> {desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    return story
