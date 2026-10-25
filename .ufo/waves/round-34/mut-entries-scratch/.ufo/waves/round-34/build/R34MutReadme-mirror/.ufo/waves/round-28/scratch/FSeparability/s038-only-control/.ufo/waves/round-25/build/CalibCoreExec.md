# CalibCoreExec — round 25 build, C1 instrument core (novelty → coverage)

Seat KengakuR25.CalibCoreExec (executor, writer). Clone /tmp/kengaku-r25-CalibCoreExec, branch r25-CalibCoreExec at observed base 3f371d2a2ce5ccf1b40b2161210f6591a8320a0a. Not committed; L1 integrates.

## Files changed
- `plans/attrib_calibration.py` (new, untracked, 888 lines, sha256 7c015ea386336bef9ae9181d8a5aa8b4576c02c7b10bc0a80badc6ef33df33ab). Nothing else was written in the clone. In the live lane, I wrote only this report.

## Behavior (shared interface, stdlib only)
- `clopper_pearson`, `wilson`, `verdict`, `parse_receipt`, `rg_bound`; CLI `[--root DIR] [--summary|--json] [--selftest]`; exit codes 0 / 1 / 2 as the interface specifies.
- CP bounds are Beta quantiles found by bisection on grader.py's continued-fraction `betai` (grader.py:879-925). grader.py is imported with importlib and `sys.dont_write_bytecode`, so no `__pycache__` is written. An AST audit of grader's module body found only defs, constants, path joins, `re.compile` and the `__main__` guard.
- P1 scope: only the last `## GT + scoring at close` block of each file counts. Trial-only files print `accuracy 0/0 … interval=UNTESTED`. When two tables are identical on (trial, prediction, GT, chain), the earliest-stamped block is kept and the other is named in `TOTAL … dup=[…]`.
- All 10 blocks (5 in P1, 5 superseded) are checked against their own rows: the `correct` cells, GT counts, ACCURACY, TARGET, BODY, STREAM TARGET and the score_summary JSON. The r23 summary verdict check depends on the instrument version (attrib-r23-stream.log:256 vs :320).
- Estimates: accuracy, recall:<leg>, specificity:<leg> (one-vs-rest), target:<leg>, stream-target:<leg>. The share:<leg> lines also print `rg95=[lo,hi] J_lo=` and show `interval=-` because shares have no bar. min-n is used only to re-derive the stored point verdicts (it appears in --json); the interval rule never uses it.
- If --root has no corpus/evidence, the tool reads that directory's `*.log` files, so fixture trees work.

## Evidence (run from the clone root)
- `python3 plans/attrib_calibration.py --summary` → exit 0. It prints 48 estimate/share lines (full text in my final message), then:
  `TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0 dup=[corpus/evidence/attrib-r22-legs.log:312-362=corpus/evidence/attrib-r22-opencode-trials.log:204-254]`
- How the stored point verdicts changed under the interval rule:
  - attrib-r22-opencode-trials.log:236 target:hyper 10/10, cp95=[0.691503,1.000000]: PASS → INDETERMINATE.
  - :237 target:opencode-go 0/0 and attrib-r23-stream.log:303 stream-target:opencode-go 0/0: FAIL → UNTESTED.
  - Accuracy stays PASS → PASS: attrib-r21-impl-ds-trials.log:297 20/20 [0.831567,1], attrib-r21-impl-glm-trials.log:173 22/22 [0.845627,1], r22-opencode:234 20/20, r23-stream:298 30/30 [0.884297,1].
- `--selftest` → exit 0, `selftest: 11 checks, 0 failed`:
  - A1: 126 known-value anchors.
  - A2: CP bounds checked against direct binomial tail sums for all 0≤k≤n≤40; worst error 3.33e-15.
  - F1/F2: fixture tree with hand-derived verdicts; the CLI exits 0 on it.
  - R1/R1b: a flipped GT cell makes the CLI exit 1.
  - R4: a flipped verdict word makes the CLI exit 1.
  - R3: with dedup turned off, totals.correct is 89 instead of 69.
  - R2: perturbing an anchor value by +1e-6 is caught.
- Red runs on scratch copies of the real receipts (scratch since removed):
  - GT cell flipped at attrib-r22-opencode-trials.log:212 → exit 1 with 8 MISMATCH lines (rows:correct@212, gt_counts@233, accuracy@234, target:hyper@236, score_summary@254 ×4).
  - attrib-r23-stream.log byte-copied as attrib-r23-zdup.log → exit 0, duplicates=2, scored_trials still 92.
  - SciPy anchor literal raised by 1e-6 → `--selftest` exit 1 (A1 FAIL).
- Independent cross-check: all 861 rows of /tmp/kengaku-r25-CpReferenceExec/plans/fixtures/r25/cp_reference.tsv (built from exact fraction tail sums) agree to within 5e-13. The worst case is 4.98e-13 (k=9, n=32, lower bound).

## Findings
1. The power ask binds exactly: PASS=12 equals n_ge_17=12. Every estimate with n<17 comes out INDETERMINATE (11) or UNTESTED (12). There are 0 FAILs, and 0 of the 92 scored trials are incorrect.
2. The deduplicated pair is two different runs whose 20-row tables happen to be byte-identical in all 7 columns. Their journal windows differ (@1792151616..@1792151737 vs @1792151440..@1792151562), and so do their frozen-table sha256 (77b8d4a0 vs 3d7861f8) (attrib-r22-legs.log:313,315 vs attrib-r22-opencode-trials.log:205,207). The frozen identity rule counts them once (n=20, not 40). That is the conservative choice, but the second block is not a copy.
3. The last-block rule drops attrib-r22-legs.log:260-310. That block is run-1, with its own journal window @1792151401..@1792151539, and it holds the lane's only opencode-go ground-truth trial (T03, :270, predicted correctly). The receipt itself calls both blocks authoritative (:378-379). As a result, recall:opencode-go is UNTESTED in every P1 block. This is a candidate amendment for L1; I did not change the rule.
4. claims:43 gives "n=16 → 0.7940", which is a 4-decimal truncation: the exact CP lower bound is 0.794092 (it rounds to 0.7941). No verdict changes. The selftest anchor checks the truncated value.
5. The Rogan–Gladen leg-share bounds carry information only where J_lo>0:
   - glm: devin [0.215205,0.616349], zai [0.383651,0.784795]
   - r22: alibaba and hyper [0.276937,0.723063]
   - r23: alibaba [0.067084,0.369862], hyper [0.630138,0.932916]
   The other 6 bounds are vacuous [0,1], because the leg had either 0 GT trials or 0 non-GT trials.
6. Observed outcomes for the registered predictions (Brier scoring is L1's job): P1 yes, P2 yes, P3 yes (4 of 4), P4 yes (for example recall:devin 9/9), P5 no.

## Risks / limits
- The tool imports grader.py from its own checkout, so any future import-time side effect added there would carry over.
- `--selftest` writes only to a system tempdir, launches the CLI 4 times, and takes about 0.6 s.
- Sibling fixtures are not wired in: CalibSelftestExec's attrib-cal/EXPECTED.tsv and CpReferenceExec's TSV. My selftest is self-contained. L1 can run those fixtures directly with flat-mode --root.

Installs: none (python3 3.14.8, stdlib only).
VERDICT: attrib_calibration.py is implemented in the clone and not committed. It produces 35 interval verdicts and 12 Rogan–Gladen bounds over P1 and re-verdicts all 7 stored verdicts (1 PASS→INDETERMINATE, 2 FAIL→UNTESTED). All 119 stored-line checks re-derive (exit 0), and the selftest passes 11/11, with every red run caught.
