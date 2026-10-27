#!/usr/bin/env bash
# R44PkgRows re-fetch: re-download each row/reject candidate from the pinned upstream
# and cmp against the capture in corpus/evidence/round44/tb2-feal-linear-cryptanalysis/.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44PkgRows
CAP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round44/tb2-feal-linear-cryptanalysis
BASE=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis
mkdir -p "$S/fetch"
printf 'refetch-base %s\n' "$BASE"
while read -r cap upstream; do
  out="$S/fetch/$cap"
  code=$(curl -sS -o "$out" -w '%{http_code}' "$BASE/$upstream")
  t=$(date +%H:%M:%S)
  sz=$(wc -c < "$out")
  if cmp -s "$out" "$CAP/$cap"; then r=identical; else r=DIFFERS; fi
  printf 'REFETCH %s %s upstream=%s http=%s bytes=%s cmp=%s\n' "$t" "$cap" "$upstream" "$code" "$sz" "$r"
done <<'EOF'
test_outputs.py tests/test_outputs.py
instruction.md instruction.md
gen.py environment/task-deps/gen.py
Dockerfile environment/Dockerfile
test.sh tests/test.sh
README.md README.md
solve.sh solution/solve.sh
decrypt.c environment/task-deps/decrypt.c
task.toml task.toml
feal.c environment/task-deps/feal.c
gitignore environment/task-deps/gitignore
EOF
printf 'refetch-done %s\n' "$(date +%H:%M:%S)"
