# Probability Distributions

## Random Variables
A random variable X maps outcomes to real numbers.
- **Discrete RV**: Countable values (integers)
- **Continuous RV**: Uncountable values (real numbers)

## Expected Value (Mean)
### Discrete
$$E[X] = \mu = \sum_{i} x_i \cdot P(X = x_i)$$

### Continuous
$$E[X] = \int_{-\infty}^{\infty} x \cdot f(x) dx$$

### Properties
- E[aX + b] = aE[X] + b
- E[X + Y] = E[X] + E[Y]
- E[XY] = E[X]E[Y] (if X, Y independent)

## Variance
$$Var(X) = \sigma^2 = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### Properties
- Var(aX + b) = a²Var(X)
- Var(X + Y) = Var(X) + Var(Y) (if independent)
- Standard Deviation: σ = √Var(X)

---

## Binomial Distribution
X ~ B(n, p) represents number of successes in n independent Bernoulli trials.

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

- **Mean**: E[X] = np
- **Variance**: Var(X) = np(1-p)

**When to use**: Fixed number of trials, each with same probability of success.

---

## Poisson Distribution
X ~ Poisson(λ) represents number of events in a fixed interval.

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

- **Mean**: E[X] = λ
- **Variance**: Var(X) = λ

**When to use**: Rare events, large n and small p (approximates Binomial when n→∞, p→0, np=λ).

---

## Geometric Distribution
X ~ Geo(p) represents number of trials until first success.

$$P(X = k) = (1-p)^{k-1} p$$

- **Mean**: E[X] = 1/p
- **Variance**: Var(X) = (1-p)/p²

---

## Normal Distribution
X ~ N(μ, σ²) is the bell curve distribution.

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

### Standard Normal (Z ~ N(0,1))
$$Z = \frac{X - \mu}{\sigma}$$

### Properties
- Symmetric about μ
- 68-95-99.7 Rule:
  - 68% within 1σ of μ
  - 95% within 2σ of μ
  - 99.7% within 3σ of μ

---

## Uniform Distribution
### Discrete Uniform
$$P(X = k) = \frac{1}{n}$$ for k = 1, 2, ..., n

### Continuous Uniform (X ~ U(a, b))
$$f(x) = \frac{1}{b-a}$$ for a ≤ x ≤ b

- Mean: (a + b)/2
- Variance: (b - a)²/12

---

## Chebyshev's Inequality
For any random variable with finite variance:
$$P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}$$

At least (1 - 1/k²) of data lies within k standard deviations.
