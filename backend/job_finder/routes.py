"""
FastAPI routes for the Job Finder assistant.
Phase 5: Backend Structure
"""

from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional

from database import get_db
from repositories import (
    JobPostRepository,
    JobPostRepository as SavedJobRepository,  # alias for clarity
)
from job_finder.orchestrator import JobFinderOrchestrator
from job_finder.models import JobSeekerProfile

router = APIRouter(prefix="/job-finder", tags=["Job Finder"])

# Global orchestrator instance - will be initialized with db on first request
orchestrator: Optional[JobFinderOrchestrator] = None


def get_orchestrator(db: Session) -> JobFinderOrchestrator:
    """Get or initialize orchestrator with database connection"""
    global orchestrator
    if orchestrator is None:
        orchestrator = JobFinderOrchestrator(db=db)
    else:
        # Update db connection for each request
        orchestrator.db = db
    return orchestrator


@router.post("/start-chat")
async def start_chat(db: Session = Depends(get_db)):
    """Initialize a new job seeker session."""
    orch = get_orchestrator(db)
    session = orch.start_session()
    return {
        "session_id": session.session_id,
        "message": "Hi! I'm your Job Finder Agent. Let's build your profile. What role are you targeting next?",
    }


@router.post("/send-message")
async def send_message(payload: Dict[str, str], db: Session = Depends(get_db)):
    """Process user message and return recommendations if profile is complete."""
    orch = get_orchestrator(db)
    session_id = payload.get("session_id")
    message = payload.get("message")
    if not session_id or not message:
        raise HTTPException(status_code=400, detail="session_id and message required")

    session = orch.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = orch.process_user_message(session_id, message)
    return result


@router.get("/recommendations/{session_id}")
async def get_recommendations(session_id: str, db: Session = Depends(get_db)):
    """Get job recommendations for a completed profile."""
    orch = get_orchestrator(db)
    session = orch.get_session(session_id)
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


@router.get("/filters")
async def get_available_filters(db: Session = Depends(get_db)):
    """Get available filter options (LinkedIn-style) from all jobs."""
    orch = get_orchestrator(db)
    jobs = orch.matching_agent.get_jobs_from_database(db)
    filters = orch.matching_agent.extract_filter_options(jobs)
    return filters


@router.post("/search")
async def search_jobs(payload: Dict, db: Session = Depends(get_db)):
    """Search and filter jobs with LinkedIn-style criteria.
    
    Example payload:
    {
        "session_id": "...",
        "filters": {
            "locations": ["Remote", "New York"],
            "work_types": ["remote"],
            "experience_levels": ["Senior"],
            "skills": ["Python", "React"],
            "keyword": "backend"
        }
    }
    """
    orch = get_orchestrator(db)
    session_id = payload.get("session_id")
    filters = payload.get("filters", {})
    
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    session = orch.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get all jobs from database
    jobs = orch.matching_agent.get_jobs_from_database(db)
    
    # Apply filters
    filtered_jobs = orch.matching_agent.filter_jobs(jobs, filters)
    
    # Score remaining jobs against seeker profile
    recommendations = []
    for job in filtered_jobs:
        score = orch.matching_agent.score_job(session.seeker_profile, job)
        if score > 0:  # Only include jobs with positive score
            recommendation = {
                "job_id": job.id,
                "match_score": score,
                "explanation": f"Match based on skills and preferences",
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "work_type": job.work_type,
                    "experience_level": job.experience_level,
                    "required_skills": job.required_skills,
                    "optional_skills": job.optional_skills,
                    "industries": job.industries,
                    "description": job.description,
                }
            }
            recommendations.append(recommendation)
    
    # Sort by match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "total_results": len(recommendations),
        "filters_applied": filters,
        "recommendations": recommendations
    }
