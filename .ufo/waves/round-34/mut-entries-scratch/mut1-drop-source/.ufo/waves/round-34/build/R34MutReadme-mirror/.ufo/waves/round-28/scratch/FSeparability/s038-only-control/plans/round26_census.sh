#!/bin/sh
# Round-26 census — run from the lane root: sh plans/round26_census.sh
# Read-only census; Python runs with bytecode disabled. Base checkout: e0037a8.
# Missing round-26 instruments print `absent`; the census itself exits 0.
set -u

if [ "$#" -ne 0 ]; then
  echo "usage: sh plans/round26_census.sh   (no arguments; run from the lane root)" >&2
  exit 2
fi
if [ ! -f SKILL.md ] || [ ! -d corpus ]; then
  echo "round26_census: cwd is not a lane root (needs SKILL.md and corpus/)" >&2
  exit 2
fi

SRC=corpus/SOURCES.md
C1=plans/grader_perturb.py
C2=plans/state_check.py
Q13=plans/gate_timing_check.py

kv() { printf '%s=%s\n' "$1" "$2"; }
sorted() { tr ' ' '\n' | sed '/^$/d' | LC_ALL=C sort | paste -s -d ' ' -; }
list_or_none() {
  if [ -n "$1" ]; then
    printf '%s\n' "$1" | LC_ALL=C sort -u | paste -s -d ',' -
  else
    printf 'none'
  fi
}

# Never attribute an exported tree's parent-repository HEAD to the lane.
top=$(git rev-parse --show-toplevel 2>/dev/null) || top=
if [ -n "$top" ] && [ "$(cd "$top" && pwd -P)" = "$(pwd -P)" ]; then
  kv head "$(git rev-parse --short refs/heads/master 2>/dev/null || echo n/a)"
  full_head=$(git rev-parse refs/heads/master 2>/dev/null) || full_head=
else
  kv head n/a
  full_head=
fi

# C1 — stored-response perturbation audit.
if [ -f "$C1" ]; then
  kv c1_instrument present
  out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$C1" --summary 2>&1); rc=$?
  total=$(printf '%s\n' "$out" | awk '/^TOTAL / { line=$0 } END { print line }')
  [ -n "$total" ] || total=none
  families=$(printf '%s\n' "$total" | awk '{ for (i=1; i<=NF; i++) if ($i ~ /^families_with_interval_verdict=/) { sub(/^families_with_interval_verdict=/, "", $i); value=$i } } END { if (value != "") print value; else print "none" }')
  kv c1_total "$total"
  kv c1_families_with_interval_verdict "$families"
  kv c1_exit "$rc"
else
  kv c1_instrument absent
  kv c1_total absent
  kv c1_families_with_interval_verdict absent
  kv c1_exit absent
fi

# C2 — retain the first summary line; count only P3 MISMATCH rows. An older
# checker without any P3 assertions is `absent`, not a misleading zero.
if [ -f "$C2" ]; then
  out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$C2" --summary 2>&1); rc=$?
  first=$(printf '%s\n' "$out" | awk 'NR == 1 { print; exit }')
  [ -n "$first" ] || first=none
  kv c2_state_check_first_line "$first"
  if grep -qE 'P3[a-e]' "$C2"; then
    p3=$(printf '%s\n' "$out" | awk '/^MISMATCH: P3[a-e](\.|:)/ { n++ } END { print n+0 }')
  else
    p3=absent
  fi
  kv c2_p3_mismatch_count "$p3"
  kv c2_exit "$rc"
else
  kv c2_state_check_first_line absent
  kv c2_p3_mismatch_count absent
  kv c2_exit absent
fi

# Q13 — measure the known red-before and this round's lesson at its landing HEAD.
if [ -f "$Q13" ]; then
  kv q13_instrument present
  rc=$(PYTHONDONTWRITEBYTECODE=1 python3 "$Q13" --lesson corpus/lessons/round-25.md --commit 8ea41f9 --repo . >/dev/null 2>&1; printf '%s' "$?")
  kv q13_round25_8ea41f9_exit "$rc"
  if [ -n "$full_head" ] && git cat-file -e "$full_head:corpus/lessons/round-26.md" 2>/dev/null; then
    rc=$(PYTHONDONTWRITEBYTECODE=1 python3 "$Q13" --lesson corpus/lessons/round-26.md --commit "$full_head" --repo . >/dev/null 2>&1; printf '%s' "$?")
    kv q13_round26_lesson present
    kv q13_round26_lesson_exit "$rc"
  else
    kv q13_round26_lesson absent
    kv q13_round26_lesson_exit absent
  fi
else
  kv q13_instrument absent
  kv q13_round25_8ea41f9_exit absent
  kv q13_round26_lesson absent
  kv q13_round26_lesson_exit absent
fi

# SOURCES.md contract-v1 census: the four frozen CORPUS.md commands, with
# histograms sorted as in the round-25 census for stable output.
if [ -f "$SRC" ]; then
  kv sources_rows "$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$SRC")"
  kv sources_malformed "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$SRC")"
  kv sources_tier_histogram "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$SRC" | sorted)"
  kv sources_status_histogram "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$SRC" | sorted)"
else
  for k in sources_rows sources_malformed sources_tier_histogram sources_status_histogram; do
    kv "$k" absent
  done
fi

# Knowledge index parity is bidirectional within corpus/README.md's knowledge
# rows: on-disk Markdown without an index row, dangling rows, and duplicate rows.
if [ -d corpus/knowledge ]; then
  files=0
  for f in corpus/knowledge/*.md; do
    [ -f "$f" ] || continue
    files=$((files + 1))
  done
  kv knowledge_files "$files"
else
  kv knowledge_files absent
fi
if [ -f corpus/README.md ]; then
  index=$(awk -F'|' '{ cell=$2; gsub(/^[[:space:]]+|[[:space:]]+$/, "", cell); if (cell ~ /^`knowledge\/[^`|]+\.md`$/) { sub(/^`/, "", cell); sub(/`$/, "", cell); print cell } }' corpus/README.md)
  index_rows=$(printf '%s\n' "$index" | awk 'NF { n++ } END { print n+0 }')
  kv knowledge_readme_index_rows "$index_rows"
  if [ -d corpus/knowledge ]; then
    unindexed=
    for f in corpus/knowledge/*.md; do
      [ -f "$f" ] || continue
      rel="knowledge/${f#corpus/knowledge/}"
      if ! printf '%s\n' "$index" | grep -Fqx "$rel"; then
        unindexed="${unindexed}${unindexed:+
}$rel"
      fi
    done
    dangling=$(printf '%s\n' "$index" | while IFS= read -r rel; do
      [ -n "$rel" ] && [ -f "corpus/$rel" ] || { [ -z "$rel" ] || printf '%s\n' "$rel"; }
    done)
    duplicates=$(printf '%s\n' "$index" | LC_ALL=C sort | uniq -d)
    kv knowledge_readme_unindexed_files "$(list_or_none "$unindexed")"
    kv knowledge_readme_dangling_rows "$(list_or_none "$dangling")"
    kv knowledge_readme_duplicate_rows "$(list_or_none "$duplicates")"
    if [ -z "$unindexed" ] && [ -z "$dangling" ] && [ -z "$duplicates" ]; then
      kv knowledge_readme_parity match
    else
      kv knowledge_readme_parity mismatch
    fi
  else
    kv knowledge_readme_unindexed_files absent
    kv knowledge_readme_dangling_rows absent
    kv knowledge_readme_duplicate_rows absent
    kv knowledge_readme_parity absent
  fi
else
  kv knowledge_readme_index_rows absent
  kv knowledge_readme_unindexed_files absent
  kv knowledge_readme_dangling_rows absent
  kv knowledge_readme_duplicate_rows absent
  kv knowledge_readme_parity absent
fi
exit 0
