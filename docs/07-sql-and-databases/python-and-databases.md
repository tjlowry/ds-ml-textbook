# Python & Databases

## Overview

Most of the time I don't sit in a SQL console — I drive the database from Python: pull a
result straight into a DataFrame for analysis, or run a whole application's reads and writes
through a manager class. This page collects the three access patterns I actually use, from
lightest to heaviest:

1. **`sqlite3` + pandas** — zero-setup, file-based, perfect for analysis. My DS 250 style.
2. **A hand-rolled `pymysql` manager** — context-managed connections and parameterized
   queries for a real MySQL-backed app. My investing project.
3. **SQLAlchemy** — the ORM / engine abstraction layer, when you want portability across
   database backends.

## sqlite3 + pandas — the analysis pattern

For analysis work, SQLite is unbeatable: the whole database is a single file, there's no
server to start, and Python ships `sqlite3` in the standard library. The pattern is three
lines — connect, hand a SQL string to `pandas.read_sql_query`, get a DataFrame back:

```python
import pandas as pd
import sqlite3

con = sqlite3.connect("lahmansbaseballdb.sqlite")
byui = pd.read_sql_query(
    """SELECT c.playerID, s.schoolID, sa.salary, sa.yearid, sa.teamid
       FROM schools s
       JOIN collegeplaying c ON c.schoolid = s.schoolid
       JOIN salaries sa      ON sa.playerid = c.playerid
       WHERE s.schoolid = 'idbyuid'
       ORDER BY sa.salary DESC""",
    con,
)
```

Source: `~/Projects/school/byui-undergrad/DS_250/Project 3/project3.py` (my own, DS 250).

The database does the join and filter (fast, and it never loads unrelated rows into
memory); pandas just receives the finished result set. This is the workflow the
[notebook](notebooks/pokemon-sql.ipynb) uses for every query.

## pymysql — the application pattern

For my investing project I wrote a `DatabaseManager` class over `pymysql` to back a real
MySQL database of market data. Two patterns from it are worth lifting out because they're
how you *should* talk to any SQL database from application code.

**Context-managed connections.** Credentials come from environment variables (never
hard-coded), and a `@contextmanager` guarantees the connection is closed even if the query
raises:

```python
import os
import pymysql
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self):
        self.db_host = os.getenv("DATABASE_HOST")
        self.db_name = os.getenv("DATABASE_NAME")
        self.db_user = os.getenv("DATABASE_USER")
        self.db_pass = os.getenv("DATABASE_PASS")

    @contextmanager
    def get_connection(self):
        con = pymysql.connect(
            host=self.db_host, user=self.db_user,
            password=self.db_pass, database=self.db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            yield con
        finally:
            con.close()
```

Source: `~/Projects/personal/investing/databasemanager.py` (my own).

**Parameterized queries — never string-format user data into SQL.** Every write passes
values as `%s` placeholders with a separate argument tuple; the driver escapes them. This
is the line between safe code and a SQL-injection hole:

```python
def get_symbol_data(self, symbol, start_date, end_date):
    query = """
        SELECT a.*, IFNULL(b.dividend_amount, 0) AS dividend_amount
        FROM symbol_data a
        LEFT JOIN symbol_dividends b
            ON a.symbol = b.symbol AND a.date = b.date
        WHERE a.symbol = %s AND a.date BETWEEN %s AND %s
        ORDER BY a.date;
    """
    with self.get_connection() as con:
        with con.cursor() as cursor:
            cursor.execute(query, (symbol, start_date, end_date))   # values passed separately
            return cursor.fetchall()
```

Source: `~/Projects/personal/investing/databasemanager.py`.

For bulk inserts the same idea scales with `cursor.executemany(query, list_of_tuples)` —
one prepared statement, many rows — which the manager uses to load thousands of price rows
at once. And writes only persist after `con.commit()`; forget it and your inserts silently
vanish when the connection closes.

## SQLAlchemy — the portability layer

SQLAlchemy sits above the raw driver: you talk to an `Engine` (built from a connection URL
like `postgresql+psycopg2://user:pass@host/db`) and it handles connection pooling and
SQL-dialect differences, so the same code moves between SQLite, MySQL, and Postgres with
only the URL changing. In STAT 624 we used it to connect to a Postgres database running in
a Docker container (`create_engine(...)` + `psycopg2`), then ran queries through the engine
or read them straight into pandas with `pd.read_sql(query, engine)`.

Source: STAT 624 Week 7 (local: `course-files/07-sql-and-databases/Week7_sqlalchemy_pythonintro.ipynb`)
— instructor-copyrighted (© Texas A&M) and requires a live Docker Postgres container to run,
so it's cited here as the concept source only; nothing is reproduced.

The practical rule: reach for SQLAlchemy when you want backend portability or an ORM's
object mapping. For a quick analysis against a fixed SQLite file, plain `sqlite3` +
`read_sql_query` is less ceremony and does the job.

## Gotchas

- **Parameterize, always.** `f"... WHERE symbol = '{symbol}'"` is a SQL-injection bug and
  also breaks on any value containing a quote. Use `%s` (pymysql/psycopg2) or `?` (sqlite3)
  placeholders and pass values as a tuple — the two drivers use *different* placeholder
  styles, which is an easy thing to trip on when moving code between them.
- **Commit your writes.** `INSERT`/`UPDATE`/`DELETE` don't persist until `con.commit()`.
  The context manager closes the connection on exit; uncommitted changes are lost.
- **Close connections.** Leaked connections pile up until the server refuses new ones. The
  `@contextmanager` + `try/finally` pattern above makes closing automatic — worth the few
  extra lines over scattering `con.close()` calls you'll forget.
- **`read_sql_query` pulls everything into memory.** It's built for result sets that fit in
  RAM. For a huge table, filter and aggregate in SQL first, or read in chunks — don't
  `SELECT *` a million rows and sort it in pandas.
