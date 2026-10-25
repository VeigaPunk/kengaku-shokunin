# FRegistryS057 — row S057 falsification under the frozen13/35 literal contract

Seat: KengakuR28.FRegistryS057 (leaf member, no subagents). Date: 2026-10-21.
Scope: row **S057 only**. Baseline = lane master export `b9b24796277020d1b9b01923b45313d6a565e664`;
final = current working tree. No production import in derivation: map derived by my own stdlib parser
(scratch `FRegistryS057/derive_s057.py`) from population.json + both `corpus/SOURCES.md` + both trees of
the 35 frozen knowledge paths. Production untouched; all mutations were scratch-only. No tool installs.

## Inputs verified

- `plans/fixtures/r28/registry/population.json` sha256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` — matches the checker's pinned `POPULATION_SHA256`. 13 source_ids (S038, S049–S060), 35 knowledge_paths.
- Baseline `corpus/SOURCES.md` (git object `b9b2479…`, exported read-only via `git archive` to scratch) sha256 `b1a74eb5f1cdbefa8e055cfee79dda7894a4b00a611788c3798140596258c62e`; final `corpus/SOURCES.md` sha256 `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1`.
- Baseline registry parses 60 source rows; final parses 66 (+6 = new rows S061–S066, outside frozen13; not my row). No duplicate or malformed S057 row in either.

## Expected-before (baseline export) vs current-after (final tree) — row S057

S057 row sits at line 79 in both files and is **byte-identical in all 11 cells** (per-cell diff empty):

- source `xFinder extraction-method comparison — https://arxiv.org/abs/2405.11874`; kind `paper`; tier `A`; status **`mined`** before and after; opened `2026-10-21`; recheck `180d`.
- used_by cell (identical before/after): `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. Both files exist in both trees; the lesson path is the allowed additional lesson used-by (lesson lines 50, 119, 201 mention S057; it is not one of the frozen35, by design).
- Literal citing set over the frozen35: exactly `corpus/knowledge/extraction-policy-comparison.md` in **both** trees — citing set identical before/after; citing ⊆ used_by holds in both. 3 standalone mentions each (file lines 1, 16, 24), none inside code fences, e.g. line 16: “xFinder (S057, reopened this round) already measures”.
- S057 contributes exactly 1 of the population's 12 reference links, before and after.

Missing/corrective/code references for this row:

- No corrective mention pattern attaches to S057 (that is S050/S058: line 18 “S058, correcting S050”). S057's three mentions are substantive prior-art citations.
- The round28 errata append to `extraction-policy-comparison.md` (+24 lines, current lines 115–138) mentions S049/S050/S058/S051/S054/S059/S064/S065 but **not S057** — my full-tree scan confirms total S057 mentions in the frozen35 stay 3 before/after. So Amendment 1 §5's “calibration errata add no new reference edge to any frozen13 ID” holds for S057 specifically.
- S057's own teaches cell references S044, which is outside frozen13; the population intersection excludes it (regex counts it in the file, `refs.keys()` filter drops it). No effect either way.
- S038's drift (baseline findings `cited_not_mined` + `missing_used_by`) and S050's baseline `missing_used_by` are the already-disclosed drifts; they are not rediscovered here, and S050's corrective-index reversal is not treated as support for its superseded reason. Row S057 has **zero findings at baseline and at final** in the delivered receipts (`registry-baseline-red.stdout`, `registry-current.stdout`) and in my own map.

## Delivered checker vs independent map

Ran `python3 -B plans/registry_check.py` (bytecode disabled, read-only): current `--summary` exit=0, `source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0`; `--json` S057 block = status `mined`, citing `[corpus/knowledge/extraction-policy-comparison.md]`, missing_used_by `[]`, used_by both paths — **equal to my independently derived current map in every field**, and equal to the delivered receipts. My baseline map likewise equals the delivered baseline receipt's S057 block.

## Exact effective denominator

Population fixed at 13 source rows × 35 frozen knowledge paths = 455 row/path pairs; literal reference
links across the whole frozen population = **12, before and after** (S060 uncited, so 12 cited IDs over
13 rows — consistent with M72's correction). Row S057's effective denominator: 35 scanned frozen paths,
exactly 1 positive path, 3 literal mentions, contributing exactly 1 of the 12 links, unchanged by the
round28 delta.

## Row-specific falsifier (demonstrated, scratch `FRegistryS057/falsifier-root/`)

Verbatim copies of population + SOURCES.md + all 35 frozen paths + `corpus/lessons/round-27.md`:

1. Control: checker `--root falsifier-root` → exit 0, 12 links, 0 findings (copy is faithful).
2. **Falsifier**: revert only S057's used_by knowledge path (line 79 `…, corpus/knowledge/extraction-policy-comparison.md` → `corpus/lessons/round-27.md`) → exit **1**, exactly one new finding `{"id": "missing_used_by", "path": "corpus/knowledge/extraction-policy-comparison.md", "source": "S057"}`. The S057 check is failure-capable and row-isolated.
3. Mention arm (boundary characterization): the check is file-level set semantics — destroying 1 of 3 mention tokens stays green; destroying all 3 drops `reference_links` 12→11 with **no finding**, because the contract is a subset check (citing ⊆ used_by) and over-inclusive used-by is unflagged by design. Losing S057's citation is therefore visible only in the link count, not as an error; losing the used-by cell entry is the red arm.
4. Restored copy → exit 0, 12 links; scratch files byte-identical to production copies afterwards.

## Conclusion

Row S057: zero expected-before/current-after divergence in status, used-by, citing set, or mention
inventory; delivered per-row output equals the independent derivation; the row-level check is shown
failure-capable. No missing, corrective, or code-reference drift exists for S057. Findings scoped to this
row only — no whole-registry truth claim, no whole-current-tree claim.

VERDICT: PASS
