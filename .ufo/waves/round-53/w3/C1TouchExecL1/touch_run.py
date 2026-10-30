#!/usr/bin/env python3
"""L1 touch-run: run each confirmed P1 test in a bwrap stub world (empty artefacts), host venv pytest, no network.

Writes /fast/scratch/hyaku/kengaku-r53/l1/touch-run-l1.json
"""
from __future__ import annotations
import ast, json, re, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GRAD = LANE / "corpus/evidence/round52/graders"
PY = "/fast/scratch/hyaku/kengaku-r53/l1/pytestenv/bin/python"
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/l1/touch")
TASKS = {
    "cobol-modernization": ["test_required_files_exist", "test_data_files_exist"],
    "log-summary-date-ranges": ["test_summary_file_exists"],
    "path-tracing-reverse": ["test_image_c_exists"],
    "sparql-university": ["test_sparql_file_exists"],
    "extract-moves-from-video": ["test_solution_file_exists"],
    "merge-diff-arc-agi-task": ["test_git_repo_init", "test_algo_py_exists"],
    "prove-plus-comm": ["test_proof_file_exists", "test_compiled_proof_exists"],
    "torch-pipeline-parallelism": ["test_pipeline_parallel_exists"],
    "fix-code-vulnerability": ["test_report_file_exists_example"],
    "modernize-scientific-stack": ["test_dependency_file_exists"],
    "pytorch-model-cli": ["test_weights_file_exists", "test_cli_tool_exists", "test_prediction_file_exists"],
    "torch-tensor-parallelism": ["test_parallel_linear_exists"],
    "gcode-to-text": ["test_hello_file_exists"],
    "mteb-leaderboard": ["test_result_exists"],
    "pytorch-model-recovery": ["test_model_file_exists"],
    "tune-mjcf": ["test_tuned_model_exists"],
    "llm-inference-batching-scheduler": ["test_output_files_exist"],
    "path-tracing": ["test_image_c_exists"],
    "sam-cell-seg": ["test_python_file_exists", "test_csv_output_exists"],
    "winning-avg-corewars": ["test_warrior_exists"],
}


CONFTEST = """import ast, sys, types, importlib.machinery
from pathlib import Path
from unittest.mock import MagicMock


class _Stub(types.ModuleType):
    def __getattr__(self, a):
        return MagicMock()


def _install(name):
    if name in sys.modules:
        return
    try:
        __import__(name)
        return
    except Exception:
        pass
    s = _Stub(name)
    s.__spec__ = importlib.machinery.ModuleSpec(name, importlib.machinery.BuiltinImporter, is_package=True)
    s.__path__ = []
    s.__file__ = "/stub/" + name.replace(".", "/") + "/__init__.py"
    sys.modules[name] = s


mods, rels = set(), set()
try:
    _tree = ast.parse((Path(__file__).parent / "test_outputs.py").read_text())
    for _n in ast.walk(_tree):
        if isinstance(_n, ast.Import):
            for _a in _n.names:
                _parts = _a.name.split(".")
                mods.add(_parts[0])
                for _k in range(2, len(_parts) + 1):
                    mods.add(".".join(_parts[:_k]))
        elif isinstance(_n, ast.ImportFrom):
            if _n.level and _n.module:
                rels.add(_n.module)
            elif _n.module:
                _parts = _n.module.split(".")
                for _k in range(1, len(_parts) + 1):
                    mods.add(".".join(_parts[:_k]))
except Exception:
    pass
for _m in sorted(mods):
    _install(_m)
for _m in sorted(rels):
    _pkg = __name__.split(".")[0] if "." in __name__ else "tests"
    _install(_pkg + "." + _m)
"""

CONFTEST_SRC = CONFTEST

def span_paths(src, fn):
    """Stub candidates: path constants referenced by the function (directly, or via module-level
    constants it reads), absolute or bare-relative."""
    tree = ast.parse(src)
    fn_node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == fn)
    names = {n.id for n in ast.walk(fn_node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    out = []
    for node in ast.walk(tree):
        val = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in names or node.targets[0].id.isupper():
                val = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id.isupper():
            val = node.value
        if val is None and isinstance(node, ast.FunctionDef) and node.name == fn:
            val = node
        if val is None:
            continue
        for sub in ast.walk(val):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                v = sub.value
                if v.startswith("/") or ("/" not in v and 0 < len(v) < 80 and " " not in v and "." in v):
                    out.append(v)
    return sorted(set(out))


def build_world(task, test, stubs):
    tf = GRAD / task / "tests/test_outputs.py"
    sandbox = SCRATCH / (task + "-" + test)
    subprocess.run(["rm", "-rf", str(sandbox)], check=True)
    world = sandbox / "world"
    (world / "tmp").mkdir(parents=True)
    (world / "app").mkdir(parents=True)
    (world / "tests").mkdir(parents=True)
    subprocess.run(["cp", str(tf), str(world / "tests/test_outputs.py")], check=True)
    for extra in (GRAD / task / "tests").iterdir():
        if extra.name not in ("test_outputs.py", "conftest.py", "__pycache__"):
            tgt = world / "tests" / extra.name
            if extra.is_dir():
                subprocess.run(["cp", "-r", str(extra), str(tgt)], check=True)
            else:
                subprocess.run(["cp", str(extra), str(tgt)], check=True)
    (world / "tests" / "conftest.py").write_text(CONFTEST_SRC)
    if re.search(r"^\s*from \.", tf.read_text(encoding="utf-8", errors="replace"), re.M):
        (world / "tests" / "__init__.py").touch()
        pkg = True
    else:
        pkg = False
    made, rel = [], []
    for p in stubs:
        if p.startswith("/"):
            target = world / p.lstrip("/")
            if target.suffix and len(target.suffix) <= 6 and target.name != target.suffix:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
            else:
                target.mkdir(parents=True, exist_ok=True)
            made.append(p)
        else:
            rel.append(p)
    return world, made, rel, pkg


def run_one(task, test):
    tf = GRAD / task / "tests/test_outputs.py"
    src = tf.read_text(encoding="utf-8", errors="replace")
    stubs = span_paths(src, test)
    world, made, rel, pkg = build_world(task, test, stubs)
    cwd_in = "/" if pkg else ("/app" if any(p.startswith("/app") for p in made) else "/tmp")
    for p in rel:
        target = world / cwd_in.lstrip("/") / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch()
        made.append(p + " (cwd " + cwd_in + ")")
    envbin = str(Path(PY).parent.parent)
    cmd = [
        "bwrap", "--unshare-net", "--unshare-pid", "--die-with-parent",
        "--bind", str(world), "/",
        "--dev-bind", "/dev", "/dev", "--proc", "/proc",
        "--ro-bind", "/usr", "/usr",
        "--ro-bind-try", "/lib", "/lib",
        "--ro-bind-try", "/lib64", "/lib64",
        "--ro-bind-try", "/etc", "/etc",
        "--ro-bind", "/home", "/home",
        "--ro-bind", envbin, "/fastenv",
        "--setenv", "TMPDIR", "/tmp", "--setenv", "HOME", "/tmp", "--setenv", "LANG", "C",
        "--setenv", "PATH", "/fastenv/bin:/usr/bin:/bin",
        "--chdir", cwd_in,
        "/fastenv/bin/python", "-m", "pytest", "/tests/test_outputs.py::" + test, "-q", "-p", "no:cacheprovider", "--no-header",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=str(world.parent))
    out = (p.stdout + p.stderr).strip()
    m = [l for l in out.splitlines() if "passed" in l or "failed" in l or "ERROR" in l]
    outcome = "passed" if p.returncode == 0 and "1 passed" in out else "failed rc=" + str(p.returncode)
    return {"task": task, "test_id": task + "::" + test, "stub_paths": made,
            "cmd": "bwrap(world=/; stub-import-hook conftest; cwd=" + cwd_in + ") pytest /tests/test_outputs.py::" + test,
            "outcome": outcome, "detail": (m[-1] if m else out[-500:])}


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    results = []
    only = sys.argv[1:] or None
    for task, tests in TASKS.items():
        for t in tests:
            if only and not any(o in f"{task}::{t}" for o in only):
                continue
            try:
                r = run_one(task, t)
            except Exception as e:
                r = {"task": task, "test_id": f"{task}::{t}", "stub_paths": [], "cmd": "", "outcome": f"error {type(e).__name__}", "detail": str(e)[:300]}
            results.append(r)
            print(r["test_id"], "->", r["outcome"], flush=True)
    Path("/fast/scratch/hyaku/kengaku-r53/l1/touch-run-l1.json").write_text(json.dumps(results, indent=1))
    from collections import Counter
    print(Counter(r["outcome"].split()[0] for r in results))


if __name__ == "__main__":
    main()
