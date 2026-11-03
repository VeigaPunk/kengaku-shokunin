#!/usr/bin/env python3
"""Count Gate admits/rejects and Mistakes table rows per lesson file (r64-C3b seat IndexParity)."""
import re, sys, pathlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons")

def sections(text):
    out = {}
    cur = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = buf
            cur = line[3:].strip()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = buf
    return out

def table_rows(lines):
    """Rows of a markdown table: lines starting '| ' minus the header and separator rows."""
    rows = []
    for ln in lines:
        if not ln.startswith("|"):
            continue
        s = ln.strip()
        if re.fullmatch(r"\|[\s:\-\|]+\|", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    # drop header row (first row of each contiguous table) -> handled by caller via 'header' flag
    return rows

for n in (57, 58, 59, 60, 61, 62):
    p = L / f"round-{n}.md"
    text = p.read_text(encoding="utf-8")
    secs = sections(text)
    print(f"===== round-{n}.md  (sha256 {__import__('hashlib').sha256(p.read_bytes()).hexdigest()[:16]}...) =====")
    # Gate section: count admits/rejects by keyword in table cells
    for name, body in secs.items():
        if name.lower().startswith("gate"):
            rows = table_rows(body)
            admits = rejects = 0
            for r in rows:
                joined = " ".join(r).lower()
                if "admit" in joined and "reject" not in joined:
                    admits += 1
                if "reject" in joined:
                    rejects += 1
            print(f"  [Gate] table rows={len(rows)} admits(decision cell)={admits} rejects={rejects}")
            for r in rows:
                if len(r) >= 5:
                    print(f"     row: id={r[0]!r} decision={r[4][:70]!r}")
        if name.lower().startswith("mistakes"):
            rows = table_rows(body)
            # first row of the table is the header
            data = rows[1:] if rows and rows[0][0].lower() == "class" else rows
            classes = [r[0].split(" —")[0].split(" -")[0].strip() for r in data]
            print(f"  [{name[:60]}] data rows={len(data)}")
            for c in classes:
                print(f"     class: {c}")
    # verdict-ish lines
    verdicts = []
    for i, ln in enumerate(text.splitlines(), 1):
        if re.search(r"PREDICATE|predicate-(met|FAILED|failed)|score held at|honest fail|C1: CLOSED|CLOSED —|admitted", ln):
            verdicts.append((i, ln.strip()[:190]))
    print("  [verdict lines]")
    for i, ln in verdicts:
        print(f"     L{i}: {ln}")
    print()
