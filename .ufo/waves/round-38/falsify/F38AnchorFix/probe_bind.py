#!/usr/bin/env python3
"""probe_bind.py — F38AnchorFix. Read-only probe of `plans/anchor_digest_check.py` binding.

Imports the tip check as a module, builds its evidence index, and prints every row whose text
pins more than one upstream URL, or whose binding admits more than one capture / digest. Those are
the rows where a single anchor token has more than one "own" capture to satisfy.

Usage: python3 probe_bind.py --lane <scratch clone> [--check <tip check.py>]
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("anchor_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--check", required=True)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    mod = load(pathlib.Path(a.check).resolve())
    idx = mod.evidence_index(lane, "head")
    rows = mod.parse_rows(lane)
    multi = 0
    for r in rows:
        text = " ".join(r["cells"])
        urls = mod.upstream_files(text)
        caps, reason = mod.bind_row(r, idx)
        digs = set()
        for path, _how in caps:
            digs |= set(mod.capture_digests(idx, path))
        if len(urls) > 1 or len(caps) > 1:
            multi += 1
            print(f"ROW {r['sid']} urls={len(urls)} caps={len(caps)} digests={len(digs)} "
                  f"anchor_tokens={len(r['atoks'])}")
            for u in urls:
                print(f"  URL  {u[1]}/{u[2][:8]}/{u[3]}")
            for c, how in caps:
                print(f"  CAP  {c} by={how} digests={len(mod.capture_digests(idx, c))}")
    print(f"rows={len(rows)} rows_with_multi_url_or_multi_capture={multi}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
