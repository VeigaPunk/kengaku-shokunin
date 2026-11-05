#!/usr/bin/env python3
"""R91-C3 gate — the routed-findings freeze gate v2 (round 91 successor to plans/round90_burndown.py).

Amendments the round-90 routing and Q68/Q69 demand, all computed inside the PREDICATE (never only
printed): a well-formed resolution that supersedes a named-invalid row clears it and emits no
DEFECT; the freeze verdict is `refused` whenever any check fails, not only when pending rows are
old; the seed clause is a conjoined PREDICATE clause; every check override is printed together
with its base check's result and requires a non-empty `override_reason`; the `--file` route gives
the check runner a real root so its selftest exercises the same read path; checks run once per
finding; every selftest case is red for its named reason. Decided-state mapping (frozen in
`plans/round-91-claims.md` before data): `pending` counts effectively-open rows only; `blocked`
rows are parked and every blocked row must name a non-empty `owner`; `refused` rows stay decided.

Usage:  python3 plans/round91_burndown.py --lane <repo> --rev <rev> --work <dir> --freeze-round N
        [--file <fixture ledger>] [--selftest]
Exit:   0 predicate pass, 1 predicate fail, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LEDGER = "corpus/routed-findings.jsonl"
STATUSES = ("open", "closed", "refused", "blocked")
REQUIRED = ("id", "class", "source", "opened_round", "status")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SOURCE_RE = re.compile(r"(.+):([0-9]+)\Z")
SEED_MIN = 6
SEED_FIRST_ROUND = 83


class CouldNotEvaluate(Exception):
    """An input the gate needs cannot be read at all."""


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=120)

    def resolve(self, rev: str) -> str:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"unresolved-revision {rev}")
        return proc.stdout.decode().strip()

    def blob_lines(self, path: str, rev: str) -> list[str] | None:
        proc = self.git("show", f"{rev}:{path}")
        return None if proc.returncode != 0 else proc.stdout.decode("utf-8", errors="replace").splitlines()


def validate(obj: object, source_lines: dict[str, list[str]]) -> str | None:
    """One parsed row -> None, or the reason it is a defect."""
    if not isinstance(obj, dict):
        return "row is not a JSON object"
    missing = [k for k in REQUIRED if k not in obj]
    if missing:
        return f"missing keys: {','.join(missing)}"
    sid = obj["id"]
    if not isinstance(sid, str) or not ID_RE.match(sid):
        return "id must match [A-Za-z0-9][A-Za-z0-9._-]*"
    if not isinstance(obj["class"], str) or not obj["class"].strip():
        return "class must be a non-empty string"
    source = obj["source"]
    if not isinstance(source, str):
        return "source must be a string"
    m = SOURCE_RE.match(source)
    if not m:
        return "source must read <path>:<line>"
    relative, line_no = m.group(1), int(m.group(2))
    pure = Path(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        return f"source path escapes the lane: {relative}"
    lines = source_lines.get(relative)
    if lines is None:
        return f"source file missing at revision: {relative}"
    if line_no < 1 or line_no > len(lines) or not lines[line_no - 1].strip():
        return f"source line {line_no} is blank or past the end of {relative}"
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
    if status == "blocked" and not (obj.get("owner") or "").strip():
        return "a blocked row must name its owner"
    owner = obj.get("owner")
    if owner is not None and (not isinstance(owner, str) or not owner.strip()):
        return "owner must be null or a non-empty string"
    override_reason = obj.get("override_reason")
    if override_reason is not None and (not isinstance(override_reason, str) or not override_reason.strip()):
        return "override_reason must be null or a non-empty string"
    check = obj.get("check")
    if check is not None and (not isinstance(check, str) or not check.strip()):
        return "check must be null or a non-empty shell command"
    supersedes = obj.get("supersedes")
    if supersedes is not None and (not isinstance(supersedes, str) or not ID_RE.match(supersedes)):
        return "supersedes must name a row id"
    return None


def run_check(command: str, lane_root: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(["sh", "-c", command], cwd=lane_root, capture_output=True,
                              text=True, timeout=300,
                              env={"PATH": "/usr/bin:/bin", "HOME": str(lane_root),
                                   "LANE": str(lane_root)})
    except (OSError, subprocess.SubprocessError) as error:
        return 2, f"check-unrunnable {error}"
    return proc.returncode, (proc.stdout or proc.stderr).strip()[-200:]


def evaluate(lane: Lane, rev: str, freeze_round: int | None) -> tuple[list[str], int]:
    rev_sha = lane.resolve(rev)
    lines = lane.blob_lines(LEDGER, rev_sha)
    if lines is None:
        raise CouldNotEvaluate(f"{LEDGER} absent at {rev_sha[:12]}")
    source_lines: dict[str, list[str]] = {}

    def lines_for(relative: str) -> list[str] | None:
        if relative not in source_lines:
            source_lines[relative] = lane.blob_lines(relative, rev_sha) or []
        return source_lines[relative] or None

    # pass 1: parse every line; schema-invalid rows stay named so a resolution can clear them
    valid_rows: list[dict] = []
    invalid_named: dict[str, tuple[int, str]] = {}
    malformed_lines = 0
    seen: set[str] = set()
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            malformed_lines += 1
            continue
        if not isinstance(obj, dict):
            malformed_lines += 1
            continue
        sid = obj.get("id")
        have_id = isinstance(sid, str) and bool(ID_RE.match(sid))
        if have_id and isinstance(obj.get("source"), str):
            m = SOURCE_RE.match(obj["source"])
            if m:
                lines_for(m.group(1))
        reason = validate(obj, source_lines)
        if reason is None:
            if sid in seen:
                malformed_lines += 1  # duplicate id: an invalid line, reported below
                continue
            seen.add(sid)
            obj["_line"] = number
            valid_rows.append(obj)
        elif have_id:
            if sid not in invalid_named:
                invalid_named[sid] = (number, reason)
        else:
            malformed_lines += 1

    # supersedes resolution: one well-formed resolution row per target id
    supersedes_by_target: dict[str, dict] = {}
    for row in valid_rows:
        target = row.get("supersedes")
        if target is None:
            continue
        if target not in seen and target not in invalid_named:
            pass  # reported as a supersedes-unknown defect below
        elif target in supersedes_by_target:
            pass  # reported as a supersedes-duplicate defect below
        else:
            supersedes_by_target[target] = row

    defects: list[str] = []
    for row in valid_rows:
        target = row.get("supersedes")
        if target is None:
            continue
        if target not in seen and target not in invalid_named:
            defects.append(f"supersedes-unknown {row['id']} -> {target}")
        elif sum(1 for r in valid_rows if r.get("supersedes") == target) > 1:
            defects.append(f"supersedes-duplicate {row['id']} -> {target}")

    # effective status per finding: the base row's status unless a resolution supersedes it.
    # A named-invalid row that a well-formed resolution supersedes is CLEAR (no DEFECT): the
    # resolution's own schema validity was enforced above (round-90 PASS IS UNREACHABLE fix).
    state: dict[str, str] = {}
    opened: dict[str, int] = {}
    deciding_row: dict[str, dict] = {}
    base_row: dict[str, dict] = {}
    for row in valid_rows:
        if row.get("supersedes") is not None:
            continue
        resolution = supersedes_by_target.get(row["id"])
        state[row["id"]] = (resolution or row)["status"]
        opened[row["id"]] = row["opened_round"]
        base_row[row["id"]] = row
        deciding_row[row["id"]] = resolution or row
    superseded_invalid: set[str] = set()
    for sid in invalid_named:
        resolution = supersedes_by_target.get(sid)
        if resolution is not None:
            state[sid] = resolution["status"]
            opened[sid] = resolution.get("opened_round", 10_000)
            base_row[sid] = {"id": sid, "check": None, "_line": invalid_named[sid][0]}
            deciding_row[sid] = resolution
            superseded_invalid.add(sid)
        else:
            state[sid] = "open"  # an unresolved invalid row stays pending
            opened[sid] = 10_000  # unknown age keeps it pending but never the sole "oldest"
            defects.append(f"line {invalid_named[sid][0]}: {sid}: {invalid_named[sid][1]}")

    # checks: run ONCE PER FINDING; every override is printed with its base check's result and
    # requires override_reason (SentinelForge H-2a / M11); the base check runs too.
    checks_run = 0
    check_failed = False
    overrides = 0
    for sid, deciding in deciding_row.items():
        if deciding.get("status") != "closed":
            continue
        base = base_row.get(sid, {})
        base_cmd = base.get("check")
        override_cmd = deciding.get("check")
        is_override = override_cmd is not None and base_cmd is not None and override_cmd != base_cmd \
            and (deciding.get("supersedes") is not None)
        if is_override:
            overrides += 1
            if not (deciding.get("override_reason") or "").strip():
                defects.append(f"override-unjustified {sid}")
            base_rc, base_out = run_check(base_cmd, lane.root)
            ovr_rc, ovr_out = run_check(override_cmd, lane.root)
            checks_run += 2
            print(f"CHECK {sid} base-rc={base_rc} base={base_cmd!r} "
                  f"override-rc={ovr_rc} override={override_cmd!r} "
                  f"reason={deciding.get('override_reason')!r} base_out={base_out[:60]!r}")
            if ovr_rc != 0:
                defects.append(f"check-failed {sid} rc={ovr_rc} {ovr_out!r}")
                check_failed = True
        else:
            command = override_cmd or base_cmd
            if not command:
                continue
            rc, output = run_check(command, lane.root)
            checks_run += 1
            if rc != 0:
                defects.append(f"check-failed {sid} rc={rc} {output!r}")
                check_failed = True

    pending = [sid for sid, status in state.items() if status == "open"]
    parked = [sid for sid, status in state.items() if status == "blocked"]
    unowned = [sid for sid in parked if not (deciding_row[sid].get("owner") or "").strip()]
    oldest = min((opened[sid] for sid in pending), default=None)
    resolutions = sum(1 for row in valid_rows if row.get("supersedes") is not None)
    unresolved_invalid = sum(1 for sid in invalid_named if sid not in superseded_invalid)
    unresolved_malformed = malformed_lines

    if freeze_round is not None:
        window_last = freeze_round - 1
        seeds = sum(1 for row in valid_rows
                    if row.get("supersedes") is None
                    and SEED_FIRST_ROUND <= row["opened_round"] <= window_last)
        refuse = (
            (bool(pending) and oldest is not None and oldest < freeze_round - 2)
            or check_failed
            or unresolved_invalid > 0
            or unresolved_malformed > 0
            or bool(unowned)
        )
        verdict = "refused" if refuse else "admitted"
    else:
        window_last = None
        seeds = sum(1 for row in valid_rows
                    if row.get("supersedes") is None and row["opened_round"] >= SEED_FIRST_ROUND)
        verdict = "admitted" if not pending else "pending-only"

    lines_out = [f"ROWS total={len(valid_rows) + len(invalid_named) + malformed_lines} "
                 f"valid={len(valid_rows)} invalid={len(invalid_named) + malformed_lines} "
                 f"superseded={resolutions}"]
    for d in defects:
        lines_out.append(f"DEFECT {d}")
    lines_out.append(f"freeze={verdict} "
                     f"oldest_pending_round={oldest if oldest is not None else '-'} "
                     f"pending={len(pending)} parked={len(parked)} unowned_blocked={len(unowned)} "
                     f"malformed_unresolved={unresolved_invalid + unresolved_malformed} "
                     + (f"seeds_83_{window_last}={seeds} " if window_last is not None else f"seeds_83plus={seeds} ")
                     + f"resolutions={resolutions} checks_run={checks_run} overrides={overrides}")
    seeds_ok = seeds >= SEED_MIN
    lines_out.append(f"SEEDS window=83-{window_last if window_last is not None else 'plus'} "
                     f"count={seeds} min={SEED_MIN} ok={seeds_ok}")
    passed = (verdict == "admitted" if freeze_round is not None else not pending) \
        and not defects and unresolved_invalid + unresolved_malformed == 0 and seeds_ok
    lines_out.append(f"PREDICATE R91-C3 {'pass' if passed else 'fail'}")
    return lines_out, (0 if passed else 1)


def selftest(work: Path) -> int:
    """Ten fixture ledgers; every red case is red for its named reason (Q69)."""
    notes = "# notes\nsome anchor line\n"
    base_open = {"id": "OLD-1", "class": "x", "source": "notes.md:2", "opened_round": 39,
                 "status": "open", "close": None, "blocker": None, "check": None, "owner": None}
    base_with_check = dict(base_open, check="exit 0")
    base_failing_check = dict(base_open, check="exit 9")
    resolution = dict(base_open, id="OLD-1-res", status="closed",
                      close="commit abc dead-beef", supersedes="OLD-1")
    blocked_unowned = dict(base_open, id="B-1", status="blocked", blocker="held upstream",
                           opened_round=85, owner=None)
    blocked_owned = dict(blocked_unowned, owner="kama")
    override = dict(resolution, check="true",
                    override_reason="base check is stale; the closing evidence is the re-run")
    no_reason = dict(resolution, check="true", override_reason=None)

    def seeds_six() -> str:
        rows = []
        for n in range(1, 7):
            rows.append(json.dumps({"id": f"SEED-{n}", "class": "x", "source": "notes.md:2",
                                    "opened_round": 88, "status": "refused",
                                    "blocker": f"declined with reason {n}"}) + "\n")
        return "".join(rows)

    seed_row = {"id": "SEED-1", "class": "x", "source": "notes.md:2", "opened_round": 88,
                "status": "refused", "blocker": "declined with reason"}

    def ledger(*rows: dict, extra: str = "", seeds: str = "") -> str:
        return extra + seeds + "".join(json.dumps(r) + "\n" for r in rows)

    cases = [
        # name, ledger text, freeze_round, want rc, want substring
        ("old-open-refuses", ledger(base_open), 90, 1, "freeze=refused"),
        ("resolved-admits", ledger(base_open, resolution, seeds=seeds_six()), 90, 0, "PREDICATE R91-C3 pass"),
        ("fresh-open-admits", ledger(dict(base_open, opened_round=89), seeds=seeds_six()), 90, 0, "PREDICATE R91-C3 pass"),
        ("blocked-unowned-refuses", ledger(blocked_unowned, seeds=seeds_six()), 90, 1, "a blocked row must name its owner"),
        ("blocked-owned-admits", ledger(blocked_owned, seeds=seeds_six()), 90, 0, "PREDICATE R91-C3 pass"),
        ("closed-check-fails", ledger(base_open, dict(resolution, check="exit 3"), seeds=seeds_six()), 90, 1,
         "check-failed OLD-1 rc=3"),
        ("malformed-json-refuses", ledger(base_open, seeds=seeds_six(), extra="{not json\n"), 90, 1, "freeze=refused"),
        ("invalid-superseded-passes",
         ledger(dict(base_open, source="prose not a path"), resolution, seeds=seeds_six()),
         90, 0, "PREDICATE R91-C3 pass"),
        ("invalid-unresolved-refuses",
         ledger(seed_row, extra=json.dumps(dict(base_open, source="prose not a path")) + "\n"),
         90, 1, "source must read <path>:<line>"),
        ("override-unjustified-refuses", ledger(base_with_check, no_reason, seeds=seeds_six()), 90, 1,
         "override-unjustified OLD-1"),
        ("override-with-reason-base-fails-admits",
         ledger(base_failing_check, dict(override, supersedes="OLD-1", check="true"), seeds=seeds_six()), 90, 0,
         "override-rc=0"),
        ("seed-starved-refuses", ledger(base_open, resolution), 90, 1, "SEEDS window=83-89 count=0 min=6 ok=False"),
        ("failing-check-refuses-freeze",
         ledger(base_open, dict(resolution, check="true"), seed_row,
                {"id": "CK-1", "class": "x", "source": "notes.md:2", "opened_round": 89,
                 "status": "closed", "close": "evidence", "check": "exit 4"}), 90, 1, "check-failed CK-1 rc=4"),
    ]
    ok = 0
    here = Path(__file__).resolve().parent
    for name, text, freeze_round, want, want_sub in cases:
        d = work / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "notes.md").write_text(notes, encoding="utf-8")
        (d / "fixture.jsonl").write_text(text, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(here / "round91_burndown.py"), "--lane", str(d),
             "--file", "fixture.jsonl", "--freeze-round", str(freeze_round), "--work", str(d)],
            capture_output=True, text=True, timeout=300, env={"PATH": "/usr/bin:/bin"})
        got = proc.returncode
        passed = got == want and want_sub in proc.stdout
        print(f"SELFTEST {name} rc={got} want={want} substring-ok={want_sub in proc.stdout} ok={passed}")
        ok += passed
    print(f"SELFTEST cases={len(cases)} red-green-ok={ok}")
    return 0 if ok == len(cases) else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--work", required=True)
    parser.add_argument("--freeze-round", type=int, default=None)
    parser.add_argument("--file", default=None, help="fixture ledger (selftest only)")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    lane_root = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if args.selftest:
        return selftest(work)
    try:
        if args.file is not None:
            fixture = lane_root / args.file
            if not fixture.is_file():
                print(f"DEFECT SETUP fixture missing {args.file}")
                print("PREDICATE R91-C3 could-not-evaluate")
                return 2
            lines = fixture.read_text(errors="replace").splitlines()

            class FileLane:  # minimal stand-in WITH a real root so check commands run (F-C3-1 fix)
                root = lane_root

                def resolve(self, _rev: str) -> str:
                    return "fixture"

                def blob_lines(self, path: str, _rev: str) -> list[str] | None:
                    if path == LEDGER:
                        return lines
                    candidate = lane_root / path
                    return candidate.read_text(errors="replace").splitlines() \
                        if candidate.is_file() else None

            lines_out, code = evaluate(FileLane(), "fixture", args.freeze_round)
        else:
            lane = Lane(lane_root)
            rev_sha = lane.resolve(args.rev)
            lines_out, code = evaluate(lane, args.rev, args.freeze_round)
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R91-C3 could-not-evaluate")
        return 2
    for line in lines_out:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
