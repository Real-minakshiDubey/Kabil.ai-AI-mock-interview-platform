
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    Numeric,
    JSON,
    ARRAY,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=True)
    email = Column(Text, unique=True, nullable=True)
    password_hash = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    role = Column(Text, nullable=False)          # e.g. "ml_engineer"
    difficulty = Column(Text, nullable=True)     # "easy", "medium", "hard"
    started_at = Column(TIMESTAMP, default=datetime.utcnow)
    ended_at = Column(TIMESTAMP, nullable=True)
    overall_score = Column(Numeric, nullable=True)
    meta = Column(JSON, nullable=True)

    qa_items = relationship(
        "InterviewQA",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    report = relationship(
        "InterviewReport",
        back_populates="session",
        uselist=False,
    )


class InterviewQA(Base):
    __tablename__ = "interview_qa"

    qa_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.session_id"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_transcript = Column(Text, nullable=True)
    partial_score = Column(JSON, nullable=True)          # {"communication":..,"technical":..,"confidence":..}
    expected_keywords = Column(ARRAY(Text), nullable=True)
    is_followup = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="qa_items")


class InterviewReport(Base):
    __tablename__ = "interview_reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.session_id"), nullable=False)
    avg_scores = Column(JSON, nullable=True)             # {"communication":..,"technical":..,"confidence":..}
    improvement_plan = Column(JSON, nullable=True)       # action items
    recommended_resources = Column(JSON, nullable=True)  # list of {title,url,reason}
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="report")
