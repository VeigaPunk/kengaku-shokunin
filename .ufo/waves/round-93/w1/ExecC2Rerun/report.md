# ExecC2Rerun — R93-C2 independent re-measurement, forgery extension

Seat: ExecC2Rerun (leaf, executor). Lane: kengaku-shokunin. Measured tip T `22972a317185216596b3dfe1c189e98d1eb86787`.
Scratch: `/fast/scratch/hyaku/kengaku-r93/ExecC2Rerun/` (clone `lane` detached at T, `git status` clean; removed before yield).
Lane not mutated: no git mutation, no commit, no fleet-root write. Tools installed: none (python3 3.14.8 already present).

## 1. Real counter at T (item 1) — PASS

Command (from the clone, cwd = clone root): `python3 plans/round93_c2_counter.py --lane "$S/lane" --rev 22972a317185216596b3dfe1c189e98d1eb86787 --work "$S/w"`
Receipt: `receipts/c2-rerun.txt`

```
TOOL plans/round93_freeze_integrity.py@22972a317185
W1 pass rc=1 summary=(4, 1, 3) intact=['plans/round92_c1_replay.py']
W2 pass  (5/5 fixtures as specified)
W3 pass
W4 pass freeze=d8d0a4b849f3 rc=0 summary=(9, 9, 0)
TARGET legs_passed=4 of 4
PREDICATE R93-C2 pass        rc=0
```

Frozen-instrument sha256 table re-verified in the clone: all 9 rows match the F table (`18b01b42…` for the gate, `ac0e26a5…` for the counter, etc.). Note: the counter's own W1 verdict (`broken=3`) is the round-92 calibration count, not a defect.

## 2. Committed forgeries at T (item 2) — with W4 evaluable

Command per forgery: `python3 plans/round93_c2_counter.py --lane "$S/lane" --rev T --work "$S/wf-<f>" --tool-file plans/round93_c2_forgeries/<f>.py`
Receipts: `receipts/forgery-committed-<f>.txt`

| forgery | W1 | W2 (failing fixtures) | W3 | W4 | legs | rc | caught? |
|---|---|---|---|---|---|---|---|
| always_broken | fail (0 intact, 4 broken) | fail: w2-intact RED, w2-unrelated RED | pass (line printed, meaningless) | fail (9/9 `broken:forged`) | 1/4 | 1 | yes (W1, W2, W4) |
| always_intact | fail (4 intact, expect 1) | fail: w2-edited, w2-edit-revert, w2-lying-table RED | pass | pass (9/9 intact, correct on clean tree) | 2/4 | 1 | yes (W1, W2); W4 blind by construction |
| bytes_only | pass | fail: w2-edit-revert RED (rc 0 vs 1) | pass | pass | 3/4 | 1 | yes (W2 only) |
| log_only | pass | fail: w2-lying-table RED (rc 0 vs 1) | pass | pass | 3/4 | 1 | yes (W2 only) |

All four committed forgeries are rejected (rc 1). W4 now distinguishes only always_broken; for the other three it reports the correct verdict on this round's clean table, so W4 is not a forgery detector on this tree. W1 catches the two "always" forgeries but not the two honest-looking ones; W2 catches all four.

## 3. Forgery extension (item 3)

Four new forgeries, each the honest gate (`forgeries/honest-gate-at-T.py`, sha256 `18b01b42…` verified) with exactly one CLI-path behaviour changed (the forged function is active only when called from `main`, so the in-process battery stays honest and W3 is not the variable). Files in `forgeries/`.

| forgery | change | counter result at T | caught by | verdict |
|---|---|---|---|---|
| x-head-not-rev.py | diffs lane `HEAD` instead of `--rev` | PREDICATE **pass**, 4/4, rc 0 | none | **uncaught** — major |
| x-first-row-only.py | checks only `rows[:1]` | W1 fail, W2 pass, W3 pass, W4 fail (`summary=(1,1,0)`), 2/4, rc 1 | W1, W4 | caught (W2 blind: its fixtures have one row) |
| x-diff-rev-minus-1.py | ignores `--freeze`; window is `rev~1..rev` (table still read at `--freeze`) | PREDICATE **pass**, 4/4, rc 0 | none | **uncaught** — major (accepts a breach, fixture B) |
| x-table-at-rev.py | reads the frozen table at `--rev` instead of `--freeze` | PREDICATE **pass**, 4/4, rc 0 | none | **uncaught** — major (accepts a repaired lie, fixture C) |

Receipts: `receipts/forgery-new-<f>.txt`.

### 3a. Each uncaught forgery is shown to differ from the honest gate (isolation fixtures)

Fixtures built in throwaway repos (`git init` in scratch, explicit `-C`, fixture identity, toplevel asserted), run through the honest gate and the forgery directly. Receipts: `receipts/fixtures/`.

- **A — --rev not HEAD.** Commits: freeze (clean), edit (HEAD). `--freeze f0 --rev f0`.
  - honest: `INSTRUMENT c.py … verdict=intact`, `FREEZE-INTEGRITY instruments=1 intact=1 broken=0`, rc 0.
  - x-head-not-rev: `REV a5293b65…` (HEAD), `verdict=broken:rev-bytes-differ+touched-after-freeze=1`, rc 1.
  - Divergence: a gate that reads HEAD rejects an intact revision. At T itself HEAD == T, so this cannot flip the real verdict; it means the counter cannot tell `--rev` from HEAD (every W2 fixture passes `--rev` == HEAD).
- **B — edit, revert, then one unrelated commit.** Commits: freeze, edit, revert, unrelated (HEAD). `--freeze f0 --rev f3`.
  - honest: `verdict=broken:touched-after-freeze=2`, rc 1.
  - x-diff-rev-minus-1: `touched=0 verdict=intact`, rc **0** — **accepts a breach**.
- **C — table lied at freeze, row repaired later.** Commits: freeze (claims row = `000…0`, bytes differ), repair-row (claims row = real sha). `--freeze f0 --rev f1`.
  - honest: `verdict=broken:freeze-bytes-differ-from-table+rev-bytes-differ`, rc 1.
  - x-table-at-rev: `table=96257f257362 … verdict=intact`, rc **0** — **accepts a breach**.

Control: the honest gate on fixture B at `--rev` = edit commit gives broken, and on A at `--rev` = HEAD gives broken. The fixture driver is reproducible from the recipe in section 5; commit hashes differ per run, verdicts do not.

### 3b. Which leg should have caught each uncaught forgery (named as requested)

1. **x-diff-rev-minus-1 — leg W2 should catch.** W2's `w2-edit-revert` fixture ends exactly at the revert commit, so `rev~1` is the edited commit, and the forgery still emits `broken` with the same count `(1,0,1)`. W2 judges only the summary counts and rc, not the reason text, and no W2 fixture has any commit after the revert. Missing fixture: *edit → revert → unrelated commit* (honest rc 1, forgery rc 0).
2. **x-table-at-rev — leg W2 should catch.** No W2 fixture rewrites the claims table after the freeze. `w2-lying-table` keeps the lie at both ends. Missing fixture: *lying table at freeze, row repaired in a later commit* (honest rc 1, forgery rc 0).
3. **x-head-not-rev — leg W2 (and W1 for the tip).** Every W2 fixture has `--rev` == HEAD. A fixture where `--rev` is an earlier commit than HEAD with a verdict that differs (fixture A: honest rc 0, forgery rc 1) would catch it. W1 cannot: at the tip and at T the honest gate returns the same `intact=1 broken=3` (see `receipts/w1-honest-at-tip.txt` and `w1-honest-at-T.txt`), so W1 is blind to HEAD-vs-rev on this history.

## 4. Findings (judged, not repaired — frozen rule)

FINDING F1 major — The counter's W2 accepts `x-diff-rev-minus-1` (4/4 PASS, rc 0 on the real counter command). If this forged gate were the gate under test, `PREDICATE R93-C2 pass` would print. Reproduce: `python3 plans/round93_c2_counter.py --lane "$S/lane" --rev 22972a317185216596b3dfe1c189e98d1eb86787 --work DIR --tool-file .ufo/waves/round-93/w1/ExecC2Rerun/forgeries/x-diff-rev-minus-1.py` → `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`. Fix to route to round 94: W2 must check reasons as well as counts and include the *edit → revert → unrelated commit* fixture.

FINDING F2 major — The counter's W2 accepts `x-table-at-rev` (4/4 PASS, rc 0). Same command with `forgeries/x-table-at-rev.py` → `PREDICATE R93-C2 pass`. Breach class: a freeze-time lying table repaired later. Route to round 94: add the *repaired-after-freeze* fixture to W2.

FINDING F3 major — The counter's W2 and W1 accept `x-head-not-rev` (4/4 PASS, rc 0). Same command with `forgeries/x-head-not-rev.py` → `PREDICATE R93-C2 pass`. It cannot flip the verdict of the real gate at T (HEAD == T in the clone), but it does mean the counter does not check that `--rev` is honoured. Route to round 94: add a fixture where `--rev` is earlier than HEAD with a differing verdict.

FINDING F4 minor — counter lines 156–159 (W3): the comment says the battery line comes from "the W1 run's output", but `out` is reassigned by the W2 loop (line 148), so W3's first check reads the last W2 fixture (`w2-unrelated`). Both checks still must hold, so no verdict flip; the comment is wrong.

FINDING F5 info — `x-first-row-only` is caught by W1 and W4; W2 and W3 are blind to row count (fixtures have one row; W3 is by design meaningless). Confirms W1/W4 are the row-count legs.

FINDING F6 info — W4 on this tree distinguishes only `always_broken`; the other three committed forgeries pass W4 because on a clean tree the honest answer is `intact`. W4 is a consistency check, not a forgery detector.

FINDING F-none (real gate) — the honest gate at T passes all four legs, sha256 of all 9 frozen instruments match the F table, and no forgery was run against the lane.

No frozen instrument was edited. Findings F1–F3 are routed to round 94; they are not repaired in round.

## 5. Fixture recipe (reproduction)

```
H=$(printf "print('counter')\n" | sha256sum | cut -d' ' -f1)
mkc() { git -C "$1" -c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -q --allow-empty -m "$2"; git -C "$1" rev-parse HEAD; }
# A: freeze(c.py=counter) → edit → HEAD        run --freeze f0 --rev f0
# B: freeze → edit → revert → unrelated(other.txt)   run --freeze f0 --rev HEAD
# C: freeze(table=000…0) → repair-row(table=$H)     run --freeze f0 --rev HEAD
python3 -I -B forgeries/honest-gate-at-T.py --lane DIR --freeze F --rev R --claims claims.md --work DIR2
python3 -I -B forgeries/x-*.py          --lane DIR --freeze F --rev R --claims claims.md --work DIR2
```

## 6. Files

- `report.md` (this file); findings also in `../ExecC2Rerun.md`.
- `receipts/c2-rerun.txt` — item 1.
- `receipts/forgery-committed-{always_broken,always_intact,bytes_only,log_only}.txt` — item 2.
- `receipts/forgery-new-{x-head-not-rev,x-first-row-only,x-diff-rev-minus-1,x-table-at-rev}.txt` — item 3 through the counter.
- `receipts/w1-honest-at-tip.txt`, `receipts/w1-honest-at-T.txt` — honest gate W1 args at R92 tip vs T.
- `receipts/fixtures/*.txt` — isolation fixtures A/B/C (honest vs forgery).
- `forgeries/honest-gate-at-T.py` (sha256 `18b01b42fb54ce658dbb98ff3afd12d06600960fae46700fec9218e73bcefcb6`, equals the frozen row) and `forgeries/x-*.py`.

Not done (outside this item): mutation test, historical census, source verification — not in ExecC2Rerun's assignment; left to the other seats.
