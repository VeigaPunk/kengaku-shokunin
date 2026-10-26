#!/usr/bin/env python3
"""Reference implementation for QUALITY.md Q26 (round 37 draft, seat R37QualityDraft).

Every `sha256` token in a `corpus/SOURCES.md` registry row's `anchor` cell must be
  * 64 lowercase hex and present in a committed manifest digest set
    (`corpus/evidence/**/SHA256SUMS*`, `plans/fixtures/**/manifest.*`), or
  * shorter hex ending in `…` (a declared prefix), or
  * backed by the same cell's declaration `snapshot hash, not a manifest pin`.

Prints one summary line `rows=<n> manifests=<m> tokens_ok=<k> bad_shape=<b>
declared_snapshot=<s> unmarked=<u>` plus one line per red token.
Exit 0 iff bad_shape=0 and unmarked=0, else 1.

Placement for landing: `plans/anchor_digest_check.py`, run as
`python3 plans/anchor_digest_check.py --lane .`.
"""
from __future__ import annotations

import argparse
import pathlib
import re

ROW = re.compile(r"^\| (S\d+) ")
TOKEN = re.compile(r"sha256 `?([0-9a-fA-F]*)(…|\.\.\.)?")
DIGEST = re.compile(r"\b[0-9a-f]{64}\b")
SUMS_LINE = re.compile(r"^([0-9a-f]{64})\s+(\S+)")
DECLARED = "snapshot hash, not a manifest pin"


def digest_set(lane: pathlib.Path) -> tuple[set[str], int]:
    paths = []
    for pat in ("corpus/evidence/**/SHA256SUMS*", "plans/fixtures/**/manifest.*"):
        paths += sorted(lane.glob(pat))
    digests: set[str] = set()
    for p in paths:
        for line in p.read_text().splitlines():
            m = SUMS_LINE.match(line.strip())
            if m:
                digests.add(m.group(1))
        digests.update(DIGEST.findall(p.read_text()))
    return digests, len(paths)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane)
    digests, n_man = digest_set(lane)
    rows = [ln for ln in (lane / "corpus/SOURCES.md").read_text().splitlines() if ROW.match(ln)]
    ok = 0
    bad_shape: list[str] = []
    declared: list[str] = []
    unmarked: list[str] = []
    for row in rows:
        cells = row.split("|")
        rid, anchor = cells[1].strip(), cells[6]
        for tok, ellipsis in TOKEN.findall(anchor):
            if not tok:
                continue
            if len(tok) != 64:
                if ellipsis:
                    ok += 1
                else:
                    bad_shape.append(f"BAD_SHAPE {rid} len={len(tok)}")
                continue
            if tok in digests:
                ok += 1
            elif DECLARED in anchor:
                declared.append(rid)
            else:
                unmarked.append(f"UNMARKED {rid} {tok}")
    for line in bad_shape + unmarked:
        print(line)
    print(
        f"rows={len(rows)} manifests={n_man} tokens_ok={ok} bad_shape={len(bad_shape)} "
        f"declared_snapshot={len(declared)} unmarked={len(unmarked)}"
    )
    return 0 if not bad_shape and not unmarked else 1


if __name__ == "__main__":
    raise SystemExit(main())
