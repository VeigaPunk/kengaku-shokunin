# MutantGateR80 — C1 gate mutation probe

Axes: coverage and calibration. Attacked six behavior-bearing validation points; no production repair or predicate change.

## Measured bytes

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`.
Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`
Output at measurement: `6669fe72e59718acc1a0f32a92849a544b0b2f1c`.
The tip advanced past freeze. Every input was copied from committed bytes at that pinned tip using `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show <tip>:<path>` (rc 0 for every listed input), not from worktree bytes. No clone or git mutation was needed.

Input SHA256 (Python `hashlib.sha256` over each `git show` stdout):

```json
{
  "plans/round80_c1_located_replay.py": "81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8",
  "plans/round80_probes.json": "caa4333f2d3a12cc9d5755828937b24aa5ca22fa4f22798031aa7ce6b1520f22",
  "plans/grader-population-ledger.json": "c93495da67949bcccbfabace43bdf81f002b10b03f16a60e935c825f618dbbf9",
  "corpus/evidence/round80/cancel-async-tasks-probe.txt": "7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e",
  "corpus/evidence/round80/chess-best-move-probe.txt": "b32f4b37d7e4e93ecf104cba131dda30df980dfd3078ccaf2a01f13ddd15003c",
  "corpus/evidence/round80/distribution-search-probe.txt": "fd337d12dff0210e3d84f4ed22619dc92976006677b7ba835dfa959ff69b188d",
  "corpus/evidence/round80/largest-eigenval-probe.txt": "9179d62d67d1f1d43cfb4ac5fb7dcd33918ce589f1b03ed8176b9a623c3f4493",
  "corpus/evidence/round80/openssl-selfsigned-cert-probe.txt": "08c10b0d12e18e39daf834538da039c9e31474858a7b3ce3d6d2c393db7b8585",
  "corpus/evidence/round80/protein-assembly-probe.txt": "82b910af1d9333e5479bbf7379e5e66341bea44e41ba81765a35758b5322da5b"
}
```

The requested gate, probe table, six real receipts and ledger were copied into the isolated fixture tree. The committed batteries themselves generate synthetic six-member fixtures; they do not replay the copied production receipts. Thus this report establishes battery sensitivity, not the production population claim.

## Verdict

All six code mutations are **killed by the combined committed selftest + mutants detector**: pristine and each exact-byte restoration pass both commands, while every mutated gate fails selftest. No combined-detector survivor or inconclusive baseline.

| Code mutation (original gate line) | Exact edit | Selftest catcher(s) | selftest rc | mutants rc |
|---|---|---|---:|---:|
| a, 248 | tool SHA conditional → `elif False:` | tool-sha-mismatch | 1 | 1 |
| b, 237 | source SHA conditional → `elif False:` | source-sha-mismatch | 1 | 0 |
| c, 251–257 | replace entire tip validation with `pass` | lane-tip-invalid | 1 | 0 |
| d, 304 | fresh/block conditional → `elif False:` | observations-foreign; copy-observations | 1 | 0 |
| e, 226 | `if named != [m]:` → `if m not in named:` | second-member | 1 | 0 |
| f, 281–295 | replace all ledger-row validation with `pass` | ledger-unlocated; ledger-wrong-receipt | 1 | 1 |

### Mutants-only coverage findings (not combined survivors)

The `--mutants` command alone **survives b/c/d/e** (exits 0 even with those code defects). Exact relevant code lines and the cases that should catch the defects:
- b: line 237, source SHA mismatch. No source-SHA data mutant exists; selftest `source-sha-mismatch` catches it.
- c: lines 251–257, tip validation. No tip data mutant exists; selftest `lane-tip-invalid` catches it. Fixture mode does not exercise the real git ancestry branch (256–257), so reachability-specific sensitivity is unmeasured.
- d: line 304, reproduction comparison. `foreign-block` should isolate this check, but it is still killed by `DIVERGENCE-UNNOTED` after the comparison is removed. Selftest `observations-foreign` isolates it; `copy-observations` additionally detects absence of the expected code despite another defect remaining.
- e: line 226, multiple members. `second-member` should isolate member cardinality, but injects the second name inside the observation block and is still killed by `REPRODUCTION-MISMATCH`. Selftest asserts the specific member-count code and catches the removed check.

In a and f, `--mutants` exits 1 because its **data** mutant respectively `wrong-tool-sha` or `flip-ledger-only` survives; that failing battery kills the **code** mutant. These are different mutation levels, not contradictory verdicts.

Could not break the combined committed battery with the six assigned code defects. Did not test selective removal of only the real git ancestry branch, individual ledger subject/verdict/round checks, or production replay; no claim is made about those unrun probes.

## Actual commands and full outputs

Every subprocess used the isolated scratch as cwd, `capture_output=True`, and a 180-second bound. Only one mutation was present at a time. Each mutation was followed by exact-byte restoration and both same detector commands. Stderr is empty throughout, explicitly retained below. Hashes are measured immediately before each pair of detector runs.

### pristine

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### a accept any TOOL_SHA

Gate SHA256: `d14aaed0d7560944f1eb4fc01bbde3b89046d9baefb3017af163e4a73542d1d4`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=- located=6 reproduced=6 FAIL
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=1
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING killed
MUTANT wrong-tool-sha codes=- SURVIVED
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=5 survived=1
```
stderr:
```text
```

### restored after a

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### b skip SOURCE_SHA

Gate SHA256: `3be11c3d7828d7090e5141f1a0ff4f4b6addbff621c3233a921a1556399f5c36`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=- located=6 reproduced=6 FAIL
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=1
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### restored after b

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### c accept any LANE_TIP

Gate SHA256: `0b836466590ad4925af2dbec0db85385c6328437a0cabd54a3b781346411b2f2`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=- located=6 reproduced=6 FAIL
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=1
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### restored after c

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### d skip reproduction comparison

Gate SHA256: `2575a0cba5749d9ac6d0cc1219ec9963500ec93fa00ac64c76e172e5835ef616`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY located=5 reproduced=6 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=- located=6 reproduced=6 FAIL
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT located=5 reproduced=6 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED located=5 reproduced=6 FAIL
SELFTEST cases=16 red=14 failures=2
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### restored after d

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### e accept multiple named members

Gate SHA256: `f9ca9a55c7baa161dacef88ea32d2b93073f9c59bd5426391c861705074b689a`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=REPRODUCTION-MISMATCH located=6 reproduced=5 FAIL
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=1
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### restored after e

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

### f drop ledger-row checks

Gate SHA256: `4dc7580870270d1dd84a0e46be8d5e851e68702ddc921a03c6cceba25058f507`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=- located=6 reproduced=6 FAIL
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=- located=6 reproduced=6 FAIL
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=2
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 1

stdout:
```text
MUTANT flip-ledger-only codes=- SURVIVED
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=5 survived=1
```
stderr:
```text
```

### restored after f

Gate SHA256: `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --selftest --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
CASE clean expect=pass observed=- located=6 reproduced=6 ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT located=5 reproduced=6 ok
CASE stamp-missing expect=STAMP-MISSING observed=STAMP-MISSING,TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE source-sha-mismatch expect=SOURCE-SHA-MISMATCH observed=SOURCE-SHA-MISMATCH located=5 reproduced=6 ok
CASE tool-sha-mismatch expect=TOOL-SHA-MISMATCH observed=TOOL-SHA-MISMATCH located=5 reproduced=6 ok
CASE receipt-missing expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED located=5 reproduced=5 ok
CASE observations-empty expect=OBSERVATIONS-EMPTY observed=DIVERGENCE-UNNOTED,LEDGER-VERDICT,OBSERVATIONS-EMPTY,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE observations-foreign expect=REPRODUCTION-MISMATCH observed=REPRODUCTION-MISMATCH located=6 reproduced=5 ok
CASE second-member expect=RECEIPT-MEMBER-COUNT observed=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
CASE ledger-unlocated expect=LEDGER-NOT-EXECUTED observed=LEDGER-NOT-EXECUTED located=6 reproduced=6 ok
CASE ledger-wrong-receipt expect=LEDGER-RECEIPT observed=LEDGER-RECEIPT located=6 reproduced=6 ok
CASE exit-nonzero expect=EXIT-NONZERO observed=EXIT-NONZERO located=5 reproduced=6 ok
CASE lane-tip-invalid expect=LANE-TIP-INVALID observed=LANE-TIP-INVALID located=5 reproduced=6 ok
CASE divergence-unnoted expect=DIVERGENCE-UNNOTED observed=DIVERGENCE-UNNOTED located=5 reproduced=6 ok
CASE divergence-noted expect=pass observed=- located=6 reproduced=6 ok
CASE copy-observations expect=REPRODUCTION-MISMATCH observed=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH located=5 reproduced=5 ok
SELFTEST cases=16 red=14 failures=0
```
stderr:
```text
```

Command: `python3 /fast/scratch/hyaku/kengaku-r80/MutantGateR80/plans/round80_c1_located_replay.py --mutants --work /fast/scratch/hyaku/kengaku-r80/MutantGateR80/battery`

Exit: 0

stdout:
```text
MUTANT flip-ledger-only codes=LEDGER-NOT-EXECUTED killed
MUTANT strip-stamp codes=STAMP-MISSING,TOOL-SHA-MISMATCH killed
MUTANT wrong-tool-sha codes=TOOL-SHA-MISMATCH killed
MUTANT foreign-block codes=DIVERGENCE-UNNOTED,REPRODUCTION-MISMATCH killed
MUTANT drop-receipt codes=RECEIPT-UNTRACKED killed
MUTANT second-member codes=RECEIPT-MEMBER-COUNT,REPRODUCTION-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
```
stderr:
```text
```

## Restoration and cleanup

All six restorations returned gate SHA256 `81bc451c210fbb36fd7c6e27621da68625b9976773e4aac036d3ad78e37e2ef8`, matching pristine bytes, and each printed `SELFTEST cases=16 red=14 failures=0` and `MUTANTS real=6 killed=6 survived=0`, both rc 0.

Scratch lifetime shell installed `trap 'rm -rf -- "$S"' EXIT`; sending newline ended its `read` and ran the trap. Command-equivalent observation: Python `not S.exists()` → `True`. No scratch artifacts remain. Only this scoped report was written in the lane. No tools installed or upgraded.

## Self-evaluation

Accuracy 4/5: full rc/stdout/hash evidence retained; synthetic fixture mode cannot establish production replay correctness. Completeness 5/5: six requested mutations, both detectors, pristine/restored runs, exact edits and cleanup captured. Clarity 4/5: distinguishes code versus data mutants but complete logs are long. Actionability 4/5: names masked mutants and isolating cases; no repairs made by this read-only seat. Conciseness 4/5: repeated restoration logs retained to meet evidence requirements. Overall 4.2/5. Improvement: isolate foreign-block and second-member data mutants; add source-SHA and real-ancestry data cases without changing the frozen contract. Self-check: assessment is bounded to this mutation ticket.
