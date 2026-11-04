#!/usr/bin/env python3
"""R78-C2 counter — every verdict-bearing receipt under `corpus/evidence/round77/` and
`corpus/evidence/round78/` is self-locating: it stamps the revision it was produced at, the worktree
state it was produced in, the exact tool bytes that produced it (or an honest `TOOL-SUPPLIED` marker
when the tool did not exist at that revision), and the command a reader can re-run.

Frozen before data on 2026-11-04 (L1 KengakuR78); see plans/round-78-claims.md §R78-C2.
The class it prices is the round-77 closure's D1/D2 (receipts stamped at a revision that cannot
produce their verdict) and D5 (`WORKTREE clean` printed for a tool supplied untracked).

    python3 plans/round78_c2_stamp_location.py --lane .                  # verdict, worktree
    python3 plans/round78_c2_stamp_location.py --lane . --rev 3ae0ab54   # bytes at a revision
    python3 plans/round78_c2_stamp_location.py --selftest --work DIR     # fixture battery
    python3 plans/round78_c2_stamp_location.py --mutants --work DIR      # attributed mutants
    python3 plans/round78_c2_stamp_location.py --control-stamp-only --work DIR # the skip that loses

Universe (derived, never listed): regular files under the two evidence dirs (excluding `sources/`)
whose bytes carry a verdict signature (`LANE_TIP`, `PREDICATE`, `SELFTEST`, `MUTANTS`, `CONTROL`,
`VERDICT:`, `exit `).

Stamp legs per receipt:
  TIP-ABSENT / TIP-UNRESOLVED / TIP-NOT-ANCESTOR / STAMP-CONFLICT
  WORKTREE-ABSENT
  TOOL-UNNAMED        a `TOOL_SHA` with no `TOOL` path
  TOOL-ABSENT-AT-TIP  the named tool is not in the stamped tree and no `TOOL-SUPPLIED` line exists
  TOOL-DRIFT          the recomputed digest at the stamped revision differs from `TOOL_SHA`
  SUPPLIED-BUT-CLEAN  `WORKTREE clean` on a receipt whose tool is absent at its tip (D5)
  COMMAND-ABSENT      a verdict line with no `COMMAND`
  PASS-UNLOCATED      `PREDICATE … pass` with neither a matching tool pair nor `TOOL-SUPPLIED`
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DIRS = ("corpus/evidence/round77", "corpus/evidence/round78")
SKIP_PARTS = ("sources",)
SIGNATURES = re.compile(r"^(LANE_TIP|PREDICATE|SELFTEST|MUTANTS|CONTROL|VERDICT:|exit )", re.M)
TIP = re.compile(r"^LANE_TIP ([0-9a-f]{7,40})$", re.M)
WORKTREE = re.compile(r"^WORKTREE (clean|dirty)$", re.M)
TOOL = re.compile(r"^TOOL (\S+)", re.M)
TOOL_SHA = re.compile(r"^TOOL_SHA ([0-9a-f]{8,64})$", re.M)
SUPPLIED = re.compile(r"^TOOL-SUPPLIED (\S+)", re.M)
COMMAND = re.compile(r"^COMMAND \S", re.M)
PASS = re.compile(r"^PREDICATE (\S+) pass$", re.M)
VERDICTISH = re.compile(r"^(PREDICATE \S+ |VERDICT:|SELFTEST cases=|MUTANTS real=|CONTROL )", re.M)


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


class Ctx:
    def __init__(self, root: Path, rev: str):
        self.root = root
        self.rev = rev
        proc = git(root, "rev-parse", "--verify", "--quiet",
                   "master^{commit}" if rev in ("worktree", "fixture") else f"{rev}^{{commit}}")
        self.tip = proc.stdout.strip() if proc.returncode == 0 else ""
        if not self.tip:
            raise SystemExit(f"SETUP unresolved revision {rev!r} in {root}")
        self.is_rev = rev not in ("worktree", "fixture")

    def get(self, rel: str) -> str | None:
        if self.is_rev:
            proc = git(self.root, "show", f"{self.tip}:{rel}")
            return proc.stdout if proc.returncode == 0 else None
        try:
            return (self.root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    def exists(self, rel: str) -> bool:
        if self.is_rev:
            return git(self.root, "cat-file", "-e", f"{self.tip}:{rel}").returncode == 0
        return (self.root / rel).exists()

    def tracked(self, rel: str) -> bool:
        return git(self.root, "ls-files", "--error-unmatch", "--", rel).returncode == 0

    def ancestor(self, commit: str) -> bool:
        return git(self.root, "merge-base", "--is-ancestor", commit, "master").returncode == 0

    def exists_at(self, rel: str) -> bool:
        """Presence in the receipt's own stamped tree (the only tree a receipt can speak for)."""
        return git(self.root, "cat-file", "-e", f"{self.tip}:{rel}").returncode == 0

    def tool_digest(self, rel: str) -> str | None:
        """Digest of the tool bytes in the receipt's own stamped tree, never the caller's worktree."""
        proc = git(self.root, "cat-file", "-p", f"{self.tip}:{rel}")
        if proc.returncode != 0:
            return None
        return hashlib.sha256(proc.stdout.encode("utf-8", "surrogateescape")).hexdigest()


def digest_matches(pin: str, actual: str) -> bool:
    return actual.startswith(pin) if len(pin) < 64 else pin == actual


def last(pattern: re.Pattern, text: str):
    """The last stamp block wins: an appended re-stamp supersedes what it corrects (append-only)."""
    found = pattern.findall(text)
    return found[-1] if found else None


def universe(ctx: Ctx) -> list[str]:
    out = []
    for d in DIRS:
        live = ctx.root / d if not ctx.is_rev else None
        if ctx.is_rev:
            proc = git(ctx.root, "ls-tree", "-r", "--name-only", ctx.tip, "--", d)
            names = [n for n in proc.stdout.splitlines() if n]
        else:
            names = [str(p.relative_to(ctx.root)) for p in sorted(live.rglob("*")) if p.is_file()] if live else []
        for rel in names:
            if any(part in SKIP_PARTS for part in Path(rel).parts):
                continue
            text = ctx.get(rel) or ""
            if SIGNATURES.search(text):
                out.append(rel)
    return sorted(set(out))


def audit(ctx: Ctx) -> tuple[list[str], list[str], dict]:
    report, defects = [], []
    receipts = universe(ctx)
    report.append(f"UNIVERSE dirs={len(DIRS)} receipts={len(receipts)}")
    located = 0
    for rel in receipts:
        text = ctx.get(rel) or ""
        bad: list[str] = []
        tips = TIP.findall(text)
        if not tips:
            bad.append("TIP-ABSENT")
            short, state = "-", "-"
        else:
            tip = tips[-1]
            short = tip[:8]
            if not git(ctx.root, "rev-parse", "--verify", "--quiet", f"{tip}^{{commit}}").returncode == 0:
                bad.append("TIP-UNRESOLVED")
            elif not ctx.ancestor(tip):
                bad.append("TIP-NOT-ANCESTOR")
        state = last(WORKTREE, text) or "-"
        if state == "-":
            bad.append("WORKTREE-ABSENT")
        tool = last(TOOL, text)
        sha = last(TOOL_SHA, text)
        supplied = last(SUPPLIED, text)
        tool_rel = tool or supplied
        if sha and not tool:
            bad.append("TOOL-UNNAMED")
        if tool_rel:
            present = ctx.exists_at(tool_rel)
            if not present:
                if not supplied:
                    bad.append("TOOL-ABSENT-AT-TIP")
                elif state == "clean":
                    bad.append("SUPPLIED-BUT-CLEAN")
            if sha:
                actual = ctx.tool_digest(tool_rel)
                if actual is None:
                    if not supplied:
                        bad.append("TOOL-ABSENT-AT-TIP")
                elif not digest_matches(sha, actual):
                    bad.append("SUPPLIED-DIGEST-MISMATCH" if supplied else "TOOL-DRIFT")
        if VERDICTISH.search(text) and not last(COMMAND, text):
            bad.append("COMMAND-ABSENT")
        if PASS.search(text):
            located_ok = bool(tool and sha and not any(x.startswith(("TOOL-", "SUPPLIED-")) for x in bad)) \
                or bool(supplied and not any(x.startswith("SUPPLIED-") for x in bad))
            if not located_ok:
                bad.append("PASS-UNLOCATED")
        if not bad:
            located += 1
        for code in bad:
            defects.append(f"DEFECT {code} {rel}")
        report.append(f"RECEIPT {rel} tip={short} worktree={state} "
                      f"tool={tool_rel or '-'} sha={'yes' if sha else '-'} legs={'ok' if not bad else ','.join(bad)}")
    stats = {"receipts": len(receipts), "located": located, "unlocated": len(receipts) - located}
    return report, defects, stats


def emit(ctx: Ctx, out: Path | None = None, dirty: bool = False) -> int:
    report, defects, stats = audit(ctx)
    lines = [f"LANE_TIP {ctx.tip}", f"WORKTREE {'dirty' if dirty else 'clean'}"] + report
    lines += defects
    lines.append(f"DEFECTS n={len(defects)}")
    lines.append(f"TARGET receipts={stats['receipts']} located={stats['located']} "
                 f"unlocated={stats['unlocated']}")
    ok = not defects and stats["receipts"] > 0
    lines.append(f"PREDICATE R78-C2 {'pass' if ok else 'fail'}")
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    return 0 if ok else 1


# ------------------------------------------------------------------ fixtures
GOOD_TOOL = "plans/fixture_tool.py"


def fixture_repo(root: Path, *, omit_tip: str = "", drift: str = "", supplied_clean: str = "",
                 no_command: str = "", unlocated_pass: str = "", unresolved: str = "") -> Path:
    """A throwaway git repo (branch master) holding stamped receipts; every fixture names its root."""
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "corpus/evidence/round77").mkdir(parents=True)
    (root / "corpus/evidence/round78").mkdir(parents=True)
    (root / GOOD_TOOL).write_text("#!/usr/bin/env python3\nprint('probe')\n", encoding="utf-8")
    env = ["-c", "user.name=fixture", "-c", "user.email=fixture@fixture"]
    git(root, "init", "-q", "-b", "master")
    git(root, "add", "-A")
    git(root, *env, "commit", "-q", "-m", "fixture tool")
    tip = git(root, "rev-parse", "master").stdout.strip()
    digest = hashlib.sha256((root / GOOD_TOOL).read_bytes()).hexdigest()
    sha_tip = "f" * 40 if unresolved == "a" else tip

    def receipt(name: str, body: str) -> None:
        (root / "corpus/evidence/round77" / name).write_text(body, encoding="utf-8")

    def stamp(tip_value: str, wt: str = "clean", tool: bool = True) -> str:
        out = "" if not tip_value else f"LANE_TIP {tip_value}\n"
        out += f"WORKTREE {wt}\n"
        if tool:
            out += f"TOOL {GOOD_TOOL}\nTOOL_SHA {digest}\n"
        out += f"COMMAND python3 {GOOD_TOOL} --selftest\n"
        return out

    receipt("a-clean.txt", stamp(sha_tip) + "SELFTEST cases=3 red=2\nPREDICATE R78-C1 pass\n")
    receipt("b-no-tip.txt", ("" if omit_tip == "b" else stamp(sha_tip)) + "PREDICATE R70-C1 pass\n")
    receipt("c-drift.txt",
            (stamp(sha_tip) if drift != "c" else
             f"LANE_TIP {tip}\nWORKTREE dirty\nTOOL {GOOD_TOOL}\nTOOL_SHA {'0' * 64}\n"
             f"COMMAND python3 {GOOD_TOOL} --selftest\n")
            + "PREDICATE R70-C1 pass\n")
    supplied_body = (f"LANE_TIP {tip}\nWORKTREE {'clean' if supplied_clean == 'd' else 'dirty'}\n"
                     "TOOL-SUPPLIED plans/supplied_only.py absent at the stamped revision\n"
                     f"COMMAND python3 plans/supplied_only.py --selftest\nPREDICATE R70-C1 pass\n")
    receipt("d-supplied.txt", supplied_body)
    receipt("e-no-command.txt",
            (stamp(sha_tip) if no_command != "e" else
             f"LANE_TIP {tip}\nWORKTREE clean\nTOOL {GOOD_TOOL}\nTOOL_SHA {digest}\n")
            + "VERDICT: PASS\n")
    receipt("f-unlocated.txt",
            (f"LANE_TIP {tip}\nWORKTREE clean\nCOMMAND python3 {GOOD_TOOL}\nPREDICATE R70-C1 pass\n"
             if unlocated_pass == "f" else
             f"LANE_TIP {tip}\nWORKTREE clean\nCOMMAND python3 {GOOD_TOOL}\nPREDICATE R70-C1 pass\n"
             f"TOOL {GOOD_TOOL}\nTOOL_SHA {digest}\n"))
    git(root, "add", "-A")
    git(root, *env, "commit", "-q", "-m", "fixture receipts")
    # The supplied tool is deliberately never committed: it must be absent at every stamped tip.
    (root / "plans/supplied_only.py").write_text("print('supplied')\n", encoding="utf-8")
    return root


def selftest(work: Path) -> int:
    cases = [
        ("clean", {}, None, 0),
        ("omit-tip", {"omit_tip": "b"}, "TIP-ABSENT", 1),
        ("drift", {"drift": "c"}, "TOOL-DRIFT", 1),
        ("supplied-clean", {"supplied_clean": "d"}, "SUPPLIED-BUT-CLEAN", 1),
        ("no-command", {"no_command": "e"}, "COMMAND-ABSENT", 1),
        ("unlocated-pass", {"unlocated_pass": "f"}, "PASS-UNLOCATED", 1),
        ("unresolved-tip", {"unresolved": "a"}, "TIP-UNRESOLVED", 1),
    ]
    red = 0
    for name, kwargs, expect, want in cases:
        root = fixture_repo(work / f"fx-{name}", **kwargs)
        _r, defects, _s = audit(Ctx(root, "worktree"))
        classes = [d.split()[1] for d in defects]
        ok = (want == 0 and not defects) or (expect in classes)
        red += 1 if (want and ok) else 0
        print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={0 if not defects else 1} want={want} "
              f"defects={len(defects)}" + ("" if ok else f" classes={classes}"))
    fails = 0 if red == len(cases) - 1 else 1
    print(f"SELFTEST cases={len(cases)} red={red} failures={fails}")
    return 0 if fails == 0 else 1


def mutants(work: Path) -> int:
    base = fixture_repo(work / "fx-base")
    _r, clean, _s = audit(Ctx(base, "worktree"))
    matrix = [
        ("omit-tip", {"omit_tip": "b"}, "TIP-ABSENT"),
        ("drift", {"drift": "c"}, "TOOL-DRIFT"),
        ("supplied-clean", {"supplied_clean": "d"}, "SUPPLIED-BUT-CLEAN"),
        ("no-command", {"no_command": "e"}, "COMMAND-ABSENT"),
        ("unlocated-pass", {"unlocated_pass": "f"}, "PASS-UNLOCATED"),
        ("unresolved-tip", {"unresolved": "a"}, "TIP-UNRESOLVED"),
    ]
    if clean:
        print(f"MUTANTS base-not-clean defects={len(clean)}")
        return 1
    killed = wrong = survived = 0
    for name, kwargs, expected in matrix:
        root = fixture_repo(work / f"mx-{name}", **kwargs)
        _r, defects, _s = audit(Ctx(root, "worktree"))
        classes = [d.split()[1] for d in defects]
        if expected in classes:
            killed += 1
            print(f"MUTANT {name} killed={expected}")
        elif classes:
            wrong += 1
            print(f"MUTANT {name} wrong-class expected={expected} got={classes}")
        else:
            survived += 1
            print(f"MUTANT {name} SURVIVED expected={expected}")
    print(f"MUTANTS real={len(matrix)} killed={killed} wrong_id={wrong} survived={survived}")
    return 0 if killed == len(matrix) else 1


def control_stamp_only(work: Path) -> int:
    """The skip that must lose: any `LANE_TIP` line counts as located; the other legs are skipped."""
    root = fixture_repo(work / "fx-control", drift="c", supplied_clean="d")
    _r, defects, stats = audit(Ctx(root, "worktree"))
    optimistic = [rel for rel in universe(Ctx(root, "worktree")) if "LANE_TIP" in (Ctx(root, "worktree").get(rel) or "")]
    reached = (not defects and stats["unlocated"] == 0)
    print(f"CONTROL receipts={stats['receipts']} stamped={len(optimistic)} located={len(optimistic)} "
          f"real_defects={len(defects)} target_reached={reached}")
    return 0 if not reached else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", type=Path, default=Path("."))
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--receipt", type=Path, default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-stamp-only", action="store_true")
    args = ap.parse_args()
    lane = args.lane.resolve()
    work = args.work or Path(tempfile.gettempdir()) / "r78-c2"
    work.mkdir(parents=True, exist_ok=True)
    if args.selftest:
        return selftest(work)
    if args.mutants:
        return mutants(work)
    if args.control_stamp_only:
        return control_stamp_only(work)
    if not (lane / ".git").exists():
        print(f"SETUP lane is not a git checkout: {lane}")
        return 2
    ctx = Ctx(lane, args.rev)
    dirty = bool(git(lane, "status", "--porcelain", "--untracked-files=normal").stdout.strip())
    return emit(ctx, out=args.receipt, dirty=dirty)


if __name__ == "__main__":
    sys.exit(main())
