# ExecC2Rerun — R94-C2 independent re-measurement and CLI-path forgery extension

Seat: ExecC2Rerun (leaf, no subagents, no task, no commit/push, no mutating git in the lane).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`.
Scratch: `/fast/scratch/hyaku/kengaku-r94/ExecC2Rerun/` (`lane` = `git clone --shared`, detached at T; removed before yield).
Tools installed or updated: none.

## Verdict

- **Step 1 (re-measure at T): PASS as frozen.** `PREDICATE R94-C2 pass`, `TARGET legs_passed=5 of 5`, rc 0. The gate under test is `plans/round94_freeze_integrity.py` at T, sha256 `8574b4d5dca7f381…` (matches the F table row).
- **Step 2 (five known false gates through `--tool-file`): all five still fail with their designated W2 fixture RED.**
- **Step 3 (forgeries on gate v2, CLI path only): 7 of 10 pass 5/5 at T.** The counter does not discriminate these forgeries. Five of the seven are false-green (verdict flips: a breached instrument reports intact, or an edited instrument is silently dropped). Two are rc-only.
- **None of this flips the verdict at T.** The gate at T is the honest one; the forgeries are not in the tree. What is flipped is the claim that the counter is a general discriminator. The frozen predicate passes a forged gate, so `PREDICATE R94-C2 pass` certifies only the 5 known false gates and the 7 CLI mutants, not the class.

Findings are routed to round 95 per the frozen rule. No instrument was repaired in round.

## Commands (exact)

All counter runs: `cd "$S/lane" && python3 plans/round94_c2_counter.py --lane "$S/lane" --rev 90c7677f0ba95d0930d93bda6a14aa50605ebe2e --work <dir> [--tool-file <file>]`.

Step 1: `--work "$S/w"`, receipt `receipts/c2-rerun.txt` (43.6 s).
Step 2: `--work "$S/w-known-<name>" --tool-file <file>`, receipts `receipts/known-false-<name>.txt`.
Step 3: `--work "$S/w-<forgery>" --tool-file forgeries/<forgery>.py`, receipts `receipts/forgery-<forgery>.txt`.

## Step 1 — counter at T (`receipts/c2-rerun.txt`)

```
TOOL plans/round94_freeze_integrity.py@90c7677f0ba9 sha256=8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de
W1 pass    (W1a r92 summary=(4,1,3) intact=[round92_c1_replay.py]; W1b r93 summary=(9,9,0))
W2 pass    fixtures=12 ok=12
W3 pass    SELFTEST cases=15 ok=15 (echoed twice)
W4 pass    freeze=844c504e5147 rc=0 summary=(11,11,0)
W5 pass    null ok fixtures_ok=12 of 12; K1..K7 killed at designated fixtures; mutants=7 killed=7
TARGET legs_passed=5 of 5
PREDICATE R94-C2 pass
rc=0
```

## Step 2 — five known false gates (`receipts/known-false-*.txt`)

Designated fixture is the one each gate was built to fail (from `controls/README.md` and the round-93 receipts).

| gate file (round-93 path) | designated W2 fixture | observed | counter |
|---|---|---|---|
| `MutTesterGate/mutants/m06-cne-exit0-pass.py` | `w2-not-ancestor` | `RED rc=0 want_rc=2` | `TARGET 2 of 5`, `PREDICATE R94-C2 fail`, rc 1 |
| `MutTesterGate/mutants/m13-table-read-at-rev.py` | `w2-lie-repaired` | `RED rc=0 want_rc=1` | `TARGET 2 of 5`, fail, rc 1 |
| `ExecC2Rerun/forgeries/x-diff-rev-minus-1.py` | `w2-edit-revert-unrelated` | `RED rc=0 want_rc=1` | `TARGET 2 of 5`, fail, rc 1 |
| `ExecC2Rerun/forgeries/x-head-not-rev.py` | `w2-rev-below-head` | `RED rc=1 want_rc=0` | `TARGET 2 of 5`, fail, rc 1 |
| `ExecC2Rerun/forgeries/x-table-at-rev.py` | `w2-lie-repaired` | `RED rc=0 want_rc=1` | `TARGET 2 of 5`, fail, rc 1 |

All five: `W2 fail` (fixtures ok 7 or 8 of 12), `W3 fail` (`cases=10`), `W4 pass` (the lane's own table), `W5 fail` (anchors absent in these older gates). Result: 5 of 5 still caught at their designated fixture.

## Step 3 — forgeries on gate v2 (`forgeries/`, `receipts/forgery-*.txt`, `receipts/fixture-demos*.txt`)

Base: `forgeries/base-v2-at-T.py` (byte copy of the T gate). Each forgery is a copy with one CLI-path change; `battery()` is unchanged. Diffs are in `receipts/forgery-diffs.txt`. All seven compile (`receipts/forgery-parse.txt`).

Forgery attack, in terms of the CLI verdict path:

| id | change to the CLI verdict path | counter legs | result |
|---|---|---|---|
| F1 `paths-dup-accepted` | delete `duplicate --paths` CNE in paths mode | W1–W5 all pass | **5/5 PASS** |
| F2 `paths-absent-dropped` | in paths mode, an absent-at-freeze path is `continue`d, not CNE | W1–W5 all pass | **5/5 PASS** |
| F3 `octopus-default-history` | `--full-history` dropped when the range has an octopus merge | W1–W4 pass; W5 fail `K5 anchor-missing` | uncaught behaviorally; red only by anchor removal |
| F3b `octopus-anchor-kept` | same, with the `"rev-list", "--full-history", ` anchor kept in the non-octopus branch | W1–W5 all pass | **5/5 PASS** |
| F4 `touched-M-only` | touched counted with `git log --diff-filter=M` | W1–W4 pass; W5 fail `K5 anchor-missing` | uncaught behaviorally; red only by anchor removal |
| F4b `touched-M-only-anchor-kept` | touched = rev-list commits ∩ `--diff-filter=M` commits, anchor kept live | W1–W5 all pass | **5/5 PASS** |
| F5 `rename-intact` | path absent at rev, but `git diff -M` shows an R with the same path; treated as intact and touched zeroed | W1–W5 all pass | **5/5 PASS** |
| F6 `paths-cne-rc1` | main's CNE branch returns 1 in paths mode | W1–W4 pass; W5 fail `K4 anchor-missing` | uncaught behaviorally; red only by anchor removal |
| F6b `entry-rc-remap` | `__main__` maps rc 2 → 1 when `--paths` is in argv; `main` untouched | W1–W5 all pass | **5/5 PASS** |
| F7 `spaced-row-dropped` | claims rows with more than two whitespace tokens are removed before parse | W1–W5 all pass | **5/5 PASS** |

Exact counter lines for the 5/5 passes (every file is in `receipts/forgery-<id>.txt`, rc 0):

```
F1  TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0   (W2 pass fixtures=12 ok=12; W5 pass mutants=7 killed=7)
F2  TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
F3b TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
F4b TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
F5  TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
F6b TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
F7  TARGET legs_passed=5 of 5 / PREDICATE R94-C2 pass / rc=0
```

The three anchor-removed forgeries (F3, F4, F6) were red only at W5 (`K5-no-full-history RED anchor-missing`, `K4-cne-exit0-pass RED anchor-missing`, rc 1). I did not count those as catches. The anchor-kept variants (F3b, F4b, F6b) are the honest measure, and they pass 5/5. My prediction was that all seven would pass; the three red results were an artifact of my own edits, and I have said so here.

### Verdict flips (fixture demos; honest gate = T gate on the same bytes)

Fixtures are in scratch, outputs in `receipts/fixture-demos*.txt`.

- **F1 duplicate paths.** `--paths c.py c.py`, freeze = rev = one commit.
  Honest: `DEFECT SETUP duplicate --paths` / `PREDICATE freeze-integrity could-not-evaluate`, rc 2.
  Forged: `instruments=2 intact=2`, `PREDICATE freeze-integrity pass`, rc 0. (rc-only: not a false intact.)
- **F2 absent path.** `--paths c.py later.py`, where `later.py` was created and edited after freeze.
  Honest: `DEFECT SETUP path later.py absent at freeze …`, rc 2.
  Forged: `instruments=1 intact=1`, rc 0. **false intact**: `later.py` is silently unchecked.
- **F3b octopus.** Freeze has `c.py`; `side1` edits `c.py`; `side2` is unrelated; `merge -s ours side1 side2` makes a 3-parent commit where `c.py` equals the freeze bytes. (`git rev-list --full-history` lists the side edit; default `rev-list -- c.py` lists nothing.)
  Honest: `INSTRUMENT c.py … touched=2 verdict=broken:touched-after-freeze=2`, `PREDICATE freeze-integrity fail`, rc 1.
  Forged: `touched=0 verdict=intact`, `PREDICATE freeze-integrity pass`, rc 0. **false intact.**
- **F4b delete then re-add identical.** Honest: `touched=2 verdict=broken:touched-after-freeze=2`, rc 1. Forged: `touched=0 verdict=intact`, rc 0. **false intact.**
- **F5 rename, identical bytes.** `git mv c.py renamed.py` after freeze.
  Honest: `rev=absent touched=1 verdict=broken:absent-at-rev+touched-after-freeze=1`, rc 1.
  Forged: `rev=96257f257362 touched=0 verdict=intact`, rc 0. **false intact**: the table names `c.py`, which does not exist at rev.
- **F6 paths-mode CNE.** `--paths nope.py`. Honest: rc 2 `could-not-evaluate`. Forged (F6b): same text, rc 1. (rc-only: false red, fail-closed.)
- **F7 spaced row.** Claims table has `c.py` (intact) and `my file.py` (edited after freeze).
  Honest: `DEFECT SETUP malformed table row …` / `could-not-evaluate`, rc 2.
  Forged: `instruments=1 intact=1`, rc 0. **false pass**: the edited instrument is silently dropped.

## Why the counter misses these (root causes, for round 95)

1. **W2 covers claims mode only, plus one 2-parent treesame merge.** There is no fixture for paths-mode (duplicate, absent-at-freeze), octopus merges, renames, delete/re-add, or spaced rows through the CLI. Paths-mode is only exercised by W1a, where every path exists at freeze and no duplicates occur.
2. **The history windows W1 and W4 contain none of those shapes.** Census (`receipts/census.txt`): octopus 0, merges 0, renames (R) 0, deletes (D) 0 in W1a (r92), W1b (r93) and W4 (round 94). W1 and W4 cannot discriminate a rename, delete/re-add, or octopus bug, so they pass every forgery above.
3. **W5 is string-anchored.** A mutant is "killed" only if the exact source substring is present once and the mutation hits a designated fixture. A forger who keeps the anchor text in live code (F3b, F4b, F6b) passes W5 in full. The three forgeries that dropped the anchor are red for that reason only.
4. **W3 only echoes the forged tool's own SELFTEST line.** The counter checks `^SELFTEST .*$` equals `SELFTEST cases=15 ok=15` (lines 278–282). It does not verify that the battery ran. *[code-read, not executed]*: a forged tool that prints that line unconditionally passes W3.

## Claim status (R94-C2)

- Frozen predicate at T: `PREDICATE R94-C2 pass`, 5/5. Met as written.
- Known false gates passing the counter: 5 → 0 at their designated fixtures. Step 2 re-confirms this at T: all five still fail, each with its designated W2 fixture RED.
- The calibration content ("kills the same 7 attacks re-made as CLI-path mutants of v2") is met for those 7. It is not general. Seven CLI-path forgeries of v2 that the counter does not catch are in this report (F1, F2, F3b, F4b, F5, F6b, F7); five of them flip a verdict to false-green.

## Routing (round 95; not repaired in round)

- Add W2 fixtures for: paths-mode duplicate, paths-mode absent-at-freeze, octopus merge with a discarded side edit, rename with identical bytes, delete then re-add identical, spaced claims row.
- Make W5 behavioural (run the mutant against the fixtures and compare outcomes) instead of string-anchored, so anchor-preserving forgeries cannot pass.
- Make W3 verify the battery ran, not echo a line.
- Extend the history census in W1 or add a fixture window with a rename, octopus and delete/re-add, so W1 is not blind to those shapes.

## Sibling overlap

Round-94 `w1` contains `MutTesterGate` (receipts still empty when I checked), `ExecFreezeCensus`, and `ExecC1Rerun`. The roster also lists `CriticC2-9`, which is working on C2. I did not coordinate with them. My forgeries F3b, F4b, F6b and F7 may overlap with MutTesterGate's mutant series. The L1 should deduplicate before scoring.

## Files

- `report.md` (this file) and copy at `.ufo/waves/round-94/w1/ExecC2Rerun.md`.
- `receipts/c2-rerun.txt` (step 1), `receipts/known-false-*.txt` (step 2), `receipts/forgery-*.txt` (step 3 counter output), `receipts/forgery-parse.txt`, `receipts/forgery-diffs.txt`, `receipts/fixture-demos.txt`, `receipts/fixture-demos-claims.txt`, `receipts/fixture-demos-anchor-kept.txt`, `receipts/census.txt`.
- `receipts/fixture-demos.txt` contains d3–d5 rows that are a fixture construction error (claims table committed after freeze, so "claims absent at freeze"). They are superseded by `fixture-demos-claims.txt` and kept for transparency.
- `forgeries/base-v2-at-T.py` and `forgeries/F1-F7`, `F3b`, `F4b`, `F6b` (10 files; copies of the gate with the CLI change).
