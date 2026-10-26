import importlib.util, pathlib, sys
lane = pathlib.Path(sys.argv[1]).resolve(); work = pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("c2", str(lane / "plans/round41_c2_verify.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for name, fn in (("V5", lambda: m.v5(lane)), ("V4", lambda: m.v4(lane)), ("V2", lambda: m.v2(lane, work))):
    try:
        ok, note = fn()
    except Exception as e:
        ok, note = False, f"exception {type(e).__name__}: {e}"
    print(f"{name} {'ok' if ok else 'DEFECT'} {note}")
