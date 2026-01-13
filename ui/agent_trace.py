"""
Agent Trace Manager - Manages and formats agent execution traces.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass 
class TraceStep:
    """Single trace step."""
    agent_name: str
    action: str
    input_preview: str
    output_preview: str
    status: str
    duration_ms: float
    timestamp: datetime
    
    def to_display_dict(self) -> Dict[str, Any]:
        """Convert to display format."""
        return {
            "agent": self.agent_name,
            "action": self.action,
            "summary": self.output_preview,
            "status": self.status,
            "duration": f"{self.duration_ms:.0f}ms"
        }


class AgentTraceManager:
    """Manages agent execution traces."""
    
    def __init__(self):
        """Initialize trace manager."""
        self.steps: List[TraceStep] = []
        self.start_time = None
    
    def start_trace(self) -> None:
        """Start a new trace session."""
        self.steps = []
        self.start_time = datetime.now()
    
    def add_step(
        self,
        agent_name: str,
        action: str,
        input_preview: str,
        output_preview: str,
        status: str = "success",
        duration_ms: float = 0.0
    ) -> None:
        """Add a trace step.
        
        Args:
            agent_name: Name of the agent.
            action: Action performed.
            input_preview: Preview of input.
            output_preview: Preview of output.
            status: 'success', 'error', or 'hitl_triggered'.
            duration_ms: Duration in milliseconds.
        """
        step = TraceStep(
            agent_name=agent_name,
            action=action,
            input_preview=input_preview[:100] if input_preview else "",
            output_preview=output_preview[:100] if output_preview else "",
            status=status,
            duration_ms=duration_ms,
            timestamp=datetime.now()
        )
        self.steps.append(step)
    
    def get_display_traces(self) -> List[Dict[str, Any]]:
        """Get traces formatted for display.
        
        Returns:
            List of trace dictionaries.
        """
        return [step.to_display_dict() for step in self.steps]
    
    def get_total_duration(self) -> float:
        """Get total trace duration.
        
        Returns:
            Total duration in milliseconds.
        """
        if not self.steps:
            return 0.0
        return sum(step.duration_ms for step in self.steps)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get trace summary.
        
        Returns:
            Summary dictionary.
        """
        return {
            "total_steps": len(self.steps),
            "total_duration_ms": self.get_total_duration(),
            "agents_involved": list(set(s.agent_name for s in self.steps)),
            "had_hitl": any(s.status == "hitl_triggered" for s in self.steps),
            "had_errors": any(s.status == "error" for s in self.steps)
        }
    
    def load_from_orchestrator(self, traces: List[Dict]) -> None:
        """Load traces from orchestrator result.
        
        Args:
            traces: List of trace dicts from orchestrator.
        """
        self.steps = []
        for t in traces:
            self.add_step(
                agent_name=t.get("agent_name", "Unknown"),
                action=t.get("action", ""),
                input_preview=t.get("input_summary", ""),
                output_preview=t.get("output_summary", ""),
                status=t.get("status", "success"),
                duration_ms=t.get("duration_ms", 0.0)
            )
