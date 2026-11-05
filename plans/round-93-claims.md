# kengaku round 93 — frozen claims (fresh start)

Frozen at commit F of round 93 (the commit that adds this file). Author: kengaku (L1 KengakuR93,
hyaku run 15, attempt 1). Base: `28e9f8bf4e8a68b1a34babfa71be9de595b78c4e` (lane tip at round
start; clean, pushed). Instruments P1: `17cb9337b99344814bc449d62eed771e29e33981`. Control
receipts P2: `0e77e98f77c2de1efcf1414de9a21689c2449548` (`.ufo/waves/round-93/L1/controls/`).

**Fresh start.** Rounds 90, 91 and 92 were closed `rejected-honest-stop` (MANIFEST indices 1333,
1342, 1361; spot-checks `corpus/lessons/round-9{0,1,2}-verifier-spotcheck.md`). The repeated root
failure is instruments edited after the freeze or after the first scored run (round 92: three
instruments, critic P1, lesson M8), plus controls written so the host cannot reproduce them
(M13). This round therefore runs in this order, and the order is the claim discipline:
P1 every instrument committed → P2 every no-work, forgery and sandbox control executed against P1
and committed with rc and leg lines → F this file, with the sha256 of every instrument below →
the official probe run and ledger flip → measurement. **No instrument in the table below changes
after F.** An instrument defect found after F is routed to round 94 and the affected claim is
reported not met; it is never repaired in round.

```frozen-instruments
6fad5d526217e08831b93b4f4280445d84715adf729c84fb785078fea01172d7  plans/round93_scheme_probe.py
078b04d2b0cdf5d1a3b4ade2b100f7c8d710a09c0f067d8af1efe75cec21c699  plans/round93-cases.json
89153db6e5254f3ef5ae9712189afd0a195965ff2608b473adfd7c4eddafc0fe  plans/round93_c1_replay.py
18b01b42fb54ce658dbb98ff3afd12d06600960fae46700fec9218e73bcefcb6  plans/round93_freeze_integrity.py
ac0e26a57b75e87038da7401c5209a01fb043a4ab7a6f5da8ec089574e33dfbc  plans/round93_c2_counter.py
993ed3cf5cff81f2bbc97696ab221e53800b37d81c2f651c51d285ef61152ba9  plans/round93_c2_forgeries/always_broken.py
5138d3546eee4409be0a993806b21d1cc9f881c6628eacdba2c9a67ea88a9383  plans/round93_c2_forgeries/always_intact.py
67d0b7576f2b8b9b19f32f515fa64962c536206d4f115d222b9269cd40c637d2  plans/round93_c2_forgeries/bytes_only.py
54bf34a2942663c9d9b74625b47e304b92e52b501306c4e3fdb03d42bb2a6102  plans/round93_c2_forgeries/log_only.py
```

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the
measurement: 11 seats — 3 executor, 1 scout, 1 connector, 1 scribe, 2 reviewer, 1 critic,
1 mutation-tester, 1 sentinel; attack share (reviewer, critic, mutation-tester) 4/11 = 36 %.
The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing is the host
table. Wave findings are routed, not repaired (frozen rule above).

## R93-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** An eleventh located offline replay of a pinned Terminal-Bench 2.0 grader:
`schemelike-metacircular-eval` @ `2fd12b88` (classes `file-artifact`, `stdout-inspection`,
`subprocess-exec`, `timing-wall`), replayed through `plans/round93_scheme_probe.py`: 8 cases ×
5 observed legs (outcome, passed, failed, total, timeouts) of the grader's own `test_interp()`;
the population ledger flips the member to `executed` (round 93).

**Frozen predicate.** At the measured tip T:
`python3 plans/round93_c1_replay.py --lane . --rev T --work DIR` prints
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`, then
`TARGET executed_rows=37 member=schemelike-metacircular-eval located=1 executed=1 cases=8 legs=40 mismatches=0 defects=0`,
then `PREDICATE R93-C1 pass`, exit 0. Class cells after (L7, from the committed ledger):
`timing-wall` 3 → 4 of 9, `subprocess-exec` 13 → 14 of 45, `stdout-inspection` 11 → 12 of 29,
`file-artifact` 27 → 28 of 76.

**Predictions (filed before the official run).** The eight vectors in `plans/round93-cases.json`.
They were observed in two pre-freeze scratch dry runs of the P1-candidate probe (disclosed: the
first run's C05 design hypothesis and the C08 stacking hypothesis were both wrong — 3 failures
predicted from mechanism, 7 observed — and the vectors were taken from the dry run, not from
mechanism; only the vectors are frozen). The decisive semantic legs: C07 (the grader passes with
no evaluator when no test programs exist), C06 (the 60 s through-eval timeout is the only failure
path that sets timeouts=1), C04 (one primitive mapping changed leaves 19 of 63 passing).

**Controls (executed against P1 and committed at P2 before this freeze).**
- do-nothing: the counter at BASE → `TARGET executed_rows=36 … executed=0`, all nine legs fail,
  `PREDICATE R93-C1 fail`, rc 1 (`controls/c1-base.txt`).
- forgery (ledger flip without any probe receipt, scratch clone of P1 with one fixture commit):
  rc 1: L7 passes (the flip itself) and L1–L6, L8, L9 fail (`controls/c1-forgery-ledger-only.txt`).
- sandbox outage (the round-92 M13 control, now injectable): `--bwrap /nonexistent/bwrap` → `DEFECT
  SETUP sandbox-unavailable`, `PREDICATE R93-C1 could-not-evaluate`, rc 2 (`controls/c1-sandbox-red.txt`).

**Source (sourced claim, CORPUS rule 1).** S290 (grader), S291 (interp.py), S292 (reference
solution), S293 (the 63 test programs), all opened 2026-11-05 at `2fd12b88`; S294 (test.sh)
rejected; S295/S296 (two other member candidates opened this round) rejected with flips.

**Kill rule.** Any failing leg, any DEFECT line, any mismatch, or `executed_rows` ≠ 37 at the
measured tip fails the claim; could-not-evaluate (rc 2) is not met. A mispredict is recorded,
never repaired.

## R93-C2 — calibration (held at ceiling 10) + capability `freeze-integrity gate`

**Claim.** The lane gains a gate that counts mismatches between what a claims file asserts was
frozen and what the repository holds: `plans/round93_freeze_integrity.py` (claims mode reads a
`frozen-instruments` table at the freeze commit; paths mode freezes the named paths' bytes at a
legacy round's freeze). An instrument is intact only if its freeze bytes match the table, its
bytes at the measured revision match, and no commit between touched it. Its ten-case battery runs
in-process in every invocation (no skip flag, no marker file, no child re-entry — round-92
M6/M10/M9). This is the round-92 routed defect 1 (M8): "no gate compares the counter bytes to the
freeze".

**Frozen predicate.** At the measured tip T: `python3 plans/round93_c2_counter.py --lane . --rev T
--work DIR` prints `W1 pass`, `W2 pass`, `W3 pass`, `W4 pass`, `TARGET legs_passed=4 of 4`,
`PREDICATE R93-C2 pass`, exit 0, where (the counter's docstring is the full definition):
- **W1** on the lane's real round-92 history (freeze B2 `f0018773`, tip `1df76536`): broken=3,
  intact=1, exactly `plans/round92_c1_replay.py` intact, rc 1 — the three mismatches between
  round-92 attempt 1's "met as frozen" and the bytes;
- **W2** five counter-owned fixture repos through the public CLI (intact rc 0, edited rc 1,
  edit-then-revert rc 1, lying table rc 1, unrelated edit rc 0);
- **W3** the gate's in-path `SELFTEST cases=10 ok=10`;
- **W4** this file's own table at T: instruments ≥ 6, broken=0, rc 0.

**Controls (executed against P1 and committed at P2 before this freeze).**
- do-nothing: the counter at BASE → tool absent, W1–W4 fail, `PREDICATE R93-C2 fail`, rc 1.
- four forgeries through the same counter path (`--tool-file`): always-intact fails W1 and W2;
  always-broken fails W1 and W2; bytes-only fails W2 on edit-then-revert; log-only fails W2 on the
  lying table — every forgery rc 1. W3 alone is shown worthless as evidence (every forgery prints
  the battery line), which is why W1/W2 exist.
- positive (blanket refusal is no gain): the real gate at P1 passes W1, W2, W3; W4 fails only
  because this file does not exist at P1.

**Calibration content.** W1's broken=3 is a count of the lane's own past self-assessment
mismatches; W4's broken=0 is the same count for this round. Score held at the ceiling 10; the
capability row enters the SCORECARD only if this predicate passes.

**Kill rule.** Any W leg failing at T fails the claim. Edits to any tabled instrument after F make
W4 fail by construction; that is the claim's own tripwire, not an exception.

## Separability

C1 is verifiable without C2 (its counter reads the table but not the gate); C2 is verifiable
without C1 landing (W1–W3 do not read C1 artifacts; W4 reads only instrument bytes, not the
receipt or the ledger).

## Not claimed (routed round-92 defects 2–6)

The round-92 gate v3 (`plans/round92_burndown.py`) override-vacuity (M9/M10(b)) and marker-skip
(M10) defects, the unpinned round-92 counters (M11) and the unguarded sibling
`cost_model_for_tests.py` (ScoutS283 F1) are not claimed this round; they are carried in the
round-93 lesson with their pointers. Routed defect 5 (injectable sandbox control, M13) is met by
construction in both new counters (`--bwrap`) and shown by the C1 sandbox-outage control.
