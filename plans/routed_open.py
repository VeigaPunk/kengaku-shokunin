#!/usr/bin/env python3
"""Routed-findings burn-down (kengaku round 41 rider, considerthese/2026-10-26.md proposal 1).

One file, one row per routed finding: `corpus/routed-findings.jsonl` (override with `--file`).
The defect ledgers (`corpus/defects*.jsonl`) are refused by name: they are pinned by
`plans/ledger_tip.py` and the round-40 C1 mutant table, so routed findings never move them.

Row (JSON object per line):

  id           unique, `[A-Za-z0-9][A-Za-z0-9._-]*`; an id appears once, ever. Appending a second
               row for an id is a defect, never an update.
  class        short slug for the finding class
  source       `<lesson file>:<line>` of the routing sentence, relative to the lane
  opened_round int >= 1
  status       one of open | closed | refused | blocked
  close        closing evidence (commit + path:line or receipt) -- required when status=closed
  blocker      the named blocker -- required when status=blocked or refused
  check        optional shell command run from the lane root that exits 0 exactly when the routed
               work is done; `--observe` compares it with `status`
  note         optional free text

Printed line (the round close quotes it):

  routed_open=<n> oldest_round=<r>

`n` counts rows whose status is `open` or `blocked` (a refusal is a decision, not a burn-down
item); `r` is the smallest `opened_round` among them, or `-` when there is none. A closed row
without closing evidence, or a blocked/refused row without a blocker, is a defect: the summary
line is withheld and the exit is 1, so a round close cannot quote a number off a broken file.

Exit: 0 clean; 1 invalid row(s), a failed `--selftest` or an `--observe` mismatch; 2 setup.
Stdlib only.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

STATUSES = ("open", "closed", "refused", "blocked")
REQUIRED = ("id", "class", "source", "opened_round", "status")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SOURCE_RE = re.compile(r"(.+):([0-9]+)\Z")


def is_ledger(path):
    """True for corpus/defects*.jsonl: pinned ledgers this file must never read or move."""
    return pathlib.Path(path).name.startswith("defects")


def source_path(lane, value):
    """Validate `<path>:<line>` against lane bytes; raise ValueError with the reason."""
    if not isinstance(value, str):
        raise ValueError("source must be a string")
    m = SOURCE_RE.match(value)
    if not m:
        raise ValueError("source must read <path>:<line>")
    relative, line = m.group(1), int(m.group(2))
    pure = pathlib.PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        raise ValueError(f"source path escapes the lane: {relative}")
    path = lane / relative
    if not path.is_file():
        raise ValueError(f"source file missing: {relative}")
    lines = path.read_text(errors="replace").splitlines()
    if line < 1 or line > len(lines) or not lines[line - 1].strip():
        raise ValueError(f"source line {line} is blank or past the end of {relative}")


def validate(obj, lane, seen):
    """One row -> None, or the reason it is a defect."""
    if not isinstance(obj, dict):
        return "row is not a JSON object"
    missing = [k for k in REQUIRED if k not in obj]
    if missing:
        return f"missing keys: {','.join(missing)}"
    sid = obj["id"]
    if not isinstance(sid, str) or not ID_RE.match(sid):
        return "id must match [A-Za-z0-9][A-Za-z0-9._-]*"
    if sid in seen:
        return f"duplicate id {sid} (one row per finding; append nothing for an existing id)"
    if not isinstance(obj["class"], str) or not obj["class"].strip():
        return "class must be a non-empty string"
    try:
        source_path(lane, obj["source"])
    except ValueError as exc:
        return str(exc)
    round_ = obj["opened_round"]
    if isinstance(round_, bool) or not isinstance(round_, int) or round_ < 1:
        return "opened_round must be an int >= 1"
    status = obj["status"]
    if status not in STATUSES:
        return f"status must be one of {'|'.join(STATUSES)}"
    close, blocker = obj.get("close"), obj.get("blocker")
    for name, value in (("close", close), ("blocker", blocker)):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            return f"{name} must be null or a non-empty string"
    if status == "closed" and not close:
        return "a closed row must carry closing evidence in `close`"
    if status in ("blocked", "refused") and not blocker:
        return f"a {status} row must name its blocker"
    check = obj.get("check")
    if check is not None and (not isinstance(check, str) or not check.strip()):
        return "check must be null or a non-empty shell command"
    note = obj.get("note")
    if note is not None and not isinstance(note, str):
        return "note must be null or a string"
    return None


def load(path, lane):
    rows, defects, seen = [], [], set()
    for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            defects.append((number, f"malformed JSON: {exc.msg}"))
            continue
        reason = validate(obj, lane, seen)
        if reason:
            defects.append((number, reason))
            continue
        seen.add(obj["id"])
        rows.append(obj)
    return rows, defects


def tally(rows):
    counts = {s: sum(r["status"] == s for r in rows) for s in STATUSES}
    pending = [r["opened_round"] for r in rows if r["status"] in ("open", "blocked")]
    oldest = min(pending) if pending else None
    return counts, counts["open"] + counts["blocked"], oldest


def observe(rows, lane, timeout):
    """Run every row's `check` from the lane root; a check exits 0 exactly when the work is done."""
    mismatched = 0
    for row in rows:
        check = row.get("check")
        if not check:
            print(f"OBSERVE {row['id']} self={row['status']} observed=n/a")
            continue
        try:
            r = subprocess.run(check, shell=True, cwd=str(lane), capture_output=True, text=True,
                               timeout=timeout)
            rc = r.returncode
        except subprocess.TimeoutExpired:
            rc = f"timeout>{timeout}s"
        observed = "pass" if rc == 0 else "fail"
        want = "pass" if row["status"] in ("closed", "refused") else "fail"
        flag = "" if observed == want else " MISMATCH"
        if flag:
            mismatched += 1
        print(f"OBSERVE {row['id']} rc={rc} observed={observed} self={row['status']}{flag}")
    print(f"OBSERVE rows={len(rows)} mismatched={mismatched}")
    return mismatched


def selftest():
    """Prove the validator can fail; every case runs the real row checks on a temp lane."""
    with tempfile.TemporaryDirectory(prefix="routed-open-selftest-") as tmp:
        lane = pathlib.Path(tmp)
        (lane / "lesson.md").write_text("R1 routed\nR2 routed\n")
        good = {"id": "R99-R1", "class": "t", "source": "lesson.md:1", "opened_round": 99,
                "status": "closed", "close": "abc123 lesson.md:2", "blocker": None,
                "check": None, "note": None}
        cases = [
            ("valid-closed", [good], 0),
            ("malformed-json", ['{"id": "R99-R2"'], 1),
            ("missing-key", [{k: v for k, v in good.items() if k != "class"}], 1),
            ("duplicate-id", [good, good], 1),
            ("closed-without-evidence", [dict(good, close=None)], 1),
            ("blocked-without-blocker", [dict(good, status="blocked", close=None, blocker=None)], 1),
            ("bad-status", [dict(good, status="done")], 1),
            ("source-past-eof", [dict(good, source="lesson.md:99")], 1),
            ("source-missing-file", [dict(good, source="absent.md:1")], 1),
            ("bad-opened-round", [dict(good, opened_round=0)], 1),
            ("bad-id", [dict(good, id="not a/row")], 1),
        ]
        ok = 0
        for name, rows, want in cases:
            path = lane / f"{name}.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            _rows, defects = load(path, lane)
            rc = 1 if defects else 0
            ok += rc == want
            print(f"SELFTEST {name} rc={rc} want={want} {'ok' if rc == want else 'FAIL'}")
        guards = [is_ledger("corpus/defects.jsonl"), is_ledger("corpus/defects-round35.jsonl"),
                  is_ledger("corpus/routed-findings.jsonl")]
        guard = 2 if guards == [True, True, False] else 0
        ok += guard == 2
        print(f"SELFTEST defect-ledger-guard rc={guard} want=2 {'ok' if guard == 2 else 'FAIL'}")
        total = len(cases) + 1
        print(f"SELFTEST {ok}/{total}")
        return 0 if ok == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--file", default=None, help="JSONL file (default: <lane>/corpus/routed-findings.jsonl)")
    ap.add_argument("--list", action="store_true", help="print one ROW line per finding")
    ap.add_argument("--observe", action="store_true", help="run each row's check against the lane tip")
    ap.add_argument("--timeout", type=int, default=180, help="per-check timeout for --observe")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    lane = pathlib.Path(a.lane).resolve()
    if not lane.is_dir():
        print(f"SETUP lane is not a directory: {a.lane}", file=sys.stderr)
        return 2
    path = pathlib.Path(a.file) if a.file else lane / "corpus/routed-findings.jsonl"
    if is_ledger(path):
        print(f"SETUP refusing {path.name}: the defect ledgers are pinned by plans/ledger_tip.py",
              file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"SETUP routed-findings file missing: {path}", file=sys.stderr)
        return 2
    rows, defects = load(path, lane)
    for number, reason in defects:
        print(f"DEFECT line={number} {reason}")
    if defects:
        print(f"ROWS total={len(rows) + len(defects)} invalid={len(defects)}")
        return 1
    counts, pending, oldest = tally(rows)
    if a.list:
        for row in rows:
            print(f"ROW {row['id']} status={row['status']} opened={row['opened_round']} source={row['source']}")
    status = 0
    if a.observe:
        status = 1 if observe(rows, lane, a.timeout) else 0
    print(f"ROWS total={len(rows)} open={counts['open']} blocked={counts['blocked']} "
          f"closed={counts['closed']} refused={counts['refused']}")
    print(f"routed_open={pending} oldest_round={oldest if oldest is not None else '-'}")
    return status


if __name__ == "__main__":
    sys.exit(main())
