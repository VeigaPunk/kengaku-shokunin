# FRegistryS050 — Independent falsification of registry row S050 (frozen13/35 literal contract)

- Seat: `KengakuR28.FRegistryS050` · Date: 2026-10-21 · Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- Baseline pin: `b9b24796277020d1b9b01923b45313d6a565e664` (round-27); population SHA256 `1a5073fc…813014` re-verified on disk.
- Method: independent re-derivation from the frozen population contract (scratch scanner `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS050/independent_scan.py`, written from scratch, does NOT import `plans/registry_check.py`); delivered lane checker run read-only with bytecode disabled (`PYTHONDONTWRITEBYTECODE=1`); three scratch-root falsifier experiments. No production file mutated; no upstream code executed; no network contact.

## Expected-before (baseline `b9b2479`)

- S050 row (baseline `corpus/SOURCES.md:72`): `kind=code`, `tier=A`, `status=mined`, used_by = `corpus/lessons/round-27.md` **only**. All other 10 cells byte-identical to current (verified by cell-split diff of the full row line).
- Baseline citing set for S050 (independent scan of the 35 frozen knowledge files at `b9b2479`): {`corpus/knowledge/extraction-policy-comparison.md`} — the file's line 18 already contained the corrective mention at baseline.
- Baseline checker state (scratch root rebuilt from `git show b9b2479:<file>` for SOURCES.md + all 35 knowledge paths, population bytes pinned): `source_rows_checked=13`, `knowledge_files_expected=35`, `reference_links=12`, **mismatch_sources=2, finding_count=3**:
  - `cited_not_mined S038 (status=queued)`
  - `missing_used_by S038 / corpus/knowledge/attribution-interval-calibration.md`
  - `missing_used_by S050 / corpus/knowledge/extraction-policy-comparison.md`

## Current-after (working tree)

- S050 row (line 72, inside `## Registry` lines 19–89; file contains zero fences; S050 appears in SOURCES.md only at line 72 and inside S058's corrective row title at line 80 — SOURCES.md is not scanned for citing): sole delta vs baseline is the used_by cell → `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. Status `mined`, tier/kind enums valid; both used_by paths exist on disk.
- Independent citing set for S050 across the 35 frozen knowledge files: {`corpus/knowledge/extraction-policy-comparison.md`} (regex-equivalent grep cross-check agrees). Missing = ∅.
- **Delivered checker vs independent derivation: identical.** Delivered (`plans/registry_check.py --json`, exit=0): 13/35/12 links, mismatch_sources=0, finding_count=0; S050 entry `{citing: [extraction-policy-comparison.md], used_by: [extraction-policy-comparison.md, lessons/round-27.md], missing_used_by: []}`. My scanner reproduces the same totals and the same S050 entry exactly.

## Exact effective denominator

13 frozen source rows × 35 frozen knowledge files; 12 reference links total across the registry. For S050 specifically: 1 citing file, 2 used_by entries (one of which, `corpus/lessons/round-27.md`, is a permitted non-scanned lesson path per the population note), 0 missing, 0 findings. S050 contributes exactly 1 of the 12 reference links.

## Reference-type confirmation

- **Missing references:** none. No `missing_used_by`, `used_by_missing`, `knowledge_missing`, or `source_missing` touches S050.
- **Corrective reference:** `corpus/knowledge/extraction-policy-comparison.md:18` (read 2026-10-21): "inspect_ai `pattern()` (S058, correcting S050) takes a first regex hit" — and the file's own disclosure at lines 123–127 (read 2026-10-21): "S050 occurs above only as the superseded reason corrected by S058" … "it does not revive S050 as support for the inaccurate blanket no-hit reason. S058 remains the authority for that behavior." Confirmed: the S050 mention is corrective-index discoverability only and is **not** support for S050's superseded blanket no-hit reason; S058 (row line 80, same pinned blob `63e45cc`, used_by both paths) controls. This reversal is disclosed, per contract — I do not count it as support.
- **Code references:** S050 row is `kind=code`/`tier=A` pinned to `https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py` with anchors `pattern() :62–64, :77–79, :119–124`. No pinned local inspect_ai fixture exists under `plans/fixtures/` and contacting the site is prohibited, so line-content truth of those anchors is outside my offline falsifiable scope; at the registry level the commit pin, enums, and recorded anchor references are present and valid. Boundary noted, not claimed verified.

## Row-specific falsifier

Scratch root = exact copy of current tree (population bytes pinned, checker copy). **Reverting only S050's used_by cell to its baseline value** (every other byte current) reproduces exactly one finding: `missing_used_by S050 / corpus/knowledge/extraction-policy-comparison.md` (mismatch_sources=1, finding_count=1). Therefore S050's current green state is solely load-bearing on that single used_by delta; any claim that S050 was already green at baseline, or that `corpus/lessons/round-27.md` alone satisfies the literal contract, is falsified by direct observation.

Complement (insufficiency direction): baseline SOURCES.md + only S050's delta (scratch `root-s050only`) leaves the harness red solely on S038 (`cited_not_mined queued` + `missing_used_by attribution-interval-calibration.md`; mismatch_sources=1). S050's delta alone cannot green the harness; only S038's status/used-by delta does. This matches the disclosed C2 boundary; S038's drift itself is already-disclosed and owned by `FRegistryS038`, reported here only as the insufficiency control.

## Verdict

Every in-scope S050 claim survived falsification: delivered per-row output matches my independently derived map byte-for-byte on the S050 entry; the baseline→current delta is exactly one used_by cell and is necessary and, for S050, sufficient; the corrective-index reversal is explicitly disclosed and not used as source support; the superseded-reason authority is S058. Out-of-scope residue: inspect_ai line-content truth (no offline fixture, network prohibited — boundary, not a defect under the literal contract).

**VERDICT: PASS**

## Scratch evidence index (`.ufo/waves/round-28/scratch/KengakuR28.FRegistryS050/`)

- `independent_scan.py` — from-scratch scanner (no production import)
- `delivered-current.json` — delivered checker output, current tree (bytecode-disabled run)
- `root-baseline/` — full baseline rebuild (SOURCES.md + 35 knowledge files from `git show b9b2479`), checker result: 2 mismatch sources / 3 findings
- `root-s050only/` — baseline + S050 used_by delta only: red solely on S038
- `root-s050revert/` — current tree with S050 used_by reverted: exactly one S050 `missing_used_by` finding
- `s050-baseline-line.txt`, `s050-current-line.txt` — row-line diff proving the single-cell delta

No tools were installed or updated (none needed; pacman transactions untouched).
