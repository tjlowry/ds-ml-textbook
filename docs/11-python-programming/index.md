# Python Programming

## Overview

Every other chapter in this book assumes I can already *write Python* — spin up a function,
loop over a CSV, catch an exception, sketch a class. This chapter is where I actually
learned to do that. It's the fundamentals chapter, and I've kept it deliberately light: the
concepts are covered well enough to jog my memory, then it gets out of the way. If you want
the deep end, that's what the [Machine Learning](../08-machine-learning/index.md) and
[Scientific ML](../12-scientific-ml/index.md) chapters are for.

It draws on two separate streams of my own coursework — from two different schools, and I'm
careful not to conflate them:

- **CSE 111 — "Programming with Functions" (BYU-Idaho undergrad).** This is where the code
  lives. A folder of ~45 small assignment programs I wrote: a compound-interest projector, a
  text-adventure game, a chemical-formula parser, CSV receipt builders, a tire-air-volume
  calculator, and a final "student-chosen" project that predicts an NBA team's win rate with
  a random forest. These are **my own programs**, so they're the backbone of every "How I did
  it" snippet — with two caveats I honor throughout: a handful of files started from
  instructor-provided skeletons (I rewrite those as fresh equivalents rather than quote them),
  and a couple of the data fixtures contain real names, which never appear here.
- **STAT 624 — "Data Science Toolbox" (Texas A&M grad, Dr. Scott A. Bruce).** The Week 9–10
  lecture notebooks (data structures, functions, classes, inheritance) and the Week 1 Git
  intro. These are the **instructor's copyrighted lecture material** — marked "do not
  distribute" — so I **paraphrase the concepts in my own words and cite the local file; I
  reproduce no lecture text, code, or outputs**. This is the same course and the same
  attribution rule as the [SQL & Databases](../07-sql-and-databases/index.md) chapter.

> **Attribution & privacy.** STAT 624 lecture notebooks and the Week 1 Git deck are Dr.
> Bruce's copyrighted course material — summarized here in my own words, nothing copied.
> Every code snippet is my own CSE 111 work. All data shown is either public-style aggregate
> data (national traffic stats) or invented; the assignment fixtures that held real student
> and children's names are never reproduced.

## Topics

- [Data Structures](data-structures.md) — lists, dictionaries, tuples, and sets, and how to
  pick the right one.
- [Functions](functions.md) — defining functions, DRY, scope, pass-by-value vs
  pass-by-reference, and `lambda`.
- [Classes & OOP](classes-and-oop.md) — `__init__`, `self`, instance/class/static methods,
  properties, and a short tkinter GUI aside.
- [Inheritance](inheritance.md) — single/multiple/multi-level inheritance, `super()`, and the
  method resolution order.
- [Error Handling](error-handling.md) — `try`/`except`, catching the right exception, and
  raising your own.
- [File I/O](file-io.md) — reading and writing text and CSV files, and the dict-lookup
  pattern.
- [Testing with pytest](testing-with-pytest.md) — why test functions matter, `assert`, and
  comparing floats with `pytest.approx`.
- [Modules & Packaging](modules-and-packaging.md) — scripts vs modules, `import`, and
  `if __name__ == "__main__"`.
- [Git Basics](git-basics.md) — the version-control workflow: working directory → staging →
  commit → remote.

## Notebook

- [Chemical Formula Parser](notebooks/chemical-formula-parser.ipynb) — my CSE 111
  molar-mass project, re-paired so it actually runs: a periodic-table dictionary, a recursive
  formula parser that raises a custom exception, molar-mass computed for a few molecules, and
  a handful of inline `assert` checks.

## Key Takeaways

- **Functions are the unit of clean code.** The single biggest lesson of the course: I
  rewrote my ML project *with* functions and it went from a tangle to something I could read
  and test. Split each task into its own function that takes parameters and returns a result.
- **Pick the data structure that matches the access pattern.** List for order, dict for
  lookup-by-key, set for membership/dedup, tuple for a fixed record. Getting this right makes
  the rest of the program fall out naturally.
- **Test the pure functions, not the I/O.** Functions that take inputs and return a result
  are trivial to test; functions that read `input()` and `print()` are not. Write most of
  your logic as the former.
