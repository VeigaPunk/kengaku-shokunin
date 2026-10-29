# W2CritA1Amendment — wave 2 (falsify), round 52, critic

Scope: attack Amendment A1 (per-test P1 classification and hardened CONFIRMED leg) and Amendment A5
(additive exclusion predicate) of R52-C1. Read-only against the lane. No lane file, `.ufo/state`,
or sibling artefact was written. Fixtures were scratch copies, now pruned. This seat did not confirm
any finding and is not a second reader for leg 3.

## Verdicts

- **A1: fitted rule (as implemented).** The correction's direction is legitimate (the frozen
  file-level V1 label is false for `pytorch-model-recovery` and `torch-tensor-parallelism`). But the
  amended rule misclassifies the two tests A1 cites as its evidence, the candidate pool keeps the
  falsified label through an OR-clause that A1's text does not describe, eligibility widens 2 → 29
  under an unchanged threshold of 2, and the "same vocabulary" and "stricter, never weaker"
  statements are false.
- **A5: honest-additive, with one demonstrated gap.** The literal verdict stays printed and drives the
  exit code; A5 cannot pass while the confirmation and prior-art legs are unlanded. But the capture
  leg reads 184 of 184 when the excluded path is present locally and a different file is absent with
  `EXCLUDED.md` re-pointed. The "digest pin" is a self-consistency check between two lane files.

## What I attacked and what I measured

| # | attack | command / source | measured |
|---|---|---|---|
| 1 | Freeze vs amendment diff | `git diff 1315234 HEAD -- plans/round-52-claims.md` (numstat `111 0`); `git diff 1315234 HEAD -- plans/round52_c1_grader_audit.py \| grep '^-'` | Claims file: insertion-only. Counter removed the frozen `candidate = cls in (V1,V4)` line and the frozen CONFIRMED checks (no candidate check, no quote-in-bytes check). |
| 2 | Frozen-rule run | `git show 1315234:plans/round52_c1_grader_audit.py > frozen_c1_counter.py; python3 frozen_c1_counter.py --lane <lane>` | `CANDIDATES total=2` (pytorch-model-recovery, torch-tensor-parallelism); `CONFIRMED new=0`. |
| 3 | Current counter | `python3 plans/round52_c1_grader_audit.py --lane <lane>` | `TASKS classified=88`, `CAPTURES present=183`, `CANDIDATES total=29`, `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0`, `LABELS 0 of 0`, `PREDICATE R52-C1 fail` (exit 1); `A5 CAPTURES 184 of 184`, `A5 TASKS 89 of 89`, `PREDICATE R52-C1-A5 fail`. |
| 4 | Cited-example classes | `python3 a1_probe.py <lane>` §1 | `test_model_file_exists` → **P3** (comment word "in", bare `\bin\b` in VALUE); `test_parallel_linear_exists` → **P2** (non-test helper `_setup_process_group` absorbed into its block, matches `dist\.`); `test_bn_sample_exists` → P1 (correct). |
| 5 | Pool: text vs code | §2 | Text ("≥1 P1") gives 27; code ("P1 OR V1/V4") gives 29. The two extra have 0 P1 tests. 27/27 P1 tasks already have a file-level content/behaviour check. |
| 6 | Vocabulary sensitivity | §3 | P1 tasks: as coded 27; comments/docstrings stripped 36; minus bare `in` 41; comparison-only 43. Threshold unchanged. |
| 7 | P1 as a weakness class | §5 | P1 tests: 25 gate-like (artefact named by another content test), 2 sole-check, 6 no path literal. |
| 8 | A5 silent-deletion mutation | scratch copy: delete `bn-fit-modify/tests/test.sh`, re-point `EXCLUDED.md` at it | `CAPTURES present=182`; `A5 CAPTURES 183 of 184`; `PREDICATE R52-C1-A5 fail`. A simple silent deletion is caught. |
| 9 | A5 swap | scratch copy: placeholder bytes present at the excluded path (scratch SHA256SUMS line rewritten for it), `bn-fit-modify/tests/test.sh` deleted, `EXCLUDED.md` re-pointed | `CAPTURES present=183`; `A5 CAPTURES 184 of 184`; `A5 TASKS 89 of 89`. The capture leg credits the swapped absence. Literal still fails. |

## Could the claim have been met without A1?

Yes, in principle. The frozen pool was exactly two tasks, and leg 3 required two independent
confirmations with verbatim quotes. Both L1 quotes are verbatim in the captured bytes. The frozen
route was 2-of-2. [INFERENCE] A1 is needed only if one of the two readers rejects. The L1 had already
measured that the file-level label is false for both.

## Timeline (git)

Freeze `1315234` 16:59:33 → wave-1 dispatch (`w1.ready.dispatched`) 17:01:05 → A1 `07ea208` 17:02:56 →
A2/A3 `19bc16c` → integration `28c0018` → A5 exclusion `bfbcb07` → A5 `87301ba`.

## Files produced

- Critique (scratch, item-mandated path): `/fast/scratch/hyaku/kengaku-r52/w2-W2CritA1Amendment/a1-critique.md`
- Probe (scratch): `/fast/scratch/hyaku/kengaku-r52/w2-W2CritA1Amendment/a1_probe.py`, output `a1-probe-output.txt`
- A5 receipts (scratch): `/fast/scratch/hyaku/kengaku-r52/w2-W2CritA1Amendment/a5-receipts.txt`
- Copies in this report dir: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritA1Amendment/receipts/` (critique, probe, probe output, A5 receipts, current counter output, frozen-rule run, frozen counter source)
- Top-level scoped findings: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritA1Amendment.md`

Scratch fixtures `a5-mut` and `a5-swap` were removed after their receipts were copied. The critique and
probe stay in scratch because the item names that path for L1 integration.

## Not done / limits

- No confirmation, prior-art or label was produced or assessed. None of those files exist at the tip.
- The P1 sole-check is a path-literal heuristic. I did not run a stub-run (grader against a placeholder
  artefact), which is the test I recommend.
- Tools: none installed. Python 3 stdlib only. No pacman transaction, no `git` mutation.

## What I would freeze instead

Full list in `a1-critique.md`. Short form:

- A1: keep the file-level classes as frozen (record the two V1 labels as measured false positives). Use an
  `ast`-based per-test walk with helper attribution. Candidate = sole-check P1, with text = code and no OR-clause.
  Report the sensitivity band. Confirmation passes on a stub-run receipt, with the verbatim quote kept as a
  necessary check. Name the leg change in the claim.
- A5: print a coverage ratio, not a `PASS` token. Assert set equality of the absent capture paths with the
  excluded path. Pin the excluded digest to a committed upstream receipt. Keep the literal as the only admit verdict.

## Checks for the L1

- Do not admit R52-C1 from the A5 line. Literal verdict is `fail`.
- Fix the A5 swap gap before any closure reads `PREDICATE R52-C1-A5`.
- Do not cite A1's "stricter" or "same vocabulary" statements in the round report.
