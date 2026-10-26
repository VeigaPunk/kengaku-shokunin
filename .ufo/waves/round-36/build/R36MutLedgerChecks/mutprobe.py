import importlib.util, pathlib, sys

lane = pathlib.Path(sys.argv[1]).resolve()
name = sys.argv[2]
spec = importlib.util.spec_from_file_location("c1v", lane / "plans" / "round36_c1_verify.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
fn = m.CHECKS.get(name)
if fn is None:
    print(f"CHECK {name} ok=MISSING no-such-check")
    sys.exit(4)
ok, note = fn(lane)
print(f"CHECK {name} ok={ok} note={note}")
sys.exit(0 if ok else 3)
