"""
convergence_rover_multi.py — cross-CORPUS Convergence-Rover.

Extends convergence_rover.py from one loom to several. The new capability:
detect a structural fact that surfaces in MULTIPLE looms — e.g. the 1995 Web
Watch columns AND the 2026 summit — under entirely different vocabularies and
separated by decades. No scholarly-graph system (citation index, keyword
search) can do this, because across corpora the shared words and shared
citations are exactly zero.

Two levels of theme:
  - fine theme   : loom-local ("generation-outruns-validation" in 2026,
                   "integrity-lags-connectivity" in 1995).
  - MACRO theme  : the cross-corpus structural fact both roll up to
                   ("capability-outruns-governance"). The roll-up map is the
                   semantic backend's cross-corpus abstraction (LLM judge /
                   embedding cluster over fine-theme descriptions), marked
                   @inferred, for human review — it is where the actual
                   cross-decade discovery is asserted, so it must be auditable.

A convergence is CROSS-CORPUS iff its members come from >= 2 distinct looms.
Nodes are namespaced `loom:id` per Loomic-Spec-v0.2 sec.4.2.

Usage:
    python convergence_rover_multi.py \
        --loom summit.json:rover_themes.json \
        --loom loom-export.json:rover_themes_webwatch.json
"""
from __future__ import annotations
import argparse, json, itertools
from collections import defaultdict
from pathlib import Path

CLAIM_TYPES = {"claim", "hypothesis"}
MIN_LOOMS = 2          # a cross-corpus convergence must span at least this many looms
MIN_SOURCES = 3

# The semantic backend's cross-corpus roll-up: fine theme -> macro structural fact.
# This is the auditable heart of the cross-decade claim. Everything a human should
# scrutinize about "is this really the same fact?" is one line in this table.
THEME_TO_MACRO = {
    # ---- 2026 summit fine themes ----
    "generation-outruns-validation": "capability-outruns-governance",
    "instrumentation-data-bottleneck": "capability-outruns-governance",
    "regional-capacity-and-access": "access-and-equity-divide",
    "autonomous-ai-society": "decentralization-dissolves-the-center",
    "ai-embedded-in-simulation": "new-empirical-substrate",
    "quantum-hardware-progress": "new-empirical-substrate",
    "sparse-reward-hard-search": "sparse-reward-hard-search",
    "representation-theory": "representation-theory",
    "human-skill-atrophy": "human-skill-atrophy",
    "interdisciplinary-mission": "interdisciplinary-mission",
    # ---- 1995 Web Watch fine themes ----
    "integrity-lags-connectivity": "capability-outruns-governance",
    "commons-preemption-window": "capability-outruns-governance",
    "decentralization-no-center": "decentralization-dissolves-the-center",
    "globalization-homogenization": "access-and-equity-divide",
    "process-over-snapshot": "new-empirical-substrate",
}


def load(loom_path, theme_path):
    d = json.loads(Path(loom_path).read_text())
    loom = d["loom"]
    themes = json.loads(Path(theme_path).read_text())["themes"]
    nodes = {}
    for n in d["nodes"]:
        if n["type"] in CLAIM_TYPES and (n.get("label") or "").strip():
            nid = f"{loom}:{n['id']}"
            fine = themes.get(n["id"], {})
            macro = THEME_TO_MACRO.get(fine.get("theme"))
            nodes[nid] = {
                "loom": loom,
                "local_id": n["id"],
                "src": (n.get("files") or [""])[0].split("/")[-1].replace(".md", "") or "?",
                "label": (n.get("label") or "")[:110],
                "fine": fine.get("theme"),
                "macro": macro,
                "role": fine.get("role"),
            }
    return loom, nodes


def cross_corpus_convergences(all_nodes):
    by_macro = defaultdict(list)
    for nid, n in all_nodes.items():
        if n["macro"]:
            by_macro[n["macro"]].append(nid)
    convs = []
    for macro, members in by_macro.items():
        looms = {all_nodes[m]["loom"] for m in members}
        srcs = {all_nodes[m]["src"] for m in members}
        if len(looms) < MIN_LOOMS or len(srcs) < MIN_SOURCES:
            continue
        convs.append({
            "macro": macro, "members": members,
            "looms": sorted(looms), "sources": sorted(srcs),
            "n_claims": len(members), "n_looms": len(looms), "n_sources": len(srcs),
            "score": len(members) * len(looms) * len(srcs),
        })
    return sorted(convs, key=lambda c: c["score"], reverse=True)


def emit(conv, all_nodes):
    fines = sorted({all_nodes[m]["fine"] for m in conv["members"]})
    parents = ",".join(f"{m}@inferred" for m in conv["members"])
    per_loom = defaultdict(list)
    for m in conv["members"]:
        per_loom[all_nodes[m]["loom"]].append(all_nodes[m]["fine"])
    span = " + ".join(f"{k} (as '{sorted(set(v))[0]}')" for k, v in per_loom.items())
    return "\n".join([
        f"::: {{#rover-xcorpus-{conv['macro']} .unknowledge asserted=2026-07-05",
        f"     asserted_by=convergence-rover-multi status=open",
        f'     parents="{parents}"}}',
        f"CANDIDATE CROSS-CORPUS CONVERGENCE (macro: {conv['macro']}).",
        f"{conv['n_claims']} claims from {conv['n_looms']} looms and "
        f"{conv['n_sources']} source documents express one structural fact.",
        f"Spanning: {span}.",
        f"Fine themes rolled up: {', '.join(f for f in fines if f)}.",
        "The roll-up (that these distinct fine themes are the same fact) is the",
        "@inferred cross-corpus abstraction; clearing requires review.cleared_by=<curator>.",
        ":::",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loom", action="append", required=True,
                    help="loom.json:themes.json  (repeatable)")
    args = ap.parse_args()

    all_nodes = {}
    loom_names = []
    for spec in args.loom:
        lp, tp = spec.split(":")
        name, nodes = load(lp, tp)
        loom_names.append(name)
        all_nodes.update(nodes)
    print(f"looms: {', '.join(loom_names)}   tagged claim pool: {len(all_nodes)}\n")

    convs = cross_corpus_convergences(all_nodes)
    if not convs:
        print("No cross-corpus convergence found.")
        return
    print(f"=== {len(convs)} CROSS-CORPUS convergence(s) "
          f"(>= {MIN_LOOMS} looms, >= {MIN_SOURCES} sources) ===\n")
    for i, c in enumerate(convs, 1):
        print(f"[{i}] score={c['score']}  {c['n_claims']} claims  "
              f"x {c['n_looms']} looms  x {c['n_sources']} sources  :: {c['macro']}")
        for m in sorted(c["members"], key=lambda x: all_nodes[x]["loom"]):
            n = all_nodes[m]
            print(f"      {n['loom']:14} {n['local_id']:32} [{n['role'] or '-':7}] "
                  f"{n['fine']:28} :: {n['label'][:55]}")
        print()
    print("=" * 72)
    print("PROPOSED LOOMIC NODES (append-only, @inferred):\n")
    for c in convs:
        print(emit(c, all_nodes)); print()


if __name__ == "__main__":
    main()
