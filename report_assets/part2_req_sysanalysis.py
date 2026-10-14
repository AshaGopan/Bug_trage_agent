"""Part 2: Chapter 3 (Software Requirement Analysis, pp. 9-12) & Chapter 4 (System Analysis, pp. 13-16).
Physical Pages 17 to 24.
"""

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

def build_part2(styles):
    story = []

    # =========================================================================
    # CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS (Page 9 / Physical Page 17)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3.1 Hardware Specification</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The Bug Triage AI architecture is intentionally engineered for high computational efficiency on CPU hardware, "
        "eliminating mandatory GPU dependencies to ensure frictionless accessibility for individual maintainers and "
        "cost-effective containerized cloud deployment.", styles['ReportBody']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 3.1: Hardware Specifications</b>", styles['TableCaption']))
    hw_data = [
        [Paragraph("<b>Component</b>", styles['TableHeader']),
         Paragraph("<b>Minimum Requirement</b>", styles['TableHeader']),
         Paragraph("<b>Recommended Specification</b>", styles['TableHeader'])],
        
        [Paragraph("Processor (CPU)", styles['TableCellBold']),
         Paragraph("Intel Core i5 (8th Gen) or AMD Ryzen 5 (4 Cores, 2.5 GHz)", styles['TableCell']),
         Paragraph("Intel Core i7/i9 (10th Gen+) or AMD Ryzen 7/9 (8+ Cores, 3.6 GHz)", styles['TableCell'])],
        
        [Paragraph("System RAM", styles['TableCellBold']),
         Paragraph("8 GB DDR4", styles['TableCell']),
         Paragraph("16 GB – 32 GB DDR4/DDR5", styles['TableCell'])],
        
        [Paragraph("Primary Storage", styles['TableCellBold']),
         Paragraph("20 GB available disk space (HDD/SSD)", styles['TableCell']),
         Paragraph("50 GB NVMe PCIe M.2 SSD", styles['TableCell'])],
        
        [Paragraph("Display Resolution", styles['TableCellBold']),
         Paragraph("1366 &times; 768 pixels", styles['TableCell']),
         Paragraph("1920 &times; 1080 Full HD or higher", styles['TableCell'])],
        
        [Paragraph("Network Interface", styles['TableCellBold']),
         Paragraph("Broadband connection (10 Mbps)", styles['TableCell']),
         Paragraph("High-speed Gigabit Ethernet / Wi-Fi 6 (100+ Mbps)", styles['TableCell'])],
        
        [Paragraph("Input / Peripherals", styles['TableCellBold']),
         Paragraph("Standard keyboard and pointer device", styles['TableCell']),
         Paragraph("Multi-monitor developer workstation", styles['TableCell'])],
    ]
    t_hw = Table(hw_data, colWidths=[110, 160, 163])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3.2 Software Specification</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 3.2: Software Specifications</b>", styles['TableCaption']))

    sw_data = [
        [Paragraph("<b>Category</b>", styles['TableHeader']),
         Paragraph("<b>Software Environment</b>", styles['TableHeader']),
         Paragraph("<b>Version</b>", styles['TableHeader'])],
        
        [Paragraph("Operating System", styles['TableCellBold']),
         Paragraph("Microsoft Windows 10/11, Ubuntu Linux 22.04 LTS, macOS 13+", styles['TableCell']),
         Paragraph("64-bit Architecture", styles['TableCellCenter'])],
        
        [Paragraph("Core Runtime", styles['TableCellBold']),
         Paragraph("Python Programming Language", styles['TableCell']),
         Paragraph("3.11.x (CPython)", styles['TableCellCenter'])],
        
        [Paragraph("Deep Learning Engine", styles['TableCellBold']),
         Paragraph("PyTorch (CPU-optimized distribution)", styles['TableCell']),
         Paragraph("2.2.0+", styles['TableCellCenter'])],
        
        [Paragraph("Graph Neural Network", styles['TableCellBold']),
         Paragraph("PyTorch Geometric (PyG)", styles['TableCell']),
         Paragraph("2.5.0+", styles['TableCellCenter'])],
    ]
    t_sw = Table(sw_data, colWidths=[130, 220, 83])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sw)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS (Page 10 / Physical Page 18)
    # =========================================================================
    story.append(Paragraph("<b>Table 3.2: Software Specifications (Continued)</b>", styles['TableCaption']))
    sw_data2 = [
        [Paragraph("<b>Category</b>", styles['TableHeader']),
         Paragraph("<b>Software Environment</b>", styles['TableHeader']),
         Paragraph("<b>Version</b>", styles['TableHeader'])],
        
        [Paragraph("Gradient Boosting", styles['TableCellBold']),
         Paragraph("LightGBM (Multi-class GBDT)", styles['TableCell']),
         Paragraph("4.3.0+", styles['TableCellCenter'])],
        
        [Paragraph("Text Embeddings", styles['TableCellBold']),
         Paragraph("SentenceTransformers (all-MiniLM-L6-v2)", styles['TableCell']),
         Paragraph("2.6.0+", styles['TableCellCenter'])],
        
        [Paragraph("Vector Database", styles['TableCellBold']),
         Paragraph("ChromaDB Persistent Client", styles['TableCell']),
         Paragraph("0.4.24+", styles['TableCellCenter'])],
        
        [Paragraph("Relational Database", styles['TableCellBold']),
         Paragraph("SQLite Embedded Database Engine", styles['TableCell']),
         Paragraph("3.42+", styles['TableCellCenter'])],
        
        [Paragraph("Agent Framework", styles['TableCellBold']),
         Paragraph("LangGraph & LangChain Core", styles['TableCell']),
         Paragraph("0.0.30+ / 0.1.20+", styles['TableCellCenter'])],
        
        [Paragraph("Backend API Framework", styles['TableCellBold']),
         Paragraph("FastAPI & Uvicorn ASGI Server", styles['TableCell']),
         Paragraph("0.110.0+ / 0.28.0+", styles['TableCellCenter'])],
        
        [Paragraph("Frontend UI Framework", styles['TableCellBold']),
         Paragraph("React 18 & Vite Build Tool", styles['TableCell']),
         Paragraph("18.3.1 / 5.4.14", styles['TableCellCenter'])],
        
        [Paragraph("CSS & Styling", styles['TableCellBold']),
         Paragraph("Tailwind CSS & PostCSS", styles['TableCell']),
         Paragraph("3.4.17+", styles['TableCellCenter'])],
        
        [Paragraph("Package & Build Manager", styles['TableCellBold']),
         Paragraph("npm (Node Package Manager) & pip", styles['TableCell']),
         Paragraph("10.8+ / 24.0+", styles['TableCellCenter'])],
    ]
    t_sw2 = Table(sw_data2, colWidths=[130, 220, 83])
    t_sw2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_sw2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3.3 Software / Tools and Their Features</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 3.3: Software Tools and Their Features (Part 1)</b>", styles['TableCaption']))

    tools_data1 = [
        [Paragraph("<b>Tool / Library</b>", styles['TableHeader']),
         Paragraph("<b>Role in Architecture</b>", styles['TableHeader']),
         Paragraph("<b>Key Functional Features</b>", styles['TableHeader'])],
        
        [Paragraph("Python 3.11", styles['TableCellBold']),
         Paragraph("Core Execution Runtime", styles['TableCell']),
         Paragraph("High-performance bytecode interpreter, robust typing, asynchronous asyncio runtime.", styles['TableCell'])],
        
        [Paragraph("PyTorch & PyG", styles['TableCellBold']),
         Paragraph("Graph Neural Network", styles['TableCell']),
         Paragraph("Tensor computation, autograd, native sparse neighborhood aggregation for GraphSAGE.", styles['TableCell'])],
        
        [Paragraph("LightGBM", styles['TableCellBold']),
         Paragraph("Multi-Modal Classifier", styles['TableCell']),
         Paragraph("Histogram-based decision trees, native multi-class support, leaf-wise split tree growth.", styles['TableCell'])],
        
        [Paragraph("SentenceTransformers", styles['TableCellBold']),
         Paragraph("Dense Text Embeddings", styles['TableCell']),
         Paragraph("Pretrained Siamese MiniLM models, 384-dimensional latent semantic projections.", styles['TableCell'])],
    ]
    t_tool1 = Table(tools_data1, colWidths=[105, 125, 203])
    t_tool1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_tool1)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS (Page 11 / Physical Page 19)
    # =========================================================================
    story.append(Paragraph("<b>Table 3.3: Software Tools and Their Features (Part 2)</b>", styles['TableCaption']))
    story.append(Spacer(1, 4))

    tools_data2 = [
        [Paragraph("<b>Tool / Library</b>", styles['TableHeader']),
         Paragraph("<b>Role in Architecture</b>", styles['TableHeader']),
         Paragraph("<b>Key Functional Features</b>", styles['TableHeader'])],
        
        [Paragraph("ChromaDB", styles['TableCellBold']),
         Paragraph("Dense Vector Index", styles['TableCell']),
         Paragraph("HNSW index, sub-millisecond top-K cosine similarity search, embedded metadata filtering.", styles['TableCell'])],
        
        [Paragraph("SQLite 3", styles['TableCellBold']),
         Paragraph("Relational Persistence", styles['TableCell']),
         Paragraph("Zero-configuration serverless database, strict transactional integrity, BLOB storage for vectors.", styles['TableCell'])],
        
        [Paragraph("LangGraph", styles['TableCellBold']),
         Paragraph("Agentic Orchestrator", styles['TableCell']),
         Paragraph("Stateful directed acyclic graph (DAG), node cycle management, conditional routing predicates.", styles['TableCell'])],
        
        [Paragraph("FastAPI", styles['TableCellBold']),
         Paragraph("REST Service API", styles['TableCell']),
         Paragraph("Asynchronous OpenAPI endpoints, automatic Pydantic request validation, high throughput.", styles['TableCell'])],
        
        [Paragraph("Uvicorn", styles['TableCellBold']),
         Paragraph("ASGI Web Server", styles['TableCell']),
         Paragraph("Lightning-fast ASGI web server implementation based on uvloop and httptools.", styles['TableCell'])],
        
        [Paragraph("React 18", styles['TableCellBold']),
         Paragraph("Frontend User Interface", styles['TableCell']),
         Paragraph("Component-based architecture, concurrent rendering, dynamic state hooks, virtual DOM.", styles['TableCell'])],
        
        [Paragraph("Vite 5", styles['TableCellBold']),
         Paragraph("Frontend Bundler", styles['TableCell']),
         Paragraph("Native ES modules, lightning-fast Hot Module Replacement (HMR), optimized production rollups.", styles['TableCell'])],
        
        [Paragraph("Tailwind CSS", styles['TableCellBold']),
         Paragraph("Utility-First Styling", styles['TableCell']),
         Paragraph("Design token abstraction, seamless dark/light mode toggling, glassmorphic card primitives.", styles['TableCell'])],
    ]
    t_tool2 = Table(tools_data2, colWidths=[105, 125, 203])
    t_tool2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_tool2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table 3.3: Software Tools and Their Features (Part 3)</b>", styles['TableCaption']))
    tools_data3 = [
        [Paragraph("<b>Tool / Library</b>", styles['TableHeader']),
         Paragraph("<b>Role in Architecture</b>", styles['TableHeader']),
         Paragraph("<b>Key Functional Features</b>", styles['TableHeader'])],
        
        [Paragraph("Lucide React", styles['TableCellBold']),
         Paragraph("Iconography Suite", styles['TableCell']),
         Paragraph("Clean, tree-shakeable SVG icons for maintainer actions, status indicators, and badges.", styles['TableCell'])],
        
        [Paragraph("Pytest", styles['TableCellBold']),
         Paragraph("Automated Testing", styles['TableCell']),
         Paragraph("Unit and integration test suites, leakage assertion fixtures, CI/CD compatibility.", styles['TableCell'])],
        
        [Paragraph("ReportLab", styles['TableCellBold']),
         Paragraph("Document Generation", styles['TableCell']),
         Paragraph("Programmatic PDF compilation, Platypus flowable document layout, vector canvas rendering.", styles['TableCell'])],
    ]
    t_tool3 = Table(tools_data3, colWidths=[105, 125, 203])
    t_tool3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_tool3)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS (Page 12 / Physical Page 20)
    # =========================================================================
    story.append(Paragraph("<b>3.3.1 Tool Selection Rationale & Technology Stack Alignment</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 4))

    rat1 = (
        "The selection of the software stack for Bug Triage AI reflects deliberate architectural trade-offs focused "
        "on reproducibility, latency, zero-leakage rigor, and deployment ergonomics:"
    )
    story.append(Paragraph(rat1, styles['ReportBody']))
    story.append(Spacer(1, 4))

    rat_items = [
        ("<b>LightGBM over Deep Neural Text Classifiers:</b> ",
         "While fine-tuning heavy Transformer models (e.g. RoBERTa or LLaMA) achieves strong language understanding, "
         "their training and inference latency on multi-thousand token bug logs exceeds acceptable real-time limits and "
         "requires enterprise-grade GPUs. LightGBM delivers microsecond-level tabular inference, seamlessly accepts "
         "concatenated multi-modal feature vectors, and achieves state-of-the-art Macro-F1 (0.7485) on standard CPU hardware."),
        ("<b>Inductive GraphSAGE over Transductive GCNs:</b> ",
         "Classical Graph Convolutional Networks require re-computing the Laplacian over the entire global graph whenever "
         "a new node is introduced. GraphSAGE learns localized neighborhood aggregation functions, allowing newly submitted "
         "issues to be dynamically embedded into the structural space via temporary K-NN inference subgraphs."),
        ("<b>ChromaDB over Remote Vector Clouds:</b> ",
         "ChromaDB operates as an embedded, serverless vector index with persistent local storage. This eliminates external "
         "network roundtrips, reduces cloud infrastructure costs, and guarantees complete data privacy for proprietary codebases."),
        ("<b>FastAPI & React over Monolithic UI Frameworks:</b> ",
         "Decoupling the machine learning serving layer (FastAPI) from the user interface (React + Vite) guarantees a clear "
         "separation of concerns. The REST API can be integrated into GitHub Actions, webhooks, or Slack bots, while the "
         "React maintainer workspace delivers a responsive, desktop-class experience with zero page reload latency.")
    ]
    for title, desc in rat_items:
        story.append(Paragraph(f"• {title}{desc}", styles['ReportBullet']))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 - SYSTEM ANALYSIS (Page 13 / Physical Page 21)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 4 - SYSTEM ANALYSIS</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4.1 Requirement Specification</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The requirements for Bug Triage AI were established through detailed analysis of maintainer workflows within "
        "the Kubernetes open-source organization. Requirements are partitioned into Functional Requirements (FR) and "
        "Non-Functional Requirements (NFR).", styles['ReportBody']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Functional Requirements (FR):</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))

    fr_items = [
        ("FR1: Issue Ingestion & Manual Input",
         "The system shall accept manual bug report submissions comprising an issue title and an unstructured markdown description."),
        ("FR2: Live GitHub Issue URL Fetching",
         "The system shall accept valid GitHub issue URLs (e.g. <code>https://github.com/kubernetes/kubernetes/issues/12345</code>), "
         "fetch live title and body contents via the GitHub REST API, and populate the triage intake buffer."),
        ("FR3: Rotating SIG Scenario Selection",
         "The system shall provide a carousel of pre-seeded, realistic Kubernetes issue scenarios spanning multiple SIG domains "
         "and completeness levels to enable rapid demonstration and maintainer testing."),
        ("FR4: Markdown & Boilerplate Sanitization",
         "The system shall strip HTML comments, GitHub issue template prompts, and extraneous whitespace while preserving technical "
         "keywords, error logs, and stack traces."),
        ("FR5: Diagnostic Completeness Auditing",
         "The system shall audit incoming reports for three essential diagnostic fields: step-by-step reproduction instructions, "
         "environment specifications (Kubernetes version, OS, container runtime), and relevant daemon logs."),
        ("FR6: Top-K Semantic Duplicate Retrieval",
         "The system shall query a dense ChromaDB vector index to retrieve the top K=5 semantically similar historical issues from the "
         "chronological training partition, reporting cosine distances."),
        ("FR7: Cold-Start Dynamic Subgraph Construction",
         "The system shall dynamically synthesize an inference subgraph linking new bug reports to retrieved nearest neighbors, computing "
         "inductive 128-dimensional GraphSAGE topological representations."),
        ("FR8: Multi-Modal Hybrid Classification",
         "The system shall concatenate text, graph, and label features (519 dimensions) and predict the target SIG category with an "
         "associated confidence probability score.")
    ]
    for title, desc in fr_items:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2.5))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 - SYSTEM ANALYSIS (Page 14 / Physical Page 22)
    # =========================================================================
    fr_cont = [
        ("FR9: Confidence-Gated Conditional Routing",
         "The system shall route predictions through a LangGraph conditional edge: cases with confidence &ge; 60% route to "
         "<code>writer_high_node</code> (/sig assignment), while cases &lt; 60% route to <code>writer_low_node</code> (clarification request)."),
        ("FR10: Suggested Maintainer Comment Synthesis",
         "The system shall synthesize an editable markdown comment that cites similar historical issues, requests missing diagnostic "
         "fields, and drafts formal slash-commands (e.g. <code>/sig node</code>)."),
        ("FR11: Audit History & Local Persistence",
         "The system shall persist all triaged sessions to browser local storage, providing a searchable history table with status tags, "
         "dates, and one-click session reloading."),
        ("FR12: Maintainer Profile & Theme Management",
         "The system shall support user authentication, maintainer profile configuration, and persistent Light Mode (#F8F9FC) and "
         "Dark Mode (#0B0F19) theme toggling.")
    ]
    for title, desc in fr_cont:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2.5))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Non-Functional Requirements (NFR):</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))

    nfr_items = [
        ("NFR1: End-to-End Latency", "The system shall complete the entire multi-modal triage pipeline (intake to draft response) within 2.0 seconds on standard CPU hardware."),
        ("NFR2: Classification Accuracy", "The hybrid model shall maintain a Macro-F1 score &ge; 0.74 on chronologically held-out test issues."),
        ("NFR3: Zero Data Leakage", "All preprocessing, indexing, and GNN training steps shall strictly isolate training data from validation and test splits."),
        ("NFR4: Responsive Design", "The web interface shall maintain responsive layouts across screen resolutions from 320px mobile to 1920px Full HD desktop displays."),
        ("NFR5: High Availability & Fallback", "The FastAPI backend shall implement robust exception handlers and rule-based fallbacks to maintain continuous service availability."),
        ("NFR6: Maintainer Trust & Explainability", "The UI shall explicitly present confidence scores, 'Why This Team' architectural justifications, and links to similar past issues.")
    ]
    for title, desc in nfr_items:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2.5))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>4.2 Characteristics of Existing System</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_exist = (
        "Conventional bug triaging in open-source projects is characterized by manual human review, ad-hoc label assignment, "
        "frequent misrouting across architectural boundaries, and significant delays in identifying duplicate reports. Existing "
        "computational tools are primarily standalone academic scripts lacking production integration, web interfaces, or "
        "relational graph reasoning capabilities."
    )
    story.append(Paragraph(p_exist, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 - SYSTEM ANALYSIS (Page 15 / Physical Page 23)
    # =========================================================================
    story.append(Paragraph("<b>4.3 Proposed System / Proposed Approach</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    p_prop = (
        "The proposed Bug Triage AI platform overcomes existing limitations by delivering an end-to-end, multi-modal "
        "engineering solution. It integrates dense sentence embeddings, inductive GraphSAGE topological representations, "
        "and training-neighbor label priors into a stateful LangGraph agentic workflow. This automated pipeline operates in "
        "tandem with an interactive React maintainer dashboard, empowering human maintainers to review, edit, and approve "
        "intelligent triage recommendations with high confidence."
    )
    story.append(Paragraph(p_prop, styles['ReportBody']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4.4 Feasibility Study</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    p_feas = (
        "A rigorous feasibility study was conducted across four dimensions—Technical, Economic, Operational, and "
        "Schedule—to ensure the viability, sustainability, and deployment readiness of the Bug Triage AI project."
    )
    story.append(Paragraph(p_feas, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>4.4.1 Technical Feasibility</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    p_tech = (
        "The project leverages mature, battle-tested open-source libraries including Python 3.11, PyTorch, PyTorch Geometric, "
        "LightGBM, SentenceTransformers, ChromaDB, FastAPI, and React 18. All core machine learning models are optimized to execute "
        "on standard multi-core CPU architectures without mandatory GPU acceleration. Dynamic K-NN subgraph construction in ChromaDB "
        "effectively solves the cold-start problem in sub-millisecond execution times. The technical risk is negligible as all "
        "underlying dependencies are commercially proven and actively maintained by global foundations."
    )
    story.append(Paragraph(p_tech, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>4.4.2 Economic Feasibility</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    p_econ = (
        "The entire software stack comprises open-source software distributed under permissive Apache 2.0 and MIT licenses. "
        "Local vector storage in ChromaDB and relational storage in SQLite eliminate recurring third-party cloud database fees. "
        "Because the model executes efficiently on standard CPU cloud instances (such as AWS t3.xlarge or DigitalOcean Droplets), "
        "operational hosting expenditures are minimal. Consequently, the project delivers exceptional return on investment "
        "by recovering hundreds of maintainer hours at negligible operational cost."
    )
    story.append(Paragraph(p_econ, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4 - SYSTEM ANALYSIS (Page 16 / Physical Page 24)
    # =========================================================================
    story.append(Paragraph("<b>4.4.3 Operational Feasibility</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_oper = (
        "The system is designed with a maintainer-in-the-loop philosophy, avoiding disruptive disruptions to established "
        "open-source governance models. Maintainers interact with an intuitive browser-based dashboard requiring zero client-side "
        "software installation. Triage suggestions, duplicate links, and drafted comments are presented transparently with "
        "confidence indicators. Maintainers retain complete editorial control, ensuring high operational acceptance across "
        "distributed developer communities."
    )
    story.append(Paragraph(p_oper, styles['ReportBody']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>4.4.4 Schedule Feasibility</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_sched = (
        "The development roadmap was organized across six structured phases spanning research, data ingestion, feature "
        "engineering, model training, agentic orchestration, and UI development. All milestones—including rigorous unit "
        "testing, zero-leakage verification, and documentation—were completed within the allocated academic timeframe."
    )
    story.append(Paragraph(p_sched, styles['ReportBody']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4.5 Software Requirement Specification (SRS)</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The complete SRS defines external interface standards, performance thresholds, and security controls:", styles['ReportBody']
    ))
    story.append(Spacer(1, 4))

    srs_items = [
        ("<b>User Interfaces:</b> Modern web browsers supporting HTML5, CSS Grid, and ES6+ (Google Chrome 110+, Mozilla Firefox 115+, Microsoft Edge 110+, Apple Safari 16+)."),
        ("<b>Hardware Interfaces:</b> Standard TCP/IP networking interface for REST API communication between Vite frontend and FastAPI backend."),
        ("<b>Software Interfaces:</b> GitHub REST API v3 for issue fetching; ChromaDB persistent API; SQLite 3 C-library bindings."),
        ("<b>Performance Constraints:</b> End-to-end inference latency under 200 ms; UI render rate of 60 FPS; memory footprint under 2.5 GB RAM."),
        ("<b>Security Controls:</b> Input sanitization to prevent Cross-Site Scripting (XSS); secure local storage keying; environment variable encapsulation for GitHub API tokens.")
    ]
    for item in srs_items:
        story.append(Paragraph(f"• {item}", styles['ReportBullet']))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    return story
