# Matrices

## Definition
A matrix is a rectangular array of numbers arranged in rows and columns.
Matrix A of order m × n has m rows and n columns.

## Types of Matrices
- **Square Matrix**: m = n
- **Row Matrix**: m = 1
- **Column Matrix**: n = 1
- **Zero Matrix**: All elements are 0
- **Diagonal Matrix**: Square matrix with non-zero elements only on diagonal
- **Identity Matrix (I)**: Diagonal matrix with 1s on diagonal
- **Scalar Matrix**: Diagonal matrix with same scalar on diagonal
- **Symmetric Matrix**: A = Aᵀ
- **Skew-Symmetric**: A = -Aᵀ
- **Orthogonal Matrix**: AᵀA = AAᵀ = I

## Matrix Operations

### Addition
(A + B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ (same dimensions required)

### Scalar Multiplication
(kA)ᵢⱼ = k · Aᵢⱼ

### Matrix Multiplication
(AB)ᵢⱼ = Σₖ Aᵢₖ · Bₖⱼ

**Dimensions**: (m×n) × (n×p) = (m×p)

**Note**: AB ≠ BA in general (non-commutative)

### Transpose
(Aᵀ)ᵢⱼ = Aⱼᵢ

**Properties**:
- (Aᵀ)ᵀ = A
- (A + B)ᵀ = Aᵀ + Bᵀ
- (AB)ᵀ = BᵀAᵀ
- (kA)ᵀ = kAᵀ

## Matrix Properties
- A + B = B + A (commutative for addition)
- A(BC) = (AB)C (associative)
- A(B + C) = AB + AC (distributive)
- AI = IA = A (identity)

## Trace
For square matrix A:
tr(A) = Σᵢ Aᵢᵢ (sum of diagonal elements)

**Properties**:
- tr(A + B) = tr(A) + tr(B)
- tr(kA) = k · tr(A)
- tr(AB) = tr(BA)

## Inverse Matrix
For square matrix A, if A⁻¹ exists:
AA⁻¹ = A⁻¹A = I

**Properties**:
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- det(A⁻¹) = 1/det(A)

### Finding Inverse (2×2)
For A = [a b; c d]:
$$A^{-1} = \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

(exists only if ad - bc ≠ 0)

### Finding Inverse (General)
A⁻¹ = (1/det(A)) · adj(A)

## Adjugate (Adjoint) Matrix
adj(A) = transpose of cofactor matrix

## Elementary Row Operations
1. Swap two rows
2. Multiply a row by non-zero scalar
3. Add multiple of one row to another
