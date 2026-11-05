#!/usr/bin/env python3
"""Freeze-integrity gate (round 93, R93-C2): did any frozen instrument change after its freeze?

The lane's claims files assert that the counters, probes and case tables named at freeze
are the bytes that scored the claim. Round 92 filed "met as frozen" while three of its
instruments had been edited after the freeze and after the first scored run (lesson
round-92 M8; no gate compared counter bytes to the freeze). This gate counts those
mismatches between the lane's self-assessment and the repository:

  claims mode  --claims PATH   the table is the ```frozen-instruments block of PATH as it
                               stood at --freeze (lines "<sha256>  <repo-relative path>")
  paths mode   --paths P ...   legacy rounds without a table: the table is the bytes of
                               each path at --freeze

For every table row the instrument is `intact` only if (a) its bytes at --freeze hash to
the table value, (b) its bytes at --rev hash to the table value, and (c) no commit in
--freeze..--rev touches the path (an edit later reverted is still a breach: something
scored in between may have used the edited bytes).

A ten-case fixture battery runs inside every invocation, in-process (no CLI skip
channel, no marker file, no child re-entry; round-92 M6/M10). A red battery case fails
the PREDICATE whatever the lane verdict is.

Usage:  python3 plans/round93_freeze_integrity.py --lane <repo> --freeze <rev> --rev <rev>
            (--claims <path> | --paths <path> ...) --work <scratch dir>
Exit:   0 every instrument intact and battery green, 1 a breach or a red battery case,
        2 could-not-evaluate (unresolvable revision, freeze not an ancestor, missing or
        empty table, a path absent at the freeze).
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
    return proc.stdout if proc.returncode == 0 else None


def parse_table(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    inside = False
    for line in text.splitlines():
        if not inside and line.strip() == BLOCK_OPEN:
            inside = True
            continue
        if inside and line.strip() == "```":
            break
        if inside and line.strip():
            m = ROW.match(line.strip())
            if not m:
                raise CouldNotEvaluate(f"malformed table row {line.strip()[:60]!r}")
            rows.append((m.group(1), m.group(2)))
    if not rows:
        raise CouldNotEvaluate("frozen-instruments table absent or empty")
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
    rows = []
    for want, p in table:
        at_f = blob(root, f, p)
        at_t = blob(root, t, p)
        log = git(root, "rev-list", f"{f}..{t}", "--", p)
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

def _fx_commit(d: Path, msg: str) -> str:
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if Path(top).resolve() != d.resolve():
        raise RuntimeError(f"fixture toplevel {top} != {d}")
    subprocess.run(["git", "-C", str(d), "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                    "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(d), "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                    "commit", "-q", "--allow-empty", "-m", msg], check=True, capture_output=True)
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def _fx_repo(base: Path, name: str) -> Path:
    d = base / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True, capture_output=True)
    return d


def _claims(d: Path, rows: list[tuple[str, str]]) -> None:
    body = "\n".join(f"{s}  {p}" for s, p in rows)
    (d / "claims.md").write_text(f"# fixture\n\n{BLOCK_OPEN}\n{body}\n```\n")


def battery(base: Path) -> list[tuple[str, bool, str]]:
    results = []

    def setup(name: str):
        d = _fx_repo(base, name)
        (d / "c.py").write_text("print('counter')\n")
        (d / "other.txt").write_text("x\n")
        _claims(d, [(sha(b"print('counter')\n"), "c.py")])
        return d, _fx_commit(d, "freeze")

    def verdicts(d, f, rev, claims="claims.md", paths=None):
        _, _, rows = evaluate(d, f, rev, claims, paths)
        return [r["verdict"] for r in rows]

    def case(name, fn, want):
        try:
            got = fn()
        except CouldNotEvaluate as error:
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
        bat = []
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
