# ExecLedgerFlip — R92-C1 ledger flip, prepared for L1 integration

Seat: ExecLedgerFlip (leaf executor). Scratch-only: no lane edit, no commit, no git mutation in the lane.
Measured revisions: BASE `4ba56182307ccda1ec436bfe3d61cb3d92e56608`; B2 `f0018773f507f363854123856990f8ff8a87eb8c`;
lane HEAD observed read-only `288511d8944e8089503011a1c50a5faf2fbed86d` (detached).

## 1. BASE member row and executed totals

Read by `python3 -c` over `plans/grader-population-ledger.json` at BASE in a scratch clone (`git show 4ba56182:…`).

Member row at BASE (verbatim, file lines 432–442):

```json
    "llm-inference-batching-scheduler": {
      "classes": [
        "crypto-credential",
        "file-artifact",
        "filesystem-metadata",
        "serialization-schema"
      ],
      "evidence": "no-blocker: tests/test_outputs.py sha256=80b06b7c4ba0db28",
      "reason": "unattempted",
      "status": "unexecuted"
    },
```

Totals at BASE (88 members):

- executed = **35** of 88
- filesystem-metadata 3, crypto-credential 3, serialization-schema 4, file-artifact 26 (matches the brief)

## 2. Proposed new member row (ready to paste, 2-space indent as at BASE)

Replaces the BASE block at lines 432–442 (the 11-line object including its closing `},`):

```json
    "llm-inference-batching-scheduler": {
      "classes": [
        "crypto-credential",
        "file-artifact",
        "filesystem-metadata",
        "serialization-schema"
      ],
      "evidence": "no-blocker: tests/test_outputs.py sha256=80b06b7c4ba0db28; receipt corpus/evidence/round92/bs-probe.txt",
      "reason": "replayed",
      "round": 92,
      "status": "executed"
    },
```

Notes:
- Classes list unchanged, same order as at BASE.
- Subject sha prefix `80b06b7c4ba0db28` (full 80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa in the probe receipt).
- `reason: "replayed"` and `round: 92` follow the shape of the executed rows already in the ledger.
- Cross-check: the integrated lane HEAD `288511d8` already carries this same row with the same evidence line, `reason`, `round` and `status`. Only the file indentation differs (see §3 note).

## 3. Recomputed after-cells from the flipped ledger

Flipped bytes built in scratch (`ledger-after.json`, 26509 bytes, sha256 `f497e686…d98ec8a`), then parsed and counted with Python:

```
members       = 88                                   (unchanged)
executed      = 35 + 1 = 36 of 88
filesystem-metadata   = 3 + 1 = 4  of 10   (members-with-class denominator 10, unchanged)
crypto-credential     = 3 + 1 = 4  of 12   (members-with-class denominator 12, unchanged)
serialization-schema  = 4 + 1 = 5  of 10   (members-with-class denominator 10, unchanged)
file-artifact         = 26 + 1 = 27 of 76  (members-with-class denominator 76, unchanged)
```

Counting method: `executed` counts rows with `status == "executed"`; each class cell counts executed rows whose `classes` list contains the class, over the total rows whose `classes` list contains it. The flip adds one to the numerator of each of the four member classes and leaves every denominator unchanged.

Parsed comparison against the integrated lane HEAD `288511d8` ledger (`ledger-head.json`):

- `flipped == HEAD` as parsed JSON: **True** (both have 36 executed).
- Byte-level: NOT identical. HEAD is re-serialized with 1-space indent (23684 bytes, `json.dumps(indent=1)` round-trips to its exact bytes); BASE and my flip use 2-space indent (BASE round-trips with `indent=2`).
- Every counter parses the ledger with `json.loads`, so both pass the L7 leg. I scanned 20 of 26 plan files that name the ledger and found no sha pin on the ledger bytes. This is a formatting divergence for L1 to decide; the content is identical.

## 4. Red-before receipt (counter at BASE on the clone)

Command (from the B2 clone, `--rev` BASE, scratch work dir):
`python3 plans/round92_c1_replay.py --lane <clone> --rev 4ba56182 --work <scratch>/w-redbase`

Verbatim TARGET line:

```
TARGET executed_rows=35 member=llm-inference-batching-scheduler located=0 executed=0 cases=0 legs=0 mismatches=0 defects=9
```

Exit code **1**. Defect lines (all nine; `DEFECT L7` present as expected):

```
DEFECT L1 receipt absent at revision: corpus/evidence/round92/bs-probe.txt
DEFECT L2 subject/input sha mismatch (cap=absent in1=absent in2=absent receipt=absent)
DEFECT L3 LANE_TIP absent not an ancestor of 4ba56182307c
DEFECT L4 case table not byte-identical to freeze commit (rev=absent A=2249d5c0ea90930a5c36300b47a4b991d41ae9c5ff400deba5adf9be28d5a693)
DEFECT L5 case coverage 0 of 0
DEFECT L6 rerun rc=2 obs=0 want=0
DEFECT L7 ledger member=unexecuted round=None executed_total=35 cells_ok=False
DEFECT L8 probe pin unreadable vs bytes absent
DEFECT L9 stamp fields mismatch (tool=None table=None python=None openssl=None userns=None)
PREDICATE R92-C1 fail
```

Copy: `.ufo/waves/round-92/w1/ExecLedgerFlip/red-before-BASE.txt`.

Note on the L7 leg: the frozen claim text lists the L7 leg among the do-nothing defects; the counter reports it as expected. The predicted TARGET values `executed_rows=35 … executed=0` match exactly.

## 5. Extra control (scratch only): the flip is green

Scratch commit `c580867b` on top of the integrated HEAD `288511d8`, with `plans/grader-population-ledger.json` replaced by the 2-space flipped bytes. Counter run at that commit:

```
TARGET executed_rows=36 member=llm-inference-batching-scheduler located=1 executed=1 cases=10 legs=60 mismatches=0 defects=0
PREDICATE R92-C1 pass
```

rc 0. Copy: `.ufo/waves/round-92/w1/ExecLedgerFlip/flip-green-scratch.txt`. This was a scratch control on a scratch commit, not a measured tip; the official measurement belongs to L1 at the post-integration tip.

## 6. Host and tool facts (read-only)

- `/usr/bin/bwrap` present; `/proc/sys/user/max_user_namespaces` = 122865 (not modified).
- No tools installed or updated. pacman not used.
- `/fast` 392 GB free at the start of the seat.

## 7. Scratch hygiene

Scratch `/fast/scratch/hyaku/kengaku-r92/ExecLedgerFlip` (clones, worktree, work dirs) was removed before yield. Receipts copied into this wave directory first.

## Items for L1

1. Choose the ledger serialization: 2-space (BASE, and what this report proposes) or 1-space (integrated `288511d8`). Content is identical.
2. The row in §2 is ready to paste at BASE lines 432–442 (or into the integrated file after the indent decision).
3. The official TARGET line for the tip is expected `executed_rows=36 … executed=1 … mismatches=0 defects=0`, `PREDICATE R92-C1 pass`.
