# E14CaptureIdentity — round 55 w1 (R55-C3 capture byte-identity)

**Verdict: all three sha256 pairs MATCH; C3 kill rule (c) not fired.**

## Receipt
Full byte-identity receipt: `.ufo/waves/round-55/w1/E14CaptureIdentity/identity.txt`.

## Pairs
| pair | subject | in-repo sha256 | upstream-at-pin sha256 | verdict |
|---|---|---|---|---|
| 1 | chess-best-move/tests/test_outputs.py (971 B) | a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286 | a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286 | MATCH (cmp-identical) |
| 2 | chess-best-move/tests/test.sh (608 B) | 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 | 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 | MATCH (cmp-identical) |
| 3 | runner-identity cross-check: chess test.sh == regex-log tests/test.sh (in-repo, and both == upstream at pin) | 4770437e…c334 both | 4770437e…c334 both | MATCH |

## Pin existence
GitHub API `repos/harbor-framework/terminal-bench-2/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6`
→ sha 2fd12b88aafdd04a52c298e3940bcb189f9766d6, committer date 2026-04-30T05:53:30Z,
message "Add task metadata to task manifests". Confirmed.

## Notes for L1
- Fetched additionally at pin: chess-best-move instruction.md (sha 6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a, 260 B) and task.toml (sha d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e, 849 B) — supports the S201/S202 source rows' identity bytes.
- The upstream task dirs live at the repo ROOT (no `tasks/` prefix); a first fetch with the prefix 404'd and was corrected (no impact).
- Method: sha256sum + `cmp -s` byte-compares, read-only GETs only, no git mutations, scratch under /fast/scratch/hyaku/kengaku-r55/E14CaptureIdentity (deleted after the receipt was copied here).
