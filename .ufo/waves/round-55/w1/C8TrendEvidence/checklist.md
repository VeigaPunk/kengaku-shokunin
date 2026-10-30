# Round-55 trend-verdict evidence checklist

seat: C8TrendEvidence (critic, w1 v2 build+attack)
date: 2026-10-30
frozen claims: `plans/round-55-claims.md` @ `80afa613`; base tip `798f5e9e`
definitions: `/home/vgpnk/Projects/shokunin/LEARNING.md` "The three trends" table (verbatim criteria quoted below)
carried verdicts: `corpus/lessons/round-54-verifier-spotcheck.md` §5 — expansion `unchanged`, quality `harmed`, discernment `improved`

Purpose: for each trend, what an `improved` / `unchanged` / `harmed` verdict at round close
MUST be able to point at, in named artifacts, and the trap that would make the claimed
verdict dishonest. The verdict is only as honest as its weakest cited artifact.

State at write time: tip is still the freeze commit `80afa613`; every round-55 receipt and
content file exists only as working-tree/untracked bytes (probe receipts under
`.ufo/waves/round-55/w1/E6ChessReceipt/`, identity under `E14CaptureIdentity/`, selftests
under `E10NoharmRuns/`, lesson/knowledge/README/PROVINCE/SOURCES edits uncommitted). Nothing
below counts as landed until the L1 integrates and commits it.

---

## 1. Expansion

LEARNING.md observable: "admitted `knowledge/` entries on ground the coverage map did not
hold, each `source:` citing a `mined` `corpus/SOURCES.md` row (`own-work` rows included);
frontier areas entered; new kinds of source; a capability admitted to `SCORECARD.md`."
- `improved` = "net new admitted entries on uncovered ground, each citing its coverage-map row"
- `harmed` = "an admitted entry fails the bar it was admitted under"

The only candidate ground this round is R55-C3's chess-best-move grader (13th TB2 grader,
coverage map "12 of 89 read" → "13 of 89"). R55-C1/R55-C2 are repair claims on ground
already held — they cannot produce expansion.

### `improved` requires (all conjuncts)
1. `corpus/knowledge/tb2-chess-best-move-grader.md` committed at the landing revision,
   opening with `source:` citing S201 **and** S202 with status `mined` — the coverage-map
   row citation LEARNING.md requires. Check: entry front matter + `corpus/SOURCES.md`
   rows S201/S202 `used-by` = the entry.
2. S201 (grader, code A) and S202 (instruction, docs A) land as `mined`, opened 2026-10-30,
   well-formed: `scripts/sources-census.sh validate` exit 0, `malformed=0`, and no NEW
   warnings beyond the 15 pre-existing W04s
   (`.ufo/waves/round-55/w1/E8SourcesRows/census-after-rows.txt` currently shows exactly
   those 15; carrier at landing: census validate re-run receipt).
3. Probe receipt committed: `corpus/evidence/round55/chess-best-move-probe.txt` with
   `cases=12 observed_pass=5 observed_fail=7 mismatches=0` — currently produced in-seat by
   `E6ChessReceipt/run1.txt` with `run2.txt`/`cmp.txt` reproducing it (cmp exit=0).
4. Coverage-map narrowing committed: `PROVINCE.md` round-55 paragraph "12 of 89 read" →
   "13 of 89"; `corpus/README.md` gains the entry/evidence index rows + Frontier narrowing
   note (both edits present uncommitted in the working tree).
5. All three C3 kill legs clear at the measured-after revision:
   (a) every observed≠predicted case counted as a mismatch — each receipt case line carries
   `predicted=` and `observed=` (run1.txt does);
   (b) oracle derived only from the captured grader's own assertions — carrier: the frozen
   case table inside `plans/round55_c3_chess_probe.py` (12 cases, predictions pre-written);
   (c) upstream identity: `E14CaptureIdentity/identity.txt` shows in-repo sha256
   `a540714e…` == upstream at pin `2fd12b88…` for `tests/test_outputs.py` (also the
   `test.sh` / S109 dedup `4770437e…`). Must be re-derived at landing, not seat-asserted.
6. QUALITY gate: entry admitted under Q1–Q17 **with the Q13/Q14 second-seat re-read on
   record** (frozen R55-C3 after-condition). Carrier: the re-read receipt in
   `.ufo/waves/round-55/w1/` + the lesson Gate note.
7. NO capability row for C3 (r52 ruling: an instrument probe is not a capability). Check:
   `SCORECARD.md` diff shows no capability added.

### `unchanged` requires
Any of: a kill leg fires and the claim is not admitted → ground not entered; or the entry
lands but without the mined-row `source:` citations; or the entry collapses to r54-style
"bounded sourced interpretation" (r54 §5 correctly refused expansion credit for
`external-anchor-freeze.md` on already-worked ground — the same rule binds here if the
probe is invalidated). Carrier: the round-55 verdict text recording the non-counting
reason; do not let `unchanged` mean "nobody wrote the verdict down".

### `harmed` requires
The entry is admitted and then fails the bar it was admitted under — e.g. its semantic
claims (full-multiset equality over whitespace-split tokens; duplicates break equality;
no case/digit normalization; the instruction's own `h1h8` example fails) not derivable
from the captured bytes at the pin — and the failure is left unmarked (no rejection
logged, no QUALITY note). Carrier: an attack receipt showing entry claim vs grader
assertion text diverging, still unmarked at close.

### Traps that make `improved` dishonest
- **T1 oracle contamination (retrospective prediction).** `mismatches=0` proves nothing if
  the predictions were written after observing grader behaviour. The receipt cannot
  self-certify pre-registration; the honesty carriers are (i) the frozen case table in
  `plans/round55_c3_chess_probe.py` committed BEFORE the first executed run
  (`E6ChessReceipt/run1.txt`), and (ii) `claims/c3-before.txt` proving the receipt absent
  at base. A case table edited post-run makes `mismatches=0` vacuous — fake ground.
- **T2 score-number substitution (false provenance).** Coverage stays L0-capped at 7
  (open `kengaku | round-25/33/51`); the claim's predicate is its counter, never the
  score. Writing expansion `improved` because "13th grader" moved a number is the trap
  r54 avoided by verdict, not luck.
- **T3 capability inflation.** Counting the probe run as a capability row would
  double-count an instrument as frontier admission; R55-C3 explicitly claims none.
- **T4 uncited ground.** Entry `source:` not citing S201/S202 as `mined` (rows land
  `queued`, or `used-by` points elsewhere) — LEARNING.md requires the mined-row citation;
  without it the entry is ungrounded even if every word is true.
- **T5 identity slip.** Counting expansion while byte-identity is only seat-level
  (`E14CaptureIdentity`) and never re-derived at the measured-after revision; kill leg
  (c) is evaluated at landing.
- **T6 the r54 relapse.** If any kill leg later fires, the entry collapses to
  interpretation of a failed instrument; r54 §5's precedent says that is not expansion.
  Verdict text must say the ground entered ONLY while legs (a)(b)(c) are all green.

---

## 2. Quality

LEARNING.md observable: "entries re-verified, deepened, or superseded by stronger ones;
`verified-at` freshness."
- `improved` = "a weaker entry is superseded by a stronger one, or stale entries
  re-verify, with no admitted entry failing its re-check"
- `harmed` = "an entry is found false or stale and left unmarked"

r54 carried `harmed` (registry regression 9→8, real and retained). Round-55 surface: the
C1 registry repair + frozen leg 2, the C2 ledger truth corrections, the chess entry's bar,
and the r54-routed obligations (r52-repair carried defect stays open until fixed, r54 §6.5).

### `improved` requires (all conjuncts)
1. **Frozen leg 2 executed in full.** Every round-55-added registry row in `SKILL.md`
   §Gate/probe registry — `round54-c1`, `round54-c2`, `round55-c2`,
   `round55-c2-controls`, `round55-c3` — names a self-test; each self-test executed ONCE
   from a clean clone at the landing revision; observed verdict == the row's verdict-map
   cell. Carrier: one receipt per row under `.ufo/waves/round-55/integrate/`. Seat-level
   pre-evidence exists (`E10NoharmRuns/{r52-c2-registry,r54-c2-entrytruth,r55-c2-controls}-selftest.txt`)
   but the canonical leg is the integrate set — all five rows, no subset.
2. R52-C2 closure counter green at the measured-after revision over the FULL advertised
   set (includes `plans/round55_c2_entryargv.py`, `round55_c2_controls.py`,
   `round55_c3_chess_probe.py`): `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
   `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R52-C2 pass`, exit 0.
   Carrier: the after-run receipt under `integrate/` (before: `claims/c1-before.txt`,
   `MISSING 2`).
3. Ledger truth corrections as data BEFORE the after-run: (a) `round35-c1-coverage`'s
   declared evidence fragment re-derived from the entry's actual output at the landing
   revision, corrected with the observed output committed; (b) `round52-c2` stays declared
   green because the repair restores its true exit 0; (c) ledger rows added for the five
   round-55 registry rows so ledger set == registry set, each declared from measured true
   behavior. Carrier: `plans/round54-entrytruth.json` diff + amended rows' evidence text;
   verifier: the after-run prints `mismatched=0 evidence_missing=0 laundered=0` and
   `TIPSTATE` declared green/red == observed green/red.
4. No admitted entry fails its re-check: census validate passes with no new warning class;
   the chess entry's claims re-derivable from the captured bytes (its receipt's
   `instruction-example-h1h8 predicted=F observed=F rc=1` line is the carrying evidence
   for the entry's h1h8 claim).
5. The r54-marked false/stale things are closed or re-marked: the registry regression
   closes via (2); the r52-repair carried defect (order-check regression + masked K7
   control — reconstructed as evidence this round by R11/RV3, production r52 counter
   unchanged by rule) must leave the entries asserting r52-repair soundness marked/staled,
   not silently trusted.

### `unchanged` requires
Registry rows added and true, operability restored (axis move 8→9), ledger corrected — but
no entry superseded and no stale entry re-verified. This is the honest default: repairing
r54's harm returns quality to baseline; repair alone is not an upward move. Carrier: the
improved-list receipts present, nothing more; the verdict text must say exactly "repair,
no upward content event".

### `harmed` requires
Any of: a round-55-added registry row's verdict-map cell is false at landing (R55-C1 kill
rule fires — the cell sat uncaught by the lane); the `round35-c1-coverage` fragment
re-derived incorrectly or edited by hand to match the declaration; the after-run shows
`laundered>0` / `mismatched>0` / `evidence_missing>0` and is waived; the chess entry is
admitted then found to fail Q1–Q17 with no rejection logged; a new census warning class is
introduced and ignored; the r52-repair defect is demonstrated and the asserting entries
stay unmarked.

### Traps that make `improved` dishonest
- **T1 the named trap: repair called "quality improved" while a new false cell sits
  uncaught.** The repair's soundness IS frozen leg 2. If any of the five integrate
  spot-leg receipts is missing or shows observed ≠ cell, the lane traded a known
  regression for an unknown one. `improved` requires the full five-row receipt set; a
  predicate line alone supports at most `unchanged`. (And per the C1 kill rule, a
  demonstrated false cell means operability holds at 8 AND the claim is not admitted —
  two axes, one lie.)
- **T2 axis/trend laundering.** The C1 repair is an operability axis move (8→9).
  Presenting the axis restoration as a quality-trend improvement double-counts one green
  gate. `quality: improved` needs a corpus-content event — supersession or re-verification
  with evidence — not a counter turning green.
- **T3 correction without evidence.** The `round35-c1-coverage` fragment "corrected" to
  match its declaration instead of re-derived from observed output is a false correction —
  worse than the stale declaration. The claims require the observed output committed
  alongside; a correction whose evidence is missing fails exactly like the r54
  `evidence_missing=1` it repairs.
- **T4 defect demonstrated, entries unmarked.** R11/RV3 reconstruct the r52-repair
  defect; if entries asserting the r52 repair stay unmarked, LEARNING.md's harmed
  definition ("found false or stale and left unmarked") is met even while every counter
  prints green — the green counters and the harmed trend are compatible.
- **T5 supersession theater.** Crediting "weaker superseded by stronger" to the chess
  entry double-counts it: it is net-new ground (expansion), not a supersession (quality).
  One artifact, one trend.
- **T6 freshness theater.** A `verified-at` bump with no `recheck:` command or citation
  behind it (LEARNING.md: entries open with `recheck:` — the command that re-verifies) is
  unmarked staleness wearing a fresh date.

---

## 3. Discernment

LEARNING.md observable: "gate decisions vs the outside spot-check; `QUALITY.md` criteria."
- `improved` = "the spot-check agrees with the gate on admits *and* rejects, or a
  disagreement becomes a lesson that adds a grounded `QUALITY.md` criterion"
- `harmed` = "a disagreement is left unlearned, or a criterion is added with no lesson
  behind it"

r54 carried `improved` (non-author closure agreed on 2 admits + 1 reject; quotes verified
verbatim ≤25 words; census re-run). Round-55 gate decisions are recorded in
`corpus/lessons/round-55.md` §Gate: **admit S201**, **admit S202**, the **A1 dropped
runner row** (reject-as-duplicate: `test.sh` sha256 `4770437e…` == held S109), "Rejections
this round: none yet (the wave's distiller/critic output is pending)", and a pre-registered
spot-check sample: "admit S201, admit S202, the dropped runner row (reject-as-duplicate),
and the reject of 'full-multiset = new class' framing if C4 ruled it a re-label."

### `improved` requires (all conjuncts)
1. The round's gate decisions complete on record before close: S201/S202 admits with
   located quotes ≤25 words + tier rationale (present in the lesson §Gate), AND at least
   one genuine reject. If no organic reject lands (critic/distiller pending), the A1
   dropped runner row serves as the reject sample — recorded as what it is: a
   dedup-by-identity refusal, not a taste rejection. The lesson's "Rejections this round:
   none yet" line must not survive to close if discernment is to be judged.
2. The Q13/Q14 second-seat re-read on record for the chess entry (frozen R55-C3
   after-condition). Carrier: re-read receipt under `.ufo/waves/round-55/w1/` + lesson
   Gate note.
3. An OUTSIDE, non-author spot-check — LEARNING.md: "A subagent the lane dispatched is
   still the lane" — sampling ≥1 admit and ≥1 reject of THIS round's gate, with
   agree/disagree + reasons, recorded in the closure artifact. By r54 analogy the carrier
   is `corpus/lessons/round-55-verifier-spotcheck.md` §4-style, authored by the non-author
   integrator; the sample is already pre-registered in the lesson (S201, S202,
   dropped-runner, conditional C4 re-label ruling).
4. OR (the alternative improved path): a disagreement — e.g. C4 ruling the full-multiset
   framing a re-label of r45's line-split membership class — becomes a lesson adding a
   grounded `corpus/QUALITY.md` criterion citing `corpus/lessons/round-55.md`. Both halves
   must exist: lesson row AND criterion row.

### `unchanged` requires
Gate admits land, entry clears Q1–Q17, but the outside spot-check is recorded as
pending/not done this round (r54's closure had to complete the check the lane left open —
the same may happen here), and no disagreement produces a criterion. Honest `unchanged`
says: the gate ran, nobody outside re-judged it.

### `harmed` requires
Any of: a disagreement (a critic disputes S201/S202's tier, or C4's re-label ruling)
left unlearned — no lesson row, no criterion; a `QUALITY.md` criterion added this round
with no lesson behind it (LEARNING.md's exact harmed definition); the second-seat re-read
flags a defect and the entry is admitted anyway; the spot-check samples admits only.

### Traps that make `improved` dishonest
- **T1 self-attestation.** A wave seat re-checking the gate and declaring agreement is the
  lane grading its own homework. r54's carrier was the non-author integrator's spotcheck
  file; r55's must be authored outside the wave too. A dispatched subagent's agreement
  does not satisfy the observable.
- **T2 admits-only sampling.** The observable requires agreement on admits AND rejects.
  Re-opening the two pinned URLs, verifying the quotes, and declaring agreement — without
  sampling the dropped-runner reject (or an organic reject) — has not run the observable.
  r54 sampled 2 admits + 1 reject; r55 must sample at least 1 + 1.
- **T3 manufactured reject.** Recording the A1 amendment as a gate "reject" to complete
  the sample without it being a considered candidate inflates the sample. It is a
  legitimate dedup refusal ONLY with its sha256-identical-to-S109 reason recorded in the
  Gate; a freeze amendment dressed as a discernment decision is cosmetic.
- **T4 criterion/lesson divorce.** A `QUALITY.md` row citing no lesson is the harmed
  case; a §Mistakes row with no criterion follow-up when no existing criterion caught it
  violates the corpus contract (LEARNING.md §3: "when no criterion caught it, a
  `QUALITY.md` criterion citing that lesson"). The pair must land together.
- **T5 quote drift.** The located quotes must be verbatim ≤25 words at the pinned URLs —
  r54's spotcheck verified each verbatim before agreeing. If S201's quote
  (`assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`) or S202's
  (`If there are multiple winning moves, print them all, one per line.`) drifts from the
  pinned bytes, agreement-with-gate is unverifiable — sampling decisions whose quotes were
  never re-derived is ceremonial.
- **T6 pending-marker freeze.** The lesson's "Admit/reject spot-check … pending the
  non-author closure" line is a statement of intent, not the check. Closing the round
  with the pending line intact while claiming discernment improved reports a todo as a
  result.

---

## Cross-trend honesty rule

LEARNING.md: "Growth without quality is not learning: `expansion: improved` with
`quality: harmed` is a trade, reported as a trade, never admitted." The plausible r55
trade shape: expansion `improved` (13th grader entered) alongside quality `harmed` (a
false registry cell uncaught, or the r52-repair defect reconstructed while asserting
entries stay unmarked). If both fire, the verdict block must print both verdicts and the
trade — averaging them into a net "learning happened" is itself the dishonesty the r54
§5 precedent exists to prevent.

## Carrier-artifact index (all paths lane-relative)

| claim leg | artifact |
|---|---|
| C1 before | `.ufo/waves/round-55/claims/c1-before.txt` (MISSING 2) |
| C1 after / closure counter | after-run receipt under `.ufo/waves/round-55/integrate/` (r54 analogy: `integrate/c1-after.txt`) |
| C1 frozen leg 2 (five registry rows) | one receipt per row under `.ufo/waves/round-55/integrate/`; registry table `SKILL.md` §Gate/probe registry |
| C2 before (laundering fixtures) | `.ufo/waves/round-55/claims/c2-before-{abbreviated-selftest,uv-decoy-script}.txt` |
| C2 fixture kills | `.ufo/waves/round-55/integrate/c2-fixture-kills.txt` |
| C2 after | after-run receipt under `.ufo/waves/round-55/integrate/` (`PREDICATE R55-C2 pass`, `laundered=0 evidence_missing=0 mismatched=0`) |
| C2 ledger corrections | `plans/round54-entrytruth.json` diff + committed observed outputs |
| C3 before | `.ufo/waves/round-55/claims/c3-before.txt` |
| C3 probe receipt | `corpus/evidence/round55/chess-best-move-probe.txt` (seat copies: `.ufo/waves/round-55/w1/E6ChessReceipt/run{1,2}.txt`, `cmp.txt`) |
| C3 oracle pre-registration | frozen case table in `plans/round55_c3_chess_probe.py` (committed before first run) |
| C3 upstream identity | `.ufo/waves/round-55/w1/E14CaptureIdentity/identity.txt` (sha256 `a540714e…` at pin `2fd12b88…`) |
| C3 knowledge entry | `corpus/knowledge/tb2-chess-best-move-grader.md` + Q13/Q14 second-seat re-read receipt |
| C3 sources rows | `corpus/SOURCES.md` S201, S202 (`mined`, 2026-10-30); census validate receipt |
| C3 coverage-map narrowing | `PROVINCE.md` ("13 of 89"), `corpus/README.md` index rows + Frontier note |
| gate decisions | `corpus/lessons/round-55.md` §Gate |
| outside spot-check | `corpus/lessons/round-55-verifier-spotcheck.md` (pending; non-author integrator) |
| trade rule | verdict block must report `expansion × quality` trade explicitly |
