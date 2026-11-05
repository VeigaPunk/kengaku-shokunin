# ExecCtrlC2 — R89-C2 before-measurement: round-88 counter on the round-89 control fixtures

Seat: ExecCtrlC2 (leaf, item R89-C2 Before). Scratch only; lane clone at `a9b8a1a00b6a5ab5206be4d377dba439e02f8244` (verified `rev-parse --show-toplevel` = clone root, `HEAD` = tip). No production file, lane, or fleet state was written. Transcript: `round88-baseline.txt` (same directory).

Method: `plans/round88_claim_figures.py` loaded from the clone with `importlib`; module-level `git` replaced by a wrapper that returns fixture bytes for `show <rev>:plans/round-87-claims.md` or `plans/round-85-claims.md` and delegates everything else to the real `git`. Fixtures derived from the tip bytes:

- (a) `plans/round-87-claims.md`, first `defects=7` -> `defects=9`.
- (b) `plans/round-85-claims.md`, the R85-C1 line 58 (`Before (BASE \`0de45354\`): \`TARGET members=1 ...\``) removed.
- (c) `plans/round-87-claims.md`, first `defects=7` -> `defect=7`.

## Observed vs predicted (round-88 `run_check`, `--rev` = tip)

| Fixture | Predicted (frozen Before) | Observed `PREDICATE R88-C2` | rc | Match |
|---|---|---|---|---|
| tip (sanity) | pass | `pass` | 0 | yes |
| (a) doctored-claimed | green | `pass` | 0 | yes |
| (b) deleted-figure | green | `pass` | 0 | yes |
| (c) doctored-key | not stated per item; claim's "0 of 4 red" aggregate implies green | `fail` | 1 | **no (mispredict)** |

Detail lines from the transcript:

- (a): `MISMATCH KNOWN R87-C1 kv:defects claimed==9 defects claimed =9 measured 3`, then `DEFECTS n=0`, `PREDICATE R88-C2 pass`. The doctored claimed value passes because the KNOWN check does not compare the claimed value.
- (b): `RECORDS ... records=49` (tip: 56; 7 records removed), `DEFECTS n=0`, `PREDICATE R88-C2 pass`.
- (c): `DEFECT F4-unparsed R87-C1:kv:defect defect absent from TARGET`, `DEFECT F5-missing-known R87-C1 kv:defects`, `DEFECTS n=2`, `PREDICATE R88-C2 fail`, rc 1.

## Findings

1. **Mispredict, R89-C2 Before ("0 of 4 red").** The frozen claim predicts the round-88 counter is green on the control battery, so the red count is 0 of 4. Measured: the doctored-key fixture (c) is red at round 88 (`PREDICATE R88-C2 fail`, rc 1). Command: `python3` load of `plans/round88_claim_figures.py` with fixture (c) substituted; `run_check(lane, a9b8a1a0…, work)`. Output: the `DEFECT F4-unparsed` and `DEFECT F5-missing-known` lines above. Per the item, a mismatch is a finding and is recorded here, not repaired. The mispredict is that round-88 detects the doctored key already, so the red-control count at BASE is at least 1, not 0. (The claim's (c) row is itself a prediction the item asked to test.) Recorded as a mispredict in the claim's own terms; not edited.

Confirmations (not findings): (a) and (b) are green at round 88 as the frozen claim predicts. The (a) result shows the KNOWN-check hole the R89 change (a) targets: a doctored claimed `9` is reported as `KNOWN` and the predicate passes.

## (d) Selftest in the predicate path (round 88)

Round 88 has no selftest hook in `run_check`. `grep -n "selftest\|run_check"` output:

```
376:def run_check(lane: Path, rev: str, work: Path) -> int:
493:def selftest(lane: Path, rev: str, work: Path) -> int:
512:        tmp = Path(tempfile.mkdtemp(prefix="q66-selftest-", dir=work)) / "claims.md"
551:    tmp = Path(tempfile.mkdtemp(prefix="q66-selftest-", dir=work)) / "dup.md"
568:    parser.add_argument("--selftest", action="store_true",
579:    if args.selftest:
580:        return selftest(lane, proc.stdout.strip(), work)
581:    return run_check(lane, proc.stdout.strip(), work)
```

`run_check` (lines 376–491) never references `selftest`; `inspect.getsource(run_check)` contains no `selftest` substring (checked). `main` dispatches exclusively: `--selftest` calls `selftest`, otherwise `run_check`. So a selftest failure cannot change the `PREDICATE R88-C2` line. Observed: selftest on tip rc 0 (`PREDICATE R88-C2-SELFTEST pass`); selftest on fixture (c) rc 1 (`T1-doctored-extract fail`, `T1-doctored-mismatch fail`, `PREDICATE R88-C2-SELFTEST fail`) while the `run_check` on (c) reports only F4/F5 defects and no SELFTEST line. Fixture (c) is also the reason the round-88 selftest, separately, is red. This is the "selftest in path" hole R89-C2 (c) closes.

## Frozen-element notes (reported, not edited)

- Item ambiguity in the (b) fixture: `plans/round-85-claims.md` has two lines beginning `Before (BASE` containing `TARGET` (line 58, R85-C1; line 108, R85-C2). The fixture uses line 58 (the R85-C1 section), per the item's wording "the R85-C1 line".
- The frozen claim's aggregate "0 of 4 red" is contradicted by fixture (c), as Finding 1.

## Tooling

No tools installed or updated. Scratch tree `/fast/scratch/hyaku/kengaku-r89/ExecCtrlC2/` removed after this report.

SEAT ExecCtrlC2 VERDICT FINDINGS findings=1
