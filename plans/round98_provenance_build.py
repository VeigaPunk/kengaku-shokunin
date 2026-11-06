#!/usr/bin/env python3
"""Build `corpus/evidence/PROVENANCE.md` for R98-C2 (round 98): one table line per frozen
population row, naming the row id, the nested capture path relative to `corpus/evidence/`, the
pinned upstream URL the row itself carries, and the sha256 of the committed capture bytes.

The frozen `plans/anchor_digest_check.py` binds a SOURCES row to a capture through a committed
`PROVENANCE.md` whose table line carries the row id and a backticked filename that resolves beside
the file (its binding rule 1). Placing the file at `corpus/evidence/` lets one table name nested
captures of every round without editing the gate or moving any capture.

The builder refuses (exit 2) when a capture is absent at the lane's HEAD, when its bytes do not
hash to the population's token, or when the row carries no pinned upstream URL. It prints the file
to stdout; it writes nothing.

Usage:  python3 plans/round98_provenance_build.py --lane <repo>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

URL = re.compile(r"https://raw\.githubusercontent\.com/[^\s|`)]+")
ROWID = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    spec = importlib.util.spec_from_file_location("c2", lane / "plans/round98_c2_nested_bind.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows = {}
    for line in (lane / "corpus/SOURCES.md").read_text(encoding="utf-8").splitlines():
        m = ROWID.match(line)
        if m:
            rows.setdefault(m.group(1), line)
    out = [
        "# Provenance bindings for nested replay captures (round 98, R98-C2)",
        "",
        "Built by `plans/round98_provenance_build.py` from the frozen population in",
        "`plans/round98_c2_nested_bind.py`. Rounds 52 and 92-97 captured whole task trees",
        "(`round<N>/graders/<task>/<sub>/<file>`); the frozen `plans/anchor_digest_check.py` looks for",
        "`<task dir>/<basename>` and so reported each such row `anchor-unbound` although its digest",
        "names committed bytes. Each line below binds one SOURCES row to the capture the replay",
        "itself staged, through the gate's provenance-row rule; no capture moved and no gate byte",
        "changed. The sha256 column is the digest of the committed capture, equal to the row's",
        "anchor token.",
        "",
        "| row | file here | pinned URL | sha256 |",
        "|---|---|---|---|",
    ]
    for sid in sorted(mod.POP, key=lambda s: int(s[1:])):
        token, path = mod.POP[sid]
        proc = subprocess.run(["git", "-C", str(lane), "show", f"HEAD:{path}"], capture_output=True)
        if proc.returncode != 0 or hashlib.sha256(proc.stdout).hexdigest() != token:
            print(f"REFUSE {sid} capture {path} absent or digest mismatch", file=sys.stderr)
            return 2
        urls = URL.findall(rows.get(sid, ""))
        if not urls:
            print(f"REFUSE {sid} row carries no pinned upstream URL", file=sys.stderr)
            return 2
        rel = path[len("corpus/evidence/"):]
        out.append(f"| {sid} | `{rel}` | {urls[0]} | `{token}` |")
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
