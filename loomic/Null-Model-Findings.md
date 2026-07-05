---
title: "Null-model test of the cross-corpus Rover — and what it kills"
date: 2026-07-05
---

# Null-model findings: the density test refutes the naive statistic

## Result, stated bluntly

I ran a 20,000-iteration permutation null against the four cross-corpus
convergences. **They do not survive it.** Every statistic came back at
p ≈ 0.998–0.999 — the opposite of significant:

```
OBSERVED:   N_xcorpus=4    N_balanced=3    TOP_score=572
p(null >= observed):  0.9986        0.9991          0.9980
null TOP_score: mean=740   max=968   vs observed=572
```

Read that carefully: when I randomly shuffle the macro labels across the 66
tagged claims, random labeling produces **more** cross-corpus spanning and
**bigger** clusters than the real, semantically-assigned labeling (null mean
score 740 vs observed 572). The impressive-looking headline — "22 claims across
2 looms and 13 sources" — is **not evidence of a real rhyme.** It is what you
get almost automatically once you sort claims from two corpora into a handful
of shared buckets. Both looms are richly represented in the pool, so nearly any
labeling makes every big bucket "span both looms."

This is exactly what a null model is for, and it just did its job: **it killed
the statistic I was ranking on.** The cross-corpus numbers in
`Convergence-Rover-CrossCorpus-Results.md` should now be read as "these claims
were sorted into shared buckets," not as "the machine discovered a cross-decade
convergence." I'd rather tell you that now than have a referee tell you later.

## Why it fails, precisely

`score = size × n_looms × n_sources` is a **pure tagging-density statistic**. It
depends only on how many claims and sources landed in a bucket — never on
whether the claims are actually about the same thing. Two things follow:

1. Any independent tagging that fills a few buckets from both corpora will score
   just as high. The score cannot distinguish a real rhyme from an arbitrary
   co-tagging.
2. The permutation null makes this visible because it holds the bucket sizes
   fixed and only scrambles *which* claim is in *which* bucket. Since the score
   ignores claim content, scrambling barely changes it — and actually raises it,
   because the real labeling "wastes" some claims on looms-specific buckets
   (sparse-reward, representation-theory, skill-atrophy, interdisciplinary
   mission are summit-only), which the random version spreads across both looms.

The one mildly reassuring signal: the real labeling is *less* loom-spanning than
random precisely because it correctly keeps several themes in a single corpus.
That is a faint sign the tagging is not random noise — but it is nowhere near a
result.

## What a valid test actually requires

The null exposes the true missing piece: **an independent semantic-similarity
oracle.** A defensible cross-corpus claim needs a statistic that goes up only
when the paired claims are genuinely similar in content, measured by something
other than the same judge that assigned the buckets. The corrected design:

1. **Oracle.** Embed every claim with a model that never saw your theme labels
   (a sentence-embedding API, or an LLM asked for pairwise similarity in a
   separate pass). This is the piece I could not run here — the sandbox blocks
   the model download — and it is why this test can currently only *refute*,
   not *confirm*.
2. **Statistic.** For each macro bucket, compute mean *within-bucket
   cross-corpus* embedding cosine — the average similarity between its 1995
   members and its 2026 members. This is zero-inflated by design for a real
   rhyme only if the content truly matches.
3. **Null.** Permute labels as here, holding bucket sizes fixed, and compare the
   observed within-bucket cross-corpus cosine to the null. Now a high score can
   *only* come from real semantic alignment, because random buckets pair
   dissimilar claims and their mean cosine collapses.
4. **Report** per-bucket p-values, so `capability-outruns-governance` stands or
   falls on its own rather than riding the aggregate.

I also confirmed offline that the two similarity signals available in-sandbox
cannot serve as that oracle: keyword-Jaccard and concept-graph overlap are both
~0 for these clusters (that was the whole point of the single-loom demo), and a
corpus-trained LSA scored the convergent claims at the random baseline. So the
oracle genuinely must be an external embedding/LLM — there is no offline
shortcut.

## Bottom line for the project

- The Convergence-Rover's *machinery* is sound and worth keeping: extract typed
  claims, attach provenance, propose `@inferred` clusters for review, gate
  everything behind human sign-off. That pipeline is real.
- The *evidence* it produced so far is not. "Spans two looms" and "big cluster"
  are free; the null proves it. Do not put the 22-claim number in a paper as a
  finding.
- The single thing that turns this from a suggestive demo into a defensible
  method is the embedding oracle in step 1. Everything else — the null harness
  in `null_model.py`, the Rover, the provenance discipline — is already built and
  waiting for it.

`null_model.py` is parameterized (`--iters`, `--seed`) and will re-run against
the corrected within-bucket-cosine statistic with a one-function change once an
embedding backend is available.
