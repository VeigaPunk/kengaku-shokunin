"""Read-only probe of the birth r54 counter in scratch: is entry_mode_ok wired, and is the registry cell read?"""
import importlib.util, json, os, sys, io, contextlib, tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location("r54birth", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S = Path(sys.argv[2])

print("== 1. entry_mode_ok on probe argvs (script=plans/gate.py)")
cases = {
 "exact --selftest": ["python3","plans/gate.py","--selftest"],
 "abbrev --selft": ["python3","plans/gate.py","--selft"],
 "abbrev --hel": ["python3","plans/gate.py","--hel"],
 "uv decoy -cprint": ["uv","run","--no-project","--offline","python3","-cprint('wrapper green')","python3","plans/gate.py"],
 "registry cell extra arg check ['python3','plans/gate.py','check','.']": ["python3","plans/gate.py","check","."],
 "non-entry flag after --": ["python3","plans/gate.py","--","--selftest"],
}
for k, a in cases.items():
    print(f"  {k!r:70} -> {m.entry_mode_ok(a, 'plans/gate.py')!r}")

def fixture(name, cell_cmd, argv, state="green", ex=0, extra_rows=None):
    root = S / "fx" / name
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "plans" / "gate.py").write_text("import sys\nprint('x')\nsys.exit(0)\n")
    (root / "SKILL.md").write_text("## Gate/probe registry\n\n| name | kind | entry | verdict map | self-test | pinned | scope | owner |\n|---|---|---|---|---|---|---|---|\n"
        f"| `gate` | gate | `{cell_cmd}` | `0` ok · `1` bad | none | none | none | kengaku |\n")
    row = {"entry_argv": argv, "entry_exit": ex, "entry_state": state}
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps({"schema": "r54-entrytruth-v1", "rows": {"gate": row}}))
    return root

def dry(root):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc, lines = m.evaluate(root, None, None, 1, 10, True)
    return rc, [l for l in lines if l.startswith("ROWS") or "ARGV" in l or "PREDICATE" in l or "DRY" in l]

print("== 2. static legs (dry) on fixtures: registry cell vs ledger argv")
for name, cell, argv in [
  ("A-exact-entry", "python3 plans/gate.py", ["python3","plans/gate.py"]),
  ("B-cell-has-check-arg-ledger-bare", "python3 plans/gate.py check .", ["python3","plans/gate.py"]),
  ("C-ledger-abbrev", "python3 plans/gate.py", ["python3","plans/gate.py","--selft"]),
  ("D-ledger-exact-selftest", "python3 plans/gate.py", ["python3","plans/gate.py","--selftest"]),
  ("E-cell-check-ledger-other-arg", "python3 plans/gate.py check .", ["python3","plans/gate.py","--expect","x"]),
]:
    root = fixture(name, cell, argv)
    rc, ls = dry(root)
    print(f"  {name:34} dry rc={rc} {ls}")
