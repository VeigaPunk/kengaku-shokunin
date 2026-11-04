# Mutation probe: MutantR76

Axes: coverage (declared-row and scope retention), calibration (leg attribution, honest printed counters).
Freeze bytes: `42fad4827797e540c60a00821d3f2f5c18539632`.

## Commands and execution

All paths below are absolute. Shell commands used (each `eval` executes the enclosed shell text):

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/MutantR76"
mkdir -p "$S" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/MutantR76 && git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 42fad4827797e540c60a00821d3f2f5c18539632 | tar -x -C "$S/lane"
```
Setup exit 0. Exactly one shared clone was created; no checkout or other git mutation was run. Initial driver invocation with EXIT cleanup returned 1: live master had advanced to `d76db01c3da0c628d85687c2e6a61c8f059cbb4d`; the freeze assertion refused it. Scratch was removed by the trap.

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/MutantR76"; trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/lane" && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 42fad4827797e540c60a00821d3f2f5c18539632 | tar -x -C "$S/lane" && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/MutantR76/probe.py
```
Second invocation exit 1 **after both matrices and all four C1 probes completed**: the freeze's `emit()` has no `work` keyword (the subsequently edited production script observed during research did). Recorded exception: `TypeError: emit() got an unexpected keyword argument 'work'`. No C2 new mutant had been applied. Scratch was removed by the trap.

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/MutantR76"; trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/lane" && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 42fad4827797e540c60a00821d3f2f5c18539632 | tar -x -C "$S/lane" && C2_ONLY=1 python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/MutantR76/probe.py
```
Remaining C2 probes: exit 0. Scratch removed by EXIT trap. No tools installed/updated.

Final CLI-branch invocation (exit 0; scratch removed by the same EXIT trap):

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/MutantR76"; trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/lane" && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 42fad4827797e540c60a00821d3f2f5c18539632 | tar -x -C "$S/lane" && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/MutantR76/matrices_cli.py
```

`matrices_cli.py` calls each frozen module's `main()` with explicit `--lane`, `--mutants`, and `--work`, exercising argparse and the shipped CLI branch with isolation routing. Receipts: `MutantR76/C1-cli-matrix.txt`, `MutantR76/C2-cli-matrix.txt`. Both returned 0 and printed the same 5/5 and 8/8 expected-id kills below. The earlier direct-function invocation alone was not CLI evidence; this final invocation supplies it.

`probe.py` contains the exact detector calls and fixture transformations. Matrix execution calls the unmodified `mutants()` functions selected by shipped `--mutants`; this is an in-process reproduction, not a claim that the CLI subprocess itself was exercised. For isolation only, two hardcoded C2 scratch destination constants were redirected in memory, and history reads from the archived lane were routed to the production object database read-only, substituting the freeze SHA for `master^{commit}`. No predicate/leg/counter logic was changed. No production files were edited. C1 uses its shipped live localhost listener; HTTP 404 counts as present, as frozen.

## Shipped matrices

### C1
```text
MUTANT M1-drop-marker killed=True expected=UNDECLARED-ABSENT matched=True
MUTANT M2-add-marker killed=True expected=STALE-ABSENT matched=True
MUTANT M3-strip-anchor killed=True expected=NOANCHOR matched=True
MUTANT M4-stale-text killed=True expected=STALE-TEXT matched=True
MUTANT M5-malformed killed=True expected=MALFORMED matched=True
MUTANTS total=5 killed=5 expected_matched=5 wrong_id=0 survived=0
EXIT 0
```

### C2
```text
MUTANT M1-drop-row killed=True expected=MISSING-ROW matched=True
MUTANT M2-open killed=True expected=OPEN matched=True
MUTANT M3-no-close-commit killed=True expected=NO-CLOSE-COMMIT matched=True
MUTANT M4-unresolved killed=True expected=CLOSE-UNRESOLVED matched=True
MUTANT M5-trivial-check killed=True expected=CHECK-TRIVIAL matched=True
MUTANT M6-missing-receipt killed=True expected=LEG-FAIL D6 matched=True
MUTANT M7-missing-d7 killed=True expected=LEG-FAIL D7 matched=True
MUTANT M8-wrong-stamp killed=True expected=LEG-FAIL D2 matched=True
MUTANTS total=8 killed=8 expected_matched=8 wrong_id=0 survived=0
EXIT 0
```

## Findings

1. **HIGH — C2 real scope hole:** `C2-new-zero-scope` deletes ids from the closure text, not ledger rows. All seven legs still pass, scope becomes zero, and `PREDICATE R76-C2 pass` remains rc 0. The frozen R75-D1…D7 universe can disappear without a missing-row defect. Pointer: freeze `scope_ids()` / `emit()`; receipt and full fixture below.
2. **MEDIUM — C2 real check-validation hole:** `C2-new-nonexistent-check-path` changes D5 check to `grep -q 'R75-D5' corpus/does-not-exist.md`. No such committed path is provided, yet CHECK-TRIVIAL admits it and discharge stays seven. This is regex recognition of a path-looking token, not validation of the frozen committed-path requirement. It does not assert checks must execute; the independent legs still run.
3. **MEDIUM — C1 row-prose coverage gap:** `C1-new-stale-third-cell` retains the dated absent marker but adds `is alive` in the trailing cell. The broader frozen claim says no present-tense prose on an absent row; the implementation and its narrower internal rule inspect only `cells[1]`. Survivor is a real row-text coverage gap against that broader sentence, not a counter-output mutation. Pointer: freeze `census()`, `stale_text` comprehension. No predicate wording was changed in this probe.
4. **LOW — C2 reporting-surface limit:** `C2-new-comment-d2` moves the entire D2 correction line into an HTML comment. D2 still reports ok because it searches raw text. This proves visible correction is not enforced, **not** that stamp derivation is broken: the literal stamp and report-tip tokens remain. State/value arms cannot kill a preserved-token reporting mutant. Frozen wording does not explicitly impose rendered visibility on D2, so this is not promoted to a value-leg defect.
5. **INFO — C1 reporting/scope limits:** deleting an absent row and duplicating a present row both survive. The census correctly reports the changed totals (2 or 4); these do not reach the fixed landing target of 11. They are reporting-surface/scope-retention limits, not failures to resolve an existing row. No frozen kill rule requires a duplicate-row detector.
6. **INFO — attributed controls killed:** reanchoring the absent row at `present.md` produces STALE-ABSENT; removing D3's numeric values produces LEG-FAIL D3. Both pristine and restored detectors return 0. All eight new probes have exact fixture-byte restoration and recorded before/mutant/after hashes.

## Per-probe evidence

Each `<name>.txt` includes original and mutant file bytes, full pristine/mutant/restored stdout and rc, and SHA-256 hashes over the complete fixture manifest (sorted relative filename + NUL + file bytes + NUL). `fixtures/<name>/` retains the complete mutated fixture, including the transient listener URL. Rerunning C1 requires a fresh listener as in the driver; the saved old ephemeral endpoint is not a perpetual live fixture.

### C1-new-delete-absent — survived

Expected detector: Scope shrink must not reach fixed target total=11; census may still pass declared rows.

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `PROVINCE.md`; exact bytes: `C1-new-delete-absent.txt` and `fixtures/C1-new-delete-absent/PROVINCE.md`.

```text
SURFACE 1 present present.md (path=present.md)
SURFACE 2 present http://127.0.0.1:45963/x (http=404)
SURFACES total=2 present=2 absent=0 prose=0
AGREE agree=2 disagree=0
PREDICATE R76-C1 pass
```

```text
before   3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
mutant   e4849178fbd9f88b76e703415c56aa6b687246108fc313a93681d23f9e7b71ed
restored 3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
```

### C1-new-duplicate-present — survived

Expected detector: Duplicate row should not falsely count a distinct surface.

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `PROVINCE.md`; exact bytes: `C1-new-duplicate-present.txt` and `fixtures/C1-new-duplicate-present/PROVINCE.md`.

```text
SURFACE 1 present present.md (path=present.md)
SURFACE 2 present present.md (path=present.md)
SURFACE 3 absent ~/r76-definitely-absent-path (path=~/r76-definitely-absent-path)
SURFACE 4 present http://127.0.0.1:45963/x (http=404)
SURFACES total=4 present=3 absent=1 prose=0
AGREE agree=4 disagree=0
PREDICATE R76-C1 pass
```

```text
before   3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
mutant   5dfbf4d73b0bf4bba9d488b80b20307165efcd9986052d57a1e4a9df9cce9edd
restored 3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
```

### C1-new-stale-third-cell — survived

Expected detector: STALE-TEXT on absent row with present-tense prose in trailing cell.

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `PROVINCE.md`; exact bytes: `C1-new-stale-third-cell.txt` and `fixtures/C1-new-stale-third-cell/PROVINCE.md`.

```text
SURFACE 1 present present.md (path=present.md)
SURFACE 2 absent ~/r76-definitely-absent-path (path=~/r76-definitely-absent-path)
SURFACE 3 present http://127.0.0.1:45963/x (http=404)
SURFACES total=3 present=2 absent=1 prose=0
AGREE agree=3 disagree=0
PREDICATE R76-C1 pass
```

```text
before   3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
mutant   378745e5dc4e79f126ac92a13f68b69d3325b55b8cad87c11b0e7f750748c6a3
restored 3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
```

### C1-new-reanchor-present — killed

Expected detector: STALE-ABSENT.

Pristine/mutated/restored exit codes: 0/1/0. Exact restoration: True.

Changed file: `PROVINCE.md`; exact bytes: `C1-new-reanchor-present.txt` and `fixtures/C1-new-reanchor-present/PROVINCE.md`.

```text
SURFACE 1 present present.md (path=present.md)
SURFACE 2 present present.md (path=present.md)
SURFACE 3 present http://127.0.0.1:45963/x (http=404)
SURFACES total=3 present=3 absent=0 prose=0
AGREE agree=2 disagree=1
DEFECT STALE-ABSENT 2 Absent path present.md marked **ABSENT 2026-10-01**
PREDICATE R76-C1 fail
```

```text
before   3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
mutant   9f6fc1a07505d3d19d26f9072e0484cf4a523faf1ac286ebfcbcd37742e5d188
restored 3eb0f66caa8780895b8aadf06a95c590aea366c8b327f75982ccda5806ddb8d0
```

### C2-new-comment-d2 — survived

Expected detector: D2 must require a visible correction, not HTML-comment-only values.

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `SCORECARD.md`; exact bytes: `C2-new-comment-d2.txt` and `fixtures/C2-new-comment-d2/SCORECARD.md`.

```text
SCOPE-SOURCE corpus/lessons/round-75-verifier-spotcheck.md
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 42fad4827797, 5d9a0ccc
LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 42fad4827797
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
LEDGER R75-D1 ok closed close_commit=42fad4827797
LEDGER R75-D2 ok closed close_commit=42fad4827797
LEDGER R75-D3 ok closed close_commit=42fad4827797
LEDGER R75-D4 ok closed close_commit=42fad4827797
LEDGER R75-D5 ok closed close_commit=42fad4827797
LEDGER R75-D6 ok closed close_commit=42fad4827797
LEDGER R75-D7 ok closed close_commit=42fad4827797
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R76-C2 pass
```

```text
before   84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
mutant   ca9151bf6985690917b4dd6f956b14c6748c6d08888c3984d3ec7dd43dc090f3
restored 84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
```

### C2-new-zero-scope — survived

Expected detector: Frozen scope R75-D1 through R75-D7 must not disappear.

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `corpus/lessons/round-75-verifier-spotcheck.md`; exact bytes: `C2-new-zero-scope.txt` and `fixtures/C2-new-zero-scope/corpus/lessons/round-75-verifier-spotcheck.md`.

```text
SCOPE-SOURCE corpus/lessons/round-75-verifier-spotcheck.md
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 42fad4827797, 5d9a0ccc
LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 42fad4827797
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
SCOPE ids=0 registered=0 closed=0 open=0 discharged=0 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R76-C2 pass
```

```text
before   84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
mutant   d3e15a8993f72a8171d6772c61ecfd210ccc498450d638d768df29f6768f091a
restored 84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
```

### C2-new-nonexistent-check-path — survived

Expected detector: CHECK-TRIVIAL for no committed path (only nonexistent path + literal).

Pristine/mutated/restored exit codes: 0/0/0. Exact restoration: True.

Changed file: `corpus/routed-findings.jsonl`; exact bytes: `C2-new-nonexistent-check-path.txt` and `fixtures/C2-new-nonexistent-check-path/corpus/routed-findings.jsonl`.

```text
SCOPE-SOURCE corpus/lessons/round-75-verifier-spotcheck.md
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 42fad4827797, 5d9a0ccc
LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 42fad4827797
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
LEDGER R75-D1 ok closed close_commit=42fad4827797
LEDGER R75-D2 ok closed close_commit=42fad4827797
LEDGER R75-D3 ok closed close_commit=42fad4827797
LEDGER R75-D4 ok closed close_commit=42fad4827797
LEDGER R75-D5 ok closed close_commit=42fad4827797
LEDGER R75-D6 ok closed close_commit=42fad4827797
LEDGER R75-D7 ok closed close_commit=42fad4827797
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R76-C2 pass
```

```text
before   84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
mutant   d604c86ca924ed1da1a4c943be1db6597d00f2bef2647ae35f469434dc453621
restored 84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
```

### C2-new-remove-d3-values — killed

Expected detector: LEG-FAIL D3.

Pristine/mutated/restored exit codes: 0/1/0. Exact restoration: True.

Changed file: `SCORECARD.md`; exact bytes: `C2-new-remove-d3-values.txt` and `fixtures/C2-new-remove-d3-values/SCORECARD.md`.

```text
SCOPE-SOURCE corpus/lessons/round-75-verifier-spotcheck.md
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 42fad4827797, 5d9a0ccc
LEG D3 FAIL SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 42fad4827797
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
LEDGER R75-D1 ok closed close_commit=42fad4827797
LEDGER R75-D2 ok closed close_commit=42fad4827797
LEDGER R75-D3 ok closed close_commit=42fad4827797
LEDGER R75-D4 ok closed close_commit=42fad4827797
LEDGER R75-D5 ok closed close_commit=42fad4827797
LEDGER R75-D6 ok closed close_commit=42fad4827797
LEDGER R75-D7 ok closed close_commit=42fad4827797
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=6 legs_pending=0 wrong=1
LEG-FAIL D3 SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
PREDICATE R76-C2 fail
```

```text
before   84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
mutant   21e9d264ab812305d547fe941fb1531964d7f0fab9746dc94fa3d7cb6506ffbf
restored 84f04903faf4532917257f08b6f6fe9f0b19b10f199c01b85cc4f53553fe61da
```

## Limits and self-evaluation

No production landing verdict, later integrated revision, side-branch mutant, or literal-only-check execution was tested. These probes challenge fixture bytes at the freeze only. Four new mutants per gate were exercised; no baselines failed. The two aborted harness invocations are disclosed above, not counted as killed mutants. Final matrix checks exercised each frozen `main()` with `--mutants`, including CLI argument parsing, with scratch/history routing documented above.

Self-evaluation (overall 4.0/5): accuracy 4 (all outcomes have receipts; in-memory isolation must be retained when reproducing); completeness 4 (eight new probes and both CLI matrices; optional side-branch probe not selected); clarity 4 (distinguishes frozen scope target from row-wise invariant); actionability 4 (complete bytes and executable drivers; listener must be recreated); conciseness 4 (full output intentionally included for audit). Highest-impact improvement: keep fixed-universe scope testing distinct from aggregate printed-target checking. The user should agree because every qualification is tied to an actual invocation or saved artifact.
