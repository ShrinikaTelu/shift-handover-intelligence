"""
PDF Generator for Shift Handover Intelligence Reports
Converts structured handover data to professionally formatted PDF documents
using ReportLab (lighter weight than WeasyPrint)
"""

from io import BytesIO
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, grey, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, PageTemplate, Frame, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import re


def generate_pdf_from_structured_data(structured_data: Dict[str, Any]) -> bytes:
    """
    Generate a professional PDF from structured handover data using ReportLab.
    
    Args:
        structured_data: Dictionary containing the parsed handover structure
        
    Returns:
        PDF file as bytes
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Shift Handover Intelligence Report"
    )
    
    # Build the story (content)
    story = build_pdf_story(structured_data)
    
    # Build PDF
    doc.build(story)
    
    # Get bytes
    buffer.seek(0)
    return buffer.getvalue()


def build_pdf_story(data: Dict[str, Any]) -> list:
    """Build the ReportLab story (list of flowables) for the PDF"""
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#333333'),
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Header
    story.append(Paragraph("📋 Shift Handover Intelligence Report", title_style))
    
    now = datetime.now().strftime("%B %d, %Y")
    header_info = f"<b>Report Date:</b> {now} | <b>Status:</b> ✓ Operational"
    story.append(Paragraph(header_info, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Shift Summary section
    if data.get('shiftSummary'):
        story.append(Paragraph("📋 Shift Summary", heading_style))
        for item in data['shiftSummary']:
            story.append(Paragraph(f"✓ {item}", normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Critical Alarms section
    if data.get('criticalAlarms'):
        story.append(Paragraph("🚨 Critical Alarms & Meaning", heading_style))
        for alarm in data['criticalAlarms']:
            alarm_name = alarm.get('alarm', 'Unknown Alarm')
            meaning = alarm.get('meaning', 'No description available')
            story.append(Paragraph(f"<b>{alarm_name}</b>", normal_style))
            story.append(Paragraph(f"<i>Meaning:</i> {meaning}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("🚨 Critical Alarms & Meaning", heading_style))
        story.append(Paragraph("No critical alarms reported", normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Open Issues section
    if data.get('openIssues'):
        story.append(Paragraph("⚠️ Open Issues", heading_style))
        for issue in data['openIssues']:
            priority = issue.get('priority', 'Med')
            emoji = get_priority_emoji(priority)
            confidence = issue.get('confidence', 0)
            issue_name = issue.get('issue', 'Unknown Issue')
            details = issue.get('details', 'No details available')
            
            story.append(Paragraph(
                f"{emoji} <b>[{priority}]</b> {issue_name} ({confidence}% confidence)",
                normal_style
            ))
            story.append(Paragraph(f"<i>Details:</i> {details}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("⚠️ Open Issues", heading_style))
        story.append(Paragraph("No open issues reported", normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Action Plan section
    if data.get('actionPlan'):
        story.append(Paragraph("📅 Action Plan & Priorities", heading_style))
        for action in data['actionPlan']:
            priority = action.get('priority', 'Med')
            emoji = get_priority_emoji(priority)
            action_name = action.get('action', 'Unknown Action')
            description = action.get('description', 'No description available')
            
            story.append(Paragraph(
                f"{emoji} <b>[{priority}]</b> {action_name}",
                normal_style
            ))
            story.append(Paragraph(f"{description}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    # Clarifying Questions section
    if data.get('clarifyingQuestions'):
        story.append(Paragraph("❓ Clarifying Questions for Day Shift", heading_style))
        for i, question in enumerate(data['clarifyingQuestions'], 1):
            story.append(Paragraph(f"<b>Q{i}:</b> {question}", normal_style))
            story.append(Spacer(1, 0.08*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated by Shift Handover Intelligence System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(footer_text, footer_style))
    
    return story


def get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level"""
    priority_lower = priority.lower()
    emojis = {
        'high': '🔴',
        'med': '🟡',
        'low': '🟢'
    }
    return emojis.get(priority_lower, '⚪')


def generate_pdf_from_markdown(markdown_content: str) -> bytes:
    """
    Generate a beautifully formatted PDF from markdown content.
    This creates a visually rich PDF that looks like the formatted report.
    
    Args:
        markdown_content: The markdown text to convert to PDF
        
    Returns:
        PDF file as bytes
    """
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Shift Handover Intelligence - Formatted Report"
    )
    
    story = parse_markdown_to_story(markdown_content)
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()


def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text


def apply_markdown_formatting(text: str) -> str:
    """Apply markdown formatting (bold, italic) to text and return HTML"""
    # Escape HTML first
    text = escape_html(text)
    # Convert markdown to HTML - bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown to HTML - italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Underscores for italic
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
    return text


def parse_markdown_to_story(markdown_text: str) -> list:
    """Convert markdown text to ReportLab story with formatting"""
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles for beautiful formatting
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=HexColor('#1a3a52'),
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#34568B'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#d9534f'),
        fontName='Courier',
        spaceAfter=6
    )
    
    # Parse markdown lines
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines (they're handled as natural spacing)
        if not stripped:
            story.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Check headers - must check ### before ## before #
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            # Apply markdown formatting to header
            text = apply_markdown_formatting(text)
            story.append(Paragraph(text, heading2_style))
            i += 1
            
        elif stripped.startswith('## '):
            text = stripped[3:].strip()
            # Apply markdown formatting to header
            text = apply_markdown_formatting(text)
            story.append(Paragraph(text, heading1_style))
            i += 1
            
        elif stripped.startswith('# '):
            text = stripped[2:].strip()
            # Apply markdown formatting to header
            text = apply_markdown_formatting(text)
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.15*inch))
            i += 1
            
        # Lists - bullet points
        elif stripped.startswith('* ') or stripped.startswith('- '):
            list_items = []
            
            while i < len(lines):
                current = lines[i].strip()
                if not current:
                    i += 1
                    break
                if current.startswith('* ') or current.startswith('- '):
                    item_text = current[2:].strip()
                    item_text = apply_markdown_formatting(item_text)
                    list_items.append(item_text)
                    i += 1
                else:
                    break
            
            # Add list items to story
            for item in list_items:
                story.append(Paragraph(f"• {item}", normal_style))
            
            story.append(Spacer(1, 0.1*inch))
            
        # Lists - numbered
        elif len(stripped) > 2 and stripped[0].isdigit() and '. ' in stripped[:4]:
            list_items = []
            item_num = 1
            
            while i < len(lines):
                current = lines[i].strip()
                if not current:
                    i += 1
                    break
                # Check if it starts with a number and dot
                if len(current) > 2 and current[0].isdigit() and '. ' in current[:4]:
                    parts = current.split('. ', 1)
                    if len(parts) == 2:
                        item_text = parts[1].strip()
                        item_text = apply_markdown_formatting(item_text)
                        list_items.append(item_text)
                    i += 1
                else:
                    break
            
            # Add numbered list items to story
            for idx, item in enumerate(list_items, 1):
                story.append(Paragraph(f"<b>{idx}.</b> {item}", normal_style))
            
            story.append(Spacer(1, 0.1*inch))
            
        # Code blocks
        elif stripped.startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            
            code_text = '\n'.join(code_lines).strip()
            story.append(Paragraph(f"<font face='Courier'>{escape_html(code_text)}</font>", code_style))
            story.append(Spacer(1, 0.1*inch))
            
        # Regular paragraphs with potential bold/italic
        else:
            # Apply markdown formatting
            html_line = apply_markdown_formatting(stripped)
            story.append(Paragraph(html_line, normal_style))
            i += 1
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"<i>Generated by Shift Handover Intelligence System on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</i>"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(footer_text, footer_style))
    
    return story

