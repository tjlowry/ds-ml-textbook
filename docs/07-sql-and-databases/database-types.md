# Database Types

## Overview

Relational databases are the default, and for good reason — but they're not the only shape.
When your data doesn't fit neatly into tables, or when the access pattern is "look up one
key as fast as possible" or "traverse a network of relationships," a **non-relational**
("NoSQL") store can be the better tool. This page is a map of the main categories and when
I'd reach for each. It's a "know these exist and why" page, not a deep dive.

Concept source: STAT 624 Week 11 (local: `course-files/07-sql-and-databases/Week 11_NoSQL
(1).pdf`) — instructor-copyrighted (© 2023 Scott A. Bruce), paraphrased only; no slide
content reproduced. External links below are the vendors' own official documentation.

## Why non-relational at all?

The relational model gives you strong guarantees — a fixed schema, referential integrity,
and **ACID** transactions (atomic, consistent, isolated, durable). Those guarantees cost
something: every write is validated, and scaling *out* across many machines is hard because
a join or a transaction may need data that lives on different servers.

NoSQL stores relax some of those guarantees to buy flexibility or scale. The **CAP theorem**
frames the core trade-off: when a distributed system hits a network **P**artition, it can
preserve either **C**onsistency (every read sees the latest write) or **A**vailability
(every request still gets an answer) — not both. Relational systems traditionally lean
consistent; many NoSQL systems lean available and offer "eventual" consistency instead.
That's the lens I use to decide: **do I need strict correctness on every read, or
throughput and flexibility?**

## The main categories

**Document stores** (e.g. **[MongoDB](https://www.mongodb.com/docs/)**) hold schema-flexible
JSON-like documents. Each record can have its own shape, so they fit data that's naturally
nested or evolving — user profiles, event payloads, product catalogs — without migrations
every time a field changes. The cost is that cross-document consistency and joins are weaker
than in SQL. Reach for one when the schema is fluid or the data is a self-contained document.

**Key-value stores** (e.g. **[Redis](https://redis.io/docs/latest/)**) are the simplest
model: a dictionary at scale, `key → value`, optimized for microsecond lookups. Redis lives
in memory, which makes it the go-to for caching, session storage, rate limiters, and
leaderboards — anything where you know the exact key and want the value *now*. You give up
querying by anything other than the key.

**Wide-column stores** (e.g. **[Cassandra](https://cassandra.apache.org/doc/)**) spread huge
tables across many nodes with tunable consistency, built for write-heavy workloads at scale
(telemetry, time-series ingestion) where availability matters more than immediate global
consistency.

**Graph databases** (e.g. **[Neo4j](https://neo4j.com/docs/)**) make *relationships*
first-class: nodes and edges with properties, queried by traversing connections. When the
important question is "how are these things connected" — social networks, recommendation
graphs, fraud rings, citation networks — a graph database answers in one traversal what
would be a pile of recursive joins in SQL. This connects directly to the graph algorithms in
the ML chapter: [PageRank](../08-machine-learning/other/pagerank.md) is exactly the kind of
node-importance question a graph database is built to store and feed.

## When to use what

| Need | Reach for |
|---|---|
| Structured data, joins, transactions, integrity | **Relational** (Postgres, MySQL, SQLite) |
| Flexible / nested / evolving schema | **Document** (MongoDB) |
| Fast lookup by known key, caching | **Key-value** (Redis) |
| Massive write throughput, horizontal scale | **Wide-column** (Cassandra) |
| Relationship traversal, network questions | **Graph** (Neo4j) |

The honest default: **start relational.** SQLite or Postgres handles the overwhelming
majority of what I build, and the relational guarantees are worth keeping until a specific
pressure — schema fluidity, lookup latency, write volume, or graph traversal — pushes me off
it. NoSQL is a targeted answer to a specific problem, not a general upgrade.

## Gotchas

- **"NoSQL" ≠ "no schema."** Document stores let you *skip declaring* a schema up front, but
  the schema still exists implicitly in your code — and now nothing enforces it. Fields drift,
  types get inconsistent, and you pay for it at read time. Flexibility is a loan, not a gift.
- **Eventual consistency surprises you.** If you write then immediately read on an
  available-leaning store, you may read stale data. Fine for a like-count, not fine for a bank
  balance. Match the consistency model to how wrong a stale read can be.
- **Don't pick NoSQL for résumé reasons.** The most common mistake is reaching for a trendy
  store when a boring relational table would have been simpler, safer, and faster to build.
  Let the data's shape and access pattern decide.
