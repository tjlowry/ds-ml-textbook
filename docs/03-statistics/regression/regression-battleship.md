# Case Study: Regression Battleship

## The exercise

Regression Battleship was the capstone game in MATH 425 (BYU-Idaho). Instead of *fitting* a
model to data someone hands you, you play the other side: you **invent a hidden "true"
regression model, simulate a dataset from it, and hand only the data to your opponents** —
who then try to reverse-engineer the model you used. You win by hiding your model well while
keeping the fit genuinely strong. It flips regression around: you become the data-generating
process, which is the single best way I found to actually understand what each term in a
model *does* to the cloud of points.

The rules I had to design against (advanced level):

- The CSV has **11 columns**: `y` plus `x1`…`x10`. You don't have to use all the x's.
- `y` (or a transformation of it) must be built from a **linear regression model** of the
  x's (or transformations of them) — only the allowed transforms: `1/Y`, `log(Y)`, `sqrt(Y)`,
  `Y^2`, `log(X)`, `sqrt(X)`, `X^2`…`X^5`, etc. Transform individual terms only, never groups,
  and the betas can't live inside a transform.
- When the **true** model is fit with `lm(...)`, **every p-value must be significant** at
  $\alpha = 0.05$.
- The **Multiple R²** must be $\geq 0.30$ (higher is more impressive).
- The model must be **2D-drawable** — expressible on a single 2D scatterplot.

Source (exercise + template): `~/Projects/school/byui-undergrad/MATH425/RegressionBattleshipCreatingYourData.Rmd`

## Simulating from a known model

The whole game rests on one skill: generating a sample from a normal-error regression model

$$
  Y_i = \beta_0 + \beta_1 X_i + \epsilon_i, \quad \epsilon_i \sim N(0, \sigma^2)
$$

You *choose* the betas and $\sigma$, draw the x's, draw the errors, and assemble `y`. Here is
the exact pattern from the class activity where I did this, with a satisfied set of
assumptions — true intercept 14.2, true slope 3.5, errors with $\sigma = 2.5$:

```r
n      <- 30                          # sample size
beta_0 <- 14.2                        # TRUE y-intercept (I pick this)
beta_1 <- 3.5                         # TRUE slope        (I pick this)
X_i    <- runif(n, 0, 20)             # sample of X-values
sigma  <- 2.5                         # TRUE error SD     (I pick this)

epsilon_i <- rnorm(n, 0, sigma)       # normally distributed errors
Y_i       <- beta_0 + beta_1*X_i + epsilon_i   # sample of Y from the TRUE model

mylm <- lm(Y_i ~ X_i)                 # now recover it from the data
```

Plotting the **true** line (dashed, using the betas I chose) against the **fitted** line
(solid, from `lm`) on the same scatterplot is the payoff: with $n = 30$ and small $\sigma$
they nearly coincide, and you can *see* the estimated model chasing the true one.

Source: `~/Projects/school/byui-undergrad/MATH425/ClassActivity-RegressionDiagnostics-1.Rmd`

## What the estimates do over many samples

A single simulated sample gives one fitted line; the deeper lesson is what happens across
*many* samples from the same true model — that's the **sampling distribution** of $\hat\beta_0$
and $\hat\beta_1$, and it's where standard errors come from. I ran a true model with
$\beta_0 = 2$, $\beta_1 = 3.5$, $\sigma = 13.8$, $n = 100$, drawing **N = 5000** fresh samples
and refitting each:

```r
n <- 100
beta_0 <- 2; beta_1 <- 3.5; sigma <- 13.8
X <- rep(seq(30, 100, length.out = n/2), each = 2)

N <- 5000
storage_b0 <- storage_b1 <- storage_rmse <- rep(NA, N)
for (i in 1:N) {
  Y <- beta_0 + beta_1*X + rnorm(n, 0, sigma)   # a fresh sample from the true model
  mylm <- lm(Y ~ X)
  storage_b0[i]   <- coef(mylm)[1]
  storage_b1[i]   <- coef(mylm)[2]
  storage_rmse[i] <- summary(mylm)$sigma
}

sd(storage_b1)   # empirical standard error of the slope
```

Overlaying all 5000 fitted lines produces a fan around the true green line; the histograms of
`storage_b0` and `storage_b1` are the sampling distributions, each centered on the true value
with a spread equal to the coefficient's standard error. That picture — betas are unbiased,
but they scatter, and the scatter shrinks with larger $n$ and smaller $\sigma$ or a wider
spread of $X$ — is exactly what makes a Battleship model with a high R² and significant
p-values possible to build in the first place.

Source: `~/Projects/school/byui-undergrad/MATH425/SamplingDistributions-1.Rmd`

## Reverse-engineering (the guesser's side)

When you're on the receiving end, you only have `rbdata.csv` and have to *find* the model.
The workflow is the mirror image of building one, and it's the same diagnostic toolkit used
throughout this chapter:

1. **Scatter `y` against each `x`** to spot which predictors matter and whether the relation
   looks straight, curved, or fanned.
2. **Read the residual-vs-fitted plot** for a curve (missing a polynomial/interaction term) or
   a widening spread (a Y-transformation is hiding).
3. **Try the allowed transforms** — a Box-Cox analysis suggests the Y-power; a curved scatter
   suggests `X^2` or `log(X)`. (I did exactly this on the `Orange` tree data over in
   [Assumptions](assumptions.md), where Box-Cox pointed to a `sqrt(Y)` fit.)
4. **Confirm** by fitting the guessed model and checking that its terms come out significant
   with a good R² — if the true model was well-hidden, several different guesses can fit
   almost equally well, which is the whole tension of the game.

## Gotchas

- **The competition template ships with placeholders.** My submitted `.Rmd` still has
  `y <- 0` and `x# <- rep(0, n)` stubs, so it renders an empty `lm(y ~ 0)` — the hidden model
  itself was never committed to the file. The code above is the *methodology* the exercise is
  built on (from my class-activity and sampling-distribution files, which are fully worked),
  not a specific secret model, so none of these numbers are invented.
- **Significant-everything is a real constraint.** Rule 3 means you can't just throw ten
  predictors in — every term in your true model has to earn its p-value, so you tune $n$ and
  $\sigma$ until the signal beats the noise.
- **Transformations break the rules if you're careless.** `Y = (β0 + β1·X)^2 + ε` is illegal
  (you transformed a *group* of terms); `sqrt(Y) = β0 + β1·X^2 + ε` is legal (individual terms
  only). Keep the linear-in-the-betas structure intact.
- **`set.seed` matters twice.** It makes your simulated CSV reproducible, and it makes the
  sampling-distribution histograms stable — but only if you run the whole chunk as one piece,
  since running lines separately advances the RNG differently.
