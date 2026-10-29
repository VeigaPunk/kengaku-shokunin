# Round 52 — a grader-vacuity triage that does not clear its own bar, and a registry that names every gate (hyaku run 11, 2026-10-28)

L1 `KengakuR52a4` (attempt 4; attempts 1–3 died mid-work, `lane-dead-no-report`; attempt 3 froze and ran wave 1 and
built wave 2). Claims frozen at `1315234` (`plans/round-52-claims.md`, base tip `30801b47`); amendments before the scored
after-run: A1 (per-test classification), A2 (counter corrections), A3 (C2 negation parser), A4 (54/42 figure retired),
A5 (additive report of the operator's exclusion of one capture), A6 (C2 counter: escape-aware cells + duplicate leg).
Two v1 waves: 35 + 33 = 68 seats, 0 dead.

- **R52-C1 (novelty 8→9) — NOT ADMITTED.** The literal frozen predicate prints `CAPTURES present=183` of 184 and
  `classified=88` of 89 (one capture deliberately absent: GH013 push protection). The additive A5 line passes. Separately,
  wave-2 attacks showed the counter reachable without the work and its per-test class leaky (see Mistakes). Novelty stays 8.
- **R52-C2 (operability 8→9) — met on its counter.** `REGISTERED total=74`, `MISSING 0 INCOMPLETE 0 ENTRY-MISSING 0
  SELFTEST-UNBACKED 0 DUPLICATE 0`, `PREDICATE R52-C2 pass`, after repairing seven false cells that wave-2 reviewers
  measured. The counter checks row existence, not row truth.

## Gate

Round-52 sources (SOURCES contract v1: URL, access date 2026-10-28, ≤25-word located quote). Rows S179–S193 were
drafted and re-fetched by `W2ScribeSourcesRows` (receipts `.ufo/waves/round-52/w2/W2ScribeSourcesRows/`) and
are census-valid at the landing tree; the fetch table (HTTP 200, bytes, sha256) is in that seat's report.

| id | verdict | URL | located quote (words) | location |
|---|---|---|---|---|
| S179 | admit, tier A, `mined` | https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1 | `"sha":"2fd12b88aafdd04a52c298e3940bcb189f9766d6"` (1) | line 1; 1446 entries, 1038 blobs |
| S180 | admit, A | …/2fd12b88…/README.md | "Each task in TB2.0 has received several hours of human and LM-assisted validation" (13) | line 87 |
| S181 | admit, A | …/bn-fit-modify/tests/test_outputs.py | "Test that the sampled data from the fitted BN exists" (10) | line 14 |
| S182 | admit, A | …/pytorch-model-recovery/tests/test_outputs.py | "Checks if the model file exists" (6) | line 104 |
| S183 | admit, A | …/torch-tensor-parallelism/tests/test_outputs.py | "Checks that the agent creates a file named parallel_linear.py in the expected directory." (14) | lines 20-21 |
| S184 | admit, A | https://github.com/harbor-framework/terminal-bench-2/pull/53 | "Tests were updated when they over-specified or let any solution pass." (11) | PR body line 8 (open PR: mutable) |
| S185 | admit, A | https://www.tbench.ai/news/terminal-bench-2-1 | "Some tasks had instructions that were not aligned to their tests." (11) | "What changed", line 81 |
| S186 | admit, **tier B** | https://huggingface.co/datasets/zai-org/terminal-bench-2-verified | "the test logic itself misjudged valid submissions or let non-compliant outputs through" (12) | 2026.08.18 update; third-party review |
| S187 | admit, A | https://arxiv.org/html/2605.26079v2 | "Our trajectory audit independently recovered 14 of these 21 issues under strict matching" (13) | line 310 |
| S188 | admit, A | https://arxiv.org/abs/2503.15223 | "a patch may pass the tests but nevertheless fail to match the developers' expectations." (14) | abstract |
| S189 | admit, A | https://testsmells.org/assets/publications/FSE2020_TechnicalPaper.pdf | "A test method that does not contain a single assertion statement and @Test(expected) annotation parameter" (15) | Table 1, pdftotext line 292 |
| S190 | admit, A | https://arxiv.org/html/2601.11868 | "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state." (24) | §2.3 "Specificity" |
| S191 | **reject** | https://june.kim/terminal-bench-frame | "On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion" (15) | line 9; measured on 2.1, not the 2.0 pin. Flip: a pin-`2fd12b88` rerun with code and output committed |
| S192 | **reject** | https://github.com/harbor-framework/terminal-bench/issues/1387 | "Verifiers that grade against a golden artifact instead of solution properties" (11) | line 114; legacy repo, opposite failure mode. Flip: an issue/PR naming a TB2.0-pin grader with a measured defect |
| S193 | **reject** | https://snorkel.ai/leaderboard/terminal-bench-2-1/ | "A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks." (18) | line 74; restates S185. Flip: a per-task grader table |

Spot-check set for the non-author closure (LEARNING.md): admits S184, S187, S190; rejects S191, S193; the OpenAI
(HTTP 403) and OpenReview "Benchmarks as Software" (challenge page) leads stay unrowed with reasons in the scribe's
report. `build-pmars` is S115 (same bytes re-opened; no second row) and is excluded from `CONFIRMED new` by the
rule (the lane read it in round 38).

Mutable-cell changes: none to existing rows (S115 re-opened, S020 left `queued` — S190 cites a different anchor).
Census: round start (this attempt, before any edit) `validate --root … kengaku` → 171 rows, 15 pre-existing `W04`,
exit 0. Round end: see the report's Sources & frontier section for the exit code and counts.

Assimilation: none (no `merge/kengaku/` theme or `considerthese/` proposal was taken; the frozen claims predate the
assimilation decision and a resumed round does not widen them).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `instrument-falsified-after-freeze` | The frozen **file-level** rule labelled `pytorch-model-recovery` and `torch-tensor-parallelism` `V1` ("satisfiable by the mere presence of an artefact"); the L1's hand-check, made after the freeze (`1315234`, 15:53) and after wave-1 dispatch (17:01), found the label false of both files and the weakness only per test (`plans/round-52-claims.md` Amendment A1; `.ufo/waves/round-52/claims/a1-observation.txt`) | none — nothing tested a frozen rule against a sample of its population before the freeze | (a) `--selftest` now covers the per-test rule (`SELFTEST classify_test cases=4`, `claims/c1-selftest.txt`); (b) a rule-behaviour probe on the captured population is a freeze-checklist step: applying it to the pinned captures prints `PROBE graders=88 contradictions=2` (`pytorch-model-recovery`, `torch-tensor-parallelism` — both file-level `V1`, both carrying per-test classes `P2`/`P3`), exit 1. Shown able to fail: mutating the counter copy so the `VALUE` branch of `classify_test` is deleted makes the selftest print `SELFTEST FAIL classify_test(P3) -> P1` and exit 1; so does deleting the presence→`P1` branch (exit 1). Both mutants run on copies in scratch |
| `counter-defect-pre-score` | A2: `CAPTURES present` counted the 89 primary graders against a 184-file target (`C1ExecCounterRun` report §1: all 184 captured byte-exact → `present=89`, `PREDICATE fail`, "no capture set can make `present == expected`"); `lane_read_tasks()` recovered `{'0','this'}` instead of 12 task ids, disabling the never-read guard | `C1ExecCounterRun`, `C1ExecClassifier` — wave 1, before the scored after-run | Amendment A2 (counter now enumerates `capture_population` and derives the 12 ids from `tb2-*-grader.md` filenames); the frozen before-state stays re-derivable. Gap named: the frozen counter was never run against a *complete* fixture population before dispatch — the same gap as the row above |
| `false-premise-in-frozen-claim` | The claims file froze `SELFTEST-UNBACKED 1 (order-check)` as a registry defect ("one row claims a self-test the script does not have"); the cell says the script has **no** self-test, and `plans/order_check.py` accepts no such flag. The counter's parser read "no `--selftest` in the script" as a claim (Amendment A3; `claims/c2-a3-pre.txt` shows `SELFTEST-UNBACKED 0` after the parser fix) | wave-1 counter runs before the scored after-run; not the freeze | A3 negation rule in the parser. Still-open gap: the C2 selftest has 3 fixtures (`clean`, `missing`, `incomplete`) and none for the negated-flag or the false-selftest control, so the parser class this row names is not exercised by `--selftest` |
| `advertised-but-unregistered` | 28 runnable instruments appeared as `python3 plans/<name>.py` in SCORECARD/SKILL/LOG/README/knowledge entries but had no row in `SKILL.md`'s *Gate/probe registry*: `claims/c2-before.txt` `MISSING 28`; the oldest of the 28 entered the tree 2026-10-16 (`plans/attrib_probe.py`), the newest 2026-10-28 (`plans/round51_surfaces.py`) — a span of twelve days, not years (the lane's first commit is 2026-09-28). The round-51 verifier routed two of them (`corpus/lessons/round-51-verifier-spotcheck.md` "Missing registry rows") | none — no counter compared the advertised universe with the registry table | `plans/round52_c2_registry.py`. Shown able to fail: base tip prints `MISSING 28`, exit 1; at draft tip `MISSING 0 … PREDICATE R52-C2 pass`; wave-1's `C1MutCounters` ran the frozen controls on a fixture proxy (`c2-control-drop-row` → `MISSING 1`, `c2-control-empty-cells` → `INCOMPLETE 28`, `c2-control-false-selftest` → `SELFTEST-UNBACKED 1`), each failing the predicate |
| `number-drift` | The round-51 LOG entry says "63 of 64 seats wrote a report … `CritAdmission` … dead"; `.ufo/waves/round-51/w1-results.json` has 64 entries, 0 without `output` (re-counted at draft: `len(results)=64`) | the round-51 verifier spot-check, by a human count of the results file (`round-51-verifier-spotcheck.md` defect 2) — **not** the ledger: the round-51 routing counter checks `routed-findings.jsonl` rows, not LOG prose | an append-only erratum in `LOG.md` ("Round-51 erratum (round 52)", landed `28c0018`); the old line stays as record. Shown able to fail: `plans/log_appendonly.py` on a scratch two-commit repo that *rewrites* `63 of 64` → `64 of 64` prints `VIOLATION … deleted=1`, exit 1, and on the append-only variant `violations=0`, exit 0; on the lane, `--since 30801b4` → `commits=1 violations=0`. Recurrence: round 51's own `number-drift` row (PROVINCE "25 rows" vs 170) was fixed by a PROVINCE-only leg, so prose counts in LOG stayed uncovered |
| `rule-unit-leak` (open) | The A1 per-test splitter cuts only at `^def test_`, so the following non-test helper functions, comments and docstrings belong to the previous test's block. Measured on the committed counter: `pytorch-model-recovery::test_model_file_exists` (`assert hello_path.exists()`) classes **P3** because a comment contains the word "in" (`VALUE` matches `\bin\b`); `torch-tensor-parallelism::test_parallel_linear_exists` classes **P2** because the helper `_setup_process_group` after it contains `dist.`. The two tests that motivated A1 are therefore **not** `P1`; both tasks appear in `CANDIDATES` only through the file-level `V1` with `presence_only=-` (`c1-after.txt`). Exploratory re-split (function body only, comment lines dropped; scratch `tight.py`): 17 of 305 test classes change, `P1` 33→37 tests and 27→31 tasks, `pytorch-model-recovery` becomes `P1`, `torch-tensor-parallelism` becomes `P3` (a docstring still holds "in") | none at draft time — the A1 selftest has four synthetic one-function bodies, none from real grader bytes | **not landed in this lesson.** Proposed, shown able to fail today: a selftest case built from the real `test_model_file_exists` block with its comment line must expect `P1`; the committed counter returns `P3` (observed), so the case fails until the splitter bounds a block at the function body and ignores comments/docstrings. Any change is a new amendment before a scored re-run, never an in-place rewrite |
| `unscreened-population` | The frozen population's captured bytes were never screened before staging; GitHub push protection (GH013) flagged a Hugging Face token pattern at line 12 of `sanitize-git-repo/tests/test_outputs.py` (`FAKE_HUGGINGFACE_TOKEN_2`, a test fixture in a public upstream repo). The capture is absent, so the literal C1 counter reports `present=183`, `classified=88` and fails (`corpus/evidence/round52/graders/EXCLUDED.md`, Amendment A5) | GitHub push protection at push time (external); nothing in the lane | A5 adds a separate `PREDICATE R52-C1-A5` line and never replaces the literal verdict (exit code follows the literal one). That records the miss; it does not repair it. A pre-stage secret-pattern scan is proposed, not landed: `grep -rEl 'hf_[A-Za-z0-9]{30,}'` finds 0 files in the 183 present captures and 1 in a synthetic fixture holding `hf_` + 34 letters, so the scan can fail but its real pattern set is GitHub's, not this one |
| `counter-reachable-without-the-work` | `W2CritC1Reach` built five routes to `PREDICATE R52-C1 pass` without reading a grader: population JSON rewritten to a 29-task subset, a forged `sanitize` stub with its digest re-pinned, confirmations with `confirmed:"false"`, example URLs as prior art; `W2MutC1` killed 0 of 16 mutants by a frozen control's named leg (`.ufo/waves/round-52/w2/W2CritC1Reach/`, `W2MutC1/`) | none — the frozen controls fail on `present=0`-style blanks, not on forged-but-complete inputs (the wave-1 `C1CritTrustBoundary` named the same class before the after-run) | not fixed this round (the literal predicate already fails, so a pass would be a forgery by construction); next round a counter must pin `plans/round52-tasks.json` by digest, read `confirmed is True`, and require per-finding verdict lines in `prior-art.md`. Gate shown able to fail only by the `c1-control-*` receipts in `.ufo/waves/round-52/claims/`, which share this blind spot |
| `false-registry-cell` | `W2ScribeRowsCheck` + `W2RevRowsA/B` measured 7 false cells in the 28 wave-1 rows (`round46-c3` `checks=7 defects=0` really `defects=6`; `round46-c1` 35 controls really 34; `round51-routing` "no `2` path" really `--bogus` exits 2; `routed-findings` `mismatched=1` really 43/12; `round35-hardening` undated live count; a stale duplicate `gate-flip-check` row with `ok=19/19` really 27/27) | none — `plans/round52_c2_registry.py` checks that a row exists, is complete and names a real script, never that a cell is true; the wave-1 scribes wrote cells from reading, and C2's own counter could not tell | all seven repaired in `SKILL.md` (`W2ExecRowsIntegrate` + L1 edits; Amendment A6 also makes the counter drop duplicate names and split on unescaped pipes). Carried: the C2 predicate still cannot see a false cell; `W2MutC2` showed padding rows of `x` passed |
| `misrooted-duplicate-of-excluded-bytes` | `W2SentinelScope` F1: the GH013-flagged upstream bytes also sat untracked at `.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/sanitize-git-repo/tests/test_outputs.py` (a 184-file duplicate of the captures inside a wave-1 report dir) | the operator's exclusion commit covered only the `corpus/evidence/` copy | the L1 deleted the untracked duplicate dir before committing (`git status --porcelain` → no `artifacts/graders`); the w1 report pointers to it are historical. A pre-stage secret-pattern scan is proposed, not landed |

Carried, not fixed this round (round-51 closure D3/D4): the routing counter's five frozen-predicate survivors
(duplicate `id`, row deletion, `check:"true"`, `fixed-verified` on an open row, directory-valued `source`)
and the open `vacuous` class (a recorded `prose` reading is not truth). Neither moved this round; the round's
two counters do not reproduce them only because they read different artefacts.

## Limits

- Both counters measure what the lane declared. C1 classifies the primary `tests/test_outputs.py` of 88–89
  tasks with a marker vocabulary; it cannot see what a grader does through helpers, `test.sh`, fixtures or the
  image, and a presence-only test beside a value check still leaves the task graded by that check. A `P1` test is
  a *candidate* weakness that a second reader must locate in the bytes, not a verdict on the task.
- The per-test class is a lexical split with the leaks recorded in the `rule-unit-leak` row. The 33/27 count
  is the committed counter's output, not a ground truth; Amendment A4 already retired the unreproducible
  54/42 scratch figure. The count has false negatives (the two A1 motivating tests) and, by construction, can
  have false positives (a presence test whose block also asserts something the vocabulary does not know).
- `CONFIRMED` rests on a receipt file the lane writes; the counter checks that the task is a candidate, was never
  read before the round and that the quote is verbatim in the captured bytes. It cannot check that the reader was
  independent: that is a rule about who wrote the file. The wave-1 critic showed the leg forgeable by anyone who
  controls the evidence directory (`C1CritTrustBoundary`).
- Phenomenon-known is priced against 10 fetched pages. Absence from them is not absence from the literature, and
  several relevant pages (OpenAI, OpenReview) were unreachable.
- C2 measures that a registry row exists, is complete and names a real entry script; it does not run the
  instrument or check that the row's verdict map is true. The two round-52 counters themselves enter the
  advertised universe as soon as SCORECARD/SKILL/LOG cite `python3 plans/round52_*.py`; each then needs its own
  registry row or the next C2 run reproduces round-51 defect D1.
- The A5 line records a digest-pinned absence; whether that counts is the operator's/closure's ruling, and the
  literal verdict stands regardless.
- In `classify_test`, the `PRESENCE.sub` stripping line is dead code on this population (removing it changes
  0 of 305 test classes) and the selftest cannot tell it from the original — an equivalent mutant, listed so a
  mutation seat does not count it as a survivor.
- This draft's probe (`rule_probe.py`) has no `--selftest` of its own; its failing run is the only evidence it
  can fail.
