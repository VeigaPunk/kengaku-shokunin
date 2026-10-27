#!/usr/bin/env python3
"""R46ScribeC3Entry verification harness (read-only on the lane; the fixture lives in scratch).

Runs the round-45 gate's own clauses P3-P8 over a scratch fixture assembled from
  - the C3 entry draft (this seat),
  - the C3 SOURCES rows (R46ScribeC3Rows, renumbered to the converged mapping),
  - the eight captured files at the pin + SHA256SUMS,
  - a minimal corpus/README.md carrying the index row and coverage bullet this seat supplies.
Then it parses the entry's sections with the round-45 counter's own regexes and unit-tests the
`## Predictor` block against hand-built end states (no graded case of the task is executed).
No network, no writes outside the fixture dir.
"""
import importlib.util
import json
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry")
PKG = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else S / "pkg"

sys.dont_write_bytecode = True


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, LANE / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod          # dataclasses resolves cls.__module__ through sys.modules
    spec.loader.exec_module(mod)
    return mod


gate = load("plans/pkg_gate.py", "pkg_gate")
r45 = load("plans/round45_c2_verify.py", "r45")

print(f"FIXTURE {PKG}")
spec = json.loads((PKG / "plans/pkg-spec-r46.json").read_text())
p = gate.Package.load(PKG, spec)
rc = 0
for name, fn in (("P3 quote_shape", gate.c_quote_shape), ("P4 quote_verbatim", gate.c_quote_verbatim),
                 ("P5 captures", gate.c_captures), ("P6 sources", gate.c_sources),
                 ("P7 provenance", gate.c_provenance), ("P8 readme", gate.c_readme)):
    try:
        ok, note = fn(p)
    except Exception as e:  # a clause that cannot run is a defect
        ok, note = False, f"error {type(e).__name__}: {e}"
    rc += not ok
    print(f"{name}: {'ok' if ok else 'DEFECT'} {note}")
print(f"GATE clauses=6 defects={rc}")

entry = (PKG / spec["entry"]).read_text()
secs = re.findall(r"^## (.+)$", entry, re.M)
tbd = entry.count("| TBD |")
print(f"SECTIONS n={len(secs)} {secs}")
print(f"CASETABLE tbd={tbd}")

sec = r45.PRED_SECTION.search(entry)
blocks = r45.PRED_BLOCK.findall(sec.group(1)) if sec else []
print(f"PREDICTOR blocks={len(blocks)}")
if len(blocks) != 1:
    print("PREDICTOR DEFECT: not exactly one python block")
    sys.exit(1)
ns = {}
exec(compile(blocks[0], "predictor", "exec"), ns)
pred = ns["predict"]
lint = r45.lint_block(blocks[0])
print(f"PREDICTOR bytes={len(blocks[0].encode())} lint={lint or 'clean'}")

oracle = (S / "tb2/polyglot-c-py/solution/solve.sh").read_text()
inside = oracle.split("cat <<'EOF' > polyglot/main.py.c\n", 1)[1].rsplit("EOF", 1)[0]
py_only = "import sys\n\ndef f(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\nprint(f(int(sys.argv[1])))\n"
c_only = '#include <stdio.h>\nint main(int argc, char **argv){\n  printf("0\\n");\n  return 0;\n}\n'
CASES = [
    ("oracle-exact-listing", ["main.py.c"], inside, True),
    ("oracle-tuple-listing", ("main.py.c",), inside, True),
    ("oracle-crlf-source", ["main.py.c"], inside.replace("\n", "\r\n"), True),
    ("oracle-cr-only-source", ["main.py.c"], inside.replace("\n", "\r"), False),
    ("listing-cmain-present", ["main.py.c", "cmain"], inside, False),
    ("listing-dotfile", [".main.py.c.swp", "main.py.c"], inside, False),
    ("listing-empty", [], inside, False),
    ("listing-absent", None, inside, False),
    ("source-absent", ["main.py.c"], None, False),
    ("source-wrong-name", ["main.py"], inside, False),
    ("source-python-only", ["main.py.c"], py_only, False),
    ("source-c-only", ["main.py.c"], c_only, False),
    ("source-empty", ["main.py.c"], "", False),
    ("source-whitespace", ["main.py.c"], "  \n\t\n", False),
]
bad = 0
for name, listing, source, want in CASES:
    got = pred(listing, source)
    bad += got != want
    print(f"  {'ok ' if got == want else 'BAD'} {name}: got={got} want={want}")
print(f"PREDICTOR unit_cases={len(CASES)} mismatches={bad}")
print("PREDICATE SCRIBE-C3", "pass" if rc == 0 and bad == 0 and len(blocks) == 1 and not lint else "fail")
sys.exit(0 if rc == 0 and bad == 0 else 1)
