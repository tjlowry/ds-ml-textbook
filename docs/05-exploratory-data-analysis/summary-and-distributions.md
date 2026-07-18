# Summaries & Distributions

## Summary

This is the first-look toolkit I run on almost every new table: look at a few rows, check
the dtypes and the holes, count the categories, and throw together a quick chart of the
distribution. The example here is a data-exploration exercise from my BYU-Idaho CSE 450
coursework — a consumer-watchdog question about whether a streaming catalog skews toward
adult or children's movies — worked on the public **Netflix titles** dataset. The whole job
is to *understand* the catalog well enough to answer the question, not to build anything
polished.

## How I did it

### First look: rows, types, and holes

The first three commands never change. Load the file, look at the head, and get a technical
summary of types and missingness — that's enough to know what I'm holding:

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/netflix_titles.csv")

df.head()          # what do the columns and a few values actually look like?
df.dtypes          # did every column come in as the type I expected?
df.isna().sum()    # how many missing values per column?
```

Source: `course-files/05-exploratory-data-analysis/basic_data_eda.py` (my own worked
answers, BYU-Idaho CSE 450; the exercise scaffold and the Netflix teaching dataset are the
course's, linked not re-hosted). The prompt's checklist — *what does the data look like,
what type is each column, which columns have missing values* — is exactly the first-look
loop, so it's the one I lead with.

### Subset, then count

Most exploratory questions are really "how many of each, within some subset." Filtering to
the rows that matter and then counting the values of a column answers a surprising number of
them. Here I narrow to movies, then count the MPAA `rating` values:

```python
# Keep just the movies — the column stores "Movie" / "TV Show", capitalized
movies = df[df["type"] == "Movie"]

# How many rows survived the filter?
movies["rating"].count()

# The actual distribution of the rating column
movies["rating"].value_counts()
```

`value_counts()` is the single most useful line in EDA: it's how I discover categories I
didn't know were there. Running it on `rating` is what surfaced the "made for TV" ratings
(`TV-MA`, `TV-14`, ...) that don't fit the MPAA scheme at all — a data reality the original
question never anticipated. Once I could see them, I could decide to exclude them:

```python
mpaa = ["G", "PG", "PG-13", "R", "NC-17"]
rated = movies[movies["rating"].isin(mpaa)].dropna()
rated.value_counts("rating")
```

Source: same file. Group-by aggregation (`df.groupby(key)[col].agg(...)`) is the
generalization of this pattern to more than one key — the same "split, then summarize" idea,
and the move I reach for on the names data in the
[name-popularity case study](case-study-name-popularity.md).

### One distribution, three libraries

For the exploration stage I don't care which plotting library draws the bar chart — I reach
for whatever is closest. It's worth seeing that the *same* count plot is a one-liner in all
three of the libraries I use. Altair, declaring the encoding and letting it aggregate:

```python
import altair as alt

alt.Chart(rated).mark_bar().encode(
    alt.X("rating"),
    alt.Y("count(rating)"),
)
```

seaborn, with a purpose-built count plot:

```python
import seaborn as sns

sns.countplot(rated, x="rating")
```

pandas' own plotting, straight off the `value_counts` result:

```python
counts = rated.value_counts("rating")
counts.plot.bar()
```

Source: same file. The polished versions of these — titles, labels, palettes, and when to
pick which library — are the subject of the
[Data Visualization](../06-data-visualization/index.md) chapter; here they're just fast ways
to *see* the distribution.

## Gotchas

- **`df.isna` without the parentheses does nothing useful.** `df.isna` is the method object;
  `df.isna()` is the boolean frame you actually want, and `df.isna().sum()` is the per-column
  count. Easy to leave the parens off and get a truthy object that never warns you.
- **`value_counts()` drops `NaN` by default.** Missing values silently vanish from the
  counts, so the bars can sum to fewer rows than you have. Pass `dropna=False` when "how much
  is missing" is part of the question.
- **A filter that matches nothing returns an empty frame, not an error.** My original CSE 450
  script filtered on `df["type"] == "movie"` — lowercase — but the column stores `"Movie"`,
  so the subset was silently empty (the snippet above is the corrected version). Check
  `.shape` (or `value_counts()` the column first) before trusting a subset — string case and
  stray whitespace are the usual culprits.
- **`count()` counts non-null, `len()`/`.shape[0]` counts rows.** They disagree exactly when
  a column has missing values, which is often the thing you're trying to measure. Know which
  one you're asking for.
- **EDA plots are throwaway on purpose.** No titles, no axis labels, no color choices — the
  moment a chart needs those, it has graduated from exploration to communication and belongs
  in the [visualization chapter](../06-data-visualization/index.md), not in this loop.
