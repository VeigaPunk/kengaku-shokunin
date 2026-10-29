# W2RevA1Intent — round 52 wave 2 (falsify): series intent and Amendment A1

Seat: W2RevA1Intent (revenger, leaf, read-only). Full report with commands, numbers and receipts:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevA1Intent/report.md`
(receipts in `…/W2RevA1Intent/receipts/`).

## The series' question (rounds 35–46)

For one Terminal-Bench 2.0 grader at pin `2fd12b88`: what does the reward bit decide, requirement by
requirement, and what does a reward-1 end state prove? Each entry answers with located byte quotes,
a frozen probe over end states, a falsifier and a Negative-space block. The README scope rows disclaim
quality verdicts: rounds 38–43 "no quality, validity, difficulty or gameability verdict"; rounds 44–46
"no quality claim" (`corpus/README.md:300–308`).

R52-C1 moves this to a population verdict ("grader-vacuity triage"), which the series declined to make
per grader. [INFERENCE on intent.]

## Invariant A1 preserved

- Frozen population, pin and capture digests (`mismatched=0` in the lane copy).
- One-sided queueing: the counter queues graders and never prints clearance.
- Confirmation needs a named second reader and a quote; `CONFIRMED ≥ 2` unchanged.
- Never-read condition (12 hand-read ids reproduced from `tb2-*-grader.md`).
- Dated, pre-after-run disclosure.

## Invariant A1 may have lost (measured on a scratch copy of the lane)

1. **"Located" reading.** AST presence-only oracle: 53 tests / 42 tasks. Counter per-test P1: 33 / 27.
   P1 precision 32/33; recall 32/53 = 60 %. Thirteen new presence-only tasks are never queued
   (e.g. `video-processing`, `headless-terminal`, `tune-mjcf`, `sparql-university`).
2. **"Same marker vocabulary, mechanical split" is false.** The per-test P1/P3 decision uses a comparison
   vocabulary (`==`, `<`, `>`, `len(`, `np.`, `\bin\b`, …) absent from the frozen text, and runs over
   docstrings, comments, assert messages and string literals. File-level labels drift: under the frozen
   literal text V1 = 5, printed V1 = 2 (`bn-fit-modify`, `portfolio-optimization` via an added
   `assert.*\bin\b`; `distribution-search` via the `\b` anchor).
3. **Candidacy ≠ A1 text.** Code: `P1 or V1 or V4`. A1: "≥1 P1". Two tasks are queued only by a file-level
   V1 label that A1 says is false of them.
4. **The A1 example is misclassified.** `torch-tensor-parallelism::test_parallel_linear_exists` is one
   presence assert; the block runs on through non-test helpers containing `dist.` and `torch.allclose`,
   so the amended counter says P2.
5. **The hardened quote leg is a substring test.** A one-word quote (`"exists"`) with a non-empty reader
   yields `CONFIRMED new=2` in a scratch fixture.
6. **The frozen blind-class control no longer kills by its frozen mechanism.** Forcing file-level V0 gives
   `CANDIDATES total=27`, not 0; it is red only because no confirmations exist.
7. **A4 discards a figure that an AST definition reproduces.** 54/42 (superseded) vs 53/42 (AST oracle).
   Different definition, post-hoc; not evidence, but the committed 33/27 under-reports the referent.
8. **The round-38 precedent is not a per-test presence unit.** `build-pmars`'s four tests are none
   presence-only (AST) and all P3 (counter); its finding is provenance-blindness. [INFERENCE: retrofit.]

## Calibration

Measured: items 1–6. Inferred: the intent drift, item 8, and the reading of A4's definition.
Any repair must be a new amendment dated before the after-run, appended to `plans/round-52-claims.md`;
frozen text is not rewritten.

## Not done

No lane edit, no git/jj mutation, no tool install, no peer message. Scratch dir removed after receipts
were copied. Did not re-fetch pinned URLs, did not evaluate A5, did not read all twelve entries end to end.
