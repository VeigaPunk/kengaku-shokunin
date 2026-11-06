# ScribeLesson — round 95 wave 1 (leaf scribe)

Drafts for the L1 to adopt or refuse. **No lane file was edited** — the lane was
read-only (`git rev-parse`/`log`/`show`/`cat-file`/`ls-tree`/`diff`/`merge-base`/`status`
plus one `git clone --shared` into scratch, since removed).

## Deliverables

| what | file |
|---|---|
| draft `corpus/QUALITY.md` criterion **Q77** (grounded in M1; check measured red on the bad receipt, green on the good one) | `.ufo/waves/round-95/w1/ScribeLesson/quality-criterion-q77.md` |
| draft `SKILL.md` `## Gate/probe registry` rows for `plans/round95_false_gate_census.py` **and** `plans/round95_c2_counter.py`, in the `freeze-integrity` row's exact column shape | `.ufo/waves/round-95/w1/ScribeLesson/skill-registry-row.md` |
| draft decision-table note for the grader class **`serialization-schema`** — the report schema and its six decisive edges (C06–C10, C14), plus the `file-artifact` companion receipt pointer | `.ufo/waves/round-95/w1/ScribeLesson/decision-table-note.md` |
| proof-read of SOURCES rows **S303–S309** against CORPUS.md's SOURCES contract — **no column violates it** | `.ufo/waves/round-95/w1/ScribeLesson/sources-proofread.md` |
| seat report | `.ufo/waves/round-95/w1/ScribeLesson/report.md` |
| raw receipts (census at T; class cells F vs T; receipt revision stamps; SOURCES census; S303–S309 re-verification) | `.ufo/waves/round-95/w1/ScribeLesson/receipts/` |
| runnable draft of Q77's check | `.ufo/waves/round-95/w1/ScribeLesson/draft-receipt-rev-check.py` |

## Findings

FINDING SL-1 major — the M1 mistake receipt's stamped HEAD (`9b93fc8f…`) is the fleet root's HEAD one directory above the lane and resolves in no lane, so a single `git cat-file -e <stamped HEAD>^{commit}` separates a receipt of this lane from a receipt of the tree above it; nothing in the lane runs that check, and the round-94 M4 lesson ("cwd asserted in the receipt") was satisfied by the M1 receipt without being verified. No effect on either round-95 verdict (both pass at T); the M1 receipt is a filed mistake, not a claim input.
FINDING SL-2 minor — the `serialization-schema` class cell reads `executed 3 of 10` at F and `executed 6 of 10` at T, a jump of three for a round that admitted one member; the cause is the declared legacy round-79 repair (claims file line 114: "lands as conformance … not as a claim") resyncing eleven class cells against the ledger, which had drifted. Reproduced: 14 DEFECTS at F → 0 at T. No defect — routed so a reader does not read it as three admissions.
FINDING SL-3 minor — the claims file's "sha256 equal to the table above" holds for four of the seven S303–S309 rows, not all seven (the instruction, test wrapper and task manifest digests are not in the `frozen-instruments` table because they are not instruments the counters read). The rows themselves carry the correct digests; the claims file is F-frozen and is not edited here.
FINDING SL-4 info — `used-by` for S303–S307 names `plans/round95-cases.json`, a plan file rather than a knowledge entry or lesson, and the file cites no S-id for those rows. This is the lane's convention for this benchmark (the round-94 rows do the same; 38 mined rows across the file point at a `plans/` or `corpus/evidence/` path). Not a violation; recorded so the L1 knows the reading.
FINDING SL-5 info — a lane-wide sweep of every committed receipt under `.ufo/waves/` finds 13 whose stamped revision does not resolve in this lane; 12 are legitimately about other trees (11 round-49 fixture-repo receipts, 1 round-76 receipt whose LANE_TIP left the history). Any gate the L1 lands on this must scope its population, not sweep the tree.

## Measured at the measured tip T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`

- R95-C2 census re-run from inside a clean clone: `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc 0 — byte-identical to the committed `c2-tip.txt`.
- Legacy round-79 population-ledger gate: 14 DEFECTS at F → `DEFECTS n=0`, `PREDICATE R79-C1 pass`, rc 0 at T.
- SOURCES anchor gate: `rows=294 cited=104 … live=0 cells=0` at F → `rows=301 cited=111 captured=98 … live=0 cells=0` at T, rc 0 — +7 rows, +7 cited, +7 captured, no new defect.
- CORPUS SOURCES census: 301 rows, 0 malformed, `A=271 B=24 C=6`, `mined=266 queued=8 rejected=27`, no duplicate ids, no enum violations, no missing `used-by` paths; the maintained CLI agrees.
- S303–S309 re-verified against the captures independently of `anchor_line_check.py`: sha256 → tracked capture, cited line → the line holding the quote, declared words → `len(quote.split())` — 7/7 match on all three; every quote ≤ 25 words (CORPUS rule 1).
- The C1 probe was **not** re-run by this seat (15 bwrap cases); its committed receipt records `mismatches=0 defects=0` over 15 cases / 105 legs and the C1 counter's receipt records `PREDICATE R95-C1 pass`, rc 0.
