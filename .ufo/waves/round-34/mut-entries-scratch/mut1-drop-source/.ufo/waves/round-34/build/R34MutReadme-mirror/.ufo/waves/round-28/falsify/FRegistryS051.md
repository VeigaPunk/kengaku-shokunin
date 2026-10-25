# FRegistryS051 — frozen literal-reference falsification

## Scope and verdict

This review covers **S051 only**, under the pinned frozen13/35 literal-reference contract. It checks registry-row presence/status, literal source mentions in the frozen knowledge paths, the row's `used_by` coverage, and cited-path liveness. It does **not** verify upstream source semantics, citation truth, or whole-registry/whole-current-tree consistency.

## Independent derivation and evidence chain

- Read `plans/fixtures/r28/registry/population.json` directly and checked its SHA-256 against the instrument pin: `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`. It pins base revision `b9b24796277020d1b9b01923b45313d6a565e664`, 13 IDs including S051, 35 exact knowledge paths, and regex `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`.
- Read `plans/registry_check.py` lines 25–86 for the literal registry-table parse, path scan, status/enum and `used_by` checks. The independent map below was derived directly from the pinned Git tree and current files with the population regex; no production module was imported for that derivation.
- At baseline `b9b24796277020d1b9b01923b45313d6a565e664`, `corpus/SOURCES.md:73` contains S051 as a `code` row, status `mined`, with `used_by` exactly `corpus/lessons/round-27.md` and `corpus/knowledge/extraction-policy-comparison.md`. Both listed paths exist in that baseline tree.
- Baseline frozen-path scan: S051 has one distinct source/path link, `corpus/knowledge/extraction-policy-comparison.md`. There are two literal S051 token occurrences there (lines 1 and 21), but the instrument counts a source/path pair once. No S051-specific `source_missing`, `cited_not_mined`, or `missing_used_by` condition is present.
- Current `corpus/SOURCES.md:73` has the same S051 row cells as baseline; status remains `mined`, kind `code`, and both `used_by` paths exist. Current frozen-path scan still yields exactly one distinct S051 link, to `corpus/knowledge/extraction-policy-comparison.md`. That file now has three standalone S051 tokens (lines 1, 21, and 135); the added line 135 is an exception-handling qualification, not an additional source/path link. The used-by list already covers this frozen path.

## Expected-before / current-after per-row result

| Observation | Baseline before | Current after |
|---|---|---|
| S051 row | Present at `SOURCES.md:73`; `mined`; `code` | Same cells and status |
| Frozen S051 citations | `extraction-policy-comparison.md` only | Same file only |
| `used_by` | Lesson plus the cited knowledge file; both live | Same two paths; both live |
| S051 row findings | None expected: not missing, not queued, no uncovered frozen citing path | None: `missing_used_by=[]`; no S051 finding |

The additional `corpus/lessons/round-27.md` used-by path is outside the frozen35 knowledge-path denominator, but it is permitted as an additional used-by entry and is live. The S051 source cell records the OpenAI evals `json_match.py` URL and `eval_sample` anchors `:76, :80–83`; this is a code-reference observation, not an independent source-truth finding.

## Exact effective denominator

The pinned scan covers 13 source IDs × 35 knowledge paths = **455 candidate ID/path checks**. Its effective positive-link count is **12 distinct source-ID/path links**, not 13 row/file pairs; those links occur in two frozen knowledge files. For S051 specifically, the denominator is **one distinct frozen citing path / one observed S051 link**, with that path present in `used_by` (1/1 covered). The other 34 frozen paths contribute no S051 link. Repeated tokens in one file do not increase the link count.

The delivered read-only current CLI, run with `PYTHONDONTWRITEBYTECODE=1`, agrees: `source_rows_checked=13`, `knowledge_files_expected=35`, `reference_links=12`, `finding_count=0`; its S051 record has `status=mined`, the single citing file above, and no missing used-by path. This is only the instrument's bounded literal result.

## Row-specific falsifier

I made an isolated counterfactual copy under `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS051/missing-used-by-counterfactual/`, retaining the pinned population and current knowledge files, then changed only S051's `used_by` cell to omit `corpus/knowledge/extraction-policy-comparison.md`. The read-only checker returned exit 1 with exactly one finding: `missing_used_by`, `source=S051`, `path=corpus/knowledge/extraction-policy-comparison.md` (while `reference_links` remained 12). This is a row-specific falsifier for the coverage claim: omitting S051's sole frozen citing path makes the contract fail. It is a counterfactual control, **not** a finding against the current row; production files were not changed.

## Separation and limits

The S050 corrective-index reversal in `extraction-policy-comparison.md:18–22` is a distinct S050/S058 matter and provides no support for S051. The new S051 exception-handling qualification at line 135 is separately counted as a literal mention within the already-indexed file. S038's previously disclosed drift is not a new S051 finding. No semantic equivalence, endorsement, or whole-registry result is claimed.

**VERDICT: PASS** — S051's current row is complete under the frozen13/35 literal contract; no S051-specific mismatch was found.