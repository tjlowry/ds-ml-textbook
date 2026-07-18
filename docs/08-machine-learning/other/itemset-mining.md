# Frequent Itemset Mining

## Overview

**Frequent itemset mining** finds sets of items that co-occur often in transaction data
("market-basket analysis") and turns them into **association rules** like *{diapers} →
{beer}*. The core measures are **support** (how often an itemset appears), **confidence**
(how often the rule's consequent follows its antecedent), and **lift** (how much more often
than chance). **Apriori** prunes the search using the downward-closure property — any
superset of an infrequent set is itself infrequent — and **FP-Growth** does the same job
faster with a compressed prefix tree.

**I don't have my own implementation of this one.** Frequent-pattern mining is covered in my
ECEN 758 notes but I never used it in a project or homework — no code of mine exists to show.
This page is a concept summary from the lecture.

## Course reference

The ECEN 758 Lecture 5 slides point to the `mlxtend` library's frequent-pattern
implementations as the practical toolkit (URLs extracted from the lecture PDF):

- Apriori: <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/>
- FP-Growth: <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/fpgrowth/>

## Gotchas (from the lecture, worth remembering)

- **Support threshold controls the blowup.** Too low and the number of frequent itemsets
  explodes combinatorially; too high and you miss interesting-but-rare patterns.
- **High confidence ≠ interesting.** If the consequent is common anyway, a rule can have high
  confidence but low **lift** — lift is the measure that corrects for base rate.
- **Apriori's pruning is the whole trick.** Downward closure (anti-monotonicity) is what
  makes the search tractable; FP-Growth keeps the result but avoids repeated database scans.
- **Correlation, not causation.** An association rule says two things co-occur, nothing about
  why.

## References

- ECEN 758 Lecture 5 — Frequent Itemset Mining and Association Rules (local:
  `course-files/08-machine-learning/758 Lec 05 Frequent Itemset Mining and Association Rules.pdf`).
  Instructor-copyrighted; concept summary only, no code of my own.
