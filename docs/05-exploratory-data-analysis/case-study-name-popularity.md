# Case Study: Name Popularity

## Summary

This is a small, question-driven EDA from my BYU-Idaho DS 250 coursework: given a public
dataset of how many U.S. babies were given each name in each birth year, *estimate how old a
typical person with a given name is today*. It's a good example of EDA that isn't a
scattershot survey of a table — it starts from one concrete question and reads a single
distribution to answer it. The data is the public
[byuidatascience baby-names](https://github.com/byuidatascience/data4names) set (name, birth
year, per-state counts, and a national `Total`), which I link and load at runtime rather than
re-hosting.

## How I did it

### Load and derive an age

The frame arrives one row per (name, year). The only transform the question needs is turning
the birth `year` into an approximate current `age`:

```python
import pandas as pd

names = pd.read_csv(
    "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
)

names["age"] = names["year"].apply(lambda x: 2023 - x)
```

Source: `course-files/05-exploratory-data-analysis/name_pop_eda.ipynb` (my own, BYU-Idaho
DS 250). The assignment framing — *how old is someone named X* — is the instructor's; I
paraphrase it.

### Read one name's distribution

To answer the question for a single name, I subset to that name and look at how its `Total`
count is spread across ages. That spread *is* the distribution of likely ages for someone
with the name — its peak is the most common birth cohort, and its width tells you how
concentrated the name is in time:

```python
import altair as alt

russell = names.query('name == "Russell"')

chart = alt.Chart(russell, title="How old is someone named Russell").encode(
    alt.X("age", scale=alt.Scale(domain=(0, 120))),
    alt.Y("Total", title="Frequency"),
).mark_line(color="Red")

chart
```

Reading the curve answers the question directly: the age where the line peaks is the single
most likely age, and a name whose curve is a tall narrow spike (a fad name) pins an age far
more tightly than one that's been steadily popular for decades (a broad, flat curve). Same
plot, different name, different answer — the technique is the reusable part.

Source: same notebook. This "subset, then read the distribution" move is the whole method;
the [summaries & distributions](summary-and-distributions.md) page covers the more general
`value_counts` / group-by version of it.

## Notebook

The full exploration — load, first-look summaries, the age transform, and the single-name
distribution chart — is in
[Name-Popularity EDA](notebooks/name-popularity-eda.ipynb). I trimmed my original DS 250
notebook down to just the names exploration (it also carried some unrelated coding-challenge
and modeling answers that belong to the [Data Wrangling](../04-data-wrangling/index.md) and
[Machine Learning](../08-machine-learning/index.md) chapters), added a context cell, and
re-ran it top to bottom against the public dataset.

## Gotchas

- **The "age" here is a birth-cohort proxy, not a real age.** `2023 - year` assumes everyone
  with the name is still alive and that the dataset counts births, not living people. It's
  fine for "which cohort is this name from," and wrong for anything actuarial — know which
  question you're actually answering.
- **A name with a narrow spike is far more predictive than a flat one.** The *shape* of the
  distribution, not just its peak, is the finding. Reporting only the single most likely age
  throws away how confident you're allowed to be.
- **`.query('name == "Russell"')` needs the quoting right.** The outer quotes and the inner
  string quotes have to differ, and the column has to exist exactly as named — a typo returns
  an empty frame and a blank chart, not an error.
- **Fixing the x-axis domain matters when comparing names.** `alt.Scale(domain=(0, 120))`
  pins the age axis so two names are drawn on the same scale; without it Altair auto-fits each
  chart and the curves look more similar than they are.
