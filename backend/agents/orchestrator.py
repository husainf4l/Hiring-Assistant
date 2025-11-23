"""
Agent Orchestrator - Coordinates all three AI agents
Phase 3: AI Logic Design
"""

import json
from typing import Dict, Any, List, Optional
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .interview_agent import InterviewAgent
    from .composer_agent import ComposerAgent
    from .formatter_agent import FormatterAgent
    from ..models import JobPost
except ImportError:
    try:
        from interview_agent import InterviewAgent
        from composer_agent import ComposerAgent
        from formatter_agent import FormatterAgent
    except ImportError:
        # If agents are in agents package
        from agents.interview_agent import InterviewAgent
        from agents.composer_agent import ComposerAgent
        from agents.formatter_agent import FormatterAgent
    from models import JobPost


class AgentOrchestrator:
    """
    Orchestrates the three AI agents:
    1. Interview Agent - collects information
    2. Composer Agent - creates the post
    3. Formatter Agent - polishes the post
    """
    
    def __init__(self):
        self._interview_agent = None
        self._composer_agent = None
        self._formatter_agent = None
        self.current_session: Optional[Dict[str, Any]] = None
    
    @property
    def interview_agent(self):
        if self._interview_agent is None:
            self._interview_agent = InterviewAgent()
        return self._interview_agent
    
    @property
    def composer_agent(self):
        if self._composer_agent is None:
            self._composer_agent = ComposerAgent()
        return self._composer_agent
    
    @property
    def formatter_agent(self):
        if self._formatter_agent is None:
            self._formatter_agent = FormatterAgent()
        return self._formatter_agent
    
    def start_session(self, session_id: str) -> Dict[str, Any]:
        """
        Start a new interview session
        
        Args:
            session_id: Unique session identifier
        
        Returns:
            Dict with initial question and session info
        """
        self.current_session = {
            "session_id": session_id,
            "conversation_history": [],
            "job_info": {},
            "is_complete": False,
            "job_post": None
        }
        
        initial_question = self.interview_agent.get_initial_question()
        
        return {
            "session_id": session_id,
            "response": initial_question,
            "is_complete": False,
            "job_post": None
        }
    
    def process_message(self, session_id: str, user_message: str, conversation_history: List[dict]) -> Dict[str, Any]:
        """
        Process a user message through the agent pipeline
        
        Args:
            session_id: Session identifier
            user_message: User's message
            conversation_history: Previous conversation messages
        
        Returns:
            Dict with agent response, completion status, and updated job post
        """
        if not self.current_session or self.current_session["session_id"] != session_id:
            # Start new session if needed
            self.start_session(session_id)
        
        # Step 1: Interview Agent processes the message
        # conversation_history is already in dict format
        interview_result = self.interview_agent.process(user_message, conversation_history)
        
        # Update session state
        self.current_session["conversation_history"] = interview_result["conversation_history"]
        self.current_session["job_info"] = interview_result["extracted_info"]
        
        # BUILD LIVE PREVIEW: Create partial JobPost as user answers
        live_preview_job_post = self._build_live_preview(interview_result["extracted_info"])
        
    # If interview is complete, move to composition
        if interview_result["is_complete"]:
            self.current_session["is_complete"] = True
            
            # Step 2: Composer Agent creates the full post
            job_post = self.composer_agent.process(interview_result["extracted_info"])
            
            # Step 3: Formatter Agent polishes the post
            job_post = self.formatter_agent.process(job_post)
            
            self.current_session["job_post"] = job_post
            
            return {
                "session_id": session_id,
                "response": interview_result["response"] + "\n\nGreat! I've created your hiring post. Check the preview on the right!",
                "is_complete": True,
                "job_post": job_post.model_dump() if hasattr(job_post, 'model_dump') else job_post.dict() if hasattr(job_post, 'dict') else job_post
            }
        else:
            # Save partial job_post into session so preview endpoint can access it
            self.current_session["job_post"] = live_preview_job_post
            # Interview still in progress - return live preview
            return {
                "session_id": session_id,
                "response": interview_result["response"],
                "is_complete": False,
                "job_post": live_preview_job_post.model_dump() if hasattr(live_preview_job_post, 'model_dump') else live_preview_job_post.dict() if hasattr(live_preview_job_post, 'dict') else live_preview_job_post
            }
    
    def regenerate_section(self, session_id: str, section_type: str, job_post: JobPost) -> JobPost:
        """
        Regenerate a specific section of the post
        
        Args:
            session_id: Session identifier
            section_type: Type of section to regenerate (summary, responsibilities, etc.)
            job_post: Current job post
        
        Returns:
            Updated JobPost with regenerated section
        """
        if section_type == "summary":
            job_post.summary = self.formatter_agent.format_section("summary", job_post.summary)
        elif section_type == "culture_and_team":
            job_post.culture_and_team = self.formatter_agent.format_section("culture_and_team", job_post.culture_and_team)
        elif section_type == "responsibilities":
            job_post.responsibilities = self.formatter_agent.format_section("responsibilities", job_post.responsibilities)
        elif section_type == "requirements":
            job_post.requirements = self.formatter_agent.format_section("requirements", job_post.requirements)
        elif section_type == "skills":
            job_post.skills = self.formatter_agent.format_section("skills", job_post.skills)
        elif section_type == "hashtags":
            # Regenerate hashtags based on current post content
            hashtags = self._regenerate_hashtags(job_post)
            job_post.hashtags = hashtags
        elif section_type == "keywords":
            # Regenerate keywords based on current post content
            keywords = self._regenerate_keywords(job_post)
            job_post.keywords = keywords
        
        # Re-format the entire post after regeneration
        job_post = self.formatter_agent.process(job_post)
        
        return job_post
    
    def _regenerate_hashtags(self, job_post: JobPost) -> List[str]:
        """Regenerate hashtags for the post"""
        prompt = f"""Generate 5-8 relevant LinkedIn hashtags for this job post:

Title: {job_post.title}
Summary: {job_post.summary}
Skills: {', '.join(job_post.skills[:5])}

Return ONLY a JSON array of hashtag strings (without the # symbol), no other text.
Example: ["hiring", "techjobs", "softwareengineer"]"""

        response = self.formatter_agent._call_llm(
            [{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            return json.loads(response)
        except:
            return job_post.hashtags
    
    def _regenerate_keywords(self, job_post: JobPost) -> List[str]:
        """Regenerate keywords for the post"""
        prompt = f"""Generate 5-10 LinkedIn-optimized keywords for this job post:

Title: {job_post.title}
Summary: {job_post.summary}
Skills: {', '.join(job_post.skills[:5])}

Return ONLY a JSON array of keyword strings, no other text.
Example: ["software engineer", "python", "remote work"]"""

        response = self.formatter_agent._call_llm(
            [{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response.strip()
            return json.loads(response)
        except:
            return job_post.keywords

    def _build_live_preview(self, extracted_info: Dict[str, Any]) -> JobPost:
        """
        Build a live preview JobPost from partially extracted information during interview
        This shows the user what we've collected so far as they answer questions
        
        Args:
            extracted_info: Extracted job information from conversation
        
        Returns:
            JobPost with live data populated
        """
        # Create a JobPost with whatever info we have so far
        job_post = JobPost(
            title=extracted_info.get("job_title"),
            company=extracted_info.get("company"),
            location=extracted_info.get("location"),
            job_type=extracted_info.get("job_type"),
            # Accept either workplace_type or work_arrangement key
            workplace_type=extracted_info.get("workplace_type") or extracted_info.get("work_arrangement"),
            summary=extracted_info.get("summary") or None,
            culture_and_team=extracted_info.get("culture_and_team") or None,
            responsibilities=extracted_info.get("responsibilities", []),
            requirements=extracted_info.get("requirements", []),
            skills=extracted_info.get("skills", []),
            keywords=extracted_info.get("keywords", []),
            hashtags=extracted_info.get("hashtags", []),
            tone_type=extracted_info.get("tone_type"),
        )
        
        return job_post