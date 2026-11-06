#!/usr/bin/env python3
import json, subprocess, sys
a = sys.argv
lane = a[a.index("--lane")+1]
rev = a[a.index("--rev")+1]
raw = subprocess.run(["git","-C",lane,"show",f"{rev}:plans/grader-population-ledger.json"],capture_output=True,text=True).stdout
ok = json.loads(raw)["members"]["build-pmars"].get("status") == "executed"
print("PREDICATE R90-C1 " + ("pass" if ok else "fail"))
sys.exit(0 if ok else 1)
