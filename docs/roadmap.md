# Roadmap

Chapters that existed as stubs and were pruned until they have real content. To write one,
run `/fill-chapter <name>` in Claude Code (see `.claude/skills/fill-chapter/`).

| Chapter | Source material to mine |
|---|---|
| 01 Introduction | `course-files/01-introduction/` |

Pruned stubs are recoverable from git history (commit before "prune stub pages").

> **Note:** Chapters 02 (Linear Algebra), 03 (Statistics), 04 (Data Wrangling), 05 (Exploratory Data Analysis), 06 (Data Visualization), 07 (SQL & Databases), 08 (Machine Learning), 09 (Time Series Forecasting), 10 (Model Evaluation), 11 (Python Programming), and 12 (Scientific Machine Learning & PINNs) are filled. Chapter 05 is deliberately the lightest chapter — the cleaning half lives in ch04 and the polished plots in ch06, so ch05 covers only the exploration/summarization middle step (BYU-Idaho Netflix data-exploration exercise for summary/count techniques, a DS 250 names-popularity notebook for a question-driven distribution read); `star_wars_eda.ipynb` was redundant with the ch04 Star Wars case study and is cited-only. Chapter 12 was never a roadmap row — it was added as an advanced capstone from ECEN 744 (SciML) coursework and the SA-PINN optimizer final project. Chapter 11 was filled from BYU-Idaho CSE 111 assignment code plus STAT 624 Week 1/9/10 lecture concepts. Chapter 10 turned out to be a **synthesis** chapter rather than a mine-one-folder chapter: `course-files/10-model-evaluation/` was empty, the forecast-metric and MASE derivations were already published in ch09, and the classification-metric theory already lived in ch03/ch08 — so ch10 cross-links those and adds the real-code evaluation layer (STAT 650 logistic-regression classification, ECEN 758 GNB-vs-kNN comparison) plus a curated leakage-patterns page.
