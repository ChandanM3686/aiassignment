# Permutations and Combinations

## Factorial
n! = n × (n-1) × (n-2) × ... × 2 × 1
- 0! = 1
- 1! = 1

## Permutations (Order Matters)
### Basic Permutation
Number of ways to arrange r items from n distinct items:
$$P(n,r) = nPr = \frac{n!}{(n-r)!}$$

### Permutations of All Items
Number of ways to arrange n distinct items: n!

### Permutations with Repetition
If there are n items with p₁ identical of type 1, p₂ identical of type 2, ...:
$$\frac{n!}{p_1! \cdot p_2! \cdot ... \cdot p_k!}$$

**Example**: Arrangements of "MISSISSIPPI" = 11!/(4!·4!·2!) = 34,650

### Circular Permutations
- Distinct objects in a circle: (n-1)!
- With clockwise/anticlockwise distinction: (n-1)!/2

## Combinations (Order Doesn't Matter)
Number of ways to select r items from n distinct items:
$$C(n,r) = nCr = \binom{n}{r} = \frac{n!}{r!(n-r)!}$$

### Properties of Combinations
- C(n,0) = C(n,n) = 1
- C(n,r) = C(n, n-r) (Symmetry)
- C(n,r) + C(n,r+1) = C(n+1,r+1) (Pascal's Identity)
- C(n,0) + C(n,1) + ... + C(n,n) = 2ⁿ

## Multinomial Coefficient
Ways to divide n objects into groups of n₁, n₂, ..., nₖ:
$$\binom{n}{n_1, n_2, ..., n_k} = \frac{n!}{n_1! \cdot n_2! \cdot ... \cdot n_k!}$$

## Selection with Repetition
Selecting r items from n types (repetition allowed):
$$C(n+r-1, r) = \frac{(n+r-1)!}{r!(n-1)!}$$

## Distribution Problems
### Distinct objects into distinct boxes
n objects into r boxes: rⁿ ways

### Identical objects into distinct boxes
n identical objects into r boxes: C(n+r-1, r-1)

### Distinct objects into identical boxes
Uses Stirling numbers of the second kind

## Derangements
Number of permutations where no element is in its original position:
$$D_n = n! \left(1 - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + ... + \frac{(-1)^n}{n!}\right)$$

## Key Formulas Summary
| Scenario | Formula |
|----------|---------|
| Arrange r from n | n!/(n-r)! |
| Select r from n | n!/(r!(n-r)!) |
| Arrange n with repeats | n!/(p₁!p₂!...) |
| Circular arrangement | (n-1)! |
