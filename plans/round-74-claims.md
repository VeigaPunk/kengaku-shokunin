# Round 74 — kengaku — frozen claims (R74-C1, R74-C2)

Frozen before data: `2026-11-04T03:50:00Z` (L1 `KengakuR74`), base tip `b7910802549978404218937d4be6a75acae0e020` (round-73
verifier spot-check). This file names the claim sentence, the counting command, the target, the
control and the kill rule for each claim. Nothing below changes after a seat scores it.

Round shape: one v1 wave, 16 seats (see `.ufo/waves/round-74/w1-dispatch.json`). The L1 holds the
canonical planner seat; a bounded planning data-walk rides the `scout` item (`RoundStateScoutR74`).

## R74-C1 — coverage (lowest non-retired axis, L0-capped at 7)

**Claim.** The registry-completeness gate decouples advertised universe discovery from `SKILL.md`'s
`## Gate/probe registry` table (scanning `SKILL.md` strictly outside the registry block, plus `SCORECARD.md`,
`LOG.md`, `corpus/README.md`, `corpus/knowledge/*.md`, and `plans/*.md`), fixes regex matching for
hyphenated directory and file names `[A-Za-z0-9_.-]+`, and verifies that every advertised instrument has
a valid registry row without circular self-advertising.

**Frozen sentence (the predicate, in one sentence).** `python3 plans/round74_c1_registry.py --lane .`
prints `UNIVERSE mode=decoupled`, `ADVERTISED total=116`, `REGISTERED total=116 rows=116`, `MISSING 0`,
`INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R74-C1 pass` and exits 0,
and `python3 plans/round74_c1_registry.py --selftest` prints `SELFTEST cases=4 failures=0`.

**Counting command (both states).**

    python3 plans/round74_c1_registry.py --lane . ; echo "rc=$?"

**Before** (measured on the frozen instrument under `--universe legacy` reproducing the pre-round-74 universe:
`UNIVERSE mode=legacy files=52 plans_seen=0 plans_only=0`, `ADVERTISED total=110`, `MISSING 5`,
`PREDICATE R52-C2 fail`, `PREDICATE R74-C1 fail`, rc 1) — receipt `corpus/evidence/round74/c1-before.txt`.

**After (target).** The frozen command prints `UNIVERSE mode=decoupled`, `ADVERTISED total=116`,
`REGISTERED total=116 rows=116`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`,
`DUPLICATE 0`, `PREDICATE R74-C1 pass`, rc 0.

**Control (cheapest skip; committed at freeze).** `--universe legacy` reproduces the pre-amendment
universe: `ADVERTISED total=110`, `MISSING 5`, rc 1. On an isolated fixture where an advertised instrument's
registry row is removed, decoupled mode raises `MISSING 1` (rc 1) whereas the legacy counter drops the
instrument from both adv and reg, falsely remaining green. Receipts: `corpus/evidence/round74/c1-before.txt`
and `corpus/evidence/round74/c1-control-decoupled.txt`.

**Kill rule.** The claim fails if any required line above is absent or differs at the landing tip,
or if selftest regresses.

**Grounding commands in self-assessment documents (prose references).**
The decoupled scanner reads runnable commands from self-assessment documents outside the registry table:
- `python3 plans/anchor_digest_check.py`
- `python3 plans/ledger_tip.py`
- `python3 plans/pkg_gate.py`
- `python3 plans/round39_c1_audit.py`
- `python3 plans/stage_scan.py`
- `python3 corpus/evidence/round13-coverage/coverage_census.py`
- `python3 plans/round74_c1_registry.py`
- `python3 plans/round74_c2_registry_audit.py`

## R74-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The lane's registry audit counter (`plans/round74_c2_registry_audit.py`) prices all four
blind spots identified in round 73:
1. Malformed table lines (columns != 8) are reported as named defects (`MALFORMED-ROW columns=<n>`)
   rather than silently dropped;
2. Entry flags declared in command syntax are verified against the script body (`D2 <name>:entry:unbacked-flag:<flag>`);
3. Self-test runner script existence is verified (`D2 <name>:self-test:script-absent`);
4. Errata revision consistency is enforced across all matching items (`ERRATA:contradictory-revision`),
reporting `MISMATCH 0` on the clean tree, while discriminating on all false-green fixtures from round 73.

**Frozen sentence (the predicate, in one sentence).** `python3 plans/round74_c2_registry_audit.py --lane .`
prints `INSTRUMENTS total=116 derived=registry rows=116`, `PARSED scripts=116 failed=0`, `D1 ok n=0`,
`D2 ok n=0`, `D3 ok n=0`, `D4 ok n=0`, `MALFORMED ok n=0`, `MISMATCH 0`, `DEFECTS n=0`,
`PREDICATE R74-C2 pass` and exits 0; `--selftest --work DIR` prints `SELFTEST arms=4 red=3 ok=True`;
`--mutants --work DIR` prints `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=1`.

**Counting command (both states).**

    python3 plans/round74_c2_registry_audit.py --lane . ; echo "rc=$?"

**Before** (measured on a fixture lane with a 9-cell malformed row: round-73 audit prints `MISMATCH 0`,
`DEFECTS n=0`, `PREDICATE R73-C2 pass`, rc 0 — silent drop; round-74 audit prints `MALFORMED defect n=1`,
`DEFECT MALFORMED-ROW columns=9`, `MISMATCH 1`, `DEFECTS n=1`, `PREDICATE R74-C2 fail`, rc 1) —
receipt `corpus/evidence/round74/c2-red-before.txt`.

**After (target).** `MISMATCH 0`, `DEFECTS n=0`, `PREDICATE R74-C2 pass`, rc 0 on the clean lane.

**Control (cheapest skip; committed at freeze).** The malformed row fixture: round-73 audit silently
drops the row and passes (`rc 0`), while round-74 audit flags the malformed line (`rc 1`).
Receipt `corpus/evidence/round74/c2-control-malformed-tuple.txt`.

**Kill rule.** The claim fails if any defect is reported on the landing tree, if any selftest arm
fails, or if any mutant survives.

## Frontier step (not a claim)

- `corpus/SOURCES.md` gains S250 (Python 3 `argparse` documentation, tier A) opened this round with a live
  fetch, capture and located quote; grounds `corpus/knowledge/registry-argv-and-flag-audit.md` (held).
- `corpus/lessons/round-74.md` carries `## Gate` and `## Mistakes`.
- Census before → after with `scripts/sources-census.sh validate --root … kengaku`.

## Amendment A1 — the R74-C1 Before description (appended 2026-11-04T00:55Z, before any seat returned)

The R73-C1 **Before** bullet above describes the legacy control with "ADVERTISED total=110,
MISSING 5" — that was the round-73-era legacy state, before round 73's own amendments
registered the five missing rows.  Measured against the committed receipt
`corpus/evidence/round74/c1-before.txt` at the freeze base, the legacy run actually prints
`UNIVERSE mode=legacy files=78 plans_seen=0 plans_only=0`, `ADVERTISED total=115`,
`REGISTERED total=115 rows=116`, `MISSING 0`, `PREDICATE R52-C2 pass`, `PREDICATE R74-C1 fail`,
rc 1.  The substantive before-state is unchanged: legacy cannot detect dropped unreferenced
rows (self-advertising masks incompleteness) and never sees `plans/*.md` instruments, so it
can never satisfy `PREDICATE R74-C1`.  The frozen predicate, counting command, after-target,
control and kill rule are unchanged.  No seat had returned when this amendment landed.
