import json, pathlib, shutil, subprocess, sys, hashlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRIPT = LANE / "plans/config_projection.py"
WORK = pathlib.Path("/tmp/r29pin3")
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
REL = {"MANIFEST": "plans/fixtures/r29/manifest.json",
       "GENERATOR": "plans/fixtures/r29/generate_test_data.py",
       "RAW": "plans/fixtures/r28/webarena/config_files/test.raw.json",
       "PROFILES": "plans/fixtures/r29/profiles.json"}

def fresh(name):
    r = WORK / name
    r.mkdir(parents=True)
    for rel in REL.values():
        dst = r / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LANE / rel, dst)
    return r

def run(r, label):
    p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(r), "--json"], capture_output=True, text=True)
    try:
        f = json.loads(p.stdout).get("findings", [])
        fid = f[0].get("id") if f else None
    except Exception:
        fid = "NONJSON:" + p.stdout[:80]
    print("%-58s exit=%s finding=%s" % (label, p.returncode, fid))

def repin(r, rel):
    m = json.loads((r / REL["MANIFEST"]).read_text())
    m["files"][rel]["sha256"] = hashlib.sha256((r / rel).read_bytes()).hexdigest()
    (r / REL["MANIFEST"]).write_text(json.dumps(m, indent=2) + "\n")

# 1. profiles.json: drop MAP key, manifest pin NOT updated
r = fresh("p1")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); del d["distinct_origins"]["values"]["MAP"]
p.write_text(json.dumps(d, indent=2))
run(r, "profiles_missing_MAP_pin_not_updated")

# 2. same + manifest pin updated
r = fresh("p2")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); del d["distinct_origins"]["values"]["MAP"]
p.write_text(json.dumps(d, indent=2)); repin(r, REL["PROFILES"])
run(r, "profiles_missing_MAP_manifest_repin")

# 3. profiles.json: MAP = 7 (non-string), manifest pin NOT updated
r = fresh("p3")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); d["distinct_origins"]["values"]["MAP"] = 7
p.write_text(json.dumps(d, indent=2))
run(r, "profiles_MAP_nonstring_pin_not_updated")

# 4. profile value breaks JSON (quote), manifest pin NOT updated
r = fresh("p4")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); d["distinct_origins"]["values"]["MAP"] = 'http://x"y'
p.write_text(json.dumps(d, indent=2))
run(r, "profiles_value_breaks_json_pin_not_updated")

# 5. same + manifest pin updated
r = fresh("p5")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); d["distinct_origins"]["values"]["MAP"] = 'http://x"y'
p.write_text(json.dumps(d, indent=2)); repin(r, REL["PROFILES"])
run(r, "profiles_value_breaks_json_manifest_repin")

# 6. generator semantically mutated (order swap), manifest pin NOT updated
r = fresh("g1")
g = r / REL["GENERATOR"]
src = g.read_text()
old = 'raw = raw.replace("__GITLAB__", GITLAB)\n    raw = raw.replace("__REDDIT__", REDDIT)'
assert old in src, src[:400]
g.write_text(src.replace(old, 'raw = raw.replace("__REDDIT__", REDDIT)\n    raw = raw.replace("__GITLAB__", GITLAB)'))
run(r, "generator_order_swapped_pin_not_updated")

# 7. generator semantically mutated + manifest pin updated
r = fresh("g2")
g = r / REL["GENERATOR"]
src = g.read_text()
g.write_text(src.replace(old, 'raw = raw.replace("__REDDIT__", REDDIT)\n    raw = raw.replace("__GITLAB__", GITLAB)'))
repin(r, REL["GENERATOR"])
run(r, "generator_order_swapped_manifest_repin")

# 8. profiles: extra unexpected profile key, manifest pin not updated
r = fresh("p6")
p = r / REL["PROFILES"]
d = json.loads(p.read_text()); d["extra_profile"] = {"purpose": "x", "values": {}}
p.write_text(json.dumps(d, indent=2))
run(r, "profiles_extra_key_pin_not_updated")
