# Machine Learning

## Overview

This chapter is the "how I actually built the model" companion to the more
statistics-flavored chapters. It covers the classic supervised and unsupervised
algorithms, the ensemble methods I reach for most, and the deep-learning work where I
implemented the pieces from scratch rather than calling a library.

It draws on three streams of my own work:

- **ECEN 758 — Data Mining and Analysis (Texas A&M grad).** Dr. Peeples' course: the
  clustering / classification / dimensionality-reduction backbone. My contributions are
  the homework notebooks (from-scratch EM, hierarchical/density clustering, PCA, applied
  kNN/Naive Bayes) and a CIFAR-100 image-classification group project.
- **ECEN 740 — Machine Learning Engineering (Texas A&M grad).** The deep-learning
  engineering course: two from-scratch projects — an MLP-fundamentals project (backprop,
  initialization, BatchNorm, dropout) and a mini-GPT transformer language model — plus my
  own PyTorch training/debugging reference notes.
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

- [Mini-GPT From Scratch](notebooks/mini-gpt-from-scratch.ipynb) — byte-level BPE,
  multi-head causal self-attention, RMSNorm, SwiGLU, and top-p decoding, built up
  component by component (ECEN 740).
- [MLP Fundamentals](notebooks/mlp-fundamentals.ipynb) — backprop by hand, hinge vs
  cross-entropy loss, Xavier/Kaiming init, BatchNorm, and a dropout sweep (ECEN 740).
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

### Deep Learning

- [Neural Network Fundamentals](deep-learning/neural-network-fundamentals.md)
- [Convolutional Neural Networks](deep-learning/cnns.md)
- [Transformers & Attention](deep-learning/transformers-attention.md)

### Other Methods

- [Recommender Systems](other/recommenders.md)
- [PageRank & Graph Methods](other/pagerank.md)
- [Frequent Itemset Mining](other/itemset-mining.md)

## Key Takeaways

- **Know which half you're in.** Supervised (labels) vs unsupervised (structure) changes
  the metric, the validation strategy, and what "done" means.
- **Implement one from scratch.** The EM, backprop, and attention pages are the ones I
  understand best precisely because I wrote the update rules by hand.
- **Ensembles are the workhorse.** For tabular problems, gradient-boosted trees (XGBoost /
  Spark GBT) were consistently my strongest baseline.
- **Honest sourcing beats coverage.** A few topics here are lecture-only; the page says so
  rather than dressing up a library call as original work.
