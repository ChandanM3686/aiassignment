# Arithmetic and Geometric Progressions

## Arithmetic Progression (AP)
A sequence where the difference between consecutive terms is constant.

### General Form
a, a+d, a+2d, a+3d, ...
- a = first term
- d = common difference

### nth Term Formula
$$a_n = a + (n-1)d$$

### Sum of First n Terms
$$S_n = \frac{n}{2}[2a + (n-1)d] = \frac{n}{2}[a + a_n]$$

### Properties of AP
- If a, b, c are in AP: 2b = a + c (b is the arithmetic mean)
- Arithmetic mean of a and b: AM = (a + b)/2
- Sum of AP = n × (arithmetic mean of first and last term)

---

## Geometric Progression (GP)
A sequence where the ratio between consecutive terms is constant.

### General Form
a, ar, ar², ar³, ...
- a = first term
- r = common ratio

### nth Term Formula
$$a_n = ar^{n-1}$$

### Sum of First n Terms
For r ≠ 1:
$$S_n = a\frac{r^n - 1}{r - 1} = a\frac{1 - r^n}{1 - r}$$

### Sum to Infinity (|r| < 1)
$$S_\infty = \frac{a}{1-r}$$

### Properties of GP
- If a, b, c are in GP: b² = ac (b is the geometric mean)
- Geometric mean of a and b: GM = √(ab)
- Product of n terms of GP: (a·aₙ)^(n/2) = (first term × last term)^(n/2)

---

## Harmonic Progression (HP)
A sequence whose reciprocals form an AP.

If a₁, a₂, a₃, ... are in HP, then 1/a₁, 1/a₂, 1/a₃, ... are in AP.

### Harmonic Mean
For two numbers a and b:
$$HM = \frac{2ab}{a+b}$$

### Key Relationship
For positive numbers: **AM ≥ GM ≥ HM**

---

## Special Sums
- Sum of first n natural numbers: n(n+1)/2
- Sum of squares: n(n+1)(2n+1)/6
- Sum of cubes: [n(n+1)/2]²

## JEE Tips
- Insert n arithmetic means between a and b: common difference = (b-a)/(n+1)
- Insert n geometric means between a and b: common ratio = (b/a)^(1/(n+1))
- For infinite GP convergence, always check |r| < 1
