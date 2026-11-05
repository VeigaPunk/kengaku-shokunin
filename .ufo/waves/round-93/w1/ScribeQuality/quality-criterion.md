# Draft — one new `corpus/QUALITY.md` criterion (round 93, seat ScribeQuality)

Draft only; the L1 integrates. Style source: the file's last three criteria (Q70, Q71, Q72,
section `## Round91 instrument-fixture lesson`), read in full before drafting.

**Numbering note (L1 must resolve).** The committed `corpus/QUALITY.md` ends at Q72. The lane
working tree already carries an *uncommitted* `## Round93 freeze-integrity lesson` section with
`Q73` and `Q74` (written during this wave, `git status` shows ` M corpus/QUALITY.md`;
`git diff corpus/QUALITY.md` shows only those two added lines). This draft is therefore numbered
**Q73** (the next free number in the committed file). If the L1 keeps the working-tree Q73/Q74
pair, renumber this one to **Q75** and drop the working-tree Q73, whose substance is the same
criterion — do not land two Q73s.

**Placement.** Append a new section at the end of `corpus/QUALITY.md` (the file is append-only by
section; earlier criteria are never rewritten).

---

## Text to append (verbatim)

```markdown
## Round93 freeze-integrity criterion

- **Q73 — a claim verdict reads "met as frozen" only when the claims file carries a `frozen-instruments` sha256 table and the freeze-integrity gate is green on that table at the measured tip; a claim with no table is not frozen at all.** Grounding: `corpus/lessons/round-92.md` Mistake M8 — round 92 attempt 1 filed C2 and C3 as "met as frozen" while three of its instruments had been edited after the freeze commit and after the first scored run (`git log --oneline f0018773..288511d8 -- plans/` lists E..E7), and no gate compared the counter bytes to the freeze, so the lane's own verdict could not see the edits it had made; the verdicts were withdrawn by SCORECARD erratum. Executable half: `plans/round93_freeze_integrity.py --claims plans/round-<N>-claims.md --freeze <the commit that added that claims file> --rev <T>` must print `FREEZE-INTEGRITY instruments=N intact=N broken=0` and `PREDICATE freeze-integrity pass`; an edit later reverted before T still breaks the instrument (`touched-after-freeze=N`), because whatever scored in between may have used the edited bytes. Shown able to fail on the lane's own history: at `--freeze f0018773 --rev 1df76536 --paths plans/round92_c1_replay.py plans/round92_c2_conformance.py plans/round92_burndown.py plans/round91_counter_pin.py` the gate prints `FREEZE-INTEGRITY instruments=4 intact=1 broken=3` and `PREDICATE freeze-integrity fail`, rc 1 — the three mismatches between round-92's filed "met as frozen" and the repository bytes. Source: `corpus/lessons/round-92.md` `## Mistakes` M8; `corpus/lessons/round-93.md` Mistake M2; the gate `plans/round93_freeze_integrity.py` and its counter `plans/round93_c2_counter.py` (leg W1).
```

---

## Why this text satisfies the assignment

- **Makes the two conditions a precondition for "met as frozen".** The first clause states the
  precondition (a `frozen-instruments` sha256 table in the claims file **and** a green
  freeze-integrity gate on that table at the measured tip); the second clause denies the verdict
  outright when the table is absent ("a claim with no table is not frozen at all").
- **Cites lesson round-92 M8** by file, row, and the command that exposed it
  (`git log --oneline f0018773..288511d8 -- plans/`), including the consequence the lesson records
  (verdicts withdrawn by SCORECARD erratum).
- **Cites this round's `plans/round93_freeze_integrity.py`** as the executable half, with the exact
  invocation, the exact required output, and the revert-still-counts clause
  (`touched-after-freeze=N`), which is the part a naive byte comparison would miss.
- **Shows the criterion able to fail** (the house rule from Q58/Q63: a criterion without a red
  witness is prose). The witness is the lane's own round-92 history, measured, not asserted:
  `broken=3`, `intact=1`, rc 1 — the three instruments round 92 had edited after its freeze.

## Evidence for every figure quoted in the criterion

Verified in scratch (`/fast/scratch/hyaku/kengaku-r93/ScribeQuality/lane`, a `git clone --shared`
of the lane checked out detached at `22972a31`); receipts copied to
`.ufo/waves/round-93/w1/ScribeQuality/receipts/`.

| claim in the criterion | how it was measured | receipt |
|---|---|---|
| the round-92 history yields `instruments=4 intact=1 broken=3`, rc 1 | `python3 plans/round93_freeze_integrity.py --lane . --freeze f0018773 --rev 1df76536 --paths plans/round92_c1_replay.py plans/round92_c2_conformance.py plans/round92_burndown.py plans/round91_counter_pin.py --work DIR` | `receipts/gate-r92-history.txt` |
| `broken=0` is what the gate prints at this round's measured tip | same gate, `--claims plans/round-93-claims.md --freeze d8d0a4b8 --rev 22972a31` → `FREEZE-INTEGRITY instruments=9 intact=9 broken=0`, `PREDICATE freeze-integrity pass`, rc 0 | `receipts/gate-at-tip.txt` |
| the C2 counter prices the same gate and prints `W1 pass` / `W4 pass` at the measured tip | `python3 plans/round93_c2_counter.py --lane . --rev 22972a31 --work DIR` → `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`, rc 0 | `receipts/c2-counter-at-tip.txt` |
| the gate really compares counter bytes to the freeze (the M8 gap) | `plans/round93_freeze_integrity.py` docstring and `evaluate()`; its three intactness conditions (freeze bytes, rev bytes, no commit touching the path) | `plans/round93_freeze_integrity.py:29-38,80-124` |
| `plans/round-93-claims.md` carries a `frozen-instruments` table of 9 rows at F `d8d0a4b8` | the file's table block; the gate parsed it and priced 9 instruments | `receipts/gate-at-tip.txt` |

The gate run at the measured tip was executed read-only against a detached clone in scratch; the
lane itself was not mutated.
