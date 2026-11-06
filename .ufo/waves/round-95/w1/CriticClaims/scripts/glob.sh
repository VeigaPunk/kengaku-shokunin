#!/bin/bash
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims
GATE=$S/lane/plans/round94_freeze_integrity.py
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false"
for NAME in probe1.py 'probe[1].py'; do
  D=$S/ho/glob-$(echo "$NAME" | tr -d '[].')
  rm -rf "$D"; mkdir -p "$D"; git -C "$D" init -q -b main
  test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "TOPLEVEL MISMATCH"; exit 1; }
  printf 'def count():\n    return 3\n' > "$D/$NAME"
  SHA=$(sha256sum "$D/$NAME" | cut -d' ' -f1)
  printf '```frozen-instruments\n%s  %s\n```\n' "$SHA" "$NAME" > "$D/claims.md"
  git -C "$D" add -A && git -C "$D" $ID commit -q -m freeze
  F=$(git -C "$D" rev-parse HEAD)
  printf 'def count():\n    return 4\n' > "$D/$NAME"; git -C "$D" add -A && git -C "$D" $ID commit -q -m edit
  printf 'def count():\n    return 3\n' > "$D/$NAME"; git -C "$D" add -A && git -C "$D" $ID commit -q -m revert
  T=$(git -C "$D" rev-parse HEAD)
  echo "== NAME=$NAME (edit then revert; bytes at rev == table)"
  python3 -I -B "$GATE" --lane "$D" --freeze "$F" --rev "$T" --claims claims.md --work "$S/ho/glob-w-$(echo "$NAME" | tr -d '[].')" | grep -E "INSTRUMENT|FREEZE-INTEGRITY|PREDICATE"; echo "rc=${PIPESTATUS[0]}"
  echo "-- git rev-list count for pathspec:"; git -C "$D" rev-list --full-history "$F..$T" -- "$NAME" | wc -l
done
