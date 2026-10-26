#!/usr/bin/env bash
# Round-37 freeze controls: run every frozen counter on a clean clone of the freeze candidate (lane HEAD plus
# the uncommitted freeze files staged index-only in the scratch clone). Writes receipts beside this script.
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
W=$L/.ufo/waves/round-37/claims
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r37/L1/controls
rm -rf "$S"; mkdir -p "$S"; export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
FILES="plans/round37_c1_verify.py plans/round37_c2_verify.py plans/git_webserver_probe.py plans/pkg-spec-r37.json corpus/evidence/round37"
mk() {  # mk NAME -> clone at $S/NAME/lane
  local D="$S/$1"; mkdir -p "$D"
  git clone -q --shared "$L" "$D/lane"
  [ "$(git -C "$D/lane" rev-parse --show-toplevel)" = "$D/lane" ] || { echo "bad clone"; exit 2; }
  for f in $FILES; do mkdir -p "$D/lane/$(dirname "$f")"; cp -r "$L/$f" "$D/lane/$(dirname "$f")/"; done
  git -C "$D/lane" add -A
  echo "$D/lane"
}
run() {  # run RECEIPT DIR CMD...
  local out=$1 dir=$2; shift 2
  { echo "\$ (clone of $(git -C "$L" rev-parse HEAD) + freeze files) $*"; (cd "$dir" && "$@"); echo "exit=$?"; } > "$W/$out" 2>&1
  tail -3 "$W/$out"
}
C=$(mk c1-nothing);  run control-c1-nothing.txt "$C" python3 plans/round37_c1_verify.py --lane .
C=$(mk c1-gate);     echo "# one appended byte line" >> "$C/plans/pkg_gate.py"; git -C "$C" add -A
                     run control-c1-gate-edited.txt "$C" python3 plans/round37_c1_verify.py --lane .
C=$(mk c1-mislabel); mkdir -p "$C/plans/battery37"; cp "$W/mislabel_battery/mislabel.py" "$C/plans/battery37/"; git -C "$C" add -A
                     run control-c1-mislabel.txt "$C" python3 plans/round37_c1_verify.py --lane .
C=$(mk c1-example);  mkdir -p "$C/plans/battery37"; cp "$W/example_battery/ex_p3_words.py" "$C/plans/battery37/"; git -C "$C" add -A
                     run control-c1-example.txt "$C" python3 plans/round37_c1_verify.py --lane .
C=$(mk c2-nothing);  run control-c2-nothing.txt "$C" python3 plans/round37_c2_verify.py --lane .
C=$(mk c2-skip);     python3 "$W/make_c2_skip.py" "$C"; git -C "$C" add -A
                     run control-c2-skip.txt "$C" python3 plans/round37_c2_verify.py --lane .
