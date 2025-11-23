"""
Data Models for HR Hiring Assistant
Phase 4: Data Model Implementation
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    """User model for HR/Recruiters"""
    id: Optional[int] = None
    email: EmailStr
    name: str
    company: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None


class JobPost(BaseModel):
    """Job Post model - LinkedIn-style hiring post"""
    id: Optional[int] = None
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    workplace_type: Optional[str] = None  # On-site, Remote, Hybrid
    job_type: Optional[str] = None  # Full-time, Part-time, Contract
    summary: Optional[str] = None
    culture_and_team: Optional[str] = None  # Company culture and team information
    responsibilities: List[str] = []
    requirements: List[str] = []
    skills: List[str] = []
    keywords: List[str] = []
    hashtags: List[str] = []
    tone_type: Optional[str] = None  # e.g., "professional", "casual", "tech"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None


class ChatMessage(BaseModel):
    """Chat message model for conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatSession(BaseModel):
    """Chat session model"""
    session_id: str
    messages: List[ChatMessage] = []
    job_post: Optional[JobPost] = None
    is_complete: bool = False
    created_at: Optional[datetime] = None


class StartChatRequest(BaseModel):
    """Request to start a new chat session"""
    user_id: Optional[int] = None


class SendMessageRequest(BaseModel):
    """Request to send a message in chat"""
    session_id: str
    message: str


class PostPreviewResponse(BaseModel):
    """Response with post preview"""
    session_id: str
    job_post: JobPost
    is_complete: bool


class SavePostRequest(BaseModel):
    """Request to save a post"""
    session_id: str
    user_id: int


class RegenerateSectionRequest(BaseModel):
    """Request to regenerate a section"""
    session_id: str
    section_type: str  # "summary", "responsibilities", "requirements", "skills", "hashtags", "keywords"

