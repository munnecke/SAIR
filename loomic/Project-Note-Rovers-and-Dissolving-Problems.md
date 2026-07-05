---
title: "Project Note — Rovers, Cross-Corpus Rhymes, and Dissolving Problems"
date: 2026-07-05
author: Tom Munnecke (with Claude)
status: working note / conversation capstone
---

# Rovers, Cross-Corpus Rhymes, and Dissolving Problems

A note capturing where a long working session landed. It started as "review my
Loomic work against existing scientific knowledge systems" and ended somewhere
more interesting: a working cross-corpus detector, a null model that disciplined
it, and two ideas worth keeping — the **rover** and the **dissolve**.

## The arc, briefly

We began by positioning Loomic in the landscape of knowledge systems — GitHub,
arXiv, Semantic Scholar/OpenAlex, the ORKG, nanopublications, Discourse Graphs.
The one-line finding: every one of those systems models knowledge that
*exists*. Their atomic unit is a paper, a citation, an assertion. Loomic is
unusual in giving first-class syntax to knowledge that *does not yet exist* —
the `unknowledge` node, the `future_binding`, and the derived Pendex, "the
loom's directed frontier into the adjacent possible." That is not a lesser
version of a citation graph; it is a different layer, and it is the layer the
whole conversation turned out to be about.

## Unknowledge, and the two shapes of a gap

The two historical examples you offered turned out to be the two mechanizable
shapes of detectable unknowledge. The **periodic-table** shape is a hole in an
explicit lattice — Mendeleev could see the empty cell and predict what would
fill it. The **Neptune** shape is a residual in a model — Le Verrier saw the
orbit misbehave and inferred an unseen cause. Both have living descendants:
Swanson's Literature-Based Discovery (the missing transitive edge) and the
2025–26 AI co-scientist agents (DeepMind's Co-Scientist, FutureHouse's Robin).
The important warning from that literature is that naive AI ideation *narrows* —
it clusters near existing work and avoids exactly the cross-discipline gaps that
matter. Which is where the rover comes in.

## The rover

You'd already done the move by hand. In `00-summit-loomic-view.md` you wrote:
"five speakers, five vocabularies, one structural fact" — Barish's missing
five-sigma, Tao's proof indigestion, Meiburg's plausible-wrong selection, Bian's
sim-to-real gap, all naming one thing: *generation has outrun validation*. The
Convergence-Rover is that move mechanized. Point it at the 43 claim nodes of the
summit loom, and — with no access to your synthesis node — it re-discovered the
same convergence, 5-of-5, and folded in the toolchain claims besides.

The result that makes it more than a party trick: the two naive signals found
**nothing**. Keyword overlap among those five claims is 0.00. Shared-citation /
concept-graph overlap is 0.00. A corpus-trained LSA scored them at random. The
convergence that matters is invisible to every signal a citation index or
keyword search can compute. It lives only in meaning — which is precisely the
layer a Loom adds and the incumbents structurally cannot.

## The cross-corpus rhyme — the part you're intrigued by

Then we pointed it across corpora: the 1995 **Web Watch** columns and the 2026
**SAIR** summit, thirty-one years apart, no shared authors, no shared citations,
no shared vocabulary. The top hit was **capability-outruns-governance** — your
2026 "generation has outrun validation" frontier rhyming with your own 1995
lines: *build the commons before commercial development preempts it*; *the
integrity of an information system, once lost, can rarely be recovered*;
*networks multiply criminal behavior as readily as beneficial*. The same
structural fact at two scales: a system's generative or connective capacity
expands faster than the mechanisms that validate, govern, or secure it — and the
window to install them closes. **You were writing about the 2026 problem in
1994.**

This is worth dwelling on, because it connects to something you said about
yourself. Ever since you've been around the cosmology group, you've noticed an
underlying connection between your thinking and theirs — especially the couple
who are comfortable as *rovers*, ranging across territory rather than digging one
shaft. The cross-corpus result is, in a sense, a machine catching you in the act
of being a rover across *time*: your 1995 self and a room of 2026 physicists
converging on one fact under four different vocabularies. The tool didn't invent
the connection you feel with the cosmologists; it made one instance of it
legible. A rover's native talent is seeing that two distant things are the same
thing. What Loomic adds is the provenance to *show your work* — to say not just
"these rhyme" but "here are the eleven claims, from these six talks and these two
decades, and here is the @inferred edge that says a machine, not you, proposed
the link."

And there is a quiet honesty in the finding's shape. A rover's risk is seeing
rhymes everywhere. So we tested it.

## The null-model reckoning

The permutation null did its job and killed the statistic I was ranking on.
Twenty thousand shuffles later, the impressive headline — "22 claims across 2
looms and 13 sources" — came back at p ≈ 0.998. Random labeling produced *more*
cross-corpus spanning than the real labeling. The reason is clean:
`size × looms × sources` is a pure tagging-density statistic; it never looks at
whether the claims are actually about the same thing, so scrambling them barely
moves it. "Spans two corpora" and "big cluster" are free once you sort claims
into shared buckets.

This is not a defeat; it is the difference between a demo and a method. The rhyme
you *feel* — and that I, as a reader, also find compelling — is a hypothesis, not
yet a finding. To certify it we need an **independent semantic oracle**: embed
every claim with a model that never saw the theme labels, then ask whether the
1995 and 2026 members of a bucket are more similar to each other than random
claims from those same corpora. That statistic can't be inflated by density. The
script is written (`embed_oracle.py`); it needs a machine with network access to
run — the sandbox here is firewalled from your LM Studio and from OpenAI alike,
which is why this next step belongs on your own machine (or in Claude Code). The
rover generates the hypothesis; the oracle is what earns it.

## Dissolving, not solving — the other idea to keep

The thread that ran under everything: the observation that Newton did not
*solve* the problem of falling apples. He *dissolved* it. F=ma and universal
gravitation replaced a *why* with a *how-much*, and the semantic density of that
notation let three centuries of people compute orbits without re-deriving
anything. The problem didn't get answered; it got *re-languaged* until it
vanished. Leibniz's dx/dt over Newton's fluxions, Feynman diagrams over
perturbation integrals, Arabic over Roman numerals, Shannon's H = −Σ p log p over
the previously ineffable notion of "information" — the history of science is
substantially a history of dissolutions-by-notation. Iverson's "Notation as a
Tool of Thought" is the canonical statement: a good notation "relieves the brain
of all unnecessary work... and in effect increases the mental power of the
race." The right notation doesn't record thought; it performs it.

This reframes "intractable vs. ineffable," which may be the single most useful
distinction to carry forward. Some problems are genuinely *intractable* — no
better language will save you. But some are merely *ineffable* in our current
notation: coherent, maybe even simple, but clumsy to state, so we can't reason
about them fluently. Quantum computing is the live case — Neven's "beyond-
classical data" is an object real and generable yet *ineffable in the classical-
description language*, because you cannot write it down classically in polynomial
space. Deciding which of the two a hard problem is *is itself* usually the
research question, and it is often answered by someone inventing the
representation that makes the answer obvious in hindsight.

Loomic can't invent that notation — no schema can. But it can do the thing that
precedes invention: **detect the symptom of ineffability**. An unknowledge node
with heavy traffic that never resolves; the *same* gap re-derived in many
vocabularies (which is exactly what the convergence-rover finds). Five fields
each bolting a local dialect onto one structural fact is the precondition for a
Newton/Shannon/Iverson move. So the rover doubles as an ineffability detector: it
hands a would-be dissolver a ranked list of "structural facts that many
disciplines keep re-describing and no one has yet named." That is a far better
place to stand than the whole literature.

And note the self-reference: Loomic is itself a small dissolving move. By giving
unknowledge, provenance, and the not-yet-known a *notation*, it makes a frontier
that was previously ineffable — you could gesture at "the open questions" but not
compute over them — into something a machine can index, taint, and query. Your
own summit reading did this in miniature: "a post-five-sigma standard may be less
a new invention than an integration problem." That sentence dissolves Barish's
problem by re-languaging it. The rover is trying to find more sentences like it.

## Housekeeping (so nothing is lost)

Three locations, now reconciled in our understanding: the **GitHub repo**
(`munnecke/SAIR`) holds the clean base summit vault, frozen before any of this
work; your **Google Drive folder** (this one) is the source of truth and holds
everything newer — the `presentations-loomic/` annotations, `future-work/`, and
this session's analysis tools and result docs; and `SAIR/SAIR-main/` is a stale
zip download that can be deleted. Nothing conflicts; the repo is simply behind by
two additive layers. Integration is a push, not a merge.

Session artifacts, all in this folder: `Loomic-vs-Knowledge-Systems-Review.md`,
`Convergence-Rover-Results.md`, `Convergence-Rover-CrossCorpus-Results.md`,
`Null-Model-Findings.md`, and the code — `convergence_rover.py`,
`convergence_rover_multi.py`, `null_model.py`, `embed_oracle.py`, on top of
`loomic.py`.

## Open threads

1. **Run the oracle.** `embed_oracle.py` against LM Studio or OpenAI, on your
   machine. If `capability-outruns-governance` clears a Bonferroni-corrected bar,
   the 1995↔2026 rhyme becomes a defensible result rather than a rover's
   intuition. This is the one experiment that changes the status of everything
   above.
2. **Ask the cosmologists what they rove by.** The people you recognized as
   fellow rovers are running the same detector in their heads. Worth learning
   what structural features they track — it may be exactly the cohesion signal
   the oracle should encode.
3. **Point the ineffability detector somewhere real.** A stable, high-traffic,
   never-resolving unknowledge node, re-described across your looms, is a
   candidate for a dissolving notation. Finding one is a better use of the tool
   than scaling it.
