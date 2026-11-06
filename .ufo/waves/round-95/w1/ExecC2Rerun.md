# ExecC2Rerun: scoped findings (R95-C2)

Tip T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`. Full report, raw receipts and drivers:
`.ufo/waves/round-95/w1/ExecC2Rerun/report.md`.

## Census re-measurement

The census reproduces the frozen predicate: `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`,
`PREDICATE R95-C2 pass`, rc 0 (`ExecC2Rerun/census-rerun.txt`). The in-sample claim (14 → 0) stands.

## Held-out forgeries (five false gates on gate v2, each wrong on a demonstrated input)

- g1 chmod-only commit not counted as a touch (numstat `0 0`): counter **misses** (pass 5/5).
- g2 table rows starting with `.` dropped: counter **misses** (pass 5/5).
- g3 `--ancestry-path` drops a pre-freeze side edit merged treesame: counter **fails it**, but only at W3 P1 and W5 K5, not at W2. The designed input is undetected.
- g4 gitlink rows skipped: counter **misses** (pass 5/5).
- g5 non-ASCII path rows skipped: counter **misses** (pass 5/5).
- e5 CR-tolerant row match: equivalent to v2 on every input (control, not counted).

Held-out result: four of five pass the counter 5/5. The counter does not discriminate held-out forgeries beyond the in-sample set.

## Unmodified gate v2: verdict defects found

- N1 `git replace` on an edited commit: v2 returns rc 0 `PREDICATE pass` on a changed instrument. **Major**, verdict flip. Route to round 96: `--no-replace-objects`.
- N2 symlink instrument: v2 hashes the link text, so a followed-target change returns rc 0 `intact`. **Major**, verdict flip; policy-dependent [INFERENCE]. Route to round 96.
- N3 gitlink row: an unchanged pin is reported broken (fail-closed). **Minor**.
- Tag object as `--rev`: correct on both cases (rc 1 on breach, rc 0 intact). No defect.

## Commands and outputs

- `python3 "$S/lane/plans/round95_false_gate_census.py" --lane "$S/lane" --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 --work "$S/w"` → `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, rc 0.
- `python3 "$S/lane/plans/round95_c2_counter.py" ... --tool-file ".ufo/waves/round-95/w1/ExecC2Rerun/forgeries/<id>.py"` → counter output per variant in `ExecC2Rerun/counters/`.
- Input demos: `ExecC2Rerun/demo-inputs-receipt.txt`, `native-inputs-receipt.txt`, `tag-input-receipt.txt`.

## Tools

None installed or upgraded. No host change.

## Paths written

- `.ufo/waves/round-95/w1/ExecC2Rerun.md` (this file)
- `.ufo/waves/round-95/w1/ExecC2Rerun/` (report.md, census, forgeries and diffs, counters, demo receipts, drivers)
