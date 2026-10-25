# FRegistryS049 — independent frozen-literal audit

Seat: `KengakuR28.FRegistryS049` · date: 2026-10-21 · axis: calibration (C2)

## Scope and method

Tested **S049 only** against the frozen population `plans/fixtures/r28/registry/population.json` (base revision `b9b24796277020d1b9b01923b45313d6a565e664`; population SHA-256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`). I independently parsed the baseline and final `corpus/SOURCES.md` rows and scanned the 35 listed knowledge files with the manifest's standalone-ID boundary rule. The derivation used only direct file/archive reads and a locally written scanner/parser; it did not import the production checker or any alternate oracle. Both row parses had no malformed/duplicate findings. The checker comparison used `python3 -B` (bytecode disabled), read-only.

For expected-before, I exported commit `b9b2479` to my seat scratch and overlaid the delivered checker and the pinned population, which postdate that baseline commit. The resulting baseline `corpus/SOURCES.md` SHA-256 was `b1a74eb5f1cdbefa8e055cfee79dda7894a4b00a611788c3798140596258c62e`, exactly matching `corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json`'s `original_sources_sha256`; the population digest also matched its recorded pin. The export and derived JSON are retained only under `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS049/`.

## Expected-before — baseline b9b2479

S049 is a well-formed 11-cell row at `corpus/SOURCES.md:71`: kind `code`, tier `A`, status `mined`, opened `2026-10-21`, recheck `2027-01-19`, and used-by `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. Its row cells exactly match the final row.

Independent scan of the frozen 35 paths found S049 in exactly one file: `corpus/knowledge/extraction-policy-comparison.md` (literal mentions at lines 1 and 17; both outside fences). Thus S049 contributes one row-file link, its frozen citing path is included in used-by, and `missing_used_by=[]`. `corpus/lessons/round-27.md` is an additional live used-by lesson path, outside the 35-path scan; the population explicitly permits additional lesson used-by paths. Status `mined` satisfies the cited-row condition. No S049 finding was present in the recreated baseline checker output.

## Current-after — final tree

The S049 row at `corpus/SOURCES.md:71` is byte-for-byte identical in all 11 cells to baseline. The same frozen knowledge path cites it; current literal mentions are at lines 1, 17, and 118, all outside fences. The appended line 118 is the S049 source-location correction in the round-28 errata. It adds no new citing **file**: the S049 citing-file set remains exactly `{corpus/knowledge/extraction-policy-comparison.md}`. The same single frozen link is covered by used-by; the lesson path remains a permitted additional entry. Status stays `mined`; no missing used-by, unsafe/missing used-by path, invalid enum, or row-shape discrepancy was observed. The date interval is exact: 2026-10-21 + 90 days = 2027-01-19.

The knowledge edit is append-only: the diff from baseline adds 24 lines and removes none. Its original header still records `extraction.py:25,47–49` (line 1); the appended erratum says the `:25` location is superseded by `:27` for `group_select: int = 0`, while `:47–49` remains operative. The row's existing `:27` anchor is unchanged. The author-side `build/OpenS049.md` receipt records the reopened pinned file's SHA-256 and quotes line 27 as `group_select: int = 0,`; this is contextual source provenance, not a claim that the literal registry check establishes citation truth. Round-27 lesson history was unchanged from baseline.

## Exact effective denominator and checker comparison

- Frozen population: **13 source rows × 35 knowledge paths**.
- S049-specific effective missing-index denominator: **35 paths**; **1** citing path, **34** paths without an S049 mention, **1** row-file link, **0** missing used-by paths.
- Whole frozen matrix (counter only, not a truth claim): baseline and final each independently yield **12 row-file links across 12 cited rows**; S060 is the one uncited row. No frozen-ID citing-file set changed between the two scans.
- Recreated baseline checker: exit 1; 13 rows, 35 paths, 12 links, 2 mismatch rows / 3 findings. Those findings concern S038 (queued plus missing used-by) and S050 (missing used-by); the S049 per-row output is clean.
- Final checker: exit 0; 13 rows, 35 paths, 12 links, 0 mismatches / 0 findings. Its S049 record (`status=mined`, citing file above, used-by paths above, `missing_used_by=[]`) exactly matches my independent derivation.

This reports only the frozen13/35 contract. It makes no claim about whole-registry truth, semantic support, or whole-current-tree consistency. S050's corrective-index reversal is not support for its superseded reason; S058 remains controlling. The already-disclosed S038 drift is not a new S049 finding.

## Row-specific falsifier tested

**F049-1:** the appended corrective S049 mention at `corpus/knowledge/extraction-policy-comparison.md:118` would falsify S049's literal index if it landed in a frozen file absent from `used_by` (or otherwise created an uncovered S049 citing path). It did not: that same file already cited S049 at baseline lines 1/17 and is listed in used-by; after the append it remains the sole citing frozen path. Both the independent map and delivered checker report `missing_used_by=[]`. This is a concrete attempted falsification, not an assertion of semantic endorsement.

## Verdict

**VERDICT: PASS** — S049 survives the assigned frozen13/35 literal-reference falsification. Expected-before and current-after per-row maps agree; no S049 status, missing-reference, or used-by defect was found.

Report path: `.ufo/waves/round-28/falsify/FRegistryS049.md`
