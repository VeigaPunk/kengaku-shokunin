# Round 77 — kengaku (2026-11-04 UTC)

Base `07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59` (round-76 verifier spot-check). R77-C1 targets
coverage (lowest non-retired axis, L0-capped at 7): one canonical declared-surface inventory carrying
every row of the three older tables, each resolved live under one typed rule, with a supersession leg
that prices a declaration no canonical row carries. R77-C2 targets calibration (held at 10, exercised):
the round-76 closure's seven routed ids (`R76-V1` … `R76-V7`) become ledger rows whose discharges
re-derive at the commit that carries their evidence.

## Gate

- **S253 admitted for reading a repository object's bytes at a named revision.** URL opened live by L1
  `KengakuR77` this round: `https://git-scm.com/docs/git-cat-file`. Access date 2026-11-04 UTC. Capture
  `corpus/evidence/round77/sources/git-cat-file.html`, HTTP 200, 79 488 bytes, sha256
  `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`. Located quote, capture lines
  2584–2585, 15 words: **"If `<type>` is specified, the raw (though uncompressed) contents of the
  `<object>` will be returned."** Kind docs, tier A for at-revision object reads. Registry change:
  absent → S253 `mined`, recheck `on-release`, used-by `corpus/lessons/round-77.md`,
  `plans/round-77-claims.md`.
- **Reject candidate:** "a receipt that names a revision was produced by the tool committed there".
  The same page establishes that an object id names bytes; nothing in it binds the run to the tool.
  The round-76 closure's R76-V1 is that failure class (battery receipts stamped at a pre-battery
  revision). Flip: stamp `TOOL_SHA` inside the receipt and recompute the tool's digest at the stamped
  commit (`plans/round77_c2_defect_discharge.py`, leg V1/V7).
- **Reject candidate:** "a declaration is evidence of resolution" — already mechanical since round 76
  (`c1-control-declared.txt`); this round re-uses it as C1's control on a fixture whose declaration
  lies, and the counter's `trust-declared` mutant keeps the class priced.
- **considerthese re-adjudication (`considerthese/2026-10-26.md`, the latest file).** Proposal 1
  (routed-findings burn-down) was implemented ~35 rounds ago (`plans/routed_open.py`, the
  `routed-findings-burndown` capability row) and R76-C2 extended it; proposal 3 (batched TB2 sweep)
  landed as the round-62 class census. Proposal 2 (`tb2_grader_admit`, one standing parametrised TB2
  admission counter with a committed filler control) is **open**: `grep -rn 'tb2_grader_admit' plans
  corpus SCORECARD.md SKILL.md` hits only `corpus/lessons/round-66.md:332`, and `plans/` carries no
  standing admission counter by that name. It is a separate instrument and is **not** mined this
  round (no implementing artifact to cite, and it does not serve either frozen claim).
- **Assimilation: none.** `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was not adopted; the mass
  id drift stays open at L0 `kengaku | round-54` and adoption would need a ~120-row renumber map
  (CORPUS.md rule 2, append-only).
- Knowledge entries: none admitted this round (both claims are instrument work; no new domain fact).

## Census and instrument readings

- `sources-census.sh validate --root … kengaku` → rc 0 at round start (244 rows, 25 `W04`,
  `corpus/evidence/round77/census-before.txt`, measured on a scratch clone at `07c97fcd`) and rc 0 at
  round end (245 rows, same 25 `W04`, `census-after.txt`).
- R77-C1 before (`--rev 07c97fcd`): `CANONICAL source=none rows=0`, `UNLISTED n=33`, `RESOLVED
  live=0`, `DEFECTS n=34`, `PREDICATE R77-C1 fail`, rc 1 → after: `TARGET total=28 unlisted=0
  live=27 agree=28 disagree=0`, `DEFECTS n=0`, `PREDICATE R77-C1 pass`, rc 0.
- R77-C2 before: `SCOPE ids=7 registered=0 closed=0 open=0 discharged=0 legs_passed=0
  legs_pending=2 wrong=12`, rc 1 → after: `registered=7 closed=7 discharged=7 legs_passed=7
  legs_pending=0 wrong=0`, rc 0.

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M77-1 scope | inserting the canonical `## Declared surfaces` section at the top of `PROVINCE.md` moved `### Adjacent` off line 129 and made `plans/state_check.py --summary` report a second `MISMATCH: P3c.box.4.pointer.1` on top of the base's one | first run of `state_check.py --summary` after the insertion: 2 `MISMATCH` lines vs 1 at base | the pinned-pointer checker itself; PROVINCE is append-only in practice, so the section landed at the file's end and the mismatch count returned to the base's 1 |
| M77-2 counter-false-red | the C1 fixture's `### Superseded` heading was not in the counter's `SUPERSEDED` tuple, so `--mutants` reported `NO-TRIGGER` for `drop-unlisted` while the mutation was actually unexercised | `MUTANT drop-unlisted NO-TRIGGER expected=UNLISTED-SURFACE` on the first matrix run | the mutant matrix's own `NO-TRIGGER` branch (added this round); the fixture heading now names `### Historical — absent, not governed`, which the counter reads |
| M77-3 vacuous-mutant | the first C2 mutant matrix asserted the expected defect class *appears* in the mutant's output, so every mutant "survived" while in fact removing a check only removes a class | `MUTANTS real=6 expected_matched=0 survived=6` on the first run | the matrix now runs the clean gate on a triggering fixture first and kills a mutant only when the clean gate fires the class and the mutant does not (`NO-TRIGGER` when the fixture is wrong) |
