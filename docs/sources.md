# Sources

A per-chapter ledger of the real files each page was built from — my own code and
coursework, plus the instructor/upstream material that is **cited but never reproduced**.
Paths are the local sources on my machine; raw course materials live in `course-files/`
(local-only, never published) and in my `~/Projects/` work folders.

## Chapter 12 — Scientific Machine Learning & PINNs

Course: **ECEN 744 Scientific Machine Learning**, Texas A&M, Spring 2026, instructor
Ulisses Braga-Neto. The final project is joint work with a project teammate, built on Levi
McClenny's public SA-PINN codebase.

| File | Author | How it's used | Page(s) |
|---|---|---|---|
| `~/Projects/school/tamu-grad/sciml/sciml_hw1.py` | **mine** (HW1) | Euler/Backward Euler/Heun/RK4 snippets + convergence table | Discretization & Autodiff |
| `~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/generate_ks_data.py` | **mine** | ETDRK4 spectral reference generator snippet | Discretization & Autodiff |
| `.../ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py` | **mine** (100% my commits) | SA-PINN loop, ascent-on-λ, two-phase dispatch, input normalization, 4th-order residual | SA-PINNs, Optimizer Study |
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
