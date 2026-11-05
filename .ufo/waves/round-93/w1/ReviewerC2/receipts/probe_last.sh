#!/bin/bash
set -u
S=/fast/scratch/hyaku/kengaku-r93/ReviewerC2; L=$S/lane; F=d8d0a4b849f3d031a6ad5525e18611a097e08bfe; T=22972a317185216596b3dfe1c189e98d1eb86787
echo "--- frozen-instruments opener count in claims at F: $(git -C $L show $F:plans/round-93-claims.md | grep -c '^```frozen-instruments')"
echo "--- CR bytes or trailing spaces in table block at F: $(git -C $L show $F:plans/round-93-claims.md | sed -n '/^```frozen-instruments/,/^```$/p' | grep -c $'\r\|  $')"
echo "--- merges in F..T: $(git -C $L rev-list --merges $F..$T | wc -l)  commits F..T: $(git -C $L rev-list $F..$T | wc -l)"
echo "--- claims blob F==T: $([ "$(git -C $L rev-parse $F:plans/round-93-claims.md)" = "$(git -C $L rev-parse $T:plans/round-93-claims.md)" ] && echo yes)"
echo "--- W4 selector list (newest first) at T: $(git -C $L log --diff-filter=A --format=%h $T -- plans/round-93-claims.md | tr '\n' ' ')"
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null"
d=$S/fx/t7; rm -rf "$d"; mkdir -p "$d"; git -C "$d" init -q -b main
[ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo MISMATCH; exit 9; }
printf 'orig\n' > $d/c.py; printf '```frozen-instruments\n%s  c.py\n```\n' "$(sha256sum $d/c.py | cut -d' ' -f1)" > $d/claims.md
git -C $d add -A && git -C $d $ID commit -q -m freeze; f=$(git -C $d rev-parse HEAD)
printf 'edited\n' > $d/c.py; printf '```frozen-instruments\n%s  c.py\n```\n' "$(sha256sum $d/c.py | cut -d' ' -f1)" > $d/claims.md
git -C $d add -A && git -C $d $ID commit -q -m "edit instrument and rewrite table after freeze"; t=$(git -C $d rev-parse HEAD)
echo "--- real gate: table rewritten after freeze to match edited bytes (expect broken) ---"
python3 -I -B $S/zgate_T.py --lane $d --freeze $f --rev $t --claims claims.md --work $S/fx/work-t7 2>&1 | grep -E '^(INSTRUMENT|PREDICATE)'; echo "rc=${PIPESTATUS[0]}"
