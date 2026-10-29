# Round 52 — grader-vacuity triage and a registry that names every gate (hyaku run 11, 2026-10-28)

L1 `KengakuR52a3`. Claims frozen at `1315234` (`plans/round-52-claims.md`, base tip `30801b47`); amendments
appended before the scored after-run: A1 `07ea208` (per-test classification), A2 `19bc16c` (counter
implementation corrections), A3/A4 `28c0018` (C2 parser, A1-observation correction), A5 `87301ba` (additive
exclusion report; operator exclusion `bfbcb07`). Two v1 waves (build, falsify); wave 2 dispatched at `28c0018`.

- **R52-C1 (novelty 8→9)** — `plans/round52_c1_grader_audit.py` triages the 89 Terminal-Bench 2.0 graders
  (pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, 184 capture files) as a population. State at lesson-draft
  tip `87301ba`: `CAPTURES present=183` of 184 and `classified=88` of 89 (one capture deliberately absent,
  A5), `CANDIDATES total=29` (33 presence-only test functions in 27 tasks), `CONFIRMED new=0`,
  `PRIOR-ART ok=False` (wave-2 evidence not yet integrated at that tip), `PREDICATE R52-C1 fail`,
  `PREDICATE R52-C1-A5 fail`. By the frozen kill rule the literal verdict is *not admitted* and novelty stays 8
  unless the landing revision's counter prints `pass`; the L1's landing receipt, not this paragraph, is the
  verdict.
- **R52-C2 (operability 8→9)** — `plans/round52_c2_registry.py` compares the advertised-instrument universe
  with `SKILL.md`'s *Gate/probe registry*. Base tip: `ADVERTISED 72`, `REGISTERED 44`, `MISSING 28`,
  `SELFTEST-UNBACKED 1`, fail. State at draft tip `87301ba`: `REGISTERED total=72 rows=74`, `MISSING 0`,
  `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `PREDICATE R52-C2 pass`.

## Gate

Candidates opened this round (SOURCES contract v1 rule 1: URL, access date, ≤25-word located quote). Row ids
are the L1's to assign at integration; those below are the next free ids after `S178`.

| candidate | verdict | reason / flip |
|---|---|---|
| TB2 grader-file population at the pin — recursive tree API document for `2fd12b88…` (`https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1`), opened 2026-10-28 | **ADMIT → S179** (tier A, kind `code`, status `mined`) | `"truncated": false`, 1446 entries, document sha256 `b5d86dfe49ca75383d6e87d36e7fadcfd60d99bc5ae18c79fbc14d272278f362` (453,523 B); 92 top-level = 89 task dirs + `.gitignore`/`LICENSE`/`README.md`; 184 grader files = 94 `test_outputs.py` + 89 `test.sh` + 1 `verify.sh`, equal to the frozen `capture_file_count`. Scope is the population only (S079 = task schema, S100 = entry count and verifier execution) |
| `build-pmars/tests/test_outputs.py` raw capture at the same pin, opened 2026-10-28 | **RE-OPEN S115, no new row** | re-fetched 2938 B / 85 lines, sha256 `d9d2796d…` — byte-identical to S115's anchor; mutable cells unchanged (`mined → mined`, `180d → 180d`, used-by unchanged). A second row would pass the census as `W04` while registering the same bytes twice (scribe receipt `rc-B-reworded-scope.txt`). Flip: any byte change at the pin |
| Terminal-Bench 2.0 paper, `https://arxiv.org/html/2601.11868` (section `S2.SS3.p2.1`), opened 2026-10-28 | **RE-OPEN S020, no new row** | same document S020 registers (`arxiv.org/abs/2601.11868`); located quote (24 words): "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state." — re-verified in the fetched body (1,088,268 B). It states the validity bar the C1 counter approximates; it names no marker rule |
| Terminal-Bench 2.1 PR #53, `https://github.com/harbor-framework/terminal-bench-2/pull/53`, opened 2026-10-28 | **ADMIT → S180** (tier B, kind `docs`, status `mined`) | API `pulls/53` HTTP 200, state open (mutable → tier B, as S114/S121 are). Quote at body line 8 (11 words): "Tests were updated when they over-specified or let any solution pass." Prices the *phenomenon* as maintainer-documented; the body attaches the clause to no task id and states no V1/V4 rule |
| tbench.ai 2.1 release note, `https://www.tbench.ai/news/terminal-bench-2-1`, opened 2026-10-28 | **ADMIT → S181** (tier A, kind `docs`, status `mined`) | official maintainer account of the 28-task revision. Quote at `#what-changed` (11 words): "Some tasks had instructions that were not aligned to their tests." Instruction/test misalignment is a different defect from the presence-only or sparse-test rule the counter applies |
| Z.ai Terminal-Bench 2.0 Verified card, `https://huggingface.co/datasets/zai-org/terminal-bench-2-verified`, opened 2026-10-28 | **ADMIT → S182** (tier B, kind `dataset`, status `mined`) | third-party review claim, not a reproducible audit. Quote at the 2026.08.18 update (12 words): "the test logic itself misjudged valid submissions or let non-compliant outputs through". Names false-pass test logic on named tasks; no marker rule |
| `https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/` | **REJECT** | HTTP 403 re-measured 2026-10-28 (scout seat saw the same); no body, no located quote. Flip: a reachable copy with a locatable anchor |
| OpenReview "Benchmarks as Software" (`openreview.net/forum?id=AhXMZPnOPS`, `/pdf?id=…`) and the `lacuna.tiptreesystems.com` summary of it | **REJECT** | OpenReview returned HTTP 200 with a challenge page (4,783 / 4,787 B), not the paper; the summary page restates an unread paper, so none of its sentences can be a located quote. Flip: the paper body fetched and a sentence located in it |
| `build-pmars` as a round-52 `CONFIRMED new` task | **EXCLUDE (definitional)** | `corpus/knowledge/tb2-build-pmars-grader.md` exists at the base tip, so the lane read this task before the round; leg 3 admits only never-read tasks. Flip: none |
| `tbench.ai` task hub / leaderboard (r50 reject) | **unchanged reject** | not re-opened; the r50 reason stands (mutable, unpinned surface) |

Prior-art pricing (scout seat `C1ScoutPriorArt`, `prior-art.md`; 10 quoted sources, each quote verified as a
substring of an HTTP 200 body): the *instrument* — static per-test presence/sparsity triage of the whole 2.0
grader population — is described in no fetched page (phenomenon-new at the instrument level), while the
*phenomenon* (tests that "let any solution pass", "limited grading logic", plausible-but-wrong patches) is
documented by S020, S180–S182 and the ABA/SWE-bench primaries. No task-level finding prices phenomenon-new
from the scout's pages alone; the score rule's "phenomenon-new" case therefore depends on the confirmed tasks'
own pricing in `corpus/evidence/round52/prior-art.md`, not on this table.

Spot-check result: the four quotes above (paper, PR #53, release note, Z.ai card) were re-located by the lesson
drafter in freshly fetched bodies of the sizes the scout recorded (1,088,268 / 28,522 API-body / 148,013 /
147,928 bytes); the OpenAI 403 was re-measured. S179's counts were re-derived from the pinned tree and from
`plans/round52-tasks.json` by the scribe seat. Non-author spot-check of this Gate is the round-52 verifier's
duty.

Census: round start (draft-time re-run, fleet root) `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → `ok`, 171 rows, 15 pre-existing `W04`, exit 0. With S179–S182 inserted
**inside** `## Registry` in a scratch copy and the lessons tree present (so `E11` resolves),
`validate --file …` → exit 0, `malformed=0`, 15 `W04` unchanged; `census` → rows 175, tier A=149/B=24/C=2,
mined=159/queued=8/rejected=8. Rows appended after `## Paths` fail `E12`; a `used-by` naming a file that does
not exist fails `E11` — so this lesson must be on disk before the round-end census.

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
