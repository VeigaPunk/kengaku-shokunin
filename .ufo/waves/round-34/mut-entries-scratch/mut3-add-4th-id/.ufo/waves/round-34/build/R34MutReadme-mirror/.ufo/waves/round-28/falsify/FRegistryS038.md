# FRegistryS038 — author-side falsification of row S038 under the frozen13/35 literal contract

Seat: KengakuR28.FRegistryS038 · 2026-10-21 · Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only over production; all mutations in own scratch).
Scope: row S038 only, per plans/round-28-claims.md C2 (:9), M65 (:33), F4/F5 (:40–41), delta partition (:52). No whole-registry truth and no whole-current-tree claim is made.

## Claim under test

C2 freezes literal source-reference coverage for exactly S038 and S049–S060 across the 35 knowledge paths of `plans/fixtures/r28/registry/population.json`; the M65 repair counts only if the delivered checker fails on the baseline and passes with allowed-cell repair as the only delta. My job was to break this for S038 specifically, deriving everything independently (no production import), then comparing with delivered per-row output.

## Inputs verified (my own hashing, no production oracle imported)

- `plans/fixtures/r28/registry/population.json` sha256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` — equals the pin in `plans/registry_check.py:10`; `base_revision` = `b9b24796277020d1b9b01923b45313d6a565e664`.
- Baseline `corpus/SOURCES.md` blob @ b9b2479 sha256 `b1a74eb5f1cdbefa8e055cfee79dda7894a4b00a611788c3798140596258c62e` — equals delivered `original_sources_sha256` in `corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json`.
- Current worktree `corpus/SOURCES.md` sha256 `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1`. This deliberately differs from the export digest below: the live tree also carries C1 rows S061–S066 and round28 sections; byte identity was tested against the C2 export, which I reconstructed myself.

## Expected-before (baseline bytes @ b9b2479, frozen13/35)

- S038 row cells: kind `paper`, tier `A`, **status `queued`**, **used-by `—`** (empty).
- Literal citation set (my regex `(?<![A-Za-z0-9_])S038(?![A-Za-z0-9_])` over exactly the 35 frozen paths): `{corpus/knowledge/attribution-interval-calibration.md}` — 1 mention, prose line 144 of the baseline blob.
- S038 findings: `cited_not_mined` (status queued) + `missing_used_by` (that path). Enum valid; no duplicate/malformed row.

## Current-after (live tree, delivered checker rerun read-only with bytecode disabled)

- S038 row cells: **status `mined`**, **used-by `corpus/knowledge/attribution-interval-calibration.md`**; citing set unchanged as a set — the same single file, now 2 mentions (prose lines 144 and 193; the second is the round28 S066-supersession erratum, same file, so it adds no new reference link: `reference_links` stays 12).
- S038 findings: none; `missing_used_by: []`. Live `python3 -B plans/registry_check.py --json` exit 0; its S038 entry is cell-for-cell identical to my independent map and to delivered `registry-current.stdout`.
- Baseline→current S038 row cell diff: exactly `{status: queued→mined, used_by: —→path}`. No other cell (source/kind/tier/scope/anchor/teaches/opened/recheck) moved — "opened/recheck unchanged" verified for this row.

## Exact effective denominator

13 source rows checked × 35 frozen knowledge files scanned; `reference_links` = 12 (baseline and current both), of which S038 contributes exactly 1 row-file link. S038's `missing_used_by` obligation denominator = 1 required path; used-by supplies exactly that 1 entry; citing set = used-by set (subset confirmed exact).

## Acceptance experiment (scratch copies only: `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS038/exp/`)

Reconstructed exports from baseline blobs (35 knowledge files + permitted used-by liveness file `corpus/lessons/round-27.md` + pinned population), mutated only in-row:

| Variant | SOURCES sha256 | exit | findings |
|---|---|---|---|
| A baseline | `b1a74eb5…` (= delivered original) | 1 | 3: S038 cited_not_mined + missing_used_by; S050 missing_used_by |
| B = A + S050 used-by only | `a06b7f65…` (= delivered s050-only) | 1 | 2: both S038 — **stays red on S038** |
| C = B + S038 status/used-by | `66e2235e…` (= delivered both) | 0 | 0 — **green** |
| D = A + S038 delta only | `ef70b2e6…` (my extra probe) | 1 | 1: only S050 missing_used_by; S038 row itself green |

All three delivered export digests reproduce byte-exactly from baseline + exactly the allowed-cell edits, so no hidden third cell participates in the green. D isolates the S038 effect: its row clears while the residual red is exactly the out-of-scope S050 repair. This matches delivered `registry-baseline-red.stdout` (3), `registry-s050-only-red.stdout` (2), `registry-s038-only-delta-green.stdout` (0) finding-for-finding.

## Row-specific falsifier (attempted, did not fire)

**Falsifier:** if any of the other 34 frozen knowledge paths contained a standalone literal `S038`, the single-entry used-by would be incomplete (`missing_used_by` non-empty) and both the current green and the C-variant green would be false. Exhaustive per-file scan of all 35 paths: standalone `S038` occurs only in `corpus/knowledge/attribution-interval-calibration.md` (baseline ×1 line 144; current ×2 lines 144, 193; both prose, zero fenced hits — and the checker counts fenced mentions anyway via whole-file scan). Near-miss tokens (`OpenS038`, `XS038`, `S038x`) correctly do not match. Falsifier does not fire; the used-by subset is exactly complete.

## Reference-class confirmations for S038

- **Missing references:** none — citing ⊆ used-by.
- **Corrective references:** the line-193 mention indexes the S066 supersession erratum inside the already-covered file; as a literal reference it is counted (contract counts all standalone mentions) but creates no new obligation; S066/S058 remain controlling, and no support for the superseded fix clause is claimed here.
- **Code references:** S038 is a paper row; no code-kind row and no fenced-block mention of S038 exists in the frozen set.
- **Status:** `queued→mined` is an allowed mutable cell; it is exactly what clears `cited_not_mined`.
- **Subset used-by:** exactly one entry, byte-equal to the citing path; liveness holds in the live tree and in every scratch root where the export includes the permitted lesson file. Note for L1: export green additionally depends on used-by path liveness (`corpus/lessons/round-27.md` must exist in the audited root) — satisfied in the live tree and, byte-reproducibly, in the delivered exports.

## Not claimed / boundaries

Already-disclosed drift (round-27 lesson :18–20, round-28 M65) is confirmed, not re-claimed as discovery. Findings for S038 are limited to the frozen literal contract; citation truth (whether the paper supports the teaching) is out of scope. S050's corrective-index reversal is disclosed, not treated as source support. No production file was mutated; no subagents; no tools installed or updated; all probes ran with bytecode disabled.

VERDICT: PASS
