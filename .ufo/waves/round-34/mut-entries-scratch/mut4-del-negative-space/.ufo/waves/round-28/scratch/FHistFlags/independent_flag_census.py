#!/usr/bin/env python3
"""FHistFlags independent census — stdlib only, no benchmark_spec_audit import.

Reads the pinned raw task JSON as data. Counts require_login / require_reset
flag distributions and storage_state path-string counts. Never opens any
referenced auth-state file; path strings are data, not credentials.
"""
import collections
import json
import sys

RAW = sys.argv[1] if len(sys.argv) > 1 else (
    "plans/fixtures/r28/webarena/config_files/test.raw.json")

tasks = json.loads(open(RAW).read())
login = collections.Counter()
reset = collections.Counter()
storage = collections.Counter()
site_storage = collections.defaultdict(collections.Counter)
anomalies = []

for i, t in enumerate(tasks):
    rl = t.get("require_login")
    rr = t.get("require_reset")
    ss = t.get("storage_state")
    if not isinstance(rl, bool):
        anomalies.append(("require_login_not_bool", i, t.get("task_id"), rl))
    if not isinstance(rr, bool):
        anomalies.append(("require_reset_not_bool", i, t.get("task_id"), rr))
    if ss is not None and not isinstance(ss, str):
        anomalies.append(("storage_state_not_str", i, t.get("task_id"), ss))
    login[str(rl).lower()] += 1
    reset[str(rr).lower()] += 1
    storage[ss if isinstance(ss, str) else "<absent>"] += 1
    site_storage[",".join(sorted(t.get("sites", [])))][ss if isinstance(ss, str) else "<absent>"] += 1

out = {
    "task_count": len(tasks),
    "require_login": dict(login),
    "require_reset": dict(reset),
    "storage_state": dict(sorted(storage.items(), key=lambda kv: -kv[1])),
    "site_set_storage": {k: dict(v) for k, v in sorted(site_storage.items())},
    "anomalies": anomalies,
}
print(json.dumps(out, indent=2, sort_keys=True))
