source: T01 (group-A placeholder set of source scribe C1ScribeSources2A, `rows.md`; the L1 renumbers from S194) — https://philmcminn.com/publications/barr2015.pdf — the oracle-strength taxonomy this lane's definition belongs to; PDF p.1 Introduction, `pdftotext` lines 26-29 of the archived extraction; quote: "a procedure that distinguishes between the correct and incorrect behaviors of the System Under Test (SUT)"; accessed 2026-10-30
source: T03 (C1ScribeSources2A placeholder) — https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf (canonical host unreachable 2026-10-30, read via Wayback snapshot 20260422011919id_) — how much a test suite without assertions still catches; PDF p.6 section D "Explicit and Implicit Checks", `pdftotext` lines 828-831; quote: "test suites with no assertions still detect a significant fraction of the mutations (43 % on average)"; accessed 2026-10-30
source: T09 (C1ScribeSources2A placeholder) — https://arxiv.org/html/2605.12673v1 — the Terminal-Bench-wide adversarial-hack measurement (phenomenon, not instrument); rendered text line 804 of the fetched HTML; quote: "Simple exploits can drive the hack rate to near-perfect on nine of the ten benchmarks, including Terminal-Bench, SWE-bench Pro, and SWE-bench Verified."; accessed 2026-10-30
source: T10 (C1ScribeSources2A placeholder) — https://arxiv.org/html/2609.34262v1 — verifiers that accept on observable outcomes, the class this lane's presence-only tests fall in; rendered text line 314 of the fetched HTML; quote: "Most benchmark verifiers evaluate observable outcomes, such as whether expected files exist, tests pass, or specified conditions are satisfied."; accessed 2026-10-30
source: T11 (C1ScribeSources2A placeholder) — https://arxiv.org/html/2606.26300v1 — reward-faithfulness framing (false positive = an incorrect solution passes the tests); rendered text line 399 of the fetched HTML; quote: "the absence of false positives (an incorrect solution passes the tests) and false negatives"; accessed 2026-10-30
source: T12 (C1ScribeSources2A placeholder) — https://raw.githubusercontent.com/holdout-cc/holdout-findings/main/README.md — a filed-issue catalogue of grader bugs and reward hacks; line 3 of the fetched README; quote: "ways an agent can score well without doing the task, and places where the grader scores work incorrectly"; accessed 2026-10-30
source: T04 (C1ScribeSources2A placeholder) — https://arxiv.org/pdf/2309.02395v1 — the named oracle-gap metric; PDF p.1 Introduction, `pdftotext` lines 79-82; quote: "We define the oracle gap as the difference between source code coverage and mutation score for a given software element"; accessed 2026-10-30
source: T05 (C1ScribeSources2A placeholder) — https://arxiv.org/html/2610.32548v1 — per-assertion oracle strength; rendered text line 239 of the fetched HTML; quote: "Oracle strength is high on average but uneven, with weaker assertions for object return property values and exceptions."; accessed 2026-10-30
source: T06 (C1ScribeSources2A placeholder) — https://arxiv.org/abs/2506.02954 — coverage without assertion strength; rendered text line 115 of the fetched abs page; quote: "some test suites achieve 100% coverage but only 4% mutation score"; accessed 2026-10-30
source: T02 (C1ScribeSources2A placeholder) — https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46584.pdf — coverage alone misleading at industrial scale; Introduction paragraph 2, `pdftotext` lines 73-76; quote: "coverage alone might be misleading, as in many cases where statements are covered but their consequences not asserted upon"; accessed 2026-10-30
source: S184 — https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 — the maintainers' 2.0-to-2.1 class of test weaknesses; PR body line 8: "Tests were updated when they over-specified or let any solution pass."; accessed 2026-10-30
source: U15 (C1ScribeSources2B placeholder) — https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/242 — the one published artefact-existence weakness of a confirmed task's grader (`modernize-scientific-stack`); issue body line 12, `tests/test_outputs.py` bullet: "Lines 46–50 (`test_dependency_file_exists`) check that `/app/requirements.txt` or `/app/pyproject.toml` exists. The file is never opened."; group-B source scribe row `U15` (`.ufo/waves/round-53/w3/C1ScribeSources2B/rows.md`, gate `gate.md`), archive `.ufo/waves/round-53/w3/C1PriceScoutC/fetched/ghapi-issues-242.json`; accessed 2026-10-30
source: U06 (C1ScribeSources2B placeholder) — https://github.com/harbor-framework/terminal-bench-2-1/issues/156 — the closest public item naming `pytorch-model-cli`, whose contract table records the verifier as checking existence only of the artefact; issue body line 28, `tasks/pytorch-model-cli/tests/test_outputs.py` row: "No (existence, executability, prediction correctness only)"; accessed 2026-10-30
source: [pending: S-id mapping — no SOURCES draft row yet] — https://docs.harborframework.com/news/reward-hacking.md — the benchmark maintainers' own taxonomy of the defect class; page "# Cracking down on reward hacking", table row "Loopholes": "Satisfies the tests without solving the problem"; wave-3 scout candidate `.ufo/waves/round-53/w3/C1ScoutLitSrc/lit.json`, archive `.../C1ScoutLitSrc/fetched/harbor-reward-hacking.md` line 30; accessed 2026-10-30
verified-at: 2026-10-30 (lane HEAD `9ead4476bf55b1ea6490d0204b668195db4a4d1d`; counter run in a clean `--shared` clone at that rev)
recheck: 90d — from the lane root run `python3 plans/round53_c1_triage.py --lane .` on a clean clone of the landing tip and compare the ORACLE / CONFIRM / PRIOR-ART lines below; re-open the `[pending: S-id mapping]` rows when the L1 assigns their S-ids from S194; re-check the two `phenomenon-known` verdicts against their tracker pages, which are mutable

# Terminal-Bench 2.0 presence-only grader tests: what a frozen AST classifier and a blind eight-seat oracle measured, and what it does not show

## Summary

Round 52 landed a lexical per-test triage of the 89 Terminal-Bench 2.0 graders and it was **not admitted**: its
classes disagreed with independent counts, its predicate was reachable without reading a grader, and 0 of 16 mutants
were killed (`corpus/knowledge/tb2-grader-vacuity-triage.md`). Round 53 replaced the lexical split with an
instrument that can be audited: an **AST classifier** over the pinned grader bytes, a **blind eight-seat label
oracle** over the same 305 test functions, **digest pins** on every input the predicate trusts, and a **freeze
order** that makes the label files unreachable before the classifier is committed.

What the oracle measured, on the committed receipt
(`.ufo/waves/round-53/claims/c1-after-oracle.txt`, reproduced in a clean clone at lane HEAD
`9ead4476bf55b1ea6490d0204b668195db4a4d1d`):

```
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
```

**The claim is not yet admitted.** The predicate still prints `PREDICATE R53-C1 fail` (exit 1) because the
PRIOR-ART leg has no rows yet at this tip (`PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0 urls=0`), and the
wave-3 pricing of the 20 confirmed tasks is still in flight. What this entry records is the *measured* part —
the instrument, the oracle, the candidate set and the confirmations — and the limits on reading them.

## What the instrument now is

| part | what it is | located pointer |
|---|---|---|
| definition | one written spec, frozen with the claims | `.ufo/waves/round-53/p1-spec.md` (committed `a34838f`) |
| classifier | `classify_source(src) -> {test key: 'P1'\|'P0'}` over the `ast` module; sha256 `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` | `plans/round53_c1_classify.py`; digest pinned in `plans/round53-c1-freeze.json` |
| freeze | the classifier and `plans/round53-c1-freeze.json` land in **one** commit and are never touched again; the eight label files land in **strictly later** commits | commits `d40b7055` (classifier + freeze) then `db90a6b7` (labels); `git log --oneline -- plans/round53_c1_classify.py plans/round53-c1-freeze.json` → 1 entry; `git log --oneline -- .ufo/waves/round-53/w1/C1Label*/labels.json` → 1 entry each |
| blind oracle | eight label seats, each reading **one** shard of the 305 ids; every id is in exactly two shards, one scout seat and one reviewer seat | shards `.ufo/waves/round-53/labels/shard-{A..H}.json`; seats `C1LabelScoutA/C/E/G` + `C1LabelRevB/D/F/H`; `FREEZE … label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4` (counter receipt) |
| digest pins | population JSON, pin tree, tests index, the round-52 control module, and the git blob SHA-1 of each of the 183 committed captures | `PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184` (counter receipt) |
| counter | the frozen five-leg predicate, with its own 47-case selftest | `plans/round53_c1_triage.py`; `.ufo/waves/round-53/claims/c1-selftest.txt` (`SELFTEST cases=47 failures=0`) |

Classifier output over the population: `P1 = 52`, `P0 = 253` over 305 ids; the 52 `P1` tests sit in **41 of the
88** task files (`.ufo/waves/round-53/w1/C1ExecClassifier/classes-305.json`, read at lane HEAD
`9ead4476bf55b1ea6490d0204b668195db4a4d1d`). The classifier's own selftest is 83 cases, 0 failures
(`python3 plans/round53_c1_classify.py --selftest` → `cases=83 failures=0`, run in a clean clone at that rev).

Two independent checks on the classifier, both committed in wave 1: an adversarial case set built from the spec
alone (90 modules, 371 tests) scores `case_fail=0 test_fail=0` after the pre-freeze fix round
(`.ufo/waves/round-53/w1/C1ExecAdvCases.md`), and a second, differently-written implementation (`C1ExecClassifierAlt`)
disagreed with the frozen classifier on **1 of 305** ids before that fix round and on 0 after it
(`.ufo/waves/round-53/w1/C1ExecClassifierAlt.md`; facts.md §C1).

## What the oracle measured — and what it cannot support

The oracle is eight blind readers' labels on the 305 test functions, merged by the counter itself: no separately
authored label file exists, each seat's file must cover exactly its shard, and a labeller named in the freeze
file's `author_seats` voids its rows (claims file Amendment A1, bullets 2–3).

Measured: **305 of 305** ids decided (0 unclassified, 0 contested, `U` never used), oracle `Y = 52` / `N = 253`,
the v2 classifier `P1 = 52`, **0 disagreements**, limit 9.2 % of decided tests, per-label agreement 1.000 against
a 0.9 floor. Per-seat `Y` counts, read from the eight committed `labels.json` files:
`C1LabelRevB` 13, `C1LabelRevD` 11, `C1LabelRevF` 12, `C1LabelRevH` 16, `C1LabelScoutA` 14, `C1LabelScoutC` 15,
`C1LabelScoutE` 13, `C1LabelScoutG` 10 — sum 104 = 2 × 52, i.e. each `Y` test carries exactly two `Y` labels. The **control** leg is non-vacuous: the round-52 per-test classifier disagrees with
the oracle on **23** decided tests and an all-`P0` classifier disagrees on **52** (`control_ok=yes`).

**What this does not support.**

- It does not show that any task's *grader* is weak. Every one of the 20 confirmed tasks also carries a content or
  behaviour test; the confirmed weakness is a **presence-only test function beside a real content check**, i.e. a
  weakness of that one test, not of the task's score (the same limit the round-52 entry states, and the point every
  wave-2 reader makes in its own report — e.g. `.ufo/waves/round-53/w2/C1ConfReadD.md`, "the task's grader as a whole
  is not presence-only: the weakness is that one test (a redundant existence gate)").
- It does not show that any task is reward-hackable end to end: no confirmed task was executed against a stub
  solution, and the one wave-3 mechanical touch-run seat that has reported is blocked at the sandbox-mount stage
  (`.ufo/waves/round-53/w3/C1TouchExecA.md`: all 13 named `P1` invocations "terminated with `bwrap: Can't create
  file /app: Read-only file system` before pytest ran"; the seat's own file records "blocked: bwrap mount setup"
  for every task), so **no touch-run result exists** at this tip (the second touch-run seat `C1TouchExecB` has not
  reported).
- It does not establish that the presence-only class is *new*. The phenomenon is documented at class level by the
  benchmark's own maintainers (T10: "Most benchmark verifiers evaluate observable outcomes, such as whether expected
  files exist"; the Harbor reward-hacking taxonomy, "Satisfies the tests without solving the problem"), by a
  benchmark-wide adversarial audit (T09: hack rate "near-perfect on nine of the ten benchmarks, including
  Terminal-Bench"), by a filed-issue catalogue of grader bugs (T12), and by the maintainers' own 2.1 test-change
  class (PR #53: "Tests were updated when they over-specified or let any solution pass"). What round 53 adds is the
  **per-test measurement**: a pinned, blind-labelled, per-test count of one weakness class over a fixed population.
- Task-level novelty is established for only **6 of the 20** confirmed tasks at this tip (the `phenomenon-new`
  rows below: no public item names an artefact-existence weakness of *that task's* grader, only the class). Two more
  are the opposite: `modernize-scientific-stack` has a published artefact-existence weakness of its own grader
  (TB2.1 issue #242, which names the task *and* `test_dependency_file_exists`), and `tune-mjcf` has a third-party
  fork archive naming its test names. The remaining **12** are `[pending: prior-art verdicts]` — the wave-3 pricing
  seats `C1PriceScoutA/B/E` have not reported at the time of writing, while `C1PriceScoutC` and `C1PriceScoutD`
  have (their verdicts are in the table below).
- It cannot prove that the eight labellers were independent. They are LLM seats that all read **one** written spec
  (`.ufo/waves/round-53/p1-spec.md`), and independence is a protocol property recorded in the seat reports, not
  something the counter can prove (claims file Amendment A1, "Not changed"; and the wave-1 attack report
  `.ufo/waves/round-53/w1/C1CritCounterReach.md`, route R4: "the counter cannot prove independence"). A perfect
  1.000 agreement is therefore a **result to be attacked**, not a validity proof — which is why the wave-3 seats
  `C1CritOracle2` and `C1CritNeverRead` exist.

## The 28 never-read candidates

`.ufo/waves/round-53/claims/c1-candidates.txt`, produced by `python3 plans/round53_c1_triage.py --lane . --candidates`
at lane HEAD `9ead4476bf55b1ea6490d0204b668195db4a4d1d`, ends `CANDIDATES never_read_tasks=28`: the 28 task files
that carry at least one `P1` test and were not named in the base-tip lane texts nor confirmed in round 52.
Each candidate line names the task and its `P1` test names, e.g. `CANDIDATE pytorch-model-cli
tests=test_weights_file_exists,test_cli_tool_exists,test_prediction_file_exists`.

20 of the 28 are confirmed; the eight not yet confirmed are `kv-store-grpc`, `large-scale-text-editing`,
`mteb-retrieve`, `multi-source-data-merger`, `raman-fitting`, `rstan-to-pystan`, `video-processing`,
`vulnerable-secret` (set difference of the candidates file against `corpus/evidence/round53/confirmations.json`).

## The 20 confirmations

`corpus/evidence/round53/confirmations.json` (landed at `9ead4476bf55b1ea6490d0204b668195db4a4d1d`) holds 20
objects, all `confirmed: true`, from **five** wave-2 reader seats — `C1ConfReadA`, `C1ConfReadB`, `C1ConfReadC`,
`C1ConfReadD`, `C1ConfReadG`, four tasks each (`C1ConfReadE` produced no report; its seat directory is empty). The
counter's own CONFIRM leg reads `CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0`.

Each confirmation names a test the classifier puts in `P1`, a quote of at least 20 characters, and the reader's
report under `.ufo/waves/round-53/w2/`. Re-locating every quote myself in the committed capture bytes: **20 of 20**
quotes occur inside their own test function's `lineno..end_lineno` span in
`corpus/evidence/round53/tests-index.json`, and **20 of 20** occur on the line the record states (script: read the
test span from `tests-index.json`, read the capture under `corpus/evidence/round52/graders/<task>/tests/`, test
`quote in span` and `quote in lines[line-1]`).

| task | confirmed test (line) | reader | the sibling check that keeps the grader honest | reader report |
|---|---|---|---|---|
| cobol-modernization | `test_required_files_exist` (18) | C1ConfReadA | `test_program_output` compares the three produced `.DAT` files to exact expected strings | `w2/C1ConfReadA.md` |
| log-summary-date-ranges | `test_summary_file_exists` (29) | C1ConfReadA | `test_summary_structure_and_counts` checks header, 15 rows and every count | `w2/C1ConfReadA.md` |
| path-tracing-reverse | `test_image_c_exists` (17) | C1ConfReadA | `test_image_compiles` + `test_image_similarity` (cosine ≥ 0.995) | `w2/C1ConfReadA.md` |
| sparql-university | `test_sparql_file_exists` (26) | C1ConfReadA | `test_sparql_query_results` compares the result set to four reference rows | `w2/C1ConfReadA.md` |
| extract-moves-from-video | `test_solution_file_exists` (334) | C1ConfReadB | `test_solution_content_similarity` (Levenshtein ≥ 90 % against an embedded solution) | `w2/C1ConfReadB.md` |
| merge-diff-arc-agi-task | `test_git_repo_init` (13) | C1ConfReadB | `test_both_bundles_fetched`, `test_algo_map_function_with_test_input` compare every cell | `w2/C1ConfReadB.md` |
| prove-plus-comm | `test_compiled_proof_exists` (12) | C1ConfReadB | `test_proof_contents` + `test_compiled_proof_content` (runs `coqc`) | `w2/C1ConfReadB.md` |
| torch-pipeline-parallelism | `test_pipeline_parallel_exists` (26) | C1ConfReadB | `test_pipeline_parallel[1,2]` compares gradients and activations to a reference | `w2/C1ConfReadB.md` |
| fix-code-vulnerability | `test_report_file_exists_example` (18) | C1ConfReadC | `test_vul_file`, `test_cwe_id`, `test_hkey_*` compare values | `w2/C1ConfReadC.md` |
| modernize-scientific-stack | `test_dependency_file_exists` (49) | C1ConfReadC | `test_modernized_code_runs` runs the script and checks two means within 0.1 | `w2/C1ConfReadC.md` |
| pytorch-model-cli | `test_weights_file_exists` (15) | C1ConfReadC | `test_cli_tool_output` compares predictions on 50 MNIST images | `w2/C1ConfReadC.md` |
| torch-tensor-parallelism | `test_parallel_linear_exists` (25) | C1ConfReadC | `test_column_parallel_linear` / `test_row_parallel_linear` (`torch.allclose` × world sizes) | `w2/C1ConfReadC.md` |
| gcode-to-text | `test_hello_file_exists` (10) | C1ConfReadD | `test_hello_file_content` compares the file with the exact flag string | `w2/C1ConfReadD.md` |
| mteb-leaderboard | `test_result_exists` (7) | C1ConfReadD | `test_data_matches` requires the line `GritLM/GritLM-7B` | `w2/C1ConfReadD.md` |
| pytorch-model-recovery | `test_model_file_exists` (108) | C1ConfReadD | four real checks (`test_weights_file_unchanged`, `test_model_loads_weights`, `test_state_dicts_match`, `test_model_loss`) | `w2/C1ConfReadD.md` |
| tune-mjcf | `test_tuned_model_exists` (28) | C1ConfReadD | `test_correctness` (`allclose` atol 1e-5) + `test_model_speed` (ratio ≤ 0.6) | `w2/C1ConfReadD.md` |
| llm-inference-batching-scheduler | `test_output_files_exist` (97) | C1ConfReadG | shape, coverage and performance-threshold tests compare request ids and shapes | `w2/C1ConfReadG.md` |
| path-tracing | `test_image_c_exists` (15) | C1ConfReadG | `test_image_similarity` (cosine ≥ 0.99) + `test_no_deps` | `w2/C1ConfReadG.md` |
| sam-cell-seg | `test_python_file_exists` (149) | C1ConfReadG | `test_run_script`, `test_csv_shape_cols`, `test_mask_alignment` (IoU) | `w2/C1ConfReadG.md` |
| winning-avg-corewars | `test_warrior_exists` (41) | C1ConfReadG | `test_warrior_performance` runs `pmars -b -r 100` against five opponents | `w2/C1ConfReadG.md` |

**Wave-3 blind re-label (independent of the oracle).** Four reviewer seats re-labelled 80 ids from the same frozen
spec without reading the oracle, the classifier or the counter: `C1RelabelRev1`–`C1RelabelRev4`
(`.ufo/waves/round-53/w3/C1RelabelRev{1..4}.md`, `labels.json` each). The 80 ids cover **all 52** `P1` ids plus 28
`P0` ids across 48 tasks; comparing each seat's labels against the frozen classifier classes gives **80 of 80
agreement, 0 disagreements** (script: read the four `labels.json` files, compare each label to
`.ufo/waves/round-53/w1/C1ExecClassifier/classes-305.json`). This is corroboration of the classifier against a
second set of blind readers, not an admission of the claim.

## Prior-art pricing of the confirmed tasks (partial)

| task | verdict | deciding archive | priced by |
|---|---|---|---|
| modernize-scientific-stack | phenomenon-known | TB2.1 issue #242 (names the task and `test_dependency_file_exists`; "The file is never opened.") | `w3/C1PriceScoutC.md` |
| tune-mjcf | phenomenon-known | a third-party fork's verifier transcript naming `test_model_ref_unchanged` / `test_tuned_model_exists` / `test_correctness` | `w3/C1PriceScoutD.md` |
| fix-code-vulnerability, pytorch-model-cli, torch-tensor-parallelism | phenomenon-new (class-level archives + 4–5 archived zero-hit sweeps each) | PR #53; arXiv:2503.15223; arXiv:2511.21654 | `w3/C1PriceScoutC.md` |
| gcode-to-text, mteb-leaderboard, pytorch-model-recovery | phenomenon-new (class-level archives + 4 archived zero-hit sweeps each) | arXiv:2507.02825v1; TB2 issue #74; arXiv:2608.23616v3 | `w3/C1PriceScoutD.md` |
| the remaining 12 confirmed tasks (cobol-modernization, log-summary-date-ranges, path-tracing-reverse, sparql-university, extract-moves-from-video, merge-diff-arc-agi-task, prove-plus-comm, torch-pipeline-parallelism, llm-inference-batching-scheduler, path-tracing, sam-cell-seg, winning-avg-corewars) | `[pending: prior-art verdicts]` | — | pricing seats `C1PriceScoutA`, `C1PriceScoutB`, `C1PriceScoutE` have not reported |

The class-level archives the `phenomenon-new` rows lean on (PR #53 = the landed row S184; arXiv:2503.15223 =
the landed row S188; arXiv:2507.02825v1 = the landed row S091; arXiv:2511.21654; arXiv:2608.23616v3; TB2 issue
#74) are **prior-art-leg evidence rows**, not SOURCES rows: they live in the pricing seats'
`prior-art-part.json` and their fetched archives under `.ufo/waves/round-53/w3/C1PriceScout{C,D}/fetched/`. Three
of them (arXiv:2511.21654, arXiv:2608.23616v3, TB2 issue #74) have no SOURCES row at all yet; the L1 writes those
rows when the PRIOR-ART leg is integrated.

`pytorch-model-cli` carries a **reading the L1 must ratify**: the closest public item, TB2.1 issue #156, describes
the task's verifier as checking "existence, executability, prediction correctness only", which the pricing seat read
as a language-contract mismatch rather than an existence-only weakness; under the other reading that row flips to
`phenomenon-known` (`w3/C1PriceScoutC.md`, "Limits" §2). One `phenomenon-new` claim in the same report also rests on
the counter's A1 rule that a sweep archive must not name the task or any of its tests — a search result for
`test_report_file_exists_example` returns one unrelated third-party PR that shares the test name and is therefore
unusable as a sweep.

## The round's second claim (R53-C2, registry tip-state)

Not a finding of this entry's subject, recorded here because the two claims share the round and the same
re-run commands. The registry has **78** rows and the committed ledger `plans/round53-tipstate.json` has **78**
entries (`python3 plans/round53_c2_tipstate.py --lane . --dry` → `ROWS registry=78 ledger=78 missing=0 extra=0
entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok`,
`ARGV entry=74 selftest=4 help=0`). The committed run 1 (`.ufo/waves/round-53/claims/c2-run1.txt`, 77 rows at
`1ebf61f`) reported `RUN executed=77 timeout=0 mismatched=18 evidence_missing=1` and `PREDICATE R53-C2 fail`;
two independent wave-3 re-measurements at `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` agree on
`RUN executed=78 timeout=0 mismatched=1 evidence_missing=0`, `TIPSTATE declared_green=66 declared_red=12
observed_green=65 observed_red=13`, `PREDICATE R53-C2 fail` — the single mismatch being `round53-c1`, whose
declared exit 0 is contradicted by the C1 counter's own `PREDICATE R53-C1 fail` (still fail because the PRIOR-ART
leg is empty) (`w3/C2MeasureExecA.md`, `w3/C2MeasureExecB.md`). The C2 counter's own selftest is
`SELFTEST cases=52 failures=0` (`.ufo/waves/round-53/claims/c2-selftest.txt`).

## Limits

- **A presence-only test beside a real content check is a weakness of that test, not of the task's grade.** Every
  confirmed task's grader also contains a content or behaviour check (the table above; each reader's own report).
  No task is shown to be reward-hackable, and none is shown to be graded by existence alone.
- **The eight labellers are LLM seats that share one written spec** (`.ufo/waves/round-53/p1-spec.md`); they are
  blind to each other and to the classifier, not independent minds. Their 1.000 agreement with the classifier is a
  result to attack (wave-3 `C1CritOracle2`), not a validity proof.
- **The counter cannot prove labeller independence** (claims file Amendment A1, "Not changed"; `w1/C1CritCounterReach.md`
  route R4). Nor can it detect a classifier that reads the labels at call time (route R14).
- **"Never-read" is not "never-examined".** The blocklist covers the base-tip lane texts and the round-52
  confirmations only; the round-52 critic's machine receipt
  `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` already holds per-test class records for these
  tasks and the counter does not consult it (claims file Amendment A1, "Not changed"; `w1/C1CritCounterReach.md`
  route R11). "Never-read" here means *not named in the base-tip lane texts and not confirmed in round 52*.
- **No execution evidence backs the confirmations.** The confirmation is a reading of the test body against the
  frozen definition plus a quote located in the pinned bytes; the reporting wave-3 mechanical touch-run seat is
  blocked at the sandbox mount stage, so no stub-solution pass is on record (`w3/C1TouchExecA.md`).
- **The population excludes one capture on purpose**: `sanitize-git-repo/tests/test_outputs.py` is absent (its pin
  blob `3269e74e…dacf199dda` is checked instead) because of a credential-shaped string in the upstream fixture, so
  the denominator is 183 committed captures of 184 pinned grader files (`PINS … absent=0 excluded_blob=ok files=184`).
- **The prior-art leg is a negative claim.** A `phenomenon-new` row rests on archived zero-hit tracker searches and
  GitHub search queries; a weakness published outside GitHub (a blog, a forum, a private tracker) would not be
  visible to it (`w3/C1PriceScoutC.md`, "Limits" §1).
- **One published row carries a per-task claim the L1 has not yet ratified** (`pytorch-model-cli`, above); a second
  (`tune-mjcf`) is known under both readings of the known/new rule (`w3/C1PriceScoutD.md`, §1).
- **[pending: S-id mapping]** — every source row cited by a `T…` placeholder here is a wave-3 source-scribe
  placeholder; the L1 assigns the final `S…` ids from **S194**. Until that mapping lands, the rows are cited by
  their placeholder id, URL and located quote only.

## Re-run

```sh
# claim R53-C1 (the presence-only triage) — on a clean clone of the landing tip
python3 plans/round53_c1_triage.py --lane .
python3 plans/round53_c1_triage.py --lane . --candidates      # the 28 never-read candidate tasks
python3 plans/round53_c1_triage.py --selftest                 # SELFTEST cases=47 failures=0
python3 plans/round53_c1_classify.py --selftest               # cases=83 failures=0 (classifier's own selftest)

# claim R53-C2 (registry tip-state) — a clean shared clone of the landing tip as --source
python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of the landing tip> --work <scratch> [--jobs 4]
python3 plans/round53_c2_tipstate.py --selftest               # SELFTEST cases=52 failures=0

# re-derive the classifier's classes and the oracle merge
python3 - <<'PY'
import json, glob
cls = json.load(open('.ufo/waves/round-53/w1/C1ExecClassifier/classes-305.json'))
print('P1', sum(1 for v in cls.values() if v == 'P1'), 'P0', sum(1 for v in cls.values() if v == 'P0'))
lab = {}
for d in sorted(glob.glob('.ufo/waves/round-53/w1/C1Label*/labels.json')):
    j = json.load(open(d))
    for k, v in j['labels'].items():
        lab.setdefault(k, []).append(v['label'])
print('ids', len(lab), 'two labels each', all(len(v) == 2 for v in lab.values()))
PY

# re-locate every confirmation quote in its own test span (20 of 20 at this tip)
python3 - <<'PY'
import json
conf = json.load(open('corpus/evidence/round53/confirmations.json'))
idx = {t['id']: t for t in json.load(open('corpus/evidence/round53/tests-index.json'))['tests']}
ok = 0
for r in conf:
    t = idx[r['test_id']]
    lines = open('corpus/evidence/round52/graders/' + t['file'], encoding='utf-8', errors='replace').read().split('\n')
    ok += r['quote'] in '\n'.join(lines[t['lineno']-1:t['end_lineno']])
print('quotes in own span', ok, 'of', len(conf))
PY
```

## Extends

`corpus/knowledge/tb2-grader-vacuity-triage.md` (round 52) — the lexical per-test triage this entry replaces as the
lane's measure of the same population. That entry's population (184 pinned captures, 183 committed), its classes
and its verdict (`not admitted`) are unchanged; what changes is that the per-test class is now produced by an AST
classifier scored against eight blind label files, with every input digest-pinned and the labels frozen after the
classifier. The round-52 entry's own recorded weaknesses (the leaky per-test split, the five reachable routes, the
non-blind labels) are the defects this round's instrument was built to close, and the wave-1 attacks on the new
counter — `.ufo/waves/round-53/w1/C1CritCounterReach.md`, `C1MutCounter.md`, `C1SentinelScreen.md` — are the
evidence that it needed closing.
