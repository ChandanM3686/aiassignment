"""
Pattern Learner - Learn and apply patterns from solved problems.
"""

from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass

from .memory_store import MemoryStore


@dataclass
class SolutionPattern:
    """A learned solution pattern."""
    topic: str
    subtopic: str
    pattern_type: str  # 'formula', 'method', 'correction'
    pattern: str
    frequency: int
    success_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "subtopic": self.subtopic,
            "pattern_type": self.pattern_type,
            "pattern": self.pattern,
            "frequency": self.frequency,
            "success_rate": self.success_rate
        }


class PatternLearner:
    """Learn patterns from solved problems and corrections."""
    
    def __init__(self, memory_store: MemoryStore = None):
        """Initialize pattern learner.
        
        Args:
            memory_store: Optional MemoryStore instance.
        """
        self.memory_store = memory_store or MemoryStore()
        
        # Cached patterns
        self._formula_patterns: Dict[str, List[str]] = defaultdict(list)
        self._method_patterns: Dict[str, List[str]] = defaultdict(list)
        self._correction_patterns: Dict[str, str] = {}
    
    def learn_from_memory(self) -> None:
        """Learn patterns from stored problems."""
        correct_solutions = self.memory_store.get_correct_solutions(limit=200)
        
        for problem in correct_solutions:
            self._learn_from_problem(problem)
        
        # Load correction patterns
        self._correction_patterns = self.memory_store.get_corrections()
    
    def _learn_from_problem(self, problem) -> None:
        """Learn from a single problem.
        
        Args:
            problem: ProblemMemory instance.
        """
        key = f"{problem.topic}/{problem.subtopic}"
        
        # Extract formulas from solution
        formulas = self._extract_formulas(problem.solution)
        self._formula_patterns[key].extend(formulas)
        
        # Extract method patterns
        method = self._extract_method(problem.solution)
        if method:
            self._method_patterns[key].append(method)
    
    def _extract_formulas(self, solution: str) -> List[str]:
        """Extract formula patterns from solution.
        
        Args:
            solution: Solution text.
            
        Returns:
            List of formula strings.
        """
        import re
        
        formulas = []
        
        # Look for equations
        equation_pattern = r'[a-zA-Z]\s*=\s*[^,\n]+'
        matches = re.findall(equation_pattern, solution)
        formulas.extend(matches)
        
        # Look for mathematical expressions
        expr_pattern = r'\$\$?[^$]+\$\$?'
        matches = re.findall(expr_pattern, solution)
        formulas.extend(matches)
        
        return formulas
    
    def _extract_method(self, solution: str) -> Optional[str]:
        """Extract solving method from solution.
        
        Args:
            solution: Solution text.
            
        Returns:
            Method description or None.
        """
        solution_lower = solution.lower()
        
        # Common methods
        methods = [
            "quadratic formula",
            "factoring",
            "completing the square",
            "substitution",
            "integration by parts",
            "u-substitution",
            "chain rule",
            "product rule",
            "quotient rule",
            "l'hopital's rule",
            "bayes theorem",
            "binomial distribution",
            "matrix multiplication",
            "cramer's rule",
            "gaussian elimination"
        ]
        
        for method in methods:
            if method in solution_lower:
                return method
        
        return None
    
    def get_patterns_for_topic(
        self,
        topic: str,
        subtopic: str = None
    ) -> Dict[str, List[str]]:
        """Get learned patterns for a topic.
        
        Args:
            topic: Main topic.
            subtopic: Optional subtopic.
            
        Returns:
            Dict with 'formulas' and 'methods'.
        """
        key = f"{topic}/{subtopic}" if subtopic else topic
        
        # Get exact matches
        formulas = self._formula_patterns.get(key, [])
        methods = self._method_patterns.get(key, [])
        
        # Also get topic-level patterns if subtopic specified
        if subtopic:
            topic_key = f"{topic}/"
            for k, v in self._formula_patterns.items():
                if k.startswith(topic_key):
                    formulas.extend(v)
            for k, v in self._method_patterns.items():
                if k.startswith(topic_key):
                    methods.extend(v)
        
        # Get most common
        common_formulas = [f for f, _ in Counter(formulas).most_common(5)]
        common_methods = [m for m, _ in Counter(methods).most_common(3)]
        
        return {
            "formulas": common_formulas,
            "methods": common_methods
        }
    
    def apply_correction_patterns(
        self,
        text: str,
        pattern_type: str = None
    ) -> str:
        """Apply learned correction patterns to text.
        
        Args:
            text: Text to correct.
            pattern_type: Optional pattern type filter.
            
        Returns:
            Corrected text.
        """
        result = text
        
        for original, corrected in self._correction_patterns.items():
            if original in result:
                result = result.replace(original, corrected)
        
        return result
    
    def get_solution_hints(
        self,
        topic: str,
        subtopic: str,
        problem_text: str
    ) -> Dict[str, Any]:
        """Get hints for solving based on patterns.
        
        Args:
            topic: Problem topic.
            subtopic: Problem subtopic.
            problem_text: Problem text.
            
        Returns:
            Dict with hints and suggestions.
        """
        patterns = self.get_patterns_for_topic(topic, subtopic)
        
        hints = {
            "suggested_methods": patterns.get("methods", []),
            "relevant_formulas": patterns.get("formulas", []),
            "tips": []
        }
        
        # Add topic-specific tips
        topic_tips = self._get_topic_tips(topic, subtopic)
        hints["tips"] = topic_tips
        
        return hints
    
    def _get_topic_tips(self, topic: str, subtopic: str) -> List[str]:
        """Get tips for a topic.
        
        Args:
            topic: Main topic.
            subtopic: Subtopic.
            
        Returns:
            List of tip strings.
        """
        tips = {
            ("algebra", "quadratic_equations"): [
                "Check if the equation can be factored easily",
                "Calculate discriminant to determine nature of roots",
                "Remember to check for extraneous solutions"
            ],
            ("calculus", "limits"): [
                "Try direct substitution first",
                "Identify indeterminate forms",
                "Consider L'Hôpital's rule for 0/0 or ∞/∞"
            ],
            ("probability", "permutations_combinations"): [
                "Determine if order matters (permutation vs combination)",
                "Check for repetition constraints",
                "Draw a diagram for complex problems"
            ],
            ("linear_algebra", "matrices"): [
                "Check matrix dimensions for multiplication",
                "For inverse, verify det ≠ 0",
                "Use row reduction for systems"
            ]
        }
        
        return tips.get((topic, subtopic), [])
    
    def get_pattern_stats(self) -> Dict[str, Any]:
        """Get statistics about learned patterns.
        
        Returns:
            Dict with pattern statistics.
        """
        return {
            "topics_with_patterns": len(self._formula_patterns),
            "total_formulas": sum(len(v) for v in self._formula_patterns.values()),
            "total_methods": sum(len(v) for v in self._method_patterns.values()),
            "correction_patterns": len(self._correction_patterns)
        }
