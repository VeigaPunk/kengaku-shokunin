# kengaku round 98 — frozen claims

Frozen at commit F of round 98 (the single commit that adds this file). Author: kengaku (L1
KengakuR98, hyaku run 15, attempt 1). BASE `49a1c4f1097db7c923da56d4213cad75772ed1c0` (lane tip at
round start; clean, pushed; round 97 closed `rejected-honest-stop`). P0 capture, mechanism
predictions, census start: `5584a6f7d157ba491d6c64909bfe3c0670f46778`. P1 instruments:
`350d0e59faceebdc53ccf338bcac8df54020d58e`. P2 control receipts: `c71f04e6167fe0a5acbed27239a9120de7a87cf1`
(`.ufo/waves/round-98/L1/controls/`).

Order (rounds 93–97): P0 predictions → P1 every instrument → P2 every do-nothing, forgery, positive
and separability control, each counter run twice against P1 bytes and committed (Q80) → F this file
with the sha256 of every instrument and every candidate byte → C: the official probe run and the
candidate bytes, nothing else → measurement at T. **No file in the frozen-instruments table changes
after F, and C lands exactly the candidate-bytes files plus the one receipt path named below.** A
defect found after F is routed to round 99 and the affected claim is reported not met; it is never
repaired in round. No closed round's frozen instrument is edited (Q79). The SKILL.md candidate also
carries the four registry rows of the new scripts (`round98-*`, kind `probe`); they were added to the
candidate after the P2 runs, which is immaterial to every control because no round-98 counter reads
SKILL.md (`grep -c SKILL` → 0 in all three). No candidate file is edited after C.

Round-97 routed defects addressed by design (not claimed as repaired beyond the counters below):
defect 1 (nested captures unbound) is R98-C2's population; defect 2 (claim-local predicates, two
prefreeze runs) shapes both predicates — neither names a global row count, and both counters have two
committed agreeing prefreeze runs; defect 3 (MutC2 survivors) is not addressed here (the round-97
census is not reused).

```frozen-instruments
871630782933871398922c510c5de1cebd2ace7fa081d014df90aeeff66d33db  plans/round98_regexchess_probe.py
02f30e6aff2f27fc01615879aea3c4e5c0892691fd189939c6b0f6481fe25da3  plans/round98-cases.json
e361383249d9bdf5c9fffb83c6df5dbd286007c951a70e68dd3e21201b2f4b2a  plans/round98_c1_replay.py
77c6ba05a00a80cc76be97a669f00920ce2e0daaaa3b78eb31996f10302bf7a7  plans/round98_c2_nested_bind.py
31493146379782b5040b979f5c6e10a450efba3bbd79c3304983b04da8ea086f  plans/round98_provenance_build.py
11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2  plans/anchor_digest_check.py
4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4  corpus/evidence/round98/tb2-regex-chess/test_outputs.py
8f7f00a1c4dde7fcca6c918c768f2aba432b8c4007c15989716c68091950da87  corpus/evidence/round98/tb2-regex-chess/test.sh
b728bf0ea392a3d244afbd0818d36933c8d3e190e47743c1382cd518d518a2e9  corpus/evidence/round98/tb2-regex-chess/solve.sh
2616cd775252303839dfda0ee2f047eb862952b053b0103bd6b2460ef90c11b7  corpus/evidence/round98/tb2-regex-chess/Dockerfile
f9c416ae9ea01dcdd5f6a43170c8434b8c0a0b389a4a30876a2048e277d191c7  corpus/evidence/round98/tb2-regex-chess/check.py
07fe52636fcc4bc9fff25d5630af145b97a5331219d719cc8decb4ca67ea21d4  corpus/evidence/round98/tb2-regex-chess/task.toml
a6ed3fcc54fc92d71a84af921942422d299ca89b410dcd92cd05a53d0d06436c  corpus/evidence/round98/tb2-regex-chess/instruction.md
```

C lands exactly these files byte-for-byte plus the probe receipt
`corpus/evidence/round98/regexchess-probe.txt` written by the official run at F.

```candidate-bytes
6daa8e1dee404fbcb9b6825c1b564e728de60319eef34004d46f7e53ed105bdc  SKILL.md
915c3b44dc5854e2f4e05c5a83f085074c1f6340daa62957b410b208ca098626  plans/grader-population-ledger.json
793b0520be4ac6b074dc463b7b74f79c15af2962c4657e67a3e8f040e206008a  corpus/SOURCES.md
d3fc4b7c9c69614fd2656407c5161780f903f0e5d1c66acad467135ba0f530b9  corpus/evidence/PROVENANCE.md
```

Ownership: R98-C1 owns the ledger flip, the two SKILL class cells (`file-artifact` 32 → 33 of 76,
`serialization-schema` 7 → 8 of 10), the registry rows `round98-regexchess-probe` / `round98-c1-replay`,
SOURCES S326–S333 and the receipt. R98-C2 owns `corpus/evidence/PROVENANCE.md` and the registry rows
`round98-c2-nested-bind` / `round98-provenance-build`.

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the measurement at
T. The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing is the host
table. Wave findings are routed, not repaired.

## R98-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A sixteenth located offline replay of a pinned Terminal-Bench 2.0 grader: `regex-chess` @
`2fd12b88` (classes `file-artifact`, `serialization-schema`), through
`plans/round98_regexchess_probe.py`. The verifier side is a venv with `test.sh`'s uvx pins (python
3.13, chess 1.11.2, pytest 8.4.1); 12 cases × 5 observed legs (the grader's four test functions as
reported by real `pytest.main` through an observe-only hook, and the reward leg — pytest's own exit
code). The captured `solve.sh` runs unmodified as the positive control. Captures are flat
(`corpus/evidence/round98/tb2-regex-chess/`) so the frozen anchor-digest gate binds the new rows
(round-97 defect 1 is not reproduced by this claim).

Sources: S326–S330 admitted (tier A), S331–S333 rejected with flips; opened 2026-11-06 08:03 -03.

**Venv staging** (network, before the probe; the probe itself runs with no network):
`uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 chess==1.11.2`.

**Frozen predicate.** At the measured tip T, from the lane root:
`python3 plans/round98_c1_replay.py --lane . --rev T --work DIR --grader-venv G` prints
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass`, then
`TARGET executed_rows=42 member=regex-chess cells=file-artifact:33,serialization-schema:8 set_equals_base_plus_member=1 located=1 executed=1 cases=12 legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`,
then `PREDICATE R98-C1 pass`, exit 0. The executed member set at T EQUALS BASE's plus `regex-chess`
(round-97 MutC1: superset let an extra unearned member pass); L10: the BASE gate bytes flag none of the
SOURCES rows added after BASE.

**Predictions.** Filed from mechanism at P0 (`.ufo/waves/round-98/L1/predictions-mechanism.txt`,
commit `5584a6f7`) before any case ran; 12 of 12 held in dry run 3
(`.ufo/waves/round-98/L1/dryrun/probe-dryrun-3.txt`; dry runs 1–2 failed on verdict-parsing defects,
`dryrun/README.md`). Grading gaps the replay locates: C04 (one legal successor duplicated in place of
another passes: membership per line plus an equal count is not set equality), C07 (an invented
en-passant square passes wherever the true field is `-`: the `rpartition` fallback), C09 (a 103-entry
lookup table of the three public games' positions passes with no move generation; C10 shows one
missing entry fails only its game). C08 is the mechanism negative for C07 (castling is not
forgiven); C11/C12 locate the two size limits separately.

**Kill rule.** Not met if any leg fails at T, if the predicate prints anything but `pass`, if a frozen
file changes after F, or if C lands bytes other than the candidate-bytes table and the receipt.

## R98-C2 — freshness (held at ceiling 10): nested replay captures the frozen anchor-digest gate cannot bind

**Claim.** Population (claim-local, one rule, derived at BASE and frozen as `POP` in
`plans/round98_c2_nested_bind.py`; list `.ufo/waves/round-98/L1/c2-pop.txt`): a SOURCES row whose only
`anchor-digest-check` defect is `anchor-unbound` with a nested-upstream detail, and whose 64-hex token
equals the sha256 of a committed nested capture `corpus/evidence/round<N>/graders/<task>/<sub>/<file>`.
39 rows at BASE (S181–S323; rounds 52 and 92–97). Their digests name committed bytes the gate cannot
reach because it looks for `<task dir>/<basename>`. The change binds each row to the replay's own
capture through the gate's provenance-row rule with ONE new file, `corpus/evidence/PROVENANCE.md`
(built by `plans/round98_provenance_build.py`); no gate byte, SOURCES row or capture changes.

**Frozen predicate.** At T: `python3 plans/round98_c2_nested_bind.py --lane . --rev T --work DIR` prints
`LEGS K1=pass K2=pass K3=pass K4=pass K5=pass K6=pass K7=pass`, then
`TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0`,
then `PREDICATE R98-C2 pass`, exit 0. BEFORE (do-nothing control at P1): `still=39`, `PREDICATE R98-C2
fail`, rc 1. The `GATE defects base=… rev=…` line is informational and not part of the predicate (it
counts rows outside the population).

**Controls (P2, two runs each, `controls/c2-*-run{1,2}.txt`).** do-nothing → fail (K3, K4); positive →
pass; partial (one line short) → fail (K3); row-edit forgery (tokens blanked out of the 39 rows, no
provenance) → fail (K4, K5); wrong-capture forgery (rows with a round-52 twin bound to the twin) →
fail (K4); gate-edit forgery (provenance present, gate bytes changed) → fail (K1); capture-edit forgery
(one capture's bytes changed) → fail (K3/K6); c1only → fail; both → pass.

**Kill rule.** Not met if the predicate is not `pass` at T, if C lands bytes other than the
candidate-bytes table and the receipt, or if a frozen file changes after F.

## Separability

C1 is verifiable without C2 (`controls/c1-positive-run*.txt` pass with no PROVENANCE.md; `c2-c1only`
fails). C2 is verifiable without C1 (`c2-positive-run*` pass at P1 with no C1 byte; `c1-c2only` fails).
Neither predicate names a quantity the other claim changes: C1's L10 is scoped to rows added after
BASE, C2's population and K7 to rows present at BASE.
