"""
null_model.py — permutation null test for the cross-corpus Convergence-Rover.

The worry it addresses: the four cross-corpus convergences might be an artifact
of *tagging density* — once you sort many claims from two corpora into a handful
of shared macro-buckets, getting clusters that "span both looms" may be nearly
guaranteed and therefore meaningless.

Method: hold the multiset of macro labels fixed and randomly PERMUTE which claim
node gets which label (destroying the association between a node's
content-derived macro and its actual loom + source document). Recompute the
Rover's cross-corpus statistics on each permutation. Compare observed to the null
distribution -> empirical p-value.

Three statistics, increasingly strict:
  N_xcorpus   : # macros spanning >= 2 looms and >= 3 total sources
  N_balanced  : # macros with >= 2 distinct sources IN EACH loom (genuine two-
                sided spread — the honest test; a density artifact tends to be
                dominated by the larger corpus)
  TOP_score   : max(size * n_looms * n_sources)  -- a pure size statistic,
                included precisely to show whether "big score" means anything.

Reads the same inputs as convergence_rover_multi.py.
"""
from __future__ import annotations
import json, random, argparse
from collections import defaultdict, Counter
from pathlib import Path

from convergence_rover_multi import THEME_TO_MACRO, CLAIM_TYPES

MIN_LOOMS, MIN_SOURCES, MIN_PER_LOOM_SOURCES = 2, 3, 2


def load_pool(pairs):
    """Return list of nodes: {loom, src, macro} for every tagged claim node."""
    pool = []
    for loom_path, theme_path in pairs:
        d = json.loads(Path(loom_path).read_text())
        loom = d["loom"]
        themes = json.loads(Path(theme_path).read_text())["themes"]
        for n in d["nodes"]:
            if n["type"] in CLAIM_TYPES and (n.get("label") or "").strip():
                fine = themes.get(n["id"], {}).get("theme")
                macro = THEME_TO_MACRO.get(fine)
                if macro:
                    src = (n.get("files") or [""])[0].split("/")[-1].replace(".md", "") or "?"
                    pool.append({"loom": loom, "src": f"{loom}:{src}", "macro": macro})
    return pool


def stats(pool, macro_assignment):
    """Compute the three statistics for a given list-of-macros aligned to pool."""
    by_macro = defaultdict(lambda: {"looms": set(), "sources": set(),
                                    "per_loom_src": defaultdict(set), "n": 0})
    for node, macro in zip(pool, macro_assignment):
        g = by_macro[macro]
        g["looms"].add(node["loom"]); g["sources"].add(node["src"])
        g["per_loom_src"][node["loom"]].add(node["src"]); g["n"] += 1
    n_x = n_bal = 0
    top = 0
    for g in by_macro.values():
        if len(g["looms"]) >= MIN_LOOMS and len(g["sources"]) >= MIN_SOURCES:
            n_x += 1
            top = max(top, g["n"] * len(g["looms"]) * len(g["sources"]))
            if all(len(s) >= MIN_PER_LOOM_SOURCES for s in g["per_loom_src"].values()) \
               and len(g["per_loom_src"]) >= MIN_LOOMS:
                n_bal += 1
    return n_x, n_bal, top


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loom", action="append", required=True, help="loom.json:themes.json")
    ap.add_argument("--iters", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    pairs = [s.split(":") for s in args.loom]

    pool = load_pool(pairs)
    labels = [n["macro"] for n in pool]
    print(f"tagged claim pool: {len(pool)} nodes across "
          f"{len(set(n['loom'] for n in pool))} looms")
    print(f"macro-label counts: {dict(Counter(labels))}")
    print(f"per-loom node counts: {dict(Counter(n['loom'] for n in pool))}\n")

    obs = stats(pool, labels)
    print(f"OBSERVED:  N_xcorpus={obs[0]}   N_balanced={obs[1]}   TOP_score={obs[2]}\n")

    rng = random.Random(args.seed)
    shuffled = list(labels)
    ge = [0, 0, 0]                      # count of null >= observed
    null_top = []
    for _ in range(args.iters):
        rng.shuffle(shuffled)
        s = stats(pool, shuffled)
        for k in range(3):
            if s[k] >= obs[k]:
                ge[k] += 1
        null_top.append(s[2])

    N = args.iters
    print(f"permutation null ({N} iters), empirical p = P(null >= observed):")
    print(f"  N_xcorpus  : p = {ge[0]/N:.4f}   (higher score = more shared macros span looms)")
    print(f"  N_balanced : p = {ge[1]/N:.4f}   (the honest two-sided-spread test)")
    print(f"  TOP_score  : p = {ge[2]/N:.4f}   (pure size statistic)")
    import statistics as st
    print(f"\n  null TOP_score: mean={st.mean(null_top):.0f}  "
          f"max={max(null_top)}  vs observed={obs[2]}")
    print("\nInterpretation guide:")
    print("  p < 0.05 on N_balanced  => the two-sided cross-corpus rhymes are NOT")
    print("     explainable by tagging density alone; the macro alignment carries signal.")
    print("  N_xcorpus/TOP_score p ~ large => raw 'spans 2 looms' and big cluster size")
    print("     are cheap once buckets are shared; they do NOT by themselves prove a rhyme.")


if __name__ == "__main__":
    main()
