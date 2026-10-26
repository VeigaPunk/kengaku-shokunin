import importlib.util
from datetime import datetime, timedelta
CAP="/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round41/tb2-constraints-scheduling/"
spec=importlib.util.spec_from_file_location("g", CAP+"test_outputs.py")
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
cals=[open(CAP+n).read() for n in ("alice_calendar.ics","bob_calendar.ics","carol_calendar.ics")]
valid=[]; t=datetime(2024,1,15,0,0)
while t<datetime(2024,1,20,0,0):
    t1=t+timedelta(hours=1)
    if g._hard_ok(t,t1) and not any(g._overlap(t,t1,c) for c in cals): valid.append(t)
    t+=timedelta(minutes=1)
print("valid 1-hour slots under the captured model:", len(valid))
for v in valid: print(" ", v.strftime("%a %Y-%m-%d %H:%M"))
