# CriticR86 — adversarial review of R86-C1 and R86-C2

Seat: `CriticR86` (leaf, attack). Read-only against the lane; every lane-relative path below
resolves in `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (lane root), and `receipts/`
abbreviates `.ufo/waves/round-86/w1/CriticR86/receipts/`.

- Measured revision: `a571044c1ea7c243791330607c5b90b6afce9a15` (`master`; moved during the
  review `f357e4c1` → `981d6f19` → `4d2a0ee8` → `ab9da0d4` → `a571044c`; instrument bytes
  re-checked unchanged at the last tip, `receipts/16-provenance.txt` §1).
- Frozen inputs: claims `61b0e074a44259c8c022aa2fda257182a0708346`, instruments
  `316811fa604eeef1d157bdbf62b5595891dc015a`, BASE `88651a72ef112ed9f5361e1c8c197babec691f96`.
- Executed by me: both counters at tip and BASE, all eight frozen controls, both selftests,
  both mutant batteries, `state_check --summary` / `--selftest`, an independent revert test
  both ways, the L1 `separation.sh`, two strict-type grader mutants under the probe's own
  sandbox, one traceback-line probe, and four negative fixtures (ancestor tip, malformed
  ledger ×2). No lane file was written; no network was used; no mutating git command.
- Deliberately **not** done: I did not re-fetch the upstream grader (my item names no
  fetch). Provenance was checked against the seat-fetch artifact and the frozen digests.

## Verdict

| claim | frozen at tip | my run at `a571044c` | BASE `88651a72` | verdict |
|---|---|---|---|---|
| R86-C1 | `defects=0`, pass, exit 0 | `TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0` / **pass** / 0 (`receipts/01`) | `defects=7`, fail, 1 (`receipts/02`) | **met on its frozen predicate and target** |
| R86-C2 | `defects=0`, pass, exit 0 | `TARGET derived_line=151 shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0` / **pass** / 0 (`receipts/06`) | `defects=3`, `state_mismatches=1`, fail, 1 (`receipts/07`) | **met on its frozen predicate and target** |

No `DEFECT` line exists at the tip; neither BASE run reaches its target; the frozen
predicates are unchanged from the freeze commit; the instruments are byte-identical to
`316811fa`. **No kill-rule trigger and no BLOCKER.** Eight defects below are precision and
fail-closed defects, not grounds to withhold either claim on its own frozen terms.

The four C1 controls all print `target_reached=False` (`receipts/03-*`), the four C2 controls
too (`receipts/08-*`); the selftests are 10/10 and 4/4 red-as-designed (`receipts/04`,
`receipts/09`); the mutant batteries reproduce the committed `5 necessary + 1 declared`,
`1 necessary + 2 declared` split (`receipts/05`, `receipts/10`); `state_check --summary`
prints `assertions=329 match=318 mismatch=0 … VERDICT: PASS` and `--selftest` exits 0
(`receipts/11`, `receipts/12`).

## Findings

Each finding names the axis it impacts, the smallest safe correction, and what would falsify
my reading. All are against the frozen text or the instrument's behaviour, never against the
frozen predicate, target, case table, control set, kill rule or leg list (none of which I
touch).

### C1-F1 — MINOR — L3 is an ancestry test, and the frozen prose claims more

- **Counterexample.** Copy the measured tree, change **one line** of the delivered receipt,
  `LANE_TIP bfda0472…` → `88651a72…` (the round-85 BASE, a tree that never held the receipt,
  table or probe), run the counter: full target, `PREDICATE R86-C1 pass`, exit 0
  (`receipts/15`, first block). The delivered receipt itself already declares
  `LANE_TIP bfda0472d5c163b2b5d2bbf22557f60a940de180`, an ancestor, not the measured tip.
- **Evidence.** `plans/round86_c1_replay.py:318-329` implements exactly the frozen leg
  ("resolves and is an ancestor"); `plans/round-86-claims.md:55` then says "`L2` and `L3` are
  what a receipt copied in from elsewhere cannot satisfy". L3 excludes cross-repo and
  non-ancestor tips only. The `forged-receipt` control tests the zero tip
  (`plans/round86_c1_replay.py:466-471`), i.e. the easy case; no control tests a wrong but
  resolvable ancestor.
- **Axis.** coverage (evidence provenance), not the count.
- **Smallest safe correction.** Do not change the leg. In the report carry the narrow form:
  "L3 excludes a tip that does not resolve in this repo or that is not an ancestor; it does
  not bind the receipt to the revision it was minted at." Optionally add an ancestor-tip
  fixture to the control set so the limit is measured rather than argued.
- **Would falsify me:** a leg elsewhere in the counter comparing the stamp to the measured
  tip, or a control that rejects an ancestor tip. Neither exists (`check()` discards
  `fresh_stamp`, `:366-367`).

### C1-F2 — MINOR — `members=1` is a literal, so "grows by exactly one member" is not counted

- **Counterexample.** `stats = {"members": 1, …}` is initialised at
  `plans/round86_c1_replay.py:209` and never recomputed; the pass conjunct reads it at
  `:386`. Nothing in the counter counts `status=executed` rows or diffs the BASE ledger, so a
  second member flipping to `executed` between BASE and tip would leave `members=1` and the
  target green.
- **Evidence.** I measured the growth independently: executed **29 → 30** of 88, and the row
  whose status changed is exactly `['raman-fitting']` (`receipts/16` §2–3). So the sentence is
  true; it is simply not what the counter measures. This is the Q31/Q46 shape ("the pass path
  prices every clause of the frozen sentence").
- **Axis.** coverage.
- **Smallest safe correction.** Report the growth as the measured 29→30 and the
  single-row diff (my `receipts/16` reproduces both commands); in a successor instrument
  count executed rows and diff against the BASE ledger instead of asserting `1`.
- **Would falsify me:** a code path that assigns `stats["members"]` from the ledger. `grep`
  shows only `:209`, `:386`, `:395`, `:405`.

### C1-F3 — MINOR — a malformed ledger produces a traceback, not a named defect, and exits 1

- **Counterexample.** Two fixtures over the measured tree: `members` as a list, and the
  `raman-fitting` row as a string. Both crash:
  `TypeError: list indices must be integers or slices, not str` at `:245`, and
  `AttributeError: 'str' object has no attribute 'get'` at `:253`; exit 1, **no `DEFECT`
  line, no `TARGET` line, no `PREDICATE` line** (`receipts/15`, last two blocks).
- **Evidence.** The module docstring promises "Exit: 1 a named defect"; `QUALITY.md` Q49
  requires "an unknown or malformed line is a named finding, never a traceback". The
  uncaught-exception exit code is 1, i.e. indistinguishable from a scored red to anything
  that reads the exit code alone.
- **Axis.** operability of the instrument; no claim axis.
- **Smallest safe correction.** Widen the parse guard at `plans/round86_c1_replay.py:243-247` to
  `except (json.JSONDecodeError, KeyError, TypeError, AttributeError)` and emit
  `DEFECT L7-ledger malformed`.
- **Would falsify me:** a top-level handler in `main` that converts this class of exception
  to `DEFECT`/`SETUP`. `main` catches only `SetupDefect` and `TimeoutExpired` (`:698-701`).

### C1-F4 — MINOR — three labels in the frozen sentence read stronger than their measurements

- **Evidence.** (a) "eight frozen schema-drift case shapes": the table's own `why` cells mark
  `exact` as the positive control and `g-amplitude-just-outside` as "numeric-band control, not
  schema" (`plans/round86-cases.json`), so six of eight are schema drift. (b) `located=1`
  means only that `corpus/evidence/round86/raman-fitting-probe.txt` exists
  (`plans/round86_c1_replay.py:276-281`), not that it was located to the subject. (c)
  `legs=24` and `mismatches=0` are parsed from the receipt's own summary line
  (`plans/round86_c1_replay.py:175-189`, `:330-340`); they are constrained by the eight `CASE` lines and the frozen
  vectors but not independently counted.
- **Axis.** coverage.
- **Smallest safe correction.** Say "eight case shapes (six schema-drift, two controls)" and
  define `located` in the report as "receipt file present"; keep the predicate.
- **Would falsify me:** a schema-drift marker on cases 1 and 8 in the frozen table. The table
  says the opposite in its `why` cells.

### C1-F5 — MINOR — the separation evidence path named by the frozen sentence does not exist at the tip

- **Evidence.** `plans/round-86-claims.md` (Causally separable): "The separation test is run
  and committed under `.ufo/waves/round-86/L1/separation.txt`." At `a571044c` the L1 tree
  carries `separation.sh` and seven other files, **no `separation.txt`**
  (`receipts/18`). The script itself is committed and, run by me at the tip, prints both
  directions green (`receipts/17`), and my own independent fixtures agree (same content:
  C2 green with C1 reverted, C1 green with C2 reverted). So the *fact* holds; the *cited
  evidence file* is absent.
- **Axis.** calibration/coverage separability (R13).
- **Smallest safe correction.** Run `separation.sh` and commit its stdout as
  `.ufo/waves/round-86/L1/separation.txt` before the report, or restate the sentence to name
  the script plus where its output is committed.
- **Would falsify me:** `git cat-file -e a571044c:.ufo/waves/round-86/L1/separation.txt`
  succeeding, or the file on disk. Both fail as of this review.

### C2-F1 — MINOR — P4/P5 read the lane's instrument, not the measured tree's

- **Evidence.** `state_summary`/`state_selftest` choose `lane/STATE` whenever it exists
  (`plans/round86_c2_repin.py:114-121`, `:124-129`), so with `--rev BASE` the **tip**
  instrument measures the BASE tree, while P3 reads the pin from the **BASE** tree. P5 ignores
  `root` entirely. This is the Q63 read-path class.
- **Measured impact: none.** Over the BASE tree the BASE instrument prints
  `match=315 mismatch=1 offline_unverifiable=7` and the tip instrument prints
  `match=317 mismatch=1 offline_unverifiable=5` (`receipts/19`, `receipts/20`): the claimed
  `state_mismatches=1` is robust under either read path. The residual risk is a dirty
  worktree instrument diverging from the measured one; at the measured tip they are the same
  bytes.
- **Axis.** calibration.
- **Smallest safe correction.** When `--root`/`--rev` is given, run `root/STATE` for P4/P5
  and print the instrument's revision (or say in the docstring that P4/P5 are taken with the
  lane instrument).
- **Would falsify me:** a code path preferring `root/STATE`. `:115` prefers `lane/STATE`.

### C2-F2 — MINOR — "not by hand-editing the pin" understates what landed

- **Evidence.** The pin is a literal: `plans/state_check.py:235`
  `(4, "PROVINCE.md:151", 151, "### Adjacent", None)`, and `SHONEN.md:12` was edited to
  match; both landed at inherited commit `0481a6d3` ("box-4 pin re-derived from PROVINCE
  bytes"), which is an ancestor of the freeze. What is derived each run is the *check* (P1)
  that the literal equals `PROVINCE.md` bytes; the edit itself was a hand edit, loudly
  annotated. The claim's P3 leg says this correctly; the Claim paragraph's "not by
  hand-editing the pin" does not.
- **Axis.** calibration.
- **Smallest safe correction.** Reword to "re-pinned to a value that is derived from
  `PROVINCE.md` bytes and re-checked every run", keeping `STALE_LINE = 129` and the lesson.
- **Would falsify me:** a pin computed at import time from `PROVINCE.md`. It is a tuple
  literal.

### WAVE-F1 — FINDING (false positive to withdraw) — ReviewerC186 F3 is wrong

- **Claim under review.** `.ufo/waves/round-86/w1/ReviewerC186/report.md` F3 asserts that the
  `2D-null-value` case sets `data["2D"] = null`, so the first failure is
  `G_peak["x0"]` and the table's cited `abs(1 - None/2670.08)` "is never evaluated".
- **Counterexample.** The case carries a **present object** with a null field:
  `"2D": {"x0": null, "gamma": 17.52, …}` (`plans/round86-cases.json`). `data["2D"]` returns
  the dict; the traceback lands exactly where the table says:
  `test_outputs.py:60 x0_correct = abs(1 - x0 / x0_expected) < 0.05`, TypeError
  (`receipts/14`). The frozen vector `P/P/E` and its prose are both correct.
- **Impact.** If F3 is copied into the round report or lesson it files a defect that does not
  exist against a frozen, correct table. Withdraw F3; the L1 should not carry it forward.
- **Would falsify me:** a rerun of the case that raises at `test_outputs.py:46`/`:55` (the
  `data["2D"]` / `G_peak["x0"]` subscript) rather than line 60. My traceback probe reports
  line 60.

## Adjudication of the assigned questions

**Is a member replay a real coverage move or a re-scored class (`db-wal-recovery`,
`sqlite-db-truncate` already `serialization-schema`)?** A real member execution, and not a
class move. At BASE the member is `unexecuted` with `reason=unattempted`; at tip it is
`executed` with a new receipt and round 86, executed 29→30, one row changed
(`receipts/16`). But `serialization-schema` was already an executed class (round 40, round
85), so the claim adds no new class; the frozen claims file says coverage "stays at its L0
cap" and does not buy a score. Read against the ledger's own contract
(`plans/grader-population-ledger.json` `why`: the unit is the member), the claim's wording is
accurate; read against a class-coverage rubric it is a no-op. That is a framing observation,
not a defect, and both readings agree with what was measured.

**Does the counter go green on ledger-only data, a forged receipt, or a table committed after
the freeze?** No in the frozen sense. `ledger-only` is red on L1/L2/L3/L5/L6
(`receipts/03-c1-control-ledger-only`); a fabricated observation is red on L5 and L6 (same
dir); a zero-tip forgery is red on L3. A table edited at the tip is refused by L4's byte
comparison against `FREEZE_REV` and, redundantly, by the probe's own `FROZEN_TABLE_SHA`
(declared redundant, `no-table-binding` mutant). The one forge that survives is the
ancestor-tip receipt (C1-F1); it survives because the observations are reproduced from the
measured tree by L6, i.e. only the *author* is unauthenticated, which the claims' honest
limit already concedes.

**Is the `E` verdict a graded observation or a harness artefact?** It is an observation of
the grader, classified by a frozen harness rule. The exceptions are raised inside the
captured function bodies — `KeyError` at `test_outputs.py:28` (renamed key),
`TypeError` at `:33` (string amplitude), `KeyError` at `:54`, `TypeError` at `:60`
(`receipts/14`) — not by the sandbox. Two caveats the claim already prices: `E` conflates
`KeyError`/`TypeError`/any other non-assertion exception, and in real TB2 both `F` and `E`
are test failures, so `E` measures the grader's *fail-softness*, not a TB2 verdict. The
verdict vocabulary in `plans/round86-cases.json` says exactly that.

**Would a strict-type grader mutant still produce the frozen vector?** No — the vector
discriminates. Under the probe's own sandbox: replacing
`A = G_peak["amplitude"]` with `A = float(G_peak["amplitude"])` flips
`g-amplitude-string` from `P/E/P` to **`P/P/P`**; inserting
`assert isinstance(A, (int, float))` flips it to **`P/F/P`**; all other cases stay put
(`receipts/13`). So the frozen `E` is load-bearing about grader strictness, not about the
harness, and the strict-type alternative that refuted a round-85 discrimination sentence is
refuted here in the other direction. This is a **failed attack**: it strengthens C1.

**Is C2's 1→0 a real calibration move or a bookkeeping repair the rubric already counts as
"restore, not extend"?** Both, correctly labelled. It is a real repair: at BASE the
instrument prints one `MISMATCH:` line, and line 129 of `PROVINCE.md` is `|---|---|---|`
while line 151 is `### Adjacent`; at tip zero and `VERDICT: PASS`. It is also a restore, and
the frozen claims file and `SCORECARD.md` (R85-C2 row: "repairs of routed defects restore,
they do not extend the ceiling") both say so — no axis increase is claimed. The repair is not
silent: `129` survives as `STALE_LINE` and in `corpus/lessons/round-86.md:58-60`.

**Is C2 separable from C1?** Yes, and better than in round 85. With C1's receipt deleted and
its ledger row restored to BASE bytes, C2 prints `defects=0` / pass; with SHONEN and the pin
back at 129, C1 prints `defects=0` / pass (`receipts/17`; my independent fixtures agree).
`state_check` carries no assertion naming `plans/grader-population-ledger.json`,
`corpus/evidence/round86/` or the raman receipt (`grep` over `plans/state_check.py`).

**Is the C2 axis named by the surface or by the number?** By the surface: the claim defines
the population as the `MISMATCH:` lines printed by `state_check.py --summary`, i.e. frozen
self-assessment prose contradicted by the repo's bytes, and names the repaired assertion
(`P3c.box.4.pointer.1`). The number 1→0 is the measurement, not the axis.

**One-artifact-one-claim, no narrowing, same sentence in plan/counter/label.** C1 counts the
receipt, table, tool, ledger row and capture; C2 counts `PROVINCE.md`, `SHONEN.md`,
`state_check.py` and its output; the revert test above is the R13 evidence. The delivered
targets are the frozen targets, un-narrowed. The plan sentence, the counter docstrings
(`plans/round86_c1_replay.py:7-22`, `plans/round86_c2_repin.py:7-19`) and the `SKILL.md` gate
rows 752–753 carry the same leg names and verdict vocabulary.

## Residual risk / limits of this review

- The tip moved five times during the review. Everything above is stated at `a571044c`; the
  instruments were re-hashed at that tip (`receipts/16` §1). A later commit touching
  `PROVINCE.md` above line 151 would move C2's derived line and turn its target red; the
  counter would report that (`derived_line` changes), so it fails loudly rather than
  silently.
- I did not re-fetch `raw.githubusercontent.com`; the pinned capture was checked by digest
  against the frozen `SUBJECT_SHA`, the seat-fetch artifact and the committed capture
  (`receipts/16` §4), not against a live 200.
- I did not read the earlier-attempt commits' provenance beyond confirming all four named
  commits are ancestors of the tip, and that the receipt was first committed at `9972c87c`
  (named in the claims as inherited work, `receipts/16` §5).
- The mutant batteries, selftests and controls were re-run by me at the measured tip; their
  results agree with `.ufo/waves/round-86/L1/freeze-battery.txt` and `base-runs.txt`.

## Receipt index

`receipts/` under this directory: `00-tip`, `01-c1-tip`, `02-c1-base`, `03-c1-control-*`
(4), `04-c1-selftest`, `05-c1-mutants`, `06-c2-tip`, `07-c2-base`, `08-c2-control-*` (4),
`09-c2-selftest`, `10-c2-mutants`, `11-state-summary`, `12-state-selftest`,
`13-strict-type-mutants`, `14-null-case-failing-line`,
`15-ancestor-tip-and-malformed-ledger`, `16-provenance`, `17-separation`,
`18-separation-evidence-at-tip`, `19-base-tree-state-check-base-instrument`,
`20-base-tree-state-check-tip-instrument`.

Scratch (`/fast/scratch/hyaku/kengaku-r86/CriticR86/`) is deleted before this seat yields;
every number quoted above is in a receipt inside this directory.
