"""Part 1: Chapter 1 (Introduction, pp. 1-4) & Chapter 2 (Literature Survey, pp. 5-8).
Physical Pages 9 to 16.
"""

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

def build_part1(styles):
    story = []

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION (Page 1 / Physical Page 9)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 1 - INTRODUCTION</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.1 Background of the Study</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    p1 = (
        "Modern large-scale open-source software (OSS) projects represent the foundational infrastructure "
        "of global enterprise computing. Among these, the <b>kubernetes/kubernetes</b> container orchestration "
        "ecosystem stands as one of the most active, receiving hundreds of thousands of issues, pull requests, "
        "and technical inquiries across dozens of distinct architectural domains. Managing such high-velocity "
        "repositories imposes a heavy cognitive and operational burden on project maintainers. In typical "
        "workflows, each incoming bug report must be promptly inspected, cleansed of template boilerplate, "
        "audited for diagnostic reproducibility, correlated with existing or duplicate reports, and routed to "
        "the appropriate Special Interest Group (SIG)—such as <code>sig/node</code>, <code>sig/network</code>, "
        "<code>sig/api-machinery</code>, <code>sig/storage</code>, or <code>sig/scheduling</code>."
    )
    story.append(Paragraph(p1, styles['ReportBody']))

    p2 = (
        "Historically, open-source repositories relied entirely on manual triage triage rotas, where senior "
        "engineers dedicate significant working hours to reviewing incoming bug logs, requesting missing reproduction "
        "steps, and tagging issues with appropriate labels. This manual paradigm creates an unsustainable "
        "operational bottleneck. Unassigned bug reports linger in triage queues for days or weeks, delaying critical "
        "security and stability patches while frustrating contributors who receive slow or disjointed initial feedback. "
        "Moreover, maintainer burnout has emerged as an acute sustainability hazard across the open-source software "
        "landscape, threatening the long-term vitality of core cloud-native platforms."
    )
    story.append(Paragraph(p2, styles['ReportBody']))

    p3 = (
        "Early attempts at software triage automation leveraged traditional information retrieval (IR) and "
        "classical statistical machine learning, such as Bag-of-Words with Naive Bayes or Support Vector Machines (SVM). "
        "While computationally lightweight, these approaches suffer from severe vocabulary mismatch, complete disregard "
        "for structural source code syntax, and an inability to model dense semantic interactions. Subsequent deep "
        "learning models improved text parsing but frequently treated bug reports as isolated text strings, ignoring "
        "the rich topological relationships—such as cross-issue citations, shared pull requests, and file modification "
        "overlaps—that naturally link bug reports within large code repositories."
    )
    story.append(Paragraph(p3, styles['ReportBody']))

    p4 = (
        "Recent breakthroughs in dense semantic sentence transformers, inductive Graph Neural Networks (GNNs), and "
        "agentic Large Language Model (LLM) orchestration present unprecedented opportunities to construct end-to-end, "
        "multi-modal bug triage agents. By integrating structural graph learning with deep semantic embeddings and "
        "strict temporal partitioning, modern software engineering can achieve explainable, high-accuracy, and "
        "production-grade triage automation that dramatically streamlines maintainer workflows."
    )
    story.append(Paragraph(p4, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION (Page 2 / Physical Page 10)
    # =========================================================================
    story.append(Paragraph("<b>1.2 Problem Statement</b>", styles['SectionHeader']))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Despite extensive research into automated software maintenance, existing bug triaging tools and research "
        "prototypes suffer from fundamental methodological, architectural, and operational deficiencies when deployed "
        "against real-world hyperscale codebases:", styles['ReportBody']
    ))
    story.append(Spacer(1, 4))

    ps_items = [
        ("<b>Accessibility & Scalability Bottleneck:</b> ",
         "Maintainers of flagship open-source repositories face a staggering volume of incoming bug submissions. "
         "Existing research prototypes often exist only as offline Python scripts or research notebooks, lacking "
         "accessible, interactive, production-ready interfaces suitable for day-to-day maintainer operations."),
        ("<b>Multi-Modal Disconnect:</b> ",
         "Most existing classifiers evaluate either pure natural language text or isolated graph structures. In reality, "
         "a bug report is deeply multi-modal: it combines descriptive text, error stack traces, cross-reference topologies "
         "(issue-to-issue links), and historical label priors. Neglecting these synergistic modalities yields suboptimal "
         "classification accuracy and high false-routing rates."),
        ("<b>Diagnostic Incompleteness Gap:</b> ",
         "A high percentage of community bug reports are submitted without essential diagnostic artifacts, such as "
         "step-by-step reproduction instructions, cluster environment details, or daemon logs. Existing classifiers "
         "blindly attempt to route incomplete reports, whereas maintainers require an upfront completeness audit "
         "before routing decisions are finalized."),
        ("<b>Chronological Data Leakage in Academic Research:</b> ",
         "A pervasive flaw in existing literature is the application of random K-fold cross-validation to software "
         "evolution data. Random splitting allows future bug reports, resolved PRs, and modern terminology to leak into "
         "the training partition, creating artificially inflated accuracy benchmarks that collapse when exposed to "
         "strictly chronological test streams."),
        ("<b>Lack of Maintainer-in-the-Loop Orchestration:</b> ",
         "Autonomous 'black box' bots that blindly assign labels or post rigid generic responses frequently provoke "
         "maintainer distrust. Effective triage demands an agentic workflow that provides confidence gauges, retrieves "
         "relevant historical duplicates, and drafts editable markdown responses for human maintainer approval.")
    ]

    for title, desc in ps_items:
        story.append(Paragraph(f"• {title}{desc}", styles['ReportBullet']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These compounding challenges demonstrate the urgent necessity for <b>Bug Triage AI</b>—a comprehensive, "
        "zero-leakage, multi-modal triage platform combining dense embeddings, inductive GraphSAGE topological "
        "representations, LangGraph stateful orchestration, and modern web engineering.", styles['ReportBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION (Page 3 / Physical Page 11)
    # =========================================================================
    story.append(Paragraph("<b>1.3 Objectives of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("The primary objectives of this project are:", styles['ReportBody']))
    story.append(Spacer(1, 4))

    obj_items = [
        "To establish a <b>strict zero-leakage temporal pipeline</b> on <code>kubernetes/kubernetes</code> issue archives, ensuring no chronological lookahead bias across training, validation, and test partitions.",
        "To engineer a <b>dense semantic text embedding module</b> using <code>all-MiniLM-L6-v2</code> to transform cleaned issue titles and descriptions into 384-dimensional latent semantic vectors on CPU.",
        "To develop an <b>inductive GraphSAGE Graph Neural Network</b> capable of learning topological representations (128d) from cross-issue references, with dynamic K-NN subgraph construction for unlinked cold-start bug reports.",
        "To extract an empirical <b>training-neighbor label awareness prior</b> (7d) that conditions predictions on historical category frequencies without validation or test split leakage.",
        "To construct a <b>multi-modal LightGBM classifier</b> that concatenates text, graph, and label features (519 dimensions) to achieve superior Macro-F1 accuracy across seven primary Kubernetes Special Interest Groups.",
        "To build a stateful <b>LangGraph agentic pipeline</b> executing intake sanitization, diagnostic completeness audits, cold-start topological retrieval, and confidence-gated response comment drafting.",
        "To implement an asynchronous <b>FastAPI REST backend</b> with strict Pydantic schemas, CPU-optimized batch inference, and ChromaDB vector indexing.",
        "To engineer a responsive, high-fidelity <b>React + Vite + Tailwind CSS Maintainer Workspace</b> supporting Light Mode (#F8F9FC), Dark Mode (#0B0F19), live issue URL fetching, and split-view session analysis."
    ]

    for idx, obj in enumerate(obj_items):
        story.append(Paragraph(f"<b>{idx+1}.</b> {obj}", styles['ReportBullet']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1.4 Scope of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The scope of Bug Triage AI encompasses:", styles['ReportBody']))
    story.append(Spacer(1, 2))

    in_scope = [
        "<b>In Scope:</b>",
        "• Data ingestion and caching of issue reports, labels, and PR cross-references from the <code>kubernetes/kubernetes</code> repository.",
        "• Markdown sanitization, HTML comment removal, and issue template stripping.",
        "• Chronological temporal partitioning enforcing max(T_train) &le; min(T_val) &le; min(T_test).",
        "• Dense vector generation via SentenceTransformers and persistent caching in SQLite.",
        "• Multi-modal feature fusion and multi-class LightGBM classification across 7 target SIG categories.",
        "• LangGraph agentic state machine with confidence routing (&ge; 60% threshold).",
        "• ChromaDB vector indexing for top-5 semantic duplicate and similar issue retrieval.",
        "• Interactive 10-screen React frontend with full local storage audit history persistence."
    ]
    for item in in_scope:
        story.append(Paragraph(item, styles['ReportBullet']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1 - INTRODUCTION (Page 4 / Physical Page 12)
    # =========================================================================
    out_scope = [
        "<b>Out of Scope:</b>",
        "• Fully autonomous modification, patching, or merging of source code in the master repository.",
        "• Direct execution or remediation actions against live production Kubernetes clusters.",
        "• Multi-lingual translation of non-English bug submissions.",
        "• Native mobile applications (iOS/Android) as maintainer workflows operate primarily on desktop workstations.",
        "• Hardware-accelerated GPU dependencies; the system is strictly engineered for CPU-only execution."
    ]
    for item in out_scope:
        story.append(Paragraph(item, styles['ReportBullet']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>1.5 Significance of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 6))

    sig1 = (
        "The significance of Bug Triage AI lies in bridging the critical divide between experimental machine learning "
        "research and practical, production-ready software engineering tools. While dozens of academic papers demonstrate "
        "algorithmic prototypes on static benchmarks, few provide the operational scaffolding required for actual "
        "open-source maintainers. Bug Triage AI delivers an end-to-end architecture that respects the nuanced realities "
        "of enterprise software maintenance."
    )
    story.append(Paragraph(sig1, styles['ReportBody']))
    story.append(Spacer(1, 4))

    sig2 = (
        "From an engineering perspective, this project pioneers the integration of <b>inductive Graph Neural Networks</b> "
        "with dense semantic language embeddings for bug triage. By introducing cold-start dynamic K-NN subgraph "
        "projection, the system solves a fundamental limitation of classical graph methods—namely, the inability to "
        "embed a newly submitted node that possesses zero existing topological edges. This enables rich graph structural "
        "reasoning even for freshly reported issues."
    )
    story.append(Paragraph(sig2, styles['ReportBody']))
    story.append(Spacer(1, 4))

    sig3 = (
        "Furthermore, the project enforces strict methodological integrity through <b>leakage-free chronological "
        "partitioning</b>. By proving that models must be evaluated against temporal splits rather than random cross-validation, "
        "the project establishes an authentic, realistic performance benchmark for the software engineering research community. "
        "Combined with an intuitive maintainer-in-the-loop interface and automated diagnostic completeness auditing, "
        "Bug Triage AI significantly accelerates issue triage cycles, reduces volunteer cognitive fatigue, and enhances "
        "the overall reliability of critical open-source software infrastructure."
    )
    story.append(Paragraph(sig3, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY (Page 5 / Physical Page 13)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 2 - LITERATURE SURVEY / EXISTING STUDIES</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>2.1 Review of Existing Systems / Research Works</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.1.1 Classical IR & TF-IDF Bug Triaging</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    lit1 = (
        "Early research in automated bug triaging framed the assignment problem as text classification over unstructured "
        "issue descriptions. Cubranic & Murphy (2004) pioneered the application of supervised text categorization, "
        "utilizing Naive Bayes classifiers trained on term frequencies extracted from bug descriptions. Anvik et al. (2006) "
        "extended this approach to Eclipse and Mozilla repositories using Support Vector Machines (SVM), establishing that "
        "filtering inactive developers and tuning term weighting noticeably improved classification precision. However, "
        "these classical Information Retrieval (IR) models rely on Bag-of-Words (BoW) representations, which suffer from "
        "high dimensionality, severe word sparsity, and an inability to account for synonymy, semantic context, or specialized "
        "cloud-native technical jargon."
    )
    story.append(Paragraph(lit1, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.1.2 Transformer & MiniLM Semantic Embeddings</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    lit2 = (
        "The emergence of Transformer architectures (Vaswani et al., 2017) and pretrained contextual language models like "
        "BERT (Devlin et al., 2019) fundamentally transformed natural language processing in software engineering. "
        "Reimers & Gurevych (2019) introduced Sentence-BERT (SentenceTransformers), fine-tuning Siamese neural networks "
        "to produce dense, fixed-dimensional vector representations that capture semantic similarity with high fidelity. "
        "In the domain of software triage, dense representations such as <i>all-MiniLM-L6-v2</i> compress complex technical "
        "narratives into 384-dimensional latent vectors. These models excel at recognizing that terms such as 'Kubelet PLEG', "
        "'cgroup memory pressure', and 'eviction manager' map to closely clustered semantic spaces, even when exact lexical "
        "tokens do not overlap."
    )
    story.append(Paragraph(lit2, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY (Page 6 / Physical Page 14)
    # =========================================================================
    story.append(Paragraph("<b>2.1.3 Graph Neural Networks & Inductive GraphSAGE</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    lit3 = (
        "While semantic text representations capture issue narratives, software repositories are inherently relational. "
        "Issues frequently cross-reference other issues, link to bug-fixing Pull Requests, and share common modified source "
        "code paths. Kipf & Welling (2017) demonstrated that Graph Convolutional Networks (GCNs) effectively capture "
        "neighborhood dependencies in relational networks. However, standard GCNs operate transductively, requiring the "
        "entire graph structure to be known during training. To triage incoming bug reports in real-time, an inductive "
        "approach is mandatory. Hamilton et al. (2017) developed <b>GraphSAGE</b> (Sample and Aggregate), an inductive framework "
        "that learns topological aggregation functions across local node neighborhoods. By training a 2-layer GraphSAGE GNN "
        "on historical cross-reference edges, structural topology can be projected into 128-dimensional continuous vectors, "
        "enriching text representations with relational context."
    )
    story.append(Paragraph(lit3, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.1.4 Agentic LLM Workflows in Software Maintenance</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    lit4 = (
        "The rapid evolution of Large Language Models (LLMs) has opened new horizons for autonomous software engineering. "
        "Frameworks such as LangChain and LangGraph (Chase, 2024) enable the construction of stateful, cyclical multi-agent "
        "workflows that decompose complex software tasks into discrete reasoning steps. Recent benchmarks like SWE-bench "
        "(Jimenez et al., 2024) demonstrate that structured agentic workflows—combining context ingestion, diagnostic checks, "
        "and conditional routing—drastically outperform monolithic one-shot prompting. By embedding multi-modal classifiers "
        "inside a LangGraph state graph, bug triage agents can perform structured diagnostic completeness audits and draft "
        "customized maintainer comments conditioned on classification confidence."
    )
    story.append(Paragraph(lit4, styles['ReportBody']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.2 Comparative Analysis</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "A rigorous comparative examination of existing literature versus the proposed Bug Triage AI architecture "
        "highlights several core differentiators across feature modalities, graph learning, leakage prevention, and "
        "agentic workflow orchestration:", styles['ReportBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY (Page 7 / Physical Page 15)
    # =========================================================================
    story.append(Paragraph("<b>Table 2.1: Comparative Analysis with Existing Systems</b>", styles['TableCaption']))
    story.append(Spacer(1, 3))

    comp_data = [
        [Paragraph("<b>System / Study</b>", styles['TableHeader']),
         Paragraph("<b>Modality</b>", styles['TableHeader']),
         Paragraph("<b>Graph Model</b>", styles['TableHeader']),
         Paragraph("<b>Leakage Split</b>", styles['TableHeader']),
         Paragraph("<b>Agentic Pipeline</b>", styles['TableHeader']),
         Paragraph("<b>Maintainer UI</b>", styles['TableHeader'])],
        
        [Paragraph("Cubranic & Murphy (2004)", styles['TableCell']),
         Paragraph("Bag-of-Words", styles['TableCell']),
         Paragraph("None", styles['TableCell']),
         Paragraph("Random Split", styles['TableCell']),
         Paragraph("No", styles['TableCell']),
         Paragraph("No", styles['TableCell'])],
        
        [Paragraph("Anvik et al. (2006)", styles['TableCell']),
         Paragraph("TF-IDF Text", styles['TableCell']),
         Paragraph("None", styles['TableCell']),
         Paragraph("Random Split", styles['TableCell']),
         Paragraph("No", styles['TableCell']),
         Paragraph("No", styles['TableCell'])],
        
        [Paragraph("Devlin et al. / BERT (2019)", styles['TableCell']),
         Paragraph("Contextual Text", styles['TableCell']),
         Paragraph("None", styles['TableCell']),
         Paragraph("Random Split", styles['TableCell']),
         Paragraph("No", styles['TableCell']),
         Paragraph("No", styles['TableCell'])],
        
        [Paragraph("Kipf & Welling (2017)", styles['TableCell']),
         Paragraph("Graph Only", styles['TableCell']),
         Paragraph("Transductive GCN", styles['TableCell']),
         Paragraph("K-Fold Split", styles['TableCell']),
         Paragraph("No", styles['TableCell']),
         Paragraph("No", styles['TableCell'])],
        
        [Paragraph("SWE-bench / LLM (2024)", styles['TableCell']),
         Paragraph("Text / Code", styles['TableCell']),
         Paragraph("None", styles['TableCell']),
         Paragraph("Snapshot", styles['TableCell']),
         Paragraph("Monolithic", styles['TableCell']),
         Paragraph("CLI Only", styles['TableCell'])],
        
        [Paragraph("<b>Bug Triage AI (Proposed)</b>", styles['TableCellBold']),
         Paragraph("<b>Multi-Modal (Text + Graph + Label)</b>", styles['TableCellBold']),
         Paragraph("<b>Inductive GraphSAGE (Dynamic K-NN)</b>", styles['TableCellBold']),
         Paragraph("<b>Strict Temporal Zero-Leakage</b>", styles['TableCellBold']),
         Paragraph("<b>LangGraph Multi-Node</b>", styles['TableCellBold']),
         Paragraph("<b>React + Vite (10 Screens)</b>", styles['TableCellBold'])],
    ]

    t_comp = Table(comp_data, colWidths=[95, 80, 80, 65, 55, 58])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#EFF6FF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>2.3 Research Gap / Limitations of Existing System</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "A critical analysis of the current literature exposes four foundational research gaps:", styles['ReportBody']
    ))
    story.append(Spacer(1, 3))

    gaps = [
        ("<b>Pervasive Chronological Lookahead Bias:</b> ",
         "The overwhelming majority of published software triage papers partition datasets via uniform random "
         "shuffling. This allows issues resolved in 2024 to train models predicting issues reported in 2021. In real-world "
         "software maintenance, temporal causality is non-negotiable: models cannot utilize future vocabulary or graphs."),
        ("<b>The Inductive Cold-Start Graph Dilemma:</b> ",
         "Existing graph-based code classifiers assume that every query node already resides within a static, pre-existing "
         "graph. However, when an external contributor opens a brand-new issue, it has zero incoming or outgoing citations. "
         "Prior methods fail to generate valid graph structural embeddings for such unlinked nodes."),
        ("<b>Diagnostic Blindness:</b> ",
         "Standard ML classifiers treat bug triaging purely as a classification problem, without evaluating whether the "
         "bug report is actionable. Attempting to assign an un-reproducible report wastes maintainer bandwidth.")
    ]
    for title, desc in gaps:
        story.append(Paragraph(f"• {title}{desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2 - LITERATURE SURVEY (Page 8 / Physical Page 16)
    # =========================================================================
    story.append(Paragraph(
        "• <b>Absence of Maintainer-Centric Delivery Interfaces:</b> State-of-the-art models published in SE conferences "
        "rarely progress beyond Jupyter notebooks or raw command-line interfaces. Maintainers require production-grade "
        "web dashboards equipped with split-view issue review, one-click comment copying, similar issue correlation, "
        "and configurable theme settings.", styles['ReportBullet']
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2.4 Proposed System / Proposed Approach</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    prop1 = (
        "To decisively overcome these research gaps, <b>Bug Triage AI</b> introduces a unified, multi-modal, "
        "and leakage-free artificial intelligence platform. The system operates on four key architectural innovations:"
    )
    story.append(Paragraph(prop1, styles['ReportBody']))
    story.append(Spacer(1, 4))

    prop_items = [
        ("<b>1. Multi-Modal Feature Concatenation (519 Dimensions):</b> ",
         "The classifier combines dense semantic sentence embeddings (384d from <code>all-MiniLM-L6-v2</code>), "
         "topological graph representations (128d from <code>GraphSAGE</code>), and training-neighbor empirical label priors "
         "(7d) into a fused multi-modal vector: x = [v_text || v_graph || v_label]. This fusion achieves a test Macro-F1 of "
         "<b>0.7485</b>, outperforming single-modality baselines."),
        ("<b>2. Inductive Cold-Start Subgraph Projection:</b> ",
         "For new, unlinked bug reports, the system queries the ChromaDB vector index to identify the top K=5 semantic "
         "neighbors from the historical training split. It dynamically constructs a local inference subgraph connecting the "
         "test issue to these neighbors, allowing the 2-layer GraphSAGE network to compute structural graph representations "
         "at runtime without model retraining."),
        ("<b>3. Zero-Leakage Chronological Partitioning:</b> ",
         "All dataset preprocessing strictly enforces temporal boundaries: max(T_train) &le; min(T_val) &le; min(T_test). "
         "All semantic index construction and GraphSAGE neighborhood samplers are restricted entirely to training-split data."),
        ("<b>4. LangGraph Stateful Multi-Agent Pipeline:</b> ",
         "A cyclical state machine orchestrates the lifecycle: text intake sanitization &rarr; diagnostic completeness audit "
         "&rarr; cold-start vector search &rarr; hybrid LightGBM classification &rarr; confidence-gated comment drafting (&ge; 60% "
         "threshold) &rarr; maintainer review in an interactive 10-screen React workspace.")
    ]
    for title, desc in prop_items:
        story.append(Paragraph(f"{title}{desc}", styles['ReportBody']))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    return story
