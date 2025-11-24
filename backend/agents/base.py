"""
Base Agent class for AI agents
Phase 3: AI Logic Design
"""

from abc import ABC, abstractmethod
from openai import OpenAI
import os
from typing import Dict, Any, Optional


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using cost-effective model
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Process method to be implemented by each agent"""
        pass
    
    def _call_llm(self, messages: list, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Helper method to call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=30.0  # 30 second timeout
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = f"Error calling OpenAI API: {str(e)}"
            print(f"ERROR in _call_llm: {error_msg}")
            raise Exception(error_msg)


