from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum
import bleach


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
    confidence: float = Field(ge=0, le=100, description="Confidence percentage 0-100")


class HandoverStructured(BaseModel):
    """Structured handover data returned by Gemini"""
    shiftSummary: List[str]
    criticalAlarms: List[CriticalAlarm]
    openIssues: List[OpenIssue]
    recommendedActions: List[str]
    questions: List[str]


class HandoverRequest(BaseModel):
    """Request payload for handover generation"""
    shiftNotes: str = Field(min_length=10, max_length=50000, description="Shift handover notes from operator")
    alarmsJson: Optional[Dict[str, Any]] = None
    trendsCsv: Optional[str] = Field(default=None, max_length=1000000)

    @field_validator('shiftNotes')
    @classmethod
    def validate_shift_notes(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Shift notes cannot be empty')
        # Sanitize input to prevent XSS
        cleaned = bleach.clean(v.strip(), tags=[], strip=True)
        return cleaned

    @field_validator('alarmsJson')
    @classmethod
    def validate_alarms_size(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if v and len(str(v)) > 1_000_000:  # 1MB limit
            raise ValueError('Alarms JSON exceeds maximum size (1MB)')
        return v


class HandoverResponse(BaseModel):
    """Response containing both markdown and structured JSON"""
    markdown: str
    json: HandoverStructured
    sessionId: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: str
