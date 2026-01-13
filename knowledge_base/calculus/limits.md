# Limits

## Definition of Limit
$$\lim_{x \to a} f(x) = L$$

means f(x) approaches L as x approaches a.

## Limit Laws
For limits that exist:
1. **Sum**: lim(f + g) = lim f + lim g
2. **Difference**: lim(f - g) = lim f - lim g
3. **Product**: lim(f · g) = lim f · lim g
4. **Quotient**: lim(f/g) = lim f / lim g (if lim g ≠ 0)
5. **Power**: lim(fⁿ) = (lim f)ⁿ
6. **Root**: lim(ⁿ√f) = ⁿ√(lim f) (if lim f ≥ 0)

## Standard Limits
$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

$$\lim_{x \to 0} \frac{\tan x}{x} = 1$$

$$\lim_{x \to 0} \frac{1 - \cos x}{x^2} = \frac{1}{2}$$

$$\lim_{x \to 0} \frac{e^x - 1}{x} = 1$$

$$\lim_{x \to 0} \frac{\ln(1 + x)}{x} = 1$$

$$\lim_{x \to 0} \frac{a^x - 1}{x} = \ln a$$

$$\lim_{x \to 0} (1 + x)^{1/x} = e$$

$$\lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e$$

$$\lim_{x \to 0} \frac{(1+x)^n - 1}{x} = n$$

## Limits at Infinity
$$\lim_{x \to \infty} \frac{1}{x^n} = 0 \quad (n > 0)$$

$$\lim_{x \to \infty} e^{-x} = 0$$

$$\lim_{x \to \infty} \frac{P(x)}{Q(x)} = \begin{cases} 0 & \text{if deg P < deg Q} \\ \frac{a_n}{b_m} & \text{if deg P = deg Q} \\ \pm\infty & \text{if deg P > deg Q} \end{cases}$$

## L'Hôpital's Rule
For indeterminate forms 0/0 or ∞/∞:
$$\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$$

(if the right-hand limit exists)

## Indeterminate Forms
- 0/0, ∞/∞ → Use L'Hôpital's Rule
- 0 · ∞ → Convert to 0/0 or ∞/∞
- ∞ - ∞ → Combine fractions
- 1^∞, 0^0, ∞^0 → Take logarithm

## Squeeze Theorem
If g(x) ≤ f(x) ≤ h(x) for all x near a, and lim g(x) = lim h(x) = L, then lim f(x) = L.

## One-Sided Limits
- **Left limit**: lim(x→a⁻) f(x)
- **Right limit**: lim(x→a⁺) f(x)
- Limit exists ⟺ both one-sided limits exist and are equal

## Continuity
f is continuous at a if:
1. f(a) is defined
2. lim(x→a) f(x) exists
3. lim(x→a) f(x) = f(a)
