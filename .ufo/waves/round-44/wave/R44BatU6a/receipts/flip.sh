#!/usr/bin/env bash
# Class-flip probe (seat R44BatU6a): build my four fixtures with the counter's own builder, then run the
# unmodified tool and the U6-relabelled copy on each, printing exit status and the DEFECT class set.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44BatU6a
LANE_PLANS=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans
MOD=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU6a/battery/u6_long_a.py
rm -rf "$S/fxbuild" "$S/tools"
mkdir -p "$S/fxbuild" "$S/tools"
python3 - "$S" <<'PY'
import pathlib, sys
s = pathlib.Path(sys.argv[1])
src = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/anchor_digest_check.py").read_text()
old = 'cls, why = ("digest-short" if len(tok) < 64 else "digest-long")'
new = 'cls, why = ("digest-short" if len(tok) < 64 else "digest-short")'
assert src.count(old) == 1
s.joinpath("tools/ref.py").write_text(src)
s.joinpath("tools/mut.py").write_text(src.replace(old, new, 1))
PY
python3 "$LANE_PLANS/round44_c1_verify.py" --build-module "$MOD" --dest "$S/fxbuild" > "$S/build.txt" 2>&1
echo "BUILD $(cat "$S/build.txt" | cut -c1-120)"
for k in 000 001 002 003; do
  d="$S/fxbuild/f$k"
  for t in ref mut; do
    out=$(python3 "$S/tools/$t.py" --lane "$d" 2>&1); rc=$?
    n=$(printf '%s\n' "$out" | grep -c '^DEFECT ')
    cls=$(printf '%s\n' "$out" | grep -o 'class=[a-z-]*' | sort -u | tr '\n' ' ')
    tok=$(printf '%s\n' "$out" | grep -o 'token=[0-9a-f]*' | head -1 | sed 's/token=//')
    echo "f$k $t rc=$rc defects=$n classes=${cls:-none} token_len=${#tok}"
  done
done
