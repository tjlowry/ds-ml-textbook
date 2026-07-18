# How PINNs Work

A physics-informed neural network is, structurally, an ordinary MLP. What makes it a PINN
is the **loss**: instead of "match these labels," it says "satisfy this differential
equation." This page builds that loss from the ground up and then points at my own
from-scratch demo that solves the 1-D Burgers equation with it.

## The one picture

![A physics-informed neural network. The inputs (x, t) feed a tanh MLP that outputs
u-hat; automatic differentiation produces u_t, u_x, u_xx, which assemble the PDE residual
r = u_t + u u_x - nu u_xx. The residual becomes the loss term L_r at collocation points;
the network output is compared to the boundary and initial data as L_b and L_0; the three
sum to the total loss L, whose gradient with respect to the weights is backpropagated to
train the network.](img/pinn-architecture.png)

Read it left to right: the network $u_\theta(x,t)$ proposes a solution; autodiff extracts
the derivatives the PDE needs; those assemble the **residual** $r$, which *should* be zero
everywhere if the network truly solves the equation. The loss measures how far from zero
$r$ is at sampled interior points, plus how well the network matches the known data on the
boundary and at the initial time. Then it's the same training loop as any other network —
backprop the loss to the weights, step, repeat.

## The residual loss, term by term

Take the viscous Burgers equation as the running example (the equation my demo solves):

$$\underbrace{u_t + u\,u_x - \nu\,u_{xx}}_{\text{must equal } 0} = 0,\qquad
u(0,x) = -\sin(\pi x),\qquad u(t,\pm 1)=0.$$

The total PINN loss is a sum of three mean-squared terms:

$$\mathcal{L} \;=\; \underbrace{\frac{1}{N_r}\sum_i r(x_r^i,t_r^i)^2}_{\mathcal{L}_r\ \text{(physics)}}
\;+\; \underbrace{\frac{1}{N_0}\sum_i \big(u_\theta(x_0^i,0)-u_0^i\big)^2}_{\mathcal{L}_0\ \text{(initial data)}}
\;+\; \underbrace{\frac{1}{N_b}\sum_i u_\theta(x_b^i,t_b^i)^2}_{\mathcal{L}_b\ \text{(boundary)}}.$$

- **$\mathcal{L}_r$ — the physics term.** Evaluated at **collocation points**: a cloud of
  $(x,t)$ locations sampled in the *interior* of the domain, with **no known answer**.
  We only demand that the equation's residual be zero there. This is the term that needs
  no labeled data — the physics is the supervision.
- **$\mathcal{L}_0$ — the initial condition.** At $t=0$ the solution *is* known
  ($-\sin\pi x$), so this is an ordinary supervised MSE.
- **$\mathcal{L}_b$ — the boundary condition.** At $x=\pm 1$ the solution is zero; again a
  supervised MSE.

The interesting term is $\mathcal{L}_r$, and it exists only because we can differentiate
the network with respect to its inputs.

## How I did it — the residual in code

Here is the residual from my own demo notebook. `u_scalar` is the network evaluated at a
single point; `u_t`, `u_x`, `u_xx` are exact derivatives from `jax.grad`, and a second
derivative is literally two nested `grad`s:

```python
def residual(params, x, t):
    u    = u_scalar(params, x, t)
    u_t  = grad(u_scalar, argnums=2)(params, x, t)             # d u / d t
    u_x  = grad(u_scalar, argnums=1)(params, x, t)             # d u / d x
    u_xx = grad(grad(u_scalar, argnums=1), argnums=1)(params, x, t)  # d²u / d x²
    return u_t + u * u_x - NU * u_xx        # Burgers operator; want this = 0
```

Source: [`notebooks/pinn-burgers-demo.ipynb`](notebooks/pinn-burgers-demo.ipynb) (mine).

The loss then just averages the squared residual over the collocation batch and adds the
two data terms:

```python
def loss_fn(params, batch):
    xf, tf, xi, ti, ui, xb, tb = batch
    mse_f = jnp.mean(batched_r(params, xf, tf) ** 2)          # L_r  physics residual
    mse_i = jnp.mean((batched_u(params, xi, ti) - ui) ** 2)   # L_0  initial condition
    mse_b = jnp.mean(batched_u(params, xb, tb) ** 2)          # L_b  boundary condition
    return mse_f + W_IC * mse_i + W_BC * mse_b, (mse_f, mse_i, mse_b)
```

The `W_IC`, `W_BC` factors up-weight the data terms so the network anchors to the
initial/boundary data early. Choosing those weights well is fiddly — and *learning* them
automatically is exactly the [self-adaptive PINN](sa-pinns.md) idea.

## Notebook

See the rendered notebook: [PINN: Burgers from scratch](notebooks/pinn-burgers-demo.ipynb).
It runs the whole loop — network, residual, hand-rolled Adam, 15,000 steps in about a
minute on a CPU — and produces the training curve and the solution field below.

Re-run locally: `jupyter lab docs/12-scientific-ml/notebooks/pinn-burgers-demo.ipynb`

The forward Burgers problem here is the *same* PDE the course's inverse-problem demo uses;
that demo instead treats the viscosity $\nu$ as **unknown** and estimates it from noisy
sensor data — the setting where PINNs genuinely beat classical solvers. I keep the forward
version because it isolates the mechanics.

## Gotchas

- **Collocation points are not training labels.** It surprised me at first: the interior
  points carry *no target value*. Their only role is "the residual should be zero here."
  More of them (or better-placed ones) means the equation is enforced more densely.
- **The residual term is the slow one.** In my run the initial/boundary MSE drops fast but
  the residual plateaus around $10^{-3}$ — the loss surface is stiff, and plain Adam
  stalls. This is the whole motivation for the [optimizer study](optimizer-study.md).
- **`u_scalar` must return a scalar to differentiate cleanly.** I write the network for a
  single point and `vmap` over the batch, rather than differentiating a batched output —
  it keeps the `grad` calls unambiguous.
- **Second derivatives cost.** Every nested `grad` is another pass through the graph; a
  4th-order PDE needs `u_xxxx` (four nested `grad`s per point), which is a real slice of
  the training time.

## Source

- [`notebooks/pinn-burgers-demo.ipynb`](notebooks/pinn-burgers-demo.ipynb) — my original
  from-scratch JAX PINN.
- Concepts from ECEN 744 Lec 4 (Physics-Informed Neural Networks), Braga-Neto
  (local: `~/Projects/school/tamu-grad/sciml/L4_PINN.pdf`) — paraphrased, not reproduced.
- The course's inverse-Burgers demo is the instructor's own notebook, cited but not
  excerpted here (local:
  `~/Projects/school/tamu-grad/sciml/PINN_Burgers_Inverse.ipynb`, authored by Braga-Neto).
