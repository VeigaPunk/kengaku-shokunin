#!/usr/bin/env python3
"""Draft addendum for plans/round36_c2_verify.py (critic proposal, NOT the lane's counter).

Adds three checks that the frozen counter lacks, without touching its existing W1-W6:

  D1 findings  — every receipt case whose line says observed=pass must be named in the entry
                 together with its `requirement=` text verbatim (the receipt supplies the bytes,
                 so a genuine entry copies, it does not invent). 8 such cases at the frozen receipt.
  D2 lines     — the `## Located quotes` locations must be >=8 distinct (file, first-line) pairs,
                 not >=8 distinct (file, start, end) triples: an 8-row table of fragments from one
                 physical line with growing `:1-N` ranges is one located line, not eight.
  D3 rows      — a teaches cell must share >=2 distinct >=4-char word tokens with its own row's
                 capture file (kills `alpha beta gamma …` filler), the anchor cell must carry the
                 pinned commit sha, and the README coverage bullet must carry >=8 words besides the path.

Usage: python3 proposed_c2_addendum.py --lane <lane>   (exit 0 = all three hold)
"""
import argparse
import importlib.util
import pathlib
import re
import sys

def _counter():
    p = pathlib.Path(__file__).resolve()
    for d in p.parents:
        q = d / "plans" / "round36_c2_verify.py"
        if q.is_file():
            return q
    raise SystemExit("counter not found above this file")


COUNTER = _counter()


def load():
    spec = importlib.util.spec_from_file_location("c2", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def d1(m, lane):
    rec = (lane / m.RECEIPT).read_text().splitlines()
    et = (lane / m.ENTRY).read_text()
    need = []
    for l in rec:
        mm = re.match(r"case=(\S+) .* observed=pass .* requirement=(['\"])(.*)\2$", l)
        if mm:
            need.append((mm.group(1), mm.group(3)))
    for name, req in need:
        if name not in et:
            return f"observed=pass case {name} not named in the entry"
        if req not in et:
            return f"observed=pass case {name} requirement not stated in the entry"
    return None


def d2(m, lane):
    sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", (lane / m.ENTRY).read_text(), re.S | re.M)
    if not sec:
        return "located-quotes section absent"
    body = [l for l in sec.group(1).splitlines()
            if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)][1:]
    lines = set()
    for l in body:
        q = m.QUOTE_RE.match(l)
        if not q:
            return f"unparsed quote row: {l[:60]}"
        lines.add((q.group(2), int(q.group(3))))
    return None if len(lines) >= 8 else f"distinct located lines={len(lines)} (want >=8)"


def d3(m, lane):
    for rid, (name, _up, _pin) in m.FILES.items():
        row = m.rows(lane)[rid][0]
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        teaches, anchor = cells[6], cells[5]
        cap = "".join((lane / m.CAP / n).read_text() for n in {n for n, _, _ in m.FILES.values()})
        words = set(re.findall(r"[A-Za-z0-9]{4,}", cap.lower()))
        toks = {w.lower() for w in re.findall(r"[A-Za-z0-9]{4,}", teaches)}
        if len(toks & words) < 2:
            return f"{rid} teaches shares {len(toks & words)} capture tokens (want >=2)"
        if m.PIN not in anchor:
            return f"{rid} anchor lacks the pinned commit sha"
    readme = (lane / "corpus/README.md").read_text()
    rel = m.ENTRY.removeprefix("corpus/")
    bullets = [l for l in readme.splitlines() if l.startswith("- ") and rel in l]
    if not bullets:
        return "coverage bullet absent"
    if all(len(l.replace(rel, "").split()) < 8 for l in bullets):
        return "coverage bullet carries <8 words besides the path"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    m = load()
    bad = 0
    for name, fn in (("D1", d1), ("D2", d2), ("D3", d3)):
        try:
            err = fn(m, lane)
        except Exception as e:
            err = f"error {type(e).__name__}: {e}"
        print(f"{name} {'DEFECT ' + err if err else 'ok'}")
        bad += bool(err)
    print(f"addendum defects={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
