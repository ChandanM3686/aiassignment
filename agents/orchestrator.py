"""
Agent Orchestrator - Coordinates the multi-agent workflow.
"""

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .parser_agent import ParserAgent
from .router_agent import RouterAgent
from .solver_agent import SolverAgent
from .verifier_agent import VerifierAgent
from .explainer_agent import ExplainerAgent
from .base_agent import AgentResponse, TraceEntry


@dataclass
class OrchestratorResult:
    """Complete result from the orchestrator."""
    success: bool
    final_answer: str
    explanation: str
    explanation_markdown: str
    confidence: float
    needs_hitl: bool
    hitl_reason: str
    traces: List[TraceEntry]
    retrieved_sources: List[Dict]
    parsed_problem: Dict
    solution: Dict
    verification: Dict
    total_time_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "final_answer": self.final_answer,
            "explanation": self.explanation,
            "explanation_markdown": self.explanation_markdown,
            "confidence": self.confidence,
            "needs_hitl": self.needs_hitl,
            "hitl_reason": self.hitl_reason,
            "traces": [t.to_dict() for t in self.traces],
            "retrieved_sources": self.retrieved_sources,
            "parsed_problem": self.parsed_problem,
            "solution": self.solution,
            "verification": self.verification,
            "total_time_ms": self.total_time_ms
        }


class AgentOrchestrator:
    """Orchestrates the multi-agent math solving workflow."""
    
    def __init__(self):
        """Initialize all agents."""
        self.parser = ParserAgent()
        self.router = RouterAgent()
        self.solver = SolverAgent()
        self.verifier = VerifierAgent()
        self.explainer = ExplainerAgent()
        
        self.traces: List[TraceEntry] = []
    
    def solve(
        self,
        raw_input: str,
        input_type: str = "text",
        input_confidence: float = 1.0
    ) -> OrchestratorResult:
        """Execute the complete solving workflow.
        
        Args:
            raw_input: Raw input text from OCR/ASR/text.
            input_type: Type of input ('image', 'audio', 'text').
            input_confidence: Confidence from input processing.
            
        Returns:
            OrchestratorResult with complete solution.
        """
        start_time = time.time()
        self.traces = []
        
        # Step 1: Parse the input
        parse_result = self.parser.execute({
            "raw_text": raw_input,
            "input_type": input_type,
            "confidence": input_confidence
        })
        
        if parse_result.trace:
            self.traces.append(parse_result.trace)
        
        if not parse_result.success:
            return self._create_error_result(
                "Failed to parse input",
                parse_result,
                time.time() - start_time
            )
        
        # Check for HITL at parsing stage
        if parse_result.needs_hitl:
            return self._create_hitl_result(
                parse_result.hitl_reason,
                parse_result.data,
                time.time() - start_time
            )
        
        parsed_problem = parse_result.data
        
        # Step 2: Route to appropriate solver
        route_result = self.router.execute(parsed_problem)
        
        if route_result.trace:
            self.traces.append(route_result.trace)
        
        routing = route_result.data
        
        # Step 3: Solve the problem
        solver_input = {**parsed_problem, **routing}
        solve_result = self.solver.execute(solver_input)
        
        if solve_result.trace:
            self.traces.append(solve_result.trace)
        
        if not solve_result.success:
            return self._create_error_result(
                "Failed to solve problem",
                solve_result,
                time.time() - start_time
            )
        
        solution = solve_result.data
        
        # Step 4: Verify the solution
        verify_result = self.verifier.execute({
            "problem_text": parsed_problem.get("problem_text", ""),
            "solution": solution
        })
        
        if verify_result.trace:
            self.traces.append(verify_result.trace)
        
        verification = verify_result.data
        
        # Check for HITL at verification stage
        if verify_result.needs_hitl:
            return self._create_verification_hitl_result(
                verify_result.hitl_reason,
                parsed_problem,
                solution,
                verification,
                time.time() - start_time
            )
        
        # Step 5: Generate explanation
        explain_result = self.explainer.execute({
            "problem_text": parsed_problem.get("problem_text", ""),
            "solution": solution,
            "verification": verification,
            "topic": parsed_problem.get("topic", ""),
            "subtopic": parsed_problem.get("subtopic", "")
        })
        
        if explain_result.trace:
            self.traces.append(explain_result.trace)
        
        explanation_data = explain_result.data
        
        total_time = (time.time() - start_time) * 1000
        
        return OrchestratorResult(
            success=True,
            final_answer=solution.get("final_answer", ""),
            explanation=explanation_data.get("formatted", {}),
            explanation_markdown=explanation_data.get("markdown", ""),
            confidence=verification.get("combined_confidence", 0.8),
            needs_hitl=False,
            hitl_reason="",
            traces=self.traces,
            retrieved_sources=solution.get("retrieved_sources", []),
            parsed_problem=parsed_problem,
            solution=solution,
            verification=verification,
            total_time_ms=total_time
        )
    
    def solve_with_correction(
        self,
        corrected_text: str,
        original_parsed: Dict[str, Any]
    ) -> OrchestratorResult:
        """Re-solve after user corrects the parsed input.
        
        Args:
            corrected_text: User-corrected problem text.
            original_parsed: Original parsed problem data.
            
        Returns:
            OrchestratorResult with new solution.
        """
        # Update parsed problem with correction
        corrected_parsed = original_parsed.copy()
        corrected_parsed["problem_text"] = corrected_text
        
        # Re-run from routing stage
        return self._solve_from_routing(corrected_parsed)
    
    def _solve_from_routing(self, parsed_problem: Dict) -> OrchestratorResult:
        """Continue solving from routing stage.
        
        Args:
            parsed_problem: Parsed problem data.
            
        Returns:
            OrchestratorResult.
        """
        start_time = time.time()
        self.traces = []
        
        # Route
        route_result = self.router.execute(parsed_problem)
        if route_result.trace:
            self.traces.append(route_result.trace)
        
        routing = route_result.data
        
        # Solve
        solver_input = {**parsed_problem, **routing}
        solve_result = self.solver.execute(solver_input)
        if solve_result.trace:
            self.traces.append(solve_result.trace)
        
        if not solve_result.success:
            return self._create_error_result(
                "Failed to solve",
                solve_result,
                time.time() - start_time
            )
        
        solution = solve_result.data
        
        # Verify
        verify_result = self.verifier.execute({
            "problem_text": parsed_problem.get("problem_text", ""),
            "solution": solution
        })
        if verify_result.trace:
            self.traces.append(verify_result.trace)
        
        verification = verify_result.data
        
        # Explain
        explain_result = self.explainer.execute({
            "problem_text": parsed_problem.get("problem_text", ""),
            "solution": solution,
            "verification": verification,
            "topic": parsed_problem.get("topic", ""),
            "subtopic": parsed_problem.get("subtopic", "")
        })
        if explain_result.trace:
            self.traces.append(explain_result.trace)
        
        explanation_data = explain_result.data
        
        return OrchestratorResult(
            success=True,
            final_answer=solution.get("final_answer", ""),
            explanation=explanation_data.get("formatted", {}),
            explanation_markdown=explanation_data.get("markdown", ""),
            confidence=verification.get("combined_confidence", 0.8),
            needs_hitl=verify_result.needs_hitl,
            hitl_reason=verify_result.hitl_reason,
            traces=self.traces,
            retrieved_sources=solution.get("retrieved_sources", []),
            parsed_problem=parsed_problem,
            solution=solution,
            verification=verification,
            total_time_ms=(time.time() - start_time) * 1000
        )
    
    def _create_error_result(
        self,
        message: str,
        result: AgentResponse,
        elapsed: float
    ) -> OrchestratorResult:
        """Create an error result."""
        return OrchestratorResult(
            success=False,
            final_answer="",
            explanation=message,
            explanation_markdown=f"# Error\n\n{message}\n\n{result.message}",
            confidence=0.0,
            needs_hitl=True,
            hitl_reason=message,
            traces=self.traces,
            retrieved_sources=[],
            parsed_problem=result.data,
            solution={},
            verification={},
            total_time_ms=elapsed * 1000
        )
    
    def _create_hitl_result(
        self,
        reason: str,
        parsed: Dict,
        elapsed: float
    ) -> OrchestratorResult:
        """Create a HITL-triggered result at parse stage."""
        return OrchestratorResult(
            success=True,
            final_answer="",
            explanation="",
            explanation_markdown="",
            confidence=parsed.get("confidence", 0.5),
            needs_hitl=True,
            hitl_reason=reason,
            traces=self.traces,
            retrieved_sources=[],
            parsed_problem=parsed,
            solution={},
            verification={},
            total_time_ms=elapsed * 1000
        )
    
    def _create_verification_hitl_result(
        self,
        reason: str,
        parsed: Dict,
        solution: Dict,
        verification: Dict,
        elapsed: float
    ) -> OrchestratorResult:
        """Create a HITL-triggered result at verification stage."""
        return OrchestratorResult(
            success=True,
            final_answer=solution.get("final_answer", ""),
            explanation="Solution requires review",
            explanation_markdown="# Solution Requires Review\n\nPlease verify the solution.",
            confidence=verification.get("combined_confidence", 0.5),
            needs_hitl=True,
            hitl_reason=reason,
            traces=self.traces,
            retrieved_sources=solution.get("retrieved_sources", []),
            parsed_problem=parsed,
            solution=solution,
            verification=verification,
            total_time_ms=elapsed * 1000
        )
    
    def get_trace_summary(self) -> List[Dict]:
        """Get summary of agent traces for UI display."""
        return [
            {
                "agent": t.agent_name,
                "action": t.action,
                "status": t.status,
                "duration": f"{t.duration_ms:.0f}ms",
                "summary": t.output_summary
            }
            for t in self.traces
        ]
