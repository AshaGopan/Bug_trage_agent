"""Part 0: Front Matter (Pages i to viii = Pages 1 to 8)."""

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

def build_frontmatter(styles):
    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE (Page i - no page number visible)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Bug Triage AI</b>", ParagraphStyle(
        'T1', fontName='Times-Bold', fontSize=22, leading=26, alignment=TA_CENTER, textColor=colors.black
    )))
    story.append(Spacer(1, 14))
    
    story.append(Paragraph(
        "<b>A PROJECT REPORT SUBMITTED TO<br/>"
        "SRM INSTITUTE OF SCIENCE & TECHNOLOGY<br/>"
        "IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE<br/>"
        "AWARD OF THE DEGREE OF<br/>"
        "MASTER OF COMPUTER APPLICATIONS</b>",
        ParagraphStyle('T2', fontName='Times-Bold', fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.black)
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

    # SRM Logo
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

    # Signatures Table
    sig_data = [
        [
            Paragraph("<b>Mrs. Leena Bai</b><br/>Assistant Professor<br/>Department of Computer Applications<br/><b>(GUIDE)</b>", styles['TableCellCenter']),
            Paragraph("<b>Dr. P.J. Arul Leena Rose</b><br/>Professor & Head,<br/>Department of Computer Applications", styles['TableCellCenter'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[210, 210])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 110))

    # Examiners Row
    exam_data = [
        [
            Paragraph("<b>INTERNAL EXAMINER</b>", styles['TableCellCenter']),
            Paragraph("<b>EXTERNAL EXAMINER</b>", styles['TableCellCenter'])
        ]
    ]
    exam_table = Table(exam_data, colWidths=[210, 210])
    exam_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
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
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))
    names_block = (
        "<b>Boni Venkata Yeswanth Kumar<br/>"
        "Muthyala Venkata Viswanath<br/>"
        "Ponnaganti Santosh Kumar<br/>"
        "Ballikura Tharun Teja</b>"
    )
    story.append(Paragraph(names_block, ParagraphStyle('N1', fontName='Times-Bold', fontSize=10.5, leading=15, alignment=TA_RIGHT)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TABLE OF CONTENTS - PART 1 (Page iv)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>TABLE OF CONTENT</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 12))

    toc_p1 = [
        ("<b>CHAPTER 1 - INTRODUCTION</b>", "<b>1</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background of the Study", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Objectives of the Project", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope of the Project", "3"),
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
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Software / Tools and Their Features", "11"),
        ("<b>CHAPTER 4 - SYSTEM ANALYSIS</b>", "<b>13</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Requirement Specification", "13"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Characteristics of Existing System", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Proposed System / Proposed Approach", "14"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Feasibility Study", "15"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Software Requirement Specification", "16"),
        ("<b>CHAPTER 5 - SYSTEM DESIGN</b>", "<b>17</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.1 System Architecture / Overall Workflow", "17"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Context Diagram", "18"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Use Case Diagram", "19"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Activity Diagram / State Diagram / UML Diagram", "20"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.5 Data Flow Diagram / ER Diagram / Class Diagram / ML Workflow", "23"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.6 Database Design / Dataset Design", "27"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.7 User Interface Design", "30"),
        ("<b>CHAPTER 6 - SYSTEM IMPLEMENTATION</b>", "<b>32</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Modules Description", "32"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Dataset Description / Data Collection", "33"),
    ]

    toc_rows1 = []
    for title, p_num in toc_p1:
        toc_rows1.append([
            Paragraph(title, styles['TableCell']),
            Paragraph(p_num, styles['TableCellCenter'])
        ])
    t_toc1 = Table(toc_rows1, colWidths=[395, 38])
    t_toc1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_toc1)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS - PART 2 (Page v)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>TABLE OF CONTENT (Continued)</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 14))

    toc_p2 = [
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Data Preprocessing", "34"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Feature Engineering / Feature Extraction", "35"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.5 Model Architecture / Algorithm Design", "36"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.6 System / Model Implementation", "37"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.7 Validation Checks", "39"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.8 User Interface Implementation", "39"),
        ("<b>CHAPTER 7 - TESTING AND EVALUATION</b>", "<b>40</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Test Cases", "40"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Unit Testing", "41"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Integration Testing", "42"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.4 System Testing", "43"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.5 Model Evaluation / Performance Evaluation", "44"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.6 Performance Metrics", "46"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;7.7 Comparative Analysis", "47"),
        ("<b>CHAPTER 8 - RESULTS AND CONCLUSION</b>", "<b>48</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.1 Results", "48"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Discussion / Analysis", "49"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Limitations", "50"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.4 Lessons Learnt", "50"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.5 Conclusion", "51"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;8.6 Future Enhancements", "51"),
        ("<b>CHAPTER 9 - APPENDICES</b>", "<b>52</b>"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 1 — Plagiarism Certificate", "52"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 2 — Screenshots", "53"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 3 — Sample Coding", "58"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 4 — User Documentation", "61"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Appendix 5 — Glossary", "62"),
        ("<b>CHAPTER 10 - BIBLIOGRAPHY / REFERENCES</b>", "<b>63</b>"),
    ]

    toc_rows2 = []
    for title, p_num in toc_p2:
        toc_rows2.append([
            Paragraph(title, styles['TableCell']),
            Paragraph(p_num, styles['TableCellCenter'])
        ])
    t_toc2 = Table(toc_rows2, colWidths=[395, 38])
    t_toc2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_toc2)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT (Page vi)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ABSTRACT</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))

    abstract_text1 = (
        "In modern hyperscale open-source software (OSS) ecosystems such as <b>kubernetes/kubernetes</b>, "
        "the rapid influx of bug reports presents a severe bottleneck for project maintainers. Inefficient manual "
        "triaging leads to significant delays in issue resolution, contributor frustration, and cognitive fatigue. "
        "This project presents <b>Bug Triage AI</b>, an intelligent, multi-modal machine learning system and stateful "
        "agentic workflow designed to automate bug report routing, duplicate retrieval, diagnostic completeness auditing, "
        "and maintainer comment synthesis."
    )
    story.append(Paragraph(abstract_text1, styles['ReportBody']))
    story.append(Spacer(1, 6))

    abstract_text2 = (
        "The analytical core of Bug Triage AI addresses the multi-modal nature of software engineering artifacts by fusing "
        "three distinct feature representations into a unified 519-dimensional input vector: dense semantic text embeddings "
        "(384d) derived from <i>all-MiniLM-L6-v2</i>, inductive structural graph embeddings (128d) computed via a 2-layer "
        "<i>GraphSAGE</i> Graph Neural Network operating over cross-issue reference topologies, and an empirical "
        "training-neighbor label awareness prior (7d). To solve the inductive cold-start challenge for unlinked new bug reports, "
        "the system dynamically constructs an inference subgraph linking the incoming issue to its top $K=5$ nearest semantic "
        "neighbors in ChromaDB vector space. A multi-class LightGBM Gradient Boosted Decision Tree performs the final routing "
        "across seven primary Kubernetes Special Interest Groups (SIGs)."
    )
    story.append(Paragraph(abstract_text2, styles['ReportBody']))
    story.append(Spacer(1, 6))

    abstract_text3 = (
        "To provide seamless operational integration, the system orchestrates a <i>LangGraph</i> state machine consisting of "
        "an intake cleaner, a diagnostic completeness auditor, a cold-start graph retriever, and a confidence-aware conditional "
        "router (threshold &ge; 60%). The solution is exposed via a high-performance <b>FastAPI</b> REST service and delivered "
        "through a modern 10-screen <b>React + Vite + Tailwind CSS</b> maintainer workspace supporting Dark Mode (#0B0F19) and "
        "Light Mode (#F8F9FC), split-view verification, and real-time execution progress tracking."
    )
    story.append(Paragraph(abstract_text3, styles['ReportBody']))
    story.append(Spacer(1, 6))

    abstract_text4 = (
        "Evaluated under strict zero-leakage chronological partitioning on real-world Kubernetes issues, Bug Triage AI achieves "
        "a superior Macro-F1 score of <b>0.7485</b>, significantly outperforming classical TF-IDF baselines (0.7020) and text-only "
        "models (0.6247). Sub-second inference latency (&lt; 200 ms) and reliable duplicate retrieval validate Bug Triage AI as an "
        "explainable, production-ready artificial intelligence platform for large-scale software repository management."
    )
    story.append(Paragraph(abstract_text4, styles['ReportBody']))
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
        ("Table 3.3: Software Tools and Their Features", "11"),
        ("Table 5.1: SQLite Issues & Edges Table Schema", "27"),
        ("Table 5.2: SQLite PR Files & Embeddings Table Schema", "27"),
        ("Table 5.3: ChromaDB Vector Collection Schema", "28"),
        ("Table 5.4: Frontend LocalStorage History Schema", "28"),
        ("Table 6.1: Feature Engineering Transformations", "35"),
        ("Table 7.1: Test Cases", "40"),
        ("Table 7.2: Unit Test Cases", "41"),
        ("Table 7.3: Integration Test Cases", "42"),
        ("Table 7.4: System Test Cases", "43"),
        ("Table 7.5: Model Performance Metrics", "44"),
        ("Table 7.6: Comparative Analysis with Existing Systems", "47"),
        ("Table 9.1: Glossary", "62"),
    ]

    lot_rows = []
    for title, p_num in lot_items:
        lot_rows.append([
            Paragraph(title, styles['TableCellBold']),
            Paragraph(p_num, styles['TableCellCenter'])
        ])
    t_lot = Table(lot_rows, colWidths=[395, 38])
    t_lot.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_lot)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: LIST OF FIGURES (Page viii)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>List of Figures</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 16))

    lof_items = [
        ("Figure 5.1: Context Diagram", "18"),
        ("Figure 5.2: Use Case Diagram", "19"),
        ("Figure 5.3: Activity Diagram", "20"),
        ("Figure 5.4: State Diagram", "21"),
        ("Figure 5.5: Sequence Diagram", "22"),
        ("Figure 5.6: Data Flow Diagram (DFD Level 1)", "23"),
        ("Figure 5.7: ER Diagram", "24"),
        ("Figure 5.8: Class Diagram", "25"),
        ("Figure 5.9: ML Workflow Diagram", "26"),
        ("Figure A2.1: Workspace Landing Screen (Dark Mode)", "53"),
        ("Figure A2.2: Workspace Landing Screen (Light Mode)", "53"),
        ("Figure A2.3: Analyzing Progress Execution Pipeline", "54"),
        ("Figure A2.4: Triage Results Screen", "54"),
        ("Figure A2.5: Similar Issues & Diagnostic Auditing Panel", "55"),
        ("Figure A2.6: Suggested Maintainer Response Editor", "55"),
        ("Figure A2.7: Split-View Triage Session", "56"),
        ("Figure A2.8: Maintainer Triage History View", "56"),
        ("Figure A2.9: Maintainer Authentication & Account Creation", "57"),
        ("Figure A2.10: Component Error & Warning States", "57"),
    ]

    lof_rows = []
    for title, p_num in lof_items:
        lof_rows.append([
            Paragraph(title, styles['TableCellBold']),
            Paragraph(p_num, styles['TableCellCenter'])
        ])
    t_lof = Table(lof_rows, colWidths=[395, 38])
    t_lof.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_lof)
    story.append(PageBreak())

    return story
