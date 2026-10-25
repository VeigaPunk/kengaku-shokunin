"""Scratch-only v2 check: raced read_snapshot output must equal unraced output; hardenings return stable ids."""
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRIPT = LANE / "plans/benchmark_spec_audit.py"
FIX = Path("plans/fixtures/r28/webarena")
spec = importlib.util.spec_from_file_location("audit_v2", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = Path(tempfile.mkdtemp(prefix="eq-", dir=Path(__file__).resolve().parent))


def fresh():
    root = Path(tempfile.mkdtemp(dir=base))
    shutil.copytree(LANE / FIX, root / FIX)
    return root


def digest(result):
    return hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()


reference, reference_code = mod.read_snapshot(fresh())
rows = {"unraced": {"exit": reference_code, "result_sha256": digest(reference)}}
original = Path.read_bytes
good = json.loads((LANE / FIX / "config_files/test.raw.json").read_text())
for name, relative, replacement in (
    ("population_object", "config_files/test.raw.json", b"{}"),
    ("population_nonobject_items", "config_files/test.raw.json", b"[1, 2, 3]"),
    ("population_truncated", "config_files/test.raw.json", json.dumps(good[:400]).encode()),
    ("evaluators_replaced", "evaluation_harness/evaluators.py", b"x = 1\n"),
    ("helpers_replaced", "evaluation_harness/helper_functions.py", b"def other():\n    pass\n"),
):
    root = fresh()
    target = (root / FIX / relative).resolve()
    reads = {"n": 0}

    def read_bytes(self, target=target, replacement=replacement, reads=reads):
        data = original(self)
        if self.resolve() == target:
            reads["n"] += 1
            if reads["n"] == 1:
                target.write_bytes(replacement)
        return data

    Path.read_bytes = read_bytes
    try:
        result, code = mod.read_snapshot(root)
    finally:
        Path.read_bytes = original
    rows[name] = {"exit": code, "result_sha256": digest(result), "identical_to_unraced": result == reference, "reads_of_target": reads["n"], "disk_now_differs": hashlib.sha256(target.read_bytes()).hexdigest() != result["source_sha256"][relative]}

try:
    mod.scorer_contract("x = 1\n")
    rows["scorer_contract_no_router"] = "no error"
except ValueError as error:
    rows["scorer_contract_no_router"] = "ValueError:" + str(error)
try:
    mod.scorer_contract("def evaluator_router():\n    match x:\n        case 'string_match': StringEvaluator()\n        case 'url_match': URLEvaluator()\n        case 'program_html': HTMLContentEvaluator()\n")
    rows["scorer_contract_no_comb"] = "no error"
except ValueError as error:
    rows["scorer_contract_no_comb"] = "ValueError:" + str(error)
nonlist = mod.audit_tasks({})
rows["audit_tasks_nonlist"] = {"findings": [f["id"] for f in nonlist["findings"]], "has_selected_task_ids": "selected_task_ids" in nonlist}
shutil.rmtree(base)
print(json.dumps(rows, indent=1))
