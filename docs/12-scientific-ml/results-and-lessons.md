# Results & Lessons

This page reports what the [optimizer study](optimizer-study.md) found, and — just as
importantly — the honest caveats about what "found" means when the environment can't be
perfectly reproduced. All numbers here are the **committed result CSVs** in the project
repo (the same data the [results notebook](notebooks/sa-pinn-optimizer-results.ipynb)
loads), at the shared 10k-phase-1 / 10k-phase-2 budget, seed `1234`.

## The headline

![Grouped bar chart of relative L2 error (log scale) for four PDEs — Burgers, Helmholtz,
Allen-Cahn, Kuramoto-Sivashinsky — each with bars for L-BFGS, Learnable, SSBFGS, and
SSBroyden2 optimizers. On Burgers, Helmholtz and Kuramoto-Sivashinsky the two self-scaled
quasi-Newton bars are dramatically lower than the L-BFGS baseline; on Allen-Cahn they are
comparable or worse and there is no SSBFGS bar.](img/optimizer-l2-comparison.png)

On **three of the four** benchmarks, simply swapping the phase-2 optimizer for a
self-scaled quasi-Newton method — with nothing else changed — cuts the relative $L^2$
error by one to nearly two orders of magnitude. The cross-benchmark numbers:

| Configuration | Burgers | Helmholtz | Allen–Cahn | Kuramoto–Sivashinsky |
|---|---|---|---|---|
| L-BFGS (baseline) | 1.62 × 10⁻³ | 5.65 × 10⁻³ | 9.77 × 10⁻² | 6.59 × 10⁻⁴ |
| Learnable | 1.08 × 10⁻³ | 5.57 × 10⁻³ | 2.61 × 10⁻¹ | 1.73 × 10⁻³ |
| **SSBFGS** | **3.09 × 10⁻⁵** | **1.26 × 10⁻⁴** | — | **3.04 × 10⁻⁴** |
| SSBroyden2 | 4.34 × 10⁻⁵ | 1.37 × 10⁻⁴ | 8.01 × 10⁻² | 3.41 × 10⁻⁴ |

(Relative $L^2$ error; lower is better. Allen–Cahn has no committed SSBFGS run.)

- **Burgers & Helmholtz:** SSBFGS is ~52× and ~45× better than the L-BFGS baseline, and it
  gets there in roughly 10–20% of the iteration budget — the self-scaled runs *terminate
  early* once the line search hits precision loss, rather than exhausting the cap.
- **Kuramoto–Sivashinsky:** the $L^2$ gap is smaller (~2×), but the **final residual** tells
  the real story — SSBFGS/SSBroyden reach residuals of order $10^{-9}$, three to four
  orders of magnitude below the baseline, on this stiff 4th-order PDE.
- **The learnable meta-optimizer disappoints:** it edges past the baseline on
  Burgers/Helmholtz but is much worse on Allen–Cahn and KS. A pretrained, frozen optimizer
  doesn't transfer to new PDEs.

## Where the advantage comes from: the two phases

![Two side-by-side loss curves for the Burgers equation. Left, phase 1 (first-order): all
four optimizers produce a noisy saddle-point loss oscillating around order 10 to 100.
Right, phase 2 (quasi-Newton refinement): the L-BFGS and Learnable curves settle around
1e-3 while the SSBFGS and SSBroyden2 curves plunge to about 1e-5 within roughly a thousand
iterations.](img/burgers-loss-curves.png)

Phase 1 looks the same for everyone — a noisy ride on the self-adaptive saddle-point
objective. The separation is entirely in **phase 2**: standard L-BFGS and the learnable
variant flatten out around $10^{-3}$, while the self-scaled methods keep descending to
$10^{-5}$ and then stop because the Wolfe line search can no longer make progress at that
loss scale. The curvature-aware self-scaling extracts far more residual reduction per
iteration on the ill-conditioned PINN loss.

## The Allen–Cahn exception

Allen–Cahn is where the tidy story breaks, and that's worth dwelling on. Its stiff cubic
reaction term ($5u^3 - 5u$) produces sharp moving interfaces, and the quasi-Newton
advantage seen everywhere else **evaporates**: SSBroyden2 (8.01 × 10⁻²) roughly ties the
L-BFGS baseline (9.77 × 10⁻²), and there is no committed SSBFGS run to compare. The
positive-definite SSBFGS update stays stable on cubic nonlinearity in the runs we did have,
but the Broyden update never reaches the precision-loss regime that ended its Burgers,
Helmholtz, and KS runs after ~1–2k iterations. **On the hardest problem, better
optimization stopped being a free lunch.**

Allen–Cahn was also the **least reproducible** benchmark: our re-runs of it landed
noticeably worse than the numbers in an earlier pass of the project report (the report's
run had the L-BFGS baseline nearer $1.7 \times 10^{-2}$, versus $9.8 \times 10^{-2}$ in the
committed re-run above). That gap between two of *our own* runs is not a footnote — it *is*
one of the lessons.

## Reproducibility, honestly

Two caveats that any re-user needs up front:

1. **The baselines are our own reproduced runs, not the paper's.** We could not perfectly
   recreate the original SA-PINN environment, so the L-BFGS row is *our* reference, not a
   byte-for-byte replay of McClenny & Braga-Neto's published numbers. Every comparison here
   is internal-consistent (same seed, same budget) but should not be read as reproducing
   the original paper.
2. **The quasi-Newton path needs a patched SciPy.** SSBFGS/SSBroyden call
   `scipy.optimize.minimize` with self-scaling options that **only exist in the vendored
   fork** — you must replace your environment's `scipy/optimize/_minimize.py` and
   `_optimize.py` with the patched files in the repo's `Optimizers/` folder. Stock SciPy
   silently ignores the options and you'd get L-BFGS-like behavior mislabeled as
   quasi-Newton. The Adam and Learnable variants run on the stock stack (TensorFlow 2.15.1
   / SciPy 1.12.0). Exact per-PDE commands and the patch steps are in the repo `README.md`
   (`~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/README.md`).

## Lessons

- **The optimizer, not the architecture, was the highest-leverage knob.** With everything
  else fixed, a curvature-aware phase-2 optimizer bought 1–4 orders of magnitude on most
  PDEs — more than tweaking the network ever did.
- **Second-order beats first-order on stiff losses.** The PINN loss surface is exactly the
  ill-conditioned regime where self-scaled quasi-Newton shines and Adam/L-BFGS stall.
- **Learned optimizers didn't transfer.** A meta-optimizer pretrained on other problems and
  frozen underperformed a plain second-order method on unseen PDEs.
- **"Better optimization" is problem-dependent.** Allen–Cahn is the counterexample that
  keeps the conclusion honest — the same method that won by 52× elsewhere merely tied (or
  lost) there.
- **Reproducibility is a first-class result.** A vendored numerical-library patch and
  run-to-run variance on the stiffest PDE are not embarrassing asides; documenting them is
  part of reporting the work honestly.

## Source

- `~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Results/*/results_summary.csv`,
  `training_loss.csv`, `lbfgs_loss.csv` — the committed run artifacts (co-authored project;
  data replotted here, credit to my project teammate and to McClenny's upstream codebase).
- `docs/results_section.tex`, `docs/method.tex` — the project report fragments (co-authored)
  the narrative here is drawn from and cross-checked against the committed CSVs.
- Figures remade by `docs/12-scientific-ml/img/generators/make_figures.py` from the copied
  CSVs; see [the notebook](notebooks/sa-pinn-optimizer-results.ipynb).
