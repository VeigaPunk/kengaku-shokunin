# W2ExecLessonDraft — round-52 lesson draft (executor, wave 2)

Item: draft `corpus/lessons/round-52.md` for the L1. Not an attack with a target; I did attack the facts the brief
asked me to mine, and two of the brief's premises came back different (below).

## Deliverable

- Draft: `/fast/scratch/hyaku/kengaku-r52/w2-W2ExecLessonDraft/lesson.md` (the only file I leave in scratch).
- Identical copy: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ExecLessonDraft/lesson.md`.
- Supporting receipts, same dir: `rule_probe.py` (the freeze-checklist probe cited by mistake 1), `tight.py` (exploratory
  re-split behind `rule-unit-leak`), `rows.md` (proposed SOURCES rows S179–S182), `census-after.txt` (census of the scratch registry).
- Sections: header (round, both claims, freeze/amendment commits) · `## Gate` · `## Mistakes` · `## Limits`.

## Mistakes mined (7 rows + a carried-defects line)

1. `instrument-falsified-after-freeze` (brief item 1) — fix shown able to fail: `rule_probe.py` → `PROBE graders=88 contradictions=2`, exit 1;
   copy of the counter with the `VALUE` branch of `classify_test` removed → `SELFTEST FAIL classify_test(P3) -> P1`, exit 1; with the
   presence→`P1` branch removed → exit 1.
2. `counter-defect-pre-score` (A2) — captured by `C1ExecCounterRun`/`C1ExecClassifier`.
3. `false-premise-in-frozen-claim` (A3, `order-check`) — the frozen claim called a correct "no self-test" cell a defect.
4. `advertised-but-unregistered` (brief item 2) — fix `plans/round52_c2_registry.py`; MISSING 28 → 0 at tip `87301ba`.
5. `number-drift` (brief item 3) — LOG 63/64 vs 64; erratum already in `LOG.md`; `log_appendonly.py` fails on a rewrite fixture, passes on an append.
6. `rule-unit-leak` (open, **new, mine**) — see below.
7. `unscreened-population` (GH013 / A5) — fix partial (A5 records, does not repair); screen proposed, not landed.
Plus D3/D4 carried-not-fixed line.

## Where the brief and the measurements disagree (calibration)

- **"28 instruments had no registry row for years"** — the oldest of the 28 entered the tree 2026-10-16 (`plans/attrib_probe.py`), the newest
  2026-10-28; the lane's first commit is 2026-09-28. Lesson says "twelve days, not years".
  (`git log --diff-filter=A --format=%ad --date=short -- plans/<name>.py`, earliest/latest over the 28 MISSING paths.)
- **"number-drift … captured-by the ledger's CHECKS/count legs"** — not supported. The round-51 verifier spot-check caught it by counting the
  entries of `w1-results.json` (64, 0 without output); the round-51 routing counter checks `routed-findings.jsonl` rows, not LOG prose.
  Lesson records captured-by = verifier spot-check (human count), and notes that round 51's own `number-drift` leg covered PROVINCE only.
- **Brief item 1's fix "selftest now covers the per-test rule"** — true (4 synthetic cases, `claims/c1-selftest.txt`) but weaker than it sounds:
  see mistake 6.

## New finding I should flag to the L1: the A1 rule does not catch its own motivating tests (attack LANDED)

Commands (scratch, counter imported read-only; lane at `87301ba`):
- `python3 rule_probe.py <lane>` → `PROBE graders=88 contradictions=2`; `P1-bearing tasks=27 of which file-level V1/V4=0`.
- Per-test classes of the two A1 tasks via `classify_test`: `pytorch-model-recovery::test_model_file_exists` → **P3** (should be P1; a *comment*
  line contains "in", matching `\bin\b` in `VALUE`); `torch-tensor-parallelism::test_parallel_linear_exists` → **P2** (the block runs on through the
  following helper `_setup_process_group`, which contains `dist.`). The splitter cuts only at `^def test_`, so helpers/comments/docstrings leak.
- `tight.py` (function body only, comment lines dropped): 305 tests, 17 class changes, P1 33→37 tests, 27→31 tasks; `pytorch-model-recovery`
  becomes P1, `torch-tensor-parallelism` becomes P3 (docstring "in"). Exploratory; it is not a proposed counter.
- Consequence for the claim: both tasks appear in `CANDIDATES` only via file-level `V1` with `presence_only=-`. A5/A1 rest on 33/27 as the
  counter prints it; that figure has false negatives. Whether any `CONFIRMED` task depends on a leaked class is for the wave-2 reviewers; I did not
  check the confirmation files beyond seeing that A/B confirmers quote presence-assert lines for `bn-fit-modify`, `build-cython-ext`, …
- Equivalent mutant: dropping the `PRESENCE.sub` strip in `classify_test` changes 0 of 305 test classes (dead code) and survives the selftest.

## Other measured numbers

- Draft-tip state (`87301ba`): C1 `present=183/184`, `classified=88/89`, `CANDIDATES 29`, `presence_only_tests=33` over 27 tasks, `CONFIRMED new=0`,
  `PRIOR-ART ok=False urls=0` (wave-2 evidence not in the lane tree at that tip), `PREDICATE R52-C1 fail`, `R52-C1-A5 fail`. C2 `72/72 rows=74`, pass, selftest 3/3.
  **The L1 must refresh the header's "state at draft tip" lines from the landing revision's receipts** — they are time-stamped, not final.
- Census: 171 rows at draft time (`validate` → ok, exit 0, 15 W04). Scratch registry with S179–S182 inserted inside `## Registry` and the lessons tree
  present: `validate --file` exit 0, 15 W04, rows 175, tier A=149/B=24/C=2, mined 159. Re-run it at round end with the real lesson on disk.
- Quotes re-located in freshly fetched bodies (sizes equal the scout's): paper 24 words (1,088,268 B), PR #53 body 11 words (API 28,522 B),
  release note 11 words (148,013 B), Z.ai card 12 words (147,928 B); OpenAI page → HTTP 403 re-measured.
- S1 (the paper) is already registered as S020 (`arxiv.org/abs/2601.11868`): the Gate row says re-open S020, not a new row.
  S115 re-open (build-pmars) follows the scribe's receipts; note the scribe's gate draft locates the quote at `:82` while S115's row anchors `:46` — the
  lesson cites neither quote line for S115, only the digest.
- Proposed ids S180–S182 assume S180 is *not* spent on build-pmars (scribe's finding F1). The L1 assigns final ids.

## Integration notes for the L1

- Lesson text refers to `rule_probe.py` only by role ("a rule-behaviour probe … prints PROBE …"). If you want it as a lane file, land it as
  `plans/round52_rule_probe.py` and add a registry row at the same time (it will be advertised once cited in SCORECARD/SKILL/LOG, and C2 would then flag
  it). It has no `--selftest`; stated in Limits.
- The Gate cites S179 numbers from the scribe seat (population counts re-derived by it from the pinned tree); I re-derived only the quotes/digests above.
- `unscreened-population` row does not claim a landed fix. Do not upgrade it without one.
- Prior-art leg and `CONFIRMED` are unchanged by this seat; the Gate's pricing paragraph defers the phenomenon-new case to `prior-art.md`.

## Commands run (cwd = scratch dir; TMPDIR set to `$PWD/tmp` for fetches)

`python3 plans/round52_c1_grader_audit.py --lane .`, `…/round52_c2_registry.py --lane .` (+`--selftest`), `python3 rule_probe.py <lane>`,
counter copies with three mutations then `--selftest --lane <lane>`, `tight.py`, `git init` fixture under scratch + `plans/log_appendonly.py --lane <fx>`
(rewrite → `VIOLATION`, exit 1; append → `violations=0`, exit 0) and on the lane `--since 30801b4`, `curl` of the paper/PR #53 API/release note/Z.ai card/OpenAI page,
`scripts/sources-census.sh validate|census [--root … kengaku | --file <scratch registry>]`, `git log --diff-filter=A` over the 28 paths,
`grep -rEl 'hf_[A-Za-z0-9]{30,}'` over the captures (0) and a synthetic fixture (1). No tool installed or upgraded. No git/jj mutation outside a scratch fixture
(`git rev-parse --show-toplevel` asserted before the fixture commits). Nothing written in the lane tree except this report dir.

Scratch: everything except `lesson.md` removed before yield; `lesson.md` left at the path the item named.
