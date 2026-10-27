#!/usr/bin/env python3
"""Q35 extension sweep: a `not fired` flip verdict that names a file is RED when
a landed knowledge entry carries a `<file>:<line>` citation of that file.

Read-only. Usage: python3 flip_cite_sweep.py --lane <lane>
Prints one FLIP-CITE line per `not fired` verdict and a FLIPS-CITE summary.
"""
import argparse, re, sys
from pathlib import Path

FLIP = re.compile(r"^Flip check \(round (\d+)\): (\S+) \u2014 (fired|not fired) \u2014 (.*)$")
CITE = re.compile(r"(?<![\w./-]){base}:(\d+)(?![\w])")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scope", choices=("all", "block"), default="block",
                    help="all = every knowledge entry; block = entries named within +-6 lines of the flip line")
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    entries = sorted((lane / "corpus/knowledge").glob("*.md"))
    lessons = sorted((lane / "corpus/lessons").glob("*.md"))
    corpus = [(p, p.read_text(encoding="utf-8", errors="replace").splitlines())
              for p in entries + lessons]
    total = red = named = 0
    for p in lessons:
        lines_all = p.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines_all, 1):
            m = FLIP.match(line)
            if not m:
                continue
            total += 1
            rnd, item, state, ev = m.groups()
            if state != "not fired":
                continue
            base = item.rstrip("/")
            if "." not in base and "/" not in base:
                print(f"FLIP-CITE {p.relative_to(lane)}:{i} item={item} verdict=SKIP (not a file name)")
                continue
            named += 1
            pat = re.compile(CITE.pattern.format(base=re.escape(base)))
            hits = []
            if a.scope == "all":
                sources = corpus
            else:
                window = "\n".join(lines_all[max(0, i - 7):i + 6])
                sources = [(q, q.read_text(encoding="utf-8", errors="replace").splitlines())
                           for q in entries if q.name in window]
            for q, elines in sources:
                for j, l in enumerate(elines, 1):
                    if pat.search(l):
                        hits.append(f"{q.relative_to(lane)}:{j}")
            if hits:
                red += 1
                print(f"FLIP-CITE {p.relative_to(lane)}:{i} item={item} verdict=RED scope={a.scope} "
                      f"cited_by={','.join(hits[:4])}"
                      + (f" (+{len(hits)-4})" if len(hits) > 4 else ""))
            else:
                print(f"FLIP-CITE {p.relative_to(lane)}:{i} item={item} verdict=ok scope={a.scope}")
    print(f"FLIPS-CITE total={total} named={named} red={red}")
    return 1 if red else 0

if __name__ == "__main__":
    sys.exit(main())
