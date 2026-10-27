#!/usr/bin/env python3
"""R45SonicPinCheck repro: verify PINS (round45_c1_verify.py) and CAPTURES
(round45_c2_verify.py) against the lane. Read-only. Run from anywhere:
    python3 verify_pins.py
"""
import ast
import hashlib
import pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")


def dict_of(path, name):
    tree = ast.parse(pathlib.Path(path).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise KeyError(name)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


pins = dict_of(LANE / "plans/round45_c1_verify.py", "PINS")
missing, mismatch, ok = [], [], []
for rel, dig in pins.items():
    p = LANE / rel
    if not p.exists():
        missing.append(rel)
    elif sha(p) == dig:
        ok.append(rel)
    else:
        mismatch.append(rel)
print(f"PINS total={len(pins)} exists_ok={len(ok)} missing={len(missing)} "
      f"digest_mismatch={len(mismatch)}")
print("missing:", missing)
print("mismatch:", mismatch)

caps = dict_of(LANE / "plans/round45_c2_verify.py", "CAPTURES")
capdir = LANE / "corpus/evidence/round45/tb2-password-recovery"
c_missing, c_mismatch, c_ok = [], [], []
for rel, dig in caps.items():
    p = capdir / rel
    if not p.exists():
        c_missing.append(rel)
    elif sha(p) == dig:
        c_ok.append(rel)
    else:
        c_mismatch.append(rel)
print(f"CAPTURES total={len(caps)} exists_ok={len(c_ok)} missing={len(c_missing)} "
      f"digest_mismatch={len(c_mismatch)}")
print("missing:", c_missing)
print("mismatch:", c_mismatch)

sums = {}
for line in (capdir / "SHA256SUMS").read_text().splitlines():
    if line.strip():
        d, n = line.split(None, 1)
        sums[n.strip().lstrip("*")] = d
print("CAPTURES not in SHA256SUMS:", sorted(set(caps) - set(sums)))
print("SHA256SUMS not in CAPTURES:", sorted(set(sums) - set(caps)))
print("digest disagreements:",
      sorted(n for n in set(caps) & set(sums) if caps[n] != sums[n]))
on_disk = sorted(str(p.relative_to(capdir)) for p in capdir.rglob("*") if p.is_file())
print("files in capdir not in CAPTURES:", sorted(set(on_disk) - set(caps)))
