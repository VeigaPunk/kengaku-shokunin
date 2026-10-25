# R35MutC1Rows — V2 mutation results

## Axes

- **Calibration:** whether V2 rejects the designated malformed/incorrect S105–S107 row cases.
- **Operability:** whether the fixture registry still passes the general `sources-census.sh validate --file` contract.

## Method and baseline

Read frozen claim at `plans/round-35-claims.md:13-37`; V2 requirements are documented in `plans/round35_c1_verify.py:11-13`, implementation at `:82-99`. In an isolated `/tmp/k35-17HO/lane` fixture clone, started from committed `master` then copied the current uncommitted registry rows from the lane. Baseline has exactly three S105–S107 rows and the required 11 fields. Baseline: exact verifier result `V2 ok`; census result `file\tok\t/tmp/k35-17HO/lane/corpus/SOURCES.md`, exit 0. No lane implementation files were edited.

Each mutant altered one row/condition at a time, then ran the actual C1 verifier and `scripts/sources-census.sh validate --file <fixture registry>`. For census validation, fixture-only used-by target paths were created so unrelated missing paths do not contaminate the result. The validator reports 15 existing W04 warnings in each case; warnings do not fail validation. All exact targeted census findings are below.

| Mutant | V2 result | Census exit / targeted finding | Assessment |
|---|---|---|---|
| 10 cells | `V2 DEFECT S105 has 10 cells` | 1; `E01 S105 fields=10` | Caught |
| Escaped `\\|` in a cell | `V2 DEFECT S105 has 12 cells` | 1; `E01 S105 fields=12` | Caught |
| `/tasks/` path instead of `/tests/` | `V2 DEFECT S105 source URL [...]tasks/test_outputs.py != ...tests/test_outputs.py` | 0; no E findings | Caught by V2 only |
| `#L2` URL fragment | `V2 DEFECT S105 source URL [...test_outputs.py#L2] != ...test_outputs.py` | 0; no E findings | Caught by V2 only |
| Tier B | `V2 DEFECT S105 tier/status/opened = B/mined/2026-10-25` | 0; no E findings | Caught by V2 only |
| Status queued | `V2 DEFECT S105 tier/status/opened = A/queued/2026-10-25` | 0; no E findings | Caught by V2 only |
| used-by with second path | `V2 DEFECT S105 used-by 'corpus/knowledge/tb2-protein-assembly-grader.md, corpus/lessons/round-35.md'` | 0; no E findings (fixture path exists) | Caught by V2 only |
| Duplicate S105 | `V2 DEFECT S105 present 2 times` | 1; `E03 S105 duplicate id` (also E04 duplicate URL/scope) | Caught |
| Two-space indentation | `V2 ok` | 0; no E findings | **Survived** |
| Kind/tier cells reordered (`A` before `code`) | `V2 DEFECT S105 tier/status/opened = code/mined/2026-10-25` | 1; `E05 kind=A`, `E06 tier=code` | Caught |

Evidence commands: `python3 <fixture>/round35_c1_verify.py --lane <fixture>/lane`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <fixture>/lane/corpus/SOURCES.md`. Results above were produced for the 10 mutations and baseline. The V2 parser's `ROW_RE` accepts zero through three leading spaces (`round35_c1_verify.py:46`), while the census parser explicitly supports that indentation (`sources-census.sh:40-42`); therefore the indented row is intentionally accepted under both contracts. V2 checks exact per-row requirements, not broader census schema correctness; census catches malformed count and invalid cell-order cases, but intentionally does not enforce V2's pinned URL/tier/status/opened/used-by exactness.

## Files and blockers

- Report only: `.ufo/waves/round-35/build/R35MutC1Rows.md`.
- Fixture/scripts were kept under `/tmp/k35-17HO`; no source lane changes, installs, or external writes.
- Risk: census validation against the full lane's registry produces W04 warnings; these were non-failing, and fixture used-by targets were materialized to keep unrelated E11s out of the tested rows.
- Blockers: none.

VERDICT: v2-mutants-9/10
