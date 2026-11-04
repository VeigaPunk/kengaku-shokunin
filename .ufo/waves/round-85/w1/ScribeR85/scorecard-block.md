## Round 85 (hyaku run 15, attempt 1, 2026-11-04): third located offline replay (first `serialization-schema` member) and the eight routed round-84 defects

Base `0de45354d7aff18e4a23a348ec13de3a1f707a44`; freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`; instruments and
repairs `99a7cb3b0165efe907814947392e6bd98fe45872`; receipt and executed ledger row `ce5b9ef8d7496a0e3e53ebb70c9a168e5511d425`.
Two causally separable claims on two distinct axes; no frozen sentence, case table, defect list, control set or kill rule
changed after the freeze.

| claim / axis | before → after and measured commit | counting command | verdict / score |
|---|---|---|---|
| R85-C1 / **coverage** (lowest non-retired axis, held at its L0 cap): first located offline replay of `sqlite-db-truncate`, the first member of the `serialization-schema` class | BASE `0de45354`: `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=8`, `PREDICATE R85-C1 fail`, exit 1. At `<L1 fills: measured commit>`: `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`, `PREDICATE R85-C1 pass`, exit 0. Ledger executed 28 → 29, unexecuted 60 → 59; `serialization-schema` 1 of 10 → 2 of 10, `file-artifact` 20 of 76 → 21 of 76. | `<L1 fills: counting command>` | **executable green, not admitted.** The eight frozen vectors reproduce with zero mismatches and the REPRODUCE leg re-runs the pinned probe; the frozen predicate's before-state is only reachable after the per-path archive repair (`e7b44805`), and the C1 mutant battery is red at the tip (`necessary=4 redundant=1`, exit 1) on a stale `flip_ledger()` verdict literal. Coverage stays at **7** — the L0 cap, not this round, holds it. |
| R85-C2 / **calibration** (held at ceiling): the eight owner-routed round-84 defects (V1, V2, V3, V5, V6, V7, V8, V9) discharged with a base-sensitive gate | BASE `0de45354`: `TARGET ids=8 closed=0 checks_passed=0 indexed=no defects=8`, `PREDICATE R85-C2 fail`, exit 1; `SENSITIVITY n=8 failed_at_base=8`. At `<L1 fills: measured commit>`: `TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0`, `PREDICATE R85-C2 pass`, exit 0; `SENSITIVITY n=8 failed_at_base=8`. R84-V4 stays operator-owned and prints `ROUTED`, never counted. | `<L1 fills: counting command>` | **executable green, not admitted.** V8's gate check was replaced by a byte-level flag test and V3 gained a code-only path after the first green, and reverting C1's receipt and ledger row leaves C2 at 7 of 8 — so the frozen predicate's "repair substantively in the measured tree" and the causal-separation property are not established by the executable green. Calibration remains **10 held**, not raised: repairs of routed defects restore, they do not extend the ceiling. |

**Measured at this seat (ScribeR85, tip `20eb9ba796324070440c95855e70755f61d059e1`, after the L1's honest-stop landing).**
Counting commands actually run, for the L1 to fill into the table above:
`python3 plans/round85_c1_replay.py --lane . --rev master --work DIR` → `PREDICATE R85-C1 pass`, exit 0;
`python3 plans/round85_c1_replay.py --lane . --rev 0de45354d7aff18e4a23a348ec13de3a1f707a44 --work DIR` → exit 1,
`defects=8`; `python3 plans/round85_c1_replay.py --lane . --mutants --work DIR` → `MUTANTS real=5 necessary=4
redundant=1`, exit 1 (**red**); `python3 plans/round85_c2_debt.py --lane . --rev master --work DIR` → exit 0;
`python3 plans/round85_c2_debt.py --lane . --rev 0de45354d7aff18e4a23a348ec13de3a1f707a44 --work DIR` → exit 1,
`defects=8`; `python3 plans/round85_c2_debt.py --lane . --sensitivity --work DIR` → `SENSITIVITY n=8 failed_at_base=8`,
exit 0. Controls, each `target_reached=False`: do-nothing (`defects=8`), ledger-only
(`LEDGER-VERDICT,RECEIPT-MISSING`), fabricated-observations (`VECTOR-MISMATCH,REPRODUCE-MISMATCH`), forged-receipt
(`REPRODUCE-MISMATCH`). C1 selftest `cases=10 red=10 failures=0`; C2 selftest `cases=6 red=6 failures=0`, C2 mutants
`real=3 necessary=3`, and `--control-presence` rejects the presence-only Q61 fixture. Standing gates at the tip: R79
population `DEFECTS n=0` pass; R75 index parity `knowledge 77/77, lessons 143/143, evidence 76/76` pass; R82 plans
registry `DEFECTS n=0` pass; R74 registry `MISSING 0` pass; defect ledger `mismatches=0` pass; sources census exit 0.
**Carried red, not caused by this round:** `plans/state_check.py --summary` reports `MISMATCH P3c.box.4.pointer.1`,
identically at BASE `0de45354`.

**A committed transcript does not reproduce.** `.ufo/waves/round-85/L1/c1-mutants.txt` and the mutants block of
`c1-battery.txt` (both committed at `20eb9ba7`) record `MUTANTS real=5 necessary=5 redundant=0` with `rc=0`, which is
what the battery printed *before* `35b1e4e0` changed the expected ledger verdict to `cases` while `flip_ledger()` still
writes `predicate`. At the tip the same command prints `necessary=4 redundant=1` and exits 1 — the figure the lane's own
clone transcript `q20-clone.txt` records. The committed `c1-controls.txt` is stale in the same way (BASE and do-nothing
printed as `DEFECT SETUP archive-failed` `rc=2`, the pre-`e7b44805` counter; `ledger-only` printed one defect code where
the tip prints two). The SCORECARD row above should carry the tip-measured numbers, and the transcripts should be
re-run at the tip rather than cited from the earlier revision.

**Other axis scores (held, no change):** novelty **8**, depth **10**, operability **10**, freshness **10**, adjacency **9**
— the round re-uses the round-83 replay method on a third member, admits no new knowledge entry, and claims no serving-
plane, route, image or model surface. No axis score moves; coverage stays 7 under its open L0 cap and calibration stays 10
under its ceiling.

**Sources.** S272 admitted (member replay only), annotation corrected by the append-only S273 supersede row: rows 263 → 265,
A 233 → 235, B 24, C 6, mined 239 → 241, rejected 16, queued 8; census exit 0, W04 30 → 30. `expansion: unchanged` (the
round-84 grade is corrected in `corpus/lessons/round-84.md` under R84-V7). Assimilation: none — `merge/kengaku/` stays
blocked by L0 `kengaku | round-54`.

### Round85 capabilities

No new capability row: the round re-uses the round-83 replay method on a third member and adds a threshold-count
vocabulary to the existing replay instrument, which is depth/operability of the same method, not a new one.

### Planned (round 86)

Not a claim until frozen.

1. Coverage: freeze a member whose grader needs a non-Python runtime *and* prove the blocker from its bytes before
   choosing it (the `Rscript` finding is the model), or replay a second `serialization-schema` member with a
   schema-drift case class instead of a threshold-count one — and price the downstream verdict vocabulary **before**
   minting the receipt, which is the round-84 debt this round repeated.
2. Calibration: re-pin the frozen `P3c.box.4.pointer.1` assertion with re-derived tokens (the only standing red gate),
   and build the standing TB2 admission counter that Q61's limits section names as open.
3. Backlog: `merge/kengaku/` mass id drift (L0 `kengaku | round-54`), the Q13 checker shape (L0 `kengaku | round-84`),
   the round-82 gate's worktree-revision blindness routed this round, and the correct-vector forged-receipt control the
   round-84 lesson names and this round's control set does not yet exercise.
