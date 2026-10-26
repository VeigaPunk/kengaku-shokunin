#!/usr/bin/env bash
# R43MutC1Counter: run the round-43 C1 freeze controls against ONE counter copy.
# Reproduces .ufo/waves/round-43/claims/c1_controls.sh on the seat clone, with:
#   - the counter under test is $1 (a scratch copy; the lane's own counter is never run mutated),
#   - outputs go to $2 instead of the frozen claims dir,
#   - the round-42 "vector open" halves of the hostile controls are not re-run here (they do not
#     involve the counter under test; the frozen control-*.txt receipts carry them).
# usage: driver.sh <counter-copy> <outdir> [control ...]   (default: all)
set -u
CNT=$(readlink -f "$1"); OUT=$(readlink -f "$2"); shift 2 || true; mkdir -p "$OUT"
L=/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter/lane
LC=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims
S=/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter
W=$S/md; rm -rf "$W"; mkdir -p "$W"
sha256sum "$CNT" | sed 's#  .*/#  #' > "$OUT/COUNTER.sha256"
env43() { "$LC/envelope.sh" "$W" "$@"; }
SEL=" ${*:-witness nothing wab nomut span value edited escape mislabel h1 h2 h3 h4 h5 h6} "
has() { case "$SEL" in *" $1 "*) return 0 ;; esac; return 1; }
mirror() { M=$W/m-$1; mkdir -p "$M/plans"; cp "$CNT" "$M/plans/round43_c1_verify.py"; cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$L"/plans/round42_c1_verify.py "$M/plans/"; }
patched() { python3 - "$M/plans/round43_c1_verify.py" "$1" "$2" <<'PY'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("patch anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
}
if has witness; then env43 python3 "$CNT" --lane "$L" --battery-dir "$LC/witness" --work "$W/w1" > "$OUT/witness.txt" 2>&1; echo "witness rc=$?"; fi
if has nothing; then env43 python3 "$CNT" --lane "$L" --work "$W/w2" > "$OUT/nothing.txt" 2>&1; echo "nothing rc=$?"; fi
if has wab; then mirror wab; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w3" > "$OUT/wab.txt" 2>&1; echo "wab rc=$?"; fi
if has nomut; then mirror nomut; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  { python3 - "$M/plans/round43_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i) + 3
open(p, "w").write(s[:i] + "MUTANTS = []\n" + s[j:])
PY
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w4"; } > "$OUT/nomut.txt" 2>&1; echo "nomut rc=$?"; fi
if has span; then mirror span; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  { patched '            span = set(range(start, start + new.count("\\n") + 1))' '            span = {1}'
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w5"; } > "$OUT/span.txt" 2>&1; echo "span rc=$?"; fi
if has value; then mirror value; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  { patched '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w6"; } > "$OUT/value.txt" 2>&1; echo "value rc=$?"; fi
if has edited; then mirror edited; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  echo "# appended" >> "$M/plans/anchor_digest_check.py"
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w7" > "$OUT/edited.txt" 2>&1; echo "edited rc=$?"; fi
if has escape; then mirror escape; mkdir -p "$M/plans/battery43"
  cat > "$M/plans/battery43/esc.py" <<'PY'
def build(ctx, d):
    ctx.init(d / "repo")
    return ["--lane", "../../../../.."]


FIXTURES = [{"fid": "escape", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
PY
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/w8" > "$OUT/escape.txt" 2>&1; echo "escape rc=$?"; fi
if has mislabel; then mirror mislabel
  { patched "    ('NA7', 'anchor', '-', 'rc-mirror', 'direct'," "    ('NA7', 'anchor', '-', 'rc-silence', 'direct',"
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --only NA7 --work "$W/w9"; } > "$OUT/mislabel.txt" 2>&1; echo "mislabel rc=$?"; fi
mirror base
for h in h1_gpgexec h2_builderleak h3_lanewrite h4_worktree h5_symlink h6_receipt_dir; do
  n=${h%%_*}; has $n || continue
  case $h in h5_*) o43=NA1 ;; *) o43=NO5 ;; esac
  d=$W/hb-$h; mkdir -p "$d"; cp "$LC/hostile/$h.py" "$d/"
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$d" --only "$o43" --work "$W/h43-$h" > "$OUT/$n.txt" 2>&1
  echo "$n rc=$?"
done
echo "driver done: $OUT"
