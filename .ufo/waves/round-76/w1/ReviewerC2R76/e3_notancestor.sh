#!/usr/bin/env bash
# E3 (fixed) — Q3: close_commit on a side branch must print CLOSE-NOT-ANCESTOR, not CLOSE-UNRESOLVED.
set -u
S=/fast/scratch/hyaku/kengaku-r76/ReviewerC2R76
D=$(mktemp -d "$S/fY.XXXXXXXX")
trap 'rm -rf -- "$D"' EXIT

python3 - "$D" <<'PYEOF'
import importlib.util, sys
from pathlib import Path
S = Path("/fast/scratch/hyaku/kengaku-r76/ReviewerC2R76")
spec = importlib.util.spec_from_file_location("gate_fixture", S / "gate_fixture.py")
gf = importlib.util.module_from_spec(spec); spec.loader.exec_module(gf)
gf.build_fixture(Path(sys.argv[1]), "fda63968f29f8f58dc2b28831acac879405b8326")
PYEOF

git -C "$D" init -q -b master
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$TOP" = "$D" ] || { echo "E3 ABORT: toplevel=$TOP want=$D"; exit 1; }
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -qm one
FIRST=$(git -C "$D" rev-parse HEAD)
printf 'more\n' >> "$D/SCORECARD.md"
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -qam two
MASTER=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side "$FIRST"
printf 'side\n' > "$D/SIDE.txt"
git -C "$D" add SIDE.txt
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -qm side
SIDE=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q master
echo "E3 branches: on=$(git -C "$D" branch --show-current) first=${FIRST:0:12} master=${MASTER:0:12} side=${SIDE:0:12}"
[ "$MASTER" != "$SIDE" ] || { echo "E3 ABORT: master==side"; exit 1; }

python3 - "$D" "$SIDE" "$MASTER" <<'PYEOF'
import json, sys
from pathlib import Path
d, side, master = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
led = d / "corpus/routed-findings.jsonl"
rows = [json.loads(l) for l in led.read_text().splitlines() if l.strip()]
for r in rows:
    # R75-D1 alone points at the side-branch commit; the rest at the master tip
    r["close_commit"] = side if r["id"] == "R75-D1" else master
led.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
for rel in ("corpus/evidence/round76/r74-c1-tip.txt", "corpus/evidence/round76/r74-c2-tip.txt",
            "corpus/evidence/round75/c1-after.txt"):
    p = d / rel
    p.write_text(p.read_text().replace("fda63968f29f8f58dc2b28831acac879405b8326", master))
for name in ("SCORECARD.md", "LOG.md"):
    p = d / name
    p.write_text(p.read_text().replace("fda63968f29f8f58dc2b28831acac879405b8326", master))
print("E3 ledger rewritten: R75-D1 -> side, others -> master")
PYEOF

echo "=== E3: gate over fixture with R75-D1 close_commit on side branch"
python3 "$S/gate_fixture.py" --lane "$D" --probe "$D" --receipt "$S/work/e3-receipt.txt" | grep -E "LEDGER R75-D1|DEFECT CLOSE|PREDICATE"
echo "=== E3 rc=$?"
