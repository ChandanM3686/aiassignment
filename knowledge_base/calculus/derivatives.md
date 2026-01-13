# Derivatives

## Definition
$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

Alternative notation: dy/dx, Df, ẏ

## Basic Derivative Rules
| Function | Derivative |
|----------|------------|
| c (constant) | 0 |
| xⁿ | nxⁿ⁻¹ |
| eˣ | eˣ |
| aˣ | aˣ ln a |
| ln x | 1/x |
| logₐ x | 1/(x ln a) |
| sin x | cos x |
| cos x | -sin x |
| tan x | sec² x |
| cot x | -csc² x |
| sec x | sec x tan x |
| csc x | -csc x cot x |
| sin⁻¹ x | 1/√(1-x²) |
| cos⁻¹ x | -1/√(1-x²) |
| tan⁻¹ x | 1/(1+x²) |

## Differentiation Rules

### Sum/Difference Rule
$$\frac{d}{dx}[f(x) \pm g(x)] = f'(x) \pm g'(x)$$

### Product Rule
$$\frac{d}{dx}[f(x) \cdot g(x)] = f'(x)g(x) + f(x)g'(x)$$

### Quotient Rule
$$\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}$$

### Chain Rule
$$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$$

Or in Leibniz notation:
$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

## Implicit Differentiation
When y is defined implicitly by F(x, y) = 0:
1. Differentiate both sides with respect to x
2. Remember that y is a function of x (use chain rule)
3. Solve for dy/dx

**Example**: x² + y² = 25
2x + 2y(dy/dx) = 0
dy/dx = -x/y

## Logarithmic Differentiation
For complex products/quotients or variable exponents:
1. Take ln of both sides
2. Use log rules to simplify
3. Differentiate implicitly
4. Solve for dy/dx

**Example**: y = xˣ
ln y = x ln x
(1/y)(dy/dx) = ln x + 1
dy/dx = xˣ(ln x + 1)

## Higher Derivatives
- Second derivative: f''(x) = d²y/dx²
- nth derivative: f⁽ⁿ⁾(x) = dⁿy/dxⁿ

## Parametric Derivatives
If x = f(t), y = g(t):
$$\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{g'(t)}{f'(t)}$$

$$\frac{d^2y}{dx^2} = \frac{d(dy/dx)/dt}{dx/dt}$$
