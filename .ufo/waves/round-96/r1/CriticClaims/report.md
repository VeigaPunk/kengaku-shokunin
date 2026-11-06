# CriticClaimsR — round 96 residual r1: adversarial critique of R96-C1 and R96-C2

Seat: CriticClaimsR (leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(master). BASE `45740a616028015b5dfcf9900753e3bb5e6fe689`; measured tip T
`09717e49ff46fad5b255619d671aaaae52dfc180`. Scratch: `/fast/scratch/hyaku/kengaku-r96/CriticClaims`
(removed before yield; receipts copied here). All commands ran from the lane root of a
`git clone --shared` at T; fixture commits used `-c user.name=fixture -c user.email=fixture@invalid`
and each fixture's `git rev-parse --show-toplevel` was asserted equal to its own root before the
first commit. No lane mutation, no subagent, no `task`.

## Verdicts

| claim | verdict | one line |
|---|---|---|
| **R96-C1 coverage** | **verifies-narrowed** | The 14th replay is real (new member; `file-artifact` 30→31, `serialization-schema` 6→7; 17 cases × 4 legs, 0 mismatches), the do-nothing fails, and C1 is separable from the C2 candidate bytes; the finding set is incomplete — three further wrong-pass states pass `P,P,P,1`. |
| **R96-C2 calibration** | **fails** | The official frozen predicate at T prints `GROWS checked=6 tolerant=5` → `PREDICATE R96-C2 fail`, so the claim is not met and the kill rule makes that verdict final; but the predicate is **nondeterministic** (my independent run at the same rev prints `GROWS 6/6`, `PREDICATE R96-C2 pass`, rc 0), and the repair also creates a new historical mismatch (r87's counter now fails at r87's own measured tip) while the "six self-assessment mismatches" count is 1 genuine + 5 growth-drift maintenance items. |

## R96-C1 — what I measured

### 1. The replay and its target are real at T

`python3 plans/round96_c1_replay.py --lane . --rev 09717e49… --work … --env-venv E --grader-venv G`
(fresh venvs staged this seat: E `3.11.17 2.2.3 17.0.0 2.4.6`, G `3.13.16 2.3.3 22.0.0 2.5.4`):

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=40 member=multi-source-data-merger cells=file-artifact:31,serialization-schema:7 set_contains_base=1 located=1 executed=1 cases=17 legs=68 mismatches=0 defects=0
PREDICATE R96-C1 pass
rc=0
```

Receipt: `c1-t-mine.txt`. The BASE ledger measured through the same counter is
`executed_rows=39`, `file-artifact:30`, `serialization-schema:6` (`c1-noc1.txt`), so the two class
cells moved exactly as claimed and the member is new (it is `unexecuted` at BASE). The 14th ordinal
is consistent with the lane's own count: rounds 83–95 are replays 1–13; round 96 is 14.

### 2. The do-nothing does not reach the target

- The committed control `controls/c1-do-nothing.txt` (lane at P1b `e8a80c0e`, no receipt, no ledger
  flip) prints all nine legs `fail`, `defects=9`, `PREDICATE R96-C1 fail`, rc 1.
- I ran the stronger do-nothing: a fixture at T with **only** the C1 ledger flip reverted
  (`git checkout BASE -- plans/grader-population-ledger.json`, one fixture commit). It fails exactly
  on the flip: `LEGS L1=pass … L6=pass L7=fail L8=pass L9=pass`,
  `TARGET executed_rows=39 … executed=0 … defects=1`,
  `DEFECT L7 ledger member=unexecuted round=None …`, `PREDICATE R96-C1 fail`, rc 1
  (`c1-noc1.txt`). The target is not reachable without the C1 work.

### 3. C1 is separable from the C2 candidate bytes landed in C `09717e49`

A fixture at T with the seven candidate counters reverted to BASE
(`plans/round87_c1_replay.py`, `round90..95_c1_replay.py`) and the C1 artifacts left intact prints
9/9 legs, the exact frozen TARGET, `PREDICATE R96-C1 pass`, rc 0 (`c1-noc2.txt`). The C1 counter
never reads those seven files; the empirical run confirms the claims' separability sentence.
**C1 lands no repaired counter bytes and does not depend on them.**

### 4. The finding set is correct as far as it goes — but incomplete

C04 (under-report passes), C06 (rows 102/103 never content-checked) and C07 (float64 `user_id`
passes) are correct: the probe's own cases reproduce them, and I re-derived the mechanism from
`tests/test_outputs.py` (the only value check of the conflict report is the `if email_conflicts:`
guard on user 101's email conflict; `set(df["user_id"]) == {101,…,104}` accepts floats; only rows
101/104 are content-checked).

I then built three states the frozen 17-case table does not contain, using the probe's own
`Box`/`stage`/`run_case` machinery (no reimplementation), and ran the captured grader unmodified.
All three pass all three test functions and the reward bit:

| new state | what is wrong | observed |
|---|---|---|
| `over-report` | a fabricated conflict for user 102, who appears in only one source (the instruction: a conflict counts only when a user appears in multiple sources with different values); `total_conflicts` bumped to 4 | `P,P,P,1` |
| `name-selected-c` | the name conflict's `selected` set to source_c's `"John D."` — the wrong priority winner (source_a must win), contradicting the merged row | `P,P,P,1` |
| `partial-values` | the email conflict's `values` loses `source_c` (`john@c.com`), though the instruction's format says include each source "if exists" | `P,P,P,1` |

Receipt: `newstate2.txt`. The grader's conflict-report surface is therefore checked at exactly one
point — user 101, field email, `values["source_a"]` and `selected` — plus the self-consistency of
`total_conflicts`/`len`. C04 is one instance of that weakness, not the whole finding set. The claim's
sentence "Decisive grading-gap cases: C04 …, C06 …, C07 …" is true but not exhaustive; a closure
reader should not read it as the complete set. This narrows the claim's coverage value, not its
predicate.

### 5. Narrowings that do not flip C1 at T

- The image (`alexgshaw/multi-source-data-merger:20251031`) and uvx-in-container were not executed;
  the replay models them with pinned venvs. ReviewerC1's real-pytest run (17/17 reward agreement,
  exact `test.sh` stack on C01/C12) closes the behavioral gap; the remaining exposure is the
  unexercised `/etc`/image-interpreter difference.
- L6's stamp equality compares the full `ENV_SIDE`/`GRADER_SIDE` lines, which embed unpinned numpy
  and the CPython micro; a future numpy/micro release would fail L6 with no behavioral change
  (ReviewerC1 F1). My fresh venvs resolved to the receipt's exact stamps today, so L6 passes at T.
- The TARGET `executed_rows`/`cells` are printed, not asserted; the kill rule keys on the legs and
  the PREDICATE line, so later ledger growth cannot retro-flip C1 (ReviewerC1 F4).

## R96-C2 — what I measured

### 1. The official frozen predicate fails at T — and the predicate is nondeterministic

The official receipt `.ufo/waves/round-96/L1/c2-tip.txt` at T:

```
STANDING total=14 green=14 red=0
BITES checked=12 bitten=12
GROWS checked=6 tolerant=5
PREDICATE R96-C2 fail
rc=1
```

My independent battery run at the same rev T **passes**:

```
STANDING total=14 green=14 red=0
BITES checked=12 bitten=12
GROWS checked=6 tolerant=6
PREDICATE R96-C2 pass
rc=0
```

(`battery-t.txt`; 616 s, run concurrently with ReviewerC2's own battery, so the host was loaded.)
The same frozen bytes, the same rev, the same command: the official L1 run prints
`GROWS checked=6 tolerant=5` → fail, my run prints `GROWS checked=6 tolerant=6` → pass. The
predicate is **nondeterministic**. The L1's diagnostic (`L1/diag-r91-grow/`) shows r91's grow
fixture passing alone and 6× parallel; my full-battery run passes 6/6. The official failure is a
flake, not a stable property of the repair.

The frozen kill rule is still decisive as written: the official predicate at T is not `pass`, so
R96-C2 is **not met** and that verdict is final under the rule (no in-round repair). But the honest
statement is stronger and worse for the instrument: the claim's failure is **not reproducible**, and
the frozen predicate cannot support a stable verdict. The battery's `bite()` also keeps no per-run
output, so the official r91 grow failure cannot be diagnosed from the receipt (the L1 diagnostic is
a separate reconstruction). This is a blocker-level instrument defect, routed to round 97: preserve
per-run output, eliminate the race, and re-freeze a deterministic predicate before the claim is
judged again.

### 2. The repair creates a new historical mismatch: r87 at its own measured tip

The SCORECARD's R87-C1 row records, at `10de494d14abf0b77979225f51b3b72e73c0d2ed`,
`TARGET executed_rows=31 member=mteb-retrieve … defects=0`, `PREDICATE R87-C1 pass`, exit 0, with
the counting command `python3 plans/round87_c1_replay.py --lane . --rev REV --work DIR`.

After round 96:

- the **pre-round-96** counter bytes, run at `10de494d`: `TARGET executed_rows=31 … executed=1 …
  defects=0`, `PREDICATE R87-C1 pass`, rc 0 (`r87-old-at-r87T.txt`);
- the **round-96 repaired** counter bytes, run at the same `10de494d`:
  `DEFECT L7-ledger row {… "subject": "tb2-result-file" …}`,
  `TARGET executed_rows=31 … executed=0 … defects=1`, `PREDICATE R87-C1 fail`, rc 1
  (`r87-at-r87T.txt`).

The ledger at `10de494d` is historical and unchanged; the counter's expectation changed from
`tb2-result-file` to `tb2-header`. The repair is a re-pin to the *current* ledger, not a
growth-tolerant key: it makes the counter green at T and red at the round's own tip. The SCORECARD
entry no longer matches observed repo state under its own counting command — the exact calibration
defect the claim says it repairs. The claims file does not disclose this cost, and the frozen
predicate (which checks only T) cannot see it.

### 3. The "six self-assessment mismatches" count is 1 genuine + 5 maintenance items

The SCORECARD rows for R90-C1…R95-C1 name their own measured revs and their counting command is
`--rev REV`; the verdicts are historical measurements, not standing claims. At those revs the
counters pass today (I verified r90, r91 and r92 at their own tips: `PREDICATE R90-C1 pass`,
`R91-C1 pass`, `R92-C1 pass`, rc 0; `hist-r90.txt`, `hist-r91.txt`, `hist-r92.txt`). The red at
BASE is growth drift: the L7 pins an absolute executed total, and the ledger grew after the round
closed. That is a maintenance defect (a brittle pin), not a false self-assessment at filing.

The one genuine standing mismatch is r79: the SCORECARD calls it "the standing population gate"
(SCORECARD:3956), and at BASE it is red on `mteb-retrieve`
(`DEFECT SUBJECT-MISMATCH mteb-retrieve ledger=tb2-result-file receipt=tb2-header`,
`DEFECTS n=1`, rc 1; `base-r79.txt`). Round 96 fixes that one at T by re-pinning the ledger and the
r87 counter. The other five are maintenance dressed as calibration. Under prompt §9 ("a calibration
claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo
state"), the five are not mismatches at the revs the rows name.

Quantitatively, with the repaired bytes at round-96 BASE the red set is **2**, not 0:
r79 (subject mismatch) and r87 (the new historical re-pin), while r90 and r91 are green
(`base-r79.txt`, `base-r87.txt`, `base-r90.txt`, `base-r91.txt`). At T the standing set is 14/14
green, but one of the 14 is green only because the ledger at T matches the new pin.

### 4. The candidate-bytes table omits the r87 ledger subject re-pin

The claims file pre-commits "C lands exactly these seven files" (the `candidate-bytes` table) and
says the diff is `candidate-edits.diff`. That diff contains only the seven counters; the ledger
change (`"subject": "tb2-result-file"` → `"tb2-header"`) is a C2 repair byte outside the table
(`git-scope.txt`; `candidate-edits.diff` has no ledger hunk). The ledger file is also C1's flip, but
the subject cell is C2's work. The kill rule "if C lands bytes other than the candidate-bytes table"
is therefore triggered as written, independently of the predicate fail. The P2 `full` control did
exercise the ledger re-pin, so it was controlled — but it was not tabled byte-exactly as claimed.

### 5. Editing frozen instruments of closed rounds: a harm to calibration, not to coverage

The freeze-integrity gate at T, run the way rounds 93–95 ran it:

```
r93: FREEZE-INTEGRITY instruments=9  intact=8  broken=1  PREDICATE freeze-integrity fail
r94: FREEZE-INTEGRITY instruments=11 intact=10 broken=1  PREDICATE freeze-integrity fail
r95: FREEZE-INTEGRITY instruments=11 intact=10 broken=1  PREDICATE freeze-integrity fail
```

The broken instrument in each is that round's own `plans/roundNN_c1_replay.py`
(`rev-bytes-differ+touched-after-freeze=1`; `freeze-r93.txt`, `freeze-r94.txt`, `freeze-r95.txt`).
Rounds 87 and 90–92 have no `frozen-instruments` table, so the gate returns
`could-not-evaluate` for them — it cannot judge them, it does not call them intact.

The closed rounds' rules say "a frozen element that looks wrong is reported, not repaired" and
"editing … after commit A/B voids the claim". Round 96 reclassifies the seven files as "the claimed
work, not instruments", but the closed rounds' frozen tables still list them and the gate does not
honor the reclassification. That is a duplicate authority / identity change: the same path is a
frozen instrument in round N's table and "not an instrument" in round 96's claim. The disclosed cost
is real: at T there is no standing gate that reads the repaired counters as intact (3× fail + 4×
could-not-evaluate). This is a harm to the **calibration** axis (the axis that owns the
freeze-integrity gate and the SCORECARD's self-assessment), not to coverage.

### 6. History rewriting: no file rewrite, but a provenance break

`git diff --name-status BASE..T` shows no edits to any round-87/90–95 receipt or claims file; the
old receipts and old claims files are untouched, and git history is append-only (`git-scope.txt`).
The break is at the instrument path: the current bytes at `plans/roundNN_c1_replay.py` are not the
bytes that produced the recorded verdict, so the old SCORECARD counting command no longer reproduces
at the old rev (r87 proven above). That is an identity change, not a history rewrite.

### 7. Would re-pinning the absolute totals to 40 have met the predicate? No.

The P2 control `controls/c2-repin-abs.txt` (fixture `d478b48e`, the candidate bytes plus
`exec_total == 40` in each L7) prints `STANDING total=14 green=14 red=0`,
`BITES checked=12 bitten=12`, `GROWS checked=6 tolerant=0`, `PREDICATE R96-C2 fail`, rc 0 (the
receipt's trailing rc is the known `echo "$(cat …) rc=$?"` defect; the PREDICATE line is the
verdict). Mechanically the GROWS leg promotes an unexecuted member, so the executed total becomes
41; an absolute 40 fails every grow. The control is the strongest form of the absolute re-pin and it
fails. The answer is no.

## Closure judge rulings

**(a) Is R96-C2 not met, and is that verdict final under the frozen kill rule regardless of the r91
grow diagnostic?** Yes, not met on the official receipt, and final under the rule as written. The
official frozen predicate at T is `PREDICATE R96-C2 fail` (`GROWS checked=6 tolerant=5`, rc 1). The
claims file's kill rule is: "Not met if the predicate is not `pass` at T, if C lands bytes other than
the candidate-bytes table, or if a frozen file changes after F." The official predicate is not pass;
the r91 grow diagnostic is not a predicate change and cannot restore the claim. **But the verdict is
not stable:** my independent run of the same frozen bytes at the same rev T prints
`GROWS checked=6 tolerant=6`, `PREDICATE R96-C2 pass`, rc 0 (`battery-t.txt`). The predicate is
nondeterministic; the official fail is a flake. The kill rule still makes the official receipt
decisive (the claim is not admitted), and the honest finding is the instrument defect: the battery
keeps no per-run output for a failed bite, so the official failure cannot be diagnosed, and a
re-run passes. Route to round 97: preserve per-run output, eliminate the race, re-freeze a
deterministic predicate.

**(b) Does ExecHarm's freeze-integrity finding constitute a harm, and does it affect R96-C1's
admission?** It is a harm to the **calibration** axis: the lane's own freeze-integrity gate at T
reports r93/r94/r95 freezes broken on exactly the instruments round 96 repaired, while those rounds'
claims say "no tabled file changed after F"; the round-96 reclassification is a second authority
that the gate does not recognize. It is not a harm to coverage, and it does not affect R96-C1's
admission: C1 is separable from the candidate bytes (fixture at T with the seven counters reverted
passes 9/9 with the exact TARGET, `c1-noc2.txt`; the do-nothing without the ledger flip fails L7,
`c1-noc1.txt`), and C1 lands no repaired counter bytes. C1 can be admitted independently; the round
as a whole is not admitted because C2 fails and the calibration axis is harmed.

## Findings

```
FINDING R96-C1-F1 major   finding set incomplete: a fabricated conflict for a single-source user (over-report), a wrong priority winner on the name conflict (name-selected-c), and an email conflict missing source_c (partial-values) all pass P,P,P,1; the grader's conflict-report surface has one value point (101/email/source_a+selected) plus total/len self-consistency
FINDING R96-C1-F2 minor   L6 stamp equality compares the full ENV_SIDE/GRADER_SIDE lines (unpinned numpy + CPython micro), so a future resolution change fails L6 with no behavioral change; fresh venvs match today, no flip at T
FINDING R96-C1-F3 info    C1 verifies with the disclosed image/uvx modeling narrowing (prebuilt image and uvx-in-container not executed; real-pytest 17/17 reward agreement closes the behavioral gap)
FINDING R96-C2-F1 blocker frozen predicate is nondeterministic: the official L1 run at T fails (GROWS checked=6 tolerant=5, PREDICATE R96-C2 fail rc 1), an independent run at the same rev passes (GROWS 6/6, PREDICATE R96-C2 pass rc 0); the claim is not met on the official receipt and that verdict is final under the kill rule, but the instrument cannot support a stable verdict
FINDING R96-C2-F2 major   the repair creates a new calibration mismatch: the repaired r87 counter fails at r87's own measured tip 10de494d (L7 subject tb2-result-file vs expected tb2-header, rc 1) while the pre-round-96 counter passes there (rc 0); the SCORECARD R87-C1 row no longer reproduces under its own counting command
FINDING R96-C2-F3 major   the candidate-bytes table omits the r87 ledger subject re-pin; C lands a C2 repair byte (plans/grader-population-ledger.json subject cell) outside the pre-committed seven-file table, so the "C lands exactly these seven files" claim and the kill rule's byte-scope check are not satisfied as written
FINDING R96-C2-F4 major   editing frozen instruments of closed rounds after closure: freeze-integrity at T reports r93/r94/r95 broken (1 each, the round's own counter); the closed rounds say report-not-repair; the round-96 reclassification ("not instruments") is a duplicate authority the gate does not honor — harm to the calibration axis
FINDING R96-C2-F5 major   the "six self-assessment mismatches" count is 1 genuine (r79 standing population gate, SUBJECT-MISMATCH at BASE) + 5 growth-drift maintenance items (r90-r94 absolute L7 pins); the SCORECARD rows name their own revs and the counters pass there (r90/r91/r92 verified), so the five are not self-assessment mismatches under prompt §9
FINDING R96-C2-F6 minor   the battery's bite() keeps no per-run output, so the official r91 grow failure is unrecoverable from the receipt; the L1 diagnostic is a separate reconstruction. Print the failing counter's output on a failed bite
FINDING R96-C2-F7 info    re-pinning the absolute totals to 40 would not meet the predicate: controls/c2-repin-abs.txt prints GROWS checked=6 tolerant=0, PREDICATE R96-C2 fail; the grow leg makes the executed total 41
FINDING R96-C2-F8 info    no old receipts or claims files were edited (git diff BASE..T clean for them); the history is append-only, but the instrument bytes at the same paths changed — a provenance break, not a file rewrite
FINDING R96-C2-F9 info    the GROWS leg covers only the six repaired counters, not the r79 standing population gate; growth tolerance of the one gate the SCORECARD calls standing is not established
```

## Strongest objection I could not refute

- **C1:** the claim's finding set is not the full set of decisive grading gaps. The grader checks the
  conflict report at exactly one point (user 101, email, `values["source_a"]` + `selected`), so
  under-report, over-report, wrong priority winners on other conflicts and incomplete `values` all
  pass. I could not refute that the replay itself is real (the probe, the captured grader, the
  unmodified solve.sh and the 17/17 reward agreement hold); the narrowing is the finding set, not
  the replay.
- **C2:** the strongest objection I could not refute is the predicate's nondeterminism. The official
  run fails (5/6 grows) and my independent run at the same rev passes (6/6), so the claim's "not
  met" is a flake rather than a stable property; the instrument cannot support a sound verdict
  either way. Separately, the five r90-r94 reds are not self-assessment mismatches at the revs the
  SCORECARD names; they are growth drift of absolute pins. I could not refute that the repair is
  useful maintenance, but I can refute the six-mismatch calibration count, and the r87 historical
  break is a new mismatch the claim does not disclose. The calibration axis is harmed by the repair,
  not improved by six.

## Tool installs

None. No pacman, uv tool, npx or binary install; the venvs are scratch (`uv venv` + `uv pip install`
from the existing cache/index, recorded above). No host sysctl was touched.

## Exact commands (representative)

```sh
S=/fast/scratch/hyaku/kengaku-r96/CriticClaims
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q --detach 09717e49ff46fad5b255619d671aaaae52dfc180
git -C "$S/lane" rev-parse --show-toplevel   # $S/lane
cd "$S/lane" && python3 plans/round96_c1_replay.py --lane . --rev 09717e49… --work "$S/w-c1t" --env-venv "$S/E" --grader-venv "$S/G"
cd "$S/lane" && python3 plans/round96_standing_battery.py --lane . --rev 09717e49… --work "$S/battery-t"
cd "$S/lane" && python3 plans/round87_c1_replay.py --lane . --rev 10de494d14abf0b77979225f51b3b72e73c0d2ed --work "$S/w-r87"
cd "$S/lane" && python3 "$S/r87-old.py" --lane . --rev 10de494d14abf0b77979225f51b3b72e73c0d2ed --work "$S/w-r87-old"
cd "$S/lane" && python3 plans/round94_freeze_integrity.py --lane . --freeze d9cd18a7 --rev 09717e49… --claims plans/round-95-claims.md --work "$S/w-freeze-95"
# fixtures: clone --shared at T, checkout BASE -- <paths>, commit with fixture identity, run the counter from the fixture root
```

## Receipts in this directory

`c1-t-mine.txt`, `c1-noc1.txt`, `c1-noc2.txt`, `newstate2.txt`, `r87-at-r87T.txt`,
`r87-old-at-r87T.txt`, `freeze-r93.txt`, `freeze-r94.txt`, `freeze-r95.txt`, `base-r79.txt`,
`base-r87.txt`, `base-r90.txt`, `base-r91.txt`, `hist-r90.txt`, `hist-r91.txt`, `hist-r92.txt`,
`git-scope.txt`, `battery-t.txt` (my independent battery run at T: `STANDING 14/14`,
`BITES 12/12`, `GROWS 6/6`, `PREDICATE R96-C2 pass`, rc 0 — the official L1 `c2-tip.txt` is the
predicate receipt and it prints `GROWS 5/6`, `PREDICATE R96-C2 fail`, rc 1).
