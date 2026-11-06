# kengaku round 97 — frozen claims

Frozen at commit F of round 97 (the single commit that adds this file). Author: kengaku (L1
KengakuR97, hyaku run 15, attempt 1). Base: `4992cd0e32b8db23ca20310deb7de12d485f8bcc` (lane tip
at round start; clean, pushed; round 96 closed `rejected-harmed`). P0 capture, mechanism
predictions and census start: `5b41c1c3e1a8e542d3a38c9f20965f7ea6404019`. Instruments P1
`b2352135e2b55e8017b6e9d1e7bc4d34d5062438`. Control receipts P2: `e40fd0c2a00ba95c190925a6ce066bc8354949ff`
(`.ufo/waves/round-97/L1/controls/README.md`).

Order (kept from rounds 93–96): P0 predictions → P1 every instrument → P2 every do-nothing,
forgery, positive and separability control executed against P1 bytes and committed → F this file
with the sha256 of every instrument and of every candidate byte → C: the official probe run and the
candidate bytes, nothing else → measurement at T. **No file in the frozen-instruments table changes
after F, and C lands exactly the candidate-bytes files plus the one receipt path named below.** A
defect found after F is routed to round 98 and the affected claim is reported not met; it is never
repaired in round. No closed round's frozen instrument is edited this round (Q79).

```frozen-instruments
13a4564d9431535f94465d5872b192e8d7173f1a87802bd298bcdb7c676f300b  plans/round97_sparql_probe.py
7b8462708d351d0c14939d128bce421eea41a92d220dc08da965614dcaa0bf01  plans/round97-cases.json
f736b04b938ce67eb8bac9fb9d748e67bbfe340d4e1ff2101b7ef8aa4c10c0c9  plans/round97_c1_replay.py
a255e83009bc137c40ba42b02c5c4d000dc6656343417d5e4319bd3395460b7f  plans/round97_gate_selftest_census.py
ecf15840fc14f1eeff2f3b6317d7f0febc8fa81f688d24e3054205ba13207b39  corpus/evidence/round97/graders/sparql-university/tests/test_outputs.py
45902b57bd0f1dd6959216bc9943ab27bb349edc7ff557035a1ecc8732e4cc6b  corpus/evidence/round97/graders/sparql-university/tests/test.sh
368ce01d32513ee04dfe592784b0c976086e514c1eab9b3165a016ca7b0192cb  corpus/evidence/round97/graders/sparql-university/tests/university_graph_test.ttl
d17995a8f29c6d656c749271fd28e10d31afee6aa75f40ad28fea1c907f2a791  corpus/evidence/round97/graders/sparql-university/solution/solve.sh
dd0abcd64e90ab16141169bcbf88a8e5f52732f207cb37765d351cc7a48916a9  corpus/evidence/round97/graders/sparql-university/environment/Dockerfile
0b0b1f2c0ee7ea7ddc9382f94ff8181996ffa7be60a1651111c1f57b49e09a85  corpus/evidence/round97/graders/sparql-university/environment/university_graph.ttl
```

C lands exactly these three files byte-for-byte (sha256 of the whole file) plus the probe receipt
`corpus/evidence/round97/sparql-probe.txt` written by the official run. They are the claimed work,
not instruments; a defect found in them after F makes the claim that owns them not met.

```candidate-bytes
739fb58bdfedc000fe8d2cf237e5603f87b621cdf2da6e01bd773d4c1a7b3df6  SKILL.md
567a26bbe05bee1710eee235ae97a885433104aa0dec8e9ebb6a68e13e6919db  plans/grader-population-ledger.json
c54a0ecea33fb1fc31314bc928077e0860502548be8544d216e6108511d0ce04  corpus/SOURCES.md
```

Ownership inside the candidate bytes: R97-C1 owns the ledger flip, the SKILL `file-artifact` class
cell (31 → 32 of 76), the two new probe rows `round97-sparql-probe` / `round97-c1-replay` and
SOURCES S317–S325; R97-C2 owns the 44 `kind` cells and the "Round-97 registry correction"
paragraph, and the new gate row `round97-gate-selftest-census`.

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the measurement
at T. The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing is the
host table. Wave findings are routed, not repaired (frozen rule above).

## R97-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A fifteenth located offline replay of a pinned Terminal-Bench 2.0 grader:
`sparql-university` @ `2fd12b88` (class `file-artifact`), through `plans/round97_sparql_probe.py`:
the verifier side is a venv with `tests/test.sh`'s uvx pins (python 3.13, rdflib 7.1.4, pytest
8.4.1); 18 cases × 4 observed legs (each of the grader's three test functions, and the reward leg —
real pytest over the captured `test_outputs.py`, not a derived bit); the captured `solve.sh` runs
unmodified as the positive control; the grader reads its own hidden graph
`tests/university_graph_test.ttl`, not the agent's. The population ledger flips the member to
`executed` (round 97) with `receipt`, `subject`, `verdict`.

Sources: S317–S322 admitted (tier A), S323–S325 rejected with flips (rows land in C; opened
2026-11-06 01:01 -03).

**Venv staging** (network, before the probe; the probe itself runs with no network):
`uv venv -p 3.13 G && uv pip install --python G/bin/python rdflib==7.1.4 pytest==8.4.1`
(pyparsing and the CPython micro are unpinned in the task; the receipt stamps them under
GRADER_UNPINNED, which L6 does not compare — round-96 W-2).

**Frozen predicate.** At the measured tip T, from the lane root:
`python3 plans/round97_c1_replay.py --lane . --rev T --work DIR --grader-venv G`
prints `LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`, then
`TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0`,
then `PREDICATE R97-C1 pass`, exit 0. Ledger after: executed 40 → 41 of 88, `file-artifact`
31 → 32 of 76, executed member set ⊇ BASE's plus the member.

**Predictions.** Filed from mechanism at P0 (`.ufo/waves/round-97/L1/predictions-mechanism.txt`)
before any grader run on the test graph; 18 of 18 held in dry run 2
(`.ufo/waves/round-97/L1/dryrun/probe-dryrun-2.txt`; dry runs 0 and 1 failed on probe defects,
`dryrun/README.md`). Grading gaps the replay locates: C05 (EU criterion never decides any
professor of the hidden graph), C06 (a NOW()-dated query passes), C10 (a literal VALUES answer
passes), C11 (duplicate rows pass — set comparison), C12 (an extra projected column passes); the
instruction-faithful per-department count and the solution's aggregate count are indistinguishable
on the hidden graph (C09); C17 shows the agent graph and the hidden graph name different professors.

**Kill rule.** Not met if any leg fails at T, if the predicate prints anything but `pass`, if a
frozen file changes after F, or if C lands bytes other than the candidate-bytes table and the
receipt.

## R97-C2 — calibration (held at ceiling 10): registry rows typed `gate` without a self-test

**Claim.** The lane's self-assessment of each tool is the `kind` cell of its SKILL.md registry row.
PROTOCOL §Gate standard requires every gate to expose a self-invocation self-test. At BASE, 44 of
127 rows typed `gate` name an entry script that exposes no self-invocation spelling (detector in
`plans/round97_gate_selftest_census.py`; list in `.ufo/waves/round-97/L1/c2-base.txt`) — 44
self-assessment mismatches against observed script bytes, among them the two round-96 rows the
round-96 spot-check routed (defects 3 and 4). The correction re-types exactly those 44 rows
`probe`, changing no other cell and no script.

**Frozen predicate.** At T, from the lane root:
`python3 plans/round97_gate_selftest_census.py --lane . --rev T` prints
`ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0`,
`GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0`,
`MISMATCH_TOTAL n=0`, then `PREDICATE R97-C2 pass`, exit 0. BEFORE (BASE `4992cd0e`,
`.ufo/waves/round-97/L1/c2-base.txt`): `GATES total=127 with_selftest=83 without=44`,
`MISMATCH_TOTAL n=44`, `PREDICATE R97-C2 fail`, rc 1.

**Controls (P2, executed before F; fixture clones, `controls/c2-*.txt`).** do-nothing (P1 bytes):
44 mismatches → fail; blanket forgery (every gate row re-typed `probe`): `DEMOTED` → fail; deletion
forgery (the 44 rows removed): `ROW-REMOVED` → fail; cell forgery (the 44 self-test cells rewritten
to claim `--selftest`, kind kept): `CELL-CHANGED` + `MISMATCH` → fail; script forgery (a
`"--selftest" in sys.argv` line appended to one closed-round script): `SCRIPT-CHANGED` → fail;
positive (the candidate bytes) → pass; separability (`c2-only`: the 44 kind cells and the paragraph,
without any C1 byte) → pass.

**Kill rule.** Not met if the predicate is not `pass` at T, if C lands bytes other than the
candidate-bytes table and the receipt, or if a frozen file changes after F.

**Harm check (pre-freeze, fixture clone, `controls/harm-pre-freeze/`).** Registry and ledger gates
at P1 vs the candidate+receipt fixture differ only in row counts and the `file-artifact` k:
r52-c2, r63 depth, r68 capability table, r72-c2, r73-c2, r74-c1, r74-c2, r75-c2, r78-c1, r79-c1,
r82-c1, grader.py — every exit code and every DEFECT line unchanged.

**Separability.** C1 is verifiable without C2 (`c1-only` control: C1 pass, C2 fail 44). C2 is
verifiable without C1 (`c2-only` control: C2 pass; C1 fail, no receipt or flip).
