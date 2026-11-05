# MutTesterC1 — mutation test of `plans/round94_c1_replay.py` (R94-C1 counter)

Seat: MutTesterC1 (kengaku round 94, wave 1, leaf). Host 2026-11-05.
Instrument under test: `plans/round94_c1_replay.py`, frozen sha256
`ff6a6e4622c56fe8f4de41dfbddcd1f9d90f9b98fa2f99bac0c1bd22447872d9` (F table row 3).
Method: 13 single-point byte-level mutants + 1 two-point interaction mutant, each run against
three situations — the lane at measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e` (scratch
`--shared` clone detached at T; a pristine anchor run against the real lane path produced
byte-identical semantic output, receipt `b-lane-actual.txt`), the rebuilt **ledger-only** forgery
fixture, and the rebuilt **member-swap** forgery fixture, both committed on P1
`997a6fe5fbb4a4af9f38e436bccd8f604da1d746` clones exactly as
`.ufo/waves/round-94/L1/controls/README.md` describes. All runs: `python3 <counter> --lane R --rev
90c7677f…(or HEAD) --work <scratch>`; every receipt in `receipts/`.

## Baselines (pristine bytes, restored state)

| receipt | result | vs committed control |
|---|---|---|
| `b-T.txt` | `LEGS L1=pass…L9=pass`, `TARGET executed_rows=38 … defects=0`, `PREDICATE R94-C1 pass`, rc 0 | equals the frozen predicate in `plans/round-94-claims.md` |
| `b-lane-actual.txt` | identical semantics to `b-T.txt` (diff on `# ` header lines only) | run against the real lane path, read-only |
| `b-fixture-ledger-only.txt` | 8/9 legs fail, only L7 pass, rc 1 | `c1-forgery-ledger-only.txt`: every semantic line equal; only the ephemeral fixture-commit sha differs (`dca46bcfb68e` → `4679b77e6530`) |
| `b-fixture-member-swap.txt` | 9/9 fail incl. `L7 … set_added=[path-tracing, write-compressor] set_removed=[circuit-fibsqrt]`, rc 1 | `c1-forgery-member-swap.txt`: equal, same caveat (`28a5ead2e3bd` → `3916879010c1`) |
| `b-pristine-bad-bwrap.txt` | `could-not-evaluate`, rc 2 | semantics of committed `c1-sandbox-red.txt` |

Fixture construction: `--shared` clones detached at P1, `plans/grader-population-ledger.json`
JSON-edited (write-compressor → `status=executed, round=94, classes=[file-artifact,
stdout-inspection, subprocess-exec]`; member-swap additionally `circuit-fibsqrt`→unexecuted,
`path-tracing`→`executed` with fibsqrt's `round=42, receipt=corpus/evidence/round42/fibsqrt-probe.txt`,
own classes), committed with `user.name=fixture <fixture@invalid>` after
`rev-parse --show-toplevel` asserted equal to the fixture dir. Fixture commits:
ledger-only `4679b77e6530d6a0babf6e0368d059c24a2f38ef`, member-swap
`3916879010c1e3aef2d67b0ede2288262f977b1d`.

## Mutants (before hash = pristine `ff6a6e46…`; after hash per row, full table in `mutants/MUTANTS.sha256`)

| id | byte mutation (anchor → replacement, applied exactly once) | after sha256 (16) |
|---|---|---|
| m01 | `and rev_set == base_set \| {MEMBER}` → `and True` (L7 member-set check dropped) | `a4a242edd1617899` |
| m02 | `set_ok = bool(base_set) and` → `set_ok = not base_bytes or` (BASE ledger absent ⇒ empty set ⇒ pass) | `45e2c0833298d53c` |
| m03 | `and seen == set(predicted) and len(receipt["cases"]) == len(predicted)` → `` (L5 coverage clauses dropped; extras/missing accepted) | `8ef92eb07010587c` |
| m04 | `and rerun_obs == receipt["obs"]` → `and len(rerun_obs) == len(receipt["obs"])` (L6 compares counts not lines) | `23fa17ab48b6c16d` |
| m05 | `text = blob(root, added[0], CLAIMS)` → `text = blob(root, rev, CLAIMS)` (L4 frozen table read at --rev) | `559f0ac2215d78fa` |
| m06 | `l9 = (f.get("TOOL_SHA")` → `l9 = True or (f.get("TOOL_SHA")` (L9 stamps skipped) | `b2c01cbf8e6dcf35` |
| m07 | `for p, want in PINS.items())` → `… if p == "tests/test_outputs.py")` (L2 checks only the grader pin) | `06fecc784c42db20` |
| m08 | sandbox branch `print("PREDICATE R94-C1 could-not-evaluate")/return 2` → `…fail"/return 1` | `cb92890dcbc3800a` |
| m09 | `l1 = receipt_bytes is not None` → `l1 = True` (receipt absent accepted) | `f3b6c2d64100e63b` |
| m10 | ` and git(lane, "merge-base", "--is-ancestor", tip, rev).returncode == 0` → `` (L3 dropped) | `e12bdca4c623b783` |
| m11 | ` and sha(tool_bytes) == frozen.get(TOOL)` → `` (L8 probe-sha pin dropped) | `ccdaad1303af20c8` |
| m12 | `return 0 if ok else 1` → `return 0` (exit-code collapse) | `74b9e9b3ca665e02` |
| m13 | handler `could-not-evaluate`/`sys.exit(2)` → `fail`/`sys.exit(1)` | `aded5b888799a038` |
| m03+m04 | both m03 and m04 applied (interaction probe) | `49a757203f1cdeab` (16) |

## Kill table (39 matrix runs + 6 CNE-path runs + 8 demo runs; every receipt in `receipts/`)

"identical" = every semantic line (`LEGS/TARGET/DEFECT/PREDICATE/rc=`) equals the pristine
baseline receipt for that situation. Kill = any semantic-line difference against a **committed**
P2 control receipt or the T predicate; such a mutant would have been caught by the round's own
battery.

| id | T | ledger-only | member-swap | verdict — killed by / finding |
|---|---|---|---|---|
| m01 | identical | identical | L7 fail→pass, set-defect gone | **KILLED** by committed `c1-forgery-member-swap.txt` (round-93 W-5 binding) |
| m02 | identical | identical | identical | **SURVIVES** — equivalence + info finding F6 |
| m03 | identical | L5 fail→pass | L5 fail→pass | **KILLED** by committed `c1-forgery-ledger-only.txt`/`-member-swap.txt` (L5 line); residual power shown in interaction D6 |
| m04 | identical | identical | identical | **SURVIVES** — FINDING F1 (major, D6) |
| m05 | identical | identical | identical | **SURVIVES** — FINDING F4 (minor) |
| m06 | identical | L9 fail→pass | L9 fail→pass | **KILLED** by the two committed fixture receipts (L9 line) |
| m07 | identical | identical | identical | **SURVIVES** — equivalence + info finding F7 |
| m08 | identical | identical | identical | **KILLED** by committed `c1-sandbox-red.txt` (rc 2/`could-not-evaluate` → rc 1/`fail`; `receipts/b-pristine-bad-bwrap.txt` vs `m08-l7-T-bad-bwrap.txt`) |
| m09 | identical | L1 fail→pass | L1 fail→pass | **KILLED** by the two committed fixture receipts (L1 line) |
| m10 | identical | identical | identical | **SURVIVES** — FINDING F3 (minor, D5) |
| m11 | identical | identical | identical | **SURVIVES** — FINDING F2 (major, D4) |
| m12 | identical | rc 1→0 | rc 1→0 | **KILLED** by the two committed fixture receipts (rc line) |
| m13 | identical | identical | identical | **SURVIVES** — FINDING F5 (minor; flip shown on `--rev deadbeef…`: pristine rc 2, mutant rc 1, `b-pristine-bad-rev.txt`/`m13-T-bad-rev.txt`) |

The T run kills nothing: every weakened check holds genuinely at T. All six kills come from the
committed forgery/do-nothing controls binding legs in their failing direction — that is exactly
what the P2 battery buys, and exactly where it stops.

## Forgery demonstrations for surviving mutants (fixtures committed on T clones, scratch only)

- **D4 probe-swap + regenerated receipt** (kills nothing committed; false pass under m11):
  `fix-probe-swap` commit `95898fe782ee2a2fd2e5f1cfe3e4c8c6bc5c3705` swaps one byte into the
  probe's CASE template (`"CASE %s"` → `"CASE  %s"`, obs bytes change, parse semantics identical)
  and replaces the receipt with the swapped probe's own stdout (`receipts/d4-regen-stdout.txt`,
  regen rc 0). Pristine: `L8=fail` only — `DEFECT L8 probe 73ae03edd340 vs frozen 3e1e17641ff6`,
  rc 1 (`b-D4-probe-swap-pristine.txt`). Under m11: `PREDICATE R94-C1 pass`, rc 0
  (`m11-D4-probe-swap.txt`). L6 cannot help: the rerun executes the same swapped probe from the
  archive and reproduces the forged obs exactly. L8 is the only leg tying the rerun to the frozen
  probe bytes, and every committed C1 fixture is P1-based, where the frozen table is absent, so
  L8 is exercised only in its failing direction.
- **D5 foreign-LANE_TIP receipt** (false pass under m10): `fix-foreign-tip` commit
  `58e5d9fce2c2915090915e8c1b932ec1cf414693` changes only the receipt's `LANE_TIP` line to the
  ledger-only fixture commit `4679b77e…` (child of P1, not an ancestor of T). Pristine: `L3=fail`
  only — `DEFECT L3 LANE_TIP 4679b77e6530d6a0babf6e0368d059c24a2f38ef not an ancestor of
  58e5d9fce2c2`, rc 1 (`b-D5-foreign-tip-pristine.txt`). Under m10: rc 0
  (`m10-D5-foreign-tip.txt`). LANE_TIP is stamped outside the OBSERVATIONS block, so L6 never
  checks provenance; L3 is the only provenance anchor.
- **D6 forged receipt omitting all five failing cases** (false pass only under m03+m04):
  `fix-trimmed-receipt` commit `0977ccfc595ff1515717cbd24c580503facdfcaa` (3-line variant) then
  `933a359185b10ea16510aede761329e9e5d88719`: receipt keeps genuine stamps and 8 obs lines that
  are `C01×3, C04×2, C08×3` — every line obs==pred (passes any per-line check), len==8 (passes a
  count check), but grader-failing cases C02/C03/C05/C06/C07 are absent. Pristine: `L5=fail` (`case
  coverage 8 of 8` — the seen-set clause) + `L6=fail` (`equal=False`), rc 1
  (`b-D6-forged-receipt-pristine.txt`). m04 alone: `L6=pass`, `L5=fail`, rc 1
  (`m04-D6-forged-receipt.txt`). m03 alone: `L5=pass`, `L6=fail`, rc 1
  (`m03-D6-forged-receipt.txt`). **m03+m04: `PREDICATE R94-C1 pass`, rc 0**
  (`m03m04-D6-forged-receipt.txt`). L5's per-line pin and L6's line equality are jointly
  load-bearing; neither alone survives this forgery, and no committed control exercises either in
  the positive direction.

## Findings (routed to round 95; no instrument touched — FROZEN RULE respected)

- **F1 (major).** `L6` compares observation blocks line-by-line, but its weakening (m04,
  counts-not-lines) survives the entire committed battery, and jointly with m03 the counter false-
  passes a receipt that hides every failing grader case (D6, rc 0). All committed C1 forgery
  controls are P1-based, so the receipt-side legs (L1, L5, L6, L9) are only ever exercised in the
  failing direction. Missing control: a post-F forged/trimmed-receipt fixture (T + receipt commit),
  judged `rc 1` by the frozen counter — my `b-D6-forged-receipt-pristine.txt` is exactly that
  receipt and can be landed as the control.
- **F2 (major).** `L8` is the only anchor from the rerun to the frozen probe bytes; m11 survives
  the battery and false-passes a probe-swap + regenerated-receipt forgery (D4, rc 0). Missing
  control: a post-F probe-swap fixture judged rc 1 (`b-D4-probe-swap-pristine.txt`).
- **F3 (minor).** `L3` is the only provenance anchor (stamps sit outside the OBSERVATIONS block);
  m10 false-passes a foreign-tip receipt (D5, rc 0). Missing control: a forged-LANE_TIP receipt
  fixture judged rc 1 (`b-D5-foreign-tip-pristine.txt`).
- **F4 (minor).** `L4`'s single-adding-commit guard (m05, table read at --rev) is uncontrolled:
  no committed C1 control re-adds `plans/round-94-claims.md` (two adding commits) or edits the
  table between the adding commit and rev. The analogous situation is controlled for the gate
  (c2's `w2-lie-repaired`), not for this counter.
- **F5 (minor).** The `__main__` could-not-evaluate path (unresolved revision `--rev deadbeef…`,
  git-archive failure) has no committed control; only the sandbox branch is controlled
  (`c1-sandbox-red.txt`). m13 flips rc 2→rc 1 on that path undetected.
- **F6 (info).** m02's BASE-absent fail-open is unreachable in every committed situation (BASE
  ledger present in all fixtures and at T); it flips only on shallow/pruned/rewritten clones,
  where the pristine counter already fails safe (L7 red). No committed shallow-clone control.
- **F7 (info).** m07's weakening is inert: the probe itself re-verifies the same six capture pins
  at rerun time and aborts rc 2 on tamper (counter → could-not-evaluate), and the kept subject pin
  still guards the grader; L2's pins are byte-level redundancy over the probe's self-check + L6.

## Equivalence / restoration evidence

- Lane `plans/round94_c1_replay.py` sha256 before session and after all runs:
  `ff6a6e4622c56fe8f4de41dfbddcd1f9d90f9b98fa2f99bac0c1bd22447872d9` (equal; also the F-table
  row). I never modified any lane-tracked file; every mutant ran from scratch bytes.
- All fixture repos asserted `git rev-parse --show-toplevel == fixture dir` before first commit;
  throwaway identity `fixture <fixture@invalid>`; no git/jj mutation in the lane; no sysctl touched.
- Host userns `122865` (> 0); bwrap `/usr/bin/bwrap`; no tool installed or upgraded (existing
  git, python3.14, bwrap, rustc 1.99.1 sufficient) — nothing to record under the tooling
  authorization.
- Scratch `/fast/scratch/hyaku/kengaku-r94/MutTesterC1` removed at seat end; nothing citable
  lives there — every receipt referenced above is copied under `receipts/`, mutants under
  `mutants/`, generators (`gen_mutants.py`, `run_one.sh`, `tabulate.py`) alongside.
- Note: the lane working tree shows ` M SCORECARD.md` and ` M SKILL.md` and a tip advanced to
  `d04e6664…` — sibling/L1 activity, not mine; all my runs pinned `--rev 90c7677f…` explicitly.
