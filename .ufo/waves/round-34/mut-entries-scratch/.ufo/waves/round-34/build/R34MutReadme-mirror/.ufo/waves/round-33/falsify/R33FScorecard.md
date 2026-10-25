# R33FScorecard — Round-33 SCORECARD truth and planned next move (falsify seat)

Seat: `KengakuR33.R33FScorecard` (leaf; no subagent dispatch). Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Verdict: **mismatch found (1 substantive + 2 landing-artifact), residual risks carried from build wave.**
No lane/fleet file edited; this report is the only write. No tools installed.

## What was tested

1. Final Round-33 section of `SCORECARD.md` (worktree read; see F2 for commit state).
2. Axis scores vs the Round-32 section in the same file.
3. All three counters re-run live at lane HEAD `77ac8c1` (dirty worktree: only `.ufo/waves/round-33/` + `SCORECARD.md`; counter inputs `corpus/*`, `plans/*` clean at HEAD).
4. C1's stated S093 delta: S093 row cells at freeze `f0b20aea` vs HEAD, `git diff f0b20aea..HEAD -- corpus/SOURCES.md`, freeze entry content `f0b20aea:corpus/knowledge/benchmark-grader-semantics.md`, control receipt.

## Findings (by severity)

### F1 — [C1 claim] The stated S093 delta is inaccurate [mismatch — the target of this seat]
- Frozen claim `plans/round-33-claims.md:37-38,48-49` states S093 is "already mined and **gains the entry in used-by**" / "S093's used-by gains the entry".
- Evidence: at freeze `f0b20aea`, the S093 row's used-by cell **already** reads `corpus/knowledge/benchmark-grader-semantics.md` (identical at HEAD). `git diff f0b20aea..HEAD -- corpus/SOURCES.md` shows **zero change** to the S093 row. S093 did not "gain" the entry this round; the cell predates the round.
- The real C1 deltas are: (a) entry citations changed `S094/S097 → S103/S104` (freeze entry cites S093/S094/S097; HEAD entry cites S093/S103/S104); (b) S103/S104 are genuinely new rows created at admission commit `b54feca` (absent at freeze, present+mined at HEAD); (c) `rows_mined` 1 → 3 and `usedby_ok` 0 → 1 are driven by S103/S104, not by S093.
- The SCORECARD C1 row itself does **not** repeat the false "gain" narrative; its before/after token strings are accurate and reproduce exactly (see F4). The inaccuracy lives in the frozen claim file and is already independently flagged by build report `R33ClaimsReview.md` §C1.

### F2 — [Scorecard landing artifact] "Round-33 section finalized at lane tip `66c734c0`" is stale; the reviewed text is not at any commit
- `SCORECARD.md` was modified **after** `66c734c0` by commits `6cb5c82` (fill-in of before→after measurements, replacing an earlier provisional "PASS" rendering) and `c1a520d` (capability row), so the section was not final at `66c734c0`.
- The reviewed text additionally contains **uncommitted worktree edits** (`git status --porcelain` → `M SCORECARD.md`): "measurements follow at landing" → "measurements below reflect the landed counters" and an appended "## Planned (round 34)" block. The exact section reviewed exists only in the worktree, not in HEAD.

### F3 — [Scorecard landing artifact] Round-33 section omits its own capability row
- `c1a520d` added capability `offline-catalog-receipt-verification` (First-working round 33) to the global `## Capabilities` table with evidence command/output matching the live C3 run. Verified present at HEAD.
- The Round-33 section itself carries no capability table (Round 32's section explicitly had a "— none —" row) and never mentions this round's new capability; its no-stagnation-waiver sentence cites only the round-31 capability row. Omission, not contradiction.

### F4 — [Measurement claim] All three counters reproduce exactly [verified]
Run at `77ac8c1` (worktree) with exact scorecard-stated output and exit codes:
- C1: `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0. ✓
- C2: `python3 plans/round33_defects.py --lane .` → `checks=6 defects=0` exit 0. ✓
- C3: `python3 plans/catalog_probe.py --verify --lane .` → `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok` exit 0. ✓
- C1 before-line in the scorecard matches the committed control receipt `.ufo/waves/round-33/claims/control-nothing.txt` verbatim (`entries=1 … rows_mined=1 usedby_ok=0 census=ok`, exit 1). Note: the **claims file** misstates this control as `entries=0` (`R33ClaimsReview.md` F1); the scorecard row is correct.

### F5 — [Axis claim] Round-32 → Round-33 axis scores consistent and unchanged [verified]
- Round-32 section: coverage 7 (held), calibration 8 (held-incomplete), freshness 8 (held-failed as declared); depth 9, novelty 7, adjacency 8, operability 8.
- Round-33 section: coverage 7 → 7 held, calibration 8 → 8 held, freshness 8 → 8 held; "no axis score changed this round" matches. Baseline/freeze ids (`112091c2d9`, `f0b20aea` + `c227e486`) match the freeze prereg. Planned round-34 move targets coverage (tied lowest with novelty) — consistent with the stated frontier.

## Residual risk / build-wave carryovers (not re-scored here)

- **C2 "closed" verdict rests on a gameable counter** (`R33CounterAttack.md`: N1 measures index not commit; N2 heading-only; N3 width 300 vs frozen 400; N4/N5/N6 token presence; full-lane fabrication F1 passes exit 0). The scorecard verdict cell reports the counter, not a semantic audit.
- **C3 counter mutated after freeze**: `plans/catalog_probe.py` changed (40 lines: `OR_URL …?limit=10`, `total_count`-based count, byte fetches) and `plans/round33_c1_verify.py` changed (9 lines) between freeze `f0b20aea` and HEAD. `plans/adoption_check.py` and `plans/round33_defects.py` are unchanged (empty diff; confirmed by `R33CounterAttack.md` for the latter). The C3 measurement therefore reflects a post-freeze counter, weakening "same condition in the counter's code"; the R33ClaimsReview caveats (offline verifier cannot establish live-probe authenticity; absolute kill-rule claim unsupported) stand.

## Verification gaps / notes
- Not independently re-fetched: live URL probe (offline `--verify` only), fleet-report contents (N3/N4), and round-30/31 lesson locators (N5/N6); all covered by sibling seats/build reports.
- No repo mutation performed; counters are read-only (write-side effects exist only in selftest/draft paths, not in the invoked modes).

VERDICT: scorecard-falsified (C1 S093 delta stated in the frozen claim is inaccurate; scorecard landing artifacts have staleness and omission issues; measurement/axis claims verified true).
