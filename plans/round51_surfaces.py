#!/usr/bin/env python3
"""Round-51 C1 counter — every surface PROVINCE.md declares is machine-checked.

Frozen predicate (plans/round-51-claims.md §C1, written before any data):

    python3 plans/round51_surfaces.py --lane .
    -> exit 0 and a final line `PREDICATE R51-C1 pass`
    iff anchors total == manifest entries with dup 0 and missing 0,
        every table row of every declared section is covered by exactly one entry
        (uncovered 0),
        every entry's probe result equals its recorded `state` (STALE 0),
        every entry's recorded `state` equals the row's prose reading (DRIFT 0),
        every absent entry's row carries an `ABSENT <ISO date>` marker
        (UNVERDICTED 0),
        every `count_claim` equals the probed count (NUMBER-DRIFT 0),
        and the number of observed-present surfaces is >= `resolve_floor`
        (RESOLVE verdict=met).

The floor is what a do-nothing cannot reach: declaring everything absent would
drive observed-present below the floor recorded before any repair.

Stdlib only. Honours --lane/--manifest/--province overrides; no /tmp hardcoding
(selftest uses tempfile.mkdtemp honouring TMPDIR).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ABSENT_RE = re.compile(r"ABSENT\s+(\d{4}-\d{2}-\d{2})")
ROW_RE = re.compile(r"^\|\s*[^|\-][^|]*\|")


def expand(p: str) -> Path:
    p = os.path.expandvars(os.path.expanduser(p))
    return Path(p)


def tip_rev(lane: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(lane), "rev-parse", "master"],
            capture_output=True, text=True, timeout=20,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:  # pragma: no cover - git always present in the lane
        pass
    return "unknown"


def section_rows(text_lines: list[str], heading: str) -> list[tuple[int, str]]:
    """Rows of the first table that follows `heading` until the next heading."""
    try:
        start = next(i for i, l in enumerate(text_lines) if l.strip().startswith(heading))
    except StopIteration:
        return []
    rows = []
    started = False
    for i in range(start + 1, len(text_lines)):
        line = text_lines[i]
        nxt = text_lines[i + 1] if i + 1 < len(text_lines) else ""
        if line.startswith("#"):
            if started:
                break
            continue
        if re.match(r"^\|[\s\-:|]+\|?\s*$", line):
            continue
        if row_like(line):
            if re.match(r"^\|[\s\-:|]+\|?\s*$", nxt):
                continue  # header row of a later table
            started = True
            rows.append((i, line))
        elif started and line.strip():
            break
    return rows


def row_like(line: str) -> bool:
    return bool(ROW_RE.match(line)) and not re.match(r"^\|[\s\-:|]+\|?\s*$", line)


def probe(entry: dict, lane: Path) -> tuple[str, str]:
    """Return (observed 'present'|'absent', detail)."""
    p = entry["probe"]
    kind = p["kind"]
    if kind == "paths":
        missing = [t for t in p["targets"] if not expand(t).exists()]
        if missing:
            return "absent", "missing: " + ", ".join(missing)
        return "present", "all %d targets resolve" % len(p["targets"])
    if kind == "sha256":
        f = expand(p["target"])
        if not f.is_file():
            return "absent", "missing file %s" % p["target"]
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        pin = p["pin"]
        if not h.startswith(pin):
            return "absent", "digest %s does not start with pin %s" % (h[:8], pin)
        return "present", "digest %s… matches pin" % pin
    if kind == "port":
        host, port = p.get("host", "127.0.0.1"), int(p["port"])
        s = socket.socket()
        s.settimeout(1.5)
        try:
            s.connect((host, port))
            return "present", "LISTEN on %s:%d" % (host, port)
        except OSError as exc:
            return "absent", "connect failed: %s" % exc
        finally:
            s.close()
    if kind == "http":
        last = ""
        for url in p["urls"]:
            try:
                with urllib.request.urlopen(url, timeout=3) as r:
                    if r.status == 200:
                        return "present", "%s -> 200" % url
                    last = "%s -> %s" % (url, r.status)
            except Exception as exc:  # noqa: BLE001 - any failure means absent
                last = "%s -> %s" % (url, exc)
        return "absent", last
    if kind == "count":
        f = lane / p["target"] if not os.path.isabs(p["target"]) else Path(p["target"])
        if not f.is_file():
            return "absent", "missing %s" % p["target"]
        n = len(re.findall(p["pattern"], f.read_text(errors="replace"), flags=re.M))
        return "present", "%s=%d" % (p.get("label", "count"), n)
    raise SystemExit("unknown probe kind %r" % kind)


def check(lane: Path, manifest_path: Path, province_path: Path) -> int:
    man = json.loads(manifest_path.read_text())
    text = province_path.read_text().split("\n")
    entries = man["surfaces"]
    sections = man["sections"]

    print("REV %s" % tip_rev(lane))
    print("MANIFEST %s entries=%d sections=%d" % (manifest_path.relative_to(lane) if manifest_path.is_relative_to(lane) else manifest_path, len(entries), len(sections)))

    problems: dict[str, list[str]] = {
        "DRIFT": [], "STALE": [], "UNVERDICTED": [], "NUMBER-DRIFT": [],
        "ANCHOR-MISSING": [], "ANCHOR-DUP": [], "UNCOVERED": [], "SECTION-MISSING": [],
    }

    # anchors — searched only inside the entry's own section table
    rows_by_section = {sec: section_rows(text, sec) for sec in sections}
    dup = miss = 0
    anchor_line: dict[str, int] = {}
    for e in entries:
        hits = [i for i, l in rows_by_section.get(e.get("section"), []) if e["anchor"] in l]
        if len(hits) == 0:
            miss += 1
            problems["ANCHOR-MISSING"].append("%s anchor not found: %s" % (e["id"], e["anchor"][:60]))
        elif len(hits) > 1:
            dup += 1
            problems["ANCHOR-DUP"].append("%s anchor appears %d times" % (e["id"], len(hits)))
        else:
            anchor_line[e["id"]] = hits[0]
    print("ANCHORS total=%d dup=%d missing=%d" % (len(entries), dup, miss))

    # coverage: every row of every declared section maps to one entry
    uncovered = 0
    for sec in sections:
        rows = rows_by_section.get(sec, [])
        used = {anchor_line[e["id"]] for e in entries if e.get("section") == sec and e["id"] in anchor_line}
        row_idx = {i for i, _ in rows}
        if not rows:
            problems["SECTION-MISSING"].append("section %r has no table rows" % sec)
        unc = row_idx - used
        uncovered += len(unc)
        for i in sorted(unc):
            problems["UNCOVERED"].append("%s row line %d has no manifest entry" % (sec, i + 1))
        stray = used - row_idx
        for i in stray:
            problems["UNCOVERED"].append("%s anchors line %d outside section %r" % (sec, i + 1, sec))
        print('ROWS section=%s rows=%d entries=%d uncovered=%d' % (
            json.dumps(sec), len(rows), sum(1 for e in entries if e.get("section") == sec), len(unc)))

    present = absent = errors = 0
    for e in entries:
        observed, detail = probe(e, lane)
        if observed == "present":
            present += 1
        else:
            absent += 1
        if observed != e["state"]:
            problems["STALE"].append("%s probe=%s state=%s (%s)" % (e["id"], observed, e["state"], detail))
        if e["prose"] != e["state"]:
            problems["DRIFT"].append("%s prose=%s state=%s (%s)" % (e["id"], e["prose"], e["state"], e.get("why", "")[:80]))
        if e["state"] == "absent":
            line = text[anchor_line[e["id"]]] if e["id"] in anchor_line else ""
            if not ABSENT_RE.search(line):
                problems["UNVERDICTED"].append("%s row has no ABSENT <ISO date> marker" % e["id"])
        if "count_claim" in e:
            m = re.search(r"(\d+)", detail)
            if not m or int(m.group(1)) != int(e["count_claim"]):
                problems["NUMBER-DRIFT"].append("%s row claims %s, probe says %s" % (e["id"], e["count_claim"], detail))
    print("PROBES run=%d present=%d absent=%d errors=%d" % (len(entries), present, absent, errors))

    ok = True
    for key in ("DRIFT", "STALE", "UNVERDICTED", "NUMBER-DRIFT", "ANCHOR-DUP", "ANCHOR-MISSING", "UNCOVERED", "SECTION-MISSING"):
        print("%s %d" % (key, len(problems[key])))
        for line in problems[key]:
            print("  DETAIL %s %s" % (key, line))
        if problems[key]:
            ok = False

    floor = int(man["resolve_floor"])
    verdict = "met" if present >= floor else "violated"
    print("RESOLVE observed_present=%d floor=%d verdict=%s" % (present, floor, verdict))
    if present < floor:
        ok = False

    print("PREDICATE R51-C1 %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# ---------------------------------------------------------------- selftest

GOOD_ROW = "| Surface A | `~/a` | does a thing |"
CORE_ROW = "| Gate A | `test -e a.txt` | present |"


def _selftest(tmp: Path) -> int:
    cases = 0
    failures = []

    def build(rows_a, rows_b, entries, floor=1):
        (tmp / "PROVINCE.md").write_text(
            "# P\n\n## Surfaces\n\n| Surface | Path | Use |\n|---|---|---|\n" + rows_a +
            "\n\n### Core\n\n| Surface | Check | Result |\n|---|---|---|\n" + rows_b + "\n")
        (tmp / "m.json").write_text(json.dumps(
            {"version": 1, "round": 51, "anchor_file": "PROVINCE.md",
             "sections": ["## Surfaces", "### Core"], "resolve_floor": floor,
             "surfaces": entries}))
        (tmp / "a").mkdir(exist_ok=True)
        (tmp / "a.txt").write_text("x")

    def run(expect_ok, expect_key=None):
        nonlocal cases
        cases += 1
        code = check(tmp, tmp / "m.json", tmp / "PROVINCE.md")
        if expect_ok and code != 0:
            failures.append("case %d expected pass, got exit %d" % (cases, code))
        if not expect_ok and code == 0:
            failures.append("case %d expected fail, got pass" % cases)
        return code

    # S0 consistent pass
    build(GOOD_ROW, CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    if run(True) != 0:
        pass
    # S1 drift: prose says resolves, state absent, row dated
    build("| Surface A | `~/a` — **ABSENT 2026-10-28** | x |", CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "absent",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "nope-a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S2 stale manifest: state present but path absent
    build(GOOD_ROW, CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "nope-a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S3 unverdicted: absent row with no ISO date
    build("| Surface A | `~/nope-a` | x |", CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "absent",
         "prose": "absent", "probe": {"kind": "paths", "targets": [str(tmp / "nope-a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S4 number drift
    build("| Surface A | `~/a` (3 rows) | x |", CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "present",
         "prose": "present", "count_claim": 3,
         "probe": {"kind": "count", "target": "a.txt", "pattern": "^S[0-9]+$", "label": "rows"}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S5 uncovered row
    build(GOOD_ROW + "\n| Surface B | `~/a` | x |", CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S6 duplicate anchor
    build(GOOD_ROW + "\n" + GOOD_ROW, CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)
    # S7 floor violated: everything declared absent and dated
    build("| Surface A | `~/nope-a` — **ABSENT 2026-10-28** | x |",
          "| Gate A | `a.txt` — **ABSENT 2026-10-28** | present |", [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface A |", "state": "absent",
         "prose": "absent", "probe": {"kind": "paths", "targets": [str(tmp / "nope-a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "absent",
         "prose": "absent", "probe": {"kind": "paths", "targets": [str(tmp / "nope-b")]}},
    ], floor=1)
    run(False)
    # S8 missing anchor
    build(GOOD_ROW, CORE_ROW, [
        {"id": "SF01", "section": "## Surfaces", "anchor": "| Surface Z |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a")]}},
        {"id": "SF02", "section": "### Core", "anchor": "| Gate A |", "state": "present",
         "prose": "present", "probe": {"kind": "paths", "targets": [str(tmp / "a.txt")]}},
    ])
    run(False)

    print("[selftest] cases=%d failures=%d" % (cases, len(failures)))
    for f in failures:
        print("[selftest] FAIL %s" % f)
    print("[selftest] %s" % ("ALL PASS" if not failures else "FAILED"))
    return 0 if not failures else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--manifest")
    ap.add_argument("--province")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    lane = Path(args.lane).resolve()
    if args.selftest:
        tmp = Path(tempfile.mkdtemp(prefix="r51surf-"))
        try:
            return _selftest(tmp)
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)
    manifest = Path(args.manifest) if args.manifest else lane / "plans/round51-surfaces.json"
    province = Path(args.province) if args.province else lane / "PROVINCE.md"
    return check(lane, manifest, province)


if __name__ == "__main__":
    sys.exit(main())
