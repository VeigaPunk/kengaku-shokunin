import importlib.util, pathlib, sys
D, S = sys.argv[1], pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("c3", D + "/round46_c3_verify.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class P:
    pass

pkg = P(); pkg.capdir = S / "dev/pkg/captures"; pkg.entry = S / "dev/entry.md"

def run(name, block):
    pkg.entry.write_text("# x\n\n## Predictor\n\n```python\n" + block + "```\n")
    ok, note = m.v11(pkg, S / ("dev/v11-" + name))
    print(f"V11 {name:22s} {'ok' if ok else 'DEFECT'} {note}")

run("reference", pathlib.Path(S / "v11-reference-predictor.py").read_text())
run("always-true", "def predict(files, source):\n    return True\n")
run("always-false", "def predict(files, source):\n    return False\n")
run("shift-table", "def predict(files, source, n=[-1]):\n    n[0] += 1\n    return (105619152396303 >> n[0]) & 1 == 1\n")
run("dict-table", "def predict(files, source):\n    t = {1: True}\n    return t[1]\n")
run("verbatim-tuple", "def predict(files, source):\n    T = (" + ", ".join("%r" % ("x" * 400) for _ in range(20)) + ")\n    return True\n")
run("file-read", "import json\ndef predict(files, source):\n    return True\n")
