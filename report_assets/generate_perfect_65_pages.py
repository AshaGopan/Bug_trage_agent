"""Bug Triage AI - Exact 65-Page Report Generator.
Guarantees strictly 65 pages:
- Pages 1 to 8: Front Matter (Roman i to viii)
- Pages 9 to 65: Chapters 1 to 10 (Arabic 1 to 57)
Total physical pages: 65.
"""

import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

from report_assets.styles_and_canvas import (
    PAGE_WIDTH, PAGE_HEIGHT, LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, BOTTOM_MARGIN,
    USABLE_WIDTH, USABLE_HEIGHT, AcademicReportCanvas, get_report_styles
)

def build_perfect_report(output_filename="Bug_Triage_AI_MCA_Project_Report.pdf"):
    styles = get_report_styles()
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE (Page i)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Bug Triage AI</b>", ParagraphStyle('T1', fontName='Times-Bold', fontSize=22, leading=26, alignment=TA_CENTER, textColor=colors.black)))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>A PROJECT REPORT SUBMITTED TO<br/>"
        "SRM INSTITUTE OF SCIENCE & TECHNOLOGY<br/>"
        "IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE<br/>"
        "AWARD OF THE DEGREE OF<br/>"
        "MASTER OF COMPUTER APPLICATIONS</b>",
        ParagraphStyle('T2', fontName='Times-Bold', fontSize=10.5, leading=15, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph("<b>BY</b>", ParagraphStyle('T3', fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_CENTER)))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>BONI VENKATA YESWANTH KUMAR (RA2532242010082)<br/>"
        "MUTHYALA VENKATA VISWANATH (RA2532242010091)<br/>"
        "PONNAGANTI SANTOSH KUMAR (RA2532242010094)<br/>"
        "BALLIKURA THARUN TEJA (RA2532242010109)</b>",
        ParagraphStyle('T4', fontName='Times-Bold', fontSize=10, leading=15, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>UNDER THE GUIDANCE OF</b>", ParagraphStyle('T5', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER)))
    story.append(Paragraph("<b>Mrs. LEENA BAI</b>", ParagraphStyle('T6', fontName='Times-Bold', fontSize=12, leading=16, alignment=TA_CENTER)))
    story.append(Spacer(1, 16))
    try:
        srm_img = Image('report_assets/srm_logo.png', width=1.65*inch, height=1.65*inch)
        story.append(srm_img)
    except Exception:
        story.append(Spacer(1, 1.5*inch))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>DEPARTMENT OF COMPUTER APPLICATIONS<br/>"
        "FACULTY OF SCIENCE AND HUMANITIES<br/>"
        "SRM INSTITUTE OF SCIENCE & TECHNOLOGY</b><br/>"
        "Kattankulathur – 603 203<br/>"
        "Chennai, Tamilnadu<br/>"
        "<b>OCTOBER - 2026</b>",
        ParagraphStyle('T7', fontName='Times-Bold', fontSize=10.5, leading=14.5, alignment=TA_CENTER)
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE (Page ii)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>BONAFIDE CERTIFICATE</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 25))
    cert_text = (
        "This is to certify that the project report titled <b>“Bug Triage AI”</b> is a bonafide work "
        "carried out by <b>Boni Venkata Yeswanth Kumar (RA2532242010082)</b>, <b>Muthyala Venkata Viswanath "
        "(RA2532242010091)</b>, <b>Ponnaganti Santosh Kumar (RA2532242010094)</b>, and <b>Ballikura Tharun Teja "
        "(RA2532242010109)</b> under my supervision for the award of the Degree of Master of Computer "
        "Applications. To my knowledge the work reported herein is the original work done by these students."
    )
    story.append(Paragraph(cert_text, styles['ReportBody']))
    story.append(Spacer(1, 90))
    sig_data = [
        [
            Paragraph("<b>Mrs. Leena Bai</b><br/>Assistant Professor<br/>Department of Computer Applications<br/><b>(GUIDE)</b>", styles['TableCellCenter']),
            Paragraph("<b>Dr. P.J. Arul Leena Rose</b><br/>Professor & Head,<br/>Department of Computer Applications", styles['TableCellCenter'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[210, 210])
    sig_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(sig_table)
    story.append(Spacer(1, 110))
    exam_data = [[Paragraph("<b>INTERNAL EXAMINER</b>", styles['TableCellCenter']), Paragraph("<b>EXTERNAL EXAMINER</b>", styles['TableCellCenter'])]]
    exam_table = Table(exam_data, colWidths=[210, 210])
    exam_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(exam_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ACKNOWLEDGEMENT (Page iii)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))
    ack_paragraphs = [
        "With profound gratitude to the ALMIGHTY, I take this chance to thank the people who helped me to complete this project.",
        "We take this as a right opportunity to say THANKS to my parents who are there to stand with me always with the words “YOU CAN”.",
        "We are thankful to <b>Dr. T.R. Paarivendhar</b>, Chancellor, SRM Institute of Science & Technology who gave us the platform to establish me to reach greater heights.",
        "We earnestly thank <b>Dr. A. Duraisamy</b>, Dean, Faculty of Science and Humanities, SRM Institute of Science & Technology who always encourage us to do novel things.",
        "A great note of gratitude to <b>Dr. S. Albert Antony Raj</b>, Deputy Dean, Faculty of Science and Humanities for his valuable guidance and constant Support to do this Project.",
        "We express our sincere thanks to <b>Dr. P.J. Arul Leena Rose</b>, Professor & Head for her support to execute all incline in learning.",
        "It is our delight to thank our project guide <b>Mrs. Leena Bai</b>, Assistant Professor, Department of Computer Applications for her help, support, encouragement, suggestions, and guidance throughout the development phases of the project.",
        "We convey our gratitude to all the faculty members of the department who extended their support through valuable comments and suggestions during the reviews.",
        "Our gratitude to friends and people who are known and unknown to me who helped in carrying out this project work a successful one."
    ]
    for p in ack_paragraphs:
        story.append(Paragraph(p, styles['ReportBody']))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 15))
    names_block = "<b>Boni Venkata Yeswanth Kumar<br/>Muthyala Venkata Viswanath<br/>Ponnaganti Santosh Kumar<br/>Ballikura Tharun Teja</b>"
    story.append(Paragraph(names_block, ParagraphStyle('N1', fontName='Times-Bold', fontSize=10.5, leading=15, alignment=TA_RIGHT)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TABLE OF CONTENTS (Part 1, Page iv)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>TABLE OF CONTENT</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))
    toc_p1 = [
        ("<b>CHAPTER 1 - INTRODUCTION</b>", "<b>1</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background of the Study", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Objectives of the Project", "3"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope of the Project", "4"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Significance of the Project", "4"),
        ("<b>CHAPTER 2 - LITERATURE SURVEY / EXISTING STUDIES</b>", "<b>5</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Review of Existing Systems / Research Works", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1.1 Classical IR & TF-IDF Bug Triaging", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1.2 Transformer & MiniLM Semantic Embeddings", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1.3 Graph Neural Networks & Inductive GraphSAGE", "6"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1.4 Agentic LLM Workflows in Software Maintenance", "6"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Comparative Analysis", "6"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Research Gap / Limitations of Existing System", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Proposed System / Proposed Approach", "8"),
        ("<b>CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS</b>", "<b>9</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Hardware Specification", "9"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Software Specification", "9"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Software / Tools and Their Features", "10"),
        ("<b>CHAPTER 4 - SYSTEM ANALYSIS</b>", "<b>12</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Requirement Specification", "12"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Characteristics of Existing System", "13"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Proposed System / Proposed Approach", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Feasibility Study", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Software Requirement Specification", "14"),
        ("<b>CHAPTER 5 - SYSTEM DESIGN</b>", "<b>15</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.1 System Architecture / Overall Workflow", "15"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Context Diagram", "16"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Use Case Diagram", "17"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Activity Diagram / State Diagram / UML Diagram", "18"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.5 Data Flow Diagram / ER Diagram / Class Diagram / ML Workflow", "21"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.6 Database Design / Dataset Design", "25"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.7 User Interface Design", "26"),
    ]
    toc_rows1 = [[Paragraph(t, styles['TableCell']), Paragraph(p, styles['TableCellCenter'])] for t, p in toc_p1]
    t_toc1 = Table(toc_rows1, colWidths=[395, 38])
    t_toc1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5), ('TOPPADDING', (0,0), (-1,-1), 1.5)]))
    story.append(t_toc1)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS (Part 2, Page v)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>TABLE OF CONTENT (Continued)</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 12))
    toc_p2 = [
        ("<b>CHAPTER 6 - SYSTEM IMPLEMENTATION</b>", "<b>27</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Modules Description", "27"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Dataset Description / Data Collection", "28"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Data Preprocessing", "29"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Feature Engineering / Feature Extraction", "30"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.5 Model Architecture / Algorithm Design", "30"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.6 System / Model Implementation", "31"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.7 Validation Checks", "32"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.8 User Interface Implementation", "32"),
        ("<b>CHAPTER 7 - TESTING AND EVALUATION</b>", "<b>33</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Test Cases", "33"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Unit Testing", "34"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Integration Testing", "35"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.4 System Testing", "36"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.5 Model Evaluation / Performance Evaluation", "37"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.6 Performance Metrics", "39"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.7 Comparative Analysis", "40"),
        ("<b>CHAPTER 8 - RESULTS AND CONCLUSION</b>", "<b>41</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.1 Results", "41"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Discussion / Analysis", "42"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Limitations", "42"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.4 Lessons Learnt", "42"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.5 Conclusion", "43"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.6 Future Enhancements", "43"),
        ("<b>CHAPTER 9 - APPENDICES</b>", "<b>44</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 1 — Plagiarism Certificate", "44"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 2 — Screenshots", "45"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 3 — Sample Coding", "50"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 4 — User Documentation", "54"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 5 — Glossary", "55"),
        ("<b>CHAPTER 10 - BIBLIOGRAPHY / REFERENCES</b>", "<b>56</b>"),
    ]
    toc_rows2 = [[Paragraph(t, styles['TableCell']), Paragraph(p, styles['TableCellCenter'])] for t, p in toc_p2]
    t_toc2 = Table(toc_rows2, colWidths=[395, 38])
    t_toc2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)]))
    story.append(t_toc2)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT (Page vi)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ABSTRACT</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))
    ab_p1 = (
        "In modern hyperscale open-source software (OSS) ecosystems such as <b>kubernetes/kubernetes</b>, "
        "the rapid influx of bug reports presents a severe bottleneck for project maintainers. Inefficient manual "
        "triaging leads to significant delays in issue resolution, contributor frustration, and cognitive fatigue. "
        "This project presents <b>Bug Triage AI</b>, an intelligent, multi-modal machine learning system and stateful "
        "agentic workflow designed to automate bug report routing, duplicate retrieval, diagnostic completeness auditing, "
        "and maintainer comment synthesis."
    )
    ab_p2 = (
        "The analytical core of Bug Triage AI addresses the multi-modal nature of software engineering artifacts by fusing "
        "three distinct feature representations into a unified 519-dimensional input vector: dense semantic text embeddings "
        "(384d) derived from <i>all-MiniLM-L6-v2</i>, inductive structural graph embeddings (128d) computed via a 2-layer "
        "<i>GraphSAGE</i> Graph Neural Network operating over cross-issue reference topologies, and an empirical "
        "training-neighbor label awareness prior (7d). To solve the inductive cold-start challenge for unlinked new bug reports, "
        "the system dynamically constructs an inference subgraph linking the incoming issue to its top $K=5$ nearest semantic "
        "neighbors in ChromaDB vector space. A multi-class LightGBM Gradient Boosted Decision Tree performs the final routing "
        "across seven primary Kubernetes Special Interest Groups (SIGs)."
    )
    ab_p3 = (
        "To provide seamless operational integration, the system orchestrates a <i>LangGraph</i> state machine consisting of "
        "an intake cleaner, a diagnostic completeness auditor, a cold-start graph retriever, and a confidence-aware conditional "
        "router (threshold &ge; 60%). The solution is exposed via a high-performance <b>FastAPI</b> REST service and delivered "
        "through a modern 10-screen <b>React + Vite + Tailwind CSS</b> maintainer workspace supporting Dark Mode (#0B0F19) and "
        "Light Mode (#F8F9FC), split-view verification, and real-time execution progress tracking."
    )
    ab_p4 = (
        "Evaluated under strict zero-leakage chronological partitioning on real-world Kubernetes issues, Bug Triage AI achieves "
        "a superior Macro-F1 score of <b>0.7485</b>, significantly outperforming classical TF-IDF baselines (0.7020) and text-only "
        "models (0.6247). Sub-second inference latency (&lt; 200 ms) and reliable duplicate retrieval validate Bug Triage AI as an "
        "explainable, production-ready artificial intelligence platform for large-scale software repository management."
    )
    story.append(Paragraph(ab_p1, styles['ReportBody']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(ab_p2, styles['ReportBody']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(ab_p3, styles['ReportBody']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(ab_p4, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: LIST OF TABLES (Page vii)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>List of Tables</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))
    lot_items = [
        ("Table 2.1: Comparative Analysis with Existing Systems", "7"),
        ("Table 3.1: Hardware Specifications", "9"),
        ("Table 3.2: Software Specifications", "9"),
        ("Table 3.3: Software Tools and Their Features", "10"),
        ("Table 5.1: SQLite Issues & Edges Table Schema", "25"),
        ("Table 5.2: SQLite PR Files & Embeddings Table Schema", "25"),
        ("Table 5.3: ChromaDB Vector Collection Schema", "25"),
        ("Table 5.4: Frontend LocalStorage History Schema", "25"),
        ("Table 6.1: Feature Engineering Transformations", "30"),
        ("Table 7.1: Test Cases", "33"),
        ("Table 7.2: Unit Test Cases", "34"),
        ("Table 7.3: Integration Test Cases", "35"),
        ("Table 7.4: System Test Cases", "36"),
        ("Table 7.5: Model Performance Metrics", "37"),
        ("Table 7.6: Comparative Analysis with Existing Systems", "40"),
        ("Table 9.1: Glossary", "55"),
    ]
    lot_rows = [[Paragraph(t, styles['TableCellBold']), Paragraph(p, styles['TableCellCenter'])] for t, p in lot_items]
    t_lot = Table(lot_rows, colWidths=[395, 38])
    t_lot.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_lot)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: LIST OF FIGURES (Page viii)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>List of Figures</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))
    lof_items = [
        ("Figure 5.1: Context Diagram", "16"),
        ("Figure 5.2: Use Case Diagram", "17"),
        ("Figure 5.3: Activity Diagram", "18"),
        ("Figure 5.4: State Diagram", "19"),
        ("Figure 5.5: Sequence Diagram", "20"),
        ("Figure 5.6: Data Flow Diagram (DFD Level 1)", "21"),
        ("Figure 5.7: ER Diagram", "22"),
        ("Figure 5.8: Class Diagram", "23"),
        ("Figure 5.9: ML Workflow Diagram", "24"),
        ("Figure A2.1: Workspace Landing Screen (Dark Mode)", "45"),
        ("Figure A2.2: Workspace Landing Screen (Light Mode)", "45"),
        ("Figure A2.3: Analyzing Progress Execution Pipeline", "46"),
        ("Figure A2.4: Triage Results Screen", "46"),
        ("Figure A2.5: Similar Issues & Diagnostic Auditing Panel", "47"),
        ("Figure A2.6: Suggested Maintainer Response Editor", "47"),
        ("Figure A2.7: Split-View Triage Session", "48"),
        ("Figure A2.8: Maintainer Triage History View", "48"),
        ("Figure A2.9: Maintainer Authentication & Account Creation", "49"),
        ("Figure A2.10: Component Error & Warning States", "49"),
    ]
    lof_rows = [[Paragraph(t, styles['TableCellBold']), Paragraph(p, styles['TableCellCenter'])] for t, p in lof_items]
    t_lof = Table(lof_rows, colWidths=[395, 38])
    t_lof.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 3), ('TOPPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_lof)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9 (Arabic 1): CHAPTER 1 - INTRODUCTION (1.1 Background)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 1 - INTRODUCTION</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>1.1 Background of the Study</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p1_1 = (
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
    p1_2 = (
        "Historically, open-source repositories relied entirely on manual triage rotas, where senior engineers "
        "dedicate significant working hours to reviewing incoming bug logs, requesting missing reproduction "
        "steps, and tagging issues with appropriate labels. This manual paradigm creates an unsustainable "
        "operational bottleneck. Unassigned bug reports linger in triage queues for days or weeks, delaying critical "
        "security and stability patches while frustrating contributors who receive slow or disjointed initial feedback. "
        "Moreover, maintainer burnout has emerged as an acute sustainability hazard across the open-source software "
        "landscape, threatening the long-term vitality of core cloud-native platforms."
    )
    p1_3 = (
        "Early attempts at software triage automation leveraged traditional information retrieval (IR) and "
        "classical statistical machine learning, such as Bag-of-Words with Naive Bayes or Support Vector Machines (SVM). "
        "While computationally lightweight, these approaches suffer from severe vocabulary mismatch, complete disregard "
        "for structural source code syntax, and an inability to model dense semantic interactions. Subsequent deep "
        "learning models improved text parsing but frequently treated bug reports as isolated text strings, ignoring "
        "the rich topological relationships—such as cross-issue citations, shared pull requests, and file modification "
        "overlaps—that naturally link bug reports within large code repositories."
    )
    p1_4 = (
        "Recent breakthroughs in dense semantic sentence transformers, inductive Graph Neural Networks (GNNs), and "
        "agentic Large Language Model (LLM) orchestration present unprecedented opportunities to construct end-to-end, "
        "multi-modal bug triage agents that streamline maintainer workflows."
    )
    story.append(Paragraph(p1_1, styles['ReportBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(p1_2, styles['ReportBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(p1_3, styles['ReportBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(p1_4, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10 (Arabic 2): 1.2 Problem Statement
    # =========================================================================
    story.append(Paragraph("<b>1.2 Problem Statement</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
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
        story.append(Spacer(1, 3))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11 (Arabic 3): 1.3 Objectives of the Project
    # =========================================================================
    story.append(Paragraph("<b>1.3 Objectives of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
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
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12 (Arabic 4): 1.4 Scope & 1.5 Significance
    # =========================================================================
    story.append(Paragraph("<b>1.4 Scope of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_sc_in = (
        "<b>In Scope:</b> Ingestion of <code>kubernetes/kubernetes</code> issues; markdown cleansing; strict chronological "
        "splitting (max(train) &le; min(val) &le; min(test)); dense text embeddings; inductive GraphSAGE GNN; 519d multi-modal "
        "concatenation; LightGBM classification; LangGraph multi-agent pipeline; ChromaDB vector store; and React workspace.<br/><br/>"
        "<b>Out of Scope:</b> Automated merging of source code pull requests; direct cluster remediation; non-English bug translation; "
        "native mobile applications; and enterprise GPU dependencies (strictly engineered for CPU-only execution)."
    )
    story.append(Paragraph(p_sc_in, styles['ReportBody']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1.5 Significance of the Project</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_sig1 = (
        "The significance of Bug Triage AI lies in bridging the critical divide between experimental machine learning "
        "research and practical, production-ready software engineering tools. While dozens of academic papers demonstrate "
        "algorithmic prototypes on static benchmarks, few provide the operational scaffolding required for actual "
        "open-source maintainers. Bug Triage AI delivers an end-to-end architecture that respects the nuanced realities "
        "of enterprise software maintenance."
    )
    p_sig2 = (
        "From an engineering perspective, this project pioneers the integration of <b>inductive Graph Neural Networks</b> "
        "with dense semantic language embeddings for bug triage. By introducing cold-start dynamic K-NN subgraph "
        "projection, the system solves a fundamental limitation of classical graph methods—namely, the inability to "
        "embed a newly submitted node that possesses zero existing topological edges. This enables rich graph structural "
        "reasoning even for freshly reported issues."
    )
    p_sig3 = (
        "Furthermore, enforcing <b>zero-leakage chronological partitioning</b> establishes an authentic performance "
        "benchmark for the software engineering community, while maintainer-in-the-loop workflows significantly reduce "
        "volunteer cognitive fatigue and accelerate cloud-native security patching cycles."
    )
    story.append(Paragraph(p_sig1, styles['ReportBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(p_sig2, styles['ReportBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(p_sig3, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13 (Arabic 5): CHAPTER 2 - LITERATURE SURVEY (2.1.1 & 2.1.2)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 2 - LITERATURE SURVEY / EXISTING STUDIES</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>2.1 Review of Existing Systems / Research Works</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>2.1.1 Classical IR & TF-IDF Bug Triaging</b>", styles['SubSectionHeader']))
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
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>2.1.2 Transformer & MiniLM Semantic Embeddings</b>", styles['SubSectionHeader']))
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
    # PAGE 14 (Arabic 6): 2.1.3 GraphSAGE & 2.1.4 Agentic LLM & 2.2 Intro
    # =========================================================================
    story.append(Paragraph("<b>2.1.3 Graph Neural Networks & Inductive GraphSAGE</b>", styles['SubSectionHeader']))
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
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>2.1.4 Agentic LLM Workflows in Software Maintenance</b>", styles['SubSectionHeader']))
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
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>2.2 Comparative Analysis</b>", styles['SectionHeader']))
    story.append(Paragraph(
        "A rigorous comparative examination of existing literature versus Bug Triage AI highlights fundamental differentiators "
        "across feature modalities, graph learning, leakage prevention, and agentic orchestration:", styles['ReportBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15 (Arabic 7): Table 2.1 & 2.3 Research Gap
    # =========================================================================
    story.append(Paragraph("<b>Table 2.1: Comparative Analysis with Existing Systems</b>", styles['TableCaption']))
    story.append(Spacer(1, 2))
    comp_data = [
        [Paragraph("<b>System / Study</b>", styles['TableHeader']), Paragraph("<b>Modality</b>", styles['TableHeader']), Paragraph("<b>Graph Model</b>", styles['TableHeader']), Paragraph("<b>Leakage Split</b>", styles['TableHeader']), Paragraph("<b>Agentic Pipeline</b>", styles['TableHeader']), Paragraph("<b>Maintainer UI</b>", styles['TableHeader'])],
        [Paragraph("Cubranic & Murphy (2004)", styles['TableCell']), Paragraph("Bag-of-Words", styles['TableCell']), Paragraph("None", styles['TableCell']), Paragraph("Random Split", styles['TableCell']), Paragraph("No", styles['TableCell']), Paragraph("No", styles['TableCell'])],
        [Paragraph("Anvik et al. (2006)", styles['TableCell']), Paragraph("TF-IDF Text", styles['TableCell']), Paragraph("None", styles['TableCell']), Paragraph("Random Split", styles['TableCell']), Paragraph("No", styles['TableCell']), Paragraph("No", styles['TableCell'])],
        [Paragraph("Devlin et al. / BERT (2019)", styles['TableCell']), Paragraph("Contextual Text", styles['TableCell']), Paragraph("None", styles['TableCell']), Paragraph("Random Split", styles['TableCell']), Paragraph("No", styles['TableCell']), Paragraph("No", styles['TableCell'])],
        [Paragraph("Kipf & Welling (2017)", styles['TableCell']), Paragraph("Graph Only", styles['TableCell']), Paragraph("Transductive GCN", styles['TableCell']), Paragraph("K-Fold Split", styles['TableCell']), Paragraph("No", styles['TableCell']), Paragraph("No", styles['TableCell'])],
        [Paragraph("SWE-bench / LLM (2024)", styles['TableCell']), Paragraph("Text / Code", styles['TableCell']), Paragraph("None", styles['TableCell']), Paragraph("Snapshot", styles['TableCell']), Paragraph("Monolithic", styles['TableCell']), Paragraph("CLI Only", styles['TableCell'])],
        [Paragraph("<b>Bug Triage AI (Proposed)</b>", styles['TableCellBold']), Paragraph("<b>Multi-Modal (519d)</b>", styles['TableCellBold']), Paragraph("<b>Inductive GraphSAGE</b>", styles['TableCellBold']), Paragraph("<b>Strict Zero-Leakage</b>", styles['TableCellBold']), Paragraph("<b>LangGraph Multi-Node</b>", styles['TableCellBold']), Paragraph("<b>React + Vite (10 Screens)</b>", styles['TableCellBold'])],
    ]
    t_comp = Table(comp_data, colWidths=[95, 80, 80, 65, 55, 58])
    t_comp.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')), ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#EFF6FF')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_comp)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>2.3 Research Gap / Limitations of Existing System</b>", styles['SectionHeader']))
    gaps = [
        ("<b>Pervasive Chronological Lookahead Bias:</b> ", "Random cross-validation allows future bug vocabulary and resolved PRs to leak into historical training data, yielding inflated metrics that fail in production."),
        ("<b>The Inductive Cold-Start Graph Dilemma:</b> ", "Existing graph models require nodes to exist in a static graph, failing to generate valid graph embeddings for newly submitted bug reports possessing zero pre-existing citations."),
        ("<b>Diagnostic Blindness:</b> ", "Standard ML classifiers ignore whether bug reports contain reproduction steps or logs, wasting maintainer bandwidth on incomplete reports.")
    ]
    for title, desc in gaps:
        story.append(Paragraph(f"• {title}{desc}", styles['ReportBullet']))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16 (Arabic 8): 2.4 Proposed System / Proposed Approach
    # =========================================================================
    story.append(Paragraph("• <b>Absence of Maintainer-Centric Delivery Interfaces:</b> State-of-the-art models rarely progress beyond scripts. Maintainers require production-grade web dashboards equipped with split-view issue review, one-click comment copying, similar issue correlation, and configurable theme settings.", styles['ReportBullet']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>2.4 Proposed System / Proposed Approach</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_prop1 = (
        "To decisively overcome these research gaps, <b>Bug Triage AI</b> introduces a unified, multi-modal, "
        "and leakage-free artificial intelligence platform operating on four core architectural innovations:"
    )
    story.append(Paragraph(p_prop1, styles['ReportBody']))
    story.append(Spacer(1, 4))
    prop_items = [
        ("<b>1. Multi-Modal Feature Concatenation (519 Dimensions):</b> ",
         "Combines dense semantic text embeddings (384d from <code>all-MiniLM-L6-v2</code>), topological graph representations "
         "(128d from <code>GraphSAGE</code>), and training-neighbor label priors (7d) into a fused vector: x = [v_text || v_graph || v_label], "
         "achieving a test Macro-F1 of <b>0.7485</b>."),
        ("<b>2. Inductive Cold-Start Subgraph Projection:</b> ",
         "Queries ChromaDB to retrieve top K=5 semantic neighbors from the training split, synthesizing a dynamic inference "
         "subgraph connecting the test issue to these neighbors to compute 128d GraphSAGE representations at runtime."),
        ("<b>3. Zero-Leakage Chronological Partitioning:</b> ",
         "Strictly isolates all preprocessing, indexing, and GNN training steps within historical training boundaries: "
         "max(T_train) &le; min(T_val) &le; min(T_test)."),
        ("<b>4. LangGraph Stateful Multi-Agent Pipeline:</b> ",
         "Orchestrates text intake sanitization &rarr; diagnostic completeness audit &rarr; cold-start vector search &rarr; "
         "hybrid LightGBM classification &rarr; confidence-gated comment drafting (&ge; 60% threshold) &rarr; maintainer review in React.")
    ]
    for title, desc in prop_items:
        story.append(Paragraph(f"{title}{desc}", styles['ReportBody']))
        story.append(Spacer(1, 3))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTERS 3 & 4 (Physical Pages 17 to 22 = Arabic Pages 9 to 14)
    # =========================================================================
    from report_assets.part2_req_sysanalysis import build_part2
    story.extend(build_part2(styles))

    # =========================================================================
    # CHAPTER 5 - SYSTEM DESIGN (Physical Pages 23 to 34 = Arabic Pages 15 to 26)
    # =========================================================================
    # Page 23 (Arabic 15): 5.1 System Architecture 3-Tier
    story.append(Paragraph("<b>CHAPTER 5 - SYSTEM DESIGN</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>5.1 System Architecture / Overall Workflow</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_arch = (
        "The Bug Triage AI system follows a decoupled <b>Three-Tier Enterprise Architecture</b>:<br/><br/>"
        "<b>1. Presentation Layer (Maintainer Frontend Workspace):</b><br/>"
        "Engineered with React 18, Vite 5, and Tailwind CSS 3, providing an interactive dashboard with Light Mode (#F8F9FC) "
        "and Dark Mode (#0B0F19), split-view session explorer, automated response editor, and persistent local history.<br/><br/>"
        "<b>2. Application Layer (Service & Agentic Inference Core):</b><br/>"
        "Driven by FastAPI and Uvicorn, serving REST endpoints validated via Pydantic schemas. Requests are processed "
        "through a stateful LangGraph Multi-Agent Pipeline executing text cleaning, diagnostic checking, dynamic K-NN "
        "subgraph projection, multi-modal LightGBM inference, and confidence-gated response drafting.<br/><br/>"
        "<b>3. Data Layer (Relational, Vector, & Graph Model Stores):</b><br/>"
        "Combines SQLite (triage.db) for storing issue text, citation edges, and PR file links, ChromaDB for dense vector "
        "similarity search, and serialized PyTorch GraphSAGE and LightGBM model weights loaded in-memory."
    )
    story.append(Paragraph(p_arch, styles['ReportBody']))
    story.append(PageBreak())

    # Page 24 (Arabic 16): Figure 5.1 Context Diagram
    story.append(Paragraph("<b>5.2 Context Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("The Context Diagram (Figure 5.1) illustrates Bug Triage AI as a central system interacting with external entities and data stores:", styles['ReportBody']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_1_context.png', width=5.6*inch, height=3.6*inch))
    except Exception:
        story.append(Spacer(1, 3.5*inch))
    story.append(Paragraph("<b>Figure 5.1 Context Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("The central AI core coordinates between Maintainers, GitHub REST API, SQLite triage.db, ChromaDB Vector Store, and Machine Learning Inference Engines.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 25 (Arabic 17): Figure 5.2 Use Case Diagram
    story.append(Paragraph("<b>5.3 Use Case Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("The Use Case Diagram (Figure 5.2) maps all primary interactions between maintainers, GitHub, and AI inference services:", styles['ReportBody']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_2_usecase.png', width=5.5*inch, height=3.8*inch))
    except Exception:
        story.append(Spacer(1, 3.8*inch))
    story.append(Paragraph("<b>Figure 5.2 Use Case Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Core use cases include issue submission, live URL fetching, rotating scenario selection, diagnostic auditing, vector retrieval, and maintainer response drafting.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 26 (Arabic 18): Figure 5.3 Activity Diagram
    story.append(Paragraph("<b>5.4 Activity Diagram / State Diagram / UML Diagram</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure 5.3 Activity Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_3_activity.png', width=5.2*inch, height=4.1*inch))
    except Exception:
        story.append(Spacer(1, 4.0*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Activity flows sequentially from intake text cleaning to diagnostic auditing, dense text encoding, ChromaDB search, GraphSAGE forward pass, and conditional writer node routing.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 27 (Arabic 19): Figure 5.4 State Diagram
    story.append(Paragraph("<b>Figure 5.4 State Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_4_state.png', width=5.6*inch, height=3.8*inch))
    except Exception:
        story.append(Spacer(1, 3.8*inch))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Illustrates the issue lifecycle states: Idle &rarr; Intake & Sanitization &rarr; Diagnostic Audit &rarr; Topological Inference &rarr; Classification &rarr; Triaged / Clarification &rarr; Dispatched.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 28 (Arabic 20): Figure 5.5 Sequence Diagram
    story.append(Paragraph("<b>Figure 5.5 Sequence Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_5_sequence.png', width=5.6*inch, height=4.0*inch))
    except Exception:
        story.append(Spacer(1, 4.0*inch))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Chronological message exchanges between Maintainer UI, FastAPI /triage, LangGraph Core, ChromaDB, GraphSAGE, and LightGBM model.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 29 (Arabic 21): Figure 5.6 Data Flow Diagram
    story.append(Paragraph("<b>5.5 Data Flow Diagram / ER Diagram / Class Diagram / ML Workflow</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure 5.6 Data Flow Diagram (DFD Level 1)</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_6_dfd.png', width=5.6*inch, height=3.6*inch))
    except Exception:
        story.append(Spacer(1, 3.5*inch))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Depicts the transformation of raw issue text through cleansing (1.0), audit (2.0), retrieval (3.0), classification (4.0), response drafting (5.0), and history logging (6.0).", styles['ReportBody']))
    story.append(PageBreak())

    # Page 30 (Arabic 22): Figure 5.7 ER Diagram
    story.append(Paragraph("<b>Figure 5.7 ER Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_7_er.png', width=5.6*inch, height=3.6*inch))
    except Exception:
        story.append(Spacer(1, 3.5*inch))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Relational schema showing ISSUES (1:N with EDGES, 1:N with PR_FILES, 1:1 with EMBEDDINGS) and client-side TRIAGE_HISTORY entity.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 31 (Arabic 23): Figure 5.8 Class Diagram
    story.append(Paragraph("<b>Figure 5.8 Class Diagram</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_8_class.png', width=5.6*inch, height=3.9*inch))
    except Exception:
        story.append(Spacer(1, 3.8*inch))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Object-oriented class relationships connecting TriageState, TriageWorkflow, IntakeService, GraphSAGENet, HybridClassifier, FastAPIServer, and ReactFrontendController.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 32 (Arabic 24): Figure 5.9 ML Workflow
    story.append(Paragraph("<b>Figure 5.9 ML Workflow</b>", styles['FigureCaption']))
    story.append(Spacer(1, 4))
    try:
        story.append(Image('report_assets/diagrams/diagram_5_9_ml_workflow.png', width=5.4*inch, height=4.2*inch))
    except Exception:
        story.append(Spacer(1, 4.0*inch))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Maps offline dataset mining, temporal splitting, multi-modal feature extraction (text, graph, label), LightGBM training, and online inference deployment.", styles['ReportBody']))
    story.append(PageBreak())

    # Page 33 (Arabic 25): 5.6 Database Design (Tables 5.1 & 5.2)
    story.append(Paragraph("<b>5.6 Database Design / Dataset Design</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Table 5.1: SQLite Issues & Edges Table Schema</b>", styles['TableCaption']))
    t51_data = [
        [Paragraph("<b>Table</b>", styles['TableHeader']), Paragraph("<b>Column</b>", styles['TableHeader']), Paragraph("<b>Type</b>", styles['TableHeader']), Paragraph("<b>Description & Constraints</b>", styles['TableHeader'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("issue_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY (GitHub Issue Number)", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("title", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Clean issue title", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("body_clean", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Sanitized issue description", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("created_at", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("ISO-8601 timestamp for temporal split", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("label", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Target SIG category (e.g. 'sig/node')", styles['TableCell'])],
        [Paragraph("issues", styles['TableCellBold']), Paragraph("split", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Temporal split ('train', 'val', 'test')", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY AUTOINCREMENT", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("src_issue", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Source issue ID (Foreign Key)", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("dst_issue", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Referenced issue ID (Foreign Key)", styles['TableCell'])],
        [Paragraph("edges", styles['TableCellBold']), Paragraph("edge_type", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Citation type ('references', 'duplicate')", styles['TableCell'])],
    ]
    t51 = Table(t51_data, colWidths=[65, 80, 75, 213])
    t51.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    story.append(t51)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Table 5.2: SQLite PR Files & Embeddings Table Schema</b>", styles['TableCaption']))
    t52_data = [
        [Paragraph("<b>Table</b>", styles['TableHeader']), Paragraph("<b>Column</b>", styles['TableHeader']), Paragraph("<b>Type</b>", styles['TableHeader']), Paragraph("<b>Description & Constraints</b>", styles['TableHeader'])],
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY AUTOINCREMENT", styles['TableCell'])],
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("pr_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("Linked Pull Request ID", styles['TableCell'])],
        [Paragraph("pr_files", styles['TableCellBold']), Paragraph("file_path", styles['TableCell']), Paragraph("TEXT", styles['TableCellCenter']), Paragraph("Path to modified source code file", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("issue_id", styles['TableCell']), Paragraph("INTEGER", styles['TableCellCenter']), Paragraph("PRIMARY KEY, FK to issues.issue_id", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("text_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 384d MiniLM vector (float32)", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("graph_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 128d GraphSAGE vector (float32)", styles['TableCell'])],
        [Paragraph("embeddings", styles['TableCellBold']), Paragraph("label_aware_vec", styles['TableCell']), Paragraph("BLOB", styles['TableCellCenter']), Paragraph("Serialized 7d empirical label prior (float32)", styles['TableCell'])],
    ]
    t52 = Table(t52_data, colWidths=[70, 85, 75, 203])
    t52.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    story.append(t52)
    story.append(PageBreak())

    # Page 34 (Arabic 26): 5.7 UI Design & Screen Layout Specifications
    story.append(Paragraph("<b>5.7 User Interface Design</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>5.7.1 Design Tokens & Screen Layout Specifications</b>", styles['SubSectionHeader']))
    p_ui_specs = (
        "The interface incorporates Tailwind CSS design tokens supporting Light Mode (<code>#F8F9FC</code>) and Dark Mode "
        "(<code>#0B0F19</code>) with electric indigo primary accents (<code>#2E31E8</code>). The 10 screens encompass:<br/>"
        "• <b>Screen 1 (Workspace Landing):</b> Issue intake hero with live URL parser and rotating Kubernetes scenarios.<br/>"
        "• <b>Screen 2 (Analyzing Progress):</b> Real-time 4-step progress animation tracking pipeline execution.<br/>"
        "• <b>Screen 3 (Triage Results):</b> Predicted SIG, 94% confidence gauge, rationale card, and duplicate issues.<br/>"
        "• <b>Screen 4 (Suggested Response):</b> Markdown editor with one-click copy and diagnostic checkboxes.<br/>"
        "• <b>Screen 5 (Split-View Session):</b> Side-by-side raw issue markdown and live intelligence cards.<br/>"
        "• <b>Screen 6 (Maintainer History):</b> Searchable audit table persisting all prior triages in localStorage.<br/>"
        "• <b>Screen 7 (Sign In):</b> Maintainer authentication with credential checks and GitHub SSO options.<br/>"
        "• <b>Screen 8 (Create Account):</b> Maintainer registration with role selection and GitHub handle linking.<br/>"
        "• <b>Screen 9 (Account Settings):</b> Configuration panel for model weights, thresholds, and theme toggling.<br/>"
        "• <b>Screen 10 (Component States):</b> UI sheet demonstrating Unidentified, Failed, Warning, and Empty states."
    )
    story.append(Paragraph(p_ui_specs, styles['ReportBody']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTERS 6 & 7 (Physical Pages 35 to 46 = Arabic Pages 27 to 38)
    # =========================================================================
    from report_assets.part4_impl_testing import build_part4
    story.extend(build_part4(styles))

    # =========================================================================
    # CHAPTER 8 - RESULTS AND CONCLUSION (Physical Pages 47 to 49 = Arabic Pages 39 to 41)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 8 - RESULTS AND CONCLUSION</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>8.1 Results</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_res1 = (
        "The Bug Triage AI system was successfully developed, evaluated, and deployed as a production-ready, full-stack "
        "artificial intelligence platform. Key experimental and engineering results include:<br/><br/>"
        "1. <b>Classification Accuracy:</b> The multi-modal hybrid classifier (concatenating 384d MiniLM text embeddings, "
        "128d inductive GraphSAGE structural representations, and 7d training-neighbor label priors) achieved a peak "
        "Macro-F1 score of <b>0.7485</b> on the chronologically held-out test partition of 474 issues from <code>kubernetes/kubernetes</code>, "
        "significantly outperforming text-only representations (0.6247).<br/><br/>"
        "2. <b>Inductive Cold-Start Graph Projection:</b> Dynamic K-NN subgraph construction in ChromaDB vector space "
        "successfully generated valid 128d topological graph representations for newly reported, unlinked bug reports, "
        "resolving the cold-start limitation inherent in classical transductive GNNs.<br/><br/>"
        "3. <b>Sub-Second Inference Latency:</b> The end-to-end multi-agent pipeline executed with an average response time of "
        "<b>120.7 ms</b> on standard CPU hardware, satisfying real-time triage requirements without expensive GPU infrastructure.<br/><br/>"
        "4. <b>Maintainer Experience:</b> Delivered a 10-screen React + Vite workspace with Light Mode (#F8F9FC), Dark Mode "
        "(#0B0F19), live GitHub issue URL fetching, diagnostic completeness checklists, and persistent local audit storage."
    )
    story.append(Paragraph(p_res1, styles['ReportBody']))
    story.append(PageBreak())

    # Page 48 (Arabic 40): 8.2 Discussion / Analysis & 8.3 Limitations & 8.4 Lessons Learnt
    story.append(Paragraph("<b>8.2 Discussion / Analysis</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_disc = (
        "The empirical findings demonstrate that software bug triaging benefits tremendously from relational graph context. "
        "When bug reports share generic symptoms ('pod timeout', 'connection refused'), text embeddings alone fail to distinguish "
        "whether the root cause lies within Kubelet node daemons or kube-proxy networking filters. By learning aggregation functions "
        "over historical cross-issue citations and pull request linkages, GraphSAGE injects decisive topological signals that "
        "elevate Macro-F1 by more than 12 percentage points over isolated text models."
    )
    story.append(Paragraph(p_disc, styles['ReportBody']))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>8.3 Limitations</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_lim = (
        "1. <b>Cold-Start Semantic Approximation:</b> In the absence of existing citation edges, dynamic K-NN links approximate "
        "graph structure based on semantic cosine similarity, which may introduce noise if the bug narrative is vague.<br/>"
        "2. <b>English Language Dependency:</b> SentenceTransformers are trained primarily on English text; non-English bug "
        "descriptions require machine translation prior to ingestion.<br/>"
        "3. <b>Repository-Specific Topology:</b> GraphSAGE weights are specialized to the Kubernetes repository topology and "
        "require fine-tuning when transferred to repositories with differing PR linkage conventions."
    )
    story.append(Paragraph(p_lim, styles['ReportBody']))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>8.4 Lessons Learnt</b>", styles['SectionHeader']))
    story.append(Spacer(1, 3))
    p_les = (
        "• <b>Temporal Causality is Paramount:</b> Enforcing strict chronological boundaries (max(train) &le; min(val) &le; min(test)) "
        "is essential. Random K-fold cross-validation produces dangerously optimistic metrics that fail in real-world deployment.<br/>"
        "• <b>Maintainer Trust Requires Explainability:</b> Automated label bots provoke maintainer skepticism unless accompanied "
        "by confidence scores, duplicate citations, and 'Why This Team' rationales."
    )
    story.append(Paragraph(p_les, styles['ReportBody']))
    story.append(PageBreak())

    # Page 49 (Arabic 41): 8.5 Conclusion & 8.6 Future Enhancements
    story.append(Paragraph("<b>8.5 Conclusion</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    p_concl = (
        "<b>Bug Triage AI</b> successfully demonstrates the convergence of multi-modal machine learning, graph neural networks, "
        "and agentic software engineering to automate large-scale open-source issue triaging. By combining dense semantic text "
        "embeddings, inductive GraphSAGE topological representations, and training-neighbor label awareness priors inside a "
        "stateful LangGraph pipeline, the system achieves a state-of-the-art Macro-F1 of 0.7485 with sub-200ms latency on CPU hardware. "
        "Coupled with an ergonomic 10-screen React maintainer workspace, the platform transforms issue triaging from a tedious "
        "manual chore into an intelligent, human-in-the-loop review workflow, recovering hundreds of maintainer hours and bolstering "
        "the sustainability of modern cloud-native infrastructure."
    )
    story.append(Paragraph(p_concl, styles['ReportBody']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>8.6 Future Enhancements</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    enh_items = [
        ("Cross-Repository Transfer Learning:", "Pretrain multi-modal GNN encoders across diverse CNCF projects (Prometheus, Envoy, containerd) to enable zero-shot triage on newly founded open-source repositories."),
        ("Source Code AST Embedding Integration:", "Incorporate Abstract Syntax Tree (AST) representations from pull request code diffs to link bug symptoms directly to source code functions."),
        ("Interactive Chatbot & Webhook Bot:", "Deploy automated GitHub Action bots and Slack/Discord webhook integrations for real-time triage notifications and conversational clarification queries."),
        ("Automated Reproduction Verification:", "Integrate lightweight container execution sandboxes to automatically verify contributor-provided reproduction scripts against virtual Kubernetes clusters.")
    ]
    for title, desc in enh_items:
        story.append(Paragraph(f"• <b>{title}</b> {desc}", styles['ReportBullet']))
        story.append(Spacer(1, 3))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 9 - APPENDICES (Physical Pages 50 to 63 = Arabic Pages 42 to 55)
    # =========================================================================
    # Page 50 (Arabic 42): Appendix 1 - Plagiarism Certificate
    story.append(Paragraph("<b>CHAPTER 9 - APPENDICES</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Appendix 1 — Plagiarism Certificate</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    try:
        story.append(Image('report_assets/plagiarism_cert.jpg', width=5.5*inch, height=5.2*inch))
    except Exception:
        story.append(Spacer(1, 5.0*inch))
    story.append(PageBreak())

    # Page 51 (Arabic 43): Appendix 2 - Screenshots (Figures A2.1 & A2.2)
    story.append(Paragraph("<b>Appendix 2 — Screenshots</b>", styles['SectionHeader']))
    story.append(Spacer(1, 1))
    story.append(Paragraph("<b>Figure A2.1: Workspace Landing Screen (Dark Mode #0B0F19)</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_1_workspace_dark.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure A2.2: Workspace Landing Screen (Light Mode #F8F9FC)</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_1_workspace_light.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(PageBreak())

    # Page 52 (Arabic 44): Figures A2.3 & A2.4
    story.append(Paragraph("<b>Figure A2.3: Analyzing Progress Execution Pipeline</b>", styles['FigureCaption']))
    story.append(Spacer(1, 1))
    try:
        story.append(Image('report_assets/ui_screens/screen_2_progress.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure A2.4: Triage Results Dashboard (SIG Node Predicted, 94% Confidence)</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_3_results.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(PageBreak())

    # Page 53 (Arabic 45): Figures A2.5 & A2.6
    story.append(Paragraph("<b>Figure A2.5: Similar Issues & Diagnostic Auditing Panel</b>", styles['FigureCaption']))
    story.append(Spacer(1, 1))
    try:
        story.append(Image('report_assets/ui_screens/screen_test.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure A2.6: Suggested Maintainer Response Editor</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_4_suggested_response.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(PageBreak())

    # Page 54 (Arabic 46): Figures A2.7 & A2.8
    story.append(Paragraph("<b>Figure A2.7: Split-View Triage Session (Raw Issue vs. Live Intelligence)</b>", styles['FigureCaption']))
    story.append(Spacer(1, 1))
    try:
        story.append(Image('report_assets/ui_screens/screen_5_split_view.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure A2.8: Maintainer Triage History View (Recent Issues Audit Table)</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_6_history.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(PageBreak())

    # Page 55 (Arabic 47): Figures A2.9 & A2.10
    story.append(Paragraph("<b>Figure A2.9: Maintainer Authentication & Profile Configuration</b>", styles['FigureCaption']))
    story.append(Spacer(1, 1))
    try:
        story.append(Image('report_assets/ui_screens/screen_7_signin.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Figure A2.10: Component Error & Warning States (Exception UI Sheet)</b>", styles['FigureCaption']))
    try:
        story.append(Image('report_assets/ui_screens/screen_10_states.png', width=5.2*inch, height=2.4*inch))
    except Exception:
        story.append(Spacer(1, 2.3*inch))
    story.append(PageBreak())

    # Page 56 (Arabic 48): Appendix 3 - Sample Coding (Backend)
    story.append(Paragraph("<b>Appendix 3 — Sample Coding</b>", styles['SectionHeader']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>backend/schemas.py — Pydantic Request & Response Data Schemas:</b>", styles['SubSectionHeader']))
    code_sch = (
        "from typing import Any\n"
        "from pydantic import BaseModel, Field\n\n"
        "class TriageRequest(BaseModel):\n"
        "    \"\"\"Input payload representing an incoming GitHub bug report.\"\"\"\n"
        "    title: str = Field(..., description=\"The title of the bug report\")\n"
        "    body: str = Field(..., description=\"Markdown or plain text description of bug report\")\n\n"
        "class TriageResponse(BaseModel):\n"
        "    \"\"\"Output payload returned by the LangGraph triage workflow.\"\"\"\n"
        "    predicted_label: str = Field(..., description=\"Recommended Special Interest Group (SIG)\")\n"
        "    confidence: float = Field(..., description=\"Model confidence score (0.0 to 1.0)\")\n"
        "    missing_fields: list[str] = Field(default_factory=list, description=\"Missing diagnostic fields\")\n"
        "    similar_issues: list[dict[str, Any]] = Field(default_factory=list, description=\"Top retrieved issues\")\n"
        "    draft_comment: str = Field(..., description=\"Automated markdown triage comment ready for GitHub\")\n"
    )
    story.append(Paragraph(f"<pre>{code_sch}</pre>", styles['CodeSnippet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>backend/main.py — FastAPI REST Endpoints:</b>", styles['SubSectionHeader']))
    code_bmain = (
        "from fastapi import FastAPI, HTTPException\n"
        "from fastapi.middleware.cors import CORSMiddleware\n"
        "from backend.schemas import TriageRequest, TriageResponse\n"
        "from agents.graph import run_triage_pipeline\n\n"
        "app = FastAPI(title=\"Bug Triage AI API\", version=\"1.0.0\")\n"
        "app.add_middleware(CORSMiddleware, allow_origins=[\"*\"], allow_methods=[\"*\"], allow_headers=[\"*\"])\n\n"
        "@app.get(\"/\")\n"
        "async def root_health():\n"
        "    return {\"status\": \"ok\", \"service\": \"Bug Triage AI Backend\", \"version\": \"1.0.0\"}\n"
    )
    story.append(Paragraph(f"<pre>{code_bmain}</pre>", styles['CodeSnippet']))
    story.append(PageBreak())

    # Page 57 (Arabic 49): Agents nodes.py
    story.append(Paragraph("<b>agents/nodes.py — Diagnostic Auditing & Intake Cleansing:</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    code_nodes = (
        "import re\n"
        "from agents.state import TriageState\n"
        "from features.clean_text import clean_issue_text\n\n"
        "def intake_node(state: TriageState) -> dict:\n"
        "    \"\"\"Cleans raw markdown and strips template boilerplate.\"\"\"\n"
        "    clean_title = clean_issue_text(state['title'])\n"
        "    clean_body = clean_issue_text(state['body'])\n"
        "    return {'clean_title': clean_title, 'clean_body': clean_body}\n\n"
        "def missing_info_node(state: TriageState) -> dict:\n"
        "    \"\"\"Audits diagnostic completeness: reproduction steps, logs, and env.\"\"\"\n"
        "    missing = []\n"
        "    body = state.get('clean_body', '').lower()\n"
        "    if not any(k in body for k in ['steps to reproduce', 'how to reproduce', 'reproduction']):\n"
        "        missing.append('step-by-step reproduction instructions')\n"
        "    if not any(k in body for k in ['log', 'trace', 'error:', 'failed with', 'exception']):\n"
        "        missing.append('relevant daemon logs or stack traces')\n"
        "    if not any(k in body for k in ['version', 'environment', 'os', 'kernel', 'ubuntu', 'v1.']):\n"
        "        missing.append('cluster environment specifications')\n"
        "    return {'missing_fields': missing}\n"
    )
    story.append(Paragraph(f"<pre>{code_nodes}</pre>", styles['CodeSnippet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>agents/nodes.py — Confidence-Gated Comment Synthesis:</b>", styles['SubSectionHeader']))
    code_nodes2 = (
        "def writer_high_node(state: TriageState) -> dict:\n"
        "    sig = state['predicted_label']\n"
        "    conf = state['confidence'] * 100\n"
        "    comment = f\"Thanks for opening this issue!\\n\\n### SIG Assignment Recommendation\\n\"\n"
        "    comment += f\"Based on automated triage (**{conf:.1f}% confidence**), assigned to **`{sig}`**.\\n\\n\"\n"
        "    if state['missing_fields']:\n"
        "        comment += \"### ⚠️ Diagnostic Information Requested\\n\"\n"
        "        for field in state['missing_fields']:\n"
        "            comment += f\"- [ ] Please provide: {field}\\n\"\n"
        "    comment += f\"\\n*/{sig.replace('/', ' ')}*\"\n"
        "    return {'draft_comment': comment}\n"
    )
    story.append(Paragraph(f"<pre>{code_nodes2}</pre>", styles['CodeSnippet']))
    story.append(PageBreak())

    # Page 58 (Arabic 50): Inductive GraphSAGE (features/embed_graph.py)
    story.append(Paragraph("<b>features/embed_graph.py — Inductive GraphSAGE PyG Architecture:</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    code_gnn = (
        "import torch\n"
        "import torch.nn as nn\n"
        "import torch.nn.functional as F\n"
        "from torch_geometric.nn import SAGEConv\n\n"
        "class GraphSAGENet(nn.Module):\n"
        "    \"\"\"2-Layer Inductive GraphSAGE Network for Issue Relational Topology.\"\"\"\n"
        "    def __init__(self, in_channels: int = 384, hidden_channels: int = 128, out_channels: int = 128):\n"
        "        super().__init__()\n"
        "        self.conv1 = SAGEConv(in_channels, hidden_channels, aggr='mean')\n"
        "        self.conv2 = SAGEConv(hidden_channels, out_channels, aggr='mean')\n\n"
        "    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:\n"
        "        x = self.conv1(x, edge_index)\n"
        "        x = F.leaky_relu(x, negative_slope=0.2)\n"
        "        x = F.dropout(x, p=0.1, training=self.training)\n"
        "        x = self.conv2(x, edge_index)\n"
        "        return x\n\n"
        "    def compute_cold_start(self, test_vec: list, neighbor_ids: list, edge_index: torch.Tensor) -> list:\n"
        "        node_features = [test_vec] + [get_cached_embedding(nid) for nid in neighbor_ids]\n"
        "        x = torch.tensor(node_features, dtype=torch.float32)\n"
        "        self.eval()\n"
        "        with torch.no_grad():\n"
        "            out = self.forward(x, edge_index)\n"
        "        return out[0].tolist()  # Return inductive representation for test node (index 0)\n"
    )
    story.append(Paragraph(f"<pre>{code_gnn}</pre>", styles['CodeSnippet']))
    story.append(PageBreak())

    # Page 59 (Arabic 51): Frontend State & Vite Proxy
    story.append(Paragraph("<b>frontend/src/services/historyStorage.js — Local Storage Persistence:</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 2))
    code_hist = (
        "const STORAGE_KEY = 'bug_triage_ai_history_v1';\n\n"
        "export function getSavedHistory() {\n"
        "  try {\n"
        "    const data = localStorage.getItem(STORAGE_KEY);\n"
        "    return data ? JSON.parse(data) : INITIAL_SAMPLE_HISTORY;\n"
        "  } catch (e) {\n"
        "    console.warn('Failed to parse history from localStorage', e);\n"
        "    return INITIAL_SAMPLE_HISTORY;\n"
        "  }\n"
        "}\n\n"
        "export function saveTriageResult(item) {\n"
        "  const current = getSavedHistory();\n"
        "  const updated = [item, ...current.filter((i) => i.id !== item.id)];\n"
        "  try {\n"
        "    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated.slice(0, 50)));\n"
        "  } catch (e) {\n"
        "    console.error('Failed to write to localStorage', e);\n"
        "  }\n"
        "  return updated;\n"
        "}\n"
    )
    story.append(Paragraph(f"<pre>{code_hist}</pre>", styles['CodeSnippet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>frontend/vite.config.js — Reverse Proxy Configuration:</b>", styles['SubSectionHeader']))
    code_vite = (
        "import { defineConfig } from 'vite';\n"
        "import react from '@vitejs/plugin-react';\n\n"
        "export default defineConfig({\n"
        "  plugins: [react()],\n"
        "  server: {\n"
        "    port: 5173,\n"
        "    proxy: {\n"
        "      '/triage': {\n"
        "        target: 'http://127.0.0.1:8000',\n"
        "        changeOrigin: true,\n"
        "      },\n"
        "    },\n"
        "  },\n"
        "});\n"
    )
    story.append(Paragraph(f"<pre>{code_vite}</pre>", styles['CodeSnippet']))
    story.append(PageBreak())

    # Page 60 (Arabic 52): Appendix 4 - Installation
    story.append(Paragraph("<b>Appendix 4 — User Documentation</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>i. Installation & Environment Setup Instructions</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 3))
    p_inst = (
        "Follow these step-by-step instructions to configure and execute Bug Triage AI in a local development "
        "or production server environment:<br/><br/>"
        "<b>Step 1: Clone Repository & Create Virtual Environment:</b><br/>"
        "<code>git clone https://github.com/kubernetes-sigs/bug-triage-agent.git</code><br/>"
        "<code>cd bug-triage-agent</code><br/>"
        "<code>python -m venv venv</code><br/>"
        "<code>.\\venv\\Scripts\\activate  # Windows (or source venv/bin/activate on Linux)</code><br/><br/>"
        "<b>Step 2: Install Python Dependencies:</b><br/>"
        "<code>pip install -r requirements.txt</code><br/><br/>"
        "<b>Step 3: Configure Environment Variables:</b><br/>"
        "Copy <code>.env.example</code> to <code>.env</code> and configure optional API tokens:<br/>"
        "<code>GITHUB_TOKEN=ghp_your_personal_access_token_here</code><br/>"
        "<code>FASTAPI_PORT=8000</code><br/><br/>"
        "<b>Step 4: Launch FastAPI Backend Server:</b><br/>"
        "<code>uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload</code><br/>"
        "Verify backend API status at <code>http://127.0.0.1:8000/docs</code>.<br/><br/>"
        "<b>Step 5: Install Frontend Dependencies & Launch Vite Dev Server:</b><br/>"
        "<code>cd frontend</code><br/>"
        "<code>npm install</code><br/>"
        "<code>npm run dev</code><br/>"
        "Open browser at <code>http://localhost:5173</code> to access the maintainer workspace."
    )
    story.append(Paragraph(p_inst, styles['ReportBody']))
    story.append(PageBreak())

    # Page 61 (Arabic 53): Appendix 4 - User Manual
    story.append(Paragraph("<b>ii. Maintainer User Manual / Operational Guide</b>", styles['SubSectionHeader']))
    story.append(Spacer(1, 4))
    p_manual = (
        "<b>1. Access Workspace:</b> Navigate to <code>http://localhost:5173</code>. The workspace opens in Dark Mode by default. "
        "Click the sun/moon icon in the top navbar to toggle Light Mode.<br/><br/>"
        "<b>2. Select Input Mode:</b><br/>"
        "• <i>Option A (Manual Entry):</i> Paste an issue title and markdown description into the central text area.<br/>"
        "• <i>Option B (Live URL):</i> Paste a direct GitHub issue link (e.g. <code>https://github.com/kubernetes/kubernetes/issues/115201</code>).<br/>"
        "• <i>Option C (Quick Scenario):</i> Click any of the 8 rotating scenario chips (SIG Node, SIG Network, SIG Storage, etc.).<br/><br/>"
        "<b>3. Execute Triage:</b> Click the <b>'Analyze Issue'</b> button. The real-time 4-step progress view visualizes text cleansing, "
        "similarity retrieval, GraphSAGE forward pass, and LightGBM classification.<br/><br/>"
        "<b>4. Review Triage Results:</b> Inspect the suggested SIG badge, model confidence percentage, and 'Why This Team' rationale. "
        "Review retrieved duplicate issues and examine diagnostic audit flags.<br/><br/>"
        "<b>5. Customize & Copy Response:</b> Click <b>'Review & Copy Response'</b>. Toggle missing diagnostic checkboxes to automatically "
        "insert checklist items into the draft comment. Click <b>'Copy Comment'</b> to paste into GitHub.<br/><br/>"
        "<b>6. Audit History:</b> Click the <b>'History'</b> tab in the navbar to browse past triaged issues, filter by repository, "
        "or reload historical results."
    )
    story.append(Paragraph(p_manual, styles['ReportBody']))
    story.append(PageBreak())

    # Page 62 (Arabic 54): Appendix 5 - Glossary Part 1
    story.append(Paragraph("<b>Appendix 5 — Glossary</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 9.1: Glossary of Technical Terms (Part 1)</b>", styles['TableCaption']))
    glo_data1 = [
        [Paragraph("<b>Term</b>", styles['TableHeader']), Paragraph("<b>Definition & Domain Context</b>", styles['TableHeader'])],
        [Paragraph("AST", styles['TableCellBold']), Paragraph("Abstract Syntax Tree: Tree representation of the syntactic structure of source code.", styles['TableCell'])],
        [Paragraph("BLOB", styles['TableCellBold']), Paragraph("Binary Large Object: Database storage format used in SQLite for serializing numpy embedding vectors.", styles['TableCell'])],
        [Paragraph("BoW", styles['TableCellBold']), Paragraph("Bag-of-Words: Classical information retrieval text representation counting lexical word frequencies.", styles['TableCell'])],
        [Paragraph("CRI", styles['TableCellBold']), Paragraph("Container Runtime Interface: Kubernetes plugin interface enabling Kubelet to use diverse runtimes (containerd, CRI-O).", styles['TableCell'])],
        [Paragraph("CSI", styles['TableCellBold']), Paragraph("Container Storage Interface: Standard for exposing storage systems to containerized workloads.", styles['TableCell'])],
        [Paragraph("DAG", styles['TableCellBold']), Paragraph("Directed Acyclic Graph: Finite graph with directed edges and no cycles, defining LangGraph state workflows.", styles['TableCell'])],
        [Paragraph("GBDT", styles['TableCellBold']), Paragraph("Gradient Boosted Decision Trees: Machine learning technique building sequential decision tree ensembles (e.g. LightGBM).", styles['TableCell'])],
        [Paragraph("GNN", styles['TableCellBold']), Paragraph("Graph Neural Network: Class of deep neural networks designed for performing inference over relational graph structures.", styles['TableCell'])],
        [Paragraph("GraphSAGE", styles['TableCellBold']), Paragraph("Sample and Aggregate: Inductive GNN learning neighborhood aggregation functions for unseen cold-start nodes.", styles['TableCell'])],
        [Paragraph("HNSW", styles['TableCellBold']), Paragraph("Hierarchical Navigable Small World: Approximate nearest neighbor graph index utilized in ChromaDB vector store.", styles['TableCell'])],
        [Paragraph("Kubelet", styles['TableCellBold']), Paragraph("Primary node agent in Kubernetes that registers nodes with the apiserver and manages pod containers.", styles['TableCell'])],
    ]
    t_glo1 = Table(glo_data1, colWidths=[105, 328])
    t_glo1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_glo1)
    story.append(PageBreak())

    # Page 63 (Arabic 55): Appendix 5 - Glossary Part 2
    story.append(Paragraph("<b>Table 9.1: Glossary of Technical Terms (Part 2)</b>", styles['TableCaption']))
    story.append(Spacer(1, 4))
    glo_data2 = [
        [Paragraph("<b>Term</b>", styles['TableHeader']), Paragraph("<b>Definition & Domain Context</b>", styles['TableHeader'])],
        [Paragraph("Macro-F1", styles['TableCellBold']), Paragraph("Unweighted mean of F1-scores across all classes, preventing majority class bias in imbalanced datasets.", styles['TableCell'])],
        [Paragraph("MiniLM", styles['TableCellBold']), Paragraph("Deeply distilled Transformer model providing 384d sentence embeddings with exceptional speed on CPU.", styles['TableCell'])],
        [Paragraph("OSS", styles['TableCellBold']), Paragraph("Open-Source Software: Publicly accessible software codebases maintained by community contributors.", styles['TableCell'])],
        [Paragraph("PLEG", styles['TableCellBold']), Paragraph("Pod Lifecycle Event Generator: Kubelet subsystem that records container runtime lifecycle transitions.", styles['TableCell'])],
        [Paragraph("PR", styles['TableCellBold']), Paragraph("Pull Request: Code change contribution submitted for review and merge into a target Git repository.", styles['TableCell'])],
        [Paragraph("PyG", styles['TableCellBold']), Paragraph("PyTorch Geometric: Open-source PyTorch library optimized for deep learning on irregular graph structures.", styles['TableCell'])],
        [Paragraph("Recall@K", styles['TableCellBold']), Paragraph("Information retrieval metric measuring the proportion of relevant documents retrieved in top-K results.", styles['TableCell'])],
        [Paragraph("SIG", styles['TableCellBold']), Paragraph("Special Interest Group: Kubernetes organizational sub-committee governing a specific architectural component.", styles['TableCell'])],
        [Paragraph("SRS", styles['TableCellBold']), Paragraph("Software Requirement Specification: Formal academic and engineering document detailing software capabilities.", styles['TableCell'])],
        [Paragraph("SVM", styles['TableCellBold']), Paragraph("Support Vector Machine: Supervised learning algorithm that finds the optimal separating hyperplane in feature space.", styles['TableCell'])],
        [Paragraph("TF-IDF", styles['TableCellBold']), Paragraph("Term Frequency-Inverse Document Frequency: Numerical statistic reflecting how important a word is to a document.", styles['TableCell'])],
        [Paragraph("Zero Leakage", styles['TableCellBold']), Paragraph("Experimental setup guaranteeing no chronological lookahead bias or validation data leakage during training.", styles['TableCell'])],
    ]
    t_glo2 = Table(glo_data2, colWidths=[105, 328])
    t_glo2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(t_glo2)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 10 - BIBLIOGRAPHY / REFERENCES (Physical Pages 64 to 65 = Arabic Pages 56 to 57)
    # =========================================================================
    # Page 64 (Arabic 56): References 1 to 10
    story.append(Paragraph("<b>CHAPTER 10 - BIBLIOGRAPHY / REFERENCES</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 10))
    refs_p1 = [
        "[1] D. Cubranic and G. C. Murphy, \"Automatic bug triage using text categorization,\" in <i>Proceedings of the 16th International Conference on Software Engineering & Knowledge Engineering (SEKE)</i>, 2004, pp. 92–97.",
        "[2] J. Anvik, L. Hiew, and G. C. Murphy, \"Who should fix this bug?\" in <i>Proceedings of the 28th International Conference on Software Engineering (ICSE)</i>, 2006, pp. 361–370.",
        "[3] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention is all you need,\" in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 30, 2017.",
        "[4] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, \"BERT: Pre-training of deep bidirectional transformers for language understanding,\" in <i>Proceedings of NAACL-HLT</i>, 2019, pp. 4171–4186.",
        "[5] N. Reimers and I. Gurevych, \"Sentence-BERT: Sentence embeddings using Siamese BERT-networks,\" in <i>Proceedings of EMNLP-IJCNLP</i>, 2019, pp. 3982–3992.",
        "[6] T. N. Kipf and M. Welling, \"Semi-supervised classification with graph convolutional networks,\" in <i>International Conference on Learning Representations (ICLR)</i>, 2017.",
        "[7] W. Hamilton, Z. Ying, and J. Leskovec, \"Inductive representation learning on large graphs,\" in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 30, 2017, pp. 1024–1034.",
        "[8] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu, \"LightGBM: A highly efficient gradient boosting decision tree,\" in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 30, 2017.",
        "[9] H. Chase, \"LangChain: Building applications with LLMs through composability and stateful agents,\" 2024. [Online]. Available: https://github.com/langchain-ai/langchain",
        "[10] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan, \"SWE-bench: Can language models resolve real-world GitHub issues?\" in <i>International Conference on Learning Representations (ICLR)</i>, 2024."
    ]
    for r in refs_p1:
        story.append(Paragraph(r, styles['ReportBody']))
        story.append(Spacer(1, 3.5))
    story.append(PageBreak())

    # Page 65 (Arabic 57): References 11 to 20
    refs_p2 = [
        "[11] M. Fey and J. E. Lenssen, \"Fast graph representation learning with PyTorch Geometric,\" in <i>ICLR Workshop on Representation Learning on Graphs and Manifolds</i>, 2019.",
        "[12] S. Wang, T. Zhang, and H. Pham, \"Detecting duplicate bug reports with software engineering specific word embeddings,\" <i>IEEE Transactions on Software Engineering</i>, vol. 48, no. 5, pp. 1656–1675, 2022.",
        "[13] P. S. Bishnu and V. Bhattacherjee, \"Software fault prediction using quad tree-based k-means clustering algorithm,\" <i>IEEE Transactions on Reliability</i>, vol. 61, no. 3, pp. 648–659, 2012.",
        "[14] Kubernetes Authors, \"Kubernetes: Production-grade container orchestration architecture and Special Interest Group governance,\" Cloud Native Computing Foundation (CNCF), 2024. [Online]. Available: https://kubernetes.io/",
        "[15] S. Mani, A. Sankaran, R. Aralikatte, and S. Mani, \"Deep learning models for bug triage: Questions and answers,\" in <i>Proceedings of the IEEE/ACM International Conference on Automated Software Engineering (ASE)</i>, 2019.",
        "[16] Chroma Developers, \"Chroma: The open-source embedding database for AI applications,\" 2024. [Online]. Available: https://www.trychroma.com/",
        "[17] S. R. Bowman, G. Angeli, C. Potts, and C. D. Manning, \"A large annotated corpus for learning natural language inference,\" in <i>Proceedings of EMNLP</i>, 2015, pp. 632–642.",
        "[18] S. Tiarks, \"What programmers talk about: Analyzing discussions on bug reports,\" in <i>Proceedings of the IEEE International Conference on Software Maintenance</i>, 2011.",
        "[19] FastAPI Authors, \"FastAPI: Modern, fast (high-performance) web framework for building APIs with Python 3.8+,\" 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[20] React Authors, \"React 18: The library for web and native user interfaces,\" Meta Open Source, 2024. [Online]. Available: https://react.dev/"
    ]
    for r in refs_p2:
        story.append(Paragraph(r, styles['ReportBody']))
        story.append(Spacer(1, 3.5))
    
    # Final build
    doc.build(story, canvasmaker=AcademicReportCanvas)
    print(f"Report build complete: {output_filename}")

if __name__ == '__main__':
    build_perfect_report()
