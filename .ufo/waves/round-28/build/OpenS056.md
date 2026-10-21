# OpenS056 — scoped author-side source reopening

Writer/seat: KengakuR28.OpenS056-2. Access date: 2026-10-21.
Axes: calibration8 (primary); source/anchor precision and frozen literal-reference completeness. No score change proposed; novelty/coverage is not assessed here.

## Verdict: PASS — S056 only

The exact existing S056 row at `corpus/SOURCES.md:78` is supported within its own-work, byte-pinned finite-corpus scope. Implementation and a committed output receipt were opened as text; neither was executed/imported. Its current `mined` status and used-by coverage need no repair. This is author-side advice, not outside closure, a round-wide PASS, independent validation, or endorsement of model performance.

## Source openings and located quotations

These are local own-work URLs, not remote publisher sources; the source cell itself names a local program and command.

| Source URL | Opened | Location | Exact quotation (≤25 words) | Scope |
|---|---|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/parser_policy_compare.py` | 2026-10-21 | module documentation, lines4–5 | “Responses and graders stay fixed; only the answer-extraction policy varies.” | Defines the stored-response counterfactual, not new model trials. |
| Same implementation URL | 2026-10-21 | `compute`, line317 | `"disagreements": sum(flips.values()),` | Counts policy-attributed disagreement events, not deduplicated response identities. |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round27-calibration/policy-final-summary.txt` | 2026-10-21 | line74 | `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5` | Preserved finite-corpus result; line1 identifies the original command and line76 records `exit=0`. This seat did not rerun it. |

Committed identity is established at baseline `b9b24796277020d1b9b01923b45313d6a565e664`: `git rev-parse BASE:PATH` and `git hash-object PATH` returned matching identities for both opened files:

- `plans/parser_policy_compare.py`: `844b6d705d33dfb84545d87ae572354e4f8577ab`.
- `corpus/evidence/round27-calibration/policy-final-summary.txt`: `5c7f4e5dd0ef69aa903a6b996e4e6075717cc75e`.

## Observed implementation and claim trace

Textual definition/caller trace only: no `lsp` tool/device is mounted in this session (the mounted `xd://` inventory exposes no LSP). Thus semantic definition/reference/hover queries were unavailable; search and located text reads are the explicit fallback, not semantic-tool proof.

- `plans/parser_policy_compare.py:137–147`, `POLICIES`: E0 baseline plus E1–E8, eight alternatives.
- `main:581–590` calls `compute` and then `render` for summary output.
- `compute:242–245` calls `gp.build_population` and returns a population failure before policy execution if recorded population errors exist.
- `plans/grader_perturb.py:20–33,187–210`, `build_population`: declares expected population1964, four input files and fixed SHA-256 identities; reads and compares their bytes. This establishes the implemented pinning mechanism, not a fresh verification of those input bytes by this seat.
- `compute:248–263`: iterates the same raw record across each policy and grades its extracted value. `grade_value:169–175` passes the fixed extracted value through the existing `gp.regrade` dispatch, restoring the grader afterward.
- `tally:195–205`: compares each verdict with `rec.stored_ok` and increments the appropriate PASS→FAIL/FAIL→PASS count.
- `compute:311–318`: excludes E0 from alternatives, sums their `n` values for comparisons and their flips for disagreements. `render:333–337,347–350` emits POLICY/TOTAL lines.
- Receipt `policy-final-summary.txt:2–10` records1964 comparisons per alternative and flip counts E1=17, E3=17, E4=1012, E5=26, E7=17; others0. Arithmetic:1964×8=15712 and17+17+1012+26+17=1089. The sum is across policies, without unique-response deduplication. No new model calls are represented by this replay.
- Existing claim `corpus/knowledge/extraction-policy-comparison.md:58–77` matches the receipt and explicitly excludes unique-response and cross-corpus algorithm-equivalence interpretations. The row's `TOTAL and POLICY lines; round-27 receipts` anchor is therefore identifiable and sufficient, albeit less specific than the precise receipt path given above.

## Frozen35 literal-reference consistency

Population source: `plans/fixtures/r28/registry/population.json:18–56` (35 explicit knowledge paths, standalone-reference pattern). The knowledge directory enumeration contained the same35 filenames. A literal search with `(?<![A-Za-z0-9_])S056(?![A-Za-z0-9_])` across that directory returned exactly one match:

- `corpus/knowledge/extraction-policy-comparison.md:1`: `S056 own-work plans/parser_policy_compare.py`.

Current `corpus/SOURCES.md:78` has `status=mined`, `opened=2026-10-21`, `recheck=90d`, and used-by `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. The one frozen citing knowledge path is covered. The lesson is an allowed additional used-by path, outside the frozen35 population; its line49 was also opened and contains the matching S056 TOTAL receipt citation. No missing-used-by or cited-but-queued defect was observed for S056.

**Allowed mutable-cell recommendation:** no change. Retain status `mined`, recheck `90d`, and the existing used-by list. No immutable cell change, new source row, or knowledge admission is proposed. Registry was not edited.

## Commands, limitations, remaining unknowns

Observed shell commands (read-only, cwd lane root):

1. `git rev-parse b9b24796277020d1b9b01923b45313d6a565e664:plans/parser_policy_compare.py b9b24796277020d1b9b01923b45313d6a565e664:corpus/evidence/round27-calibration/policy-final-summary.txt`
2. `git hash-object plans/parser_policy_compare.py corpus/evidence/round27-calibration/policy-final-summary.txt`

Other actions were tool-based searches, relevant ranged reads, tool-inventory discovery, and writing this assigned report. No installs/updates, builds, tests, linters, formatters, benchmark-site requests, REA MCP, registry edits, production code writes, or dispatch occurred.

High confidence in the scoped source/receipt opening and literal coverage result. This seat did not reproduce execution, independently verify all stored inputs/grading decisions, or independently establish the knowledge entry's assertion that E1/E3/E7 share identical affected record identities; none is necessary to the narrower row claim. The preserved receipt records success, not a fresh successful run. S038's publisher/full-text/Introduction requirement is conditional on opening S038 and is outside this S056 assignment; no S038 opening or repair is claimed. Q13 structural evidence is not source endorsement. Round27's disclosed offline/superseded P4 limitations are unchanged, with no endpoint restoration or whole-tree claim.
