# FxMutF1 — wrong-answer-span mutation probe
writer: KengakuR26-2.FxMutF1
candidate: grader-perturbation audit draft; lane-dispatched advisory only, not admission or outside verification.
revision: integration 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 (from integration-revision.txt).
Axes: F1 transform fidelity; selftest sensitivity; pin/baseline guard stability; exact restoration.
Read: plans/round-26-claims.md including POST-OUTPUT Amendment 1 and Amendment 2; corpus/lessons/round-26.md; draft grader-perturbation-audit.md.

## Isolated inputs and one audit mutant
Scratch S = /tmp/kengaku-r26-FxMutF1-Jci2H6; guard roots are S-pin and S-baseline.
Export command (exit 0):
```sh
git --git-dir=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 grader.py plans/grader_perturb.py plans/attrib_calibration.py corpus/evidence/round8-horizon/results.jsonl corpus/evidence/round9-replication/results-r9.jsonl corpus/evidence/round11-power/results-r11.jsonl corpus/evidence/round12-ladder/results-r12.jsonl | tar -x -C /tmp/kengaku-r26-FxMutF1-Jci2H6
```
Only S/plans/grader_perturb.py:404 changed: `match = _answer_fence(raw)` → `match = FENCED_RE.search(raw)` inside F1. It strips the first rather than last matched fence; F2 and all other branches remain untouched.
Expected detector: existing _selftest_check at plans/grader_perturb.py:571–572 requires one remaining fence, extraction {"x":0}, and False regrade on the two-fence fixture (:598). Wrong-span stripping must fail that check.

## Same bounded commands on pristine / mutated / restored bytes
Each stage ran these four commands concurrently, each with a 180-second deadline, cwd /tmp:
```sh
python3 -B /tmp/kengaku-r26-FxMutF1-Jci2H6/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutF1-Jci2H6 --selftest
python3 -B /tmp/kengaku-r26-FxMutF1-Jci2H6/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutF1-Jci2H6 --summary
python3 -B /tmp/kengaku-r26-FxMutF1-Jci2H6/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutF1-Jci2H6-pin --summary
python3 -B /tmp/kengaku-r26-FxMutF1-Jci2H6/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutF1-Jci2H6-baseline --summary
```
Guard controls, held fixed across stages: pin root has one extra blank JSONL line; baseline root changes grader.py:225 from `got == want` to `got != want`, leaving all evidence pins intact.
Exit vectors (pristine, mutated, restored): selftest **0,1,0**; clean summary **0,0,0**; pin summary **1,1,1**; baseline summary **1,1,1**. All 12 stderr streams empty; no deadlines reached.
Pristine/restored output: `SELFTEST F1 PASS`; `SELFTEST MUTATION-CATCH PASS caught=12`; `SELFTEST TOTAL families=10 failed=0`.
Mutant output (exact):
```text
SELFTEST F1 FAIL: AssertionError: 
SELFTEST MUTATION-CATCH FAIL: caught=10 expected=12
SELFTEST TOTAL families=10 failed=2
```
Clean summary F1 changes from k/n=1802/1819 to 1819/1819; MULTI changes from 14/31 to 31/31. Thus summary alone masks the registered counterexample; it is not the transform-correctness detector.
All three clean summaries print `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`.
Pin guard errors are identical in all stages: actual fd7f325d8c0e47972a594569bd2d3e1c3d4c281334e5bfdec5864850125e406b differs from frozen bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204.
Baseline guard errors are identical in all stages: 1708 baseline mismatches plus `ERROR frozen population mismatch: candidates=1964 population=256 excluded=1708 expected=1964`; no pin-error lines.
Full exact argv/output/exits: /tmp/kengaku-r26-FxMutF1-Jci2H6/pristine.json, /tmp/kengaku-r26-FxMutF1-Jci2H6/mutated.json, /tmp/kengaku-r26-FxMutF1-Jci2H6/restored.json; corresponding stage-case.stdout/.stderr files retain raw streams.

## Restoration evidence and scope
SHA-256 of audit script, before: 8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b
SHA-256 of audit script, mutant: 4ed64bd2fdbe453c22d0ac4a603b2c74e24cdf82c55d6dd98427e37804722bb0
SHA-256 of audit script, restored: 8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b
Restoration command (exit 0): `cp /tmp/kengaku-r26-FxMutF1-Jci2H6-pristine.py /tmp/kengaku-r26-FxMutF1-Jci2H6/plans/grader_perturb.py`.
Exact byte comparison with backup is True; restored stdout/stderr equal pristine for every command. Both guard-control files were subsequently copied back from S (cp exits 0; exact byte comparisons True).
Restoration receipt: /tmp/kengaku-r26-FxMutF1-Jci2H6/restoration.json. No live production file or repository state was mutated; this report is the sole lane write.
Tools: existing Python 3.14.8; no installs or updates. No other checks, endpoint traffic, or admission judgment.
VERDICT: KILLED — existing --selftest rejects the plausible F1 first-fence mutant; --summary pin/baseline guards remain effective; exact scratch bytes restored. Scoped result only, not general F1 applicability coverage.
