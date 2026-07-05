# Loomic pilot — presentations

Loomic 0.2 rewrites of the SAIR UCR 2026 presentation notes. Conventions:

- **Originals are untouched.** Files in `../presentations/` are the historical record; every Loomic file carries `parents` edges back to its transcript and talk.
- **Loom:** `sair-ucr-2026`. All IDs are loom-wide unique.
- **Syntax:** Pandoc attributes per `Loomic-Spec-v0.2.md` — `[span]{#id .type key=value}` inline, `::: {...}` for blocks and standalone nodes.
- **Density:** structural — people/concept refs, key claims, derivation edges, unknowledge/frontier/future-binding nodes. Not every sentence.
- **Derivation discipline:** Summaries were AI-generated from transcripts → summary blocks carry `parents="<transcript-id>@paraphrased"`. Transcripts are faithful records of the talks (`@faithful`) but auto-transcribed, so `confidence.textual=medium` (e.g., "Gaussian tales" verbatim).
- **Wiki links** (`[[...]]`) remain as Obsidian sugar for plain mentions; annotated mentions use `[text]{ref=id}` or full spans.
- **Note:** the vault's `loom-language-spec.md` ("Loom Language v0.2", intrinsics/cascades) is a different lineage from Loomic; naming reconciliation pending.

Pilot files:

1. `barry-barish-closing-discovery-confidence.md`
2. `terence-tao-ai-augmented-mathematics.md`
3. `david-brin-contextual-dimensions-of-ai.md`
4. `ucr-welcome-and-sair-foundation-opening.md`
5. `ucr-chancellor-address.md`
6. `sair-platform-overview.md`
7. `anima-anandkumar-neural-operators.md`
8. `hartmut-neven-quantum-computing.md`
9. `evangelos-papalexakis-tensor-decomposition.md`
