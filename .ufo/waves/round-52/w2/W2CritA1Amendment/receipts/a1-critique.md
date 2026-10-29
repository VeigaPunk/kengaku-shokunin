# W2CritA1Amendment — critique of R52-C1 Amendments A1 and A5 (read-only)

Seat: W2CritA1Amendment (critic). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin, tip `87301ba`.
Scope: attack A1 (per-test P1 classification, hardened CONFIRMED leg) and A5 (additive exclusion
predicate). No lane file was edited; every fixture is a copy under scratch. Reproduce the numbers
with `python3 a1_probe.py /home/vgpnk/Projects/shokunin/kengaku-shokunin` (output in `a1-probe-output.txt`).

Caveat on independence: this seat read the captured graders for the cited tests in order to test the
rule. It did not confirm any finding and does not count as a second reader for R52-C1 leg 3.

## Verdicts

- **A1: fitted rule (as implemented).** The direction of the correction is legitimate: the frozen
  file-level V1 label is false for the two tasks it flags. But the amended rule does not measure
  what A1 says it measures, and the candidate pool still contains the falsified label. A1's
  "stricter, never weaker", "same marker vocabulary" and "not tuned" statements do not survive a
  read of the code.
- **A5: honest-additive, with one demonstrated gap.** The literal verdict stays printed and drives
  the exit code, and A5 cannot pass without the confirmation and prior-art legs. But the
  digest "pin" is a self-consistency check between two lane files, and the capture count can be
  made to read 184 of 184 for a swapped absence. Close the gap before any closure reads the A5 line.

## A1 — evidence

**E1. The rule fails its own motivating examples** (`a1-probe-output.txt` §1):

| task / test | A1 says | amended counter says | cause |
|---|---|---|---|
| pytorch-model-recovery / `test_model_file_exists` | presence-only (P1) | **P3** | the word `in` in a *comment* inside the block (`# Reference the directory the agent operated in …`) matches the bare `\bin\b` in VALUE |
| torch-tensor-parallelism / `test_parallel_linear_exists` | presence-only (P1) | **P2** | the test block is cut only at `def test_`, so the following non-test helper `_setup_process_group` (containing `dist.init_process_group`) is absorbed into this test and matches BEHAV_T `dist\.`; the docstring `in the expected directory` also matches VALUE |
| bn-fit-modify / `test_bn_sample_exists` | presence-only | P1 | correct |

The two falsified tasks therefore have **zero P1 tests** under the amended counter
(`presence_only=-` in `c1-after.txt`). The selftest cases (`c1-selftest.txt`) are four toy
blocks and do not include either cited test, so the selftest passes while the motivating examples
misclassify.

**E2. The code and the text disagree on the candidate definition.** A1 text: "A task is a vacuity
candidate when ≥1 of its tests is P1." Code (`plans/round52_c1_grader_audit.py`, `collect`):
`"candidate": bool(p1) or cls in ("V1", "V4")`. The OR-clause is not in the amendment text. It
admits exactly the two tasks whose file-level label A1 declares false:
`candidates with zero P1 tests admitted only by the V1/V4 OR-clause: ['pytorch-model-recovery', 'torch-tensor-parallelism']`.
The amended text would give a pool of **27**, not 29.

**E3. "Stricter, never weaker" is false for eligibility; true only against the frozen code.**
- Frozen *prose* (claims §Claim 1, leg 3): a confirmed task must be "flagged by the instrument".
  Frozen *counter* (`git show 1315234:plans/round52_c1_grader_audit.py`, `verdict`): counts any
  never-read task with a quote, a reader and `confirmed` — no candidate check and no quote-in-bytes
  check. The frozen code was looser than the frozen prose.
- Measured with the frozen counter (`frozen-rule-run.txt`): `CANDIDATES total=2`
  (pytorch-model-recovery, torch-tensor-parallelism).
- Amended: pool **29** (27 P1 tasks + the 2 above), ~14.5× the frozen flagged set, with the same
  `CONFIRMED ≥ 2` threshold.
- So A1 adds two checks the frozen code lacked (candidate membership, verbatim quote) — stricter
  than frozen code — and widens eligibility from 2 to 29 — looser than frozen prose. The
  "never weaker" sentence in A1 is wrong on eligibility. A1 should say both.

**E4. "Same marker vocabulary" is false.** The file-level CONTENT/BEHAVIOUR regexes are unchanged
(confirmed: `git diff 1315234 07ea208` has no hunk at those lines). The per-test layer adds:
VALUE = `== != <= >= [<> allclose len( np\. torch\. .keys() \bin\b` and BEHAV_T adds
`multiprocessing mp\. threading dist\.`. The added tokens `torch.`, `allclose`, `.keys()` and
`dist.` are the exact idioms of the three graders the L1 had hand-read (`bn-fit-modify`,
`pytorch-model-recovery`, `torch-tensor-parallelism`; A1 receipt). This is the fitting tell:
the vocabulary was extended with the tokens of the graders that motivated the change, and the
result misclassifies them anyway.

**E5. P1 is a weak weakness class for a benchmark grader.**
- All **27 of 27** P1 tasks already carry a content or behaviour check at file level (V2/V3). The
  per-test split adds a flag only where a presence test sits beside other tests.
- In **25 of 33** P1 tests the artefact path is named by another P2/P3 test in the same grader
  (`a1-probe-output.txt` §5, path-literal heuristic). Presence-then-content is the normal shape of a
  TB2 grader; a presence test is a gate, not a vacuity.
- Sole-check (artefact named by no other content/behaviour test): **2** tasks with a literal
  (hf-model-inference, sam-cell-seg), **6** P1 tests with no path literal (undecidable by this
  heuristic). A presence-only check that is the sole check on the output is the only version of
  this class that says something about task validity, and it is a handful of tasks.
- Under a presence-only class, the "graders can be satisfied by an artefact's presence" claim is
  about a prerequisite. It does not show the task's correctness is unchecked. The class that
  does is a stub-run: run the grader against a placeholder artefact and see whether it passes.

**E6. The pool is an artefact of unfrozen vocabulary choices** (`a1-probe-output.txt` §3):

| variant (same 89 graders) | P1 tests | P1 tasks |
|---|---|---|
| as coded | 33 | 27 |
| as coded, comments/docstrings stripped | 46 | 36 |
| as coded minus bare `in` | 59 | 41 |
| comparison-only, original BEHAVIOUR | 61 | 43 |

The frozen threshold (`CONFIRMED ≥ 2`) does not move while the candidate pool moves 27 → 43. The
as-coded variant is the most conservative of those measured, so this is not evidence that A1 was
tuned upward. It is evidence that the leg's effective difficulty is set by unfrozen code choices.

**E7. Could the claim have been met without A1?** Yes, in principle. The frozen pool was exactly
two tasks. Two independent readers confirming the L1's verbatim presence asserts
(`assert hello_path.exists()` in pytorch-model-recovery; `assert parallel_linear_path.exists()` in
torch-tensor-parallelism; both verbatim in the captured bytes) would have met leg 3 as written.
The frozen route was 2-of-2. A1 is needed only if one of those two is rejected. [INFERENCE] The L1 expected that case, since the L1 had already measured that the file-level label is false for
both. The amendment therefore widens the pool at the point where the frozen pool was failing,
and its threshold stays at the frozen 2. The A1 receipt shows the L1 measured the population before
writing A1 (disclosed). Timeline (`git log`): freeze `1315234` 16:59:33 → wave-1 dispatch
`w1.ready.dispatched` 17:01:05 → A1 `07ea208` 17:02:56.

**What is right about A1:** the disclosure is complete (receipt `a1-observation.txt`, A4
correction of 54/42 to 33/27, the frozen pool and threshold both printed). The per-test unit is a
principled response to a real false positive.

### What I would freeze instead (for the closure to choose from)

1. Keep the file-level classes and V1/V4 exactly as frozen. Record the two V1 labels as a measured
   false-positive result for the frozen vocabulary (2 of 2 hand-checked V1 labels false), not as
   something to patch out of the pool.
2. Replace the regex split with an `ast`-based per-test walk: parse the grader, attribute every
   non-test helper to the tests that call it, and classify by AST assertion shape. Comments and
   docstrings then cannot match. Freeze the AST rule and its selftest, with both cited tests as
   fixtures: `test_model_file_exists` must be P1, `test_parallel_linear_exists` must be P1 once the
   helper is removed from its block.
3. Define the candidate as the sole-check P1 (presence-only test whose artefact is not read or run
   by any other test in the same grader), with **text = code**; no OR-clause.
4. Report the pool with the sensitivity band from E6 and name the variant that is frozen.
5. Make the confirmation pass condition a **stub-run receipt**: the grader, run in the TB2 harness
   against an empty or wrong-content artefact, passes. The verbatim quote stays as a necessary
   check, not a sufficient one. Keep `CONFIRMED ≥ 2`, the kill rule and the score rule.
6. State in the claim, not in a footnote, that leg 3 changed from "flagged, quote, reader" to
   "stub-run pass", and cite the eligibility numbers before and after.

## A5 — evidence

**What holds.**
- The literal verdict is printed and drives the exit code: current tip gives `PREDICATE R52-C1 fail`,
  `CAPTURES present=183`, `TASKS classified=88`, exit 1 (`c1-current.txt`).
- `ok_without_capture_legs` requires `len(conf_new) >= 2` and `pa_ok`. A5 cannot pass while the
  confirmation or prior-art legs are unlanded. Those files do not exist at the tip
  (`corpus/evidence/round52/` has no `confirmations.json`, `prior-art.md` or `labels.json`).
- Silent deletion of a non-excluded file is caught. Scratch copy `a5-mut` (`bn-fit-modify/tests/test.sh`
  deleted, `EXCLUDED.md` re-pointed at it with its SHA256SUMS digest): `CAPTURES present=182`,
  `A5 CAPTURES present+pinned_excluded=183 of 184`, `PREDICATE R52-C1-A5 fail`. Because the
  original GH013 absence becomes unpinned, the arithmetic exposes the swap.

**The gap (demonstrated).** Scratch copy `a5-swap`: restore the excluded path locally (a
placeholder with its digest written into the scratch SHA256SUMS; the real bytes would also pass),
delete `bn-fit-modify/tests/test.sh`, and re-point `EXCLUDED.md` at it with its digest. Output:
`CAPTURES expected=184 present=183`, `A5 CAPTURES present+pinned_excluded=184 of 184`,
`A5 TASKS classified+excluded=89 of 89`. The A5 capture leg credits the swapped absence. The
counter never checks that the excluded path is the *only* absent path, or that the excluded bytes
are absent locally. The swap needs the GH013-flagged bytes to be present in the tree, which the
operator decided against, so this is a policy gap as much as a counter gap. The counter cannot
see the policy.

**Other notes.**
- The "digest pin" is `EXCLUDED.md`'s sha256 compared with the SHA256SUMS line. Both are
  lane-authored. The counter does not fetch upstream. The upstream check exists only as a sibling
  side probe (`.ufo/waves/round-52/w2/W2ExecCapturesVerify/report.md`, line 27: upstream bytes sha256
  `57e4904177ac…b59e`, 2687 B). That receipt is not an input to the counter.
- `excluded_captures` uses `re.search` and so reads only the first excluded path. A5 can absorb at
  most one absence, which is why the single-deletion mutation fails. That bound is the only thing
  stopping a larger swap.
- A5 labels a task with no record ("capture absent") as "classified+excluded". The label is honest
  in print. The leg name is not: "classified" now counts a task that was never classified.
- A5 says it "changes no frozen rule". It adds a second predicate that redefines leg 2 for one task.
  That is additive, but a second admit-capable line is a choice point, and the claim says "the
  closure can rule on both readings". Deferring the ruling this way is the thing to avoid.

### What I would freeze instead for A5

1. Print the exclusion as a coverage ratio (`classified 88 of 89; 1 excluded by operator decision,
   GH013, digest pinned to <upstream receipt file>`). No `PASS` token on the A5 line.
2. Assert set equality: the set of absent capture paths must equal `{excluded path}`. The swap
   fails under this rule, and so does any other single absence.
3. Assert the excluded path is absent locally, and pin its digest to a committed upstream receipt,
   not to `EXCLUDED.md` text.
4. Keep the literal verdict as the only verdict that feeds the kill rule.

## Summary table

| attack | result |
|---|---|
| A1: does it change a threshold/target/population/kill? | No threshold, target, population or kill rule changed. The frozen candidate predicate (leg 3, "flagged") changed by an OR-clause and two added checks. |
| A1: stricter or looser? | Stricter vs frozen code (candidate + quote checks). Looser vs frozen prose (eligibility 2 → 29, 14.5×). |
| A1: could the claim be met without it? | Yes in principle: 2-of-2 frozen route, with verbatim quotes available. |
| A1: is P1 the right weakness class? | No as framed: 27/27 P1 tasks already have content/behaviour checks; 25/33 P1 tests are gates; the pool swings 27–43 on vocabulary. |
| A1 verdict | **fitted rule (as implemented)** |
| A5: does the literal verdict stay? | Yes: fail, 183/184, 88/89, exit 1. |
| A5: does it launder a miss? | Not in the landed tree (no confirmations or prior-art yet). Demonstrated gap: capture leg reads 184 of 184 after an absence swap. |
| A5 verdict | **honest-additive, with one demonstrated gap to close** |
