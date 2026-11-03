# ControlOrigin — r65 w1 (revenger): the four r64 routed defects, re-derived and targeted

Read-only seat. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; r64 tip
`21b13dc7`; base `12a62551`; freeze `b5032ff8`. Full command→bytes receipt:
`.ufo/waves/round-65/w1/ControlOrigin/evidence.txt`; origin→target detail:
`.ufo/waves/round-65/w1/ControlOrigin/origins.md`.

## Origins and targets

D1: origin `corpus/SOURCES.md:246` (anchor cell and also the scope cell quote the rendered
`"Port 5328 is not listening - …"`; the lesson repeats it at `corpus/lessons/round-64.md:20`)
→ repair target `corpus/SOURCES.md` (new S234 row at `:250`, anchor quoting source line 96
verbatim) + appended `## Erratum (round 65)` in `corpus/lessons/round-64.md` — RIGHT-TARGET
(Q34 new-row supersession + filed erratum precedent `round-61.md:79`; S230's 1083-byte row
`cmp`-identical).

D2: origin `SCORECARD.md:2583,2644,2743,2801,2838,2860` (6 × `freshness 10`, 0 ×
`addendum-classified` at `21b13dc7`) → repair target `SCORECARD.md`, appended dated block —
RIGHT-TARGET (same file; the r64 section is the tail, so the block is an EOF append and the
base bytes stay a prefix).

D3: origin fleet `.ufo/reports/round-64/kengaku.md:17,18,19,20,31,92,110,114` (8 × bare
`.ufo/waves/…`, 0 lane-root mentions) → repair target `corpus/QUALITY.md` Q47 + this round's
report — RIGHT-TARGET (forward-only: the filed report is not the lane's to rewrite; R1 appends;
Q47 is the next free number, Q46 at `QUALITY.md:1189`, `grep -c Q47` → 0).

D4: origin `corpus/SOURCES.md:246` teaches cell = 34 words (37 when hyphens split: the three
compounds `seven-leg`, `lane-built`, `5-7`; 35 slash-split — the spotcheck's counter splits
hyphens, the frozen counter does not; S230 was 34 at both `7c2217ed` and `21b13dc7`, absent at
`6b0908a5`) → repair target S234 teaches = 22 words ≤ 25 — RIGHT-TARGET.

ORIGINS: 4/4 right-target

## Findings the L1 must price (reported, not edited)

1. **C2's cmp clause cannot hold for SOURCES.md.** Freeze landing: `git diff --numstat
   12a62551 b5032ff8 -- corpus/SOURCES.md` → `3 0`, hunk `@@ -247,0 +248,3 @@`; prefix `cmp`
   differs at char 181789, line 248 (before `## Paths`). The frozen sentence "SOURCES.md …
   keep their base bytes as a byte-prefix" is false for any id-ordered row that must land before
   `## Paths`; the intended property holds (0 deletions, S230 row byte-identical). Needs a dated
   amendment or the claim misses on its own clause as worded.
2. **D1 residual + invisibility.** S230's scope cell carries the same rendered fragment and no
   declared repair cell restates it (supersession leaves it, lawfully). `plans/anchor_line_check.py`
   reports `rows=227 … live=0` but emits no row for S230/S234 (its quote grammar is
   `commit <sha>, <file>:<N> "<quote>"`), so neither the defect nor its repair is machine-checked.
3. **D2 counter weakness.** Six citations across r59–r64; the frozen `≥1` passes on a block that
   qualifies one. The block should name all six line numbers (§7.2 says "wherever").
4. **D4 content.** S234's teaches is meta ("anchor quotes … within the word bar") — it meets the
   25-word bar and the Q34 opener but does not itself state a grounded learner benefit.
5. **Uncounted promise.** Repair 1 also promises an appended kv-store knowledge-entry addendum
   re-pointing to S234; no frozen counter covers it (`git diff --stat 12a62551 b5032ff8 --
   corpus/knowledge/` is empty at the freeze tip).

No tooling installed; no port bound; no file outside this seat dir and the report path written.
