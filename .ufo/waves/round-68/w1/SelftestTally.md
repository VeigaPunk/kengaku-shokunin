# SelftestTally — R68-C2 routed defect 3: committed round-67 probe selftest tally

Seat: `SelftestTally` (leaf, one instrument write into L: `corpus/evidence/round68/r67-probe-selftest.txt`).
Round: 68, wave 1. Date (UTC): 2026-11-03T23:00:47Z.

## Verdict

PASS. The committed round-67 probe's `--selftest` ran green-and-red as designed
(`SELFTEST green_rc=0 red_rc=1 ok`, in-runner `rc=0`) and its tally is now committed with the
probe's own sha256 recorded in-file. The committed round-67 receipt of record also re-derives
clean (`PREDICATE R67-C1 pass`, in-runner `rc=0`). Every R68-C2 E3 condition is satisfied by the
committed bytes.

## Commands and captured exits

Both exits were captured inside the runner (`cmd; rc=$?`), not taken from a wrapper or typed.

### 1. `--selftest` (R68-C2 E3 primary)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round67_c1_pipeline_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r68/SelftestTally/tally
rc=0
```

Verbatim captured stdout+stderr (9 lines, exactly the bytes committed in the tally):

```
CHECK ok cases=6
PREDICATE R67-C1 pass
CHECK defect: q1-ref vector FPPP != frozen PPPP
CHECK defect: q1-ref frozen label match contradicts vector FPPP
CHECK defect: q1-ref rc=0 is not the pytest status for vector FPPP (want 1)
CHECK defect: VECTOR q1-ref FPPP disagrees with its junit PPPP
CHECK findings=4
PREDICATE R67-C1 fail
SELFTEST green_rc=0 red_rc=1 ok
```

The instrument's red fixture is a single-leg flip (`VECTOR q1-ref exists=P` → `exists=F`) in a copy
of the committed receipt, so `check_receipt` reports four findings on it — that is the expected
red-fixture reading, not drift. The final `SELFTEST` line is the claim's quoted string exactly.

### 2. `--check-receipt` on the committed round-67 receipt

```
python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt
rc=0
```

Verbatim output (2 lines); last line:

```
PREDICATE R67-C1 pass
```

## Committed evidence

- `corpus/evidence/round68/r67-probe-selftest.txt` — 14 lines, LF endings, sha256
  `5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467`.
  Shape: line 1 heading, line 2 UTC date, line 3 `PROBE sha256=03793f4f…`, line 4 the command as run,
  then the 9 verbatim selftest lines, last line `rc=0`.
- `PROBE sha256=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e`
  — re-computed by `sha256sum plans/round67_c1_pipeline_probe.py` in this seat, matches the R68-C2 E3
  expectation and the epoch-1 erratum sha the claim names (the other cited sha,
  `32bacf1d…`, is the pre-A1 probe and is not this file's bytes).
- Committed receipt re-derived at check time: `corpus/evidence/round67/pipe/receipt.txt`
  sha256 `41076ad5253a8ac0d31f61e18bf13934c154a91681449d6a62d95de50618e14d` (unchanged; this seat
  read it, never wrote it).

The committed tally file was verified byte-for-byte against the captured stream:
`diff -u` of (header + `selftest.out` + `rc=0`) against the committed file → clean.

## R68-C2 E3 correspondence (checked directly, gate not executed by this seat)

`plans/round68_c2_correction_gate.py` is another seat's instrument built in this wave; this seat
did not run it and did not write its `gate/red-before.txt` receipt. E3's conditions were checked
against the committed bytes:

- file exists at the named path — yes;
- contains a `PROBE sha256=03793f4f…` line — yes (line 3);
- contains a `SELFTEST` line — yes (`SELFTEST green_rc=0 red_rc=1 ok`);
- contains an `rc=` capture — yes (`rc=0`, last line);
- gate's own re-hash of `plans/round67_c1_pipeline_probe.py` equals `03793f4f…` — verified here by
  `sha256sum` (same bytes the gate will hash).

## Notes and risks for the L1

1. The tally's line 4 records the command *as run*, including the ephemeral scratch work dir
   (`/fast/scratch/hyaku/kengaku-r68/SelftestTally/tally`), which is deleted before yield. Nothing in
   the committed file depends on that path existing; the selftest needs `--work` only to stage its
   one-copy red fixture.
2. Readability, not correctness: because the selftest proves both legs in one run, the verbatim block
   contains `PREDICATE R67-C1 fail` from the injected red fixture, seven lines above the final
   `SELFTEST ... ok`. The claim's E3 requires presence checks only; a human reader should not mistake
   that line for the tally's own verdict. The `#` heading on line 1 names the provenance, and the
   exact shape was fixed by the seat spec, so no annotation was added to the committed file.
3. This seat ran the probe only in `--selftest` and `--check-receipt` modes; it did not run `--run`,
   did not touch port 8080 (nothing bound or started), and did not modify the probe (sha unchanged
   before and after: `03793f4f…`).
4. Tool installs: none. pacman not used (host-paused); no uv/npx/binary install needed — the
   instrument is stdlib-only and the probe's venv is not needed for these two modes.
5. Scratch `/fast/scratch/hyaku/kengaku-r68/SelftestTally` removed before yield; `/tmp` unused.

## Tally line

```
TALLY committed=corpus/evidence/round68/r67-probe-selftest.txt selftest-ok=True check-receipt=pass
```
