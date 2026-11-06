#!/usr/bin/env python3
"""MutC1 mutation driver — R99-C1 counter/probe. Fixture-only git plumbing commits on top of T."""
import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r99/MutC1")
CLONE = S / "clone"
G = S / "G"
T = "f72a8bc710b12473b5c768004e2581f980d924f4"
BASE = "2233a66195e3d3d85856248fb8f66c1d8127cede"
RECEIPT = "corpus/evidence/round99/bnfit-probe.txt"
ENV = dict(os.environ, TMPDIR=str(S / "tmp"))


def git(*args, env=None, input=None):
    return subprocess.run(["git", "-C", str(CLONE), *args], capture_output=True, input=input,
                          env=env or ENV)


def show(rev, path):
    p = git("show", f"{rev}:{path}")
    assert p.returncode == 0, (rev, path, p.stderr[:200])
    return p.stdout


def rep(data, old, new, count=1):
    o, n = old.encode(), new.encode()
    got = data.count(o)
    assert got == count, (old[:70], got, count)
    return data.replace(o, n)


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- mutation catalogue -------------------------------------------------
def edits_for(mid):
    """Return {path: new_bytes or None(delete)} for mutant mid, computed from T bytes."""
    e = {}
    receipt = show(T, RECEIPT)
    table = show(T, "plans/round99-cases.json")
    ledger = show(T, "plans/grader-population-ledger.json")
    sources = show(T, "corpus/SOURCES.md")
    probe = show(T, "plans/round99_bnfit_probe.py")
    counter = show(T, "plans/round99_c1_replay.py")
    skill = show(T, "SKILL.md")
    claims = show(T, "plans/round-99-claims.md")

    if mid == "M01":   # receipt CASE observed edit
        e[RECEIPT] = rep(receipt,
            "CASE C01 predicted=P,P,P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,P,P,1 ok=True",
            "CASE C01 predicted=P,P,P,P,P,P,P,P,P,1 observed=F,P,P,P,P,P,P,P,P,1 ok=True")
    elif mid == "M01b":  # receipt drops a case (CASE + DETAIL)
        r = receipt
        for line in (b"CASE C13 predicted=P,P,P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,P,P,1 ok=True\n",
                     b"DETAIL C13 learned=1efe8fe9a8c37901 intervened=458d8ecd0bc5dd7a final=390259ae5b321c23 quantile-grid\n"):
            assert r.count(line) == 1, line
            r = r.replace(line, b"")
        e[RECEIPT] = r
    elif mid == "M02":  # receipt CASE predicted edit (pred==obs, both wrong vs table)
        e[RECEIPT] = rep(receipt,
            "CASE C12 predicted=P,P,P,P,P,P,P,P,F,0 observed=P,P,P,P,P,P,P,P,F,0 ok=True",
            "CASE C12 predicted=P,P,P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,P,P,1 ok=True")
    elif mid == "M03":  # receipt DETAIL digest edit
        e[RECEIPT] = rep(receipt,
            "DETAIL C03 learned=1efe8fe9a8c37901 intervened=458d8ecd0bc5dd7a final=a9ad7f5f874cd77f marginal-only",
            "DETAIL C03 learned=1efe8fe9a8c37901 intervened=458d8ecd0bc5dd7a final=a9ad7f5f874cd770 marginal-only")
    elif mid == "M04a":  # LANE_TIP -> descendant (not ancestor)
        e[RECEIPT] = rep(receipt,
            "LANE_TIP 24a5a5554130065917d55618ae10309403abf60d",
            "LANE_TIP 23d580366db2a3462c9bbfc3b0ff71bce5837374")
    elif mid == "M04b":  # LANE_TIP -> an ancestor (BASE), wrong but ancestral
        e[RECEIPT] = rep(receipt,
            "LANE_TIP 24a5a5554130065917d55618ae10309403abf60d",
            "LANE_TIP 2233a66195e3d3d85856248fb8f66c1d8127cede")
    elif mid == "M05":  # case-table predicted edit
        e["plans/round99-cases.json"] = rep(table,
            '"id": "C11",\n   "app": "ks-shift-small",\n   "predicted": "P,P,P,P,P,P,P,P,P,1"',
            '"id": "C11",\n   "app": "ks-shift-small",\n   "predicted": "P,P,P,P,P,P,P,P,F,0"')
    elif mid == "M06":  # ledger class edit (member gains a class)
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '  "bn-fit-modify": {\n   "classes": [\n    "file-artifact"\n   ],',
            '  "bn-fit-modify": {\n   "classes": [\n    "file-artifact",\n    "numeric-band"\n   ],')
    elif mid == "M07":  # ledger round edit
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '"status": "executed",\n   "round": 99,\n   "receipt": "corpus/evidence/round99/bnfit-probe.txt",',
            '"status": "executed",\n   "round": 98,\n   "receipt": "corpus/evidence/round99/bnfit-probe.txt",')
    elif mid == "M08":  # ledger receipt field edit
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '"round": 99,\n   "receipt": "corpus/evidence/round99/bnfit-probe.txt",',
            '"round": 99,\n   "receipt": "corpus/evidence/round99/bnfit-probe2.txt",')
    elif mid == "M09":  # ledger subject edit
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '"receipt": "corpus/evidence/round99/bnfit-probe.txt",\n   "subject": "tb2-header",',
            '"receipt": "corpus/evidence/round99/bnfit-probe.txt",\n   "subject": "tb2-body",')
    elif mid == "M10":  # second member flipped executed -> located
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '"receipt": "corpus/evidence/round38/build-pmars-probe.txt",\n   "round": 38,\n   "status": "executed",',
            '"receipt": "corpus/evidence/round38/build-pmars-probe.txt",\n   "round": 38,\n   "status": "located",')
    elif mid == "M11":  # another executed member loses the file-artifact class
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '  "build-pmars": {\n   "classes": [\n    "file-artifact",\n    "subprocess-exec"\n   ],',
            '  "build-pmars": {\n   "classes": [\n    "subprocess-exec"\n   ],')
    elif mid == "M12":  # SOURCES row added after BASE, unbound -> gate flags it
        row = ("\n| S342 | mutant unbound row — https://example.invalid/mutant | docs | A | mutant | "
               "sha256 0000000000000000000000000000000000000000000000000000000000000000 | mutant | "
               "queued | 2026-11-06 | on-release | — |\n")
        e["corpus/SOURCES.md"] = sources + row.encode()
    elif mid == "M13":  # SOURCES row added after BASE, correctly bound -> gate silent
        row = ("\n| S342 | mutant duplicate of S334 — https://raw.githubusercontent.com/harbor-framework/"
               "terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py | "
               "code | A | mutant | tests/test_outputs.py:150 quote “assert p_value >= 0.001, (” (5 words); "
               "sha256 364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b | mutant | mined | "
               "2026-11-06 | on-release | — |\n")
        e["corpus/SOURCES.md"] = sources + row.encode()
    elif mid == "M14":  # one of the eight new SOURCES rows removed
        lines = sources.decode().splitlines(keepends=True)
        keep = [ln for ln in lines if not ln.startswith("| S341 |")]
        assert len(keep) == len(lines) - 1, (len(keep), len(lines))
        e["corpus/SOURCES.md"] = "".join(keep).encode()
    elif mid == "M15":  # capture byte edit
        e["corpus/evidence/round99/tb2-bn-fit-modify/test_outputs.py"] = show(
            T, "corpus/evidence/round99/tb2-bn-fit-modify/test_outputs.py") + b"\n"
    elif mid == "M16":  # fixture byte edit
        e["corpus/evidence/round99/bn-fit-modify-solution/final_bn_sample.csv"] = show(
            T, "corpus/evidence/round99/bn-fit-modify-solution/final_bn_sample.csv") + b"\n"
    elif mid == "M17":  # probe byte edit, behaviour-neutral comment
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            "from __future__ import annotations\n",
            "from __future__ import annotations\n# mutant comment\n")
    elif mid == "M18":  # counter byte edit, behaviour-neutral comment
        e["plans/round99_c1_replay.py"] = rep(counter,
            "from __future__ import annotations\n",
            "from __future__ import annotations\n# mutant comment\n")
    elif mid == "M19":  # builder C03: draw U instead of D
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'df["D"] = rng.normal(TRUE_MEAN, TRUE_STD, 10000)',
            'df["U"] = rng.normal(TRUE_MEAN, TRUE_STD, 10000)')
    elif mid == "M20":  # builder C03: seed 3 -> 5
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'rng = np.random.default_rng(3)', 'rng = np.random.default_rng(5)')
    elif mid == "M21":  # builder C11: shift 0.045 -> 0.060
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'k = 0.045 if kind == "ks-shift-small" else 0.050',
            'k = 0.060 if kind == "ks-shift-small" else 0.050')
    elif mid == "M22":  # builder C12: shift 0.050 -> 0.040
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'k = 0.045 if kind == "ks-shift-small" else 0.050',
            'k = 0.045 if kind == "ks-shift-small" else 0.040')
    elif mid == "M23":  # builder C13: quantile grid -> seeded random draw
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'df["D"] = norm.ppf((np.arange(10000) + 0.5) / 10000, TRUE_MEAN, TRUE_STD)',
            'df["D"] = np.random.default_rng(7).normal(TRUE_MEAN, TRUE_STD, 10000)')
    elif mid == "M24":  # builder comment only (no byte change in the built app)
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            "# deterministic: a normal quantile grid shifted by k sd",
            "# deterministic: a normal quantile grid shifted by k sd.")
    elif mid == "M25":  # probe stops checking: ok = True
        e["plans/round99_bnfit_probe.py"] = rep(probe,
            'ok = observed == case["predicted"]', 'ok = True')
    elif mid == "M26":  # receipt LEG_ORDER swap
        e[RECEIPT] = rep(receipt,
            "LEG_ORDER bn_exists,ldag_exists,ldag_cols,ldag_struct,idag_exists,idag_cols,idag_struct,sample_cols,sample_data,reward",
            "LEG_ORDER ldag_exists,bn_exists,ldag_cols,ldag_struct,idag_exists,idag_cols,idag_struct,sample_cols,sample_data,reward")
    elif mid == "M27":  # receipt HOST_BASH edit
        e[RECEIPT] = rep(receipt,
            "HOST_BASH GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)",
            "HOST_BASH GNU bash, version 5.2.0(1)-release (x86_64-pc-linux-gnu)")
    elif mid == "M28":  # receipt SUBJECT_SHA edit
        e[RECEIPT] = rep(receipt,
            "SUBJECT_SHA 364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b",
            "SUBJECT_SHA 364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455c")
    elif mid == "M29":  # receipt DATASET_SHA edit
        e[RECEIPT] = rep(receipt,
            "DATASET_SHA 7d4c27aca2f7443500f993bf0cc31fc7c7e4ef45bb5370ba890848ee1ef3cb04",
            "DATASET_SHA 7d4c27aca2f7443500f993bf0cc31fc7c7e4ef45bb5370ba890848ee1ef3cb05")
    elif mid == "M30":  # ledger status executed -> located for the member
        e["plans/grader-population-ledger.json"] = rep(ledger,
            '"status": "executed",\n   "round": 99,',
            '"status": "located",\n   "round": 99,')
    elif mid == "M31":  # extra file at T (not in the candidate-bytes table)
        e["plans/round99_extra.txt"] = b"mutant\n"
    elif mid == "M32":  # SKILL file-artifact cell edit (candidate byte)
        e["SKILL.md"] = rep(skill,
            "executed 34 of 76 (round 99 adds",
            "executed 35 of 76 (round 99 adds")
    elif mid == "M33":  # claims candidate-bytes edit at rev
        e["plans/round-99-claims.md"] = rep(claims,
            "05116b87550f534be71736ab600791bf7f3ab8a6ba3c649de2bd941b53586d1f  corpus/SOURCES.md",
            "05116b87550f534be71736ab600791bf7f3ab8a6ba3c649de2bd941b53586d1e  corpus/SOURCES.md")
    elif mid == "M34":  # receipt mismatches line edit
        e[RECEIPT] = rep(receipt, "\nmismatches 0\n", "\nmismatches 1\n")
    elif mid == "M35":  # receipt GRADER_SIDE stamp edit
        e[RECEIPT] = rep(receipt,
            "GRADER_SIDE python,pandas,scipy,pytest 3.13 2.3.2 1.16.1 8.4.1",
            "GRADER_SIDE python,pandas,scipy,pytest 3.13 2.3.2 1.16.1 8.4.0")
    elif mid == "M37":  # weakened counter (L10 ignores flagged) + the row it should reject
        e["plans/round99_c1_replay.py"] = rep(counter,
            "l10 = bool(added) and not flagged", "l10 = bool(added)")
        row = ("\n| S342 | mutant unbound row — https://example.invalid/mutant | docs | A | mutant | "
               "sha256 0000000000000000000000000000000000000000000000000000000000000000 | mutant | "
               "queued | 2026-11-06 | on-release | — |\n")
        e["corpus/SOURCES.md"] = sources + row.encode()
    elif mid == "M38":  # frozen gate edited at rev (L10 reads BASE bytes only)
        e["plans/anchor_digest_check.py"] = rep(show(T, "plans/anchor_digest_check.py"),
            "from __future__ import annotations\n",
            "from __future__ import annotations\n# mutant comment\n")
    elif mid == "M39":  # receipt deleted
        e[RECEIPT] = None
    else:
        raise SystemExit("unknown mutant " + mid)
    return e


DESC = {
    "M01": ("receipt CASE C01 observed flipped P->F", "L5/L6"),
    "M01b": ("receipt drops case C13 (CASE+DETAIL)", "L5/L6"),
    "M02": ("receipt CASE C12 predicted+observed flipped to pass", "L5/L6"),
    "M03": ("receipt DETAIL C03 final digest edited", "L6"),
    "M04a": ("receipt LANE_TIP -> descendant 23d58036", "L3"),
    "M04b": ("receipt LANE_TIP -> ancestor BASE 2233a661", "L3"),
    "M05": ("case table C11 predicted flipped", "L4/L5"),
    "M06": ("ledger member classes += numeric-band", "L7"),
    "M07": ("ledger member round 99->98", "L7"),
    "M08": ("ledger member receipt path edited", "L7"),
    "M09": ("ledger member subject tb2-header->tb2-body", "L7"),
    "M10": ("second executed member build-pmars -> located", "L7"),
    "M11": ("other executed member loses file-artifact class", "L7/cells"),
    "M12": ("SOURCES S342 added, unbound digest", "L10"),
    "M13": ("SOURCES S342 added, correctly bound", "L10/new_rows"),
    "M14": ("SOURCES S341 removed", "L10/new_rows"),
    "M15": ("capture test_outputs.py byte appended", "L2"),
    "M16": ("fixture final_bn_sample.csv byte appended", "L2"),
    "M17": ("probe comment inserted", "L6/L8/L9"),
    "M18": ("counter comment inserted", "L11"),
    "M19": ("builder C03 draws U instead of D", "L6/L8"),
    "M20": ("builder C03 seed 3->5", "L6(DETAIL)/L8"),
    "M21": ("builder C11 shift 0.045->0.060", "L6/L8"),
    "M22": ("builder C12 shift 0.050->0.040", "L6/L8"),
    "M23": ("builder C13 quantile grid -> seeded random", "L6(DETAIL)/L8"),
    "M24": ("builder comment only", "L6/L8"),
    "M25": ("probe mismatch check disabled (ok=True)", "L6/L8"),
    "M26": ("receipt LEG_ORDER first two legs swapped", "none"),
    "M27": ("receipt HOST_BASH edited", "L9"),
    "M28": ("receipt SUBJECT_SHA edited", "L2"),
    "M29": ("receipt DATASET_SHA edited", "L2"),
    "M30": ("ledger member status executed->located", "L7"),
    "M31": ("extra file plans/round99_extra.txt added", "none"),
    "M32": ("SKILL file-artifact cell 34->35", "none"),
    "M33": ("claims candidate-bytes SOURCES sha edited", "none"),
    "M34": ("receipt mismatches 0->1", "none"),
    "M35": ("receipt GRADER_SIDE stamp 8.4.1->8.4.0", "L6"),
    "M37": ("weakened counter L10 + unbound SOURCES row (pair)", "L11"),
    "M38": ("frozen gate anchor_digest_check.py edited at rev", "none"),
    "M39": ("receipt file deleted", "L1"),
}
PROBE_DIRECT = {"M19", "M20", "M21", "M22", "M23", "M24", "M25"}


def mkcommit(mid, edits):
    parent = T
    idx = S / "idx" / mid
    idx.parent.mkdir(parents=True, exist_ok=True)
    if idx.exists():
        idx.unlink()
    env = dict(ENV)
    env.update({
        "GIT_INDEX_FILE": str(idx),
        "GIT_AUTHOR_NAME": "MutC1", "GIT_COMMITTER_NAME": "MutC1",
        "GIT_AUTHOR_EMAIL": "mutc1@example.invalid", "GIT_COMMITTER_EMAIL": "mutc1@example.invalid",
        "GIT_AUTHOR_DATE": "2026-11-06T12:00:00 -0300", "GIT_COMMITTER_DATE": "2026-11-06T12:00:00 -0300",
    })
    p = git("read-tree", parent, env=env)
    assert p.returncode == 0, p.stderr
    record = {"mutant": mid, "parent": parent, "paths": {}}
    for path, data in sorted(edits.items()):
        before = show(T, path) if git("cat-file", "-e", f"{T}:{path}").returncode == 0 else None
        if data is None:
            p = git("update-index", "--force-remove", path, env=env)
            assert p.returncode == 0, p.stderr
            record["paths"][path] = {"before": sha(before) if before is not None else "absent", "after": "absent"}
        else:
            b = git("hash-object", "-w", "--stdin", input=data, env=env)
            assert b.returncode == 0, b.stderr
            blob = b.stdout.decode().strip()
            p = git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
            assert p.returncode == 0, p.stderr
            record["paths"][path] = {"before": sha(before) if before is not None else "absent",
                                     "after": sha(data), "blob": blob}
    tree = git("write-tree", env=env)
    assert tree.returncode == 0, tree.stderr
    tree_sha = tree.stdout.decode().strip()
    c = git("commit-tree", tree_sha, "-p", parent, env=env, input=f"mutant {mid}\n".encode())
    assert c.returncode == 0, c.stderr
    commit = c.stdout.decode().strip()
    r = git("update-ref", f"refs/heads/mut-{mid}", commit)
    assert r.returncode == 0, r.stderr
    record["commit"] = commit
    record["tree"] = tree_sha
    return record


def run_counter(mid, rev):
    work = S / "work" / mid
    shutil.rmtree(work, ignore_errors=True)
    t0 = time.time()
    p = subprocess.run([sys.executable, "plans/round99_c1_replay.py", "--lane", ".", "--rev", rev,
                        "--work", str(work), "--grader-venv", str(G)],
                       cwd=str(CLONE), capture_output=True, text=True, timeout=1800, env=ENV)
    dt = time.time() - t0
    out = p.stdout
    err = p.stderr
    res = S / "results"
    res.mkdir(exist_ok=True)
    (res / f"{mid}.out").write_text(out)
    (res / f"{mid}.err").write_text(err)
    (res / f"{mid}.rc").write_text(str(p.returncode))
    legs = next((ln for ln in out.splitlines() if ln.startswith("LEGS ")), "")
    pred = next((ln for ln in out.splitlines() if ln.startswith("PREDICATE ")), "")
    targ = next((ln for ln in out.splitlines() if ln.startswith("TARGET ")), "")
    setup = next((ln for ln in out.splitlines() if ln.startswith("DEFECT SETUP ")), "")
    return {"mutant": mid, "rc": p.returncode, "legs": legs, "predicate": pred, "target": targ,
            "setup": setup, "seconds": round(dt, 1)}


def run_probe_direct(mid, rev):
    ex = S / "probe" / mid
    shutil.rmtree(ex, ignore_errors=True)
    ex.mkdir(parents=True)
    arc = git("archive", rev)
    assert arc.returncode == 0, arc.stderr
    with tarfile.open(fileobj=__import__("io").BytesIO(arc.stdout)) as tar:
        tar.extractall(ex, filter="data")
    work = S / "probework" / mid
    shutil.rmtree(work, ignore_errors=True)
    p = subprocess.run([sys.executable, "-I", "-B", str(ex / "plans/round99_bnfit_probe.py"),
                        "--lane", str(ex), "--work", str(work), "--grader-venv", str(G)],
                       capture_output=True, text=True, timeout=1800, env=ENV)
    out = p.stdout
    res = S / "results"
    res.mkdir(exist_ok=True)
    (res / f"{mid}.probe.out").write_text(out)
    (res / f"{mid}.probe.rc").write_text(str(p.returncode))
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(ex, ignore_errors=True)
    return {"mutant": mid, "probe_rc": p.returncode, "probe_out": out}


def obs_block(text):
    inside = False
    lines = []
    for ln in text.splitlines():
        if ln == "OBSERVATIONS_BEGIN":
            inside = True
            continue
        if ln == "OBSERVATIONS_END":
            break
        if inside:
            lines.append(ln)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    ids = [x for x in a.only.split(",") if x] or list(DESC)
    top = git("rev-parse", "--show-toplevel").stdout.decode().strip()
    assert top == str(CLONE), (top, str(CLONE))
    assert git("rev-parse", "HEAD").stdout.decode().strip() == T
    records = {}
    for mid in ids:
        e = edits_for(mid)
        records[mid] = mkcommit(mid, e)
        print(f"built {mid} {records[mid]['commit'][:12]} paths={list(e)}", flush=True)
    manifest = S / "manifest.json"
    old = json.loads(manifest.read_text()) if manifest.exists() else {}
    old.update(records)
    manifest.write_text(json.dumps(old, indent=1, sort_keys=True))
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(run_counter, mid, records[mid]["commit"]): mid for mid in ids}
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            results[r["mutant"]] = r
            print(f"done {r['mutant']} rc={r['rc']} {r['legs']} {r['predicate']} {r['seconds']}s", flush=True)
    probe_res = {}
    pids = [m for m in ids if m in PROBE_DIRECT]
    if pids:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(3, len(pids))) as pool:
            futs = {pool.submit(run_probe_direct, mid, records[mid]["commit"]): mid for mid in pids}
            for f in concurrent.futures.as_completed(futs):
                r = f.result()
                probe_res[r["mutant"]] = r
                print(f"probe {r['mutant']} rc={r['probe_rc']}", flush=True)
    summary = S / "summary.json"
    base = json.loads(summary.read_text()) if summary.exists() else {}
    for mid, r in results.items():
        r["desc"], r["expected"] = DESC[mid]
        r["commit"] = records[mid]["commit"]
        r["paths"] = records[mid]["paths"]
        if mid in probe_res:
            r["probe_rc"] = probe_res[mid]["probe_rc"]
            r["probe_obs"] = obs_block(probe_res[mid]["probe_out"])
        base[mid] = r
    summary.write_text(json.dumps(base, indent=1, sort_keys=True))
    print("SUMMARY", json.dumps({m: {"rc": r["rc"], "legs": r["legs"].replace("LEGS ", ""),
                                      "pred": r["predicate"]} for m, r in sorted(results.items())}, indent=0))


if __name__ == "__main__":
    main()
