# Round 73 — kengaku — frozen claims (R73-C1, R73-C2)

Frozen before data: `2026-11-04T02:45:00Z` (L1 `KengakuR73`), base tip `d96c3e62` (round-72
verifier spot-check). This file names the claim sentence, the counting command, the target, the
control and the kill rule for each claim. Nothing below changes after a seat scores it.

Round shape: one v1 wave, 16 seats (see `.ufo/waves/round-73/w1-dispatch.json`). The L1 holds the
canonical planner seat; a bounded planning data-walk rides the `scout` item (`PlansUniverseScoutR73`).

## R73-C1 — coverage (lowest non-retired axis, L0-capped at 7)

**Claim.** The registry-completeness gate's advertised universe gains `plans/*.md` — a claims
document naming `python3 plans/<instrument>.py` advertises that instrument to later rounds — and
under that widened universe every advertised instrument has a registry row.

**Frozen sentence (the predicate, in one sentence).** `python3 plans/round52_c2_registry.py --lane .`
prints `UNIVERSE mode=full`, `ADVERTISED total>=111`, `MISSING 0`, `INCOMPLETE 0`,
`ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R73-C1 pass` and exits 0, and
`python3 plans/round52_c2_registry.py --selftest` prints `SELFTEST cases=4 failures=0`.

**Counting command (both states).**

    python3 plans/round52_c2_registry.py --lane . ; echo "rc=$?"

**Before** (`d96c3e62`, the base gate bytes: `ADVERTISED total=110`, `MISSING 5`, `PREDICATE
R52-C2 fail`, rc 1) — receipt `corpus/evidence/round73/c1-before.txt`.

**After (target).** The frozen command prints `ADVERTISED total=112` (>=111; 2 instruments enter
the universe through the plans/ leg), `MISSING 0`, `PREDICATE R73-C1 pass`, rc 0.

**Control (cheapest skip; committed at freeze).** `--universe legacy` reproduces the pre-amendment
universe: `ADVERTISED total=110`, `MISSING 5`, rc 1. The cheapest *landing* cheat — adding the five
rows without widening the universe — reaches `MISSING 0` but cannot reach `ADVERTISED total=112`,
so it does not meet the claim. Receipt `corpus/evidence/round73/c1-control-legacy.txt` (legacy run)
and the gate's own `plans-fixture` selftest arm (a plans-doc-only instrument is MISSING under
`full`, invisible under `legacy`).

**Kill rule.** The claim fails if any required line above is absent or differs at the landing tip,
or if either selftest arm regresses.

**Work (not claim-narrowing).** Add the seven missing rows the widened universe exposes
(`plans/round32_c1_verify.py`, `plans/round32_defects.py`, `plans/round66_c1_tensor_probe.py`,
`plans/round69_c1_nginx_probe.py`, `plans/round69_c2_routed_defects.py`,
`plans/round70_c1_nginx_probe.py`, `plans/round70_c2_routed_defects.py`) plus a row for this
round's new instrument (`plans/round73_c2_registry_audit.py`) and the amended `round52-c2` entry;
every added row must satisfy the R73-C2 audit at the landing tip.

## R73-C2 — calibration

**Claim.** The lane's registry self-assessment is re-derived from committed bytes: a counter whose
instrument set is the registry's own rows, which prices every row's eight fields, keeps every row,
and binds each round-72 erratum item to its own revision, reports `MISMATCH 0` at the tip — where
the round-72 counter it supersedes reports `DEFECTS n=0` on the same tree while a fifth, a
duplicate second, and a mismatched erratum all pass it.

**Frozen sentence (the predicate, in one sentence).** `python3 plans/round73_c2_registry_audit.py
--lane .` prints `INSTRUMENTS total=106 derived=registry rows=106`, `PARSED scripts=106 failed=0`,
`D1 ok n=0`, `D2 ok n=0`, `D3 ok n=0`, `D4 ok n=0`, `MISMATCH 0`, `PREDICATE R73-C2 pass` and exits
0; `--selftest --work DIR` prints `SELFTEST arms=4 red=3 ok=True`; `--mutants --work DIR` prints
`MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=1`.

**Counting command (both states).**

    python3 plans/round73_c2_registry_audit.py --lane . ; echo "rc=$?"

**Before** (`d96c3e62`, frozen audit instrument over the base tree's bytes): `MISMATCH 2`, rc 1 —
receipt `corpus/evidence/round73/c2-red-before.txt`. The two defects are real row declarations the
round-72 counter never priced: `sources-adopt` is a `gate` whose verdict map declares no failure
class (`0,2,3,4,5,6,7,8,9`), and `round62-c1-class-survey` carries `kind=census gate`, outside the
`gate|probe` enum.

**After (target).** `MISMATCH 0` — the two row declarations corrected (verdict map states `failed`
for its non-zero refusal codes; kind becomes `gate`) — with `INSTRUMENTS total=106` and rc 0.

**Control (cheapest skip; committed at freeze).** Keep the round-72 counter's frozen four-instrument
tuple: on a fixture lane whose registry is the four real rows plus a fifth row with `kind=census
gate` and `owner=sibling`, `python3 plans/round72_c2_routed_defects.py --lane <fixture>` prints
`E1a ok … DEFECTS n=0`, `PREDICATE R72-C2 pass`, rc 0, while the frozen audit prints `MISMATCH 2`,
rc 1 on the same fixture. Receipt `corpus/evidence/round73/c2-control-frozen-tuple.txt`.

**Kill rule.** The claim fails if the audit prints any defect at the landing tip, if a required
selftest arm or mutant is absent/surviving, or if the instrument's own `--lane` run requires a
fixture. A rule changed after a seat scores is not this claim's rule.

## Frontier step (not a claim)

- `corpus/SOURCES.md` gains S249 (Python 3 `ast` documentation, tier A) opened this round with a live
  fetch, capture and located quote; the knowledge entry it grounds is `corpus/knowledge/
  instrument-registry-derivation.md`, cited by R73-C2's evidence.
- `corpus/lessons/round-73.md` carries `## Gate` (all rows opened this round) and `## Mistakes`.
- Census before → after with `scripts/sources-census.sh validate --root … kengaku`.

## Non-claims (corrections and bookkeeping, each with a re-deriving check)

1. The two SKILL.md registry row corrections R73-C2 prices (`sources-adopt`, `round62-c1-class-survey`).
2. The `round52-c2` registry row's entry cell gains `--universe {full,legacy}` for the amended gate.
3. The round-72 knowledge entry (`corpus/knowledge/tb2-hf-model-inference-offline.md`) stays on
   `admission: hold` this round: no second-wave falsify seats exist to discharge Q13/Q14 under the
   run-15 one-wave shape; the hold is re-recorded, not silently lifted.
4. The round-72 spot-check's three conformance defects (39-char hash, census-tip label, lesson sweep)
   are recorded in the round-73 lesson's `## Mistakes` with the criterion each one exposes.
