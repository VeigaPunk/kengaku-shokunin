#!/usr/bin/env python3
"""R79-C2 counter — the previous closure's routed defects are discharged, not restated.

Universe (derived, never listed): the routed ids of the newest non-author spot-check,
`corpus/lessons/round-78-verifier-spotcheck.md` §6 (`- **R78-D<n> (severity) — ...`).

A discharged id has exactly one row in `corpus/routed-findings.jsonl` with:
  status   `closed`
  source   `<spotcheck>:<line>` and that line carries the id
  close    a tracked path, or a commit reachable from master, that is NOT the spot-check file
           itself and whose bytes carry the id (the repair, not the routing)
  check    a shell command, run from the lane root, that exits 0 exactly when the repair holds;
           a check that cannot fail (`true`, `:`, `exit 0`, empty) is `CHECK-TRIVIAL`
plus: `corpus/README.md` indexes the spot-check file (the closure artifact is not a dead file).

Frozen before data on 2026-11-04 (L1 KengakuR79); see plans/round-79-claims.md §R79-C2.

    python3 plans/round79_c2_closure_debt.py --lane .                  # verdict, worktree
    python3 plans/round79_c2_closure_debt.py --lane . --rev 660ec0b9   # same checks over that tree
    python3 plans/round79_c2_closure_debt.py --selftest --work DIR     # fixture battery
    python3 plans/round79_c2_closure_debt.py --mutants --work DIR      # attributed mutants
    python3 plans/round79_c2_closure_debt.py --control-presence --work DIR

Printed lines:
    UNIVERSE spotcheck=<path> ids=<n> [<csv>]
    DEBT <id> status=<s> close=<path|-> check=<present|absent>
    DEBT-TOTAL ids=<n> registered=<n> closed=<n> checks_passed=<n>
    INDEX <path> indexed=<yes|no>
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET ids=<n> closed=<n> checks_passed=<n> indexed=<yes|no>
    PREDICATE R79-C2 pass|fail
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SPOTCHECK = "corpus/lessons/round-78-verifier-spotcheck.md"
ROUTED = "corpus/routed-findings.jsonl"
README = "corpus/README.md"
ID_LINE = re.compile(r"^- \*\*(R\d+-D\d+) \(([a-z]+)\)", re.M)
TRIVIAL = re.compile(r"^\s*(true|:|exit 0|echo .*|/bin/true)\s*$")
STATUSES = ("open", "closed", "refused", "blocked")
TIMEOUT = 180


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Tree:
    def __init__(self, root: Path, label: str, tip: str, tracked: set[str] | None):
        self.root = root
        self.label = label
        self.tip = tip
        self._tracked = tracked

    def read(self, rel: str) -> str | None:
        try:
            return (self.root / rel).read_text(errors="replace")
        except OSError:
            return None

    def tracked(self, rel: str) -> bool:
        if self._tracked is None:
            return (self.root / rel).is_file()
        return rel in self._tracked

    def exists(self, rel: str) -> bool:
        return (self.root / rel).exists()


def worktree_tree(lane: Path) -> Tree:
    tip = git(lane, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip()
    tracked = set(git(lane, "ls-files", "-z").stdout.split("\0"))
    tracked.discard("")
    return Tree(lane, "worktree", tip, tracked)


def rev_tree(lane: Path, rev: str, work: Path) -> Tree:
    tip = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").stdout.strip()
    if not tip:
        raise SystemExit(f"SETUP unresolved revision {rev!r}")
    root = work / f"tree-{tip[:12]}"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    proc = subprocess.run(["bash", "-c", f"git -C {lane} archive {tip} | tar -x -C {root}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"SETUP git archive failed: {proc.stderr[:300]}")
    tracked = set(git(lane, "ls-tree", "-r", "--name-only", tip).stdout.splitlines())
    return Tree(root, rev, tip, tracked)


def derive_ids(spotcheck_text: str) -> list[str]:
    return [m.group(1) for m in ID_LINE.finditer(spotcheck_text)]


def load_rows(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"__invalid__": line[:80]})
    return rows


def run_check(tree: Tree, command: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(["bash", "-lc", command], cwd=str(tree.root), capture_output=True,
                              text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip().splitlines()[-1][:120] if (
        proc.stdout + proc.stderr).strip() else f"rc={proc.returncode}"


def check(tree: Tree, run_checks: bool = True) -> tuple[list[tuple[str, str]], dict, dict]:
    defects: list[tuple[str, str]] = []
    spot = tree.read(SPOTCHECK)
    if not spot:
        raise SystemExit(f"SETUP spot-check absent: {SPOTCHECK}")
    ids = derive_ids(spot)
    rows = load_rows(tree.read(ROUTED) or "")
    by_id: dict[str, list[dict]] = {}
    for row in rows:
        if "__invalid__" in row:
            defects.append(("ROW-INVALID", row["__invalid__"]))
            continue
        by_id.setdefault(str(row.get("id")), []).append(row)
    stats = {"ids": len(ids), "registered": 0, "closed": 0, "checks_passed": 0}
    detail: dict[str, str] = {}
    spot_lines = spot.splitlines()
    for rid in ids:
        found = by_id.get(rid, [])
        if not found:
            defects.append(("DEBT-UNREGISTERED", rid))
            detail[rid] = "status=- close=- check=absent"
            continue
        if len(found) > 1:
            defects.append(("DEBT-DUPLICATE", f"{rid} rows={len(found)}"))
        stats["registered"] += 1
        row = found[0]
        status = row.get("status")
        if status not in STATUSES:
            defects.append(("STATUS-UNKNOWN", f"{rid} {status!r}"))
        src = row.get("source")
        m = re.match(r"(.+):(\d+)$", str(src or ""))
        if not m or m.group(1) != SPOTCHECK:
            defects.append(("SOURCE-MISMATCH", f"{rid} {src!r}"))
        else:
            n = int(m.group(2))
            if not (1 <= n <= len(spot_lines)) or rid not in spot_lines[n - 1]:
                defects.append(("SOURCE-LINE", f"{rid} line {n} does not carry it"))
        close = row.get("close")
        if status == "closed":
            stats["closed"] += 1
            if not isinstance(close, str) or not close.strip():
                defects.append(("CLOSE-ABSENT", rid))
            elif close.strip() == SPOTCHECK:
                defects.append(("CLOSE-NOT-REPAIR", f"{rid} close names the routing file"))
            else:
                named = re.search(r"([\w./-]+\.(?:md|py|txt|json|jsonl|sh))", close)
                commit = re.search(r"\b([0-9a-f]{7,40})\b", close)
                if named and tree.tracked(named.group(1)):
                    if rid not in (tree.read(named.group(1)) or ""):
                        defects.append(("CLOSE-NOT-EVIDENCE", f"{rid} {named.group(1)} does not carry it"))
                elif commit:
                    proc = git(Path(tree.root), "merge-base", "--is-ancestor", commit.group(1), tree.tip)
                    if proc.returncode != 0:
                        defects.append(("CLOSE-COMMIT", f"{rid} {commit.group(1)} not an ancestor"))
                else:
                    defects.append(("CLOSE-UNRESOLVED", f"{rid} {close!r}"))
            cmd = row.get("check")
            if not isinstance(cmd, str) or TRIVIAL.match(cmd or ""):
                defects.append(("CHECK-TRIVIAL", rid))
            elif run_checks:
                ok, tail = run_check(tree, cmd)
                if ok:
                    stats["checks_passed"] += 1
                else:
                    defects.append(("CHECK-FAIL", f"{rid} {tail}"))
        elif status in ("blocked", "refused"):
            if not row.get("blocker"):
                defects.append(("BLOCKER-ABSENT", rid))
        detail[rid] = (f"status={status} close={close or '-'} "
                       f"check={'present' if row.get('check') else 'absent'}")
    readme = tree.read(README) or ""
    indexed = SPOTCHECK.split("/")[-1] in readme
    if not indexed:
        defects.append(("INDEX-MISSING", SPOTCHECK))
    return defects, stats, {"ids": ids, "detail": detail, "indexed": indexed}


def run(tree: Tree, verbose: bool = True, run_checks: bool = True) -> int:
    defects, stats, extra = check(tree, run_checks)
    print(f"UNIVERSE spotcheck={SPOTCHECK} ids={stats['ids']} {','.join(extra['ids'])}")
    if verbose:
        for rid in extra["ids"]:
            print(f"DEBT {rid} {extra['detail'].get(rid, 'status=- close=- check=absent')}")
    print(f"DEBT-TOTAL ids={stats['ids']} registered={stats['registered']} closed={stats['closed']} "
          f"checks_passed={stats['checks_passed']}")
    print(f"INDEX {SPOTCHECK} indexed={'yes' if extra['indexed'] else 'no'}")
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET ids={stats['ids']} closed={stats['closed']} checks_passed={stats['checks_passed']} "
          f"indexed={'yes' if extra['indexed'] else 'no'}")
    ok = (not defects and stats["closed"] == stats["ids"]
          and stats["checks_passed"] == stats["ids"] and extra["indexed"])
    print(f"PREDICATE R79-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# ---------------------------------------------------------------- fixture battery


FIXTURE_SPOT = """# spot-check

## 6. Routed defects

- **R78-D1 (high) — first defect.** body
- **R78-D2 (low) — second defect.** body
"""

FIXTURE_README = "# corpus\n\n| entry | covers |\n|---|---|\n| `lessons/round-78-verifier-spotcheck.md` | x |\n"
FIXTURE_REPAIR = "# repair log\n\nR78-D1 correction: counted.\nR78-D2 correction: counted.\n"


def fixture(root: Path, rows: list[dict] | None = None, repair: str = FIXTURE_REPAIR,
            readme: str = FIXTURE_README) -> None:
    files = {
        SPOTCHECK: FIXTURE_SPOT,
        README: readme,
        "corpus/lessons/round-79.md": repair,
        ROUTED: "\n".join(json.dumps(r) for r in (rows or [])) + "\n",
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def good_rows() -> list[dict]:
    return [
        {"id": "R78-D1", "class": "x", "source": f"{SPOTCHECK}:5", "opened_round": 78,
         "status": "closed", "close": "corpus/lessons/round-79.md:3 (R78-D1 correction)",
         "blocker": None, "check": "grep -q 'R78-D1 correction' corpus/lessons/round-79.md"},
        {"id": "R78-D2", "class": "x", "source": f"{SPOTCHECK}:6", "opened_round": 78,
         "status": "closed", "close": "corpus/lessons/round-79.md:4 (R78-D2 correction)",
         "blocker": None, "check": "grep -q 'R78-D2 correction' corpus/lessons/round-79.md"},
    ]


CASES = [
    ("clean", "pass"),
    ("unregistered", "DEBT-UNREGISTERED"),
    ("trivial-check", "CHECK-TRIVIAL"),
    ("check-fails", "CHECK-FAIL"),
    ("close-routing-file", "CLOSE-NOT-REPAIR"),
    ("close-no-evidence", "CLOSE-NOT-EVIDENCE"),
    ("source-line", "SOURCE-LINE"),
    ("index-missing", "INDEX-MISSING"),
    ("duplicate-row", "DEBT-DUPLICATE"),
]


def selftest(work: Path) -> int:
    failures = 0
    root = work / "c2-fixture"
    for name, expect in CASES:
        if root.exists():
            shutil.rmtree(root)
        rows = good_rows()
        repair, readme = FIXTURE_REPAIR, FIXTURE_README
        if name == "unregistered":
            rows = rows[:1]
        elif name == "trivial-check":
            rows[0]["check"] = "true"
        elif name == "check-fails":
            rows[0]["check"] = "grep -q 'absent marker' corpus/lessons/round-79.md"
        elif name == "close-routing-file":
            rows[0]["close"] = SPOTCHECK
        elif name == "close-no-evidence":
            rows[0]["close"] = "corpus/lessons/round-79.md:3 (R78-D1 correction)"
            repair = FIXTURE_REPAIR.replace("R78-D1 correction: counted.", "nothing here.")
        elif name == "source-line":
            rows[0]["source"] = f"{SPOTCHECK}:6"
        elif name == "index-missing":
            readme = "# corpus\n\nnothing\n"
        elif name == "duplicate-row":
            rows = rows + [dict(rows[0])]
        fixture(root, rows, repair, readme)
        tree = Tree(root, "fixture", "fixture", None)
        defects, _stats, _extra = check(tree)
        codes = {c for c, _ in defects}
        good = (not defects) if expect == "pass" else (expect in codes)
        failures += 0 if good else 1
        print(f"CASE {name} expect={expect} observed={','.join(sorted(codes)) or '-'} "
              f"{'ok' if good else 'FAIL'}")
    if root.exists():
        shutil.rmtree(root)
    print(f"SELFTEST cases={len(CASES)} red={len(CASES) - 1} failures={failures}")
    return 0 if failures == 0 else 1


MUTANTS = [
    ("drop-one-row", "DEBT-UNREGISTERED"),
    ("close-names-spotcheck", "CLOSE-NOT-REPAIR"),
    ("check-made-trivial", "CHECK-TRIVIAL"),
    ("status-reopened", "TARGET"),
]


def mutants(lane: Path, work: Path) -> int:
    root = work / "c2-mut"
    killed = survived = 0
    for name, expect in MUTANTS:
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        for rel in (SPOTCHECK, ROUTED, README, "corpus/lessons/round-79.md", "SCORECARD.md", "LOG.md",
                    "corpus/evidence/round79/routed-open.txt", "corpus/evidence/round79/gates-clean.txt"):
            src = lane / rel
            if src.is_file():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, root / rel)
        rows = load_rows((lane / ROUTED).read_text())
        ids = derive_ids((lane / SPOTCHECK).read_text())
        rows = [r for r in rows if r.get("id") in ids]
        if name == "drop-one-row":
            rows = rows[1:]
        elif name == "close-names-spotcheck":
            rows[0]["close"] = SPOTCHECK
        elif name == "check-made-trivial":
            rows[0]["check"] = ":"
        elif name == "status-reopened":
            rows[0]["status"] = "open"
        (root / ROUTED).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        tree = Tree(root, "fixture", git(lane, "rev-parse", "master").stdout.strip(), None)
        defects, stats, extra = check(tree)
        codes = {c for c, _ in defects}
        if expect == "TARGET":
            ok = not (stats["closed"] == stats["ids"] and stats["checks_passed"] == stats["ids"]
                      and extra["indexed"] and not defects)
        else:
            ok = expect in codes
        killed += 1 if ok else 0
        survived += 0 if ok else 1
        print(f"MUTANT {name} expect={expect} observed={','.join(sorted(codes)) or '-'} "
              f"{'killed' if ok else 'SURVIVED'}")
        shutil.rmtree(root)
    print(f"MUTANTS real={len(MUTANTS)} killed={killed} survived={survived}")
    return 0 if survived == 0 else 1


def control(lane: Path, work: Path) -> int:
    """The cheapest skip: register every id as closed with the routing file as `close` and a
    check that cannot fail."""
    root = work / "c2-ctl"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / SPOTCHECK).parent.mkdir(parents=True, exist_ok=True)
    (root / SPOTCHECK).write_text((lane / SPOTCHECK).read_text())
    (root / README).parent.mkdir(parents=True, exist_ok=True)
    (root / README).write_text((lane / README).read_text())
    ids = derive_ids((lane / SPOTCHECK).read_text())
    rows = [{"id": rid, "class": "x", "source": f"{SPOTCHECK}:5", "opened_round": 78,
             "status": "closed", "close": SPOTCHECK, "blocker": None, "check": "true"}
            for rid in ids]
    (root / ROUTED).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    tree = Tree(root, "fixture", "fixture", None)
    defects, stats, extra = check(tree)
    codes = sorted({c for c, _ in defects})
    print(f"CONTROL presence ids={stats['ids']} closed={stats['closed']} defects={len(defects)} "
          f"codes={','.join(codes) or '-'}")
    reached = (not defects and stats["closed"] == stats["ids"] and extra["indexed"])
    print(f"CONTROL presence target_reached={reached}")
    shutil.rmtree(root)
    return 0 if not reached else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-presence", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve() if a.work else Path("/fast/scratch/hyaku/kengaku-r79/c2")
    work.mkdir(parents=True, exist_ok=True)
    if a.selftest:
        return selftest(work)
    if a.mutants:
        return mutants(lane, work)
    if a.control_presence:
        return control(lane, work)
    tree = worktree_tree(lane) if a.rev in ("worktree", "", None) else rev_tree(lane, a.rev, work)
    return run(tree, verbose=not a.quiet)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
