# FRegistryS053 — falsification of row S053 under the frozen13/35 literal contract

Seat: KengakuR28.FRegistryS053 (leaf, no subagents). Round28 fresh falsification wave.
Scope: row **S053** only, over population `plans/fixtures/r28/registry/population.json`
(sha256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`, pin verified before any
derivation), 13 source rows S038, S049–S060, 35 knowledge paths, baseline `b9b24796277020d1b9b01923b45313d6a565e664`.
No whole-registry truth claim, no whole-current-tree claim. All writes confined to
`.ufo/waves/round-28/scratch/KengakuR28.FRegistryS053/` and this report. No installs, no network,
no browser, no upstream execution, no production edits.

## Method

- Independent re-derivation from the frozen contract text (11-column `## Registry` table, fenced-block
  skip, standalone `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` mentions in the 35 frozen knowledge
  paths, used_by comma/semicolon parse with backtick strip, citing ⊆ used_by, used_by liveness,
  status/tier/kind enums, cited-implies-mined). Script `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS053/census_s053.py`
  imports no production module (bytecode disabled, `python3 -B`).
- Expected-before from my own `git archive b9b2479… -- corpus` export into scratch (read-only; no jj
  commands, no index writes). Current-after read from the working tree.
- Delivered checker compared read-only on: my baseline export, the current tree, and four scratch
  variants (below): `python3 -B plans/registry_check.py --root <tree> --json`.

Self-disclosed false start: my first baseline export extracted only `corpus/SOURCES.md` +
`corpus/knowledge`, which spuriously reported `used_by_missing corpus/lessons/round-27.md` for
S049–S060 (the lesson file was simply absent from my scratch copy). Re-extracted the full baseline
corpus; every number below is from the full-corpus export. `corpus/lessons/round-27.md` **exists at
b9b2479** (`git cat-file -e` ok). That red herring is mine, not the lane's; superseded.

## Expected-before (b9b2479, full-corpus export)

Delivered checker on my independent baseline export: `finding_count=3, mismatch_sources=2,
reference_links=12, source_rows_checked=13, knowledge_files_expected=35` — findings only:

- `S038` cited_not_mined (queued) + missing_used_by `corpus/knowledge/attribution-interval-calibration.md`
- `S050` missing_used_by `corpus/knowledge/extraction-policy-comparison.md`

**S053: zero findings at baseline.** Row present, status=mined, citing_files=
`corpus/knowledge/extraction-policy-comparison.md`, used_by=`corpus/lessons/round-27.md,
corpus/knowledge/extraction-policy-comparison.md`, missing_used_by=∅. S053 contributed nothing to the
baseline red; the red is exactly the already-disclosed S038 status/used-by delta plus the S050
corrective-index omission. My row census reproduces this byte-for-byte.

## Current-after (final tree)

Delivered checker: `finding_count=0, mismatch_sources=0, reference_links=12`. **S053: zero findings.**
The S053 row line is byte-identical baseline→current (line-75 sha256 `c1e7b5ebecb4870d6df75357c24a0a8077f02ea33a8ad987bba65936efff1fd6`
both sides): spec/A, §2 JSON Grammar, status=mined, opened 2026-10-21, recheck 2027-01-19, used_by
unchanged. No S053 mutable cell changed in this round. Delivered per-row output equals my independent
map on every tree checked (baseline, current, all probe variants).

## Exact effective denominator

- C2 overall: 13 source rows × 35 frozen knowledge files → **12 literal reference links**
  (S038:1 via attribution-interval-calibration.md; S049–S059:1 each via extraction-policy-comparison.md;
  S060:0, rejected with empty citing set — vacuously green by contract).
- Row S053: **citing_count=1** — 2 standalone mentions (`S053/S059` line 1; `(S053)` line 51) in the
  single file `corpus/knowledge/extraction-policy-comparison.md`. Per-row denominator for
  missing_used_by coverage = 1 file. No other frozen knowledge file mentions S053 on either tree.

## Missing / corrective / code references; status; used-by subset

- Missing: none, both trees (citing ⊆ used_by; both used-by paths exist on both trees).
- Corrective: none against S053. The file's corrective/errata content targets S050 (line 18 per
  claims; S058 pattern() chain in the line-1 index). The `S059` row *extends* S053's anchor (§6 after
  §2) citing "independent reread FSourceS053" — a downstream dependency, not a reversal. Lines 1 and 51
  are primary coverage; line 51 restates the taught claim ("E4's Unicode `strip()` is broader than RFC
  8259 whitespace (S053)") in the row's own terms. S050's corrective-index reversal is disclosed
  context only and is not treated as support for any superseded reason; S038's drift is
  already-disclosed and reported here only as observed baseline/final context, not rediscovery.
- Code: no code-kind row or code path participates in S053's used_by; enum checks pass (kind=spec,
  tier=A, no community-A conflict).
- Status: mined + cited ⇒ consistent (violating it is detectable — falsifier below).

## Row-specific falsifier (executed, scratch copies only)

**Flip the single status cell mined→queued in a scratch copy of the final tree.** Delivered checker
result: `{"id":"cited_not_mined","source":"S053","status":"queued"}`, finding_count 0→1, S053 the sole
mismatch source. The delivered S053 green is a real conditional measurement tied to that one cell —
falsifiable, not vacuous.

Supporting probes (same scratch protocol, delivered checker):

- Both S053 mentions removed: citing=∅, reference_links 12→11, findings stay 0. Contract boundary
  observed: total loss of S053's knowledge coverage is silently green under the literal contract
  (empty citing set is vacuously covered; additional used-by paths need not match citing). Declared
  scope ("literal mentions, not citation truth") — noted as a boundary, not a defect.
- `corpus/lessons/round-27.md` deleted: `used_by_missing S053` fires (+11 siblings, finding_count=12)
  — the additional lesson used-by path is liveness-enforced, reproducing exactly the finding class my
  defective first export had faked.

## Conclusion

S053 was never red under the frozen13/35 literal contract, is byte-unchanged across the round, is
covered by exactly one file carrying two primary-support mentions, has no corrective/superseding or
code-reference entanglement, and its delivered per-row output is independently reproduced on baseline
export and final tree, with its green proven conditional (status-cell flip flips it).

**VERDICT: PASS** — complete actual support for S053's delivered registry result within my scoped
literal contract; falsification attempts did not falsify it.

Evidence retained at `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS053/`:
`census_s053.py`, `census-out.json`, `baseline/` (b9b2479 full corpus export),
`final{,-status,-nomention,-nolesson}/` probe trees.
