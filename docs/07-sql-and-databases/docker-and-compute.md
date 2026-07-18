# Docker & Compute

## Overview

Two practical problems sit next to databases in any real data-science workflow, and STAT 624
spent real time on both: **how do I run this database (or environment) reproducibly?** and
**what do I do when the data no longer fits on one machine?** The first is Docker; the second
is parallel/distributed computing with Dask and HPC clusters. This page is the concept map
for both — light, since I've used Docker hands-on but the Dask/HPC material is coursework I'm
summarizing rather than production code of my own.

All content here is paraphrased from STAT 624 lecture notebooks and decks, which are
**instructor/TA-copyrighted and marked do-not-distribute** — I describe the ideas and cite
the local originals; **nothing is quoted and no executed output is reproduced.**

## Docker — reproducible databases and environments

A **container** packages an application with everything it needs to run — libraries, config,
the exact runtime — into an image that runs identically on any machine with Docker. Unlike a
virtual machine, a container shares the host's kernel instead of booting a whole guest OS, so
it's lightweight and starts in seconds. That's what makes "works on my machine" stop being a
problem: the image *is* the machine.

For databases this is a genuine quality-of-life win. Instead of installing Postgres system-wide
and fighting version conflicts, you run it in a container: one command brings up a clean,
disposable Postgres with a known version, and `docker-compose` can bring up a whole stack —
a database plus a **pgAdmin** web UI to browse it — with a single config file and one
`docker compose up`. When you're done, you tear it down and your host is untouched. In STAT
624 this is exactly how we stood up the Postgres database that the
[SQLAlchemy notebook](python-and-databases.md#sqlalchemy-the-portability-layer) connected to.

Concept source: STAT 624 Week 2 (local: `course-files/07-sql-and-databases/Week 2_Docker.pdf`)
and `STAT624_Docker_082523.pdf` — both instructor-copyrighted, summarized only. Official
docs: [Docker](https://docs.docker.com/) · [Docker Compose](https://docs.docker.com/compose/).

The mental model I hold onto: a **Dockerfile** is the recipe (how to build the image), an
**image** is the built artifact, and a **container** is a running instance of that image.
Volumes persist data outside the container's lifecycle, which matters for a database — kill
the container and the data survives on a mounted volume.

## Parallel computing with Dask

When a dataset is bigger than memory or a computation is too slow on one core, the answer is
to split the work. **[Dask](https://docs.dask.org/)** scales the familiar PyData tools:
`dask.dataframe` mirrors the pandas API but operates on a dataset partitioned into many
chunks, `dask.array` does the same for NumPy, and both build a **task graph** of the
computation that only actually runs when you call `.compute()` (lazy evaluation). The payoff
is that you write near-pandas code but process data that would never fit in RAM, by streaming
it through in chunks and running independent pieces in parallel.

The core ideas STAT 624 covered: **chunking** (partition the data so each piece fits in
memory), **lazy task graphs** (Dask records the operations and optimizes the whole graph
before executing), and **memory profiling** to find where a pipeline blows up. The honest
caveat from the course material: Dask shines on genuinely large or embarrassingly-parallel
work; for data that fits comfortably in memory, plain pandas is faster and simpler because
you skip all the scheduling overhead.

Concept source: STAT 624 Week 13 (local: `course-files/07-sql-and-databases/Week13_daskparallelization.ipynb`)
— instructor-copyrighted, do-not-distribute; summarized, not reproduced.

## Scaling out — HPC clusters

Dask's real power shows when it stops running on your laptop's cores and starts running on a
**cluster**. A Dask **scheduler** coordinates many **workers** — which can live on separate
machines — and `dask.distributed` farms the task graph out across all of them. STAT 624
demonstrated this on Texas A&M's **HPRC** high-performance computing clusters (FASTER/Grace),
including GPU-backed clusters where `LocalCUDACluster` and CuPy push array work onto GPUs.

The concept that generalizes: the *same* Dask code that ran on my laptop scales to a cluster
by pointing it at a distributed scheduler instead of the local one — the programming model
doesn't change, only where the workers live. That's the whole appeal of this layer: develop
locally on a sample, then scale out to the cluster for the full run without rewriting.

Concept source: STAT 624 Week 14 (local: `course-files/07-sql-and-databases/Week14_Dask_Scheduler_Cluster (1).ipynb`,
TA-copyrighted) — this notebook requires TAMU HPRC VPN and GPU-cluster access to run, so it's
cited as the concept source only; nothing is reproduced.

## Gotchas

- **Containers are ephemeral — mount a volume for a database.** Data written inside a
  container's own filesystem dies with the container. A database needs its data directory on a
  mounted volume, or every teardown wipes it.
- **Don't reach for Dask too early.** The scheduling overhead means small-to-medium data is
  *slower* on Dask than on pandas. Distributed computing is the answer to a real
  memory-or-time wall, not a default. Profile first; scale out only when one machine genuinely
  can't cope.
- **`.compute()` is where the work actually happens.** Dask's laziness means bugs and blow-ups
  surface at `.compute()`, not at the line that looks like it's doing the work. Read the task
  graph, not just the traceback.
