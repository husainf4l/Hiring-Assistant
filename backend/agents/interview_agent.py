"""
Interview Agent - Asks structured questions about the job
Phase 7: Enhanced AI Prompt Strategy
"""

import json
from typing import Dict, Any, List, Optional
try:
    from .base import BaseAgent
    from .prompts import InterviewAgentPrompts
except ImportError:
    from base import BaseAgent
    from prompts import InterviewAgentPrompts


class InterviewAgent(BaseAgent):
    """
    Interview Agent:
    - Asks the right questions
    - Controls the flow
    - One question at a time
    - Stops only when it has all job information
    """
    
    def __init__(self):
        super().__init__()
        self.questions_asked = []
        self.conversation_history = []
    
    def get_system_prompt(self) -> str:
        """System prompt for the Interview Agent"""
        return InterviewAgentPrompts.get_base_prompt()

    def process(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process user message and generate next question or completion signal
        
        Args:
            user_message: The user's response
            conversation_history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            Dict with:
                - response: Agent's response/question
                - is_complete: Boolean indicating if interview is done
                - extracted_info: Dict with extracted job information
        """
        print(f"DEBUG [InterviewAgent.process]: Starting with user_message={user_message[:50]}")
        
        # Check if user is asking for help/suggestions
        help_section = InterviewAgentPrompts.detect_help_request(user_message)
        
        if help_section:
            print(f"DEBUG [InterviewAgent.process]: User asking for help with: {help_section}")
            # Extract current job info to provide contextual suggestions
            extracted_info = self._extract_job_info_from_history(conversation_history)
            
            # Generate suggestions for the requested section
            suggestion_prompt = InterviewAgentPrompts.get_help_suggestions_prompt(extracted_info, help_section)
            
            try:
                suggestions = self._call_llm(
                    [{"role": "user", "content": suggestion_prompt}],
                    temperature=0.8,
                    max_tokens=800
                )
                
                response = f"Great question! Here are some suggestions for {help_section} for a {extracted_info.get('seniority_level', 'mid-level')} {extracted_info.get('job_title', 'position')}:\n\n{suggestions}\n\nFeel free to use these as inspiration or provide your own details. What would you like to include?"
                
                return {
                    "response": response,
                    "is_complete": False,
                    "extracted_info": extracted_info,
                    "conversation_history": conversation_history + [
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": response}
                    ]
                }
            except Exception as e:
                print(f"DEBUG [InterviewAgent.process]: Error generating suggestions: {e}")
                # Fall through to normal flow if suggestions fail
                pass
        
        # Add user message to conversation
        self.conversation_history = conversation_history + [{"role": "user", "content": user_message}]
        print(f"DEBUG [InterviewAgent.process]: conversation_history length={len(self.conversation_history)}")
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + self.conversation_history
        
        # Add instruction to check if we have enough info
        try:
            completion_prompt = InterviewAgentPrompts.get_completion_check_prompt()
        except:
            completion_prompt = """After your response, analyze if you have collected enough information. 
            If yes, end your response with: [INTERVIEW_COMPLETE]
            If not, continue asking questions."""
        messages.append({
            "role": "system",
            "content": completion_prompt
        })
        
        # Get response from LLM
        print(f"DEBUG [InterviewAgent.process]: Calling LLM with {len(messages)} messages")
        try:
            response = self._call_llm(messages, temperature=0.7, max_tokens=500)
            print(f"DEBUG [InterviewAgent.process]: LLM returned response of length {len(response)}")
        except Exception as e:
            print(f"DEBUG [InterviewAgent.process]: ERROR in _call_llm: {e}")
            raise
        
        # Check if interview is complete
        is_complete = "[INTERVIEW_COMPLETE]" in response
        if is_complete:
            response = response.replace("[INTERVIEW_COMPLETE]", "").strip()
        
        # Extract information from conversation
        print(f"DEBUG [InterviewAgent.process]: Extracting job info...")
        extracted_info = self._extract_job_info()
        print(f"DEBUG [InterviewAgent.process]: Extracted info keys: {list(extracted_info.keys())}")
        
        return {
            "response": response,
            "is_complete": is_complete,
            "extracted_info": extracted_info,
            "conversation_history": self.conversation_history + [{"role": "assistant", "content": response}]
        }
    
    def _extract_job_info(self) -> Dict[str, Any]:
        """Extract structured job information from conversation"""
        return self._extract_job_info_from_history(self.conversation_history)
    
    def _extract_job_info_from_history(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Extract structured job information from given conversation history"""
        # Use LLM to extract structured information
        try:
            extraction_base = InterviewAgentPrompts.get_extraction_prompt()
        except:
            extraction_base = """Based on the following conversation, extract the job information in JSON format.

Extract and return ONLY a JSON object with this structure:
{
    "job_title": "string or null",
    "company": "string or null",
    "location": "string or null",
    "job_type": "string or null",
    "seniority_level": "string or null",
    "responsibilities": ["string"],
    "requirements": ["string"],
    "skills": ["string"],
    "preferred_skills": ["string"],
    "other_info": "string or null"
}

Return ONLY the JSON, no other text."""
        
        extraction_prompt = f"""{extraction_base}

Conversation:
{json.dumps(conversation_history, indent=2)}"""

        try:
            response = self._call_llm(
                [{"role": "user", "content": extraction_prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            # Clean response to get JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            extracted = json.loads(response)
            return extracted
        except Exception as e:
            # Fallback: return empty structure
            return {
                "job_title": None,
                "company": None,
                "location": None,
                "job_type": None,
                "seniority_level": None,
                "responsibilities": [],
                "requirements": [],
                "skills": [],
                "preferred_skills": [],
                "other_info": None
            }
    
    def get_initial_question(self) -> str:
        """Get the first question to start the interview"""
        return "Hi! I'm here to help you create a professional LinkedIn hiring post. Let's start with the basics - what position are you looking to fill?"

