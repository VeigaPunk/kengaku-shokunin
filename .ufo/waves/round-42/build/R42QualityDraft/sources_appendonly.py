#!/usr/bin/env python3
"""Draft check for QUALITY Q34: corpus/SOURCES.md is append-only outside the three
mutable cells (status, recheck, used-by); a correction to any other cell must land as a
NEW row whose `teaches` cell opens `supersedes S0NN —` in the SAME commit.

Reads git commits only (working tree and index ignored). Exit 1 iff any in-place change
of a non-mutable cell in a commit has no superseding row in that commit.
"""
import re
import subprocess
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "."
PATHSPEC = "corpus/SOURCES.md"
COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
        "status", "opened", "recheck", "used-by"]
MUTABLE = {"status", "recheck", "used-by"}
ROW = re.compile(r"S\d{3,}\Z")
SUP = re.compile(r"supersedes\s+(S\d{3,})\s+—")


def git(*args):
    return subprocess.run(["git", "-C", LANE, *args],
                          capture_output=True, text=True)


def rows(text):
    out = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and ROW.match(cells[0]):
            out[cells[0]] = cells
    return out


def main():
    log = git("log", "--reverse", "--format=%H", "--", PATHSPEC)
    if log.returncode != 0:
        print(f"SETUP git log failed: {log.stderr.strip()}")
        return 2
    commits = log.stdout.split()
    prev, hits, arity = {}, [], []
    for sha in commits:
        show = git("show", f"{sha}:{PATHSPEC}")
        if show.returncode != 0:
            continue
        cur = rows(show.stdout)
        new_ids = [i for i in cur if i not in prev]
        superseded = set()
        for i in new_ids:
            cells = cur[i]
            teaches = cells[6] if len(cells) > 6 else ""
            m = SUP.search(teaches)
            if m:
                superseded.add(m.group(1))
        for rid, cells in cur.items():
            if rid not in prev:
                continue
            old = prev[rid]
            if len(old) != len(cells):
                arity.append((sha[:8], rid, len(old), len(cells)))
                continue
            for name, a, b in zip(COLS, old, cells):
                if a == b or name in MUTABLE:
                    continue
                # rule 2 is act-level: a non-mutable cell never changes in place, whether
                # or not a superseding row lands beside it. The repair row is context only.
                hits.append((sha[:8], rid, name, rid in superseded))
        prev = cur
    print(f"SOURCES-COMMITS scanned={len(commits)} rows_at_tip={len(prev)}")
    for sha, rid, name, ok in hits:
        print(f"CELL {sha} {rid} {name} repair_row={'same-commit' if ok else 'none'}")
    for sha, rid, a, b in arity:
        print(f"ARITY {sha} {rid} cells {a}->{b}")
    print(f"SOURCES-APPENDONLY violations={len(hits)} arity={len(arity)}")
    return 1 if hits or arity else 0


if __name__ == "__main__":
    sys.exit(main())
