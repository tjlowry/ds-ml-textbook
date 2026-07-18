# Neural Network Fundamentals

## Overview

A neural network stacks linear layers (`Wx + b`) with nonlinear activations, and learns by
**backpropagation**: run a forward pass, compute a loss, then propagate gradients backward
through the chain rule and take a gradient-descent step. Everything else — initialization,
BatchNorm, dropout, the choice of activation and optimizer — is engineering to make that
loop train stably and generalize.

This is the deepest hands-on material in the chapter. In ECEN 740 I built an MLP project
that implements the pieces from scratch (hinge loss, manual backprop, init schemes,
BatchNorm, dropout) and wrote my own PyTorch training/debugging reference to go with it.

## How I did it

**The training loop** is the pattern every project reuses — zero grads, forward, loss,
backward, step:

```python
def train_one_epoch(model, trainloader, criterion, optimizer, device):
    model.train()
    for inputs, labels in trainloader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
```

Source: `~/Projects/school/tamu-grad/ecen740/Copy_of_ECEN740_Project1.ipynb`

**Loss from scratch.** The project implements multi-class hinge loss by hand and validates
it against known values (e.g. scores `[3.2, 5.1, -1.7]` with true class 0 → loss 2.9), then
compares hinge vs cross-entropy training dynamics.

**Backprop by hand.** Rather than trusting autograd, one task verifies backpropagation
through a single sigmoid neuron and then a full two-layer network manually — deriving the
local gradients and checking them — which is the exercise that made the chain rule concrete
for me.

**Cross-entropy from log-softmax** (from the mini-GPT project, same idea):

```python
log_probs = F.log_softmax(logits, dim=-1)
loss = -log_probs_flat[torch.arange(B * T), targets_flat].mean()
```

Source: `~/Projects/school/tamu-grad/ecen740/ECEN740_project3.ipynb`

The project also sweeps the engineering knobs directly: **Xavier vs Kaiming**
initialization paired with different activations, **BatchNorm** and its train/eval-mode
behavior, a **dropout** sweep to find the regularization sweet spot, and an optimizer
comparison visualized as trajectories on a 2-D loss surface.

### Backprop by hand, with numbers

I also worked a single neuron end-to-end by hand in ECEN 758 Assignment 4 — the smallest
example that shows *why the update rule you pick matters*. Take one perceptron with inputs
$x_1 = 2$, $x_2 = 1$, weights $w_1 = 2$, $w_2 = -1$, bias $b = 1$, sigmoid activation, and a
target $d = 1$.

**Forward pass.** The pre-activation is $\text{net} = b + w_1 x_1 + w_2 x_2 = 1 + 2(2) + (-1)(1) = 4$,
so

$$y = \sigma(4) = \frac{1}{1 + e^{-4}} \approx 0.982, \qquad e = d - y \approx 0.018.$$

**Perceptron learning rule** ($w_j^\text{new} = w_j^\text{old} + \eta\, e\, x_j$, with $\eta = 1$):

$$w_1 \to 2 + (1)(0.018)(2) = 2.036, \quad w_2 \to -1 + (1)(0.018)(1) = -0.982, \quad b \to 1.018.$$

**Backprop / SGD on squared error** $J = \tfrac12 (d - y)^2$ instead. Now the sigmoid
derivative enters the gradient — $\partial J / \partial w_j = e \cdot (-1)\cdot \sigma(\text{net})\,(1 - \sigma(\text{net}))\cdot x_j$
— and $w_j^\text{new} = w_j^\text{old} - \eta\,\partial J/\partial w_j$ gives

$$w_1 \to 2.00064, \qquad w_2 \to -0.99968, \qquad b \to 1.00032.$$

The lesson is in the contrast: the perceptron rule moved $w_1$ by $0.036$, but backprop moved
it by only $0.00064$ — about 50× smaller — on the *same* neuron and the *same* learning rate.
The difference is the factor $\sigma(\text{net})(1 - \sigma(\text{net})) \approx 0.982 \times 0.018 \approx 0.0177$:
a saturated sigmoid has a tiny slope, so the gradient signal through it is tiny. That is
**vanishing-gradient in miniature** — the concrete reason ReLU and careful initialization
matter once you stack many of these layers. (The assignment extends the same hand-derivation
to a one-hidden-layer network, $y \approx 0.378$ on its forward pass, which is the two-layer
chain-rule bookkeeping the from-scratch project above then automates.)

Source: my ECEN 758 Assignment 4 solutions
(`course-files/appendix/Homework/ecen758_hw/Assignment_4_ECEN_758_Solutions.pdf`, my own work;
instructor prompt paraphrased).

## Notebook

See the rendered notebook: [MLP Fundamentals](../notebooks/mlp-fundamentals.ipynb) — the
full sequence of tasks from data normalization through the final best-MLP design.

Re-run locally: `jupyter lab docs/08-machine-learning/notebooks/mlp-fundamentals.ipynb`

!!! note "Outputs are from the original GPU run"
    The MLP notebook was not re-executed for the textbook (its plots were stripped to keep
    the file light, and training used `device = 'cuda'`). Run it locally to regenerate the
    figures.

## Gotchas

These are the five bugs I catalogued in my own PyTorch training guide
(`~/Projects/school/tamu-grad/ecen740/PyTorch_Training_Guide.ipynb`) — the ones that bite
every time:

- **Forgetting `optimizer.zero_grad()`.** PyTorch *accumulates* gradients; skip the zero and
  each step mixes in stale gradients, so training silently diverges.
- **Wrong learning rate.** Too high → loss explodes/NaNs; too low → it barely moves. It's
  the first knob to check when nothing learns.
- **Forgetting `model.eval()` / `torch.no_grad()` at inference.** Leaving the model in train
  mode keeps dropout and BatchNorm's batch statistics active, so eval numbers are wrong and
  noisy.
- **Dead neurons from bad init.** Poor initialization (or a big learning rate) can push
  ReLU units into the always-zero region where they never recover — hence Xavier/Kaiming.
- **Data on the wrong device.** A CPU tensor meeting a CUDA model throws (or silently
  slows); keep inputs and model on the same `device`.

The single most useful debugging technique from that guide: **overfit a tiny batch first.**
If the model can't drive loss to ~0 on 4 examples, the bug is in the code, not the data.
