"""
Verifier Agent - Verifies solution correctness and triggers HITL if needed.
"""

import time
from typing import Any, Dict

from .base_agent import BaseAgent, AgentResponse


class VerifierAgent(BaseAgent):
    """Agent that verifies solution correctness and quality."""
    
    def __init__(self):
        super().__init__(
            name="Verifier Agent",
            description="Verifies solution correctness, checks edge cases, and triggers HITL"
        )
        
        self.confidence_threshold = self.settings.verifier_confidence_threshold
        
        self.system_instruction = """You are a meticulous math solution verifier. Your job is to:

1. Check mathematical correctness of each step
2. Verify the final answer
3. Check for edge cases and domain restrictions
4. Identify any logical errors or missing steps
5. Verify that formulas were applied correctly

Respond in this JSON format:
{
    "is_correct": true/false,
    "verification_steps": [
        {"check": "step 1 verification", "passed": true/false, "note": "..."},
        {"check": "final answer check", "passed": true/false, "note": "..."}
    ],
    "errors_found": ["list of errors if any"],
    "edge_cases_checked": ["what edge cases were verified"],
    "confidence": 0.0-1.0,
    "suggestions": ["improvements if any"],
    "needs_human_review": true/false,
    "review_reason": "why human review is needed (if applicable)"
}
"""
    
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Verify the solution.
        
        Args:
            input_data: Dict with problem and solution.
            
        Returns:
            AgentResponse with verification results.
        """
        start_time = time.time()
        
        problem_text = input_data.get("problem_text", "")
        solution = input_data.get("solution", {})
        solution_steps = solution.get("solution_steps", [])
        final_answer = solution.get("final_answer", "")
        solver_confidence = solution.get("confidence", 0.5)
        
        # Build verification prompt
        prompt = self._build_verification_prompt(
            problem_text,
            solution_steps,
            final_answer
        )
        
        try:
            response = self._call_llm(prompt, self.system_instruction)
            verification = self._parse_verification(response)
            
            if not verification:
                # Default to uncertain if parsing fails
                verification = {
                    "is_correct": None,
                    "verification_steps": [],
                    "errors_found": [],
                    "edge_cases_checked": [],
                    "confidence": 0.5,
                    "suggestions": [],
                    "needs_human_review": True,
                    "review_reason": "Could not complete automated verification"
                }
            
            duration = (time.time() - start_time) * 1000
            
            # Combine solver and verifier confidence
            combined_confidence = (solver_confidence + verification.get("confidence", 0.5)) / 2
            
            # Determine if HITL needed
            needs_hitl = (
                verification.get("needs_human_review", False) or
                combined_confidence < self.confidence_threshold or
                not verification.get("is_correct", True) or
                len(verification.get("errors_found", [])) > 0
            )
            
            hitl_reason = ""
            if needs_hitl:
                if verification.get("errors_found"):
                    hitl_reason = f"Errors found: {', '.join(verification['errors_found'][:3])}"
                elif verification.get("review_reason"):
                    hitl_reason = verification["review_reason"]
                elif combined_confidence < self.confidence_threshold:
                    hitl_reason = f"Low confidence ({combined_confidence:.2f})"
            
            return AgentResponse(
                success=True,
                data={
                    "verification": verification,
                    "is_correct": verification.get("is_correct", False),
                    "combined_confidence": combined_confidence,
                },
                message="Verified" if verification.get("is_correct") else "Issues found",
                needs_hitl=needs_hitl,
                hitl_reason=hitl_reason,
                confidence=combined_confidence,
                trace=self._create_trace(
                    "verify",
                    f"Answer: {final_answer[:30]}",
                    f"Correct: {verification.get('is_correct')}, Confidence: {combined_confidence:.2f}",
                    duration_ms=duration,
                    status="hitl_triggered" if needs_hitl else "success"
                )
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={"error": str(e)},
                message=f"Verification error: {str(e)}",
                needs_hitl=True,
                hitl_reason="Verification process failed",
                trace=self._create_trace(
                    "verify",
                    final_answer[:30],
                    f"Error: {str(e)}",
                    status="error"
                )
            )
    
    def _build_verification_prompt(
        self,
        problem: str,
        steps: list,
        answer: str
    ) -> str:
        """Build the verification prompt.
        
        Args:
            problem: Original problem.
            steps: Solution steps.
            answer: Final answer.
            
        Returns:
            Complete prompt string.
        """
        steps_text = "\n".join([
            f"Step {s.get('step', i+1)}: {s.get('description', '')} - {s.get('calculation', '')}"
            for i, s in enumerate(steps)
        ])
        
        return f"""# Problem
{problem}

# Solution Steps
{steps_text}

# Final Answer
{answer}

Please verify this solution thoroughly. Check each step, the final answer, and consider edge cases or domain restrictions."""
    
    def _parse_verification(self, response: str) -> Dict:
        """Parse verification response.
        
        Args:
            response: Raw LLM response.
            
        Returns:
            Parsed verification dict.
        """
        import json
        import re
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Parse from text if JSON fails
        return self._parse_verification_text(response)
    
    def _parse_verification_text(self, text: str) -> Dict:
        """Parse verification from unstructured text.
        
        Args:
            text: Raw text response.
            
        Returns:
            Parsed verification dict.
        """
        text_lower = text.lower()
        
        # Determine if correct
        is_correct = not any(word in text_lower for word in 
                           ["incorrect", "wrong", "error", "mistake", "false"])
        
        # Extract confidence
        import re
        conf_match = re.search(r'confidence[:\s]+(\d+\.?\d*)', text_lower)
        confidence = float(conf_match.group(1)) if conf_match else 0.7
        if confidence > 1:
            confidence = confidence / 100
        
        return {
            "is_correct": is_correct,
            "verification_steps": [],
            "errors_found": [],
            "edge_cases_checked": [],
            "confidence": confidence,
            "suggestions": [],
            "needs_human_review": not is_correct,
            "review_reason": "Parsed from unstructured response"
        }
