#!/usr/bin/env bash
# Round-43 C1 freeze controls. Every run is inside the round-43 envelope (claims/envelope.sh) and on a scratch MIRROR
# (a copy of the working tree's plans/ + the frozen witness/hostile modules); the lane is only read. Each control
# writes claims/control-c1-<name>.txt; a patched counter copy prints its `diff -u` against the frozen counter first.
#   usage: .ufo/waves/round-43/claims/c1_controls.sh            (from the lane root)
set -u
L=$PWD; C=$L/.ufo/waves/round-43/claims; R=/fast/scratch/hyaku/kengaku-r43; S=$R/L1/ctl
grep -q 'kengaku r43 round root' "$R/.ROUND-ROOT-SENTINEL" || { echo "SENTINEL MISSING"; exit 3; }
case "$S" in "$R/L1/"*) rm -rf -- "$S" ;; *) exit 3 ;; esac
mkdir -p "$S"
mirror() {  # mirror <name> -> a dir holding plans/ (tools, counters) and nothing else of the lane
  local m=$S/m-$1; mkdir -p "$m/plans"
  cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$L"/plans/round43_c1_verify.py \
     "$L"/plans/round42_c1_verify.py "$m/plans/"; echo "$m"; }
env43() { "$C/envelope.sh" "$S" "$@"; }
patched() {  # patched <mirror> <python-replace-old> <python-replace-new> : edit the mirror's counter copy, print diff
  python3 - "$1/plans/round43_c1_verify.py" "$2" "$3" <<'PY'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
  diff -u "$L/plans/round43_c1_verify.py" "$1/plans/round43_c1_verify.py" | sed 's/^/DIFF /'; }
B=$(mirror base)
# 1 witness run (directions re-derived through the counter, development mode)
env43 python3 "$L/plans/round43_c1_verify.py" --lane "$L" --battery-dir "$C/witness" --work "$S/w1" > "$C/witness-run.txt" 2>&1
# 2 do-nothing: no plans/battery43
env43 python3 "$L/plans/round43_c1_verify.py" --lane "$L" --work "$S/w2" > "$C/control-c1-nothing.txt" 2>&1
# 3 the freeze modules copied as the battery (reachable by witnessed work)
M=$(mirror wab); mkdir -p "$M/plans/battery43"; cp "$C/witness/w_near.py" "$M/plans/battery43/"
env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w3" > "$C/control-c1-witness-as-battery.txt" 2>&1
# 4 emptied mutant list
M=$(mirror nomut); mkdir -p "$M/plans/battery43"; cp "$C/witness/w_near.py" "$M/plans/battery43/"
{ python3 - "$M/plans/round43_c1_verify.py" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i) + 3
open(p, "w").write(s[:i] + "MUTANTS = []\n" + s[j:])
PY
  diff -u "$L/plans/round43_c1_verify.py" "$M/plans/round43_c1_verify.py" | sed 's/^/DIFF /' | head -12
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w4"; } > "$C/control-c1-no-mutants.txt" 2>&1
# 5 span attribution forced to line 1 (leg f can fail)
M=$(mirror span); mkdir -p "$M/plans/battery43"; cp "$C/witness/w_near.py" "$M/plans/battery43/"
{ patched "$M" '            span = set(range(start, start + new.count("\\n") + 1))' '            span = {1}'
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w5"; } > "$C/control-c1-attribution.txt" 2>&1
# 6 site records forced equal (leg g can fail)
M=$(mirror value); mkdir -p "$M/plans/battery43"; cp "$C/witness/w_near.py" "$M/plans/battery43/"
{ patched "$M" '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w6"; } > "$C/control-c1-value.txt" 2>&1
# 7 one appended line in the anchor tool
M=$(mirror edited); mkdir -p "$M/plans/battery43"; cp "$C/witness/w_near.py" "$M/plans/battery43/"
echo "# appended" >> "$M/plans/anchor_digest_check.py"
env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w7" > "$C/control-c1-tool-edited.txt" 2>&1
# 8 a relative argv token escaping d
M=$(mirror escape); mkdir -p "$M/plans/battery43"
cat > "$M/plans/battery43/esc.py" <<'PY'
def build(ctx, d):
    ctx.init(d / "repo")
    return ["--lane", "../../../../.."]


FIXTURES = [{"fid": "escape", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
PY
{ cat "$M/plans/battery43/esc.py" | sed 's/^/MODULE /'
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$S/w8"; } > "$C/control-c1-hostile-escape.txt" 2>&1
# 9 a carried direction mislabelled (NA7 rc-mirror -> rc-silence) must survive (Q33 restore control)
M=$(mirror mislabel)
{ patched "$M" "    ('NA7', 'anchor', '-', 'rc-mirror', 'direct'," "    ('NA7', 'anchor', '-', 'rc-silence', 'direct',"
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$C/witness" --only NA7 --work "$S/w9"; } \
  > "$C/control-c1-direction-mislabel.txt" 2>&1
# 10 hostile modules: round-42 counter (vector open) vs round-43 counter (vector closed), one module per run
for h in h1_gpgexec h2_builderleak h3_lanewrite h4_worktree h5_symlink h6_receipt_dir; do
  case $h in h5_*) o42=X1; o43=NA1 ;; *) o42=XO1; o43=NO5 ;; esac
  d=$S/hb-$h; mkdir -p "$d"; cp "$C/hostile/$h.py" "$d/"
  { echo "== round-42 counter (plans/round42_c1_verify.py) --only $o42"
    env43 python3 "$B/plans/round42_c1_verify.py" --lane "$B" --battery-dir "$d" --only "$o42" --work "$S/h42-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
    echo "== round-43 counter (plans/round43_c1_verify.py) --only $o43"
    env43 python3 "$B/plans/round43_c1_verify.py" --lane "$B" --battery-dir "$d" --only "$o43" --work "$S/h43-$h" 2>&1 \
      | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks'
  } > "$C/control-c1-hostile-${h%%_*}.txt"
done
rm -rf -- "$S"
grep -H -E 'PREDICATE|^MUTANTS |SETUP|escapes|FIXTURE h|SURVIVED|UNATTRIBUTED|^PINS' "$C"/control-c1-*.txt "$C/witness-run.txt"
