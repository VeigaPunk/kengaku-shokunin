#!/usr/bin/env python3
"""Robust counts: mistakes rows including single-row tables appended outside a Mistakes section;
gate admits/rejects from prose; claim verdicts."""
import re, pathlib, hashlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons")

def secs_of(text):
    out = []
    cur = ("(preamble)", [])
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((cur[0], cur[1])); cur = (line[3:].strip(), [])
        else:
            cur[1].append(line)
    out.append((cur[0], cur[1]))
    return out

def tables_of(body):
    tables, cur = [], []
    for ln in body:
        if ln.strip().startswith("|"):
            cur.append(ln.strip())
        else:
            if cur: tables.append(cur); cur = []
    if cur: tables.append(cur)
    res = []
    for t in tables:
        rows = []
        for s in t:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append(cells)
        if rows: res.append(rows)
    return res

for n in (57, 58, 59, 60, 61, 62):
    p = L / f"round-{n}.md"
    t = p.read_text(encoding="utf-8")
    print(f"##### round-{n}.md sha256={hashlib.sha256(p.read_bytes()).hexdigest()}")
    for name, body in secs_of(t):
        tabs = tables_of(body)
        if not tabs:
            continue
        for ti, rows in enumerate(tabs):
            hdr = rows[0][0].lower() if rows[0] else ""
            data = rows[1:] if hdr == "class" else rows
            kind = "MISTAKES-TABLE" if name.lower().startswith("mistakes") else f"table-in[{name[:45]}]"
            print(f"  {kind}: rows={len(rows)} data={len(data)} header={rows[0][0][:20]!r}")
            for r in data:
                print(f"     * {r[0][:95]}")
    print()
