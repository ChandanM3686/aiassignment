# Common Calculus Mistakes

## Limits

### Mistake 1: Direct Substitution Without Checking
❌ lim(x→0) sin(x)/x = 0/0 = undefined
✅ This is an indeterminate form → use L'Hôpital's or standard limit = 1

### Mistake 2: Misapplying L'Hôpital's Rule
❌ Using L'Hôpital's when form is NOT indeterminate
✅ Only use for 0/0 or ∞/∞ forms

❌ lim(x→0) (x+1)/x = lim 1/1 = 1
✅ lim(x→0) (x+1)/x = undefined (not an indeterminate form)

### Mistake 3: Wrong Standard Limits
❌ lim(x→0) (1-cos x)/x = 0
✅ lim(x→0) (1-cos x)/x = 0 (not 1!)
BUT lim(x→0) (1-cos x)/x² = 1/2

## Derivatives

### Mistake 4: Chain Rule Forgetting
❌ d/dx[sin(x²)] = cos(x²)
✅ d/dx[sin(x²)] = cos(x²) · 2x = 2x cos(x²)

ALWAYS apply chain rule for composite functions!

### Mistake 5: Product Rule Confusion
❌ d/dx[x·sin x] = 1·cos x = cos x
✅ d/dx[x·sin x] = 1·sin x + x·cos x = sin x + x cos x

### Mistake 6: Quotient Rule Sign Error
❌ d/dx[f/g] = (f'g + fg')/g²
✅ d/dx[f/g] = (f'g - fg')/g² (minus, not plus!)

### Mistake 7: Derivative of eˣ Variants
❌ d/dx[e^(2x)] = e^(2x)
✅ d/dx[e^(2x)] = 2e^(2x) (chain rule!)

❌ d/dx[e²] = 2e
✅ d/dx[e²] = 0 (e² is a constant!)

### Mistake 8: ln Derivative
❌ d/dx[ln(2x)] = 1/(2x)
✅ d/dx[ln(2x)] = 1/(2x) · 2 = 1/x (chain rule!)

## Integration

### Mistake 9: Missing Constant
❌ ∫ 2x dx = x²
✅ ∫ 2x dx = x² + C

### Mistake 10: Substitution Incomplete
❌ ∫ x·e^(x²) dx = e^(x²) + C (missing factor)
✅ Let u = x², du = 2x dx
   ∫ x·e^(x²) dx = (1/2)∫ e^u du = (1/2)e^(x²) + C

### Mistake 11: Integration by Parts - Wrong Choice
LIATE order: Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential
Choose u from earlier in list, dv from later.

## Optimization

### Mistake 12: Not Checking Endpoints
❌ Finding critical point and stopping
✅ Compare critical point values with endpoint values

### Mistake 13: Second Derivative Test
❌ f''(c) = 0 means c is an inflection point
✅ f''(c) = 0 means test is inconclusive

## Related Rates

### Mistake 14: Not Differentiating Implicitly
❌ A = πr² → dA/dt = 2πr
✅ A = πr² → dA/dt = 2πr · (dr/dt)

### Mistake 15: Substituting Before Differentiating
❌ At r = 5: dA/dt = d/dt[π(5)²] = 0
✅ First differentiate, THEN substitute known values

## Prevention Strategies
1. Write down each step explicitly
2. Check units and dimensions
3. Verify with alternative methods
4. Use technology to check answers
5. Practice common patterns repeatedly
