#!/usr/bin/env python3
"""Calibration for plans/order_check.py (draft at .ufo/waves/round-39/build/R39OrderGate/order_check.py).

Twelve fixtures (each its own repository in scratch) and six source mutants. Run:

  python3 calibrate.py --gate <order_check.py> --work <scratch dir>

Prints one `CASE` line per fixture/mutant and a `SELFTEST` total. Exit 1 on any WRONG.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# fixed author/committer identity and timestamps: fixture commit hashes are then reproducible and
# two calibration runs are byte-equal (the lane's receipt practice)
STAMP = "2026-10-26T00:00:00 +0000"
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
       "GIT_AUTHOR_DATE": STAMP, "GIT_COMMITTER_DATE": STAMP}

CLAIMS = "plans/round-99-claims.md"
RECEIPT = "corpus/evidence/round99/probe.txt"
CLAIMS_DIR = ".ufo/waves/round-99/claims/control.txt"
EXEC = "    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt\n"
CASE = "CASE empty-tree predicted=fail observed=fail tests=FFFF match=yes -- do-nothing\n"
CLEAN = "    gate: P10 DEFECT receipt unreadable\n"
TOLERATED = "    gate: P10 DEFECT receipt unreadable: corpus/evidence/round99/probe.txt\n"

MUTANTS = {
    # every P10 DEFECT line counts, so the one excused detail is a hit
    "m1-excuse-removed": ('EXECUTED_EXCUSE = re.compile(r"^receipt unreadable(?:: \\S+)?$")',
                          'EXECUTED_EXCUSE = re.compile(r"^\\x00never$")'),
    # the receipt-shaped CASE arm never fires
    "m2-case-arm-removed": ("if CASE_LINE.match(line):", "if False and CASE_LINE.match(line):"),
    # the freeze commit may already carry the receipt
    "m3-freeze-clause-removed": ('if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:', "if False:"),
    # the receipt may be an ancestor of the freeze commit
    "m4-order-clause-removed": (
        'if freeze != receipt_commit and git.rc("merge-base", "--is-ancestor", receipt_commit, freeze) == 0:',
        "if False:",
    ),
    # scan only the freeze commit's tree (misses controls added between freeze and receipt)
    "m5-window-freeze-only": (
        "hits = scan_claims(git, claims_dir, receipt_commit)",
        "hits = scan_claims(git, claims_dir, freeze)",
    ),
    # scan up to HEAD (flags controls added after the receipt)
    "m6-window-head": (
        "hits = scan_claims(git, claims_dir, receipt_commit)",
        'hits = scan_claims(git, claims_dir, "HEAD")',
    ),
}


def git(d: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} rc={r.returncode}: {r.stderr.strip()[:200]}")
    return r


def commit(d: Path, msg: str, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        git(d, "add", "--", rel)
    git(d, "commit", "-q", "-m", msg)


def rm_commit(d: Path, msg: str, paths: list[str]) -> None:
    for rel in paths:
        git(d, "rm", "-q", "--", rel)
    git(d, "commit", "-q", "-m", msg)


def new_repo(work: Path, name: str) -> Path:
    d = work / "fixtures" / name
    d.mkdir(parents=True, exist_ok=True)
    git(d, "init", "-q")
    return d


FIXTURES: dict[str, tuple[Path, str, str, int]] = {}


def build_fixtures(work: Path) -> None:
    for old in (work / "fixtures",):
        if old.exists():
            subprocess.run(["rm", "-rf", str(old)])

    # F1 probe executed in a control committed at freeze
    d = new_repo(work, "f1-executed")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: EXEC})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f1-executed-before-receipt"] = (d, CLAIMS, RECEIPT, 1)

    # F2 a receipt-shaped CASE line in a claims file at freeze
    d = new_repo(work, "f2-case")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CASE})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f2-case-observed"] = (d, CLAIMS, RECEIPT, 1)

    # F3 (negative) the only P10 line is the unexecuted form
    d = new_repo(work, "f3-clean")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f3-clean-passes"] = (d, CLAIMS, RECEIPT, 0)

    # F4 (negative) the unexecuted form with a path appended is still excused
    d = new_repo(work, "f4-tolerated")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: TOLERATED})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f4-tolerated-detail"] = (d, CLAIMS, RECEIPT, 0)

    # F5 receipt committed before the claims file
    d = new_repo(work, "f5-inverted")
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN})
    FIXTURES["f5-receipt-before-claims"] = (d, CLAIMS, RECEIPT, 1)

    # F5b inversion only: the receipt is an ancestor of the freeze commit but the freeze tree
    # no longer carries it, so only the ancestry clause can see the inversion
    d = new_repo(work, "f5b-inverted-deleted")
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    rm_commit(d, "freeze without the receipt", [RECEIPT])
    commit(d, "freeze files", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN})
    commit(d, "receipt restored", {RECEIPT: "cases=1\n"})
    FIXTURES["f5b-receipt-ancestor-of-freeze"] = (d, CLAIMS, RECEIPT, 1)

    # F6 freeze commit already carries the receipt
    d = new_repo(work, "f6-same-commit")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN, RECEIPT: "cases=1\n"})
    FIXTURES["f6-freeze-contains-receipt"] = (d, CLAIMS, RECEIPT, 1)

    # F7 offending control committed after the freeze, before the receipt
    d = new_repo(work, "f7-late-control")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN})
    commit(d, "control", {CLAIMS_DIR: EXEC})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f7-control-between-freeze-and-receipt"] = (d, CLAIMS, RECEIPT, 1)

    # F8 offending control committed after the receipt (outside the window)
    d = new_repo(work, "f8-after-receipt")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    commit(d, "later control", {CLAIMS_DIR: EXEC})
    FIXTURES["f8-control-after-receipt"] = (d, CLAIMS, RECEIPT, 0)

    # F9 setup error: receipt never committed
    d = new_repo(work, "f9-no-receipt")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: EXEC})
    FIXTURES["f9-receipt-uncommitted"] = (d, CLAIMS, RECEIPT, 2)

    # F10 setup error: not a git work tree
    d = work / "fixtures" / "f10-not-git"
    d.mkdir(parents=True)
    (d / CLAIMS).parent.mkdir(parents=True)
    (d / CLAIMS).write_text("# claims\n")
    FIXTURES["f10-not-a-repo"] = (d, CLAIMS, RECEIPT, 2)

    # F11 setup error: claims file name carries no round number
    d = new_repo(work, "f11-bad-name")
    commit(d, "freeze", {"plans/foo.md": "# claims\n", CLAIMS_DIR: CLEAN})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f11-bad-claims-name"] = (d, "plans/foo.md", RECEIPT, 2)

    # F12 scoping: the offending control lives under another round's claims dir
    d = new_repo(work, "f12-other-round")
    commit(d, "freeze", {CLAIMS: "# claims\n", CLAIMS_DIR: CLEAN,
                         ".ufo/waves/round-98/claims/control.txt": EXEC})
    commit(d, "receipt", {RECEIPT: "cases=1\n"})
    FIXTURES["f12-other-round-ignored"] = (d, CLAIMS, RECEIPT, 0)


def run(gate: Path, lane: Path, claims: str, receipt: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(gate), "--lane", str(lane), "--claims", claims,
                        "--receipt", receipt], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    args = ap.parse_args(argv)
    args.work.mkdir(parents=True, exist_ok=True)
    build_fixtures(args.work)

    wrong = 0
    observed: dict[str, int] = {}
    for fid, (lane, claims, receipt, want) in FIXTURES.items():
        rc, out = run(args.gate, lane, claims, receipt)
        observed[fid] = rc
        ok = rc == want
        wrong += not ok
        first = next((l for l in out.splitlines() if "FAIL" in l or "ERROR" in l or "RESULT" in l), "")
        print(f"CASE {fid} expect={want} observed={rc} {'ok' if ok else 'WRONG'} -- {first[:110]}")
    print(f"FIXTURES total={len(FIXTURES)} wrong={wrong}")

    src = args.gate.read_text()
    mdir = args.work / "mutants"
    mdir.mkdir(parents=True, exist_ok=True)
    mwrong = 0
    # Attribution: a mutant is KILLED only when the set of fixtures whose verdict changed is exactly
    # the set this mutant is supposed to change -- a degenerate mutant (syntax error, always exit 2)
    # changes everything and therefore counts as SURVIVED/UNATTRIBUTED, not as a kill.
    kill_map = {
        # the excuse branch is the only thing keeping every CLEAN-control fixture green: f3/f4 (the
        # P10 line itself) and f8/f12, whose scanned window holds the same excused line
        "m1-excuse-removed": {"f3-clean-passes", "f4-tolerated-detail",
                              "f8-control-after-receipt", "f12-other-round-ignored"},
        "m2-case-arm-removed": {"f2-case-observed"},
        "m3-freeze-clause-removed": {"f6-freeze-contains-receipt"},
        "m4-order-clause-removed": {"f5b-receipt-ancestor-of-freeze"},
        "m5-window-freeze-only": {"f7-control-between-freeze-and-receipt"},
        "m6-window-head": {"f8-control-after-receipt"},
    }
    for mid, (old, new) in MUTANTS.items():
        if src.count(old) != 1:
            print(f"MUTANT {mid} INVALID anchor-count={src.count(old)}")
            mwrong += 1
            continue
        path = mdir / f"{mid}.py"
        path.write_text(src.replace(old, new))
        changed = []
        for fid, (lane, claims, receipt, _want) in FIXTURES.items():
            rc, _out = run(path, lane, claims, receipt)
            if rc != observed[fid]:
                changed.append(fid)
        want_change = kill_map[mid]
        got = set(changed)
        attacked = got == want_change
        status = "KILLED" if attacked else ("UNATTRIBUTED" if got else "SURVIVED")
        mwrong += not attacked
        extra = f" extra={','.join(sorted(got - want_change))}" if got - want_change else ""
        print(f"MUTANT {mid} {status} by={','.join(sorted(got)) or '-'}{extra}")
    print(f"MUTANTS total={len(MUTANTS)} killed={len(MUTANTS) - mwrong} survived={mwrong}")
    print(f"SELFTEST cases={len(FIXTURES)} wrong={wrong} mutants_wrong={mwrong}")
    return 1 if (wrong or mwrong) else 0


if __name__ == "__main__":
    sys.exit(main())
