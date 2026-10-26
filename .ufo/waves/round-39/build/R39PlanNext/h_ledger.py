#!/usr/bin/env python3
"""R39PlanNext harness: mutants of plans/ledger_tip.py (post-D4) vs fixture detectors."""
import os, pathlib, re, shutil, subprocess, sys, json
from concurrent.futures import ThreadPoolExecutor

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/R39PlanNext")
BASE = S / "lane"
TAG = os.environ.get("TAG", "")
FX = S / ("fx_ledger" + TAG)
MUT = S / ("mut_ledger" + TAG)
TOOL = pathlib.Path(os.environ.get("TOOL") or (BASE / "plans/ledger_tip.py"))
SRC = TOOL.read_text()


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True)


def clone(name, shared_from=BASE):
    d = FX / name
    if d.exists():
        shutil.rmtree(d)
    r = sh("git", "clone", "-q", "--shared", str(shared_from), str(d))
    assert r.returncode == 0, r.stderr
    return d


FIXT = []
def fx(fid, group):
    def deco(f):
        FIXT.append((fid, f, group)); return f
    return deco

# each builder returns argv tail given a fresh clone dir `d` (the fixture tree) and a work dir `w`
@fx("T00-control-tip", "tip")
def _(d, w): return ["--lane", str(d)]

@fx("T01-source-normal", "tip")
def _(d, w): return ["--source", str(d), "--work", str(w)]

@fx("T02-source-no-master (D4)", "d4")
def _(d, w):
    sh("git", "-C", str(d), "checkout", "-q", "--detach", cwd=d)
    sh("git", "-C", str(d), "branch", "-D", "master")
    return ["--source", str(d), "--work", str(w)]

@fx("T03-source-stale-master (R5 shape)", "new")
def _(d, w):
    # master exists but points at an older commit; HEAD (tip under audit) is detached at the tip
    sh("git", "-C", str(d), "checkout", "-q", "--detach", cwd=d)
    sh("git", "-C", str(d), "branch", "-f", "master", "HEAD~6")
    return ["--source", str(d), "--work", str(w)]

@fx("T04-control-untracked-r34-path", "new")
def _(d, w):
    p = d / "plans/round34_defects.py"; p.write_text("# untracked\n")
    return ["--lane", str(d)]

@fx("T05-control-row-flipped-open", "new")
def _(d, w):
    p = d / "corpus/defects.jsonl"
    t = p.read_text(); t2 = t.replace('"check": "r34_d2", "status": "closed"', '"check": "r34_d2", "status": "open"')
    assert t != t2; p.write_text(t2)
    return ["--lane", str(d)]

@fx("T06-control-empty-ledgers", "new")
def _(d, w):
    (d / "corpus/defects.jsonl").write_text(""); (d / "corpus/defects-round35.jsonl").write_text("")
    return ["--lane", str(d)]

@fx("T07-control-unknown-check", "new")
def _(d, w):
    p = d / "corpus/defects.jsonl"; t = p.read_text()
    p.write_text(t.replace('"check": "r34_d5"', '"check": "r34_nope"')); return ["--lane", str(d)]

@fx("T08-source-not-a-repo", "new")
def _(d, w):
    nd = FX / "not-a-repo"; nd.mkdir(exist_ok=True)
    return ["--source", str(nd), "--work", str(w)]

@fx("T09-source-work-exists", "new")
def _(d, w):
    (w / "lane").mkdir(parents=True, exist_ok=True)
    return ["--source", str(d), "--work", str(w)]

@fx("T10-control-check-crashes", "new")
def _(d, w):
    (d / "plans/../.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS").unlink(); return ["--lane", str(d)]

@fx("T11-control-dirty-tree", "new")
def _(d, w):
    (d / "scratch.txt").write_text("x\n"); return ["--lane", str(d)]

@fx("T12-control-closed-row-fails-live", "new")
def _(d, w):
    # R35 live check: untracked file in the whole-lane set
    (d / "corpus/untracked-r39.md").write_text("x\n"); return ["--lane", str(d)]


NORM = [(re.compile(re.escape(str(S)) + r"[^\s:]*"), "<P>"), (re.compile(r"\b[0-9a-f]{40}\b"), "<sha>")]
def norm(t):
    for rx, rep in NORM:
        t = rx.sub(rep, t)
    return t


def run_tool(tool, argv, d):
    r = subprocess.run([sys.executable, str(tool)] + argv, capture_output=True, text=True, cwd=d,
                       env=dict(os.environ, TMPDIR=str(S)))
    return {"rc": r.returncode, "out": norm(r.stdout), "err": norm(r.stderr.strip().splitlines()[0] if r.stderr.strip() else "")}


MUTANTS = []
def mut(mid, old, new, note): MUTANTS.append((mid, old, new, note))

mut("L01", "    raise SystemExit(2)\n\n\ndef load_module", "    raise SystemExit(1)\n\n\ndef load_module", "refuse exits 1 not 2")
mut("L02", 'if git_out(lane, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"):\n            continue', 'if True:\n            continue', "never bind a missing pin ref")
mut("L03", '        setattr(mod, "BRANCH", tip)\n        src =', '        pass\n        src =', "bind recorded but not applied")
mut("L04", '        print(f"REF BIND ref={ref} rev={tip} source_ref={src or \'absent\'} why=clone-lacks-ref")', '        pass', "REF BIND provenance line dropped")
mut("L05", 'agree = (is_closed and ok) or (st == "open" and not ok)', 'agree = ok', "open-row staleness ignored")
mut("L06", "return 0 if (rows and mism == 0) else 1", "return 0 if mism == 0 else 1", "zero rows accepted")
mut("L07", "            mism += not agree\n            lclosed", "            mism += 0\n            lclosed", "global mismatch count never rises")
mut("L08", "            passed += ok\n            mism", "            passed += 1\n            mism", "observed_pass counts every row")
mut("L09", "            closed += is_closed\n            passed", "            closed += 1\n            passed", "closed counts every row")
mut("L10", "                    refuse(f\"check {r.get('check')} could not query {lane}: {e}\")", "                    ok, note = False, f\"error {e}\"", "CalledProcessError folded back into a mismatch (D4 revert)")
mut("L11", "    if dest.exists():\n        refuse", "    if False:\n        refuse", "existing clone dir reused (clone then fails)")
mut("L12", "    if dirty:\n        refuse(f\"clone is not clean", "    if False:\n        refuse(f\"clone is not clean", "clean-tree refusal off")
mut("L13", "if top is None or pathlib.Path(top).resolve() != dest.resolve():", "if False:", "clone top check off")
mut("L14", "                    ok, note = False, f\"error {type(e).__name__}: {e}\"", "                    ok, note = True, f\"error {type(e).__name__}: {e}\"", "check crash counted as pass")
mut("L15", "                ok, note = False, f\"unknown check {r.get('check')!r}\"", "                ok, note = True, f\"unknown check {r.get('check')!r}\"", "unknown check counted as pass")
mut("L16", "        if ref in bound:\n            setattr(mod, \"BRANCH\", bound[ref])\n            continue\n", "", "second ledger rebinding prints REF BIND twice")
mut("L17", '"r34_d1": "live"', '"r34_d1": "pin"', "kind label flips")
mut("L18", "dirty = len([x for x in dirty_txt.splitlines() if x])", "dirty = 0", "control-mode dirty count lost")
mut("L19", "refuse(f\"{rel} pins {ref} and no commit is under audit\")", "return", "no-tip refusal (unreachable)")
mut("L20", "        if ref in bound:\n            setattr(mod, \"BRANCH\", bound[ref])", "        if ref in bound:\n            setattr(mod, \"BRANCH\", tip)", "shared-ref rebinding to tip (equivalent)")


def main():
    FX.mkdir(exist_ok=True); MUT.mkdir(exist_ok=True)
    built = {}
    for fid, b, g in FIXT:
        name = fid.split(" ")[0]
        d = clone(name)
        w = FX / (name + "-w")
        if w.exists(): shutil.rmtree(w)
        built[fid] = (d, b(d, w), w)

    def one(tool, fid):
        d, argv, w = built[fid]
        # clones made by the tool go to w/lane: reset w between runs (T09 keeps its pre-made w/lane)
        if w.exists() and not fid.startswith("T09"):
            shutil.rmtree(w)
        if fid.startswith("T09"):
            shutil.rmtree(w / "lane", ignore_errors=True); (w / "lane").mkdir(parents=True)
        return run_tool(tool, argv, d)

    ref = {}
    for fid in built:
        ref[fid] = one(TOOL, fid)
    print("== pristine verdicts ==")
    for fid, r in ref.items():
        last = [l for l in r["out"].splitlines() if l.startswith("rows=")]
        print(f"{fid:40s} rc={r['rc']} {last[-1] if last else '-'} refbind={len(re.findall('REF BIND', r['out']))} err={r['err'][:100]}")
    groups = {fid: g for fid, _, g in FIXT}
    tot = {"tip": 0, "tip+d4": 0, "all": 0}
    n = 0
    for mid, old, new, note in MUTANTS:
        if SRC.count(old) != 1:
            print(f"{mid}: SETUP needle count {SRC.count(old)}"); continue
        mp = MUT / f"{mid}.py"; mp.write_text(SRC.replace(old, new, 1))
        kills = []
        for fid in built:
            r = one(mp, fid)
            if r != ref[fid]:
                kills.append(fid.split(" ")[0] + ":" + ("rc" if r["rc"] != ref[fid]["rc"] else "text"))
        n += 1
        kt = [k for k in kills if groups[[f for f in built if f.startswith(k.split(':')[0])][0]] == "tip"]
        k4 = [k for k in kills if groups[[f for f in built if f.startswith(k.split(':')[0])][0]] in ("tip", "d4")]
        tot["tip"] += bool(kt); tot["tip+d4"] += bool(k4); tot["all"] += bool(kills)
        print(f"{mid} tip={'K' if kt else '-'} tip+d4={'K' if k4 else '-'} all={'K' if kills else '-'}  {note}  killers={kills[:8]}")
    print(f"MUTANTS n={n} killed_by_tip={tot['tip']} killed_by_tip+d4={tot['tip+d4']} killed_by_all={tot['all']}")


if __name__ == "__main__":
    main()
