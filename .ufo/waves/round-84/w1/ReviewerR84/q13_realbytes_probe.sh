#!/usr/bin/env bash
# ReviewerR84 Q13 acceptance probe with the REAL report bytes, two directory shapes.
set -u
S=/fast/scratch/hyaku/kengaku-r84/ReviewerR84
export TMPDIR="$S"
CHK=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py
export PYTHONDONTWRITEBYTECODE=1
REPORT="$S/report.md"

build() { # $1 dir, $2 wave dir, $3 cited path
  D="$1"; W="$2"; CITED="$3"
  rm -rf "$D"; mkdir -p "$D"
  git -C "$D" init -q || return 1
  top=$(git -C "$D" rev-parse --show-toplevel) || return 1
  [ "$top" = "$(cd "$D" && pwd -P)" ] || { echo "TOPLEVEL MISMATCH: $top"; return 1; }
  mkdir -p "$D/corpus/lessons" "$D/corpus/knowledge" "$D/.ufo/waves/round-84/$W"
  printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | second-seat re-read `%s`; Q1/Q21 repaired in this commit |\n' "$CITED" > "$D/corpus/lessons/round-84.md"
  printf 'writer: KengakuR84\nsource: S267 — https://example.invalid/pinned :10-31\nverified-at: 2026-11-04\nrecheck: 2027-01-18 re-open S267 at pin 2fd12b88\n' > "$D/corpus/knowledge/tb2-code-from-image-offline.md"
  cp "$REPORT" "$D/$CITED"
  printf '{"members":{"ReviewerR84":{"role":"reviewer","agentId":null}}}\n' > "$D/.ufo/waves/round-84/$W/swarm-registry.json"
  git -C "$D" add -A && git -C "$D" -c user.name=FixtureSeat -c user.email=fixture@example.invalid \
    -c commit.gpgsign=false commit -q -m fixture && git -C "$D" rev-parse HEAD
}

F="$S/fx-real-falsify"; W="$S/fx-real-w1"
rf=$(build "$F" falsify ".ufo/waves/round-84/falsify/ReviewerR84.md") || exit 2
rw=$(build "$W" w1 ".ufo/waves/round-84/w1/ReviewerR84.md") || exit 2
echo "COMMIT_REAL_FALSIFY=$rf COMMIT_REAL_W1=$rw"
echo "----- REAL BYTES at falsify/ReviewerR84.md -----"
python3 "$CHK" --lesson corpus/lessons/round-84.md --commit "$rf" --repo "$F"; echo "REAL_FALSIFY_EXIT=$?"
echo "----- REAL BYTES at w1/ReviewerR84.md -----"
python3 "$CHK" --lesson corpus/lessons/round-84.md --commit "$rw" --repo "$W"; echo "REAL_W1_EXIT=$?"
echo "----- nested report.md shape at w1 -----"
cp "$REPORT" "$W/.ufo/waves/round-84/w1/report.md" 2>/dev/null
D="$W"; mkdir -p "$W/.ufo/waves/round-84/w1/ReviewerR84"
cp "$REPORT" "$W/.ufo/waves/round-84/w1/ReviewerR84/report.md"
printf '# fixture\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n| corpus/knowledge/tb2-code-from-image-offline.md | admit | re-read `.ufo/waves/round-84/w1/ReviewerR84/report.md` |\n' > "$W/corpus/lessons/round-84.md"
git -C "$W" add -A && rw2=$(git -C "$W" -c user.name=FixtureSeat -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -q -m nested && git -C "$W" rev-parse HEAD)
python3 "$CHK" --lesson corpus/lessons/round-84.md --commit "$rw2" --repo "$W"; echo "REAL_NESTED_EXIT=$?"
