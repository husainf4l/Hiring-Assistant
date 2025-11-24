"""
High-level orchestrator for the Job Finder assistant.
Phase 3: AI Logic scaffolding
"""

from __future__ import annotations

import uuid
from typing import Dict, Optional

from .interview_agent import InterviewAgent
from .matching_agent import MatchingAgent
from .formatter_agent import FormatterAgent
from .models import (
    JobFinderSession,
    JobRecommendation,
    JobSeekerProfile,
    SAMPLE_JOB_LISTINGS,
)


class JobFinderOrchestrator:
    """Coordinates the interview, matching, and formatting agents."""

    def __init__(self) -> None:
        self.sessions: Dict[str, JobFinderSession] = {}
        self.interview_agent = InterviewAgent()
        self.matching_agent = MatchingAgent()
        self.formatter_agent = FormatterAgent()

    def start_session(self) -> JobFinderSession:
        session_id = str(uuid.uuid4())
        profile = JobSeekerProfile(id=session_id)
        session = JobFinderSession(
            session_id=session_id,
            seeker_profile=profile,
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[JobFinderSession]:
        return self.sessions.get(session_id)

    def process_user_message(
        self,
        session_id: str,
        message: str,
    ) -> Dict[str, str | bool | list]:
        session = self.sessions[session_id]
        result = self.interview_agent.process_message(message, session.seeker_profile)

        if result["updates"]:
            session.seeker_profile = session.seeker_profile.copy(update=result["updates"])

        session.messages.append({"role": "user", "content": message})
        session.messages.append({"role": "assistant", "content": result["question"]})
        session.is_profile_complete = bool(result["is_complete"])

        if session.is_profile_complete:
            raw_recs = self.matching_agent.match_jobs(
                session.seeker_profile,
                SAMPLE_JOB_LISTINGS,
            )
            formatted = self.formatter_agent.format_recommendations(raw_recs)
            session.recommendations = formatted

        return {
            "next_question": result["question"],
            "profile": session.seeker_profile.model_dump(),
            "recommendations": [
                rec.model_dump() for rec in session.recommendations
            ],
            "is_profile_complete": session.is_profile_complete,
        }

