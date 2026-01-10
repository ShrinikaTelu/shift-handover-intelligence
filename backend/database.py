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
    alarms_json = Column(Text, nullable=True)  # JSON stored as text
    trends_csv = Column(Text, nullable=True)
    markdown_output = Column(Text, nullable=False)
    json_output = Column(Text, nullable=False)  # JSON stored as text
    created_at = Column(DateTime, default=datetime.utcnow)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting database sessions"""
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
    """Save a handover session to the database"""

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
    """Retrieve a handover session by session_id"""
    from sqlalchemy import select

    result = await session.execute(
        select(HandoverSessionDB).where(HandoverSessionDB.session_id == session_id)
    )
    return result.scalar_one_or_none()
