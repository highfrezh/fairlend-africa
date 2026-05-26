"""
Database connection and session management.
SQLAlchemy is used for ORM — keeping it simple and compatible
with both PostgreSQL (production) and SQLite (local fallback).
"""

from sqlalchemy import (
    create_engine, Column, Integer, Float,
    String, DateTime, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from api.config import settings


engine       = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()


class PredictionLog(Base):
    """
    Logs every prediction request for audit and research purposes.
    In a real system this enables model monitoring and drift detection.
    """
    __tablename__ = "prediction_logs"

    id                    = Column(Integer, primary_key=True, index=True)
    borrower_id           = Column(String, nullable=True)
    repayment_probability = Column(Float)
    credit_score          = Column(Integer)
    recommendation        = Column(String)
    risk_tier             = Column(String)
    input_data            = Column(Text)   # JSON string
    shap_values           = Column(Text)   # JSON string
    created_at            = Column(DateTime,
                                   default=lambda: datetime.now(timezone.utc))


def get_db():
    """Dependency injected into route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Called once at startup."""
    Base.metadata.create_all(bind=engine)