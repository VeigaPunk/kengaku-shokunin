# kengaku round 96 — frozen claims

Frozen at commit F of round 96 (the single commit that adds this file). Author: kengaku (L1
KengakuR96, hyaku run 15, attempt 1). Base: `45740a616028015b5dfcf9900753e3bb5e6fe689` (lane tip
at round start; clean, pushed; round 95 closed). P0 mechanism predictions, capture, census start
and the standing-counter BASE receipts: `ff6765a662425d65ead297bc0c9fd86f5577be5f`. Instruments P1
`cea469bd8c007b7ff60a22a82df72068f03559eb`, battery grow leg P1b
`e8a80c0e23f8a2b365756b4e971b4210afa3f829`. Control receipts P2: `a3b5732104cb4e36cdefa4a070fc453f88bfaecd`
(`.ufo/waves/round-96/L1/controls/README.md`).

Order (kept from rounds 93–95): P0 predictions and population → P1 every instrument → P2 every
do-nothing, forgery, positive and separability control executed against P1/P1b bytes and
committed → F this file with the sha256 of every instrument → the official probe run, ledger flip,
counter repairs and SOURCES rows (C) → measurement at T. **No file in the frozen-instruments table
changes after F.** An instrument defect found after F is routed to round 97 and the affected claim
is reported not met; it is never repaired in round.

```frozen-instruments
78ce14ceab7156c230536e02aeb42abd2f49daaed737213a5f97a2f0ef776f17  plans/round96_merger_probe.py
b5efb7b004730ebd6756c32471fccc84bb91c9833faf82be000a894adf3d5354  plans/round96-cases.json
0752287902145fe1adc49f985978905244dc906f1015eb88874b39182bf8940c  plans/round96_c1_replay.py
989eb10f31b23beb3f34c9fa33a5e47a79230d77ce197d4899a64aea780d2c99  plans/round96_standing_battery.py
a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5  corpus/evidence/round96/graders/multi-source-data-merger/tests/test_outputs.py
d5a00e64413c0e1ae452f38a1aa1a47c3ed7b4416bbfccae1a4c053025a336d1  corpus/evidence/round96/graders/multi-source-data-merger/tests/test.sh
1b3d0d50e31930d042495d48f4c8e95f1a9c1a979c803b7f7cec651322537e1e  corpus/evidence/round96/graders/multi-source-data-merger/solution/solve.sh
c95a40d3d35b473dc15ae1e8784ba7fb1725805c0583fc574dd2764325d75e4f  corpus/evidence/round96/graders/multi-source-data-merger/environment/Dockerfile
75e51e2d3ab0bdba2269d7cf3757576f84f3ee2c13407d2db94289a5958a1778  corpus/evidence/round96/graders/multi-source-data-merger/environment/data/source_a/users.json
8e87d16dc47d166edd8e56165955bad265b630d53d02762367c816affb5fa760  corpus/evidence/round96/graders/multi-source-data-merger/environment/data/source_b/users.csv
23d1ea51c4170bdba53febb885a0f495e28de525a52667347b2932136b9a72fe  corpus/evidence/round96/graders/multi-source-data-merger/environment/data/source_c/users.parquet
```

The R96-C2 repair is pre-committed byte-exactly: C lands exactly these seven files (sha256 of the
whole file; the diff is `.ufo/waves/round-96/L1/controls/candidate-edits.diff`). These are the
claimed work, not instruments; a defect found in them after F makes R96-C2 not met.

```candidate-bytes
52ab93c021743c45aa380b9c852e61480550b2ae428143d774ba69f400e5a661  plans/round87_c1_replay.py
f96014625fe90d27442c2319c720e85cea64a14f4b6941bbb4eae82c886cc5eb  plans/round90_c1_replay.py
2be919c5f57d3c4f289e1494a67994e665b84fb4a8f3177709194acc8d51ab4a  plans/round91_c1_replay.py
092ba438623f3ef7e6a6221b35b7f46f1f096111ec7a853f5c7d8a6becf9d0db  plans/round92_c1_replay.py
78edd3a6abb6ffe92d104ea7e00dada9e93b74ef62bc926b46677061e122937f  plans/round93_c1_replay.py
44e38899bbbb3035ba2042dfa63eb70aa64952280111321bb5d806581bcecbf9  plans/round94_c1_replay.py
110d7fd72608b52222e064e8ff7aa8d18a25725255a6e090684a49a91f48be6b  plans/round95_c1_replay.py
```

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the
measurement. The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing
is the host table. Wave findings are routed, not repaired (frozen rule above).

## R96-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A fourteenth located offline replay of a pinned Terminal-Bench 2.0 grader:
`multi-source-data-merger` @ `2fd12b88` (classes `file-artifact`, `serialization-schema`), through
`plans/round96_merger_probe.py`: the agent side is modelled by a venv with the Dockerfile's pins
(python 3.11, pandas 2.2.3, pyarrow 17.0.0), the verifier side by a venv with `tests/test.sh`'s
uvx pins (python 3.13, pandas 2.3.3, pyarrow 22.0.0); 17 cases × 4 observed legs (each of the
grader's three test functions, and the reward bit `tests/test.sh` derives from them); the captured
`solve.sh` runs unmodified as the positive control. Unlike round 95, `tests/test.sh` runs only
`test_outputs.py`, so the reward leg is the member's reward rule, not a narrowed scope. The
population ledger flips the member to `executed` (round 96) with `receipt`, `subject`, `verdict`.

Sources: S310–S314 admitted, S315–S316 rejected (rows land in C; opened 2026-11-05 22:30 -03).

**Venv staging** (network, before the probe; the probe itself runs with no network):
`uv venv -p 3.11 E && uv pip install --python E/bin/python pandas==2.2.3 pyarrow==17.0.0`;
`uv venv -p 3.13 G && uv pip install --python G/bin/python pandas==2.3.3 pyarrow==22.0.0`
(numpy is unpinned on both sides, as in the task; the receipt stamps the resolved versions).

**Frozen predicate.** At the measured tip T, from the lane root:
`python3 plans/round96_c1_replay.py --lane . --rev T --work DIR --env-venv E --grader-venv G`
prints `LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`, then
`TARGET executed_rows=40 member=multi-source-data-merger cells=file-artifact:31,serialization-schema:7 set_contains_base=1 located=1 executed=1 cases=17 legs=68 mismatches=0 defects=0`,
then `PREDICATE R96-C1 pass`, exit 0. Ledger after: executed 39 → 40 of 88, `file-artifact`
30 → 31 of 76, `serialization-schema` 6 → 7 of 10, executed member set ⊇ BASE's plus the member.

**Predictions.** Filed from mechanism at P0 (`.ufo/waves/round-96/L1/predictions-mechanism.txt`)
before any probe run; 17 of 17 held in dry run 1 (`.ufo/waves/round-96/L1/dryrun/probe-dryrun-1.txt`).
Decisive grading-gap cases: C04 (an under-reporting conflict report passes: the email check is
guarded by `if email_conflicts:`), C06 (users 102/103 never content-checked), C07 (float64
user_id passes the stated integer requirement); edges C09 (datetime64 date fails), C12 (KeyError,
not an assertion), C16 (ArrowInvalid).

**Kill rule.** Not met if any leg fails at T, if the predicate prints anything but `pass`, or if
a frozen file changes after F.

## R96-C2 — calibration (held at ceiling 10): standing C1 counters red while recorded met

**Claim.** The lane's SCORECARD records each of fourteen C1 counters (round 79 population gate,
rounds 83–95 replay counters) as met. At BASE six of them are red at the lane tip (round 79:
`SUBJECT-MISMATCH mteb-retrieve`; rounds 90–94: L7 pins an absolute executed total) — six
self-assessment mismatches. The repair keys L7 of rounds 90–95 to the executed member SET of each
round's own BASE (growth-tolerant, removal-sensitive) and re-pins round 87's ledger subject to the
round-79 gate's frozen shape (`tb2-header`) with the ledger cell set to match.

**Frozen predicate.** At T, from the lane root:
`python3 plans/round96_standing_battery.py --lane . --rev T --work DIR` prints
`STANDING total=14 green=14 red=0`, `BITES checked=12 bitten=12`, `GROWS checked=6 tolerant=6`,
then `PREDICATE R96-C2 pass`, exit 0. BEFORE (P0 `ff6765a6`, `dryrun/battery-base.txt`):
`STANDING total=14 green=8 red=6`, `PREDICATE R96-C2 fail`.

**Controls (P2, executed before F; fixture clones, `controls/c2-*.txt`).** do-nothing at a
C1-landed tip (`c1-only`): red 7 (round 95's L7 pins 39 too) → fail; forgery deleting L7
(`delete-l7`): green 14 but bitten 0 → fail; forgery re-pinning L7 to the absolute total 40
(`repin-abs`): bites pass, grows fail → fail; positive (`full`, the candidate bytes + C1 flip) →
pass; separability (`c2-only`, the candidate bytes without the C1 flip) → pass.

**Kill rule.** Not met if the predicate is not `pass` at T, if C lands bytes other than the
candidate-bytes table, or if a frozen file changes after F.

**Separability.** C1 is verifiable without C2 (its L7 is member-set keyed; its own counter is not
in the battery population). C2 is verifiable without C1 (`c2-only` control).
