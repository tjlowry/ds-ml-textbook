# Roadmap

Chapters that existed as stubs and were pruned until they have real content. To write one,
run `/fill-chapter <name>` in Claude Code (see `.claude/skills/fill-chapter/`).

| Chapter | Source material to mine |
|---|---|
| 01 Introduction | `course-files/01-introduction/` |
| 04 Data Wrangling | `course-files/04-data-wrangling/`, DS 250 work |
| 05 Exploratory Data Analysis | `course-files/05-exploratory-data-analysis/` (star wars, name-pop EDA notebooks) |
| 07 SQL & Databases | `course-files/07-sql-and-databases/` |
| 10 Model Evaluation | `course-files/10-model-evaluation/`, distribution demand-forecasting evaluation code |
| 11 Python Programming | `course-files/11-python-programming/` (week 9–10 notebooks) |
| Appendix: cheat sheets | rewrite from scratch as they become useful |

Pruned stubs are recoverable from git history (commit before "prune stub pages").

> **Note:** Chapters 02 (Linear Algebra), 08 (Machine Learning), and 09 (Time Series Forecasting) are filled. When filling **10 Model Evaluation**, mine its two notebooks and the distribution demand-forecasting evaluation code they draw on — `09-time-series-forecasting/notebooks/` plus `demand-forecast/src/evaluation/metrics.py` (private distribution-forecasting repo; MASE, under/zero-forecast ratios) — so metric definitions stay consistent across chapters instead of being re-derived.
