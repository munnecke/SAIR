# Web Watch columns — Loomic corpus

Tom Munnecke's Web Watch columns (San Diego Daily Transcript, 1994-95),
converted to Loomic 0.2. Source: `webwatchcolumns.rtf` / `webwatch-columns.txt`
in the SAIR root.

Conventions — these differ from the summit corpus (`presentations-loomic/`)
because these are primary sources, not transcripts of talks:

- **The column text IS the record.** No transcript/summary split. Body text is
  verbatim from the 1995 file, including its typos ("resitance", "lineardemand").
  Annotation adds only span brackets, attribute blocks, and standalone divs.
- **Assertion time is publication time.** Frontmatter sets `asserted:` to the
  column's publication date (1994-1995). Claims from these columns enter the
  loom as 1990s assertions, so time-scoped queries (`as_of=1995-01-01`) see
  the web as Tom saw it then.
- **Predictions are typed as they were then.** A 1994 forecast is a
  `.hypothesis` or `.future_binding` with `status=pending` — that was its
  status when asserted. History's verdict arrives separately:
- **2026 retrospectives.** Each column may carry at most one curator div
  (`.resolution` or `.interpretation`) with `asserted=2026-07-04` and
  `asserted_by=claude-curator`, adding `resolves=` / `outdates=` edges only
  where history is unambiguous. Uncertain verdicts stay unmarked. Retrospective
  prose follows `writing-style.md` (SAIR root): flat, sourced, no epigrams.
- **IDs** are prefixed `ww-` plus a short column slug (e.g. `ww-commons-`).
- **Cross-corpus edges** to the summit loom (`sair-ucr-2026`) are allowed
  sparingly in retrospectives — e.g. a 1994 idea that `@motivated` a 2026
  discussion. The two looms currently share a flat namespace; cross-loom
  syntax is an open spec question (Loomic-Spec-v0.2 Appendix E).
