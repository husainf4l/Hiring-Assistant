"""
Simplified Interview Agent for the Job Finder assistant.
Phase 3: AI Logic scaffolding
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional
from openai import OpenAI

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
        # Initialize OpenAI client for LLM fallback
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"
        else:
            self.client = None
            self.model = None

    def get_next_question(self, profile: JobSeekerProfile) -> str | None:
        # Check if we have enough info to make recommendations
        # Required: skills, preferred_titles, work_type
        has_skills = bool(profile.skills)
        has_titles = bool(profile.preferred_titles)
        has_work_type = bool(profile.work_type)
        
        # If we have at least skills and titles and work type, we're good
        if has_skills and has_titles and has_work_type:
            return None
        
        # Otherwise, ask for missing info
        for field in self.questions_order:
            value = getattr(profile, field)
            if field in ["current_role", "salary_expectation"]:
                # These are optional - skip them
                continue
            if not value:
                return REQUIRED_FIELDS[field]
        return None

    def process_message(
        self,
        message: str,
        profile: JobSeekerProfile,
    ) -> Dict[str, str | bool]:
        """
        Extract structured data from user message with improved keyword extraction and LLM fallback.
        """
        lower = message.lower()
        updates: Dict[str, str | List[str]] = {}

        # Extract work type
        if "remote" in lower:
            updates["work_type"] = "remote"
        elif "hybrid" in lower:
            updates["work_type"] = "hybrid"
        elif "onsite" in lower or "on-site" in lower:
            updates["work_type"] = "onsite"

        # Extract preferred titles
        title_keywords = ["frontend", "backend", "full-stack", "fullstack", "full stack", "engineer", 
                         "developer", "product manager", "designer", "devops", "data scientist",
                         "qa", "lead", "senior", "junior", "mid-level"]
        found_titles = [t for t in title_keywords if t in lower]
        if found_titles:
            updates["preferred_titles"] = found_titles

        # Extract skills - more sophisticated parsing
        skill_keywords = ["react", "next.js", "nextjs", "angular", "vue", "svelte",
                         "typescript", "javascript", "python", "java", "golang",
                         "node", "nodejs", "express", "django", "flask", "fastapi", 
                         "kubernetes", "docker", "aws", "gcp", "azure", 
                         "sql", "postgres", "mongodb", "redis", "firebase",
                         "figma", "sketch", "ui", "ux", "design", "testing", "selenium",
                         "git", "agile", "scrum", "leadership", "communication", "graphql"]
        found_skills = [s for s in skill_keywords if s in lower]
        if found_skills:
            existing_skills = [s.lower() for s in profile.skills if len(s) > 3]
            all_skills = list(set(existing_skills + found_skills))
            updates["skills"] = sorted(all_skills)

        # Extract industries
        industry_keywords = ["ai", "saas", "fintech", "healthcare", "ecommerce", "edtech",
                           "travel", "social", "startup", "fortune 500", "crypto", "blockchain"]
        found_industries = [ind for ind in industry_keywords if ind in lower]
        if found_industries:
            updates["industries"] = found_industries

        # Extract preferred locations (more comprehensive)
        location_keywords = ["remote", "san francisco", "new york", "seattle", "austin",
                            "london", "berlin", "toronto", "us", "usa", "europe",
                            "jordan", "amman", "beirut", "dubai", "uae", "middle east",
                            "tokyo", "singapore", "sydney", "india", "bangalore"]
        found_locations = [loc for loc in location_keywords if loc in lower and loc != "remote"]
        
        # If they mention "remote", add it to locations
        if "remote" in lower:
            found_locations.append("remote")
        
        if found_locations:
            updates["preferred_locations"] = found_locations

        # Check if user explicitly mentioned their current role
        if any(word in lower for word in ["i'm a", "i am a", "currently", "working as", "my role"]):
            # Extract role from message
            words = message.split()
            updates["current_role"] = message[:100]  # Take first 100 chars as current role

        # If no keywords were extracted and LLM is available, use LLM to understand the message
        if not updates and self.client and len(message.strip()) >= 2:
            try:
                updates = self._extract_with_llm(message, profile)
            except Exception as e:
                print(f"DEBUG [InterviewAgent]: LLM extraction failed: {e}, continuing with no updates")
                # Continue without updates - will just ask next question

        
        next_question = self.get_next_question(profile.copy(update=updates))
        is_complete = next_question is None
        
        # If no updates were made (user said something like "hi" or "how are you"),
        # generate a more natural follow-up response
        final_response = next_question or "[PROFILE_COMPLETE]"
        if not updates and next_question and self.client:
            try:
                final_response = self._generate_conversational_response(message, next_question, profile)
            except Exception as e:
                print(f"DEBUG [InterviewAgent]: Failed to generate conversational response: {e}")
                # Fall back to just the question

        return {
            "question": final_response,
            "is_complete": is_complete,
            "updates": updates,
        }

    def _extract_with_llm(self, message: str, profile: JobSeekerProfile) -> Dict[str, str | List[str]]:
        """
        Use LLM to extract job seeker information from conversational input.
        
        Args:
            message: User's conversational message
            profile: Current job seeker profile
            
        Returns:
            Dictionary with extracted updates
        """
        # Build context about what we're missing
        missing_fields = []
        if not profile.preferred_titles:
            missing_fields.append("preferred_titles (target job titles)")
        if not profile.skills:
            missing_fields.append("skills (technical/professional skills)")
        if not profile.work_type:
            missing_fields.append("work_type (remote/hybrid/onsite)")
        if not profile.preferred_locations:
            missing_fields.append("preferred_locations (cities or remote)")
        if not profile.industries:
            missing_fields.append("industries (tech, finance, healthcare, etc)")
        
        prompt = f"""You are helping extract job seeker information from a conversational message.
The user just said: "{message}"

Current profile state:
- preferred_titles: {profile.preferred_titles or 'Not specified'}
- skills: {profile.skills or 'Not specified'}
- work_type: {profile.work_type or 'Not specified'}
- preferred_locations: {profile.preferred_locations or 'Not specified'}
- industries: {profile.industries or 'Not specified'}
- current_role: {profile.current_role or 'Not specified'}

Missing fields we're trying to collect: {', '.join(missing_fields) if missing_fields else 'None'}

Based on the user's message, extract relevant information in JSON format:
{{
    "preferred_titles": ["title1", "title2"] or null,
    "skills": ["skill1", "skill2"] or null,
    "work_type": "remote|hybrid|onsite" or null,
    "preferred_locations": ["location1"] or null,
    "industries": ["industry1"] or null,
    "current_role": "description" or null
}}

IMPORTANT: Only include fields where you found VERY SPECIFIC job-related information.
For casual messages like 'hi', 'how are you', 'thanks', etc with no job info, return empty JSON {{}}.
Return ONLY valid JSON, no markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Low temperature for structured extraction
                max_tokens=300,
                timeout=10.0
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            extracted = json.loads(response_text)
            
            # Filter out null values
            result = {k: v for k, v in extracted.items() if v is not None}
            
            return result
        except json.JSONDecodeError as e:
            print(f"DEBUG [InterviewAgent]: Failed to parse LLM response as JSON: {e}")
            return {}
        except Exception as e:
            print(f"DEBUG [InterviewAgent]: LLM extraction error: {e}")
            return {}

    def _generate_conversational_response(self, user_message: str, next_question: str, profile: JobSeekerProfile) -> str:
        """
        Generate a natural, conversational response that acknowledges the user's message 
        and smoothly transitions to the next interview question.
        
        Args:
            user_message: The user's non-informative message (e.g., "hi", "how are you")
            next_question: The next interview question to ask
            profile: Current job seeker profile
            
        Returns:
            A conversational response that includes the next question
        """
        prompt = f"""You are a friendly job finder assistant helping someone build their professional profile.

The user just said: "{user_message}"

The next question you need to ask them is: "{next_question}"

Your task: Write a natural, friendly response that:
1. Acknowledges their message in a warm way
2. Smoothly transitions to asking the question above
3. Keeps the tone conversational and encouraging
4. Is concise (2-3 sentences max)

Write ONLY the response, no preamble. End with the question."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # Slightly higher for natural tone
                max_tokens=150,
                timeout=10.0
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"DEBUG [InterviewAgent]: Failed to generate conversational response: {e}")
            # Fall back to just the question
            return next_question




