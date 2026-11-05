# kengaku round 95 — frozen claims

Frozen at commit F of round 95 (the single commit that adds this file). Author: kengaku (L1
KengakuR95, hyaku run 15, attempt 1). Base: `4524072dfae9c5e8210592b7c1da26959aa29dae` (lane tip at
round start; clean, pushed; round 94 closed). P0 mechanism predictions, capture, the C2 false-gate
population and its BEFORE receipts: `2457f0254efcef452591fc1ac691dc7670b1aded`. Instruments P1:
`16dcfed7ef4c9e2ac7d28568d855905a8457b20d`. Control receipts P2:
`7783e9cbc83c207a3eb09224de68050c383f68f0` (`.ufo/waves/round-95/L1/controls/README.md`).

Order (kept from rounds 93–94): P0 predictions and population → P1 every instrument → P2 every
do-nothing, forgery, positive and sandbox control executed against P1 and committed → F this file
with the sha256 of every instrument → the official probe run, ledger flip and SOURCES rows →
measurement. **No file in the table below changes after F.** An instrument defect found after F is
routed to round 96 and the affected claim is reported not met; it is never repaired in round.

```frozen-instruments
932e66b1e47662b687a4fe9994b09ebda8453e8dc2e0b1728569adbd9bb1c775  plans/round95_vuln_probe.py
ff361d141561a9763b68e478e8ff0257beb6f407fc9f41eda1ff6b5b8c0266e8  plans/round95-cases.json
c7e13dc9146ebc1fc3fcd07b404f985ce842e33fdea38c9a4cc21b3b3a7ff3e2  plans/round95_c1_replay.py
2fc2e7f0a1c26599c60f2f142c7d73a581974cb6949b65a90e9e3cbf08a13a7c  plans/round95_c2_counter.py
38fed2c23d46792ebf90295bac5d07072be71d8e35244ab1a4c48226d74334ba  plans/round95_false_gate_census.py
6b455d9e38c54eaca164e0043a6dbd2cb6c90ebcc2cf6d4ec5e2bae00dce8f9d  plans/round95-false-gates.tsv
8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de  plans/round94_freeze_integrity.py
c006a5de95b69bd78055aa26cc055734dbd50718ede25d331f767bfee4ef7f26  corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py
7a0131b369d83ae8546ecc3f9b4e23d38240f1bd1f0941e4430fa85b5182ee03  corpus/evidence/round95/graders/fix-code-vulnerability/solution/solve.sh
0917470986224df4daf4854a71302ae81c73ba5dd6e25be1232d29b758a5b3ab  corpus/evidence/round95/graders/fix-code-vulnerability/environment/Dockerfile
abf643683b4870e07500f8a035d1a076d4bf0bbf98eb2fb5180fbc3ef8fad802  corpus/evidence/round95/graders/fix-code-vulnerability/upstream-bottle/bottle.py
```

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the
measurement. The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing
is the host table. Wave findings are routed, not repaired (frozen rule above).

## R95-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A thirteenth located offline replay of a pinned Terminal-Bench 2.0 grader:
`fix-code-vulnerability` @ `2fd12b88` (classes `file-artifact`, `serialization-schema`), replayed
through `plans/round95_vuln_probe.py`: the task image's /app/bottle.py is rebuilt offline from the
captured upstream bottle.py @ bottlepy `0207a34f` with the Dockerfile's two oracle-removing sed
deletions; 15 cases × 7 observed legs (the outcome of each of the grader's six test functions and
the file the grader's `from bottle import _hkey` resolved to); the captured `solve.sh` runs
unmodified as the positive control. The population ledger flips the member to `executed`
(round 95) with the legacy-gate fields `receipt`, `subject`, `verdict`.

**Frozen predicate.** At the measured tip T:
`python3 plans/round95_c1_replay.py --lane . --rev T --work DIR` prints
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`, then
`TARGET executed_rows=39 member=fix-code-vulnerability located=1 executed=1 cases=15 legs=105 mismatches=0 defects=0`,
then `PREDICATE R95-C1 pass`, exit 0. Ledger after (L7): executed 38 → 39 of 88, `file-artifact`
29 → 30 of 76, `serialization-schema` 5 → 6 of 10, the executed member set equals BASE's plus
`fix-code-vulnerability`.

**Predictions.** Filed from mechanism at P0 (`.ufo/waves/round-95/L1/predictions-mechanism.txt`)
before any probe run; 15 of 15 held in dry run 1 (`.ufo/waves/round-95/L1/dryrun/probe-dryrun-1.txt`).
Decisive semantic legs: C11 (only `_hkey` patched — no function of the grader calls `_hval`, so a
half fix passes this file), C15 (a package `/app/bottle/__init__.py` shadows the vulnerable
`/app/bottle.py` on the same sys.path entry, so the grader passes while the reported file stays
vulnerable), C13 (an over-strict fix errors, not fails), C08/C10/C14 (report-schema edges).

**Controls (executed against P1, committed at P2).** do-nothing at BASE and at P1: all nine legs
fail, rc 1; receipt-side, on a scratch clone of P1 with a draft table of the P1 bytes: the honest
receipt + flip passes all nine legs, rc 0; probe swap with regenerated receipt (L8), foreign
LANE_TIP (L3), cases dropped (L5, L6), forged stamp (L6), legacy fields omitted (L7), ledger-only
flip (L1), member swap (L7) each rc 1; sandbox outage rc 2.

**Source (sourced claim, CORPUS rule 1).** New rows for the grader, the reference solution, the
Dockerfile's oracle-removal lines, the upstream bottle.py and the instruction, opened 2026-11-05
(HTTP 200, sha256 equal to the table above); `tests/test.sh` and `task.toml` are opened and
rejected as replay inputs.

**Kill rule.** Any failing leg, any DEFECT line, any mismatch, or `executed_rows` ≠ 39 at the
measured tip fails the claim; could-not-evaluate (rc 2) is not met.

## R95-C2 — calibration (held at ceiling 10)

**Claim (calibration content).** The lane's round-94 self-assessment: the freeze-integrity counter
discriminates forged gates ("kills the same 7 attacks", `plans/round-94-claims.md`; capability row
`freeze-integrity gate` v2). Observed at BASE on this host: **14** known false gates — built by
the round-94 wave on gate v2 and listed with sha256 in `plans/round95-false-gates.tsv` (frozen at
P0) — pass the frozen round-94 counter 5/5 (`controls/before-r94-counter-<id>.txt`, 14 × rc 0).
After: the round-95 counter (20 CLI fixtures, battery driven red by three probe mutations,
PREDICATE-line/rc agreement, ten CLI mutants) passes the unchanged honest gate v2 and fails all 14,
each at its designated leg. Known false gates passing the lane's counter: **14 → 0**.

**Frozen predicate.** At the measured tip T:
`python3 plans/round95_false_gate_census.py --lane . --rev T --work DIR` prints one `GATE` line
per row with `passes=0 designated_red=1`, `HONEST rc=0 predicate=pass`,
`FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, exit 0.
The honest run is `plans/round95_c2_counter.py --rev T` on `plans/round94_freeze_integrity.py` at T:
W1..W5 pass, where W4 reads this file's table with freeze = the single commit adding this file.

**Controls (executed against P1, committed at P2).** do-nothing — the census scoring the frozen
round-94 counter: `passing=14 designated_red=0`, rc 1; the census at P1 with the round-95 counter:
`passing=0 designated_red=14 honest=fail` (W4 only, no claims yet), rc 1.

**Scope (declared before data).** In-sample: the 14 are the recorded set the counter was built
against. M04, M10 and M18 are excluded with reasons in the tsv header (equivalence or no
observable). Discrimination of false gates the counter has not seen is not claimed; the wave is
asked to build new ones and they are reported beside the verdict.

**Kill rule.** `passing` > 0, `designated_red` < 14, an honest failure, or rc ≠ 0 at T fails the
claim; any tabled file changed after F fails W4 by construction.

## Separability

C1 is verifiable without C2 (its counter reads this file's table, not the gate or census); C2 is
verifiable without C1 landing (the census and counter read no C1 artifact; W4 reads only tabled
bytes, which exist at F before the C1 receipt and ledger flip).

## Not claimed (carried, with pointers)

The legacy `plans/round79_c1_population_ledger.py` repair (round-94 routed defect 5) lands as
conformance with its before/after counts in the report, not as a claim. Round-92 gate v3 defects
(override vacuity `plans/round92_burndown.py:306-329`, marker skip `:445`/`:558`), the unpinned
round-92 counters and the unguarded `cost_model_for_tests.py` stay open.
