#!/usr/bin/env python3
"""ExecC1 independent reward check: for every one of the 18 cases, stage the app exactly as the
captured image does and run real pytest on the captured tests/test_outputs.py; compare pytest's
exit code with the reward leg the committed receipt observed.

Staging reuses the frozen probe's VARIANTS table and stage() (data + the same bwrap recipe); the
reward is measured here by pytest's own exit code, not read from the probe's payload.
"""
import importlib.util
import json
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
G = Path(sys.argv[2]).resolve()
WORK = Path(sys.argv[3]).resolve()

spec = importlib.util.spec_from_file_location("probe", LANE / "plans/round97_sparql_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

cap = LANE / probe.CAP
box = probe.Box("/usr/bin/bwrap", sorted({str(G), probe.interpreter_root(G)}))
table = json.loads((LANE / probe.TABLE).read_text())
receipt = (LANE / "corpus/evidence/round97/sparql-probe.txt").read_text()

reward = {}
for line in receipt.splitlines():
    if line.startswith("CASE "):
        tok = line.split()[1:]
        cid = tok[0]
        parts = dict(t.split("=", 1) for t in tok[1:] if "=" in t)
        reward[cid] = parts["observed"].split(",")[-1]

tests = WORK / "tests"
if tests.exists():
    import shutil
    shutil.rmtree(tests)
tests.mkdir(parents=True)
for n in ("test_outputs.py", "university_graph_test.ttl"):
    import shutil
    shutil.copyfile(cap / "tests" / n, tests / n)

print("case pytest_rc receipt_reward match")
bad = []
for case in table["cases"]:
    cid = case["id"]
    app = probe.stage(box, case, cap, WORK / "cases" / cid)
    p = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests")], "/app",
                str(G) + "/bin:/usr/bin",
                [str(G / "bin/python"), "-I", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 "/tests/test_outputs.py"])
    got = "1" if p.returncode == 0 else "0"
    ok = got == reward.get(cid)
    if not ok:
        bad.append((cid, p.returncode, reward.get(cid), p.stdout[-300:]))
    print(cid, p.returncode, reward.get(cid), "OK" if ok else "MISMATCH")
print("reward_mismatches=%d" % len(bad))
for b in bad:
    print("BAD", b)
