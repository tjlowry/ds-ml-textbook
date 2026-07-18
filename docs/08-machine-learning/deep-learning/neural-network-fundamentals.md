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
