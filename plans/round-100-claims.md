# kengaku round 100 — frozen claims

Frozen at commit F of round 100 (the single commit that adds this file). Author: kengaku (L1
KengakuR100, hyaku run 15, attempt 1). BASE `7846037679de77d050141c785996471801e5a19a` (lane tip at round
start; clean, pushed; round 99 closed `admitted`). P0 capture, solution fixture, mechanism predictions,
census start: `fb0f125cb272be31143a0bc57685b093b356b984`. P1 instruments, C2 BASE population, live
re-fetch, dry runs 1–2, pre-freeze able-to-fail receipts, candidate bytes:
`4df35de800425ca1dbe66681368f372361b891fe`. P1b amendment 1 (`.ufo/waves/round-100/L1/amendment-1.txt`):
`934b984a1d200e61aad84f67cacd7293f394ed9a`. P1c amendment 1b: `f07c026ec1b1ac47bb925ffdc70afcf5a8c782d8`.
P2 control receipts of record (two runs each against the P1c bytes): ``5220b71d337a3703eaba4cdf6b85eaf343497ae0``
(`.ufo/waves/round-100/L1/controls/`).

Order (rounds 93–99): P0 predictions → P1 every instrument → P2 every do-nothing, forgery, positive and
separability control, each run twice against P1 bytes and committed (Q80), each forgery asserted to differ
from its positive (Q85) → the pre-freeze standing-gate check on the candidate tree (round-99 routed
defect 1; `prefreeze-both-run{1,2}.txt`: `VERDICT clean`) → F this file → C: the candidate bytes and the
official probe receipt, nothing else → measurement at T. **No file in the frozen-instruments table
changes after F, and C lands exactly the candidate-bytes files plus the one receipt path named below.**
A defect found after F is routed to round 101 and the affected claim is reported as the frozen predicate
says; it is not repaired in round. Unlike round 99, no dated correction of candidate bytes after T is
planned: the standing gates that round 99's corrections answered (`anchor_line_check`, `round82-c1`) were
run on the candidate tree before F and are clean. No closed round's frozen instrument is edited (Q79).

Runs that preceded the predictions (M5 rule): one maintainer-OCR run to build the positive fixture; no
grader run. P0 predictions are unchanged through F (15/15 in dry runs 1 and 2). Amendments 1 and 1b
changed only C2 counter bytes and one candidate quote cell, both before any freeze.

Round-99 routed defects addressed by design (spot-check `corpus/lessons/round-99-verifier-spotcheck.md`):
(1) frozen-clause departures — the pre-freeze check above; (2) harm battery counted, not set-diffed, and
read untargeted trees — `plans/round100_prefreeze_check.py` diffs finding SETS per explicit revision;
(3) C2 census finding-level only — K8 row-level census; (4) mutation survivors — C1 L3/L10/L12, C2 K3/K4;
(5) ledger class note — carried, not changed (frozen `classes_source`).

```frozen-instruments
b255a4287b025dcb9e9b4cf8ab1083640c10edb6585c45b110b8474ab737b90b  plans/round100_fdp_probe.py
286d1772ff9e0e1b7ebee303f672a3e1771d56d4dfa51b5552df43307b565142  plans/round100-cases.json
96fdf22fa793b48b04bc817d8d34c09aa3a237bbc1fcb29990f777fb31ae9164  plans/round100_c1_replay.py
e0eec212059b415fc4889c4e0e53bdd76b81736fcaf3275472ef017e46278bcc  plans/round100_c2_rowcensus_bind.py
8ee8918cc1dba1f502f2163a5f50000002efb2097cd4c335c1ae98eb48e5b69e  plans/round100_provenance_build.py
c9841d35b0c9396725e5eb3f12893e0d2d772c7374e4ee78963f00d73eac50ba  plans/round100_prefreeze_check.py
11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2  plans/anchor_digest_check.py
814a091e26eb9886d74ab290cb4e8c320a2ffda71d2359d9c946c835056415fc  plans/anchor_line_check.py
1399146ca852882222f91adb47d2515281bc7cbe8541052cd8393be97014e7ad  .ufo/waves/round-100/L1/c2-live-refetch.txt
0a137bdb179c5d4e9056565e8fa18725bf94f56b43fa78547db888bb1cb46fa3  corpus/evidence/round100/tb2-financial-document-processor/SHA256SUMS
978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a  corpus/evidence/round100/tb2-financial-document-processor/test_outputs.py
48abbda713ace5cee00dd28c7398959f28280062350eb88206a6697a28c72790  corpus/evidence/round100/tb2-financial-document-processor/test.sh
90861b79c4bd7733909616ffa058151847eb67a4d43395a964c449cf7e24c4fb  corpus/evidence/round100/tb2-financial-document-processor/solve.sh
97fbf7930b838bc28556a67ba296b131660b8d1e18272b288c169e9a5183ed6f  corpus/evidence/round100/fdp-solution/SHA256SUMS
32518f87d43be98e862086e6dd847538b3d2800ad9f083ff3994826a1fb48209  corpus/evidence/round100/fdp-solution/placement.tsv
08724ad988ea1fe13804ddaf85da9b3731289ac5b9a9e730117b9134c3e977b2  corpus/evidence/round100/fdp-solution/summary.csv
```

The two SHA256SUMS rows bind every other capture and fixture byte (the probe and C1 L2 verify that each
SHA256SUMS lists exactly its directory's files and that every line hashes).

C lands exactly these files byte-for-byte plus the probe receipt `corpus/evidence/round100/fdp-probe.txt`
written by the official run at F.

```candidate-bytes
726dcdc8c06aa45d10552539cbe90a1eb7ac0414aa5a8655d1bd84229fbf4ec8  SKILL.md
d0df8332876de0bf39f8639b9fa7cbfe7c6e52a6b0978bf4320ecf6cd4903834  plans/grader-population-ledger.json
1f4c2354b813eb82c009591cd44b81fc1aa71a56c35471ef66c866af40f584ec  corpus/SOURCES.md
18be616be3826b5133de255a12e9494293ed3b08d295e09269d1b0788ed9491e  corpus/evidence/round52/PROVENANCE.md
a910b60a6deb82d8bdc12e32de5fbcc2e413d98f4ba67f1c6a295025198b0e46  corpus/evidence/round58/PROVENANCE.md
974ba21db8703283d81430e3771ac205dea92985001f00e69abd559e3b3ca047  corpus/evidence/round94/PROVENANCE.md
```

Ownership: R100-C1 owns the ledger flip, the two SKILL class cells (`crypto-credential` 4 → 5 of 12,
`file-artifact` 34 → 35 of 76), the five registry rows `round100-*` (all ride in the SKILL candidate),
SOURCES S342–S349 and the receipt. R100-C2 owns the three `corpus/evidence/round<N>/PROVENANCE.md` files.

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the measurement at T.
The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing is the host table.
Wave findings are routed, not repaired.

## R100-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Member choice (Q86).** Class arithmetic at BASE (`plans/grader-population-ledger.json`, executed 43 of
88): `min_class=crypto-credential 4/12` (0.333), tied with `shell-exec 2/6` and `subprocess-exec 15/45`;
then filesystem-metadata 4/10, numeric-band 4/10 (0.400), timing-wall 4/9 (0.444), file-artifact 34/76
(0.447), stdout-inspection 13/29 (0.448, the median executed fraction over the 15 classes),
candidate-import 3/6, db-state 1/2, network-service 4/8 (0.500), git-plumbing 2/3, process-environment
2/3 (0.667), serialization-schema 8/10 (0.800), signal-delivery 1/1. The tie is broken by marginal lift
(round-99 ConnectorOverlap CO-7/CO-9): `shell-exec`'s four remaining members need nginx+sshd, apt
texlive at test time, QEMU, or a candidate library (none feasible offline this round); a
`subprocess-exec` member lifts its class by 1/45; `financial-document-processor` lifts
`crypto-credential` by 1/12 (0.333 → 0.417) with a pandas pin the lane already stages. Classes
`crypto-credential, file-artifact` (frozen `classes_source`).

**Claim.** An eighteenth located offline replay of a pinned Terminal-Bench 2.0 grader:
`financial-document-processor` @ `2fd12b88`, through `plans/round100_fdp_probe.py`. Verifier side: a venv
with `test.sh`'s uvx pins (python 3.13, pytest 8.4.1, pandas 2.3.2, pytest-json-ctrf 0.3.5; numpy
unpinned and stamped); 15 cases × 8 observed legs (the grader's seven test functions as reported by real
`pytest.main` through an observe-only hook, and the reward leg — pytest's own exit). The positive control
stages the committed placement and summary of one offline run of the maintainer's OCR solution (host
tesseract 5.5.3; its output equals the grader's table). Captures are flat
(`corpus/evidence/round100/tb2-financial-document-processor/`, documents under `documents/`).

Sources: S342–S347 admitted (tier A), S348 rejected (A), S349 rejected (B); opened 2026-11-06 12:06 -03.

**Venv staging** (network, before the probe; the probe itself runs with no network):
`uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2 pytest-json-ctrf==0.3.5`
(resolves numpy 2.5.4 on 2026-11-06; numpy is stamped, not refused).

**Frozen predicate.** At the measured tip T, from the lane root:
`python3 plans/round100_c1_replay.py --lane . --rev T --work DIR --grader-venv G` prints `REV <T>`, then
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass L11=pass L12=pass L13=pass`,
then
`TARGET executed_rows=44 member=financial-document-processor cells=crypto-credential:5,file-artifact:35 set_equals_base_plus_member=1 located=1 executed=1 cases=15 legs=120 mismatches=0 new_rows=8 new_rows_flagged=0 new_rows_line_live=0 changed_outside_table=0 defects=0`,
then `PREDICATE R100-C1 pass`, exit 0. BEFORE (do-nothing control at P1c): `PREDICATE R100-C1 fail`, rc 1.

**What is new against round 99's counter** (the discriminating content): L3 run identity = F (P2
`receipt-identity`: only L3 fails); L10 exact new-row count (P2 `extra-row`); L12 F..rev file set and
candidate-byte equality (P2 `extra-file`, `skill-cell`); L13 the line gate on new rows (P2 `typed-words`).

**Grading gaps the replay locates** (predicted at P0 from mechanism, 15/15 held in dry runs 1–2): C03 —
summary of 11 `total` rows passes; C04 — ten copies of one invoice row pass; C07 — copies retained in a
subdirectory of `/app/documents` pass; C08 — a duplicate invoice copy passes (set collapse). Boundaries
and format splits: C11/C12 (strict < 0.01), C14/C15 (structure test order/BOM-sensitive, content test
not). Mechanism negatives: C02, C06, C09, C13.

**Kill rule.** Not met if any leg fails at T, if the predicate prints anything but `pass`, if a frozen
file changes after F, or if C lands bytes other than the candidate-bytes table and the receipt.

## R100-C2 — freshness (held at ceiling 10): path-matched provenance for wrongly bound TB2 rows, live re-fetch, row-level census

**Claim.** Population (claim-local, one rule, derived at BASE and frozen as `POP` in
`plans/round100_c2_rowcensus_bind.py`; list `.ufo/waves/round-100/L1/c2-pop.txt`): a BASE SOURCES row
whose BASE gate output carries a `digest-wrong-capture` or `anchor-unbound` finding with a 64-hex token,
whose first pinned TB2 raw URL `<task>/<rel>` has a committed copy at `…/<task>/<rel>` or
`…/tb2-<task>/<rel>` hashing to that token, and that no BASE PROVENANCE.md names. 9 rows (S210, S211,
S219, S228, S232, S279, S281, S298, S300 on its 64-hex token). S298 enters on the committed copy of the very
file its URL names (`round94/graders/write-compressor/tests/original-decomp.c`), not on the decomp.c
digest round-99 CO-11 warned about. Each upstream file was re-fetched live before the freeze (HTTP 200,
sha256 = token, 9/9; `c2-live-refetch.txt`). Each row is bound by a NEW three-cell
`corpus/evidence/round<N>/PROVENANCE.md` line (rounds 52, 58, 94), built by
`plans/round100_provenance_build.py`; no gate byte, SOURCES row, capture or existing provenance file changes.

**Frozen predicate.** At T: `python3 plans/round100_c2_rowcensus_bind.py --lane . --rev T --work DIR`
prints `REV <T>`, `REF <F~1>`, then
`LEGS K1=pass K2=pass K3=pass K4=pass K5=pass K6=pass K7=pass K8=pass K9=pass K10=pass`, then
`TARGET pop=9 cleared=9 still=0 outside_rows=324 outside_removed=0 outside_added=0 outside_rebound=0 base_rows=333 base_rows_not_equal=0 new_provenance_files=3 url_channel_files=0 not_three_cells=0 ids_not_in_pop=0 live_rows=9 rows_changed=0 captures_changed=0`,
then `PREDICATE R100-C2 pass`, exit 0. BEFORE (do-nothing control): `still=9`, `PREDICATE R100-C2 fail`,
rc 1. The `GATE defects base=… ref=… rev=…` line is informational (P2 positive: 33 / 32 / 23; the
ref 32 is C1's P0 capture re-binding S295, amendment 1). The `RECLASS` line for S300 `fa53d657` is
informational.

**What is new against round 99** (the claim's discriminating content): K8 row-level census (P2
`outside-row-delete`: deleting S001, a row with no gate output, fails K8 only — round-99 MutC2 M17 /
CriticClaims F6 killed); K3 exactly three cells (`fourth-cell`); K4 no id outside POP (`fabricated-id`
S999, `outside-rebind` S236); K9 live re-fetch receipt (`live-forged`); K10 file set (`c2-extra-file`);
a different defect class (`digest-wrong-capture`: the frozen gate had bound these rows by `row-path` to a
probe receipt the row mentions) and a population rule that requires the capture to be the URL's own file.

**Kill rule.** Not met if the predicate is not `pass` at T, if C lands bytes other than the
candidate-bytes table and the receipt, or if a frozen file changes after F.

## Separability

C1 is verifiable without C2 (`c1-positive` = the c1only fixture passes; `c2-c1only` fails with
`still=9`). C2 is verifiable without C1 (`c2-positive` = the c2only fixture passes; `c1-c2only` fails).
Neither predicate names a quantity the other changes: C1's L10/L13 read rows added after BASE; C2's
population, K7 and K8 read rows present at BASE, and its censuses start at REF = F~1, which already holds
C1's P0 capture. Shared file: none (C1 writes SKILL.md, SOURCES.md, the ledger; C2 the three
PROVENANCE.md). `c1-both` and `c2-both` pass.
