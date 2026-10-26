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
`REFUSE <reason>` line (stderr) and no ledger statement: row and per-ledger lines are buffered and
flushed only after every ledger has been evaluated (round-38 F2, round-39 R5b).

Ref provenance (round-38 routed D4/F1, `.ufo/waves/round-38/falsify/F38LedgerTip.md`; round-39 R5b).
Both pin-kind check bodies name a branch ref: `plans/defect_ledger.py:29` and
`plans/round36_c1_verify.py:38` each hold `BRANCH = "refs/heads/master"`. Neither file is edited here
— `plans/defect_ledger.py` is pinned by `plans/pkg-spec-r35.json` `frozen_instruments` (gate clause
P1) and `plans/round36_c1_verify.py` is pinned by `plans/round38_c1_verify.py` PINS — so the driver
resolves every such ref itself, binds each imported module's `BRANCH` to the commit it printed, and
states what it audits before any row is evaluated:

  REF AUDIT ref=<ref> rev=<sha> tip=<sha> state=match
      the ref resolves to the commit under audit; the body is bound to that sha.
  REF BIND ref=<ref> rev=<sha> tip=<sha> source_ref=<sha|absent> why=clone-lacks-ref
      the clone does not carry the ref (`git clone` of a detached source has no local branch, so
      before round 38 both pin rows raised `ls-tree … refs/heads/master` exit 128 from a healthy
      tree and the exception was folded into `observed=fail agree=NO`); the body is bound to the
      commit under audit and the source's value, when any, is printed.
  REFUSE stale pin ref … (exit 2)
      the ref exists but resolves to a commit other than the one under audit. Reading it would make
      a pin row observe a tree the `TIP commit=` line does not name — measured at round 38 as
      `rows=9 … mismatches=2`, exit 1, from a clean tree, with no line naming the ref
      (`.ufo/waves/round-38/falsify/F38LedgerTip/06-control-stale-master.log`) — so a stale ref is a
      setup refusal before any ledger statement, not a row outcome. The `TIP commit=` line is printed
      first, so the refusal names both revisions.
Because a body's ref is replaced by the sha the driver printed, what a row reads cannot change under
it mid-run, and the printed provenance is the whole story. A `CalledProcessError` raised by a check
body (git could not read the tree) is likewise a setup refusal at exit 2, never a mismatch, and the
buffered row lines are dropped, so `1` keeps meaning "a ledger row disagrees".

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


def audit_pin_refs(lane, modules, tip, source):
    """State the revision each pin row reads, or refuse a ref that names another commit.

    Every ref a check body names is resolved once, printed once, and bound into every module that
    reads it, so the observed tree is the commit that was printed. An absent ref is bound to the
    commit under audit (`REF BIND`, the detached-clone case of round 38 D4). A ref that resolves to
    anything but the commit under audit is refused at exit 2 before any ledger statement (round-39
    R5b: the round-38 F1 harm — a pin row read a stale `refs/heads/master` and reded a clean tree
    with no provenance line).
    """
    bound = {}  # ref -> the commit every body naming it is bound to, so a shared ref prints once
    for rel, mod in modules.items():
        ref = getattr(mod, "BRANCH", None)
        if not ref:
            continue
        if ref in bound:
            setattr(mod, "BRANCH", bound[ref])
            continue
        rev = git_out(lane, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        if rev and rev != tip:
            refuse(f"stale pin ref: {ref} resolves to {rev} in {lane} but the commit under audit is "
                   f"{tip}; {rel} would observe a different tree (check out that ref or delete it, "
                   f"or audit {rev} instead)")
        if rev:
            bound[ref] = rev
            setattr(mod, "BRANCH", rev)
            print(f"REF AUDIT ref={ref} rev={rev} tip={tip} state=match")
            continue
        if not tip:
            refuse(f"{rel} pins {ref} and no commit is under audit")
        bound[ref] = tip
        setattr(mod, "BRANCH", tip)
        src = (git_out(source, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
               if source else None)
        print(f"REF BIND ref={ref} rev={tip} tip={tip} source_ref={src or 'absent'} "
              f"why=clone-lacks-ref")


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
    audit_pin_refs(lane, modules, head, source)
    rows = closed = passed = mism = 0
    statements = []  # buffered: a refusal must leave no ledger statement behind (round-38 F2)
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
            statements.append(f"{r['id']} status={st} observed={'pass' if ok else 'fail'} "
                              f"agree={'yes' if agree else 'NO'} {tail}".rstrip()
                              + f" ledger={ledger_rel} kind={kind}")
        statements.append(f"LEDGER {ledger_rel} rows={len(ledger)} closed={lclosed} "
                          f"observed_pass={lpassed} mismatches={lmism}")
    for line in statements:
        print(line)
    print(f"rows={rows} closed={closed} observed_pass={passed} mismatches={mism}")
    return 0 if (rows and mism == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
