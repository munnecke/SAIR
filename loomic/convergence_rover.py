"""
convergence_rover.py — the Convergence-Rover for Loom graphs.

Goal: mechanically re-discover cross-discipline UNKNOWLEDGE — one structural
fact that surfaces, in different vocabularies, across source documents that
share no citations and no keywords. This is the "five speakers, five
vocabularies, one structural fact" move performed by hand in
00-summit-loomic-view.md (the `view-generation-outruns-validation` node).

The Rover's thesis, and the reason it belongs on a Loom rather than on a
citation graph or a keyword index:

    Cross-discipline convergence is invisible to LEXICAL signals (shared
    words) and to TOPOLOGICAL signals (shared graph neighbours / citations).
    It lives only in the SEMANTIC content of the claims. So the detector
    needs a semantic cohesion backend; the Loom then supplies the two things
    the backend cannot: (a) source-provenance, so "distance between sources"
    is measurable, and (b) an append-only, @inferred-qualified place to
    record the proposal without laundering a machine guess into the record.

Pipeline
--------
1. Extract claim-like nodes (the candidate pool).
2. Score three cohesion signals between claims:
     - lexical      : keyword Jaccard            (offline baseline; expected to FAIL)
     - concept_graph: shared ref->concept edges  (offline baseline; expected to FAIL)
     - semantic     : latent-theme agreement     (pluggable backend; the one that WORKS)
   The two baselines are included precisely to demonstrate *why* naive tools
   miss these gaps.
3. Cluster the claim pool under the chosen signal, keeping only clusters that
   span >= MIN_SOURCES distinct source documents (the cross-discipline test).
4. Rank clusters by  size * distinct_sources  (a "surprise" score:
   many claims from many different talks = a strong latent convergence).
5. Emit each surviving cluster as a Loomic `.unknowledge`/`.synthesis` div
   with @inferred parent edges — a proposal, not an assertion.

The `semantic` backend here loads rover_themes.json (an LLM-judge / embedding
map). In production, swap `load_semantic_themes()` for a call to an embedding
API + clustering, or an LLM classifier. Everything else is unchanged.

Usage:
    python convergence_rover.py --loom summit.json --signal semantic
    python convergence_rover.py --loom summit.json --signal lexical   # watch it fail
    python convergence_rover.py --loom summit.json --signal concept_graph
"""
from __future__ import annotations
import argparse, json, re, itertools
from collections import defaultdict
from pathlib import Path

CLAIM_TYPES = {"claim"}          # candidate pool; widen to include hypothesis/observation if desired
MIN_SOURCES = 3                  # a convergence must span at least this many distinct source docs
STOP = set("the a an and or of to in for on with is are be as that this it by we you they our "
           "their can will not no more most than then so at from into may its has have was were "
           "which who what when where how also but if while these those there here".split())


# ----------------------------------------------------------------------
# Loom access helpers
# ----------------------------------------------------------------------
def load_loom(path):
    d = json.loads(Path(path).read_text())
    nodes = {n["id"]: n for n in d["nodes"]}
    return d, nodes, d["edges"]


def node_text(n):
    return (n.get("label") or n.get("attrs", {}).get("title", "") or "").strip()


def source_doc(n):
    f = (n.get("files") or [""])[0]
    return f.split("/")[-1].replace(".md", "") or n.get("container") or "?"


def claim_pool(nodes):
    return [n for n in nodes.values() if n["type"] in CLAIM_TYPES and node_text(n)]


# ----------------------------------------------------------------------
# Cohesion signals
# ----------------------------------------------------------------------
def _tokens(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


def lexical_cohesion(pool, edges):
    """Keyword Jaccard between claim labels. Offline. Expected to FAIL cross-vocabulary."""
    tok = {n["id"]: _tokens(node_text(n)) for n in pool}
    def score(a, b):
        A, B = tok[a], tok[b]
        u = A | B
        return len(A & B) / len(u) if u else 0.0
    return score


def concept_graph_cohesion(pool, edges):
    """Shared ref->concept edges (incl. document co-members). Offline. Expected to FAIL:
    convergent claims sit in different topical neighbourhoods."""
    concept_ids = {e["dst"] for e in edges if e["kind"] == "ref"}
    members = defaultdict(list)
    for nid in [n["id"] for n in pool]:
        members[nid] = []
    refs = defaultdict(set)
    for e in edges:
        if e["kind"] == "ref":
            refs[e["src"]].add(e["dst"])
    cset = {n["id"]: set(refs.get(n["id"], set())) for n in pool}
    def score(a, b):
        A, B = cset[a], cset[b]
        u = A | B
        return len(A & B) / len(u) if u else 0.0
    return score


def load_semantic_themes(path="rover_themes.json"):
    return json.loads(Path(path).read_text())["themes"]


def semantic_cohesion(pool, edges, themes):
    """Latent-theme agreement. THIS is the signal that works. 1.0 if two claims
    express the same structural fact (same theme), else 0. In production replace
    with embedding cosine or LLM pairwise judgement."""
    def score(a, b):
        ta, tb = themes.get(a, {}).get("theme"), themes.get(b, {}).get("theme")
        return 1.0 if (ta and ta == tb) else 0.0
    return score


# ----------------------------------------------------------------------
# Clustering + ranking
# ----------------------------------------------------------------------
def cluster(pool, score, threshold=0.5):
    """Connected components over the 'cohesion >= threshold' graph (single-link)."""
    ids = [n["id"] for n in pool]
    parent = {i: i for i in ids}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    for a, b in itertools.combinations(ids, 2):
        if score(a, b) >= threshold:
            union(a, b)
    comp = defaultdict(list)
    for i in ids:
        comp[find(i)].append(i)
    return [members for members in comp.values() if len(members) > 1]


def rank_convergences(clusters, nodes):
    out = []
    for members in clusters:
        srcs = {source_doc(nodes[m]) for m in members}
        if len(srcs) < MIN_SOURCES:
            continue
        out.append({
            "members": members,
            "sources": sorted(srcs),
            "n_claims": len(members),
            "n_sources": len(srcs),
            "score": len(members) * len(srcs),   # surprise: many claims x many talks
        })
    return sorted(out, key=lambda c: c["score"], reverse=True)


# ----------------------------------------------------------------------
# Emit a Loomic proposal (append-only, @inferred)
# ----------------------------------------------------------------------
def emit_loomic(conv, nodes, themes, idx):
    theme = themes.get(conv["members"][0], {}).get("theme", "cross-discipline-convergence")
    node_id = f"rover-convergence-{theme}"
    gaps = [m for m in conv["members"] if themes.get(m, {}).get("role") == "gap"]
    parents = ",".join(f"{m}@inferred" for m in conv["members"])
    lines = [
        f"::: {{#{node_id} .unknowledge asserted=2026-07-05 asserted_by=convergence-rover",
        f"     status=open parents=\"{parents}\"}}",
        f"CANDIDATE CROSS-DISCIPLINE CONVERGENCE (theme: {theme}).",
        f"{conv['n_claims']} claims from {conv['n_sources']} distinct source documents",
        f"express one structural fact under different vocabularies. Sources:",
        "  " + "; ".join(conv["sources"]) + ".",
        f"Gap-role claims (open problems feeding this frontier): {', '.join(gaps) or '—'}.",
        "Proposed for human review. All parent edges are @inferred (machine-proposed,",
        "not asserted); clearing requires review.cleared_by=<curator>.",
        ":::",
    ]
    return "\n".join(lines)


# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loom", default="summit.json")
    ap.add_argument("--signal", choices=["lexical", "concept_graph", "semantic"], default="semantic")
    ap.add_argument("--themes", default="rover_themes.json")
    ap.add_argument("--threshold", type=float, default=0.5)
    args = ap.parse_args()

    d, nodes, edges = load_loom(args.loom)
    pool = claim_pool(nodes)
    print(f"loom={d['loom']}  claim-pool={len(pool)} nodes  signal={args.signal}\n")

    if args.signal == "lexical":
        score = lexical_cohesion(pool, edges)
    elif args.signal == "concept_graph":
        score = concept_graph_cohesion(pool, edges)
    else:
        themes = load_semantic_themes(args.themes)
        score = semantic_cohesion(pool, edges, themes)

    clusters = cluster(pool, score, args.threshold)
    convs = rank_convergences(clusters, nodes)

    if not convs:
        print("No cross-discipline convergence found at this signal/threshold.")
        print("(For lexical & concept_graph baselines this is the POINT: the signal is blind\n"
              " to convergence that spans vocabularies. Re-run with --signal semantic.)")
        return

    themes = load_semantic_themes(args.themes) if args.signal == "semantic" else {}
    print(f"=== {len(convs)} cross-discipline convergence(s) found "
          f"(>= {MIN_SOURCES} distinct sources) ===\n")
    for i, c in enumerate(convs, 1):
        print(f"[{i}] score={c['score']}  {c['n_claims']} claims x {c['n_sources']} sources")
        for m in c["members"]:
            role = themes.get(m, {}).get("role", "") if themes else ""
            print(f"      - {m:36} {('['+role+']') if role else '':8} ({source_doc(nodes[m])})")
        print()
    if args.signal == "semantic":
        print("=" * 70)
        print("PROPOSED LOOMIC NODES (append-only, @inferred — paste into a new dated doc):\n")
        for i, c in enumerate(convs, 1):
            print(emit_loomic(c, nodes, themes, i)); print()


if __name__ == "__main__":
    main()
