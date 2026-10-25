#!/bin/bash
# Round-36 freeze controls. Builds a sparse shared clone of the lane's committed master in a mktemp
# dir, copies the not-yet-committed round-36 files in, and records each control's output.
# Usage: make-controls.sh <lane> <out-dir>
set -u
L=$1; O=$2; mkdir -p "$O"
D=$(mktemp -d /tmp/k36-ctl-XXXX)
git clone -q --no-checkout --shared "$L" "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build
git -C "$D/lane" checkout -q master
[ "$(git -C "$D/lane" rev-parse --show-toplevel)" = "$D/lane" ] || { echo "bad fixture root"; exit 9; }
for p in plans/regex_log_probe.py plans/round36_c1_verify.py plans/round36_c2_verify.py plans/pkg-spec-r35.json corpus/defects-round35.jsonl; do
  cp "$L/$p" "$D/lane/$p"
done
mkdir -p "$D/lane/corpus/evidence/round36" && cp -r "$L/corpus/evidence/round36/." "$D/lane/corpus/evidence/round36/"
cd "$D/lane"
run() { name=$1; shift; { echo "# control $name — $*"; "$@"; echo "exit=$?"; } > "$O/$name.txt" 2>&1; }
run control-c1-nothing python3 plans/round36_c1_verify.py --lane .
run control-c1-legacy python3 plans/round36_c1_verify.py --lane . --legacy
printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' > plans/pkg_gate.py
run control-c1-accept-all python3 plans/round36_c1_verify.py --lane .
printf '#!/usr/bin/env python3\nimport sys\nsys.exit(1)\n' > plans/pkg_gate.py
run control-c1-reject-all python3 plans/round36_c1_verify.py --lane .
rm plans/pkg_gate.py
run control-c2-nothing python3 plans/round36_c2_verify.py --lane .
python3 "$L/.ufo/waves/round-36/claims/make_c2_skip.py" "$D/lane"
run control-c2-skip python3 plans/round36_c2_verify.py --lane .
echo "clone=$D/lane" >&2
rm -rf "$D"
