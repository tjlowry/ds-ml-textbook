# Deep Learning

## Overview

This chapter is the deep-learning half of what used to be one giant Machine Learning
chapter: the work where I implemented the pieces from scratch — backprop by hand,
convolution arithmetic, attention — rather than calling a library. The
[Machine Learning](../index.md) chapter keeps the classical algorithms (classification,
clustering, ensembles); this one covers neural networks from the single neuron up to
transformers.

It draws on two streams of my own work:

- **ECEN 740 — Machine Learning Engineering (Texas A&M grad).** The deep-learning
  engineering course: two from-scratch projects — an MLP-fundamentals project (backprop,
  initialization, BatchNorm, dropout) and a mini-GPT transformer language model — plus my
  own PyTorch training/debugging reference notes.
- **ECEN 758 — Data Mining and Analysis (Texas A&M grad).** The deep-learning unit and my
  Assignment 4 worked problems (perceptron vs backprop updates), plus the CIFAR-100
  image-classification group project written up as this chapter's case study.

Every "How I did it" section points at a real file with a `Source:` path.

> **Attribution & privacy.** The ECEN 758 lecture slides are Dr. Joshua Peeples'
> copyrighted course material — this chapter paraphrases concepts and never reproduces
> slides. The CIFAR-100 project was a four-person group project; it is referred to
> throughout as "our group project" without naming teammates. No datasets used here are
> private (CIFAR-10/100 are public benchmarks).

## Topics

- [Neural Network Fundamentals](neural-network-fundamentals.md) — the single neuron,
  backprop by hand, vanishing gradients, initialization, BatchNorm, dropout.
- [Convolutional Neural Networks](cnns.md) — convolution/pooling building blocks and the
  architecture choices behind the CIFAR-100 CNN.
- [Transformers & Attention](transformers-attention.md) — multi-head causal
  self-attention and the components of a small GPT.

## Case Study

- [CIFAR-100 Image Classification](../case-study-cifar100.md) — Random Forest vs custom
  CNN vs CLIP transfer learning on 100 classes, and an honest lesson about finishing the
  write-up.

## Notebooks

- [Mini-GPT From Scratch](../notebooks/mini-gpt-from-scratch.ipynb) — byte-level BPE,
  multi-head causal self-attention, RMSNorm, SwiGLU, and top-p decoding, built up
  component by component (ECEN 740).
- [MLP Fundamentals](../notebooks/mlp-fundamentals.ipynb) — backprop by hand, hinge vs
  cross-entropy loss, Xavier/Kaiming init, BatchNorm, and a dropout sweep (ECEN 740).

## Key Takeaways

- **Implement one from scratch.** The backprop and attention pages are the ones I
  understand best precisely because I wrote the update rules by hand.
- **Most training bugs are plumbing.** Dead ReLUs, forgotten `model.eval()`, and bad
  initialization caused more pain in my projects than any architecture decision.
- **Finish the write-up.** The CIFAR-100 case study's sharpest lesson isn't about
  architecture: our group never recorded the CLIP transfer-learning result, so the
  comparison the whole project was built around can't be completed from the report.
