# M5LedgerDeclMutants — scoped findings (round 55, wave 1, seat M5LedgerDeclMutants)

Role: mutation-tester. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen base tip `798f5e9ef30ef39291295565209b65a17343c00e`. Scratch
`/fast/scratch/hyaku/kengaku-r55/M5LedgerDeclMutants/` (deleted at end of seat).
Full receipts: `.ufo/waves/round-55/w1/M5LedgerDeclMutants/mutants.md` · report:
`.ufo/waves/round-55/w1/M5LedgerDeclMutants/report.md`.

## Question

Do the ledger's own declarations bind? Four mutants of a **copy** of `plans/round54-entrytruth.json`
(scratch clones only) run against the frozen r54 counter `plans/round54_c2_entrytruth.py`
(sha256 `44c3f412…`), which re-executes every ledger row and compares declared vs observed truth.

Detector (identical in every arm):
`python3 plans/round54_c2_entrytruth.py --lane <pristine-clone> --source <arm-clone> --work <scratch>/work/<arm> --jobs 8`

## Results — all four mutants killed

| mutant | mutation | observed counter output | verdict |
|---|---|---|---|
| M1 | green row `config-projection`: `entry_exit` 0→1, state kept `green` | `BAD-DECL config-projection` (`bad_decl=1`); row dropped from execution (`executed=77`, `observed_green` 59→58) | **KILLED** |
| M2 | green row `grader-perturb` → `red`, `entry_exit` 1, bogus evidence, well-formed reason | `MISMATCH grader-perturb declared exit=1 observed exit=0` (`mismatched=1`) | **KILLED** |
| M3 | ledger row `catalog-probe` deleted | `MISSING catalog-probe` (`missing=1 extra=0`) — **MISSING** direction, `EXTRA` never fires | **KILLED** |
| M4 | row name duplicated in the JSON (`no_dup` hook) | `LEDGER ledger unreadable: duplicate JSON key`, `ledger=0`, 78×`MISSING`, **no execution at all** (no `SOURCE`/`RUN`/`TIPSTATE`) | **KILLED** |

Direction corrections to the seat brief (observed, not assumed): a false **red** declaration is reported as
`MISMATCH`, never `LAUNDERED` (r54 labels `LAUNDERED` only for declared-green rows that exit nonzero); a
**deleted** ledger row is reported as `MISSING` (registry→ledger direction), never `EXTRA`; a duplicate JSON
key surfaces as *ledger unreadable*, not through the counter's `duplicate_names=0` field (that field counts
duplicate SKILL.md registry rows). In M2 the bogus **evidence fragment is never tested** — the exit mismatch
short-circuits before the evidence leg.

## Baseline finding the L1 must act on (measured at the frozen base tip, clean clone)

The **pristine baseline is already RED**: `PREDICATE R54-C2 fail`, exit 1, with `laundered=3`,
`evidence_missing=1` — four rows of the r54 ledger are false declarations *at the base tip*:

* `defect-ledger` — declared green/0, observed exit 1 → `LAUNDERED`
* `round36-c1-battery` — declared green/0, observed exit 1 → `LAUNDERED`
* `round52-c2` — declared green/0, observed exit 1 → `LAUNDERED` (the known r52 registry regression that
  R55-C1 repairs; the claim keeps this row green)
* `round35-c1-coverage` — declared red/1, declared evidence fragment absent from the output → `EVIDENCE-MISSING`
  (the claim names this row for re-derivation)

R55-C2's frozen after-predicate requires `laundered=0 mismatched=0 evidence_missing=0` and
`TIPSTATE declared == observed`. The claim's correction list names only `round35-c1-coverage` (evidence) and
`round52-c2` (kept green after the repair). **`defect-ledger` and `round36-c1-battery` are not named and are
still declared green/0 in the lane's current working-tree ledger (83 rows, checked 2026-10-30 after the
L1's `248a42b8`)** — unless their behaviour changes at the landing revision, the after-predicate cannot hold.
Re-measure both at the landing revision and re-declare them from observed behaviour.

## Baseline-red consequence for the method

Because the pristine baseline is red, the overall predicate is not an oracle here (a baseline failure is
inconclusive). The kill signal used is **per-row and differential**: a mutant is killed iff its arm emits a
defect line naming the mutated row that is absent from both the pristine baseline arm and a dirty-tree
control arm (DC: the only ledger change is the unused `sec` field `0.4`→`0.41`, so the tree is dirty but
semantically identical). The DC arm reproduced the baseline defect set exactly and differed only in
`clean=NO` — so the dirty-tree confound contributes no defect line.

## Restoration evidence

All four mutant trees plus the control were restored byte-for-byte (ledger sha256 back to
`40a77a3baa10f8d96159b136083cc1de3f86c1b6515f318bb6fd6503216de5f7`, `git status --porcelain` empty in each),
and the detector was re-run on every restored tree: all four restored arms print the **byte-identical**
baseline block, i.e. every mutant signal disappears on restore. The lane worktree's own ledger was never
written (same sha256 before and after; `git status --porcelain` empty there).

## Defects found in the round's own artefacts

1. R55-C2's after-predicate cannot hold at the landing revision unless the two unnamed false declarations
   (`defect-ledger`, `round36-c1-battery`) are re-declared — see above. This is a *ledger data* fix, not a
   rule change.
2. The r54 counter's `duplicate_names=N` field does not cover duplicate JSON keys in the ledger; that class
   of tampering appears only as `LEDGER ledger unreadable: duplicate JSON key`. A reader scanning
   `duplicate_names=0` alone would not see it. Not a soundness break (the ledger fails closed), but the
   field name over-promises. Reported, not fixed (the r54 counter is frozen).
