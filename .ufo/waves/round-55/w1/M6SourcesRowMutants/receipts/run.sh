#!/usr/bin/env bash
# run.sh <label> — restore pristine SOURCES.md, apply mutant <label> (or none for
# baseline), run the three detectors, write a labelled transcript to out/<label>.txt.
# Detectors:
#   D1  CORPUS.md §Census frozen manual command set (7 commands, lane-root relative)
#   D2  fleet scripts/sources-census.sh validate --file <scratch copy>
#   D3  lane's advertised SOURCES gate plans/anchor_digest_check.py (differential)
set -u
S=/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants
LABEL=$1
MUT=${2:-}
LANE="$S/lane"
OUT="$S/out/$LABEL.txt"
mkdir -p "$S/out"

cp "$S/pristine/SOURCES.md" "$LANE/corpus/SOURCES.md"
{
  echo "=== label=$LABEL mutant=${MUT:-none} ==="
  echo "pristine sha256: $(sha256sum "$S/pristine/SOURCES.md" | cut -d' ' -f1)"
  if [ -n "$MUT" ]; then
    echo "--- mutate ---"
    python3 "$S/mutate.py" "$MUT"
    echo "mutate exit=$?"
  fi
  echo "target sha256: $(sha256sum "$LANE/corpus/SOURCES.md" | cut -d' ' -f1)"

  echo "=== D1 CORPUS.md §Census manual commands (cwd=$LANE) ==="
  cd "$LANE"
  echo "--- D1a rows ---"
  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; echo "exit=$?"
  echo "--- D1b malformed (NF!=13) must be 0 ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md; echo "exit=$?"
  echo "--- D1c tier histogram ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md; echo "exit=$?"
  echo "--- D1d status histogram ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md; echo "exit=$?"
  echo "--- D1e duplicate ids must print nothing ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d; echo "exit=$?"
  echo "--- D1f enum violations + tier inflation must print nothing ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md; echo "exit=$?"
  echo "--- D1g mined rows whose used-by paths do not exist must print nothing ---"
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done; echo "exit=$?"

  echo "=== D2 sources-census.sh validate --file ==="
  bash "$S/tools/sources-census.sh" validate --file "$LANE/corpus/SOURCES.md" 2>&1 | awk '!/^file\t(W04\t|ok\t)/'
  echo "D2 exit=${PIPESTATUS[0]}"

  echo "=== D3 anchor_digest_check.py (lane advertised gate) ==="
  python3 "$LANE/plans/anchor_digest_check.py" --lane "$LANE" 2>&1 | grep -E '^(DEFECT S20[12] |rows=)'
  echo "D3 exit=${PIPESTATUS[0]}"
} > "$OUT" 2>&1
echo "wrote $OUT"
