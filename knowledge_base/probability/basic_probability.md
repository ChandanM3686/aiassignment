# Basic Probability

## Fundamental Concepts

### Sample Space and Events
- **Sample Space (S)**: Set of all possible outcomes
- **Event (E)**: A subset of the sample space
- **Complement (E')**: Everything NOT in E

### Probability Definition
$$P(E) = \frac{\text{Number of favorable outcomes}}{\text{Total number of outcomes}}$$

**Properties**:
- 0 ≤ P(E) ≤ 1
- P(S) = 1 (certain event)
- P(∅) = 0 (impossible event)
- P(E') = 1 - P(E)

## Addition Rule
For any two events A and B:
$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

For mutually exclusive events (A ∩ B = ∅):
$$P(A \cup B) = P(A) + P(B)$$

## Multiplication Rule
$$P(A \cap B) = P(A) \cdot P(B|A) = P(B) \cdot P(A|B)$$

For independent events:
$$P(A \cap B) = P(A) \cdot P(B)$$

## Conditional Probability
$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

Read as: "Probability of A given B"

## Independence
Events A and B are independent if:
- P(A ∩ B) = P(A) · P(B)
- P(A|B) = P(A)
- P(B|A) = P(B)

## Bayes' Theorem
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

### Law of Total Probability
If B₁, B₂, ..., Bₙ partition the sample space:
$$P(A) = \sum_{i=1}^{n} P(A|B_i) \cdot P(B_i)$$

### Extended Bayes' Theorem
$$P(B_k|A) = \frac{P(A|B_k) \cdot P(B_k)}{\sum_{i=1}^{n} P(A|B_i) \cdot P(B_i)}$$

## Odds
- Odds in favor of E = P(E)/(1 - P(E))
- Odds against E = (1 - P(E))/P(E)

## Common Probability Problems
1. **Coin Toss**: P(Head) = P(Tail) = 1/2
2. **Die Roll**: P(any face) = 1/6
3. **Card Drawing**: P(Ace) = 4/52 = 1/13
4. **Birthday Problem**: P(at least 2 share birthday) with n people
