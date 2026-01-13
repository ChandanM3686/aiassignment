"""
Text Handler for direct text input.
Preprocesses and normalizes math text input.
"""

from typing import Dict, Any
from dataclasses import dataclass
import re


@dataclass
class TextResult:
    """Result from text processing."""
    text: str
    original_text: str
    was_modified: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "original_text": self.original_text,
            "was_modified": self.was_modified
        }


class TextHandler:
    """Handles direct text input for math problems."""
    
    def __init__(self):
        """Initialize the text handler."""
        pass
    
    def process_text(self, text: str) -> TextResult:
        """Process and normalize text input.
        
        Args:
            text: Raw text input.
            
        Returns:
            TextResult with processed text.
        """
        original = text
        
        # Normalize whitespace
        processed = ' '.join(text.split())
        
        # Detect and convert LaTeX
        if self._contains_latex(processed):
            processed = self._normalize_latex(processed)
        
        # Normalize math expressions
        processed = self._normalize_math(processed)
        
        # Clean up
        processed = processed.strip()
        
        return TextResult(
            text=processed,
            original_text=original,
            was_modified=(processed != original)
        )
    
    def _contains_latex(self, text: str) -> bool:
        """Check if text contains LaTeX notation.
        
        Args:
            text: Text to check.
            
        Returns:
            True if LaTeX is detected.
        """
        latex_patterns = [
            r'\$.*\$',           # Inline math
            r'\\\(.*\\\)',       # Alternative inline
            r'\\\[.*\\\]',       # Display math
            r'\\frac',           # Fractions
            r'\\sqrt',           # Square root
            r'\\sum',            # Summation
            r'\\int',            # Integral
            r'\\lim',            # Limit
            r'\\begin\{',        # Environments
        ]
        return any(re.search(pattern, text) for pattern in latex_patterns)
    
    def _normalize_latex(self, text: str) -> str:
        """Convert LaTeX notation to readable format.
        
        Args:
            text: Text with LaTeX.
            
        Returns:
            Normalized text.
        """
        # Remove math delimiters
        text = re.sub(r'\$\$?', '', text)
        text = re.sub(r'\\\[|\\\]', '', text)
        text = re.sub(r'\\\(|\\\)', '', text)
        
        # Convert common LaTeX commands
        conversions = {
            r'\\frac\{([^}]+)\}\{([^}]+)\}': r'(\1)/(\2)',
            r'\\sqrt\{([^}]+)\}': r'sqrt(\1)',
            r'\\sqrt\[(\d+)\]\{([^}]+)\}': r'\1rt(\2)',
            r'\\sum_\{([^}]+)\}\^\{([^}]+)\}': r'sum from \1 to \2 of',
            r'\\int_\{([^}]+)\}\^\{([^}]+)\}': r'integral from \1 to \2 of',
            r'\\lim_\{([^}]+)\}': r'limit as \1 of',
            r'\\infty': '∞',
            r'\\pi': 'π',
            r'\\theta': 'θ',
            r'\\alpha': 'α',
            r'\\beta': 'β',
            r'\\gamma': 'γ',
            r'\\delta': 'δ',
            r'\\lambda': 'λ',
            r'\\mu': 'μ',
            r'\\sigma': 'σ',
            r'\\omega': 'ω',
            r'\\sin': 'sin',
            r'\\cos': 'cos',
            r'\\tan': 'tan',
            r'\\log': 'log',
            r'\\ln': 'ln',
            r'\\exp': 'exp',
            r'\^': '^',
            r'_': '_',
            r'\\cdot': '*',
            r'\\times': '*',
            r'\\div': '/',
            r'\\pm': '±',
            r'\\mp': '∓',
            r'\\leq': '≤',
            r'\\geq': '≥',
            r'\\neq': '≠',
            r'\\approx': '≈',
            r'\\rightarrow': '→',
            r'\\to': '→',
            r'\\in': '∈',
            r'\\subset': '⊂',
            r'\\cup': '∪',
            r'\\cap': '∩',
        }
        
        for pattern, replacement in conversions.items():
            text = re.sub(pattern, replacement, text)
        
        # Remove remaining backslashes
        text = re.sub(r'\\([a-zA-Z]+)', r'\1', text)
        
        # Clean up braces
        text = text.replace('{', '(').replace('}', ')')
        
        return text
    
    def _normalize_math(self, text: str) -> str:
        """Normalize math expressions for consistency.
        
        Args:
            text: Text with math expressions.
            
        Returns:
            Normalized text.
        """
        # Standardize operators
        text = text.replace('×', '*')
        text = text.replace('÷', '/')
        text = text.replace('−', '-')
        text = text.replace('—', '-')
        
        # Standardize exponents
        text = re.sub(r'(\d+)\s*\*\*\s*(\d+)', r'\1^\2', text)
        
        # Handle common Unicode math symbols
        unicode_to_text = {
            '²': '^2',
            '³': '^3',
            '⁴': '^4',
            '⁵': '^5',
            '⁶': '^6',
            '⁷': '^7',
            '⁸': '^8',
            '⁹': '^9',
            '√': 'sqrt',
            '∛': 'cbrt',
            '∜': '4rt',
            '½': '1/2',
            '⅓': '1/3',
            '¼': '1/4',
            '⅕': '1/5',
            '⅙': '1/6',
            '⅛': '1/8',
            '⅔': '2/3',
            '¾': '3/4',
            '⅖': '2/5',
            '⅗': '3/5',
            '⅘': '4/5',
            '⅚': '5/6',
            '⅝': '5/8',
            '⅞': '7/8',
        }
        
        for unicode_char, replacement in unicode_to_text.items():
            text = text.replace(unicode_char, replacement)
        
        # Normalize spacing around operators
        text = re.sub(r'\s*([+\-*/^=<>])\s*', r' \1 ', text)
        text = ' '.join(text.split())  # Clean up extra spaces
        
        return text
    
    def extract_variables(self, text: str) -> list:
        """Extract variable names from math text.
        
        Args:
            text: Math text.
            
        Returns:
            List of variable names.
        """
        # Common math variables
        common_vars = set('xyzabcnmhkpqrst')
        
        # Find single letter variables (not part of function names)
        words = re.findall(r'\b[a-zA-Z]\b', text.lower())
        
        # Filter to likely variables
        variables = [v for v in words if v in common_vars]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_vars = []
        for v in variables:
            if v not in seen:
                seen.add(v)
                unique_vars.append(v)
        
        return unique_vars
    
    def detect_problem_type(self, text: str) -> str:
        """Detect the type of math problem from text.
        
        Args:
            text: Math problem text.
            
        Returns:
            Problem type string.
        """
        text_lower = text.lower()
        
        # Keywords for different problem types
        type_keywords = {
            'derivative': ['derivative', 'differentiate', 'd/dx', 'dy/dx', "f'", "f''"],
            'integral': ['integral', 'integrate', '∫', 'antiderivative'],
            'limit': ['limit', 'lim', 'approaches', '→'],
            'equation': ['solve', 'find x', 'find y', 'roots', 'solutions', '= 0'],
            'quadratic': ['quadratic', 'x^2', 'x²', 'parabola'],
            'probability': ['probability', 'chance', 'likely', 'odds', 'dice', 'cards', 'coin'],
            'combination': ['combination', 'permutation', 'choose', 'arrange', 'ways'],
            'matrix': ['matrix', 'matrices', 'determinant', 'inverse'],
            'vector': ['vector', 'dot product', 'cross product', 'magnitude'],
            'optimization': ['maximum', 'minimum', 'optimize', 'max', 'min'],
        }
        
        for problem_type, keywords in type_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return problem_type
        
        return 'general'
