# SimplifyC2 — bounded C2 design review

Writer/seat: KengakuR28.SimplifyC2-2. Author-side advice, 2026-10-21.

## Axes and scoped verdict

Primary axis: calibration8 (held). Preservation axes: historical P2–P4 integrity, bounded reproducibility, and implementation simplicity. **PASS for the preregistered standalone design boundary; PARTIAL for delivered behavior, which this seat did not execute or review as an implementation.** This is not a round PASS, outside closure, citation endorsement, or score increase.

No production edits or deletions made. No historical code is a deletion candidate: the apparent duplicate citation machinery has materially different contracts. The useful simplification is to decline a common P4/C2 adapter, new registry schema, and a second persisted authority for computed citation results.

## Exact evidence

- `plans/round-28-claims.md:9`: C2 is exactly S038 and S049–S060 against 35 frozen knowledge paths, not all registry uses or source-truth validation. Located quote: “Expected S038 drift is already disclosed, not a new discovery; score8 held.”
- `plans/round-28-claims.md:11`: preserve existing P2–P4 boundaries; C1-only knowledge/new rows do not enlarge C2. Located quote: “Historical state_check.py unchanged unless an actual regression requires a separately disclosed repair”.
- `plans/round-28-claims.md:23–27`: standalone stdlib CLI, Registry-section 11-column parsing, literal mentions including historical references, subset coverage rather than used-by equality, per-source output, and CLI-level fixture expectations.
- `plans/fixtures/r28/registry/population.json:2–18,19–56`: baseline b9b24796277020d1b9b01923b45313d6a565e664, explicit 13 IDs/35 paths, and literal boundary pattern `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`. Its note explicitly excludes semantic endorsement and round28 knowledge.
- `plans/state_check.py:343–345,427–455`: P4 freezes at b5719440e5eee46c1886fddbdf7bdc1624829454; P4e has six IDs S043–S048 and two paths (`corpus/knowledge/grader-perturbation-audit.md`, `corpus/lessons/round-26.md`). Its citation regex admits numeric ranges.
- `plans/state_check.py:3455–3466`: P4 expands ranges and specially excludes S043 on lines containing “supersedes S043”. C2 must instead count every standalone literal mention, without range expansion or this exception.
- `plans/state_check.py:3487–3512`: P4e compares exact used-by/citing-file sets, checks duplicates, and routes through historical full-token supersession. C2 permits additional lesson paths and requires only that citing frozen paths are covered. Reusing this evaluator would alter at least population, matching semantics, equality, and correction policy.
- `corpus/SOURCES.md:19–22`: existing Registry section already supplies all 11 required columns. No schema addition is needed.
- `corpus/SOURCES.md:60`: S038 currently has status `queued`, recheck `180d`, used-by `—`. `corpus/knowledge/attribution-interval-calibration.md:144–145` contains the standalone S038 mention; that path is frozen at population line22. These bytes establish a literal status/coverage inconsistency, not whether the cited statistical statement is true.
- `corpus/SOURCES.md:82`: S060 is `rejected` with a lesson-only used-by. Rejected is not inherently erroneous: an uncited rejected row is allowed, and lessons are outside the C2 input file population.

These are local design/source-file inspections, not new upstream source openings. No benchmark site, upstream executable, network source, or model runtime was used.

## Minimum persisted expectations

1. Keep `population.json` as the explicit population authority: base revision, exact 13 IDs, exact 35 relative paths, literal-boundary rule, and limitations. Do not duplicate observed citing-file maps inside that authority or persist an expected-zero mismatch table as truth. Cardinalities alone do not prove membership.
2. Persist small hand-authored CLI fixtures with explicit expected exit/finding IDs and source/path attribution, independent of production computations. This meets the existing preregistration rather than inventing a registry format.
3. Persist baseline/final CLI receipts, including population counts, per-source `citing_files`, `used_by`, `missing_used_by`, `status`, finding IDs, exit status, and scope. Receipts are observations, not a second source of current truth.
4. Preserve the S038 old→new allowed-cell delta and actual reopening evidence in the round lesson. Do not rewrite immutable source/anchor/teaching cells merely to make the diagnostic green. Do not promote queued status solely because the scanner finds a mention.

## Minimum failure-capable cases

- Valid mined citation with complete used-by coverage: exit0. Extra lesson used-by permitted; no exact-set requirement.
- Cited queued row, and cited rejected row: exit1 with status finding; uncited queued/rejected rows remain clean.
- Missing citing frozen path in used-by: exit1; report the concrete missing path.
- Duplicate selected ID, absent selected source row, and absent frozen knowledge file: non-success, never silently reduce the denominator. Preregistration requires missing frozen file/source row to be failure; actual exit1-versus-exit2 treatment must be documented consistently with unreadable-input handling, never exit0.
- Unknown population source: non-success; no vacuous skip. Malformed/unreadable population or registry input: exit2 could-not-evaluate, not a clean result.
- Registry-section boundary and 11-column fixture: examples outside Registry must not supply missing rows; malformed selected-row shape cannot pass. Exercise duplicate-ID validation per the declared contract without adding off-population citation/status obligations.
- Safe lane-relative used-by paths: unsafe absolute/traversing entries cannot satisfy coverage.
- Quoted/code-fenced/historical standalone mentions count. Embedded identifiers such as `XS038` and `S038_tail` do not. A literal range `S049–S051` names its two endpoints under this pattern, not an invented S050 mention. This is deliberately different from P4.
- Unused extra row and a newly added knowledge file do not alter frozen coverage; no row admission, filesystem glob census, or round28 population growth.

## Preserved contract and tradeoff

Retain standalone `plans/registry_check.py`; do not import `state_check.py` (whose execution path also invokes frozen evidence commands), extend P4 assertion inventories, add R27 correction machinery to C2, or remove historical provenance. A small amount of local parsing is justified because P4 and C2 are not interchangeable authorities. Stop simplification before sharing their semantic evaluator or discarding failure fixtures.

A clean result means only literal-reference/status consistency for these 13 rows over these 35 paths at the inspected root. It does not establish source support, source accuracy, current endpoint availability, coverage of every lesson/new knowledge file, or whole-tree health. Keep prior round27's two P4 offline groups and one superseded P4 ID disclosed. Q13 structural evidence is not endorsement.

## Commands, non-mutation evidence, limitations

Observed shell command (twice, before and after the final source inspection):

`sha256sum plans/state_check.py plans/fixtures/r28/registry/population.json corpus/SOURCES.md plans/round-28-claims.md`

Both outputs were identical:

- state_check.py: `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c`
- population.json: `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`
- SOURCES.md: `b1a74eb5f1cdbefa8e055cfee79dda7894a4b00a611788c3798140596258c62e`
- round-28-claims.md: `8b2e237a05b15dc2f10a62a19947ab8b15120af3c16ae9cf245da1945c485a5f`

Read/grep/glob tools supplied the remaining local evidence. Only this assigned report was written; no scratch experiment, production edit, index mutation, tool installation/update, build/test/lint/formatter, or checker execution occurred. Hash evidence proves those four reviewed inputs unchanged across the review interval, not that the entire concurrently shared tree is byte-identical. No semantic caller-absence claim or code deletion is proposed, so LSP deletion proof is inapplicable.

The writer clone listing did not contain `plans/registry_check.py` at inspection time. No delivered-checker behavior or retained-behavior improvement is claimed. Integration needs the preregistered narrow CLI selftest and baseline/final receipts, plus two-way C1/C2 isolation evidence; this seat did not run them under the no-production-check constraint.

Final scoped verdict: PASS on preserving the standalone frozen13/35 design rather than extending P4; PARTIAL on implementation evidence pending the writer's delivered checker and receipts. Calibration8 remains held.
