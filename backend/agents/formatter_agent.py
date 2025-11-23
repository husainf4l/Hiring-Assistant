"""
Formatter Agent - Polishes the hiring post
Phase 7: Enhanced AI Prompt Strategy
"""

import json
from typing import Dict, Any
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .base import BaseAgent
    from ..models import JobPost
    from .prompts import FormatterAgentPrompts
except ImportError:
    try:
        from base import BaseAgent
        from models import JobPost
        from prompts import FormatterAgentPrompts
    except ImportError:
        from agents.base import BaseAgent
        from agents.prompts import FormatterAgentPrompts
        from models import JobPost


class FormatterAgent(BaseAgent):
    """
    Formatter Agent:
    - Bullet points
    - Spacing
    - Paragraph formatting
    - Clean English
    - Professional tone
    - No fluff
    """
    
    def get_system_prompt(self) -> str:
        """System prompt for the Formatter Agent"""
        return FormatterAgentPrompts.get_base_prompt()

    def process(self, job_post: JobPost) -> JobPost:
        """
        Format and polish a JobPost
        
        Args:
            job_post: The JobPost object to format
        
        Returns:
            Formatted JobPost object
        """
        # Convert JobPost to dict for processing
        post_dict = {
            "title": job_post.title or "",
            "summary": job_post.summary or "",
            "culture_and_team": job_post.culture_and_team or "",
            "responsibilities": job_post.responsibilities or [],
            "requirements": job_post.requirements or [],
            "skills": job_post.skills or [],
            "keywords": job_post.keywords or [],
            "hashtags": job_post.hashtags or [],
            "tone_type": job_post.tone_type or "professional"
        }
        
        try:
            base_prompt = FormatterAgentPrompts.get_base_prompt()
        except:
            base_prompt = """You are an expert content editor and formatter specializing in LinkedIn hiring posts."""
        
        user_prompt = f"""{base_prompt}

Format and polish this hiring post. Make it clean, professional, and LinkedIn-ready:

{json.dumps(post_dict, indent=2)}

Return the formatted version in the same JSON structure."""

        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]
        
        # Get response from LLM
        response = self._call_llm(messages, temperature=0.5, max_tokens=2000)
        
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
            
            formatted_data = json.loads(response)
            
            # Update JobPost with formatted content
            job_post.title = formatted_data.get("title", job_post.title)
            job_post.summary = formatted_data.get("summary", job_post.summary)
            job_post.culture_and_team = formatted_data.get("culture_and_team", job_post.culture_and_team)
            job_post.responsibilities = formatted_data.get("responsibilities", job_post.responsibilities)
            job_post.requirements = formatted_data.get("requirements", job_post.requirements)
            job_post.skills = formatted_data.get("skills", job_post.skills)
            job_post.keywords = formatted_data.get("keywords", job_post.keywords)
            job_post.hashtags = formatted_data.get("hashtags", job_post.hashtags)
            job_post.tone_type = formatted_data.get("tone_type", job_post.tone_type)
            
            return job_post
            
        except json.JSONDecodeError:
            # If parsing fails, return original post
            return job_post
    
    def format_section(self, section_type: str, content: Any) -> Any:
        """
        Format a specific section of the post
        
        Args:
            section_type: Type of section (summary, responsibilities, requirements, etc.)
            content: The content to format
        
        Returns:
            Formatted content
        """
        try:
            section_prompt = FormatterAgentPrompts.get_section_formatting_prompt(section_type)
            base_prompt = FormatterAgentPrompts.get_base_prompt()
        except:
            base_prompt = """You are an expert content editor and formatter specializing in LinkedIn hiring posts."""
            section_prompt = f"Format this {section_type} for a LinkedIn hiring post. Make it clean, professional, and engaging."
        
        prompt = f"""{section_prompt}

Content to format:
{json.dumps(content, indent=2) if isinstance(content, (list, dict)) else content}

Return the formatted version. If it's a list, return a JSON array. If it's text, return the formatted text string."""

        messages = [
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(messages, temperature=0.5, max_tokens=1000)
        
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            if isinstance(content, list):
                return json.loads(response)
            else:
                return response.strip()
        except:
            return content

