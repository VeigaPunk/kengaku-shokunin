#!/bin/bash
set -u
S=/fast/scratch/hyaku/kengaku-r93/ReviewerC2
GATE=$S/zgate_T.py
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null"
sha() { sha256sum "$1" | cut -d' ' -f1; }
d=$S/fx/t4b; rm -rf "$d"; mkdir -p "$d"; git -C "$d" init -q -b main
[ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo MISMATCH; exit 9; }
printf 'orig\n' > $d/c.py; printf 'main\n' > $d/other.txt
printf '```frozen-instruments\n%s  c.py\n```\n' "$(sha $d/c.py)" > $d/claims.md
git -C $d add -A && git -C $d $ID commit -q -m freeze; f=$(git -C $d rev-parse HEAD)
git -C $d $ID checkout -q -b feat; printf 'feature-edit\n' > $d/c.py; git -C $d add -A && git -C $d $ID commit -q -m "feat edits c.py"
git -C $d checkout -q main; printf 'main-unrelated\n' > $d/other.txt; git -C $d add -A && git -C $d $ID commit -q -m "main unrelated"
git -C $d $ID merge -q --no-commit --no-ff feat >/dev/null 2>&1
git -C $d checkout -q HEAD -- c.py          # resolve c.py to main's bytes => merge TREESAME to parent 1
git -C $d add -A && git -C $d $ID commit -q -m "merge; c.py resolved to main bytes"; t=$(git -C $d rev-parse HEAD)
echo "c.py bytes at T: $(git -C $d show $t:c.py | tr -d '\n')  merges in f..t: $(git -C $d rev-list --merges $f..$t | wc -l)"
echo "touched default: $(git -C $d rev-list $f..$t -- c.py | wc -l)  --full-history: $(git -C $d rev-list --full-history $f..$t -- c.py | wc -l)"
echo "--- counter-style gate run (default rev-list) ---"
python3 -I -B "$GATE" --lane "$d" --freeze "$f" --rev "$t" --claims claims.md --work "$S/fx/work-t4b" 2>&1 | grep -E '^(INSTRUMENT|FREEZE-INTEGRITY|PREDICATE|DEFECT)'; echo "rc=${PIPESTATUS[0]}"
echo "--- literal pathspec sanity (git option before subcommand) ---"
d2=$S/fx/t3b; rm -rf "$d2"; mkdir -p "$d2"; git -C "$d2" init -q -b main; printf 'orig\n' > "$d2/probe[1].py"; printf 'z\n' > "$d2/probe1.py"
git -C $d2 add -A && git -C $d2 $ID commit -q -m freeze; f2=$(git -C $d2 rev-parse HEAD)
printf 'edited\n' > "$d2/probe[1].py"; git -C $d2 add -A && git -C $d2 $ID commit -q -m edit
printf 'orig\n' > "$d2/probe[1].py"; git -C $d2 add -A && git -C $d2 $ID commit -q -m revert; t2=$(git -C $d2 rev-parse HEAD)
echo "default glob-pathspec touched: $(git -C $d2 rev-list $f2..$t2 -- 'probe[1].py' | wc -l)   literal: $(git -C $d2 --literal-pathspecs rev-list $f2..$t2 -- 'probe[1].py' | wc -l)"
echo "--- census of claims files and tables in lane history ---"
L=$S/lane
git -C $L log --all --diff-filter=A --format='%h %ad %s' --date=short -- 'plans/round-*-claims.md' 'plans/round*-claims.md' | head -20
echo "--- historical frozen-instruments blocks in repo (any commit) ---"
git -C $L log --all --format=%h -S'```frozen-instruments' -- plans corpus | head -20
echo "--- round-numbered freeze/gate files at T ---"
git -C $L ls-tree -r --name-only 22972a317185216596b3dfe1c189e98d1eb86787 -- plans | grep -E 'freeze|gate|counter|burndown|replay|conformance|pin' | sort
