# R44ScoutRefetch — freshness re-fetch of tb2 feal-linear-cryptanalysis captures

Pin: terminal-bench-2 @ 2fd12b88aafdd04a52c298e3940bcb189f9766d6. Capture dir: corpus/evidence/round44/tb2-feal-linear-cryptanalysis/. Nothing in the lane was written.

## Re-fetch (2026-10-26, start 20:33:08 -03, end 20:33:10 -03)
Command: `curl -fsS -o f/<cap> https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88.../feal-linear-cryptanalysis/<upstream>` then `cmp f/<cap> <capture dir>/<cap>`. Upstream paths for feal.c and .gitignore come from the pin's git tree (`gh api repos/.../git/trees/<pin>?recursive=1`, 11 blobs under the task dir).

| time | capture | upstream path | curl rc | cmp | sha256[:16] | bytes |
|---|---|---|---|---|---|---|
| 20:33:08 | test_outputs.py | tests/test_outputs.py | 0 | IDENTICAL | f59ebc7218a64858 | 2914 |
| 20:33:08 | instruction.md | instruction.md | 0 | IDENTICAL | a2f1669d4067af6c | 618 |
| 20:33:08 | gen.py | environment/task-deps/gen.py | 0 | IDENTICAL | 3a71f0b5d9095440 | 3496 |
| 20:33:09 | Dockerfile | environment/Dockerfile | 0 | IDENTICAL | ef521cded1b5e0e9 | 386 |
| 20:33:09 | test.sh | tests/test.sh | 0 | IDENTICAL | 9431cbc2bad2b690 | 611 |
| 20:33:09 | README.md | README.md | 0 | IDENTICAL | a038645f908b4e01 | 1810 |
| 20:33:09 | solve.sh | solution/solve.sh | 0 | IDENTICAL | be50ae01a3ea850a | 7724 |
| 20:33:09 | decrypt.c | environment/task-deps/decrypt.c | 0 | IDENTICAL | 4c6864e0d3a76626 | 3982 |
| 20:33:09 | task.toml | task.toml | 0 | IDENTICAL | a39ec2c427af534c | 917 |
| 20:33:10 | feal.c | environment/task-deps/feal.c | 0 | IDENTICAL | bbd38d19f976b27e | 3472 |
| 20:33:10 | gitignore | .gitignore | 0 | IDENTICAL | 9a8dd8d9b6c3adb8 | 177 |

Output: `ok=11`. `sha256sum -c SHA256SUMS` run over the fresh fetches: all 11 `OK`. The nine S138-S146 digests also equal those pinned in plans/pkg-spec-r44.json (the SHA256SUMS lines match the json values).

## Upstream drift since the pin
- `gh api repos/harbor-framework/terminal-bench-2 --jq .default_branch` -> `main`.
- `gh api repos/.../commits/HEAD` -> `2fd12b88aafdd04a52c298e3940bcb189f9766d6 2026-04-30T05:53:30Z` — default-branch HEAD IS the pin.
- `gh api 'repos/.../compare/<pin>...HEAD'` -> `identical ahead=0 files_in_feal=0`.
- `gh api 'repos/.../commits?path=feal-linear-cryptanalysis&per_page=100'` -> 12 commits; newest is the pin itself (2026-04-30T05:53:30Z "Add task metadata to task manifests"), then 8773c988 (2026-04-30 "Add task README and gitignore files"), b3418b60 (2025-10-31), abd7e85f, 02550aa1, 090f4b12, 22a360eb, 13946e71, 8ce3434b, 27799640, 38ca7295, 3dbbcbbe. No commit after the pin touches the path.

Drift: 0 files changed, 0 commits after the pin.

Scratch: /fast/scratch/hyaku/kengaku-r44/R44ScoutRefetch removed after this report was written.

VERDICT: refetch-identical-11/11-upstream-drift-0
