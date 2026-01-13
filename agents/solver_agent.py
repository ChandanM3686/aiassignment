"""
Solver Agent - Solves math problems using RAG and tools.
"""

import time
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent, AgentResponse
from rag.retriever import Retriever, RetrievedContext
from utils.math_tools import MathCalculator, SymbolicSolver


class SolverAgent(BaseAgent):
    """Agent that solves math problems using RAG context and mathematical tools."""
    
    def __init__(self):
        super().__init__(
            name="Solver Agent",
            description="Solves math problems using RAG-enhanced reasoning and tools"
        )
        
        self.retriever = Retriever()
        self.calculator = MathCalculator()
        self.symbolic_solver = SymbolicSolver()
        
        self.system_instruction = """You are an expert math tutor solving JEE-level problems. 

Given:
1. A structured math problem
2. Relevant knowledge base context
3. A solving strategy

Your job is to:
1. Analyze the problem carefully
2. Apply relevant formulas and methods from the context
3. Solve step by step
4. Provide the final answer

IMPORTANT RULES:
- Show all steps clearly
- Use only formulas that appear in the provided context (no hallucination)
- If you're uncertain about a step, note it
- Express confidence in your solution (0.0 to 1.0)

Respond in this JSON format:
{
    "solution_steps": [
        {"step": 1, "description": "...", "calculation": "..."},
        {"step": 2, "description": "...", "calculation": "..."}
    ],
    "final_answer": "...",
    "formulas_used": ["formula 1", "formula 2"],
    "confidence": 0.9,
    "notes": "any important observations"
}
"""
    
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Solve the math problem.
        
        Args:
            input_data: Dict with parsed problem and routing info.
            
        Returns:
            AgentResponse with solution.
        """
        start_time = time.time()
        
        problem_text = input_data.get("problem_text", "")
        topic = input_data.get("topic", "general")
        subtopic = input_data.get("subtopic", "")
        needs_rag = input_data.get("needs_rag", True)
        rag_query = input_data.get("rag_query", problem_text)
        tools = input_data.get("tools", [])
        
        # Retrieve context if needed
        retrieved_contexts: List[RetrievedContext] = []
        context_str = ""
        
        if needs_rag:
            retrieved_contexts = self.retriever.retrieve_with_fallback(
                rag_query,
                topic=topic
            )
            context_str = self.retriever.format_context_for_prompt(retrieved_contexts)
        
        # Try symbolic solving first for certain problem types
        symbolic_result = None
        if "sympy" in tools:
            symbolic_result = self._try_symbolic_solve(problem_text)
        
        # Build prompt
        prompt = self._build_solver_prompt(
            problem_text,
            context_str,
            tools,
            symbolic_result
        )
        
        try:
            # Call LLM for solution
            response = self._call_llm(prompt, self.system_instruction)
            
            # Parse solution
            solution = self._parse_solution(response)
            
            if not solution:
                return AgentResponse(
                    success=False,
                    data={"problem": problem_text},
                    message="Failed to generate solution",
                    trace=self._create_trace(
                        "solve",
                        problem_text[:50],
                        "Solution generation failed",
                        status="error"
                    )
                )
            
            duration = (time.time() - start_time) * 1000
            
            # Add retrieved sources to solution
            solution["retrieved_sources"] = self.retriever.get_sources_summary(retrieved_contexts)
            solution["symbolic_verification"] = symbolic_result
            
            return AgentResponse(
                success=True,
                data=solution,
                message=f"Solved with {len(solution.get('solution_steps', []))} steps",
                confidence=solution.get("confidence", 0.8),
                trace=self._create_trace(
                    "solve",
                    problem_text[:50],
                    f"Answer: {solution.get('final_answer', 'N/A')[:50]}",
                    duration_ms=duration
                )
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={"error": str(e)},
                message=f"Solver error: {str(e)}",
                trace=self._create_trace(
                    "solve",
                    problem_text[:50],
                    f"Error: {str(e)}",
                    status="error"
                )
            )
    
    def _build_solver_prompt(
        self,
        problem: str,
        context: str,
        tools: List[str],
        symbolic_result: Optional[Dict]
    ) -> str:
        """Build the solver prompt.
        
        Args:
            problem: Problem text.
            context: RAG context.
            tools: Available tools.
            symbolic_result: Result from symbolic solver if available.
            
        Returns:
            Complete prompt string.
        """
        prompt_parts = [
            "# Math Problem to Solve\n",
            f"{problem}\n\n",
        ]
        
        if context:
            prompt_parts.append("# Retrieved Knowledge Base Context\n")
            prompt_parts.append(f"{context}\n\n")
        
        if tools:
            prompt_parts.append("# Available Tools\n")
            prompt_parts.append(f"{', '.join(tools)}\n\n")
        
        if symbolic_result:
            prompt_parts.append("# Symbolic Computation Result (for verification)\n")
            prompt_parts.append(f"{symbolic_result}\n\n")
        
        prompt_parts.append("Solve this problem step by step using the provided context.")
        
        return "".join(prompt_parts)
    
    def _try_symbolic_solve(self, problem: str) -> Optional[Dict]:
        """Attempt to solve symbolically using SymPy.
        
        Args:
            problem: Problem text.
            
        Returns:
            Symbolic result or None.
        """
        try:
            # Try to extract and solve equation
            result = self.symbolic_solver.solve_equation(problem)
            if result:
                return {"symbolic_solution": str(result)}
        except Exception:
            pass
        
        return None
    
    def _parse_solution(self, response: str) -> Optional[Dict]:
        """Parse LLM response into solution dict.
        
        Args:
            response: Raw LLM response.
            
        Returns:
            Parsed solution dict or None.
        """
        import json
        import re
        
        try:
            # Try direct JSON parse
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Fallback: Create solution from raw text
        return {
            "solution_steps": [{"step": 1, "description": "Solution", "calculation": response}],
            "final_answer": self._extract_answer(response),
            "formulas_used": [],
            "confidence": 0.7,
            "notes": "Parsed from unstructured response"
        }
    
    def _extract_answer(self, text: str) -> str:
        """Extract answer from unstructured text.
        
        Args:
            text: Solution text.
            
        Returns:
            Extracted answer string.
        """
        import re
        
        # Look for common answer patterns
        patterns = [
            r'(?:answer|result|solution)\s*[:=]\s*(.+?)(?:\n|$)',
            r'(?:x|y|z)\s*=\s*(.+?)(?:\n|$)',
            r'(?:therefore|thus|hence)\s*[:,]?\s*(.+?)(?:\n|$)',
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()
        
        # Return last line as fallback
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return lines[-1] if lines else ""
