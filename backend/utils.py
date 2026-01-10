import json
import csv
from io import StringIO
from typing import Dict, Any, Optional, List
import re


def parse_csv_to_summary(csv_content: str) -> str:
    """Parse CSV trend data and create a human-readable summary"""
    if not csv_content or not csv_content.strip():
        return ""

    try:
        reader = csv.DictReader(StringIO(csv_content))
        rows = list(reader)

        if not rows:
            return "Empty trend data."

        # Create a summary of the trend data
        fieldnames = reader.fieldnames or []
        summary_lines = [
            f"Trend data contains {len(rows)} records with fields: {', '.join(fieldnames)}",
        ]

        # Add sample of first few and last few rows
        if len(rows) <= 5:
            summary_lines.append(f"All records: {rows}")
        else:
            summary_lines.append(f"First record: {rows[0]}")
            summary_lines.append(f"Last record: {rows[-1]}")

        return "\n".join(summary_lines)

    except Exception as e:
        return f"Could not parse CSV trend data: {str(e)}"


def format_alarms_json(alarms: Dict[str, Any]) -> str:
    """Format alarms JSON into a readable structure"""
    if not alarms:
        return ""

    try:
        # Pretty format the JSON for better readability
        return json.dumps(alarms, indent=2)
    except Exception as e:
        return f"Could not format alarms: {str(e)}"


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON object from text that may contain markdown code blocks or other content.
    Tries multiple strategies to find valid JSON.
    """
    if not text:
        return None

    # Strategy 1: Try to parse the entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Look for JSON in markdown code blocks
    json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_block_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Strategy 3: Find JSON object boundaries
    json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)

    # Try matches in reverse order (often the last one is most complete)
    for match in reversed(matches):
        try:
            parsed = json.loads(match)
            # Validate it has expected structure
            if isinstance(parsed, dict) and any(key in parsed for key in ['shiftSummary', 'openIssues', 'recommendedActions']):
                return parsed
        except json.JSONDecodeError:
            continue

    return None


def validate_handover_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and repair handover JSON structure.
    Ensures all required fields are present with proper types.
    """
    repaired = {
        'shiftSummary': [],
        'criticalAlarms': [],
        'openIssues': [],
        'recommendedActions': [],
        'questions': []
    }

    # Validate shiftSummary
    if 'shiftSummary' in data:
        if isinstance(data['shiftSummary'], list):
            repaired['shiftSummary'] = [str(item) for item in data['shiftSummary']]
        elif isinstance(data['shiftSummary'], str):
            repaired['shiftSummary'] = [data['shiftSummary']]

    # Validate criticalAlarms
    if 'criticalAlarms' in data and isinstance(data['criticalAlarms'], list):
        for alarm in data['criticalAlarms']:
            if isinstance(alarm, dict) and 'alarm' in alarm:
                repaired['criticalAlarms'].append({
                    'alarm': str(alarm.get('alarm', '')),
                    'meaning': str(alarm.get('meaning', 'No meaning provided'))
                })

    # Validate openIssues
    if 'openIssues' in data and isinstance(data['openIssues'], list):
        for issue in data['openIssues']:
            if isinstance(issue, dict) and 'issue' in issue:
                priority = issue.get('priority', 'Med')
                if priority not in ['High', 'Med', 'Low']:
                    priority = 'Med'

                confidence = issue.get('confidence', 50)
                try:
                    confidence = float(confidence)
                    confidence = max(0, min(100, confidence))
                except (ValueError, TypeError):
                    confidence = 50

                repaired['openIssues'].append({
                    'issue': str(issue.get('issue', '')),
                    'priority': priority,
                    'confidence': confidence
                })

    # Validate recommendedActions
    if 'recommendedActions' in data:
        if isinstance(data['recommendedActions'], list):
            repaired['recommendedActions'] = [str(item) for item in data['recommendedActions']]
        elif isinstance(data['recommendedActions'], str):
            repaired['recommendedActions'] = [data['recommendedActions']]

    # Validate questions
    if 'questions' in data:
        if isinstance(data['questions'], list):
            repaired['questions'] = [str(item) for item in data['questions']]
        elif isinstance(data['questions'], str):
            repaired['questions'] = [data['questions']]

    return repaired


def create_markdown_from_structured(data: Dict[str, Any]) -> str:
    """Create formatted markdown from structured handover data"""
    md_lines = ["# Shift Handover Intelligence Report\n"]

    # Shift Summary
    md_lines.append("## 📋 Shift Summary")
    if data.get('shiftSummary'):
        for item in data['shiftSummary']:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("_No summary available_")
    md_lines.append("")

    # Critical Alarms
    md_lines.append("## 🚨 Critical Alarms & Meaning")
    if data.get('criticalAlarms'):
        for alarm in data['criticalAlarms']:
            md_lines.append(f"### {alarm.get('alarm', 'Unknown')}")
            md_lines.append(f"**Meaning:** {alarm.get('meaning', 'N/A')}\n")
    else:
        md_lines.append("_No critical alarms reported_\n")

    # Open Issues
    md_lines.append("## ⚠️ Open Issues")
    if data.get('openIssues'):
        for issue in data['openIssues']:
            priority = issue.get('priority', 'Med')
            confidence = issue.get('confidence', 0)
            priority_emoji = {"High": "🔴", "Med": "🟡", "Low": "🟢"}.get(priority, "⚪")
            md_lines.append(f"### {priority_emoji} {issue.get('issue', 'Unknown')}")
            md_lines.append(f"**Priority:** {priority} | **Confidence:** {confidence}%\n")
    else:
        md_lines.append("_No open issues identified_\n")

    # Recommended Actions
    md_lines.append("## ✅ Recommended Actions")
    if data.get('recommendedActions'):
        for i, action in enumerate(data['recommendedActions'], 1):
            md_lines.append(f"{i}. {action}")
    else:
        md_lines.append("_No recommended actions_")
    md_lines.append("")

    # Questions for Next Shift
    md_lines.append("## ❓ Questions for Next Shift")
    if data.get('questions'):
        for q in data['questions']:
            md_lines.append(f"- {q}")
    else:
        md_lines.append("_No questions_")
    md_lines.append("")

    md_lines.append("---")
    md_lines.append("_Generated by Shift Handover Intelligence with Gemini AI_")

    return "\n".join(md_lines)
