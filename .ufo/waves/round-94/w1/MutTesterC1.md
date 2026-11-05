# MutTesterC1 — scoped findings (R94-C1 counter mutation test)

Full report: `.ufo/waves/round-94/w1/MutTesterC1/report.md`. Receipts:
`.ufo/waves/round-94/w1/MutTesterC1/receipts/` (59 files incl. `TABLE.md`, the machine kill
table; 77 files seat-wide). Mutants + hashes: `.ufo/waves/round-94/w1/MutTesterC1/mutants/` (`MUTANTS.sha256`).

13 single-point byte-level mutants (+ 1 two-point interaction probe m03+m04) of frozen
`plans/round94_c1_replay.py` (`ff6a6e4622c56fe8f4de41dfbddcd1f9d90f9b98fa2f99bac0c1bd22447872d9`),
each run at measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e` and against the two rebuilt
P2 forgery fixtures (ledger-only `4679b77e6530d6a0babf6e0368d059c24a2f38ef`, member-swap
`3916879010c1e3aef2d67b0ede2288262f977b1d`, committed on P1 clones per
`.ufo/waves/round-94/L1/controls/README.md`; both baselines reproduce the committed control
receipts line-for-line except the ephemeral fixture-commit shas).

Killed by committed controls (6): m01 (member-swap, L7 set line), m03 (fixtures, L5 line), m06
(fixtures, L9 line), m08 (c1-sandbox-red, rc 2 → 1), m09 (fixtures, L1 line), m12 (fixtures, rc
line). The T run kills nothing — all committed C1 forgery controls are P1-based, so every
receipt-side leg is exercised only in its failing direction.

Survivors (7) with disposition:
- m04 (L6 counts-not-lines) — FINDING major: with m03 it false-passes a forged receipt
  (`C01×3, C04×2, C08×3`, 8 obs lines, all obs==pred, len==8) that omits the five grader-failing
  cases; fixture commit `933a359185b10ea16510aede761329e9e5d88719`; pristine rc 1, pair rc 0;
  each mutant alone stays rc 1 (L5 pin / L6 equality respectively). Receipt-side legs have no
  committed positive-direction control; `receipts/b-D6-forged-receipt-pristine.txt` is the missing
  control's expected output.
- m11 (L8 probe-sha dropped) — FINDING major: false-passes a probe-swap + receipt-regenerated-by-
  swapped-probe forgery (fixture `95898fe782ee2a2fd2e5f1cfe3e4c8c6bc5c3705`); pristine `L8=fail`
  rc 1, m11 rc 0; L6 reproduces the forged obs because the rerun executes the same swapped probe.
  Missing control expected output: `receipts/b-D4-probe-swap-pristine.txt`.
- m10 (L3 ancestor check dropped) — FINDING minor: false-passes a genuine receipt whose LANE_TIP
  is replaced by a non-ancestor commit (fixture `58e5d9fce2c2915090915e8c1b932ec1cf414693`);
  pristine `L3=fail` rc 1, m10 rc 0; LANE_TIP is stamped outside the OBSERVATIONS block so no
  other leg sees provenance. Missing control expected output:
  `receipts/b-D5-foreign-tip-pristine.txt`.
- m05 (L4 table read at --rev) — FINDING minor: no committed C1 control re-adds the claims file
  (two adding commits) or edits the table after the adding commit; the analogous case is
  controlled for the c2 gate (`w2-lie-repaired`), not here.
- m13 (handler could-not-evaluate rc 2→1) — FINDING minor: no committed control on the
  unresolved-revision / archive-failure path (`--rev deadbeef…`: pristine rc 2, m13 rc 1); only
  the sandbox branch is controlled.
- m02 (BASE-ledger-absent ⇒ empty set ⇒ pass) — info: unreachable in all committed situations;
  flips only shallow/pruned/rewritten clones where pristine already fails safe; no shallow-clone
  control.
- m07 (L2 only grader pin) — info: inert; the probe self-verifies the same six capture pins at
  rerun (tamper → probe rc 2 → could-not-evaluate) and the kept subject pin guards the grader.

Restoration: lane instrument bytes unchanged before/after (`ff6a6e46…`, the F-table row); no
lane-tracked file modified; all mutations ran from scratch bytes; fixtures asserted
`rev-parse --show-toplevel` before committing with throwaway identity; no sysctl touched; no
tools installed/upgraded. Scratch `/fast/scratch/hyaku/kengaku-r94/MutTesterC1` removed. The ` M
SCORECARD.md` / ` M SKILL.md` working-tree modifications and the tip advance past T are sibling/L1
activity, not this seat's.

FINDING R94-C1-counter-mutm04 major — L6 line equality + L5 coverage clauses are jointly load-bearing; m04 survives the committed battery and m03+m04 false-pass a receipt hiding all five failing cases (rc 0); lane lacks any post-F forged-receipt control
FINDING R94-C1-counter-mutm11 major — L8 is the only rerun↔frozen-probe anchor; m11 survives the battery and false-passes a probe-swap + regenerated-receipt forgery (rc 0); lane lacks a post-F probe-swap control
FINDING R94-C1-counter-mutm10 minor — L3 is the only provenance anchor (stamps outside OBSERVATIONS block); m10 false-passes a foreign-LANE_TIP receipt (rc 0); lane lacks a forged-tip control
FINDING R94-C1-counter-mutm05 minor — L4's single-adding-commit guard has no committed C1 control (claims re-add / post-F table edit unexercised)
FINDING R94-C1-counter-mutm13 minor — handler could-not-evaluate path (unresolved rev / archive failure) uncontrolled; rc 2→1 undetected
FINDING R94-C1-counter-mutm02 info — BASE-absent fail-open reachable only on shallow/pruned clones where pristine already fails safe; no shallow-clone control
FINDING R94-C1-counter-mutm07 info — L2 pin weakening inert (probe self-verifies all six capture pins at rerun)

Paths written:
- .ufo/waves/round-94/w1/MutTesterC1.md
- .ufo/waves/round-94/w1/MutTesterC1/report.md
- .ufo/waves/round-94/w1/MutTesterC1/receipts/ (59 files: baselines b-*, matrix m*-T/-FL/-FS, CNE probes, demos b-D4/D5/D6 + mutant runs, TABLE.md, d4-regen)
- .ufo/waves/round-94/w1/MutTesterC1/mutants/ (13 + interaction + MUTANTS.sha256)
- .ufo/waves/round-94/w1/MutTesterC1/{gen_mutants.py, run_one.sh, tabulate.py}
