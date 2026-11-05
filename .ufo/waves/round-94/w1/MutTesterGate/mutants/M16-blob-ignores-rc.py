#!/usr/bin/env python3
"""Freeze-integrity gate v2 (round 94, R94-C2): did any frozen instrument change after its freeze?

Successor of plans/round93_freeze_integrity.py (R93-C2, admitted). The lane's claims files
assert that the counters, probes and case tables named at freeze are the bytes that scored
the claim. This gate counts mismatches between that self-assessment and the repository:

  claims mode  --claims PATH   the table is the ONE ```frozen-instruments block of PATH as it
                               stood at --freeze (lines "<sha256>  <repo-relative path>")
  paths mode   --paths P ...   legacy rounds without a table: the table is the bytes of
                               each path at --freeze

For every table row the instrument is `intact` only if (a) its bytes at --freeze hash to
the table value, (b) its bytes at --rev hash to the table value, and (c) no commit in
--freeze..--rev touches the path, counted with `git rev-list --full-history` so a side-branch
edit that a TREESAME merge discarded still counts (round-93 wave finding W-2). An edit later
reverted is still a breach: something scored in between may have used the edited bytes.

Changes against v1 (round-93 lesson W-2, W-3, W-6; closure routed defect 4):
  - touched count uses --full-history (v1 default simplification reported a discarded side
    edit as touched=0, a false intact);
  - a claims file with more than one frozen-instruments block, an unterminated block, or a
    path listed twice is could-not-evaluate (v1 read the first block only and counted
    duplicate rows twice);
  - the freeze is whatever --freeze names; callers that derive it (counters) document their
    selector.

A fifteen-case fixture battery runs inside every invocation, in-process (no CLI skip
channel, no marker file, no child re-entry; round-92 M6/M10). A red battery case fails
the PREDICATE whatever the lane verdict is.

Usage:  python3 plans/round94_freeze_integrity.py --lane <repo> --freeze <rev> --rev <rev>
            (--claims <path> | --paths <path> ...) --work <scratch dir>
Exit:   0 every instrument intact and battery green, 1 a breach or a red battery case,
        2 could-not-evaluate (unresolvable revision, freeze not an ancestor, missing, empty,
        duplicated or unterminated table, a path absent at the freeze).
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

BLOCK_OPEN = "```frozen-instruments"
ROW = re.compile(r"^([0-9a-f]{64})  (\S+)$")


class CouldNotEvaluate(Exception):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=120)


def resolve(root: Path, rev: str) -> str:
    proc = git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {rev}")
    return proc.stdout.decode().strip()


def blob(root: Path, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout


def parse_table(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    blocks = 0
    inside = False
    for line in text.splitlines():
        if not inside and line.strip() == BLOCK_OPEN:
            blocks += 1
            inside = True
            continue
        if inside and line.strip() == "```":
            inside = False
            continue
        if inside and line.strip():
            m = ROW.match(line.strip())
            if not m:
                raise CouldNotEvaluate(f"malformed table row {line.strip()[:60]!r}")
            rows.append((m.group(1), m.group(2)))
    if inside:
        raise CouldNotEvaluate("frozen-instruments block not terminated")
    if blocks > 1:
        raise CouldNotEvaluate(f"frozen-instruments blocks={blocks}, exactly one allowed")
    if not rows:
        raise CouldNotEvaluate("frozen-instruments table absent or empty")
    paths = [p for _, p in rows]
    dups = sorted({p for p in paths if paths.count(p) > 1})
    if dups:
        raise CouldNotEvaluate(f"duplicate table paths {','.join(dups)}")
    return rows


def evaluate(root: Path, freeze: str, rev: str, claims: str | None, paths: list[str] | None):
    f = resolve(root, freeze)
    t = resolve(root, rev)
    if git(root, "merge-base", "--is-ancestor", f, t).returncode != 0:
        raise CouldNotEvaluate(f"freeze {f[:12]} is not an ancestor of {t[:12]}")
    if claims is not None:
        text = blob(root, f, claims)
        if text is None:
            raise CouldNotEvaluate(f"claims file {claims} absent at freeze {f[:12]}")
        table = parse_table(text.decode(errors="replace"))
    else:
        table = []
        for p in paths or []:
            b = blob(root, f, p)
            if b is None:
                raise CouldNotEvaluate(f"path {p} absent at freeze {f[:12]}")
            table.append((sha(b), p))
        if not table:
            raise CouldNotEvaluate("no paths given")
        if len({p for _, p in table}) != len(table):
            raise CouldNotEvaluate("duplicate --paths")
    rows = []
    for want, p in table:
        at_f = blob(root, f, p)
        at_t = blob(root, t, p)
        log = git(root, "rev-list", "--full-history", f"{f}..{t}", "--", p)
        if log.returncode != 0:
            raise CouldNotEvaluate(f"rev-list failed for {p}")
        touched = len([x for x in log.stdout.decode().split() if x])
        reasons = []
        if at_f is None or sha(at_f) != want:
            reasons.append("freeze-bytes-differ-from-table")
        if at_t is None:
            reasons.append("absent-at-rev")
        elif sha(at_t) != want:
            reasons.append("rev-bytes-differ")
        if touched:
            reasons.append(f"touched-after-freeze={touched}")
        rows.append({"path": p, "table": want, "freeze": sha(at_f) if at_f else "absent",
                     "rev": sha(at_t) if at_t else "absent", "touched": touched,
                     "verdict": "intact" if not reasons else "broken:" + "+".join(reasons)})
    return f, t, rows


# ---- in-process battery -------------------------------------------------------------

GIT_ID = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
          "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]


def _fx_git(d: Path, *args: str) -> None:
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if Path(top).resolve() != d.resolve():
        raise RuntimeError(f"fixture toplevel {top} != {d}")
    subprocess.run(["git", "-C", str(d), *GIT_ID, *args], check=True, capture_output=True)


def _fx_commit(d: Path, msg: str) -> str:
    _fx_git(d, "add", "-A")
    _fx_git(d, "commit", "-q", "--allow-empty", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def _fx_repo(base: Path, name: str) -> Path:
    d = base / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    subprocess.run(["git", "-C", str(d), "init", "-q", "-b", "main"], check=True, capture_output=True)
    return d


def _claims(d: Path, rows: list[tuple[str, str]], extra: str = "") -> None:
    body = "\n".join(f"{s}  {p}" for s, p in rows)
    (d / "claims.md").write_text(f"# fixture\n\n{BLOCK_OPEN}\n{body}\n```\n{extra}")


def battery(base: Path) -> list[tuple[str, bool, str]]:
    results = []
    good = sha(b"print('counter')\n")

    def setup(name: str):
        d = _fx_repo(base, name)
        (d / "c.py").write_text("print('counter')\n")
        (d / "other.txt").write_text("x\n")
        _claims(d, [(good, "c.py")])
        return d, _fx_commit(d, "freeze")

    def verdicts(d, f, rev, claims="claims.md", paths=None):
        _, _, rows = evaluate(d, f, rev, claims, paths)
        return [r["verdict"] for r in rows]

    def case(name, fn, want):
        try:
            got = fn()
        except CouldNotEvaluate:
            got = "could-not-evaluate"
        ok = (got == want) if not callable(want) else want(got)
        results.append((name, ok, str(got)))

    d, f = setup("b01-intact")
    t = _fx_commit(d, "later empty")
    case("B01 intact", lambda: verdicts(d, f, t), ["intact"])

    d, f = setup("b02-edited")
    (d / "c.py").write_text("print('edited')\n")
    t = _fx_commit(d, "edit")
    case("B02 edited-after-freeze", lambda: verdicts(d, f, t),
         lambda v: len(v) == 1 and "rev-bytes-differ" in v[0] and "touched-after-freeze=1" in v[0])

    d, f = setup("b03-reverted")
    (d / "c.py").write_text("print('edited')\n")
    _fx_commit(d, "edit")
    (d / "c.py").write_text("print('counter')\n")
    t = _fx_commit(d, "revert")
    case("B03 edit-then-revert", lambda: verdicts(d, f, t),
         lambda v: len(v) == 1 and v[0] == "broken:touched-after-freeze=2")

    d = _fx_repo(base, "b04-lying-table")
    (d / "c.py").write_text("print('counter')\n")
    _claims(d, [("0" * 64, "c.py")])
    f = _fx_commit(d, "freeze")
    case("B04 table-lies-about-freeze-bytes", lambda: verdicts(d, f, f),
         lambda v: len(v) == 1 and "freeze-bytes-differ-from-table" in v[0])

    d, f = setup("b05-deleted")
    (d / "c.py").unlink()
    t = _fx_commit(d, "delete")
    case("B05 deleted-at-rev", lambda: verdicts(d, f, t),
         lambda v: len(v) == 1 and "absent-at-rev" in v[0])

    d, f = setup("b06-unrelated")
    (d / "other.txt").write_text("y\n")
    t = _fx_commit(d, "unrelated")
    case("B06 unrelated-edit-stays-intact", lambda: verdicts(d, f, t), ["intact"])

    d, f = setup("b07-not-ancestor")
    subprocess.run(["git", "-C", str(d), "checkout", "-q", "--orphan", "side"], check=True, capture_output=True)
    t = _fx_commit(d, "orphan")
    case("B07 freeze-not-ancestor", lambda: verdicts(d, f, t), "could-not-evaluate")

    d = _fx_repo(base, "b08-no-table")
    (d / "claims.md").write_text("# no table\n")
    f = _fx_commit(d, "freeze")
    case("B08 table-absent", lambda: verdicts(d, f, f), "could-not-evaluate")

    d, f = setup("b09-paths-mode")
    (d / "c.py").write_text("print('edited')\n")
    t = _fx_commit(d, "edit")
    case("B09 paths-mode-edit", lambda: verdicts(d, f, t, claims=None, paths=["c.py", "other.txt"]),
         lambda v: len(v) == 2 and v[0].startswith("broken:") and v[1] == "intact")

    d = _fx_repo(base, "b10-malformed")
    (d / "claims.md").write_text(f"{BLOCK_OPEN}\nnot-a-sha  c.py\n```\n")
    f = _fx_commit(d, "freeze")
    case("B10 malformed-row", lambda: verdicts(d, f, f), "could-not-evaluate")

    # v2 cases
    d, f = setup("b11-treesame-merge")
    _fx_git(d, "checkout", "-q", "-b", "side")
    (d / "c.py").write_text("print('side edit')\n")
    _fx_commit(d, "side edit")
    _fx_git(d, "checkout", "-q", "main")
    _fx_git(d, "merge", "-q", "-s", "ours", "--no-edit", "side")
    t = git(d, "rev-parse", "HEAD").stdout.decode().strip()
    case("B11 treesame-merge-side-edit", lambda: verdicts(d, f, t),
         lambda v: len(v) == 1 and v[0].startswith("broken:") and "touched-after-freeze=" in v[0]
         and "rev-bytes-differ" not in v[0])

    d = _fx_repo(base, "b12-second-block")
    (d / "c.py").write_text("print('counter')\n")
    _claims(d, [(good, "c.py")], extra=f"\n{BLOCK_OPEN}\n{'1' * 64}  c.py\n```\n")
    f = _fx_commit(d, "freeze")
    case("B12 second-table-block", lambda: verdicts(d, f, f), "could-not-evaluate")

    d = _fx_repo(base, "b13-duplicate-row")
    (d / "c.py").write_text("print('counter')\n")
    _claims(d, [(good, "c.py"), (good, "c.py")])
    f = _fx_commit(d, "freeze")
    case("B13 duplicate-table-row", lambda: verdicts(d, f, f), "could-not-evaluate")

    d, f = setup("b14-rev-below-head")
    mid = _fx_commit(d, "unrelated empty")
    (d / "c.py").write_text("print('edited after rev')\n")
    _fx_commit(d, "edit after rev")
    case("B14 rev-below-head-intact", lambda: verdicts(d, f, mid), ["intact"])

    d = _fx_repo(base, "b15-lie-repaired")
    (d / "c.py").write_text("print('counter')\n")
    _claims(d, [("0" * 64, "c.py")])
    f = _fx_commit(d, "freeze with lying table")
    _claims(d, [(good, "c.py")])
    t = _fx_commit(d, "table repaired after freeze")
    case("B15 table-repaired-after-freeze", lambda: verdicts(d, f, t),
         lambda v: len(v) == 1 and "freeze-bytes-differ-from-table" in v[0])
    return results


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--claims")
    ap.add_argument("--paths", nargs="+")
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    if (a.claims is None) == (a.paths is None):
        print("DEFECT SETUP exactly one of --claims/--paths is required")
        print("PREDICATE freeze-integrity could-not-evaluate")
        return 2
    work = Path(a.work).resolve()
    bat_dir = work / "freeze-integrity-battery"
    bat_dir.mkdir(parents=True, exist_ok=True)
    try:
        bat = battery(bat_dir)
    finally:
        shutil.rmtree(bat_dir, ignore_errors=True)
    bat_ok = sum(1 for _, ok, _ in bat if ok)
    for name, ok, got in bat:
        print(f"BATTERY {name.split()[0]} {'ok' if ok else 'RED'} got={got}")
    print(f"SELFTEST cases={len(bat)} ok={bat_ok}")
    try:
        f, t, rows = evaluate(Path(a.lane).resolve(), a.freeze, a.rev, a.claims, a.paths)
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE freeze-integrity could-not-evaluate")
        return 2
    broken = [r for r in rows if r["verdict"] != "intact"]
    print(f"FREEZE {f} REV {t}")
    for r in rows:
        print(f"INSTRUMENT {r['path']} table={r['table'][:12]} freeze={r['freeze'][:12]} "
              f"rev={r['rev'][:12]} touched={r['touched']} verdict={r['verdict']}")
    print(f"FREEZE-INTEGRITY instruments={len(rows)} intact={len(rows) - len(broken)} broken={len(broken)}")
    passed = not broken and bat_ok == len(bat)
    print(f"PREDICATE freeze-integrity {'pass' if passed else 'fail'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
