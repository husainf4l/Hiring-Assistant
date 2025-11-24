"""
SQLAlchemy models for the Job Finder assistant.
Phase 4: Data Model
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class JobSeekerProfileORM(Base):
    """Persistent job seeker profile."""

    __tablename__ = "job_finder_profiles"

    id = Column(String, primary_key=True, index=True)
    current_role = Column(String(255), nullable=True)
    skills = Column(JSON, default=list)
    years_experience = Column(Integer, nullable=True)
    preferred_titles = Column(JSON, default=list)
    preferred_locations = Column(JSON, default=list)
    salary_expectation = Column(String(255), nullable=True)
    work_type = Column(String(50), nullable=True)
    industries = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String(64), nullable=True)

    recommendations = relationship(
        "JobRecommendationORM",
        back_populates="seeker",
        cascade="all, delete-orphan",
    )


class JobListingORM(Base):
    """Job listings imported from internal database."""

    __tablename__ = "job_finder_listings"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    required_skills = Column(JSON, default=list)
    optional_skills = Column(JSON, default=list)
    experience_level = Column(String(50), nullable=True)
    salary_range = Column(String(100), nullable=True)
    work_type = Column(String(50), nullable=True)
    industries = Column(JSON, default=list)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    recommendations = relationship("JobRecommendationORM", back_populates="job")


class JobRecommendationORM(Base):
    """Saved recommendation entries."""

    __tablename__ = "job_finder_recommendations"

    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("job_finder_listings.id"), nullable=False)
    seeker_id = Column(String, ForeignKey("job_finder_profiles.id"), nullable=False)
    match_score = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobListingORM", back_populates="recommendations")
    seeker = relationship("JobSeekerProfileORM", back_populates="recommendations")

