#!/usr/bin/env python3
"""
Generate individual PDFs for Prompts 03 through 18.
Matches the official visual styling of MSE2026015_Prompt_01 and MSE2026015_Prompt_02.

Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import glob
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from scripts.generate_prompt_pdfs import NumberedCanvas, sanitize_text

def build_single_prompt_pdf(md_path: str, out_pdf: str, prompt_num_str: str):
    doc = SimpleDocTemplate(
        out_pdf,
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
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2b6cb0'),
        alignment=1,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=12,
        spaceAfter=5
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=8,
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
        leftIndent=14,
        bulletIndent=4,
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
        borderPadding=5,
        spaceBefore=4,
        spaceAfter=5
    )

    story = []

    # Title Page / Header
    story.append(Paragraph(f"PROMPT {prompt_num_str} IMPLEMENTATION", title_style))
    story.append(Paragraph("Accountable Research Workspace for an Implementation-Based Second Paper", subtitle_style))
    story.append(Paragraph(
        "<b>Student:</b> Sujal Rajesh Ghagare | <b>Roll No:</b> MSE2026015 | <b>Degree:</b> M.Tech (IT)<br/>"
        "<b>Institution:</b> Indian Institute of Information Technology Allahabad (IIIT Allahabad)<br/>"
        "<b>Course:</b> AI Tools for Research | <b>Selected Gap:</b> Gap G2 (Claim-Level Citation Support)",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2b6cb0"), spaceAfter=12))

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    table_rows = []
    in_code = False
    code_lines = []

    for line in lines:
        raw = line.strip()

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

        if "|" in raw and not in_code:
            if re.match(r'^\|?\s*:?-+:?\s*\|', raw):
                continue
            cells = [c.strip() for c in raw.strip("|").split("|")]
            if len(cells) > 1:
                table_rows.append(cells)
                in_table = True
                continue
        else:
            if in_table:
                if table_rows:
                    col_count = len(table_rows[0])
                    avail_width = 504
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
            story.append(Spacer(1, 3))
            continue

        # Skip duplicate titles at start of markdown
        if raw.startswith("# PROMPT"):
            continue
        if raw.startswith("## ") and ("Implementation" in raw or "Framing" in raw or "Configure" in raw or "Mapping" in raw):
            p_text = sanitize_text(raw[3:])
            story.append(Paragraph(f"<b>{p_text}</b>", h1_style))
            continue

        if raw.startswith("# "):
            p_text = sanitize_text(raw[2:])
            story.append(Paragraph(p_text, h1_style))
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
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#e2e8f0"), spaceBefore=4, spaceAfter=6))
        else:
            p_text = sanitize_text(raw)
            story.append(Paragraph(p_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {out_pdf}")

def generate_all_individual_pdfs():
    os.makedirs("prompts_pdf", exist_ok=True)
    prompt_files = sorted(glob.glob("prompts/PROMPT_*_IMPLEMENTATION.md"))
    for pfile in prompt_files:
        match = re.search(r'PROMPT_(\d+)_IMPLEMENTATION', pfile)
        if match:
            p_num = match.group(1)
            out_pdf = f"prompts_pdf/MSE2026015_Prompt_{p_num}.pdf"
            build_single_prompt_pdf(pfile, out_pdf, p_num)

if __name__ == "__main__":
    generate_all_individual_pdfs()
