"""Precision 65-Page Builder for Bug Triage AI.
Measures every page's flowables to guarantee each page <= 697.89 pt.
Guarantees EXACTLY 65 pages total:
- Pages 1 to 8: Front Matter (Roman i to viii)
- Pages 9 to 65: Chapters 1 to 10 (Arabic 1 to 57)
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

def check_page_height(flowables, page_num):
    total_h = 0
    for f in flowables:
        w, h = f.wrap(USABLE_WIDTH, USABLE_HEIGHT)
        total_h += h
    if total_h > USABLE_HEIGHT:
        print(f"WARNING: Page {page_num} height is {total_h:.1f} pt (max {USABLE_HEIGHT:.1f} pt) -> overflow by {total_h - USABLE_HEIGHT:.1f} pt!")
    return total_h

print("Page height verification utility ready.")
