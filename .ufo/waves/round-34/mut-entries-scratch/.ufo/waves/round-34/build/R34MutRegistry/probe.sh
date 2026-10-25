#!/usr/bin/env bash
# R34MutRegistry — mutation probe: fleet sources-census.sh against a scratch mirror
# of corpus/SOURCES.md + drafted append rows S105-S107. Read-only on the lane;
# all writes stay under .ufo/waves/round-34/build/R34MutRegistry/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
S="$LANE/.ufo/waves/round-34/build/R34MutRegistry"
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
OUT="$S/out"
rm -rf "$OUT" "$S/mirror" "$S/mut"
mkdir -p "$OUT" "$S/mirror" "$S/mut"

# --- 1. scratch mirror: full corpus copy + staged C1 entry + drafted rows ----
cp -a "$LANE/corpus" "$S/mirror/corpus"
cp "$LANE/.ufo/waves/round-34/build/R34EntryTB2/entry.md" \
   "$S/mirror/corpus/knowledge/terminal-bench-task-grader.md"
M="$S/mirror/corpus/SOURCES.md"
gawk '
  { print }
  /^\| S104 \|/ && !done {
    print "| S105 | https://github.com/harbor-framework/terminal-bench-2/blob/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py | code | A | protein-assembly evaluator grading logic | test_outputs.py: lines 18-23 | Validates one-line DNA gBlock alphabet and maximum length | mined | 2026-10-25 | annual | corpus/knowledge/terminal-bench-task-grader.md |"
    print "| S106 | https://github.com/harbor-framework/terminal-bench-2/blob/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh | code | A | protein-assembly evaluator runner and reward writer | test.sh: lines 18-29 | Runs pytest with pinned dependencies and writes binary reward | mined | 2026-10-25 | annual | corpus/knowledge/terminal-bench-task-grader.md |"
    print "| S107 | https://github.com/harbor-framework/terminal-bench-2/blob/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/environment/antibody.fasta and protein-assembly/environment/pdb_ids.txt | dataset | A | protein-assembly expected antibody and PDB identifier artifacts | antibody.fasta: lines 1-4; pdb_ids.txt: lines 1-20 | Expected antibody chains and PDB identifier list | mined | 2026-10-25 | annual | corpus/knowledge/terminal-bench-task-grader.md |"
    done=1
  }' "$LANE/corpus/SOURCES.md" > "$M"
echo "== appended rows =="
grep -c '^| S10[567] |' "$M"
sha256sum "$M" | tee "$OUT/pristine.sha256"

# --- 2. baseline (pristine) runs ---------------------------------------------
{ "$CENSUS" census  --file "$M"; echo "EXIT=$?"; } > "$OUT/baseline.census.txt" 2>&1
{ "$CENSUS" validate --file "$M"; echo "EXIT=$?"; } > "$OUT/baseline.validate.txt" 2>&1
sha256sum "$M" > "$OUT/pristine.after-baseline.sha256"

# --- 3. five mutants, one behavior-bearing point each ------------------------
mutate() { # $1 name, $2 gawk program
  gawk "$2" "$M" > "$S/mut/$1.md" || { echo "gawk failed: $1" >&2; return 1; }
  { "$CENSUS" validate --file "$S/mut/$1.md"; echo "EXIT=$?"; } > "$OUT/mut-$1.txt" 2>&1
  sha256sum "$S/mut/$1.md" > "$OUT/mut-$1.sha256"
  grep -n '^\| S105\|^\| S106\|^\| S107' "$S/mut/$1.md" > "$OUT/mut-$1.row.txt"
}

# M1 malformed column count: drop the scope cell from the S106 row (11 -> 10 fields)
mutate m1-column-count '{ if ($0 ~ /^\| S106 \|/) { n=split($0,a,"|"); printf "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n", a[1],a[2],a[3],a[4],a[5],a[7],a[8],a[9],a[10],a[11],a[12]; next } print }'

# M2 escaped pipe inside a cell: append "\| alt" inside the S105 teaches cell
mutate m2-escaped-pipe '{ if ($0 ~ /^\| S105 \|/) { n=split($0,a,"|"); a[8]=a[8] " \\| alt"; out=""; for(i=1;i<=n;i++) out=out a[i] (i<n?"|":""); print out; next } print }'

# M3 duplicate id: relabel the S106 row id as S105
mutate m3-duplicate-id '{ if ($0 ~ /^\| S106 \|/) { sub(/\| S106 \|/,"| S105 |"); print; next } print }'

# M4 community tier A: S107 kind dataset -> community, tier stays A
mutate m4-community-tier-a '{ if ($0 ~ /^\| S107 \|/) { sub(/\| dataset \|/,"| community |"); print; next } print }'

# M5 mined row with missing used-by path: S105 used-by -> nonexistent file
mutate m5-missing-usedby '{ if ($0 ~ /^\| S105 \|/) { sub(/terminal-bench-task-grader\.md \|$/,"terminal-bench-task-grader-MISSING.md |"); print; next } print }'

# --- 4. restoration evidence: pristine re-validated, bytes re-hashed ---------
{ "$CENSUS" validate --file "$M"; echo "EXIT=$?"; } > "$OUT/post.validate.txt" 2>&1
sha256sum "$M" > "$OUT/pristine.post.sha256"
cmp -s "$OUT/baseline.validate.txt" "$OUT/post.validate.txt" && echo "PRISTINE-VALIDATE-IDENTICAL=yes" || echo "PRISTINE-VALIDATE-IDENTICAL=no"
cmp -s "$OUT/pristine.after-baseline.sha256" "$OUT/pristine.post.sha256" && echo "PRISTINE-BYTES-RESTORED=yes" || echo "PRISTINE-BYTES-RESTORED=no"

# --- 5. verdict table ----------------------------------------------------------
verdict() { # $1 mutant $2 expected-code
  if grep -qF "$2" "$OUT/mut-$1.txt" && grep -q '^EXIT=1$' "$OUT/mut-$1.txt"; then
    echo "killed	$1	$2"
  else
    echo "SURVIVED	$1	$2"
  fi
}
verdict m1-column-count    E01
verdict m2-escaped-pipe    E01
verdict m3-duplicate-id    E03
verdict m4-community-tier-a E10
verdict m5-missing-usedby  E11
