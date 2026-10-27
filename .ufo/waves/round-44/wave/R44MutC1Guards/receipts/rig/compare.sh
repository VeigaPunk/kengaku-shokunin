#!/usr/bin/env bash
# Normalize + compare control outputs: base vs a mutant variant.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
V=$1

norm() { # $1=file; prints normalized lines
  sed -E \
    -e '/^ENVELOPE /d' \
    -e '/^DIFF /d' \
    -e "s|$L|LANE|g" \
    -e "s|$S|SCR|g" \
    -e 's|k44-c1-[A-Za-z0-9_]+|k44-c1-X|g' \
    -e 's#mm-[A-Za-z0-9]+-(f[1-6]|wab|standing|nomut|span|value|edited|mislabel|nothing)#mm-V-\1#g' \
    -e 's#h44-[A-Za-z0-9]+-f([1-6])_[a-z]+#h44-V-f\1#g' \
    -e 's#hb-[A-Za-z0-9]+-f([1-6])_[a-z]+#hb-V-f\1#g' \
    "$1"
}

echo "== $V vs base =="
changed=0
for c in witness nothing standing wab nomut span value edited mislabel f1 f2 f3 f4 f5 f6; do
  a=$S/out-base/$c.txt; b=$S/out-$V/$c.txt
  if [ ! -f "$a" ]; then echo "MISSING base $c"; continue; fi
  if [ ! -f "$b" ]; then echo "MISSING $V $c"; continue; fi
  if diff <(norm "$a") <(norm "$b") > "$S/tmp-diff-$$" 2>&1; then
    echo "$c: unchanged"
  else
    changed=1
    echo "$c: CHANGED"
    head -20 "$S/tmp-diff-$$" | sed 's/^/    /'
  fi
done
rm -f "$S/tmp-diff-$$"
[ "$changed" = 0 ] && echo "VERDICT: survived" || echo "VERDICT: caught"
