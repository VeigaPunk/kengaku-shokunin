#!/usr/bin/env python3
"""Round-12 powered emission-granularity LADDER + transport — runner.

Lineage: run_r11.py (← run_r9.py). Same scaffolding: the probe module is
imported by path, `call` is wrapped to stamp `request_ts`, `log` is wrapped to
attach the last request's timestamp, one filler request precedes every cell,
descriptors pin the serving stack in-band, and the SUMMARY is recomputed by
re-reading the run's own JSONL.

Deviations from run_r11.py (exhaustive; probe_plan_r12.md §7):
  1. five family-1 arms (A-INC, A-CKPT4710, A-CKPT710, A-CKPT10, A-MONO)
     instead of two; arm order rotated by pid index (a rotation Latin square)
     instead of pid parity;
  2. A-INC uses the r8 `run_inc(proto='INC')` ask wording ("Output the FULL
     state after applying it." on every turn) — `ladder(..., dense=True)`;
     the CHECKPOINT wording is reserved for proper-subset checkpoint sets, so
     the three CKPT arms stay verbatim r11;
  3. a second task family (T-DENSE / T-SPARSE, positional token-sequence
     editing) with its own pids/seeds, interleaved with family 1 pid-by-pid so
     a slow host drift cannot align with a family;
  4. a `descriptors_end` record re-reads /v1/models + the server argv at the
     end of the run (mid-run drift detection, probe_plan_r12.md §8);
  5. the descriptors record also pins the sha256 of this file, of the prereg
     bundle and of predict_r12.py, and the realized arm-position counts;
  6. SUMMARY lists 7 cells.

Environment: KENGAKU_R12_OUT (default /tmp/kengaku-r12), KENGAKU_R12_N
(family-1 problems, default 64), KENGAKU_R12_N2 (family-2 problems, default
48), KENGAKU_R12_BASE (probe endpoint; the mock smoke redirects everything
through http_proxy instead — see round12-fleet/r12-mock-smoke.md).
"""
import importlib.util
import json
import hashlib
import os
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("KENGAKU_R12_OUT", "/tmp/kengaku-r12")
N = int(os.environ.get("KENGAKU_R12_N", "64"))
N2 = int(os.environ.get("KENGAKU_R12_N2", "48"))
PIDS = list(range(201, 201 + N))
PIDS2 = list(range(401, 401 + N2))
HOST = "http://127.0.0.1:34113"
RESULTS = "results-r12.jsonl"

ARMS = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO"]
CKPTS = {"A-INC": set(range(1, 11)), "A-CKPT4710": {4, 7, 10},
         "A-CKPT710": {7, 10}, "A-CKPT10": {10}}
T_CKPTS = {"T-DENSE": {4, 7, 10}, "T-SPARSE": {7, 10}}
SEED1 = "3000+pid*41"
SEED2 = "5000+pid*37"

os.makedirs(OUT, exist_ok=True)
_spec = importlib.util.spec_from_file_location("probe", os.path.join(HERE, "probe_r12.py"))
p = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p)
p.OUT = OUT
p.LOGF = open(os.path.join(OUT, RESULTS), "a")

last_req = None


def call(msgs):
    global last_req
    last_req = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return p.call_orig(msgs)


def log(rec):
    if last_req and "request_ts" not in rec:
        rec = dict(rec); rec["request_ts"] = last_req
    p.LOGF.write(json.dumps(rec, separators=(",", ":")) + "\n")
    p.LOGF.flush()


p.call_orig = p.call
p.call = call
p.log = log


def ladder(pid, init, ops, checkpoints, name, fam=1, dense=False):
    """Verbatim run_r11.py `ladder()` for family 1 (and for family 2 with the
    family-2 rules/op-renderer/simulator/grader swapped in). `dense=True`
    selects the r8 `run_inc(proto='INC')` ask wording, which is the wording
    A-INC was measured under in round 8 — using the CHECKPOINT wording there
    would change the arm, not just its label."""
    if fam == 2:
        RULES, op_str, states_along, grade = p.RULES2, p.op_str2, p.states_along2, p.grade_seq
    else:
        RULES, op_str, states_along, grade = p.RULES, p.op_str, p.states_along, p.grade_state
    full_ask = "Output the FULL state after applying it."
    msgs = [{"role": "user", "content":
             RULES + f"\nInitial state: {json.dumps(init)}\nNext operation: {op_str(ops[0])}\n{full_ask}"}]
    truth = states_along(init, ops)
    for i, op in enumerate(ops):
        r = p.call(msgs)
        msgs.append({"role": "assistant", "content": r["content"]})
        turn = i + 1
        if turn in checkpoints:
            got = p.extract_json_block(r["content"])
            exact, nwrong = grade(got, truth[i])
            p.log({"cell": name, "pid": pid, "turn": turn, "ok": exact, "nwrong": nwrong,
                   "got": got, "want": truth[i], "finish": r["finish_reason"],
                   "usage": r["usage"], "wall_s": r["wall_s"], "raw": r["content"]})
        else:
            p.log({"cell": name + "-ack", "pid": pid, "turn": turn, "raw": r["content"][:80],
                   "finish": r["finish_reason"], "usage": r["usage"], "wall_s": r["wall_s"]})
        if i + 1 < len(ops):
            if dense:
                ask = full_ask
            else:
                ask = full_ask if turn in checkpoints else "Reply 'ok'."
                if (i + 2) in checkpoints:
                    ask = "CHECKPOINT — output the FULL state now."
            msgs.append({"role": "user", "content": f"Next operation: {op_str(ops[i+1])}\n{ask}"})


def filler():
    r = p.call([{"role": "user", "content": "Reply with the single word: ready."}])
    p.log({"cell": "filler", "finish": r["finish_reason"], "usage": r["usage"],
           "wall_s": r["wall_s"], "raw": r["content"]})


def _sha(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        return f"unreadable: {e!r}"


def _server_pin():
    """Best-effort llama-server pid + argv. Failure is recorded, never fatal."""
    try:
        out = subprocess.run(["pgrep", "-f", "llama-server"], capture_output=True,
                             text=True, timeout=5).stdout.split()
        pid = int(out[0]) if out else None
        if pid is None:
            return {"pid": None}
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            argv = [a for a in f.read().decode("utf-8", "replace").split("\0") if a]
        return {"pid": pid, "argv": argv}
    except Exception as e:
        return {"error": repr(e)}


def _models():
    try:
        with urllib.request.urlopen(HOST + "/v1/models", timeout=10) as r:
            return json.load(r)
    except Exception as e:
        return {"error": repr(e)}


def _arm_orders():
    orders = {}
    for k, pid in enumerate(PIDS):
        rot = k % len(ARMS)
        orders[pid] = ARMS[rot:] + ARMS[:rot]
    return orders


def descriptors(jobs):
    """Experimental-unit descriptors, captured at run time (probe_plan_r12.md §3)."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    orders = _arm_orders()
    pos = {a: [0] * len(ARMS) for a in ARMS}
    for pid, order in orders.items():
        for i, a in enumerate(order):
            pos[a][i] += 1
    p.log({"cell": "descriptors", "request_ts": ts, "endpoint": HOST,
           "models_json": _models(), "server": _server_pin(),
           "temp": p.TEMP, "maxtok": p.MAXTOK, "system_prompt": p.SYSTEM,
           "families": {"1": "inventory ledger (dict state, integer arithmetic)",
                        "2": "positional token-sequence editing (list state)"},
           "seed_scheme": SEED1, "seed_scheme_f2": SEED2,
           "pids": PIDS, "pids_f2": PIDS2, "n": N, "n2": N2,
           "arms": ARMS, "arm_checkpoints": {k: sorted(v) for k, v in CKPTS.items()},
           "t_checkpoints": {k: sorted(v) for k, v in T_CKPTS.items()},
           "arm_order_rule": "rotation Latin square: ARMS[k%5:] + ARMS[:k%5], k = pid-201",
           "arm_order_counts": pos,
           "counterbalance": "family 2: even pid -> T-DENSE first, odd pid -> T-SPARSE first",
           "schedule": "families interleaved pid-block-by-pid-block (family1 block k, then family2 block k)",
           "n_jobs": len(jobs),
           "machinery_sha256": _sha(os.path.join(HERE, "probe_r12.py")),
           "runner_sha256": _sha(os.path.join(HERE, "run_r12.py")),
           "predictor_sha256": _sha(os.path.join(HERE, "predict_r12.py")),
           "prereg_bundle_sha256": _sha(os.path.join(HERE, "prereg-bundle.sha256")),
           "probe_lineage": ("probe_r12.py family-1 machinery = round11-power/probe_r11.py "
                             "byte-identical except docstring + 3 env constants; family-2 "
                             "section new in round 12")})


def descriptors_end(t0):
    p.log({"cell": "descriptors_end",
           "request_ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "endpoint": HOST, "models_json": _models(), "server": _server_pin(),
           "wall_total_s": round(time.time() - t0, 1),
           "n_records": sum(1 for _ in open(os.path.join(OUT, RESULTS)))})


def main():
    jobs = []
    for k in range(max(len(PIDS), len(PIDS2))):
        if k < len(PIDS):
            jobs += [(c, 1, PIDS[k]) for c in _arm_orders()[PIDS[k]]]
        if k < len(PIDS2):
            pid = PIDS2[k]
            order = ["T-DENSE", "T-SPARSE"] if pid % 2 == 0 else ["T-SPARSE", "T-DENSE"]
            jobs += [(c, 2, pid) for c in order]
    descriptors(jobs)
    for pid in PIDS:
        seed = 3000 + pid * 41
        init, ops = p.gen_problem(seed)
        p.log({"cell": "meta", "pid": pid, "seed": seed, "init": init,
               "ops": [list(x) for x in ops], "truth": p.states_along(init, ops),
               "tail_touched": sorted(p.tail_touched(ops))})
    for pid in PIDS2:
        seed = 5000 + pid * 37
        init, ops = p.gen_seq_problem(seed)
        p.log({"cell": "meta2", "pid": pid, "seed": seed, "init": init,
               "ops": [list(x) for x in ops], "truth": p.states_along2(init, ops),
               "features": {"n_ops": len(ops), "init_len": len(init),
                            "final_len": len(p.states_along2(init, ops)[-1]),
                            "kinds": sorted({o[0] for o in ops}),
                            "tail_positions": sorted(p.tail_positions(ops))}})
    t0 = time.time()
    for i, (cellname, fam, pid) in enumerate(jobs):
        try:
            filler()
            if fam == 1:
                init, ops = p.gen_problem(3000 + pid * 41)
                if cellname == "A-MONO":
                    p.run_mono(pid, init, ops)
                else:
                    ladder(pid, init, ops, CKPTS[cellname], cellname,
                           fam=1, dense=(cellname == "A-INC"))
            else:
                init, ops = p.gen_seq_problem(5000 + pid * 37)
                ladder(pid, init, ops, T_CKPTS[cellname], cellname, fam=2)
        except Exception as e:
            p.log({"cell": "error", "job": [cellname, fam, pid], "err": repr(e)})
        print(f"[{i+1}/{len(jobs)}] ({cellname!r}, {pid})", flush=True)
    print("\n=== SUMMARY ===", flush=True)
    recs = [json.loads(l) for l in open(os.path.join(OUT, RESULTS))]
    for cellname in ARMS + ["T-DENSE", "T-SPARSE"]:
        fturn = 1 if cellname == "A-MONO" else 10
        fin = [r for r in recs if r.get("cell") == cellname and r.get("turn") == fturn and "ok" in r]
        print(f"{cellname}: {sum(1 for r in fin if r['ok'])}/{len(fin)}", flush=True)
    print(f"wall_total_s: {time.time() - t0:.1f}", flush=True)
    descriptors_end(t0)


if __name__ == "__main__":
    main()
