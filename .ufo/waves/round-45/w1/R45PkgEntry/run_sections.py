#!/usr/bin/env python3
"""Run the frozen C2 counter's section legs (V7, V9, V10, V11) against a staged clone holding the draft entry."""
import importlib.util, pathlib, shutil, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45PkgEntry/lane")
WORK = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45PkgEntry/v11work")
ENTRY = LANE / ".ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md"

shutil.copy(ENTRY, CLONE / "corpus/knowledge" / ENTRY.name)
WORK.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("c2", LANE / "plans/round45_c2_verify.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for name in ("v1", "v3", "v4", "v5", "v7", "v9", "v10"):
    try:
        ok, note = getattr(m, name)(CLONE)
    except Exception as e:
        ok, note = False, f"raised {type(e).__name__}: {e}"
    print(f"{name.upper()} {'ok' if ok else 'DEFECT'} {note}")
try:
    ok, note = m.v11(CLONE, WORK)
except Exception as e:
    ok, note = False, f"raised {type(e).__name__}: {e}"
print(f"V11 {'ok' if ok else 'DEFECT'} {note}")
