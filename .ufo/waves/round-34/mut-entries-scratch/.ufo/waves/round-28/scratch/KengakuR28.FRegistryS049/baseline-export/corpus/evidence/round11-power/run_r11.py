#!/usr/bin/env python3
"""Round-11 powered emission-granularity rerun — runner (lineage: run_r9.py).

Cells: A-CKPT4710 (checkpoints {4,7,10}) vs A-CKPT710 (checkpoints {7,10}) on
the SAME n problems (default 64, pids 201..200+n, seed 3000+pid*41), paired
per pid, cell order counterbalanced by pid parity (even pid: 4710 first; odd
pid: 710 first), one filler call before each cell's first request. Ladder
turn semantics — including the post-checkpoint FULL-state ask that r9 logged
as an `-ack` record — are copied verbatim from run_r9.py so the construct is
identical; the only deviation is documented in probe_plan_r11.md §Deviations.

First endpoint request of the process is the /v1/models fetch inside the
`descriptors` record; ordering.log proves the preregistration bundle was
hashed before it. Stdlib only.

Env: KENGAKU_R11_OUT (default /tmp/kengaku-r11), KENGAKU_R11_N (default 64),
     KENGAKU_R11_BASE forwarded to probe_r11.py (mock-server smoke runs).
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
OUT = os.environ.get("KENGAKU_R11_OUT", "/tmp/kengaku-r11")
N = int(os.environ.get("KENGAKU_R11_N", "64"))
PIDS = list(range(201, 201 + N))
HOST = "http://127.0.0.1:34113"

os.makedirs(OUT, exist_ok=True)
_spec = importlib.util.spec_from_file_location("probe", os.path.join(HERE, "probe_r11.py"))
p = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p)
p.OUT = OUT
p.LOGF = open(os.path.join(OUT, "results-r11.jsonl"), "a")

last_req = None

def call(msgs):
    global last_req
    last_req = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return p.call_orig(msgs)

def log(rec):
    if last_req and "request_ts" not in rec:
        rec = dict(rec)
        rec["request_ts"] = last_req
    p.LOGF.write(json.dumps(rec, separators=(",", ":")) + "\n")
    p.LOGF.flush()

p.call_orig = p.call
p.call = call
p.log = log

def ladder(pid, init, ops, checkpoints, name):
    """Verbatim run_r9.py ladder semantics minus the dead A-INC clause."""
    msgs = [{"role": "user", "content": p.RULES + f"\nInitial state: {json.dumps(init)}\nNext operation: {p.op_str(ops[0])}\nOutput the FULL state after applying it."}]
    truth = p.states_along(init, ops)
    for i, op in enumerate(ops):
        r = p.call(msgs)
        msgs.append({"role": "assistant", "content": r["content"]})
        turn = i + 1
        if turn in checkpoints:
            got = p.extract_json_block(r["content"])
            exact, nwrong = p.grade_state(got, truth[i])
            p.log({"cell": name, "pid": pid, "turn": turn, "ok": exact, "nwrong": nwrong,
                   "got": got, "want": truth[i], "finish": r["finish_reason"],
                   "usage": r["usage"], "wall_s": r["wall_s"], "raw": r["content"]})
        else:
            p.log({"cell": name + "-ack", "pid": pid, "turn": turn, "raw": r["content"][:80],
                   "finish": r["finish_reason"], "usage": r["usage"], "wall_s": r["wall_s"]})
        if i + 1 < len(ops):
            ask = "Output the FULL state after applying it." if turn in checkpoints else "Reply 'ok'."
            if (i + 2) in checkpoints:
                ask = "CHECKPOINT — output the FULL state now."
            msgs.append({"role": "user", "content": f"Next operation: {p.op_str(ops[i+1])}\n{ask}"})

def filler():
    r = p.call([{"role": "user", "content": "Reply with the single word: ready."}])
    p.log({"cell": "filler", "finish": r["finish_reason"], "usage": r["usage"],
           "wall_s": r["wall_s"], "raw": r["content"]})

def descriptors():
    """Experimental-unit descriptors (§Planned(b)): serving-stack pin captured
    at run time. Best-effort /proc read; failure is recorded, never fatal —
    the gate is hermetic and grades only what landed here."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    models = None
    try:
        with urllib.request.urlopen(HOST + "/v1/models", timeout=10) as r:
            models = json.load(r)
    except Exception as e:
        models = {"error": repr(e)}
    srv = None
    try:
        out = subprocess.run(["pgrep", "-f", "llama-server"], capture_output=True,
                             text=True, timeout=5).stdout.split()
        pid = int(out[0]) if out else None
        if pid is not None:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                argv = [a for a in f.read().decode("utf-8", "replace").split("\0") if a]
            srv = {"pid": pid, "argv": argv}
        else:
            srv = {"pid": None}
    except Exception as e:
        srv = {"error": repr(e)}
    p.log({"cell": "descriptors", "request_ts": ts, "endpoint": HOST,
           "models_json": models, "server": srv, "temp": p.TEMP, "maxtok": p.MAXTOK,
           "system_prompt": p.SYSTEM, "seed_scheme": "3000+pid*41", "pids": PIDS,
           "n": N, "counterbalance": "even pid: 4710 first; odd pid: 710 first",
           "machinery_sha256": hashlib.sha256(
               open(os.path.join(HERE, "probe_r11.py"), "rb").read()).hexdigest(),
           "probe_lineage": "probe_r11.py = round9-replication/replicate.py (BASE/OUT env-overridable)"})

def main():
    descriptors()
    probs = {}
    for pid in PIDS:
        init, ops = p.gen_problem(3000 + pid * 41)
        probs[pid] = (init, ops)
        p.log({"cell": "meta", "pid": pid, "init": init, "ops": [list(x) for x in ops],
               "truth": p.states_along(init, ops),
               "tail_touched": sorted(p.tail_touched(ops))})
    jobs = []
    for pid in PIDS:
        order = ["A-CKPT4710", "A-CKPT710"] if pid % 2 == 0 else ["A-CKPT710", "A-CKPT4710"]
        jobs += [(cell, pid) for cell in order]
    t0 = time.time()
    for i, (cell, pid) in enumerate(jobs):
        init, ops = probs[pid]
        try:
            filler()
            ckpts = {4, 7, 10} if cell == "A-CKPT4710" else {7, 10}
            ladder(pid, init, ops, ckpts, cell)
        except Exception as e:
            p.log({"cell": "error", "job": [cell, pid], "err": repr(e)})
        print(f"[{i+1}/{len(jobs)}] ({cell!r}, {pid})", flush=True)
    print("\n=== SUMMARY ===", flush=True)
    recs = [json.loads(l) for l in open(os.path.join(OUT, "results-r11.jsonl"))]
    for cell in ("A-CKPT4710", "A-CKPT710"):
        fin = [r for r in recs if r.get("cell") == cell and r.get("turn") == 10 and "ok" in r]
        print(f"{cell}: {sum(1 for r in fin if r['ok'])}/{len(fin)}", flush=True)
    print(f"wall_total_s: {time.time() - t0:.1f}", flush=True)

if __name__ == "__main__":
    main()
