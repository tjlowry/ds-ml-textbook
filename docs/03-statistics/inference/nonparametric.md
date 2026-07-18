# Nonparametric Tests

## Overview

Most of the classic inference tools (t-tests, ANOVA, ordinary regression) lean on the data
being roughly normal, or on a sample big enough for the Central Limit Theorem to rescue the
sampling distribution of the mean. When those assumptions fail — small samples, heavy skew,
ordinal outcomes, or outliers that a Q-Q plot flags as non-normal — I reach for a
**nonparametric** test instead. These tests trade a bit of power (when normality *does*
hold) for robustness: they work on **ranks** or on **resampling** rather than on the raw
values and their assumed distribution.

| Situation | Parametric | Nonparametric alternative |
|---|---|---|
| Two independent groups | Two-sample t-test | **Wilcoxon rank-sum** (Mann-Whitney) |
| Paired / two related samples | Paired t-test | **Wilcoxon signed-rank** |
| 3+ independent groups | One-way ANOVA | **Kruskal-Wallis** |
| Any statistic, unknown null distribution | (depends) | **Permutation test** |

The null hypothesis is usually phrased in terms of distributions or medians ("both samples
come from the same distribution") rather than means.

!!! note "Attribution"
    Several examples on this page are adapted from the
    [BYU-I Statistics-Notebook](https://github.com/byuistats/Statistics-Notebook) (GPL-3.0),
    which supplied the dataset framing and the permutation-test scaffolding I built on. The
    analyses, data choices, and interpretations are my own MATH 425 (BYU-Idaho, Winter 2024)
    work.

## Wilcoxon Rank-Sum (Mann-Whitney)

The rank-sum test compares two independent groups by pooling all observations, ranking them,
and asking whether one group's ranks are systematically higher. It's the go-to when the
outcome is ordinal or the group sizes are small.

### How I did it

I looked at the `Friendly` dataset (`library(car)`), from a study on how the *order* new
material is presented affects memory recall. Two teaching conditions — **Meshed** (new words
interleaved with previously-recalled words) and **Before** (recalled words shown first, then
new ones) — were compared on the number of words correctly recalled out of 40. Because the
outcome is a bounded count and I only wanted to compare the two active conditions (dropping
the `SFR` control), I used a rank-sum test rather than a t-test:

```r
library(mosaic); library(car); library(pander)

Friend <- filter(Friendly, condition != 'SFR')   # keep Meshed vs Before

Friend %>%
  group_by(condition) %>%
  summarise(median = median(correct), mean = mean(correct), n = n()) %>%
  pander()

wilcox.test(correct ~ condition, data = Friend,
            mu = 0, alternative = 'two.sided') %>% pander()
```

The boxplot made "Before" look better (median **39** vs **36.5** correct), but the rank-sum
test returned **p = 0.378**, so I failed to reject the null. My conclusion was that both
methods are effectively equivalent and a teacher can pick whichever suits their students.

$$
  H_0: \mu_\text{Meshed} - \mu_\text{Before} = 0 \qquad H_a: \mu_\text{Meshed} - \mu_\text{Before} \neq 0
$$

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/Wilcoxon Tests/RecallingWords.Rmd`

## Kruskal-Wallis

Kruskal-Wallis is the rank-based generalization of one-way ANOVA to three or more groups.
The natural time to reach for it is exactly when the ANOVA diagnostic plots tell you the
normality assumption is broken.

### How I did it

Using a student food-choices survey, I tested whether **diet type** relates to **GPA**. The
diet was coded 1–4 (1 = healthy/balanced, 2 = unhealthy/random, 3 = repetitious, 4 =
unclear). I started toward an ANOVA, but the normal Q-Q plot of the ANOVA residuals was
clearly non-normal — which is precisely what pushes you from ANOVA to Kruskal-Wallis:

```r
food <- filter(food, GPA > 0 & GPA < 5)     # drop impossible / missing GPAs

# The ANOVA's Q-Q plot showed non-normal residuals:
test.aov <- aov(GPA ~ diet_current_coded, data = food)
plot(test.aov, which = 2)

# ... so the appropriate test is Kruskal-Wallis:
kruskal.test(GPA ~ diet_current_coded, data = food) %>% pander()
```

$$
  H_0: \text{all groups come from the same distribution} \qquad
  H_a: \text{at least one group is stochastically different}
$$

The test returned **p = 0.1924**, so I failed to reject: a student's self-reported diet
category does not have a statistically significant effect on GPA. The group medians and means
were all close, and — as I noted — GPA has far more going into it than diet, and these values
were self-reported.

Source: `~/Projects/school/byui-undergrad/statistics-notebook/Analyses/Kruskal-Wallis Test/Food.Rmd`

## Permutation Tests

A permutation test builds the null distribution *empirically*. The logic: if the grouping
label has no effect, then shuffling the labels shouldn't change the test statistic much. So I
compute the statistic on the real data, then recompute it thousands of times on shuffled
labels, and see where the observed value falls in that shuffled distribution. The p-value is
just the fraction of shuffles at least as extreme as what I observed. This works for *any*
statistic — a t-stat, an F-stat, even a logistic-regression z — without assuming a
theoretical null distribution.

### How I did it

**Two groups (permuting a t-statistic).** Comparing car weight between 4- and 8-cylinder
cars in `mtcars`, I shuffled the `wt` values 2000 times and rebuilt the t-statistic each time:

```r
car <- filter(mtcars, cyl %in% c(4, 8))
observed <- t.test(wt ~ cyl, data = car)$statistic

N <- 2000
permuted <- rep(NA, N)
set.seed(21)
for (i in 1:N) {
  permuted[i] <- t.test(sample(wt) ~ as.factor(cyl), data = car)$statistic
}

hist(permuted, xlim = c(-7, 7)); abline(v = observed, col = "blue")

# two-sided permutation p-value
sum(permuted >= observed) / N * 2
```

The observed t-statistic sat far out in the tail of the shuffled distribution, matching the
strong difference the parametric t-test also finds.

**Three-plus groups (permuting an F-statistic).** The same recipe works with an ANOVA
F-statistic — here `price ~ clarity` — by shuffling the grouping factor and re-extracting the
F value each iteration:

```r
observed_F <- summary(aov(price ~ clarity, data = diamonds))[[1]]$`F value`[1]

N <- 100
permuted_F <- rep(NA, N)
for (i in 1:N) {
  permuted_F[i] <- summary(aov(price ~ sample(clarity), data = diamonds))[[1]]$`F value`[1]
}
hist(permuted_F); abline(v = observed_F)
```

**Paired data (sign-flipping).** For paired measurements the permutation isn't a full
reshuffle — it's randomly flipping the sign of each within-pair difference, which is what
"no treatment effect" implies:

```r
N <- 2000
permutedTestStats <- rep(NA, N)
for (i in 1:N) {
  flip <- sample(c(-1, 1), size = 30, replace = TRUE)     # random sign per pair
  d <- flip * (theData$values[theData$group == 1] - theData$values[theData$group == 2])
  permutedTestStats[i] <- t.test(d, mu = 0)$statistic
}
```

Source: `~/Projects/school/byui-undergrad/statistics-notebook/permutation_practice.Rmd`

## Gotchas

- **Nonparametric ≠ assumption-free.** The rank-sum and Kruskal-Wallis tests still assume the
  groups have similarly *shaped* distributions; when that holds they test medians, otherwise
  they test the more general "same distribution."
- **Let the diagnostics choose the test.** The honest reason I used Kruskal-Wallis on the GPA
  data is that the ANOVA Q-Q plot failed — decide *after* looking at the residuals, not before.
- **Set a seed for permutation tests.** Results are random. Without `set.seed(...)` the p-value
  wobbles run to run, and small `N` (I used 100 in a couple of examples) makes it wobble more —
  bump `N` up for a stable p-value.
- **Two-sided bookkeeping.** For a two-sided permutation p-value you double the one-tailed tail
  proportion (or count `abs()` beyond `abs(observed)`); it's easy to report a one-sided p-value
  by accident.
- **Ties.** Lots of tied ranks (common with bounded counts like "words recalled") make R warn
  that it "cannot compute exact p-value with ties" and fall back to a normal approximation —
  usually fine, but worth noticing.
