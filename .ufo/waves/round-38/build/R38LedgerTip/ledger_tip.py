#!/usr/bin/env python3
"""Ledger-at-tip re-runner (round 37 wave 1, considerthese/2026-10-25.md proposal 2(a)).

Re-runs EVERY routed-defect row's check at the lane tip, on a clean shared clone of the lane,
using the two check bodies of record:
  corpus/defects.jsonl        -> plans/defect_ledger.py      CHECKS (r34_d1..r34_d5)
  corpus/defects-round35.jsonl -> plans/round36_c1_verify.py CHECKS (r35_d1..r35_d4)
No ledger row and no check body is edited here: the clone's tip bytes are imported as-is, so a
check that fails fails on the tip, not on a local rewrite.

Per row it prints
  <id> status=<open|closed> observed=<pass|fail> agree=<yes|NO> <check note> ledger=<file> kind=<pin|live>
  kind=live  the check exercises behaviour (runs the package gate, the battery, the line fixtures,
             a repo-state query with a zero-tolerance observation)
  kind=pin   the check only pins closure bytes (a manifest digest list, a committed path count, a
             correction/erratum line, a quote's presence in a frozen capture); a pin failing means
             the closure evidence moved, not that the defect class came back
and then the summary line
  rows=<n> closed=<n> observed_pass=<n> mismatches=<n>
mismatches counts every closed row whose check fails plus every open row whose check passes (stale
self-assessment), exactly as the two checkers of record define it.

Exit codes are the registry row's contract (SKILL.md:581): `0` no mismatch · `1` a ledger row
genuinely disagrees with its observation · `2` usage/clone/setup refusal, i.e. the tree could not be
evaluated and therefore no ledger statement is made. A refusal prints exactly one
`REFUSE <reason>` line (stderr) and no summary line.

Detached-clone refs (round-38 routed D4; `.ufo/waves/round-37/falsify/F37NoHarmSweep.md` §3). Both
pin-kind check bodies name a branch ref: `plans/defect_ledger.py:29` and `plans/round36_c1_verify.py:38`
each hold `BRANCH = "refs/heads/master"`. Neither file is edited here — `plans/defect_ledger.py` is
pinned by `plans/pkg-spec-r35.json` `frozen_instruments` (gate clause P1) and
`plans/round36_c1_verify.py` is pinned by `plans/round38_c1_verify.py` PINS — so the binding is done by
the driver: after the clone, every imported module's `BRANCH` is read; if the clone carries that ref it
is left alone (normal clones, byte-identical output to before), and if it does not, the module's
`BRANCH` is bound to the commit under audit (the clone's HEAD, the same commit the `TIP commit=` line
names) and one line is printed per binding:

  REF BIND ref=<ref> rev=<rev> source_ref=<sha|absent> why=clone-lacks-ref

`git clone` of a detached source produces a clone with no local branch, so before this binding both
pin rows raised `ls-tree … refs/heads/master` exit 128 from a healthy tree and the exception was
folded into `observed=fail agree=NO` — a false red at exit 1 in the clone shape the fleet's fixture
rule mandates. A `CalledProcessError` from any check body (git could not read the tree) is now a setup
refusal at exit 2, not a mismatch, so `1` keeps meaning "a ledger row disagrees".

Usage:
  python3 ledger_tip.py --source /path/to/lane --work /path/to/scratch
The clone is created at <work>/lane (must not exist), verified with rev-parse --show-toplevel, and
left in place for inspection; the caller removes the scratch tree.
  python3 ledger_tip.py --lane /path/to/clone            (control mode)
runs the same checks on an already prepared tree WITHOUT the clean-tree refusal, so a deliberately
broken clone can be used to show each check still bites. Control mode prints `dirty=<n>`.
"""
import argparse
import importlib.util
import json
import pathlib
import subprocess
import sys

LEDGERS = (
    ("corpus/defects.jsonl", "plans/defect_ledger.py"),
    ("corpus/defects-round35.jsonl", "plans/round36_c1_verify.py"),
)

# Closure-byte pins vs behaviour checks. Both kinds may be `closed` in the ledger; only a failing
# `live` row is a behavioural regression.
KIND = {
    "r34_d1": "live",   # git ls-files --others over the round-34 paths
    "r34_d2": "pin",    # committed path count under three fixed mirror roots
    "r34_d3": "pin",    # SHA256SUMS digest list of a frozen capture
    "r34_d4": "pin",    # the SCORECARD correction line still says what it said
    "r34_d5": "pin",    # frozen capture quote + erratum/mistake rows
    "r35_d1": "live",   # 14-fixture battery + genuine package re-run through the gate
    "r35_d2": "live",   # whole-lane untracked set + 6 directional line fixtures
    "r35_d3": "pin",    # committed nested-wave path count at the branch tip
    "r35_d4": "pin",    # toolathlon recount vs the round-36 erratum line
}


def refuse(msg):
    """Setup/clone/usage refusal: exit 2, never 1 (the row's declared code for a clone problem)."""
    print(f"REFUSE {msg}", file=sys.stderr)
    raise SystemExit(2)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        refuse(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        refuse(f"cannot import {path}: {type(e).__name__}: {e}")
    return mod


def git_out(lane, *args):
    """stdout of a git command, or None when git could not answer (ref absent, not a repo)."""
    r = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def clone_lane(source, work):
    if git_out(source, "rev-parse", "--git-dir") is None:
        refuse(f"--source {source} is not a readable git repository")
    dest = work / "lane"
    if dest.exists():
        refuse(f"will not reuse {dest}; remove it first")
    r = subprocess.run(["git", "-c", "advice.detachedHead=false", "clone", "-q", "--shared",
                        str(source), str(dest)], capture_output=True, text=True)
    if r.returncode != 0:
        tail = (r.stderr.strip().splitlines() or [""])[-1]
        refuse(f"git clone --shared {source} failed rc={r.returncode}: {tail[:160]}")
    top = git_out(dest, "rev-parse", "--show-toplevel")
    if top is None or pathlib.Path(top).resolve() != dest.resolve():
        refuse(f"clone top {top} != {dest}")
    head = git_out(dest, "rev-parse", "HEAD")
    if head is None:
        refuse(f"clone {dest} has no resolvable HEAD")
    dirty = git_out(dest, "status", "--porcelain")
    if dirty is None:
        refuse(f"clone {dest} cannot be queried with git status")
    if dirty:
        refuse(f"clone is not clean:\n{dirty}")
    return dest, head


def bind_pin_refs(lane, modules, tip, source):
    """Make each check body's hard-coded pin ref resolve in `lane`.

    A ref the clone already carries is left untouched. A ref it lacks (a `git clone` of a detached
    source has no local branch) is bound to the commit under audit and reported, so the pin observes
    the same tree as the `TIP commit=` line instead of raising exit 128.
    """
    bound = {}  # ref -> the commit it was bound to, so a ref shared by both ledgers prints once
    for rel, mod in modules.items():
        ref = getattr(mod, "BRANCH", None)
        if not ref:
            continue
        if ref in bound:
            setattr(mod, "BRANCH", bound[ref])
            continue
        if git_out(lane, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"):
            continue
        if not tip:
            refuse(f"{rel} pins {ref} and no commit is under audit")
        bound[ref] = tip
        setattr(mod, "BRANCH", tip)
        src = (git_out(source, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
               if source else None)
        print(f"REF BIND ref={ref} rev={tip} source_ref={src or 'absent'} why=clone-lacks-ref")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="lane to clone (shared, read-only)")
    ap.add_argument("--work", help="scratch dir; clone goes to <work>/lane")
    ap.add_argument("--lane", help="control mode: run on this tree, no clean-tree refusal")
    ap.add_argument("--keep-notes", action="store_true", help="print the check note even on pass")
    a = ap.parse_args()
    if a.lane:
        lane = pathlib.Path(a.lane).resolve()
        head = git_out(lane, "rev-parse", "HEAD")
        if head is None:
            refuse(f"{lane} is not a readable git work tree")
        dirty_txt = git_out(lane, "status", "--porcelain")
        if dirty_txt is None:
            refuse(f"{lane} cannot be queried with git status")
        dirty = len([x for x in dirty_txt.splitlines() if x])
        print(f"TIP commit={head} control={lane} dirty={dirty}")
        source = None
    else:
        if not (a.source and a.work):
            ap.error("either --lane, or both --source and --work")
        work = pathlib.Path(a.work).resolve()
        work.mkdir(parents=True, exist_ok=True)
        source = pathlib.Path(a.source).resolve()
        lane, head = clone_lane(source, work)
        print(f"TIP commit={head} clone={lane}")

    modules = {rel: load_module(rel.replace("/", "_")[:-3], lane / rel) for _l, rel in LEDGERS}
    bind_pin_refs(lane, modules, head, source)
    rows = closed = passed = mism = 0
    for ledger_rel, mod_rel in LEDGERS:
        mod = modules[mod_rel]
        p = lane / ledger_rel
        try:
            ledger = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        except (OSError, ValueError) as e:
            refuse(f"cannot read {ledger_rel}: {type(e).__name__}: {e}")
        lclosed = lpassed = lmism = 0
        for r in ledger:
            fn = mod.CHECKS.get(r.get("check"))
            if fn is None:
                ok, note = False, f"unknown check {r.get('check')!r}"
            else:
                try:
                    ok, note = fn(lane)
                except subprocess.CalledProcessError as e:
                    # git could not read the tree: no observation was made, so this is setup, not a
                    # ledger statement (round-38 routed D4: it used to be folded into agree=NO).
                    refuse(f"check {r.get('check')} could not query {lane}: {e}")
                except Exception as e:  # a crash is an observed failure, never a pass
                    ok, note = False, f"error {type(e).__name__}: {e}"
            st = r.get("status")
            is_closed = st == "closed"
            agree = (is_closed and ok) or (st == "open" and not ok)
            kind = KIND.get(r.get("check"), "unknown")
            rows += 1
            closed += is_closed
            passed += ok
            mism += not agree
            lclosed += is_closed
            lpassed += ok
            lmism += not agree
            tail = note if (a.keep_notes or not ok) else ""
            print(f"{r['id']} status={st} observed={'pass' if ok else 'fail'} "
                  f"agree={'yes' if agree else 'NO'} {tail}".rstrip()
                  + f" ledger={ledger_rel} kind={kind}")
        print(f"LEDGER {ledger_rel} rows={len(ledger)} closed={lclosed} "
              f"observed_pass={lpassed} mismatches={lmism}")
    print(f"rows={rows} closed={closed} observed_pass={passed} mismatches={mism}")
    return 0 if (rows and mism == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
