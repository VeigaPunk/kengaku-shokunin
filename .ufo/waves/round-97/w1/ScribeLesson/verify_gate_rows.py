#!/usr/bin/env python3
"""ScribeLesson: verify the S317-S325 SOURCES rows against the captured bytes at T.

Read-only. For each row: parse the 11 SOURCES cells, extract the anchor's `<path>:<line>`
and the curly-quoted quote, read the captured file under
corpus/evidence/round97/graders/sparql-university/<path>, and check:
  - the captured file's sha256 and byte size equal the row's stamp
  - the quote occurs on the cited line
  - the row's word count equals len(quote.split())
Prints one line per row plus a summary; exit 1 on any mismatch.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SOURCES = Path(sys.argv[1]) if len(sys.argv) > 1 else LANE / "corpus/SOURCES.md"
CAP = Path(sys.argv[2]) if len(sys.argv) > 2 else LANE / "corpus/evidence/round97/graders/sparql-university"

ROW = re.compile(r"^\| (S3(?:1[7-9]|2[0-5])) \|")
ANCHOR = re.compile(r"([\w./-]+):(\d+) quote \u201c(.+?)\u201d \((\d+) words?\)")
SHA = re.compile(r"sha256 ([0-9a-f]{64})")
SIZE = re.compile(r"HTTP (\d{3}), (\d+) B")


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main() -> int:
    text = SOURCES.read_text(encoding="utf-8")
    rows = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if m:
            rows[m.group(1)] = split_row(line)
    if sorted(rows) != [f"S{n}" for n in range(317, 326)]:
        print("ROW-SET", sorted(rows))
        return 1
    bad = 0
    for sid in sorted(rows):
        cells = rows[sid]
        if len(cells) != 11:
            print(f"{sid} CELLS {len(cells)}")
            bad += 1
            continue
        _id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used = cells
        am = ANCHOR.search(anchor)
        if not am:
            print(f"{sid} ANCHOR-PARSE-FAIL {anchor[:80]!r}")
            bad += 1
            continue
        path, lineno, quote, words = am.group(1), int(am.group(2)), am.group(3), int(am.group(4))
        cap = CAP / path
        if not cap.is_file():
            print(f"{sid} CAPTURE-MISSING {path}")
            bad += 1
            continue
        data = cap.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        sm = SHA.search(anchor)
        zm = SIZE.search(anchor)
        row_sha = sm.group(1) if sm else None
        row_size = int(zm.group(2)) if zm else None
        lines = data.decode("utf-8", errors="replace").split("\n")
        on_line = lineno <= len(lines) and quote in lines[lineno - 1]
        wc = len(quote.split())
        ok = (sha == row_sha and len(data) == row_size and on_line and wc == words)
        print(
            f"{sid} {kind}/{tier} status={status} opened={opened} "
            f"sha={'ok' if sha == row_sha else 'MISMATCH'} size={'ok' if len(data) == row_size else 'MISMATCH'} "
            f"line={lineno} on_line={'yes' if on_line else 'NO'} words={wc}/{words} "
            f"flip={recheck!r} used={used!r}"
        )
        if not ok:
            bad += 1
            if not on_line:
                for i in range(max(0, lineno - 2), min(len(lines), lineno + 1)):
                    print(f"   {i + 1}: {lines[i][:160]}")
    print(f"ROWS {len(rows)} defects {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
