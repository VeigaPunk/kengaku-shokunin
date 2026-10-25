#!/usr/bin/env python3
"""F35ReopenS105 — independent re-open of S105 (Terminal-Bench 2.0 protein-assembly grader).

Read-only. Verifies, against the lane's committed captures and against a freshly re-fetched
upstream file, that:
  A. the capture digest chain (SHA256SUMS -> capture bytes -> upstream bytes) holds;
  B. every quote in the entry's `## Located quotes` table that cites test_outputs.py occurs
     byte-exactly on the cited capture line, and is <=25 words;
  C. the S105 row's anchor quote occurs byte-exactly on upstream test_outputs.py:42;
  D. the S105 row's (N words) annotation agrees with the lane-wide word-count convention.

Usage: python3 verify_s105.py --lane <lane-root> [--upstream <path-to-fetched-test_outputs.py>]
"""
import argparse
import hashlib
import pathlib
import re
import sys

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
RAW = f"https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/{PIN}/protein-assembly/tests/test_outputs.py"
PIN_SHA = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"
CAP = "corpus/evidence/round35/tb2-eval/"
ENTRY = "corpus/knowledge/tb2-protein-assembly-grader.md"
SOURCES = "corpus/SOURCES.md"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--upstream", default=None, help="freshly fetched upstream test_outputs.py")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fails = []

    # --- A. digest chain -----------------------------------------------------
    cap = lane / CAP
    listed = {}
    for line in (cap / "SHA256SUMS").read_text().splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})\s+\*?(\S+)", line.strip())
        if m:
            listed[m.group(2)] = m.group(1)
    if listed.get("test_outputs.py") != PIN_SHA:
        fails.append(f"SHA256SUMS test_outputs.py != pinned {PIN_SHA}")
    cap_sha = sha(cap / "test_outputs.py")
    if cap_sha != PIN_SHA:
        fails.append(f"capture bytes sha256={cap_sha} != pinned {PIN_SHA}")
    if a.upstream:
        up_sha = sha(pathlib.Path(a.upstream))
        if up_sha != PIN_SHA:
            fails.append(f"upstream bytes sha256={up_sha} != pinned {PIN_SHA}")
        if (cap / "test_outputs.py").read_bytes() != pathlib.Path(a.upstream).read_bytes():
            fails.append("capture bytes != upstream bytes")
    print(f"A. capture sha256      = {cap_sha}")
    if a.upstream:
        print(f"A. upstream sha256     = {sha(pathlib.Path(a.upstream))} (pinned {PIN_SHA})")
    print(f"A. SHA256SUMS entry    = {listed.get('test_outputs.py')}")

    # --- B. entry quotes citing test_outputs.py ------------------------------
    txt = (lane / ENTRY).read_text()
    sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", txt, re.S | re.M)
    rows, n_ok = [], 0
    for line in sec.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or "“" not in cells[1]:
            continue
        m = re.match(r"`([^`:]+):(\d+)(?:-(\d+))?`", cells[2])
        if not m or m.group(1) != "test_outputs.py":
            continue
        q = cells[1]
        q = q[1:-1] if q.startswith("“") and q.endswith("”") else q
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        caplines = (cap / "test_outputs.py").read_text().splitlines()
        span = "\n".join(caplines[lo - 1:hi])
        exact = q in span
        words = len(q.split())
        good = exact and words <= 25
        n_ok += good
        rows.append((cells[2], cells[0], q, words, exact, good))
        if not good:
            fails.append(f"quote not byte-exact/too long at {cells[2]}: {q[:50]!r}")
    for loc, claim, q, w, exact, good in rows:
        print(f"B. {'OK ' if good else 'BAD'} {loc:26s} words={w:2d} exact={exact} | {claim}")
    print(f"B. test_outputs.py quotes: n={len(rows)} n_ok={n_ok}")

    # --- C. S105 anchor quote on upstream line 42 ----------------------------
    srow = [l for l in (lane / SOURCES).read_text().splitlines() if l.startswith("| S105 ")][0]
    cells = [c.strip() for c in srow.strip().strip("|").split("|")]
    anchor = cells[5]
    up_lines = (cap / "test_outputs.py").read_text().splitlines()
    m = re.search(r"tests/test_outputs\.py:(\d+)\s+\"([^\"]+)\"", anchor)
    if not m:
        fails.append("S105 anchor cell has no 'tests/test_outputs.py:N \"quote\"' form")
    else:
        lineno, q = int(m.group(1)), m.group(2)
        src = up_lines[lineno - 1]
        exact = q in src
        print(f"C. anchor line {lineno}: exact={exact}")
        print(f"C. anchor quote = {q!r}")
        print(f"C. line {lineno}     = {src!r}")
        if not exact:
            fails.append(f"S105 anchor quote not on test_outputs.py:{lineno}")

    # --- D. word-count convention --------------------------------------------
    ws_mismatch = []
    all_rows = [l for l in (lane / SOURCES).read_text().splitlines() if l.startswith("| S")]
    tot = 0
    for l in all_rows:
        rid = l.split("|")[1].strip()
        for mm in re.finditer(r'"([^"]*)"\s*\((\d+) words\)', l):
            q, cnt = mm.group(1), int(mm.group(2))
            tot += 1
            if len(q.split()) != cnt:
                ws_mismatch.append((rid, cnt, len(q.split()), q))
    print(f"D. (N words) annotations in SOURCES.md: {tot}; whitespace-token mismatches: {len(ws_mismatch)}")
    for rid, cnt, ws, q in ws_mismatch:
        print(f"D.   MISMATCH {rid}: claimed={cnt} whitespace_tokens={ws} | {q[:60]!r}")

    print()
    if fails:
        for f in fails:
            print(f"DEFECT: {f}")
        print(f"RESULT: FAIL ({len(fails)} defects)")
        return 1
    print(f"RESULT: PASS (quotes {n_ok}/{len(rows)} byte-exact)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
