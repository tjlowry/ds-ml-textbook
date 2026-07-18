# Self-Adaptive PINNs

A plain PINN weights every collocation point equally. But the hard part of a PDE is
usually *localized* — a shock front, a sharp interface — and equal weighting lets the
network get the easy, smooth regions right while the residual stays large exactly where it
matters. **Self-adaptive PINNs (SA-PINNs)**, introduced by
[McClenny & Braga-Neto](https://doi.org/10.1016/j.jcp.2022.111722), fix this by making the
per-point weights **trainable** — and training them in the *opposite* direction from the
network. This page is the conceptual setup for my final project, whose whole codebase is
built on their public implementation.

## The idea: weights that fight the network

Give every collocation, boundary, and initial point its own scalar weight
$\lambda^i \ge 0$, and form the weighted loss

$$\mathcal{L}_{SA}(\theta,\lambda)
= \frac{1}{N_r}\sum_i \lambda_r^i\, r(x_r^i;\theta)^2
+ \frac{1}{N_b}\sum_i \lambda_b^i\, b(x_b^i;\theta)^2
+ \frac{1}{N_0}\sum_i \lambda_0^i\, \ell_0(x_0^i;\theta)^2.$$

Now the twist. The network weights $\theta$ are trained to **minimize** this loss, as
usual. But the point-weights $\lambda$ are trained to **maximize** it:

$$\min_{\theta}\;\max_{\lambda}\;\mathcal{L}_{SA}(\theta,\lambda).$$

It's a **saddle-point** problem. Intuitively: wherever the residual stays stubbornly
large, gradient *ascent* pushes that point's $\lambda$ up, which forces the network to pay
more attention there on its next descent step. The weights act like a soft attention mask
over the domain that automatically concentrates on the points the network is failing — no
hand-tuned weighting schedule required. (This is what the fixed `W_IC`/`W_BC` factors in
my [plain-PINN demo](pinns.md) are a crude, static substitute for.)

## How it looks in the training loop

In practice the saddle point is handled by a simple simultaneous scheme: **descend** on
$\theta$, **ascend** on $\lambda$, both with Adam, in the same step. Concretely, the
ascent is just a descent on the *negated* gradient of the weight variables. Here is that
exact move from my own Kuramoto–Sivashinsky training script — `col_weights` and
`u_weights` are the $\lambda$ vectors, and note the **minus signs** that turn their update
into gradient ascent:

```python
# theta: ordinary descent on the network weights
tf_optimizer.apply_gradients(zip(grads, u_model.trainable_variables))

# lambda: ASCENT on the self-adaptive weights -> note the negated gradients
tf_optimizer_weights.apply_gradients(
    zip([-grads_col, -grads_u], [col_weights, u_weights]))
```

Source:
`~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py`
(my own benchmark script, following the SA-PINN scheme).

The weighted-residual loss itself is the same three-term structure as a plain PINN, just
with the $\lambda$ vectors multiplying inside each mean:

```python
mse_0_u = tf.reduce_mean(tf.square(u_weights   * (u0 - u0_pred)))   # weighted IC
mse_f_u = tf.reduce_mean(tf.square(col_weights * f_u_pred[0]))      # weighted residual
```

Source: same file, my `loss(...)` function.

## Where the mask concentrates

Because the weights are trainable and visible, you can *plot* them at the end of training
and literally see where the network struggled. In the project scripts the final
`col_weights` are scattered over the collocation cloud (`collocation_weights.png` per run)
— the big weights cluster on the sharp features (the shock in Burgers, the interface in
Allen–Cahn), which is the mechanism working as intended.

## Why this matters for the optimizer study

The self-adaptive weighting is held **fixed across every configuration** in my
[final project](optimizer-study.md) — same $\lambda$ scheme, same architecture, same loss.
That is deliberate: it isolates the *optimizer* as the only thing that changes, so any
difference in final error is attributable to the optimizer and not to a different weighting
trick. SA-PINN is the platform; the experiment is about what you run on top of it.

## Gotchas

- **It's a saddle point, not a minimum.** You are not minimizing a single objective, so
  the usual "loss went down, good" intuition is subtler — the $\lambda$ ascent *wants* the
  weighted loss up in places. Watch the *unweighted* residual to judge real progress.
- **The minus sign is the whole thing.** Ascent-by-negated-gradient is easy to get
  backwards; flip it and the mask suppresses the hard points instead of emphasizing them.
- **More knobs to initialize.** The $\lambda$ initialization (e.g. $\lambda_0\sim
  100\cdot\mathcal{U}(0,1)$ for a stiff initial layer) is itself a hyperparameter, chosen
  per PDE in the project.

## Source

- `~/Projects/school/tamu-grad/ECEN744-FinalProject-SA-PINNs/Kuramoto-Sivashinsky/ks.py`
  — my SA-PINN training loop for the KS benchmark.
- Original method: McClenny, L. & Braga-Neto, U., *Self-Adaptive Physics-Informed Neural
  Networks using a Soft Attention Mechanism*, J. Comput. Phys. (2023),
  [arXiv:2009.04544](https://arxiv.org/abs/2009.04544); public code:
  [github.com/levimcclenny/SA-PINNs](https://github.com/levimcclenny/SA-PINNs). Cited as
  the upstream method and codebase — its paper/derivation is referenced, not reproduced.
- Concepts also from ECEN 744 Lec 4, Braga-Neto
  (local: `~/Projects/school/tamu-grad/sciml/L4_PINN.pdf`).
