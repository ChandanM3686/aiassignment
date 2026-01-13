# Determinants

## Definition
The determinant is a scalar value computed from a square matrix.

## 2×2 Determinant
$$\det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$$

## 3×3 Determinant (Sarrus' Rule / Cofactor Expansion)
$$\det\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} = a(ei-fh) - b(di-fg) + c(dh-eg)$$

## Cofactor Expansion
Along row i:
$$\det(A) = \sum_{j=1}^{n} a_{ij} \cdot C_{ij}$$

where Cᵢⱼ = (-1)^(i+j) · Mᵢⱼ (Mᵢⱼ is the minor)

## Properties of Determinants

### Basic Properties
1. det(I) = 1
2. det(Aᵀ) = det(A)
3. det(AB) = det(A) · det(B)
4. det(kA) = kⁿ · det(A) for n×n matrix
5. det(A⁻¹) = 1/det(A)

### Row/Column Operations
6. Swapping two rows/columns: det changes sign
7. Multiplying row/column by k: det multiplied by k
8. Adding multiple of one row to another: det unchanged
9. If two rows/columns are identical: det = 0
10. If row/column is all zeros: det = 0

### Special Matrices
11. Triangular matrix: det = product of diagonal elements
12. Diagonal matrix: det = product of diagonal elements

## Application: Solving Linear Systems

### Cramer's Rule
For system Ax = b where det(A) ≠ 0:
$$x_i = \frac{\det(A_i)}{\det(A)}$$

where Aᵢ is A with column i replaced by b.

### Conditions for Solution
- det(A) ≠ 0: Unique solution exists
- det(A) = 0: No unique solution (may have none or infinitely many)

## Area and Volume
- Area of parallelogram: |det([v₁; v₂])|
- Volume of parallelepiped: |det([v₁; v₂; v₃])|

## Characteristic Equation
$$\det(A - \lambda I) = 0$$

Gives eigenvalues λ of matrix A.

## Common Determinant Patterns

### Block Triangular
$$\det\begin{bmatrix} A & B \\ 0 & D \end{bmatrix} = \det(A) \cdot \det(D)$$

### Vandermonde Determinant
$$\det\begin{bmatrix} 1 & a & a^2 \\ 1 & b & b^2 \\ 1 & c & c^2 \end{bmatrix} = (b-a)(c-a)(c-b)$$
