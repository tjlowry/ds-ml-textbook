# Support Vector Machines

## Overview

A **Support Vector Machine (SVM)** finds the hyperplane that separates two classes with the
*maximum margin* — the widest possible gap between the boundary and the nearest points of
each class (the "support vectors"). A soft margin allows some violations for
non-separable data, and the **kernel trick** (RBF, polynomial) lets the same idea carve
nonlinear boundaries by implicitly lifting the data into a higher-dimensional space without
computing the coordinates. SVMs shine on small-to-medium, high-dimensional problems with a
clear margin.

**I don't have my own implementation of this one.** SVMs are covered in my ECEN 758 notes
but I never used them in a project or homework I can point to — no from-scratch or applied
code of mine exists for margins/kernels. This page is a concept summary from the lecture;
if I build an SVM later I'll add a real "How I did it" section.

## Gotchas (from the lecture, worth remembering)

- **Scale features first.** The margin is defined by distances, so unscaled features
  distort the hyperplane — standardize before fitting.
- **The kernel and `C` are the whole game.** `C` trades margin width against
  misclassification; the RBF `gamma` sets how local each support vector's influence is.
  Both need cross-validation.
- **Doesn't scale to huge datasets.** Kernel SVMs are roughly quadratic in sample count,
  which is why gradient-boosted trees and neural nets took over most large-scale tabular
  and image tasks.
- **Binary at heart.** Multi-class SVM is built from one-vs-rest or one-vs-one wrappers.

## References

- ECEN 758 Lecture 20 — Support Vector Machines (local:
  `course-files/08-machine-learning/758 Lec 20 Support Vector Machines.pdf`).
  Instructor-copyrighted; concept summary only, no code of my own.
