# Vectors

## Definition
A vector has both magnitude and direction.
Represented as v = (x, y) in 2D or v = (x, y, z) in 3D.

## Vector Notation
- **Position vector**: OA→ = (a₁, a₂, a₃)
- **Unit vectors**: î = (1,0,0), ĵ = (0,1,0), k̂ = (0,0,1)
- **Component form**: v = a₁î + a₂ĵ + a₃k̂

## Basic Operations

### Addition
(a₁, a₂, a₃) + (b₁, b₂, b₃) = (a₁+b₁, a₂+b₂, a₃+b₃)

### Scalar Multiplication
k(a₁, a₂, a₃) = (ka₁, ka₂, ka₃)

## Magnitude (Length)
$$|\vec{v}| = \sqrt{a_1^2 + a_2^2 + a_3^2}$$

## Unit Vector
$$\hat{v} = \frac{\vec{v}}{|\vec{v}|}$$

## Dot Product (Scalar Product)
$$\vec{a} \cdot \vec{b} = a_1b_1 + a_2b_2 + a_3b_3 = |\vec{a}||\vec{b}|\cos\theta$$

### Properties
- a · b = b · a (commutative)
- a · (b + c) = a · b + a · c (distributive)
- a · a = |a|² (gives magnitude)
- a · b = 0 ⟺ a ⊥ b (perpendicular)

## Cross Product (Vector Product)
$$\vec{a} \times \vec{b} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ a_1 & a_2 & a_3 \\ b_1 & b_2 & b_3 \end{vmatrix}$$

$$= (a_2b_3 - a_3b_2)\hat{i} - (a_1b_3 - a_3b_1)\hat{j} + (a_1b_2 - a_2b_1)\hat{k}$$

### Magnitude
$$|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$$

### Properties
- a × b = -(b × a) (anti-commutative)
- a × a = 0
- a × b = 0 ⟺ a ∥ b (parallel)
- Direction: Right-hand rule
- î × ĵ = k̂, ĵ × k̂ = î, k̂ × î = ĵ

## Triple Products

### Scalar Triple Product
$$\vec{a} \cdot (\vec{b} \times \vec{c}) = \begin{vmatrix} a_1 & a_2 & a_3 \\ b_1 & b_2 & b_3 \\ c_1 & c_2 & c_3 \end{vmatrix}$$

**Application**: Volume of parallelepiped = |a · (b × c)|

### Vector Triple Product
$$\vec{a} \times (\vec{b} \times \vec{c}) = (\vec{a} \cdot \vec{c})\vec{b} - (\vec{a} \cdot \vec{b})\vec{c}$$

## Geometric Applications

### Projection
Scalar projection of a onto b: comp_b(a) = (a · b)/|b|
Vector projection: proj_b(a) = ((a · b)/|b|²)b

### Area of Triangle
Area = ½|AB × AC|

### Area of Parallelogram
Area = |a × b|

### Collinearity
Three points A, B, C are collinear if AB × AC = 0

### Coplanarity
Four points are coplanar if [AB, AC, AD] = 0 (scalar triple product)
