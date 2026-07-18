---
name: fill-chapter
description: Fill or upgrade one chapter of the DS/ML textbook from Tyler's real coursework and project code. Use when asked to write, fill, or improve a textbook chapter, e.g. "/fill-chapter machine-learning".
---

# Fill a Textbook Chapter

Turn one chapter from stub/outline into real reference content grounded in Tyler's own
work. One chapter per invocation. Never invent facts about what a project did — every
claim must trace to a file you actually read.

## Step 1 — Inventory (before writing anything)

1. List `course-files/<chapter>/` (raw PDFs, notebooks, scripts — local-only).
2. Search `~/Projects/` for related real work (school, clients, personal, research).
3. Read the chapter's existing `docs/` pages, if any.
4. Present Tyler a short inventory: what material exists, which topics it supports,
   which 1–3 notebooks are the best promotion candidates. Get his OK on scope.

## Step 2 — Draft

Every topic page follows this template (skip sections with nothing real to put in them):

    # <Topic>

    <2–6 sentence summary: what it is, when I'd reach for it, where I used it.>

    ## How I did it

    <real snippet from Tyler's code>
    Source: `~/Projects/<...>` or `course-files/<...>`

    ## Notebook

    See the rendered notebook: [<title>](../notebooks/<name>.ipynb)
    Re-run locally: `jupyter lab docs/<chapter>/notebooks/<name>.ipynb`

    ## Gotchas

    - <mistakes made, confusing parts, what to remember>

Notebook promotion checklist (per promoted notebook):
- Copy from source into `docs/<chapter>/notebooks/`; original stays put.
- Add a title cell + short context markdown (what project, what it shows).
- Execute top-to-bottom locally so outputs/plots are saved. If it can't run
  (dead deps, missing data), keep existing outputs and add an admonition noting that.
- Strip embedded data; keep the file under ~2MB. `execute: false` in CI means
  whatever outputs you commit are what renders.

Instructor-content rules (the site is PUBLIC; personal use ≠ license to republish):
- Never reproduce instructor slide text, figures, or worked examples verbatim. Math,
  theorems, and algorithms are ideas — re-derive and re-express them in Tyler's/our
  own words with our own examples. Cite the local original:
  `From ECEN 758 Lec N (local: course-files/<...>.pdf)`.
- **Remake key diagrams and graphs.** Where a lecture's important concept is visual
  (a geometry picture, a convergence plot, an algorithm flow), regenerate it ourselves
  — matplotlib PNG committed under `docs/<chapter>/img/` (follow the dataviz skill),
  or a mermaid block for flow/structure diagrams. Never screenshot slides.
- **Modern-ML concept mapping.** Where it genuinely fits, connect the classical
  concept to modern ML Tyler cares about (embeddings, LLMs/attention, residuals,
  low-rank/LoRA, PCA) with a short example or figure — visuals teach Tyler best.
- **Private Drive slide links.** Lecture PDFs cited on a page also get a
  `Full slides: [Drive](<url>)` line IF a private-Drive copy exists (Tyler-only
  sharing). Upload cited PDFs to Drive folder `textbook-course-slides/<chapter>/`
  during drafting if access allows; skip the line rather than fake a URL.
- Instructor-provided public links (their own Colab/GitHub) may be linked directly —
  but only URLs actually extracted from the source PDFs.

Then: add the chapter + pages to `nav:` in `mkdocs.yml`, add notebooks under a
"Notebooks" sub-item, update `docs/roadmap.md` (remove the filled chapter), and update
the chapter list in `docs/index.md`.

## Step 3 — Review gate

Run `mkdocs build --strict` (must pass) and `mkdocs serve` for Tyler to review.
Wait for his corrections — especially anything that misrepresents what his work did.

## Step 4 — Deploy

Commit and push to `master`; GitHub Actions publishes the site. Confirm the live page.
