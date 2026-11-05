# Round 88 — frozen claims (kengaku)

Frozen in commit A (this file and `plans/round88-cases.json`), before any instrument, receipt or score
exists. Base: `801b903af6412cb424209a60b3a52e56c3532866` (round-87 spot-check tip, `master`). Measured tip:
the commit that lands the receipt, ledger and corpus edits (named in the round report), never a commit
whose bytes changed after the first score. Nothing below may be edited after freeze; a frozen element that
looks wrong is reported, not repaired.

Two claims, causally separable (C1 reads the replay surface, C2 reads the claims corpus and historical
counters). Shape: one v1 wave.

## R88-C1 — coverage (lowest non-retired axis)

**Move:** a sixth located offline replay of a Terminal-Bench 2.0 grader, `fix-git`, by the round-88
replay counter `plans/round88_c1_replay.py` over the frozen eight-case table `plans/round88-cases.json`.
The captured grader compares md5 digests of paired files under `/app` (`resources/patch_files/` versus
`personal-site/`); the case table exercises content match/mismatch, a missing new file, trailing
whitespace tolerance, and `IsADirectoryError` surfaces on both legs. This member carries classes
`crypto-credential` and `file-artifact`; no recent round has moved `crypto-credential`.

- **Before (BASE `801b903a`):** `TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`,
  `PREDICATE R88-C1 fail`, exit 1.
- **After (measured tip):** `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`,
  `PREDICATE R88-C1 pass`, exit 0. Ledger: executed 31 → 32; `crypto-credential` 2 of 12 → 3 of 12;
  `file-artifact` 23 of 76 → 24 of 76.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R88-C1` line and the report):**
  pass iff the captured grader bytes at the measured revision hash to the frozen subject SHA, and the receipt
  at that revision re-derives under legs L1–L8, and the probe re-run from the measured tree reproduces the
  receipt observation block, and the observed vector of all eight frozen cases equals its predicted vector.
- **Kill rule:** any leg L1–L8 failing at the measured tip makes the claim unmet; so does any mismatch between
  the probe re-run and the receipt. Editing the case table after commit A voids the claim.
- **Do-nothing control:** the counter at BASE must report `defects=3` (exit 1). A ledger-only control (ledger
  row flipped, receipt absent) must fail L1. A forged-receipt control (stamp `LANE_TIP` replaced by a commit
  that is not an ancestor of the measured revision) must fail L3. Each control's exit code and defect lines are
  committed to `.ufo/waves/round-88/L1/` before the measured tip is scored.
- **Sourced:** the grader bytes are row `S277` in `corpus/SOURCES.md`, opened in this round (2026-11-05):
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-git/tests/test_outputs.py`
  returned HTTP 200, 1194 bytes, sha256 `a8a6f51e…43f3`, byte-identical to the round-52 capture.
- **Honest limit (carried):** a receipt whose observation block is correct and whose stamp names the
  measured tip is not distinguishable by observation from a freshly minted one. L6 reproduces the
  observation; it does not authenticate an author.

## R88-C2 — capability acquisition: Q66 counter-side check (routed defect R87-V4/V2)

**Move:** `plans/round88_claim_figures.py` lands — the executable half of QUALITY.md Q66 routed to round 88
by the round-87 verifier spot-check. For every claim in the eight frozen claims files `plans/round-8?-claims.md`
(rounds 80–87), the instrument extracts each before-figure record from the claim bytes (never hand-copied),
re-runs that claim's own counter at that claim's own BASE revision, and compares. Extraction is mechanical:
`before`/`at BASE` markers open spans, end-markers and clause boundaries close them, and only counter-output
vocabulary inside a failing span yields a record.

- **Before (BASE `801b903a`):** the instrument does not exist —
  `git cat-file -e 801b903a:plans/round88_claim_figures.py` fails; the Q66 counter-side check is unreachable.
- **After (measured tip):** `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`
  with exactly one `MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`, `DEFECTS n=0`,
  `PREDICATE R88-C2 pass`, exit 0; `python3 plans/round88_claim_figures.py --selftest` prints four
  `SELFTEST … pass` lines and `PREDICATE R88-C2-SELFTEST pass`, exit 0.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R88-C2` line and the report):**
  pass iff every extracted before-figure record is checked, every claim's counter completes at its BASE, the
  mismatch set equals the frozen KNOWN set `{(R87-C1, kv:defects): claimed 7, measured 3}` exactly — reported
  `MISMATCH KNOWN`, never `UNEXPECTED` — and the selftest battery exits 0.
- **Frozen KNOWN set (the corpus's one documented mispredict):** the round-87 claims file asserts
  `defects=7` as R87-C1's BASE figure; the counter's own BASE output measures `defects=3`. This is routed
  defect R87-V2, recorded here so the instrument reports it on the record instead of silently passing or
  failing on it.
- **Kill rule:** any `MISMATCH UNEXPECTED`, any `F5-missing-known`, any `DEFECT F*` line, a selftest failure,
  or any edit to a frozen claims file, case table, counter or this instrument after commit A makes the claim
  unmet.
- **Controls:** do-nothing = the instrument absent at BASE (predicate unreachable, verified by
  `git cat-file -e`). Able-to-fail = `--selftest` T1 feeds a doctored claims copy (`defects=7`→`defects=9`)
  through the same extract+check pipeline and must observe `verdict=mismatch`; T2–T4 pin marker negatives,
  backward `at BASE` direction and dedupe. Selftest output is committed to `.ufo/waves/round-88/L1/`.
- **Axis note:** capability acquisition, no axis-score move — the same framing as round-82 C3. The instrument
  measures the claims corpus; it does not itself move coverage, calibration or any held score.

## Frontier step (not a claim)

`corpus/SOURCES.md` gains `S277` (grader bytes for `fix-git`, tier A for scope "member replay only",
status `mined`, used-by the round-88 lesson). Census before → after is measured by
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0 required at round end).

## Mistake mined (not a claim)

Class `figure-not-measured`: the round-87 claims file's R87-C1 before-figure `defects=7` was asserted without
being copied from the counter's own BASE output (Q66; routed defects R87-V2/V4). The counter measured `defects=3`.
Fix: `plans/round88_claim_figures.py` makes every frozen before-figure re-derivable and reports the known
mispredict on the record. Red-before is the round-87 spot-check's V2 finding; green-after is `PREDICATE R88-C2 pass`
with the `MISMATCH KNOWN` line.

## Exploratory claims

None. Assimilation: none — `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.
