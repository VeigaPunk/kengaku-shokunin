#!/bin/sh
# kengaku round-24 census v2 — run from the lane root: sh plans/round24_census.sh
# Reads the WORKING TREE. Before values were taken at 99cf615 by running v1
# there (plans/round-24-claims.md); v2 tightens matching after the
# pre-registration review (§Amendment 1 of that file). Base is reproducible
# with: mkdir -p /tmp/k24base && git archive 99cf615 | tar -x -C /tmp/k24base, then
# run this script with cwd /tmp/k24base (HEAD line prints n/a there).
echo "HEAD $(git rev-parse --short HEAD 2>/dev/null || echo n/a)"

# --- C1 coverage: index parity, both directions, backticked rows only -------
unidx() { # $1 = dir under corpus/ ; prints files with no backticked README row
  for f in corpus/"$1"/*; do b=$(basename "$f"); grep -qF "\`$1/$b\`" corpus/README.md || echo "$b"; done; }
echo "C1.knowledge_files $(ls corpus/knowledge/*.md | wc -l)"
echo "C1.knowledge_unindexed $(unidx knowledge | wc -l)"
echo "C1.lessons_files $(ls corpus/lessons/*.md | wc -l)"
echo "C1.lessons_unindexed_excl_round24 $(unidx lessons | grep -vx 'round-24.md' | wc -l)"
echo "C1.root_logs_indexed $(for f in corpus/evidence/*.log; do b=$(basename "$f"); { grep -qF "| \`$b\` |" corpus/README.md || grep -qF "| \`evidence/$b\` |" corpus/README.md; } && echo x; done | wc -l)/$(ls corpus/evidence/*.log | wc -l)"
echo "C1.plans_indexed $(for f in plans/*; do grep -qF "\`plans/$(basename "$f")\`" corpus/README.md && echo x; done | wc -l)/$(ls plans | wc -l)"
# literal path tokens only (globs/brace sets are prose); a trailing :line or §anchor is stripped
echo "C1.dead_index_rows $(grep -oE '`(knowledge|lessons|evidence)/[^`*{?]+`' corpus/README.md | tr -d '`' | sed 's/[:§].*$//' | sort -u | while read -r p; do [ -e "corpus/$p" ] || echo "$p"; done | wc -l)"
echo "C1.dead_plans_rows $(grep -oE '`plans/[^`*{?]+`' corpus/README.md | tr -d '`' | sed 's/[:§].*$//' | sort -u | while read -r p; do [ -e "$p" ] || echo "$p"; done | wc -l)"
echo "C1.coverage_map_rows $(awk '/^## Coverage map/{f=1;next}/^## /{f=0}f&&/^- /{c++}END{print c+0}' corpus/README.md)"
echo "C1.frontier_rows $(awk '/^## Frontier/{f=1;next}/^## /{f=0}f&&/^- /&&!/^- (TBD|TODO|none)/{c++}END{print c+0}' corpus/README.md)"
echo "C1.province_map_sections $(grep -cE '^### (Core|Frontier|Adjacent|Historical)' PROVINCE.md)"

# --- C1 expansion: entries whose first three lines are the triad AND whose
#     source: line cites a SOURCES row that is `mined` and lists the entry -----
triad() { head -3 "$1" | awk 'NR==1&&/^source: S[0-9]{3}/{a=1} NR==2&&/^verified-at: [0-9]{4}-[0-9]{2}-[0-9]{2}$/{b=1} NR==3&&/^recheck: [0-9]{4}-[0-9]{2}-[0-9]{2}/{c=1} END{exit !(a&&b&&c)}'; }
echo "C1.full_triad_knowledge $(for f in corpus/knowledge/*.md; do triad "$f" && echo "$f"; done | wc -l)"
exp=0
if [ -e corpus/SOURCES.md ]; then
  for f in corpus/knowledge/*.md; do
    triad "$f" || continue
    for id in $(head -1 "$f" | grep -oE 'S[0-9]{3,}' | sort -u); do
      awk -F'|' -v id="$id" -v p="$f" '{i=$2; gsub(/[[:space:]]/,"",i); s=$9; gsub(/[[:space:]]/,"",s)} i==id && s=="mined" && index($12,p) {ok=1} END{exit !ok}' corpus/SOURCES.md && { exp=$((exp+1)); break; }
    done
  done
fi
echo "C1.expansion_entries_on_mined_rows $exp"
if [ -e corpus/SOURCES.md ]; then
  echo "C1.sources_rows $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)"
  echo "C1.sources_mined_without_used_by $(awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {s=$9; u=$12; gsub(/[[:space:]]/,"",s); gsub(/[[:space:]]/,"",u); if (s=="mined" && (u==""||u=="—")) n++} END{print n+0}' corpus/SOURCES.md)"
  echo "C1.sources_rejected_without_flip $(awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if (s=="rejected" && $8 !~ /REJECTED:.*flip:/) n++} END{print n+0}' corpus/SOURCES.md)"
else
  echo "C1.sources_rows absent"
fi

# --- C2 calibration: mistakes mined, closure criteria, round-23 record -------
if [ -e corpus/lessons/round-24.md ]; then
  echo "C2.lesson_mistake_rows $(awk '/^## Mistakes/{f=1;next}/^## /{f=0}f&&/^\| M[0-9]+ /{c++}END{print c+0}' corpus/lessons/round-24.md)"
  echo "C2.lesson_mistake_dup_ids $(awk '/^## Mistakes/{f=1;next}/^## /{f=0}f&&/^\| M[0-9]+ /{print $2}' corpus/lessons/round-24.md | sort | uniq -d | wc -l)"
else
  echo "C2.lesson_mistake_rows absent"
fi
if [ -e corpus/QUALITY.md ]; then
  # an R-row counts when its block cites round-24.md AND at least one more lesson path or a mistake id
  echo "C2.closure_criteria_citing_round24 $(awk '/^## Round-closure criteria/{s=1;next} /^## /{s=0} s&&/^- \*\*R[0-9]+/ && /corpus\/lessons\/round-24\.md/ && /M[0-9][0-9]/{c++} END{print c+0}' corpus/QUALITY.md)"
else
  echo "C2.closure_criteria_citing_round24 absent"
fi
echo "C2.round23_sections $(grep -cE '^## Round 23 ' LOG.md) $(grep -cE '^## Round 23 ' SCORECARD.md)"
echo "C2.round23_not_admitted_with_fail_quote $(awk '/^## Round 23 /{f=1;next}/^## /{f=0}f' LOG.md | tr '\n' ' ' | grep -c 'NOT-ADMITTED.*' | awk -v q="$(awk '/^## Round 23 /{f=1;next}/^## /{f=0}f' LOG.md | grep -c 'attrib-r23-stream.log')" '{print ($1>0 && q>0)?1:0}')"
echo "C2.saturation_declared $(awk '/^## Saturation/{f=1;next}/^## /{f=0}f' SCORECARD.md | grep -cE 'saturation line: [0-9]+.*stagnation window N: [0-9]+')"
echo "C2.capability_rows $(awk '/^## Capabilities/{f=1;next}/^## /{f=0}f&&/^\| [a-z0-9-]+ \|/{c++}END{print c+0}' SCORECARD.md)"
# SCORECARD-vs-repo state defects named in the W1 STATE dossier §5 (D10-D14, D16); prints the open ones
sd=0
awk '/^## Round 24 /{f=1;next}/^## /{f=0}f&&/^\| \*?\*?(novelty|calibration|depth|coverage|operability|freshness|adjacency)/{c++}END{exit !(c>=7)}' SCORECARD.md || { sd=$((sd+1)); echo "  open D10 (no re-derived 7-axis table for round 24)"; }
[ "$(awk '/^## Capabilities/{f=1;next}/^## /{f=0}f&&/^\| [a-z0-9-]+ \|/{c++}END{print c+0}' SCORECARD.md)" -ge 1 ] || { sd=$((sd+1)); echo "  open D11 (capabilities table empty)"; }
awk '/^## Saturation/{f=1;next}/^## /{f=0}f' SCORECARD.md | grep -qE 'saturation line: [0-9]+.*stagnation window N: [0-9]+' || { sd=$((sd+1)); echo "  open D12 (saturation undeclared)"; }
{ grep -qE '^## Planned \(round 25\)' SCORECARD.md && awk '/^## Planned \(next axis-move\)/{f=1;next}/^## /{f=0}f' SCORECARD.md | grep -q '^Superseded (round 24)'; } || { sd=$((sd+1)); echo "  open D13 (planned block stale or old plan not marked superseded)"; }
grep -qE '^- \*\*D14 errata' SCORECARD.md || { sd=$((sd+1)); echo "  open D14 (149-checks line uncorrected)"; }
grep -qE '^## Round 23 ' SCORECARD.md || { sd=$((sd+1)); echo "  open D16 (round 23 unrecorded)"; }
echo "C2.scorecard_state_defects_open $sd/6"
