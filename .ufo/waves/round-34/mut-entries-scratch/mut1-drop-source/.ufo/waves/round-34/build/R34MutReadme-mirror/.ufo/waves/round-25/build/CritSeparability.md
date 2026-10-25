# CritSeparability — C1/C2 separability + lowest-axis tie-break (round 25)

Scope: attack `plans/round-25-claims.md` separability (:95-96) and the novelty/coverage tie-break (:10-19). Read-only; base `6180e4f`, worktree `3f371d2`.

## Findings

**F1 — r24 `capability_rows` breach recurs, via `corpus/SOURCES.md` (HIGH).** The separability
sentence (round-25-claims.md:95-96) freezes only *SCORECARD rows*. But P2a row 3 re-derives
`sources-registry` whose evidence cell pins counts: "rows 25, malformed 0, `A=24 C=1`,
`mined=18 queued=5 rejected=2`" (SCORECARD.md:557). C1 is *required* to append SOURCES rows
(claims:100-101). P2a's frozen rule is "every expected token in the row's evidence cell must
appear in its output" (claims:76-77) — after C1 lands, `rows 25` fails. Revert C1 → token
matches again. Same failure shape as r24: C2's count moves with C1's landing
(round24_census.sh:64 counted rows C1 created). C2's `match/mismatch` is not separable.

**F2 — P2e file→row direction is unfrozen (HIGH).** claims:85 checks `corpus/README.md`
"both directions (row → file; file → row)". File enumeration happens on the landed tree;
C1 adds `knowledge/` entry (claims:101), `lessons/round-25.md` (claims:102), possibly
`evidence/` files. Any without an index row → C2 mismatch. Whether C2's appended corrections
may add index rows for C1's files is unregistered; either way C2's count depends on C1's
bookkeeping discipline — or the check silently skips all new files and "match" overstates.

**F3 — `## Capabilities` insertion shifts P2b anchors (MED).** A new capability row for the
demonstrated instrument (the natural r24-pattern landing; AXES.md:57-64) inserts above
SCORECARD.md:610-616, shifting every `:line` anchor P2b must resolve — including the table's
own basis pointer `:162` inside the novelty row (:610). C1's bookkeeping write becomes a C2
mismatch storm. Note claims:78 cites `:610-616` verbatim from base bytes.

**F4 — P2c's authority is outside the lane repo and unfrozen (MED).** The SHONEN seed lives at
/home/vgpnk/Projects/shokunin/PROTOCOL.md:439-448 — absent from the lane repo and from any
`git archive 6180e4f` tree (no PROTOCOL.md/AXES.md/scripts/ in lane root; verified). Fleet
PROTOCOL last edited 2026-10-19 (7c5b34f). C2's "before" run on the base archive (claims:89)
cannot re-derive P2c; a mid-round fleet edit flips a C2 assertion with no lane change. Same
for `scripts/sources-census.sh` (P2a-3, claims:103-104) and `AXES.md` (claims:15,79).

**F5 — P2d wording diverges from QUALITY R4; row class ambiguous (MED).** claims:83 demands
"ABSENT" on the row; QUALITY.md:89 (R4) accepts "ABSENT <date> *or a dated erratum*" — and
PROVINCE.md:95-100 is exactly that erratum. Today `~/Projects/webzites/repos/llm-wiki`
(PROVINCE.md:12) and `~/archive/bench-arena/` (:13) fail `test -e` with no on-row `ABSENT`;
:14 mixes a dead endpoint with dead local paths (`/proc/1299/cmdline`) — "first backticked
local path" is ambiguous (first backtick is a URL). Literal-P2d manufactures base mismatches
that C2 then "closes" — inflating then flattering the headline count; R4-P2d reports them
already-conformant. Base mismatch number is implementation-dependent, not frozen.

**F6 — duplicate assertions inflate `assertions=` (LOW).** P2b basis cells re-name P2a's
commands: `python3 grader.py` `n=733` (SCORECARD.md:555 vs :614) and `freeze-check`
(:556 vs :614). One fact, two registered assertions → one failure = two mismatches, one
appended correction closes both.

**F7 — tie-break is moot; mapping creates dual score authority (tradeoff).** claims:10-12
tie-breaks novelty vs coverage, but SCORECARD.md:566 records owned axes as
"novelty 7 / calibration 8" — coverage is not this lane's axis; there is no owned-axis tie,
C1 alone discharges AXES.md:33-34. The material issue: C1's +1 lands on legacy `novelty`
while mapped to canonical `coverage`, whose row stays 7-capped pending the operator's
round-24 ruling (claims:11-12; SCORECARD:613). Result: one canonical axis carrying
irreconcilable numbers (coverage 7 "held" / novelty→coverage 8) — a score a non-author
cannot re-derive (PROTOCOL.md:512-516). The pre-reg defers the cap ruling yet presumes the
row-scoped reading that makes its scoring legal.

**F8 — shared end-gate (LOW).** `sources-census.sh validate` is both the round-level frontier
gate (claims:103-104) and inside P2a-3: one malformed C1 row fails both — acceptable only if
F1 is fixed.

## Smallest safe correction (claims amendment, no redesign)
(i) Freeze P2a-3's asserted tokens to census *cleanliness* (`kengaku ok`, zero E-codes,
malformed=0); base counts reported-not-asserted. (ii) Scope P2e file→row to the base file
manifest; C1 files carry their own index rows. (iii) Either ban `## Capabilities` rows this
round or make state_check resolve the axis table by heading+row-name, never the `:610-616`
literal. (iv) Pin PROTOCOL.md/AXES.md/sources-census.sh digests in P2's freeze block.
(v) Adopt R4's erratum allowance in P2d and define "first *local* backticked path".
(vi) Dedupe P2a/P2b shared commands. (vii) Record C1's +1 as verdict-only on the canonical
axis (r21 precedent, SCORECARD:610) until the operator's cap ruling, or amend that the cap
binds the `coverage` row only.

## Falsifiable condition
On the landed tree, apply a revert of only C1's delta (SOURCES rows, knowledge/lessons/
evidence files + their README rows, `plans/attrib_calibration.py`, fixtures):
`state_check --summary` must print identical `match`/`mismatch`/`offline_unverifiable` and
exit code; symmetrically, reverting C2's corrections must leave `attrib_calibration.py`
verdicts identical. Under the frozen spec as written, F1 alone falsifies separability
(`rows 25` vs `rows ≥26`).

VERDICT: Separability fails as registered — F1 is a direct r24-class re-breach (C2's P2a-3 count moves when C1's SOURCES rows land/revert); F2/F3/F4 share the same unfrozen-surface defect; F7 is a tradeoff for the judge, not a defect. Smallest correction: re-scope P2a-3 to cleanliness-only, freeze P2e file-side to base, pin external authorities. No tools installed (read-only review; pacman paused, none needed).
