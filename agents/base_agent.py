"""
Base Agent class for the Math Mentor multi-agent system.
Defines common interfaces and utilities for all agents.
Uses Gemini for LLM calls with rate limiting.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import time
import google.generativeai as genai

from config.settings import get_settings

# Rate limiting for LLM calls
_last_llm_call = 0
_MIN_LLM_DELAY = 1.0  # Minimum 1 second between LLM calls


def _rate_limit_llm():
    """Enforce rate limiting for LLM calls."""
    global _last_llm_call
    elapsed = time.time() - _last_llm_call
    if elapsed < _MIN_LLM_DELAY:
        time.sleep(_MIN_LLM_DELAY - elapsed)
    _last_llm_call = time.time()


@dataclass
class TraceEntry:
    """Single entry in agent execution trace."""
    agent_name: str
    action: str
    input_summary: str
    output_summary: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    status: str = "success"  # success, error, hitl_triggered
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "action": self.action,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "status": self.status
        }


@dataclass
class AgentResponse:
    """Standard response from an agent."""
    success: bool
    data: Dict[str, Any]
    message: str = ""
    needs_hitl: bool = False
    hitl_reason: str = ""
    confidence: float = 1.0
    trace: Optional[TraceEntry] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
            "needs_hitl": self.needs_hitl,
            "hitl_reason": self.hitl_reason,
            "confidence": self.confidence,
            "trace": self.trace.to_dict() if self.trace else None
        }


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, description: str):
        """Initialize the agent.
        
        Args:
            name: Agent name for identification.
            description: Brief description of agent's role.
        """
        self.name = name
        self.description = description
        self.settings = get_settings()
        self._model = None
    
    @property
    def model(self):
        """Lazy load Gemini model."""
        if self._model is None:
            genai.configure(api_key=self.settings.gemini_api_key)
            self._model = genai.GenerativeModel(self.settings.gemini_model)
        return self._model
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Execute the agent's main function.
        
        Args:
            input_data: Input data for the agent.
            
        Returns:
            AgentResponse with results.
        """
        pass
    
    def _call_llm(self, prompt: str, system_instruction: str = None) -> str:
        """Call the Gemini LLM with a prompt and rate limiting.
        
        Args:
            prompt: The user prompt.
            system_instruction: Optional system instruction.
            
        Returns:
            LLM response text.
        """
        try:
            _rate_limit_llm()  # Enforce rate limiting
            
            if system_instruction:
                model = genai.GenerativeModel(
                    self.settings.gemini_model,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"LLM Error in {self.name}: {e}")
            return ""
    
    def _create_trace(
        self,
        action: str,
        input_summary: str,
        output_summary: str,
        duration_ms: float = 0.0,
        status: str = "success"
    ) -> TraceEntry:
        """Create a trace entry for this agent action.
        
        Args:
            action: Action description.
            input_summary: Summary of input.
            output_summary: Summary of output.
            duration_ms: Duration in milliseconds.
            status: Status string.
            
        Returns:
            TraceEntry object.
        """
        return TraceEntry(
            agent_name=self.name,
            action=action,
            input_summary=input_summary,
            output_summary=output_summary,
            duration_ms=duration_ms,
            status=status
        )
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
