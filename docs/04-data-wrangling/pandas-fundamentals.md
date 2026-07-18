# pandas Fundamentals

## Summary

Before any reshaping or modeling, a raw file needs the boring, essential first pass:
**read it, fix how "missing" is encoded, get the dtypes right, and clean up the strings and
column names**. None of this is glamorous, but skip it and every later step inherits the
mess. This page collects the fundamentals I reach for on literally every dataset, each shown
with real code from my DS 250 work.

The single most important idea here: **pandas only treats `NaN` (and `None`/`NaT`) as
missing.** Anything else in the file — a `-999`, the string `"N/A"`, a blank cell — is just
data as far as pandas is concerned, and it will happily average it into your results. Fixing
that is job one.

## Normalizing missing-value sentinels

Real datasets encode "missing" in whatever way the source system happened to use. One
coding-challenge dataset packed *four* different sentinels into a single column: the string
`'N/A'`, the number `-999`, the string `'broken'`, and an actual `np.nan`. The task was to
turn all of them into real `NaN`, then impute from a second column:

```python
import pandas as pd
import numpy as np

my_df = pd.DataFrame({
    "column1": ['N/A', 52, 22, 45, 31, -999, 21, 2, 0, 0, 'broken',
                19, 6, 27, 0, np.nan, 0, 33, 42, -999],
    "column2": [25.7, 6.6, 42.5, 72.0, 4.8, 4.0, 81.2, 654.5, 42.0, 5.7,
                54.2, 4.2, 6.3, 76.5, 7.2, 42.5, 76.8, 46.2, 11.9, 94.6],
})

# Every non-standard sentinel -> real NaN
my_df.replace('N/A', np.nan, inplace=True)
my_df.replace(-999, np.nan, inplace=True)
my_df.replace('broken', np.nan, inplace=True)

# Impute the gaps with the mean of the paired column
fill_value = my_df["column2"].mean()
my_df.replace(np.nan, fill_value, inplace=True)

print(f"Mean: {my_df['column1'].mean()}")
print(f"Std:  {my_df['column1'].std()}")
```

Source: `~/Projects/school/byui-undergrad/DS_250/Coding_challenge/ds250_challenge.qmd`
(my own, DS 250; mirrored at `course-files/04-data-wrangling/ds250-final-chal-wrangling.qmd`).

Once several sentinels are in play, listing them out for one `replace` is cleaner than
chaining calls. That's the pattern I used to finish the flights dataset — one sweep that maps
every string flavor of "missing" to a single `NaN`:

```python
df = df.replace(['', ' ', 'NA', 'N/A', 'null', 'None', 'nan'], np.nan)
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project 2/Project2.qmd`
(my own, DS 250; the flights case study). The full end-to-end version, including the numeric
`-999` sentinel, is in the [missing-data case study](missing-data-case-study.md).

## Dtype casting

A sneaky consequence of a text sentinel: **one `'broken'` in a column of numbers forces the
whole column to `object` dtype**, and arithmetic on it silently misbehaves or errors. After
cleaning the sentinels out, cast the column back to a real numeric type so `.mean()`,
comparisons, and model code behave:

```python
# income_group came in as object because of the text 'no' sentinel for missing;
# cast to float before doing math or thresholding on it.
df['target'] = df['income_group'].astype(float).apply(
    lambda x: 1 if (x >= 3 and x < 6) else 0)
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project5/project_5.qmd` (my own, DS 250;
mirrored at `course-files/04-data-wrangling/data_cleaning_starwars.qmd`). The `.astype(float)`
there is load-bearing — the column was `object`, and the `>=` comparison needs a number.

## String cleaning with `.str`

pandas exposes vectorized string methods through the `.str` accessor — the same operations
you'd write on one Python string, applied down a whole column at once. From the tidy-data
lesson, working a small `firstname`/`surname` frame:

```python
df['surname'].str.capitalize()          # 'brown' -> 'Brown'
df['surname'].str.isalpha()             # True/False mask: letters only?
df['surname'].str.replace('Brook', 'Brooke')
df['surname'].str.contains('B')         # boolean mask for filtering
df['surname'].str.count('[aeiou]')      # regex: vowels per value
df['surname'].str.len()                 # length of each string
```

Source: `course-files/04-data-wrangling/data_cleaning_lesson.ipynb` (my own-typed DS 250
"Week 10" tidy-data lesson; mirrors `DS_250/Project5/week11_class/week10-lesson2.ipynb`).

The `.str.split(expand=True)` method — splitting one string column into several — is common
enough that I gave it its own treatment on the
[tidy-data & reshaping](tidy-data-reshaping.md#splitting-one-column-into-several) page.

## Renaming columns

When a file's column names are unusable — survey questions, `Unnamed: 4`, trailing
encoding junk — a rename dictionary maps old to new in one pass. The Star Wars export was the
extreme case: 34 columns, most of them either a full survey question or an anonymous
`Unnamed: N`. A dictionary makes the mapping explicit and reviewable:

```python
names = {
    'RespondentID': 'response_id',
    'Have you seen any of the 6 films in the Star Wars franchise?': 'seen_all',
    'Do you consider yourself to be a fan of the Star Wars film franchise?': 'fan',
    'Which of the following Star Wars films have you seen? Please select all that apply.': 'watch_ep1',
    'Unnamed: 4': 'watch_ep2',
    # ... 30 more ...
    'Which character shot first?': 'shot_first',
}
df = df.rename(columns=names)
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project5/project_5.qmd` (my own, DS 250).
The full 34-entry dictionary and the rest of that cleanup are in the
[Star Wars case study](case-study-star-wars-survey.md).

## Gotchas

- **`-999` is not missing to pandas — it's negative nine hundred ninety-nine.** It will drag
  a mean down hard and never trigger `.isna()`. Grep new numeric columns for absurd sentinel
  values (`-999`, `9999`, `-1`) before trusting any summary statistic.
- **One text value poisons a whole numeric column's dtype.** A single `'broken'` or `'no'`
  makes the column `object`; `.mean()` then either errors or does string concatenation. Clean
  sentinels *first*, then `.astype(float)`.
- **`inplace=True` returns `None`.** `df = df.replace(...)` and `df.replace(..., inplace=True)`
  both work, but `df = df.replace(..., inplace=True)` gives you a `None` and silently deletes
  your DataFrame. Pick one form per line.
- **`.str` methods skip `NaN` and can return `NaN`.** `df['col'].str.contains('B')` yields
  `NaN` (not `False`) for missing entries, which then breaks boolean indexing — pass
  `na=False` when you use the mask to filter.
- **A rename dict is silent about typos.** `rename(columns=...)` ignores keys that don't
  match any column, so a mistyped source name just... doesn't rename, with no error. Diff the
  before/after column list to confirm every rename landed.
