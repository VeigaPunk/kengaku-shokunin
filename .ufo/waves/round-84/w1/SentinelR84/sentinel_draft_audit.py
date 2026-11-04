#!/usr/bin/env python3
"""SentinelR84 audit of the reviewed R84 probe and counter snapshots.

Pins the audited bytes by sha256, compares the R84 sandbox vector to the R83
baseline, executes the R84 vector once against a diagnostic harness, and proves
the counter parses (never executes) receipt COMMAND values. Read-only on the lane.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
OUT = Path(__file__).resolve().parent
BASE = LANE / "plans/round83_code_image_probe.py"
PROBE = OUT / "reviewed-ProbeR84-round84_gcode_probe.py"
COUNTER = OUT / "reviewed-CounterR84-round84_c1_replay.py"
CAP = LANE / "corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py"
WORK = Path(os.environ["SENTINEL_WORK"])
WORK.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(WORK)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DIAG = r'''
import json, os, socket, subprocess
from pathlib import Path
out = {}
out["env"] = dict(os.environ)
out["netns"] = os.stat("/proc/self/ns/net").st_ino
out["home_visible"] = any(os.path.exists(p) for p in ("/home", "/home/vgpnk", "/home/vgpnk/.ssh", "/home/vgpnk/.omp"))
def attempt(tag, fn):
    try: fn(); out[tag] = "ok"
    except BaseException as e: out[tag] = type(e).__name__ + ":" + str(e)[:80]
attempt("write_tests", lambda: Path("/tests/planted.py").write_text("x"))
attempt("write_usr", lambda: Path("/usr/planted").write_text("x"))
attempt("write_etc", lambda: Path("/etc/planted").write_text("x"))
attempt("write_tmp", lambda: Path("/tmp/planted").write_text("x"))
try:
    s = socket.socket(); s.settimeout(2); s.connect(("1.1.1.1", 80)); out["net"] = "CONNECTED"
except BaseException as e: out["net"] = type(e).__name__ + ":" + str(e)[:60]
print(json.dumps(out))
'''

print(f"PIN probe={PROBE} sha256={hashlib.sha256(PROBE.read_bytes()).hexdigest()}")
print(f"PIN counter={COUNTER} sha256={hashlib.sha256(COUNTER.read_bytes()).hexdigest()}")
print(f"PIN baseline_sha256={hashlib.sha256(BASE.read_bytes()).hexdigest()}")
print(f"HOST netns={os.stat('/proc/self/ns/net').st_ino}")

baseline = load("r83probe", BASE)
probe = load("r84probe", PROBE)
counter = load("r84counter", COUNTER)

case_dir = WORK / "vector-case"
(case_dir / "app").mkdir(parents=True)
(case_dir / "harness.py").write_text(DIAG, encoding="utf-8")
staged = WORK / "test_outputs.py"
staged.write_bytes(CAP.read_bytes())

v83 = baseline.sandbox_argv(staged, case_dir)
v84 = probe.sandbox_argv(staged, case_dir)
print(f"VECTOR equal_to_r83_baseline={v83 == v84}")
print(f"VECTOR argv={json.dumps(v84)}")

p = subprocess.run(v84, capture_output=True, text=True, timeout=60, env={"PATH": "/usr/bin"})
print(f"VECTOR run rc={p.returncode} stderr={p.stderr.strip()[:120]!r}")
obs = json.loads(p.stdout)
print(f"OBS env={json.dumps(obs['env'])}")
print(f"OBS netns_sandbox={obs['netns']} netns_unshared={obs['netns'] != os.stat('/proc/self/ns/net').st_ino}")
print(f"OBS home_visible={obs['home_visible']}")
for key in ("write_tests", "write_usr", "write_etc", "write_tmp", "net"):
    print(f"OBS {key}={json.dumps(obs[key])}")

canonical = "python3 plans/round84_gcode_probe.py --lane . --work /scratch/w"
hostile = (f"python3 plans/round84_gcode_probe.py --lane . --work x; "
           f"touch {WORK / 'COMMAND-EXECUTED'}")
print(f"COMMAND canonical_matches={counter.command_matches(canonical, 'plans/round84_gcode_probe.py')}")
print(f"COMMAND hostile_matches={counter.command_matches(hostile, 'plans/round84_gcode_probe.py')}")
print(f"COMMAND hostile_executed={(WORK / 'COMMAND-EXECUTED').exists()}")

receipt = (f"# tb2 gcode-to-text grader probe\nCOMMAND {hostile}\n"
           "OBSERVATIONS_BEGIN\nCASE exact predicted=P/P observed=P/P\n"
           "cases=8 mismatches=0\nPREDICATE R84-PROBE pass\nOBSERVATIONS_END\n")
stamp, block, structure = counter.parse_receipt(receipt)
print(f"RECEIPT structure={structure!r} stamp_keys={sorted(stamp)} block_lines={len(block)}")
print(f"RECEIPT command_field={stamp.get('COMMAND')!r}")

probe_src = PROBE.read_text(encoding="utf-8")
counter_src = COUNTER.read_text(encoding="utf-8")
print(f"SOURCE probe_receipt_mentions={probe_src.count('RECEIPT')} probe_ledger_mentions={probe_src.count('LEDGER')}")
print(f"SOURCE probe_secret_paths={sum(probe_src.count(s) for s in ('/.ssh', '/.omp', '/.config', '/home/'))}")
print(f"SOURCE counter_secret_paths={sum(counter_src.count(s) for s in ('/.ssh', '/.omp', '/.config', '/home/'))}")
print(f"SOURCE shell_true={probe_src.count('shell=True') + counter_src.count('shell=True')}")
print(f"SOURCE os_system={probe_src.count('os.system') + counter_src.count('os.system')}")
print(f"SOURCE eval_exec={sum(probe_src.count(s) for s in ('eval(', 'exec(')) + sum(counter_src.count(s) for s in ('eval(', 'exec('))}")
