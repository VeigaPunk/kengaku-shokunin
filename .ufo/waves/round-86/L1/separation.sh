#!/bin/bash
# Round-86 causal-separation test. Each claim's counter is run on a tree with the OTHER
# claim's landing reverted; both must still print PREDICATE pass. Evidence, not a gate.
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
W=${1:?usage: separation.sh <scratch-dir>}
mkdir -p "$W"
TIP=$(git -C "$L" rev-parse master)
echo "# R86 separation test — tip $TIP, $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "# A: revert C1 (ledger row back to unexecuted, receipt removed); run C2."
rm -rf "$W/a"; mkdir -p "$W/a"
git -C "$L" archive "$TIP" | tar -x -C "$W/a"
python3 - "$W/a" <<'PY'
import json, os, sys
root = sys.argv[1]
p = os.path.join(root, "plans/grader-population-ledger.json")
d = json.load(open(p))
row = d["members"]["raman-fitting"]
row.clear(); row.update({"classes": ["file-artifact", "numeric-band", "serialization-schema"],
                         "evidence": "no-blocker: tests/test_outputs.py sha256=171fae772ccf262a",
                         "reason": "unattempted", "status": "unexecuted"})
json.dump(d, open(p, "w"), indent=2); open(p, "a").write("\n")
os.remove(os.path.join(root, "corpus/evidence/round86/raman-fitting-probe.txt"))
print("reverted C1 artefacts in the fixture")
PY
echo "\$ python3 plans/round86_c2_repin.py --lane $W/a --root $W/a --work $W/a-w --no-selftest"
python3 "$L/plans/round86_c2_repin.py" --lane "$W/a" --root "$W/a" --work "$W/a-w" --no-selftest 2>&1
echo "rc=$?"
echo
echo "# B: revert C2 (box-4 pointer and pin back to the stale 129); run C1."
rm -rf "$W/b"; mkdir -p "$W/b"
git -C "$L" archive "$TIP" | tar -x -C "$W/b"
python3 - "$W/b" <<'PY'
import os, sys
root = sys.argv[1]
def rewrite(path, old, new):
    t = open(path).read(); assert old in t, old
    tmp = path + ".tmp"; open(tmp, "w").write(t.replace(old, new, 1)); os.replace(tmp, path)
rewrite(os.path.join(root, "SHONEN.md"), "PROVINCE.md:151", "PROVINCE.md:129")
rewrite(os.path.join(root, "plans/state_check.py"),
        '4, "PROVINCE.md:151", 151,', '4, "PROVINCE.md:129", 129,')
print("reverted C2 repair in the fixture")
PY
echo "\$ python3 plans/round86_c1_replay.py --lane $W/b --repo $L --work $W/b-w"
python3 "$L/plans/round86_c1_replay.py" --lane "$W/b" --repo "$L" --work "$W/b-w" 2>&1
echo "rc=$?"
