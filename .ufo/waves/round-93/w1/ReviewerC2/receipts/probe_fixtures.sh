#!/bin/bash
# Throwaway fixtures for R93-C2 gate edge probes. Every git call uses -C and an explicit identity.
set -u
S=/fast/scratch/hyaku/kengaku-r93/ReviewerC2
GATE=$S/zgate_T.py
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null"
new_repo() { # $1 name -> prints dir
  local d=$S/fx/$1; rm -rf "$d"; mkdir -p "$d"; git -C "$d" init -q -b main
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo "TOPLEVEL MISMATCH $d" >&2; exit 9; }
  echo "$d"; }
commit() { git -C "$1" add -A && git -C "$1" $ID commit -q --allow-empty -m "$2" && git -C "$1" rev-parse HEAD; }
gate() { python3 -I -B "$GATE" --lane "$1" --freeze "$2" --rev "$3" --claims "$4" --work "$S/fx/work-$5" 2>&1 | grep -E '^(INSTRUMENT|FREEZE-INTEGRITY|PREDICATE|DEFECT|BATTERY .* RED)'; echo "rc=${PIPESTATUS[0]}"; }
sha() { sha256sum "$1" | cut -d' ' -f1; }

echo "##### T1 second frozen-instruments block (valid rows, after a closed first block)"
d=$(new_repo t1); printf 'a\n' > $d/a.py; printf 'b\n' > $d/b.py
ha=$(sha $d/a.py); hb=$(sha $d/b.py)
printf '# claims\n\n```frozen-instruments\n%s  a.py\n```\n\nprose\n\n```frozen-instruments\n%s  b.py\n```\n' "$ha" "$hb" > $d/claims.md
f=$(commit $d "freeze"); printf 'B-EDITED\n' > $d/b.py; t=$(commit $d "edit b")
echo "b.py (second block) edited after freeze; expect broken on b.py:"; gate $d $f $t claims.md t1

echo "##### T2 duplicate rows of one intact path (count inflation vs MIN_SELF_INSTRUMENTS=6)"
d=$(new_repo t2); printf 'a\n' > $d/a.py; ha=$(sha $d/a.py)
{ echo '```frozen-instruments'; for i in 1 2 3 4 5 6 7 8; do echo "$ha  a.py"; done; echo '```'; } > $d/claims.md
f=$(commit $d "freeze"); t=$(commit $d "later")
echo "eight duplicate rows, one file, no edits; expect instruments=8 intact=8 (W4 needs >=6):"; gate $d $f $t claims.md t2

echo "##### T3 glob-metacharacter path edited then reverted (pathspec magic in rev-list -- PATH)"
d=$(new_repo t3); printf 'orig\n' > "$d/probe[1].py"; hp=$(sha "$d/probe[1].py")
printf '```frozen-instruments\n%s  probe[1].py\n```\n' "$hp" > $d/claims.md
f=$(commit $d "freeze"); printf 'edited\n' > "$d/probe[1].py"; commit $d "edit" >/dev/null
printf 'orig\n' > "$d/probe[1].py"; t=$(commit $d "revert")
echo "probe[1].py edited then reverted; a true edit-then-revert must be broken+touched>=2:"; gate $d $f $t claims.md t3
echo "raw touched count via rev-list (default pathspec) vs literal:"
echo "  default: $(git -C $d rev-list $f..$t -- 'probe[1].py' | wc -l)   literal: $(git -C $d rev-list $f..$t --literal-pathspecs -- 'probe[1].py' | wc -l)"

echo "##### T4 merge topology: feature edits instrument, merge resolves back to parent-1 bytes"
d=$(new_repo t4); printf 'orig\n' > $d/c.py; printf '```frozen-instruments\n%s  c.py\n```\n' "$(sha $d/c.py)" > $d/claims.md
f=$(commit $d "freeze")
git -C $d $ID checkout -q -b feat; printf 'feature-edit\n' > $d/c.py; commit $d "feat edits c.py" >/dev/null
git -C $d checkout -q main; printf 'main-unrelated\n' > $d/other.txt; commit $d "main unrelated" >/dev/null
git -C $d $ID merge -q --no-ff -X ours feat -m "merge feat keeping main bytes" >/dev/null 2>&1 || true
printf 'orig\n' > $d/c.py; t=$(commit $d "merge result restores orig bytes")
echo "merge commits in f..t: $(git -C $d rev-list --merges $f..$t | wc -l)"
echo "default rev-list -- c.py: $(git -C $d rev-list $f..$t -- c.py | wc -l)   --full-history: $(git -C $d rev-list --full-history $f..$t -- c.py | wc -l)   feature commit present in f..t: $(git -C $d rev-list $f..$t | wc -l) total commits"
gate $d $f $t claims.md t4

echo "##### T5 path containing spaces (regex \\S+ rejects)"
d=$(new_repo t5); mkdir -p "$d/my dir"; printf 'x\n' > "$d/my dir/c.py"; printf '```frozen-instruments\n%s  my dir/c.py\n```\n' "$(sha "$d/my dir/c.py")" > $d/claims.md
f=$(commit $d "freeze"); t=$(commit $d "later")
gate $d $f $t claims.md t5

echo "##### T6 mode-only change (chmod +x), bytes identical"
d=$(new_repo t6); printf 'x\n' > $d/c.py; printf '```frozen-instruments\n%s  c.py\n```\n' "$(sha $d/c.py)" > $d/claims.md
f=$(commit $d "freeze"); chmod +x $d/c.py; t=$(commit $d "chmod")
gate $d $f $t claims.md t6
