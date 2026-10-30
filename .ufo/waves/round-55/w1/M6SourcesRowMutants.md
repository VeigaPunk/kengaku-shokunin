# M6SourcesRowMutants — scoped findings (kengaku round 55, wave 1, v2 build+attack)

Seat `M6SourcesRowMutants`, 2026-10-30. Lane `kengaku-shokunin`; frozen claims
`plans/round-55-claims.md` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` read first; no predicate,
counter or kill rule changed. Target: *do the census/gate catch defective SOURCES rows?*

**Verdict: mostly yes — 4 of 5 injected row defects are killed by the frozen census; one survives and
is the reviewer-eyes item.**

## Mutants (scratch copy of `corpus/SOURCES.md`, one defect at a time, on the DRAFT row S201)

| id | defect | `CORPUS.md` §Census (7 manual commands) | `scripts/sources-census.sh validate --file` | lane gate `plans/anchor_digest_check.py` |
|---|---|---|---|---|
| M1 | drop one pipe → 10 columns | **caught** (malformed=1) | **caught** (`E01 S201 fields=10`, exit 1) | caught (`class=row-malformed cells=10`) |
| M2 | sha256 token moved out of the anchor cell | **MISSED** (all clean) | **MISSED** (exit 0, `file ok`) | caught (`class=token-outside-anchor sha256-claim-in-cell-7-of-11`) |
| M3 | tier `D` | **caught** (`tier S201 D`) | **caught** (`E06 tier=D`, exit 1) | missed (no enum leg) |
| M4 | status `mined!` | **caught** (`status S201 mined!`) | **caught** (`E07 status=mined!`, exit 1) | missed |
| M5 | duplicate id | **caught** (dup list prints `S201`) | **caught** (`E03 duplicate id` + `E04`, exit 1) | caught (duplicate defect line) |

Controls: the pristine draft registry is **clean** under both frozen census families (rows=195,
malformed=0, no duplicate ids, no enum violations, no missing `used-by`; `sources-census.sh validate`
exit 0 with only 15 pre-existing `W04` warnings). The committed base tip `80afa61` is clean too
(rows=193). Mutation hashes and full transcripts: `.ufo/waves/round-55/w1/M6SourcesRowMutants/mutants.md`
and `.../M6SourcesRowMutants/receipts/`.

## Reviewer-eyes item (feeds the round lesson)

**The census has no anchor-content leg.** A sha256 pin displaced out of the anchor cell — or dropped
from it — leaves both frozen census command families green (D2 prints `file ok`, exit 0). The census
checks id shape, column count, kind/tier/status enums, dates, URL duplication and `used-by`
existence, nothing inside the anchor cell. Only the lane's own `plans/anchor_digest_check.py`
(`token-outside-anchor`) detects the displacement, and **that gate is red on this tip**, so a green
census is not evidence that the new rows' pins are sound.

## Defects found (reported, not fixed — not this seat's files)

1. The lane's advertised anchor gate is **already red**: `python3 plans/anchor_digest_check.py --lane .`
   → exit 1, `rows=193 tokens=92 defects=21` at base tip `80afa61` (S173–S193, all `anchor-unbound`),
   `rows=195 tokens=94 defects=23` with the round-55 draft rows (S201/S202 add two more).
2. **S202's pinned digest is not resolvable from committed corpus evidence.** Token
   `sha256 6ba25be4…ce7a` matches
   `.ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census/chess-best-move/instruction.md`
   (verified by `sha256sum`), not anything under `corpus/evidence/`; no `chess-best-move/instruction.md`
   capture exists there.
3. **S201's pin is true but unbindable by the gate.** Capture
   `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` has exactly the anchored
   digest `a540714e…f286` (also listed in `corpus/evidence/round52/graders/SHA256SUMS` line 18), but
   the round-52 graders tree has no `task.toml`/`PROVENANCE.md` locator, so the tool derives task
   `tests` instead of `chess-best-move` and reports `anchor-unbound` — the same root cause as the 21
   base-tip defects.

## Hygiene

Scratch root `/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/` created, used, receipts copied
into `.ufo/waves/round-55/w1/M6SourcesRowMutants/receipts/`, then deleted. No mutating git/jj command
was run; the lane was read-only; no fleet-root file was written; no tool installed. Pristine registry
restored and verified byte-identical (`1b8bd314…d8fa`).
