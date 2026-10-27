#!/usr/bin/env bash
# R45PkgRows control receipts: E12 (rows outside ## Registry), capture manifest, gitignore has no graded role.
set -u
S=/fast/scratch/hyaku/kengaku-r45/R45PkgRows
LANE=$S/lane
REP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w1/R45PkgRows
ROWS=$REP/rows-S149-S156.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
CAPDIR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round45/tb2-password-recovery

echo "TIP $(git -C "$LANE" rev-parse HEAD)"
echo "== E12 red control (the same eight rows appended at EOF instead of after the last Registry row)"
mkdir -p "$S/e12/corpus/knowledge"
git -C "$LANE" show HEAD:corpus/SOURCES.md > "$S/e12/corpus/SOURCES.md"
cat "$ROWS" >> "$S/e12/corpus/SOURCES.md"
printf '%s\n' '# PLACEHOLDER' > "$S/e12/corpus/knowledge/tb2-password-recovery-grader.md"
"$CENSUS" validate --file "$S/e12/corpus/SOURCES.md" > "$S/e12-green.txt" 2>&1; echo "E12_control_exit=$?"
echo "E12_rows=$(grep -c '	E12	' "$S/e12-green.txt") E12_ids=$(grep '	E12	' "$S/e12-green.txt" | awk -F'	' '{print $3}' | tr '\n' ' ')"
echo "CENSUS_rows_mode=$( "$CENSUS" census --file "$S/e12/corpus/SOURCES.md" 2>/dev/null | awk -F'\t' '$2=="rows"{print $3}' )"

echo "== Capture manifest (read-only; the entry's own recheck command)"
( cd "$CAPDIR" && sha256sum -c SHA256SUMS ); echo "SHA256SUMS_exit=$?"
echo "CAPTURE_FILES $(cd "$CAPDIR" && find . -type f | sort | tr '\n' ' ')"

echo "== gitignore has no graded role (reject evidence)"
echo "gitignore_mentions_test_outputs=$(grep -c gitignore "$CAPDIR/tests/test_outputs.py")"
echo "gitignore_mentions_test_sh=$(grep -c gitignore "$CAPDIR/tests/test.sh")"
echo "gitignore_mentions_setup=$(grep -c gitignore "$CAPDIR/environment/setup.sh")"
echo "spec_row_ids=$(python3 -c 'import json;print(",".join(json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r45.json"))["rows"]))')"
echo "gitignore_sha256=$(sha256sum "$CAPDIR/gitignore" | cut -d' ' -f1)"
