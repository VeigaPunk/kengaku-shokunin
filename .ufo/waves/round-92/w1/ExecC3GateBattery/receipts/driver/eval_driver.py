import importlib.util, os, sys
from pathlib import Path
clone = Path(sys.argv[1]); rev = sys.argv[2]; work = Path(sys.argv[3])
os.environ["SHOKUNIN_ROOT"] = "/home/vgpnk/Projects/shokunin"
spec = importlib.util.spec_from_file_location("r92gate", clone / "plans/round92_burndown.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lane = m.Lane(Path(clone).resolve())
lines, code = m.evaluate(lane, rev, 92, work)
for line in lines:
    print(line)
print("EVALUATE-RC", code)
