# W2MutC1 — mutation test of the AMENDED R52-C1 counter (kengaku round 52, wave 2, falsify)

Seat: W2MutC1 (mutation-tester, leaf, read-only on the lane). Attack target: `plans/round52_c1_grader_audit.py`
at lane base `30801b47` + landed captures (183/184, `sanitize-git-repo` excluded per A5), with
`classify_test()`, `split_tests()`, the candidate rule, and the CONFIRMED checks as the attacked points.
Frozen rules were NOT edited; every mutant is a single-line change in a scratch copy.

## Verdict

The attack **landed**. Measured results:

1. **0 of 16 mutants are killed by any of the four frozen §C1 controls on their named legs.** The
   four frozen controls (`c1-control-nothing`, `c1-control-name-only`, `c1-control-blind-class`,
   `c1-control-drop-capture`) do not exercise the per-test classifier, the candidate rule, or any
   of the CONFIRMED checks. `c1-control-nothing` and `c1-control-name-only` produce no output
  difference for any mutant. `c1-control-blind-class` and `c1-control-drop-capture` do not reproduce
  their stated named signatures on the pristine counter (D6); under blind-class, M08 and M11 print
  `CANDIDATES total=0` while pristine prints 27, so that control cannot be read as a kill signal.
2. Five mutants of the **CONFIRMED leg** (drop quote-verbatim, drop candidate membership, drop
   new-task check, drop `confirmed` flag, lower threshold 2→1) are killed only by probes I built in
   scratch, not by any frozen control. The leg that carries novelty is unguarded by the frozen set.
3. The frozen `classify_test()` has a **real defect** (D1): comments and docstrings reach the
   VALUE regex (`\bin\b` matches English "in"). Two of the three presence-only tests the A1
   hand-read receipt names are **not** P1 in the counter's printed output. Stripping docstrings and
   comments (AST view) gives P1 = 48, not 33.
4. The per-test **split** has a boundary defect (D2): a test block runs to the next `def test_`, so it
   swallows following helper defs and top-level code (10 tests affected); this moves markers between tests.
5. The **candidate rule** in code (`bool(p1) or cls in ("V1","V4")`) is not the A1 text
   ("a vacuity candidate when ≥1 of its tests is P1"); the two extra candidates are exactly the two
   V1 tasks that A1 declares false (D3).

Scope note: I did not fix the counter. Survivors and defects are reported, not repaired.

## Environment and tooling

- Python 3.14.8 (`/usr/lib/python3.14`), stdlib only. **No tool installed or upgraded.** No pacman, no
  `uv`, no network access used.
- Lane counter run only with `--lane` pointing at scratch copies, except the two read-only lane runs below.
- Scratch dir `/fast/scratch/hyaku/kengaku-r52/w2-W2MutC1/` (removed before yield; receipts copied to
  `.ufo/waves/round-52/w2/W2MutC1/receipts/`).

## Commands run (exact)

Read-only, against the lane:

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round52_c1_grader_audit.py --lane .          # exit 1  (A5 fail; literal 183/184, 88/89)
python3 plans/round52_c1_grader_audit.py --selftest        # exit 0  (6 cases, 0 failures)
```

Scratch set-up (copies only; the lane was not written):

```sh
S=/fast/scratch/hyaku/kengaku-r52/w2-W2MutC1; L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
mkdir -p $S/lane-base/plans $S/lane-base/corpus/knowledge $S/mut $S/fx
cp -a $L/plans/round52-tasks.json $S/lane-base/plans/
cp -a $L/corpus/evidence/round52 $S/lane-base/corpus/evidence/   # 24 MB
cp -a $L/corpus/knowledge/tb2-*-grader.md $S/lane-base/corpus/knowledge/
cp -a $L/plans/round52_c1_grader_audit.py $S/mut/base.py          # cmp: SAME
cd $S && python3 mut/base.py --lane lane-base > pristine.out      # exit 1
```

Mutants: 16 copies of `mut/base.py` (`M01.py`…`M16.py`), each changed by one `edit` call on the
scratch copy (single-line PUTs; verified with `diff base.py Mxx.py`, all 16 differ only on the intended
line(s), see `receipts/mut/`). M16 touches two lines (227 and 332 in the file after numbering).

Matrix: `TMPDIR=$S/tmp python3 drive.py` → 238 in-process runs (17 variants × 14 scenarios) → `results/`
(`matrix.json`, `stats.json`, one `.txt` per run). Per-test value analysis: `python3 analyze_value.py`.

## Frozen controls, run against the pristine counter (named signature vs observed)

| control (claims §C1) | fixture | expected named leg | observed | reproduces? |
|---|---|---|---|---|
| c1-control-nothing | lane with no `corpus/evidence/round52` | `CAPTURES present=0`, `CONFIRMED new=0` | `CAPTURES expected=184 present=0 mismatched=0`; `CONFIRMED new=0 []` | yes |
| c1-control-name-only | population with 89 names, `[]` file lists | `classified=0` | `TASKS total=89 records=89 classified=0` | yes |
| c1-control-blind-class (as written: force file-level class to V0) | base lane, `classify()`→V0 | `CANDIDATES total=0` → `CONFIRMED new=0` | `CANDIDATES total=27` (not 0); `CONFIRMED new=0` | **no** (D6) |
| c1-control-blind-class (full: also `classify_test()`→P0) | base lane | `CANDIDATES total=0` | `CANDIDATES total=0`; `CONFIRMED new=0` | yes, but only because the per-test layer is also forced |
| c1-control-drop-capture (a: delete one captured file) | base lane minus `bn-fit-modify/tests/test_outputs.py` | `present=183 mismatched=1` | `present=182 mismatched=0` | **no** (D6) |
| c1-control-drop-capture (b: remove its SHA256SUMS line) | base lane, one `SHA256SUMS` line removed | `present=183 mismatched=1` | `present=183 mismatched=1` | yes |

## Mutant table

Killed = the expected killer's named leg (or the measured figure the claim cites) differs from pristine.
"Frozen" means one of the four §C1 controls; "probe" means a fixture I built in scratch (NOT frozen).

| mutant | change (file line) | expected killer | killed? | observed (mutant vs pristine) |
|---|---|---|---|---|
| M01 | `classify_test` L104: P3 suppressed when a presence call exists | selftest `classify_test` case 2; A4 figure P1=33/27 | **yes** (selftest, A4 figure; no frozen control) | `SELFTEST FAIL classify_test(P3) -> P1`; `TESTCLASS presence_only_tests=111 tasks_with_presence_only=62` (base 33/27); `CANDIDATES total=63` (base 29) |
| M02 | `classify_test` L99: "assert" gate removed | none in frozen set (no assert-free presence case in selftest) | **no — survives** | identical output in all 14 scenarios; P1 33/27 unchanged. Gate is untested. |
| M03 | VALUE regex: `\bin\b` removed (the A1-consistent flip) | A1 receipt: `test_model_file_exists` is presence-only | **yes by diff; mutant over-corrects** | `TESTCLASS 59/41` (base 33/27); 26 base-P3 tests become P1 and 18 become P0. Of the 18, 10 are real code-level membership asserts (`assert "x" in out`) that the marker correctly catches, and 8 match only in comments/docstrings. Removing the marker is the wrong fix (see D1). |
| M04 | VALUE regex: `[<>]` removed | A4 figure 33/27 | **yes** (diff) | `TESTCLASS 37/31`, `CANDIDATES 33`. Not in selftest. |
| M05 | `classify_test` L102: P2 only if no VALUE | selftest case 3 (P2) | **no — survives** | identical in all scenarios; no population test carries both P2 and P3 markers. Ordering untested. |
| M06 | BEHAV_T: `dist\.` removed | none | **no — survives (equivalent on population)** | identical output; no test body calls `dist.` directly. |
| M07 | `classify_test` L101: presence not stripped before marker check | none | **no — survives (equivalent on population)** | identical output; presence calls contain no VALUE or BEHAV token. Equivalent mutant. |
| M08 | `TESTDEF` without `re.M` | A4 figure 33/27 | **yes** | `test_functions_split=0` (stats.json); `TESTCLASS 0/0`; `CANDIDATES total=2`. Selftest does not exercise split, so selftest passes. |
| M09 | `TESTDEF` matches any `def` (`\w+`) | A4 figure 33/27; A1 "308 test functions" | **yes** | `test_functions_split=407` (base 305); `TESTCLASS 34/28`; `CANDIDATES total=30`. Helper functions become "tests". |
| M10 | candidate = `bool(p1)` (drop file-level V1/V4) | `CANDIDATES` receipt (29 names, incl. the two V1 tasks) | **yes** | `CANDIDATES total=27`; `pytorch-model-recovery` and `torch-tensor-parallelism` drop out. Probe P-quote: `CONFIRMED new=0` (base 1). |
| M11 | candidate = V1/V4 only (drop P1 path) | same | **yes** | `CANDIDATES total=2` (base 29); `CONFIRMED` loses `bn-fit-modify`. |
| M12 | CONFIRMED: quote-verbatim check removed | c1-control-nothing (no control supplies a confirmation) | **frozen: NO — survives all four.** probe P-quote: **yes** | probe P-quote (one good receipt + one fabricated quote): base `CONFIRMED new=1 ['pytorch-model-recovery']`, `REJECTED torch-tensor-parallelism quote-not-in-captured-bytes`; mutant `CONFIRMED new=2 ['pytorch-model-recovery','torch-tensor-parallelism']` |
| M13 | CONFIRMED: candidate-membership check removed | same | **frozen: NO. probe P-member: yes** | probe P-member (real quote, non-candidate `adaptive-rejection-sampler`): base `CONFIRMED new=0`; mutant `CONFIRMED new=1 ['adaptive-rejection-sampler']` |
| M14 | CONFIRMED: new-task (`t in read`) check removed | same | **frozen: NO. probe P-read: yes** | probe P-read (real quote, `password-recovery`, in lane read set): base `CONFIRMED new=0`; mutant `CONFIRMED new=1 ['password-recovery']` |
| M15 | CONFIRMED: `confirmed` flag check removed | same | **frozen: NO. probe P-unconf: yes** | probe P-unconf (`confirmed: false`, `prove-plus-comm`): base `CONFIRMED new=0`; mutant `CONFIRMED new=1 ['prove-plus-comm']` |
| M16 | threshold `>= 2` → `>= 1` (both `verdict` and `ok_without_capture_legs`) | "CONFIRMED new ≥ 2" leg (no control supplies a single confirmation) | **frozen: NO. probe P-thr1: yes, on the A5 line only** | probe P-thr1 (one valid confirmation + synthetic prior-art): base `R52-C1-A5 fail`; mutant `R52-C1-A5 pass`. Literal `R52-C1` stays `fail` in both because `present=183`, so the literal verdict cannot show this kill. |

Summary: named-leg kills by a **frozen** control: **0 / 16**. Kills by the selftest or a claim-cited
measured figure: M01, M04, M08, M09, M10, M11 (and M03 by diff). Kills only by my probes: M12–M16.
Survivors on every scenario: M02, M05 (untested ordering/gate), M06, M07 (equivalent on this population).

Stats (`results/stats.json`, primary graders present, 88 files, excluded file absent):
base 305 split test functions, 33 P1; M08 0/0; M09 407/34; M01 305/111; M03 305/59; M04 305/37.

## Defects found in the frozen predicate (reported, not fixed)

**D1 — comments and docstrings reach the VALUE marker (`classify_test`).** `VALUE` contains `\bin\b`,
which matches the English word "in" in comments and docstrings. Measured:
- `pytorch-model-recovery` `test_model_file_exists` (L103–108): body is `assert hello_path.exists(), …`,
  but the comment at L105 "…the agent operated **in** (the WORKDIR…)" makes it P3. The printed output
  says `presence_only=-` for this task, which contradicts the A1 receipt (which names this test as
  presence-only).
- `torch-tensor-parallelism` `test_parallel_linear_exists`: the docstring at L21 "…in the expected
  directory" makes it P2/P3-contaminated (see D2); the A1 receipt names it presence-only; the printed
  output says `presence_only=-`.
- `bn-fit-modify` `test_bn_sample_exists` is P1 in the printed output (consistent with A1).
- With docstrings and comments removed before classification (AST view, `analyze_value.py`), the
  presence-only count is **48**, not 33. Transitions base→AST: P3→P1 14, P2→P3 5, P2→P1 1, P3→P0 1.
- Removing `\bin\b` (M03) is not the fix: it also drops 10 real membership asserts
  (`assert "x" in out`) from P3 to P0, while fixing 8 comment-only matches. The correct repair direction is to strip comments and
  docstrings before marker matching. Selftest has no docstring or comment case, so this is unguarded.

**D2 — block boundary contamination (`split_tests`).** `TESTDEF` only matches `def test_`, and a block
runs to the next `def test_` or EOF. Non-test helper defs and top-level code are therefore attributed to
the preceding test. Measured: 10 tests' base blocks contain non-test top-level code, for example
`torch-tensor-parallelism::test_parallel_linear_exists` swallows `_setup_process_group` (which calls
`dist.init_process_group`) and gets P2 from it; `circuit-fibsqrt::test_gates_file_size` swallows
`fibonacci`/`isqrt`; `install-windows-3.11::test_qemu_running_with_correct_params` swallows 8 helper defs.
Some of the 88 P2 tests are therefore misattributed. M09 (any `def`) fixes the boundary but adds helpers
as tests (407 units), so the split needs an end-of-test rule, not a looser regex.

**D3 — candidate rule disagrees with the A1 text.** A1 (claims file, "Changed") says "a task is a
vacuity candidate when ≥1 of its tests is P1". The code says `bool(p1) or cls in ("V1","V4")`. The two
extra candidates, `pytorch-model-recovery` and `torch-tensor-parallelism`, are the two tasks A1 itself
states are **falsely** labelled V1 ("the file-level label … is FALSE of those graders as a whole"). Their
candidacy rests on the label A1 disowned. Under the A1 text literally, candidates = 27 (M10 output).

**D4 — selftest covers almost nothing of the per-test layer.** `--selftest` has 4 `classify_test` cases
and no split, candidate, or CONFIRMED case. It kills only M01. It cannot detect M02, M03, M05, M08,
M09, M10–M16.

**D5 — the CONFIRMED leg, which carries the novelty score, has no frozen control.** None of the four
§C1 controls supplies a confirmation receipt, so the quote-verbatim, candidate-membership, new-task,
`confirmed`-flag, and threshold checks are all unexercised (M12–M16 survive the frozen set). The
Amendment A1 claim that these are "stricter, never weaker" is therefore not checked by any control.
This is the largest gap: a regression in five checks would leave every frozen control passing exactly as before.

**D6 — two frozen control signatures are not reproduced by the pristine counter.**
- `c1-control-blind-class` as written (force every task's file-level class to V0) gives
  `CANDIDATES total=27`, not the stated 0, because after A1 the per-test P1 tests still make tasks
  candidates. Only forcing the per-test class too (`classify_test`→P0) yields 0. The control's named
  signature therefore needs rewording.
- `c1-control-drop-capture`: removing the file yields `present=182 mismatched=0`; only removing its
  SHA256SUMS line yields the stated `present=183 mismatched=1`. The control text does not say which.

**D7 — a number the claims cite is not printed by the counter.** A1 cites "308 test functions";
the counter prints no test total and computes 305 on the 88 present primary graders. The excluded
`sanitize-git-repo` file cannot be counted from the lane (bytes absent, per A5). The figure cannot be
checked from printed output.

## Files produced (absolute paths)

- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2MutC1/report.md`
  (copied to `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2MutC1.md` per the seat item)
- Receipts (copied out of scratch before removal): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2MutC1/receipts/`
  - `drive.py` (driver), `analyze_value.py` (AST-view analysis), `pristine.out` (base output)
  - `mut/base.py`, `mut/M01.py`…`mut/M16.py` (mutants)
  - `results/matrix.json` (238 outputs), `results/stats.json`, `results/<mutant>__<scenario>.txt`
- Scratch fixtures and copies (removed): `/fast/scratch/hyaku/kengaku-r52/w2-W2MutC1/`

## Probes (NOT frozen controls; for the confirmation leg only)

The probe fixtures are synthetic. They use `reader: "W2MutC1-synthetic-fixture-reader"` and prior-art
URLs under `example.invalid` (reserved TLD) so no real URL is invented. They are mechanical probes to
exercise the counter's branches, not evidence, and nothing was written into the lane.

## Non-goals and unchanged state

- Lane tree, `.ufo/state/`, `.ufo/watchdog.log`, sibling lanes, and fleet files were not written.
- No `git`/`jj` mutation was run. No mutation was applied to the lane's counter.
- No tool was installed or upgraded.
