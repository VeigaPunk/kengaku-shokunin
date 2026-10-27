#!/usr/bin/env bash
# R44LabratControls: replay of .ufo/waves/round-44/claims/c1_controls.sh against a clean --no-local clone at
# 5f16ed04b04a80a17a5a1a060c12093d9a152a64. Every command mirrors the frozen script's, with $L the clone and
# every output under $O (never the lane, never the clone's claims tree).
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44LabratControls
L=$S/lane
C=$L/.ufo/waves/round-44/claims
O=${1:-$S/out}
W=${2:-$S/ctl}
mkdir -p "$O" "$W"
grep -q 'kengaku r44 round root' /fast/scratch/hyaku/kengaku-r44/.ROUND-ROOT-SENTINEL || { echo "SENTINEL MISSING"; exit 3; }
[ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || { echo "CLONE TOPLEVEL MISMATCH"; exit 3; }
[ "$(git -C "$L" rev-parse HEAD)" = "5f16ed04b04a80a17a5a1a060c12093d9a152a64" ] || { echo "CLONE HEAD MISMATCH"; exit 3; }
env44() { "$C/envelope.sh" "$W" "$@"; }
mirror() {
  local m=$W/m-$1; rm -rf -- "$m"; mkdir -p "$m/plans"
  cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$L"/plans/round44_c1_verify.py \
     "$L"/plans/round43_c1_verify.py "$m/plans/"; echo "$m"; }
patched() {
  python3 - "$1/plans/round44_c1_verify.py" "$2" "$3" <<'PY'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
  diff -u "$L/plans/round44_c1_verify.py" "$1/plans/round44_c1_verify.py" | sed 's/^/DIFF /'; }
B=$(mirror base)
# 1 witness run
env44 python3 "$L/plans/round44_c1_verify.py" --lane "$L" --battery-dir "$C/witness" --work "$W/w1" > "$O/witness-run.txt" 2>&1
# 2 do-nothing
env44 python3 "$L/plans/round44_c1_verify.py" --lane "$L" --work "$W/w2" > "$O/control-c1-nothing.txt" 2>&1
# 3 standing batteries
M=$(mirror standing); mkdir -p "$M/plans/battery44"
for f in "$L"/plans/battery42/*.py; do cp "$f" "$M/plans/battery44/b42_$(basename "$f")"; done
for f in "$L"/plans/battery43/*.py; do cp "$f" "$M/plans/battery44/b43_$(basename "$f")"; done
{ ls "$M/plans/battery44" | sed 's/^/MODULE /'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w3s"; } > "$O/control-c1-standing-batteries.txt" 2>&1
# 4 witness as battery
M=$(mirror wab); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w3" > "$O/control-c1-witness-as-battery.txt" 2>&1
# 5 emptied mutant list
M=$(mirror nomut); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ python3 - "$M/plans/round44_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i) + 3
open(p, "w").write(s[:i] + "MUTANTS = []\n" + s[j:])
PY
  diff -u "$L/plans/round44_c1_verify.py" "$M/plans/round44_c1_verify.py" | sed 's/^/DIFF /' | head -12
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w4"; } > "$O/control-c1-no-mutants.txt" 2>&1
# 6 span attribution forced to line 1
M=$(mirror span); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ patched "$M" '            span = set(range(start, start + new.count("\\n") + 1))' '            span = {1}'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w5"; } > "$O/control-c1-attribution.txt" 2>&1
# 7 site records forced equal
M=$(mirror value); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ patched "$M" '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w6"; } > "$O/control-c1-value.txt" 2>&1
# 8 anchor tool edited
M=$(mirror edited); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
echo "# appended" >> "$M/plans/anchor_digest_check.py"
env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$W/w7" > "$O/control-c1-tool-edited.txt" 2>&1
# 9 direction mislabel
M=$(mirror mislabel)
{ patched "$M" "    ('U7', 'anchor', '-', 'rc-mirror', 'direct'," "    ('U7', 'anchor', '-', 'rc-silence', 'direct',"
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --battery-dir "$C/witness" --only U7 --work "$W/w9"; } \
  > "$O/control-c1-direction-mislabel.txt" 2>&1
# 10 hostile modules
for h in f1_gitfile f2_deep f3_abbrev f4_fifo f5_alternates f6_above; do
  d=$W/hb-$h; rm -rf -- "$d"; mkdir -p "$d"; cp "$C/hostile/$h.py" "$d/"
  { echo "== round-43 counter (plans/round43_c1_verify.py) --only NO5 (timeout 60)"
    env44 timeout 60 python3 "$B/plans/round43_c1_verify.py" --lane "$B" --battery-dir "$d" --only NO5 --work "$W/h43-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
    echo "== round-44 counter (plans/round44_c1_verify.py) --only U14c"
    env44 python3 "$B/plans/round44_c1_verify.py" --lane "$B" --battery-dir "$d" --only U14c --work "$W/h44-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
  } > "$O/control-c1-hostile-${h%%_*}.txt"
done
echo "REPLAY DONE"
