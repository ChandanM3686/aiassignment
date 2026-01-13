# Basic Integration

## Definition
If F'(x) = f(x), then F(x) is an **antiderivative** of f(x).

$$\int f(x) dx = F(x) + C$$

C = constant of integration

## Definite Integral
$$\int_a^b f(x) dx = F(b) - F(a)$$

where F'(x) = f(x) (Fundamental Theorem of Calculus)

## Basic Integration Formulas
| Function | Integral |
|----------|----------|
| xⁿ (n ≠ -1) | xⁿ⁺¹/(n+1) + C |
| 1/x | ln|x| + C |
| eˣ | eˣ + C |
| aˣ | aˣ/ln a + C |
| sin x | -cos x + C |
| cos x | sin x + C |
| sec² x | tan x + C |
| csc² x | -cot x + C |
| sec x tan x | sec x + C |
| csc x cot x | -csc x + C |
| 1/√(1-x²) | sin⁻¹ x + C |
| 1/(1+x²) | tan⁻¹ x + C |

## Integration Rules

### Constant Multiple
$$\int k \cdot f(x) dx = k \int f(x) dx$$

### Sum/Difference
$$\int [f(x) \pm g(x)] dx = \int f(x) dx \pm \int g(x) dx$$

## Substitution Method (u-substitution)
$$\int f(g(x)) \cdot g'(x) dx = \int f(u) du$$

where u = g(x)

### Steps
1. Choose u = g(x)
2. Find du = g'(x) dx
3. Substitute and simplify
4. Integrate
5. Substitute back

## Integration by Parts
$$\int u \, dv = uv - \int v \, du$$

### LIATE Rule (for choosing u)
**L**ogarithmic → **I**nverse trig → **A**lgebraic → **T**rigonometric → **E**xponential

## Properties of Definite Integrals
1. $$\int_a^a f(x) dx = 0$$
2. $$\int_a^b f(x) dx = -\int_b^a f(x) dx$$
3. $$\int_a^c f(x) dx = \int_a^b f(x) dx + \int_b^c f(x) dx$$
4. $$\int_a^b c \cdot f(x) dx = c \int_a^b f(x) dx$$

## Area Under Curve
$$\text{Area} = \int_a^b |f(x)| dx$$

## Special Integrals (JEE)
$$\int \frac{1}{x^2 + a^2} dx = \frac{1}{a} \tan^{-1}\left(\frac{x}{a}\right) + C$$

$$\int \frac{1}{\sqrt{a^2 - x^2}} dx = \sin^{-1}\left(\frac{x}{a}\right) + C$$

$$\int \frac{1}{x^2 - a^2} dx = \frac{1}{2a} \ln\left|\frac{x-a}{x+a}\right| + C$$
