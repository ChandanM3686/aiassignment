"""
Parser Agent - Converts raw input into structured math problems.
"""

import json
import time
from typing import Any, Dict, Optional
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentResponse


@dataclass
class ParsedProblem:
    """Structured representation of a math problem."""
    problem_text: str
    topic: str
    subtopic: str
    variables: list
    constraints: list
    needs_clarification: bool
    clarification_needed: str
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "problem_text": self.problem_text,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "variables": self.variables,
            "constraints": self.constraints,
            "needs_clarification": self.needs_clarification,
            "clarification_needed": self.clarification_needed,
            "confidence": self.confidence
        }


class ParserAgent(BaseAgent):
    """Agent that parses raw input into structured math problems."""
    
    def __init__(self):
        super().__init__(
            name="Parser Agent",
            description="Converts raw OCR/ASR/text input into structured math problems"
        )
        
        self.system_instruction = """You are a math problem parser. Your job is to:
1. Clean and correct any OCR or speech recognition errors in the input
2. Identify the mathematical topic and subtopic
3. Extract variables and constraints
4. Determine if any clarification is needed

Topics: algebra, probability, calculus, linear_algebra
Subtopics for algebra: quadratic_equations, polynomials, inequalities, progressions, logarithms
Subtopics for probability: basic_probability, permutations_combinations, distributions
Subtopics for calculus: limits, derivatives, applications, integration
Subtopics for linear_algebra: matrices, determinants, vectors

Respond ONLY with a valid JSON object in this exact format:
{
    "problem_text": "cleaned and corrected problem text",
    "topic": "main topic",
    "subtopic": "specific subtopic",
    "variables": ["x", "y"],
    "constraints": ["x > 0"],
    "needs_clarification": false,
    "clarification_needed": "",
    "confidence": 0.95
}

If the problem is ambiguous or unclear, set needs_clarification to true and explain what needs clarification.
"""
    
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Parse raw input into structured problem.
        
        Args:
            input_data: Dict with 'raw_text' and optional 'input_type', 'confidence'.
            
        Returns:
            AgentResponse with ParsedProblem in data.
        """
        start_time = time.time()
        
        raw_text = input_data.get("raw_text", "")
        input_type = input_data.get("input_type", "text")
        input_confidence = input_data.get("confidence", 1.0)
        
        if not raw_text:
            return AgentResponse(
                success=False,
                data={},
                message="No input text provided",
                trace=self._create_trace(
                    "parse",
                    "Empty input",
                    "Error: No input",
                    status="error"
                )
            )
        
        # Create prompt for parsing
        prompt = f"""Parse the following math problem:

Input Type: {input_type}
Input Confidence: {input_confidence}

Problem Text:
{raw_text}

Parse this into a structured format. Consider that if the input came from OCR or speech recognition, there may be errors that need correction."""
        
        try:
            response = self._call_llm(prompt, self.system_instruction)
            
            # Extract JSON from response
            parsed = self._extract_json(response)
            
            if not parsed:
                return AgentResponse(
                    success=False,
                    data={"raw_text": raw_text},
                    message="Failed to parse problem structure",
                    trace=self._create_trace(
                        "parse",
                        raw_text[:50] + "...",
                        "Parse failed",
                        duration_ms=(time.time() - start_time) * 1000,
                        status="error"
                    )
                )
            
            # Create ParsedProblem
            problem = ParsedProblem(
                problem_text=parsed.get("problem_text", raw_text),
                topic=parsed.get("topic", "general"),
                subtopic=parsed.get("subtopic", ""),
                variables=parsed.get("variables", []),
                constraints=parsed.get("constraints", []),
                needs_clarification=parsed.get("needs_clarification", False),
                clarification_needed=parsed.get("clarification_needed", ""),
                confidence=parsed.get("confidence", 0.8)
            )
            
            duration = (time.time() - start_time) * 1000
            
            # Determine if HITL is needed
            needs_hitl = problem.needs_clarification or problem.confidence < 0.6
            
            return AgentResponse(
                success=True,
                data=problem.to_dict(),
                message=f"Parsed as {problem.topic}/{problem.subtopic}",
                needs_hitl=needs_hitl,
                hitl_reason=problem.clarification_needed if needs_hitl else "",
                confidence=problem.confidence,
                trace=self._create_trace(
                    "parse",
                    raw_text[:50] + "..." if len(raw_text) > 50 else raw_text,
                    f"Topic: {problem.topic}, Confidence: {problem.confidence:.2f}",
                    duration_ms=duration,
                    status="hitl_triggered" if needs_hitl else "success"
                )
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={"raw_text": raw_text, "error": str(e)},
                message=f"Parser error: {str(e)}",
                trace=self._create_trace(
                    "parse",
                    raw_text[:50],
                    f"Error: {str(e)}",
                    duration_ms=(time.time() - start_time) * 1000,
                    status="error"
                )
            )
    
    def _extract_json(self, response: str) -> Optional[Dict]:
        """Extract JSON from LLM response.
        
        Args:
            response: Raw LLM response.
            
        Returns:
            Parsed JSON dict or None.
        """
        try:
            # Try direct parsing first
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in response
        import re
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return None
