#!/usr/bin/env python3
"""R90-C3 gate — routed-findings burn-down and the freeze rule (considerthese/2026-10-26.md item 1).

Ledger: `corpus/routed-findings.jsonl`, one row per routed finding, append-only. A base row states
a finding once (id unique forever). A resolution row is a NEW row carrying `"supersedes": "<id>"`
plus the finding's current state — the base row is never edited. The ledger's only writer is the
round process; `plans/routed_open.py` (round 41) stays untouched and uninvoked by this gate.

Row fields (base and resolution rows): id, class, source (`<repo-relative path>:<line>`, validated
against the bytes at the measured revision), opened_round (int >= 1), status
(open | closed | refused | blocked); closed rows carry closing evidence in `close`, refused/blocked
rows name their `blocker`; an optional `check` is a shell command that exits 0 exactly when the
routed work is done — the gate runs it for every effectively-closed row and treats a nonzero exit
as a defect, so a close without the work fails closed.

Freeze rule (wired from round 91 on: every freeze commit of a new coverage claim cites a
`freeze=admitted` run at `--freeze-round <N>`): a freeze of round N is refused while any finding
is effectively pending (status open or blocked after resolution) whose opened_round is older than
N-2. A refusal is the honest outcome; it exits 1 with `freeze=refused`. The ledger is read from
the measured revision; a row's `check` command runs against the lane working tree with `$LANE` set
to the lane root — the tree is the surface a round-close triage verifies.

Prints one `DEFECT <reason>` line per invalid row or failed check, one summary line, and one
`PREDICATE R90-C3 pass|fail` line. Predicate pass requires: freeze admitted (or the ledger's
pending set is empty), no unresolved malformed row, no duplicate id, no failed check, every
closed row carrying closing evidence and every refused/blocked row naming its blocker.

Usage:  python3 plans/round90_burndown.py --lane <repo> --rev <rev> --work <dir> --freeze-round <N>
        (--file <path> reads a fixture ledger instead of git objects; selftest-only)
Exit:   0 predicate pass, 1 predicate fail (refusal, defect, or failed selftest case),
        2 could not evaluate (unresolved revision, unreadable ledger, no git).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

LEDGER = "corpus/routed-findings.jsonl"
STATUSES = ("open", "closed", "refused", "blocked")
REQUIRED = ("id", "class", "source", "opened_round", "status")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SOURCE_RE = re.compile(r"(.+):([0-9]+)\Z")


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

    def blob(self, path: str, rev: str) -> bytes | None:
        proc = self.git("show", f"{rev}:{path}")
        return proc.stdout if proc.returncode == 0 else None

    def blob_lines(self, path: str, rev: str) -> list[str] | None:
        raw = self.blob(path, rev)
        return None if raw is None else raw.decode("utf-8", errors="replace").splitlines()


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
    check = obj.get("check")
    if check is not None and (not isinstance(check, str) or not check.strip()):
        return "check must be null or a non-empty shell command"
    supersedes = obj.get("supersedes")
    if supersedes is not None and (not isinstance(supersedes, str) or not ID_RE.match(supersedes)):
        return "supersedes must name a row id"
    return None


def load_ledger(text: str, source_lines: dict[str, list[str]]) -> tuple[list[dict], list[tuple[int, str]]]:
    """Parse rows; keep malformed lines as (line-number, best-effort-id-or-empty) defects."""
    rows: list[dict] = []
    defects: list[tuple[int, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            defects.append((number, "malformed JSON"))
            continue
        reason = validate(obj, source_lines)
        if reason:
            defects.append((number, reason))
            continue
        sid = obj["id"]
        if sid in seen:
            defects.append((number, f"duplicate id {sid}"))
            continue
        seen.add(sid)
        obj["_line"] = number
        rows.append(obj)
    return rows, defects


def effective_state(rows: list[dict], parse_defects: list[tuple[int, str]]) \
        -> tuple[dict[str, str], dict[str, dict], list[str]]:
    """Resolve supersedes; return {finding-id: effective status}, {id: deciding row}, extra defects."""
    defects: list[str] = []
    supersedes_by_target: dict[str, dict] = {}
    for row in rows:
        target = row.get("supersedes")
        if target is None:
            continue
        known = {r["id"] for r in rows}
        malformed_ids = {d_id for _, d_id in parse_defects if d_id}
        if target not in known and target not in malformed_ids:
            defects.append(f"supersedes-unknown {row['id']} -> {target}")
            continue
        if target in supersedes_by_target:
            defects.append(f"supersedes-duplicate {row['id']} -> {target}")
            continue
        supersedes_by_target[target] = row
    state: dict[str, str] = {}
    deciding: dict[str, dict] = {}
    for row in rows:
        sid = row["id"]
        resolution = supersedes_by_target.get(sid)
        if resolution is not None:
            state[sid] = resolution["status"]
            deciding[sid] = resolution
        else:
            state[sid] = row["status"]
            deciding[sid] = row
    for number, reason in parse_defects:
        if reason == "malformed JSON":
            continue  # an unparseable row has no id; only a resolution naming one can clear it
        pass
    for row in rows:
        if row.get("supersedes") is not None:
            target = row["supersedes"]
            if target not in state and not any(d_id == target for _, d_id in parse_defects):
                pass  # already reported by supersedes-unknown
    return state, deciding, defects


def run_check(command: str, lane_root: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(["sh", "-c", command], cwd=lane_root, capture_output=True,
                              text=True, timeout=120,
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
                malformed_lines += 1  # duplicate id: counted as an invalid line and a defect below
                continue
            seen.add(sid)
            obj["_line"] = number
            valid_rows.append(obj)
        elif have_id:
            if sid not in invalid_named:
                invalid_named[sid] = (number, reason)
        else:
            malformed_lines += 1

    defects: list[str] = []
    for sid, (number, reason) in sorted(invalid_named.items(), key=lambda kv: kv[1][0]):
        defects.append(f"line {number}: {sid}: {reason}")

    # supersedes resolution: one well-formed resolution row per target id
    supersedes_by_target: dict[str, dict] = {}
    for row in valid_rows:
        target = row.get("supersedes")
        if target is None:
            continue
        if target not in seen and target not in invalid_named:
            defects.append(f"supersedes-unknown {row['id']} -> {target}")
            continue
        if target in supersedes_by_target:
            defects.append(f"supersedes-duplicate {row['id']} -> {target}")
            continue
        supersedes_by_target[target] = row

    # effective status per finding: the base row's status unless a resolution supersedes it
    state: dict[str, str] = {}
    opened: dict[str, int] = {}
    for row in valid_rows:
        if row.get("supersedes") is not None:
            continue
        resolution = supersedes_by_target.get(row["id"])
        state[row["id"]] = (resolution or row)["status"]
        opened[row["id"]] = row["opened_round"]
    for sid in invalid_named:
        resolution = supersedes_by_target.get(sid)
        if resolution is not None:
            state[sid] = resolution["status"]
            opened[sid] = resolution["opened_round"]
        else:
            state[sid] = "open"  # an invalid row stays pending until a resolution clears it
            opened[sid] = 10_000  # unknown age keeps it pending but never the sole "oldest"
            defects.append(f"invalid-row-unresolved {sid}")

    # checks: every effectively-closed finding whose row names a check command must pass it
    checks_run = 0
    base_by_id = {row["id"]: row for row in valid_rows}
    for row in valid_rows:
        target = row.get("supersedes")
        deciding = row if target is not None else supersedes_by_target.get(row["id"], row)
        if deciding.get("status") != "closed":
            continue
        base = base_by_id.get(target) if target is not None else row
        command = deciding.get("check") or (base or {}).get("check")
        if not command:
            continue
        checks_run += 1
        rc, output = run_check(command, lane.root)
        if rc != 0:
            defects.append(f"check-failed {deciding.get('id', row['id'])} rc={rc} {output!r}")

    pending = [sid for sid, status in state.items() if status in ("open", "blocked")]
    oldest = min((opened[sid] for sid in pending), default=None)
    resolutions = sum(1 for row in valid_rows if row.get("supersedes") is not None)
    seeds = sum(1 for row in valid_rows
                if row.get("supersedes") is None and 83 <= row["opened_round"] <= 89)
    unresolved_invalid = sum(1 for sid in invalid_named if state.get(sid) in ("open", "blocked"))

    if freeze_round is not None:
        refuse = bool(pending) and oldest is not None and oldest < freeze_round - 2
        verdict = "refused" if refuse else "admitted"
    else:
        verdict = "admitted" if not pending else "pending-only"
    lines_out = [f"ROWS total={len(valid_rows) + len(invalid_named) + malformed_lines} "
                 f"valid={len(valid_rows)} invalid={len(invalid_named) + malformed_lines} "
                 f"superseded={resolutions}"]
    for d in defects:
        lines_out.append(f"DEFECT {d}")
    lines_out.append(f"freeze={verdict} "
                     f"oldest_pending_round={oldest if oldest is not None else '-'} "
                     f"pending={len(pending)} malformed_unresolved={unresolved_invalid + malformed_lines} "
                     f"seeds_83_89={seeds} resolutions={resolutions} checks_run={checks_run}")
    passed = (verdict != "refused") and not defects \
        and (unresolved_invalid + malformed_lines) == 0
    lines_out.append(f"PREDICATE R90-C3 {'pass' if passed else 'fail'}")
    return lines_out, (0 if passed else 1)


def selftest(work: Path) -> int:
    """Seven fixture ledgers proving the gate fails before it passes."""
    cases: list[tuple[str, str, int | None, int]] = []

    base_open = {"id": "OLD-1", "class": "x", "source": "notes.md:2", "opened_round": 39,
                 "status": "open", "close": None, "blocker": None, "check": None}
    notes = "# notes\nsome anchor line\n"
    resolution = dict(base_open, id="OLD-1-res", status="closed",
                      close="commit abc dead-beef", supersedes="OLD-1")
    refused_row = dict(base_open, id="OLD-1-res", status="refused",
                       blocker="declined round 90", supersedes="OLD-1")

    cases.append(("old-open-refuses",
                  json.dumps(base_open) + "\n", 90, 1))
    cases.append(("resolved-admits",
                  json.dumps(base_open) + "\n" + json.dumps(resolution) + "\n", 90, 0))
    cases.append(("refused-admits",
                  json.dumps(base_open) + "\n" + json.dumps(refused_row) + "\n", 90, 0))
    cases.append(("closed-check-fails",
                  json.dumps(base_open) + "\n" +
                  json.dumps(dict(resolution, check="exit 3")) + "\n", 90, 1))
    cases.append(("supersede-unknown",
                  json.dumps(base_open) + "\n" +
                  json.dumps(dict(resolution, supersedes="NOPE")) + "\n", 90, 1))
    cases.append(("fresh-open-admits",
                  json.dumps(dict(base_open, opened_round=89)) + "\n", 90, 0))
    cases.append(("malformed-refuses",
                  "{not json\n" + json.dumps(dict(base_open, id="OTHER-1")) + "\n", 90, 1))

    ok = 0
    for name, ledger_text, freeze_round, want in cases:
        d = work / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "notes.md").write_text(notes, encoding="utf-8")
        (d / "fixture.jsonl").write_text(ledger_text, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--lane", str(d),
             "--file", "fixture.jsonl", "--freeze-round", str(freeze_round), "--work", str(d)],
            capture_output=True, text=True, timeout=120, env={"PATH": "/usr/bin:/bin"})
        got = proc.returncode
        passed = got == want
        print(f"SELFTEST {name} rc={got} want={want} ok={passed}")
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
                print("PREDICATE R90-C3 could-not-evaluate")
                return 2
            lines = fixture.read_text(errors="replace").splitlines()
            # --file mode validates sources against the lane working tree, never git objects
            class FileLane:  # minimal stand-in with the one method evaluate() needs
                def resolve(self, _rev: str) -> str:
                    return "fixture"
                def blob_lines(self, path: str, _rev: str) -> list[str] | None:
                    return lines if path == LEDGER else \
                        (lane_root / path).read_text(errors="replace").splitlines() \
                        if (lane_root / path).is_file() else None
            lines_out, code = evaluate(FileLane(), "fixture", args.freeze_round)
        else:
            lane = Lane(lane_root)
            rev_sha = lane.resolve(args.rev)
            lines_out, code = evaluate(lane, args.rev, args.freeze_round)
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R90-C3 could-not-evaluate")
        return 2
    for line in lines_out:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
