# The Optimizer Study

This is the centerpiece of the chapter: my ECEN 744 **final project**, a controlled study
of *which optimizer trains a self-adaptive PINN best*. It's joint work with a project
teammate, built on top of [Levi McClenny's public SA-PINN codebase](https://github.com/levimcclenny/SA-PINNs)
— his self-adaptive weighting and training scaffolding are the platform; our contribution
is the experiment that swaps the optimizer and measures what happens, across four PDEs.

## The question

The original SA-PINN paper trains with the deep-learning default: **Adam**, then a phase of
**L-BFGS** to polish. But PINN losses are notoriously **stiff and ill-conditioned** — the
kind of loss surface first-order methods crawl on. Several papers propose optimizers
tailored to that regime. So: *holding the network, the loss, and the self-adaptive weights
completely fixed, does a better optimizer substitute for — or complement — the
self-adaptive mechanism?*

The design makes the optimizer the **only** moving part. Same architecture, same loss,
same self-adaptive $\lambda$ scheme, same seed (`1234`), same iteration budgets. Any
difference in final error is then attributable to the optimizer alone.

## Two-phase training

Every configuration trains in two phases, and the variants differ only in which optimizer
drives each phase:

- **Phase 1 (first-order).** The network weights $\theta$ and the self-adaptive weights
  $\lambda$ are trained jointly on the saddle-point objective for 10,000 iterations.
  $\lambda$ is always ascended with Adam; $\theta$ is driven either by **Adam** or by the
  **learnable optimizer**.
- **Phase 2 (second-order refinement).** $\lambda$ is frozen and $\theta$ is refined by a
  quasi-Newton method — **L-BFGS** (baseline) or a **self-scaled** variant — for up to
  10,000 iterations, or until the line search can no longer make progress.

Here is that dispatch from my own Kuramoto–Sivashinsky training script — the phase-1 loop
picks Adam vs. the learnable optimizer, and phase 2 picks L-BFGS vs. the SciPy
quasi-Newton path:

```python
# --- phase 1: first-order update on the network weights ---
if optimizer_name == "learnable":
    weights_updated = learnable_optimizer.apply_gradients(
        u_model.trainable_variables, grads, learnable_optimizer.optimizer)
    reshape_to_model(weights_updated, u_model)
else:
    tf_optimizer.apply_gradients(zip(grads, u_model.trainable_variables))
# (self-adaptive weights are ascended with Adam in the same step)

# --- phase 2: second-order refinement on the network weights ---
if optimizer_name == "quasi-newton":
    lbfgs_history = run_quasi_newton_refinement(
        loss_and_flat_grad, get_weights(u_model), newton_iter,
        qn_method=qn_method, qn_method_bfgs=qn_method_bfgs)   # SSBFGS_AB / SSBroyden2
else:
    _, lbfgs_f_hist, _ = lbfgs(
        loss_and_flat_grad, get_weights(u_model), Struct(),
        maxIter=newton_iter, learningRate=0.8)                # standard L-BFGS baseline
```

Source:
`~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py`
(my own benchmark script). The `LearnableOptimizer` and `run_quasi_newton_refinement`
it calls are my project teammate's modules and the vendored SciPy patch — framed below.

## The three optimizer families

**1. Adam → L-BFGS (the SA-PINN baseline).** The standard recipe: Adam for phase 1,
limited-memory BFGS for phase 2. This is the reference every other configuration is
measured against.

**2. A learnable meta-optimizer (Bihlo, 2023).** Instead of a fixed Adam update rule, a
small recurrent network *is* the optimizer: it maps gradients to parameter updates,

$$\theta_{t+1} = \theta_t + f_\phi\big(\nabla_\theta \mathcal{L}_{SA}(\theta_t),\, h_t\big),$$

with its parameters $\phi$ pretrained offline by unrolling optimization trajectories. We
use the released pretrained optimizer, frozen, for phase 1 only. The implementation lives
in my project teammate's `Optimizers/learnable_optimizer.py` (extending the Bihlo method);
I contributed the KS-specific integration and a few fixes.

**3. Self-scaled quasi-Newton (Urbán et al., 2025).** Quasi-Newton methods approximate the
loss's curvature (the inverse Hessian) without ever forming it, from the secant pair
$s_t=\theta_{t+1}-\theta_t$, $y_t=g_{t+1}-g_t$. Standard L-BFGS scales poorly when the
curvature changes fast — exactly the PINN regime. The **self-scaled** variants rescale the
Hessian approximation each step:

- **SSBFGS_AB** — self-scaled BFGS, rescaling with $s_t^\top y_t$ and $y_t^\top H_t y_t$ to
  keep the update well-conditioned;
- **SSBroyden2** — the self-scaled Broyden update, more robust on indefinite curvature.

These live in a **patched SciPy fork** (`_minimize.py` / `_optimize.py`) vendored in the
repo's `Optimizers/` folder; phase 2 calls `scipy.optimize.minimize` through my project
teammate's `run_quasi_newton_refinement` wrapper. Stock SciPy silently ignores the
self-scaling options — a real reproducibility snag covered on the
[results page](results-and-lessons.md).

## The four benchmarks

Each PDE stresses a different source of optimization difficulty:

| PDE | Form | What makes it hard |
|---|---|---|
| **Burgers** | $u_t + u u_x - \tfrac{0.01}{\pi}u_{xx}=0$ | a sharp shock near $x=0$ |
| **Helmholtz** | $u_{xx}+u_{yy}+k^2u = q$ | multi-scale oscillatory solution |
| **Allen–Cahn** | $u_t - 0.0001\,u_{xx} + 5u^3 - 5u = 0$ | stiff cubic reaction, moving interfaces |
| **Kuramoto–Sivashinsky** | $u_t + u u_x + u_{xx} + u_{xxxx}=0$ | 4th-order operator; needs `u_xxxx` |

The KS benchmark is the one I added to the project myself — it extends the original
SA-PINN evaluation (all second-order) to a stiff 4th-order PDE. Getting it to train needed
an **input-normalization layer**, because on the $L_x=8\pi$ domain the raw $x\in[-12.6,
12.6]$ saturates `tanh`:

```python
# map (x, t) from the physical domain into [-1, 1]^2 before the tanh stack,
# so a wide spatial domain doesn't saturate the activations. The chain rule
# still flows through tf.gradients, so the residual uses raw (x, t).
model.add(layers.Lambda(lambda z: 2.0 * (z - lb_t) / (ub_t - lb_t) - 1.0))
```

Source: same `ks.py` (my own). And the 4th-order residual is just four nested autodiff
calls:

```python
u_x    = tf.gradients(u,     x)
u_xx   = tf.gradients(u_x,   x)
u_xxx  = tf.gradients(u_xx,  x)
u_xxxx = tf.gradients(u_xxx, x)
f_u = u_t + u * u_x + u_xx + u_xxxx        # KS operator; want 0
```

## Notebook

The comparison across all four PDEs — plus the Burgers phase-1/phase-2 loss curves — is
worked in [SA-PINN optimizer results](notebooks/sa-pinn-optimizer-results.ipynb), which
loads the committed result CSVs and replots them. The [results page](results-and-lessons.md)
walks through what it found.

## Gotchas

- **Isolate one variable or the study means nothing.** The single hardest design decision
  was resisting the urge to also tune the architecture or weighting per optimizer. Keeping
  everything else byte-identical is what makes "the optimizer caused this" a valid claim.
- **The 4th-order term dominates KS training cost.** `u_xxxx` is four passes through the
  autodiff graph per collocation point, per step — the KS runs are noticeably slower than
  the second-order PDEs.
- **`tanh` saturation is silent.** On the wide KS domain the network just refused to learn
  until the input-normalization layer went in; nothing errors, the loss just sits.

## Source

- `~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py`
  — my SA-PINN training script (two-phase dispatch, input normalization, 4th-order
  residual).
- `Optimizers/learnable_optimizer.py`, `Optimizers/pinn_quasi_newton.py`, and the patched
  `Optimizers/_minimize.py` / `_optimize.py` — my project teammate's modules and the
  vendored SciPy fork; referenced, not reproduced here.
- Upstream method + code: McClenny & Braga-Neto, SA-PINN
  ([arXiv:2009.04544](https://arxiv.org/abs/2009.04544),
  [github.com/levimcclenny/SA-PINNs](https://github.com/levimcclenny/SA-PINNs)); optimizer
  papers: Bihlo (2023), Urbán et al. (2025).
