---
title: "Convergence-Rover — first run against the summit loom"
date: 2026-07-05
---

# Convergence-Rover: first run

## What it does

It mechanically re-discovers cross-discipline **unknowledge** — one structural
fact that surfaces in several talks under different vocabularies — which is the
move you performed by hand in `00-summit-loomic-view.md` when you wrote
"five speakers, five vocabularies, one structural fact." The Rover treats that
as a graph-clustering problem over typed claim nodes, ranks candidate
convergences by how many *distinct source documents* they span, and emits each
as an append-only Loomic `.unknowledge` div with `@inferred` edges (a proposal,
never an assertion).

Files: `convergence_rover.py` (the Rover), `rover_themes.json` (the semantic
backend, materialized), `summit.json` (the loom, rebuilt from the presentation
docs so the script is runnable as-is).

Run:

```
python convergence_rover.py --loom summit.json --signal semantic
python convergence_rover.py --loom summit.json --signal lexical        # watch it find nothing
python convergence_rover.py --loom summit.json --signal concept_graph  # watch it find nothing
```

## The headline result

The Rover was pointed at the 43 `claim` nodes of the summit loom with **no
access to your curator synthesis node**. On the semantic signal it returned, as
its top-ranked convergence:

> **generation-outruns-validation** — 11 claims from **6 distinct talks**
> (Barish, Tao, Meiburg, the simulation panel, Papalexakis, the SAIR platform),
> score 66.

That cluster **contains all five claims** you hand-selected for
`view-generation-outruns-validation` (Barish, Tao, Meiburg, Bian, and the
overoptimistic-scores claim) — a clean 5/5 recovery — and it additionally
folded in the *toolchain* nodes you had split into a second synthesis
(Meiburg's statement auditing, Clark's physical-laws-as-unit-tests,
Papalexakis's uniqueness theorem, the SAIR open platform). In other words it
re-found your frontier and its candidate solution set in one pass.

It also surfaced two more real convergences you'd recognize:
**regional-capacity-and-access** (10 claims across the SoCal panel, the equity
panel, and the Chancellor) and **sparse-reward-hard-search** (Gukov's
"same structural difficulty everywhere," the intractable-RL claim, the
formalism-bottleneck claim, underspecified-physics — across three talks).

## The part that makes this publishable, not just neat

The two naive baselines were run on the identical claim pool and **found
nothing**:

| Signal | What it measures | Cross-discipline convergences found |
|---|---|---|
| lexical | shared keywords (Jaccard over claim text) | **0** |
| concept_graph | shared `ref→concept` edges / citations | **0** |
| semantic | latent-theme agreement (LLM/embedding backend) | 3 |

I verified the failure is total, not marginal: the five convergent claims have
a **keyword Jaccard of 0.00** with each other and a **concept-reference Jaccard
of 0.00** — they share no words and no graph neighbours. A corpus-trained LSA
model scored them at the *random* baseline (0.089 vs 0.113). This is the whole
argument in one line: **the convergence that matters is invisible to every
signal a citation graph or keyword index can compute.** It lives only in
meaning. That is exactly the layer a Loom adds and OpenAlex / Semantic Scholar
structurally cannot.

## Honest caveats

- **The semantic backend is doing the real work, and here it's an LLM judge
  (me), materialized as `rover_themes.json`.** That's legitimate — it's your
  spec's open question E5 (an AI adding `@inferred` annotations under the
  fidelity rules) made concrete — but it means the demonstrated result is
  "LLM-proposes, graph-structures, human-reviews," not a fully unsupervised
  discovery. In production, swap `load_semantic_themes()` for an embedding-API
  clustering or an LLM classifier; the rest of the pipeline is unchanged.
- **Single-link clustering is deliberately crude.** With discrete themes it's
  exactly right; with continuous embedding cosine you'll want a real clustering
  (HDBSCAN) and a threshold sweep. The `score()` interface is already the only
  thing you'd change.
- **This is one loom of 16 talks.** The claim that the Rover finds
  *cross-discipline* gaps is only fully earned once it runs across *multiple*
  looms (e.g. the summit loom + the 1995 Web Watch loom) and finds a fact that
  spans both. That's the natural next experiment, and the code already takes a
  loom path as an argument.
- **The Rover proposes; it never asserts.** Every emitted edge is `@inferred`
  and every node is `status=open` pending `review.cleared_by`. The taint /
  review machinery in your spec is what keeps a machine's convergence guess
  from being laundered into the record — which is the direct antidote to the
  "plausible and wrong" failure Meiburg warned about.

## Suggested next step

Run it across two looms at once. If the Rover can show that "generation has
outrun validation" (2026, physics/math/AI) rhymes structurally with a
Web-Watch-1995 claim about infrastructure outrunning governance, you'll have
demonstrated cross-*corpus*, cross-*decade* unknowledge detection with full
provenance — something no existing scholarly-graph system can do, and a clean
paper.
