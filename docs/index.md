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
- [Machine Learning](08-machine-learning/index.md) — classification, clustering, ensembles, deep learning (ECEN 758/740)
- [Time Series Forecasting](09-time-series-forecasting/index.md) — senior project + distribution demand forecasting
- [Appendix](appendix/full-textbooks.md) — textbooks and homework archive

Unwritten chapters live on the [Roadmap](roadmap.md).

## Running notebooks locally

Notebooks under `docs/**/notebooks/` are committed with saved outputs. To re-run one:

    cd ~/Projects/personal/textbook
    jupyter lab docs/09-time-series-forecasting/notebooks/

Raw course materials (PDFs, original notebooks, datasets) live in `course-files/` at the
repo root — local-only, never published.
