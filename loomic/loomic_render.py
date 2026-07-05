"""
loomic_render.py — Loomic 0.2 rendering filter.

Renders Loomic-annotated Markdown into a single self-contained HTML reader:
- clean, readable prose (annotations stripped from view)
- annotated spans get a subtle type-colored underline
- clicking a span opens a popup card: node type, attributes, derived state
- the card lists the node's edges; each edge is clickable, so the whole
  graph can be browsed as popups from within the text
- "Show in text" jumps to a node's anchor in whichever document holds it
- a toggle switches between annotated view and pure clean prose

Usage (library, no CLI):
    from loomic_render import render_reader
    render_reader(
        doc_paths=["SAIR/SAIR UCR 2026/presentations-loomic"],
        graph_paths=["SAIR/SAIR UCR 2026/presentations-loomic",
                     "SAIR/SAIR UCR 2026/people",
                     "SAIR/SAIR UCR 2026/concepts"],
        out_path="loom-reader.html")
"""

from __future__ import annotations

import html as _htmlmod
import json
import re
from pathlib import Path

from loomic import (
    Loom, _split_frontmatter, _mask_code, _find_divs, _find_spans,
    _slug, WIKI_RE,
)

CARD_TYPES = {
    "unknowledge", "frontier", "future_binding", "resolution", "problem",
    "hypothesis", "interpretation", "evidence_gap",
}

TYPE_COLORS = {
    "claim": "#D85A30", "historical_claim": "#993C1D",
    "unknowledge": "#7F77DD", "frontier": "#534AB7",
    "future_binding": "#EF9F27", "resolution": "#639922",
    "observation": "#888780", "experimental_result": "#1D9E75",
    "synthesis": "#378ADD", "interpretation": "#185FA5",
    "hypothesis": "#BA7517", "problem": "#993C1D",
    "context": "#5F5E5A", "concept": "#B4B2A9",
    "person": "#BA7517", "document": "#B4B2A9", "unknown": "#B4B2A9",
}


def _esc(s: str) -> str:
    return _htmlmod.escape(s, quote=False)


def _span_open(node_id: str, ntype: str, extra_class: str = "") -> str:
    return f'<span class="lnode {extra_class} t-{ntype}" data-id="{node_id}">'


def _render_body(text: str, fname: str) -> str:
    """Transform one Loomic markdown body into reader HTML."""
    fm, masked = _split_frontmatter(text)
    code_masked = _mask_code(masked)
    warnings: list = []
    divs = _find_divs(code_masked, warnings, fname)
    span_text = code_masked
    for d in divs:
        span_text = span_text[:d["attr_open"]] + " " * (d["attr_close"] + 1 - d["attr_open"]) + span_text[d["attr_close"] + 1:]
    spans = _find_spans(span_text, warnings, fname)

    edits = []  # (start, end, replacement_html)

    for d in divs:
        a = d["attrs"]
        ntype = a["classes"][0] if a["classes"] else "unknown"
        nid = a["id"] or ""
        if ntype in CARD_TYPES:
            open_html = (f'\n<div class="lcard t-{ntype}" data-block="{nid}">\n'
                         f'<div class="lhead lnode t-{ntype}" data-id="{nid}">'
                         f'<span class="chip t-{ntype}">{_esc(ntype)}</span> {_esc(nid)}</div>\n')
        else:
            tx = " transcript" if nid.endswith("transcript") else ""
            open_html = (f'\n<div class="lwrap{tx} t-{ntype}" data-block="{nid}">\n'
                         f'<div class="lhead lnode t-{ntype}" data-id="{nid}">'
                         f'<span class="chip t-{ntype}">{_esc(ntype)}</span> {_esc(nid)}</div>\n')
        edits.append((d["start"], d["content_start"], open_html))
        edits.append((d["content_end"], d["end"], "\n</div>\n"))

    for s in spans:
        a = s["attrs"]
        kv = a["kv"]
        body = _esc(s["body"])
        if a["id"] is None and not a["classes"] and set(kv) <= {"ref"} and "ref" in kv:
            nid, ntype, cls = kv["ref"].strip(), "concept", "lref"
        else:
            nid = a["id"] or ""
            ntype = a["classes"][0] if a["classes"] else "unknown"
            cls = ""
        open_tag = _span_open(nid, ntype, cls)
        body = re.sub(r"\n[ \t]*\n", "</span>\n\n" + open_tag, body)
        edits.append((s["start"], s["end"], open_tag + body + "</span>"))

    edits.sort(key=lambda e: e[0])
    out, pos = [], 0
    for start, end, rep in edits:
        if start < pos:
            continue
        out.append(_esc(text[pos:start]))
        out.append(rep)
        pos = end
    out.append(_esc(text[pos:]))
    html = "".join(out)

    def _wiki(m):
        target = _slug(m.group(1).strip())
        label = (m.group(2) or m.group(1)).strip()
        return f'<span class="lnode lwiki t-concept" data-id="{target}">{_esc(label)}</span>'
    html = WIKI_RE.sub(_wiki, html)

    # paragraphize
    out_lines, buf = [], []

    def flush():
        if buf:
            out_lines.append("<p>" + " ".join(buf) + "</p>")
            buf.clear()

    for line in html.split("\n"):
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith("<div") or s.startswith("</div"):
            flush()
            out_lines.append(s)
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            flush()
            lvl = min(len(m.group(1)) + 1, 5)
            out_lines.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
            continue
        buf.append(s)
    flush()
    return "\n".join(out_lines), fm


def render_reader(doc_paths, graph_paths=None, out_path="loom-reader.html",
                  title="Loom reader"):
    """Render Loomic documents into a self-contained interactive HTML reader."""
    graph_paths = graph_paths or doc_paths
    loom = Loom.from_paths(list(graph_paths))

    files = []
    for p in doc_paths:
        p = Path(p)
        if p.is_dir():
            files.extend(sorted(f for f in p.rglob("*.md")
                                if f.name.lower() != "readme.md"))
        elif p.exists():
            files.append(p)

    sections, nav_items = [], []
    doc_of_node = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        body_html, fm = _render_body(text, str(f))
        doc_id = _slug(f.stem)
        doc_title = str(fm.get("title", f.stem))
        speaker = str(fm.get("speaker", "") or "")
        date = str(fm.get("date", "") or "")
        url = str(fm.get("youtube_url", "") or "")
        meta_bits = [b for b in (speaker, date) if b]
        meta = " · ".join(meta_bits)
        link = f' · <a href="{_htmlmod.escape(url)}" target="_blank">recording</a>' if url else ""
        sections.append(
            f'<section class="doc" id="doc-{doc_id}">'
            f"<h2>{_esc(doc_title)}</h2>"
            f'<div class="docmeta">{_esc(meta)}{link}</div>'
            f"{body_html}</section>")
        nav_items.append((doc_id, speaker or doc_title, doc_title))
        for nid, node in loom.nodes.items():
            if str(f) in node.get("files", []):
                doc_of_node.setdefault(nid, doc_id)

    nodes_js = {}
    for nid, n in loom.nodes.items():
        nodes_js[nid] = {
            "type": n["type"], "label": n.get("label", "")[:200],
            "attrs": n.get("attrs", {}), "derived": n.get("derived", {}),
            "stub": bool(n.get("stub")), "doc": doc_of_node.get(nid),
        }
    edges_js = [{"src": e["src"], "dst": e["dst"], "kind": e["kind"],
                 "q": e["qualifier"]} for e in loom.edges]

    nav_html = "".join(
        f'<a class="doc-link" data-doc="{d}" title="{_htmlmod.escape(full)}">{_esc(short)}</a>'
        for d, short, full in nav_items)

    type_css = "\n".join(
        f".t-{t}{{--c:{c}}}" for t, c in TYPE_COLORS.items())

    real = [n for n in loom.nodes.values() if not n.get("stub")]
    stats = f"{len(real)} nodes · {len(loom.edges)} edges · {len(files)} documents"

    page = HTML_TEMPLATE
    page = page.replace("__TITLE__", _esc(title))
    page = page.replace("__STATS__", stats)
    page = page.replace("__TYPECSS__", type_css)
    page = page.replace("__NAV__", nav_html)
    page = page.replace("__SECTIONS__", "\n".join(sections))
    page = page.replace("__NODES__", json.dumps(nodes_js, ensure_ascii=False))
    page = page.replace("__EDGES__", json.dumps(edges_js, ensure_ascii=False))
    Path(out_path).write_text(page, encoding="utf-8")
    return out_path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
body{font:16px/1.7 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif;margin:0;color:#2c2c2a;background:#faf9f5}
.layout{display:flex}
nav{width:280px;flex:none;border-right:1px solid #e5e2d9;padding:18px 14px;box-sizing:border-box;position:sticky;top:0;height:100vh;overflow:auto;background:#f4f2ea}
nav h1{font-size:17px;margin:0 0 2px}
nav .sub{font-size:12px;color:#8a887f;margin-bottom:12px}
nav .toggle{font-size:13px;color:#555;display:flex;align-items:center;gap:6px;margin:10px 0 14px;cursor:pointer;user-select:none}
a.doc-link{display:block;padding:6px 9px;border-radius:7px;font-size:13px;color:#454540;cursor:pointer}
a.doc-link.active{background:#e7e3d4;font-weight:600}
main{flex:1;min-width:0;max-width:840px;padding:30px 46px 90px;box-sizing:border-box}
section.doc{display:none}
section.doc.active{display:block}
h2{font-size:22px;margin:6px 0 6px}
h3{font-size:17px;margin:26px 0 8px}
.docmeta{color:#8a887f;font-size:13px;margin-bottom:14px}
.docmeta a{color:#8a887f}
p{margin:0 0 14px}
.lnode{border-bottom:2px dotted var(--c,#999);cursor:pointer;transition:background .15s}
.lnode:hover{background:color-mix(in srgb,var(--c,#999) 14%,transparent)}
.lwiki{border-bottom-style:dashed;border-bottom-width:1px;opacity:.9}
.lwrap{border-left:3px solid color-mix(in srgb,var(--c,#999) 45%,transparent);padding:2px 0 2px 16px;margin:14px 0}
.lcard{border:1px solid color-mix(in srgb,var(--c,#999) 45%,transparent);border-left:4px solid var(--c,#999);border-radius:10px;padding:10px 16px 2px;margin:16px 0;background:#fff}
.lhead{font-size:12px;color:#77756c;margin:2px 0 8px;border-bottom:none;font-family:ui-monospace,Menlo,monospace}
.lhead:hover{background:#f0eee6}
.chip{display:inline-block;font-size:11px;padding:1px 8px;border-radius:99px;background:color-mix(in srgb,var(--c,#999) 16%,transparent);color:var(--c,#555);font-weight:600;font-family:-apple-system,sans-serif;margin-right:6px}
body.clean .lnode{border-bottom:none;cursor:text}
body.clean .lnode:hover{background:none}
body.clean .lhead{display:none}
body.clean .lcard{background:none;border-color:#e5e2d9;border-left-width:1px}
body.clean .lwrap{border-left-color:#eee9dd}
body.notx .transcript{display:none}
body.notx .transcript-h{display:none}
#card{position:fixed;right:22px;top:70px;width:360px;max-height:78vh;overflow:auto;background:#fff;border:1px solid #ddd9cc;border-radius:14px;box-shadow:0 10px 34px rgba(60,55,40,.18);padding:16px 18px;display:none;z-index:50;font-size:13.5px}
#card.open{display:block}
#card h4{margin:0 0 2px;font-size:14px;font-family:ui-monospace,Menlo,monospace;word-break:break-all}
#card .label{color:#66645c;font-size:12.5px;margin:6px 0 10px;line-height:1.5}
#card table{border-collapse:collapse;width:100%;margin:4px 0 10px}
#card td{padding:2px 6px 2px 0;vertical-align:top;font-size:12px;color:#555;border-bottom:1px solid #f0ede2}
#card td:first-child{color:#98958a;white-space:nowrap;font-family:ui-monospace,Menlo,monospace}
#card .sec{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#98958a;margin:12px 0 4px}
.edge{display:block;padding:4px 8px;border-radius:7px;font-size:12.5px;cursor:pointer;color:#39382f}
.edge:hover{background:#f4f1e6}
.edge .kind{color:#98958a;font-family:ui-monospace,Menlo,monospace;font-size:11px}
.edge .q{color:#BA7517;font-size:11px}
#card .bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
#card button{border:none;background:#f0ede2;border-radius:7px;padding:3px 10px;font-size:12px;cursor:pointer;color:#555}
#card button:hover{background:#e5e1d2}
.goto{color:#185FA5;font-size:12px;cursor:pointer}
.flash{animation:flash 1.6s ease-out}
@keyframes flash{0%{background:#ffe9a8}100%{background:transparent}}
.badge{display:inline-block;font-size:11px;padding:1px 8px;border-radius:99px;margin:0 4px 4px 0;font-weight:600}
.b-open{background:#EEEDFE;color:#534AB7}.b-resolved{background:#EAF3DE;color:#3B6D11}
.b-pending{background:#FAEEDA;color:#854F0B}.b-fired{background:#EAF3DE;color:#3B6D11}
.b-review{background:#FCEBEB;color:#A32D2D}.b-outdated{background:#FCEBEB;color:#A32D2D}
__TYPECSS__
</style></head><body>
<div class="layout">
<nav>
<h1>__TITLE__</h1>
<div class="sub">__STATS__</div>
<label class="toggle"><input type="checkbox" id="cleanToggle"> clean prose (hide annotations)</label>
<label class="toggle"><input type="checkbox" id="txToggle"> hide transcripts</label>
__NAV__
</nav>
<main>
__SECTIONS__
</main>
</div>
<div id="card"></div>
<script>
const NODES = __NODES__;
const EDGES = __EDGES__;
const OUT = {}, IN = {};
EDGES.forEach(e => {(OUT[e.src] ||= []).push(e); (IN[e.dst] ||= []).push(e);});
let hist = [];

function esc(s){const d=document.createElement('div');d.textContent=s??'';return d.innerHTML;}

function showDoc(id, scrollTop=true){
  document.querySelectorAll('section.doc').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('a.doc-link').forEach(a=>a.classList.toggle('active', a.dataset.doc===id));
  const sec = document.getElementById('doc-'+id);
  if(sec){sec.classList.add('active'); if(scrollTop) window.scrollTo(0,0);}
}

function gotoText(id){
  const n = NODES[id];
  if(!n || !n.doc) return;
  showDoc(n.doc, false);
  const el = document.querySelector('#doc-'+n.doc+' [data-id="'+CSS.escape(id)+'"]');
  if(el){
    if(el.offsetParent === null && document.body.classList.contains('notx')){
      document.body.classList.remove('notx');
      document.getElementById('txToggle').checked = false;
    }
    el.scrollIntoView({behavior:'smooth', block:'center'});
    el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');}
}

function badges(d){
  let h='';
  if(d.status) h += '<span class="badge b-'+esc(d.status)+'">'+esc(d.status)+'</span>';
  if(d.temporal) h += '<span class="badge b-outdated">'+esc(d.temporal)+(d.outdated_by?' by '+esc(d.outdated_by):'')+'</span>';
  if(d.review) h += '<span class="badge b-review">review needed</span>';
  if(d.resolved_by) h += '<span class="badge b-resolved">resolved by '+esc(d.resolved_by)+'</span>';
  if(d.fired_by) h += '<span class="badge b-fired">fired by '+esc(d.fired_by)+'</span>';
  return h;
}

function edgeRow(other, kind, q, dirOut){
  const arrow = dirOut ? '→' : '←';
  const qs = (q && q !== 'unspecified') ? ' <span class="q">@'+esc(q)+'</span>' : '';
  const t = NODES[other] ? NODES[other].type : '?';
  return '<a class="edge" onclick="openCard(\\''+other.replace(/'/g,"\\\\'")+'\\')">' +
    '<span class="kind">'+esc(kind)+qs+' '+arrow+'</span> ' + esc(other) +
    ' <span class="kind">('+esc(t)+')</span></a>';
}

function openCard(id, push=true){
  const n = NODES[id];
  const card = document.getElementById('card');
  if(!n){card.innerHTML='<div class="bar"><h4>'+esc(id)+'</h4><button onclick="closeCard()">✕</button></div><div class="label">Not in this loom.</div>';card.classList.add('open');return;}
  if(push) hist.push(id);
  let h = '<div class="bar"><span>';
  if(hist.length>1) h += '<button onclick="goBack()">← back</button> ';
  h += '</span><button onclick="closeCard()">✕</button></div>';
  h += '<span class="chip t-'+esc(n.type)+'">'+esc(n.type)+'</span>';
  h += '<h4>'+esc(id)+'</h4>';
  h += badges(n.derived||{});
  if(n.label) h += '<div class="label">'+esc(n.label)+'</div>';
  if(n.doc) h += '<div><span class="goto" onclick="gotoText(\\''+id.replace(/'/g,"\\\\'")+'\\')">↳ show in text</span></div>';
  const attrs = n.attrs||{};
  const keys = Object.keys(attrs).filter(k=>k!=='title');
  if(keys.length){h += '<div class="sec">attributes</div><table>';
    keys.forEach(k=>{h += '<tr><td>'+esc(k)+'</td><td>'+esc(String(attrs[k]))+'</td></tr>';});
    h += '</table>';}
  const outs = OUT[id]||[], ins = IN[id]||[];
  if(outs.length){h += '<div class="sec">outgoing ('+outs.length+')</div>';
    outs.forEach(e=>{h += edgeRow(e.dst, e.kind, e.q, true);});}
  if(ins.length){h += '<div class="sec">incoming ('+ins.length+')</div>';
    ins.forEach(e=>{h += edgeRow(e.src, e.kind, e.q, false);});}
  card.innerHTML = h;
  card.classList.add('open');
}
function goBack(){hist.pop(); const prev = hist[hist.length-1]; if(prev) openCard(prev,false); else closeCard();}
function closeCard(){document.getElementById('card').classList.remove('open'); hist=[];}

document.addEventListener('click', ev=>{
  const t = ev.target.closest('.lnode');
  if(t && !document.body.classList.contains('clean')){
    ev.preventDefault(); hist=[]; openCard(t.dataset.id); return;
  }
  const d = ev.target.closest('a.doc-link');
  if(d){showDoc(d.dataset.doc); closeCard();}
});
document.getElementById('cleanToggle').addEventListener('change', ev=>{
  document.body.classList.toggle('clean', ev.target.checked);
  if(ev.target.checked) closeCard();
});
document.getElementById('txToggle').addEventListener('change', ev=>{
  document.body.classList.toggle('notx', ev.target.checked);
});
document.querySelectorAll('main h2,main h3,main h4').forEach(h=>{
  if(h.textContent.trim().toLowerCase()==='transcript') h.classList.add('transcript-h');
});
document.addEventListener('keydown', ev=>{if(ev.key==='Escape') closeCard();});
showDoc(document.querySelector('a.doc-link').dataset.doc);
</script>
</body></html>
"""
