#!/usr/bin/env python3
"""
Generate professional PDF report for Prompts 03 through 18.
Matches the official visual styling of MSE2026015_Prompt_01 and MSE2026015_Prompt_02.

Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import os
import glob
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        footer_text = f"AI Tools for Research | MSE2026015 | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, footer_text)
        self.restoreState()

def sanitize_text(text: str) -> str:
    """Sanitize XML characters for ReportLab Paragraphs."""
    t = text.replace("&", "&amp;")
    t = re.sub(r'<br\s*/?>', '<br/>', t, flags=re.IGNORECASE)
    t = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.*?)\*', r'<i>\1</i>', t)
    t = t.replace("$", "").replace("\\uparrow", "↑").replace("\\downarrow", "↓")
    t = t.replace("\\pm", "±").replace("\\ge", "≥").replace("\\le", "≤")
    t = t.replace("\\tau", "τ").replace("\\rightarrow", "→")
    return t

def build_pdf(output_pdf: str):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2b6cb0'),
        alignment=1,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1a202c'),
        backColor=colors.HexColor('#edf2f7'),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # Title Page / Header
    story.append(Paragraph("AI TOOLS FOR RESEARCH: LAB 02 ASSIGNMENT", title_style))
    story.append(Paragraph("Complete Implementation of Prompts 03 through 18", subtitle_style))
    story.append(Paragraph(
        "<b>Student:</b> Sujal Rajesh Ghagare | <b>Roll No:</b> MSE2026015 | <b>Degree:</b> M.Tech (IT)<br/>"
        "<b>Institution:</b> Indian Institute of Information Technology Allahabad (IIIT Allahabad)<br/>"
        "<b>Selected Research Gap:</b> Gap G2 — Claim-Level Citation Support in Literature Synthesis",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2b6cb0"), spaceAfter=15))

    # Read all prompt implementation markdown files
    prompt_files = sorted(glob.glob("prompts/PROMPT_*_IMPLEMENTATION.md"))

    for p_idx, pfile in enumerate(prompt_files):
        with open(pfile, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if p_idx > 0:
            story.append(PageBreak())

        in_table = False
        table_rows = []

        in_code = False
        code_lines = []

        for line in lines:
            raw = line.strip()

            # Code blocks
            if raw.startswith("```"):
                if in_code:
                    code_text = "<br/>".join([c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for c in code_lines])
                    story.append(Paragraph(code_text, code_style))
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue

            if in_code:
                code_lines.append(line.rstrip("\r\n"))
                continue

            # Markdown Tables
            if "|" in raw and not in_code:
                if re.match(r'^\|?\s*:?-+:?\s*\|', raw):
                    continue  # Separator line
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if len(cells) > 1:
                    table_rows.append(cells)
                    in_table = True
                    continue
            else:
                if in_table:
                    # Flush table
                    if table_rows:
                        col_count = len(table_rows[0])
                        avail_width = 504  # 612 - 108 margins
                        col_w = avail_width / col_count

                        formatted_table = []
                        for r_idx, row in enumerate(table_rows):
                            p_row = []
                            for cell in row:
                                is_head = (r_idx == 0)
                                p_style = ParagraphStyle(
                                    'Cell',
                                    parent=body_style,
                                    fontName='Helvetica-Bold' if is_head else 'Helvetica',
                                    fontSize=7.5,
                                    leading=9.5,
                                    textColor=colors.HexColor('#1a202c') if not is_head else colors.HexColor('#ffffff')
                                )
                                clean_cell = sanitize_text(cell)
                                p_row.append(Paragraph(clean_cell, p_style))
                            formatted_table.append(p_row)

                        t = Table(formatted_table, colWidths=[col_w] * col_count)
                        t.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
                            ('TOPPADDING', (0, 0), (-1, -1), 3),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                        ]))
                        story.append(t)
                        story.append(Spacer(1, 6))
                    table_rows = []
                    in_table = False

            if not raw:
                story.append(Spacer(1, 4))
                continue

            # Headers
            if raw.startswith("# "):
                p_text = sanitize_text(raw[2:])
                story.append(Paragraph(p_text, title_style))
            elif raw.startswith("## "):
                p_text = sanitize_text(raw[3:])
                story.append(Paragraph(p_text, h1_style))
            elif raw.startswith("### "):
                p_text = sanitize_text(raw[4:])
                story.append(Paragraph(p_text, h2_style))
            elif raw.startswith("#### "):
                p_text = sanitize_text(raw[5:])
                story.append(Paragraph(f"<b>{p_text}</b>", body_style))
            elif raw.startswith("* ") or raw.startswith("- "):
                p_text = sanitize_text(raw[2:])
                story.append(Paragraph(f"• {p_text}", bullet_style))
            elif re.match(r'^\d+\.\s', raw):
                p_text = sanitize_text(re.sub(r'^\d+\.\s', '', raw))
                story.append(Paragraph(f"1. {p_text}", bullet_style))
            elif raw.startswith("---"):
                story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#e2e8f0"), spaceBefore=6, spaceAfter=8))
            else:
                p_text = sanitize_text(raw)
                story.append(Paragraph(p_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_pdf}")

if __name__ == "__main__":
    out_pdf = "MSE2026015_Prompt_03_to_18_Complete.pdf"
    build_pdf(out_pdf)
