#!/usr/bin/env bash
# R45PkgRows validation receipt: rows -> scratch clone -> census validate + V3 + anchor digest, with red controls.
set -u
S=/fast/scratch/hyaku/kengaku-r45/R45PkgRows
LANE=$S/lane
REP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w1/R45PkgRows
ROWS=$REP/rows-S149-S156.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ANCHOR=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/anchor_digest_check.py
ENTRY=$LANE/corpus/knowledge/tb2-password-recovery-grader.md

echo "TIP $(git -C "$LANE" rev-parse HEAD) toplevel=$(git -C "$LANE" rev-parse --show-toplevel)"
echo "ROWS_BEFORE $(grep -c '^| S' "$LANE/corpus/SOURCES.md")"
# insert after the LAST registry row (the file has trailing sections; appending at EOF would be E12)
python3 - "$LANE/corpus/SOURCES.md" "$ROWS" <<'PY'
import pathlib, re, sys
sources, rows = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
lines = sources.read_text().split("\n")
last = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3} \|", l))
new = lines[:last + 1] + rows.read_text().rstrip("\n").split("\n") + lines[last + 1:]
sources.write_text("\n".join(new))
print(f"INSERTED_AFTER_LINE {last + 1} added={len(rows.read_text().rstrip(chr(10)).split(chr(10)))}")
PY
echo "ROWS_AFTER $(grep -c '^| S' "$LANE/corpus/SOURCES.md")"

# E11 target: the entry is authored by another seat; census tests existence only.
mkdir -p "$LANE/corpus/knowledge"
printf '%s\n' '# PLACEHOLDER — E11 existence target only (R45PkgRows validation copy; never a lane file)' \
  'The entry corpus/knowledge/tb2-password-recovery-grader.md is drafted by a different round-45 seat.' > "$ENTRY"

echo "== ROWCHECK (cells/upstream/verbatim-line/word-count/sha256-pin/entry_rules)"
python3 "$REP/rowcheck.py" "$ROWS"; echo "ROWCHECK_exit=$?"

echo "== V3 (the frozen C2 counter's own function, read-only import, lane=clone)"
python3 - "$LANE" <<'PY'
import importlib.util, pathlib, sys
lane = pathlib.Path(sys.argv[1])
p = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c2_verify.py"
sp = importlib.util.spec_from_file_location("c2r45", p)
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
ok, detail = m.v3(lane)
print(f"V3 ok={ok} {detail}")
PY
echo "V3_exit=$?"

echo "== CENSUS green (rows in Registry, E11 placeholder present)"
"$CENSUS" validate --file "$LANE/corpus/SOURCES.md"; echo "CENSUS_exit_code=$?"
"$CENSUS" validate --file "$LANE/corpus/SOURCES.md" > "$S/census-green.txt" 2>&1
echo "CENSUS_counts W04=$(grep -c '	W04	' "$S/census-green.txt") E-codes=$(grep -cE '	E[0-9]+	' "$S/census-green.txt")"
echo "== CENSUS rows (registry total after append)"
"$CENSUS" census --file "$LANE/corpus/SOURCES.md" 2>/dev/null | head -2
echo "SOURCE_ROW_regex_hits $(grep -cE '^ {0,3}\| S[0-9]{3} \|' "$LANE/corpus/SOURCES.md")"

echo "== CENSUS red control (E11 target removed -> E11 must fire on all eight rows)"
mv "$ENTRY" "$S/entry-placeholder.moved"
"$CENSUS" validate --file "$LANE/corpus/SOURCES.md" > "$S/census-red.txt" 2>&1; echo "CENSUS_red_exit_code=$?"
mv "$S/entry-placeholder.moved" "$ENTRY"
echo "E11_rows_fired=$(grep -c '	E11	' "$S/census-red.txt") E11_ids=$(grep '	E11	' "$S/census-red.txt" | awk -F'	' '{print $3}' | tr '\n' ' ')"

echo "== ANCHOR green leg A (rows in Registry): each row's sha256 token binds to its own committed capture"
python3 "$ANCHOR" --lane "$LANE" > "$S/anchor-verbose.txt" 2>&1; echo "ANCHOR_exit=$?"
head -1 "$S/anchor-verbose.txt"
grep -E "^(BIND|UNBOUND|DEFECT|RESOLVED) S1(49|5[0-6])" "$S/anchor-verbose.txt"
tail -1 "$S/anchor-verbose.txt"

echo "== ANCHOR red control (S154 digest last nibble flipped -> one named defect)"
cp "$LANE/corpus/SOURCES.md" "$S/SOURCES.green"
python3 - "$LANE/corpus/SOURCES.md" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text()
old = "sha256 122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add"
assert old in t, "S154 digest not found"
p.write_text(t.replace(old, old[:-1] + "f"))
PY
python3 "$ANCHOR" --lane "$LANE" > "$S/anchor-mutant.txt" 2>&1; echo "ANCHOR_mutant_exit=$?"
grep -E "^DEFECT S154" "$S/anchor-mutant.txt"; tail -1 "$S/anchor-mutant.txt"
cp "$S/SOURCES.green" "$LANE/corpus/SOURCES.md"
echo "RESTORED_rows=$(grep -c '^| S' "$LANE/corpus/SOURCES.md")"
echo "GIT_STATUS_LINES $(git -C "$LANE" status --porcelain | wc -l)"
