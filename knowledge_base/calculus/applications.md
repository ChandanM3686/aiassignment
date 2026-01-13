# Applications of Derivatives

## Increasing/Decreasing Functions
- f is **increasing** on interval I if f'(x) > 0 for all x in I
- f is **decreasing** on interval I if f'(x) < 0 for all x in I

## Critical Points
x = c is a critical point if:
- f'(c) = 0, or
- f'(c) does not exist

## First Derivative Test
At a critical point c:
- If f' changes from + to -: **local maximum**
- If f' changes from - to +: **local minimum**
- If f' doesn't change sign: **neither**

## Second Derivative Test
At a critical point c where f'(c) = 0:
- If f''(c) > 0: **local minimum** (concave up)
- If f''(c) < 0: **local maximum** (concave down)
- If f''(c) = 0: **test is inconclusive**

## Concavity and Inflection Points
- f is **concave up** if f''(x) > 0 (curves upward, like a cup)
- f is **concave down** if f''(x) < 0 (curves downward)
- **Inflection point**: where concavity changes (f'' = 0 and changes sign)

## Optimization Problems
### Steps to Solve
1. Draw diagram and identify variables
2. Write function to optimize in terms of one variable
3. Find domain (constraints on variable)
4. Find critical points (set derivative = 0)
5. Test critical points and endpoints
6. Verify using first or second derivative test

### Common Constraints
- Perimeter fixed: 2l + 2w = P
- Area fixed: l × w = A
- Volume fixed: l × w × h = V

## Maxima and Minima
### Absolute (Global) Extrema
To find absolute max/min on closed interval [a, b]:
1. Find all critical points in (a, b)
2. Evaluate f at critical points and endpoints
3. Largest value = absolute maximum
4. Smallest value = absolute minimum

### Extreme Value Theorem
A continuous function on [a, b] attains both an absolute maximum and absolute minimum.

## Related Rates
### Steps
1. Identify all quantities that change with time
2. Find equation relating these quantities
3. Differentiate implicitly with respect to time t
4. Substitute known values
5. Solve for desired rate

### Common Related Rates Problems
- Expanding/contracting shapes
- Ladder sliding down wall
- Shadow length problems
- Filling/draining containers

## Mean Value Theorem
If f is continuous on [a, b] and differentiable on (a, b), there exists c in (a, b) such that:
$$f'(c) = \frac{f(b) - f(a)}{b - a}$$

## Rolle's Theorem
Special case of MVT: If f(a) = f(b), then there exists c where f'(c) = 0.
