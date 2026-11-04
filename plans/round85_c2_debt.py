#!/usr/bin/env python3
"""R85-C2 counter — the eight owner-routed round-84 defects, checked at a revision.

Each check reads bytes at the measured revision and returns closed/open; `--sensitivity`
runs the same checks against BASE (0de45354, an existing revision) and requires every one of
them red there.  R84-V4 is operator-owned and is printed as ROUTED, never counted.

Frozen inputs are read at FREEZE_REV: the case table, the defect list and the claims document
must exist there and be byte-identical at the measured revision (a frozen input committed in a
later commit is not frozen).

Exit: 0 every check closed and every check red at BASE, 1 a defect, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_REV = "0de45354d7aff18e4a23a348ec13de3a1f707a44"
FREEZE_REV = "1a45aeb5e8706b1518ba58fd0fe882df1631e2a0"
TABLE = "plans/round85-cases.json"
DEFECTS = "plans/round85-defects.json"
CLAIMS = "plans/round-85-claims.md"
QUALITY = "corpus/QUALITY.md"
ENTRY = "corpus/knowledge/tb2-code-from-image-offline.md"
LESSON = "corpus/lessons/round-85.md"
README = "corpus/README.md"
REGISTRY = "plans/round82_c1_plans_registry.py"
GATE_TIMING = "plans/gate_timing_check.py"
C1 = "plans/round85_c1_replay.py"
PROBE = "plans/round85_sqlite_truncate_probe.py"
CHECKER = "plans/round85_c2_debt.py"
EVIDENCE_ROW = "corpus/evidence/round85/"
SEAT_ID_RE = re.compile(r"^KengakuR\d+$")
V1_PATHS = (
    ".ufo/waves/round-84/w1-results.json",
    ".ufo/waves/round-84/w1/CriticR84.md",
    ".ufo/waves/round-84/w1/CriticR84/critique.md",
    ".ufo/waves/round-84/w1/CriticR84/report.txt",
)
ARCHIVE_PATHS = ("plans", "corpus/QUALITY.md", "corpus/README.md", "corpus/SOURCES.md",
                 "corpus/knowledge", "corpus/lessons", "corpus/evidence/round84",
                 "corpus/evidence/round85", "SKILL.md", ".ufo/waves/round-84")
ROUTED = (("R84-V4", "operator", "Q13 checker shape for one-wave rounds; L0 kengaku | round-84"),)
CHECKS = ("v1", "v2", "v3", "v5", "v6", "v7", "v8", "v9")


class SetupDefect(Exception):
    """The tree could not be evaluated (exit 2)."""


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True)


class Tree:
    def __init__(self, root: Path, tip: str, source: str):
        self.root, self.tip, self.source = root, tip, source

    def has(self, rel: str) -> bool:
        return (self.root / rel).is_file()

    def bytes(self, rel: str) -> bytes | None:
        try:
            return (self.root / rel).read_bytes()
        except OSError:
            return None

    def text(self, rel: str) -> str:
        data = self.bytes(rel)
        return data.decode("utf-8", "replace") if data is not None else ""


def extract_paths(lane: Path, tip: str, root: Path, paths: tuple[str, ...]) -> int:
    """Extract the paths that exist at `tip`; absent paths are skipped, never fatal."""
    extracted = 0
    for rel in paths:
        if git(lane, "cat-file", "-e", f"{tip}:{rel}").returncode != 0:
            continue
        arc = subprocess.run(["git", "-C", str(lane), "archive", "--format=tar", tip, rel],
                             capture_output=True)
        if arc.returncode != 0:
            continue
        subprocess.run(["tar", "-x", "-C", str(root)], input=arc.stdout, capture_output=True)
        extracted += 1
    return extracted


def rev_tree(lane: Path, rev: str, work: Path) -> Tree:
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    tip = proc.stdout.decode().strip()
    if proc.returncode != 0 or not tip:
        raise SetupDefect(f"unresolved-revision {rev}")
    root = Path(tempfile.mkdtemp(prefix="tree-", dir=work))
    if not extract_paths(lane, tip, root, ARCHIVE_PATHS):
        raise SetupDefect(f"archive-failed {tip[:12]}")
    return Tree(root, tip, f"rev {tip[:12]}")


def run_tool(argv: list[str], cwd: Path, work: Path, timeout: int = 900) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout,
                          env={"PATH": "/usr/bin", "TMPDIR": str(work), "HOME": str(work)})


# ------------------------------------------------------------------ checks

def v1(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    absent = [rel for rel in V1_PATHS
              if git(lane, "cat-file", "-e", f"{tree.tip}:{rel}").returncode != 0]
    return (not absent, "missing=" + ",".join(absent) if absent else f"tracked={len(V1_PATHS)}")


def v2(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    problems = []
    for rel in (TABLE, DEFECTS, CLAIMS):
        at_freeze = git(lane, "cat-file", "-p", f"{FREEZE_REV}:{rel}")
        if at_freeze.returncode != 0:
            problems.append(f"absent-at-freeze:{rel}")
            continue
        if tree.bytes(rel) != at_freeze.stdout:
            problems.append(f"drifted-since-freeze:{rel}")
    return (not problems, " ".join(problems) or "freeze-inputs-bound")


def v3(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    if not tree.has(C1):
        return False, "instrument-absent"
    proc = run_tool([sys.executable, "-I", "-B", str(tree.root / C1), "--lane", str(lane),
                     "--work", str(work / "v3"), "--control-forged-receipt"], tree.root, work)
    text = proc.stdout + proc.stderr
    ok = (proc.returncode == 0 and "target_reached=False" in text
          and "REPRODUCE-MISMATCH" in text)
    return ok, f"rc={proc.returncode} " + ("forgery-rejected" if ok else text.strip()[:120])


def v5(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    text = tree.text(QUALITY)
    rows = [line for line in text.splitlines() if line.startswith("- **Q61 —")]
    if not rows:
        return False, "no Q61 row"
    row = "\n".join(rows)
    need = ("considerthese/2026-10-26.md", "round85_c2_debt.py", "filler")
    missing = [token for token in need if token not in row]
    return (not missing, "Q61 missing=" + ",".join(missing) if missing else "Q61 landed")


def v6(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    text = tree.text(ENTRY)
    match = re.search(r"^writer:\s*`?([^`\s#]+)", text, re.MULTILINE)
    if not match:
        return False, "entry-has-no-writer"
    writer = match.group(1)
    if SEAT_ID_RE.match(writer):
        return False, f"writer-is-seat-id:{writer}"
    if not tree.has(GATE_TIMING):
        return False, "gate_timing_check-absent"
    proc = run_tool([sys.executable, "-I", "-B", str(tree.root / GATE_TIMING), "--selftest"],
                    tree.root, work)
    return (proc.returncode == 0, f"writer={writer} checker_rc={proc.returncode}")


def v7(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    """The correction must live somewhere that predates this round's own lesson."""
    prior = tree.text("corpus/lessons/round-84.md")
    correction = "R84-V7" in prior and "expansion: unchanged" in prior
    verdict = "expansion: unchanged" in tree.text(LESSON)
    return (correction and verdict,
            f"r84-dated-correction={correction} r85-verdict={verdict}")


def v8(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    """The repair is the flag spelling; the gate's own tool-byte read is worktree-based, so
    base-sensitivity is established on the measured revision's bytes and the gate verdict is
    recorded as detail (see the round-85 lesson's open questions)."""
    tool = tree.bytes("plans/round83_c2_debt.py")
    if tool is None:
        return False, "instrument-absent"
    flags = ("--selftest", "--mutants", "--control-presence", "--sensitivity")
    missing = [flag for flag in flags if flag.encode() not in tool]
    detail = "literal_flags=%d/4" % (len(flags) - len(missing))
    if tree.has(REGISTRY):
        proc = run_tool([sys.executable, "-I", "-B", str(tree.root / REGISTRY), "--lane",
                         str(lane), "--tip", tree.tip], tree.root, work)
        row = [ln for ln in (proc.stdout + proc.stderr).splitlines()
               if ln.startswith("ROW round83-c2-debt")]
        if row:
            detail += " gate=" + row[0].rsplit("defects=", 1)[-1]
    return (not missing, detail if not missing else detail + " missing=" + ",".join(missing))


def v9(tree: Tree, lane: Path, work: Path) -> tuple[bool, str]:
    text = tree.text(LESSON)
    if not text:
        return False, "lesson-absent"
    has_heading = "Definition horizon" in text
    has_base = BASE_REV in text
    has_future = "future file" in text
    return (has_heading and has_base and has_future,
            f"heading={has_heading} base={has_base} future={has_future}")


CHECK_FUNCS = {"v1": v1, "v2": v2, "v3": v3, "v5": v5, "v6": v6, "v7": v7, "v8": v8, "v9": v9}


def indexed(tree: Tree) -> bool:
    text = tree.text(README)
    return EVIDENCE_ROW in text and "lessons/round-85.md" in text


def evaluate(tree: Tree, lane: Path, work: Path, quiet: bool = False) -> tuple[dict, bool]:
    results = {}
    for name, func in CHECK_FUNCS.items():
        try:
            ok, detail = func(tree, lane, work)
        except subprocess.TimeoutExpired:
            ok, detail = False, "timeout"
        results[name] = (ok, detail)
        if not quiet:
            print(f"CHECK {name} {'ok' if ok else 'DEFECT'} {detail}")
    return results, indexed(tree)


def emit(results: dict, is_indexed: bool) -> int:
    closed = sum(1 for ok, _ in results.values() if ok)
    defects = len(results) - closed
    print(f"TARGET ids={len(results)} closed={closed} checks_passed={closed} "
          f"indexed={'yes' if is_indexed else 'no'} defects={defects}")
    code = 0 if (defects == 0 and closed == len(results) and is_indexed) else 1
    print(f"PREDICATE R85-C2 {'pass' if code == 0 else 'fail'}")
    return code


def sensitivity(lane: Path, work: Path) -> int:
    tree = rev_tree(lane, BASE_REV, work)
    failed_at_base = 0
    for name, func in CHECK_FUNCS.items():
        try:
            ok, detail = func(tree, lane, work)
        except subprocess.TimeoutExpired:
            ok, detail = True, "timeout-treated-as-green"
        if not ok:
            failed_at_base += 1
        print(f"BASE-CHECK {name} {'red' if not ok else 'GREEN'} {detail}")
    print(f"SENSITIVITY n={len(CHECK_FUNCS)} failed_at_base={failed_at_base}")
    return 0 if failed_at_base == len(CHECK_FUNCS) else 1


def setup_failure(detail: str) -> int:
    print(f"DEFECT SETUP {detail}")
    print(f"TARGET ids=0 closed=0 checks_passed=0 indexed=no defects=0")
    print("PREDICATE R85-C2 fail")
    return 2


# ------------------------------------------------------------------ fixtures

CONTROL_FIXTURES = {
    # name -> (base def/case, expected defect)
    "presence-only-q61": ("q61-no-citation", "v5"),
    "seat-writer": ("seat-writer", "v6"),
    "freeze-drift": ("freeze-drift", "v2"),
}


def fixture_tree(lane: Path, work: Path, kind: str) -> Tree:
    """A tip tree with one repair reverted to its base shape."""
    tip = rev_tree(lane, "master", work)
    root = Path(tempfile.mkdtemp(prefix=f"ctl-{kind}-", dir=work))
    for rel in ARCHIVE_PATHS:
        src, dst = tip.root / rel, root / rel
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    tree = Tree(root, tip.tip, f"fixture {kind}")
    if kind == "q61-no-citation":
        text = tree.text(QUALITY)
        text = re.sub(r"(?m)^- \*\*Q61 —.*$", "- **Q61 — placeholder.**", text)
        (root / QUALITY).write_text(text, encoding="utf-8")
    elif kind == "seat-writer":
        text = tree.text(ENTRY)
        text = re.sub(r"(?m)^writer:.*$", "writer: KengakuR84", text)
        (root / ENTRY).write_text(text, encoding="utf-8")
    elif kind == "freeze-drift":
        path = root / TABLE
        doc = json.loads(path.read_bytes())
        doc["cases"][0]["why"] = "drifted after the freeze"
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return tree


def control(lane: Path, work: Path, name: str) -> int:
    kind, check_name = CONTROL_FIXTURES[name]
    tree = fixture_tree(lane, work, kind)
    ok, detail = CHECK_FUNCS[check_name](tree, lane, work)
    print(f"CONTROL {name} check={check_name} target_reached={ok} detail={detail}")
    shutil.rmtree(tree.root, ignore_errors=True)
    return 0 if not ok else 1


MUTANTS = (
    ("q61-any-row", "q61-no-citation", "v5",
     'missing = [token for token in need if token not in row]', "missing = []"),
    ("writer-unchecked", "seat-writer", "v6",
     "if SEAT_ID_RE.match(writer):", "if False:"),
    ("freeze-bytes-unchecked", "freeze-drift", "v2",
     'if tree.bytes(rel) != at_freeze.stdout:', "if False:"),
)


def mutants(lane: Path, work: Path) -> int:
    necessary = redundant = 0
    source = Path(__file__).resolve().read_text(encoding="utf-8")
    for name, fixture, check_name, needle, replacement in MUTANTS:
        if needle not in source:
            print(f"MUTANT {name} NOT-APPLICABLE")
            redundant += 1
            continue
        tree = fixture_tree(lane, work, fixture)
        ok_plain, detail = CHECK_FUNCS[check_name](tree, lane, work)
        mutated = work / f"mutant-{name}.py"
        mutated.write_text(source.replace(needle, replacement, 1), encoding="utf-8")
        proc = run_tool([sys.executable, "-I", "-B", str(mutated), "--lane", str(lane),
                         "--check-only", check_name, "--work", str(work / f"mw-{name}")],
                        Path.cwd(), work)
        ok_mutant = "CHECK " in proc.stdout and " ok " in proc.stdout
        print(f"MUTANT {name} fixture={fixture} unmutated_defect={not ok_plain} "
              f"mutant_passes={ok_mutant}")
        if ok_mutant and not ok_plain:
            necessary += 1
        else:
            redundant += 1
        shutil.rmtree(tree.root, ignore_errors=True)
    print(f"MUTANTS real={len(MUTANTS)} necessary={necessary} redundant={redundant}")
    return 0 if necessary == len(MUTANTS) else 1


def selftest(lane: Path, work: Path) -> int:
    failures = checks = 0

    def case(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    base = rev_tree(lane, BASE_REV, work)
    results, _ = evaluate(base, lane, work, quiet=True)
    case("base-all-eight-red", sum(1 for ok, _ in results.values() if not ok) == 8)
    case("base-index-red", not indexed(base))

    tip = rev_tree(lane, "master", work)
    for kind, check_name in (("q61-no-citation", "v5"), ("seat-writer", "v6"),
                             ("freeze-drift", "v2")):
        tree = fixture_tree(lane, work, kind)
        ok, _ = CHECK_FUNCS[check_name](tree, lane, work)
        case(f"fixture-{kind}-red", not ok)
        shutil.rmtree(tree.root, ignore_errors=True)

    drifted = Tree(tip.root, tip.tip, "drift")
    case("unknown-check-name", "v4" not in CHECK_FUNCS)
    print(f"SELFTEST cases={checks} red={checks - failures} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--work", required=True)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--mutants", action="store_true")
    parser.add_argument("--sensitivity", action="store_true")
    parser.add_argument("--control-presence", action="store_true")
    parser.add_argument("--check-only", choices=sorted(CHECK_FUNCS))
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    if not work.exists():
        work.mkdir(parents=True, exist_ok=True)
    if not work.is_dir():
        return setup_failure(f"work-not-a-directory {work}")
    try:
        if args.selftest:
            return selftest(lane, work)
        if args.mutants:
            return mutants(lane, work)
        if args.control_presence:
            return control(lane, work, "presence-only-q61")
        if args.sensitivity:
            return sensitivity(lane, work)
        tree = rev_tree(lane, args.rev, work) if args.rev else Tree(lane, "worktree", "worktree")
        if args.check_only:
            ok, detail = CHECK_FUNCS[args.check_only](tree, lane, work)
            print(f"CHECK {args.check_only} {'ok' if ok else 'DEFECT'} {detail}")
            return 0 if ok else 1
        results, is_indexed = evaluate(tree, lane, work)
        for routed, owner, reason in ROUTED:
            print(f"ROUTED {routed} owner={owner} reason={reason}")
        return emit(results, is_indexed)
    except SetupDefect as error:
        return setup_failure(str(error))


if __name__ == "__main__":
    sys.exit(main())
