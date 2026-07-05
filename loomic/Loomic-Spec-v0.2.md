# Loomic Specification

**Version 0.2 — Draft**
**Status:** working proposal for review
**Supersedes:** Loomic-Grammar-Spec-v0.1 (delimiter change: `<<...>>` → Pandoc attributes; adds temporal model)
**Depends on:** Loom/Loomic Handoff v0.9

Loomic is a lightweight inline annotation vocabulary for Loom documents. Prose remains primary and human-readable; annotations expose a directed, temporally-indexed graph for machine reasoning. Loom represents both knowledge and unknowledge: provenance, confidence, verification, unresolved questions, and future capabilities are all first-class.

v0.2 makes two major changes from v0.1:

1. **Surface syntax is Pandoc/Quarto attribute syntax**, not a custom delimiter. Loomic becomes a *vocabulary and schema* layered on an existing, widely-implemented standard. This keeps Loom tool-agnostic (Obsidian is a prototyping host, not a dependency), LaTeX-safe, and renderable/hideable via the existing Pandoc filter ecosystem.
2. **Diachronic semantics.** Every claim is indexed to assertion time; the graph is append-only; later events annotate earlier text through backward-pointing edges rather than edits. "What was known, when" is a first-class query.

---

## 1. Design constraints

1. A Loom document with all annotations stripped must remain a coherent Markdown document.
2. Annotations live **in the document**, never in sidecar files. Hiding, folding, and decorating are rendering-layer concerns.
3. Every annotation has an unambiguous **anchor** — the prose span or block it binds to (or none, for standalone nodes).
4. IDs are stable and immutable; graph identity survives document edits.
5. **The record is immutable.** Original text is never rewritten to reflect later knowledge — that would be the same silent-substitution failure (the Gemini incident) that motivated Loom. The world changes; the graph grows; the text stands.
6. Unknown keys are preserved, not rejected (forward compatibility).
7. Annotation burden must stay low enough that authors actually annotate (the Semantic MediaWiki lesson). Tooling should assist; the schema should have few required fields.

---

## 2. Surface syntax

Loomic uses Pandoc's attribute syntax. Full grammar reference: Pandoc's `bracketed_spans`, `fenced_divs`, and `attributes` extensions (also supported by Quarto and, near-identically, djot).

### 2.1 Inline spans

```markdown
[anchored prose]{#id .type key=value key="quoted value"}
```

- `#id` — node identity (§4)
- `.type` — node type (§5); exactly one type class per annotation
- `key=value` — bare values match `[A-Za-z0-9_.:/@\-]+`; anything else is double-quoted with backslash escapes
- Dotted keys form namespaces: `confidence.textual`, `trigger.capability`
- Multi-valued keys use commas inside a quoted value: `parents="a,b@substituted"`

### 2.2 Block nodes (fenced divs)

For standalone nodes — unknowledge, frontiers, future bindings, resolutions — and for annotating whole blocks:

```markdown
::: {#post-five-sigma .unknowledge parents=barish-confidence-gap status=open}
What should replace the five-sigma standard for AI-assisted discovery?
:::
```

The div body is the node's content. Divs nest (Pandoc handles this); a nested div's node is `part_of` its parent unless stated otherwise.

### 2.3 Concept references

Canonical form for referencing an existing node inline:

```markdown
[Barry Barish]{ref=barry-barish}
```

Obsidian `[[wiki links]]` are accepted as prototyping sugar; a normalizer rewrites `[[Barry Barish]]` → `[Barry Barish]{ref=barry-barish}` using the loom's ID table. The canonical serialization never contains wiki links.

### 2.4 LaTeX and math

Pandoc parses `$...$` and `$$...$$` before attributes, so braces inside math never collide with annotation syntax. To annotate an equation, wrap it in a span or div:

```markdown
[$P(|x| > 5\sigma) \approx 5.7 \times 10^{-7}$]{#gaussian-tail .claim
  tense=timeless verification.lean=GaussianTailProbability}
```

### 2.5 Exclusions

Annotations are not parsed inside code fences, inline code, or YAML frontmatter. Frontmatter may carry document-level defaults (§4.3).

---

## 3. Anchoring

| Form | Syntax | Anchor |
|---|---|---|
| Span-bound | `[prose]{...}` | the bracketed prose |
| Block-bound | `::: {...}` around a block | the block content |
| Standalone | fenced div whose type is a graph-object type (unknowledge, frontier, future_binding, ...) | none — the node is about the loom, not located in prose |
| Reference | `{ref=id}` | mention of an existing node; creates no node |

There is no "bare annotation binds to previous paragraph" rule (v0.1 §3.3 is withdrawn): wrapping the paragraph in a div is explicit and survives editing. Ambiguity is impossible by construction.

**Anchor robustness:** spans break if prose is edited without the annotation. The extractor SHOULD record a content fingerprint (normalized-text hash) per anchor so drift is detectable, borrowing the selector concept from the W3C Web Annotation model.

---

## 4. Identity

### 4.1 IDs

- `#id`: lowercase slug, `[a-z0-9][a-z0-9\-]*`, unique within a **loom** (a declared corpus of documents, not one file).
- IDs are immutable. Meaning-changes get a new node with `supersedes=old-id`.
- Annotations without `#id` create **anonymous nodes** (content-hash IDs). Anonymous nodes cannot be referenced; anything cited needs an explicit ID.

### 4.2 Looms and federation

Cross-file references within a loom are bare IDs (flat namespace). Cross-loom references are deferred; the reserved form is `loomname:id`.

### 4.3 Document-level defaults

YAML frontmatter may set defaults inherited by every node in the file:

```yaml
loomic:
  loom: sair-notes
  asserted: 2026-06-30
  source: sai-summit-2026
```

Node-level keys override file-level defaults.

---

## 5. Node types

One `.class` per annotation, drawn from the (evolving) Loom type vocabulary:

`person, concept, claim, observation, historical_claim, context, evidence_gap, problem, hypothesis, experimental_result, interpretation, synthesis, frontier, unknowledge, future_binding, resolution`

`pendex_node` (v0.9) is withdrawn as a type: Pendex membership is derived from status, not declared (§8.3). `resolution` is added: a node whose purpose is to resolve or outdate earlier nodes (§7.4).

---

## 6. Edges

Edge keys take node IDs as values (schema-driven; no sigil):

| Key | Meaning |
|---|---|
| `parents` | derived from / caused by / asked because of |
| `depends` | cannot be evaluated until these resolve |
| `resolves` | answers/settles the referenced unknowledge |
| `outdates` | the referenced claim was true when asserted; the world has since changed (§7.4) |
| `refines` | narrows or sharpens |
| `supports` / `contradicts` | evidentiary relation to a claim |
| `part_of` | membership (frontier, synthesis, collaboration) |
| `supersedes` | identity replacement: the *statement* was revised or corrected |
| `source` | provenance: the document/talk/dataset node this came from |
| `ref` | mention only; creates no semantic edge beyond citation |

**`supersedes` vs `outdates`** is the load-bearing distinction of the temporal model: `supersedes` says the statement was wrong or reworded; `outdates` says the statement stands as a correct record of its moment, but reality moved. Barish's claim is *outdated* in April 2027, never *superseded* — he was right when he said it.

### 6.1 Derivation qualifiers

A parent reference may carry an `@qualifier` marking the fidelity of the derivation edge — a property of the edge, not the node (this encodes the Gemini failure mode):

```
parents="handwritten-notes-p3@faithful"
parents="textbook-derivation@substituted"
```

Vocabulary: `faithful`, `paraphrased`, `interpolated`, `substituted`, `external`, `inferred`, `motivated`. Unqualified edges default to `unspecified` — deliberately distinct from `faithful`; fidelity must be asserted, never assumed. `motivated` (new in v0.2) marks descent-by-provocation: the child exists because the parent posed the problem. It is the workhorse of evolutionary attribution — the Engelbart → Nelson → Berners-Lee chains are largely `@motivated` edges.

---

## 7. Temporal model (diachronic semantics)

### 7.1 Two time dimensions

Following bitemporal database practice, every node distinguishes:

- `asserted=` — when the statement was made (transaction time). ISO 8601, day precision typical. Usually inherited from frontmatter.
- `valid.from=` / `valid.to=` — the interval during which the stated fact held (valid time). Optional; open-ended by default.

### 7.2 Tense

- `tense=indexical` — a claim about the state of the world at assertion time ("no framework exists"). Can be **outdated** by later events.
- `tense=timeless` — mathematics, definitions. Cannot be outdated, only **corrected** (superseded).
- Default: `indexical` for claims and observations; `timeless` for anything carrying `verification.lean`.

### 7.3 Append-only discipline

Documents are historical records. When knowledge changes, authors write **new** nodes with backward edges (`resolves`, `outdates`, `supersedes`, `contradicts`). Nothing is deleted; resolved unknowledge gets `status=resolved resolved_by=<id>` and remains as history.

### 7.4 Worked diachronic example

June 30, 2026:

```markdown
[AI-assisted science has no comparable discovery-confidence
framework]{#barish-confidence-gap .claim tense=indexical
  asserted=2026-06-30 source=sai-summit-2026 status=open}

::: {#post-five-sigma .unknowledge parents=barish-confidence-gap status=open}
What should replace the five-sigma standard for AI-assisted discovery?
:::
```

April 2027, in a new document:

```markdown
::: {#loom-validation-v1 .resolution asserted=2027-04-12
     resolves=post-five-sigma
     outdates=barish-confidence-gap
     parents="barish-confidence-gap@motivated"}
Loom's verification layer now provides discovery-confidence
certification for AI-assisted results: ...
:::
```

Effects, all without touching the 2026 file:

- `post-five-sigma` → `status=resolved resolved_by=loom-validation-v1` (derived)
- `barish-confidence-gap` → outdated as of 2027-04-12 (derived)
- The 2027 system carries the 2026 talk in its ancestry via `@motivated`
- Rendering the 2026 document *after* April 2027 decorates the span: *"outdated 2027-04 → loom-validation-v1"*; rendering `as_of=2026-06-30` shows it open

### 7.5 Time-scoped queries

Every graph query takes an optional `as_of` timestamp. The graph state at time *t* includes only nodes with `asserted ≤ t` and evaluates all statuses using only edges asserted by *t*. This makes "what was known, when" — and therefore honest histories of discovery — mechanically answerable.

### 7.6 Taint propagation

When a node is outdated or superseded, its descendants are **not** automatically invalidated. Whether the change undermines them requires judgment. Instead the extractor propagates a taint: every node downstream of an `outdates`/`supersedes`/`contradicts` event via `parents`, `depends`, or `supports` edges gets `review=needed` (with the triggering event recorded). Clearing the flag is a human or AI review act, recorded as `review.cleared_by=` / `review.cleared=<date>`. The taint queue is itself a research instrument: the graph tells you what to rethink when the world moves.

---

## 8. Confidence, verification, and future bindings

### 8.1 Confidence (fidelity)

`confidence.textual`, `confidence.historical`, `confidence.interpretive`, `confidence.identity` — values are a number in [0,1] or `high|medium|low`.

### 8.2 Verification (independent evidence)

`verification.transcript`, `verification.lean`, `verification.review`, `verification.software`, `verification.reproduced`, `verification.external` — values are node IDs, external identifiers (e.g. a mathlib theorem name), or `pending`. Lean/mathlib is one verification engine among several: `verification.lean=GaussianTailProbability` certifies the mathematics without claiming the surrounding scientific interpretation is proven.

### 8.3 Future bindings and Pendex

A future binding names a capability or event that does not yet exist (the SMTP-before-TCP/IP pattern):

```markdown
::: {#archive-ai-reader .future_binding target=future_ai_agents
     trigger.capability="reason over full Loom archive with provenance"
     trigger.test="can answer: which unknowledge nodes does
                   barish-confidence-gap block?"
     status=pending}
Addressed to future AI systems capable of reasoning over this archive.
:::
```

- `trigger.*` is structured: `trigger.capability`, `trigger.event`, `trigger.node=<id>` (fires when that node resolves), `trigger.test` (an acceptance probe checkable by a human or AI).
- **Firing is a diachronic event** (§7): a resolution node asserts `resolves=archive-ai-reader`, and the binding's derived status becomes `fired`, timestamped by the resolution's `asserted` date.
- **The Pendex is a derived index**, not declared syntax: the set of all nodes with derived status `pending`, maintained by the extractor. It is the loom's directed frontier into the adjacent possible.

---

## 9. Rendering layer

The document is immutable; the **view** is a function of (document, graph, as_of, audience). Reference implementation path: Pandoc Lua filters (or Python via panflute), giving for free:

- **strip** — clean prose (PDF, print): drop all attributes, unwrap spans, hide standalone divs
- **fold** — annotated HTML: attributes collapsed behind hover/click affordances
- **decorate** — temporal overlay: badges on outdated/resolved/tainted spans, computed from the graph at view time
- **extract** — emit the graph (JSON; GraphML/JSON-LD export) instead of a document

An Obsidian plugin is one more renderer, not the architecture.

---

## 10. Extraction pipeline

```
Markdown files → Pandoc AST (or djot) → Loomic extractor
  → node/edge tables with anchors + fingerprints
  → derived state (statuses, taints, Pendex) at requested as_of
  → exports: JSON graph, JSON-LD/PROV, GraphML, review queue
```

Prototype target per user preference: Python (panflute for AST walking, networkx for the graph).

---

## Appendix A — PROV-O mapping

Loomic derivation vocabulary maps onto the W3C PROV ontology, so extracted graphs can be exported as standards-compliant provenance with no information loss on these edges:

| Loomic | PROV-O |
|---|---|
| `parents=x@faithful` | `prov:wasQuotedFrom` |
| `parents=x@paraphrased` | `prov:wasDerivedFrom` |
| `parents=x@substituted` | `prov:wasDerivedFrom` + loom:substituted (extension) |
| `parents=x@inferred` | `prov:wasDerivedFrom` + loom:inferred |
| `parents=x@motivated` | `prov:wasInfluencedBy` |
| `supersedes` | `prov:wasRevisionOf` (inverse) |
| `source` | `prov:hadPrimarySource` |
| `asserted` | `prov:generatedAtTime` |
| author/agent metadata | `prov:wasAttributedTo` |

`outdates`, `resolves`, taint, and tense have no PROV equivalents — they are Loom extensions (proposed namespace `loom:`). Export serializes them alongside PROV terms in JSON-LD.

## Appendix B — Discourse Graph mapping

Joel Chan's Discourse Graphs (Questions/Claims/Evidence in researcher notebooks; active Roam/Obsidian ecosystem) are the closest living relative. Mapping:

| Discourse Graph | Loomic |
|---|---|
| Question (QUE) | `unknowledge` |
| Claim (CLM) | `claim` |
| Evidence (EVD) | `observation` / `experimental_result` |
| supports / opposes | `supports` / `contradicts` |
| informs | `parents=@motivated` |

Loomic supersets: tense/temporal model, derivation fidelity, verification namespace, future bindings, frontiers, taint. Interop with the Discourse Graph community is a stated goal; an exporter to their format is cheap given the mapping.

## Appendix C — Other prior art (design debts)

- **Wikidata statement model** — qualifiers + references + ranks on statements: the at-scale precedent for claims-with-provenance; ranks (preferred/deprecated + point-in-time) prefigure `outdates`.
- **Nanopublications** — assertion/provenance/pubinfo named graphs; append-only retraction model matches §7.3.
- **Bitemporal databases** — assertion vs valid time (§7.1).
- **W3C Web Annotation / Hypothes.is** — selector model for robust anchoring (§3).
- **IBIS / Compendium** — questions as first-class nodes; ancestry of `unknowledge`.
- **Semantic MediaWiki** — inline semantic annotation; cautionary lesson on annotation burden (§1.7).
- **CriticMarkup** — `{>> ... <<}` comment syntax; a delimiter-collision reason v0.1's `<<...>>` was withdrawn.
- **Engelbart, Nelson, FRESS/Xanadu** — evolutionary attribution lineage that Loom itself must represent.

## Appendix D — Changes from v0.1

1. Delimiters `<<...>>` → Pandoc attributes (`[span]{...}`, `::: {...}`); CriticMarkup collision removed; LaTeX-safe.
2. Block-binds-to-previous-paragraph rule withdrawn; explicit divs instead.
3. Temporal model added: `asserted`, `valid.*`, `tense`, `outdates`, time-scoped queries, taint propagation.
4. `resolution` node type added; `pendex_node` withdrawn (Pendex is derived).
5. `@motivated` derivation qualifier added.
6. Frontmatter defaults added.
7. PROV / Discourse Graph mappings added.

## Appendix E — Open questions (unknowledge about Loomic)

1. Loom (corpus) manifest format and cross-loom federation (`loomname:id`).
2. Whether edge qualifiers generalize beyond derivation (e.g., `supports=x@weak`).
3. Anchor-drift repair workflow when prose is edited under a span.
4. Canonical graph serialization: JSON-LD context design for the `loom:` namespace.
5. Authoring ergonomics: how much annotation can an AI assistant add subject to the fidelity rules it is annotating? (Self-application: the assistant's additions need `@inferred` edges.)
6. Taint semantics across `contradicts`: symmetric or directed?
