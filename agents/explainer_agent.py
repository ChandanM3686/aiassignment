"""
Explainer Agent - Generates step-by-step student-friendly explanations.
"""

import time
from typing import Any, Dict, List

from .base_agent import BaseAgent, AgentResponse


class ExplainerAgent(BaseAgent):
    """Agent that generates clear, student-friendly explanations."""
    
    def __init__(self):
        super().__init__(
            name="Explainer Agent",
            description="Generates step-by-step explanations for students"
        )
        
        self.system_instruction = """You are an expert math tutor creating explanations for JEE students.

Your explanations should:
1. Be clear and easy to follow
2. Explain the "why" behind each step, not just the "what"
3. Highlight key concepts and formulas used
4. Point out common mistakes to avoid
5. Use proper mathematical notation
6. Include helpful tips and shortcuts

Format your response as JSON:
{
    "title": "Brief title of the solution",
    "summary": "One sentence summary of the answer",
    "detailed_steps": [
        {
            "step_number": 1,
            "action": "What we're doing",
            "explanation": "Why we're doing it",
            "calculation": "The math work",
            "result": "What we got"
        }
    ],
    "final_answer": "The complete answer with units if applicable",
    "key_concepts": ["concept 1", "concept 2"],
    "formulas_applied": ["formula 1", "formula 2"],
    "tips": ["helpful tip 1", "helpful tip 2"],
    "common_mistakes": ["mistake to avoid"],
    "related_problems": ["type of similar problems this method applies to"]
}

Make the explanation engaging and educational!
"""
    
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Generate explanation for the solution.
        
        Args:
            input_data: Dict with problem, solution, and verification.
            
        Returns:
            AgentResponse with explanation.
        """
        start_time = time.time()
        
        problem_text = input_data.get("problem_text", "")
        solution = input_data.get("solution", {})
        verification = input_data.get("verification", {})
        topic = input_data.get("topic", "")
        subtopic = input_data.get("subtopic", "")
        
        # Build explanation prompt
        prompt = self._build_explanation_prompt(
            problem_text,
            solution,
            verification,
            topic,
            subtopic
        )
        
        try:
            response = self._call_llm(prompt, self.system_instruction)
            explanation = self._parse_explanation(response)
            
            if not explanation:
                # Create basic explanation from solution
                explanation = self._create_basic_explanation(solution)
            
            duration = (time.time() - start_time) * 1000
            
            # Format for display
            formatted_explanation = self._format_for_display(explanation)
            
            return AgentResponse(
                success=True,
                data={
                    "explanation": explanation,
                    "formatted": formatted_explanation,
                    "markdown": self._to_markdown(explanation),
                },
                message="Explanation generated",
                confidence=0.95,
                trace=self._create_trace(
                    "explain",
                    f"Topic: {topic}/{subtopic}",
                    f"Generated {len(explanation.get('detailed_steps', []))} step explanation",
                    duration_ms=duration
                )
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data={"error": str(e)},
                message=f"Explanation error: {str(e)}",
                trace=self._create_trace(
                    "explain",
                    problem_text[:50],
                    f"Error: {str(e)}",
                    status="error"
                )
            )
    
    def _build_explanation_prompt(
        self,
        problem: str,
        solution: Dict,
        verification: Dict,
        topic: str,
        subtopic: str
    ) -> str:
        """Build the explanation prompt.
        
        Args:
            problem: Original problem.
            solution: Solution dict.
            verification: Verification results.
            topic: Math topic.
            subtopic: Specific subtopic.
            
        Returns:
            Complete prompt string.
        """
        solution_steps = solution.get("solution_steps", [])
        steps_text = "\n".join([
            f"Step {s.get('step', i+1)}: {s.get('description', '')} = {s.get('calculation', '')}"
            for i, s in enumerate(solution_steps)
        ])
        
        return f"""# Math Problem
{problem}

# Topic: {topic} / {subtopic}

# Solution Steps
{steps_text}

# Final Answer
{solution.get('final_answer', 'N/A')}

# Formulas Used
{', '.join(solution.get('formulas_used', []))}

Please create a detailed, student-friendly explanation of this solution. 
Make it educational and engaging for JEE preparation."""
    
    def _parse_explanation(self, response: str) -> Dict:
        """Parse explanation response.
        
        Args:
            response: Raw LLM response.
            
        Returns:
            Parsed explanation dict.
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
        
        return None
    
    def _create_basic_explanation(self, solution: Dict) -> Dict:
        """Create basic explanation from solution.
        
        Args:
            solution: Solution dict.
            
        Returns:
            Basic explanation dict.
        """
        steps = solution.get("solution_steps", [])
        
        return {
            "title": "Solution",
            "summary": f"The answer is {solution.get('final_answer', 'N/A')}",
            "detailed_steps": [
                {
                    "step_number": s.get("step", i + 1),
                    "action": s.get("description", ""),
                    "explanation": "",
                    "calculation": s.get("calculation", ""),
                    "result": ""
                }
                for i, s in enumerate(steps)
            ],
            "final_answer": solution.get("final_answer", ""),
            "key_concepts": [],
            "formulas_applied": solution.get("formulas_used", []),
            "tips": [],
            "common_mistakes": [],
            "related_problems": []
        }
    
    def _format_for_display(self, explanation: Dict) -> Dict:
        """Format explanation for UI display.
        
        Args:
            explanation: Raw explanation dict.
            
        Returns:
            Formatted for display.
        """
        return {
            "title": explanation.get("title", "Solution"),
            "answer_box": explanation.get("final_answer", ""),
            "steps": [
                {
                    "number": s.get("step_number", i + 1),
                    "title": s.get("action", f"Step {i + 1}"),
                    "content": s.get("explanation", ""),
                    "math": s.get("calculation", ""),
                }
                for i, s in enumerate(explanation.get("detailed_steps", []))
            ],
            "concepts": explanation.get("key_concepts", []),
            "tips": explanation.get("tips", []),
            "warnings": explanation.get("common_mistakes", []),
        }
    
    def _to_markdown(self, explanation: Dict) -> str:
        """Convert explanation to markdown.
        
        Args:
            explanation: Explanation dict.
            
        Returns:
            Markdown string.
        """
        lines = [
            f"# {explanation.get('title', 'Solution')}",
            "",
            f"**Summary:** {explanation.get('summary', '')}",
            "",
            "## Solution Steps",
            ""
        ]
        
        for step in explanation.get("detailed_steps", []):
            lines.append(f"### Step {step.get('step_number', '')}: {step.get('action', '')}")
            if step.get("explanation"):
                lines.append(f"\n{step['explanation']}")
            if step.get("calculation"):
                lines.append(f"\n$$\n{step['calculation']}\n$$")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            f"## Final Answer",
            f"**{explanation.get('final_answer', '')}**",
            ""
        ])
        
        if explanation.get("key_concepts"):
            lines.append("## Key Concepts")
            for concept in explanation["key_concepts"]:
                lines.append(f"- {concept}")
            lines.append("")
        
        if explanation.get("tips"):
            lines.append("## 💡 Tips")
            for tip in explanation["tips"]:
                lines.append(f"- {tip}")
            lines.append("")
        
        if explanation.get("common_mistakes"):
            lines.append("## ⚠️ Common Mistakes to Avoid")
            for mistake in explanation["common_mistakes"]:
                lines.append(f"- {mistake}")
        
        return "\n".join(lines)
