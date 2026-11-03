# DeterminismProbe — R66-C1 probe determinism check

Seat: `DeterminismProbe` (round 66, wave 1, leaf). One extra run of the frozen probe in a scratch mirror;
the lane receipt of record was not touched. Item: determinism check of R66-C1, step 1–4 as dispatched.

## Verdict

- **VECTOR lines: identical to the frozen control.** `diff` of the VECTOR lines only
  (`prefreeze-run2.txt` vs mirror receipt) → **exit 0, no differences**; also run1 vs run2 → exit 0.
  Five cases, 13 keys each; K1 13/13 P; K2 all F; K3 exists P / 12 F; K4 column ws1 P, ws2/ws4 F, row all P;
  K5 column all P, row ws1 P, ws2/ws4 F. **No outcome differs → no flake finding.**
- **Mirror run**: `--run` → **EXIT=0**, 62.76 s, `PREDICATE R66-C1 pass`; receipt 9204 bytes
  sha256 `dd70201f8a56ea3274bf63404c7afc3f80fe977ad37ee9f4d269d7b077bdedfd`; `PROBE`/`GRADER` lines match
  the frozen bytes (`c5ef1b54…`, `4ae4285e…`). `--check-receipt` on the mirror receipt → **exit 0**
  (`CHECK ok cases=5`). Mirror probe/grader/case shas equal the lane bytes (table in `result.md`).
- **FRAGMENT lines: key set identical (33/33), 17 texts byte-identical, 16 differ by exactly one
  character** — the spawn rank digit at offset 65 of `-- Process N terminated with the following error:`
  (160-char truncated message). Cause: `torch.multiprocessing.spawn` reports the first worker that raised;
  which rank surfaces is scheduler-dependent. All 16 are single `replace` opcodes at offset 65
  (`DeterminismProbe/fragment-table.txt`). The differing keys are listed with run2→mirror ranks in `result.md`.
- **CASE lines**: `case_sha` identical for all five; `junit_sha` differs for all five (run2, mirror,
  working tree pairwise). Cause measured, not inferred: pytest junit `timestamp=` and per-test `time=`
  attributes, plus spawn rank and `ProcessContext object at 0x…` heap addresses in failing cases
  (`DeterminismProbe/junit-sha-table.txt`; normalising those makes k1-ref XML byte-identical).

## Findings (reported, nothing edited)

- **D1 (no flake).** The frozen vector table is reproducible across three independent runs (run1, run2,
  this mirror run); the predicate outcome is stable. R66-C1's outcome evidence is not run-sensitive.
- **D2 (`junit_sha` is run-local, not a cross-run invariant).** `prefreeze-run2.txt` now fails
  `--check-receipt` against the working tree: exit 1 with five `CHECK defect: <case> junit_sha does not
  match committed junit bytes` (read-only invocation of the lane counter). The pre-freeze junit bytes are
  intact at `9a07df6a` and match the control's `junit_sha` values exactly for all five cases; the
  working-tree junit is the post-freeze run's, and HEAD `2c1ef88a` says so ("junit replaced, pre-freeze
  junit retained at 9a07df6a"). So the frozen predicate clause "every `case_sha` and `junit_sha` equals
  the committed bytes" is satisfiable only by the same run's bytes — the probe's receipt-local junit
  design protects receipts placed outside the evidence dir, not the committed dir itself. Calibration
  note for the claim wording / checker design (e.g. a junit-dir or commit argument for control receipts);
  the claim text and kill rules are not changed by this seat.
- **D3 (bind the right thing).** FRAGMENT text and `junit_sha` are not deterministic; only the fragment
  key set and the VECTOR table are. A future counter that binds FRAGMENT text or a control receipt's
  `junit_sha` across runs will flake.

## Evidence (all written this seat, observed bytes)

- `DeterminismProbe/result.md` — commands, exit codes, tables.
- `DeterminismProbe/mirror-receipt.txt` — the mirror run's receipt (sha256 `dd70201f…`).
- `DeterminismProbe/vector.diff` (`(no differences)`, diff exit 0), `DeterminismProbe/lane-vs-prefreeze.vector.diff`
  (lane receipt vectors also identical), `DeterminismProbe/run1-vs-run2.vector.diff` (empty, exit 0).
- `DeterminismProbe/fragment-table.txt`, `DeterminismProbe/junit-sha-table.txt`.

## Bounds kept

- Scratch `S=/fast/scratch/hyaku/kengaku-r66/DeterminismProbe` removed before yield; nothing written in
  the lane except this seat dir (`DeterminismProbe/`, `DeterminismProbe.md`). Lane receipt sha256
  `8b164d5b…`, mtime 18:04:49 unchanged by this seat; lane junit untouched.
- Port 12355 free at start (no listener, no probe process); the probe's own flock at
  `~/.local/share/kengaku-r66/port-12355.lock` was used as designed.
- No network; no install (nothing needed); no git/jj mutation; no model, no `ask`.
- Confidence: high — byte-level diffs over three runs.
