"""
Post Composer Agent - Builds the full hiring post
Phase 7: Enhanced AI Prompt Strategy
"""

import json
from typing import Dict, Any, List
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .base import BaseAgent
    from ..models import JobPost
    from .prompts import ComposerAgentPrompts
except ImportError:
    try:
        from base import BaseAgent
        from models import JobPost
        from prompts import ComposerAgentPrompts
    except ImportError:
        from agents.base import BaseAgent
        from agents.prompts import ComposerAgentPrompts
        from models import JobPost


class ComposerAgent(BaseAgent):
    """
    Post Composer Agent:
    - Builds the full hiring post
    - Creates job summary
    - Generates responsibilities
    - Generates requirements
    - Generates skills
    - Generates LinkedIn keywords
    - Generates hashtags
    - Writes with the right tone based on job type & seniority
    """
    
    def get_system_prompt(self, job_info: Dict[str, Any]) -> str:
        """System prompt for the Composer Agent"""
        try:
            return ComposerAgentPrompts.get_base_prompt(job_info)
        except:
            # Fallback prompt if imports fail
            return f"""You are an expert LinkedIn hiring post writer. Create a professional, engaging LinkedIn hiring post based on the job information provided.

Job Information: {job_info}

Return a JSON object with: title, summary, responsibilities, requirements, skills, keywords, hashtags, tone_type."""

    def _determine_tone(self, job_info: Dict[str, Any]) -> str:
        """Determine the appropriate tone based on job type and seniority"""
        # This method is now handled by ComposerAgentPrompts._get_tone_instruction
        # Keeping for backward compatibility but using prompts module
        try:
            return ComposerAgentPrompts._get_tone_instruction(job_info)
        except:
            # Fallback tone instruction
            return "Professional tone: Clear, engaging, results-oriented. Use strong action verbs. Emphasize impact and opportunities."

    def process(self, job_info: Dict[str, Any]) -> JobPost:
        """
        Compose a full hiring post from job information
        
        Args:
            job_info: Dictionary with extracted job information from Interview Agent
        
        Returns:
            JobPost object with all fields populated
        """
        # Build the prompt
        system_prompt = self.get_system_prompt(job_info)
        
        try:
            user_prompt = ComposerAgentPrompts.get_user_prompt(job_info)
        except:
            user_prompt = f"""Create a LinkedIn hiring post based on this information:

{json.dumps(job_info, indent=2)}

Remember to make it engaging and LinkedIn-optimized."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Get response from LLM
        response = self._call_llm(messages, temperature=0.7, max_tokens=2000)
        
        # Parse JSON response
        try:
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            post_data = json.loads(response)
            
            # Create JobPost object
            job_post = JobPost(
                title=post_data.get("title", job_info.get("job_title", "")),
                company=job_info.get("company", ""),
                location=job_info.get("location", ""),
                workplace_type=job_info.get("work_arrangement", ""),
                job_type=job_info.get("job_type", ""),
                summary=post_data.get("summary", ""),
                culture_and_team=post_data.get("culture_and_team", job_info.get("culture_and_team", "")),
                responsibilities=post_data.get("responsibilities", []),
                requirements=post_data.get("requirements", []),
                skills=post_data.get("skills", []),
                keywords=post_data.get("keywords", []),
                hashtags=post_data.get("hashtags", []),
                tone_type=post_data.get("tone_type", "professional")
            )
            
            return job_post
            
        except json.JSONDecodeError as e:
            # Fallback: create basic post from job_info
            return self._create_fallback_post(job_info)
    
    def _create_fallback_post(self, job_info: Dict[str, Any]) -> JobPost:
        """Create a basic post if JSON parsing fails"""
        return JobPost(
            title=job_info.get("job_title", "Position"),
            company=job_info.get("company", ""),
            location=job_info.get("location", ""),
            workplace_type=job_info.get("work_arrangement", ""),
            job_type=job_info.get("job_type", ""),
            summary=f"We're looking for a {job_info.get('job_title', 'talented professional')} to join our team.",
            responsibilities=job_info.get("responsibilities", []),
            requirements=job_info.get("requirements", []),
            skills=job_info.get("skills", []) + job_info.get("preferred_skills", []),
            keywords=[],
            hashtags=[],
            tone_type="professional"
        )

