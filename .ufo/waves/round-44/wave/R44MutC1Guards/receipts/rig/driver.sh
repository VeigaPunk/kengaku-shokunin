#!/usr/bin/env bash
# Round-44 C1-mutant control driver (seat R44MutC1Guards): runs the committed round-44 control
# set against a given counter copy (base or M01..M15). One control per line; every run is inside
# the round-44 envelope (claims/envelope.sh). Each control uses its OWN fresh mirror (the lane
# counter copy plus anchor/order), matching c1_controls.sh semantics. Outputs: $S/out-<V>/<control>.txt.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
C=$L/.ufo/waves/round-44/claims
ENV="$C/envelope.sh"
V=$1

mkdir -p "$S/out-$V"
out() { cat > "$S/out-$V/$1.txt"; }

fresh() { # $1=control suffix -> prints a fresh mirror dir
  local m=$S/mm-$V-$1
  rm -rf "$m"; mkdir -p "$m/plans"
  cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$S/mut/$V.py" "$m/plans/"
  mv "$m/plans/$V.py" "$m/plans/round44_c1_verify.py"
  echo "$m"
}
patched() { # $1=counter file, $2=old, $3=new (mirrors c1_controls.sh)
  python3 - "$1" "$2" "$3" <<'PY' || true
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
  diff -u "$L/plans/round44_c1_verify.py" "$1" | sed 's/^/DIFF /' | head -20
}

# 1 witness (directions re-derived through the counter, development mode)
"$ENV" "$S" python3 "$S/mut/$V.py" --lane "$L" --battery-dir "$C/witness" --work "$S/w1-$V" 2>&1 | out witness

# 2 do-nothing: no plans/battery44
N=$(fresh nothing)
"$ENV" "$S" python3 "$N/plans/round44_c1_verify.py" --lane "$N" --work "$S/w2-$V" 2>&1 | out nothing
# 3 standing batteries: battery42 + battery43 copied in as battery44
B=$(fresh standing)
mkdir -p "$B/plans/battery44"
for f in "$L"/plans/battery42/*.py; do cp "$f" "$B/plans/battery44/b42_$(basename "$f")"; done
for f in "$L"/plans/battery43/*.py; do cp "$f" "$B/plans/battery44/b43_$(basename "$f")"; done
{ ls "$B/plans/battery44" | sed 's/^/MODULE /'
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w3s-$V"; } 2>&1 | out standing

# 4 witness-as-battery
B=$(fresh wab)
mkdir -p "$B/plans/battery44"; cp "$C/witness/w_u.py" "$B/plans/battery44/"
"$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w3-$V" 2>&1 | out wab

# 5 emptied mutant list
B=$(fresh nomut)
mkdir -p "$B/plans/battery44"; cp "$C/witness/w_u.py" "$B/plans/battery44/"
{ python3 - "$B/plans/round44_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i) + 3
open(p, "w").write(s[:i] + "MUTANTS = []\n" + s[j:])
PY
  diff -u "$L/plans/round44_c1_verify.py" "$B/plans/round44_c1_verify.py" | sed 's/^/DIFF /' | head -12
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w4-$V"; } 2>&1 | out nomut

# 6 span attribution forced to line 1 (leg f can fail)
B=$(fresh span)
mkdir -p "$B/plans/battery44"; cp "$C/witness/w_u.py" "$B/plans/battery44/"
{ patched "$B/plans/round44_c1_verify.py" '            span = set(range(start, start + new.count("\\n") + 1))' '            span = {1}'
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w5-$V"; } 2>&1 | out span

# 7 site records forced equal (leg g can fail)
B=$(fresh value)
mkdir -p "$B/plans/battery44"; cp "$C/witness/w_u.py" "$B/plans/battery44/"
{ patched "$B/plans/round44_c1_verify.py" '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w6-$V"; } 2>&1 | out value

# 8 one appended line in the anchor tool
B=$(fresh edited)
mkdir -p "$B/plans/battery44"; cp "$C/witness/w_u.py" "$B/plans/battery44/"
echo "# appended" >> "$B/plans/anchor_digest_check.py"
"$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --work "$S/w7-$V" 2>&1 | out edited

# 9 a carried direction mislabelled (U7 rc-mirror -> rc-silence) must survive (Q33 restore control)
B=$(fresh mislabel)
{ patched "$B/plans/round44_c1_verify.py" "    ('U7', 'anchor', '-', 'rc-mirror', 'direct'," "    ('U7', 'anchor', '-', 'rc-silence', 'direct',"
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --battery-dir "$C/witness" --only U7 --work "$S/w9-$V"; } 2>&1 | out mislabel

# 10 hostile modules f1-f6 (round-44 half only; the round-43 counter half does not run the mutated counter)
for h in f1_gitfile f2_deep f3_abbrev f4_fifo f5_alternates f6_above; do
  B=$(fresh "${h%%_*}")
  d=$S/hb-$V-$h; rm -rf "$d"; mkdir -p "$d"; cp "$C/hostile/$h.py" "$d/"
  "$ENV" "$S" python3 "$B/plans/round44_c1_verify.py" --lane "$B" --battery-dir "$d" --only U14c --work "$S/h44-$V-$h" 2>&1 \
    | grep -E '^(ENVELOPE|SETUP|FIXTURE|BATTERY|SIDECHANNEL)|escapes|breaks' | out "${h%%_*}"
done

echo "done $V"
