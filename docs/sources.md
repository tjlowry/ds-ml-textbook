# Source Manifest

This page tracks every source file I've consulted while writing each chapter, and what
happened to its content: excerpted as a code snippet, re-typeset as a worked example,
paraphrased into prose, promoted into a runnable notebook, used as the basis for a
regenerated figure, linked without incorporating its content, read and set aside, or (for
SQL) inventoried ahead of a chapter that hasn't been drafted yet. The point is to answer
one question fast: **"did I already use this file, and if so, where?"** — so a
half-remembered PDF or notebook I stumble across later doesn't get re-read from scratch or,
worse, silently duplicated into a second page.

## How to check a new file

1. **Grep this page for the filename** (basename is usually enough — paths get long):
   `grep -i "some_file.ipynb" docs/sources.md`
   If it shows up, the disposition column tells you what happened to it and the "landed"
   column tells you where to go read the result.
2. **Not found here?** Check the chapter's topic pages directly for a `Source:` line —
   this manifest is generated from those lines plus the inventory/report notes, so it
   should be complete, but the pages are the ultimate ground truth:
   `git grep -n 'Source:' docs/<chapter>/`
3. **Suspect an exact duplicate** (e.g. you found a second copy of a PDF/notebook in a
   different folder)? Compare checksums instead of eyeballing filenames:
   `md5 "course-files/path/to/file.pdf"` (macOS) and compare against the path recorded
   here for the same topic — if the hash matches a file already listed, it's the same
   content under a different name/location, not new material.
4. Still unsure after both checks → treat it as new and read it; then add a row here
   (see the `fill-chapter` skill, Step 2, for the exact instruction to do this going
   forward).

### Dispositions

| Disposition | Meaning |
|---|---|
| `snippet` | Code excerpted onto a page under "How I did it" |
| `worked-example` | Handwritten/scanned HW re-typeset as a worked example |
| `summarized` | Concepts paraphrased into prose; nothing copied verbatim |
| `promoted-notebook` | Copied, cleaned, and committed into `docs/**/notebooks/` |
| `figure-basis` | A committed figure was remade from this file's concept/data |
| `cited-only` | Linked or pointed to; its content was not incorporated |
| `examined-not-used` | Read during inventory, ultimately not used for this chapter |
| `inventoried-pending` | Surveyed for chapter 07 (SQL), which is not yet drafted |

---

## Chapter 02 — Linear Algebra (MATH 677, TAMU)

Inventory: `.superpowers/sdd/ch02-inventory.md` · Report: `.superpowers/sdd/ch02-report.md`

| Path | Disposition | Where it landed |
|---|---|---|
| `course-files/02-linear-algebra/1+Solving+linear+systems+complete.pdf` | summarized | `02-linear-algebra/linear-systems.md` |
| `course-files/02-linear-algebra/2 Solving least squares complete.pdf` | summarized | `02-linear-algebra/least-squares.md` |
| `course-files/02-linear-algebra/3A Eigenvalues and eigenvectors complete.pdf` | summarized | `02-linear-algebra/eigenvalues-eigenvectors.md` |
| `course-files/02-linear-algebra/3B Eigenvalues and eigenvectors complete.pdf` | summarized | `02-linear-algebra/eigenvalues-eigenvectors.md` |
| `course-files/02-linear-algebra/4 SVD complete (1).pdf` | summarized | `02-linear-algebra/svd.md` |
| `course-files/02-linear-algebra/5 Perron-Frobenius complete.pdf` | summarized | `02-linear-algebra/perron-frobenius.md` |
| `course-files/02-linear-algebra/6+Dynamic+programming+complete.pdf` | summarized | `02-linear-algebra/dynamic-programming.md` |
| `course-files/02-linear-algebra/7 General optimization complete.pdf` | summarized | `02-linear-algebra/gradient-descent.md` (also cross-ref in `svd.md`) |
| `course-files/02-linear-algebra/8 Steepest descent complete.pdf` | summarized | `02-linear-algebra/gradient-descent.md` |
| `course-files/02-linear-algebra/9 Convex optimization complete.pdf` | summarized | `02-linear-algebra/convex-optimization.md` |
| `course-files/02-linear-algebra/10 Compressed sensing complete.pdf` | summarized | `02-linear-algebra/compressed-sensing.md` |
| `course-files/02-linear-algebra/Theorem list.pdf` (BYU-I M341, misfiled — not MATH 677) | worked-example | `02-linear-algebra/theorem-reference.md` (re-typeset in own wording/layout) |
| `course-files/02-linear-algebra/FinalExamReviewLinearAlgebra.pdf` (BYU-I M341, misfiled) | examined-not-used | — |
| `course-files/02-linear-algebra/proj_gradient.py` (Tyler's own code) | snippet, promoted-notebook | `02-linear-algebra/gradient-descent.md`; `02-linear-algebra/notebooks/projected-gradient-descent.ipynb` |
| `course-files/appendix/Homework/math_677_linAlg/linear_algebra_hw/` (whole subfolder: BYU-I M341 exam/cheatsheets/HW1-1…HW6-7/textbook PDF — not MATH 677) | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/1 Solving linear systems.pdf` (duplicate of Lecture 1 PDF) | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/fibonacci.py` (Tyler's own code, instructor skeleton + his loop) | snippet | `02-linear-algebra/dynamic-programming.md` |
| `course-files/appendix/Homework/math_677_linAlg/HW1_written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/HW2_written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/HW3_Written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/Hw4.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/HW 5 Written.pdf` | worked-example | `02-linear-algebra/least-squares.md` (normal equations, x=[6/11,−1/33]) |
| `course-files/appendix/Homework/math_677_linAlg/HW 6 Written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/HW 7 Written.pdf` | worked-example | `02-linear-algebra/eigenvalues-eigenvectors.md` (power-method convergence ≈24 iters) |
| `course-files/appendix/Homework/math_677_linAlg/Hw 8 written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/Hw 9 written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/Hw 10 written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/Hw 11 written.pdf` | worked-example | `02-linear-algebra/gradient-descent.md` (steepest descent by hand, Armijo/Wolfe, Newton's method) |
| `course-files/appendix/Homework/math_677_linAlg/Hw12_written.pdf` | examined-not-used | — |
| `course-files/appendix/Homework/math_677_linAlg/Hw13 written.pdf` | examined-not-used | — |
| `~/Projects/personal/nfl_prospect_recommender/.../nmf_model.py` (sklearn NMF) | examined-not-used | considered as SVD/low-rank motivation, not promoted (library call, not hand-derived) |
| `~/Projects/personal/nfl_prospect_recommender/.../implicit_model.py` (implicit ALS/BPR) | examined-not-used | considered as least-squares motivation, not promoted |
| `~/Projects/research/.../biomed_research/02_spateo_3d_reconstruction.ipynb` (PCA step) | examined-not-used | considered as SVD/PCA motivation, not promoted (calls `dyn.tl.reduceDimension`) |

## Chapter 03 — Statistics

**Legacy — written before source tracking.** Chapter 03 predates the inventory/report/`Source:`-line
workflow used for 02/08/09, so there is no file-level manifest to reconstruct honestly. Known
origins, from memory and the content's own style: **STAT 650 weekly notebooks** (TAMU) for
inference/regression pages, and general **DS 350 R coursework** (BYU-Idaho) influence on some
descriptive-stats framing. If chapter 03 is ever re-passed through the `fill-chapter` workflow,
replace this note with real rows.

## Chapter 06 — Data Visualization

**Legacy — written before source tracking.** Same situation as chapter 03: no inventory/report
exists for this chapter. Known origins: **STAT 650 weekly notebooks** (TAMU) for the Python
plotting pages (matplotlib/seaborn/plotly), and **DS 350 R coursework** (BYU-Idaho) for the
`ggplot2`/grammar-of-graphics pages. BI (DAX/dashboards) and best-practices pages have no
specific traceable source. If chapter 06 is ever re-passed through `fill-chapter`, replace this
note with real rows.

## Chapter 08 — Machine Learning (ECEN 758/740, TAMU + BYU-Idaho side material)

Inventory: `.superpowers/sdd/ch08-inventory.md` · Report: `.superpowers/sdd/ch08-report.md`

| Path | Disposition | Where it landed |
|---|---|---|
| `course-files/08-machine-learning/758 Lec 04 Dimensionality Reduction.pdf` | summarized | `08-machine-learning/dimensionality-reduction/pca.md` |
| `course-files/08-machine-learning/758 Lec 05 Frequent Itemset Mining and Association Rules.pdf` | summarized | `08-machine-learning/other/itemset-mining.md` |
| `course-files/08-machine-learning/758 Lec 06 Representative Clustering I.pdf` | summarized | `08-machine-learning/clustering/kmeans.md` |
| `course-files/08-machine-learning/758 Lec 07 Representative Clustering II.pdf` | summarized | `08-machine-learning/clustering/kmeans.md` |
| `course-files/08-machine-learning/758 Lec 08 Gaussian Mixture Models (1).pdf` | summarized | `08-machine-learning/clustering/gmm-em.md` |
| `course-files/08-machine-learning/758 Lec 09 EM Algorithm (1).pdf` | summarized | `08-machine-learning/clustering/gmm-em.md` |
| `course-files/08-machine-learning/758 Lec 10 Hierarchical Clustering.pdf` | summarized | `08-machine-learning/clustering/hierarchical.md` |
| `course-files/08-machine-learning/758 Lec 11 Density_based Clustering (1).pdf` | summarized | `08-machine-learning/clustering/density-clustering.md` |
| `course-files/08-machine-learning/758 Lec 12 Bayesian and Nearest Neighbor Classification.pdf` | summarized | `08-machine-learning/classification/knn.md`, `08-machine-learning/classification/naive-bayes.md` |
| `course-files/08-machine-learning/758 Lec 13 Decision Tree Classification.pdf` | summarized | `08-machine-learning/classification/decision-trees.md`, `08-machine-learning/classification/random-forests.md` |
| `course-files/08-machine-learning/758 Lec 14 Graphs, Pagerank and Search.pdf` | summarized | `08-machine-learning/other/pagerank.md` |
| `course-files/08-machine-learning/758 Lec 15 Recommendation Systems I.pdf` | summarized | `08-machine-learning/other/recommenders.md` |
| `course-files/08-machine-learning/758 Lec 16 Recommendation Systems II.pdf` | summarized | `08-machine-learning/other/recommenders.md` |
| `course-files/08-machine-learning/758 Lec 18 Linear Regression*.pdf` | examined-not-used | belongs conceptually to statistics chapter, not cited in ch08 pages |
| `course-files/08-machine-learning/758 Lec 19 Logistic Regression*.pdf` | examined-not-used | same as above |
| `course-files/08-machine-learning/758 Lec 20 Support Vector Machines.pdf` | summarized | `08-machine-learning/classification/svm.md` (lecture-only, no code of mine) |
| `course-files/08-machine-learning/758 Lec 20 Support Vector Machines (1).pdf` (duplicate) | examined-not-used | duplicate download, see flags in inventory |
| `course-files/08-machine-learning/758 Lec 22 Deep Learning.pdf` | summarized | `08-machine-learning/deep-learning/cnns.md` |
| `course-files/appendix/Homework/ecen758_hw/HW 1/ECEN758_HW1.ipynb` | snippet | `08-machine-learning/fundamentals/overview.md`, `08-machine-learning/dimensionality-reduction/pca.md` |
| `course-files/appendix/Homework/ecen758_hw/HW 2/hw2.ipynb` | snippet, promoted-notebook | `08-machine-learning/clustering/gmm-em.md`; `08-machine-learning/notebooks/gmm-em-from-scratch.ipynb` |
| `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb` | snippet | `08-machine-learning/classification/knn.md`, `naive-bayes.md`; `08-machine-learning/clustering/kmeans.md`, `hierarchical.md`, `density-clustering.md` |
| `course-files/appendix/Homework/ecen758_hw/group_project/ecen758_group_report.pdf` | summarized | `08-machine-learning/classification/random-forests.md`, `08-machine-learning/deep-learning/cnns.md`, `08-machine-learning/dimensionality-reduction/pca.md` |
| `course-files/appendix/Homework/ecen758_hw/group_project/CNN_draft2.pdf` | summarized | `08-machine-learning/deep-learning/cnns.md` |
| `course-files/appendix/Homework/ecen758_hw/group_project/data_explore.ipynb` | examined-not-used | not promoted (parent dir 355MB incl. CIFAR-100 binaries + 13MB checkpoint) |
| `course-files/appendix/Homework/ecen758_hw/group_project/best_model.pth` | examined-not-used | — |
| `course-files/appendix/Homework/ecen758_hw/group_project/` (CIFAR-100 train/test binaries) | examined-not-used | — |
| `course-files/appendix/Homework/ecen758_hw/two_stage_pipeline.py` | examined-not-used | flagged misfiled (unrelated YOLO/U-Net scaffolding), excluded entirely |
| `course-files/08-machine-learning/swampdonkey_ml_model.ipynb` (BYU-I capstone, misfiled into TAMU folder) | snippet | `08-machine-learning/ensembles/bagging-boosting.md` |
| `course-files/08-machine-learning/week08-lesson2 - decision tree.ipynb` (DataCamp-tutorial-derived) | examined-not-used | — |
| `course-files/08-machine-learning/week08-lesson2 - random forest.ipynb` (DataCamp-tutorial-derived) | examined-not-used | — |
| `course-files/08-machine-learning/Week12. scikit-learn.ipynb` ("© Scott A. Bruce. Do not distribute.") | examined-not-used | never quoted or promoted (confirmed via privacy grep) |
| `course-files/08-machine-learning/random_forest_classifier.qmd` (Tyler's own, DS 250/BYU-Idaho) | snippet | `08-machine-learning/classification/decision-trees.md`, `random-forests.md`, `08-machine-learning/fundamentals/overview.md` |
| `course-files/08-machine-learning/ds250_challenge.py` | examined-not-used | scaffolding-dominated, minor value |
| `course-files/appendix/Homework/cse450_hw/Team4-Module2-Executive-Summary.pdf` (names 4 teammates) | examined-not-used | — |
| `course-files/appendix/Homework/cse450_hw/` (4 prediction CSVs + blank `executive-summary.docx`) | examined-not-used | — |
| `~/Projects/school/tamu-grad/ecen740/Copy_of_ECEN740_Project1.ipynb` | snippet, promoted-notebook | `08-machine-learning/deep-learning/neural-network-fundamentals.md`; `08-machine-learning/notebooks/mlp-fundamentals.ipynb` |
| `~/Projects/school/tamu-grad/ecen740/ECEN740_project3.ipynb` | snippet, promoted-notebook | `08-machine-learning/deep-learning/transformers-attention.md`; `08-machine-learning/notebooks/mini-gpt-from-scratch.ipynb` |
| `~/Projects/school/tamu-grad/ecen740/PyTorch_Training_Guide.ipynb` | snippet | `08-machine-learning/deep-learning/neural-network-fundamentals.md` (5 named bugs) |
| `~/Projects/school/tamu-grad/stat654/presentation/654Project2.ipynb` | snippet | `08-machine-learning/ensembles/xgboost.md`, `08-machine-learning/fundamentals/overview.md` |
| `~/Projects/personal/nfl_prospect_recommender/src/models/ensemble.py` | snippet | `08-machine-learning/other/recommenders.md` |
| `~/Projects/personal/nfl_prospect_recommender/src/similarity/gm_similarity.py` | snippet | `08-machine-learning/other/recommenders.md` |
| `~/Projects/personal/nfl_prospect_recommender/claude.md` | summarized | `08-machine-learning/other/recommenders.md` |
| `~/Projects/personal/{baseball_sim,dbacks-batting-sim}` (R Markdown baseball sim) | examined-not-used | not ML material |
| `~/Projects/friends-family/family-hist-app` (Laravel/PHP) | examined-not-used | not ML material |

## Chapter 09 — Time Series Forecasting (senior project + production forecasting work)

Inventory: `.superpowers/sdd/task-6-inventory.md` · Report: `.superpowers/sdd/task-6-report.md`

| Path | Disposition | Where it landed |
|---|---|---|
| `course-files/09-time-series-forecasting/time-series-forecasting/forecasting-pipeline.py` | snippet | `09-time-series-forecasting/fundamentals/stationarity.md`, `seasonality-trends.md`, `autocorrelation.md`; `statistical/naive-methods.md`, `ets.md`, `arima.md`, `sarima.md`; `ml/feature-engineering.md`, `xgboost.md`; `transformations/log.md`, `sqrt.md`, `box-cox.md`, `differencing.md`; `evaluation/metrics.md`, `comparison.md` |
| `course-files/09-time-series-forecasting/time-series-forecasting/resampling-utilities.py` | snippet | `09-time-series-forecasting/fundamentals/concepts.md` |
| `course-files/09-time-series-forecasting/time-series-forecasting/forecast-visualization.py` | examined-not-used | fabricated-data illustrative script, not a snippet source |
| `course-files/09-time-series-forecasting/time-series-forecasting/synthetic-data-generator.py` | promoted-notebook | basis for `09-time-series-forecasting/notebooks/senior-project-pipeline.ipynb` |
| `course-files/09-time-series-forecasting/time-series-forecasting/streamlit-dashboard-main.py` | examined-not-used | broken imports as checked out, not executable |
| `course-files/09-time-series-forecasting/time-series-forecasting/streamlit-data-overview.py` | examined-not-used | considered as EDA-workflow background reading, not directly cited |
| `course-files/09-time-series-forecasting/time-series-forecasting/streamlit-model-comparison.py` | examined-not-used | considered as background reading, not directly cited |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/takeaways.md` | summarized | Gotchas sections across `transformations/`, `evaluation/`; `transformations/yeo-johnson.md` |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/model_info.md` | summarized | `09-time-series-forecasting/fundamentals/concepts.md` and general prose backbone |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/steps.md` | examined-not-used | trivial one-line stub |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/outline.md` | summarized | `09-time-series-forecasting/index.md` (scoped "planned vs implemented"), `ml/random-forest.md` |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/Questions.md` | examined-not-used | — |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/data_Privacy.py` | examined-not-used | privacy flag only (obfuscation script, not anonymization) — not incorporated |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/` (raw real demand-history export, private ERP source) | examined-not-used | private, never published |
| `course-files/09-time-series-forecasting/time-series-forecasting/retail_data.csv`, `daily_sales.csv` | examined-not-used | derived from real data, not used as the public/runnable dataset |
| `course-files/09-time-series-forecasting/time-series-forecasting/docs/time_series_outputs/*.png`, `time_series_plot.png` | examined-not-used | not embedded; plots regenerated from synthetic data instead |
| `demand-forecast/README.md` (private distribution-forecasting repo) | summarized | `09-time-series-forecasting/index.md` |
| `demand-forecast/docs/technical_summary.md` (private distribution-forecasting repo) | summarized | `09-time-series-forecasting/index.md`, `evaluation/selection-framework.md` |
| `demand-forecast/src/features/lag.py` (private distribution-forecasting repo; `LagFeatureEngineer.transform`) | snippet | `09-time-series-forecasting/ml/feature-engineering.md` |
| `demand-forecast/src/features/rolling.py` (private distribution-forecasting repo; `RollingFeatureEngineer._calculate_rolling_stat`) | snippet | `09-time-series-forecasting/ml/feature-engineering.md` |
| `demand-forecast/src/features/demand_patterns.py` (private distribution-forecasting repo; simplified reconstruction) | snippet | `09-time-series-forecasting/evaluation/selection-framework.md` |
| `demand-forecast/src/features/temporal.py`, `hierarchical.py`, `base.py` (private distribution-forecasting repo) | examined-not-used | secondary, not directly cited |
| `demand-forecast/tests/test_data_leakage.py` (private distribution-forecasting repo) | summarized | leakage-assertion pattern mirrored in `09-time-series-forecasting/notebooks/distribution-feature-engineering-demo.ipynb` |
| `demand-forecast/src/evaluation/metrics.py` (private distribution-forecasting repo; `mase`) | snippet | `09-time-series-forecasting/evaluation/metrics.md` |
| `demand-forecast/src/ensemble/weighted.py` (private distribution-forecasting repo; `WeightedEnsemble._optimize_weights`) | snippet | `09-time-series-forecasting/evaluation/comparison.md` |
| `demand-forecast/src/data/preprocessor.py` (private distribution-forecasting repo) | summarized | `09-time-series-forecasting/transformations/log.md` (log-transform-as-config) |
| `demand-forecast/src/pipeline.py` (private distribution-forecasting repo) | summarized | `09-time-series-forecasting/index.md` (high-level "how it's wired together") |
| `demand-forecast/legacy/forecast.py` (private distribution-forecasting repo) | summarized | evolution narrative contrast, `statistical/naive-methods.md` |
| `demand-forecast/docs/legacy_comparison.md`, `new_methods_report.md`, `previous_model_report.md`, `docs_vs_reality.md`, `blind_audit.md` (private distribution-forecasting repo) | examined-not-used | skimmed for potential Gotchas material, not directly drawn from |
| `demand-forecast/notebooks/forecast_eda.ipynb` (private distribution-forecasting repo) | examined-not-used | contains real stock IDs in outputs, cannot be published |
| `demand-forecast/notebooks/chronos2_benchmark.ipynb` (private distribution-forecasting repo) | examined-not-used | out of scope for this chapter |
| `demand-forecast/outputs/evaluation_200stocks_report.ipynb` (private distribution-forecasting repo) | examined-not-used | — |
| `demand-forecast/models/*`, real demand-history exports, `brame_demand/models/*` (private distribution-forecasting repo) | examined-not-used | private, never published |
| `scripts/` top-level (`brame_prophet.py`, `functions.py`, notebooks; private distribution-forecasting repo) | examined-not-used | lower quality/superseded, historical color only |
| `monthly_forecast-2024/` (private distribution-forecasting repo) | examined-not-used | superseded by `demand-forecast/`, same privacy concerns |

## Chapter 07 — SQL & Databases (STAT 624, TAMU + DS 250, BYU-Idaho)

Inventory: `.superpowers/sdd/ch07-inventory.md` · Report: `.superpowers/sdd/ch07-report.md`

Deliberately lighter chapter (6 pages + 1 notebook). STAT 624 lecture material is
instructor/TA-copyrighted — every row below sourced from it is `summarized` (concepts
paraphrased, nothing quoted, no executed outputs reproduced).

| Path | Disposition | Where it landed |
|---|---|---|
| `course-files/07-sql-and-databases/Week 2_Docker.pdf` | summarized | `07-sql-and-databases/docker-and-compute.md` |
| `course-files/07-sql-and-databases/STAT624_Docker_082523.pdf` | summarized | `07-sql-and-databases/docker-and-compute.md` (© 2023 Scott A. Bruce, do-not-distribute; cited-only, not reproduced) |
| `course-files/07-sql-and-databases/Week 3_RDBM.pdf` | summarized | `07-sql-and-databases/schema-design.md` (© 2023 Scott A. Bruce; relational-fundamentals framing) |
| `course-files/07-sql-and-databases/Week 4_Basics of SQL.pdf` | examined-not-used | SQL basics covered from Tyler's own DS 250 queries instead; lecture not directly cited |
| `course-files/07-sql-and-databases/Week 6_Aggregation_Window Functions.pdf` | summarized | `07-sql-and-databases/sql-essentials.md` (aggregation/window-function concept source) |
| `course-files/07-sql-and-databases/Week 11_NoSQL (1).pdf` | summarized | `07-sql-and-databases/database-types.md` (© 2023 Scott A. Bruce; CAP/NoSQL categories paraphrased) |
| `course-files/07-sql-and-databases/Week7_sqlalchemy_pythonintro.ipynb` | summarized | `07-sql-and-databases/python-and-databases.md` (© Texas A&M; SQLAlchemy/Postgres concept source, cited-only, needs live docker Postgres) |
| `course-files/07-sql-and-databases/Week13_daskparallelization.ipynb` | summarized | `07-sql-and-databases/docker-and-compute.md` (© Scott A. Bruce, do-not-distribute; Dask concepts, not reproduced) |
| `course-files/07-sql-and-databases/Week14_Dask_Scheduler_Cluster (1).ipynb` | summarized | `07-sql-and-databases/docker-and-compute.md` (© Seung-Yeon Ha 2025; HPC/cluster concepts, needs TAMU HPRC, cited-only) |
| `course-files/07-sql-and-databases/Dask-Ch13_ML (2).ipynb` | examined-not-used | copied O'Reilly "Scaling Python with Dask" book code, not Tyler's; excluded |
| `course-files/07-sql-and-databases/db_assignment/pokemon_erd.sql` | snippet, figure-basis, promoted-notebook | `07-sql-and-databases/schema-design.md` (ERD remade as mermaid, bugs → Gotchas); `07-sql-and-databases/notebooks/pokemon-sql.ipynb` (adapted to SQLite) |
| `course-files/07-sql-and-databases/db_assignment/Queries.txt` | snippet | `07-sql-and-databases/sql-essentials.md` (master-key LEFT JOIN pattern); notebook |
| `course-files/07-sql-and-databases/db_assignment/Stuff for Insert Into.txt` | snippet | `07-sql-and-databases/notebooks/pokemon-sql.ipynb` (region/generation/rarity seed data) |
| `course-files/07-sql-and-databases/db_assignment/pokemon.mwb`, `How to add a pokemon.txt`, `sql_converter.py`, `pokemon_test.csv` | examined-not-used | binary model file / workflow notes / loader script — not incorporated |
| `course-files/07-sql-and-databases/baseball-report-sql.qmd`, `baseball-sql-analysis.py`, `sqlite.py`, `week06.ipynb` | examined-not-used | superseded by the better self-contained copy in DS_250/Project 3 (below) |
| `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.qmd` | snippet | `07-sql-and-databases/sql-essentials.md`, `python-and-databases.md` (real SELECT/JOIN/GROUP BY queries) |
| `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.py` | snippet | `07-sql-and-databases/python-and-databases.md` (sqlite3 + pandas pattern) |
| `~/Projects/school/byui-undergrad/DS_250/Project 3/lahmansbaseballdb.sqlite` (66 MB, referenced by absolute path, never copied into repo) | snippet | `07-sql-and-databases/notebooks/pokemon-sql.ipynb` (Part 2 baseball queries, executed live) |
| `~/Projects/personal/investing/databasemanager.py` | snippet | `07-sql-and-databases/python-and-databases.md` (pymysql context-managed connections, parameterized queries) |
| `~/Projects/friends-family/family-hist-app` (Laravel migrations) | examined-not-used | schema-as-code paradigm not needed once Pokemon ERD covered schema design |

## Appendix

The appendix pages (`docs/appendix/full-textbooks.md`, `misc-homework.md`,
`external-resources.md`, `miscellaneous.md`) are themselves raw indexes of local file paths —
homework PDFs, full textbook chapters, syllabi, and external links — linked for reference but
not narratively incorporated into any chapter page. Every file listed on those four pages is
effectively `cited-only` by definition; rather than duplicate hundreds of rows here, check
those pages directly (they're already organized by course/topic and are just as greppable):

    git grep -n 'Local:' docs/appendix/

No separate inventory/report exists for the appendix — it is maintained by hand as files are
added to `course-files/`.

## Chapter 12 — Scientific Machine Learning & PINNs

Course: **ECEN 744 Scientific Machine Learning**, Texas A&M, Spring 2026, instructor
Ulisses Braga-Neto. The final project is joint work with a project teammate, built on Levi
McClenny's public SA-PINN codebase.

| File | Author | How it's used | Page(s) |
|---|---|---|---|
| `~/Projects/school/tamu-grad/sciml/sciml_hw1.py` | **mine** (HW1) | Euler/Backward Euler/Heun/RK4 snippets + convergence table | Discretization & Autodiff |
| `~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/generate_ks_data.py` | **mine** | ETDRK4 spectral reference generator snippet | Discretization & Autodiff |
| `.../ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py` | **mine** (primary author) | SA-PINN loop, ascent-on-λ, two-phase dispatch, input normalization, 4th-order residual | SA-PINNs, Optimizer Study |
| `.../ECEN744-FinalProject-SA-PINNs/Results/*/results_summary.csv`, `training_loss.csv`, `lbfgs_loss.csv` | co-authored (team) | committed run data → figures + results notebook (small CSVs copied/downsampled into `notebooks/data/`) | Results & Lessons, notebook 2 |
| `.../ECEN744-FinalProject-SA-PINNs/docs/method.tex`, `docs/results_section.tex` | co-authored (team) | equations + results narrative, cross-checked against the CSVs | SA-PINNs, Optimizer Study, Results |
| `.../ECEN744-FinalProject-SA-PINNs/README.md` | co-authored (team) | run commands + SciPy-patch reproducibility caveat | Optimizer Study, Results |
| `.../ECEN744-FinalProject-SA-PINNs/Optimizers/learnable_optimizer.py`, `pinn_quasi_newton.py`, patched `_minimize.py`/`_optimize.py` | **project teammate** + vendored SciPy fork | referenced (named as teammate's / upstream), **not reproduced** | Optimizer Study |
| `~/Projects/school/tamu-grad/sciml/L2_Discretization.pdf`, `L3_Automatic_Differentiation.pdf`, `L4_PINN.pdf` | instructor (Braga-Neto) | concepts paraphrased in my own words; **no slide text/figure reproduced** | Discretization, PINNs, SA-PINNs |
| `~/Projects/school/tamu-grad/sciml/PINN_Burgers_Inverse.ipynb` | instructor (Braga-Neto) | cited as the course's inverse-problem demo; **not excerpted** | PINNs |

**Original artifacts I created for this chapter** (all in `docs/12-scientific-ml/`):

| Artifact | What it is |
|---|---|
| `notebooks/pinn-burgers-demo.ipynb` | my own from-scratch JAX PINN solving forward Burgers (executed, ~1 min CPU) |
| `notebooks/sa-pinn-optimizer-results.ipynb` | loads the committed project CSVs and replots the optimizer comparison (executed) |
| `img/generators/make_figures.py` | generates the PINN architecture schematic and the two results figures |

**Upstream credit (named + linked):** Levi McClenny's SA-PINN paper
([arXiv:2009.04544](https://arxiv.org/abs/2009.04544)) and public code
([github.com/levimcclenny/SA-PINNs](https://github.com/levimcclenny/SA-PINNs)); optimizer
methods from Bihlo (2023) and Urbán et al. (2025). PDE benchmark data is the public Raissi
PINNs repository. Excluded from this chapter: misfiled ECEN 740 (Deep Learning) files that
were sitting in the `sciml/` folder.

## 10 — Model Evaluation (synthesis: STAT 650 + ECEN 758, TAMU)

Inventory: `.superpowers/sdd/ch10-inventory.md` · Report: `.superpowers/sdd/ch10-report.md`

**Synthesis chapter.** `course-files/10-model-evaluation/` is empty; the forecast-metric and
MASE derivations were already published in ch09 and the classification-metric theory in ch03/ch08.
This chapter cross-links those and adds the real-code evaluation layer (a logistic-regression
classifier + a two-classifier comparison) plus a curated leakage-patterns page. No new material was
pulled from the private distribution-forecasting repo beyond what ch09 already published.

| Path | Disposition | Where it landed |
|---|---|---|
| `course-files/appendix/Homework/stat650_hw/final/STAT650-F25-Final.ipynb` (my own code; instructor-authored task text paraphrased, professor name and point values omitted) | snippet, promoted-notebook | `classification-metrics.md`, `roc-auc.md`, `cross-validation-and-splitting.md`; basis for `notebooks/classification-metrics-demo.ipynb` |
| `course-files/appendix/Homework/stat650_hw/final/report.ipynb` (my own write-up; provides the Situation 1 regression-comparison numbers and Situation 2 results) | summarized | `regression-and-forecast-metrics.md`, `classification-metrics.md` |
| `course-files/appendix/Homework/stat650_hw/final/Fish.csv` (public Kaggle Fish Market dataset, 158 rows after cleaning, <8 KB) | promoted-notebook | committed as `notebooks/Fish.csv` alongside the demo notebook |
| `course-files/appendix/Homework/ecen758_hw/ecen758_hw3.ipynb` (my own code — GNB-vs-kNN `classification_report` comparison on public "crabs" data) | snippet | `classification-metrics.md` (cross-links ch08 knn/naive-bayes) |
| `course-files/appendix/Homework/ecen758_hw/Assignment_3_Dataset.txt` (public "crabs" morphology set) | cited-only | referenced, not committed |
| `course-files/appendix/Homework/ecen758_hw/Assignment_3_ECEN_758.pdf` (instructor-authored prompt; names a TA) | examined-not-used | prompt text and TA name deliberately not reproduced |
| `course-files/appendix/Homework/stat650_hw/final/{STAT650-F25-Final.pdf, .html, report.pdf}` | examined-not-used | rendered exports; content sourced from the `.ipynb` files instead |
| `course-files/appendix/Homework/stat650_hw/final/figures/{s2_conf_matrix.png, s2_roc_curve.png, …}` (my own exam renders) | examined-not-used | figures remade fresh from the demo notebook rather than reusing exam PNGs |
| `course-files/appendix/Homework/stat650_hw/final/mmm.ipynb` | examined-not-used | empty file (0 bytes) |
| `course-files/10-model-evaluation/` | examined-not-used | empty directory — confirmed no source material |
| `~/Projects/school/tamu-grad/stat654/class_notes/Classification.R` | examined-not-used | near-verbatim ISLR2 textbook lab (copyrighted); not quoted or attributed as original work |
| `~/Projects/school/tamu-grad/stat654/figures/roc_curve.png` | examined-not-used | orphaned artifact — no in-repo script generates it; provenance unverifiable |
| `demand-forecast/src/evaluation/metrics.py`, `tests/test_data_leakage.py` (private distribution-forecasting repo) | cited-only | already published in ch09; cross-linked from `leakage-patterns.md` / `regression-and-forecast-metrics.md`, no new code pulled |

**Cross-linked (not re-derived):** `03-statistics/regression/logistic.md` (confusion-matrix /
precision / recall / ROC formulas), `08-machine-learning/fundamentals/overview.md` (train/val/test
discipline, scaler-leakage gotcha), `08-machine-learning/classification/{knn,naive-bayes}.md`,
`09-time-series-forecasting/evaluation/{metrics,comparison,selection-framework}.md`,
`09-time-series-forecasting/ml/feature-engineering.md` (`.shift(1)` temporal-leakage story).

**Original artifacts I created for this chapter** (all in `docs/10-model-evaluation/`):

| Artifact | What it is |
|---|---|
| `notebooks/classification-metrics-demo.ipynb` | logistic-regression classifier on Fish.csv rebuilt from my STAT 650 code — confusion matrix, ROC, odds ratios (executed top-to-bottom, ~96 KB) |
| `img/confusion-matrix.png`, `img/roc-curve.png` | generated by the demo notebook |
| `img/leakage-timeline.png` | matplotlib timeline contrasting leakage-safe (`.shift(1)`) vs leaky rolling features across a train/test boundary |
