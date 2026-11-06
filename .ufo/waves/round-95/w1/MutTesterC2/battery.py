#!/usr/bin/env python3
"""MutTesterC2 battery — single-site mutants of plans/round95_c2_counter.py and
plans/round95_false_gate_census.py at T afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239,
each scored by the census (or the mutated census) exactly as the frozen predicate runs it.
Everything under /fast/scratch/hyaku/kengaku-r95/MutTesterC2; the lane is only read."""
import hashlib
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r95/MutTesterC2")
LANE = S / "lane"
T = "afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239"
P1 = "16dcfed7ef4c9e2ac7d28568d855905a8457b20d"
COUNTER = S / "pristine-counter.py"
CENSUS = S / "pristine-census.py"
MUT = S / "mut"
REC = S / "receipts"
WORK = S / "work"
CTRL = S / "controls"
R94C = CTRL / "round94_c2_counter.py"     # round-94 counter bytes (do-nothing control)
P1C = CTRL / "counter-under-test.py"      # round-95 counter bytes at P1 (== T bytes)
PY = sys.executable

def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---------------- counter mutants: (id, anchor, replacement) ----------------
COUNTER_MUTANTS = [
    ("CM01-w5-target-ignored",
     "        w5 = w5 and hit\n",
     "        w5 = w5 and True\n"),
    ("CM02-w1-leg-dropped",
     "    legs[\"W1\"] = w1a and w1b\n",
     "    legs[\"W1\"] = True\n"),
    ("CM03-w4-leg-dropped",
     "        legs[\"W4\"] = rc == 0 and s is not None and s[0] >= MIN_SELF_INSTRUMENTS and s[2] == 0 and pred_ok(rc, out)\n",
     "        legs[\"W4\"] = True\n"),
    ("CM04-w3-ok-le-15",
     "        red_line = len(st) == 1 and st[0][0] == \"15\" and int(st[0][1]) < 15\n",
     "        red_line = len(st) == 1 and st[0][0] == \"15\" and int(st[0][1]) <= 15\n"),
    ("CM05-predok-multiplicity",
     "    return len(lines) == 1 and PRED_FOR_RC.get(rc) == lines[0]\n",
     "    return len(lines) >= 1 and PRED_FOR_RC.get(rc) == lines[0]\n"),
    ("CM06-drop-w2-unrelated",
     "    (\"w2-unrelated\", CLAIMS_ARGS, 0, (1, 1, 0)),\n",
     ""),
    ("CM07-cne-summary-ignored",
     "            ok = rc == 2 and s is None\n",
     "            ok = rc == 2\n"),
    ("CM08-predok-always-true",
     "    return len(lines) == 1 and PRED_FOR_RC.get(rc) == lines[0]\n",
     "    return True\n"),
    ("CM09-w2-always-ok",
     "        results[name] = (ok, f\"rc={rc} want_rc={want_rc} summary={s} want={want_s} predicate_line_ok={p_ok}\")",
     "        results[name] = (True, f\"rc={rc} want_rc={want_rc} summary={s} want={want_s} predicate_line_ok={p_ok}\")"),
    ("CM10-w2-edited-want-rc0",
     "    (\"w2-edited\", CLAIMS_ARGS, 1, (1, 0, 1)),\n",
     "    (\"w2-edited\", CLAIMS_ARGS, 0, (1, 0, 1)),\n"),
    ("CM11-minself-8-to-99",
     "MIN_SELF_INSTRUMENTS = 8",
     "MIN_SELF_INSTRUMENTS = 99"),
    ("CM12-w2-intact-want-rc1",
     "    (\"w2-intact\", CLAIMS_ARGS, 0, (1, 1, 0)),\n",
     "    (\"w2-intact\", CLAIMS_ARGS, 1, (1, 1, 0)),\n"),
    ("CM13-w3-rc-dropped",
     "        ok = red_line and rc == 1 and PRED_LINE.findall(out) == [\"fail\"]\n",
     "        ok = red_line and PRED_LINE.findall(out) == [\"fail\"]\n"),
    ("CM14-w3-pred-any",
     "        ok = red_line and rc == 1 and PRED_LINE.findall(out) == [\"fail\"]\n",
     "        ok = red_line and rc == 1 and len(PRED_LINE.findall(out)) >= 1\n"),
    ("CM15-w3-pred-dropped",
     "        ok = red_line and rc == 1 and PRED_LINE.findall(out) == [\"fail\"]\n",
     "        ok = red_line and rc == 1\n"),
    ("CM16-fx-refresh-dropped",
     "    if d.exists():\n        shutil.rmtree(d)",
     "    if False:\n        shutil.rmtree(d)"),
    ("CM17-w1b-intact-only",
     "    w1b = rc_b == 0 and s_b == (9, 9, 0) and pred_ok(rc_b, out_b)\n",
     "    w1b = rc_b == 0 and s_b[1] == 9 and pred_ok(rc_b, out_b)\n"),
    ("CM18-w2-summary-optional",
     "            ok = rc == want_rc and s == want_s\n",
     "            ok = rc == want_rc and (s is None or s == want_s)\n"),
    ("CM19-w4-broken-ignored",
     "s[2] == 0 and pred_ok(rc, out)",
     "True and pred_ok(rc, out)"),
    ("CM20-drop-w2-second-block",
     "    (\"w2-second-block\", CLAIMS_ARGS, 2, None),\n",
     ""),
]

# ---------------- census mutants: (id, anchor, replacement, extra_run) ----------------
CENSUS_MUTANTS = [
    ("XM1-designated-forced",
     "        dred = int(designated_red(DESIGNATED[gid], out))\n",
     "        dred = 1\n",
     "donothing"),   # extra run: do-nothing reproduction at P1 with the r94 counter
    ("XM2-passes-polarity",
     "        passes = int(rc == 0 and PASS_LINE.search(out) is not None)\n",
     "        passes = int(rc != 0 or PASS_LINE.search(out) is not None)\n",
     None),
    ("XM3-honest-dropped",
     "    ok = passing == 0 and red == TOTAL and honest == \"pass\"\n",
     "    ok = passing == 0 and red == TOTAL\n",
     "atP1"),        # extra run: census at P1 with the P1 counter
    ("XM4-sha-dropped",
     "        if data.returncode != 0 or hashlib.sha256(data.stdout).hexdigest() != want or gid not in DESIGNATED:\n",
     "        if data.returncode != 0 or False or gid not in DESIGNATED:\n",
     None),
    ("XM5-total-weakened",
     "    if len(rows) != TOTAL or {g for g, _, _ in rows} != set(DESIGNATED):\n",
     "    if len(rows) > TOTAL or {g for g, _, _ in rows} != set(DESIGNATED):\n",
     None),
    ("XM6-echo-dropped",
     "        if re.match(r\"^(TOOL|W[1-5] (pass|fail)|TARGET)\", line):\n",
     "        if re.match(r\"^ZZZNOMATCH\", line):\n",
     None),
    ("XM7-passline-any",
     "PASS_LINE = re.compile(r\"^PREDICATE R\\d+-C2 pass$\", re.M)",
     "PASS_LINE = re.compile(r\"^PREDICATE R\\d+-C2\", re.M)",
     None),
]

R94_SHA = "17d2a7d52fbd703db1c4df661168f22a36481f289962ea66d5e98a0466190b98"
P1C_SHA = "2fc2e7f0a1c26599c60f2f142c7d73a581974cb6949b65a90e9e3cbf08a13a7c"


def setup_controls() -> None:
    for p in (MUT, REC, WORK, CTRL):
        p.mkdir(parents=True, exist_ok=True)
    b = subprocess.run(["git", "-C", str(LANE), "show", f"{P1}:plans/round94_c2_counter.py"],
                       capture_output=True, timeout=120)
    assert b.returncode == 0, b.stderr
    R94C.write_bytes(b.stdout)
    assert sha(R94C) == R94_SHA, f"r94 counter sha {sha(R94C)}"
    shutil.copyfile(S / "controls" / "r95-counter-at-P1.py", P1C)
    assert sha(P1C) == P1C_SHA, f"P1 counter sha {sha(P1C)}"
    (CTRL / "r94-counter-at-BASE.py").unlink(missing_ok=True)  # wrong file from first extraction (was the gate)


def generate() -> None:
    manifest = {"counter_pristine_sha256": sha(COUNTER), "census_pristine_sha256": sha(CENSUS),
                "mutants": []}
    sc, sx = COUNTER.read_text(), CENSUS.read_text()
    for mid, anchor, repl in COUNTER_MUTANTS:
        n = sc.count(anchor)
        assert n == 1, f"{mid}: counter anchor count {n}"
        p = MUT / f"{mid}.py"
        p.write_text(sc.replace(anchor, repl))
        manifest["mutants"].append({"id": mid, "target": "counter", "anchor": anchor,
                                    "replacement": repl, "sha256": sha(p)})
    for mid, anchor, repl, extra in CENSUS_MUTANTS:
        n = sx.count(anchor)
        assert n == 1, f"{mid}: census anchor count {n}"
        p = MUT / f"{mid}.py"
        p.write_text(sx.replace(anchor, repl))
        manifest["mutants"].append({"id": mid, "target": "census", "anchor": anchor,
                                    "replacement": repl, "extra": extra, "sha256": sha(p)})
    (S / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"generated {len(manifest['mutants'])} mutants")


def census_cmd(script: Path, rev: str, work: Path, counter: Path | None) -> list[str]:
    a = [PY, "-I", "-B", str(script), "--lane", str(LANE), "--rev", rev, "--work", str(work)]
    if counter:
        a += ["--counter", str(counter)]
    return a


def build_jobs() -> list[tuple[str, list[str]]]:
    jobs: list[tuple[str, list[str]]] = []
    jobs.append(("B0-T", census_cmd(CENSUS, T, WORK / "B0-T", None)))
    for mid, _, _ in COUNTER_MUTANTS:
        jobs.append((mid, census_cmd(CENSUS, T, WORK / mid, MUT / f"{mid}.py")))
    for mid, _, _, extra in CENSUS_MUTANTS:
        rev, counter = T, None
        if extra == "donothing":
            rev, counter = P1, R94C
        elif extra == "atP1":
            rev, counter = P1, P1C
        jobs.append((mid, census_cmd(MUT / f"{mid}.py", rev, WORK / mid, counter)))
        if extra == "donothing":
            jobs.append((mid + "-DN", census_cmd(MUT / f"{mid}.py", P1, WORK / (mid + "-DN"), R94C)))
        elif extra == "atP1":
            jobs.append((mid + "-P1", census_cmd(MUT / f"{mid}.py", P1, WORK / (mid + "-P1"), P1C)))
    jobs.append(("XM1DN-pristine-BASECTRL", census_cmd(CENSUS, P1, WORK / "XM1DN-pristine-BASECTRL", R94C)))
    jobs.append(("XM3P1-pristine-BASECTRL", census_cmd(CENSUS, P1, WORK / "XM3P1-pristine-BASECTRL", P1C)))
    jobs.append(("B0-END", census_cmd(CENSUS, T, WORK / "B0-END", None)))
    return jobs


def run_job(job) -> tuple[str, int, float]:
    jid, argv = job
    t0 = time.time()
    p = subprocess.run(argv, cwd=str(LANE), capture_output=True, text=True, timeout=3600)
    dt = time.time() - t0
    (REC / f"{jid}.out").write_text(p.stdout)
    (REC / f"{jid}.txt").write_text(
        f"# id {jid}\n# argv {argv}\n# cwd {LANE}\n{p.stdout}# stderr:\n{p.stderr}rc={p.returncode} seconds={dt:.1f}\n")
    print(f"DONE {jid} rc={p.returncode} {dt:.0f}s", flush=True)
    return jid, p.returncode, dt


PRED = "PREDICATE R95-C2 pass"


def body_lines(jid: str) -> list[str]:
    return [ln for ln in (REC / f"{jid}.out").read_text().splitlines() if not ln.startswith("COUNTER ")]


def main() -> int:
    setup_controls()
    generate()
    t0 = time.time()
    run_job(("B0-T", census_cmd(CENSUS, T, WORK / "B0-T", None)))
    print(f"baseline B0-T done at {time.time()-t0:.0f}s", flush=True)
    jobs = [j for j in build_jobs() if j[0] != "B0-T"]
    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(run_job, jobs))
    base = body_lines("B0-T")
    verdicts = []
    for jid, argv in build_jobs():
        out = (REC / f"{jid}.out").read_text()
        rc = 0
        m = [ln for ln in (REC / f"{jid}.txt").read_text().splitlines() if ln.startswith("rc=")]
        rc = int(m[-1].split()[0][3:]) if m else -1
        pred = "pass" if "PREDICATE R95-C2 pass" in out.splitlines()[-2:] else \
               ("fail" if "PREDICATE R95-C2 fail" in out.splitlines()[-2:] else "none")
        diffs = [f"-{b}\n+{a}" for a, b in zip(body_lines(jid), base) if a != b] if jid != "B0-T" else []
        extra = len(body_lines(jid)) - len(base)
        verdicts.append({"id": jid, "rc": rc, "predicate_tail": pred,
                         "delta_lines": len(diffs), "len_delta": extra,
                         "sample_diffs": diffs[:6]})
    (S / "verdicts.json").write_text(json.dumps(verdicts, indent=1))
    meta = {"t_seconds": time.time() - t0,
            "counter_sha_before": sha(COUNTER), "counter_sha_after": sha(COUNTER),
            "census_sha_before": sha(CENSUS), "census_sha_after": sha(CENSUS)}
    st = subprocess.run(["git", "-C", str(LANE), "status", "--porcelain"], capture_output=True, text=True)
    hd = subprocess.run(["git", "-C", str(LANE), "rev-parse", "HEAD"], capture_output=True, text=True)
    meta["lane_porcelain"] = st.stdout
    meta["lane_head_after"] = hd.stdout.strip()
    (S / "meta.json").write_text(json.dumps(meta, indent=1))
    for v in verdicts:
        print(f"V {v['id']} rc={v['rc']} pred={v['predicate_tail']} delta={v['delta_lines']} lenΔ={v['len_delta']}")
    print(f"battery wall {meta['t_seconds']:.0f}s; lane clean={not meta['lane_porcelain']} head={meta['lane_head_after'][:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
