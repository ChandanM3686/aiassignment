"""
Text Processing - Utilities for math text processing.
"""

import re
from typing import Dict, List


def normalize_math_text(text: str) -> str:
    """Normalize mathematical text for consistency.
    
    Args:
        text: Raw math text.
        
    Returns:
        Normalized text.
    """
    # Normalize operators
    text = text.replace('×', '*')
    text = text.replace('÷', '/')
    text = text.replace('−', '-')
    text = text.replace('—', '-')
    
    # Normalize exponents
    text = text.replace('²', '^2')
    text = text.replace('³', '^3')
    text = re.sub(r'(\d+)\s*\*\*\s*(\d+)', r'\1^\2', text)
    
    # Normalize spacing around operators
    text = re.sub(r'\s*([+\-*/^=<>])\s*', r' \1 ', text)
    
    # Clean up multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()


def latex_to_unicode(latex: str) -> str:
    """Convert LaTeX notation to Unicode.
    
    Args:
        latex: LaTeX string.
        
    Returns:
        Unicode string.
    """
    conversions = {
        r'\\alpha': 'α',
        r'\\beta': 'β',
        r'\\gamma': 'γ',
        r'\\delta': 'δ',
        r'\\epsilon': 'ε',
        r'\\theta': 'θ',
        r'\\lambda': 'λ',
        r'\\mu': 'μ',
        r'\\pi': 'π',
        r'\\sigma': 'σ',
        r'\\omega': 'ω',
        r'\\infty': '∞',
        r'\\pm': '±',
        r'\\leq': '≤',
        r'\\geq': '≥',
        r'\\neq': '≠',
        r'\\approx': '≈',
        r'\\times': '×',
        r'\\div': '÷',
        r'\\sqrt': '√',
        r'\\sum': 'Σ',
        r'\\prod': 'Π',
        r'\\int': '∫',
        r'\\partial': '∂',
        r'\\rightarrow': '→',
        r'\\leftarrow': '←',
        r'\\Rightarrow': '⇒',
        r'\\Leftarrow': '⇐',
        r'\\in': '∈',
        r'\\subset': '⊂',
        r'\\cup': '∪',
        r'\\cap': '∩',
        r'\\forall': '∀',
        r'\\exists': '∃',
    }
    
    result = latex
    for pattern, replacement in conversions.items():
        result = result.replace(pattern, replacement)
    
    # Remove remaining backslashes from commands
    result = re.sub(r'\\([a-zA-Z]+)', r'\1', result)
    
    return result


def unicode_to_latex(text: str) -> str:
    """Convert Unicode symbols to LaTeX.
    
    Args:
        text: Text with Unicode math symbols.
        
    Returns:
        LaTeX string.
    """
    conversions = {
        'α': r'\\alpha',
        'β': r'\\beta',
        'γ': r'\\gamma',
        'δ': r'\\delta',
        'ε': r'\\epsilon',
        'θ': r'\\theta',
        'λ': r'\\lambda',
        'μ': r'\\mu',
        'π': r'\\pi',
        'σ': r'\\sigma',
        'ω': r'\\omega',
        '∞': r'\\infty',
        '±': r'\\pm',
        '≤': r'\\leq',
        '≥': r'\\geq',
        '≠': r'\\neq',
        '≈': r'\\approx',
        '×': r'\\times',
        '÷': r'\\div',
        '√': r'\\sqrt',
        'Σ': r'\\sum',
        'Π': r'\\prod',
        '∫': r'\\int',
        '∂': r'\\partial',
        '→': r'\\rightarrow',
        '←': r'\\leftarrow',
        '⇒': r'\\Rightarrow',
        '⇐': r'\\Leftarrow',
        '∈': r'\\in',
        '⊂': r'\\subset',
        '∪': r'\\cup',
        '∩': r'\\cap',
        '∀': r'\\forall',
        '∃': r'\\exists',
    }
    
    result = text
    for symbol, latex in conversions.items():
        result = result.replace(symbol, latex)
    
    return result


def extract_variables(text: str) -> List[str]:
    """Extract variable names from mathematical text.
    
    Args:
        text: Mathematical text.
        
    Returns:
        List of unique variable names.
    """
    # Common single-letter variables
    common_vars = set('xyzabcnmhkpqrst')
    
    # Find standalone letters
    letters = re.findall(r'\b([a-zA-Z])\b', text)
    
    # Filter to likely variables
    variables = [l.lower() for l in letters if l.lower() in common_vars]
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for v in variables:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    
    return unique


def extract_numbers(text: str) -> List[float]:
    """Extract numbers from text.
    
    Args:
        text: Text containing numbers.
        
    Returns:
        List of numbers.
    """
    # Match integers and decimals
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    
    numbers = []
    for m in matches:
        try:
            numbers.append(float(m))
        except ValueError:
            pass
    
    return numbers


def format_answer(answer: str) -> str:
    """Format a mathematical answer for display.
    
    Args:
        answer: Raw answer string.
        
    Returns:
        Formatted answer.
    """
    # Clean up
    answer = answer.strip()
    
    # Format fractions nicely
    answer = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', answer)
    
    # Format square roots
    answer = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', answer)
    
    # Format exponents
    answer = re.sub(r'\^(\d+)', r'^{\1}', answer)
    answer = re.sub(r'\^([a-zA-Z])', r'^{\1}', answer)
    
    return answer


def split_into_steps(solution_text: str) -> List[Dict[str, str]]:
    """Split solution text into numbered steps.
    
    Args:
        solution_text: Full solution text.
        
    Returns:
        List of step dicts with 'number' and 'content'.
    """
    steps = []
    
    # Try to find numbered steps
    step_pattern = r'(?:Step\s*)?(\d+)[.):]\s*(.+?)(?=(?:Step\s*)?\d+[.):]|$)'
    matches = re.findall(step_pattern, solution_text, re.DOTALL | re.IGNORECASE)
    
    if matches:
        for num, content in matches:
            steps.append({
                'number': int(num),
                'content': content.strip()
            })
    else:
        # Fall back to splitting by newlines
        lines = [l.strip() for l in solution_text.split('\n') if l.strip()]
        for i, line in enumerate(lines, 1):
            steps.append({
                'number': i,
                'content': line
            })
    
    return steps


def clean_ocr_output(text: str) -> str:
    """Clean common OCR errors in mathematical text.
    
    Args:
        text: Raw OCR output.
        
    Returns:
        Cleaned text.
    """
    # Common OCR mistakes
    replacements = {
        'O': '0',  # Letter O to zero (in numeric contexts)
        'l': '1',  # Lowercase L to one (in numeric contexts)
        'I': '1',  # Capital I to one (in numeric contexts)
        'S': '5',  # S to 5 (sometimes)
        '|': '1',  # Pipe to one
        'xX': 'x',  # Double x
    }
    
    result = text
    
    # Only apply O/l/I replacements in numeric contexts
    result = re.sub(r'(?<=[0-9])O(?=[0-9])', '0', result)
    result = re.sub(r'(?<=[0-9])l(?=[0-9])', '1', result)
    result = re.sub(r'(?<=[0-9])I(?=[0-9])', '1', result)
    
    # Fix spacing issues
    result = ' '.join(result.split())
    
    return result
