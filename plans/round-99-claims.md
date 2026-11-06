# kengaku round 99 — frozen claims

Frozen at commit F of round 99 (the single commit that adds this file). Author: kengaku (L1
KengakuR99, hyaku run 15, attempt 1). BASE `2233a66195e3d3d85856248fb8f66c1d8127cede` (lane tip at round
start; clean, pushed; round 98 closed `admitted`). P0 capture, solution fixture, mechanism predictions,
census start: `f9d29eb3df9cfec26fd11feac8695a6d26a871c1`. P1 instruments, dry runs, prediction amendment 1,
C2 BASE population: `e219e785281703058f05bec9c29d81c943d35596`. P2 control receipts:
`b08a01923361cdfc6ecd1366028630b0db7c9f6e` (`.ufo/waves/round-99/L1/controls/`).

Order (rounds 93–98): P0 predictions → P1 every instrument → P2 every do-nothing, forgery, positive and
separability control, each run twice against P1 bytes and committed (Q80) → F this file with the sha256 of
every instrument and every candidate byte → C: the candidate bytes and the official probe receipt,
nothing else → measurement at T. **No file in the frozen-instruments table changes after F, and C lands
exactly the candidate-bytes files plus the one receipt path named below.** A defect found after F is
routed to round 100 and the affected claim is reported not met; it is never repaired in round. No closed
round's frozen instrument is edited (Q79).

Runs that preceded the predictions (M5 rule): one maintainer-R run to build the positive fixture; no
grader run. Prediction amendment 1 (after dry run 1, before F) changed C11/C12 from seeded random draws to
deterministic grids with unchanged predicted vectors; the dry-run-1 miss is lesson M1.

Round-98 routed defects addressed by design: defect 1 (provenance side channel) is R99-C2's K3/K7;
defect 2 (MutC2 survivors M05/M11/M16/M18, MutC1 counter self-integrity) is K4 and C1 L11 / C2 K1-self;
defect 3 (receipts name their revision) is the `REV <hash>` first line of both counters.

```frozen-instruments
afacbf81fcc84fd9b5216b6a3e66072cddc565291617bfaaf62e515c6d5563eb  plans/round99_bnfit_probe.py
ee76e2b5ae7477849fd74e66e969ae687bfb883a8affdae54091bea2d2839e73  plans/round99-cases.json
3619199e709dfd542e39ac1d6f020ca84110731dcdf6122e524436c88bb8ff23  plans/round99_c1_replay.py
8b470d7ac3c2ba7644079ed50f37f9db10d6bf97326c379517d7b747ad74d745  plans/round99_c2_rowscoped_bind.py
f6606371d9e17a3c585809311466cd04777c264f5494bee2f2be53e72d64aae0  plans/round99_provenance_build.py
11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2  plans/anchor_digest_check.py
364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b  corpus/evidence/round99/tb2-bn-fit-modify/test_outputs.py
ea2adeb779621e9625d1f80a17f9d19b6ecec017b8ad8974b668a4a0fbdeb4c3  corpus/evidence/round99/tb2-bn-fit-modify/test.sh
813eb810cf041466468703ef14fdb06ada533b9accddf774eecc7a7191d5cb79  corpus/evidence/round99/tb2-bn-fit-modify/solve.sh
8b0b1056e9c66c01a14a3d79332cc425498f2926b6deda13d200591ee5e5e6cc  corpus/evidence/round99/tb2-bn-fit-modify/Dockerfile
6493f7162da424a4fd95da721bd3fd1ce7e5dd26e792132cb9c46db536b67090  corpus/evidence/round99/tb2-bn-fit-modify/task.toml
5f5207ce23c375270c26719fb66d89843bc88cf1d40671ed87c6b7bab4d394e5  corpus/evidence/round99/tb2-bn-fit-modify/instruction.md
647d14a74c316f554dbd6eb70dd5da79b347eb8395fb5e92bf5ad8319faf7919  corpus/evidence/round99/tb2-bn-fit-modify/README.md
7d4c27aca2f7443500f993bf0cc31fc7c7e4ef45bb5370ba890848ee1ef3cb04  corpus/evidence/round99/tb2-bn-fit-modify/bn_sample_10k.csv
1efe8fe9a8c379014c5f898536f5cff3cdff2c3236d2b44e1ab90e761c85e2f4  corpus/evidence/round99/bn-fit-modify-solution/learned_dag.csv
458d8ecd0bc5dd7aca59acb78a11de228d51a09025a6497d3c1ec59a5e6296bd  corpus/evidence/round99/bn-fit-modify-solution/intervened_dag.csv
982a7441d4469c4b09eb0c9a27d5ca62f7fb38bdee6542b56a767e0c4b26ab66  corpus/evidence/round99/bn-fit-modify-solution/final_bn_sample.csv
c0a54e0b880c6810ea819e85dc2aa843a4d53e269146a600f3632e2ec86dbccf  corpus/evidence/round99/bn-fit-modify-solution/modify_bn.R
```

C lands exactly these files byte-for-byte plus the probe receipt `corpus/evidence/round99/bnfit-probe.txt`
written by the official run at F.

```candidate-bytes
0025b8e0b028ccd043fe0e78a1bb12f08ba4a6ffab61a4671078f5e2a8961883  SKILL.md
5e9c4182efd9f33bafa144f329ddef7e5ddc511c365c8b61d10d6b308ff6d623  plans/grader-population-ledger.json
05116b87550f534be71736ab600791bf7f3ab8a6ba3c649de2bd941b53586d1f  corpus/SOURCES.md
d52af96b1c35deaaa8498701e5a9a66a451f98da29a65f5e0baab65c97a0a23d  corpus/evidence/round50/PROVENANCE.md
7f3909f713db1e4181bb722be907ea93bbb81a123ba004b9e553b58d3111201a  corpus/evidence/round59/PROVENANCE.md
618916af90e754a08a3a3ad5a6a21816170a0146ecce67a541d4fd0adbbc18c6  corpus/evidence/round61/PROVENANCE.md
ce364b507c5efea269360a37b2e1292de51a47e8a49916a1dba0e228849426dd  corpus/evidence/round79/PROVENANCE.md
88c1cb8c2549da97e47806795b7baafba732ada6e13dffea5c5f9c4fdebc2026  corpus/evidence/round82/PROVENANCE.md
486dcba928989ff1e639bc3c3477e255347c4a6af8396207925404c0922582f9  corpus/evidence/round92/PROVENANCE.md
dc383775342b31fef4aa787adb7030ddddf61e228de7296f87e2eebcc25b56bb  corpus/evidence/round93/PROVENANCE.md
5e1001a37f8b7a0b32dd11e6b406339ce2fcae7ad541ce1c00dd2ddedd350fb5  corpus/evidence/round95/PROVENANCE.md
```

Ownership: R99-C1 owns the ledger flip, the SKILL `file-artifact` cell (33 → 34 of 76), the four registry
rows `round99-*` (all four ride in the SKILL candidate; no counter reads SKILL.md), SOURCES S334–S341 and
the receipt. R99-C2 owns the eight `corpus/evidence/round<N>/PROVENANCE.md` files.

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the measurement at T.
The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing is the host table.
Wave findings are routed, not repaired.

## R99-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A seventeenth located offline replay of a pinned Terminal-Bench 2.0 grader: `bn-fit-modify` @
`2fd12b88` (ledger class `file-artifact`), through `plans/round99_bnfit_probe.py`. Verifier side: a venv
with `test.sh`'s uvx pins (python 3.13, pandas 2.3.2, scipy 1.16.1, pytest 8.4.1) plus numpy 2.5.4 for the
seeded case builder; 13 cases × 10 observed legs (the grader's nine test functions as reported by real
`pytest.main` through an observe-only hook, and the reward leg — pytest's own exit). The positive control
stages the committed outputs of the maintainer's R solution (bnlearn; one offline run at P0, fit equal to
the grader's constants). Captures are flat (`corpus/evidence/round99/tb2-bn-fit-modify/`).

Sources: S334–S339 admitted (tier A), S340 rejected (A), S341 rejected (B); opened 2026-11-06 10:28 -03.

**Venv staging** (network, before the probe; the probe itself runs with no network):
`uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2 scipy==1.16.1`
(resolves numpy 2.5.4; the probe refuses another numpy).

**Frozen predicate.** At the measured tip T, from the lane root:
`python3 plans/round99_c1_replay.py --lane . --rev T --work DIR --grader-venv G` prints `REV <T>`, then
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass L11=pass`, then
`TARGET executed_rows=43 member=bn-fit-modify cells=file-artifact:34 set_equals_base_plus_member=1 located=1 executed=1 cases=13 legs=130 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`,
then `PREDICATE R99-C1 pass`, exit 0. BEFORE (do-nothing control at P1): `PREDICATE R99-C1 fail`, rc 1.

**Grading gaps the replay locates** (predicted at P0 from mechanism, 13/13 held in dry runs 2–3): C03 —
only column D of the sample is read: U,R,Y,M at 0.0 with D drawn from the target normal passes (no BN, no
fit, no intervention); C13 — a deterministic quantile grid passes (no sampling); C11/C12 — the p ≥ 0.001
KS rule admits a mean shift of 0.045 sd and rejects 0.050; C07 — duplicated edges plus an extra column
pass (set comparison). Mechanism negatives: C04 (no intervention fails the KS leg), C05 (R's default
row-names column fails the exactly-5-columns assert), C08/C09/C10.

**Kill rule.** Not met if any leg fails at T, if the predicate prints anything but `pass`, if a frozen
file changes after F, or if C lands bytes other than the candidate-bytes table and the receipt.

## R99-C2 — freshness (held at ceiling 10): row-scoped provenance bindings, URL channel closed, symmetric census

**Claim.** Population (claim-local, one rule, derived at BASE and frozen as `POP` in
`plans/round99_c2_rowscoped_bind.py`; list `.ufo/waves/round-99/L1/c2-pop.txt`): a SOURCES row present at
BASE whose BASE gate output is exactly ONE DEFECT line, class `anchor-unbound`, 64-hex token, with a file
committed under `corpus/evidence/` at BASE whose sha256 equals the token. 12 rows (S173–S177, S180, S220,
S225, S270, S285, S293, S306). Each is bound by a NEW three-column `corpus/evidence/round<N>/PROVENANCE.md`
(row, file, sha256 — no URL), built by `plans/round99_provenance_build.py`; no gate byte, SOURCES row,
capture or existing provenance file changes.

**Frozen predicate.** At T: `python3 plans/round99_c2_rowscoped_bind.py --lane . --rev T --work DIR` prints
`REV <T>`, then `LEGS K1=pass K2=pass K3=pass K4=pass K5=pass K6=pass K7=pass`, then
`TARGET pop=12 cleared=12 still=0 outside_rows=313 outside_removed=0 outside_added=0 outside_rebound=0 url_channel_files=0 rows_changed=0 captures_changed=0`,
then `PREDICATE R99-C2 pass`, exit 0. BEFORE (do-nothing control at P1): `still=12`, `PREDICATE R99-C2
fail`, rc 1. The `GATE defects base=… rev=…` line is informational (P2 positive: 45 → 33).

**What is new against round 98** (the claim's discriminating content): K7 is symmetric (removals and
re-bindings outside the population count, not only additions); K3 forbids the URL column the round-98
file used (P2 `url-channel` forgery re-binds S256 and fails K3/K7); K4 reads every provenance line and
the sha column (P2 `duplicate-line`, `sha-column` fail); K1 binds the counter's own bytes.

**Kill rule.** Not met if the predicate is not `pass` at T, if C lands bytes other than the
candidate-bytes table and the receipt, or if a frozen file changes after F.

## Separability

C1 is verifiable without C2 (`c1-positive` = the c1only fixture passes; `c2-c1only` fails with
`GATE base=45 rev=45`). C2 is verifiable without C1 (`c2-positive` = the c2only fixture passes; `c1-c2only`
fails). Neither predicate names a quantity the other changes: C1's L10 is scoped to rows added after BASE,
C2's population and K7 to rows present at BASE (`outside_rows=313` counts BASE rows only, so C1's eight new
rows cannot enter it).
