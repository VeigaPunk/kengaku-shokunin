#!/usr/bin/env python3
"""R90-C2 checker — external pins over the lane's frozen counters and the round-89 record table.

Round 89's counters carry their pins inside themselves (`TRUSTED_TOOL_SHA` constants); SentinelR89
H1–H3 showed a writer who can edit the tree can rewrite both sides of such a self-pin in one
commit. This instrument moves the pins outside the pinned bytes: `plans/counter-pins-r90.json`
lists, per frozen instrument, the sha256 of its bytes as committed beside them, plus the git blob
of the round-89 record table at its creating commit. At any measured revision the checker verifies
bytes-at-revision against the pins. An absent pinned path is a `PIN-MISMATCH absent`, never a
skip: missing output fails closed (kagi r33/r34 lesson).

Pinned set (frozen in plans/round-90-claims.md): plans/round88_claim_figures.py,
plans/round89_c1_replay.py, plans/round89_claim_figures.py, plans/round90_c1_replay.py,
plans/round90_polydiff_probe.py, plans/round90_burndown.py, and the record table blob
163f284316141a831484dacb7f69ad4cbbaadfb3 (anchor commit 0e6bb05f…, the table's creating commit —
the r89 spot-check's "freeze-commit blob" is impossible: the table does not exist at d1c4f1b0).

Honest limit: a writer who can edit the tree can rewrite this pin ledger too, in one commit. The
residual is the round-89 disclosure narrowed — the adversary now edits a third file whose diff any
review sees — and is disclosed here, not hidden.

Usage:  python3 plans/round90_counter_pin.py --lane <repo> --rev <rev> [--work <dir>] [--selftest]
Exit:   0 all pins match and selftest green (when run), 1 a mismatch or a failed selftest case,
        2 could not evaluate (unresolved revision, unreadable pin ledger, missing git).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PIN_FILE = "plans/counter-pins-r90.json"
RECORD_TABLE = "plans/round89-q66-records.json"
RECORD_BLOB = "163f284316141a831484dacb7f69ad4cbbaadfb3"
RECORD_ANCHOR = "0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619"
EXPECTED_PINS = (
    "plans/round88_claim_figures.py",
    "plans/round89_c1_replay.py",
    "plans/round89_claim_figures.py",
    "plans/round90_c1_replay.py",
    "plans/round90_polydiff_probe.py",
    "plans/round90_burndown.py",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=120)

    def resolve(self, rev: str) -> str | None:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        return proc.stdout.decode().strip() if proc.returncode == 0 else None

    def blob(self, path: str, rev: str) -> bytes | None:
        proc = self.git("show", f"{rev}:{path}")
        return proc.stdout if proc.returncode == 0 else None

    def blob_id(self, path: str, rev: str) -> str | None:
        proc = self.git("rev-parse", f"{rev}:{path}")
        return proc.stdout.decode().strip() if proc.returncode == 0 else None


def load_pins(lane: Lane, rev_sha: str) -> list[dict] | None:
    raw = lane.blob(PIN_FILE, rev_sha)
    if raw is None:
        return None
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return None
    pins = doc.get("pins")
    if not isinstance(pins, list):
        return None
    return pins


def check(lane: Lane, rev: str) -> tuple[int, int, int, list[str]]:
    rev_sha = lane.resolve(rev)
    if rev_sha is None:
        return 0, 0, 0, [f"DEFECT SETUP unresolved-revision {rev}"]
    pins = load_pins(lane, rev_sha)
    if pins is None:
        return 0, 0, 0, [f"DEFECT SETUP unreadable {PIN_FILE} at {rev_sha[:12]}"]
    mismatched = 0
    details: list[str] = []
    seen = set()
    for pin in pins:
        path = pin.get("path")
        want = pin.get("sha256")
        if not isinstance(path, str) or not isinstance(want, str):
            mismatched += 1
            details.append(f"PIN-MISMATCH schema {path!r}")
            continue
        if path in seen:
            mismatched += 1
            details.append(f"PIN-MISMATCH duplicate {path}")
        seen.add(path)
        got_bytes = lane.blob(path, rev_sha)
        if got_bytes is None:
            mismatched += 1
            details.append(f"PIN-MISMATCH absent {path} at {rev_sha[:12]}")
        elif sha256(got_bytes) != want:
            mismatched += 1
            details.append(f"PIN-MISMATCH bytes {path} got={sha256(got_bytes)[:16]} want={want[:16]}")
    missing_set = [p for p in EXPECTED_PINS if p not in seen]
    for path in missing_set:
        mismatched += 1
        details.append(f"PIN-MISMATCH pin-file-missing-entry {path}")
    blob = lane.blob_id(RECORD_TABLE, rev_sha)
    record_ok = blob == RECORD_BLOB
    if blob is None:
        details.append(f"RECORD-TABLE absent {RECORD_TABLE} at {rev_sha[:12]}")
        mismatched += 1
    elif record_ok:
        details.append(f"RECORD-TABLE blob={blob[:16]} matched")
    else:
        details.append(f"RECORD-TABLE blob={blob[:16]} != pinned {RECORD_BLOB[:16]}")
        mismatched += 1
    counted = len(pins) + 1
    matched = max(counted - mismatched, 0)
    return counted, matched, mismatched, details


def selftest(lane_root: Path, work: Path) -> int:
    """Five cases over synthetic commit fixtures; every red case must be red.

    Fixtures never touch the lane: each case builds a fresh scratch repo. The real record-table
    bytes are copied from the lane working tree so a green case can reproduce the pinned blob id.
    Fixtures are written through fresh inodes only (no hardlinks), per QUALITY Q64.
    """
    record_bytes = (lane_root / RECORD_TABLE).read_bytes() if (lane_root / RECORD_TABLE).is_file() \
        else b"record-v1\n"

    def fixture(name: str, commits: list[dict[str, str]]) -> tuple[Lane, str] | None:
        d = work / name
        d.mkdir(parents=True, exist_ok=True)
        env = {"PATH": "/usr/bin", "GIT_CONFIG_GLOBAL": "/dev/null",
               "GIT_CONFIG_SYSTEM": "/dev/null", "HOME": str(d)}
        subprocess.run(["git", "init", "-q", "-b", "master"], cwd=d, capture_output=True)
        head = None
        for index, files in enumerate(commits, 1):
            for fname, content in files.items():
                target = d / fname
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content.encode("utf-8"))
                subprocess.run(["git", "add", fname], cwd=d, capture_output=True, env=env)
            r = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                                "commit", "-q", "--allow-empty", "-m", f"c{index}"],
                               cwd=d, capture_output=True, env=env)
            if r.returncode != 0:
                return None
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d,
                                  capture_output=True, env=env).stdout.decode().strip()
        return Lane(d), head

    counter_original = "def check():\n    return 1\n"
    counter_mutated = "def check():\n    return 2\n"

    ok = 0
    total = 0

    def pins_single(content: str) -> list[dict]:
        return [{"path": "plans/fake_counter.py", "sha256": sha256(content.encode("utf-8"))}]

    # T1 modified-counter: pins pin the c1 bytes; c2 mutates one byte -> PIN-MISMATCH bytes
    total += 1
    got = fixture("t1", [
        {"plans/fake_counter.py": counter_original,
         "plans/counter-pins-r90.json": json.dumps({"pins": pins_single(counter_original)})},
        {"plans/fake_counter.py": counter_mutated},
    ])
    if got is None:
        print("SELFTEST modified-counter setup-fail")
    else:
        lane, rev = got
        _, _, mismatched, details = check(lane, rev)
        red = any("PIN-MISMATCH bytes plans/fake_counter.py" in x for x in details)
        print(f"SELFTEST modified-counter {'red' if red else 'GREEN'} want=red ok={red}")
        ok += red

    # T2 modified-record-table: blob changes at c2 -> record-table mismatch against the pinned blob
    total += 1
    got = fixture("t2", [
        {RECORD_TABLE: record_bytes.decode("utf-8", errors="replace"),
         "plans/counter-pins-r90.json": json.dumps({"pins": pins_single("x")})},
        {RECORD_TABLE: record_bytes.decode("utf-8", errors="replace") + "# drift\n"},
    ])
    if got is None:
        print("SELFTEST modified-record-table setup-fail")
    else:
        lane, rev = got
        _, _, mismatched, details = check(lane, rev)
        red = any("!= pinned" in x for x in details)
        print(f"SELFTEST modified-record-table {'red' if red else 'GREEN'} want=red ok={red}")
        ok += red

    # T3 absent-path fail-closed: the pin names a path committed nowhere -> PIN-MISMATCH absent
    total += 1
    got = fixture("t3", [
        {"plans/counter-pins-r90.json": json.dumps(
            {"pins": [{"path": "plans/ghost.py", "sha256": "0" * 64}]})},
    ])
    if got is None:
        print("SELFTEST absent-path setup-fail")
    else:
        lane, rev = got
        _, _, mismatched, details = check(lane, rev)
        red = any("PIN-MISMATCH absent plans/ghost.py" in x for x in details)
        print(f"SELFTEST absent-path {'red' if red else 'GREEN'} want=red ok={red}")
        ok += red

    # T4 clean green: all six frozen pin paths plus the record table byte-identical across two commits
    total += 1
    stubs = {p: f"pin-stub {p}\n" for p in EXPECTED_PINS}
    pins_all = [{"path": p, "sha256": sha256(c.encode("utf-8"))} for p, c in stubs.items()]
    files_c1 = dict(stubs)
    files_c1[RECORD_TABLE] = record_bytes.decode("utf-8", errors="replace")
    files_c1["plans/counter-pins-r90.json"] = json.dumps({"pins": pins_all})
    got = fixture("t4", [files_c1, {"README.md": "no byte changes to pinned files\n"}])
    if got is None:
        print("SELFTEST clean-green setup-fail")
    else:
        lane, rev = got
        _, _, mismatched, details = check(lane, rev)
        green = mismatched == 0
        print(f"SELFTEST clean-green {'green' if green else 'RED'} want=green ok={green}")
        ok += green

    # T5 incomplete pin set: a pin ledger naming fewer than the frozen paths is a mismatch
    total += 1
    got = fixture("t5", [
        {"plans/counter-pins-r90.json": json.dumps(
            {"pins": [{"path": "plans/only_one.py", "sha256": "0" * 64}]})},
    ])
    if got is None:
        print("SELFTEST incomplete-pin-set setup-fail")
    else:
        lane, rev = got
        _, _, mismatched, details = check(lane, rev)
        red = any("pin-file-missing-entry" in x for x in details)
        print(f"SELFTEST incomplete-pin-set {'red' if red else 'GREEN'} want=red ok={red}")
        ok += red

    print(f"SELFTEST cases={total} red-green-ok={ok}")
    return 0 if ok == total else 1


def run(lane_root: Path, rev: str, want_selftest: bool, work: Path) -> int:
    lane = Lane(lane_root)
    if want_selftest:
        return selftest(lane_root, work)
    checked, matched, mismatched, details = check(lane, rev)
    for line in details:
        print(line)
    if checked == 0 and mismatched == 0:
        print("PREDICATE R90-C2 could-not-evaluate")
        return 2
    print(f"PINS checked={checked} matched={matched} mismatched={mismatched}")
    verdict = "pass" if mismatched == 0 else "fail"
    print(f"PREDICATE R90-C2 {verdict}")
    return 0 if mismatched == 0 else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--work", help="scratch directory for the selftest fixtures")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    work = Path(args.work).resolve() if args.work else None
    if args.selftest and work is None:
        print("DEFECT SETUP --selftest requires --work")
        return 2
    if work is None:
        work = Path(tempfile.mkdtemp(prefix="r90pin-"))
    return run(Path(args.lane).resolve(), args.rev, args.selftest, work)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
