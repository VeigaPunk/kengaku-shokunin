#!/usr/bin/env python3
"""Mechanical test-function index of the TB2 primary grader captures (round 53, C1).

No classification: lists every ``test_*`` function (module level or inside a class) of each
task's primary grader capture (``<task>/tests/test_outputs.py``, else
``<task>/environment/tests/test_outputs.py``) with its 1-based line span.  Used to cut the
blind-label shards before any classifier output exists.
"""
import ast, json, sys
from pathlib import Path

def primary(cap: Path, task: str):
    for rel in (f"{task}/tests/test_outputs.py", f"{task}/environment/tests/test_outputs.py"):
        if (cap / rel).is_file():
            return rel
    return None

def index(lane: Path):
    pop = json.loads((lane / "plans/round52-tasks.json").read_text())
    cap = lane / "corpus/evidence/round52/graders"
    out, nofile, bad = [], [], []
    for task in sorted(pop["tasks"]):
        rel = primary(cap, task)
        if rel is None:
            nofile.append(task); continue
        src = (cap / rel).read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            bad.append([task, str(e)]); continue
        def walk(body, cls=None):
            for n in body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_"):
                    out.append({"id": f"{task}::{(cls + '.') if cls else ''}{n.name}", "task": task,
                                "file": rel, "name": n.name, "class": cls,
                                "lineno": n.lineno, "end_lineno": n.end_lineno})
                elif isinstance(n, ast.ClassDef):
                    walk(n.body, n.name)
        walk(tree.body)
    return {"tests": out, "no_primary_capture": nofile, "syntax_error": bad}

if __name__ == "__main__":
    lane = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    r = index(lane)
    print(f"TESTS total={len(r['tests'])} tasks={len({t['task'] for t in r['tests']})} "
          f"no_primary={len(r['no_primary_capture'])} syntax_error={len(r['syntax_error'])}")
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(r, indent=1) + "\n")
