# SQL & Databases

## Overview

This is the deliberately **lighter** chapter of the book. SQL is a tool I reach for
constantly — pulling data for an analysis, standing up a schema for a side project,
wiring Python to a database — but it's a skill you learn by *doing queries*, not by
reading pages of theory. So this chapter covers the concepts well and then gets out of
the way: one consolidated query reference, one schema-design page, one Python-integration
page, two "know these exist" pages on non-relational stores and compute, and a runnable
notebook.

It draws on two streams of my own work:

- **STAT 624 — "Data Science Toolbox" (Texas A&M grad, Dr. Scott A. Bruce).** The
  relational-database, SQL, NoSQL, Docker, and Dask/parallelization material. These are
  the instructor's copyrighted lecture decks and notebooks — I **paraphrase concepts and
  cite the local originals; I reproduce no slide text, figures, or executed outputs**.
- **DS 250 — "Data Science Programming" (BYU-Idaho undergrad).** My own baseball-analytics
  project against the [Lahman baseball database](http://seanlahman.com/) (SQLite), plus a
  Pokemon relational schema I designed in MySQL Workbench for a database assignment. This
  is my own code, no license issue — it's the backbone of the query examples and the
  notebook.

Every query on the [SQL Essentials](sql-essentials.md) page is a real query from one of
those two projects (or, where I had no real example, an honestly-labeled teaching query).

> **Attribution & privacy.** STAT 624 lecture PDFs and notebooks are the instructor's /
> TA's copyrighted course material — this chapter summarizes ideas in my own words and
> cites the local file; no content or output is copied. The Pokemon schema and the DS 250
> baseball queries are my own work. All data shown is either public (Lahman baseball) or
> invented (Pokemon).

## Topics

- [SQL Essentials](sql-essentials.md) — one page, the whole query toolkit: `SELECT`,
  filtering, joins, aggregations, subqueries, and window functions, each shown with a
  real query.
- [Schema Design](schema-design.md) — keys, relationships, and normalization, taught
  through the Pokemon ERD I built (bugs and all).
- [Python & Databases](python-and-databases.md) — `sqlite3`, SQLAlchemy, and `pymysql`
  patterns, grounded in my investing project's database manager.
- [Database Types](database-types.md) — beyond relational: document, key-value, and graph
  stores, and when to reach for each.
- [Docker & Compute](docker-and-compute.md) — running databases in containers, and scaling
  past one machine with Dask and HPC clusters.

## Notebook

- [Pokemon SQL](notebooks/pokemon-sql.ipynb) — I load my Pokemon schema into an in-memory
  SQLite database, seed it, and run joins / aggregations / window functions against it;
  then run a few of my DS 250 baseball queries against the real Lahman SQLite DB.

## Key Takeaways

- **SQL is declarative.** You describe the result you want (`SELECT … WHERE … GROUP BY`);
  the engine figures out how to get it. That's the whole mental shift from pandas-style
  step-by-step manipulation.
- **Joins are the point of a relational database.** Data is split across tables to avoid
  duplication (normalization); joins put it back together on demand.
- **Know when *not* to use SQL.** Document, key-value, and graph databases each trade the
  relational model's guarantees for something else (flexibility, speed, relationship
  traversal). Pick the store that matches the shape of your data and your access pattern.
