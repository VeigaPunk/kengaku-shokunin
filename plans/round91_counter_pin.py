#!/usr/bin/env python3
"""R91-C2 checker — the pin set extended to the checker itself, the selftest inside the predicate
path, and fail-closed absence (round 91).

Reads `plans/counter-pins-r91.json` from git objects at --rev. Entries are sha pins (the bytes at
the measured revision must hash to the pin; an absent path is `PIN-MISMATCH absent`, never a skip
— round-90 M9) and blob pins (the blob id at the measured revision must equal the pin and exist at
the entry's anchor commit). The checker's own entry additionally verifies the RUNNING file's bytes
against the pin (`SELF-PIN`), narrowing the round-90 SentinelForge H-1 checker-only-edit residual.
The selftest battery runs inside the default predicate path (round-90 M5), in a scratch work dir:
every declared red case must be red FOR ITS NAMED REASON (Q69) and the unmodified tree must be
green. Frozen inputs that cannot be read at all are `DEFECT SETUP` + exit 2 (Q62), never a
synthetic substitute.

Usage:  python3 plans/round91_counter_pin.py --lane <repo> --rev <rev> --work <scratch dir>
        [--selftest] [--skip-selftest] [--self-entry-path <fixture path for the self-pin leg>]
Exit:   0 predicate pass, 1 a pin mismatch or a selftest case wrong, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PINS = "plans/counter-pins-r91.json"
SELF_PATH = "plans/round91_counter_pin.py"
SELF_ENTRY_FLAG = "--self-entry-path"


class CouldNotEvaluate(Exception):
    pass


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", *args], capture_output=True, timeout=120)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve(lane: Path, rev: str) -> str:
    proc = git(str(lane), "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {rev}")
    return proc.stdout.decode().strip()


def blob(lane: Path, path: str, rev: str) -> bytes | None:
    proc = git(str(lane), "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def blob_id(lane: Path, path: str, rev: str) -> str | None:
    proc = git(str(lane), "rev-parse", "--verify", "--quiet", f"{rev}:{path}")
    return proc.stdout.decode().strip() if proc.returncode == 0 else None


def check_pins(lane: Path, rev: str, self_entry: str, pins_obj: dict) -> tuple[list[str], int, int]:
    """One pass of the pin table at rev. -> (defect lines, matched, checked)."""
    defects: list[str] = []
    matched = checked = 0
    entries = pins_obj.get("entries", [])
    for entry in entries:
        kind = entry.get("kind")
        path = entry.get("path", "?")
        checked += 1
        if kind == "sha":
            data = blob(lane, path, rev)
            pin = entry.get("sha256", "")
            if data is None:
                defects.append("PIN-MISMATCH absent %s" % path)
                continue
            if sha(data) != pin:
                defects.append("PIN-MISMATCH bytes %s" % path)
                continue
            if path == self_entry:
                running = Path(sys.argv[0]).resolve()
                if running.is_file() and sha(running.read_bytes()) != pin:
                    defects.append("SELF-PIN-MISMATCH %s" % path)
                    continue
                if not running.is_file():
                    defects.append("SELF-PIN-MISMATCH unreadable %s" % path)
                    continue
            matched += 1
            print("PIN-OK %s" % path)
        elif kind == "blob":
            pin = entry.get("blob", "")
            anchor = entry.get("anchor_commit", "")
            current = blob_id(lane, path, rev)
            anchored = blob_id(lane, path, anchor) if anchor else None
            if current is None:
                defects.append("RECORD-TABLE absent %s" % path)
            elif current != pin:
                defects.append("RECORD-TABLE mismatch %s %s != %s" % (path, current[:16], pin[:16]))
            elif anchored != pin:
                defects.append("RECORD-TABLE anchor %s (anchor %s holds %s)"
                               % (path, anchor[:12], (anchored or "absent")[:16]))
            else:
                matched += 1
                print("PIN-OK %s" % path)
        else:
            defects.append("PIN-ENTRY unknown kind %s %s" % (kind, path))
    return defects, matched, checked


def run_checker(lane: Path, rev: str, work: Path, self_entry: str, skip_selftest: bool) -> int:
    pins_bytes = blob(lane, PINS, rev)
    if pins_bytes is None:
        print("DEFECT SETUP unreadable %s" % PINS)
        print("PREDICATE R91-C2 could-not-evaluate")
        return 2
    try:
        pins_obj = json.loads(pins_bytes.decode())
    except json.JSONDecodeError as error:
        print("DEFECT SETUP unparsable %s %s" % (PINS, error))
        print("PREDICATE R91-C2 could-not-evaluate")
        return 2
    defects, matched, checked = check_pins(lane, rev, self_entry, pins_obj)
    selftest_ok, selftest_cases = True, 0
    if not skip_selftest:
        selftest_cases = 8
        rc = selftest(work / "selftest", self_entry)
        selftest_ok = rc == 0
        print("SELFTEST cases=%d red-green-ok=%d" % (selftest_cases, selftest_cases if selftest_ok else 0))
    for d in defects:
        print("DEFECT %s" % d)
    print("PINS checked=%d matched=%d mismatched=%d" % (checked, matched, checked - matched))
    passed = not defects and matched == checked and selftest_ok
    print("PREDICATE R91-C2 %s" % ("pass" if passed else "fail"))
    return 0 if passed else 1


FIXTURE_FILES = {
    "plans91/a.txt": "alpha-bytes-v1\n",
    "plans91/b.json": "{\"record\": \"v1\"}\n",
    "plans91/c.txt": "present-at-v1\n",
}
SELF_BYTES = "checker-v1-bytes\n"


def fixture_repo(work: Path, commits: list[dict[str, str]], delete_second: list[str] | None = None) -> Path:
    repo = work
    repo.mkdir(parents=True, exist_ok=True)
    def gitr(*args: str) -> None:
        proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError("fixture git failed: %s %s" % (" ".join(args), proc.stderr.decode()[:120]))
    gitr("init", "-q", "-b", "main")
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "fixture@invalid"],
                   capture_output=True, timeout=60)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "fixture"], capture_output=True, timeout=60)
    for index, commit in enumerate(commits):
        for path, content in commit.items():
            target = repo / path
            if content is None:
                if target.exists():
                    target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for path, content in commit.items():
            if content is not None:
                gitr("add", path)
        if delete_second and index == 1:
            for path in delete_second:
                gitr("rm", "-q", "--cached", path)
        gitr("commit", "-q", "-m", "fixture commit %d" % index)
    return repo


def selftest(work: Path, self_entry: str) -> int:
    """Eight fixture repos; every red case must be red for its named reason (Q69)."""
    ok = 0
    checks: list[tuple[str, Path, str, str, int]] = []

    # 1 clean-green: pins match the committed bytes
    repo1 = fixture_repo(work / "clean-green", [
        {**FIXTURE_FILES, "checker-v1.txt": SELF_BYTES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": sha(FIXTURE_FILES["plans91/a.txt"].encode())},
            {"kind": "sha", "path": "plans91/b.json", "sha256": sha(FIXTURE_FILES["plans91/b.json"].encode())},
            {"kind": "sha", "path": "checker-v1.txt", "sha256": sha(SELF_BYTES.encode())},
        ]})},
    ])
    checks.append(("clean-green", repo1, "", "", 0))
    # 2 counter-byte-mutated: second commit mutates the pinned counter bytes
    repo2 = fixture_repo(work / "counter-byte-mutated", [
        {**FIXTURE_FILES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": sha(FIXTURE_FILES["plans91/a.txt"].encode())},
        ]})},
    ])
    (repo2 / "plans91/a.txt").write_text("alpha-bytes-v1-tampered\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo2), "add", "plans91/a.txt"], capture_output=True)
    subprocess.run(["git", "-C", str(repo2), "commit", "-q", "-m", "mutate"], capture_output=True)
    checks.append(("counter-byte-mutated", repo2, "PIN-MISMATCH bytes plans91/a.txt", "HEAD", 1))
    # 3 path-absent: a pinned path absent at the revision is a mismatch, never a skip
    repo3 = fixture_repo(work / "path-absent", [
        {**FIXTURE_FILES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/c.txt", "sha256": "x"},
        ]})},
    ])
    checks.append(("path-absent", repo3, "PIN-MISMATCH absent plans91/c.txt", "HEAD", 1))
    # 4 tampered-pin: a pin value edited in an otherwise green ledger must mismatch
    repo4 = fixture_repo(work / "tampered-pin", [
        {**FIXTURE_FILES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": "0" * 64},
        ]})},
    ])
    checks.append(("tampered-pin", repo4, "PIN-MISMATCH bytes plans91/a.txt", "HEAD", 1))
    # 5 blob-mutated: the pinned blob's content changed after the anchor
    repo5 = fixture_repo(work / "blob-mutated", [
        {**FIXTURE_FILES},
        {PINS: json.dumps({"entries": [
            {"kind": "blob", "path": "plans91/b.json", "blob": sha(FIXTURE_FILES["plans91/b.json"].encode()),
             "anchor_commit": "HEAD"},
        ]})},
    ])
    (repo5 / "plans91/b.json").write_text('{"record": "v2"}\n', encoding="utf-8")
    subprocess.run(["git", "-C", str(repo5), "add", "plans91/b.json"], capture_output=True)
    subprocess.run(["git", "-C", str(repo5), "commit", "-q", "-m", "mutate blob"], capture_output=True)
    checks.append(("blob-mutated", repo5, "RECORD-TABLE mismatch plans91/b.json", "HEAD", 1))
    # 6 absent-pin-ledger: fail closed (setup), never a synthetic substitute
    repo6 = fixture_repo(work / "absent-pin-ledger", [{**FIXTURE_FILES}])
    checks.append(("absent-pin-ledger", repo6, "DEFECT SETUP unreadable %s" % PINS, "HEAD", 2))
    # 7 self-pin-mismatch: the running checker's bytes differ from its own pin
    repo7 = fixture_repo(work / "self-pin-mismatch", [
        {**FIXTURE_FILES, "selfcopy.py": SELF_BYTES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "selfcopy.py", "sha256": sha((SELF_BYTES + "edited").encode())},
        ]})},
    ])
    checks.append(("self-pin-mismatch", repo7, "SELF-PIN-MISMATCH selfcopy.py", "HEAD", 1))
    # 8 blob-anchor-missing: the pinned blob does not exist at the anchor commit
    repo8 = fixture_repo(work / "blob-anchor-missing", [
        {**FIXTURE_FILES},
        {PINS: json.dumps({"entries": [
            {"kind": "blob", "path": "plans91/b.json",
             "blob": sha(b'{"record": "v1"}\n'), "anchor_commit": "HEAD"},
        ]})},
    ])
    # rebuild so the anchor commit is the empty first commit: re-init with the ledger only
    import shutil
    shutil.rmtree(repo8)
    repo8 = fixture_repo(work / "blob-anchor-missing", [
        {PINS: json.dumps({"entries": [
            {"kind": "blob", "path": "plans91/b.json",
             "blob": sha(b'{"record": "v1"}\n'), "anchor_commit": "HEAD"},
        ]})},
        {**FIXTURE_FILES},
    ])
    checks.append(("blob-anchor-missing", repo8, "RECORD-TABLE anchor plans91/b.json", "HEAD", 1))

    here = Path(__file__).resolve().parent
    for name, repo, want_defect, rev, want_rc in checks:
        cmd = [sys.executable, "-I", "-B", str(here / "round91_counter_pin.py"),
               "--lane", str(repo), "--rev", rev, "--work", str(repo / "work"),
               "--skip-selftest", SELF_ENTRY_FLAG, "selfcopy.py"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                              env={"PATH": "/usr/bin:/bin"})
        got_rc = proc.returncode
        got_defect_ok = want_defect in proc.stdout
        passed = got_rc == want_rc and got_defect_ok
        print("SELFTEST %s rc=%d want=%d defect-ok=%s ok=%s"
              % (name, got_rc, want_rc, got_defect_ok, passed))
        ok += passed
    print("SELFTEST-DETAIL cases=%d red-green-ok=%d" % (len(checks), ok))
    return 0 if ok == len(checks) else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--work", required=True)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--skip-selftest", action="store_true")
    parser.add_argument("--self-entry-path", default=SELF_PATH)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        if args.selftest:
            return selftest(work, args.self_entry_path)
        return run_checker(lane, resolve(lane, args.rev), work, args.self_entry_path, args.skip_selftest)
    except CouldNotEvaluate as error:
        print("DEFECT SETUP %s" % error)
        print("PREDICATE R91-C2 could-not-evaluate")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
