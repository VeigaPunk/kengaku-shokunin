# F38MutC2Counter — mutation test of `plans/round38_c2_verify.py` (round 38 wave 2, falsify)

Seat F38MutC2Counter, 2026-10-26. Lane tip under attack `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`, clone at
`/fast/scratch/hyaku/kengaku-r38/F38MutC2Counter/lane` (toplevel verified, tree clean, counter digest
`d906d55f26562807a818ac55c0118cb5b43b7f570c0d891c525c64be2e9d437d` = frozen). Receipts (raw outputs):
`.ufo/waves/round-38/falsify/F38MutC2Counter/00…05*.txt`.

## Method

Detector: `python3 <counter.py> --lane <clone>` — full 7-check output plus gate block, exit code. Mutants are
copies in scratch (`$S/mut/`), never in-tree edits; the lane tree bytes stay pristine except during a fixture,
then are restored from byte-verified backups and re-hashed. Kill standard (C1-style, attributable): a mutant is
KILLED iff on some input tree its verdict differs from the expected verdict in the dangerous direction — expected
`fail`, mutant says `pass` (false-green hole), or expected `pass` (honest tree), mutant says `fail` (false-red that
blocks any real admission). A baseline failure would be inconclusive; baseline passed.

**Baseline (pristine on landing clone): `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0** — receipt
`00-baseline-pristine.txt`. Matches `measure-final.txt`.

## Mutants (diff points in `plans/round38_c2_verify.py`)

| id | clause | weakening | honest tree | committed controls | fixture | verdict |
|---|---|---|---|---|---|---|
| M1 | V3 | anchor token may equal ANY row's spec pin | green | no kill (skip: correct anchors→ok both; nothing: rows absent→red both) | F3 swap S115↔S116 digests | **KILLED** (F3: pristine `defects=1`, M1 `defects=0` pass) |
| M1b | V3 (bonus, weaker) | anchor token may be any 64-hex | green | no kill | F1b garbage token | **KILLED** (F1b: M1b pass) — note F3 does NOT kill M1b (swap keeps hex-ness) |
| M2 | V4 | summary counts tolerate ±1 vs CASE lines | green | no kill | F4 summary 7/15→8/14 | **SURVIVED** — check-level flip only (V4 DEFECT→ok); predicate stays red via gate P10 |
| M3 | V7 | derive label from FIRST violating case only | **RED** (all 7 tags: "labelled partly, receipt derives enforced") | no kill (skip receipt's first violator also fails → ok both) | F7 map relabelled enforced×7 citing `empty-tree` | **KILLED** twice: false-red on honest tree; false-green on F7 (pristine fail, M3 pass) |
| M4 | V2 | drop `--rerun` (gate P10 skipped, cf. `pkg_gate.py` line 308) | green | **no kill** (skip co-fires P3/P4/P6/P8 → V2 red under mutant too; nothing: receipt absent) | F2 fabricated receipt (dry-derived, observed=predicted) | **KILLED** (F2: pristine `defects=1` = P10 only; M4 `checks=7 defects=0` pass) |
| M5 | V1 | ignore extra SHA256SUMS entries | green | no kill | F1 extra manifest line | **SURVIVED** — check-level flip only; predicate stays red via gate P5 (+P9 for real files) |

Killed 3/5 assigned (M1, M3, M4); bonus M1b 1/1. Survivors: M2, M5.

## Findings

1. **The committed controls kill NONE of the five counter mutants.** `control-c2-nothing.txt` fails V2/V3/V4/V7
   structurally (absent files/rows), so any of these weakenings stays red; `control-c2-skip.txt` co-fires
   receipt-independent gate defects (P3/P4/P6/P8) plus census V6, so dropping `--rerun` leaves V2 red
   (defects 5→4), and its anchors/receipt/map are correct-shape so V1/V3/V4/V7 are `ok` under pristine and mutant
   alike. The controls demonstrate that clauses fire; they cannot attribute a kill to any single clause.
2. **M4 (drop `--rerun`) is the sharpest survivor-shaped hole — and it is killable, but only by a fixture that
   did not exist at freeze.** F2 (landing tree + hand-typed dry-derived receipt, `observed=predicted`) shows:
   pristine's ONLY defect is P10 (`fresh probe output is not byte-equal to the receipt`); every other check —
   including V4 and V7 — is green on fabricated bytes. Under M4: `checks=7 defects=0`, `PREDICATE C2 pass`,
   exit 0, on evidence no run ever produced. This empirically confirms the claims file's design statement
   (round-38-claims.md: "V2's P10 fresh-run byte compare is what makes such a receipt red") and the N21-style
   lesson that a hand-typed receipt satisfies everything else.
3. **M2 (V4 off-by-one) and M5 (V1 ignore-extra) have NO killing input at predicate level — genuine survivors,
   coverage findings, not contract changes.** Both clauses are shielded by the gate's own redundancy: any receipt
   with a wrong summary differs from a fresh probe run → P10 → V2 red (M2); any extra manifest line is
   byte-checked by gate P5, and any real extra file is untracked → P9 (M5). V4's summary agreement and V1's
   extra clause are defense-in-depth: currently untestable at predicate level, and only load-bearing if the
   shielding gate clause (P10 / P5+P9) were itself weakened — e.g. M2 becomes load-bearing exactly when M4's
   weakening is applied. The C2 kill rule ("predicate not met → not admitted") is therefore NOT endangered by
   these two mutants on this tip; their risk is conditional on gate edits.
4. **M3 confirms the round-37 D2 fix is load-bearing and observable.** The first-violator weakening turns every
   tag's label into `enforced` (the first receipt line `empty-tree` violates all 7 tags and is observed fail), so
   the mutant is false-red on the honest tree — and F7 shows it admits a one-witness `enforced`×7 map against a
   receipt whose full violating sets derive `partly`×7. V7's all-cases derivation is the clause doing D2's work;
   no committed control exercises it (the skip control's fabricated receipt is derivation-consistent by
   construction).
5. **V3's own-row pin (round-37 routed D3) is the sole catcher of a cross-bound anchor**: neither the gate (P6
   `ok` on the swapped tree) nor the census (`ok`) re-derives the binding. The any-row weakening dies only to my
   F3 swap fixture; the even weaker any-hex weakening needs F1b's garbage token. Both are cheap fixtures the
   freeze did not include.

## Verdict accounting

Killed / assigned = **3/5** (M1, M3, M4). Survivors with no killing control or fixture: M2, M5 (both
predicate-equivalent on this tip due to gate P10 / P5+P9 shielding). Committed controls in
`.ufo/waves/round-38/claims/`: 0 kills across all five.

## Hygiene

No lane file, jj state, or Git index touched; no commits; mutants and fixtures confined to
`/fast/scratch/hyaku/kengaku-r38/F38MutC2Counter/` (TMPDIR redirected there); all four fixture files restored
byte-exact (receipt `05-restoration-and-final-state.txt`: paired sha256s, clean `git status --porcelain`, pristine
re-run green on the restored clone); scratch removed at finish. No tools installed (none needed).

VERDICT: c2-counter-mutants-3/5
