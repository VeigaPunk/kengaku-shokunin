# ExecLedgerFlip — scoped findings (R92-C1 ledger flip)

Full report: `.ufo/waves/round-92/w1/ExecLedgerFlip/report.md`. Receipts: `.ufo/waves/round-92/w1/ExecLedgerFlip/red-before-BASE.txt`, `.ufo/waves/round-92/w1/ExecLedgerFlip/flip-green-scratch.txt`.

## Findings

- **BASE row and totals (measured):** `llm-inference-batching-scheduler` is `unexecuted`, reason `unattempted`, classes `crypto-credential`, `file-artifact`, `filesystem-metadata`, `serialization-schema`. Executed = 35 of 88; `filesystem-metadata` 3, `crypto-credential` 3, `serialization-schema` 4, `file-artifact` 26.
- **Proposed flip (measured on the flipped bytes):** the row becomes `status executed`, `round 92`, `reason replayed`, evidence naming `corpus/evidence/round92/bs-probe.txt`. After-cells: executed 36 of 88; `filesystem-metadata` 4 of 10; `crypto-credential` 4 of 12; `serialization-schema` 5 of 10; `file-artifact` 27 of 76.
- **Red-before (BASE, counter run):** rc 1, `TARGET executed_rows=35 member=llm-inference-batching-scheduler located=0 executed=0 cases=0 legs=0 mismatches=0 defects=9`, `PREDICATE R92-C1 fail`. The defects include `DEFECT L7` as predicted, plus L1–L6, L8, L9 (receipt, pins and stamp absent at BASE).
- **Green control (scratch commit on integrated HEAD `288511d8` with the flipped ledger):** rc 0, `TARGET executed_rows=36 … executed=1 … mismatches=0 defects=0`, `PREDICATE R92-C1 pass`.
- **Divergence for L1:** the integrated HEAD ledger is serialized at 1-space indent; BASE and the proposal use 2-space. Parsed content is identical (both 36 executed). No pin on the ledger bytes was found in the 20 of 26 plan files scanned. L1 must pick one convention.

## Tool installs and host facts

No tools installed or updated. `/usr/bin/bwrap` present; `max_user_namespaces` 122865, not modified. pacman not used.

## Scratch

`/fast/scratch/hyaku/kengaku-r92/ExecLedgerFlip` removed before yield. The lane was not edited; the only lane writes are the two report files named in the spec.

## Blockers

None for the flip. One note above (ledger indentation) is a decision for L1, not a blocker.
