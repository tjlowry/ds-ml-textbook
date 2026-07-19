# Machine Learning

## Overview

This chapter is the "how I actually built the model" companion to the more
statistics-flavored chapters. It covers the classic supervised and unsupervised
algorithms and the ensemble methods I reach for most; neural networks from backprop up
to transformers live in the [Deep Learning](deep-learning/index.md) chapter.

It draws on two streams of my own work:

- **ECEN 758 — Data Mining and Analysis (Texas A&M grad).** Dr. Peeples' course: the
  clustering / classification / dimensionality-reduction backbone. My contributions are
  the homework notebooks (from-scratch EM, hierarchical/density clustering, PCA, applied
  kNN/Naive Bayes) and a CIFAR-100 image-classification group project (written up in the
  [Deep Learning chapter's case study](case-study-cifar100.md)).
- **Earlier coursework and side projects.** DS 250 (BYU-Idaho) tree/random-forest client
  report, a STAT 654 XGBoost regression model, a PySpark ensemble revenue model, and a
  personal NFL-draft recommender system.

Every "How I did it" section points at a real file with a `Source:` path. Where a topic
only ever showed up in a lecture (no code of my own), the page says so plainly and cites
the ECEN 758 lecture instead of pretending I have an implementation.

> **Attribution & privacy.** The ECEN 758 lecture slides are Dr. Joshua Peeples'
> copyrighted course material — this chapter paraphrases concepts and never reproduces
> slides. The CIFAR-100 project was a four-person group project; it is referred to
> throughout as "our group project" without naming teammates. No datasets used here are
> private (CIFAR-100, iris, UCI, and public Census data).

## Notebooks

- [GMM & EM From Scratch](notebooks/gmm-em-from-scratch.ipynb) — the E-step / M-step of
  Expectation-Maximization coded by hand on a Gaussian mixture and the three-coin problem
  (ECEN 758). Re-executed locally.

## Topics

### Fundamentals

- [ML Overview & Workflow](fundamentals/overview.md) — supervised vs unsupervised,
  the bias-variance tradeoff, and how I split/validate.

### Classification

- [k-Nearest Neighbors](classification/knn.md)
- [Naive Bayes](classification/naive-bayes.md)
- [Decision Trees](classification/decision-trees.md)
- [Random Forests](classification/random-forests.md)
- [Support Vector Machines](classification/svm.md)

### Clustering

- [k-Means](clustering/kmeans.md)
- [Hierarchical Clustering](clustering/hierarchical.md)
- [Density-Based Clustering](clustering/density-clustering.md)
- [Gaussian Mixture Models & EM](clustering/gmm-em.md)

### Dimensionality Reduction

- [Principal Component Analysis](dimensionality-reduction/pca.md)

### Ensembles

- [Bagging & Boosting](ensembles/bagging-boosting.md)
- [XGBoost](ensembles/xgboost.md)

### Other Methods

- [Recommender Systems](other/recommenders.md)
- [PageRank & Graph Methods](other/pagerank.md)
- [Frequent Itemset Mining](other/itemset-mining.md)

Neural networks, CNNs, transformers, and the CIFAR-100 case study moved to the
[Deep Learning](deep-learning/index.md) chapter.

## Key Takeaways

- **Know which half you're in.** Supervised (labels) vs unsupervised (structure) changes
  the metric, the validation strategy, and what "done" means.
- **Implement one from scratch.** The EM page (and the backprop and attention pages in
  the Deep Learning chapter) are the ones I understand best precisely because I wrote
  the update rules by hand.
- **Ensembles are the workhorse.** For tabular problems, gradient-boosted trees (XGBoost /
  Spark GBT) were consistently my strongest baseline.
- **Honest sourcing beats coverage.** A few topics here are lecture-only; the page says so
  rather than dressing up a library call as original work.
