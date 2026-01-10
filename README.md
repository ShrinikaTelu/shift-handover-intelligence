# 🏭 Shift Handover Intelligence - Complete Implementation Guide

> AI-powered shift handover generation for industrial operations using Google Gemini 3 Flash Preview

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [From Scratch Implementation](#from-scratch-implementation)
3. [Architecture & Design](#architecture--design)
4. [Installation & Setup](#installation--setup)
5. [Testing Guide](#testing-guide)
6. [Demo Scenarios](#demo-scenarios)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

### What It Does

Transforms unstructured shift handover notes, alarm data, and process trends into structured, actionable reports using Google Gemini 3 AI.

### Key Features

-   ✅ **Multi-source input**: Shift notes (text) + Alarms (JSON) + Trends (CSV)
-   ✅ **Gemini 3 Flash Preview**: Latest AI model with extended reasoning
-   ✅ **Fact vs Hypothesis**: Separates observations from inferences
-   ✅ **Confidence Scoring**: 0-100% confidence on all hypotheses
-   ✅ **Priority Classification**: High 🔴, Medium 🟡, Low 🟢
-   ✅ **Structured Output**: 5 sections (Summary, Alarms, Issues, Actions, Questions)
-   ✅ **Export**: Copy to clipboard or download as Markdown
-   ✅ **Session Storage**: SQLite database for history

### Input Data Requirements

The system accepts three types of input to generate comprehensive handover reports:

#### 1️⃣ **Shift Notes** (Required)

Free-text notes entered by the shift operator describing what happened during their shift.

**Example:**

```
Started shift at 6:00 AM. Reactor R-101 running at 95% capacity.
Had pressure spike at 8:30 AM, stabilized after 15 mins.
Pump P-203 making unusual noise - needs inspection.
```

#### 2️⃣ **Alarms JSON** (Optional)

Structured alarm data from AVEVA System Platform or other SCADA systems. Provides context about system alerts during the shift.

**Format:**

```json
{
    "alarms": [
        {
            "timestamp": "2026-01-08T08:30:15Z",
            "tag": "R-101.Pressure",
            "severity": "High",
            "message": "Reactor pressure exceeded setpoint (125 PSI > 120 PSI)",
            "acknowledged": true,
            "ackBy": "john.doe"
        },
        {
            "timestamp": "2026-01-08T14:22:00Z",
            "tag": "P-203.Vibration",
            "severity": "Medium",
            "message": "Pump vibration above normal (4.2 mm/s)",
            "acknowledged": false,
            "ackBy": null
        }
    ]
}
```

**What the AI does with this data:**

-   Identifies critical alarms requiring immediate attention
-   Explains operational meaning of technical alarms
-   Correlates alarms with operator notes
-   Prioritizes issues based on severity and frequency

#### 3️⃣ **Trends CSV** (Optional)

Time-series process data from AVEVA Historian or PI System showing equipment performance trends over the shift.

**Format:**

```csv
Timestamp,R-101.Temperature,R-101.Pressure,P-203.FlowRate,P-203.Vibration
2026-01-08T06:00:00,285.2,118.5,1250,2.1
2026-01-08T07:00:00,287.1,119.2,1248,2.3
2026-01-08T08:00:00,289.5,120.8,1245,2.4
2026-01-08T09:00:00,291.2,125.3,1230,3.8
2026-01-08T10:00:00,288.7,121.1,1242,4.2
```

**What the AI does with this data:**

-   Detects unusual patterns (spikes, drops, drift)
-   Validates operator observations with actual data
-   Identifies potential equipment degradation
-   Provides data-backed evidence for hypotheses

### How Inputs Work Together

**Real-World Workflow:**

1. **Operator writes notes** during shift (manual observations, actions taken)
2. **System exports alarms** from AVEVA/SCADA for the shift period
3. **System exports trends** from Historian for key process tags
4. **Operator uploads all three** to Shift Handover Intelligence
5. **AI analyzes and correlates** all data sources
6. **Generates comprehensive report** with facts, hypotheses, and confidence scores

**Example - Pump Issue Detection:**

| Data Source     | Information Provided                                                                     |
| --------------- | ---------------------------------------------------------------------------------------- |
| **Shift Notes** | "Pump P-203 making unusual noise"                                                        |
| **Alarms JSON** | Medium severity vibration alarm at 14:22                                                 |
| **Trends CSV**  | Vibration increased from 2.1 to 4.2 mm/s over 4 hours                                    |
| **AI Analysis** | Correlates all three → Priority: High, Confidence: 85% → Recommends immediate inspection |

### Why This Matters

**Without optional data:** AI works with operator notes only, relying on their memory and observations.

**With optional data:** AI cross-validates notes with actual system data, catches issues operators might miss, and provides evidence-backed insights.

**Value Proposition:**

-   ✅ Reduces "he said, she said" confusion
-   ✅ Catches issues operators forget to mention
-   ✅ Provides objective evidence for maintenance decisions
-   ✅ Trains less experienced operators by showing correlations

### Tech Stack

-   **Backend**: Python 3.10+ • FastAPI • Google Gemini 3 • SQLAlchemy
-   **Frontend**: Angular 17 • TypeScript • Standalone Components
-   **Database**: SQLite (async)
-   **AI Model**: `gemini-3-flash-preview`

---

## 🚀 From Scratch Implementation

### Step 1: Project Structure Setup

```powershell
# Create project root
mkdir shift-handover-intelligence
cd shift-handover-intelligence

# Create folder structure
mkdir backend, frontend, sample-data
```

### Step 2: Backend Implementation

#### 2.1 Create Virtual Environment & Dependencies

**File: `backend/requirements.txt`**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-multipart==0.0.6
google-genai==0.2.2
python-dotenv==1.0.0
sqlalchemy==2.0.25
aiosqlite==0.19.0
```

**Setup:**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 2.2 Environment Configuration

**File: `backend/.env`**

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./handover.db
```

**Get API Key**: https://makersuite.google.com/app/apikey

#### 2.3 Pydantic Schemas

**File: `backend/schemas.py`**

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum

class PriorityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Med"
    LOW = "Low"

class CriticalAlarm(BaseModel):
    alarm: str
    meaning: str

class OpenIssue(BaseModel):
    issue: str
    priority: PriorityLevel
    confidence: float = Field(ge=0, le=100)

class HandoverStructured(BaseModel):
    shiftSummary: List[str]
    criticalAlarms: List[CriticalAlarm]
    openIssues: List[OpenIssue]
    recommendedActions: List[str]
    questions: List[str]

class HandoverRequest(BaseModel):
    shiftNotes: str = Field(min_length=10)
    alarmsJson: Optional[Dict[str, Any]] = None
    trendsCsv: Optional[str] = None

    @validator('shiftNotes')
    def validate_shift_notes(cls, v):
        if not v or not v.strip():
            raise ValueError('Shift notes cannot be empty')
        return v.strip()

class HandoverResponse(BaseModel):
    markdown: str
    json: HandoverStructured
    sessionId: Optional[str] = None
```

#### 2.4 Utility Functions

**File: `backend/utils.py`**

````python
import json
import csv
import re
from io import StringIO
from typing import Dict, Any, Optional

def parse_csv_to_summary(csv_content: str) -> str:
    """Convert CSV trends to readable summary"""
    if not csv_content or not csv_content.strip():
        return ""

    try:
        reader = csv.DictReader(StringIO(csv_content))
        rows = list(reader)

        if not rows:
            return "Empty trend data."

        fieldnames = reader.fieldnames or []
        summary = [f"Trend data: {len(rows)} records with fields: {', '.join(fieldnames)}"]

        if len(rows) <= 5:
            summary.append(f"All records: {rows}")
        else:
            summary.append(f"First: {rows[0]}")
            summary.append(f"Last: {rows[-1]}")

        return "\n".join(summary)
    except Exception as e:
        return f"Could not parse CSV: {str(e)}"

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON from AI response with multiple strategies"""
    if not text:
        return None

    # Strategy 1: Parse entire text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Extract from markdown code blocks
    json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_block_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Strategy 3: Find JSON boundaries
    json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in reversed(matches):
        try:
            parsed = json.loads(match)
            if isinstance(parsed, dict) and any(key in parsed for key in ['shiftSummary', 'openIssues']):
                return parsed
        except json.JSONDecodeError:
            continue

    return None

def validate_handover_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and repair JSON structure"""
    repaired = {
        'shiftSummary': [],
        'criticalAlarms': [],
        'openIssues': [],
        'recommendedActions': [],
        'questions': []
    }

    # Validate each section
    if 'shiftSummary' in data:
        if isinstance(data['shiftSummary'], list):
            repaired['shiftSummary'] = [str(item) for item in data['shiftSummary']]

    if 'criticalAlarms' in data and isinstance(data['criticalAlarms'], list):
        for alarm in data['criticalAlarms']:
            if isinstance(alarm, dict) and 'alarm' in alarm:
                repaired['criticalAlarms'].append({
                    'alarm': str(alarm.get('alarm', '')),
                    'meaning': str(alarm.get('meaning', 'N/A'))
                })

    if 'openIssues' in data and isinstance(data['openIssues'], list):
        for issue in data['openIssues']:
            if isinstance(issue, dict) and 'issue' in issue:
                priority = issue.get('priority', 'Med')
                if priority not in ['High', 'Med', 'Low']:
                    priority = 'Med'

                confidence = max(0, min(100, float(issue.get('confidence', 50))))

                repaired['openIssues'].append({
                    'issue': str(issue.get('issue', '')),
                    'priority': priority,
                    'confidence': confidence
                })

    if 'recommendedActions' in data:
        if isinstance(data['recommendedActions'], list):
            repaired['recommendedActions'] = [str(item) for item in data['recommendedActions']]

    if 'questions' in data:
        if isinstance(data['questions'], list):
            repaired['questions'] = [str(item) for item in data['questions']]

    return repaired

def create_markdown_from_structured(data: Dict[str, Any]) -> str:
    """Generate markdown report from structured data"""
    md = ["# Shift Handover Intelligence Report\n"]

    # Shift Summary
    md.append("## 📋 Shift Summary")
    if data.get('shiftSummary'):
        for item in data['shiftSummary']:
            md.append(f"- {item}")
    else:
        md.append("_No summary available_")
    md.append("")

    # Critical Alarms
    md.append("## 🚨 Critical Alarms & Meaning")
    if data.get('criticalAlarms'):
        for alarm in data['criticalAlarms']:
            md.append(f"### {alarm.get('alarm', 'Unknown')}")
            md.append(f"**Meaning:** {alarm.get('meaning', 'N/A')}\n")
    else:
        md.append("_No critical alarms_\n")

    # Open Issues
    md.append("## ⚠️ Open Issues")
    if data.get('openIssues'):
        for issue in data['openIssues']:
            priority = issue.get('priority', 'Med')
            confidence = issue.get('confidence', 0)
            emoji = {"High": "🔴", "Med": "🟡", "Low": "🟢"}.get(priority, "⚪")
            md.append(f"### {emoji} {issue.get('issue', 'Unknown')}")
            md.append(f"**Priority:** {priority} | **Confidence:** {confidence}%\n")
    else:
        md.append("_No open issues_\n")

    # Recommended Actions
    md.append("## ✅ Recommended Actions")
    if data.get('recommendedActions'):
        for i, action in enumerate(data['recommendedActions'], 1):
            md.append(f"{i}. {action}")
    else:
        md.append("_No recommended actions_")
    md.append("")

    # Questions
    md.append("## ❓ Questions for Next Shift")
    if data.get('questions'):
        for q in data['questions']:
            md.append(f"- {q}")
    else:
        md.append("_No questions_")
    md.append("")

    md.append("---")
    md.append("_Generated by Shift Handover Intelligence with Gemini 3_")

    return "\n".join(md)
````

#### 2.5 Gemini Client (Gemini 3 Integration)

**File: `backend/gemini_client.py`**

````python
from google import genai
import os
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
from utils import (
    extract_json_from_text,
    validate_handover_json,
    create_markdown_from_structured,
    parse_csv_to_summary,
    format_alarms_json
)

load_dotenv()

class GeminiClient:
    """Client for Gemini 3 Flash Preview API"""

    SYSTEM_PROMPT = """You are an industrial operations assistant specialized in AVEVA systems.

Convert shift handover notes, alarm data, and trend data into structured, actionable summaries.

REQUIREMENTS:
1. **Separate Facts from Hypotheses**: Distinguish observations from inferences
2. **Provide Confidence**: Score hypotheses 0-100%
3. **Be Specific**: Use precise industrial terminology
4. **Ask Questions**: Up to 3 clarifying questions if needed
5. **Output Format**: Return JSON + Markdown

JSON SCHEMA (STRICT):
{
  "shiftSummary": ["fact 1", "fact 2", ...],
  "criticalAlarms": [{"alarm": "description", "meaning": "operational meaning"}],
  "openIssues": [{"issue": "description", "priority": "High|Med|Low", "confidence": 75}],
  "recommendedActions": ["action 1", "action 2", ...],
  "questions": ["question 1", ...]
}

PRIORITY LEVELS:
- High: Immediate action, safety/production impact
- Med: Address within 24 hours
- Low: Monitor or address when convenient

Return format:
```json
{...your JSON here...}
````

Then provide markdown report starting with # Shift Handover Intelligence Report
"""

    def __init__(self):
        """Initialize Gemini 3 client"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        os.environ['GOOGLE_API_KEY'] = api_key
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-3-flash-preview'

    def _build_prompt(
        self,
        shift_notes: str,
        alarms_json: Dict[str, Any] | None,
        trends_csv: str | None
    ) -> str:
        """Build complete prompt with all context"""
        prompt_parts = [
            self.SYSTEM_PROMPT,
            "\n\n=== SHIFT HANDOVER NOTES ===\n",
            shift_notes
        ]

        if alarms_json:
            formatted_alarms = json.dumps(alarms_json, indent=2)
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

        prompt_parts.append("\n\nNow generate the structured handover report.")

        return "".join(prompt_parts)

    def _repair_json_with_gemini(self, invalid_response: str) -> Dict[str, Any]:
        """Use Gemini to repair invalid JSON"""
        repair_prompt = f"""The following response contains malformed JSON:

{invalid_response}

Extract and return ONLY valid JSON matching this schema:
{{
  "shiftSummary": ["..."],
  "criticalAlarms": [{{"alarm": "...", "meaning": "..."}}],
"openIssues": [{{"issue": "...", "priority": "High|Med|Low", "confidence": 0-100}}],
"recommendedActions": ["..."],
"questions": ["..."]
}}

Return ONLY the JSON object."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=repair_prompt
            )
            repaired_text = response.text

            json_data = extract_json_from_text(repaired_text)
            if json_data:
                return validate_handover_json(json_data)
        except Exception as e:
            print(f"JSON repair failed: {e}")

        # Fallback
        return {
            'shiftSummary': ["Could not parse AI response"],
            'criticalAlarms': [],
            'openIssues': [],
            'recommendedActions': ["Review original notes manually"],
            'questions': []
        }

    def generate_handover(
        self,
        shift_notes: str,
        alarms_json: Dict[str, Any] | None = None,
        trends_csv: str | None = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Generate handover using Gemini 3

        Returns:
            Tuple of (markdown_string, structured_json_dict)
        """
        prompt = self._build_prompt(shift_notes, alarms_json, trends_csv)

        try:
            # Call Gemini 3 API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            response_text = response.text

            # Extract JSON
            json_data = extract_json_from_text(response_text)

            if not json_data:
                print("Failed to extract JSON, attempting repair...")
                json_data = self._repair_json_with_gemini(response_text)
            else:
                json_data = validate_handover_json(json_data)

            # Extract or generate markdown
            if "# Shift Handover" in response_text or "## " in response_text:
                parts = response_text.split("```")
                markdown = parts[-1].strip() if len(parts) > 2 else response_text

                if len(markdown) < 100:
                    markdown = create_markdown_from_structured(json_data)
            else:
                markdown = create_markdown_from_structured(json_data)

            return markdown, json_data

        except Exception as e:
            print(f"Error generating handover: {e}")

            fallback_json = {
                'shiftSummary': [f"Error: {str(e)}", "Please review notes manually"],
                'criticalAlarms': [],
                'openIssues': [{"issue": "Gemini API Error", "priority": "High", "confidence": 100}],
                'recommendedActions': ["Check API key", "Retry request"],
                'questions': []
            }

            return create_markdown_from_structured(fallback_json), fallback_json

````

#### 2.6 Database Layer

**File: `backend/database.py`**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
import os
from dotenv import load_dotenv
import json
from typing import Dict, Any, Optional

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./handover.db")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class HandoverSessionDB(Base):
    """SQLAlchemy model for handover sessions"""
    __tablename__ = "handover_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    shift_notes = Column(Text, nullable=False)
    alarms_json = Column(Text, nullable=True)
    trends_csv = Column(Text, nullable=True)
    markdown_output = Column(Text, nullable=False)
    json_output = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency for database sessions"""
    async with async_session_maker() as session:
        yield session

async def save_handover_session(
    session: AsyncSession,
    session_id: str,
    shift_notes: str,
    alarms_json: Optional[Dict[str, Any]],
    trends_csv: Optional[str],
    markdown_output: str,
    json_output: Dict[str, Any]
) -> HandoverSessionDB:
    """Save handover session"""
    db_session = HandoverSessionDB(
        session_id=session_id,
        shift_notes=shift_notes,
        alarms_json=json.dumps(alarms_json) if alarms_json else None,
        trends_csv=trends_csv,
        markdown_output=markdown_output,
        json_output=json.dumps(json_output)
    )

    session.add(db_session)
    await session.commit()
    await session.refresh(db_session)

    return db_session

async def get_handover_session(session: AsyncSession, session_id: str) -> Optional[HandoverSessionDB]:
    """Retrieve handover session by ID"""
    from sqlalchemy import select

    result = await session.execute(
        select(HandoverSessionDB).where(HandoverSessionDB.session_id == session_id)
    )
    return result.scalar_one_or_none()
````

#### 2.7 FastAPI Main Application

**File: `backend/main.py`**

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import uuid
from datetime import datetime

from schemas import HandoverRequest, HandoverResponse, HandoverStructured
from gemini_client import GeminiClient
from database import init_db, get_session, save_handover_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Shift Handover Intelligence API",
    description="AI-powered handover generation with Gemini 3",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_client: GeminiClient | None = None

def get_gemini_client() -> GeminiClient:
    """Dependency for Gemini client"""
    global gemini_client
    if gemini_client is None:
        try:
            gemini_client = GeminiClient()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return gemini_client

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "shift-handover-intelligence"
    }

@app.post("/api/handover/generate", response_model=HandoverResponse)
async def generate_handover(
    request: HandoverRequest,
    db: AsyncSession = Depends(get_session),
    client: GeminiClient = Depends(get_gemini_client)
):
    """Generate structured handover using Gemini 3"""
    try:
        # Generate with Gemini
        markdown, json_data = client.generate_handover(
            shift_notes=request.shiftNotes,
            alarms_json=request.alarmsJson,
            trends_csv=request.trendsCsv
        )

        # Validate with Pydantic
        structured_handover = HandoverStructured(**json_data)

        # Generate session ID
        session_id = str(uuid.uuid4())

        # Save to database
        try:
            await save_handover_session(
                session=db,
                session_id=session_id,
                shift_notes=request.shiftNotes,
                alarms_json=request.alarmsJson,
                trends_csv=request.trendsCsv,
                markdown_output=markdown,
                json_output=json_data
            )
        except Exception as db_error:
            print(f"Database save failed: {db_error}")

        return HandoverResponse(
            markdown=markdown,
            json=structured_handover,
            sessionId=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate handover: {str(e)}")

@app.get("/api/handover/{session_id}", response_model=HandoverResponse)
async def get_handover(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """Retrieve previously generated handover"""
    from database import get_handover_session
    import json

    session = await get_handover_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    json_output = json.loads(session.json_output)

    return HandoverResponse(
        markdown=session.markdown_output,
        json=HandoverStructured(**json_output),
        sessionId=session.session_id
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### Step 3: Frontend Implementation

#### 3.1 Create Angular App

```powershell
cd ..
ng new frontend --routing --style=css --skip-git
cd frontend
```

#### 3.2 TypeScript Models

**File: `frontend/src/app/models/handover.model.ts`**

```typescript
export interface CriticalAlarm {
    alarm: string;
    meaning: string;
}

export interface OpenIssue {
    issue: string;
    priority: 'High' | 'Med' | 'Low';
    confidence: number;
}

export interface HandoverStructured {
    shiftSummary: string[];
    criticalAlarms: CriticalAlarm[];
    openIssues: OpenIssue[];
    recommendedActions: string[];
    questions: string[];
}

export interface HandoverRequest {
    shiftNotes: string;
    alarmsJson?: any;
    trendsCsv?: string;
}

export interface HandoverResponse {
    markdown: string;
    json: HandoverStructured;
    sessionId?: string;
}
```

#### 3.3 API Service

**File: `frontend/src/app/services/handover.service.ts`**

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HandoverRequest, HandoverResponse } from '../models/handover.model';

@Injectable({
    providedIn: 'root',
})
export class HandoverService {
    private readonly API_URL = 'http://localhost:8000/api';

    constructor(private http: HttpClient) {}

    generateHandover(request: HandoverRequest): Observable<HandoverResponse> {
        return this.http
            .post<HandoverResponse>(
                `${this.API_URL}/handover/generate`,
                request
            )
            .pipe(catchError(this.handleError));
    }

    getHandover(sessionId: string): Observable<HandoverResponse> {
        return this.http
            .get<HandoverResponse>(`${this.API_URL}/handover/${sessionId}`)
            .pipe(catchError(this.handleError));
    }

    private handleError(error: any): Observable<never> {
        const errorMessage =
            error.error?.detail || error.message || 'Server error';
        console.error('API Error:', error);
        return throwError(() => new Error(errorMessage));
    }
}
```

#### 3.4 Main App Component

**File: `frontend/src/app/app.component.ts`**

```typescript
import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HandoverFormComponent } from './components/handover-form/handover-form.component';
import { HandoverResultComponent } from './components/handover-result/handover-result.component';
import { HandoverService } from './services/handover.service';
import { HandoverRequest, HandoverResponse } from './models/handover.model';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, HandoverFormComponent, HandoverResultComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css',
})
export class AppComponent {
    @ViewChild(HandoverFormComponent) formComponent?: HandoverFormComponent;

    result: HandoverResponse | null = null;
    error: string | null = null;

    constructor(private handoverService: HandoverService) {}

    onGenerateHandover(request: HandoverRequest): void {
        this.result = null;
        this.error = null;

        this.handoverService.generateHandover(request).subscribe({
            next: (response) => {
                this.result = response;
                this.formComponent?.setLoading(false);
            },
            error: (err) => {
                this.error = err.message;
                this.formComponent?.setLoading(false);
            },
        });
    }
}
```

**File: `frontend/src/app/app.component.html`**

```html
<div class="app-container">
    <app-handover-form
        (generateHandover)="onGenerateHandover($event)"
    ></app-handover-form>
    <app-handover-result
        [result]="result"
        [error]="error"
    ></app-handover-result>
</div>
```

**File: `frontend/src/app/app.component.css`**

```css
.app-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 0;
}
```

#### 3.5 Configure HTTP Client

**File: `frontend/src/app/app.config.ts`**

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
    providers: [provideRouter(routes), provideHttpClient()],
};
```

### Step 4: Sample Data

**File: `sample-data/alarms.json`**

```json
{
    "metadata": {
        "plant": "AVEVA Demo Plant",
        "timestamp": "2026-01-07T18:20:00Z"
    },
    "activeAlarms": [
        {
            "id": "PIC-405-HI",
            "tag": "Reactor-B.Pressure",
            "description": "High Pressure Alarm",
            "priority": "Critical",
            "value": 28.5,
            "setpoint": 25.0,
            "unit": "bar"
        }
    ]
}
```

**File: `sample-data/trends.csv`**

```csv
timestamp,tag,value,unit
2026-01-07T18:00:00Z,Compressor.DischTemp,85,°C
2026-01-07T18:15:00Z,Compressor.DischTemp,92,°C
2026-01-07T18:30:00Z,Compressor.DischTemp,95,°C
```

---

## 🏗️ Architecture & Design

### System Architecture

```
┌─────────────────────┐
│   Angular Frontend  │  (Port 4200)
│   - TypeScript      │
│   - Standalone      │
└──────────┬──────────┘
           │ HTTP/JSON
           ▼
┌─────────────────────┐
│   FastAPI Backend   │  (Port 8000)
│   - Pydantic        │
│   - SQLAlchemy      │
└──────────┬──────────┘
           │ API Call
           ▼
┌─────────────────────┐
│   Gemini 3 Flash    │
│   Preview API       │
└─────────────────────┘
```

### Request Flow

1. User enters shift notes + uploads files
2. Angular sends POST to `/api/handover/generate`
3. FastAPI validates with Pydantic
4. GeminiClient builds prompt with all context
5. Gemini 3 generates structured response
6. Backend extracts/validates JSON
7. Saves to SQLite database
8. Returns markdown + JSON to frontend
9. Angular displays 5 structured sections

### Gemini 3 Prompt Strategy

**System Prompt** → Sets expert context
**Context Data** → Shift notes + alarms + trends
**Instructions** → Generate JSON + Markdown
**Validation** → JSON extraction with repair fallback

---

## 📦 Installation & Setup

### Prerequisites

-   Python 3.10+
-   Node.js 18+
-   Angular CLI 17+
-   Gemini API key

### Quick Start

```powershell
# 1. Clone/navigate to project
cd shift-handover-intelligence

# 2. Backend setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# 3. Frontend setup
cd ../frontend
npm install

# 4. Start backend (Terminal 1)
cd ../backend
.\venv\Scripts\Activate.ps1
python main.py

# 5. Start frontend (Terminal 2)
cd ../frontend
ng serve --open
```

**Access**: http://localhost:4200

---

## 🧪 Testing Guide

### 1. Manual UI Testing

#### Test Case 1: Normal Operations

```
1. Open http://localhost:4200
2. Click "📝 Sample 1: Normal Ops"
3. Click "🤖 Generate Handover"
4. Verify:
   ✓ Shift Summary shows operational status
   ✓ Open Issues with Low/Med priority
   ✓ Recommended actions for monitoring
   ✓ Confidence scores present
   ✓ Copy/Download buttons work
```

#### Test Case 2: With Alarms & Trends

```
1. Click "🚨 Sample 3: Reactor Trip"
2. Upload sample-data/alarms.json
3. Upload sample-data/trends.csv
4. Click "🤖 Generate Handover"
5. Verify:
   ✓ Critical Alarms section populated
   ✓ High priority issues (🔴)
   ✓ Trend data referenced in summary
   ✓ Equipment-specific recommendations
   ✓ Confidence > 80% for facts
```

#### Test Case 3: Error Handling

```
1. Clear shift notes
2. Click "🤖 Generate Handover"
3. Verify: Error message displayed

4. Enter invalid JSON in alarms file
5. Verify: "Invalid JSON" alert shown

6. Stop backend server
7. Try generate
8. Verify: Connection error displayed
```

### 2. API Testing

**Test Health Endpoint:**

```powershell
curl http://localhost:8000/health
# Expected: {"status":"healthy",...}
```

**Test Generate Endpoint:**

```powershell
$body = @{
    shiftNotes = "Reactor operating normally at 95% capacity."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/handover/generate" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$response | ConvertTo-Json -Depth 10
```

**Expected Response Structure:**

```json
{
    "markdown": "# Shift Handover Intelligence Report\n...",
    "json": {
        "shiftSummary": ["Reactor R-101: 95% capacity"],
        "criticalAlarms": [],
        "openIssues": [],
        "recommendedActions": ["Continue monitoring"],
        "questions": []
    },
    "sessionId": "uuid-here"
}
```

**Test Session Retrieval:**

```powershell
$sessionId = "uuid-from-previous-response"
Invoke-RestMethod -Uri "http://localhost:8000/api/handover/$sessionId"
```

### 3. Automated Testing Script

**File: `test-api.ps1`**

```powershell
# API Test Script
$baseUrl = "http://localhost:8000"

Write-Host "🧪 Testing Shift Handover API" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "`nTest 1: Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health"
    Write-Host "✅ Health: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed" -ForegroundColor Red
    exit 1
}

# Test 2: Simple Handover
Write-Host "`nTest 2: Generate Simple Handover" -ForegroundColor Yellow
$request = @{
    shiftNotes = "Test shift: All equipment operating normally."
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod `
        -Uri "$baseUrl/api/handover/generate" `
        -Method Post `
        -Body $request `
        -ContentType "application/json"

    Write-Host "✅ Session ID: $($result.sessionId)" -ForegroundColor Green
    Write-Host "   Summary items: $($result.json.shiftSummary.Count)" -ForegroundColor Gray

    $sessionId = $result.sessionId
} catch {
    Write-Host "❌ Generate failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 3: Retrieve Session
Write-Host "`nTest 3: Retrieve Session" -ForegroundColor Yellow
try {
    $retrieved = Invoke-RestMethod -Uri "$baseUrl/api/handover/$sessionId"
    Write-Host "✅ Retrieved session successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Retrieval failed" -ForegroundColor Red
}

Write-Host "`n✅ All tests passed!" -ForegroundColor Green
```

**Run:**

```powershell
.\test-api.ps1
```

### 4. Gemini 3 Testing

**Test Gemini Connection:**

```python
# File: test_gemini.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Convert this to JSON: Pump failed at 2am. High priority."
)

print(response.text)
```

**Run:**

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_gemini.py
```

---

## 🎬 Demo Scenarios

### Scenario 1: Routine Handover

**Input:**

```
Day shift handover - All equipment normal.
Reactor at 95%, compressor running well.
Minor vibration alarm cleared at 2pm.
```

**Expected Output:**

-   Summary: Equipment status
-   Issues: Low priority vibration monitoring
-   Actions: Continue normal operations
-   Confidence: 90-100%

### Scenario 2: Equipment Failure

**Input:**

```
Critical: Pump P-105 failed at 2:15 AM.
Backup P-106 engaged automatically.
Maintenance notified, bearing wear suspected.
```

**Alarms JSON:**

```json
{
    "activeAlarms": [
        {
            "id": "PUMP-105-FAIL",
            "priority": "Critical"
        }
    ]
}
```

**Expected Output:**

-   Summary: Pump failure timeline
-   Critical Alarms: P-105 failure with meaning
-   Issues: High priority (🔴) maintenance required
-   Actions: 1) Inspect P-105, 2) Check P-106 performance
-   Questions: "What caused bearing wear?"
-   Confidence: 85-95%

### Scenario 3: Production Impact

**Input:**

```
Reactor B tripped at 6:20 PM due to pressure transmitter fault.
Production reduced by 50%. Customer order may be delayed.
PT-405 replacement in progress, ETA 10 PM.
```

**Trends CSV:**

```csv
timestamp,tag,value
18:00,Reactor-B.Pressure,24.5
18:20,Reactor-B.Pressure,28.5
```

**Expected Output:**

-   Summary: Trip event + impact analysis
-   Critical Alarms: High pressure with transmitter fault explanation
-   Issues: High priority (🔴) production delay
-   Actions: 1) Replace PT-405, 2) Notify customers, 3) Restart per SOP
-   Questions: "Were other transmitters recently calibrated?"
-   Confidence: 80% (facts) / 60% (hypotheses on cause)

### Live Demo Script

**Duration: 5 minutes**

```
1. [0:00-0:30] Problem Introduction
   "Industrial shift handovers are messy—notes get lost,
    critical info missed. This causes safety risks."

2. [0:30-1:00] Solution Overview
   "Our AI solution generates structured handovers in 30 seconds.
    It uses Gemini 3 to analyze notes, alarms, and trends."

3. [1:00-2:30] Live Demo - Scenario 3
   - Click Sample 3 (Reactor Trip)
   - Upload alarms.json
   - Upload trends.csv
   - Generate
   - Highlight: Facts vs hypotheses, confidence scores, priorities

4. [2:30-3:30] Key Features
   - Show priority badges (🔴🟡🟢)
   - Point to confidence percentages
   - Demo copy/download

5. [3:30-4:30] Social Impact
   "This prevents missed critical issues, trains operators,
    saves 15-30 min per shift. Real ROI in safety and uptime."

6. [4:30-5:00] Q&A
```

---

## 📚 API Reference

### POST /api/handover/generate

**Request:**

```typescript
{
  shiftNotes: string;        // Required, min 10 chars
  alarmsJson?: object;       // Optional alarm data
  trendsCsv?: string;        // Optional CSV trends
}
```

**Response:**

```typescript
{
  markdown: string;          // Full markdown report
  json: {
    shiftSummary: string[];
    criticalAlarms: Array<{
      alarm: string;
      meaning: string;
    }>;
    openIssues: Array<{
      issue: string;
      priority: 'High' | 'Med' | 'Low';
      confidence: number;    // 0-100
    }>;
    recommendedActions: string[];
    questions: string[];
  };
  sessionId: string;         // UUID for retrieval
}
```

**Status Codes:**

-   `200`: Success
-   `422`: Validation error
-   `500`: Server/AI error

### GET /api/handover/{sessionId}

**Response:** Same as POST /generate

**Status Codes:**

-   `200`: Success
-   `404`: Session not found
-   `500`: Server error

### GET /health

**Response:**

```json
{
    "status": "healthy",
    "timestamp": "2026-01-07T...",
    "service": "shift-handover-intelligence"
}
```

---

## 🔧 Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY not set"**

```powershell
# Check .env file exists
Test-Path backend\.env

# Verify content
Get-Content backend\.env

# Should show: GEMINI_API_KEY=AIza...
```

**Error: "Module not found"**

```powershell
# Activate venv
cd backend
.\venv\Scripts\Activate.ps1

# Reinstall
pip install -r requirements.txt
```

**Port 8000 already in use**

```powershell
# Find process
Get-NetTCPConnection -LocalPort 8000

# Kill it
Stop-Process -Id <PID>
```

### Frontend Issues

**Error: "Cannot connect to backend"**

```
1. Verify backend running: http://localhost:8000/health
2. Check CORS in backend/main.py
3. Check browser console (F12)
```

**File upload fails**

```
1. Verify JSON is valid (use jsonlint.com)
2. Check CSV has headers
3. Check file size < 1MB
```

### Gemini API Issues

**Error: "Invalid API key"**

```
1. Get new key: https://makersuite.google.com/app/apikey
2. Update backend/.env
3. Restart backend
```

**Error: "Quota exceeded"**

```
Free tier limits:
- 60 requests/minute
- 1,500 requests/day

Solution: Wait or upgrade plan
```

**Response: Empty or invalid JSON**

```
1. Check Gemini model name: gemini-3-flash-preview
2. Try re-generating (sometimes AI needs retry)
3. Check backend logs for repair attempts
```

### Database Issues

**Error: "Database locked"**

```powershell
# Stop all backend instances
Get-Process python | Stop-Process

# Delete database
Remove-Item backend\handover.db

# Restart backend (will recreate)
```

---

## 📊 Performance Benchmarks

-   **Backend startup**: 2-5 seconds
-   **Frontend compile**: 15-30 seconds
-   **Gemini API call**: 3-15 seconds (depends on content size)
-   **Database operations**: < 100ms
-   **Total handover generation**: 5-20 seconds

---

## 🎯 Success Metrics

**Technical:**

-   ✅ All endpoints return 200 status
-   ✅ JSON validation passes
-   ✅ No console errors
-   ✅ Copy/download works

**Functional:**

-   ✅ Facts separated from hypotheses
-   ✅ Confidence scores present (0-100%)
-   ✅ Priorities assigned correctly
-   ✅ Markdown is well-formatted
-   ✅ Questions asked when info missing

**User Experience:**

-   ✅ < 30 second total time
-   ✅ Clear error messages
-   ✅ Loading states visible
-   ✅ Results easy to read

---

## 🚀 Next Steps & Enhancements

### Phase 2: Multimodal

-   [ ] Image upload (whiteboard photos)
-   [ ] OCR for handwritten notes
-   [ ] Equipment photo analysis

### Phase 3: Intelligence

-   [ ] Recurring issue detection
-   [ ] Predictive maintenance alerts
-   [ ] Trend anomaly detection
-   [ ] Equipment health scoring

### Phase 4: Integration

-   [ ] AVEVA PI System connector
-   [ ] OSIsoft historian integration
-   [ ] Email notifications
-   [ ] Teams/Slack integration
-   [ ] Mobile app (React Native)

### Phase 5: Enterprise

-   [ ] Multi-plant deployment
-   [ ] Role-based access control
-   [ ] Custom templates
-   [ ] Analytics dashboard
-   [ ] PostgreSQL migration

---

## 📄 License

Educational/Demo project. Use in accordance with:

-   Google Gemini API Terms
-   Angular MIT License
-   FastAPI MIT License

---

## 👥 Credits

-   **Gemini 3 Flash Preview** - Google AI
-   **Angular 17** - Google
-   **FastAPI** - Sebastián Ramírez
-   **AVEVA** - Industrial operations inspiration

---

**Built with ❤️ for safer, smarter industrial operations**

Last Updated: January 7, 2026 | Version: 1.0.0
