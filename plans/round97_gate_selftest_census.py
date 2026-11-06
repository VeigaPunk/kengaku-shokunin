#!/usr/bin/env python3
"""R97-C2 counter — registry rows that call themselves a `gate` without the self-test
PROTOCOL §Gate standard requires of every gate (round 97).

PROTOCOL.md §Gate standard, Self-test: "Every gate exposes a self-invocation mode over isolated
fixtures ... The flag spelling is the lane's (`--selftest`, `--self-test`, `run_selftest()`) and
the registry records it". The lane's self-assessment is the `kind` cell of each row of the
SKILL.md `## Gate/probe registry`; the observed state is the entry script's own bytes at the
measured revision. A MISMATCH is a row of kind `gate` whose entry script exposes no
self-invocation spelling (detector below). Every input is read with `git show REV:<path>`; the
working tree is never read.

Detector (a self-invocation entry point in the script's code, not a mention in prose):
  add_argument("--selftest" | "--self-test"), add_parser("selftest"), a `"--selftest" in|==`
  comparison or `in|== "--selftest"` / `"selftest"` dispatch, or `def run_selftest`.

Population pin and anti-laundering legs, against --base (default: round-97 BASE 4992cd0e):
  ROW-REMOVED     a row name present at BASE is absent at REV
  ROW-DUPLICATE   a row name occurs twice at REV
  CELL-CHANGED    a BASE row differs at REV in any cell other than `kind`
  DEMOTED         a row that is `gate` at BASE and `probe` at REV although its script HAS a
                  self-test spelling (over-correction: blanket retyping is not calibration)
  SCRIPT-CHANGED  the entry script of a row that is a no-spelling gate at BASE differs at REV
                  (a spelling added to a closed round's instrument is Q79 harm, not a repair)
  MISMATCH        a `gate` row at REV whose script has no self-test spelling

Usage:  python3 plans/round97_gate_selftest_census.py --lane . --rev REV [--base REV]
        python3 plans/round97_gate_selftest_census.py --selftest --work DIR
Exit:   0 `PREDICATE R97-C2 pass` (every leg 0) · 1 any finding · 2 could-not-evaluate
        (unresolved revision, no registry section at a revision, usage).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
SKILL = "SKILL.md"
HEADING = "## Gate/probe registry"
SPLIT = re.compile(r"(?<!\\)\|")
SCRIPT = re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
FINDING_IDS = ("ROW-REMOVED", "ROW-DUPLICATE", "CELL-CHANGED", "DEMOTED", "SCRIPT-CHANGED", "MISMATCH")
SPELLING = [re.compile(p) for p in (
    r"add_argument\(\s*[\"']--self-?test[\"']",
    r"add_parser\(\s*[\"']self-?test[\"']",
    r"[\"']--self-?test[\"']\s*(?:in|==|not in)\b",
    r"(?:\bin|==)\s*\(?[\"']--self-?test[\"']",
    r"def run_selftest\b",
    r"(?:==|\bin)\s*\(?[\"']self-?test[\"']",
)]


class CouldNotEvaluate(Exception):
    pass


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


def registry(root: Path, rev: str) -> list[list[str]]:
    data = blob(root, rev, SKILL)
    if data is None:
        raise CouldNotEvaluate(f"{SKILL} absent at {rev[:12]}")
    lines = data.decode(errors="replace").split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith(HEADING)]
    if len(starts) != 1:
        raise CouldNotEvaluate(f"registry heading count {len(starts)} at {rev[:12]}")
    rows = []
    for line in lines[starts[0] + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("| `"):
            rows.append([c.strip() for c in SPLIT.split(line.strip())[1:-1]])
    if not rows:
        raise CouldNotEvaluate(f"registry has no rows at {rev[:12]}")
    return rows


def script_of(row: list[str]) -> str | None:
    m = SCRIPT.search(row[2]) if len(row) > 2 else None
    return m.group(1) if m else None


def has_selftest(body: bytes | None) -> bool:
    text = (body or b"").decode(errors="replace")
    return any(p.search(text) for p in SPELLING)


def census(root: Path, rev_arg: str, base_arg: str) -> tuple[list[str], list[tuple[str, str]]]:
    rev = resolve(root, rev_arg)
    base = resolve(root, base_arg)
    at_rev = registry(root, rev)
    at_base = registry(root, base)
    lines: list[str] = []
    findings: list[tuple[str, str]] = []
    names = [r[0] for r in at_rev]
    by_rev = {r[0]: r for r in at_rev}
    by_base = {r[0]: r for r in at_base}
    for n in sorted({n for n in names if names.count(n) > 1}):
        findings.append(("ROW-DUPLICATE", n))
    for n, brow in by_base.items():
        rrow = by_rev.get(n)
        if rrow is None:
            findings.append(("ROW-REMOVED", n))
            continue
        if [c for i, c in enumerate(brow) if i != 1] != [c for i, c in enumerate(rrow) if i != 1]:
            findings.append(("CELL-CHANGED", n))
        script = script_of(brow)
        bbody = blob(root, base, script) if script else None
        rbody = blob(root, rev, script) if script else None
        if brow[1] == "gate" and not has_selftest(bbody) and rbody != bbody:
            findings.append(("SCRIPT-CHANGED", f"{n} {script}"))
        if brow[1] == "gate" and len(rrow) > 1 and rrow[1] == "probe" and has_selftest(rbody):
            findings.append(("DEMOTED", f"{n} {script}"))
    gates = with_st = 0
    for r in at_rev:
        if len(r) < 3 or r[1] != "gate":
            continue
        gates += 1
        script = script_of(r)
        if has_selftest(blob(root, rev, script) if script else None):
            with_st += 1
        else:
            findings.append(("MISMATCH", f"{r[0]} {script or 'no-script'}"))
    count = {k: sum(1 for f in findings if f[0] == k) for k in
             ("ROW-REMOVED", "ROW-DUPLICATE", "CELL-CHANGED", "DEMOTED", "SCRIPT-CHANGED", "MISMATCH")}
    lines.append(f"REV {rev} BASE {base}")
    lines.append(f"ROWS base={len(at_base)} rev={len(at_rev)} removed={count['ROW-REMOVED']} "
                 f"duplicate={count['ROW-DUPLICATE']} cells_changed={count['CELL-CHANGED']}")
    lines.append(f"GATES total={gates} with_selftest={with_st} without={count['MISMATCH']} "
                 f"demoted_with_selftest={count['DEMOTED']} scripts_changed={count['SCRIPT-CHANGED']}")
    lines.append(f"MISMATCH_TOTAL n={count['MISMATCH']}")
    return lines, findings


def run(root: Path, rev: str, base: str) -> int:
    lines, findings = census(root, rev, base)
    for line in lines:
        print(line)
    for kind, what in findings:
        print(f"{kind} {what}")
    ok = not findings
    print("PREDICATE R97-C2 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


# ----------------------------------------------------------------------------------- selftest
HEAD = HEADING + "\n\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n|---|---|---|---|---|---|---|---|\n"
WITH = 'import argparse\np = argparse.ArgumentParser()\np.add_argument("--selftest", action="store_true")\n'
WITHOUT = '"""No self-test: the parser rejects --selftest (measured)."""\nimport sys\nsys.exit(0)\n'


def row(name: str, kind: str, script: str, selftest: str = "none") -> str:
    return f"| `{name}` | {kind} | `python3 {script}` | `0` clean · `1` failed | {selftest} | pins | read-only | kengaku |\n"


def fixture(d: Path, skill: str, scripts: dict[str, str], message: str) -> str:
    (d / "plans").mkdir(parents=True, exist_ok=True)
    (d / SKILL).write_text("# fixture\n\n" + skill + "\n## Next\n", encoding="utf-8")
    for name, body in scripts.items():
        (d / name).write_text(body, encoding="utf-8")
    for args in (("add", "-A"), ("-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                                 "commit", "-q", "--no-gpg-sign", "--allow-empty", "-m", message)):
        proc = git(d, *args)
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"fixture git {args[0]} failed: {proc.stderr.decode()[-200:]}")
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def selftest(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="r97c2-selftest-", dir=work))
    failures = 0
    try:
        base_scripts = {"plans/a.py": WITH, "plans/b.py": WITHOUT, "plans/c.py": WITHOUT}
        base_skill = HEAD + row("a", "gate", "plans/a.py", "`--selftest`") + row("b", "gate", "plans/b.py") \
            + row("c", "probe", "plans/c.py")
        # (case id, skill at REV, scripts at REV, expected rc, expected finding ids)
        cases = [
            ("base-red", base_skill, base_scripts, 1, {"MISMATCH"}),
            ("retype-green", base_skill.replace("| `b` | gate |", "| `b` | probe |"), base_scripts, 0, set()),
            ("row-removed", HEAD + row("a", "gate", "plans/a.py", "`--selftest`") + row("c", "probe", "plans/c.py"),
             base_scripts, 1, {"ROW-REMOVED"}),
            ("demoted", base_skill.replace("| `b` | gate |", "| `b` | probe |").replace("| `a` | gate |", "| `a` | probe |"),
             base_scripts, 1, {"DEMOTED"}),
            ("cell-changed", base_skill.replace("| `b` | gate |", "| `b` | probe |").replace(
                "| `b` | probe | `python3 plans/b.py` | `0` clean · `1` failed | none |",
                "| `b` | probe | `python3 plans/b.py` | `0` clean · `1` failed | `--selftest` |"),
             base_scripts, 1, {"CELL-CHANGED"}),
            ("script-forged", base_skill, {**base_scripts, "plans/b.py": WITHOUT + 'if "--selftest" in sys.argv:\n    pass\n'},
             1, {"SCRIPT-CHANGED"}),
            ("prose-only", base_skill.replace("| `b` | gate |", "| `b` | probe |") + row("d", "gate", "plans/d.py"),
             {**base_scripts, "plans/d.py": WITHOUT}, 1, {"MISMATCH"}),
            ("duplicate", base_skill.replace("| `b` | gate |", "| `b` | probe |") + row("a", "gate", "plans/a.py", "`--selftest`"),
             base_scripts, 1, {"ROW-DUPLICATE"}),
        ]
        for cid, skill, scripts, want_rc, want_ids in cases:
            d = root / cid
            d.mkdir()
            proc = git(d, "init", "-q")
            top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
            if proc.returncode != 0 or Path(top).resolve() != d.resolve():
                raise CouldNotEvaluate(f"fixture repo {d} toplevel {top}")
            base = fixture(d, base_skill, base_scripts, "base")
            for p in d.glob("plans/*.py"):
                p.unlink()
            rev = fixture(d, skill, scripts, cid)
            # the public CLI path, not the helper: exit code and finding ids from stdout
            cli = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--lane", str(d),
                                  "--rev", rev, "--base", base], capture_output=True, text=True, timeout=300)
            ids = {l.split()[0] for l in cli.stdout.splitlines() if l.split() and l.split()[0] in FINDING_IDS}
            rc = cli.returncode
            ok = rc == want_rc and ids == want_ids
            failures += 0 if ok else 1
            print(f"CASE {cid} rc={rc} want_rc={want_rc} ids={','.join(sorted(ids)) or '-'} "
                  f"want_ids={','.join(sorted(want_ids)) or '-'} ok={ok}")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"SELFTEST cases={len(cases)} failed={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if a.selftest:
        if not a.work:
            raise CouldNotEvaluate("--selftest needs --work DIR")
        return selftest(Path(a.work).resolve())
    if not a.rev:
        raise CouldNotEvaluate("--rev REV is required (the measured revision is never inferred)")
    return run(Path(a.lane).resolve(), a.rev, a.base)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R97-C2 could-not-evaluate")
        sys.exit(2)
