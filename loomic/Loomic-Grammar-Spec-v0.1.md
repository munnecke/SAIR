# Loomic Grammar Specification

**Version 0.1 — Draft**
**Status:** working proposal for review
**Depends on:** Loom/Loomic Handoff v0.9

Loomic is a lightweight inline annotation language for Loom documents. Prose remains primary and human-readable; annotations expose a directed graph for machine reasoning. This spec defines the syntax precisely enough to write a parser, while deferring most semantics (node-type vocabularies, trigger evaluation) to companion specs.

---

## 1. Design constraints

1. A Loom document with all annotations deleted must remain a coherent Markdown/Obsidian document.
2. Annotations must be extractable by a simple single-pass parser with no knowledge of Markdown beyond code-fence awareness.
3. Every annotation must have an unambiguous **anchor** — the piece of prose (or nothing) it binds to.
4. IDs are stable and immutable; graph identity survives document edits.
5. The syntax should degrade gracefully: an unknown key is preserved, not an error.

---

## 2. Lexical basics

### 2.1 Delimiters

An annotation is delimited by `<<` and `>>`:

```
<<key=value key=value ...>>
```

Annotations may span multiple lines. `>>` inside a quoted string does not terminate the annotation.

Parsers MUST ignore `<<...>>` sequences inside Markdown code fences, inline code spans, and YAML frontmatter.

### 2.2 Keys

```
key        = segment ("." segment)*
segment    = [a-z][a-z0-9_]*
```

Dots create namespaces: `confidence.textual`, `verification.lean`. Keys are lowercase; parsers reject uppercase keys (reserved for future use).

### 2.3 Values

Three value forms:

**Bare token** — `[A-Za-z0-9_.:/@\-]+`
```
type=claim   confidence.textual=0.95
```

**Quoted string** — double quotes, backslash escapes (`\"`, `\\`, `\n`):
```
trigger="Future AI systems capable of reasoning over this archive"
```

**List** — comma-separated bare tokens (no commas inside bare tokens; use repeated keys or quoted strings if a literal comma is needed):
```
parents=barish-close,ai-confidence-scores
```

A repeated key is equivalent to a list: `parent=a parent=b` ≡ `parents=a,b`. Plural/singular key aliases are resolved by the schema layer, not the grammar.

### 2.4 Node references vs. literals

Values of **edge keys** (§6) are always node IDs. Values of other keys are literals. This is schema-driven, not syntactic — Loomic does not use a sigil like `#id`, keeping annotations quiet on the page.

---

## 3. Anchoring (binding scope)

Every annotation binds to exactly one anchor, determined by what immediately precedes `<<`:

### 3.1 Link-bound

Annotation immediately follows an Obsidian wiki link (whitespace allowed):

```
[[Barry Barish]] <<id=barry-barish type=person role=speaker>>
```

Anchor = the linked concept.

### 3.2 Span-bound

For anchoring to arbitrary prose, wrap the span in `{...}`:

```
{silently substituted canonical derivations}<<id=gemini-substitution
  type=observation derivation=substituted>>
```

Anchor = the braced text. The braces are Loomic syntax and are stripped on rendering. No whitespace between `}` and `<<`. Spans do not nest.

### 3.3 Block-bound

Annotation alone on its own line binds to the **preceding block** (paragraph, list item, heading, or blockquote):

```
Barish observed that physics has the five-sigma standard but
AI-assisted science has no comparable framework.

<<id=barish-confidence-gap type=claim source=barish-2026-close
  confidence.textual=high>>
```

Anchor = that paragraph.

### 3.4 Standalone (anchorless) nodes

An annotation whose first key is `node` declares a graph node with no prose anchor — used for unknowledge, frontiers, future bindings, and Pendex entries that are *about* the document rather than *in* it:

```
<<node id=post-five-sigma
  type=unknowledge
  question="What should replace the five-sigma standard for AI-assisted discovery?"
  parents=barish-confidence-gap
  status=open>>
```

`node` takes no value; it is a marker. Standalone nodes conventionally live at the end of a section or document, but may appear anywhere.

### 3.5 Resolution order

Preceding `}` → span-bound. Else preceding `]]` → link-bound. Else annotation alone on a line → block-bound. Else (mid-sentence, no span/link) → **error**: ambiguous anchor.

---

## 4. Identity

- `id=` assigns a stable ID: lowercase slug, `[a-z0-9][a-z0-9\-]*`, unique within a **loom** (a defined corpus, not just one file).
- IDs are immutable. Renaming is done via a new node with `supersedes=old-id`.
- An annotation without `id=` creates an **anonymous node**; parsers assign a content-hash ID. Anonymous nodes cannot be referenced by other annotations, so anything cited elsewhere needs an explicit ID.
- Cross-file references are bare IDs — the loom namespace is flat by design. (Federation across looms is deferred; likely `loomname:id`.)

## 5. Versioning

- `rev=N` (optional) marks a revision of the same node; content at rev N+1 supersedes rev N but preserves identity.
- `supersedes=id` creates a new identity replacing an old one (stronger than a revision — use when meaning changes).
- Resolved unknowledge is never deleted: it gets `status=resolved resolved_by=<node-id>` and remains in the graph as history.

## 6. Edges

Edge keys whose values are node references:

| Key | Meaning |
|---|---|
| `parents` | derived from / caused by / asked because of |
| `depends` | cannot be evaluated until these nodes resolve |
| `resolves` | this node answers/settles the referenced unknowledge |
| `refines` | narrows or sharpens the referenced node |
| `supports` / `contradicts` | evidentiary relation to a claim |
| `part_of` | membership (frontier, synthesis, collaboration) |
| `supersedes` | identity replacement (§5) |
| `source` | provenance: the document/talk/dataset node this came from |

### 6.1 Edge qualifiers

A parent reference may carry a **derivation qualifier** with `@`, addressing the Gemini failure mode — fidelity is a property of the edge, not the node:

```
parents=handwritten-notes-p3@faithful
parents=textbook-derivation@substituted
```

Qualifier vocabulary (initial): `faithful`, `paraphrased`, `interpolated`, `substituted`, `external`, `inferred`. Unqualified edges default to `unspecified`, which is deliberately distinct from `faithful` — fidelity must be asserted, never assumed.

## 7. Confidence and verification

Per Handoff v0.9, these are separate namespaces:

```
confidence.textual=0.95        # numeric 0–1, or high|medium|low
confidence.interpretive=medium
verification.lean=GaussianTailProbability
verification.transcript=summit-2026-recording
verification.review=pending
```

Grammar-level rule only: `confidence.*` values are a number in [0,1] or one of `high|medium|low`; `verification.*` values are node IDs, external identifiers, or `pending`. Semantics belong to the epistemics spec.

## 8. Future bindings and Pendex

A future binding is a standalone node:

```
<<node id=archive-ai-reader
  type=future_binding
  target=future_ai_agents
  trigger.capability="reason over full Loom archive with provenance"
  trigger.test="can answer: which unknowledge nodes does barish-confidence-gap block?"
  status=pending>>
```

Grammar contribution: `trigger.*` is a namespace, so triggers can be structured (`trigger.capability`, `trigger.event`, `trigger.node=<id>` meaning "fires when that node resolves") rather than a single opaque string. `trigger.test` is a human/AI-checkable acceptance probe. The **Pendex is not separate syntax** — it is the derived index of all nodes with `status=pending`, kept current by the extractor.

## 9. Escaping and edge cases

- Literal `<<` in prose: write `\<<`. (Rare; guillemets `«»` are unaffected.)
- Literal `{` before an annotation: only significant if immediately followed by text and `}<<`; escape as `\{`.
- Annotations inside tables bind to the cell (treated as a block).
- Unknown keys MUST be preserved in the extracted graph (forward compatibility).
- Duplicate non-edge keys on one annotation: last wins, parser warns.

## 10. EBNF (extraction layer)

```ebnf
annotation   = "<<" ws? [node-marker ws] pair (ws pair)* ws? ">>" ;
node-marker  = "node" ;
pair         = key "=" value ;
key          = segment ("." segment)* ;
segment      = lowercase (lowercase | digit | "_")* ;
value        = list | quoted | bare ;
list         = bare ("," bare)+ ;
bare         = barechar+ ;                (* [A-Za-z0-9_.:/@-] *)
quoted       = '"' (escaped | char)* '"' ;
escaped      = "\\" ('"' | "\\" | "n") ;
ws           = (space | tab | newline)+ ;

span         = "{" text "}" annotation ;   (* no ws before annotation *)
```

Anchoring (§3) is resolved by the extractor against the surrounding Markdown, not by this grammar.

## 11. Worked micro-example

```markdown
## Summit close

[[Barry Barish]] <<id=barry-barish type=person role=speaker>> closed the
2026 [[Science and AI Summit]] <<id=sai-summit-2026 type=context>> by
observing that {physics has five-sigma, but AI-assisted science has no
comparable discovery-confidence framework}<<id=barish-confidence-gap
  type=claim source=sai-summit-2026
  confidence.textual=high verification.transcript=pending>>.

<<node id=post-five-sigma type=unknowledge
  question="What should replace five-sigma for AI-assisted discovery?"
  parents=barish-confidence-gap
  part_of=ai-discovery-confidence-frontier
  status=open>>

<<node id=ai-discovery-confidence-frontier type=frontier
  label="Discovery confidence for AI-assisted science"
  status=active>>
```

Extracted graph: 5 nodes, 4 edges, 1 Pendex-adjacent open unknowledge. Delete every `<<...>>` and `{}` pair and the prose reads cleanly.

---

## 12. Open questions (unknowledge about Loomic itself)

1. Should span braces `{}` collide too often with prose/LaTeX? Alternative: `==highlight==<<...>>` reusing Obsidian highlights.
2. Loom (corpus) definition and federation syntax across looms.
3. Whether edge qualifiers (`@`) should generalize beyond derivation (e.g., `supports=x@weak`).
4. Canonical serialization of the extracted graph (JSON-LD? plain JSON + GraphML export?).
5. How annotations interact with Obsidian rendering — a plugin could hide/fold them.
