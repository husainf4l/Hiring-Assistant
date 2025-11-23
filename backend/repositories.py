"""
Repository layer for database operations
Phase 4: Data Model
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
try:
    from .db_models import User, JobPost, ChatSession
    from .models import JobPost as JobPostPydantic, User as UserPydantic, ChatMessage
except ImportError:
    from db_models import User, JobPost, ChatSession
    from models import JobPost as JobPostPydantic, User as UserPydantic, ChatMessage


class UserRepository:
    """Repository for User operations"""
    
    @staticmethod
    def create(db: Session, user_data: dict) -> User:
        """Create a new user"""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()


class JobPostRepository:
    """Repository for JobPost operations"""
    
    @staticmethod
    def create(db: Session, job_post_data: dict) -> JobPost:
        """Create a new job post"""
        job_post = JobPost(**job_post_data)
        job_post.updated_at = datetime.utcnow()
        db.add(job_post)
        db.commit()
        db.refresh(job_post)
        return job_post
    
    @staticmethod
    def get_by_id(db: Session, post_id: int) -> Optional[JobPost]:
        """Get job post by ID"""
        return db.query(JobPost).filter(JobPost.id == post_id).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[JobPost]:
        """Get all job posts for a user"""
        return db.query(JobPost).filter(JobPost.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, post_id: int, job_post_data: dict) -> Optional[JobPost]:
        """Update a job post"""
        job_post = db.query(JobPost).filter(JobPost.id == post_id).first()
        if job_post:
            for key, value in job_post_data.items():
                setattr(job_post, key, value)
            job_post.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(job_post)
        return job_post
    
    @staticmethod
    def delete(db: Session, post_id: int) -> bool:
        """Delete a job post"""
        job_post = db.query(JobPost).filter(JobPost.id == post_id).first()
        if job_post:
            db.delete(job_post)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[JobPost]:
        """Get all job posts with pagination"""
        return db.query(JobPost).offset(skip).limit(limit).all()


class ChatSessionRepository:
    """Repository for ChatSession operations"""
    
    @staticmethod
    def create(db: Session, session_data: dict) -> ChatSession:
        """Create a new chat session"""
        chat_session = ChatSession(**session_data)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        return chat_session
    
    @staticmethod
    def get_by_session_id(db: Session, session_id: str) -> Optional[ChatSession]:
        """Get chat session by session_id"""
        return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    
    @staticmethod
    def update(db: Session, session_id: str, session_data: dict) -> Optional[ChatSession]:
        """Update a chat session"""
        chat_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if chat_session:
            for key, value in session_data.items():
                setattr(chat_session, key, value)
            chat_session.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(chat_session)
        return chat_session
    
    @staticmethod
    def add_message(db: Session, session_id: str, message: dict) -> Optional[ChatSession]:
        """Add a message to the chat session"""
        chat_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if chat_session:
            if chat_session.messages is None:
                chat_session.messages = []
            chat_session.messages.append(message)
            chat_session.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(chat_session)
        return chat_session
    
    @staticmethod
    def get_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        """Get all chat sessions for a user"""
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete(db: Session, session_id: str) -> bool:
        """Delete a chat session"""
        chat_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if chat_session:
            db.delete(chat_session)
            db.commit()
            return True
        return False


def db_to_pydantic_job_post(db_job_post: JobPost) -> JobPostPydantic:
    """Convert SQLAlchemy JobPost to Pydantic JobPost"""
    return JobPostPydantic(
        id=db_job_post.id,
        title=db_job_post.title,
        company=db_job_post.company,
        location=db_job_post.location,
        workplace_type=db_job_post.workplace_type,
        job_type=db_job_post.job_type,
        summary=db_job_post.summary,
        culture_and_team=db_job_post.culture_and_team,
        responsibilities=db_job_post.responsibilities or [],
        requirements=db_job_post.requirements or [],
        skills=db_job_post.skills or [],
        keywords=db_job_post.keywords or [],
        hashtags=db_job_post.hashtags or [],
        tone_type=db_job_post.tone_type,
        created_at=db_job_post.created_at,
        updated_at=db_job_post.updated_at,
        user_id=db_job_post.user_id
    )


def db_to_pydantic_user(db_user: User) -> UserPydantic:
    """Convert SQLAlchemy User to Pydantic User"""
    return UserPydantic(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        company=db_user.company,
        role=db_user.role,
        created_at=db_user.created_at
    )

