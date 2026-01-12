# 📘 Shift Handover Intelligence - Complete Implementation Guide

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Solution Architecture](#3-solution-architecture)
4. [Features Explained](#4-features-explained)
5. [Technology Stack](#5-technology-stack)
6. [Implementation Details](#6-implementation-details)
   - [6.1 Backend Implementation](#61-backend-implementation)
   - [6.2 Frontend Implementation](#62-frontend-implementation)
   - [6.3 Google Gemini AI Integration](#63-google-gemini-ai-integration---complete-guide)
     - [6.3.1 Overview](#631-overview-of-gemini-ai-in-this-project)
     - [6.3.2 Obtaining API Key](#632-obtaining-a-gemini-api-key)
     - [6.3.3 API Key Configuration](#633-api-key-configuration)
     - [6.3.4 Code Implementation](#634-code-implementation-deep-dive)
     - [6.3.5 Making API Calls](#635-making-api-calls)
     - [6.3.6 System Prompt Engineering](#636-system-prompt-engineering)
     - [6.3.7 Error Handling](#637-error-handling--resilience)
     - [6.3.8 API Usage & Rate Limits](#638-api-usage--rate-limits)
     - [6.3.9 Testing Integration](#639-testing-the-gemini-integration)
     - [6.3.10 Security Considerations](#6310-security-considerations)
     - [6.3.11 Troubleshooting](#6311-troubleshooting-gemini-api-issues)
7. [API Documentation](#7-api-documentation)
8. [Testing Guide](#8-testing-guide)
9. [Deployment Guide](#9-deployment-guide)
10. [Troubleshooting](#10-troubleshooting)
11. [Demo Examples](#11-demo-examples)
12. [Future Enhancements](#12-future-enhancements)

---

## 1. Project Overview

**Shift Handover Intelligence** is an AI-powered application designed to transform unstructured shift notes, alarm data, and trend information into professional, structured handover reports. It leverages Google's Gemini AI to intelligently analyze and organize industrial shift data.

### Live URLs
- **Frontend**: https://shrinikatelu.github.io/shift-handover-intelligence/
- **Backend API**: https://shift-handover-intelligence-production.up.railway.app/
- **API Docs (Swagger)**: https://shift-handover-intelligence-production.up.railway.app/docs

---

## 2. Problem Statement

### The Challenge

In industrial settings (manufacturing plants, refineries, pharmaceutical facilities, etc.), shift handovers are critical for operational continuity. However, traditional handover processes face several challenges:

1. **Unstructured Information**: Operators write notes in free-form text, making it hard to extract key information
2. **Inconsistent Format**: Each operator has their own style, leading to varying quality of handovers
3. **Time-Consuming**: Creating structured reports manually takes valuable time
4. **Information Loss**: Important details may be buried in lengthy notes
5. **No Standardization**: Lack of consistent format across shifts and teams

### Real-World Examples

#### Example 1: Pharmaceutical Manufacturing
```
Raw shift notes:
"Started batch 2024-001 at 0600. Reactor temp hit 85C at 0730, had to adjust cooling.
API addition completed by 1100. QC samples sent. Pump P-102 making noise again,
told maintenance. Lunch break 1200-1230. Finished batch at 1400, yield looks good
around 98%. Need to check filter F-201 tomorrow, pressure dropping."
```

**Problem**: Key information (batch ID, yield, equipment issues) is mixed with routine activities.

#### Example 2: Oil Refinery
```
Raw shift notes:
"Night shift quiet until 0300 when we got high level alarm on V-101. Drained
to V-102. Compressor K-301 tripped at 0415, restarted after 10 min. Flow rates
stable. Received 3 trucks of crude. Lab results pending for stream 5."
```

**Problem**: Critical events (alarms, trips) need to be highlighted separately from routine operations.

### The Solution

Shift Handover Intelligence uses AI to:
- ✅ Parse unstructured text and extract key information
- ✅ Categorize events (safety, equipment, process, pending actions)
- ✅ Generate consistent, professional reports
- ✅ Integrate alarm and trend data for context
- ✅ Create downloadable PDF reports

---

## 3. Solution Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                             │
│                        (Angular 18 Frontend)                         │
│                                                                      │
│   ┌────────────────┐   ┌────────────────┐   ┌────────────────────┐  │
│   │  Shift Notes   │   │  Alarms JSON   │   │   Trends CSV       │  │
│   │  Text Input    │   │  Input         │   │   Input            │  │
│   └───────┬────────┘   └───────┬────────┘   └─────────┬──────────┘  │
│           │                    │                       │             │
│           └────────────────────┼───────────────────────┘             │
│                                │                                      │
│                     ┌──────────▼──────────┐                          │
│                     │   HandoverService   │                          │
│                     │   (HTTP Client)     │                          │
│                     └──────────┬──────────┘                          │
└────────────────────────────────┼────────────────────────────────────┘
                                 │ HTTPS
                                 │ REST API
┌────────────────────────────────┼────────────────────────────────────┐
│                                ▼                                     │
│                        BACKEND SERVER                                │
│                    (FastAPI + Python 3.9)                           │
│                                                                      │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │                     API Layer (main.py)                     │    │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │    │
│   │  │ /api/       │  │ /health     │  │ CORS Middleware     │ │    │
│   │  │ handover/*  │  │             │  │                     │ │    │
│   │  └──────┬──────┘  └─────────────┘  └─────────────────────┘ │    │
│   └─────────┼──────────────────────────────────────────────────┘    │
│             │                                                        │
│   ┌─────────▼──────────┐    ┌─────────────────────────────────┐     │
│   │   GeminiClient     │    │      PDF Generator              │     │
│   │ (gemini_client.py) │    │   (pdf_generator.py)            │     │
│   │                    │    │                                 │     │
│   │ • Prompt building  │    │ • Markdown to PDF conversion    │     │
│   │ • AI response      │    │ • Professional formatting       │     │
│   │ • JSON parsing     │    │ • ReportLab library             │     │
│   └─────────┬──────────┘    └─────────────────────────────────┘     │
│             │                                                        │
│             ▼                                                        │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                   Google Gemini AI API                       │   │
│   │                  (gemini-1.5-flash model)                    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                   SQLite Database                            │   │
│   │              (Async via aiosqlite)                           │   │
│   │                                                              │   │
│   │  handover_sessions table:                                    │   │
│   │  • session_id (UUID)                                         │   │
│   │  • shift_notes (TEXT)                                        │   │
│   │  • markdown_output (TEXT)                                    │   │
│   │  • json_output (JSON)                                        │   │
│   │  • created_at (TIMESTAMP)                                    │   │
│   └─────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input**: Operator enters shift notes, optional alarms JSON, optional trends CSV
2. **API Request**: Frontend sends POST request to `/api/handover/generate`
3. **AI Processing**: Backend sends data to Gemini AI with structured prompt
4. **Response Parsing**: AI returns markdown and JSON formatted handover
5. **Storage**: Handover saved to SQLite with unique session ID
6. **Display**: Frontend renders structured output with download option

---

## 4. Features Explained

### 4.1 AI-Powered Text Analysis

The core feature uses Google Gemini AI to:
- Extract key events from unstructured text
- Categorize information (safety, equipment, process, quality)
- Identify pending actions and recommendations
- Generate executive summaries

**How it works:**

```python
# gemini_client.py - Prompt structure
prompt = f"""
You are a shift handover assistant. Analyze the following shift information 
and create a structured handover report.

SHIFT NOTES:
{shift_notes}

ALARMS (if provided):
{alarms_json}

TRENDS (if provided):
{trends_csv}

Generate:
1. Executive Summary
2. Key Events (categorized)
3. Equipment Status
4. Safety Observations
5. Pending Actions
6. Recommendations for Next Shift
"""
```

### 4.2 Multi-Format Input Support

| Input Type | Format | Description |
|------------|--------|-------------|
| Shift Notes | Plain Text | Free-form operator notes |
| Alarms | JSON Array | `[{"time": "06:00", "tag": "P-101", "description": "High pressure", "priority": "High"}]` |
| Trends | CSV | `time,tag,value\n06:00,TI-101,85.5\n06:30,TI-101,87.2` |

### 4.3 Structured Output

The AI generates two outputs:
1. **Markdown**: Human-readable formatted report
2. **JSON**: Machine-readable structured data

**Example JSON Structure:**
```json
{
  "executiveSummary": "...",
  "shiftInfo": {
    "date": "2026-01-12",
    "shift": "Day",
    "operator": "..."
  },
  "keyEvents": [
    {
      "time": "06:00",
      "category": "Equipment",
      "description": "...",
      "priority": "Medium"
    }
  ],
  "equipmentStatus": [...],
  "safetyObservations": [...],
  "pendingActions": [...],
  "recommendations": [...]
}
```

### 4.4 PDF Report Generation

Professional PDF reports generated using ReportLab library:
- Company header and timestamp
- Formatted sections with colors
- Tables for structured data
- Download with automatic filename (date-based)

### 4.5 Session Management

- Each handover gets a unique UUID
- Stored in SQLite database
- Can be retrieved later via session ID
- Supports PDF download by session

---

## 5. Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Runtime |
| FastAPI | 0.109.0 | Web framework |
| Uvicorn | 0.27.0 | ASGI server |
| Pydantic | 2.5.3 | Data validation |
| SQLAlchemy | 2.0.25 | Database ORM |
| aiosqlite | 0.19.0 | Async SQLite |
| google-genai | 0.2.2 | Gemini AI SDK |
| ReportLab | 4.0.9 | PDF generation |
| python-dotenv | 1.0.0 | Environment config |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| Angular | 18.1.0 | UI framework |
| TypeScript | ~5.4.0 | Language |
| RxJS | ~7.8.0 | Reactive programming |
| Angular CLI | 18.1.0 | Build tools |

### DevOps

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Railway | Backend hosting |
| GitHub Pages | Frontend hosting |
| GitHub Actions | CI/CD (optional) |

---

## 6. Implementation Details

### 6.1 Backend Implementation

#### main.py - Core API

```python
# Key endpoints
@app.post("/api/handover/generate")
async def generate_handover(request: HandoverRequest):
    """
    1. Receives shift notes, alarms, trends
    2. Calls Gemini AI for processing
    3. Saves to database
    4. Returns structured response
    """
    
@app.get("/api/handover/{session_id}")
async def get_handover(session_id: str):
    """Retrieve previously generated handover"""

@app.post("/api/handover/download-pdf")
async def download_pdf(request: HandoverRequest):
    """Generate and stream PDF download"""
```

#### gemini_client.py - AI Integration

```python
class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        
    def generate_handover(self, shift_notes, alarms_json, trends_csv):
        # Build prompt
        # Call Gemini API
        # Parse response to markdown + JSON
        return markdown, json_data
```

#### CORS Configuration

```python
# Critical for GitHub Pages to communicate with Railway backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://shrinikatelu.github.io",  # Production
        "http://localhost:4200",            # Development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### 6.2 Frontend Implementation

#### handover.service.ts - API Communication

```typescript
@Injectable({ providedIn: 'root' })
export class HandoverService {
    private readonly API_URL = environment.apiUrl;
    
    generateHandover(request: HandoverRequest): Observable<HandoverResponse> {
        return this.http.post<HandoverResponse>(
            `${this.API_URL}/handover/generate`,
            request
        );
    }
    
    downloadPdf(request: HandoverRequest): Observable<Blob> {
        return this.http.post(
            `${this.API_URL}/handover/download-pdf`,
            request,
            { responseType: 'blob' }
        );
    }
}
```

#### Environment Configuration

```typescript
// environment.ts (production)
export const environment = {
    production: true,
    apiUrl: 'https://shift-handover-intelligence-production.up.railway.app/api',
    healthUrl: 'https://shift-handover-intelligence-production.up.railway.app/health'
};
```

### 6.3 Google Gemini AI Integration - Complete Guide

This section provides a comprehensive explanation of how the Google Gemini 3 API is integrated into the Shift Handover Intelligence application, including API key management, authentication, usage patterns, and best practices.

#### 6.3.1 Overview of Gemini AI in This Project

The application uses **Google Gemini 3 Flash Preview** (`gemini-3-flash-preview`) model for:
- Natural language understanding of unstructured shift notes
- Intelligent categorization of events (safety, equipment, process)
- Generation of structured JSON output
- Creation of human-readable markdown reports
- Context-aware analysis combining notes, alarms, and trends

#### 6.3.2 Obtaining a Gemini API Key

**Step 1: Access Google AI Studio**
1. Navigate to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Accept the Terms of Service if prompted

**Step 2: Generate API Key**
1. Click on **"Get API Key"** in the left sidebar
2. Click **"Create API Key"**
3. Choose an existing Google Cloud project or create a new one
4. Copy the generated API key (it will look like: `AIzaSy...`)

**Step 3: API Key Security Best Practices**
```
✅ DO:
- Store API key in environment variables
- Use .env files for local development
- Set API key in Railway dashboard for production
- Add .env to .gitignore

❌ DON'T:
- Hardcode API key in source code
- Commit API key to version control
- Share API key publicly
- Use same key for development and production
```

#### 6.3.3 API Key Configuration

**Local Development Setup:**

1. Create `.env` file in project root:
```bash
# .env (never commit this file!)
GEMINI_API_KEY=AIzaSy_your_actual_api_key_here
```

2. Add to `.gitignore`:
```
# Environment files
.env
.env.local
.env.production
```

**Production Setup (Railway):**

1. Go to Railway Dashboard → Your Project → Variables
2. Add new variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your actual API key
3. Railway automatically injects this into the container environment

#### 6.3.4 Code Implementation Deep Dive

**File: `backend/gemini_client.py`**

```python
from google import genai
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (handles relative paths correctly)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class GeminiClient:
    """Client for interacting with Google Gemini API"""

    def __init__(self):
        """Initialize Gemini client with API key from environment"""
        
        # Step 1: Retrieve API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Step 2: Validate API key exists
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # Step 3: Set Google API key (required by google-genai library)
        os.environ['GOOGLE_API_KEY'] = api_key
        
        # Step 4: Initialize the Gemini client
        self.client = genai.Client(api_key=api_key)
        
        # Step 5: Configure model version
        self.model_name = 'gemini-3-flash-preview'
```

**Key Implementation Details:**

| Component | Purpose |
|-----------|---------|
| `load_dotenv()` | Loads environment variables from .env file |
| `os.getenv('GEMINI_API_KEY')` | Retrieves API key from environment |
| `genai.Client(api_key=...)` | Creates authenticated Gemini client |
| `os.environ['GOOGLE_API_KEY']` | Sets key for google-genai library internals |

#### 6.3.5 Making API Calls

**The Request Flow:**

```
User Input → FastAPI Endpoint → GeminiClient → Gemini API → Response Parsing
     │              │                │              │              │
     │              │                │              │              │
Shift Notes    Validates      Builds Prompt    AI Processing   Extract JSON
Alarms JSON    Request        Sends to API     Generates       & Markdown
Trends CSV                                     Response
```

**API Call Implementation:**

```python
def generate_handover(self, shift_notes, alarms_json=None, trends_csv=None):
    """
    Generate handover summary using Gemini API
    
    Args:
        shift_notes: Raw text from operator
        alarms_json: Optional alarm data as dict
        trends_csv: Optional trend data as CSV string
    
    Returns:
        Tuple[str, Dict]: (markdown_report, structured_json)
    """
    
    # Build comprehensive prompt with all context
    prompt = self._build_prompt(shift_notes, alarms_json, trends_csv)
    
    # Make API call to Gemini
    response = self.client.models.generate_content(
        model=self.model_name,      # 'gemini-3-flash-preview'
        contents=prompt              # Combined prompt with all data
    )
    
    # Extract text response
    response_text = response.text
    
    # Parse JSON from response
    json_data = extract_json_from_text(response_text)
    
    # Generate or extract markdown
    markdown = self._extract_or_generate_markdown(response_text, json_data)
    
    return markdown, json_data
```

#### 6.3.6 System Prompt Engineering

The quality of AI output depends heavily on the system prompt. Here's the complete prompt used:

```python
SYSTEM_PROMPT = """You are an industrial operations assistant specialized 
in AVEVA systems and manufacturing operations.

Your task is to convert shift handover notes, alarm data, and trend data 
into a structured, actionable handover summary.

CRITICAL REQUIREMENTS:
1. **Separate Facts from Hypotheses**: Clearly distinguish between 
   observed facts and inferred hypotheses.
2. **Provide Confidence**: For any hypothesis or inference, provide 
   a confidence percentage (0-100%).
3. **Be Specific and Operational**: Use precise industrial terminology. 
   Reference specific equipment, tags, or alarm IDs when available.
4. **Ask Clarifying Questions**: If critical information is missing, 
   ask up to 3 specific questions.
5. **Output Format**: Return BOTH:
   - A valid JSON object matching the exact schema below
   - A markdown-formatted report

JSON SCHEMA (STRICT):
{
  "shiftSummary": ["fact 1", "fact 2", ...],
  "criticalAlarms": [{"alarm": "...", "meaning": "..."}],
  "openIssues": [{"issue": "...", "priority": "High|Med|Low", "confidence": 75}],
  "recommendedActions": ["action 1", "action 2", ...],
  "questions": ["question 1", "question 2", ...]
}

PRIORITY LEVELS:
- High: Immediate action required, safety/production impact
- Med: Should be addressed within 24 hours
- Low: Monitor or address when convenient
"""
```

**Why This Prompt Works:**

| Technique | Purpose |
|-----------|---------|
| Role Definition | "industrial operations assistant" sets context |
| Clear Requirements | Numbered list prevents ambiguity |
| Strict Schema | JSON schema ensures parseable output |
| Priority Guidelines | Standardizes categorization |
| Dual Output | Both human and machine-readable formats |

#### 6.3.7 Error Handling & Resilience

**Robust Error Handling:**

```python
def generate_handover(self, shift_notes, alarms_json=None, trends_csv=None):
    try:
        # Normal API call
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        # ... process response
        
    except Exception as e:
        # Log error for debugging
        logger.error(f"Gemini API error: {e}", exc_info=True)
        
        # Return graceful fallback response
        fallback_json = {
            'shiftSummary': [f"Error: {str(e)}", "Review notes manually"],
            'criticalAlarms': [],
            'openIssues': [{
                "issue": "Gemini API Error",
                "priority": "High",
                "confidence": 100
            }],
            'recommendedActions': ["Check API key", "Retry request"],
            'questions': []
        }
        
        return create_markdown_from_structured(fallback_json), fallback_json
```

**JSON Self-Repair Feature:**

When Gemini returns malformed JSON, the client attempts self-repair:

```python
def _repair_json_with_gemini(self, invalid_response):
    """Use Gemini to repair its own malformed JSON output"""
    
    repair_prompt = f"""The following response contains malformed JSON:

{invalid_response}

Please extract and return ONLY a valid JSON object.
Return ONLY the JSON, nothing else."""

    response = self.client.models.generate_content(
        model=self.model_name,
        contents=repair_prompt
    )
    
    return extract_json_from_text(response.text)
```

#### 6.3.8 API Usage & Rate Limits

**Gemini API Pricing (as of 2026):**

| Model | Input | Output | RPM Limit |
|-------|-------|--------|-----------|
| gemini-3-flash-preview | $0.075/1M tokens | $0.30/1M tokens | 60 |
| gemini-3-pro | $1.25/1M tokens | $5.00/1M tokens | 60 |

**Token Estimation:**
- Average shift notes: ~500 tokens
- Average alarm JSON: ~200 tokens
- Average trends CSV: ~300 tokens
- Average response: ~1,500 tokens
- **Cost per handover**: ~$0.0005 (less than 1 cent)

**Rate Limiting Considerations:**

```python
# For high-volume deployments, add rate limiting:
import time
from functools import wraps

def rate_limit(max_per_minute=50):
    """Decorator to rate limit API calls"""
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

#### 6.3.9 Testing the Gemini Integration

**Manual Testing:**

```bash
# 1. Set environment variable
export GEMINI_API_KEY="your_api_key"

# 2. Start backend
cd backend
python -m uvicorn main:app --reload

# 3. Test with curl
curl -X POST http://localhost:8000/api/handover/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shift_notes": "Started batch 2024-001 at 0600. Reactor temp hit 85C.",
    "alarms_json": [{"time": "07:30", "tag": "TI-101", "desc": "High temp"}],
    "trends_csv": "time,tag,value\n06:00,TI-101,75\n07:00,TI-101,85"
  }'
```

**Unit Testing:**

```python
# tests/test_gemini_client.py
import pytest
from unittest.mock import Mock, patch

def test_gemini_client_initialization():
    """Test client initializes with valid API key"""
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        client = GeminiClient()
        assert client.model_name == 'gemini-3-flash-preview'

def test_gemini_client_missing_key():
    """Test client raises error without API key"""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            GeminiClient()
        assert "GEMINI_API_KEY" in str(exc_info.value)
```

#### 6.3.10 Security Considerations

**API Key Protection Checklist:**

- [x] API key stored in environment variables only
- [x] `.env` file added to `.gitignore`
- [x] Production key set in Railway dashboard (not in code)
- [x] Different keys for development vs production (recommended)
- [x] API key validated on startup (fails fast if missing)

**Environment Variable Loading Order:**

```
1. Railway Dashboard (production) → Injected at container start
2. .env file (local development) → Loaded by python-dotenv
3. System environment → Fallback
```

**Verifying API Key is Set:**

```python
# In main.py startup
@app.on_event("startup")
async def verify_gemini_key():
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY not set - AI features will fail!")
    else:
        logger.info("Gemini API key configured successfully")
```

#### 6.3.11 Troubleshooting Gemini API Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ValueError: GEMINI_API_KEY not set` | Missing API key | Add key to `.env` or Railway variables |
| `401 Unauthorized` | Invalid API key | Regenerate key in Google AI Studio |
| `429 Too Many Requests` | Rate limit exceeded | Implement rate limiting, upgrade plan |
| `500 Internal Server Error` | Gemini service issue | Retry with exponential backoff |
| Malformed JSON response | Prompt issue | Check prompt, use JSON repair feature |

**Debug Logging:**

```python
# Enable detailed logging
import logging
logging.getLogger('google.genai').setLevel(logging.DEBUG)

# In gemini_client.py
logger.debug(f"Prompt length: {len(prompt)} chars")
logger.debug(f"Response length: {len(response.text)} chars")
```

---

## 7. API Documentation

### Base URL
```
Production: https://shift-handover-intelligence-production.up.railway.app
Local: http://localhost:8000
```

### Endpoints

#### GET /
Returns API information and available endpoints.

**Response:**
```json
{
    "message": "Welcome to Shift Handover Intelligence API",
    "service": "shift-handover-intelligence",
    "version": "1.0.0",
    "status": "running",
    "endpoints": {
        "health": "/health",
        "generate_handover": "/api/handover/generate",
        "get_handover": "/api/handover/{session_id}",
        "download_pdf": "/api/handover/download-pdf"
    },
    "docs": "/docs",
    "redoc": "/redoc"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2026-01-12T10:30:00.000Z",
    "service": "shift-handover-intelligence",
    "checks": {
        "database": "ok",
        "gemini_api": "initialized"
    }
}
```

#### POST /api/handover/generate
Generate a structured handover report.

**Request Body:**
```json
{
    "shiftNotes": "string (required)",
    "alarmsJson": "string (optional)",
    "trendsCsv": "string (optional)"
}
```

**Response:**
```json
{
    "markdown": "# Shift Handover Report\n...",
    "json": {
        "executiveSummary": "...",
        "keyEvents": [...],
        "equipmentStatus": [...],
        "safetyObservations": [...],
        "pendingActions": [...],
        "recommendations": [...]
    },
    "sessionId": "uuid-string"
}
```

#### GET /api/handover/{session_id}
Retrieve a previously generated handover.

#### POST /api/handover/download-pdf
Generate and download PDF report.

**Response:** PDF file (application/pdf)

---

## 8. Testing Guide

### 8.1 Sample Test Data

#### Sample Shift Notes (Pharmaceutical)
```
Morning shift 0600-1400. Started batch B-2026-001 for Product X.
Reactor R-101 charged with 500L solvent at 0630. Heating initiated at 0700.
Temperature reached setpoint 75°C at 0745. API addition started at 0800.
Completed API addition at 0900. Stirring continued at 150 RPM.

Issues:
- Agitator seal on R-101 showing minor leak, maintenance notified
- Cooling water pressure low at 0830, normalized after 10 minutes

QC samples taken at 0930 and 1100. Results pending.
Batch completion expected by 1400.

For next shift:
- Monitor agitator seal
- Complete batch filtration
- Send final QC samples
```

#### Sample Alarms JSON
```json
[
    {
        "time": "08:30",
        "tag": "PT-101",
        "description": "Low cooling water pressure",
        "priority": "Medium",
        "acknowledged": true
    },
    {
        "time": "10:15",
        "tag": "LSH-102",
        "description": "High level alarm tank T-102",
        "priority": "High",
        "acknowledged": true
    }
]
```

#### Sample Trends CSV
```csv
time,tag,value,unit
06:00,TI-101,25.5,°C
06:30,TI-101,45.2,°C
07:00,TI-101,65.8,°C
07:30,TI-101,74.5,°C
08:00,TI-101,75.1,°C
08:30,TI-101,75.0,°C
09:00,TI-101,75.2,°C
```

### 8.2 Testing Steps

#### Local Testing

1. **Start Backend**
   ```bash
   cd backend
   source venv_shift/bin/activate
   export GEMINI_API_KEY="your_key"
   python main.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Test via UI**
   - Open http://localhost:4200
   - Paste sample notes
   - Click "Generate Handover"
   - Verify output formatting
   - Test PDF download

4. **Test via API**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Generate handover
   curl -X POST http://localhost:8000/api/handover/generate \
     -H "Content-Type: application/json" \
     -d '{"shiftNotes": "Test shift notes here"}'
   ```

#### Production Testing

```bash
# Test health
curl https://shift-handover-intelligence-production.up.railway.app/health

# Test CORS
curl -X OPTIONS \
  -H "Origin: https://shrinikatelu.github.io" \
  -H "Access-Control-Request-Method: POST" \
  https://shift-handover-intelligence-production.up.railway.app/api/handover/generate \
  -v
```

### 8.3 Expected Results

| Test Case | Expected Result |
|-----------|-----------------|
| Empty shift notes | Error: "Shift notes required" |
| Valid shift notes | Structured markdown + JSON response |
| With alarms JSON | Alarms integrated into report |
| With trends CSV | Trends analyzed in report |
| PDF download | Valid PDF file downloads |
| Invalid session ID | 404 Not Found |
| CORS from GitHub Pages | 200 OK with proper headers |

---

## 9. Deployment Guide

### 9.1 Backend Deployment (Railway)

#### Prerequisites
- Railway account (https://railway.app)
- GitHub repository connected
- Gemini API key

#### Steps

1. **Create Railway Project**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `shift-handover-intelligence` repository

2. **Configure Build Settings**
   - Railway auto-detects Dockerfile
   - Build context: `/` (root)
   - Dockerfile path: `Dockerfile`

3. **Set Environment Variables**
   ```
   GEMINI_API_KEY=your_actual_api_key
   ALLOWED_ORIGINS=https://shrinikatelu.github.io
   DEBUG=false
   ```

4. **Configure Networking**
   - Generate domain
   - Port: 8000

5. **Deploy**
   - Railway auto-deploys on push
   - Monitor logs for errors

#### Dockerfile (Backend)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend/ .

RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 Frontend Deployment (GitHub Pages)

#### Prerequisites
- GitHub repository
- Node.js and npm installed
- Backend URL ready

#### Deployment Script (deploy.sh)
```bash
#!/bin/bash
set -e

REPO_OWNER="ShrinikaTelu"
REPO_NAME="shift-handover-intelligence"
FRONTEND_DIR="frontend"

# Get Railway URL
read -p "Enter Railway Backend URL: " RAILWAY_URL

# Write environment file
cat > "$FRONTEND_DIR/src/environments/environment.ts" <<EOF
export const environment = {
  production: true,
  apiUrl: '${RAILWAY_URL}/api',
  healthUrl: '${RAILWAY_URL}/health'
};
EOF

# Build and deploy
cd "$FRONTEND_DIR"
npm ci || npm install
npx ng build --configuration production --base-href "/$REPO_NAME/"
npx angular-cli-ghpages --dir=dist/frontend/browser --repo=https://github.com/$REPO_OWNER/$REPO_NAME.git
```

#### Running Deployment
```bash
chmod +x deploy.sh
./deploy.sh
# Enter: https://shift-handover-intelligence-production.up.railway.app
```

### 9.3 GitHub Pages Settings

1. Go to repository Settings
2. Navigate to Pages section
3. Source: "Deploy from a branch"
4. Branch: `gh-pages`
5. Save

---

## 10. Troubleshooting

### Common Issues

#### Issue: CORS Error ("0 Unknown Error")
**Symptoms:** Frontend can't communicate with backend

**Solution:**
1. Check backend CORS configuration includes GitHub Pages domain
2. Verify `ALLOWED_ORIGINS` in Railway environment variables
3. Test CORS with curl:
   ```bash
   curl -X OPTIONS -H "Origin: https://shrinikatelu.github.io" \
     https://your-backend-url/api/handover/generate -v
   ```

#### Issue: Backend 502 Error
**Symptoms:** Railway returns "Application failed to respond"

**Solutions:**
1. Check Railway logs for crash details
2. Verify `GEMINI_API_KEY` is set
3. Ensure Dockerfile CMD is correct
4. Check if port 8000 is exposed

#### Issue: Frontend 404 on GitHub Pages
**Symptoms:** Page not found after deployment

**Solutions:**
1. Verify build uses `--base-href "/shift-handover-intelligence/"`
2. Check deployment uses `dist/frontend/browser` (Angular 18)
3. Confirm `gh-pages` branch exists
4. Wait 2-3 minutes for GitHub Pages to update

#### Issue: PDF Download Fails
**Symptoms:** PDF generation returns error

**Solutions:**
1. Check `reportlab` is in requirements.txt
2. Verify backend has enough memory
3. Check logs for specific error message

#### Issue: Gemini API Not Initialized
**Symptoms:** Health check shows `gemini_api: not_initialized`

**Solutions:**
1. Verify `GEMINI_API_KEY` environment variable
2. Check API key is valid at https://ai.google.dev
3. Restart Railway deployment

### Debug Commands

```bash
# Check backend health
curl https://shift-handover-intelligence-production.up.railway.app/health

# Test API directly
curl -X POST https://shift-handover-intelligence-production.up.railway.app/api/handover/generate \
  -H "Content-Type: application/json" \
  -d '{"shiftNotes": "Test notes"}'

# Check CORS headers
curl -I -X OPTIONS \
  -H "Origin: https://shrinikatelu.github.io" \
  -H "Access-Control-Request-Method: POST" \
  https://shift-handover-intelligence-production.up.railway.app/api/handover/generate
```

---

## 11. Demo Examples

### Example 1: Basic Shift Notes

**Input:**
```
Day shift 06:00-14:00. All systems normal at shift start.
Pump P-101 started at 07:00 for tank transfer.
Received delivery of raw materials at 09:30.
Completed inventory count at 11:00.
Minor spill in warehouse, cleaned up by 12:00.
Handover to evening shift at 14:00.
```

**Output Summary:**
- Executive summary of routine operations
- Key events: pump start, delivery, inventory
- Safety observation: spill incident with resolution
- No pending actions

### Example 2: Complex Industrial Scenario

**Input:**
```
Night shift 22:00-06:00 at Refinery Unit 3.

00:30 - CDU feed rate reduced from 50,000 BPD to 45,000 BPD due to 
        high column pressure on T-301
01:15 - Alarm: High pressure on T-301 (15.2 barg vs setpoint 14.5)
01:30 - Opened bypass on PC-301, pressure normalized
02:00 - Compressor K-201 showing high vibration (8.2 mm/s)
02:30 - Called maintenance, scheduled inspection for day shift
03:45 - Lab results: off-spec naphtha sulfur content (120 ppm vs spec 50 ppm)
04:00 - Increased caustic injection rate on treating unit
05:00 - Resampled naphtha, results pending
05:30 - Shift relief walkthrough completed

Equipment out of service:
- Pump P-203 (seal replacement in progress)
- Heat exchanger E-105 (tube leak)

For day shift:
1. Monitor K-201 vibration
2. Await lab results for naphtha
3. Coordinate P-203 return to service with maintenance
```

**With Alarms JSON:**
```json
[
  {"time": "01:15", "tag": "PAH-301", "description": "High pressure column T-301", "priority": "High"},
  {"time": "02:00", "tag": "VAH-201", "description": "High vibration compressor K-201", "priority": "High"},
  {"time": "03:45", "tag": "QA-NAPHTHA", "description": "Off-spec product alert", "priority": "Medium"}
]
```

**Expected Output Sections:**
1. **Executive Summary**: Overview of reduced throughput, equipment issues, quality deviation
2. **Key Events**: Chronological list with categories (Process, Equipment, Quality)
3. **Equipment Status**: Table of out-of-service items
4. **Safety Observations**: Pressure relief actions, proper procedures followed
5. **Pending Actions**: 3 items for next shift
6. **Recommendations**: Prioritized action items

### Example 3: Pharmaceutical Batch Production

**Input:**
```
Production Batch: PROD-2026-0112
Product: Aspirin 500mg Tablets
Shift: Day (06:00-14:00)
Operator: John Smith

06:00 - Shift handover received, reviewed batch record
06:30 - Verified raw materials (API, excipients) per BOM
07:00 - Started granulation in FL-01
08:30 - Granulation complete, yield 98.5%
09:00 - Transferred to V-blender VB-01
09:30 - Blending complete (15 min at 12 RPM)
10:00 - Compression started on press CP-01
12:00 - IPC results: weight 505mg (spec: 500-510mg), hardness 8.5 kP (spec: 6-10 kP)
13:00 - Compression complete, bulk tablets to staging
13:30 - Area cleaning initiated
14:00 - Handover to evening shift

Deviations: None
Out of spec: None
Equipment issues: None

Next shift: Complete coating operation
```

**Expected Output:**
- Clean batch summary with all quality parameters
- Compliance-ready documentation format
- Clear handover point for coating operation

---

## 12. Future Enhancements

### Planned Features

1. **User Authentication**
   - Login/logout functionality
   - Role-based access (operator, supervisor, manager)
   - Audit trail of all handovers

2. **Dashboard & Analytics**
   - Shift history visualization
   - Trend analysis across shifts
   - Equipment reliability metrics

3. **Integration Options**
   - Connect to real alarm systems (OPC-UA)
   - Pull trends from historians (OSIsoft PI, Honeywell PHD)
   - Export to CMMS systems

4. **Advanced AI Features**
   - Predictive maintenance suggestions
   - Anomaly detection in shift patterns
   - Natural language queries on historical data

5. **Mobile App**
   - iOS/Android native app
   - Offline capability
   - Push notifications for handover reminders

6. **Multi-Language Support**
   - Internationalization (i18n)
   - Support for non-English shift notes

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Summary

Shift Handover Intelligence transforms the way industrial facilities manage shift transitions. By leveraging AI, it:

- **Saves Time**: Automated report generation
- **Improves Quality**: Consistent, structured output
- **Reduces Risk**: Nothing gets lost in translation
- **Enables Compliance**: Audit-ready documentation

**Live Demo**: https://shrinikatelu.github.io/shift-handover-intelligence/

---

*Document Version: 1.0.0*
*Last Updated: January 12, 2026*
*Author: Shrinika Telu*
