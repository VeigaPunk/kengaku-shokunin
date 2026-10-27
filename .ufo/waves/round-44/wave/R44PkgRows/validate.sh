#!/usr/bin/env bash
# R44PkgRows validation: census + anchor check on a scratch --shared clone of the lane with rows
# S138-S146 appended (uncommitted), plus one red control per leg.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44PkgRows
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ANCHOR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/anchor_digest_check.py
L="$S/lane"
echo "TIP $(git -C "$L" rev-parse HEAD) untracked_in_clone=$(git -C "$L" status --porcelain | wc -l)"
echo "ROWS $(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$L/corpus/SOURCES.md")"
grep -E '^\| S1(3[89]|4[0-6]) \|' "$L/corpus/SOURCES.md" > "$S/rows-landed.txt"
if cmp -s "$S/rows-landed.txt" "$S/rows.md"; then echo "DRAFT-EQUALS-LANDED yes"; else echo "DRAFT-EQUALS-LANDED NO"; fi

echo "== ROWCHECK (cell count / URL basename / verbatim quote line / word count / sha256 pin)"
python3 "$S/rowcheck.py" "$S/rows-landed.txt"; echo "ROWCHECK_exit=$?"

echo "== CENSUS green (rows appended, E11 placeholder present)"
"$CENSUS" validate --file "$L/corpus/SOURCES.md" | tail -2
"$CENSUS" validate --file "$L/corpus/SOURCES.md" >"$S/census-green.txt" 2>&1; echo "CENSUS_exit_code=$?"
echo "CENSUS W04=$(grep -c W04 "$S/census-green.txt") E-codes=$(grep -cE $'\tE[0-9]{2}\t' "$S/census-green.txt")"

echo "== CENSUS red control (used-by entry removed -> E11 must fire on S138-S146)"
P="$L/corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md"
mv "$P" "$P.away"
"$CENSUS" validate --file "$L/corpus/SOURCES.md" >"$S/census-red.txt" 2>&1; echo "CENSUS_red_exit_code=$?"
grep -cE 'E11\tS1(3[89]|4[0-6])' "$S/census-red.txt" | sed 's/^/E11_rows_fired=/'
mv "$P.away" "$P"

echo "== ANCHOR green"
python3 "$ANCHOR" --lane "$L"; echo "ANCHOR_exit=$?"
python3 "$ANCHOR" --lane "$L" --verbose >"$S/anchor-verbose.txt" 2>&1
echo "ANCHOR_BIND=$(grep -cE '^BIND S1(3[89]|4[0-6]) ' "$S/anchor-verbose.txt") ANCHOR_RESOLVED=$(grep -cE '^RESOLVED S1(3[89]|4[0-6]) ' "$S/anchor-verbose.txt")"
grep -E '^BIND S1(3[89]|4[0-6]) ' "$S/anchor-verbose.txt" | head -3

echo "== ANCHOR red control (S138 digest last nibble flipped -> one defect, named)"
M="$S/lane_mut"
rm -rf "$M"
git clone -q --shared "$L" "$M"
cp "$L/corpus/SOURCES.md" "$M/corpus/SOURCES.md"
sed -E -i 's/f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f9/f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f8/' "$M/corpus/SOURCES.md"
python3 "$ANCHOR" --lane "$M"; echo "ANCHOR_mutant_exit=$?"
rm -rf "$M"
