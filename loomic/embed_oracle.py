"""
embed_oracle.py — the independent semantic oracle the null model demanded.

RUN THIS ON YOUR OWN MACHINE (not in the Cowork sandbox, which is firewalled off
from your localhost). It talks to a local LM Studio server over its
OpenAI-compatible embeddings endpoint, embeds every claim in both looms with a
model that never saw the theme labels, and asks the one question that actually
decides whether the cross-corpus rhymes are real:

    For a macro bucket with `a` claims from the 1995 loom and `b` claims from the
    2026 loom, is the mean CROSS-CORPUS cosine similarity between those two
    subsets higher than you'd get by drawing a random 1995-subset of size `a`
    and a random 2026-subset of size `b`?

This is a matched-size resampling null: it holds the two-sided sizes fixed and
tests only whether THESE particular claims are more semantically aligned across
the corpora than random claims from the same corpora. Unlike the size statistic
the first null demolished, a high score here can only come from real content
similarity.

--------------------------------------------------------------------------------
SETUP (on your machine)
  1. In LM Studio: download an embedding model (e.g. "nomic-embed-text-v1.5" or
     "text-embedding-bge-m3"), then start the local server (Developer tab ->
     Start Server). Default base URL is http://localhost:1234/v1 .
  2. pip install numpy   (requests optional; stdlib urllib is used otherwise)
  3. Put this file in the SAIR folder next to summit.json, loom-export.json,
     rover_themes.json, rover_themes_webwatch.json, convergence_rover_multi.py.
  4. Run:
       python embed_oracle.py --check          # verify server + list models
       python embed_oracle.py --model nomic-embed-text-v1.5
     (omit --model to auto-pick the first embedding model the server lists)

OUTPUT: a per-bucket table with observed cross-corpus cosine and an empirical
p-value, plus a JSON dump (embed_oracle_results.json) and an embedding cache
(embed_cache.json) so re-runs are instant.
--------------------------------------------------------------------------------
"""
from __future__ import annotations
import argparse, json, hashlib, random, sys, urllib.request, urllib.error
from pathlib import Path
from collections import defaultdict

import numpy as np

from convergence_rover_multi import THEME_TO_MACRO, CLAIM_TYPES

HERE = Path(__file__).resolve().parent
CACHE = HERE / "embed_cache.json"

# (loom json, theme json) — same inputs as the multi-loom Rover
LOOMS = [
    ("summit.json", "rover_themes.json"),
    ("loom-export.json", "rover_themes_webwatch.json"),
]


# ---------------------------------------------------------------- OpenAI-compatible I/O
# Works with any OpenAI-compatible embeddings server: LM Studio (local, no key),
# OpenAI (--base https://api.openai.com/v1 + key), or others. API key is read
# from --api-key or the OPENAI_API_KEY / LMSTUDIO_API_KEY env var, and is only
# ever sent as an Authorization header — never printed or written to disk.
_API_KEY = None


def _headers():
    h = {"Content-Type": "application/json"}
    if _API_KEY:
        h["Authorization"] = f"Bearer {_API_KEY}"
    return h


def _post(url, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=_headers())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def list_models(base):
    try:
        return [m["id"] for m in _get(base.rstrip("/") + "/models")["data"]]
    except Exception as e:
        print(f"  ! could not list models: {e}")
        return []


def embed_batch(base, model, texts):
    out = _post(base.rstrip("/") + "/embeddings", {"model": model, "input": texts})
    return [np.asarray(d["embedding"], dtype=np.float32) for d in out["data"]]


# ---------------------------------------------------------------- loom loading
def load_nodes():
    """All claim/hypothesis nodes from both looms: id-> {loom, src, text, macro}."""
    nodes = {}
    for loom_path, theme_path in LOOMS:
        d = json.loads((HERE / loom_path).read_text())
        loom = d["loom"]
        themes = json.loads((HERE / theme_path).read_text())["themes"]
        for n in d["nodes"]:
            if n["type"] in CLAIM_TYPES and (n.get("label") or "").strip():
                fine = themes.get(n["id"], {}).get("theme")
                nodes[f"{loom}:{n['id']}"] = {
                    "loom": loom,
                    "src": (n.get("files") or [""])[0].split("/")[-1].replace(".md", "") or "?",
                    "text": n["label"].strip(),
                    "macro": THEME_TO_MACRO.get(fine),
                }
    return nodes


# ---------------------------------------------------------------- embeddings
def get_embeddings(base, model, nodes):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    key = lambda t: hashlib.sha1((model + "" + t).encode()).hexdigest()
    todo = [n["text"] for n in nodes.values() if key(n["text"]) not in cache]
    todo = sorted(set(todo))
    if todo:
        print(f"  embedding {len(todo)} new texts via {model} ...")
        for i in range(0, len(todo), 32):
            chunk = todo[i:i + 32]
            for t, v in zip(chunk, embed_batch(base, model, chunk)):
                cache[key(t)] = v.tolist()
            print(f"    {min(i+32,len(todo))}/{len(todo)}")
        CACHE.write_text(json.dumps(cache))
    emb = {}
    for nid, n in nodes.items():
        v = np.asarray(cache[key(n["text"])], dtype=np.float32)
        nrm = np.linalg.norm(v)
        emb[nid] = v / nrm if nrm else v          # L2-normalize -> dot = cosine
    return emb


# ---------------------------------------------------------------- statistic + null
def cross_cosine(ids_a, ids_b, emb):
    """Mean cosine over all cross-corpus pairs (a in loom1, b in loom2)."""
    A = np.stack([emb[i] for i in ids_a]); B = np.stack([emb[i] for i in ids_b])
    return float((A @ B.T).mean())


def run(base, model, iters, seed):
    nodes = load_nodes()
    emb = get_embeddings(base, model, nodes)

    looms = sorted({n["loom"] for n in nodes.values()})
    L1, L2 = looms[0], looms[1]
    pool1 = [i for i, n in nodes.items() if n["loom"] == L1]
    pool2 = [i for i, n in nodes.items() if n["loom"] == L2]

    buckets = defaultdict(lambda: {L1: [], L2: []})
    for nid, n in nodes.items():
        if n["macro"]:
            buckets[n["macro"]][n["loom"]].append(nid)

    rng = random.Random(seed)
    rows = []
    for macro, side in sorted(buckets.items()):
        a, b = side[L1], side[L2]
        if len(a) < 1 or len(b) < 1:
            continue                                  # not cross-corpus
        obs = cross_cosine(a, b, emb)
        ge = 0
        for _ in range(iters):
            ra = rng.sample(pool1, len(a))
            rb = rng.sample(pool2, len(b))
            if cross_cosine(ra, rb, emb) >= obs:
                ge += 1
        rows.append({"macro": macro, "n_1995": len(b), "n_2026": len(a),
                     "obs_cosine": round(obs, 4), "p": round((ge + 1) / (iters + 1), 4)})

    rows.sort(key=lambda r: r["p"])
    print(f"\nmodel={model}   looms: {L1} (n={len(pool1)})  x  {L2} (n={len(pool2)})")
    print(f"matched-size resampling null, {iters} iters/bucket\n")
    print(f"  {'macro':40} {'n2026':>5} {'n1995':>5} {'cos':>7} {'p':>7}")
    for r in rows:
        star = "  <-- survives (p<0.05)" if r["p"] < 0.05 else ""
        print(f"  {r['macro']:40} {r['n_2026']:5} {r['n_1995']:5} "
              f"{r['obs_cosine']:7.3f} {r['p']:7.4f}{star}")
    survivors = [r["macro"] for r in rows if r["p"] < 0.05]
    print(f"\n  survivors (real cross-corpus rhymes at p<0.05): {survivors or 'NONE'}")
    (HERE / "embed_oracle_results.json").write_text(
        json.dumps({"model": model, "iters": iters, "buckets": rows}, indent=2))
    print(f"  wrote embed_oracle_results.json")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:1234/v1",
                    help="OpenAI-compatible base URL "
                         "(LM Studio default; use https://api.openai.com/v1 for OpenAI)")
    ap.add_argument("--model", default=None, help="embedding model id (auto if omitted; "
                    "for OpenAI use e.g. text-embedding-3-small)")
    ap.add_argument("--api-key", default=None,
                    help="API key; defaults to $OPENAI_API_KEY. Not needed for LM Studio.")
    ap.add_argument("--iters", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--check", action="store_true", help="probe server + list models, then exit")
    args = ap.parse_args()

    global _API_KEY
    import os
    _API_KEY = args.api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("LMSTUDIO_API_KEY")

    try:
        models = list_models(args.base)
    except Exception as e:
        sys.exit(f"Cannot reach LM Studio at {args.base}\n  {e}\n"
                 "Is the LM Studio server running? (Developer tab -> Start Server)")
    print(f"server OK at {args.base}; models: {models or '(none listed)'}")
    if args.check:
        return

    model = args.model or next((m for m in models if "embed" in m.lower()), None) \
        or (models[0] if models else None)
    if not model:
        sys.exit("No model available. Load an embedding model in LM Studio.")
    if "embed" not in model.lower():
        print(f"  ! '{model}' may not be an embedding model; pass --model explicitly if this fails.")
    run(args.base, model, args.iters, args.seed)


if __name__ == "__main__":
    main()
