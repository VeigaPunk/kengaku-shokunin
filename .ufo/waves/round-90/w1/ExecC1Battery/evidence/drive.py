#!/usr/bin/env python3
"""ExecC1Battery fixture driver. Builds fixture clones under S only; never touches the lane tree."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r90/ExecC1Battery")
L = S / "lane"
W = S / "ctl"
W.mkdir(parents=True, exist_ok=True)
B = "664435cfcb9419c4e8ac7828a55aec11a1f36ec4"
BASE = "dcdd494ef4b4a6c0ae349ecb597527124ee54f91"
C1 = L / "plans/round90_c1_replay.py"
C2 = L / "plans/round90_counter_pin.py"
PROBE = "plans/round90_polydiff_probe.py"
LEDGER = "plans/grader-population-ledger.json"
RECEIPT = "corpus/evidence/round90/merge-diff-probe.txt"
MEMBER = "merge-diff-arc-agi-task"
SMOKE = (S / "w4/receipt-smoke.txt").read_text()
results = {}


def run(args, cwd=None, timeout=900):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def git(repo, *args):
    return run(["git", "-C", str(repo), *args])


def must_git(repo, *args):
    rc, o, e = git(repo, *args)
    if rc:
        raise SystemExit(f"git {args} rc={rc} stderr={e[-300:]!r}")
    return o.strip()


def fixture(name):
    base = Path(tempfile.mkdtemp(prefix=name + ".", dir=S))
    repo = base / "repo"
    rc, o, e = run(["git", "clone", "-q", "--no-hardlinks", str(L), str(repo)])
    if rc:
        raise SystemExit(f"clone rc={rc} {e[-300:]!r}")
    top = must_git(repo, "rev-parse", "--show-toplevel")
    assert top == str(repo), (top, repo)
    return repo


def commit(repo, paths, msg):
    assert must_git(repo, "rev-parse", "--show-toplevel") == str(repo)
    must_git(repo, "add", "--", *paths)
    rc, o, e = run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-q", "-m", msg])
    if rc:
        raise SystemExit(f"commit rc={rc} {e[-300:]!r}")
    return must_git(repo, "rev-parse", "HEAD")


def flip_ledger(repo):
    p = repo / LEDGER
    d = json.loads(p.read_text())
    row = d["members"][MEMBER]
    d["members"][MEMBER] = {"classes": row["classes"], "receipt": RECEIPT, "round": 90,
                            "status": "executed", "subject": "tb2-header", "verdict": "cases"}
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def write_receipt(repo, text):
    target = repo / RECEIPT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def counter(repo, rev, tag):
    rc, o, e = run(["python3", str(C1), "--lane", str(repo), "--rev", rev, "--work", str(W / tag)])
    (W / f"{tag}.out").write_text(o)
    (W / f"{tag}.err").write_text(e)
    defects = [x for x in o.splitlines() if x.startswith("DEFECT")]
    target = [x for x in o.splitlines() if x.startswith("TARGET")]
    pred = [x for x in o.splitlines() if x.startswith("PREDICATE")]
    results[tag] = {"rc": rc, "defects": defects, "target": target, "predicate": pred,
                    "stderr_tail": e[-300:], "repo": str(repo), "rev": rev}
    return rc, o, defects


def build_tip(ledger):
    repo = fixture("tip" + ("-ledger" if ledger else ""))
    sib = must_git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit-tree",
                   f"{BASE}^{{tree}}", "-p", BASE, "-m", "sibling commit, not an ancestor of B")
    stamp = SMOKE.replace(f"LANE_TIP {B}", f"LANE_TIP {sib}", 1)
    assert stamp != SMOKE
    write_receipt(repo, stamp)
    paths = [RECEIPT]
    if ledger:
        flip_ledger(repo)
        paths.append(LEDGER)
    head = commit(repo, paths, "forged tip: LANE_TIP names a sibling commit")
    results.setdefault("_fixtures", {})["tip" + ("-ledger" if ledger else "")] = {"sib": sib, "head": head}
    return repo, head


def build_ledger_only():
    repo = fixture("ledger-only")
    flip_ledger(repo)
    head = commit(repo, [LEDGER], "ledger flip without receipt")
    results.setdefault("_fixtures", {})["ledger-only"] = {"head": head}
    return repo, head


def build_probe(ledger):
    repo = fixture("probe" + ("-ledger" if ledger else ""))
    tool = repo / PROBE
    src = tool.read_text()
    old = "        payload = run_case(staged, work, case)\n"
    assert src.count(old) == 1, src.count(old)
    new = ('        payload = {"tests": [[name, letter, ""] for name, letter in zip(TESTS, case["predicted"])]}\n')
    tool.write_text(src.replace(old, new))
    rc, o, e = run(["python3", str(tool), "--lane", str(repo), "--work", str(S / "ctl/forge-work")])
    assert rc == 0 and "PREDICATE R90-PROBE pass" in o, (rc, e[-300:])
    write_receipt(repo, o)
    paths = [PROBE, RECEIPT]
    if ledger:
        flip_ledger(repo)
        paths.append(LEDGER)
    head = commit(repo, paths, "forged probe echoes predicted vectors + regenerated receipt")
    results.setdefault("_fixtures", {})["probe" + ("-ledger" if ledger else "")] = {"head": head,
        "forged_tool_sha": must_git(repo, "hash-object", str(tool))}
    return repo, head


def build_positive():
    repo = fixture("positive")
    write_receipt(repo, SMOKE)
    flip_ledger(repo)
    head = commit(repo, [RECEIPT, LEDGER], "legitimate receipt at B + ledger flip (positive fixture)")
    results.setdefault("_fixtures", {})["positive"] = {"head": head}
    return repo, head


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("== controls 1-3 + positive fixture")
    repo, head = build_tip(False)
    counter(repo, "HEAD", "c1-forged-tip")
    repo, head = build_tip(True)
    counter(repo, "HEAD", "c1-forged-tip-with-ledger")
    repo, head = build_ledger_only()
    counter(repo, "HEAD", "c2-ledger-only")
    repo, head = build_probe(False)
    counter(repo, "HEAD", "c3-forged-probe")
    repo, head = build_probe(True)
    counter(repo, "HEAD", "c3-forged-probe-with-ledger")
    repo, pos_head = build_positive()
    counter(repo, "HEAD", "x-positive-c1")
    print("== separation")
    # 5a: worktree-only deletion of pin files in a clone at B
    wt = fixture("sep-worktree")
    (wt / "plans/counter-pins-r90.json").unlink()
    (wt / "plans/round90_counter_pin.py").unlink()
    counter(wt, B, "c5a-c1-pins-deleted-worktree")
    # 5b: committed deletion of pin files, counter run at the deletion commit
    sc = fixture("sep-committed")
    must_git(sc, "rm", "-q", "--", "plans/counter-pins-r90.json", "plans/round90_counter_pin.py")
    rc_commit = run(["git", "-C", str(sc), "-c", "user.name=t", "-c", "user.email=t@t",
                     "commit", "-q", "-m", "delete pin ledger and checker (separation control)"])
    assert rc_commit[0] == 0, rc_commit
    counter(sc, "HEAD", "c5b-c1-pins-deleted-committed")
    # 5c: C2 checker verdict with the C1 receipt absent + ledger unflipped (at B) and with receipt+flip
    rc, o, e = run(["python3", str(C2), "--lane", str(L), "--rev", B, "--work", str(W / "c5c-c2-at-B")])
    results["c5c-c2-at-B"] = {"rc": rc, "out": o, "err_tail": e[-300:]}
    rc, o, e = run(["python3", str(C2), "--lane", str(repo), "--rev", pos_head,
                    "--work", str(W / "c5c-c2-at-positive")])
    results["c5c-c2-at-positive"] = {"rc": rc, "out": o, "err_tail": e[-300:]}
    rc, o, e = run(["python3", str(C2), "--lane", str(L), "--rev", BASE, "--work", str(W / "c5-c2-at-base")])
    results["c5-c2-at-base"] = {"rc": rc, "out": o, "err_tail": e[-300:]}
    print("== control 6: do-nothing at BASE")
    counter(L, BASE, "c6-do-nothing-base")
    print("== control 4: positive probe smoke at B")
    rc, o, e = run(["python3", str(PROBE), "--lane", str(L), "--work", str(W / "c4-smoke")])
    (W / "c4-smoke.out").write_text(o)
    results["c4-smoke"] = {"rc": rc, "cases": [x for x in o.splitlines() if x.startswith("CASE")],
                           "summary": [x for x in o.splitlines() if x.startswith("cases=") or x.startswith("PREDICATE")],
                           "err_tail": e[-300:]}
    (W / "summary.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    for k, v in results.items():
        if k.startswith("_"):
            print(k, json.dumps(v))
            continue
        if "defects" in v:
            print(f"--- {k} rc={v['rc']}")
            for d in v["defects"]:
                print("   " + d)
            for t in v["target"] + v["predicate"]:
                print("   " + t)
        else:
            print(f"--- {k} rc={v.get('rc')}")
            if "out" in v:
                print("   " + v["out"].replace("\n", "\n   "))
            for key in ("cases", "summary"):
                for line in v.get(key, []) if isinstance(v.get(key), list) else []:
                    print("   " + line)


if __name__ == "__main__":
    main()
