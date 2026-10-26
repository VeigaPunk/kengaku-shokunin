# F37XMutD4 — wave 2 (falsify): four new D4 mutants beyond M44–M47

Target: `plans/battery37/d4.py` (3 fixtures, docstring claims single-defect isolation) and the D4 clause
of `plans/pkg_gate.py:315-326`. Tip `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`; gate digest
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (frozen, verified on my clone).

## Setup and method

```
git clone -q --no-local …/kengaku-shokunin $S/lane && git -C $S/lane checkout -q 357deceb…
git -C $S/lane rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r37/F37XMutD4/lane
python3 …/F37XMutD4/harness.py --lane $S/lane --work $S
```
Harness (`…/falsify/F37XMutD4/harness.py`) imports `plans/round37_c1_verify.py` as a module and uses its
`sha256`, `load_r36`, `Ctx`, `r36_fixtures`, `battery37_fixtures`, `run_gate`; builds all fixtures once,
runs the reference gate, then each mutant gate over the same fixture argv. Kill = the first fixture whose
`(returncode, DEFECT-clause set)` differs from the reference. Output (`…/F37XMutD4/harness-out.txt`):

```
GATE plans/pkg_gate.py sha256=ea6388…edd41 frozen=True
BATTERY fixtures=64
REFERENCE wrong=0
MUTANT X1 killed by=d4-m45-not-one-line -- count off-by-one: a two-line file passes (len > 2 instead of len != 1)
MUTANT X2 killed by=d4-m45-not-one-line -- branch reordered as a conjunction: the label check shadows the count check
MUTANT X3 SURVIVED -- last directional pattern unchecked (patterns[:-1])
MUTANT X4 SURVIVED -- directional pattern regex loosened to case-insensitive
EXTRA-MUTANTS total=4 killed=2 survived=2
```

Each `old` occurs exactly once in the frozen gate (`str.count(old)==1`, checked inside the harness; no
`INVALID` line printed) and each mutant compiles.

## The four new mutants (exact `old -> new`, each unique in the gate)

| id | clause part | old -> new | result |
|---|---|---|---|
| X1 | count threshold, off-by-one | `if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):` -> `if len(lines) > 2 or not lines[0].startswith(spec["d4"]["label"]):` | **killed** by `d4-m45-not-one-line` |
| X2 | branch reordered, label shadows count | same old -> `if not lines[0].startswith(spec["d4"]["label"]) and len(lines) != 1:` | **killed** by `d4-m45-not-one-line` (also by `d4-m46-label-not-carried`) |
| X3 | pattern check applied to a prefix of the list | `enumerate(spec["d4"]["patterns"], 1)` -> `enumerate(spec["d4"]["patterns"][:-1], 1)` | **SURVIVED** |
| X4 | pattern regex loosened | `if not re.search(pat, lines[0])]` -> `if not re.search(pat, lines[0], re.IGNORECASE)]` | **SURVIVED** |

Kill mechanics, direct (`…/F37XMutD4/kill-proof.txt`; `d4-line` on a two-line genuine-first file and on
the relabelled line):

```
PROOF m45-two-lines gate=ref rc=1 note=D4 DEFECT line_count=2 labelled=False
PROOF m45-two-lines gate=X1 rc=0 note=D4 ok patterns=3 failed=0
PROOF m45-two-lines gate=X2 rc=0 note=D4 ok patterns=3 failed=0
PROOF m46-relabelled gate=ref rc=1 note=D4 DEFECT line_count=1 labelled=False
PROOF m46-relabelled gate=X1 rc=1 note=D4 DEFECT line_count=1 labelled=False
PROOF m46-relabelled gate=X2 rc=0 note=D4 ok patterns=3 failed=0
```

X1/X2 are killed for the right reason (the count fixture is accepted); X2 is additionally accepted on the
relabelled line, which is why `d4-m46` would kill it too.

## Survivors are battery limits, not inert mutations

Both survivors change observable behaviour. Witness probe (`…/F37XMutD4/witness.py`, receipt
`witness-out.txt`) builds the X3/X4 gates from the frozen source and runs them on two D4 lines derived
from the genuine line:

```
WITNESS w-pattern3-token-changed gate=ref rc=1 note=D4 DEFECT patterns=3 failed=['pattern3']
WITNESS w-pattern3-token-changed gate=X3 rc=0 note=D4 ok patterns=3 failed=0
WITNESS w-case-altered-pattern1 gate=ref rc=1 note=D4 DEFECT patterns=3 failed=['pattern1']
WITNESS w-case-altered-pattern1 gate=X4 rc=0 note=D4 ok patterns=3 failed=0
```

So a line missing only the third directional token, and a line whose `SELFTEST cases=10 failed=0` is
uppercased, are both rejected by the frozen gate and accepted by the mutant. The battery contains no
fixture of either shape: the only fixture that exercises the directional patterns at all is `r36-L2`
(two `file:line` citations swapped), which breaks patterns 1 and 2 jointly, so dropping pattern 3 is
invisible; and no fixture alters letter case. Frozen attribution on my clone
(`python3 plans/round37_c1_verify.py --lane . --only M44,M45,M46,M47 --work $S`):

```
MUTANT M44 D4 killed by=d4-m44-file-unreadable
MUTANT M45 D4 killed by=d4-m45-not-one-line
MUTANT M46 D4 killed by=d4-m46-label-not-carried
MUTANT M47 D4 killed by=r36-L2
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
```

`d4.py` contributes no fixture to the pattern half of the clause; the whole-loop mutation M47 is caught
only by a round-36 fixture. Smallest safe corrections (reported, not written into the lane): add two
fixtures to `d4.py` — genuine line with `counter draft's selftest was green` -> `… was red`, and genuine
line with `SELFTEST cases=10 failed=0` uppercased — each declaring `defects ["D4"]`, both rejected by the
frozen gate (`failed=['pattern3']` / `failed=['pattern1']` above).

## Do the three `d4.py` fixtures isolate one defect each?

- **M44 `d4-m44-file-unreadable` — yes.** Note is `file unreadable` (only branch (a)); the path
  `d4-correction-absent.txt` is inside the fixture dir and never created, so nothing but readability is
  wrong. The renamed run relocates it because the path is built from `d`.
- **M45 `d4-m45-not-one-line` — yes.** Note `line_count=2 labelled=False`; the first line is
  `ctx.d4_line()`, i.e. label plus all three patterns hold (the reference accepts the same line alone,
  `r36-L1`), so only `len(lines) != 1` rejects. X1 and X2 both accept this fixture, confirming the label
  and pattern halves pass.
- **M46 `d4-m46-label-not-carried` — yes.** Note `line_count=1`; the altered line matches all three
  patterns (`re.search` on `"- **D4 correction note (round 34 C2):**" + genuine[len(label):]` returns
  `[True, True, True]`, and the label is neither a prefix nor a substring of it), so only
  `startswith(label)` rejects. X1 still rejects it (count is fine), X2 accepts it (label check shadowed).

One diagnostic observation, not a calibration defect: the reject message hardcodes `labelled=False`
(`plans/pkg_gate.py:322`), so M45's note reports the label half as failed when it actually held; the
clause's verdict is still correct.

Nothing was written outside `.ufo/waves/round-37/falsify/` (this report plus the receipts under
`F37XMutD4/`); scratch
`/fast/scratch/hyaku/kengaku-r37/F37XMutD4` was removed after copying the three receipts.

VERDICT: extra-mutants-d4-killed-2/4
