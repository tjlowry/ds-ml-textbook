# Data Science & ML Textbook

My personal reference, built from my own coursework and projects — the goal is to be able
to come back to any topic and re-learn it from **work I actually did**, not generic notes.

## How each topic page is structured

1. **Summary** — what the concept is and when I'd reach for it.
2. **How I did it** — real code from my projects, each snippet with a `Source:` path.
3. **Notebook** — a rendered notebook you can read here; open the stated local path in
   Jupyter to re-run it.
4. **Gotchas** — what tripped me up.

## Chapters

- [Linear Algebra](02-linear-algebra/index.md) — systems, least squares, eigen/SVD, and optimization (MATH 677)
- [Statistics](03-statistics/index.md) — probability, inference, regression (STAT 650)
- [Data Visualization](06-data-visualization/index.md) — matplotlib/seaborn/plotly, ggplot2, BI
- [SQL & Databases](07-sql-and-databases/index.md) — queries, schema design, Python integration, NoSQL & compute (STAT 624 / DS 250)
- [Machine Learning](08-machine-learning/index.md) — classification, clustering, ensembles, deep learning (ECEN 758/740)
- [Time Series Forecasting](09-time-series-forecasting/index.md) — senior project + distribution demand forecasting
- [Model Evaluation](10-model-evaluation/index.md) — metrics, cross-validation, and leakage, synthesized across chapters (STAT 650 / ECEN 758)
- [Scientific Machine Learning & PINNs](12-scientific-ml/index.md) — physics-informed neural networks + SA-PINN optimizer study (ECEN 744)
- [Sources](sources.md) — per-chapter ledger of the files each page was built from
- [Appendix](appendix/full-textbooks.md) — textbooks and homework archive

Unwritten chapters live on the [Roadmap](roadmap.md).

## Running notebooks locally

Notebooks under `docs/**/notebooks/` are committed with saved outputs. To re-run one:

    cd ~/Projects/personal/textbook
    jupyter lab docs/09-time-series-forecasting/notebooks/

Raw course materials (PDFs, original notebooks, datasets) live in `course-files/` at the
repo root — local-only, never published.
