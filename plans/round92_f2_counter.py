#!/usr/bin/env python3
"""R92-F2 companion counter — capture pins for the S260/S261/S265/S266 blind-spot chains.

Round-91 routing (defect 9 / lesson M5): the four blind-spot rows parse but carry no capture
pin, so their quotes are cited and not byte-verified. CORPUS rule 2 keeps the registry
append-only, so the pins land as supersede rows: S287 supersedes S265 (the round-81 receipt
capture), S288 supersedes S266 (the log-summary instruction capture), S289 supersedes S288
(the vulnerable-secret instruction capture; a chain row, because one row can name only one
capture file). This counter proves, on the real registry:

  1. each of S287, S288, S289 exists, parses as a line-cited row, resolves its sha256 token
     to a git-tracked capture under corpus/evidence/, and carries no anchor defect;
  2. the full checker's ANCHORLINE line shows captured >= 74 (71 before the pins) and live=0;
  3. the repaired parser can still FAIL: the wrong-line fixture is caught (inherited from the
     round-91 F1 able-to-fail witness).

Usage:  python3 plans/round92_f2_counter.py --lane <repo> --work <scratch dir>
Exit:   0 all hold, 1 any fails, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

PINNED = ("S287", "S288", "S289")
MIN_CAPTURED = 74


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("anchor_line_check_r92", path)
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
        print("PREDICATE R92-F2 could-not-evaluate")
        return 2
    module = load_module(tool)
    defects: list[str] = []

    rows = module.parse_rows(registry.read_text(encoding="utf-8"))
    by_id = {rid: (cells, line) for rid, cells, line in rows}
    idx = module.evidence_index(lane)
    pinned: dict[str, int] = {}
    for rid in PINNED:
        hit = by_id.get(rid)
        if hit is None:
            defects.append(f"PARSE-MISSING {rid} (supersede row absent)")
            continue
        cells, line = hit
        cited, cap, kinds = module.row_defects(cells, line, idx, lane)
        sha_hit = bool(module.SHA_RE.findall(line)) and bool(cap)
        ok = cited and sha_hit and not kinds
        pinned[rid] = 1 if ok else 0
        if not ok:
            defects.append(f"PIN-DEFECTIVE {rid} cited={cited} cap={cap} kinds={kinds}")
    print("CAPTURE-PINNED " + ",".join("%s=%d" % (k, v) for k, v in sorted(pinned.items())))

    proc = subprocess.run([sys.executable, "-I", "-B", str(tool), "--lane", str(lane)],
                          capture_output=True, text=True, timeout=300)
    anchorline = next((ln for ln in proc.stdout.splitlines() if ln.startswith("ANCHORLINE")), "")
    print("ANCHORLINE %s rc=%d" % (anchorline or "absent", proc.returncode))
    captured_ok = False
    import re as _re
    m = _re.search(r"captured=(\d+)", anchorline)
    if m:
        captured_ok = int(m.group(1)) >= MIN_CAPTURED and " live=0" in anchorline and proc.returncode == 0
    if not captured_ok:
        defects.append("ANCHORLINE captured<%d or live>0 or rc=%d" % (MIN_CAPTURED, proc.returncode))

    capture = b"# notes\nfirst line\nsecond line\n"
    digest = hashlib.sha256(capture).hexdigest()
    fixture = work / "wrong-line"
    fixture.mkdir(parents=True, exist_ok=True)
    (fixture / "notes.md").write_bytes(capture)
    anchor = ("notes.md:3 quote \u201cfirst line\u201d (2 words); sha256 " + digest +
              "; fetched 2026-11-05")
    row = ("| S992 | fixture source | fixture origin | docs | A | " + anchor +
           " | pad | pad | pad | pad | the quote sits on line 2, the anchor cites line 3 |\n")
    frows = module.parse_rows("# registry\n" + row)
    fidx = {digest: ["notes.md"]}
    caught = False
    for rid, cells, line_no in frows:
        cited, _rel, kinds = module.row_defects(cells, line_no, fidx, fixture)
        if rid == "S992" and cited and "line" in kinds:
            caught = True
    print("WRONG-LINE-CAUGHT %s" % caught)
    if not caught:
        defects.append("WRONG-LINE not caught (the repair broke the true positive)")

    for d in defects:
        print("DEFECT %s" % d)
    passed = (not defects and len(pinned) == len(PINNED)
              and all(v == 1 for v in pinned.values()) and captured_ok and caught)
    print("PREDICATE R92-F2 %s" % ("pass" if passed else "fail"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
