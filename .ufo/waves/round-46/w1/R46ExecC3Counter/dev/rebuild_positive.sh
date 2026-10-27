#!/usr/bin/env bash
set -eu
S=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter
D=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Counter
rm -rf "$S/lane"; git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
cp "$D/round46_c3_verify.py" "$S/lane/plans/round46_c3_verify.py"
rm -rf "$S/lane/plans/filler46"; cp -r "$D/filler46" "$S/lane/plans/filler46"
python3 "$S/dev/build_positive.py"
python3 - <<'PY'
import hashlib, pathlib
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter"); L = S / "lane"
D = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Counter")
src = (D / "round46_c3_verify.py").read_text()
def sh(p): return hashlib.sha256((L / p).read_bytes()).hexdigest()
for name, rel in (("SPEC_SHA256", "plans/pkg-spec-r46.json"),
                  ("PROBE_SHA256", "plans/polyglot_c_py_probe.py"),
                  ("DRY_SHA256", "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt")):
    src = src.replace(name + " = PENDING", '%s = "%s"' % (name, sh(rel)))
(L / "plans/dev_pinned_c3_verify.py").write_text(src)
print("dev-pinned:", sh("plans/dev_pinned_c3_verify.py"))
PY
