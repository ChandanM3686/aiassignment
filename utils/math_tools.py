"""
Math Tools - Calculator and symbolic solver utilities.
"""

from typing import Any, Dict, List, Optional, Union
import re


class MathCalculator:
    """Safe calculator for mathematical expressions."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.allowed_names = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'pow': pow,
        }
        
        # Import math functions
        import math
        self.allowed_names.update({
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
            'ceil': math.ceil,
            'floor': math.floor,
            'factorial': math.factorial,
        })
    
    def evaluate(self, expression: str) -> Optional[float]:
        """Safely evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression string.
            
        Returns:
            Result or None if evaluation fails.
        """
        try:
            # Clean expression
            expr = self._clean_expression(expression)
            
            # Compile expression
            code = compile(expr, "<string>", "eval")
            
            # Check for disallowed operations
            for name in code.co_names:
                if name not in self.allowed_names:
                    return None
            
            # Evaluate
            result = eval(code, {"__builtins__": {}}, self.allowed_names)
            
            return float(result)
            
        except Exception:
            return None
    
    def _clean_expression(self, expr: str) -> str:
        """Clean expression for evaluation.
        
        Args:
            expr: Raw expression.
            
        Returns:
            Cleaned expression.
        """
        # Replace common notations
        expr = expr.replace('^', '**')
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('√', 'sqrt')
        
        # Handle implicit multiplication
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        
        return expr
    
    def factorial(self, n: int) -> int:
        """Calculate factorial.
        
        Args:
            n: Non-negative integer.
            
        Returns:
            n!
        """
        import math
        return math.factorial(n)
    
    def combination(self, n: int, r: int) -> int:
        """Calculate combination nCr.
        
        Args:
            n: Total items.
            r: Items to choose.
            
        Returns:
            nCr value.
        """
        import math
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
    
    def permutation(self, n: int, r: int) -> int:
        """Calculate permutation nPr.
        
        Args:
            n: Total items.
            r: Items to arrange.
            
        Returns:
            nPr value.
        """
        import math
        return math.factorial(n) // math.factorial(n - r)


class SymbolicSolver:
    """Symbolic math solver using SymPy."""
    
    def __init__(self):
        """Initialize the solver."""
        self._sympy = None
    
    @property
    def sympy(self):
        """Lazy load sympy."""
        if self._sympy is None:
            import sympy
            self._sympy = sympy
        return self._sympy
    
    def solve_equation(self, equation_str: str) -> Optional[List]:
        """Solve an equation symbolically.
        
        Args:
            equation_str: Equation string (e.g., "x^2 - 4 = 0").
            
        Returns:
            List of solutions or None.
        """
        try:
            # Parse equation
            equation = self._parse_equation(equation_str)
            if equation is None:
                return None
            
            # Identify variable
            symbols = equation.free_symbols
            if len(symbols) != 1:
                return None
            
            var = list(symbols)[0]
            
            # Solve
            solutions = self.sympy.solve(equation, var)
            
            return [str(sol) for sol in solutions]
            
        except Exception:
            return None
    
    def differentiate(self, expr_str: str, var: str = 'x') -> Optional[str]:
        """Differentiate an expression.
        
        Args:
            expr_str: Expression string.
            var: Variable to differentiate with respect to.
            
        Returns:
            Derivative as string or None.
        """
        try:
            x = self.sympy.Symbol(var)
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            derivative = self.sympy.diff(expr, x)
            return str(derivative)
        except Exception:
            return None
    
    def integrate(self, expr_str: str, var: str = 'x') -> Optional[str]:
        """Integrate an expression.
        
        Args:
            expr_str: Expression string.
            var: Variable to integrate with respect to.
            
        Returns:
            Integral as string or None.
        """
        try:
            x = self.sympy.Symbol(var)
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            integral = self.sympy.integrate(expr, x)
            return str(integral) + " + C"
        except Exception:
            return None
    
    def evaluate_limit(
        self,
        expr_str: str,
        var: str = 'x',
        point: str = '0'
    ) -> Optional[str]:
        """Evaluate a limit.
        
        Args:
            expr_str: Expression string.
            var: Variable.
            point: Point to evaluate limit at.
            
        Returns:
            Limit value as string or None.
        """
        try:
            x = self.sympy.Symbol(var)
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            
            # Handle infinity
            if point == 'infinity' or point == 'inf':
                point_val = self.sympy.oo
            elif point == '-infinity' or point == '-inf':
                point_val = -self.sympy.oo
            else:
                point_val = self.sympy.sympify(point)
            
            result = self.sympy.limit(expr, x, point_val)
            return str(result)
        except Exception:
            return None
    
    def simplify(self, expr_str: str) -> Optional[str]:
        """Simplify an expression.
        
        Args:
            expr_str: Expression string.
            
        Returns:
            Simplified expression or None.
        """
        try:
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            simplified = self.sympy.simplify(expr)
            return str(simplified)
        except Exception:
            return None
    
    def expand(self, expr_str: str) -> Optional[str]:
        """Expand an expression.
        
        Args:
            expr_str: Expression string.
            
        Returns:
            Expanded expression or None.
        """
        try:
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            expanded = self.sympy.expand(expr)
            return str(expanded)
        except Exception:
            return None
    
    def factor(self, expr_str: str) -> Optional[str]:
        """Factor an expression.
        
        Args:
            expr_str: Expression string.
            
        Returns:
            Factored expression or None.
        """
        try:
            expr = self.sympy.sympify(self._clean_expr(expr_str))
            factored = self.sympy.factor(expr)
            return str(factored)
        except Exception:
            return None
    
    def _parse_equation(self, eq_str: str):
        """Parse an equation string.
        
        Args:
            eq_str: Equation string.
            
        Returns:
            SymPy equation or None.
        """
        eq_str = self._clean_expr(eq_str)
        
        if '=' in eq_str:
            left, right = eq_str.split('=', 1)
            left_expr = self.sympy.sympify(left)
            right_expr = self.sympy.sympify(right)
            return left_expr - right_expr
        else:
            return self.sympy.sympify(eq_str)
    
    def _clean_expr(self, expr: str) -> str:
        """Clean expression for sympy.
        
        Args:
            expr: Raw expression.
            
        Returns:
            Cleaned expression.
        """
        expr = expr.replace('^', '**')
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        
        # Handle common functions
        expr = re.sub(r'sqrt\(', 'sqrt(', expr)
        expr = re.sub(r'sin\(', 'sin(', expr)
        expr = re.sub(r'cos\(', 'cos(', expr)
        expr = re.sub(r'tan\(', 'tan(', expr)
        expr = re.sub(r'log\(', 'log(', expr)
        expr = re.sub(r'ln\(', 'log(', expr)  # ln = natural log
        
        return expr.strip()
