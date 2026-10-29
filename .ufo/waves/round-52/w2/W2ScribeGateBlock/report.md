# W2ScribeGateBlock — round 52, wave 2 (falsify), scribe seat

Item: write the `## Gate` block for `corpus/lessons/round-52.md` (candidates opened this round, each ADMIT→row or REJECT with reason and flip), and attack the landed R52-C1 instrument where it touches the candidates. Leaf seat: no subagent dispatch, no lane-tree edit, no git or jj mutation, no sibling messaged.

Base tip read: `30801b47`. Lane tree read-only.

## Result

- **Gate draft:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock/gate-block.md`. The scratch original `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeGateBlock/gate-block.md` was removed at yield per the scratch directive; the report-dir copy is the kept draft.
- **Verdicts: 13 ADMIT, 4 REJECT** (17 candidate rows, S179–S195). The 13 admits are `mined`; the 4 rejects are `rejected`, tier C, each with reason and flip. Plus one re-open of S115 (build-pmars) with no new row. The OpenAI SWE-bench post is not a new candidate: it was not re-opened this round and S005 already registers it.
- **Census on a scratch copy** of `corpus/SOURCES.md` with the 17 rows inserted inside `## Registry`: `scripts/sources-census.sh validate --file …/SOURCES.md` → exit 0, E-codes 0, 15 `W04` (unchanged), registry rows 171 → 188. The scratch run used a placeholder `corpus/lessons/round-52.md` (E11 needs that path on disk); the placeholder is not carried into the lane.
- **Id note:** ids S179–S195 are proposed from the lane's current maximum S178. The parallel wave-2 SOURCES seat (`w2-W2ScribeSourcesRows`) may propose overlapping ids; the L1 must reconcile before integration. I did not message that seat (not addressed).

## What I attacked and whether it landed

### A. R52-C1 counter, read-only (`plans/round52_c1_grader_audit.py`, copied to scratch; sha256 `0b1d4213…a7b3`, identical to the lane file)

**A1 — the candidate predicate does not match Amendment A1's own text: LANDED.**
A1 defines a vacuity candidate as "≥1 of its tests is P1". The frozen `collect()` sets `"candidate": bool(p1) or cls in ("V1", "V4")`. Measured, read-only (`receipts/c1-readonly-collect.txt`): `candidates 29` = 27 P1-tasks plus 2 tasks with zero P1 tests, `pytorch-model-recovery` and `torch-tensor-parallelism`. Those are the two tasks A1 says the file-level V1 misdescribes. The frozen pool re-admits them through the file-level class. Under leg (i) of the A1-hardened CONFIRMED rule, a confirmation of either would pass on the counter's definition and fail on A1's text.

**A2 — the per-test splitter misclassifies the presence-only tests A1 cites: LANDED (two tasks, measured).** (`receipts/c1-per-test-probe.txt`)
- `pytorch-model-recovery::test_model_file_exists` (lines 103–108; presence-only by reading) is classed **P3**. Cause: the block's comment "operated in (the WORKDIR…" matches the value marker `\bin\b`; `VALUE` runs on comments and docstrings.
- `torch-tensor-parallelism::test_parallel_linear_exists` (lines 18–25; presence-only by reading) is classed **P2**. Cause: `split_tests` splits only at `^def test_`, so the block runs to line 184 and absorbs the helpers `_setup_process_group` and `_test_column_parallel_linear`. Those contain `dist.`, which `BEHAV_T` matches, and `BEHAV_T` is checked before `PRESENCE`.
- `bn-fit-modify` is classed correctly: 3 P1 tests (lines 13, 20, 58).

**A3 — the P1 count is unstable under the obvious mechanical repairs: LANDED as instrument sensitivity, not as proof of a wrong frozen count.** (`receipts/c1-alt-measure.txt`; variants computed in scratch; the frozen counter unchanged.)
- frozen: P1 tests 33 across 27 tasks
- split at any top-level construct: 34 across 28
- strip comments and docstrings before marker checks: 46 across 36
- both repairs: 48 across 38; 22 tests change class.

Some changes are correct (e.g. `pytorch-model-recovery::test_model_file_exists` P3→P1; `torch-tensor-parallelism::test_parallel_linear_exists` P2→P1). At least one is wrong: `sparql-university::test_sparql_runs_without_error` becomes P1 under "both", but the test executes the SPARQL query inside `try/except` and fails on error, so it is not satisfied by mere presence. The corrected counts are therefore an upper bound; I did not read all 22 changes and do not claim the variant is right. The frozen predicate is not changed by this finding; the L1 decides.

**A4 — the frozen counter's capture and digest legs: FAILED TO LAND.** The read-only run gives `present 183 mismatched 0 expected 184` (the single A5 absence). Separately, all 183 captures match the pin tree's git blob id and byte size (`receipts/tree-blob-check.txt`: `population 184 blob_and_size_match 183 absent [sanitize-git-repo/tests/test_outputs.py] mismatch []`). No mismatch found.

**A5 — the A1 rule's counts: consistent with wave 1.** My read-only `collect()` run reproduces wave-1 A4 (`P1 tests 33, tasks 27`, 89 records, 183 present).

### B. Gate candidates: attack on the admitted sources

- **README at the pin:** quote "tasks are (1) solvable, (2) realistic, and (3) well-specified" located at line 87. ADMIT tier A.
- **Three graders (A1 set):** byte-identical to the pin raw files and to the lane captures (sha256 `364069f8…`, `5d4d57c4…`, `4ae4285e…`). Each quote is located at its anchor line (17, 108, 25). Presence-only test counts by reading: bn 3, pytorch 1, torch-tp 1.
- **Pin tree document:** re-fetched; sha256 `b5d86dfe…f362` matches wave 1; 1446 entries; `truncated: false`; 94 / 89 / 1 grader files.
- **Prior-art primaries:** the admitted quotes re-located by script in bytes fetched this round (`receipts/quotes-verify.txt`: 15/15 HIT, including the grader quotes). Rejects: the OpenReview forum and pdf return a challenge page (4787 bytes); lacuna is a secondary summary; the TB3 issue is out of scope; the Snorkel page restates a count.

Attack on the Gate itself: the admitted rows are correct for their scopes. The rows admit sources, not confirmations (note N1 in the draft). S182 and S183 are admitted on the source; their candidate status rests on the counter's file-level V1, which A1 disclaims.

## Exact commands

All read-only against the lane; scratch = `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeGateBlock/`.

```sh
S=/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeGateBlock; mkdir -p $S/fetch
P=2fd12b88aafdd04a52c298e3940bcb189f9766d6; R=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/$P
curl -fsS -m 60 "$R/README.md" -o readme.md
curl -fsS -m 60 "$R/<task>/tests/test_outputs.py" -o <task>.test_outputs.py   # bn-fit-modify, pytorch-model-recovery, torch-tensor-parallelism
curl -fsS -m 90 "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/$P?recursive=1" -o tree.json
# prior-art primaries: curl -sSL of the arXiv html (x2), PR #53 API and html, tbench.ai, HF card, june.kim, tsdetect PDF,
# arXiv 2503.15223, snorkel, OpenReview forum, lacuna, GitHub issue 1387
python3 verify_quotes.py                                   # → quotes-verify.txt
cp plans/round52_c1_grader_audit.py c1_counter_copy.py     # copy; the lane file is not run or written
python3 -B run_collect.py                                  # imports the copy; collect(lane) read-only
python3 -B probe_tests.py                                  # per-test classes for the three graders
python3 -B alt_measure.py                                  # variants computed in scratch
# blob check: git blob sha1 over each capture vs the pin tree (python hashlib) → tree-blob-check.txt
./scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md   # exit 0 on the scratch copy with 17 rows
```

Counter run (frozen, read-only, from the scratch copy): `present 183 mismatched 0 expected 184 records 89 candidates 29`; file-level classes `V2 53, V3 31, V0 3, V1 2`; `P1 tests 33 tasks 27`.

## Files produced (absolute paths)

Report dir (kept):
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock/report.md` (this file)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock/gate-block.md` (the Gate draft)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock/rows-S179-S195.md` (the 17 SOURCES rows, census-tested on a scratch copy)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock/receipts/` — `quotes-verify.txt`, `c1-readonly-collect.txt`, `c1-per-test-probe.txt`, `c1-alt-measure.txt`, `alt_measure.json`, `tree-blob-check.txt`, `census-validate-after.txt`, and the scripts `verify_quotes.py`, `probe_tests.py`, `run_collect.py`, `alt_measure.py`, `c1_counter_copy.py`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeGateBlock.md` (same content as this report, at the item's path)

Scratch `/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeGateBlock/` was removed at yield after the copies above.

## Tooling

None installed or upgraded (curl, pdftotext, python3 were already present). No pacman, no `uv tool`, no package install. Nothing to record.

## Not done / out of scope

- I did not run the C2 counter, did not check the 28 new registry rows, and did not evaluate the CONFIRMED legs (independent readers). Those belong to other seats.
- I did not run the frozen counter's selftest; I read its classifier and ran functions from a copy.
- I did not fix or amend the counter. Findings A1–A3 go to the L1 for disposition under the protocol (no in-place rule change after scoring).
- No lane-tree, sibling, fleet or `.ufo/state/` file was touched. No git or jj command was run.
