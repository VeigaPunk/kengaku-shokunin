"""CLI-level task-shape probes on a re-pinned scratch copy; production files are only read."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HERE = Path(__file__).resolve().parent
FIX = Path("plans/fixtures/r28/webarena")
RAW_REL = "config_files/test.raw.json"
pristine = json.loads((LANE / FIX / RAW_REL).read_text())
source = (LANE / "plans/benchmark_spec_audit.py").read_text()
old_manifest_sha = "c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd"
assert old_manifest_sha in source


def run(name, payload_text):
    root = HERE / "roots_cli" / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(LANE / FIX, root / FIX)
    raw = root / FIX / RAW_REL
    raw.write_text(payload_text)
    manifest_path = root / FIX / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files"][RAW_REL]["sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2))
    new_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    script = root / "plans/benchmark_spec_audit.py"
    script.write_text(source.replace(old_manifest_sha, new_sha))
    shutil.copy(LANE / "plans/fixtures/r28/contract-expected.json", root / "plans/fixtures/r28/contract-expected.json")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    out = subprocess.run([sys.executable, "-B", str(script), "--root", str(root), "--json"], capture_output=True, text=True, env=env)
    summ = subprocess.run([sys.executable, "-B", str(script), "--root", str(root), "--summary"], capture_output=True, text=True, env=env)
    try:
        ids = [f["id"] for f in json.loads(out.stdout)["findings"]]
        tasks_len = len(json.loads(out.stdout).get("tasks", []))
    except Exception as error:
        ids, tasks_len = ["UNPARSEABLE " + repr(error)], None
    detail = [f.get("detail") for f in json.loads(out.stdout)["findings"]] if ids and not ids[0].startswith("UNPARSEABLE") else None
    print(json.dumps({"case": name, "json_exit": out.returncode, "summary_exit": summ.returncode, "finding_ids": ids,
                      "details": detail, "tasks_records": tasks_len, "stderr_tail": out.stderr[-200:] + summ.stderr[-200:],
                      "summary_total": [l for l in summ.stdout.splitlines() if l.startswith("TOTAL")]}, sort_keys=True))


def variant(fn):
    tasks = json.loads(json.dumps(pristine))
    fn(tasks)
    return json.dumps(tasks)


run("control_repinned", json.dumps(pristine))
run("top_dict", json.dumps({"tasks": pristine}))
run("top_null", "null")
run("task0_int", variant(lambda t: t.__setitem__(0, 0)))
run("task0_id_true", variant(lambda t: t[0].__setitem__("task_id", True)))
run("task0_id_missing", variant(lambda t: t[0].pop("task_id")))
run("task0_sites_null", variant(lambda t: t[0].__setitem__("sites", None)))
run("task0_intent_missing", variant(lambda t: t[0].pop("intent")))
run("task0_eval_null", variant(lambda t: t[0].__setitem__("eval", None)))
run("task0_login_missing", variant(lambda t: t[0].pop("require_login")))
run("task0_reset_str", variant(lambda t: t[0].__setitem__("require_reset", "false")))
text = json.dumps(pristine)
first = text.index('"task_id": 0,')
run("task0_duplicate_key_shadow", text[:first] + '"task_id": 811, ' + text[first:])
shutil.rmtree(HERE / "roots_cli")
