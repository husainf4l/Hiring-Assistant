"""
FastAPI routes for the Job Finder assistant.
Phase 5: Backend Structure
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from ..database import get_db
from ..repositories import (
    JobPostRepository,
    JobPostRepository as SavedJobRepository,  # alias for clarity
)
from .orchestrator import JobFinderOrchestrator
from .models import JobSeekerProfile

router = APIRouter(prefix="/job-finder", tags=["Job Finder"])
orchestrator = JobFinderOrchestrator()


@router.post("/start-chat")
async def start_chat():
    """Initialize a new job seeker session."""
    session = orchestrator.start_session()
    return {
        "session_id": session.session_id,
        "message": "Hi! I’m your Job Finder Agent. Let’s build your profile. What role are you targeting next?",
    }


@router.post("/send-message")
async def send_message(payload: Dict[str, str]):
    session_id = payload.get("session_id")
    message = payload.get("message")
    if not session_id or not message:
        raise HTTPException(status_code=400, detail="session_id and message required")

    session = orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = orchestrator.process_user_message(session_id, message)
    return result


@router.get("/recommendations/{session_id}")
async def get_recommendations(session_id: str):
    session = orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return [rec.model_dump() for rec in session.recommendations]


@router.post("/save-job")
async def save_job(payload: Dict[str, str], db: Session = Depends(get_db)):
    session_id = payload.get("session_id")
    job_id = payload.get("job_id")
    if not session_id or not job_id:
        raise HTTPException(status_code=400, detail="session_id and job_id required")

    # Placeholder: reuse existing JobPostRepository structure
    job = JobPostRepository.get_by_id(db, int(job_id))  # adapt as needed
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"message": "Job saved successfully"}


@router.get("/saved-jobs")
async def saved_jobs(user_id: int, db: Session = Depends(get_db)):
    posts = SavedJobRepository.get_by_user(db, user_id)
    return {"posts": posts}


@router.post("/refine-search")
async def refine_search(payload: Dict[str, str]):
    """Adjust filters on the fly (placeholder)."""
    # This would update seeker profile preferences
    return {"message": "Filters updated"}

