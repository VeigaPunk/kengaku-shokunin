#!/usr/bin/env python3
"""probe_sums.py — F38AnchorFix. Are the two accepted views of a capture ever different?

`capture_digests` accepts both the committed file's sha256 and the digest a committed `SHA256SUMS*`
lists for that filename. If those disagree for any capture, the check accepts a digest that is not
the committed bytes. Prints every disagreeing capture and the totals.

Usage: python3 probe_sums.py --lane <clone> --check <tip check.py>
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--check", required=True)
    a = ap.parse_args(argv)
    spec = importlib.util.spec_from_file_location("ac", pathlib.Path(a.check).resolve())
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    idx = mod.evidence_index(pathlib.Path(a.lane).resolve(), "head")
    files, entries = idx["file_digest"], idx["dir_entries"]
    disagree, checked = [], 0
    for p, dig in sorted(files.items()):
        d, base = p.rsplit("/", 1) if "/" in p else ("", p)
        if (d, base) in entries:
            checked += 1
            if entries[(d, base)] != dig:
                disagree.append((p, dig, entries[(d, base)]))
    for p, fdig, mdig in disagree:
        print(f"DISAGREE {p} file={fdig} manifest={mdig}")
    print(f"captures_listed_in_a_manifest={checked} disagree={len(disagree)} "
          f"manifest_entries={len(entries)} manifest_digests={len(idx['manifest'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
