#!/bin/bash
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims
HONEST=$S/lane/plans/round94_freeze_integrity.py
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false"
mkfx() { D=$1; rm -rf "$D"; mkdir -p "$D"; git -C "$D" init -q -b main; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo TOPLEVEL-MISMATCH; exit 1; }; }
run() { # label gate-file lane freeze rev extra-args...
  label=$1; gate=$2; lane=$3; f=$4; t=$5; shift 5
  out=$(python3 -I -B "$gate" --lane "$lane" --freeze "$f" --rev "$t" "$@" --work "$S/ho/vw-$label-$(basename $gate .py)" 2>&1); rc=$?
  echo "  [$label] gate=$(basename $gate .py) rc=$rc $(echo "$out" | grep -E '^(INSTRUMENT|PREDICATE|DEFECT)' | tr '\n' ' ')"
}
# ---- A: live row plus a commented-out row for a breached instrument (claims mode)
D=$S/ho/fxA; mkfx $D
printf 'def count():\n    return 3\n' > $D/probe.py; printf 'notes\n' > $D/notes.md
SP=$(sha256sum $D/probe.py|cut -d' ' -f1); SN=$(sha256sum $D/notes.md|cut -d' ' -f1)
printf '```frozen-instruments\n%s  probe.py\n# %s  notes.md\n```\n' "$SP" "$SN" > $D/claims.md
git -C $D add -A && git -C $D $ID commit -q -m freeze; F=$(git -C $D rev-parse HEAD)
printf 'edited\n' > $D/notes.md; git -C $D add -A && git -C $D $ID commit -q -m edit; T=$(git -C $D rev-parse HEAD)
echo "A: notes.md (commented row) edited after freeze"
run A $HONEST $D $F $T --claims claims.md
run A $S/ho/HO-A-comment-row-skipped.py $D $F $T --claims claims.md
# ---- B: paths mode, edit then revert
D=$S/ho/fxB; mkfx $D
printf 'def count():\n    return 3\n' > $D/probe.py
git -C $D add -A && git -C $D $ID commit -q -m freeze; F=$(git -C $D rev-parse HEAD)
printf 'def count():\n    return 4\n' > $D/probe.py; git -C $D add -A && git -C $D $ID commit -q -m edit
printf 'def count():\n    return 3\n' > $D/probe.py; git -C $D add -A && git -C $D $ID commit -q -m revert; T=$(git -C $D rev-parse HEAD)
echo "B: paths mode probe.py edited then reverted (bytes at rev == freeze bytes)"
run B $HONEST $D $F $T --paths probe.py
run B $S/ho/HO-B-paths-mode-no-history.py $D $F $T --paths probe.py
# ---- C: claims mode, edit-then-revert then 60 unrelated commits (window forgery)
D=$S/ho/fxC; mkfx $D
printf 'def count():\n    return 3\n' > $D/probe.py; printf 'notes\n' > $D/notes.md
SP=$(sha256sum $D/probe.py|cut -d' ' -f1)
printf '```frozen-instruments\n%s  probe.py\n```\n' "$SP" > $D/claims.md
git -C $D add -A && git -C $D $ID commit -q -m freeze; F=$(git -C $D rev-parse HEAD)
printf 'def count():\n    return 4\n' > $D/probe.py; git -C $D add -A && git -C $D $ID commit -q -m edit
printf 'def count():\n    return 3\n' > $D/probe.py; git -C $D add -A && git -C $D $ID commit -q -m revert
for i in $(seq 1 60); do echo $i > $D/notes.md; git -C $D add -A && git -C $D $ID commit -q -m "unrelated $i"; done; T=$(git -C $D rev-parse HEAD)
echo "C: edit-then-revert, then 60 unrelated commits (claims mode)"
run C $HONEST $D $F $T --claims claims.md
run C $S/ho/HO-C-history-window-50.py $D $F $T --claims claims.md
