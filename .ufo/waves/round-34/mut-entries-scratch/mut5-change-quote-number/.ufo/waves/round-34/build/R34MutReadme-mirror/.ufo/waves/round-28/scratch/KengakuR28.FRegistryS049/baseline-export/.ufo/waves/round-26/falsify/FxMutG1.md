# FxMutG1 — wrong-answer-span mutant survives the designated selftest
Date: 2026-10-21. Seat: KengakuR26-2.FxMutG1; advisory FALSIFY only, not admission/outside verification.
Integration inspected/exported: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`.
Read round-26 claims including explicitly post-output Amendment 1, Amendment 2, lesson, and grader-perturbation-audit draft.
Axes: novelty→canonical coverage/constructs (G1 detector coverage); guard preservation; exact-byte isolation/restoration.
Only this report was written in the live lane; all probe code, exports and fixtures are under `/tmp/kengaku-r26-FxMutG1.nswx1r`.

## Mutant and expected detector
At the exported `plans/grader_perturb.py:456`, replace G1's last-selected-answer `_dump_like(raw, changed_obj)` with first-fence replacement; leave applicability and G2 untouched:
```python
first = FENCED_RE.search(raw)
changed = (raw[:first.start(1)] + json.dumps(changed_obj) + raw[first.end(1):]
           if first is not None else _dump_like(raw, changed_obj))
```
Expected: `--selftest` rejects this G1 transform defect with exit 1. Actual: exit 0, including `SELFTEST G1 PASS`, `SELFTEST MUTATION-CATCH PASS caught=12`, `SELFTEST TOTAL families=10 failed=0`.
Missing behavior: G1's own fixture (`plans/grader_perturb.py:608`) contains only one answer fence; it cannot distinguish first-fence mutation from mutation of the selected last answer. Existing multi-fence checks exercise F1/F2, not G1.

## Exact bounded commands and observed exits
Set `R=/tmp/kengaku-r26-FxMutG1.nswx1r`; paths below expand to absolute paths. No model/network traffic.
Executed `python3 -B /tmp/kengaku-r26-FxMutG1.nswx1r/probe.py pristine`, then the surgical scratch edit, then the same command with `mutated`, then `restored`; each driver exit 0.
Each stage ran these same five commands concurrently (all individual exits retained, not replaced by driver exit):
```sh
/usr/bin/python3 -B "$R/plans/grader_perturb.py" --root "$R" --selftest
/usr/bin/python3 -B "$R/plans/grader_perturb.py" --root "$R" --summary
/usr/bin/python3 -B "$R/plans/grader_perturb.py" --root "$R/pin-root" --summary
/usr/bin/python3 -B "$R/plans/grader_perturb.py" --root "$R/baseline-root" --summary
/usr/bin/python3 -B "$R/g1_span_assert.py"
```
| bytes | selftest exit / failed | summary exit / G1 k/n | pin exit | baseline exit | minimal assertion exit |
|---|---|---|---|---|---|
| pristine | 0 / 0 | 0 / 1021/1021 | 1 | 1 | 0 |
| mutant | 0 / 0 | 0 / 1004/1021 | 1 | 1 | 1 |
| restored | 0 / 0 | 0 / 1021/1021 | 1 | 1 | 0 |
All ordinary stages print `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`.
Mutant summary: `rate=0.983350 cp95_nominal=[0.973475,0.990271] verdict=PASS`; G1 MULTI becomes `17/0@0.000` versus pristine/restored `17/17@1.000`. Composite becomes 136/143, INDETERMINATE. Summary exposes the changed stratum; exit 0 is correctly allowed for family findings.
Pin fixture appends one blank JSONL line only: every stage exits 1 with actual hash `fd7f325d8c0e47972a594569bd2d3e1c3d4c281334e5bfdec5864850125e406b` versus frozen `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204`; baseline population stays 1964/0.
Baseline fixture preserves all pinned evidence; its grader wrapper flips only the first grade_state result. Every stage exits 1: `results.jsonl:11 cell='A-INC' pid=1 turn=1: baseline re-grade False != stored ok True`, plus `frozen population mismatch: candidates=1964 population=1963 excluded=1 expected=1964`; no pin error. Both guards remain failure-capable.

## Minimal failing assertion
With audit module `a` configured against the exported root:
```python
raw = '```json\n{"x": 0}\n```\n```json\n{"x": 1}\n```'
r = a.Rec('minimal', 1, 'A-INC', 1, 2, 'state', raw, {'x': 1}, True, {'x': 0})
assert a.regrade(r, a.apply_family('G1', raw, a._GRADER.extract_json_block(raw), r)) is False
```
Pristine/restored output: `before=True after=False selected={'x': 2}`. Mutant output: `before=True after=True selected={'x': 1}`; assertion fails with `AssertionError: G1 must change the selected last answer, not an earlier fence` (exit 1).
This isolates a selftest coverage gap, not a defect observed in pristine G1 or permission to change the contract. Add this multiblock negative-control assertion rather than weakening the registered selected-answer rule.

## Restoration and retained evidence
Pristine SHA-256: `8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b`.
Mutant SHA-256: `03ae3c4b9ffed7338c8726858fde7e4df04daf6a8adfeba750f80eb2214a0d00` (retained as `$R/grader_perturb.mutant.py`).
Driver restored the backup in `finally`: `RESTORED sha256=8d92314246b96c9e9dec29574f2824b42d87a8fccabf35cbacdd588588f1cc8b exact_bytes=True`.
Before/after `sha256sum` of the live script, scratch target and pristine backup all equal that pristine hash; the restored detector reproduces the pristine outcomes above.
Full exact child commands/stdout/stderr/exits: `$R/{pristine,mutated,restored}/results.json`, plus each stage's `*.stdout`/`*.stderr`; harness `$R/probe.py`, assertion `$R/g1_span_assert.py`.
Tools: existing system Python 3.14.8 and existing git/tar/coreutils; no installs/updates. No live source, Git/jj state, routing or services mutated.
VERDICT: SURVIVED the assigned --selftest (exit 0); KILLED by the supplied minimal last-answer assertion; pin/baseline guards preserved and exact scratch bytes restored.
