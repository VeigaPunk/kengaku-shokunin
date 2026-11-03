import re, pathlib, json, importlib.util
spec = importlib.util.spec_from_file_location("gate", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round63_gate_checks.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
print("TRIO_WINDOW", gate.TRIO_WINDOW, "HEADING_PREFIX", repr(gate.HEADING_PREFIX), "KEYS", gate.TRIO_KEYS)
K = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge")
files = sorted(K.glob("*.md"))
red = [f for f in files if gate.trio_missing(f.read_text(errors="replace"))]
print("TOTAL", len(files), "RED-under-real-gate", len(red))
# frozen list
frozen = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round64/trio-red-at-base.txt")
fl = frozen.read_text()
print("--- frozen list head ---")
print("\n".join(fl.splitlines()[:6]))
print("--- frozen count ---", len([l for l in fl.splitlines() if l.strip()]))
