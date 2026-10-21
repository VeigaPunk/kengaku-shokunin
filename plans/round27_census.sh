#!/bin/sh
# Round-27 census — run from the lane root: sh plans/round27_census.sh
# Read-only census; Python runs with bytecode disabled. Missing instruments print absent.
set -u

if [ "$#" -ne 0 ]; then
  echo "usage: sh plans/round27_census.sh   (no arguments; run from the lane root)" >&2
  exit 2
fi
if [ ! -f SKILL.md ] || [ ! -d corpus ]; then
  echo "round27_census: cwd is not a lane root (needs SKILL.md and corpus/)" >&2
  exit 2
fi

SRC=corpus/SOURCES.md
C1=plans/parser_policy_compare.py
ORACLE=plans/fixtures/r27/policy_oracle.py
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

# C1 — compare extraction policies on the pinned stored responses.
if [ -f "$C1" ]; then
  kv c1_instrument present
  out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$C1" --summary 2>&1); rc=$?
  total=$(printf '%s\n' "$out" | awk '/^TOTAL / { line=$0 } END { print line }')
  [ -n "$total" ] || total=none
  disagreements=$(printf '%s\n' "$total" | awk '{ for (i=1; i<=NF; i++) if ($i ~ /^disagreements=/) { sub(/^disagreements=/, "", $i); print $i; exit } }')
  [ -n "$disagreements" ] || disagreements=none
  kv c1_total "$total"
  kv c1_disagreements "$disagreements"
  kv c1_exit "$rc"
else
  kv c1_instrument absent
  kv c1_total absent
  kv c1_disagreements absent
  kv c1_exit absent
fi
if [ -f "$ORACLE" ]; then
  PYTHONDONTWRITEBYTECODE=1 python3 "$ORACLE" --root . >/dev/null 2>&1
  oracle_rc=$?
  kv c1_oracle_exit "$oracle_rc"
else
  kv c1_oracle_exit absent
fi

# C2 — retain the first summary line and count only P4 ids in JSON assertions.
if [ -f "$C2" ]; then
  out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$C2" --summary 2>&1); rc=$?
  first=$(printf '%s\n' "$out" | awk 'NR == 1 { print; exit }')
  [ -n "$first" ] || first=none
  kv c2_state_check_first_line "$first"
  json_out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$C2" --json 2>&1)
  p4_counts=$(printf '%s\n' "$json_out" | PYTHONDONTWRITEBYTECODE=1 python3 -c 'import json, re, sys; d=json.load(sys.stdin); a=[x for x in d["assertions"] if re.match(r"^P4[a-e](?:\.|$)", x.get("id", ""))]; print(len(a), sum(x.get("verdict") == "MISMATCH" for x in a))' 2>/dev/null) || p4_counts=none
  if [ "$p4_counts" = none ]; then
    p4_assertions=none
    p4_mismatch=none
  else
    p4_assertions=$(printf '%s\n' "$p4_counts" | awk '{print $1}')
    p4_mismatch=$(printf '%s\n' "$p4_counts" | awk '{print $2}')
  fi
  kv c2_p4_assertions "$p4_assertions"
  kv c2_p4_mismatch "$p4_mismatch"
  kv c2_exit "$rc"
else
  kv c2_state_check_first_line absent
  kv c2_p4_assertions absent
  kv c2_p4_mismatch absent
  kv c2_exit absent
fi

# Q13 — check the round-27 lesson at the lane's master ref when present.
if [ -f "$Q13" ] && [ -n "$full_head" ] && git cat-file -e "$full_head:corpus/lessons/round-27.md" 2>/dev/null; then
  rc=$(PYTHONDONTWRITEBYTECODE=1 python3 "$Q13" --lesson corpus/lessons/round-27.md --commit "$full_head" --repo . >/dev/null 2>&1; printf '%s' "$?")
  kv q13_round27_lesson_exit "$rc"
else
  kv q13_round27_lesson_exit absent
fi

# SOURCES.md contract-v1 census: the four frozen CORPUS.md commands.
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

# Knowledge-index parity is bidirectional within corpus/README.md knowledge rows.
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
