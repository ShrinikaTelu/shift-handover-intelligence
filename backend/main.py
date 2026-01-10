from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
import uuid
from datetime import datetime
import logging
import os

from schemas import HandoverRequest, HandoverResponse, ErrorResponse, HandoverStructured
from gemini_client import GeminiClient
from database import init_db, get_session, save_handover_session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Shift Handover Intelligence API",
    description="AI-powered shift handover generation using Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client (will be created on first request)
gemini_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """Dependency for getting Gemini client"""
    global gemini_client
    if gemini_client is None:
        try:
            gemini_client = GeminiClient()
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini client initialization failed: {str(e)}. Please set GEMINI_API_KEY environment variable."
            )
    return gemini_client


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for consistent error responses"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc),
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_session)):
    """Health check endpoint with dependency checks"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "shift-handover-intelligence",
        "checks": {}
    }

    # Check database connectivity
    try:
        await db.execute("SELECT 1")
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["checks"]["database"] = "error"
        health_status["status"] = "unhealthy"

    # Check Gemini client initialization
    try:
        if gemini_client is not None:
            health_status["checks"]["gemini_api"] = "initialized"
        else:
            health_status["checks"]["gemini_api"] = "not_initialized"
    except Exception as e:
        logger.error(f"Gemini API health check failed: {e}")
        health_status["checks"]["gemini_api"] = "error"
        health_status["status"] = "degraded"

    return health_status


@app.post("/api/handover/generate", response_model=HandoverResponse)
async def generate_handover(
    request: HandoverRequest,
    db: AsyncSession = Depends(get_session),
    client: GeminiClient = Depends(get_gemini_client)
):
    """
    Generate a structured shift handover summary using Gemini AI.

    Takes shift notes, optional alarms JSON, and optional trends CSV.
    Returns both markdown and structured JSON output.
    """

    try:
        # Generate handover using Gemini
        markdown, json_data = client.generate_handover(
            shift_notes=request.shiftNotes,
            alarms_json=request.alarmsJson,
            trends_csv=request.trendsCsv
        )

        # Validate the structured data using Pydantic
        structured_handover = HandoverStructured(**json_data)

        # Generate unique session ID
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
            logger.info(f"Handover session saved: {session_id}")
        except Exception as db_error:
            logger.warning(f"Database save failed (non-critical): {db_error}")
            # Continue even if DB save fails

        return HandoverResponse(
            markdown=markdown,
            json=structured_handover,
            sessionId=session_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate handover: {str(e)}"
        )


@app.get("/api/handover/{session_id}", response_model=HandoverResponse)
async def get_handover(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """Retrieve a previously generated handover by session ID"""

    from database import get_handover_session
    import json

    session = await get_handover_session(db, session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Handover session {session_id} not found"
        )

    json_output = json.loads(session.json_output)

    return HandoverResponse(
        markdown=session.markdown_output,
        json=HandoverStructured(**json_output),
        sessionId=session.session_id
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
