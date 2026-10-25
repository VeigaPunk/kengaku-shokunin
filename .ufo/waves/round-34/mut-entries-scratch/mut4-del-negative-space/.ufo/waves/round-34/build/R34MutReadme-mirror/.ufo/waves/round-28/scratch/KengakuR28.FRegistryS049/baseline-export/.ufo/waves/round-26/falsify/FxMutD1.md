# FxMutD1 — eligible-sequence D1 no-op survives selftest
Reviewer: KengakuR26-2.FxMutD1; advisory FALSIFY only; candidate: grader-perturbation-audit draft.
Axes: C1 novelty→canonical coverage/constructs; detector sensitivity, guard preservation, isolation/restoration.
Read claims including POST-OUTPUT Amendment 1, round-26 lesson, and draft; D1 is PC, not MP.
Integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; no live-lane source or Git/jj state writes.
Scratch R=`/tmp/kengaku-r26-FxMutD1-YsTSto`; guard G=`/tmp/kengaku-r26-FxMutD1-YsTSto-guard`.
## Setup and one source mutant
Commands executed (exit 0; mktemp returned R):
```sh
mktemp -d /tmp/kengaku-r26-FxMutD1-XXXXXX
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive --format=tar 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 grader.py plans/grader_perturb.py plans/attrib_calibration.py corpus/evidence/round8-horizon/results.jsonl corpus/evidence/round9-replication/results-r9.jsonl corpus/evidence/round11-power/results-r11.jsonl corpus/evidence/round12-ladder/results-r12.jsonl | tar -x -C /tmp/kengaku-r26-FxMutD1-YsTSto
cp /tmp/kengaku-r26-FxMutD1-YsTSto/plans/grader_perturb.py /tmp/kengaku-r26-FxMutD1-YsTSto/grader_perturb.pristine.py
cp -a /tmp/kengaku-r26-FxMutD1-YsTSto /tmp/kengaku-r26-FxMutD1-YsTSto-guard
```
Only source delta, applied/restored with hashline edit at R/plans/grader_perturb.py:442:
`rec.grader not in ("state", "seq")` → `rec.grader not in ("state",)`.
This makes D1 return None (inapplicable/no-op) for every eligible sequence answer while retaining state behavior.
Guard fixture only: G/corpus/evidence/round9-replication/results-r9.jsonl:9 `ok:true`→`ok:false`; restored afterward.
## Same bounded detectors on pristine, mutant, restored
Each stage ran these exact commands concurrently, each with a 90-second subprocess deadline:
```sh
python3 -B /tmp/kengaku-r26-FxMutD1-YsTSto/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutD1-YsTSto --selftest
python3 -B /tmp/kengaku-r26-FxMutD1-YsTSto/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutD1-YsTSto --summary
python3 -B /tmp/kengaku-r26-FxMutD1-YsTSto/plans/grader_perturb.py --root /tmp/kengaku-r26-FxMutD1-YsTSto-guard --summary
python3 -B /tmp/kengaku-r26-FxMutD1-YsTSto/seq_assert.py
```
Runner invocations: `python3 -B /tmp/kengaku-r26-FxMutD1-YsTSto/probe.py pristine` (then `mutated`, then `restored`); each runner exit 0, child exits below.
| Actual result | pristine | mutated | restored |
|---|---|---|---|
| --selftest exit; D1 k/n | 0; 909/909 | 0; 892/892 | 0; 909/909 |
| --summary exit; policy_checks | 0; 909 | 0; 892 | 0; 909 |
| guard --summary exit | 1 | 1 | 1 |
| minimal sequence assertion exit | 0 | 1 | 0 |
Every selftest printed `SELFTEST D1 PASS`, `SELFTEST MUTATION-CATCH PASS caught=12`, `SELFTEST TOTAL families=10 failed=0`.
Every clean-root run printed population=1964 excluded=0 audited_verdicts=15168 families_with_interval_verdict=9.
All three guard runs emitted the same three ERROR lines (other output varies only with D1 counts):
```text
ERROR corpus/evidence/round9-replication/results-r9.jsonl: sha256 518147f7d5dd90fb29d3d9523117ef4b32641c5c2cf2050bbcc088f907d7205f != frozen c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb
ERROR corpus/evidence/round9-replication/results-r9.jsonl:9 cell='A-INC' pid=101 turn=1: baseline re-grade True != stored ok False
ERROR frozen population mismatch: candidates=1964 population=1963 excluded=1 expected=1964
```
## Missing behavior and minimal failing assertion
Selftest constructs only a state/A-INC D1 record (source :613–615); eligible sequence applicability is untested.
After importing the scratch audit and calling `audit._configure(R)`, the executed assertion is:
```python
raw = '```json\n["beta"]\n```'
rec = audit.Rec('selftest', 1, 'T-DENSE', 1, 2, 'seq', raw, ['beta'], True, ['alpha'])
changed = audit.apply_family('D1', raw, ['beta'], rec)
assert changed is not None and audit._GRADER.extract_json_block(changed) == rec.previous, 'D1 must apply to eligible sequence previous truth'
```
Mutant actual output: `D1_SEQ changed=None`; `AssertionError: D1 must apply to eligible sequence previous truth`.
Pristine/restored output: appended reference block containing `["alpha"]`, followed by `D1_SEQ_ASSERT PASS`.
## Restoration evidence
Source SHA-256 before/restored/live: `8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b`; mutant: `57a2dcdf94bd9d72dd901f589f2d0c9e954984d7e76fa7d38ead21824b2f8eb5`.
Guard input SHA-256 before/restored: `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`; tampered: `518147f7d5dd90fb29d3d9523117ef4b32641c5c2cf2050bbcc088f907d7205f`.
`cmp` exit 0 for restored source versus pristine backup, restored guard versus original input, and pristine/restored selftest, summary and guard stdout byte pairs.
Logs: R/{pristine,mutated,restored}-{selftest,summary,guard,seq_assert}.{stdout,stderr}; commands/exits in R/{pristine,mutated,restored}-results.json.
Python 3.14.8; tool installs/updates: none. No model/network traffic, services, production code changes or admission judgment.
VERDICT: SURVIVED --selftest: one-line D1 applicability loss silently removes 17 policy checks; proposed sequence assertion kills it; pin/baseline guards remain red on tampering; exact bytes restored.
