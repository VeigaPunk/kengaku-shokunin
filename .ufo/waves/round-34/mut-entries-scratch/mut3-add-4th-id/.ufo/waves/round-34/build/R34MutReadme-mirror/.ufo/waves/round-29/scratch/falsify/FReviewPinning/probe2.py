import json, pathlib, shutil, subprocess, sys, os, resource

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRIPT = LANE / "plans/config_projection.py"
WORK = pathlib.Path("/tmp/r29pin2")
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
REL = ["plans/fixtures/r29/manifest.json", "plans/fixtures/r29/generate_test_data.py",
       "plans/fixtures/r28/webarena/config_files/test.raw.json", "plans/fixtures/r29/profiles.json"]
root = WORK / "tree"
for rel in REL:
    dst = root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LANE / rel, dst)

def run(script, r, label):
    p = subprocess.run([sys.executable, str(script), "--root", str(r), "--json"], capture_output=True, text=True)
    try:
        f = json.loads(p.stdout).get("findings", [])
        fid = f[0].get("id") if f else None
    except Exception:
        fid = "NONJSON"
    print("%-46s exit=%s finding=%s stderr_tail=%s" % (label, p.returncode, fid, p.stderr.strip().splitlines()[-1:] ))
    return p

# A: ORDER constant edited in a copy of the instrument -> authentic generator must be rejected
src = SCRIPT.read_text()
s1 = WORK / "order_edited.py"
assert 'ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")' in src
s1.write_text(src.replace('ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")',
                           'ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "MAP", "WIKIPEDIA")'))
run(s1, root, "A_order_constant_edited_vs_authentic_gen")

# B: MANIFEST_SHA256 constant edited only (no rebinding)
s2 = WORK / "pin_edited.py"
s2.write_text(src.replace('MANIFEST_SHA256 = "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87"',
                           'MANIFEST_SHA256 = "0000000000000000000000000000000000000000000000000000000000000000"'))
run(s2, root, "B_manifest_pin_constant_edited_only")

# C: pinned raw path is a symlink to /dev/zero (unbounded read), address-space capped
root2 = WORK / "tree_zero"
shutil.copytree(root, root2, symlinks=True)
raw = root2 / "plans/fixtures/r28/webarena/config_files/test.raw.json"
raw.unlink()
raw.symlink_to("/dev/zero")
def limit():
    resource.setrlimit(resource.RLIMIT_AS, (400 * 1024 * 1024, 400 * 1024 * 1024))
p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root2), "--json"],
                   capture_output=True, text=True, preexec_fn=limit, timeout=120)
print("C_raw_symlink_to_dev_zero exit=%s stderr_tail=%s" % (p.returncode, p.stderr.strip().splitlines()[-3:]))
