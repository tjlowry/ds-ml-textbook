# SQL Essentials

## Overview

This is the one page I'd want open while writing a query. It walks the toolkit in the
order the clauses actually execute against the data — pick columns, filter rows, join
tables, aggregate groups, nest queries, then window over rows — and every step is a **real
query from my own work**: my DS 250 baseball analysis against the Lahman SQLite database,
or my Pokemon schema. Where I never wrote a real example (subqueries), I say so and teach
the concept plainly instead.

The mental model to hold onto: SQL is **declarative**. You describe the result set you
want; the engine plans how to produce it. That's the whole difference from writing a
pandas pipeline step by step.

> **Clause execution order** (not the order you write them): `FROM`/`JOIN` → `WHERE` →
> `GROUP BY` → `HAVING` → `SELECT` → `window functions` → `ORDER BY` → `LIMIT`. Knowing
> this explains a lot of "why can't I use my column alias in `WHERE`?" errors — `WHERE`
> runs before `SELECT` computes the alias.

## SELECT, filtering, and sorting

The base of everything: choose columns, keep the rows you want with `WHERE`, order them,
and cap the count with `LIMIT`. Here's my DS 250 batting-average query — hits over at-bats,
best averages first, top 5 only:

```sql
SELECT b.playerid, b.yearid,
       CAST(b.h AS FLOAT) / CAST(b.ab AS FLOAT) AS batting_avg
FROM batting b
WHERE b.ab > 10
ORDER BY batting_avg DESC, b.playerid
LIMIT 5;
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.qmd` (my own, DS 250).

Two things I learned the hard way here, both in the [Gotchas](#gotchas): the `CAST(... AS
FLOAT)` is not optional, and `ORDER BY batting_avg` works even though `batting_avg` is a
computed alias — because `ORDER BY` runs *after* `SELECT`.

## Joins

Joins are why a relational database exists: data is deliberately split across tables so
nothing is duplicated, and a join stitches it back together on a shared key. The most
common is the **inner join** (`JOIN`), which keeps only rows that match on both sides.

My DS 250 question "which BYU-Idaho players made it to the majors, and what did they earn?"
needs three tables chained together — a school, who played there, and their salaries:

```sql
SELECT c.playerID, s.schoolID, sa.salary, sa.yearid, sa.teamid
FROM schools s
JOIN collegeplaying c ON c.schoolid = s.schoolid
JOIN salaries sa      ON sa.playerid = c.playerid
WHERE s.schoolid = 'idbyuid'
ORDER BY sa.salary DESC;
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.qmd`.

**`LEFT JOIN` keeps every row from the left table** even when the right side has no match
(you get `NULL`s for the missing columns). That's what you want for a "give me everything
about X, and fill in related details where they exist" query. The master query for my
Pokemon schema is built entirely from left joins so that a pokemon with, say, no second
type still shows up:

```sql
SELECT p.pokemon_name, g.generation, r.region_name, rar.rarity_name
FROM pokemon p
LEFT JOIN generation g   ON p.generation_id = g.generation_id
LEFT JOIN region     r   ON p.region_id     = r.region_id
LEFT JOIN rarity     rar ON p.rarity_id      = rar.rarity_id;
```

Source: adapted from `~/Projects/…/db_assignment/Queries.txt` (my own Pokemon schema). The
original chained 9 `LEFT JOIN`s to flatten the whole schema into one wide "turn all the
foreign keys into readable values" result — the pattern you reach for when handing a
denormalized extract to someone who doesn't want to write joins themselves.

**Many-to-many needs a junction table.** A pokemon has several types and a type has many
pokemon, so neither side can hold a foreign key to the other. The `pokemon_has_type`
junction table sits between them, and joining *through* it resolves the relationship — this
is demonstrated end-to-end in the [notebook](notebooks/pokemon-sql.ipynb).

## Aggregations

`GROUP BY` collapses rows into groups and computes one summary value per group with an
aggregate function (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`). My DS 250 career-batting-average
query groups every batting row by player and averages across their whole career, keeping
only players with real playing time:

```sql
SELECT b.playerid,
       AVG(CAST(b.h AS FLOAT) / CAST(b.ab AS FLOAT)) AS batting_avg
FROM batting b
WHERE b.ab > 100
GROUP BY b.playerid
ORDER BY batting_avg DESC, b.playerid
LIMIT 5;
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.qmd`.

The rule that trips everyone up: **every column in `SELECT` must be either inside an
aggregate or named in `GROUP BY`** — otherwise the engine doesn't know which row's value to
show for the group. And to filter *on an aggregate* you use `HAVING`, not `WHERE`, because
`WHERE` runs before the grouping happens:

```sql
-- keep only players whose career average clears .300
SELECT b.playerid, AVG(CAST(b.h AS FLOAT)/CAST(b.ab AS FLOAT)) AS avg
FROM batting b
GROUP BY b.playerid
HAVING avg > 0.300;
```

Aggregation depth (the `WHERE`-vs-`HAVING` split, `COUNT(DISTINCT …)`) is covered in STAT
624 Week 6 (local: `course-files/07-sql-and-databases/Week 6_Aggregation_Window
Functions.pdf`) — concept summary only, instructor-copyrighted.

## Subqueries

A subquery is a `SELECT` nested inside another query — used as a filter (`WHERE x IN
(SELECT …)`), as a derived table in the `FROM` clause, or as a scalar value in the
`SELECT` list.

> **Honest note:** I don't have a real subquery from my own projects — none of my DS 250
> or Pokemon queries needed one, and STAT 624 didn't give me a saved example either. So the
> query below is a **plain teaching example I wrote for this page**, not something I ran in
> anger. It's still valid SQL against the Lahman schema.

```sql
-- players whose career batting average beats the overall league average:
-- the inner query computes one number; the outer query compares against it.
SELECT b.playerid, AVG(CAST(b.h AS FLOAT)/CAST(b.ab AS FLOAT)) AS avg
FROM batting b
GROUP BY b.playerid
HAVING avg > (
    SELECT AVG(CAST(h AS FLOAT)/CAST(ab AS FLOAT))
    FROM batting
    WHERE ab > 0
);
```

The thing to understand is *correlated* vs *uncorrelated*: the subquery above is
**uncorrelated** — it computes a single value once, independent of the outer row. A
**correlated** subquery references the outer row and re-runs per row, which is powerful but
can be slow; often a join or a window function does the same job faster.

## Window functions

A window function computes across a set of rows *related to the current row* without
collapsing them the way `GROUP BY` does — you keep every row **and** get an aggregate,
ranking, or running total alongside it. The shape is `func() OVER (PARTITION BY … ORDER BY
…)`.

The classic use is ranking within groups. "Rank each player's seasons by batting average,
best season = 1, without losing the individual season rows":

```sql
SELECT b.playerid, b.yearid,
       CAST(b.h AS FLOAT)/CAST(b.ab AS FLOAT) AS avg,
       RANK() OVER (
           PARTITION BY b.playerid
           ORDER BY CAST(b.h AS FLOAT)/CAST(b.ab AS FLOAT) DESC
       ) AS season_rank
FROM batting b
WHERE b.ab > 100;
```

`PARTITION BY` is the window's equivalent of `GROUP BY` (which rows share a window), and
the `OVER (... ORDER BY ...)` orders rows *inside* each window — for `RANK`/`ROW_NUMBER`
and for running totals. This is **lecture-only in my STAT 624 material** (Week 6 PDF, no
runnable example was provided), so I wrote the query above myself and **actually run a
window function against my Pokemon data in the [notebook](notebooks/pokemon-sql.ipynb)** —
that's the executable proof for this section.

Concept source: STAT 624 Week 6 (local: `course-files/07-sql-and-databases/Week
6_Aggregation_Window Functions.pdf`) — instructor-copyrighted, summarized only.

## Notebook

See the rendered notebook: [Pokemon SQL](notebooks/pokemon-sql.ipynb) — joins,
aggregations, and a real window function against my Pokemon schema, plus DS 250 baseball
queries against the Lahman database.
Re-run locally: `jupyter lab docs/07-sql-and-databases/notebooks/pokemon-sql.ipynb`

## Gotchas

- **Integer division silently lies.** `b.h / b.ab` in SQLite (and Postgres) is *integer*
  division when both columns are integers — every batting average came out `0`. The fix is
  `CAST(... AS FLOAT)` on at least one operand. This was a real bug in my first DS 250
  query; the corrected version casts both sides.
- **`WHERE` can't see `SELECT` aliases.** Because `WHERE` runs before `SELECT`, you can't
  filter on a computed alias there — repeat the expression, or wrap the query. `ORDER BY`
  and `HAVING`, which run after, *can* use the alias.
- **`WHERE` filters rows, `HAVING` filters groups.** Reaching for `WHERE` on an aggregate
  is the most common grouping error. `WHERE b.ab > 100` (per-row) is fine; "average > .300"
  (per-group) must be `HAVING`.
- **`GROUP BY` requires every non-aggregated `SELECT` column.** MySQL will sometimes let
  you skip this (its old `ONLY_FULL_GROUP_BY`-off behavior) and hand back an arbitrary row;
  SQLite and Postgres are stricter. Don't rely on the lenient behavior.
