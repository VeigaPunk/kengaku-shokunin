#!/usr/bin/env bash
# ReviewerR84 Q13 mechanics probe — isolated fixture repos, read-only on the lane.
set -u
S=/fast/scratch/hyaku/kengaku-r84/ReviewerR84
export TMPDIR="$S"
CHK=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py
export PYTHONDONTWRITEBYTECODE=1

make_repo() {  # $1 = variant dir; sets D
  D="$1"
  mkdir -p "$D"
  git -C "$D" init -q || return 1
  top=$(git -C "$D" rev-parse --show-toplevel) || return 1
  [ "$top" = "$(cd "$D" && pwd -P)" ] || { echo "TOPLEVEL MISMATCH: $top"; return 1; }
  mkdir -p "$D/corpus/lessons" "$D/corpus/knowledge"
  return 0
}

commit_repo() {
  git -C "$D" add -A && git -C "$D" -c user.name=FixtureSeat -c user.email=fixture@example.invalid \
    -c commit.gpgsign=false commit -q -m "fixture" && git -C "$D" rev-parse HEAD
}

# variant A: w1 directory, entry carries writer
A="$S/fx-a"; rm -rf "$A"; make_repo "$A" || exit 2
mkdir -p "$A/.ufo/waves/round-84/w1"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/w1/ReviewerR84.md` |\n' > "$A/corpus/lessons/round-84.md"
printf 'writer: KengakuR84\nsource: S267\nverified-at: 2026-11-04\nrecheck: monthly\n' > "$A/corpus/knowledge/tb2-code-from-image-offline.md"
printf 'Re-read corpus/knowledge/tb2-code-from-image-offline.md\nVERDICT: agree\n' > "$A/.ufo/waves/round-84/w1/ReviewerR84.md"
printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$A/.ufo/waves/round-84/w1/swarm-registry.json"
ca=$(commit_repo) || exit 2

# variant B: falsify directory, entry carries writer
B="$S/fx-b"; rm -rf "$B"; D=""; make_repo "$B" || exit 2
mkdir -p "$B/.ufo/waves/round-84/falsify"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/falsify/ReviewerR84.md` |\n' > "$B/corpus/lessons/round-84.md"
printf 'writer: KengakuR84\nsource: S267\nverified-at: 2026-11-04\nrecheck: monthly\n' > "$B/corpus/knowledge/tb2-code-from-image-offline.md"
printf 'Re-read corpus/knowledge/tb2-code-from-image-offline.md\nVERDICT: agree\n' > "$B/.ufo/waves/round-84/falsify/ReviewerR84.md"
printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$B/.ufo/waves/round-84/falsify/swarm-registry.json"
cb=$(commit_repo) || exit 2

# variant C: falsify, entry WITHOUT writer field
C="$S/fx-c"; rm -rf "$C"; D=""; make_repo "$C" || exit 2
mkdir -p "$C/.ufo/waves/round-84/falsify"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/falsify/ReviewerR84.md` |\n' > "$C/corpus/lessons/round-84.md"
printf 'source: S267\nverified-at: 2026-11-04\nrecheck: monthly\n' > "$C/corpus/knowledge/tb2-code-from-image-offline.md"
printf 'Re-read corpus/knowledge/tb2-code-from-image-offline.md\nVERDICT: agree\n' > "$C/.ufo/waves/round-84/falsify/ReviewerR84.md"
printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$C/.ufo/waves/round-84/falsify/swarm-registry.json"
cc=$(commit_repo) || exit 2

# variant D: falsify, report declares writer == candidate writer
E="$S/fx-d"; rm -rf "$E"; D=""; make_repo "$E" || exit 2
mkdir -p "$E/.ufo/waves/round-84/falsify"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/falsify/ReviewerR84.md` |\n' > "$E/corpus/lessons/round-84.md"
printf 'writer: KengakuR84\nsource: S267\nverified-at: 2026-11-04\nrecheck: monthly\n' > "$E/corpus/knowledge/tb2-code-from-image-offline.md"
printf 'writer: KengakuR84\nRe-read corpus/knowledge/tb2-code-from-image-offline.md\nVERDICT: agree\n' > "$E/.ufo/waves/round-84/falsify/ReviewerR84.md"
printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$E/.ufo/waves/round-84/falsify/swarm-registry.json"
cd_=$(commit_repo) || exit 2

# variant E: w1 with nested report.md cited
F="$S/fx-e"; rm -rf "$F"; D=""; make_repo "$F" || exit 2
mkdir -p "$F/.ufo/waves/round-84/w1/ReviewerR84"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/w1/ReviewerR84/report.md` |\n' > "$F/corpus/lessons/round-84.md"
printf 'writer: KengakuR84\nsource: S267\nverified-at: 2026-11-04\nrecheck: monthly\n' > "$F/corpus/knowledge/tb2-code-from-image-offline.md"
printf 'Re-read corpus/knowledge/tb2-code-from-image-offline.md\nVERDICT: agree\n' > "$F/.ufo/waves/round-84/w1/ReviewerR84/report.md"
printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$F/.ufo/waves/round-84/w1/swarm-registry.json"
cf=$(commit_repo) || exit 2

echo "COMMIT_A=$ca COMMIT_B=$cb COMMIT_C=$cc COMMIT_D=$cd_ COMMIT_E=$cf"
for pair in "A:$A:$ca" "B:$B:$cb" "C:$C:$cc" "D:$E:$cd_" "E:$F:$cf"; do
  label=${pair%%:*}; rest=${pair#*:}; dir=${rest%%:*}; rev=${rest##*:}
  echo "----- VARIANT $label ($dir @ $rev) -----"
  python3 "$CHK" --lesson corpus/lessons/round-84.md --commit "$rev" --repo "$dir"
  echo "VARIANT_${label}_EXIT=$?"
done
