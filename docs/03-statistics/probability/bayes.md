# Bayesian Probability

## Overview

Bayesian probability provides a framework for updating our beliefs in light of new evidence. Named after Reverend Thomas Bayes, this approach treats probability as a measure of belief or certainty rather than just long-run frequency.

## Bayes' Theorem

### The Formula

For events $A$ and $B$ where $P(B) > 0$:

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

### Component Definitions

- **$P(A)$**: Prior probability - our initial belief about $A$ before seeing evidence
- **$P(B|A)$**: Likelihood - probability of observing evidence $B$ given $A$ is true
- **$P(B)$**: Marginal likelihood - total probability of observing $B$
- **$P(A|B)$**: Posterior probability - updated belief about $A$ after observing $B$

### Intuitive Understanding

Bayes' theorem answers: "Given that we observed $B$, how should we update our belief about $A$?"

```python
def bayes_theorem(prior, likelihood, marginal_likelihood):
    """
    Calculate posterior probability using Bayes' theorem.

    Parameters:
    -----------
    prior : float
        P(A) - Prior probability of A
    likelihood : float
        P(B|A) - Probability of B given A
    marginal_likelihood : float
        P(B) - Total probability of B

    Returns:
    --------
    float : Posterior probability P(A|B)
    """
    posterior = (likelihood * prior) / marginal_likelihood
    return posterior

# Example: Medical diagnosis
# Prior: 1% of population has disease
# Test sensitivity: 95% (P(positive | disease))
# Test specificity: 90% (P(negative | no disease))

prior_disease = 0.01
sensitivity = 0.95  # P(positive | disease)
specificity = 0.90  # P(negative | no disease)
false_positive_rate = 1 - specificity  # P(positive | no disease)

# P(positive test)
p_positive = (sensitivity * prior_disease +
              false_positive_rate * (1 - prior_disease))

# P(disease | positive test)
posterior = bayes_theorem(prior_disease, sensitivity, p_positive)

print("Medical Test Example")
print("=" * 50)
print(f"Prior P(disease) = {prior_disease:.2%}")
print(f"Test sensitivity P(+|disease) = {sensitivity:.2%}")
print(f"Test specificity P(-|no disease) = {specificity:.2%}")
print(f"\nP(positive test) = {p_positive:.4f}")
print(f"P(disease | positive test) = {posterior:.4f} = {posterior:.2%}")
print("\nNote: Despite the positive test, there's still only a")
print(f"{posterior:.1%} chance of actually having the disease!")
```

### R Implementation

```r
# Bayes' theorem function
bayes_theorem <- function(prior, likelihood, marginal_likelihood) {
  posterior <- (likelihood * prior) / marginal_likelihood
  return(posterior)
}

# Medical diagnosis example
prior_disease <- 0.01
sensitivity <- 0.95
specificity <- 0.90
false_positive_rate <- 1 - specificity

# P(positive test)
p_positive <- sensitivity * prior_disease +
              false_positive_rate * (1 - prior_disease)

# P(disease | positive test)
posterior <- bayes_theorem(prior_disease, sensitivity, p_positive)

cat("Medical Test Example\n")
cat(sprintf("Prior P(disease) = %.2f%%\n", prior_disease * 100))
cat(sprintf("P(positive test) = %.4f\n", p_positive))
cat(sprintf("P(disease | positive test) = %.2f%%\n", posterior * 100))
```

## Law of Total Probability

The marginal likelihood $P(B)$ is calculated using the law of total probability:

$$P(B) = \sum_{i} P(B|A_i) \cdot P(A_i)$$

where $\{A_1, A_2, \ldots, A_n\}$ is a partition of the sample space.

For the binary case:

$$P(B) = P(B|A) \cdot P(A) + P(B|A^c) \cdot P(A^c)$$

```python
import numpy as np

def calculate_marginal_probability(likelihoods, priors):
    """
    Calculate P(B) using law of total probability.

    Parameters:
    -----------
    likelihoods : list
        P(B|A_i) for each partition element
    priors : list
        P(A_i) for each partition element

    Returns:
    --------
    float : Marginal probability P(B)
    """
    return sum(l * p for l, p in zip(likelihoods, priors))

# Example: Three factories produce a product
# Factory A: 30% of production, 2% defect rate
# Factory B: 45% of production, 3% defect rate
# Factory C: 25% of production, 5% defect rate

factories = ['A', 'B', 'C']
production_shares = [0.30, 0.45, 0.25]  # P(factory)
defect_rates = [0.02, 0.03, 0.05]        # P(defect | factory)

# P(defect)
p_defect = calculate_marginal_probability(defect_rates, production_shares)

print("Factory Quality Example")
print("=" * 50)
print("\nProduction shares and defect rates:")
for f, share, rate in zip(factories, production_shares, defect_rates):
    print(f"  Factory {f}: {share:.0%} production, {rate:.0%} defect rate")

print(f"\nP(defect) = {p_defect:.4f} = {p_defect:.2%}")

# P(factory | defect) for each factory
print("\nGiven a defective item, probability it came from:")
for f, share, rate in zip(factories, production_shares, defect_rates):
    p_factory_given_defect = (rate * share) / p_defect
    print(f"  Factory {f}: {p_factory_given_defect:.4f} = {p_factory_given_defect:.2%}")
```

## Extended Form of Bayes' Theorem

When we have multiple hypotheses $H_1, H_2, \ldots, H_n$:

$$P(H_i|E) = \frac{P(E|H_i) \cdot P(H_i)}{\sum_{j=1}^{n} P(E|H_j) \cdot P(H_j)}$$

```python
import numpy as np

def bayes_multiple_hypotheses(likelihoods, priors):
    """
    Calculate posterior probabilities for multiple hypotheses.

    Parameters:
    -----------
    likelihoods : array-like
        P(Evidence | H_i) for each hypothesis
    priors : array-like
        P(H_i) for each hypothesis

    Returns:
    --------
    array : Posterior probabilities P(H_i | Evidence)
    """
    likelihoods = np.array(likelihoods)
    priors = np.array(priors)

    # Calculate marginal likelihood (normalizing constant)
    marginal = np.sum(likelihoods * priors)

    # Calculate posteriors
    posteriors = (likelihoods * priors) / marginal

    return posteriors

# Example: Disease diagnosis with multiple possible conditions
# Symptoms could indicate one of three conditions or no condition

conditions = ['Condition A', 'Condition B', 'Condition C', 'No Condition']
priors = [0.05, 0.03, 0.02, 0.90]  # Base rates
# P(symptoms | condition)
likelihoods = [0.80, 0.65, 0.70, 0.10]

posteriors = bayes_multiple_hypotheses(likelihoods, priors)

print("Multi-Condition Diagnosis")
print("=" * 50)
print("\nPrior probabilities and likelihoods:")
for cond, prior, like in zip(conditions, priors, likelihoods):
    print(f"  {cond:15}: P(cond)={prior:.2f}, P(symptoms|cond)={like:.2f}")

print("\nPosterior probabilities P(condition | symptoms):")
for cond, post in zip(conditions, posteriors):
    print(f"  {cond:15}: {post:.4f} = {post:.2%}")

print(f"\nSum of posteriors: {posteriors.sum():.4f}")
```

## Sequential Bayesian Updating

One powerful feature of Bayesian analysis is that the posterior from one piece of evidence becomes the prior for the next piece:

$$P(H|E_1, E_2) = \frac{P(E_2|H, E_1) \cdot P(H|E_1)}{P(E_2|E_1)}$$

```python
import numpy as np

def sequential_bayesian_update(prior, evidence_sequence, likelihoods_if_true, likelihoods_if_false):
    """
    Update beliefs sequentially with multiple pieces of evidence.

    Parameters:
    -----------
    prior : float
        Initial P(H)
    evidence_sequence : list
        Sequence of evidence observations (True/False)
    likelihoods_if_true : list
        P(evidence_i | H=True) for each evidence type
    likelihoods_if_false : list
        P(evidence_i | H=False) for each evidence type

    Returns:
    --------
    list : Sequence of posterior probabilities
    """
    posteriors = [prior]
    current_belief = prior

    for i, evidence in enumerate(evidence_sequence):
        # Get likelihoods based on evidence observation
        if evidence:
            like_true = likelihoods_if_true[i]
            like_false = likelihoods_if_false[i]
        else:
            like_true = 1 - likelihoods_if_true[i]
            like_false = 1 - likelihoods_if_false[i]

        # Calculate marginal likelihood
        marginal = like_true * current_belief + like_false * (1 - current_belief)

        # Update belief
        current_belief = (like_true * current_belief) / marginal
        posteriors.append(current_belief)

    return posteriors

# Example: Determining if a coin is fair or biased
# H: Coin is biased (70% heads)
# Each flip is evidence

# Prior: 50% chance the coin is biased
prior = 0.5

# Likelihoods for observing heads
p_heads_if_biased = 0.70
p_heads_if_fair = 0.50

# Observe sequence of flips: H, H, T, H, H, H, T, H, H, H
flips = [True, True, False, True, True, True, False, True, True, True]

posteriors = sequential_bayesian_update(
    prior,
    flips,
    [p_heads_if_biased] * len(flips),  # P(H | biased)
    [p_heads_if_fair] * len(flips)      # P(H | fair)
)

print("Sequential Bayesian Update: Is the coin biased?")
print("=" * 55)
print(f"Prior P(biased) = {prior:.2f}")
print(f"P(heads | biased) = {p_heads_if_biased:.2f}")
print(f"P(heads | fair) = {p_heads_if_fair:.2f}")
print("\nObservations and updated beliefs:")
print(f"{'Flip':<6} {'Outcome':<10} {'P(biased)':<12}")
print("-" * 30)
print(f"{'Start':<6} {'--':<10} {posteriors[0]:.4f}")
for i, (flip, post) in enumerate(zip(flips, posteriors[1:]), 1):
    outcome = "Heads" if flip else "Tails"
    print(f"{i:<6} {outcome:<10} {post:.4f}")
```

## Bayesian vs Frequentist Interpretation

### Frequentist View
- Probability = long-run frequency
- Parameters are fixed, unknown constants
- Data is random
- Cannot say "P(parameter | data)"

### Bayesian View
- Probability = degree of belief
- Parameters have probability distributions
- Data is fixed (once observed)
- Can say "P(parameter | data)"

```python
import numpy as np
from scipy import stats

# Example: Estimating a population proportion
# Observed: 7 successes in 10 trials

successes = 7
trials = 10

print("Estimating a Proportion: Frequentist vs Bayesian")
print("=" * 55)
print(f"Observed: {successes} successes in {trials} trials\n")

# Frequentist approach
p_hat = successes / trials
se = np.sqrt(p_hat * (1 - p_hat) / trials)
ci_freq = stats.norm.interval(0.95, loc=p_hat, scale=se)

print("FREQUENTIST APPROACH:")
print(f"  Point estimate: p-hat = {p_hat:.3f}")
print(f"  95% CI: ({ci_freq[0]:.3f}, {ci_freq[1]:.3f})")
print("  Interpretation: If we repeated this experiment many times,")
print("  95% of the intervals would contain the true p.")

# Bayesian approach with uniform prior (Beta(1,1))
alpha_prior, beta_prior = 1, 1  # Uniform prior
alpha_post = alpha_prior + successes
beta_post = beta_prior + (trials - successes)

posterior = stats.beta(alpha_post, beta_post)
ci_bayes = posterior.interval(0.95)

print("\nBAYESIAN APPROACH (uniform prior):")
print(f"  Prior: Beta({alpha_prior}, {beta_prior})")
print(f"  Posterior: Beta({alpha_post}, {beta_post})")
print(f"  Posterior mean: {posterior.mean():.3f}")
print(f"  95% Credible Interval: ({ci_bayes[0]:.3f}, {ci_bayes[1]:.3f})")
print("  Interpretation: Given the data, there is a 95% probability")
print("  that the true p lies in this interval.")
```

## Conjugate Priors

A prior is **conjugate** to a likelihood if the posterior belongs to the same family as the prior.

### Common Conjugate Pairs

| Likelihood | Conjugate Prior | Posterior |
|------------|-----------------|-----------|
| Binomial | Beta | Beta |
| Poisson | Gamma | Gamma |
| Normal (known variance) | Normal | Normal |
| Normal (known mean) | Inverse Gamma | Inverse Gamma |
| Multinomial | Dirichlet | Dirichlet |

```python
import numpy as np
from scipy import stats

class BetaBinomialModel:
    """
    Bayesian model for binomial data with Beta prior.
    """
    def __init__(self, alpha_prior=1, beta_prior=1):
        """
        Initialize with Beta(alpha, beta) prior.
        alpha=1, beta=1 is uniform (non-informative)
        """
        self.alpha = alpha_prior
        self.beta = beta_prior

    def update(self, successes, trials):
        """Update posterior with new data."""
        self.alpha += successes
        self.beta += (trials - successes)

    def posterior_mean(self):
        """Return posterior mean."""
        return self.alpha / (self.alpha + self.beta)

    def posterior_mode(self):
        """Return posterior mode (MAP estimate)."""
        if self.alpha > 1 and self.beta > 1:
            return (self.alpha - 1) / (self.alpha + self.beta - 2)
        return None

    def credible_interval(self, confidence=0.95):
        """Return credible interval."""
        posterior = stats.beta(self.alpha, self.beta)
        return posterior.interval(confidence)

    def posterior_pdf(self, p_values):
        """Return posterior density at given values."""
        return stats.beta.pdf(p_values, self.alpha, self.beta)


# Example: Learning about a coin's bias
model = BetaBinomialModel(alpha_prior=1, beta_prior=1)  # Uniform prior

print("Learning Coin Bias with Beta-Binomial Model")
print("=" * 50)
print(f"Prior: Beta({model.alpha}, {model.beta})")
print(f"Prior mean: {model.posterior_mean():.3f}")

# Collect data in batches
data_batches = [
    (6, 10),   # 6 heads in 10 flips
    (14, 20),  # 14 heads in 20 flips
    (35, 50),  # 35 heads in 50 flips
]

for i, (successes, trials) in enumerate(data_batches, 1):
    model.update(successes, trials)
    ci = model.credible_interval()
    print(f"\nAfter batch {i}: {successes}/{trials} heads")
    print(f"  Posterior: Beta({model.alpha}, {model.beta})")
    print(f"  Mean: {model.posterior_mean():.3f}")
    print(f"  95% CI: ({ci[0]:.3f}, {ci[1]:.3f})")
```

### R Implementation

```r
# Beta-Binomial conjugate analysis
alpha_prior <- 1
beta_prior <- 1

# Update with data
successes <- 7
trials <- 10

alpha_post <- alpha_prior + successes
beta_post <- beta_prior + (trials - successes)

# Posterior summary
posterior_mean <- alpha_post / (alpha_post + beta_post)
ci <- qbeta(c(0.025, 0.975), alpha_post, beta_post)

cat("Beta-Binomial Model\n")
cat(sprintf("Prior: Beta(%d, %d)\n", alpha_prior, beta_prior))
cat(sprintf("Data: %d successes in %d trials\n", successes, trials))
cat(sprintf("Posterior: Beta(%d, %d)\n", alpha_post, beta_post))
cat(sprintf("Posterior mean: %.3f\n", posterior_mean))
cat(sprintf("95%% Credible Interval: (%.3f, %.3f)\n", ci[1], ci[2]))
```

## Choosing Priors

### Types of Priors

1. **Non-informative (Flat/Uniform)**: Represent ignorance
2. **Weakly informative**: Constrain to reasonable range
3. **Informative**: Incorporate prior knowledge
4. **Empirical Bayes**: Estimate prior from data

```python
import numpy as np
from scipy import stats

# Example: Different priors for estimating coin bias
successes, trials = 3, 10

print("Effect of Different Priors")
print("=" * 50)
print(f"Data: {successes} heads in {trials} flips\n")

priors = [
    ("Uniform (non-informative)", 1, 1),
    ("Jeffreys prior", 0.5, 0.5),
    ("Weakly informative (fair)", 5, 5),
    ("Strong prior (fair)", 50, 50),
    ("Strong prior (biased high)", 8, 2),
]

print(f"{'Prior Type':<30} {'Posterior Mean':<15} {'95% CI'}")
print("-" * 65)

for name, alpha_p, beta_p in priors:
    alpha_post = alpha_p + successes
    beta_post = beta_p + (trials - successes)

    posterior = stats.beta(alpha_post, beta_post)
    mean = posterior.mean()
    ci = posterior.interval(0.95)

    print(f"{name:<30} {mean:.3f}           ({ci[0]:.3f}, {ci[1]:.3f})")

print("\nNote: Strong priors shrink the estimate toward prior belief,")
print("while weak priors let the data dominate.")
```

## Bayesian Hypothesis Testing

Instead of p-values, Bayesians use **Bayes Factors** to compare hypotheses:

$$BF_{10} = \frac{P(D|H_1)}{P(D|H_0)} = \frac{\text{Likelihood of data under } H_1}{\text{Likelihood of data under } H_0}$$

Interpretation guidelines:
- $BF < 1$: Evidence for $H_0$
- $1 < BF < 3$: Anecdotal evidence for $H_1$
- $3 < BF < 10$: Moderate evidence for $H_1$
- $10 < BF < 30$: Strong evidence for $H_1$
- $BF > 30$: Very strong evidence for $H_1$

```python
import numpy as np
from scipy import stats
from scipy.special import beta as beta_func

def bayes_factor_proportion(successes, trials, p_null=0.5, prior_alpha=1, prior_beta=1):
    """
    Calculate Bayes Factor for testing H0: p = p_null vs H1: p != p_null

    Uses Beta(alpha, beta) prior under H1.
    """
    # Likelihood under H0 (point null)
    likelihood_h0 = stats.binom.pmf(successes, trials, p_null)

    # Marginal likelihood under H1 (integrated over prior)
    # For Beta prior, this has a closed form (Beta-Binomial)
    alpha_post = prior_alpha + successes
    beta_post = prior_beta + (trials - successes)

    likelihood_h1 = (beta_func(alpha_post, beta_post) /
                     beta_func(prior_alpha, prior_beta))

    bayes_factor = likelihood_h1 / likelihood_h0

    return bayes_factor

# Example: Testing if a coin is fair
np.random.seed(42)

test_cases = [
    (5, 10, "5/10 heads"),
    (7, 10, "7/10 heads"),
    (60, 100, "60/100 heads"),
    (70, 100, "70/100 heads"),
]

print("Bayes Factor for Testing Fair Coin (p = 0.5)")
print("=" * 55)
print("H0: p = 0.5  vs  H1: p != 0.5")
print()

for successes, trials, desc in test_cases:
    bf = bayes_factor_proportion(successes, trials)

    # Interpret
    if bf < 1:
        interp = f"Evidence for H0 (BF = {1/bf:.2f} for H0)"
    elif bf < 3:
        interp = "Anecdotal evidence for H1"
    elif bf < 10:
        interp = "Moderate evidence for H1"
    elif bf < 30:
        interp = "Strong evidence for H1"
    else:
        interp = "Very strong evidence for H1"

    print(f"Data: {desc}")
    print(f"  BF_10 = {bf:.3f}")
    print(f"  {interp}\n")
```

## Practical Applications

### Spam Filter Example

```python
import numpy as np

class NaiveBayesSpamFilter:
    """Simple Naive Bayes spam classifier."""

    def __init__(self):
        self.p_spam = 0.5  # Prior probability of spam
        self.word_spam_prob = {}  # P(word | spam)
        self.word_ham_prob = {}   # P(word | not spam)

    def train(self, spam_words, ham_words, smoothing=1):
        """Train on lists of words from spam and ham emails."""
        all_words = set(spam_words + ham_words)

        # Count occurrences
        spam_counts = {w: spam_words.count(w) for w in all_words}
        ham_counts = {w: ham_words.count(w) for w in all_words}

        # Laplace smoothing
        total_spam = len(spam_words) + smoothing * len(all_words)
        total_ham = len(ham_words) + smoothing * len(all_words)

        for word in all_words:
            self.word_spam_prob[word] = (spam_counts[word] + smoothing) / total_spam
            self.word_ham_prob[word] = (ham_counts[word] + smoothing) / total_ham

    def classify(self, email_words):
        """Classify an email based on its words."""
        # Log probabilities to avoid underflow
        log_p_spam = np.log(self.p_spam)
        log_p_ham = np.log(1 - self.p_spam)

        for word in email_words:
            if word in self.word_spam_prob:
                log_p_spam += np.log(self.word_spam_prob[word])
                log_p_ham += np.log(self.word_ham_prob[word])

        # Convert back to probabilities
        max_log = max(log_p_spam, log_p_ham)
        p_spam_given_email = np.exp(log_p_spam - max_log)
        p_ham_given_email = np.exp(log_p_ham - max_log)

        # Normalize
        total = p_spam_given_email + p_ham_given_email
        p_spam_given_email /= total

        return p_spam_given_email, "SPAM" if p_spam_given_email > 0.5 else "HAM"


# Demo
spam_training = ["free", "winner", "click", "free", "money", "click", "free"]
ham_training = ["meeting", "report", "project", "meeting", "deadline", "report"]

filter = NaiveBayesSpamFilter()
filter.train(spam_training, ham_training)

test_emails = [
    ["free", "money"],
    ["meeting", "report"],
    ["free", "meeting", "click"],
]

print("Naive Bayes Spam Filter")
print("=" * 50)

for email in test_emails:
    prob, label = filter.classify(email)
    print(f"Email words: {email}")
    print(f"  P(spam|email) = {prob:.4f}")
    print(f"  Classification: {label}\n")
```

## Summary

Key concepts in Bayesian probability:

1. **Bayes' Theorem**: Updates prior beliefs with evidence to form posterior beliefs

2. **Prior distributions**: Encode initial knowledge or uncertainty about parameters

3. **Posterior distributions**: Combine prior knowledge with observed data

4. **Conjugate priors**: Enable closed-form posterior calculations

5. **Sequential updating**: Posterior becomes prior for next observation

6. **Bayes Factors**: Alternative to p-values for hypothesis testing

Advantages of Bayesian approach:
- Incorporates prior knowledge formally
- Provides probability statements about parameters
- Natural for sequential learning
- Handles small samples better with informative priors

Considerations:
- Choice of prior can influence results
- Computational complexity for complex models
- Different philosophical interpretation of probability
