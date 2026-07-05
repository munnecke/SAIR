"""
loomic.py — Loomic 0.2 extractor.

Parses Loomic annotations (Pandoc attribute syntax) from Markdown files and
builds a temporally-indexed knowledge graph per Loomic-Spec-v0.2.md.

Library-only: designed for Jupyter / pipeline use. No CLI.

Usage:
    from loomic import Loom
    loom = Loom.from_paths(["SAIR/SAIR UCR 2026/presentations-loomic"])
    loom.report()
    loom.node("barish-confidence-gap")
    loom.pendex()
    loom.to_json("loom.json")
    g = loom.to_networkx()          # optional, needs networkx

Dependencies: pyyaml (frontmatter). Optional: networkx (graph export),
pandas (dataframe views).

Parser notes: this is a self-contained parser for the Loomic subset of
Pandoc syntax (bracketed spans, fenced divs, attribute blocks, wiki links,
YAML frontmatter). A pandoc-AST backend could replace it later without
changing the public API.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

__version__ = "0.2.0"

# ----------------------------------------------------------------------
# Vocabulary (Loomic-Spec-v0.2)
# ----------------------------------------------------------------------

EDGE_KEYS = {
    "parents", "parent", "depends", "resolves", "outdates", "refines",
    "supports", "contradicts", "part_of", "supersedes", "source", "ref",
}
EDGE_KEY_ALIASES = {"parent": "parents"}

DERIVATION_QUALIFIERS = {
    "faithful", "paraphrased", "interpolated", "substituted",
    "external", "inferred", "motivated", "unspecified",
}

NODE_TYPES = {
    "person", "concept", "claim", "observation", "historical_claim",
    "context", "evidence_gap", "problem", "hypothesis",
    "experimental_result", "interpretation", "synthesis", "frontier",
    "unknowledge", "future_binding", "resolution", "document", "unknown",
}

TAINT_EVENT_KINDS = {"outdates", "supersedes", "contradicts"}
TAINT_PROPAGATION_KINDS = {"parents", "depends", "supports"}


# ----------------------------------------------------------------------
# Small utilities
# ----------------------------------------------------------------------

def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return re.sub(r"-+", "-", s).strip("-")


def _fingerprint(text: str) -> str:
    norm = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]


def _parse_date(v):
    if isinstance(v, date):
        return v
    if v is None:
        return None
    try:
        return date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


# ----------------------------------------------------------------------
# Low-level parsing
# ----------------------------------------------------------------------

def _split_frontmatter(text: str):
    """Return (frontmatter_dict, full_text). Offsets are into full_text."""
    fm = {}
    if text.startswith("---"):
        m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", text, re.S)
        if m:
            if yaml is not None:
                try:
                    fm = yaml.safe_load(m.group(1)) or {}
                except yaml.YAMLError:
                    fm = {}
            # Mask frontmatter so body parsing skips it.
            masked = _mask_region(text, 0, m.end())
            return fm, masked
    return fm, text


def _mask_region(text: str, start: int, end: int) -> str:
    """Replace text[start:end] with spaces, preserving newlines & length."""
    chunk = "".join(c if c == "\n" else " " for c in text[start:end])
    return text[:start] + chunk + text[end:]


def _mask_code(text: str) -> str:
    """Mask fenced code blocks and inline code spans."""
    out_lines = []
    in_fence = False
    fence_char = ""
    for line in text.split("\n"):
        stripped = line.lstrip()
        if in_fence:
            out_lines.append(" " * len(line))
            if stripped.startswith(fence_char * 3):
                in_fence = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence_char = stripped[0]
            in_fence = True
            out_lines.append(" " * len(line))
            continue
        # Mask inline code `...`
        line = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        out_lines.append(line)
    return "\n".join(out_lines)


def _match_brace(text: str, open_idx: int):
    """Given index of '{', return index of matching '}' (quote-aware)."""
    depth = 0
    in_quote = False
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if in_quote:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_quote = False
        else:
            if c == '"':
                in_quote = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return None


def parse_attrs(s: str) -> dict:
    """Parse a Pandoc attribute block body (without outer braces)."""
    result = {"id": None, "classes": [], "kv": {}}
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c == "#":
            j = i + 1
            while j < n and not s[j].isspace():
                j += 1
            result["id"] = s[i + 1:j]
            i = j
        elif c == ".":
            j = i + 1
            while j < n and not s[j].isspace():
                j += 1
            result["classes"].append(s[i + 1:j])
            i = j
        else:
            j = i
            while j < n and s[j] != "=" and not s[j].isspace():
                j += 1
            key = s[i:j]
            if j < n and s[j] == "=":
                j += 1
                if j < n and s[j] == '"':
                    k = j + 1
                    buf = []
                    while k < n:
                        if s[k] == "\\" and k + 1 < n:
                            buf.append(s[k + 1])
                            k += 2
                            continue
                        if s[k] == '"':
                            break
                        buf.append(s[k])
                        k += 1
                    val = "".join(buf)
                    j = k + 1
                else:
                    k = j
                    while k < n and not s[k].isspace():
                        k += 1
                    val = s[j:k]
                    j = k
                result["kv"][key] = val
            else:
                result["kv"][key] = "true"
            i = j
    return result


def _find_divs(text: str, warnings: list, fname: str):
    """Find fenced divs `::: {attrs} ... :::`. Returns list of dicts."""
    divs = []
    stack = []
    for m in re.finditer(r"^[ \t]*(:{3,})[ \t]*(\{?)", text, re.M):
        line_end = text.find("\n", m.start())
        if line_end == -1:
            line_end = len(text)
        if m.group(2) == "{":
            brace_open = m.end() - 1
            brace_close = _match_brace(text, brace_open)
            if brace_close is None:
                warnings.append(f"{fname}:{_line_of(text, m.start())}: unclosed div attribute block")
                continue
            content_start = text.find("\n", brace_close)
            content_start = len(text) if content_start == -1 else content_start + 1
            stack.append({
                "attr_open": brace_open,
                "attr_close": brace_close,
                "attrs": parse_attrs(text[brace_open + 1:brace_close]),
                "start": m.start(),
                "content_start": content_start,
            })
        else:
            # Closing fence: rest of line must be blank
            if text[m.end():line_end].strip():
                continue
            if not stack:
                continue
            d = stack.pop()
            d["content_end"] = m.start()
            d["end"] = line_end
            divs.append(d)
    while stack:
        d = stack.pop()
        warnings.append(f"{fname}:{_line_of(text, d['start'])}: div never closed; closed at EOF")
        d["content_end"] = len(text)
        d["end"] = len(text)
        divs.append(d)
    divs.sort(key=lambda d: d["start"])
    return divs


def _find_spans(text: str, warnings: list, fname: str):
    """Find bracketed spans `[body]{attrs}` (multi-line, nested brackets)."""
    spans = []
    i = 0
    n = len(text)
    while True:
        j = text.find("]{", i)
        if j == -1:
            break
        # Match backward for the opening '['
        depth = 1
        k = j - 1
        while k >= 0 and depth > 0:
            c = text[k]
            if c == "]":
                depth += 1
            elif c == "[":
                depth -= 1
            k -= 1
        if depth != 0:
            i = j + 2
            continue
        start = k + 1
        body = text[start + 1:j]
        if body.startswith("[") and body.endswith("]"):
            # Looks like an annotated wiki link `[[x]]{...}` — not canonical.
            warnings.append(f"{fname}:{_line_of(text, start)}: attributes on wiki link ignored")
            i = j + 2
            continue
        brace_close = _match_brace(text, j + 1)
        if brace_close is None:
            i = j + 2
            continue
        attrs = parse_attrs(text[j + 2:brace_close])
        spans.append({
            "start": start,
            "body_start": start + 1,
            "body_end": j,
            "attr_open": j + 1,
            "attr_close": brace_close,
            "end": brace_close + 1,
            "body": body,
            "attrs": attrs,
        })
        i = brace_close + 1
    return spans


WIKI_RE = re.compile(r"\[\[([^\]|\n]+)(?:\|([^\]\n]+))?\]\]")


# ----------------------------------------------------------------------
# Loom
# ----------------------------------------------------------------------

class Loom:
    """A Loomic knowledge graph extracted from Markdown files."""

    def __init__(self, name: str = "loom"):
        self.name = name
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []
        self.warnings: list[str] = []
        self._as_of: date | None = None
        self._anon_counter = 0

    # -- construction ---------------------------------------------------

    @classmethod
    def from_paths(cls, paths, name: str = "loom") -> "Loom":
        """Build a Loom from files and/or directories (recursive *.md)."""
        loom = cls(name=name)
        for p in paths:
            p = Path(p)
            if p.is_dir():
                for f in sorted(p.rglob("*.md")):
                    loom.add_file(f)
            elif p.exists():
                loom.add_file(p)
            else:
                loom.warnings.append(f"path not found: {p}")
        loom._derive()
        return loom

    def add_file(self, path) -> "Loom":
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        self.add_text(text, filename=str(path))
        return self

    def add_text(self, text: str, filename: str = "inline.md") -> "Loom":
        """Parse a Markdown string into the loom (usable for simulations)."""
        self._parse_document(text, filename)
        self._derive()
        return self

    # -- node/edge helpers ----------------------------------------------

    def _ensure_node(self, node_id: str, ntype: str = "unknown", stub: bool = True, **extra):
        node = self.nodes.get(node_id)
        if node is None:
            node = {
                "id": node_id, "type": ntype, "stub": stub,
                "attrs": {}, "files": [], "derived": {},
            }
            self.nodes[node_id] = node
        else:
            if node.get("stub") and not stub:
                node["stub"] = False
                node["type"] = ntype
            elif node["type"] == "unknown" and ntype != "unknown":
                node["type"] = ntype
        for k, v in extra.items():
            node.setdefault(k, v)
        return node

    def _add_edge(self, src: str, dst: str, kind: str, qualifier: str = "unspecified",
                  asserted=None, provenance: str = ""):
        if src == dst:
            return
        self.edges.append({
            "src": src, "dst": dst, "kind": kind,
            "qualifier": qualifier, "asserted": asserted, "provenance": provenance,
        })
        self._ensure_node(dst)

    def _next_anon(self, fingerprint: str) -> str:
        return f"anon-{fingerprint}"

    # -- document parsing -------------------------------------------------

    def _parse_document(self, raw: str, fname: str):
        fm, text = _split_frontmatter(raw)
        text = _mask_code(text)

        loomic_fm = fm.get("loomic", {}) if isinstance(fm, dict) else {}
        defaults = {
            "asserted": str(loomic_fm.get("asserted") or fm.get("date") or "") or None,
            "source": loomic_fm.get("source"),
            "loom": loomic_fm.get("loom"),
        }
        if defaults["loom"] and self.name == "loom":
            self.name = str(defaults["loom"])

        # Document node
        doc_id = _slug(Path(fname).stem)
        doc = self._ensure_node(doc_id, "document", stub=False)
        doc["files"].append(fname)
        doc["attrs"].update({k: str(v) for k, v in fm.items()
                             if isinstance(v, (str, int, float))})
        if defaults["asserted"]:
            doc["attrs"].setdefault("asserted", defaults["asserted"])

        divs = _find_divs(text, self.warnings, fname)

        # Mask div attribute blocks before span scanning
        span_text = text
        for d in divs:
            span_text = _mask_region(span_text, d["attr_open"], d["attr_close"] + 1)
        spans = _find_spans(span_text, self.warnings, fname)

        # Region table for containment: (start, end, node_id)
        regions = []

        def make_node(attrs: dict, anchor_text: str, offset: int, kind: str):
            classes = [c for c in attrs["classes"]]
            kv = dict(attrs["kv"])
            ref_only = attrs["id"] is None and not classes and set(kv) <= {"ref"}
            if ref_only:
                return None  # mention handled by caller
            node_id = attrs["id"]
            fp = _fingerprint(anchor_text) if anchor_text else _fingerprint(json.dumps(kv, sort_keys=True))
            if node_id is None:
                node_id = self._next_anon(fp)
                self.warnings.append(
                    f"{fname}:{_line_of(text, offset)}: anonymous node ({node_id}); cannot be referenced")
            elif node_id in self.nodes and not self.nodes[node_id].get("stub") \
                    and self.nodes[node_id]["type"] != "unknown" \
                    and fname not in self.nodes[node_id]["files"]:
                self.warnings.append(f"{fname}: duplicate id '{node_id}' (also in {self.nodes[node_id]['files']})")

            ntype = classes[0] if classes else "unknown"
            if classes and ntype not in NODE_TYPES:
                self.warnings.append(f"{fname}:{_line_of(text, offset)}: unknown node type '.{ntype}'")
            if not classes and "ref" not in kv:
                self.warnings.append(f"{fname}:{_line_of(text, offset)}: node '{node_id}' has no .type class")

            node = self._ensure_node(node_id, ntype, stub=False)
            node["type"] = ntype if classes else node["type"]
            if fname not in node["files"]:
                node["files"].append(fname)
            node["anchor_kind"] = kind
            node["anchor_fingerprint"] = fp
            preview = re.sub(r"\s+", " ", anchor_text).strip()
            node["label"] = (preview[:120] + "…") if len(preview) > 120 else preview
            node["line"] = _line_of(text, offset)

            # Split kv into edges and attributes
            asserted = kv.get("asserted") or defaults["asserted"]
            if asserted:
                node["attrs"].setdefault("asserted", str(asserted))
            for key, val in kv.items():
                base = EDGE_KEY_ALIASES.get(key, key)
                if base in EDGE_KEYS:
                    for target in str(val).split(","):
                        target = target.strip()
                        if not target:
                            continue
                        qual = "unspecified"
                        if "@" in target:
                            target, qual = target.rsplit("@", 1)
                            if qual not in DERIVATION_QUALIFIERS:
                                self.warnings.append(
                                    f"{fname}: unknown qualifier '@{qual}' on {node_id}->{target}")
                        self._add_edge(node_id, target, base, qual,
                                       asserted=str(asserted) if asserted else None,
                                       provenance=fname)
                else:
                    node["attrs"][key] = str(val)

            # Default source edge from frontmatter
            if defaults["source"] and "source" not in kv and node_id != defaults["source"] \
                    and ntype not in ("document",):
                self._add_edge(node_id, str(defaults["source"]), "source",
                               asserted=str(asserted) if asserted else None,
                               provenance=fname + " (frontmatter default)")
            return node_id

        # Divs first (outer to inner ordering not guaranteed; sort by start)
        div_nodes = []
        for d in divs:
            body = text[d["content_start"]:d["content_end"]]
            nid = make_node(d["attrs"], body, d["start"], "div")
            if nid:
                regions.append((d["content_start"], d["content_end"], nid))
                div_nodes.append((d, nid))

        for s in spans:
            attrs = s["attrs"]
            kv = attrs["kv"]
            if attrs["id"] is None and not attrs["classes"] and set(kv) <= {"ref"} and "ref" in kv:
                # Pure mention: [text]{ref=id}
                container = self._container_at(regions, s["start"], doc_id)
                target = kv["ref"].strip()
                self._add_edge(container, target, "ref", provenance=fname)
                self._ensure_node(target, "concept", stub=True)
                continue
            nid = make_node(attrs, s["body"], s["start"], "span")
            if nid:
                regions.append((s["body_start"], s["body_end"], nid))

        # Containment: innermost region -> container attribute / part_of for divs
        regions.sort(key=lambda r: (r[0], -(r[1] - r[0])))
        for start, end, nid in regions:
            container = self._container_at(
                [r for r in regions if r[2] != nid], start, doc_id, end=end)
            node = self.nodes[nid]
            node["container"] = container
            if node.get("anchor_kind") == "div" and container != doc_id:
                existing = any(e for e in self.edges
                               if e["src"] == nid and e["kind"] == "part_of")
                if not existing:
                    self._add_edge(nid, container, "part_of", provenance=fname + " (nesting)")

        # Wiki links -> mention edges (mask span attr blocks first)
        wiki_text = span_text
        for s in spans:
            wiki_text = _mask_region(wiki_text, s["attr_open"], s["attr_close"] + 1)
        for m in WIKI_RE.finditer(wiki_text):
            target_name = m.group(1).strip()
            target = _slug(target_name)
            self._ensure_node(target, "concept", stub=True)["attrs"].setdefault("title", target_name)
            container = self._container_at(regions, m.start(), doc_id)
            self._add_edge(container, target, "ref", provenance=fname)

    @staticmethod
    def _container_at(regions, offset, default, end=None):
        best = None
        for start, rend, nid in regions:
            if start <= offset and (rend >= (end or offset)):
                if best is None or (rend - start) < (best[1] - best[0]):
                    best = (start, rend, nid)
        return best[2] if best else default

    # -- derived state ----------------------------------------------------

    def _visible(self, node_id: str) -> bool:
        if self._as_of is None:
            return True
        node = self.nodes.get(node_id)
        if node is None:
            return False
        a = _parse_date(node["attrs"].get("asserted"))
        return a is None or a <= self._as_of

    def _visible_edges(self):
        return [e for e in self.edges
                if self._visible(e["src"]) and self._visible(e["dst"])]

    def _derive(self):
        for node in self.nodes.values():
            node["derived"] = {}
        edges = self._visible_edges()

        # resolves -> resolved; outdates -> outdated; supersedes -> superseded
        for e in edges:
            dst = self.nodes.get(e["dst"])
            if dst is None:
                continue
            when = e["asserted"] or self.nodes[e["src"]]["attrs"].get("asserted")
            if e["kind"] == "resolves":
                dst["derived"]["status"] = "resolved"
                dst["derived"]["resolved_by"] = e["src"]
                dst["derived"]["resolved"] = when
            elif e["kind"] == "outdates":
                dst["derived"]["temporal"] = "outdated"
                dst["derived"]["outdated_by"] = e["src"]
                dst["derived"]["outdated"] = when
            elif e["kind"] == "supersedes":
                dst["derived"]["temporal"] = "superseded"
                dst["derived"]["superseded_by"] = e["src"]

        # future_binding firing: resolved directly, or via trigger.node
        for node in self.nodes.values():
            if node["type"] != "future_binding" or not self._visible(node["id"]):
                continue
            d = node["derived"]
            if d.get("status") == "resolved":
                d["status"] = "fired"
                d["fired_by"] = d.pop("resolved_by", None)
                d["fired"] = d.pop("resolved", None)
                continue
            trig = node["attrs"].get("trigger.node")
            if trig:
                t = self.nodes.get(trig)
                if t and t["derived"].get("status") == "resolved":
                    d["status"] = "fired"
                    d["fired_by"] = t["derived"].get("resolved_by")
                    d["fired"] = t["derived"].get("resolved")

        # effective status
        for node in self.nodes.values():
            declared = node["attrs"].get("status")
            node["derived"].setdefault("status", declared or None)

        # taint propagation
        incoming = {}
        for e in edges:
            if e["kind"] in TAINT_PROPAGATION_KINDS:
                incoming.setdefault(e["dst"], []).append(e["src"])
        for e in edges:
            if e["kind"] not in TAINT_EVENT_KINDS:
                continue
            cause = f"{e['src']} {e['kind']} {e['dst']}" + (f" ({e['asserted']})" if e["asserted"] else "")
            seen = set()
            frontier = list(incoming.get(e["dst"], []))
            while frontier:
                z = frontier.pop()
                if z in seen or z == e["src"]:
                    continue
                seen.add(z)
                node = self.nodes.get(z)
                if node is not None:
                    node["derived"].setdefault("review", "needed")
                    node["derived"].setdefault("review_causes", []).append(cause)
                frontier.extend(incoming.get(z, []))

    # -- queries -----------------------------------------------------------

    def node(self, node_id: str) -> dict:
        return self.nodes[node_id]

    def by_type(self, ntype: str) -> list[dict]:
        return [n for n in self.nodes.values()
                if n["type"] == ntype and self._visible(n["id"])]

    def unknowledge(self, status: str | None = None) -> list[dict]:
        out = self.by_type("unknowledge")
        if status:
            out = [n for n in out if n["derived"].get("status") == status]
        return out

    def frontiers(self) -> list[dict]:
        return self.by_type("frontier")

    def pendex(self) -> list[dict]:
        """The pending index: all visible nodes with effective status 'pending'."""
        return [n for n in self.nodes.values()
                if self._visible(n["id"]) and n["derived"].get("status") == "pending"]

    def taints(self) -> list[dict]:
        return [n for n in self.nodes.values()
                if self._visible(n["id"]) and n["derived"].get("review") == "needed"]

    def edges_of(self, node_id: str, direction: str = "both") -> list[dict]:
        out = []
        for e in self._visible_edges():
            if direction in ("out", "both") and e["src"] == node_id:
                out.append(e)
            elif direction in ("in", "both") and e["dst"] == node_id:
                out.append(e)
        return out

    def as_of(self, when) -> "Loom":
        """Return a time-scoped view of the loom at the given date."""
        view = copy.deepcopy(self)
        view._as_of = _parse_date(when)
        view._derive()
        return view

    # -- validation ----------------------------------------------------------

    def validate(self) -> list[str]:
        msgs = list(self.warnings)
        for e in self.edges:
            dst = self.nodes.get(e["dst"])
            if dst is None or (dst.get("stub") and dst["type"] == "unknown"):
                msgs.append(f"dangling reference: {e['src']} -{e['kind']}-> {e['dst']}")
        for n in self.nodes.values():
            if n["type"] == "unknown" and not n.get("stub"):
                msgs.append(f"node '{n['id']}' has no recognized type")
        return msgs

    # -- exports ---------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "loom": self.name,
            "loomic_version": __version__,
            "as_of": str(self._as_of) if self._as_of else None,
            "nodes": [self._export_node(n) for n in self.nodes.values()
                      if self._visible(n["id"])],
            "edges": self._visible_edges(),
            "warnings": self.warnings,
        }

    @staticmethod
    def _export_node(n: dict) -> dict:
        out = {k: v for k, v in n.items() if k != "derived"}
        out["derived"] = n["derived"]
        return out

    def to_json(self, path=None, **kwargs) -> str:
        s = json.dumps(self.to_dict(), indent=2, default=str, **kwargs)
        if path:
            Path(path).write_text(s, encoding="utf-8")
        return s

    def to_networkx(self):
        import networkx as nx
        g = nx.MultiDiGraph(name=self.name)
        for n in self.nodes.values():
            if not self._visible(n["id"]):
                continue
            attrs = {"type": n["type"], "label": n.get("label", n["id"]),
                     "stub": str(n.get("stub", False))}
            attrs.update({f"attr_{k}": str(v) for k, v in n["attrs"].items()})
            attrs.update({f"derived_{k}": str(v) for k, v in n["derived"].items()})
            g.add_node(n["id"], **attrs)
        for e in self._visible_edges():
            g.add_edge(e["src"], e["dst"], kind=e["kind"],
                       qualifier=e["qualifier"], asserted=str(e["asserted"] or ""))
        return g

    def to_graphml(self, path):
        import networkx as nx
        nx.write_graphml(self.to_networkx(), str(path))
        return path

    TYPE_COLORS = {
        "claim": "#e74c3c", "historical_claim": "#c0392b",
        "unknowledge": "#9b59b6", "frontier": "#8e44ad",
        "future_binding": "#f39c12", "resolution": "#27ae60",
        "observation": "#95a5a6", "experimental_result": "#16a085",
        "synthesis": "#3498db", "interpretation": "#2980b9",
        "hypothesis": "#e67e22", "problem": "#d35400",
        "context": "#7f8c8d", "concept": "#bdc3c7",
        "person": "#f1c40f", "document": "#ecf0f1",
    }

    def to_html(self, path="loom.html", include_documents=False,
                include_stubs=False, height="800px"):
        """Interactive draggable/zoomable graph (self-contained HTML, pyvis)."""
        from pyvis.network import Network
        net = Network(height=height, width="100%", directed=True,
                      cdn_resources="in_line", select_menu=True)
        included = set()
        for n in self.nodes.values():
            if not self._visible(n["id"]):
                continue
            if n["type"] == "document" and not include_documents:
                continue
            if n.get("stub") and not include_stubs:
                continue
            included.add(n["id"])
            d = n["derived"]
            tip = f"{n['type']}: {n.get('label', '')}"
            for k, v in {**n["attrs"], **{f"derived.{k}": v for k, v in d.items()}}.items():
                tip += f"\n{k} = {v}"
            border = "#e74c3c" if d.get("review") == "needed" else None
            shape = {"frontier": "hexagon", "unknowledge": "diamond",
                     "future_binding": "star", "resolution": "triangle"}.get(n["type"], "dot")
            net.add_node(n["id"], label=n["id"], title=tip, shape=shape,
                         color=self.TYPE_COLORS.get(n["type"], "#bdc3c7"),
                         borderWidth=3 if border else 1)
        for e in self._visible_edges():
            if e["src"] in included and e["dst"] in included:
                lbl = e["kind"] + (f"@{e['qualifier']}" if e["qualifier"] != "unspecified" else "")
                net.add_edge(e["src"], e["dst"], label=lbl, arrows="to",
                             color="#cccccc", font={"size": 8, "color": "#888888"})
        net.write_html(str(path), open_browser=False, notebook=False)
        return path

    def derivation_dag(self, kinds=("parents", "depends", "resolves",
                                    "outdates", "refines", "part_of")):
        """Directed graph of derivation edges, ancestors -> descendants.

        Suitable for layered/hierarchical layout (roots at top).
        """
        import networkx as nx
        g = nx.DiGraph(name=self.name)
        for e in self._visible_edges():
            if e["kind"] not in kinds:
                continue
            for nid in (e["src"], e["dst"]):
                n = self.nodes.get(nid)
                if n is None or n["type"] == "document" or n.get("stub"):
                    break
            else:
                # edges like parents point child->parent; flip so ancestry flows down
                g.add_edge(e["dst"], e["src"], kind=e["kind"], qualifier=e["qualifier"])
        for nid in g.nodes:
            n = self.nodes[nid]
            g.nodes[nid]["type"] = n["type"]
            g.nodes[nid]["label"] = n.get("label", nid)
        return g

    def nodes_df(self):
        import pandas as pd
        rows = []
        for n in self.nodes.values():
            if not self._visible(n["id"]):
                continue
            rows.append({
                "id": n["id"], "type": n["type"], "stub": n.get("stub", False),
                "status": n["derived"].get("status"),
                "temporal": n["derived"].get("temporal"),
                "review": n["derived"].get("review"),
                "asserted": n["attrs"].get("asserted"),
                "label": n.get("label", ""),
            })
        return pd.DataFrame(rows)

    def edges_df(self):
        import pandas as pd
        return pd.DataFrame(self._visible_edges())

    # -- reporting -----------------------------------------------------------

    def report(self):
        vis = [n for n in self.nodes.values() if self._visible(n["id"])]
        real = [n for n in vis if not n.get("stub")]
        stubs = [n for n in vis if n.get("stub")]
        print(f"Loom: {self.name}" + (f"  (as of {self._as_of})" if self._as_of else ""))
        print(f"  {len(real)} nodes, {len(stubs)} concept stubs, {len(self._visible_edges())} edges")
        by_type = {}
        for n in real:
            by_type[n["type"]] = by_type.get(n["type"], 0) + 1
        print("  types: " + ", ".join(f"{t}={c}" for t, c in sorted(by_type.items())))
        open_u = self.unknowledge("open")
        if open_u:
            print(f"\n  Open unknowledge ({len(open_u)}):")
            for n in open_u:
                print(f"    ? {n['id']}: {n.get('label', '')[:90]}")
        resolved = self.unknowledge("resolved")
        if resolved:
            print(f"\n  Resolved unknowledge ({len(resolved)}):")
            for n in resolved:
                d = n["derived"]
                print(f"    * {n['id']} — resolved by {d.get('resolved_by')} ({d.get('resolved')})")
        pend = self.pendex()
        if pend:
            print(f"\n  Pendex — pending future bindings ({len(pend)}):")
            for n in pend:
                print(f"    ~ {n['id']}: {n['attrs'].get('trigger.capability') or n['attrs'].get('trigger.event') or n.get('label','')[:90]}")
        fired = [n for n in self.by_type("future_binding")
                 if n["derived"].get("status") == "fired"]
        if fired:
            print(f"\n  Fired bindings ({len(fired)}):")
            for n in fired:
                print(f"    ! {n['id']} — fired by {n['derived'].get('fired_by')} ({n['derived'].get('fired')})")
        outdated = [n for n in vis if n["derived"].get("temporal") in ("outdated", "superseded")]
        if outdated:
            print(f"\n  Outdated/superseded ({len(outdated)}):")
            for n in outdated:
                d = n["derived"]
                print(f"    x {n['id']} — {d.get('temporal')} by {d.get('outdated_by') or d.get('superseded_by')}")
        taints = self.taints()
        if taints:
            print(f"\n  Review queue — tainted nodes ({len(taints)}):")
            for n in taints:
                print(f"    ! {n['id']} <- {n['derived']['review_causes'][0]}")
        issues = [w for w in self.validate()]
        if issues:
            print(f"\n  Warnings ({len(issues)}):")
            for w in issues[:15]:
                print(f"    - {w}")
            if len(issues) > 15:
                print(f"    … {len(issues) - 15} more")
