## Round 85 (hyaku run 15, attempt 1, 2026-11-04)

Lowest non-retired axis: **coverage 7** (held at its L0 cap `kengaku | round-25/33/51`, which stays open, nothing assumed
answered). Tie-break: novelty is also 7, but novelty requires a new construct plus a prior-art verdict, and no
identity-verified model endpoint exists on this host; coverage is the axis whose move is measurable in-repo and
excluded from any waiver — **no stagnation waiver applies** (novelty has moved within the window, r83–r84). Base
`0de45354d7aff18e4a23a348ec13de3a1f707a44`; freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`; instruments and repairs
`99a7cb3b0165efe907814947392e6bd98fe45872`; receipt and executed ledger row `ce5b9ef8d7496a0e3e53ebb70c9a168e5511d425`.

- **R85-C1 (coverage) — third located offline replay, first `serialization-schema` member.** `sqlite-db-truncate`'s
  pinned grader (`8f5bc110…`) runs unmodified in bubblewrap over eight frozen `/app/recover.json` end states; two legs
  per case (set-intersection score, `score > 6` verdict). Tip `TARGET members=1 cases=8 legs=16 mismatches=0 located=1
  executed=1 defects=0`, `PREDICATE R85-C1 pass`, exit 0; BASE `defects=8`, `located=0 executed=0`,
  `PREDICATE R85-C1 fail`, exit 1. Ledger executed 28 → 29, unexecuted 60 → 59; `serialization-schema` 1 of 10 → 2 of 10,
  `file-artifact` 20 of 76 → 21 of 76 (SKILL cells updated). Controls: do-nothing, ledger-only, fabricated-observations
  and forged-receipt each `target_reached=False`; selftest 10/10. Receipt `corpus/evidence/round85/sqlite-db-truncate-probe.txt`
  (`WORKTREE clean`, `LANE_TIP dc02d818`, re-minted from a clean clone with the `tb2-header` subject line).
  **Correction (R85-F1):** the frozen claims' "`serialization-schema` 0 of 9 → 1 of 9" is wrong on both the numerator and
  the denominator — the class census has 10 members and `db-wal-recovery` was already executed at round 40, so the
  ledger's own numbers are 1 of 10 → 2 of 10; the frozen claim is not rewritten and no verdict depends on the figure.
  **Correction (S272 → S273):** the landed S272 anchor cites `:30` (a blank line) and `(6 whitespace-split words)`; the
  assertion is on line 31 and the quote is 9 words. The old row is preserved and the append-only S273 supersede carries
  the corrected annotation.
- **R85-C2 (calibration) — the eight owner-routed round-84 defects discharged.** Tip `TARGET ids=8 closed=8
  checks_passed=8 indexed=yes defects=0`, `PREDICATE R85-C2 pass`, exit 0; `SENSITIVITY n=8 failed_at_base=8`, exit 0;
  selftest 6/6; mutants 3/3 necessary; `--control-presence` rejects the presence-only Q61 fixture. R84-V4 is printed
  `ROUTED owner=operator` and is never counted. **Honest stop:** V8's gate check was replaced after the first green by a
  byte-level flag test (the registry gate reads working-copy bytes and is revision-blind), V3 gained a code-only path
  when no receipt exists to forge, and reverting C1's receipt and ledger row leaves C2 at 7 of 8 — so the frozen
  predicate's "repair substantively in the measured tree" and the causal separation between the two claims are not
  established by the executable green. Both claims stay unadmitted pending outside closure; the frozen doc is not edited.
- Gates at the tip: R79 population `replayed=29 unexecuted=59 DEFECTS n=0` PASS; R75 index parity `knowledge 77/77,
  lessons 143/143, evidence 76/76` PASS; R82 plans registry `DEFECTS n=0` PASS; R74 registry `MISSING 0` PASS; defect
  ledger `mismatches=0` PASS; `sources-census.sh validate` exit 0 before and after. **Carried red, not caused by this
  round:** `plans/state_check.py --summary` reports `MISMATCH P3c.box.4.pointer.1` (SHONEN box 4 pins
  `PROVINCE.md:129` = `### Adjacent`; that line is a table rule today, and the round-26 correction restates the frozen pin,
  which the post-fix checker refuses to launder). Red at BASE `0de45354` with the same tokens; not repaired here because
  the fix is a frozen-assertion re-pin, not a claim of this round. Carried to round 86.
- **Red at the tip, not repaired here:** the C1 mutant battery `python3 plans/round85_c1_replay.py --lane . --mutants
  --work DIR` prints `MUTANTS real=5 necessary=4 redundant=1` and exits 1 — `flip_ledger()` still writes
  `verdict="predicate"` while `check()` requires `"cases"` since `35b1e4e0`, so the `no-ledger` mutant cannot reach the
  target and the `ledger-only` control reports an extra `LEDGER-VERDICT` code. A scratch copy with only that literal
  changed restores `necessary=5 redundant=0`, exit 0. **The committed transcripts assert the opposite and do not
  reproduce:** `.ufo/waves/round-85/L1/c1-mutants.txt` and the mutants block of `c1-battery.txt` (both committed at
  `20eb9ba7`) record `necessary=5 redundant=0` `rc=0`, which is the pre-`35b1e4e0` figure; the same commands at the tip
  print `necessary=4 redundant=1` and exit 1, as the lane's own clone transcript `q20-clone.txt` records. The committed
  `c1-controls.txt` is stale in the same way (its BASE and do-nothing lines read `DEFECT SETUP archive-failed` `rc=2`,
  the pre-`e7b44805` counter). Transcripts should be re-run at the tip rather than cited from an earlier revision.
- Census: `scripts/sources-census.sh validate --root … kengaku` exit 0 before and after; rows 263 → 265 (S272 admitted,
  S273 supersedes its annotation), A 233 → 235, B 24, C 6, mined 239 → 241, rejected 16, queued 8, W04 30 → 30.
- **Dated correction of the round-84 grade (R84-V7).** The round-84 report graded `expansion: improved` on a
  ledger/source move; under `LEARNING.md` the expansion trend counts admitted `knowledge/` entries on uncovered ground,
  frontier areas, new source kinds or a capability row, and round 84 landed none. Corrected grade: `expansion: unchanged`,
  appended to `corpus/lessons/round-84.md` and carried in the round-85 lesson.
- **Dated correction of the frozen class figure (R85-F1).** The frozen claims' "`serialization-schema` class executed
  0 of 9 → 1 of 9" is wrong on both the numerator and the denominator: the class census has 10 members and
  `db-wal-recovery` was already executed at round 40, so the ledger's own numbers are 1 of 10 → 2 of 10
  (`file-artifact` 20 of 76 → 21 of 76). The frozen claim is not rewritten — the C1 predicate does not reference the
  class figure, so no verdict depends on it.
- **Dated correction of the S272 annotation (S273).** S272's anchor cites `:30` (a blank line) and
  `(6 whitespace-split words)`; the assertion is on line 31 and `len(quote.split())` is 9. The old row is preserved and
  the append-only S273 supersede carries the corrected annotation.
- Re-verification: the pinned URL was fetched this round (HTTP 200, 1097 B, sha256 `8f5bc110…`) and equals the round-52
  capture byte for byte; the served-model endpoint `:34113` remains ABSENT (carried, operator-side); `~/Projects/bounties`
  remains ABSENT (carried).
- Frontier: Q61 landed from `considerthese/2026-10-26.md` §2 (per-entry form; the standing counter is still open);
  `expansion: unchanged` (the round-84 grade is corrected in `corpus/lessons/round-84.md` under R84-V7); assimilation none
  (`merge/kengaku/` blocked by L0 `kengaku | round-54`).
- Receipts and commits: `corpus/evidence/round85/sqlite-db-truncate-probe.txt` (first mint `ce5b9ef8`, re-mint from a clean
  clone `f8884277`, `LANE_TIP dc02d818`); ledger row `sqlite-db-truncate` executed (`ce5b9ef8`, `subject=tb2-header`,
  `verdict=cases` after `35b1e4e0`); `plans/round85_sqlite_truncate_probe.py` (`99a7cb3b`, header line `2410f403`);
  `plans/round85_c1_replay.py` (`99a7cb3b`, freeze anchor + work-dir repairs `e7b44805`, header-line acceptance
  `b1e57097`); `plans/round85_c2_debt.py` (`99a7cb3b`, v7/v8 repairs `e7b44805`, v3 exit convention `217910c5`, byte-level
  v8 `da463cbd`, v3 split `def5d0ea`); `plans/round85-cases.json` and `plans/round85-defects.json` in the freeze commit
  `1a45aeb5`; `corpus/QUALITY.md` Q61 (`99a7cb3b`); entry writer rename to `kengaku-L1-round83-admission` (`99a7cb3b`);
  round-84 wave evidence committed (`99a7cb3b`); `corpus/SOURCES.md` S272 (`e7b44805`) and S273 (`20eb9ba7`); `corpus/lessons/round-85.md` (`e7b44805`, v8 base-sensitivity note `da463cbd`, honest-stop erratum and S273 correction `20eb9ba7`); `corpus/README.md` index rows
  (`e7b44805`, round-84 closure row `2410f403`); registry rows for the three instruments (`35b1e4e0`). Final tip and the
  round report: `<L1 fills: final tip commit and report path>`.
- Re-verification lines: R79 population gate green at the tip (`DEFECTS n=0`) after the ledger's `verdict` was re-priced
  to `cases` to match the receipt's `CASE` observation form (`35b1e4e0`) — the same vocabulary gap round 84 recorded and
  round 85 repeated; R75 index parity green (`lessons 143/143`); R82 and R74 registries green; `gate_timing_check.py
  --selftest` exit 0 and `plans/gate_timing_check.py --lesson corpus/lessons/round-85.md --commit master` prints
  `no admit rows`, the honest state for a round that admits no knowledge entry; `state_check.py --summary` still FAIL with
  the one carried mismatch.
- Transcripts: `.ufo/waves/round-85/L1/`; wave evidence: `.ufo/waves/round-85/w1/`.
