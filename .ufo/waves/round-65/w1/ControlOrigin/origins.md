# ControlOrigin — r65 w1: four routed defects, origin → repair target

Seat: ControlOrigin (revenger). Read-only. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Defect source: `corpus/lessons/round-64-verifier-spotcheck.md` §7 (lines 104–110). Round-64 tip
`21b13dc70fae6645ce0d6c7cdec5117ca397d071`; base `12a6255170bcc466029bf82037885fd69e20370f`;
freeze tip `b5032ff8391dcb5939c3be53516b31a50ab340a0`. Every value below is reproduced, with its
command, in `evidence.txt` (same dir).

## Re-derived origins (filed bytes at 21b13dc7)

**D1 — rendered f-string in a quote.** `corpus/SOURCES.md:246` (row S230). The anchor cell
(`awk -F'|'` field 7) reads `… located quotes "Port 5328 is not listening - no real gRPC server is
running" (line 96) …`, and the scope cell (field 6) carries the same rendered fragment. The
round-64 lesson's `## Gate` repeats it at `corpus/lessons/round-64.md:20`
(`` `"Port 5328 is not listening - no real gRPC server is running"` (line 96) ``). The grader's
true source line 96 (`corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py`,
sha256 `115de2e9…1b0e`) is:

```
    assert result == 0, f"Port {port} is not listening - no real gRPC server is running"
```

`grep -c 'Port 5328 is not listening' <grader>` → `0`; the f-string form → `1`. The quote is a
rendering, not source bytes: the defect is real and located in exactly those two artifacts.

**D2 — unqualified freshness-10 citation.** `SCORECARD.md` lines `2583, 2644, 2743, 2801, 2838,
2860` (sections r59, r60, r61, r62, r63, r64): `grep -c 'freshness 10'` → `6`;
`grep -c 'addendum-classified'` → `0`. All six cite freshness held at 10 without the qualifier
that the 29 frozen entries' openings are `TRIO-ADDENDUM` (spotcheck §7.2: "wherever freshness 10
is cited").

**D3 — bare `.ufo/waves/` base in the report.** Fleet repo (read-only)
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-64/kengaku.md` lines `17, 18, 19, 20, 31, 92,
110, 114`: eight backticked citations, all rooted at `.ufo/waves/…` (e.g.
`` `.ufo/waves/round-64/w1/GraderRecon/s231-quotes.txt` ``); `grep -ci 'lane-root\|kengaku-shokunin/\.ufo'`
→ `0`. No lane-root base is stated anywhere in the report.

**D4 — teaches length.** `corpus/SOURCES.md:246` teaches cell (`awk -F'|'` field 8) = `34`
whitespace tokens (`wc -w`); `37` when hyphens split (`tr '-' ' ' | wc -w`), `35` when only `/`
splits. S230 did not exist at `6b0908a5` (0) and is `34` at both `7c2217ed` and `21b13dc7`, so the
spotcheck's 37 is not an older row state. Reconciliation: the spotcheck's counter splits the three
hyphenated compounds `seven-leg`, `lane-built`, `5-7` (each +1), while the frozen counter
`awk -F'|' '{print $8}' | wc -w` splits only on whitespace; both counters read the same cell, and
`34 + 3 = 37` exactly. The claims doc's 34 is the frozen-counter value; no filed byte changed.

## Targeting check against plans/round-65-claims.md R65-C2

D1: origin `corpus/SOURCES.md:246` (anchor + scope cells) and `corpus/lessons/round-64.md:20` (Gate)
→ repair target `corpus/SOURCES.md` (new row S234 at `:250`, anchor cell quoting the full source line
96 verbatim, teaches opening `supersedes S230 —`, 22 words) plus an appended `## Erratum (round 65)`
block in `corpus/lessons/round-64.md` (marker `R64-ERRATUM-65`) — **RIGHT-TARGET**: right files; the
SOURCES half uses the only lawful form (Q34: a correction is a NEW row whose teaches opens
`supersedes S0NN —`), the lesson half matches the filed erratum precedent
(`corpus/lessons/round-61.md:79`), and S230's row is byte-identical at the freeze tip
(`cmp` of the extracted 1083-byte row → equal).

D2: origin `SCORECARD.md:2583,2644,2743,2801,2838,2860` → repair target `SCORECARD.md`, appended
dated correction block — **RIGHT-TARGET**: right file, right form (a dated appended block; precedent
`### Round-59 verifier-routed precision corrections (appended 2026-11-02, round 60 …)` at
`SCORECARD.md:2597`). The r64 section is the file tail (`### Planned (round 65)` is its subsection
at `:2864`), so "after the round-64 section" is an EOF append, which keeps the base bytes a prefix.

D3: origin fleet `.ufo/reports/round-64/kengaku.md:17,18,19,20,31,92,110,114` → repair target
`corpus/QUALITY.md` criterion Q47 plus this round's report — **RIGHT-TARGET** (forward-only): the
filed report is in the fleet repo and its bytes are not the lane's to rewrite (R1: corrections are
appended, never rewritten); a criterion in the lane's own bar is the routed remedy, and Q47 is the
next free number (Q46 at `corpus/QUALITY.md:1189`; `grep -c 'Q47'` → `0`). The frozen counter proves
the rule landed, not that the eight filed citations changed.

D4: origin `corpus/SOURCES.md:246` teaches cell = 34 words → repair target `corpus/SOURCES.md` S234
teaches cell (22 words, ≤ the 25-word bar) — **RIGHT-TARGET**: right file, right form (new row; S230's
cell stays byte-identical).

ORIGINS: 4/4 right-target

## Notes for the L1 (report, do not edit)

1. **D1 residual instance.** S230's *scope* cell (field 6) carries the same rendered fragment and no
   declared repair cell restates the corrected quote for it; S234's scope cell describes the fix
   instead. Under Q34 this is lawful (the old row stays), but the rendered quote survives in filed
   bytes at `corpus/SOURCES.md:246` in two cells, not one.
2. **D1 is not machine-checked.** `plans/anchor_line_check.py --lane . --verbose` emits no row for
   S230 or S234 (`grep -cE 'S230|S234'` → `0`; its anchor grammar wants `commit <sha>, <file>:<N>
   "<quote>"`), so the supersession's correctness rests on the frozen grep counter and human reading.
3. **C2's cmp clause is false for SOURCES.md as frozen.** `git diff --numstat 12a62551 b5032ff8 --
   corpus/SOURCES.md` → `3 0` and hunk `@@ -247,0 +248,3 @@` (rows inserted at the table end, before
   `## Paths`); `head -c 192299 corpus/SOURCES.md | cmp - <base>` → differs at char 181789, line 248.
   The frozen sentence "SOURCES.md … keep their base bytes as a byte-prefix" cannot hold for any
   id-ordered registry row that must land before `## Paths`, while the intended property does hold:
   zero deleted/modified lines and S230's row byte-identical. Flagged as a rule-wording defect for a
   dated amendment; not a seat edit.
4. **D2 coverage vs counter.** Six citations, only `:2860` in the r64 section; `grep -c
   'addendum-classified'` → `≥1` passes even if the block qualifies one site. The block should name
   all six line numbers (r59–r64) to discharge §7.2's "wherever".
5. **D4 content.** S234's teaches (`22` words) is meta — "anchor quotes the grader's own f-string
   verbatim, teaches is one benefit within the word bar" — and does not itself state a grounded
   learner benefit about the source, which is what §7.4 asks for. The word bar is met; the intent is
   only partly met.
6. **Uncounted declaration.** R65-C2 repairs item 1 also promises an appended dated addendum to
   `corpus/knowledge/tb2-kv-store-grpc-offline.md` re-pointing its citation to S234; no frozen counter
   covers it (`git diff --stat 12a62551 b5032ff8 -- corpus/knowledge/` is empty at the freeze tip).
