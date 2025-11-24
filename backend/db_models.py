"""
SQLAlchemy Database Models
Phase 4: Data Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
try:
    from .database import Base
except ImportError:
    from database import Base


class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Should be hashed in production
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_posts = relationship("JobPost", back_populates="user")


class JobPost(Base):
    """Job Post database model"""
    __tablename__ = "job_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    workplace_type = Column(String(100), nullable=True)
    job_type = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    responsibilities = Column(JSON, default=list)  # List of strings
    requirements = Column(JSON, default=list)  # List of strings
    skills = Column(JSON, default=list)  # List of strings
    keywords = Column(JSON, default=list)  # List of strings
    hashtags = Column(JSON, default=list)  # List of strings
    culture_and_team = Column(Text, nullable=True)
    tone_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="job_posts")


class ChatSession(Base):
    """Chat Session database model"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    messages = Column(JSON, default=list)  # List of message dicts
    job_info = Column(JSON, default=dict)  # Extracted job information
    is_complete = Column(Integer, default=0)  # 0 = False, 1 = True (SQLite compatibility)
    job_post_id = Column(Integer, ForeignKey("job_posts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_post = relationship("JobPost", foreign_keys=[job_post_id])


