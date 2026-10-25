#!/usr/bin/env python3
"""Second probe: parse/loop ordering mutants + strength of the PINNED generator."""
import ast
import importlib.util
import json
from pathlib import Path

BASE = Path("/tmp/freview-astcontract")
GEN = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py")
spec = importlib.util.spec_from_file_location("cp", BASE / "config_projection.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
source = GEN.read_text()

LOOP = '    for idx, item in enumerate(data):\n        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)\n'
PARSE = "    data = json.loads(raw)\n"
assert LOOP in source and PARSE in source

mutants = {
    "M11a_loop_before_parse": source.replace(PARSE + LOOP, LOOP + PARSE),
    "M11b_parse_after_loop_and_after_replaces": source.replace(PARSE + LOOP, LOOP + PARSE + "    "),
}
for name, text in mutants.items():
    assert text != source, name
    try:
        contract = cp.source_contract(text)
    except cp.Unevaluable as error:
        print("%-42s REJECT %s / %s" % (name, error.finding.get("id"), error.finding.get("detail")))
    else:
        print("%-42s ACCEPT parse_line=%s loop_line=%s" % (name, contract["parse_line"], contract["enumerate_loop_line"]))

# --- strength of the PINNED generator against the properties the contract claims ---
tree = ast.parse(source)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
loop = [n for n in main.body if isinstance(n, ast.For)][0]
js = [n for n in ast.walk(loop) if isinstance(n, ast.JoinedStr)]
print("\nPINNED joined-strings in loop:", [ast.unparse(n) for n in js])
opens = [n for n in ast.walk(loop) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"]
print("PINNED open() calls in loop:", [ast.unparse(n) for n in opens])
print("PINNED joined-str is open() arg0:", bool(js) and isinstance(opens[0].args[0], ast.JoinedStr))
mutations_of_data = [ast.unparse(s) for s in main.body
                     if isinstance(s, ast.Assign) and any(getattr(t, "id", None) == "data" for t in s.targets)]
print("PINNED assignments to data:", mutations_of_data)
raw_mutations = [ast.unparse(s) for s in main.body
                 if isinstance(s, ast.Assign) and any(getattr(t, "id", None) == "raw" for t in s.targets)]
print("PINNED assignments to raw:", raw_mutations)
print("PINNED module-level names bound:", [ast.unparse(s) for s in tree.body if isinstance(s, ast.Assign)])
print("PINNED star import line:", [s.lineno for s in tree.body if isinstance(s, ast.ImportFrom)])
print("PINNED main invoked:", any(isinstance(s, ast.If) for s in tree.body))
print("PINNED import path levels:", [(s.module, s.level, [a.name for a in s.names]) for s in tree.body if isinstance(s, ast.ImportFrom)])
