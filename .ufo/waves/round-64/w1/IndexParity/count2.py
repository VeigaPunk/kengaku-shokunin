#!/usr/bin/env python3
"""Independent cross-check of gate/mistakes/verdict facts for lessons round-57..62."""
import re, pathlib, hashlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons")

def split_sections(text):
    secs = []
    cur = ("(preamble)", [])
    for line in text.splitlines():
        if line.startswith("## "):
            secs.append((cur[0], cur[1]))
            cur = (line[3:].strip(), [])
        else:
            cur[1].append(line)
    secs.append((cur[0], cur[1]))
    return secs

def table_data_rows(body):
    """Data rows of any markdown tables in body, header/separator excluded."""
    out = []
    for ln in body:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        out.append(cells)
    # group into contiguous tables; drop the first row of each table (header)
    tables, cur = [], []
    prev_is_tbl = False
    for ln in body:
        s = ln.strip()
        is_tbl = s.startswith("|")
        if is_tbl:
            cur.append(s)
        else:
            if cur:
                tables.append(cur); cur = []
    if cur:
        tables.append(cur)
    data = []
    for t in tables:
        rows = []
        for s in t:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append(cells)
        if rows:
            data.append(rows[1:])
    return data

for n in (57, 58, 59, 60, 61, 62):
    p = L / f"round-{n}.md"
    b = p.read_bytes()
    t = b.decode("utf-8")
    print(f"##### round-{n}.md  sha256={hashlib.sha256(b).hexdigest()}")
    secs = split_sections(t)
    # mistake rows, section by section
    m_total = 0
    for name, body in secs:
        if name.lower().startswith("mistakes"):
            rows = [r for tbl in table_data_rows(body) for r in tbl]
            print(f"  Mistakes section '{name[:70]}': {len(rows)} data rows")
            for r in rows:
                print(f"     - {r[0].split('—')[0].split('(')[0].strip()[:60]}")
            m_total += len(rows)
    # stray table rows outside any Mistakes section
    stray = 0
    for name, body in secs:
        if name.lower().startswith("mistakes"):
            continue
        rows = [r for tbl in table_data_rows(body) for r in tbl]
        if rows and not name.lower().startswith("gate"):
            stray += len(rows)
            print(f"  [non-Mistakes section '{name[:60]}'] carries {len(rows)} table row(s)")
    print(f"  MISTAKES TOTAL (Mistakes sections) = {m_total}; stray rows outside = {stray}")
    # gate admits/rejects by S-row table
    for name, body in secs:
        if name.lower().startswith("gate"):
            rows = [r for tbl in table_data_rows(body) for r in tbl]
            if rows:
                adm = [r[0] for r in rows if "admit" in " ".join(r).lower()]
                rej = [r[0] for r in rows if "reject" in " ".join(r).lower()]
                print(f"  Gate table: {len(rows)} rows; admits={adm}; rejects={rej}")
            else:
                print("  Gate table: none (prose)")
    # claim verdicts
    for i, ln in enumerate(t.splitlines(), 1):
        if re.search(r"R5[7-9]-C\d|R6[0-2]-C\d", ln) and re.search(r"pass|fail|CLOSED|MISS|met|admit", ln, re.I):
            print(f"  verdict L{i}: {ln.strip()[:170]}")
    print()
