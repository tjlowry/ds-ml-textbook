# Exploratory Data Analysis

## Overview

Once a dataset is clean, the next question is the honest one: **what is actually in it?**
Exploratory data analysis (EDA) is the unglamorous looking-around I do before I trust a
single summary statistic or fit a single model — checking the shape and dtypes, counting
categories, eyeing distributions, and letting the data suggest the questions worth asking.

This is deliberately the lightest chapter in the book, because most of the *doing* lives
next door. The cleaning half — normalizing missing values, encoding, reshaping — is all in
[Data Wrangling](../04-data-wrangling/index.md), and the polished, presentation-quality
plots are in [Data Visualization](../06-data-visualization/index.md). What's left here, and
what this chapter is about, is the middle step: the quick, throwaway summaries and charts I
make *for myself* to understand a table before committing to anything.

## My EDA workflow

Every time I open a new dataset I walk the same short loop, roughly in this order:

1. **Shape & dtypes** — `df.shape`, `df.head()`, `df.dtypes`. How many rows and columns,
   and did each column come in as the type I expected?
2. **Missingness** — `df.isna().sum()`. Where are the holes, and are they the real holes or
   the [sentinel-encoded kind](../04-data-wrangling/pandas-fundamentals.md) that pandas
   won't flag?
3. **Summaries** — `df.describe()` for the numbers, `value_counts()` for the categories.
4. **Distributions** — a fast histogram or bar chart, thrown together in whatever library
   is closest to hand, just to see the shape.
5. **Relationships & questions** — group-by aggregations and correlations that turn a vague
   "I wonder if…" into something I can check.

The output of this loop is not a deliverable — it's a set of questions and a short list of
things I now know are true about the data.

## Where I did this

The pages here are built from two pieces of my own coursework:

- A **BYU-Idaho** data-exploration exercise on the public **Netflix titles** catalog —
  filter to movies, count MPAA ratings, and answer a stakeholder question. It's my worked
  example of the summary-and-count half of EDA, and of drawing the *same* count plot three
  different ways (Altair, seaborn, pandas).
- My own **names-popularity** notebook on the public
  [byuidatascience baby-names](https://github.com/byuidatascience/data4names) dataset, where
  a single question — *how old is a typical person with a given name?* — is answered by
  reading one name's frequency distribution across birth years.

I also consulted a **STAT 650 (TAMU)** lecture on EDA with pandas/NumPy/SciPy for the
concept framing; nothing from it is reproduced here.

## Topics

- [Summaries & Distributions](summary-and-distributions.md) — the first-look toolkit:
  `head`/`dtypes`/`isna`, `value_counts`, subset-and-count, and one count plot in three
  libraries.
- [Case Study: Name Popularity](case-study-name-popularity.md) — a question-driven EDA on
  the baby-names data, reading a single name's distribution over time.

## Notebooks

- [Name-Popularity EDA](notebooks/name-popularity-eda.ipynb) — my own DS 250 names notebook,
  trimmed to the exploration and re-run against the public dataset.

## Key Takeaways

- **EDA is looking, not deciding.** The point is to understand the table well enough to ask
  good questions — not to produce a finished chart or a fitted model. Both of those come
  later, in their own chapters.
- **`value_counts()` and `describe()` catch most surprises early.** A category you didn't
  know existed, a "made for TV" rating that breaks your scheme, a max value that's obviously
  a sentinel — the cheap summaries surface these before they poison an analysis.
- **EDA leads straight into modeling, and that's a hazard.** The exploration you do to
  choose features is also where [leakage](../10-model-evaluation/leakage-patterns.md) can
  sneak in if you peek at the whole dataset before splitting. Explore freely, but remember
  the test set is supposed to be unseen.
