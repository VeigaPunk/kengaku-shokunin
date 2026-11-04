# ReviewerC285 — independent R85-C2 attack

Axes: coverage, calibration. Recommendation: **FINDINGS** (not an admission decision).

## Measurement boundary

Frozen claims read in full; freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`, BASE `0de45354d7aff18e4a23a348ec13de3a1f707a44`. Final measured revision: **`def5d0ea5fbf49389400663d30c5a2c8820e56a5`**. Earlier failures at `d4253aa0` were superseded by integration and are not counted below. The lane advanced during review; final runs used an isolated scratch Git repository with both HEAD and master pinned to the measured revision, avoiding mixed-revision controls (the instruments internally use master).

No production edits, network requests, installations, subagents, or other-seat messages. LSP unavailable: `xd://lsp` returned “No such tool”; references/definitions/diagnostics could not be obtained. Evidence below is committed-byte inspection and explicitly exercised behavior, not semantic proof from text search.

## Findings, ordered by severity

1. **Moderate — V8's executable check drops the frozen gate-verdict requirement.** `plans/round85_c2_debt.py:190-207` returns success solely from four literal flag strings. It runs the registry but never requires its exit code or `PREDICATE R82-C1 pass`; only the round83-c2-debt row's `defects=` text is diagnostic detail. The frozen V8 check explicitly requires the registry predicate and exit 0. Thus an unrelated registry failure could coexist with `CHECK v8 ok`. Independently, the actual registry is green at the measured revision; this is a check-contract defect, not a claim that the repair failed.

2. **Moderate — V6 recognizes only one spelling family of seat identity.** `plans/round85_c2_debt.py:41,166-178` uses `^KengakuR\d+$`, not the committed seat identities. A fixture changing only the candidate writer to the real round-84 seat name `CriticR84` produced `CHECK v6 ok writer=CriticR84 checker_rc=0`. This reinstates a seat-id writer while passing the check. The actual renamed writer is distinct and the original `KengakuR84` regression is caught.

3. **Moderate, adjacent C1 instrument defect — stale fixture verdict breaks its mutant battery.** `plans/round85_c1_replay.py:216` now requires ledger verdict `cases`, but `flip_ledger()` at `:340-345` still writes `predicate`. Consequently the ledger-bad fixture carries a second defect: dropping the status check cannot admit it. Against the pinned repository, `--mutants` returned **1**, `MUTANTS real=5 necessary=4 redundant=1`; `no-ledger ... mutant_reaches_target=False`. Other four mutants, including no-reproduce, reached the target when their checks were removed. This is not evidence that REPRODUCE is non-load-bearing; it is a contaminated ledger fixture.

4. **Minor — V2's registered check omits the promised SETUP fixture leg.** `plans/round85_c2_debt.py:120-129` checks freeze existence and byte identity only. The frozen V2 cell says “freeze-tree presence + a SETUP fixture run.” The behavior is real and independently demonstrated, but that second half is not executed by v2: it lives in the C1 selftest instead.

5. **Minor — frozen V3 exit convention disagrees with execution.** The frozen V3 cell says forged-receipt rejection prints `target_reached=False`, exit **1**. The C1 control actually exits **0** when rejection succeeds; C2 now requires 0 (changed in `217910c5`). Observed rejection was `CONTROL forged-receipt target_reached=False defects=1 codes=REPRODUCE-MISMATCH`, exit 0. The frozen element appears wrong; it was not edited here. The substantive rejection is genuine.

6. **Minor — Q61 overstates a “committed filler package.”** `corpus/QUALITY.md:1320` uses that phrase, but its executable half constructs a degraded Q61 row at runtime (`plans/round85_c2_debt.py:296-299`), replacing the row with `- **Q61 — placeholder.**`. This is a working executable control, not a separately committed filler package. V5 itself (`:155-163`) only checks the criterion row and three tokens; it does not execute the named control.

7. **Contract-level prose-only finding — V7 and V9 are satisfied by prose tokens.** `plans/round85_c2_debt.py:181-187,210-219` accepts occurrences of correction/verdict/horizon strings, without establishing a dated correction's meaning or the pricing's adequacy. The actual prose is substantive and honest on inspection, but these two checks are prose-only, which the assignment explicitly asks to flag. V7 also does not inspect the round-85 report named by the frozen repair; that report is absent at this measured revision. V9 has additional real executable support: BASE resolves and the sensitivity run evaluates it.

## One row per routed id

| id | Repair at measured revision | Substantive? | Red at BASE? | Evidence |
|---|---|---|---|---|
| R84-V1 | All four named round-84 wave paths tracked | Yes: real evidence, not empty placeholders | Yes: all four absent | `git cat-file -e REV:<path>` succeeds for `.ufo/waves/round-84/w1-results.json`, `w1/CriticR84.md`, `w1/CriticR84/critique.md`, `w1/CriticR84/report.txt`; fails for all at BASE. Results JSON contains 12 results; report.txt is 3,874 bytes. CriticR84.md and critique.md intentionally resolve to the same blob `8e86b5a3…` (duplicate content, not an additional independent review). |
| R84-V2 | Frozen tables present at freeze and unchanged | Yes; registered check incomplete (finding 4) | Yes: round-85 inputs absent | Case-table blob at both freeze/tip `e6574d21866c5d5cbd6555a1187ab3c10f7200fa`; defects blob `5656699f310b91e94ad6f7cc880e0e67c9b710c3`; claims blob `9abd3a93eb83c027cb938c510cdcf3b55b028a62`. C1 selftest reports `freeze-anchor-fails-closed pass`. Separate Git fixture with FREEZE_REV redirected only in a scratch counter copy to a claims-only commit: `DEFECT SETUP frozen-input-missing plans/round85-cases.json@…`, exit 2. |
| R84-V3 | Production REPRODUCE runs or rejects; forged control dies | Yes, behavioral rejection; source-string code leg is only a proxy | Yes: `instrument-absent`, explicitly absence-red | C1 production `run()` calls `check(tree, work)` with default reproduce=True; no CLI bypass. Forged control rejected solely by `REPRODUCE-MISMATCH`; no-reproduce mutant reaches target. Frozen exit discrepancy: finding 5. |
| R84-V5 | Q61 criterion and executable control | Yes in the round-84 freeze's expressly per-entry form, not the standing universal counter; “committed” caveat | Yes: `no Q61 row` | Round-84 claims :94-95 promise a QUALITY criterion using the C2 filler control's per-entry form. Q61 cites considerthese §2 and names `--control-presence`; exercised output `target_reached=False`, exit 0. Standing parametrised admission counter remains explicitly open. Finding 6. |
| R84-V6 | Writer renamed to `kengaku-L1-round83-admission` | Yes for actual collision; checker proxy incomplete | Yes: `writer-is-seat-id:KengakuR84` | Entry line 4 has the new writer, distinct from the named seats. `gate_timing_check.py` uses line-start MULTILINE writer/author regexes (:55-57), and selftest fixtures :755-758 exercise declared writer/author conflicts. `--selftest` exits 0, ALL PASS. It does not establish universal namespace disjointness: finding 2. |
| R84-V7 | Dated append-only correction in round-84 lesson, repeated unchanged verdict in round-85 lesson | Meaningful correction, prose-only check | Yes: correction/verdict absent | `corpus/lessons/round-84.md` appended `R84-V7 (2026-11-04)` and `expansion: unchanged`; round-85 lesson carries unchanged expansion. Historical report bytes not rewritten. Round-85 report not yet committed here. Finding 7. |
| R84-V8 | Four dynamically constructed flags replaced by literal add_argument calls | Yes; registered check differs from freeze | Yes: literal_flags=0/4; actual base-tree gate also red | `plans/round83_c2_debt.py` replaces `for mode … add_argument('--'+mode,…)` with literal `--selftest`, `--mutants`, `--control-presence`, `--sensitivity`; behavior need not change. Actual registry at tip: exit 0, `PREDICATE R82-C1 pass`. In isolated BASE worktree: exit 1, `DEFECT ROW-SELFTEST-FLAG:--selftest round83-c2-debt`. Running `--tip BASE` from repaired worktree misleadingly passes because the registry reads working-copy bodies; lesson discloses this. Finding 1. |
| R84-V9 | Existing BASE revision plus explicit definition-horizon pricing | Yes on inspection; prose-only pricing check | Yes: `lesson-absent`, explicitly priced | Counter's BASE is existing `0de45354…`; both before-state and sensitivity execute successfully. Committed lesson §Definition horizon says absence-red is not “measured and wrong,” identifies future repair/lesson conditions, and leaves independent closure to judge their text. Finding 7. |

## Exercised outcomes

Final pinned repository/instrument measurements (not inferred from filed receipts):

- C2 tip: `TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0`, `PREDICATE R85-C2 pass`, exit 0.
- C2 BASE: `TARGET ids=8 closed=0 checks_passed=0 indexed=no defects=8`, fail, exit 1.
- C2 sensitivity: `SENSITIVITY n=8 failed_at_base=8`, exit 0. V3 and V9 reds are absence-red, not measurements of incorrect content; lesson prices this.
- C2 selftest: 6 cases, 0 failures, exit 0. Mutants: 3 necessary, 0 redundant, exit 0. Presence control: target_reached=False, exit 0.
- C1 tip: cases=8, legs=16, mismatches=0, located=1, executed=1, defects=0, exit 0. BASE: cases=0, located=0, executed=0, defects=8, exit 1.
- C1 selftest: 10 cases, 0 failures, exit 0. Forged control: only REPRODUCE-MISMATCH, exit 0. C1 mutant battery: exit 1 as finding 3 describes.

## Residual risks and verification gaps

The counter's aggregate target is reproducible, but does not erase the frozen/check mismatches above. V7's report-half awaits the L1's report. Q13/R84-V4 remains operator-owned, excluded from eight ids, and no admission is inferred. No network source re-open was needed or performed. Later lane commits were not assessed beyond the explicitly pinned revision. No tool installs/updates.

Self-evaluation: accuracy 4/5 (moving lane mitigated by pinned final repository); completeness 4/5 (all eight covered, report absent); clarity 4/5 (separates actual repairs from weak checks); actionability 4/5 (exact functions and failing fixture provided); conciseness 3/5 (long because frozen-contract discrepancies require separate treatment). Overall 3.8/5.

SEAT ReviewerC285 VERDICT FINDINGS findings=7
