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


def git_blob_id(data: bytes) -> str:
    """The id `git hash-object` gives a blob (sha1 over the header and the bytes)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


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
                running = Path(__file__).resolve()
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
RED_CASES = ("counter-byte-mutated", "path-absent", "tampered-pin", "blob-mutated",
             "absent-pin-ledger", "self-pin-mismatch", "blob-anchor-missing")


def fixture_repo(work: Path, commits: list[dict[str, str | None]]) -> Path:
    """A fresh repo; each commit maps path -> text (None deletes the path). Own identity, no
    global config is read (HOME is the scratch dir)."""
    if work.exists():
        import shutil
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    env = {"PATH": "/usr/bin:/bin", "HOME": str(work), "LC_ALL": "C",
           "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@invalid",
           "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@invalid"}

    def gitr(*args: str) -> None:
        proc = subprocess.run(["git", "-C", str(work), *args], capture_output=True, timeout=60, env=env)
        if proc.returncode != 0:
            raise RuntimeError("fixture git failed: %s %s" % (" ".join(args), proc.stderr.decode()[:160]))

    gitr("init", "-q", "-b", "main")
    for index, commit in enumerate(commits):
        for path, content in commit.items():
            target = work / path
            if content is None:
                if target.exists():
                    target.unlink()
                    gitr("rm", "-q", "--cached", path)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            gitr("add", path)
        gitr("commit", "-q", "--allow-empty", "-m", "fixture commit %d" % index)
    return work


def selftest(work: Path, self_entry: str) -> int:
    """Eight fixture repos. Each red case must exit its named code and print its named defect; the
    clean case must be green. Children run the production entry point with --skip-selftest so the
    selftest does not recurse. The self-pin case plants a stale checker at the self path."""
    here = Path(__file__).resolve()
    checks: list[tuple[str, Path, str, int, str]] = []
    v1 = FIXTURE_FILES["plans91/b.json"].encode()

    # 1 clean-green: pins equal the committed bytes, a checker entry matches the running checker
    repo = fixture_repo(work / "clean-green", [
        {**FIXTURE_FILES, "checker.txt": SELF_BYTES},
        {PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": sha(FIXTURE_FILES["plans91/a.txt"].encode())},
            {"kind": "sha", "path": "checker.txt", "sha256": sha(SELF_BYTES.encode())},
        ]})},
    ])
    checks.append(("clean-green", repo, "PREDICATE R91-C2 pass", 0, "PREDICATE R91-C2 pass"))

    # 2 counter-byte-mutated: a pinned counter byte changes after the pin commit
    repo = fixture_repo(work / "counter-byte-mutated", [
        {**FIXTURE_FILES, PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": sha(FIXTURE_FILES["plans91/a.txt"].encode())}]})},
        {"plans91/a.txt": "alpha-bytes-v1-tampered\n"},
    ])
    checks.append(("counter-byte-mutated", repo, "", 1, "PIN-MISMATCH bytes plans91/a.txt"))

    # 3 path-absent: a pinned path that does not exist at the revision is a mismatch, never a skip
    repo = fixture_repo(work / "path-absent", [
        {**FIXTURE_FILES, PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/missing.txt", "sha256": sha(b"x")}]})},
    ])
    checks.append(("path-absent", repo, "", 1, "PIN-MISMATCH absent plans91/missing.txt"))

    # 4 tampered-pin: a pin value edited in an otherwise green ledger
    repo = fixture_repo(work / "tampered-pin", [
        {**FIXTURE_FILES, PINS: json.dumps({"entries": [
            {"kind": "sha", "path": "plans91/a.txt", "sha256": "0" * 64}]})},
    ])
    checks.append(("tampered-pin", repo, "", 1, "PIN-MISMATCH bytes plans91/a.txt"))

    # 5 blob-mutated: the blob the ledger pins changes after the anchor commit (HEAD~1 holds v1)
    repo = fixture_repo(work / "blob-mutated", [
        {**FIXTURE_FILES, PINS: json.dumps({"entries": [
            {"kind": "blob", "path": "plans91/b.json", "blob": git_blob_id(v1), "anchor_commit": "HEAD~1"}]})},
        {"plans91/b.json": "{\"record\": \"v2\"}\n"},
    ])
    checks.append(("blob-mutated", repo, "", 1, "RECORD-TABLE mismatch plans91/b.json"))

    # 6 absent-pin-ledger: no ledger at the revision -> setup, fail closed, never a substitute
    repo = fixture_repo(work / "absent-pin-ledger", [{**FIXTURE_FILES}])
    checks.append(("absent-pin-ledger", repo, "", 2, "DEFECT SETUP unreadable " + PINS))

    # 7 self-pin-mismatch: the committed copy of the checker at the self path is a stale file,
    #   its pin matches that committed copy, and the RUNNING checker differs from its own pin
    stale = "stale checker bytes\n"
    repo = fixture_repo(work / "self-pin-mismatch", [
        {SELF_PATH: stale, PINS: json.dumps({"entries": [
            {"kind": "sha", "path": SELF_PATH, "sha256": sha(stale.encode())}]})},
    ])
    checks.append(("self-pin-mismatch", repo, "", 1, "SELF-PIN-MISMATCH " + SELF_PATH))

    # 8 blob-anchor-missing: the pinned blob is present at HEAD but absent at its anchor commit
    repo = fixture_repo(work / "blob-anchor-missing", [
        {PINS: json.dumps({"entries": [
            {"kind": "blob", "path": "plans91/b.json", "blob": git_blob_id(v1), "anchor_commit": "HEAD~1"}]})},
        {**FIXTURE_FILES},
    ])
    checks.append(("blob-anchor-missing", repo, "", 1, "RECORD-TABLE anchor plans91/b.json"))

    ok = 0
    for name, repo, _unused, want_rc, want_text in checks:
        cmd = [sys.executable, "-I", "-B", str(here), "--lane", str(repo), "--rev", "HEAD",
               "--work", str(repo.parent / (name + "-run")), "--skip-selftest"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                              env={"PATH": "/usr/bin:/bin", "HOME": str(work), "LC_ALL": "C"})
        got_rc = proc.returncode
        text_ok = want_text in proc.stdout
        passed = got_rc == want_rc and text_ok
        print("SELFTEST %s rc=%d want=%d defect-ok=%s ok=%s" % (name, got_rc, want_rc, text_ok, passed))
        if not passed:
            print("SELFTEST-CHILD %s stdout=%r stderr=%r" % (name, proc.stdout[-400:], proc.stderr[-300:]))
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
