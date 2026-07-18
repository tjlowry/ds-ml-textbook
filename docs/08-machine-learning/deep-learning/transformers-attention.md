# Transformers & Attention

## Overview

The **transformer** replaced recurrence with **self-attention**: every token looks at every
other token and decides how much to attend to each, so context flows in one parallel step
instead of stepwise through a sequence. **Scaled dot-product attention** is the core
operation — queries dotted with keys, scaled, softmaxed, and used to weight values — and
**multi-head** attention runs several of these in parallel subspaces. Stacked with
normalization and feed-forward blocks, this is the architecture behind modern LLMs.

This is the from-scratch project I'm proudest of in the chapter: in ECEN 740 I built a
decoder-only GPT-style language model component by component, no `nn.Transformer`.

## How I did it

**Scaled dot-product attention** — the heart of it, with an optional causal mask:

```python
def scaled_dot_product_attention(q, k, v, mask=None, dropout_p=0.0, training=True):
    d_k = q.size(-1)
    scores = (q @ k.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores + mask            # additive -inf mask blocks future positions
    attn = F.softmax(scores, dim=-1)
    attn = F.dropout(attn, p=dropout_p, training=training)
    return attn @ v
```

**Multi-head causal self-attention** — one fused QKV projection, reshape into heads, apply
attention with a lower-triangular `-inf` mask, then recombine:

```python
class MultiHeadSelfAttention(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.qkv_proj = nn.Linear(cfg.d_model, 3 * cfg.d_model, bias=False)
        self.out_proj = nn.Linear(cfg.d_model, cfg.d_model, bias=False)
        causal = torch.tril(torch.ones(cfg.context_length, cfg.context_length))
        causal = causal.masked_fill(causal == 0, float('-inf')).masked_fill(causal == 1, 0.0)
        self.register_buffer('causal_mask', causal)

    def forward(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv_proj(x).split(self.d_model, dim=-1)
        q = q.view(B, T, self.n_heads, self.d_head).transpose(1, 2)   # (B, heads, T, d_head)
        k = k.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        v = v.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        out = scaled_dot_product_attention(q, k, v, mask=self.causal_mask[:T, :T],
                                           dropout_p=self.drop_p, training=self.training)
        return self.out_proj(out.transpose(1, 2).contiguous().view(B, T, D))
```

**A pre-norm transformer block** — RMSNorm before each sublayer, residual add around each,
with a SwiGLU feed-forward net:

```python
class TransformerBlock(nn.Module):
    def forward(self, x):
        x = x + self.attn(self.norm1(x))    # pre-norm + residual
        x = x + self.ffn(self.norm2(x))
        return x
```

Source (all three): `~/Projects/school/tamu-grad/ecen740/ECEN740_project3.ipynb`

The project also implements the surrounding machinery from scratch: GPT-2-style byte-level
**BPE** tokenization (pre-tokenization regex → iterative pair merges), **RMSNorm**, a
**SwiGLU** gated feed-forward (`w2(silu(w_gate(x)) * w1(x))`), tied input/output embeddings,
and **temperature + top-p** sampling for generation. Each piece has a self-grading test.

## Notebook

See the rendered notebook: [Mini-GPT From Scratch](../notebooks/mini-gpt-from-scratch.ipynb)
— every component above, built and tested in order, training on the tiny-Shakespeare corpus.

Re-run locally: `jupyter lab docs/08-machine-learning/notebooks/mini-gpt-from-scratch.ipynb`

!!! note "Outputs are from the original GPU run"
    The notebook was not re-executed for the textbook — training a transformer on CPU is
    impractical, so the committed outputs are from the original `DEVICE = 'cuda'` run. Run
    it on a CUDA machine to reproduce them.

## Gotchas

- **The `/ sqrt(d_k)` scaling isn't optional.** Without it, dot products grow with dimension,
  push softmax into saturation, and kill the gradients. It's a one-line detail that breaks
  training if you drop it.
- **The causal mask is what makes it a language model.** Additive `-inf` above the diagonal
  stops a position from attending to future tokens — otherwise the model cheats by seeing the
  answer.
- **Shape bookkeeping is the hard part.** The `view`/`transpose` dance to split `d_model`
  into `(heads, d_head)` and back is where every attention bug lives; getting the
  `.contiguous()` and axis order right matters.
- **Tie the embeddings.** Sharing the token-embedding matrix with the output projection
  (`lm_head.weight = tok_emb.weight`) cuts parameters and usually helps — a standard GPT
  trick worth remembering.

## References

- ECEN 740 (Machine Learning Engineering, TAMU) — Project 3; supporting slide decks
  `ModernLLM.pptx` / `Transformers.pptx` (local, `~/Projects/school/tamu-grad/ecen740/`).
