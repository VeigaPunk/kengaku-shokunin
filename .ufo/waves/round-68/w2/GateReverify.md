# GateReverify — round 68, attempt 2, w2

Axes: coverage and calibration. Scoped result: R68-C2 re-derived green; selftest refused all five injected defects; both targeted E1 attacks refused. No predicate, counter, case, kill rule, target, or implementation file changed.

## Byte provenance

Read `plans/round-68-claims.md` in full, including Amendments A1/A2, and all 238 lines of `plans/round68_c2_correction_gate.py`.

The actual lane HEAD and origin/master were both `7803bdd4da5bda14713f23dae8278aef479b9c19` (A2 freeze), whose parent is the assignment's `0e52fb5d` landing. Initial status showed untracked concurrent wave artifacts, not a pristine tree; none were modified by this seat. Before the targeted attacks, the driver compared the working gate and all five named fixture inputs against `git -C L show HEAD:<path>`: all six were byte-identical. Retained hashes and equality results: `GateReverify/committed-bytes.txt` (relative to this report's directory).

Gate SHA256: `1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d`.

## Commands, exits, and exact results

Commands below ran with lane-root cwd; each receipt records the command, actual stdout/stderr, and in-runner `rc=` capture. Scratch work was explicitly under `/fast/scratch/hyaku/kengaku-r68/GateReverify`.

### Landed tree

`python3 plans/round68_c2_correction_gate.py` — rc 0. Receipt: `GateReverify/green.txt`.

```text
E1 ok section present, correct-sha=True, wrong-sha-named=True
E2 ok 7-refused=True, 1-accepted-by-design=True
E3 ok probe-line=True, selftest-line=True, rc-capture=True, probe-rehash=ok
E4 ok pipeline-row=True, sqlite-row-strict=True
E5 ok recipe-unexecuted=True, executed-2-of-3=True
DEFECTS n=0
PREDICATE R68-C2 pass
rc=0
```

### Frozen selftest

`python3 plans/round68_c2_correction_gate.py --selftest --work /fast/scratch/hyaku/kengaku-r68/GateReverify/gate` — rc 0. Receipt: `GateReverify/selftest.txt`.

```text
E1 defect ## Erratum (round 68) section absent in plans/round-67-claims.md
E2 defect no erratum section
E3 defect corpus/evidence/round68/r67-probe-selftest.txt missing (probe re-hash ok)
E4 defect pipeline-row=False, sqlite-row-strict=False
E5 defect no erratum section
DEFECTS n=5
PREDICATE R68-C2 fail
SELFTEST defects-in-fake=5 want=5 all-fail=True
rc=0
```

The inner fake-tree check fails as intended; the outer selftest succeeds. Its `all-fail=True` also requires the inner check's exit to equal 1.

### E1 exactly-one attack

Built `S/fakeroot/duplicate-heading` from HEAD bytes of these five files: `plans/round-67-claims.md`, `corpus/evidence/round68/r67-probe-selftest.txt`, `plans/round67_c1_pipeline_probe.py`, `SKILL.md`, and `corpus/evidence/round67/pipe/a1-mutants.txt`. Appended exactly `\n## Erratum (round 68)\n` to the copied claims file, leaving all other bytes unchanged.

`python3 plans/round68_c2_correction_gate.py --root /fast/scratch/hyaku/kengaku-r68/GateReverify/fakeroot/duplicate-heading` — rc 1. Receipt: `GateReverify/e1-duplicate-heading.txt`.

```text
E1 defect ## Erratum (round 68) heading count 2 (want exactly 1)
E2 ok 7-refused=True, 1-accepted-by-design=True
E3 ok probe-line=True, selftest-line=True, rc-capture=True, probe-rehash=ok
E4 ok pipeline-row=True, sqlite-row-strict=True
E5 ok recipe-unexecuted=True, executed-2-of-3=True
DEFECTS n=1
PREDICATE R68-C2 fail
rc=1
```

Amendment A1 item 3 is live: duplication alone triggers E1, while E2–E5 remain green.

### E1 golden-sha-only attack

Independently mirrored the same five HEAD files into `S/fakeroot/golden-only`. Within the copied round-68 erratum section only, replaced every occurrence of `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` with `[removed wrong sha for E1 attack]`; retained the golden SHA and all E2/E5 correction text.

`python3 plans/round68_c2_correction_gate.py --root /fast/scratch/hyaku/kengaku-r68/GateReverify/fakeroot/golden-only` — rc 1. Receipt: `GateReverify/e1-golden-only.txt`.

```text
E1 defect section present, correct-sha=True, wrong-sha-named=False
E2 ok 7-refused=True, 1-accepted-by-design=True
E3 ok probe-line=True, selftest-line=True, rc-capture=True, probe-rehash=ok
E4 ok pipeline-row=True, sqlite-row-strict=True
E5 ok recipe-unexecuted=True, executed-2-of-3=True
DEFECTS n=1
PREDICATE R68-C2 fail
rc=1
```

## Committed-receipt comparison

The comparison driver extracted fresh stdout by removing only the command trailer/header and `rc=` wrapper, and fetched both historical receipts with read-only `git show HEAD:<path>`.

- Fresh green stdout exactly equals committed `corpus/evidence/round68/c2-green.txt`: **True**.
- Fresh selftest's inner red stdout exactly equals committed `.ufo/waves/round-68/w1/gate/red-before.txt`: **True**.
- Green versus historical red-before is the expected transition: all E1–E5 defect → ok, `DEFECTS n=5` → `n=0`, predicate fail → pass. No unexpected output drift.
- Historical receipt files themselves contain no `rc=` line; their exits are not inferred here. Fresh exits are captured explicitly above.

Retained comparison: `GateReverify/comparison.txt`. The fixture/comparison driver completed successfully (rc 0), asserting both attack exits were 1, each had exactly one defect (E1), E2–E5 passed, and both historical stdout comparisons were equal.

## Findings, limits, and cleanup

No scoped blocker or new R68-C2 defect found. The gate checks correction presence/self-consistency, not the round-67 probe's behavior. Although the requested fixture mirrors five named files, `check()` actually reads four: `A1_MUTANTS` is copied by selftest but not checked by the predicate. This is an observed coverage boundary, not a changed rule or a failed frozen E1–E5 condition. The selftest bundles all five failures in one fake tree; the two extra E1 fixtures isolate its duplicate-heading and missing-wrong-SHA clauses.

No LSP tool was available in this seat's exposed tool inventory; no symbol refactor was performed. No tools installed or upgraded. No git writes, network listeners, or unrelated gates/builds/tests/formatters were run. Only the scoped report and six receipt files were retained. Scratch was removed and absence confirmed before reporting; no scratch defect remains.

Self-evaluation (1–5): accuracy 5 (captured outputs, exits, and committed-byte bindings); completeness 5 (all assigned runs, attacks, comparisons, cleanup); clarity 4 (full output duplication increases length); actionability 5 (six explicit receipt paths); conciseness 4 (commands repeated in receipts and report). Overall 4.6; the retained repetition supports the requested audit trail. Would the user agree? Expected, based on exact requested evidence; no broader acceptance judgment is claimed.
