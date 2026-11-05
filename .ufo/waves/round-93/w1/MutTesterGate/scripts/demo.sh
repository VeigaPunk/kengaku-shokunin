#!/usr/bin/env bash
# Throwaway fixture demonstrations (never the lane). Each fixture: git init, explicit -C,
# throwaway identity, toplevel asserted before the first commit.
set -u
S=/fast/scratch/hyaku/kengaku-r93/MutTesterGate
W=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-93/w1/MutTesterGate
GATE=$S/lane/plans/round93_freeze_integrity.py
M13=$W/mutants/m13-table-read-at-rev.py
M06=$W/mutants/m06-cne-exit0-pass.py
ID=(-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false)

mkfx() { # $1 dir
  rm -rf -- "$1"; mkdir -p -- "$1"; git -C "$1" init -q
  top=$(git -C "$1" rev-parse --show-toplevel); [ "$top" = "$(realpath "$1")" ] || { echo "TOPLEVEL MISMATCH $top"; exit 9; }
}
commit() { git -C "$1" "${ID[@]}" add -A && git -C "$1" "${ID[@]}" commit -q --allow-empty -m "$2" && git -C "$1" rev-parse HEAD; }

echo "### DEMO A: claims table repaired after freeze (lying table at freeze, correct table at rev); c.py untouched"
D=$S/demoA; mkfx "$D"; printf "print('counter')\n" > "$D/c.py"
printf '# claims\n\n```frozen-instruments\n%s  c.py\n```\n' "$(printf 'f%.0s' $(seq 64))" > "$D/claims.md"
F=$(commit "$D" freeze)
printf '# claims\n\n```frozen-instruments\n%s  c.py\n```\n' "$(printf "print('counter')\n" | sha256sum | cut -c1-64)" > "$D/claims.md"
R=$(commit "$D" "repair table")
for tool in "$GATE" "$M13"; do
  echo "-- tool=$(basename "$tool") freeze=${F:0:12} rev=${R:0:12}"
  python3 "$tool" --lane "$D" --freeze "$F" --rev "$R" --claims claims.md --work "$S/demoA-w-$(basename "$tool" .py)" | grep -E '^(INSTRUMENT|FREEZE-INTEGRITY|PREDICATE)'; echo "rc=${PIPESTATUS[0]}"
done

echo "### DEMO B: claims file absent at freeze (could-not-evaluate) -> real gate vs m06"
B=$S/demoB; mkfx "$B"; printf "print('counter')\n" > "$B/c.py"; printf 'no table\n' > "$B/claims.md"; F=$(commit "$B" freeze)
printf 'x\n' > "$B/other.txt"; R=$(commit "$B" later)
for tool in "$GATE" "$M06"; do
  echo "-- tool=$(basename "$tool")"
  python3 "$tool" --lane "$B" --freeze "$F" --rev "$R" --claims absent.md --work "$S/demoB-w-$(basename "$tool" .py)" | grep -E '^(DEFECT|PREDICATE)'; echo "rc=${PIPESTATUS[0]}"
done

echo "### DEMO C: side-branch edit discarded by a merge (-s ours); touched check vs. history simplification"
C=$S/demoC; mkfx "$C"; printf "A\n" > "$C/c.py"; printf "frozen table\n" > "$C/claims.md"
printf '```frozen-instruments\n%s  c.py\n```\n' "$(printf 'A\n' | sha256sum | cut -c1-64)" >> "$C/claims.md"
F=$(commit "$C" freeze)
git -C "$C" checkout -q -b side
printf "B\n" > "$C/c.py"; S1=$(commit "$C" side-edit)
git -C "$C" checkout -q -
git -C "$C" "${ID[@]}" checkout -q -b main-line 2>/dev/null || true
printf "x\n" > "$C/other.txt"; commit "$C" mainline >/dev/null
git -C "$C" "${ID[@]}" merge -q -s ours --no-edit side >/dev/null && M=$(git -C "$C" rev-parse HEAD)
echo "-- freeze=${F:0:12} side-edit=${S1:0:12} merge=${M:0:12}"
echo "-- c.py at merge: $(git -C "$C" show "$M:c.py" | tr -d '\n')"
echo "-- rev-list F..M -- c.py (default):"; git -C "$C" rev-list "$F..$M" -- c.py | sed 's/^/   /'; echo "   count=$(git -C "$C" rev-list "$F..$M" -- c.py | wc -l)"
echo "-- rev-list --full-history F..M -- c.py:"; git -C "$C" rev-list --full-history "$F..$M" -- c.py | sed 's/^/   /'
echo "-- gate at merge:"
python3 "$GATE" --lane "$C" --freeze "$F" --rev "$M" --claims claims.md --work "$S/demoC-w" | grep -E '^(INSTRUMENT|FREEZE-INTEGRITY|PREDICATE)'; echo "rc=${PIPESTATUS[0]}"
echo "### merges in lane windows (verdict relevance check)"
echo "-- W1 f0018773..1df76536 merges: $(git -C "$S/lane" rev-list --merges f0018773f507f363854123856990f8ff8a87eb8c..1df7653633bd4c5a5f373d139f9f1ed02e0f9c07 | wc -l)"
echo "-- W4 d8d0a4b8..T merges: $(git -C "$S/lane" rev-list --merges d8d0a4b849f3 22972a317185216596b3dfe1c189e98d1eb86787 2>/dev/null | wc -l)"
