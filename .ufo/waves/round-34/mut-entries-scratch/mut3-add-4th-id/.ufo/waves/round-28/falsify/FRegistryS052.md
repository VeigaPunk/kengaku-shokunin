# FRegistryS052 — independent falsification of registry row S052 under the frozen13/35 literal contract

Seat: KengakuR28.FRegistryS052 · 2026-10-21 · lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Baseline master `b9b24796277020d1b9b01923b45313d6a565e664` · population `plans/fixtures/r28/registry/population.json` (13 IDs, 35 knowledge paths, pin sha256 `1a5073fc…3014`).
Scope: row S052 only. No whole-registry truth, no whole-current-tree consistency claim, no semantic citation-support claim.

## Method

- Independent derivation from raw bytes with a self-written parser (own Registry-section/fence logic, own regex from `population.json.reference_pattern`); no production import, no `registry_check` import before derivation. Baseline files read via read-only `git cat-file -p b9b2479…:path` (no index/jj mutation); final files read from the worktree.
- Delivered checker run once read-only: `PYTHONDONTWRITEBYTECODE=1 python3 plans/registry_check.py --json` (bytecode disabled), cwd lane root, exit 0, empty stderr.
- Falsifier/boundary probes ran only on a scratch replica under `.ufo/waves/round-28/scratch/FRegistryS052/replica/`; production files were only read, never edited. No installs; no pacman.

## Row S052 — expected-before (baseline b9b2479) vs current-after (final worktree)

Independent derivation:

| facet | expected-before (baseline) | current-after (final) |
|---|---|---|
| row bytes | `mined` / docs / A; used-by `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md` | identical (0 changed cells across all 11 columns); row line sha256 `f5c7ef8c652c6e1554d03abc1427ab1b6be9e93e0acb68e2a9adab3eef4d30da` |
| citing frozen paths | `corpus/knowledge/extraction-policy-comparison.md` | same |
| missing/corrective/code refs | none: citing ⊂ used-by (extra `corpus/lessons/round-27.md` is the allowed non-frozen used-by path, outside the 35); 32 standalone `S052` occurrences in extraction-policy-comparison.md, at line 1 (source header) and line 49 (`E7/E8 use Python's decoder primitive (S052)`) — not corrective: the line-18 S050 corrective sentence `(S058, correcting S050)` contains no S052 | same |
| status | `mined` | `mined` |
| findings for S052 | none | none |

Delivered per-row output (checker `--json`) equals the independent map exactly: `{"source":"S052","status":"mined","citing_files":["corpus/knowledge/extraction-policy-comparison.md"],"used_by":["corpus/knowledge/extraction-policy-comparison.md","corpus/lessons/round-27.md"],"missing_used_by":[]}`. Whole-run context also agrees: 13 rows / 35 paths / `reference_links`=12 / 0 mismatched / 0 findings, exit 0.

## Exact effective denominator (independently reproduced)

- `reference_links` = **12**, identical at baseline and final (per `(row, file)` links, not raw mentions).
- All 12 links live in exactly 2 files: `extraction-policy-comparison.md` (11: S049–S059 incl. S050's corrective mention) and `attribution-interval-calibration.md` (1: S038). 33 of 35 paths are zero-reference controls.
- S060 is the only uncited frozen ID (0 links); 13 rows checked, 12 cited — M72's 12-vs-13 conflation correction independently confirmed. S052 contributes exactly 1 of 12.
- Baseline red independently reproduced as exactly 3 findings (S038 status/used-by ×2, S050 missing-used-by ×1) — the already-disclosed rows; not re-claimed as discovery. S050's used-by addition stays a literal corrective index, not endorsement of the superseded reason (S058 controls); S038's drift remains previously disclosed. Neither touches S052.

## Row-specific falsifier (failure-capable, scratch-only)

**Primary — FA: drop `corpus/knowledge/extraction-policy-comparison.md` from S052's used-by cell** in the scratch replica: checker exits 1 with finding `{"id":"missing_used_by","source":"S052","path":"corpus/knowledge/extraction-policy-comparison.md"}` while links stay 12. The contract is keyed to S052's own cell and fails when broken.

Boundary confirmations (same replica, restored between runs):
- **FB**: S052 status `mined`→`queued` → exit 1, `cited_not_mined` on S052.
- **FC2**: all 32 standalone `S052` mentions neutralized to `S052x` → exit 0, S052 citing empty, links 12→11, no finding (no false-positive count; exact decrement).
- **FD2**: a fenced code block containing `S060` added to extraction-policy-comparison.md → exit 1, links 12→13, S060 gains `missing_used_by`+`cited_not_mined` (status `rejected`) — literal counting includes code fences, and S052 is unaffected.

Raw probe receipts: `scratch/FRegistryS052/probe-*.json`, `independent-derivation.json`, `delivered-current.json`, `row-byte-evidence.json`.

## Exclusions checked

S052 absent from `attribution-interval-calibration.md`, from the round28 drafts dir (0 matches; candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` is an excluded new file), and from any non-frozen knowledge path; `corpus/lessons/round-27.md` appears only as the allowed extra used-by path, not as a frozen citing file.

## VERDICT: PASS

Row S052 fully satisfies the frozen13/35 literal contract expected-before and current-after: row bytes unchanged across the round, exactly one citing frozen path covered by its used-by, status `mined`, zero findings, and the delivered checker's per-row output is byte-equal to the independent derivation. The falsifier proves the check failure-capable and S052-keyed. No contract violation found; nothing to repair on this row.
 
## Dated correction — 2026-10-21 (count units)

The original report text above is preserved. Its phrases “32 standalone `S052` occurrences” (table) and “all 32 standalone `S052` mentions” (FC2) are incorrect: **32** was the count of all standalone `S[0-9]{3,}` tokens in the final `extraction-policy-comparison.md`, across multiple IDs, not the S052-specific count. Direct raw-text recount (no checker rerun) finds exactly **2 standalone S052 occurrences** in that file in both baseline and final, at final lines 1 and 49. The final file has 32 standalone S-ID tokens total; the baseline file had 21 total. FC2 neutralized all **2** S052 occurrences, yielding the already-recorded result: S052 citing empty and links 12→11. The per-row/file link remains exactly 1/12; S052 status, missing-used-by, findings, delivered-checker comparison, and VERDICT are unchanged.
