"""Styles and Canvas setup for Bug Triage AI MCA Project Report.
Matches SRM Institute of Science & Technology formatting specifications:
- Times New Roman
- 16pt bold centered chapter titles
- 14pt bold section headers
- 12pt justified body text with 1.5 line spacing (17-18pt leading)
- 1.25" left margin, 1.0" top/right/bottom margins
- Roman i-viii for front matter, Arabic 1-57 for chapters
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib import colors

# Dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 1.25 * inch   # 90 pt
RIGHT_MARGIN = 1.0 * inch   # 72 pt
TOP_MARGIN = 1.0 * inch     # 72 pt
BOTTOM_MARGIN = 1.0 * inch  # 72 pt
USABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN # 433.27 pt
USABLE_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN # 697.89 pt

def to_roman(n):
    roman_map = [(10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]
    result = ''
    for val, num in roman_map:
        while n >= val:
            result += num
            n -= val
    return result

class AcademicReportCanvas(canvas.Canvas):
    """Two-pass canvas to calculate total pages and draw formal headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for idx, page in enumerate(self.pages):
            self.__dict__.update(page)
            p_num = idx + 1
            self.draw_decorations(p_num, num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_num, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 12)
        
        # Front matter: pages 1 to 8
        if page_num == 1:
            # Title page: NO page number
            pass
        elif 2 <= page_num <= 8:
            # Roman numerals centered at bottom (ii, iii, iv, v, vi, vii, viii)
            roman_str = to_roman(page_num)
            self.drawCentredString(LEFT_MARGIN + USABLE_WIDTH / 2.0, 50, roman_str)
        else:
            # Chapter pages: Arabic page numbers starting at 1 on page 9
            arabic_page = page_num - 8
            # In SRM reference format, page number is printed at bottom right
            self.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 50, str(arabic_page))
            
        self.restoreState()

def get_report_styles():
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='ProjectTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=12
    ))
    
    styles.add(ParagraphStyle(
        name='ProjectSubtitle',
        fontName='Times-Bold',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=8
    ))
    
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=0,
        spaceAfter=14,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='SubSectionHeader',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='SubSubSectionHeader',
        fontName='Times-BoldItalic',
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='ReportBody',
        fontName='Times-Roman',
        fontSize=12,
        leading=17,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceBefore=0,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='ReportBullet',
        fontName='Times-Roman',
        fontSize=12,
        leading=16.5,
        alignment=TA_LEFT,
        leftIndent=16,
        firstLineIndent=-10,
        textColor=colors.black,
        spaceBefore=0,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name='FigureCaption',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='TableCaption',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name='TableCellCenter',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name='CodeSnippet',
        fontName='Courier',
        fontSize=8.0,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A')
    ))

    styles.add(ParagraphStyle(
        name='CodeSnippetComment',
        fontName='Courier-Oblique',
        fontSize=8.0,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#059669')
    ))

    styles.add(ParagraphStyle(
        name='TOCItem',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=17,
        alignment=TA_LEFT,
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name='TOCSubItem',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=TA_LEFT,
        leftIndent=15,
        textColor=colors.black
    ))

    return styles
