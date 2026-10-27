# R45ScoutRefetch — refetch of tb2 password-recovery @ pin (2026-10-26, 23:25:41–23:26:04 -03)

Pin: 2fd12b88aafdd04a52c298e3940bcb189f9766d6. Base: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/<pin>/password-recovery/
Captures: corpus/evidence/round45/tb2-password-recovery/. Refetch: curl -sS per path into /fast/scratch/hyaku/kengaku-r45/R45ScoutRefetch/f/ (HTTP 200 for all nine). No lane writes.

## Byte-compare (cmp + sha256sum, both sides)
| path | sha256 (fetch == capture) | cmp |
|---|---|---|
| README.md | 122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add | identical |
| instruction.md | bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5 | identical |
| task.toml | cfd0362d201b957796f9bf1c02cc75646250cb2bd107ec88c768bfcfd091b24b | identical |
| environment/Dockerfile | 6fabcb9e1fcb7155bf8cfe106c17f2dfa3344103e97960dab580c2444b6c9fe0 | identical |
| environment/setup.sh | 9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8 | identical |
| solution/solve.sh | c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f | identical |
| tests/test.sh | 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 | identical |
| tests/test_outputs.py | 2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e | identical |
| .gitignore (capture stored as `gitignore`, no dot) | 9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953 | identical |

9/9 identical. Note: the capture file `gitignore` is upstream `password-recovery/.gitignore` (dot dropped in the capture name; fetching literal `/gitignore` returns 404 — expected). All 9 sha256 equal the lines in the capture's SHA256SUMS. Tree-listing blob sizes at the pin agree with the captures (README 2007, task.toml 949, instruction 644, .gitignore 177, test_outputs.py 594, test.sh 608, setup.sh 1582, Dockerfile 497, solve.sh 3071).

## Pin / HEAD
- `git ls-remote https://github.com/harbor-framework/terminal-bench-2 HEAD refs/heads/main` → `2fd12b88aafdd04a52c298e3940bcb189f9766d6 HEAD` and `… refs/heads/main`. HEAD == pin; no newer commit.
- GitHub API commits/<pin> and commits/HEAD both return sha 2fd12b88…, "Add task metadata to task manifests", Alex Shaw, 2026-04-30T05:53:30Z, tree ec7c02c7f0b59ce8ed2f7c88d1e70cda7427edfa → pin resolves.
- Recursive tree listing (truncated=False): `password-recovery/` still present at the same path with exactly the 9 files above (3 subdirs: environment, solution, tests); task dir did not move.
- HEAD-path raw fetch of tests/test_outputs.py sha256 = 2dc14fc1…3ffc9e (same as capture).

## Drift
None. (Only observation: the capture name `gitignore` vs upstream `.gitignore` is a naming difference, content identical.)

VERDICT: refetch-identical-9/9-pin-ok-yes
