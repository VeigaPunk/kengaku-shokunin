#!/usr/bin/env python3
"""R91-C3 companion counter — R82-F1's QUOTE_RE repair proved on the real registry (round 91).

R82-F1 (ledger row `R82-F1`, superseded by `R82-F1-R90`): `plans/anchor_line_check.py` QUOTE_RE
could not see the S260/S261/S265/S266 anchor shapes (curly quotes, and the `line N` form), so the
gate reported `cited=72 ... live=0` — green because blind, not because clean. The round-91 repair
extends QUOTE_RE with the two shapes. This counter proves the repair on the lane's own registry:

  1. the four blind-spot rows S260, S261, S265, S266 now PARSE as line-cited rows;
  2. the full checker stays `live=0` over the real registry (the newly parsed quotes sit on their
     cited lines with their stated word counts);
  3. the repaired parser can still FAIL: a fixture anchor with a curly-quoted quote citing a line
     the quote is not on must produce a `line` defect (a true positive the repair must retain).

Usage:  python3 plans/round91_f1_counter.py --lane <repo> --work <scratch dir>
Exit:   0 all three hold, 1 any fails, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

BLIND_SPOT = ("S260", "S261", "S265", "S266")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("anchor_line_check_r91", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    tool = lane / "plans" / "anchor_line_check.py"
    registry = lane / "corpus" / "SOURCES.md"
    if not tool.is_file() or not registry.is_file():
        print("DEFECT SETUP unreadable plans/anchor_line_check.py or corpus/SOURCES.md")
        print("PREDICATE R91-F1 could-not-evaluate")
        return 2
    module = load_module(tool)
    defects: list[str] = []

    # 1. the four blind-spot rows parse as line-cited rows
    rows = module.parse_rows(registry.read_text(encoding="utf-8"))
    by_id = {rid: cells for rid, cells, _line in rows}
    parsed: dict[str, int] = {}
    for rid in BLIND_SPOT:
        cells = by_id.get(rid)
        if cells is None or len(cells) < 11:
            defects.append(f"PARSE-MISSING {rid}")
            continue
        count = len(module.anchor_quotes(cells[5]))
        if count == 0:
            defects.append(f"PARSE-ABSENT {rid} (QUOTE_RE still blind)")
        else:
            parsed[rid] = count
    print("PARSED " + ",".join("%s=%d" % (k, v) for k, v in sorted(parsed.items())))

    # 2. the full checker stays live=0 over the real registry
    proc = subprocess.run([sys.executable, "-I", "-B", str(tool), "--lane", str(lane)],
                          capture_output=True, text=True, timeout=300)
    anchorline = next((ln for ln in proc.stdout.splitlines() if ln.startswith("ANCHORLINE")), "")
    live_zero = proc.returncode == 0 and " live=0" in anchorline
    print("ANCHORLINE %s rc=%d" % (anchorline or "absent", proc.returncode))
    if not live_zero:
        defects.append("FULL-CHECK rc=%d %s" % (proc.returncode, anchorline))

    # 3. able to fail: a curly-quoted anchor citing a wrong line is caught, on a sha-bound capture
    capture = b"# notes\nfirst line\nsecond line\n"
    digest = hashlib.sha256(capture).hexdigest()
    fixture = work / "wrong-line"
    fixture.mkdir(parents=True, exist_ok=True)
    (fixture / "notes.md").write_bytes(capture)
    anchor = ("notes.md:3 quote \u201cfirst line\u201d (2 words); sha256 " + digest +
              "; fetched 2026-11-05")
    row = ("| S991 | fixture source | fixture origin | docs | A | " + anchor +
           " | pad | pad | pad | pad | the quote sits on line 2, the anchor cites line 3 |\n")
    frows = module.parse_rows("# registry\n" + row)
    idx = {digest: ["notes.md"]}
    caught = False
    for rid, cells, line in frows:
        cited, _rel, kinds = module.row_defects(cells, line, idx, fixture)
        if rid == "S991" and cited and "line" in kinds:
            caught = True
    print("WRONG-LINE-CAUGHT %s" % caught)
    if not caught:
        defects.append("WRONG-LINE not caught (the repair broke the true positive)")

    for d in defects:
        print("DEFECT %s" % d)
    passed = not defects and len(parsed) == len(BLIND_SPOT) and live_zero and caught
    print("PREDICATE R91-F1 %s" % ("pass" if passed else "fail"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
