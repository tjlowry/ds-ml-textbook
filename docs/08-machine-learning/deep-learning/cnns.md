# Convolutional Neural Networks

## Overview

A **Convolutional Neural Network (CNN)** slides learnable filters over an image, building up
a hierarchy of features — early layers detect edges and textures, deeper layers compose them
into object parts and whole objects. Weight sharing (the same filter everywhere) and
pooling (downsampling) give CNNs translation tolerance and far fewer parameters than a
fully-connected net on the same image, which is why they dominate image classification.

I worked with CNNs in our ECEN 758 CIFAR-100 group project, where a custom CNN was the
centerpiece model against classical baselines.

## How I did it

!!! note "Full case study"
    This section summarizes the CNN track; the complete write-up of the project — all three
    approaches, the EDA, the accuracy figure, and the honest lessons — lives on the
    [CIFAR-100 case-study page](../case-study-cifar100.md).

Our group project on CIFAR-100 (100 classes, 32×32 color images) built up through three
increasingly capable approaches, which is a nice illustration of *why* CNNs win on images:

1. **Random Forest + HOG features** — a classical baseline. HOG features feeding a
   100-tree forest reached about **22% accuracy**. Real signal over the 1% random rate,
   but capped by hand-designed features.
2. **A custom CNN** — three convolutional blocks, each using 3×3 kernels to capture local
   spatial structure, with max-pooling to shrink spatial resolution while growing feature-map
   depth. Trained for 25 epochs (where loss/accuracy stabilized) with the Adam optimizer at
   learning rate 0.001, L2 weight regularization, and cross-entropy loss. The first CNN run
   reached about **52% accuracy** — more than double the random-forest baseline.
3. **CLIP-based transfer learning** — using a pretrained vision-language model's features
   as a stronger transfer-learning approach.

Source: our ECEN 758 CIFAR-100 group project report
(`course-files/appendix/Homework/ecen758_hw/group_project/CNN_draft2.pdf` and
`ecen758_group_report.pdf`)

The takeaway from that progression: the random forest needed *me* to design features (HOG);
the CNN **learned** its own filters end to end, which is exactly why it jumped from 22% to
52% on the same data. (These are the group's reported numbers from a draft report; the
final write-up's results section was still in progress.)

The two operations that make up each of those convolutional blocks are worth seeing
concretely. A 3×3 kernel slides over the input and each window position produces one cell of
the feature map (with ReLU applied); then 2×2 max-pooling downsamples that map, keeping the
strongest response in each little window. The schematic below traces one window through both
stages — the same 3×3-kernel-plus-max-pool building blocks our CIFAR-100 CNN stacked three
times.

![Convolution-and-pooling schematic. An 8×8 input has a 3×3 kernel window highlighted, with an
arrow to the single cell it produces in the 6×6 feature map (8 − 3 + 1 = 6, stride 1, valid,
plus ReLU). A 2×2 window on the feature map maps by max-pooling to one cell of the 3×3 pooled
map (6 / 2 = 3). These are the building blocks of the CIFAR-100 CNN's convolutional
blocks.](../img/cnn-conv-pool.png)

## Course notebook

The ECEN 740 material's deep-learning lecture (ECEN 758 Lecture 22) references a repository
of convolution-arithmetic animations that make the kernel/stride/padding mechanics click:
<https://github.com/vdumoulin/conv_arithmetic> (URL extracted from the lecture PDF).

## Gotchas

- **Learned features beat hand-crafted ones on images.** The whole point of the 22% → 52%
  jump: don't hand-design HOG features if you can let convolutions learn them.
- **Pick epochs by the curve, not a guess.** The project used 25 epochs *because* that's
  where training loss and accuracy flattened — more would just risk overfitting.
- **Regularize deep nets.** L2 weight decay plus (from the fundamentals work) dropout and
  BatchNorm are what keep a CNN from memorizing the training set.
- **100 classes is hard.** 52% top-1 on CIFAR-100 sounds low next to CIFAR-10 numbers, but
  chance is 1% and the classes are fine-grained — context matters when reading accuracy.
- **It was a group effort.** This was a four-person project; the CNN, random-forest, and
  CLIP tracks were divided across the team.

## References

- ECEN 758 Lecture 22 — Deep Learning (local:
  `course-files/08-machine-learning/758 Lec 22 Deep Learning.pdf`).
  Instructor-copyrighted; concept summary only.
