#!/usr/bin/env python3
"""R82-C2 counter — the previous closure's routed defects are discharged, not restated.

Universe (derived, never listed): the routed ids of the NEWEST verifier spot-check under
`corpus/lessons/`, `round-<n>-verifier-spotcheck.md` chosen by the largest round number in the
measured tree; its `## 5.` section's `- **V<n> · ...**` lines carry the short ids, and the lane
registry names them `R<n>-V<n>` (the round whose work the spot-check closed). Round 81 and the
id list are never hardcoded: rename the newest spot-check and the universe follows it.

A discharged id has exactly one row in `corpus/routed-findings.jsonl` with:
  status   `closed`
  source   `<spotcheck>:<line>` and that line carries the short id
  close    a tracked path, or a commit reachable from master, that is NOT the spot-check file
           itself and whose bytes carry the id (the repair, not the routing)
  check    a shell command, run from the lane root, that exits 0 exactly when the repair holds;
           a check that cannot fail (`true`, `:`, `exit 0`, empty) is `CHECK-TRIVIAL`
plus: `corpus/README.md` indexes the spot-check file (the closure artifact is not a dead file),
and a sensitivity leg: each closed row may name `evidence_path` (+ optional
`reverted_state: "dir"` for deletion repairs); the check must FAIL when that path is reverted to
its state at the base revision `a3a03ac31451e58f1742b9bccb73b72c2d90a95c` (base blob restored when
the path is tracked there, deleted when it is new, created as an empty directory when
`reverted_state` is `dir`). A check that still passes reverted is `CHECK-NOT-REPAIR-SENSITIVE`.

Frozen before data on 2026-11-04 (L1 KengakuR82); see plans/round-82-claims.md §R82-C2.

    python3 plans/round82_c2_closure_debt.py --lane .                  # verdict, worktree
    python3 plans/round82_c2_closure_debt.py --lane . --rev <rev>      # same checks over that tree
    python3 plans/round82_c2_closure_debt.py --selftest --work DIR     # fixture battery
    python3 plans/round82_c2_closure_debt.py --mutants --work DIR      # attributed mutants
    python3 plans/round82_c2_closure_debt.py --control-presence --work DIR

Printed lines:
    UNIVERSE spotcheck=<path> ids=<n> [<csv>]
    DEBT <id> status=<s> close=<path|-> check=<present|absent>
    DEBT-TOTAL ids=<n> registered=<n> closed=<n> checks_passed=<n>
    INDEX <path> indexed=<yes|no>
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET ids=<n> closed=<n> checks_passed=<n> indexed=<yes|no>
    PREDICATE R82-C2 pass|fail
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROUTED = "corpus/routed-findings.jsonl"
README = "corpus/README.md"
LESSONS = "corpus/lessons"
SPOTCHECK_NAME = re.compile(r"^round-(\d+)-verifier-spotcheck\.md$")
ID_LINE = re.compile(r"^- \*\*([A-Z])(\d+) · ", re.M)
SECTION5 = re.compile(r"^## 5\..*$", re.M)
NEXT_SECTION = re.compile(r"^## ", re.M)
TRIVIAL = re.compile(r"^\s*(true|:|exit 0|echo .*|/bin/true)\s*$")
STATUSES = ("open", "closed", "refused", "blocked")
TIMEOUT = 300
BASE_REV = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"  # round-82 base (round-81 tip); the repair must fail here


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
    if not tip:
        raise SystemExit("SETUP no master commit in lane")
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
    gitdir = subprocess.run(["git", "-C", str(lane), "rev-parse", "--git-dir"],
                            capture_output=True, text=True).stdout.strip()
    if gitdir:
        gd = Path(gitdir)
        if not gd.is_absolute():
            gd = lane / gd
        (root / ".git").write_text(f"gitdir: {gd}\n")
    tracked = set(git(lane, "ls-tree", "-r", "--name-only", tip).stdout.splitlines())
    return Tree(root, rev, tip, tracked)


def derive_universe(tree: Tree) -> tuple[str, int, list[str], str]:
    """Newest `corpus/lessons/round-*-verifier-spotcheck.md` by round number; ids from its
    `## 5.` section's `- **<X><n> · ` lines, registered as `R<round>-<X><n>` (round 81 → V,
    round 80 → U — the letter rides the file, never this code)."""
    best: tuple[int, str] | None = None
    base = tree.root / LESSONS
    if base.is_dir():
        for p in sorted(base.iterdir()):
            m = SPOTCHECK_NAME.match(p.name)
            if m and (best is None or int(m.group(1)) > best[0]):
                best = (int(m.group(1)), f"{LESSONS}/{p.name}")
    if tree._tracked is not None:
        for rel in tree._tracked:
            m = SPOTCHECK_NAME.match(Path(rel).name) if rel.startswith(LESSONS + "/") else None
            if m and (best is None or int(m.group(1)) > best[0]):
                best = (int(m.group(1)), rel)
    if best is None:
        raise SystemExit(f"SETUP no {LESSONS}/round-*-verifier-spotcheck.md in this tree")
    rnd, path = best
    text = tree.read(path)
    if text is None:
        raise SystemExit(f"SETUP spot-check unreadable: {path}")
    m5 = SECTION5.search(text)
    if m5:
        nxt = NEXT_SECTION.search(text, m5.end())
        section = text[m5.start():nxt.start() if nxt else len(text)]
    else:
        section = text
    ids = [f"R{rnd}-{mg.group(1)}{mg.group(2)}" for mg in ID_LINE.finditer(section)]
    return path, rnd, ids, section


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
    spot, _rnd, ids, _section = derive_universe(tree)
    spot_text = tree.read(spot) or ""
    rows = load_rows(tree.read(ROUTED) or "")
    by_id: dict[str, list[dict]] = {}
    for row in rows:
        if "__invalid__" in row:
            defects.append(("ROW-INVALID", row["__invalid__"]))
            continue
        by_id.setdefault(str(row.get("id")), []).append(row)
    stats = {"ids": len(ids), "registered": 0, "closed": 0, "checks_passed": 0}
    detail: dict[str, str] = {}
    spot_lines = spot_text.splitlines()
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
        if not m or m.group(1) != spot:
            defects.append(("SOURCE-MISMATCH", f"{rid} {src!r}"))
        else:
            n = int(m.group(2))
            short = rid.split("-", 1)[1] if "-" in rid else rid
            if not (1 <= n <= len(spot_lines)) or short not in spot_lines[n - 1]:
                defects.append(("SOURCE-LINE", f"{rid} line {n} does not carry it"))
        close = row.get("close")
        literal = str(row.get("evidence_literal") or "")
        if status == "closed":
            stats["closed"] += 1
            if not isinstance(close, str) or not close.strip():
                defects.append(("CLOSE-ABSENT", rid))
            elif close.strip() == spot:
                defects.append(("CLOSE-NOT-REPAIR", f"{rid} close names the routing file"))
            else:
                named = re.search(r"([\w./-]+\.(?:md|py|txt|json|jsonl|sh))", close)
                commit = re.search(r"\b([0-9a-f]{7,64})\b", close)
                if named and tree.tracked(named.group(1)):
                    ev_text = tree.read(named.group(1)) or ""
                    if rid not in ev_text:
                        defects.append(("CLOSE-NOT-EVIDENCE", f"{rid} {named.group(1)} does not carry it"))
                    elif literal and literal not in ev_text:
                        defects.append(("EVIDENCE-LITERAL-ABSENT", f"{rid} {named.group(1)} lacks {literal!r}"))
                elif commit:
                    proc = git(Path(tree.root), "merge-base", "--is-ancestor", commit.group(1), "master")
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
    indexed = Path(spot).name in readme
    if not indexed:
        defects.append(("INDEX-MISSING", spot))
    return defects, stats, {"ids": ids, "detail": detail, "indexed": indexed, "spot": spot}


def sensitivity(tree: Tree, rows: list[dict], ids: list[str], work: Path) -> list[tuple[str, str]]:
    """Revert each closed row's evidence path to its BASE_REV state in a copy of the tree and
    require the row's check to FAIL there: the base blob when the path is tracked at BASE_REV,
    deletion when the file is new, an empty directory when the row says `reverted_state: dir`.
    A check that still passes is not sensitive to the repair it claims to test."""
    defects: list[tuple[str, str]] = []
    if tree.label == "fixture":
        return defects
    cur = work / "sens-cur"
    if cur.exists():
        shutil.rmtree(cur)

    def ignore(_d: str, names: list[str]) -> set[str]:
        return {n for n in names if n == ".git"}

    shutil.copytree(tree.root, cur, ignore=ignore)
    gitdir = subprocess.run(["git", "-C", str(tree.root), "rev-parse", "--git-dir"],
                            capture_output=True, text=True).stdout.strip()
    if gitdir:
        gd = Path(gitdir)
        if not gd.is_absolute():
            gd = Path(tree.root) / gd
        (cur / ".git").write_text(f"gitdir: {gd}\n")
    for row in rows:
        rid = row.get("id")
        if rid not in ids or row.get("status") != "closed":
            continue
        ev = str(row.get("evidence_path") or "")
        cmd = str(row.get("check") or "")
        if not ev or not cmd:
            continue
        target = cur / ev
        saved = target.read_bytes() if target.is_file() else None
        made_dir = False
        if row.get("reverted_state") == "dir":
            target.mkdir(parents=True, exist_ok=True)
            made_dir = True
        else:
            base = subprocess.run(["git", "-C", str(cur), "show", f"{BASE_REV}:{ev}"],
                                  capture_output=True, text=True)
            if base.returncode == 0:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(base.stdout)
            elif target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
        ok, _tail = run_check(Tree(cur, "sens", tree.tip, None), cmd)
        if ok:
            defects.append(("CHECK-NOT-REPAIR-SENSITIVE", f"{rid} passes with {ev} at its base bytes"))
        if made_dir:
            shutil.rmtree(target, ignore_errors=True)
        elif saved is None:
            if target.is_file():
                target.unlink()
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(saved)
    shutil.rmtree(cur)
    return defects


def run(tree: Tree, verbose: bool = True, run_checks: bool = True, work: Path | None = None,
        rows: list[dict] | None = None, ids: list[str] | None = None) -> int:
    defects, stats, extra = check(tree, run_checks)
    if run_checks and work is not None and rows is not None and ids is not None:
        defects += sensitivity(tree, rows, ids, work)
    print(f"UNIVERSE spotcheck={extra['spot']} ids={stats['ids']} {','.join(extra['ids'])}")
    if verbose:
        for rid in extra["ids"]:
            print(f"DEBT {rid} {extra['detail'].get(rid, 'status=- close=- check=absent')}")
    print(f"DEBT-TOTAL ids={stats['ids']} registered={stats['registered']} closed={stats['closed']} "
          f"checks_passed={stats['checks_passed']}")
    print(f"INDEX {extra['spot']} indexed={'yes' if extra['indexed'] else 'no'}")
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET ids={stats['ids']} closed={stats['closed']} checks_passed={stats['checks_passed']} "
          f"indexed={'yes' if extra['indexed'] else 'no'}")
    ok = (not defects and stats["closed"] == stats["ids"]
          and stats["checks_passed"] == stats["ids"] and extra["indexed"])
    print(f"PREDICATE R82-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# ---------------------------------------------------------------- fixture battery

FIXTURE_SPOT_80 = """# round-80 spot-check

## 5. Routed defects

- **U1 · stale.** body
- **U2 · stale.** body
"""

FIXTURE_SPOT = """# round-81 spot-check

## 5. Routed defects

- **V1 · first defect.** body
- **V2 · second defect.** body
"""

FIXTURE_README = ("# corpus\n\n| entry | covers |\n|---|---|\n"
                  "| `lessons/round-81-verifier-spotcheck.md` | x |\n")
FIXTURE_REPAIR = "# repair log\n\nR81-V1 correction: counted.\nR81-V2 correction: counted.\n"


def fixture(root: Path, rows: list[dict] | None = None, repair: str = FIXTURE_REPAIR,
            readme: str = FIXTURE_README, spot_name: str = "round-81-verifier-spotcheck.md") -> None:
    files = {
        f"{LESSONS}/round-80-verifier-spotcheck.md": FIXTURE_SPOT_80,
        f"{LESSONS}/{spot_name}": FIXTURE_SPOT,
        README: readme,
        "corpus/lessons/round-81.md": repair,
        ROUTED: "\n".join(json.dumps(r) for r in (rows or [])) + "\n",
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


SPOT_PATH = f"{LESSONS}/round-81-verifier-spotcheck.md"


def good_rows() -> list[dict]:
    return [
        {"id": "R81-V1", "class": "x", "source": f"{SPOT_PATH}:5", "opened_round": 81,
         "status": "closed", "close": "corpus/lessons/round-81.md:3 (R81-V1 correction)",
         "blocker": None, "check": "grep -q 'R81-V1 correction' corpus/lessons/round-81.md"},
        {"id": "R81-V2", "class": "x", "source": f"{SPOT_PATH}:6", "opened_round": 81,
         "status": "closed", "close": "corpus/lessons/round-81.md:4 (R81-V2 correction)",
         "blocker": None, "check": "grep -q 'R81-V2 correction' corpus/lessons/round-81.md"},
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
    ("stale-spotcheck", "DEBT-UNREGISTERED"),
]


def selftest(work: Path) -> int:
    failures = 0
    root = work / "c2r82-fixture"
    for name, expect in CASES:
        if root.exists():
            shutil.rmtree(root)
        rows = good_rows()
        repair, readme, spot_name = FIXTURE_REPAIR, FIXTURE_README, "round-81-verifier-spotcheck.md"
        if name == "unregistered":
            rows = rows[:1]
        elif name == "trivial-check":
            rows[0]["check"] = "true"
        elif name == "check-fails":
            rows[0]["check"] = "grep -q 'absent marker' corpus/lessons/round-81.md"
        elif name == "close-routing-file":
            rows[0]["close"] = SPOT_PATH
        elif name == "close-no-evidence":
            rows[0]["close"] = "corpus/lessons/round-81.md:3 (R81-V1 correction)"
            repair = FIXTURE_REPAIR.replace("R81-V1 correction: counted.", "nothing here.")
        elif name == "source-line":
            rows[0]["source"] = f"{SPOT_PATH}:6"
        elif name == "index-missing":
            readme = "# corpus\n\nnothing\n"
        elif name == "duplicate-row":
            rows = rows + [dict(rows[0])]
        elif name == "stale-spotcheck":
            spot_name = "round-79-verifier-spotcheck.md"
        fixture(root, rows, repair, readme, spot_name)
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
    ("rename-spotcheck-round", "DEBT-UNREGISTERED"),
    ("evidence-literal-absent", "EVIDENCE-LITERAL-ABSENT"),
]


def mutants(lane: Path, work: Path) -> int:
    """Six attributed data mutations on the frozen fixture scaffold, each must be killed.
    Runs before the real rows exist, so it never depends on integration state."""
    killed = survived = 0
    root = work / "c2r82-mut"
    for name, expect in MUTANTS:
        if root.exists():
            shutil.rmtree(root)
        rows = good_rows()
        repair, readme, spot_name = FIXTURE_REPAIR, FIXTURE_README, "round-81-verifier-spotcheck.md"
        if name == "drop-one-row":
            rows = rows[1:]
        elif name == "close-names-spotcheck":
            rows[0]["close"] = SPOT_PATH
        elif name == "check-made-trivial":
            rows[0]["check"] = ":"
        elif name == "status-reopened":
            rows[0]["status"] = "open"
        elif name == "rename-spotcheck-round":
            spot_name = "round-83-verifier-spotcheck.md"
        elif name == "evidence-literal-absent":
            rows[0]["evidence_literal"] = "no-such-literal"
        fixture(root, rows, repair, readme, spot_name)
        tree = Tree(root, "fixture", "fixture", None)
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
    shutil.rmtree(root, ignore_errors=True)
    print(f"MUTANTS real={len(MUTANTS)} killed={killed} survived={survived}")
    return 0 if survived == 0 else 1


def control(lane: Path, work: Path) -> int:
    """The cheapest skip: register every id as closed with the routing file as `close` and a
    check that cannot fail. Must not reach the target."""
    root = work / "c2r82-ctl"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    lane_tree = worktree_tree(lane)
    spot, _rnd, ids, _section = derive_universe(lane_tree)
    (root / spot).parent.mkdir(parents=True, exist_ok=True)
    (root / spot).write_text(lane_tree.read(spot) or "")
    (root / README).parent.mkdir(parents=True, exist_ok=True)
    (root / README).write_text(lane_tree.read(README) or "")
    rows = [{"id": rid, "class": "x", "source": f"{spot}:5", "opened_round": 81,
             "status": "closed", "close": spot, "blocker": None, "check": "true"}
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
    work = Path(a.work).resolve() if a.work else Path("/fast/scratch/hyaku/kengaku-r82/c2")
    work.mkdir(parents=True, exist_ok=True)
    if a.selftest:
        return selftest(work)
    if a.mutants:
        return mutants(lane, work)
    if a.control_presence:
        return control(lane, work)
    tree = worktree_tree(lane) if a.rev in ("worktree", "", None) else rev_tree(lane, a.rev, work)
    rows = load_rows(tree.read(ROUTED) or "")
    _spot, _rnd, ids, _section = derive_universe(tree)
    return run(tree, verbose=not a.quiet, work=work, rows=rows, ids=ids)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
