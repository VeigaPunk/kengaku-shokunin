# Map raw-word diffs to extracted amounts: diff extracted JSONs between the two runs if any
import json, pathlib
h = pathlib.Path("run-host553/invoices-json"); c = pathlib.Path("run-conda534/invoices-json")
for j in sorted(h.iterdir()):
    a = json.loads(j.read_text()); b = json.loads((c / j.name).read_text())
    print(j.name, "SAME" if a == b else f"DIFF host={a} conda={b}")
