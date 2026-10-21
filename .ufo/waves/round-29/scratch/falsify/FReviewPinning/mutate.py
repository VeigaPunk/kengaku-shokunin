import json, os, shutil, subprocess, sys, hashlib, pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRIPT = LANE / "plans/config_projection.py"
WORK = pathlib.Path("/tmp/r29pin")
REL = {
    "MANIFEST": "plans/fixtures/r29/manifest.json",
    "GENERATOR": "plans/fixtures/r29/generate_test_data.py",
    "RAW": "plans/fixtures/r28/webarena/config_files/test.raw.json",
    "PROFILES": "plans/fixtures/r29/profiles.json",
}

def fresh(name):
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for rel in REL.values():
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LANE / rel, dst)
    return root

def run(root, script=SCRIPT, extra=None):
    cmd = [sys.executable, str(script), "--root", str(root), "--json"]
    if extra:
        cmd = [sys.executable, str(script), "--root", str(root)] + extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        payload = json.loads(p.stdout)
        findings = payload.get("findings", [])
        fid = findings[0].get("id") if findings else None
        fdet = findings[0] if findings else None
    except Exception:
        fid, fdet = "NONJSON", p.stdout[:200] + "|" + p.stderr[-200:]
    return p.returncode, fid, fdet

def report(label, root, script=SCRIPT):
    rc, fid, fdet = run(root, script)
    print("SCENARIO %-42s exit=%s finding=%s detail=%s" % (label, rc, fid, json.dumps(fdet, sort_keys=True) if isinstance(fdet, dict) else fdet))
    return rc, fid

print("== baseline ==")
report("baseline_authentic", fresh("s00"))

print("== manifest states ==")
r = fresh("s01"); (r / REL["MANIFEST"]).unlink(); report("manifest_deleted", r)
r = fresh("s02"); (r / REL["MANIFEST"]).write_bytes((r / REL["MANIFEST"]).read_bytes() + b" "); report("manifest_extra_byte", r)
r = fresh("s03"); m = json.loads((r / REL["MANIFEST"]).read_text()); (r / REL["MANIFEST"]).write_text(json.dumps(m, indent=4)); report("manifest_reformatted_semantically_same", r)
r = fresh("s04"); m = json.loads((r / REL["MANIFEST"]).read_text()); m["files"]["plans/fixtures/r29/extra.json"] = {"sha256": "00"*32}; (r / REL["MANIFEST"]).write_text(json.dumps(m, indent=2)); report("manifest_fileset_changed_pin_in_code", r)
r = fresh("s05"); m = json.loads((r / REL["MANIFEST"]).read_text()); m["replacement_order"] = list(reversed(m["replacement_order"])); (r / REL["MANIFEST"]).write_text(json.dumps(m, indent=2)); report("manifest_replacement_order_reversed", r)
r = fresh("s06"); (r / REL["MANIFEST"]).write_bytes(b""); report("manifest_empty", r)
r = fresh("s07"); (r / REL["MANIFEST"]).write_bytes(b"{not json"); report("manifest_not_json", r)

print("== pinned input states ==")
for key in ("GENERATOR", "RAW", "PROFILES"):
    r = fresh("m_" + key); (r / REL[key]).unlink(); report(key + "_deleted", r)
    r = fresh("t_" + key); p = r / REL[key]; p.write_bytes(p.read_bytes() + b" "); report(key + "_byte_appended", r)
    r = fresh("d_" + key); p = r / REL[key]; p.unlink(); p.mkdir(); report(key + "_is_directory", r)
    r = fresh("s_" + key); p = r / REL[key]; p.unlink(); p.symlink_to("/nonexistent/nope"); report(key + "_broken_symlink", r)

print("== coherent rebinding ==")
r = fresh("c01")
raw = r / REL["RAW"]
data = raw.read_bytes().replace(b'"task_id": 0,', b'"task_id": 0, "extra": "__MAP__",', 1)
raw.write_bytes(data)
m = json.loads((r / REL["MANIFEST"]).read_text())
m["files"][REL["RAW"]]["sha256"] = hashlib.sha256(data).hexdigest()
(r / REL["MANIFEST"]).write_text(json.dumps(m, indent=2) + "\n")
report("coherent_rebinding_manifest_pin_updated", r)

# same, plus the instrument's own MANIFEST_SHA256 constant edited (co-located trust anchor)
r = fresh("c02")
raw = r / REL["RAW"]
data = raw.read_bytes().replace(b'"task_id": 0,', b'"task_id": 0, "extra": "__MAP__",', 1)
raw.write_bytes(data)
m = json.loads((r / REL["MANIFEST"]).read_text())
m["files"][REL["RAW"]]["sha256"] = hashlib.sha256(data).hexdigest()
(r / REL["MANIFEST"]).write_text(json.dumps(m, indent=2) + "\n")
newdigest = hashlib.sha256((r / REL["MANIFEST"]).read_bytes()).hexdigest()
sc = WORK / "c02_script.py"
src = SCRIPT.read_text()
assert 'MANIFEST_SHA256 = "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87"' in src
sc.write_text(src.replace('MANIFEST_SHA256 = "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87"', 'MANIFEST_SHA256 = "%s"' % newdigest))
rc, fid, fdet = run(r, script=sc)
print("SCENARIO %-42s exit=%s finding=%s detail=%s" % ("coherent_rebinding_PLUS_code_pin_edited", rc, fid, json.dumps(fdet, sort_keys=True) if isinstance(fdet, dict) else fdet))
if rc == 0:
    payload = json.loads(subprocess.run([sys.executable, str(sc), "--root", str(r), "--json"], capture_output=True, text=True).stdout)
    print("   rebinding_blessed_population", payload["population"]["task_profile_projections"], "inputs", json.dumps(payload["inputs"], sort_keys=True))

print("== root misdirection ==")
r = fresh("r01"); (r / REL["GENERATOR"]).unlink(); report("only_manifest_present", r)
r = fresh("r02")
# authentic manifest reached through a symlink
(r / REL["MANIFEST"]).unlink()
(r / REL["MANIFEST"]).symlink_to(LANE / REL["MANIFEST"])
report("manifest_behind_symlink_to_authentic", r)
r = fresh("r03")
# pinned raw file replaced by a symlink to a different file with different content
alt = WORK / "alt_raw.json"
alt.write_text("[]\n")
(r / REL["RAW"]).unlink()
(r / REL["RAW"]).symlink_to(alt)
report("raw_symlink_to_other_content", r)
