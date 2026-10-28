# R49C1MutBattery — C1 fence mutation candidates

Axes: calibration (R49-C1); mutation-floor coverage for the candidate fence. This is a mutation-authoring/apply check only; it does not admit either claim.

## Freeze and candidate

- Stage-1 freeze verified in the lane tree before any measurement: commit `9d2900af41e4d1fc6022eff99010436fde6dbd93`, authored `kengaku-shokunin`, dated `Tue Oct 27 09:58:06 2026 -0300`; it is an ancestor of lane HEAD `af88aab193e6034cb9b386472064e3c18fa90128`.
- Read, in full, `plans/round-49-claims.md` and `corpus/lessons/round-48-verifier-spotcheck.md`; read the round-48 lesson for the described fence mutation weaknesses.
- Candidate source: §7 diff from `.ufo/waves/round-48/w1/R48C1ExecFenceA.md`, applied to the frozen-base `plans/fixture_fence.py`. Candidate SHA-256: `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` (810 lines). The frozen-base source SHA-256 before patch: `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.
- Candidate patch application output: `apply-check exit=0`; `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52  fence_candidate.py`; `810 fence_candidate.py`; `candidate parses OK`.

## Deliverable

`R49C1MutBattery.c1-mutants.json` in this same wave directory contains 23 rows with inline unified-diff payloads, payload SHA-256, resulting mutant SHA-256 (`digest`), mutation class, and expected effect. Bundle SHA-256: `2e5cfe6622c5d1497570724939b1346f15d80ed4b978e5fcaee925bb8b5ff865`.

Mutation classes cover deleted checks, weakened checks/allowlists, comparison changes, and reordered checks. Targets include gitdir/commondir redirects, symlinks, device and hardlink boundaries, object-info redirects, config parsing/allowlists, path containment, HEAD/ref validation, required store entries, argv checks, hook names, commit-graph validation and lane membership. Mutant 13 (ENTRY_CAP 20) specifically probes honest over-refusal, complementing the hostile-admission mutants.

## Exact commands and observed outputs

1. `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git log -1 --format='%H %an %ad %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93 && git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD`

   Verbatim: `commit`; `9d2900af41e4d1fc6022eff99010436fde6dbd93 kengaku-shokunin Tue Oct 27 09:58:06 2026 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`; `freeze is ancestor of HEAD`.

2. Applied the R48 §7 diff with `git -C "$D" apply --check` and `git -C "$D" apply` in the scratch clone after asserting `git rev-parse --show-toplevel` equals `$D`. Verbatim outputs: `apply-check exit=0`; `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52  fence_candidate.py`; `810 fence_candidate.py`; `candidate parses OK`.

3. Ran `./check_patches.sh` in scratch. It asserted the clone top-level, reset the candidate file for each payload, ran `git -C "$D" apply --check` then `git -C "$D" apply`, and compared resulting SHA-256 against the independently generated mutant bytes. Verbatim summary: 23 `APPLY_OK <id> sha256=<digest>` rows, IDs `c1-mut-01-gitdir-file` through `c1-mut-23-gitdir-repo-reorder`; all 23 passed. The exact per-row outputs and digests are recorded in the JSON's `digest` fields.

4. Validated the published JSON: `JSON_VALID rows=23; payload hashes=23/23; mutated fence hashes=23/23`; bundle digest as above.

## Detector, restoration, limits

No scored C1 counter/probe was run: the stage-2 counter and frozen mutant population do not exist at this stage, and this item is limited to authoring/apply verification. Thus no killed/survived behavioral verdict is claimed; per-mutant `expected_effect` is a prospective detector expectation, not observed behavior. The bounded detector executed here was clean patch application plus exact mutated-byte digest comparison for all 23 candidates.

The scratch clone's `plans/fixture_fence.py` was restored to the exact frozen-base byte value after the patch checks: SHA-256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. Scratch tree removed before yield. No external source URL was opened; therefore no URL/access-date/quote applies.

VERDICT: 23 byte-level candidate mutants authored; all 23 patches apply cleanly to the §7 fence candidate and produce their recorded digests. No claim admission or scored counter result is asserted.
