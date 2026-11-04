# Round 77 — kengaku — declared claims (frozen before data)

Base: `07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59` (round-76 verifier spot-check).
Frozen 2026-11-04 by L1 `KengakuR77`. Nothing below may be re-worded after a seat has scored it
(PROTOCOL §9): predicate, counter, target, control and kill rule are the same sentence here, in the
counter's code and in the receipt label.

Round shape: ONE v1 wave, 12 seats (executor 3, scribe 2, scout 1, connector 1, reviewer 1,
critic 1, mutation-tester 1, sentinel 1, distiller 1). Attack roles 5/12 = 41.7 % (≥25 %);
connector 1 (≤2). The L1 holds the §3 planner seat (the validator rejects `planner`); the planning
data-walk rides the scout item.

Why these two claims, and no third. `SCORECARD.md`'s axes after round 76 read coverage **7**
(lowest non-retired axis, capped by the open L0 at `round-25`), calibration **10**, operability 10,
depth 10, freshness 10, adjacency 9, novelty 8. The lowest non-retired axis is coverage, and the
round-76 closure itself recorded the routed item this round's C1 discharges: "the `### Core`
declarations are recorded as a routed item for a future claim (an all-declarations inventory needs
an authoritative supersession of the older tables, not another row in this one)"
(`corpus/lessons/round-76.md`, §Amendment A8). C2 discharges the same closure's seven routed defect
ids, which is the standing burn-down duty every round carries.

## R77-C1 — coverage (lowest non-retired axis, L0-capped at 7): one canonical declared-surface inventory, every row resolved live, every declaration agreeing

**Claim.** The lane stops declaring surfaces in three tables that no single command reads. A new
canonical table (`PROVINCE.md` → `## Declared surfaces — canonical, machine-checked`) carries every
surface the three older tables declare — 28 rows across the kinds `path`, `http`, `tcp`, `hash`,
`count`, `cmd`, `exec`, `remote` — and its `Supersedes` cell names the older declaration it
replaces. The gate `plans/round77_c1_declared_surfaces.py` resolves every row *live* under one rule
(`test -e`, loopback HTTP status, TCP connect, recomputed sha256 pin, recomputed row count, committed
run receipt, or a dated no-egress `REMOTE` marker), requires a dated `ABSENT YYYY-MM-DD` marker
exactly where the host answers absent, and reports `UNLISTED-SURFACE` for every row of the three
superseded tables that no canonical row carries.

**Axis named by the surface it moves.** Coverage is scored as "PROVINCE.md lists every surface; none
unexplored without reason". The surface this round moves is *the declaration's universe*: 11
machine-read rows → 28, with three probe classes the lane never machine-checked (hash pins, count
pins, run receipts) and a supersession leg that makes a deleted or un-listed declaration a defect.
It is not a re-score of round 76's table gate: that gate keeps its own universe and stays green.

**Before** (`corpus/evidence/round77/c1-before.txt`, `--rev 07c97fcd`):
`CANONICAL source=none rows=0`, `SURFACES total=0 present=0 absent=0 remote=0`, `UNLISTED n=33`,
`RESOLVED live=0`, `AGREE agree=0 disagree=0`, `DEFECTS n=34`, `PREDICATE R77-C1 fail`, rc 1. The 33
are the row count of the three older tables that carry a resolvable anchor (11 + 10 + 12 measured
at base), each unread by any machine check.

**Target (after).** At the landing tip the frozen command prints
`TARGET total=28 unlisted=0 live=27 agree=28 disagree=0 defects=0`, no `DEFECT` line,
`PREDICATE R77-C1 pass`, rc 0. `live=27` because the remote-API row is declared `REMOTE` and is
never probed (the gate keeps no egress); it is the only row whose verdict does not come from the
host.

**Counting command.** `python3 plans/round77_c1_declared_surfaces.py --lane .`

**Control that must lose** (`corpus/evidence/round77/c1-control-declared.txt`): accept each row's own
declaration as if resolved — on a fixture whose declaration lies (`absent ABSENT 2026-11-01` on a
path that exists) it prints `CONTROL rows=7 declared_verdicts=7 agree=7 live=0 target_reached=False`:
a declaration-trusting counter can reach `agree=` but never `live=27`, and it cannot see the
`STALE-ABSENT` the live rule catches. The mutant `trust-declared` in the counter's own matrix shows
the same class on the same fixture.

**Kill rules.** (a) any `DEFECT` line; (b) `UNLISTED n=` not 0; (c) any of the five `TARGET` fields
short; (d) a `SURFACE` line whose verdict is not one of `present|absent|remote`. Selftest battery
`cases=6 red=5`; mutant matrix `real=6 expected_matched=6 survived=0` (each mutant is killed by the
class it makes disappear on a fixture that fires it).

**Stated limits.** `live=27` is the counter's own probe loop; its independent content is the
per-row identity each `SURFACE` line prints (`path=`, `http=`, `tcp=`, `sha256=`, `rows=`,
`receipt=`) and the `AGREE` leg computed from the live verdict against the row's own words. The
`hash`/`count` rows read declared bytes at `--rev` and worktree bytes otherwise, so a receipt taken
at a revision measures that revision. `remote` rows are never probed by design.

**Causal separability.** C1 reads `PROVINCE.md` and the host only. It needs no ledger row, no
correction block and no round-76 receipt: its target holds whether or not C2 lands, and C2's target
holds whether or not the canonical inventory exists (`--rev 07c97fcd` prints the same C2 verdict
with or without C1's bytes).

## R77-C2 — calibration (held at ceiling 10, exercised): the round-76 closure's seven routed defects become a burn-down whose discharges re-derive at the commit that carries them

**Claim.** `corpus/routed-findings.jsonl` becomes the register for the newest closure's routed ids
(`R76-V1` … `R76-V7`, named in `corpus/lessons/round-76-verifier-spotcheck.md` §6), and each
discharge is priced by a leg that re-derives its value at check time: the two round-76 C1 battery
receipts must carry a `TOOL_SHA` equal to the counter's sha256 **at the receipt's own `LANE_TIP`**;
the two round-76 `SKILL.md` registry rows must carry the final tallies and the A5/A8/A9 defect
classes; `LOG.md`, `corpus/lessons/round-76.md` and `SCORECARD.md` must each carry an appended,
dated correction naming **both** the superseded and the corrected value; `LOG.md` must carry the
`Second-reviewer classes` block the report's commit R pointed at; the `considerthese` re-adjudication
must record proposal 2 (`tb2_grader_admit`) as open; one capability name must hold in `PROVINCE.md`
and `SCORECARD.md`; and three stamped rerun receipts must carry an ancestor `LANE_TIP`, a `TOOL_SHA`
matching that tip's tool bytes, and a passing predicate line.

**Before** (`corpus/evidence/round77/c2-before.txt`, `--rev 07c97fcd`):
`SCOPE ids=7 registered=0 closed=0 open=0 discharged=0 legs_passed=0 legs_pending=2 wrong=12`,
`DEFECTS n=12`, `PREDICATE R77-C2 fail`, rc 1 — the closure's seven defects never entered the
ledger, and five of the seven legs fail on the base bytes.

**Target (after).** At the landing tip: `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7
legs_passed=7 legs_pending=0 wrong=0`, `DEFECTS n=0`, `PREDICATE R77-C2 pass`, rc 0.

**Counting command.** `python3 plans/round77_c2_defect_discharge.py --lane .`

**Control that must lose** (`corpus/evidence/round77/c2-control-status.txt`): register the seven ids
as `closed` with a trivial check and stale evidence —
`CONTROL rows_claimed_closed=7 trivial_checks=7 failed_legs=3 defects=7 target_reached=False`.

**Kill rules.** (a) any `MISSING-ROW`, `OPEN`, `NO-CLOSE-COMMIT`, `CLOSE-NOT-ANCESTOR`,
`CLOSE-UNRESOLVED`, `NO-VERIFIED-AT`, `CHECK-TRIVIAL`, `NO-EVIDENCE-FIELD`,
`EVIDENCE-ABSENT-AT-CLOSE`, `EVIDENCE-LITERAL-MISSING`, `NEGATED-DISCHARGE`, `EMPTY-SCOPE`,
`LEG-FAIL` defect; (b) any of the eight `TARGET` fields short. Selftest `cases=10 red=9`; git arms
`3/3` (ancestor / not-ancestor / unresolved); mutant matrix `real=6 expected_matched=6 survived=0`
(each mutant is killed by the class it makes disappear on a fixture that fires it).

**Stated limits.** `CHECK-TRIVIAL` is syntactic (a path-shaped token plus a quoted literal), not
execution; the leg reads markdown after stripping HTML comments and fences, so a commented-out
correction cannot satisfy it; and the `V1`/`V7` tool-sha leg proves the receipt was produced by the
tool bytes at its stamp, not that the run was honest — provenance of a live run stays the
reviewer's read.

**Causal separability.** C2 changes the ledger, five correction blocks, three receipts and two
registry rows; it never writes `PROVINCE.md`'s canonical inventory or the C1 counter, and C1's
target is independent of every C2 byte.

## Sources and frontier (§2b)

- **S253 (admitted this round)** — Git `git-cat-file` documentation for reading a repository
  object's bytes at a named revision: https://git-scm.com/docs/git-cat-file, opened live
  2026-11-04, capture `corpus/evidence/round77/sources/git-cat-file.html` (HTTP 200, 79 488 B,
  sha256 `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`), located quote at
  capture lines 2584–2585, 15 words: "If <type> is specified, the raw (though uncompressed)
  contents of the <object> will be returned." It grounds both counters' at-revision reads
  (`git cat-file blob <rev>:<path>`): C1's `hash` rows recompute a pin from the revision's own
  bytes, and C2's `TOOL_SHA` leg compares a receipt's stamp against the tool at that stamp.
- **Rejected this round** — "a receipt that names a revision was produced by the tool committed
  there". The same page establishes that an object id names bytes; it says nothing about which tool
  read them. The round-76 closure's R76-V1 is exactly that failure. Flip: stamp `TOOL_SHA` inside
  the receipt and recompute the tool's digest at the stamped commit (C2's V1/V7 legs).
- **Frontier.** `corpus/README.md` §Frontier gains no new entry; the round repairs the declaration
  inventory and the burn-down. `considerthese/2026-10-26.md` proposal 2 (`tb2_grader_admit`) is
  re-adjudicated in `corpus/lessons/round-77.md` and stays **open** — it is a separate instrument,
  not this round's claim. Assimilation: none (the kengaku package's mass id drift stays open at L0
  `round-54`; adoption would need a ~120-row renumber map).

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ rc 0 at round start, 244 rows, 25 `W04` duplicate-URL warnings (`corpus/evidence/round77/census-before.txt`);
rc 0 at round end, 245 rows (S253), the same 25 warnings (`census-after.txt`).

## Amendment A1 (2026-11-04, leg strengthened before the after-state, target unchanged) — V7 accepts a report-only tool's own verdict form

The frozen R77-C2 leg V7 read "a `PREDICATE … pass` line". `plans/routed_open.py` is a report-only
gate: it prints `ROWS total=… open=… closed=…` and exits 0, and it has no `PREDICATE` line to print.
The leg now requires, for every one of the three receipts, `EXIT 0` **and** — when the receipt carries
a `PREDICATE` line — that the line says `pass`; a receipt whose tool printed a failing predicate is
still a failure. The predicate, the eight `TARGET` fields and both controls are unchanged; the leg can
only add defects, never remove one. The minting driver
(`plans/round77_remint_r76_batteries.py`) now appends `EXIT <rc>` to every receipt, so the clause is
re-derivable from the receipt bytes alone.

## Amendment A2 (2026-11-04, control reported to its receipt, target unchanged) — the status-only control loses on the ledger legs

The R77-C2 control line above reads `failed_legs=3 defects=7`. The committed receipt prints
`CONTROL rows_claimed_closed=7 trivial_checks=7 failed_legs=0 defects=7 target_reached=False`: the
fixture's legs all pass, and the skip is caught where it should be — seven `CHECK-TRIVIAL`/
`EVIDENCE-*` ledger defects, `discharged=0`, so the target's `discharged=7` is unreachable. Only the
control's prose changes; its predicate, the eight target fields and both kill rules are unchanged.
