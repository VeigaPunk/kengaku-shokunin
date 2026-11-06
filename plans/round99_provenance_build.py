#!/usr/bin/env python3
"""Build the R99-C2 row-scoped provenance files (round 99).

For every row of the frozen population POP in `plans/round99_c2_rowscoped_bind.py`, one table line
`| <sid> | `<capture path relative to corpus/evidence/round<N>/>` | `<sha256>` |` is written to
`corpus/evidence/round<N>/PROVENANCE.md`, where round<N> is the capture's top-level round directory.
Three columns, no URL: the frozen gate's provenance-row rule binds the row id to the capture, and
no line can feed its `prov_url` fallback (round-98 lesson M4).

Refuses (exit 2) when a capture is absent at the lane's HEAD, when its bytes do not hash to the
population's token, or when a target PROVENANCE.md already exists at HEAD. Writes under --out
(default: the lane) and prints each path written.

Usage:  python3 plans/round99_provenance_build.py --lane <repo> [--out <root>]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROUND_DIR = re.compile(r"^(corpus/evidence/round(\d+))/(.+)$")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    out_root = Path(a.out).resolve() if a.out else lane
    spec = importlib.util.spec_from_file_location("c2", lane / "plans/round99_c2_rowscoped_bind.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    groups: dict[str, list[str]] = {}
    for sid in sorted(mod.POP, key=lambda s: int(s[1:])):
        token, path = mod.POP[sid]
        proc = subprocess.run(["git", "-C", str(lane), "show", f"HEAD:{path}"], capture_output=True)
        if proc.returncode != 0 or hashlib.sha256(proc.stdout).hexdigest() != token:
            print(f"REFUSE {sid} capture {path} absent or digest mismatch", file=sys.stderr)
            return 2
        m = ROUND_DIR.match(path)
        if not m:
            print(f"REFUSE {sid} capture {path} not under a round directory", file=sys.stderr)
            return 2
        groups.setdefault(m.group(1), []).append(f"| {sid} | `{m.group(3)}` | `{token}` |")
    for d, lines in sorted(groups.items()):
        target = f"{d}/PROVENANCE.md"
        if subprocess.run(["git", "-C", str(lane), "cat-file", "-e", f"HEAD:{target}"],
                          capture_output=True).returncode == 0:
            print(f"REFUSE {target} already committed", file=sys.stderr)
            return 2
        text = "\n".join([
            f"# Row-scoped provenance bindings ({d.rsplit('/', 1)[-1]}; round 99, R99-C2)",
            "",
            "Built by `plans/round99_provenance_build.py` from the frozen population in",
            "`plans/round99_c2_rowscoped_bind.py`: SOURCES rows whose only anchor-digest finding was",
            "`anchor-unbound` although their sha256 equals bytes committed in this directory. Each line",
            "binds one row id to that capture through the frozen gate's provenance-row rule. Three",
            "columns and no URL, so no line can re-bind another row through the gate's provenance-URL",
            "fallback (round-98 lesson M4). The sha256 column is the committed capture's digest, equal",
            "to the row's anchor token.",
            "",
            "| row | file here | sha256 |",
            "|---|---|---|",
            *lines,
        ]) + "\n"
        dest = out_root / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
