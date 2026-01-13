"""
Router Agent - Classifies problems and routes to appropriate workflow.
"""

import time
from typing import Any, Dict

from .base_agent import BaseAgent, AgentResponse


class RouterAgent(BaseAgent):
    """Agent that routes problems to appropriate solving strategies."""
    
    def __init__(self):
        super().__init__(
            name="Intent Router Agent",
            description="Classifies problem type and routes to optimal solving workflow"
        )
        
        # Define routing strategies for different problem types
        self.routing_strategies = {
            "algebra": {
                "quadratic_equations": "algebraic_solver",
                "polynomials": "algebraic_solver",
                "inequalities": "algebraic_solver",
                "progressions": "formula_based_solver",
                "logarithms": "algebraic_solver",
            },
            "probability": {
                "basic_probability": "probability_solver",
                "permutations_combinations": "combinatorics_solver",
                "distributions": "probability_solver",
            },
            "calculus": {
                "limits": "calculus_solver",
                "derivatives": "calculus_solver",
                "applications": "optimization_solver",
                "integration": "calculus_solver",
            },
            "linear_algebra": {
                "matrices": "matrix_solver",
                "determinants": "matrix_solver",
                "vectors": "vector_solver",
            },
        }
        
        # Tools needed for each strategy
        self.strategy_tools = {
            "algebraic_solver": ["sympy", "quadratic_formula", "factoring"],
            "formula_based_solver": ["formula_lookup", "calculator"],
            "probability_solver": ["probability_rules", "calculator"],
            "combinatorics_solver": ["factorial", "combinations", "permutations"],
            "calculus_solver": ["sympy", "differentiation", "integration"],
            "optimization_solver": ["sympy", "critical_points", "second_derivative_test"],
            "matrix_solver": ["numpy", "matrix_operations"],
            "vector_solver": ["numpy", "vector_operations"],
        }
    
    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Route the problem to appropriate solver.
        
        Args:
            input_data: Parsed problem data from ParserAgent.
            
        Returns:
            AgentResponse with routing decision.
        """
        start_time = time.time()
        
        topic = input_data.get("topic", "general")
        subtopic = input_data.get("subtopic", "")
        problem_text = input_data.get("problem_text", "")
        
        # Determine strategy
        strategy = self._determine_strategy(topic, subtopic, problem_text)
        tools = self.strategy_tools.get(strategy, ["calculator"])
        
        # Determine complexity
        complexity = self._assess_complexity(problem_text)
        
        # Check if we need additional context
        needs_rag = self._needs_rag_context(topic, subtopic, complexity)
        
        duration = (time.time() - start_time) * 1000
        
        routing_decision = {
            "strategy": strategy,
            "tools": tools,
            "complexity": complexity,
            "needs_rag": needs_rag,
            "rag_query": self._build_rag_query(topic, subtopic, problem_text) if needs_rag else None,
            "topic": topic,
            "subtopic": subtopic,
        }
        
        return AgentResponse(
            success=True,
            data=routing_decision,
            message=f"Routed to {strategy} with complexity {complexity}",
            confidence=0.95,
            trace=self._create_trace(
                "route",
                f"Topic: {topic}/{subtopic}",
                f"Strategy: {strategy}, Tools: {len(tools)}, RAG: {needs_rag}",
                duration_ms=duration
            )
        )
    
    def _determine_strategy(self, topic: str, subtopic: str, problem_text: str) -> str:
        """Determine the solving strategy.
        
        Args:
            topic: Main topic.
            subtopic: Specific subtopic.
            problem_text: The problem text.
            
        Returns:
            Strategy name.
        """
        # Try to get from mapping
        if topic in self.routing_strategies:
            if subtopic in self.routing_strategies[topic]:
                return self.routing_strategies[topic][subtopic]
        
        # Default strategies based on topic
        defaults = {
            "algebra": "algebraic_solver",
            "probability": "probability_solver",
            "calculus": "calculus_solver",
            "linear_algebra": "matrix_solver",
        }
        
        return defaults.get(topic, "general_solver")
    
    def _assess_complexity(self, problem_text: str) -> str:
        """Assess problem complexity.
        
        Args:
            problem_text: The problem text.
            
        Returns:
            Complexity level: 'basic', 'intermediate', or 'advanced'.
        """
        text_lower = problem_text.lower()
        
        # Advanced indicators
        advanced_keywords = [
            "prove", "derive", "show that", "if and only if",
            "eigenvalue", "eigenvector", "taylor series",
            "multiple variables", "partial derivative", "triple integral",
            "optimization with constraints"
        ]
        
        # Intermediate indicators
        intermediate_keywords = [
            "implicit", "parametric", "integration by parts",
            "bayes", "conditional probability",
            "system of equations", "determinant",
            "chain rule", "quotient rule"
        ]
        
        if any(kw in text_lower for kw in advanced_keywords):
            return "advanced"
        elif any(kw in text_lower for kw in intermediate_keywords):
            return "intermediate"
        else:
            return "basic"
    
    def _needs_rag_context(self, topic: str, subtopic: str, complexity: str) -> bool:
        """Determine if RAG context is needed.
        
        Args:
            topic: Main topic.
            subtopic: Subtopic.
            complexity: Complexity level.
            
        Returns:
            True if RAG should be used.
        """
        # Always use RAG for intermediate and advanced problems
        if complexity in ["intermediate", "advanced"]:
            return True
        
        # Use RAG for certain topics that benefit from formulas
        formula_heavy_topics = ["probability", "calculus", "linear_algebra"]
        if topic in formula_heavy_topics:
            return True
        
        return False
    
    def _build_rag_query(self, topic: str, subtopic: str, problem_text: str) -> str:
        """Build a query for RAG retrieval.
        
        Args:
            topic: Main topic.
            subtopic: Subtopic.
            problem_text: Problem text.
            
        Returns:
            RAG query string.
        """
        # Combine topic info with problem for targeted retrieval
        query_parts = []
        
        if topic:
            query_parts.append(topic)
        if subtopic:
            query_parts.append(subtopic)
        
        # Extract key mathematical terms from problem
        query_parts.append(problem_text[:200])  # Limit length
        
        return " ".join(query_parts)
