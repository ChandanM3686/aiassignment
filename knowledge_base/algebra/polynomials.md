# Polynomials

## Definition
A polynomial in x is an expression of the form:
P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀

where aₙ ≠ 0 (leading coefficient) and n is the degree.

## Polynomial Division
**Division Algorithm**: P(x) = D(x)·Q(x) + R(x)
- P(x): Dividend
- D(x): Divisor
- Q(x): Quotient
- R(x): Remainder (degree < degree of D(x))

## Remainder Theorem
When polynomial P(x) is divided by (x - a), the remainder equals P(a).

## Factor Theorem
(x - a) is a factor of P(x) if and only if P(a) = 0.

## Fundamental Theorem of Algebra
Every polynomial of degree n has exactly n roots (counting multiplicities, including complex roots).

## Polynomial Identities
1. (a + b)² = a² + 2ab + b²
2. (a - b)² = a² - 2ab + b²
3. (a + b)³ = a³ + 3a²b + 3ab² + b³
4. (a - b)³ = a³ - 3a²b + 3ab² - b³
5. a³ + b³ = (a + b)(a² - ab + b²)
6. a³ - b³ = (a - b)(a² + ab + b²)
7. aⁿ - bⁿ = (a - b)(aⁿ⁻¹ + aⁿ⁻²b + ... + bⁿ⁻¹)

## Relation Between Roots and Coefficients
For P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₀ with roots α₁, α₂, ..., αₙ:
- Sum of roots: Σαᵢ = -aₙ₋₁/aₙ
- Sum of products taken two at a time: Σαᵢαⱼ = aₙ₋₂/aₙ
- Product of all roots: α₁α₂...αₙ = (-1)ⁿ(a₀/aₙ)

## Synthetic Division
A quick method to divide by (x - a):
1. Write down coefficients
2. Bring down leading coefficient
3. Multiply by a, add to next coefficient
4. Repeat until complete

## Partial Fractions
For rational functions, decompose into simpler fractions:
- Linear factors: A/(x-a)
- Repeated linear: A/(x-a) + B/(x-a)² + ...
- Irreducible quadratic: (Ax+B)/(x²+px+q)
