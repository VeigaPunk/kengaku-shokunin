#!/usr/bin/env python3
"""F37C2Rerun: is gate P10 (fresh probe vs receipt) the load-bearing authenticity guard?

Forge one grader-stdout line inside the committed receipt — a byte that V1, V3, V4, V5, V6
and V7 never read — then ask pkg_gate.c_rerun whether it notices. And check the V6 census
duplicate-id rule (E03) really is caught."""
import importlib.util
import json
import pathlib
import sys
import time

MUT = pathlib.Path(sys.argv[1])


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


c2 = load("c2", MUT / "plans/round37_c2_verify.py")
gate = load("gate", MUT / "plans/pkg_gate.py")

spec = json.loads((MUT / "plans/pkg-spec-r37.json").read_text())
receipt = MUT / spec["receipt"]
pkg = gate.Package(root=MUT, spec=spec)

# --- V6 E03 duplicate id, fixed mutation ------------------------------------------------
src = MUT / "corpus/SOURCES.md"
bak = src.read_bytes()
try:
    dup = "".join(l for l in bak.decode().splitlines(True) if l.startswith("| S111 |"))
    src.write_bytes(bak + dup.encode())
    print("MUT V6 duplicate id (E03):", *c2.v6(MUT))
finally:
    src.write_bytes(bak)

# --- P10 forged receipt byte ------------------------------------------------------------
orig = receipt.read_bytes()
try:
    forged = orig.replace(b"'Content: hello world'", b"'Content: hello world!'", 1)
    assert forged != orig, "forge target not present"
    receipt.write_bytes(forged)
    print(f"forged_receipt sha256_changed={forged != orig} bytes={len(forged)}")
    for check, fn in (("V4", lambda: c2.v4(MUT)), ("V7", lambda: c2.v7(MUT)), ("V1", lambda: c2.v1(MUT))):
        print(f"forged {check}:", *fn())
    t0 = time.time()
    ok, note = gate.c_rerun(pkg)
    print(f"forged P10: {'ok' if ok else 'DEFECT'} {note} wall={time.time() - t0:.1f}s")
    p10_forged = ok
finally:
    receipt.write_bytes(orig)

t0 = time.time()
ok, note = gate.c_rerun(pkg)
print(f"restored P10: {'ok' if ok else 'DEFECT'} {note} wall={time.time() - t0:.1f}s")
print(f"VERDICT p10_catches_forged_stdout={not p10_forged} p10_ok_on_original={ok}")
sys.exit(0 if (not p10_forged and ok) else 1)
