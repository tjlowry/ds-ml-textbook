# Data Wrangling

## Overview

Every project in this book starts with data that is the wrong shape. Column names are
survey questions 90 characters long. "Missing" shows up as `-999` in one column, a blank
string in another, and the literal text `"1500+"` in a third. Years are spread across a
dozen columns when they should be one. **Data wrangling is the work of getting from that
mess to a tidy, model-ready table** — and in practice it's where most of the hours on any
real analysis actually go.

This chapter is built almost entirely from my **BYU-Idaho DS 250 ("Data Science
Programming")** coursework, where nearly every assignment handed me a deliberately messy
dataset and asked for a clean result:

- A **flights-delay** dataset with four different encodings of "missing" and a column that
  had to be *reconstructed* from business rules — the [missing-data case
  study](missing-data-case-study.md).
- A **FiveThirtyEight Star Wars survey** exported from Qualtrics, with 34 unusable column
  names, categorical answers that needed ordinal codes, and a target column to build before
  any model could touch it — the [Star Wars case study](case-study-star-wars-survey.md),
  the flagship of the chapter.
- A tidy-data lesson working the four reshape verbs (`melt`, `pivot`, split, unite) on the
  classic `table1`–`table5` teaching data — [tidy data & reshaping](tidy-data-reshaping.md).

The one page not from DS 250 is [NumPy arrays](numpy-arrays.md), which covers the
vectorization ideas underneath pandas. It's written from scratch — I only *cite* the
Texas A&M STAT 624 notebook that first taught me the material, because that notebook is
the instructor's copyrighted, do-not-distribute content (see the note below).

> **Attribution & privacy.** The DS 250 projects, the coding-challenge answers, and the
> tidy-data lesson code are my own work. The assignment *prompts* embedded in those files
> are the instructor's, so I paraphrase them rather than quote. The STAT 624 "Week 12"
> NumPy/pandas notebook (© 2023 Scott A. Bruce, "Do not distribute") is **cited only** — no
> text, code, or output from it appears here. All data shown is public: the
> [FiveThirtyEight Star Wars survey](https://github.com/fivethirtyeight/data/tree/master/star-wars-survey)
> and the [byuidatascience teaching datasets](https://github.com/byuidatascience) (flights,
> `table1`–`table5`, `mpg`). I link those sources rather than re-hosting the raw files.

## How each page is structured

The book's standard shape: a short **Summary**, a **"How I did it"** walk through real code
from my projects (each snippet tagged with a `Source:` path), a **Notebook** you can read
here and re-run locally, and a **Gotchas** section of what tripped me up.

## Topics

- [pandas Fundamentals](pandas-fundamentals.md) — reading messy files, normalizing missing
  values, dtype casting, string cleaning, and renaming columns.
- [NumPy Arrays](numpy-arrays.md) — arrays vs. lists, vectorization and broadcasting, and
  why the array is the object pandas is built on.
- [Tidy Data & Reshaping](tidy-data-reshaping.md) — the tidy-data rules and the four reshape
  verbs: `melt`, `pivot_table`, splitting one column into several, uniting several into one.
- [Missing Data: A Flights Case Study](missing-data-case-study.md) — multiple missing-value
  encodings in one real dataset, plus rule-driven imputation and a derived column.
- [Case Study: The Star Wars Survey](case-study-star-wars-survey.md) — cleaning a
  Qualtrics export end to end into an ML-ready feature matrix.

## Notebooks

- [Flights: Missing Data & Imputation](notebooks/flights-data-wrangling.ipynb) — my DS 250
  Project 2, re-run against the public flights dataset.
- [Tidy Data: melt / pivot / split / unite](notebooks/tidy-data-lesson.ipynb) — the reshape
  verbs demonstrated on small public teaching tables.

## Key Takeaways

- **"Missing" is not one thing.** Real files encode it as sentinels (`-999`, `"N/A"`,
  `"broken"`, blank strings) that pandas reads as ordinary data. The first job is always to
  map every one of them to a single canonical `NaN` — otherwise every downstream mean, sum,
  and model is quietly wrong.
- **Tidy data has a definition:** one variable per column, one observation per row, one
  value per cell. Most wrangling is just moving a messy table toward that shape with a
  handful of reshape verbs.
- **Wrangling is upstream of modeling, not separate from it.** Ordinal encoding, one-hot
  encoding, and building a target column are wrangling steps that decide what a model can
  even learn — the Star Wars case study runs straight from raw CSV into a
  `RandomForestClassifier` to make that link concrete.
