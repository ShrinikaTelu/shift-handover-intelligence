from google import genai
import os
import json
import logging
from typing import Dict, Any, Tuple, Optional
from dotenv import load_dotenv
from utils import (
    extract_json_from_text,
    validate_handover_json,
    create_markdown_from_structured,
    parse_csv_to_summary,
    format_alarms_json
)

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini API"""

    SYSTEM_PROMPT = """You are an industrial operations assistant specialized in AVEVA systems and manufacturing operations.

Your task is to convert shift handover notes, alarm data, and trend data into a structured, actionable handover summary.

CRITICAL REQUIREMENTS:
1. **Separate Facts from Hypotheses**: Clearly distinguish between observed facts and inferred hypotheses.
2. **Provide Confidence**: For any hypothesis or inference, provide a confidence percentage (0-100%).
3. **Be Specific and Operational**: Use precise industrial terminology. Reference specific equipment, tags, or alarm IDs when available.
4. **Ask Clarifying Questions**: If critical information is missing, ask up to 3 specific questions.
5. **Output Format**: Return BOTH:
   - A valid JSON object matching the exact schema below
   - A markdown-formatted report

JSON SCHEMA (STRICT):
{
  "shiftSummary": ["fact 1", "fact 2", ...],
  "criticalAlarms": [{"alarm": "alarm description", "meaning": "operational meaning"}],
  "openIssues": [{"issue": "description", "priority": "High|Med|Low", "confidence": 75}],
  "recommendedActions": ["action 1", "action 2", ...],
  "questions": ["question 1", "question 2", ...]
}

PRIORITY LEVELS:
- High: Immediate action required, safety/production impact
- Med: Should be addressed within 24 hours
- Low: Monitor or address when convenient

Return your response in this exact format:
```json
{...your JSON here...}
```

Then on a new line, provide the markdown report starting with # Shift Handover Intelligence Report
"""

    def __init__(self):
        """Initialize Gemini client with API key"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        os.environ['GOOGLE_API_KEY'] = api_key
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-3-flash-preview'

    def _build_prompt(
        self,
        shift_notes: str,
        alarms_json: Optional[Dict[str, Any]],
        trends_csv: Optional[str]
    ) -> str:
        """Build the complete prompt with all context"""

        prompt_parts = [
            self.SYSTEM_PROMPT,
            "\n\n=== SHIFT HANDOVER NOTES ===\n",
            shift_notes
        ]

        if alarms_json:
            formatted_alarms = format_alarms_json(alarms_json)
            prompt_parts.extend([
                "\n\n=== ALARMS DATA (JSON) ===\n",
                formatted_alarms
            ])

        if trends_csv:
            trend_summary = parse_csv_to_summary(trends_csv)
            if trend_summary:
                prompt_parts.extend([
                    "\n\n=== TREND DATA SUMMARY ===\n",
                    trend_summary
                ])

        prompt_parts.append(
            "\n\nNow generate the structured handover report as specified."
        )

        return "".join(prompt_parts)

    def _repair_json_with_gemini(self, invalid_response: str) -> Dict[str, Any]:
        """Use Gemini to repair invalid JSON response"""

        repair_prompt = f"""The following response should contain valid JSON but is malformed:

{invalid_response}

Please extract and return ONLY a valid JSON object that matches this schema:
{{
  "shiftSummary": ["..."],
  "criticalAlarms": [{{"alarm": "...", "meaning": "..."}}],
  "openIssues": [{{"issue": "...", "priority": "High|Med|Low", "confidence": 0-100}}],
  "recommendedActions": ["..."],
  "questions": ["..."]
}}

Return ONLY the JSON object, nothing else."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=repair_prompt
            )
            repaired_text = response.text

            # Try to extract JSON
            json_data = extract_json_from_text(repaired_text)
            if json_data:
                return validate_handover_json(json_data)

        except Exception as e:
            logger.error(f"JSON repair failed: {e}", exc_info=True)

        # If repair fails, return minimal structure
        return {
            'shiftSummary': ["Could not parse Gemini response"],
            'criticalAlarms': [],
            'openIssues': [],
            'recommendedActions': ["Review original shift notes manually"],
            'questions': []
        }

    def generate_handover(
        self,
        shift_notes: str,
        alarms_json: Optional[Dict[str, Any]] = None,
        trends_csv: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate handover summary using Gemini.

        Returns:
            Tuple of (markdown_string, structured_json_dict)
        """

        # Build the prompt
        prompt = self._build_prompt(shift_notes, alarms_json, trends_csv)
        try:
            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            response_text = response.text

            # Extract JSON from response
            json_data = extract_json_from_text(response_text)

            if not json_data:
                logger.warning("Failed to extract JSON, attempting repair...")
                json_data = self._repair_json_with_gemini(response_text)
            else:
                # Validate and repair the JSON structure
                json_data = validate_handover_json(json_data)

            # Check if response contains markdown, otherwise generate it
            if "# Shift Handover" in response_text or "## " in response_text:
                # Extract markdown portion (after JSON block)
                parts = response_text.split("```")
                markdown = parts[-1].strip() if len(parts) > 2 else response_text

                # If markdown is too short, generate it
                if len(markdown) < 100:
                    markdown = create_markdown_from_structured(json_data)
            else:
                # Generate markdown from structured data
                markdown = create_markdown_from_structured(json_data)

            return markdown, json_data

        except Exception as e:
            # Error handling - return minimal valid response
            error_message = f"Error generating handover: {str(e)}"
            logger.error(error_message, exc_info=True)

            fallback_json = {
                'shiftSummary': [f"Error occurred: {str(e)}", "Please review shift notes manually"],
                'criticalAlarms': [],
                'openIssues': [{"issue": "Gemini API Error", "priority": "High", "confidence": 100}],
                'recommendedActions': ["Check API key and connection", "Retry the request"],
                'questions': []
            }

            fallback_markdown = create_markdown_from_structured(fallback_json)

            return fallback_markdown, fallback_json
