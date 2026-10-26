#!/usr/bin/env bash
# Round-44 C1 freeze controls (adapted from round 43's). Every run is inside the round-44 envelope (claims/envelope.sh,
# the round-43 envelope unchanged) and on a scratch MIRROR (a copy of plans/ tools + counters); the lane is only read.
# Each control writes claims/control-c1-<name>.txt; a patched counter copy prints its `diff -u` against the frozen one.
#   usage: .ufo/waves/round-44/claims/c1_controls.sh            (from the lane root)
set -u
L=$PWD; C=$L/.ufo/waves/round-44/claims; R=/fast/scratch/hyaku/kengaku-r44; S=$R/L1/ctl
grep -q 'kengaku r44 round root' "$R/.ROUND-ROOT-SENTINEL" || { echo "SENTINEL MISSING"; exit 3; }
case "$S" in "$R/L1/"*) rm -rf -- "$S" ;; *) exit 3 ;; esac
mkdir -p "$S"
mirror() {
  local m=$S/m-$1; mkdir -p "$m/plans"
  cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$L"/plans/round44_c1_verify.py \
     "$L"/plans/round43_c1_verify.py "$m/plans/"; echo "$m"; }
env44() { "$C/envelope.sh" "$S" "$@"; }
patched() {
  python3 - "$1/plans/round44_c1_verify.py" "$2" "$3" <<'PY'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
  diff -u "$L/plans/round44_c1_verify.py" "$1/plans/round44_c1_verify.py" | sed 's/^/DIFF /'; }
B=$(mirror base)
# 1 witness run (directions re-derived through the counter, development mode)
env44 python3 "$L/plans/round44_c1_verify.py" --lane "$L" --battery-dir "$C/witness" --work "$S/w1" > "$C/witness-run.txt" 2>&1
# 2 do-nothing: no plans/battery44
env44 python3 "$L/plans/round44_c1_verify.py" --lane "$L" --work "$S/w2" > "$C/control-c1-nothing.txt" 2>&1
# 3 standing batteries: battery42 + battery43 copied in as battery44 (what the lane already demonstrates)
M=$(mirror standing); mkdir -p "$M/plans/battery44"
for f in "$L"/plans/battery42/*.py; do cp "$f" "$M/plans/battery44/b42_$(basename "$f")"; done
for f in "$L"/plans/battery43/*.py; do cp "$f" "$M/plans/battery44/b43_$(basename "$f")"; done
{ ls "$M/plans/battery44" | sed 's/^/MODULE /'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w3s"; } > "$C/control-c1-standing-batteries.txt" 2>&1
# 4 the freeze module copied as the battery (reachable by witnessed work)
M=$(mirror wab); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w3" > "$C/control-c1-witness-as-battery.txt" 2>&1
# 5 emptied mutant list
M=$(mirror nomut); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ python3 - "$M/plans/round44_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i) + 3
open(p, "w").write(s[:i] + "MUTANTS = []\n" + s[j:])
PY
  diff -u "$L/plans/round44_c1_verify.py" "$M/plans/round44_c1_verify.py" | sed 's/^/DIFF /' | head -12
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w4"; } > "$C/control-c1-no-mutants.txt" 2>&1
# 6 span attribution forced to line 1 (leg f can fail)
M=$(mirror span); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ patched "$M" '            span = set(range(start, start + new.count("\\n") + 1))' '            span = {1}'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w5"; } > "$C/control-c1-attribution.txt" 2>&1
# 7 site records forced equal (leg g can fail)
M=$(mirror value); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
{ patched "$M" '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w6"; } > "$C/control-c1-value.txt" 2>&1
# 8 one appended line in the anchor tool
M=$(mirror edited); mkdir -p "$M/plans/battery44"; cp "$C/witness/w_u.py" "$M/plans/battery44/"
echo "# appended" >> "$M/plans/anchor_digest_check.py"
env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --work "$S/w7" > "$C/control-c1-tool-edited.txt" 2>&1
# 9 a carried direction mislabelled (U7 rc-mirror -> rc-silence) must survive (Q33 restore control)
M=$(mirror mislabel)
{ patched "$M" "    ('U7', 'anchor', '-', 'rc-mirror', 'direct'," "    ('U7', 'anchor', '-', 'rc-silence', 'direct',"
  env44 python3 "$M/plans/round44_c1_verify.py" --lane "$M" --battery-dir "$C/witness" --only U7 --work "$S/w9"; } \
  > "$C/control-c1-direction-mislabel.txt" 2>&1
# 10 hostile modules: round-43 counter (vector open) vs round-44 counter (vector closed), one module per run
for h in f1_gitfile f2_deep f3_abbrev f4_fifo f5_alternates f6_above; do
  d=$S/hb-$h; mkdir -p "$d"; cp "$C/hostile/$h.py" "$d/"
  { echo "== round-43 counter (plans/round43_c1_verify.py) --only NO5 (timeout 60)"
    env44 timeout 60 python3 "$B/plans/round43_c1_verify.py" --lane "$B" --battery-dir "$d" --only NO5 --work "$S/h43-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
    echo "== round-44 counter (plans/round44_c1_verify.py) --only U14c"
    env44 python3 "$B/plans/round44_c1_verify.py" --lane "$B" --battery-dir "$d" --only U14c --work "$S/h44-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
  } > "$C/control-c1-hostile-${h%%_*}.txt"
done
