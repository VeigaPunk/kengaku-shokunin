"""Faithful re-implementation of the pinned generator's main() write path (read-only w.r.t. lane)."""
import hashlib, json, os, shutil, sys
from pathlib import Path
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
out = Path(sys.argv[1]); profile = json.loads(sys.argv[2])
if out.exists(): shutil.rmtree(out)
(out / "config_files").mkdir(parents=True)
shutil.copyfile(LANE / "plans/fixtures/r28/webarena/config_files/test.raw.json", out / "config_files/test.raw.json")
env = profile["values"]
with open(out / "config_files/test.raw.json", "r") as f:      # upstream: text mode, locale encoding, universal newlines
    raw = f.read()
for name in ("GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"):
    raw = raw.replace("__%s__" % name, env[name])
with open(out / "config_files/test.json", "w") as f:          # upstream: text mode, locale encoding
    f.write(raw)
data = json.loads(raw)
for idx, item in enumerate(data):
    with open(out / ("config_files/%d.json" % idx), "w") as f:
        json.dump(item, f, indent=2)
print("TESTJSON_SHA", hashlib.sha256((out/"config_files/test.json").read_bytes()).hexdigest())
print("TASK_SHA", json.dumps({str(i): hashlib.sha256((out/("config_files/%d.json"%i)).read_bytes()).hexdigest() for i in (0,1,2,405,811)}))
