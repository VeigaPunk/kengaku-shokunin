"""Scratch-only probes of plans/benchmark_spec_audit.py; production files are only read/copied."""
import hashlib
import importlib.util
import io
import json
import contextlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRIPT = LANE / "plans/benchmark_spec_audit.py"
FIX = Path("plans/fixtures/r28/webarena")
OUT = Path(__file__).resolve().parent


def fresh(base):
    root = Path(tempfile.mkdtemp(prefix="root-", dir=base))
    shutil.copytree(LANE / FIX, root / FIX)
    return root


def cli(root, *extra):
    p = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(root), "--json", *extra], capture_output=True, text=True)
    try:
        body = json.loads(p.stdout)
        findings = [f["id"] for f in body.get("findings", [])]
        inventory = "metrics" in body and bool(body.get("metrics"))
    except json.JSONDecodeError:
        findings, inventory = ["<non-json stdout>"], False
    return {"exit": p.returncode, "findings": findings[:6], "n_findings": len(findings), "inventory_emitted": inventory, "stderr_tail": p.stderr.strip().splitlines()[-1:] }


def load_module():
    spec = importlib.util.spec_from_file_location("audit_probe", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(mod)
    return mod


def race(mod, root, relative, replacement):
    """Simulate a writer that replaces `relative` immediately after the hash read; returns main()-equivalent outcome."""
    target = (root / FIX / relative).resolve()
    original = Path.read_bytes
    state = {"hashed": 0}

    def read_bytes(self):
        data = original(self)
        if self.resolve() == target and state["hashed"] == 0:
            state["hashed"] = 1
            target.write_bytes(replacement)
        return data

    Path.read_bytes = read_bytes
    try:
        try:
            result, code = mod.read_snapshot(root)
            outcome = {"exit": code, "findings": [f["id"] for f in result["findings"]][:6], "n_findings": len(result["findings"]), "inventory_emitted": bool(result.get("metrics")), "task_count": result.get("metrics", {}).get("task_count"), "upstream_revision_claimed": result.get("upstream_revision"), "source_sha256_claimed": result.get("source_sha256", {}).get(relative)}
        except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
            outcome = {"exit": 2, "findings": ["input_missing" if isinstance(error, FileNotFoundError) else "input_invalid"], "detail": str(error)}
        except BaseException as error:  # anything main() does not catch escapes as a traceback
            outcome = {"uncaught": type(error).__name__, "detail": str(error), "process_exit_if_cli": 1}
    finally:
        Path.read_bytes = original
    outcome["bytes_actually_audited_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    return outcome


def main():
    base = Path(tempfile.mkdtemp(prefix="run-", dir=OUT))
    rows = {}
    rows["P0_baseline_copy"] = cli(fresh(base))

    r = fresh(base); (r / FIX / "manifest.json").unlink(); rows["P1_manifest_missing"] = cli(r)
    r = fresh(base); (r / FIX / "manifest.json").write_text("[]"); rows["P2_manifest_nonobject_list"] = cli(r)
    r = fresh(base); (r / FIX / "manifest.json").unlink(); (r / FIX / "manifest.json").mkdir(); rows["P3_manifest_is_directory"] = cli(r)
    r = fresh(base); (r / FIX / "selected-task-ids.json").unlink(); rows["P4_selection_missing"] = cli(r)
    r = fresh(base); (r / FIX / "selected-task-ids.json").write_text("{}"); rows["P5_selection_nonlist"] = cli(r)
    r = fresh(base); (r / FIX / "config_files/test.raw.json").write_text("{}"); rows["P6_population_nonobject_static"] = cli(r)
    r = fresh(base); (r / FIX / "config_files/test.raw.json").write_text("[]"); rows["P7_population_empty_static"] = cli(r)

    # Coherent static rebind: alter population, then rewrite manifest sha and selection to match.
    r = fresh(base)
    pop = r / FIX / "config_files/test.raw.json"
    tasks = json.loads(pop.read_text()); tasks = tasks[:16]; pop.write_text(json.dumps(tasks))
    m = json.loads((r / FIX / "manifest.json").read_text())
    m["files"]["config_files/test.raw.json"]["sha256"] = hashlib.sha256(pop.read_bytes()).hexdigest()
    (r / FIX / "manifest.json").write_text(json.dumps(m))
    (r / FIX / "selected-task-ids.json").write_text(json.dumps(list(range(16))))
    rows["P8_coherent_rebind_manifest_selection_population"] = cli(r)

    mod = load_module()
    rows["R1_population_swapped_to_object_after_hash"] = race(mod, fresh(base), "config_files/test.raw.json", b"{}")
    rows["R2_population_swapped_to_nonobject_items_after_hash"] = race(mod, fresh(base), "config_files/test.raw.json", b"[1, 2, 3]")
    good = json.loads((LANE / FIX / "config_files/test.raw.json").read_text())
    rows["R3_population_truncated_after_hash"] = race(mod, fresh(base), "config_files/test.raw.json", json.dumps(good[:400]).encode())
    rows["R4_evaluators_swapped_after_hash"] = race(mod, fresh(base), "evaluation_harness/evaluators.py", b"x = 1\n")
    rows["R5_selection_swapped_after_hash_control"] = race(mod, fresh(base), "selected-task-ids.json", b"[]")
    rows["R6_manifest_swapped_after_hash_control"] = race(mod, fresh(base), "manifest.json", b"[]")
    shutil.rmtree(base)
    print(json.dumps(rows, indent=1))


main()
