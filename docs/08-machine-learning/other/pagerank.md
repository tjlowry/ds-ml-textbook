# PageRank & Graph Methods

## Overview

**PageRank** ranks the nodes of a graph by importance, where a node is important if
important nodes point to it. It models a "random surfer" following edges at random (with a
damping factor for occasionally teleporting to a random node); the PageRank of a node is the
long-run probability the surfer is there — the stationary distribution of that random walk,
computable as the dominant eigenvector of the (damped) transition matrix. It's the algorithm
that originally ranked web pages and generalizes to any network centrality question
(citations, social graphs, recommendation).

**I don't have my own implementation of this one.** PageRank and graph search are covered in
my ECEN 758 notes but I never used them in a project or homework — no code of mine exists to
show. This page is a concept summary from the lecture.

## Gotchas (from the lecture, worth remembering)

- **The damping factor keeps it well-defined.** Without teleportation (typically ~0.85
  chance of following a link), rank gets trapped in dead-ends and cycles ("rank sinks").
- **It's an eigenvector / power-iteration problem.** You rarely solve it directly; iterate
  the transition until the rank vector converges.
- **Link-based, not content-based.** PageRank scores *structure* — who points to whom — so
  it's complementary to, not a replacement for, content relevance.
- **Related to the random-walk view of many methods.** The same stationary-distribution idea
  shows up in Markov chains and some graph-based clustering.

## References

- ECEN 758 Lecture 14 — Graphs, PageRank and Search (local:
  `course-files/08-machine-learning/758 Lec 14 Graphs, Pagerank and Search.pdf`).
  Instructor-copyrighted; concept summary only, no code of my own.
