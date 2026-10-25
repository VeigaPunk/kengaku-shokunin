#!/usr/bin/env bash
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
SCRATCH=$LANE/.ufo/waves/round-35/build/R35MutC1V4V5
D=$(mktemp -d /tmp/k35-XXXX)
printf '%s\n' "$D" > "$SCRATCH/fixture-path.txt"
git clone -q --no-checkout --shared "$LANE" "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/corpus/**' '/plans/**'
git -C "$D/lane" checkout -q master
TOP=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$TOP" = "$D/lane" ] || { echo "toplevel mismatch: $TOP"; exit 1; }
echo "toplevel ok: $TOP"
# uncommitted round-35 package files from the lane working tree
mkdir -p "$D/lane/corpus/evidence/round35"
cp "$LANE/corpus/README.md" "$LANE/corpus/SOURCES.md" "$D/lane/corpus/"
cp "$LANE/corpus/knowledge/tb2-protein-assembly-grader.md" "$D/lane/corpus/knowledge/"
cp -r "$LANE/corpus/evidence/round35/tb2-eval" "$D/lane/corpus/evidence/round35/"
cp "$LANE/corpus/evidence/round35/tb2-grader-probe.txt" "$D/lane/corpus/evidence/round35/"
rm -rf "$D/lane/corpus/evidence/round35/tb2-eval/__pycache__"
# stage the new knowledge entry so v4's `git ls-files` count sees the package (no commit)
git -C "$D/lane" add corpus/knowledge/tb2-protein-assembly-grader.md
echo "staged knowledge files: $(git -C "$D/lane" ls-files 'corpus/knowledge/*.md' | wc -l)"
mkdir -p "$D/pristine"
cp "$D/lane/corpus/README.md" "$D/pristine/README.md"
cp "$D/lane/corpus/SOURCES.md" "$D/pristine/SOURCES.md"
cp "$D/lane/corpus/knowledge/tb2-protein-assembly-grader.md" "$D/pristine/entry.md"
cp "$D/lane/corpus/evidence/round35/tb2-grader-probe.txt" "$D/pristine/receipt.txt"
cp "$D/lane/plans/tb2_grader_probe.py" "$D/pristine/probe.py"
echo "--- pristine sha256 ---"
sha256sum "$D"/pristine/README.md "$D"/pristine/SOURCES.md "$D"/pristine/entry.md "$D"/pristine/receipt.txt "$D"/pristine/probe.py
