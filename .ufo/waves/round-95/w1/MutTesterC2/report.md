# MutTesterC2 — mutation test of the R95-C2 counter and census at T

Seat: MutTesterC2 (leaf, Kengaku round 95 wave 1). Target instruments at T
`afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`:
`plans/round95_c2_counter.py` sha256 `2fc2e7f0a1c26599…` and `plans/round95_false_gate_census.py`
sha256 `38fed2c23d46792e…`, both equal to the frozen-instruments table in
`plans/round-95-claims.md` (frozen at F `d9cd18a7519a58a1`). Mutant bytes, raw receipts and the
verdict ledger are in this directory (`mutants/`, `receipts/`, `manifest.json`,
`final_verdicts.json`). Nothing outside this wave dir and my scratch was written; the lane clone
stayed read-only (`meta.json`: porcelain empty, HEAD `afe9c229e37a` after the battery).

## Method

One `git clone --shared` of the lane into scratch, detached at T. Baseline: pristine census at T
(`B0-T`), byte-identical to the committed receipt `.ufo/waves/round-95/L1/c2-tip.txt` (only
difference: the receipt's wrapper `rc=0` footer line). Counter mutants are scored by the pristine
census with `--counter <mutant>`; a counter mutant **survives iff the census prints
`PREDICATE R95-C2 pass` and exits 0** (the item's criterion). Census mutants are scored by running
the mutated census at T with the counter read from git at T; kill channels checked in order:
census verdict at T, byte-diff vs the committed T receipt, and the two committed P2 control
receipts (`controls/c2-census-do-nothing-r94-counter.txt`,
`controls/c2-census-at-P1.txt`), each reproduced byte-exactly first (`XM1DN-pristine-BASECTRL`,
`XM3P1-pristine-BASECTRL`). Restoration leg: pristine census re-run after the whole battery
(`B0-END`) is byte-identical to `B0-T`.

27 single-site mutants (20 counter, 7 census), anchors asserted to occur exactly once
(`manifest.json`). Runs 6-wide; 33 census runs, wall 82 min (each census internally runs 15
counters 8-wide, so under my 6-wide battery each census took 8–19 min instead of the ~4 min solo;
the two corrected T runs below took 192 s / 219 s at 2-wide).

**Harness correction (disclosed).** `battery.py build_jobs` leaked the extra run's
`rev/counter` into XM1's and XM3's "at T" jobs, so their first receipts are actually P1 runs. The
P1 receipts are kept as kill evidence (`XM1-designated-forced.out` = the do-nothing reproduction;
`XM3-honest-dropped.out` = the at-P1 reproduction); the corrected T runs are
`XM1-designated-forced-T.*` and `XM3-honest-dropped-T.*`, and `final_verdicts.json` is built from
those. My first in-flight verdict table was wrong; every verdict below rests on the corrected
receipts.

## Counter mutants — 14 survived, 6 killed

Census at T with `--counter mutants/<id>.py`. `Δ` = differing lines vs `B0-T` (COUNTER line
excluded). Survivor = `PREDICATE R95-C2 pass`, rc 0.

| id | single-site change | verdict | Δ | kill channel / equivalence |
|---|---|---|---|---|
| CM01-w5-target-ignored | `w5 = w5 and hit` → `and True` | **survived** | 0 | byte-identical: `hit` is still computed and printed (`W5 … killed=10`), only its gating removed; honest W5 passes at T, forged rows fail at their designated legs, so nothing observable changes |
| CM02-w1-leg-dropped | `legs["W1"] = w1a and w1b` → `True` | **survived** | 0 | byte-identical: W1 checks still evaluated and echoed (`W1 pass`), not gating; honest passes W1, forged rows fail elsewhere |
| CM03-w4-leg-dropped | `legs["W4"] = …` → `True` | **survived** | 0 | byte-identical: same pattern for W4 |
| CM04-w3-ok-le-15 | W3 `int(st[0][1]) < 15` → `<= 15` | **survived** | 0 | byte-identical: every driven probe at T prints ok<15 (battery genuinely red), so `<` vs `<=` never decides; a future green-but-exiting-1 probe would be accepted as red |
| CM05-predok-multiplicity | pred_ok `len(lines) == 1` → `>= 1` | **survived** | 0 | equivalence: no measured gate run prints ≥2 PREDICATE lines |
| CM06-drop-w2-unrelated | `w2-unrelated` tuple deleted | **survived** | 1 | census passes; the one differing line is `HONEST W2 pass fixtures=19 ok=19` vs committed `fixtures=20 ok=20` — a field nothing asserts (see MUTC2-2/6) |
| CM07-cne-summary-ignored | CNE spec `ok = rc == 2 and s is None` → `rc == 2` | **survived** | 0 | equivalence: no measured rc-2 run emits a FREEZE-INTEGRITY summary line |
| CM08-predok-always-true | pred_ok body → `return True` | killed (rc 1) | 3 | M15-predicate-always-pass loses its designated `W2:w2-edited` red → `designated_red=13` |
| CM09-w2-always-ok | `results[name] = (ok, …)` → `(True, …)` | killed (rc 1) | 15 | all W2 designated reds gone (`designated_red=4`) **and** honest fails (W5's red detection blinded too) |
| CM10-w2-edited-want-rc0 | `w2-edited` want_rc 1 → 0 | killed (rc 1) | 6 | honest gate run fails W2 (polarity flip visible to the honest leg) |
| CM11-minself-8-to-99 | `MIN_SELF_INSTRUMENTS = 8` → `99` | killed (rc 1) | 5 | honest W4 fails (11 instruments < 99) |
| CM12-w2-intact-want-rc1 | `w2-intact` want_rc 0 → 1 | killed (rc 1) | 6 | honest gate run fails W2 |
| CM13-w3-rc-dropped | W3 probe `ok` drops `rc == 1` | **survived** | 0 | equivalence: every measured red probe run has rc==1 (battery failure forces exit 1), so the rc clause never decides |
| CM14-w3-pred-any | W3 probe predicate `== ["fail"]` → `>= 1` | **survived** | 0 | M15's probes (red battery, rc 1, predicate pass) are rescued at its W3 leg, but M15 still fails W1 and W2:w2-edited, so its census row is unchanged; no W3-designated row (X1/M07/M19/M20) is rescued |
| CM15-w3-pred-dropped | W3 probe `ok` drops the predicate clause | **survived** | 0 | same rescue analysis as CM14 |
| CM16-fx-refresh-dropped | `if d.exists(): rmtree` → `if False:` | **survived** | 0 | equivalence: fixture dirs never pre-exist in fresh work dirs |
| CM17-w1b-intact-only | `s_b == (9, 9, 0)` → `s_b[1] == 9` | **survived** | 0 | equivalence: intact/broken counts of the W1b summary unchecked; every measured run is (9,9,0) |
| CM18-w2-summary-optional | W2 `s == want_s` → `(s is None or s == want_s)` | **survived** | 0 | equivalence: no measured non-CNE run has `s is None` |
| CM19-w4-broken-ignored | W4 `s[2] == 0` → `True` | **survived** | 0 | equivalence: honest W4 has broken=0 and each forged gate's W4 also 0 at T |
| CM20-drop-w2-second-block | `w2-second-block` tuple deleted | killed (rc 1) | 6 | honest run fails **W5**: counter mutant `K6-second-block-ignored` designates `w2-second-block`, so the honest leg transitively guards every W5 target fixture even though the census DESIGNATED map does not name it (pre-registered as a predicted survivor — wrong; recorded as observed) |

Kill channels exercised: designated-red loss (CM08, CM09), honest-leg failure (CM09–CM12, CM20).
All six kills and all fourteen survivals are in `receipts/<id>.{out,txt}`.

## Census mutants — 1 killed at T, 1 killed by the committed T receipt, 2 killed by committed P2 controls, 3 equivalence survivors

Mutated census run at T with the pristine counter (default, read from git at T).

| id | single-site change | census verdict at T | Δ vs B0-T | verdict across all committed evidence |
|---|---|---|---|---|
| XM1-designated-forced | `dred = int(designated_red(…))` → `dred = 1` | pass, rc 0 | 0 (byte-identical, `XM1-designated-forced-T.out`) | **survives T and the frozen predicate**; killed only by the committed do-nothing control: mutant at P1/r94-counter prints `FALSEGATES … designated_red=14` where `c2-census-do-nothing-r94-counter.txt` records `designated_red=0` (`XM1-designated-forced.out`) |
| XM2-passes-polarity | `passes = int(rc == 0 and …)` → `int(rc != 0 or …)` | fail, rc 1 | 16 | **killed at T** (passing=14) — validation |
| XM3-honest-dropped | `ok = passing == 0 and red == TOTAL and honest == "pass"` → drops `honest == "pass"` | pass, rc 0 | 0 (byte-identical, `XM3-honest-dropped-T.out`) | **survives T and the frozen predicate**; killed only by the committed at-P1 control: mutant prints `PREDICATE R95-C2 pass` rc 0 at P1 where `c2-census-at-P1.txt` records fail rc 1 (`XM3-honest-dropped.out`) |
| XM4-sha-dropped | row sha clause → `False` | pass, rc 0 | 0 | **equivalence survivor**: no committed control feeds a row file whose bytes mismatch its tsv sha256 |
| XM5-total-weakened | population `len(rows) != TOTAL` → `> TOTAL` | pass, rc 0 | 0 | **equivalence survivor**: under-population exercised by no committed control |
| XM6-echo-dropped | HONEST echo regex → never matches | pass, rc 0 | −7 lines | census verdict survives, **killed by the committed T receipt byte-diff**: the 7 `HONEST …` echo lines are missing from `c2-tip.txt`'s content; the frozen predicate itself does not mention them |
| XM7-passline-any | PASS_LINE `…-C2 pass$` → `…-C2` | pass, rc 0 | 0 | **equivalence survivor**: the forged rows are excluded by the rc==0 requirement alone; PASS_LINE polarity never decides any committed run |

## Findings (routed to round 96 per the frozen rule; nothing repaired here)

1. **MUTC2-1 (major) — most of the counter's judgeable surface has no negative control at T.**
   Thirteen of twenty counter mutants produce byte-identical census output at T and are killed by
   no committed control: removal of the W1, W4 or W5 verdict gating (CM01–03), relaxation of
   pred_ok multiplicity (CM05), of the CNE summary strictness (CM07), of the W3 probe acceptance
   (`<= 15` CM04 — the item's example —, rc-drop CM13, predicate-clause drop CM14/15), of the W1b
   summary tuple (CM17), of W4 `broken == 0` (CM19), and of the fixture-refresh step (CM16). Each
   has an equivalence argument above: the violated clause is never the discriminator on the honest
   gate, the 14 forged gates, or any inner fixture/mutant battery. Practical meaning: a future
   counter could silently stop gating W1/W4/W5 or stop requiring a genuinely red probe battery,
   and the census, the frozen predicate, and every committed receipt would still say pass.
2. **MUTC2-2 (minor) — four W2 fixtures are removable undetected.** Fixtures outside
   (census DESIGNATED ∪ counter-W5 targets) — the class of `w2-intact`, `w2-unrelated`,
   `w2-edit-revert`, `w2-lying-table` — are dead weight for detection; CM06 executed the class on
   `w2-unrelated` (survived; only the unasserted `fixtures=19` echo differs). Note the converse
   held beyond pre-registration: `w2-second-block` is census-undesignated but W5-load-bearing, and
   its removal was killed (CM20) — the honest W5 leg transitively guards exactly the W5 targets.
3. **MUTC2-3 (major) — `designated_red` is fabricated, not measured, at T.** Forcing `dred = 1`
   is byte-invisible at T because every row genuinely fails at its designated leg; the frozen
   predicate (`designated_red=14`) is an output value the mutant census still prints. The only
   committed artifact that kills it is the P2 do-nothing receipt. If that control is not re-run in
   a later round, the census cannot detect loss of the designated-leg mechanism — i.e. a row
   failing for the *wrong reason* would still count as discriminated.
4. **MUTC2-4 (major) — the census's honest-pass clause is dead code at T.** XM3 is
   byte-identical at T and satisfies the frozen predicate; only the at-P1 control receipt (honest
   fails there because the claims file does not exist yet) exposes it. The 14→0 discrimination
   result does not logically require the honest gate to pass under this `ok` computation.
5. **MUTC2-5 (minor) — census input-integrity clauses are unobserved.** Row-file sha check (XM4),
   population `!=` check (XM5), and PASS_LINE polarity (XM7) are equivalence survivors against
   every committed run; no control tampers a row file, under-populates the tsv, or prints a
   non-pass predicate at rc 0.
6. **MUTC2-6 (info) — receipt-only fields are recorded but asserted nowhere.** The 7 `HONEST …`
   echo lines, `fixtures=20 ok=20` and `killed=10` appear in the committed receipts but in neither
   the census's `ok` computation nor the frozen predicate. XM6 and CM06 contradict the committed
   receipt byte-wise while satisfying the predicate verbatim. Whether that counts as a kill
   depends on reading the frozen predicate as the complete contract; recorded here so the round
   can decide.
7. **MUTC2-7 (info) — the measured channels are genuinely sensitive.** 6/20 counter mutants
   killed (designated-red and honest channels), census passes-polarity killed at T (XM2),
   echo-removal caught by receipt diff (XM6), designated-fabrication and honest-clause removal
   caught by the P2 controls (XM1, XM3); baseline byte-reproduces all three committed receipts;
   restoration run byte-identical; lane clean at T before and after.

No verdict of R95-C2 at T is flipped by any of these mutants — all survivors are coverage
findings about the instrument's sensitivity envelope, consistent with the claims' declared
in-sample scope.

## Record

- Tool installs: none (stock `git` + `python3` 3.14.8 only; no pacman use, per the host-wide pause).
- Scratch `/fast/scratch/hyaku/kengaku-r95/MutTesterC2` removed after this report was written;
  all citable evidence lives in this wave dir.
