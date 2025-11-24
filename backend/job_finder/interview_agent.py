"""
Simplified Interview Agent for the Job Finder assistant.
Phase 3: AI Logic scaffolding
"""

from __future__ import annotations

from typing import Dict, List

from .models import JobSeekerProfile

REQUIRED_FIELDS: Dict[str, str] = {
    "current_role": "What is your current or most recent role?",
    "preferred_titles": "What job titles are you targeting next?",
    "skills": "List 3-5 core skills you want to highlight.",
    "preferred_locations": "Do you have preferred locations or are you open to remote roles?",
    "work_type": "What work style do you prefer? (remote / onsite / hybrid)",
    "industries": "Which industries are you most interested in?",
    "salary_expectation": "Do you have a salary range in mind?",
}


class InterviewAgent:
    """Collects structured data about the job seeker."""

    def __init__(self) -> None:
        self.questions_order = list(REQUIRED_FIELDS.keys())

    def get_next_question(self, profile: JobSeekerProfile) -> str | None:
        for field in self.questions_order:
            value = getattr(profile, field)
            if not value:
                return REQUIRED_FIELDS[field]
        return None

    def process_message(
        self,
        message: str,
        profile: JobSeekerProfile,
    ) -> Dict[str, str | bool]:
        """
        Very lightweight keyword extraction to simulate structured collection.
        """
        lower = message.lower()
        updates: Dict[str, str | List[str]] = {}

        if "remote" in lower:
            updates["work_type"] = "remote"
        elif "hybrid" in lower:
            updates["work_type"] = "hybrid"
        elif "onsite" in lower or "on-site" in lower:
            updates["work_type"] = "onsite"

        skill_tokens = [
            token.strip()
            for token in message.replace("/", ",").split(",")
            if len(token.strip()) > 2
        ]
        if skill_tokens:
            updates["skills"] = sorted(
                list({*profile.skills, *(s.lower() for s in skill_tokens)})
            )

        next_question = self.get_next_question(profile.copy(update=updates))
        is_complete = next_question is None

        return {
            "question": next_question or "[PROFILE_COMPLETE]",
            "is_complete": is_complete,
            "updates": updates,
        }


