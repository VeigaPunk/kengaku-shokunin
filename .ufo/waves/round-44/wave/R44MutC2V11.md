# R44MutC2V11 — mutation test of V11 in `plans/round44_c2_verify.py` (round 44 wave, 2026-10-26)

Seat: R44MutC2V11 (mutation-tester, leaf). Target invariant: the frozen V11 freeze control
`.ufo/waves/round-44/claims/c2_predictor_control.py` (sha256 `15300786…b9ead8`) detects single-edit defects in
the V11 machinery of `plans/round44_c2_verify.py` — `STATE_KINDS`, `states()`, `v11()`, `sandboxed()`,
`GRADE_PY`, `PREDICT_PY` — i.e. its four required predictor verdicts (always-true→DEFECT, token-set→DEFECT,
exact-lines→DEFECT, substring→ok) flip. One plausible single-edit mutant per named site, n=6.

Method: the frozen control imports the counter from `<cwd>/plans/round44_c2_verify.py`, so each mutant lived
in its own scratch mirror lane root (`/fast/scratch/hyaku/kengaku-r44/R44MutC2V11/<mid>/`) holding the mutated
counter plus the two frozen inputs V11 reads (`plans/pkg-spec-r44.json` `1f31cf40…bbe4b8`,
`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/test_outputs.py` `f59ebc72…ed9f9` — digests verified
equal to the counter's pins before use). Mutant copies only; the lane file was never written. Every run went
through `claims/envelope.sh`. Pristine baseline first: `receipt-pristine.txt` — all four rows as required,
`CONTROL-C2-PREDICTOR red-as-required`, exit 0, tally `states=48 grader_pass=24 grader_fail=24 disagree=0`.

## Mutant table

All edits at `plans/round44_c2_verify.py:<line>` in the scratch copy (line in the frozen file; pristine
sha256 `334ce2da…fc82a6`). Detector = frozen control, envelope-wrapped, per-mutant receipt.

| id | site (file:line) | old → new | mutant sha256 (16) | caught | observed (required verdicts) |
|---|---|---|---|---|---|
| m1-statekinds-absent | :381 `STATE_KINDS` | `"absent", "empty", "comma"` → `"empty", "comma"` | `1eb57cbb574c5517` | **survived** | `red-as-required` exit 0; tally silently 26/22 (was 24/24); no row flips |
| m2-states-pop-elided | :404 `states()` drop-one | `c.pop(rng.randrange(len(c)))` → `rng.randrange(len(c))` | `1f04ec19c2deec75` | **survived** | `red-as-required` exit 0; tally 27/21; no row flips |
| m3-v11-dis-inverted | :520 `v11()` | `if graded[k] != pred[k]]` → `== pred[k]]` | `9d6b81c646e19baa` | **caught** | substring flips: required=ok, got DEFECT `disagree=48`; control `NOT-AS-REQUIRED` exit 1 |
| m4-sandbox-unshare-net-dropped | :477 `sandboxed()` | `[BWRAP, "--unshare-net", "--unshare-pid"` → `[BWRAP, "--unshare-pid"` | `9cb4cafd4026929d` | **survived** | byte-identical verdicts to pristine (24/24, disagree=0); net fence loss invisible |
| m5-grade-except-true | :463 `GRADE_PY` | `res.append(False)` → `res.append(True)` | `d96b0939b854d16a` | **caught** | grader 48/0 pass/fail; substring required=ok got DEFECT `disagree=24`; `NOT-AS-REQUIRED` exit 1 |
| m6-predict-exec-ns-dropped | :471 `PREDICT_PY` | `"exec"), ns)` → `"exec"))` | `148c2c2aa5322ad4` | **caught** | every predictor `predictor failed: predict.py exit=1` (KeyError ns["predict"]); substring required=ok got DEFECT; `NOT-AS-REQUIRED` exit 1 |

Caught 3/6 (m3, m5, m6). Survivors are coverage findings, not licence to change the contract.

## Why the survivors survive

- **m1 / m2:** V11's non-vacuity floor is only `npass>=8 and nfail>=8`; with 8 fail-kinds ×3 the executed set
  keeps ≥21 grader fails after either edit, and none of the four control predictors is sensitive to WHICH
  states exist — `substring` agrees with the grader on any text by construction (`test_outputs.py:121-122`
  and the predictor test the same predicate). So the generator can silently lose the `absent` (None) case or
  the drop-one pop and the control stays green.
- **m4:** neither `GRADE_PY` nor `PREDICT_PY` touches the network, so verdicts cannot move when the net fence
  is removed; the fence protects execution, not the verdicts, and nothing in the control observes it.

## Draft controls for the survivors (this dir, offered to the L1; not frozen)

- `draft-c2-tally-pin.py` — kills m1 and m2. Pins, independently of the module under test, (1) the sha256 of
  the 48-state list `states()` must produce (`a8a5de5b…16ce6241`, embedded constant) and (2) the executed
  substring-row tally `states=48 grader_pass=24 grader_fail=24 disagree=0`. Calibration: base →
  `red-as-required` exit 0 (`receipt-tally-base.txt`); m1 → DEFECT `states_sha=95ea4517…` + tally 26/22,
  exit 1 (`receipt-tally-m1…`); m2 → DEFECT `states_sha=5b5f1dca…` + tally 27/21, exit 1
  (`receipt-tally-m2…`). Trade-off named: it re-pins the documented `random.Random(44)` output, so any
  deliberate state-set change needs the two embedded pins refreshed.
- `draft-c2-fence-canary.py` — kills m4. Runs a `/proc/net/dev` canary through the counter's own
  `sandboxed()` and requires the loopback-only netns (`nics == ['lo']`). Calibration: base → `nics=['lo']`
  ok, exit 0 (`receipt-fence-base.txt`); m4 → host interfaces `['br-4e7a72f4b2ff', …, 'enp7s0', 'lo']`
  DEFECT, exit 1 (`receipt-fence-m4…`).

## Envelope record (QUALITY Q32)

Every run above was wrapped: `envelope.sh <scratch>/env-<run> /usr/bin/python3 <control> <scratch>/w-<run>`
with cwd = the mirror. All 12 receipts carry `local_bin_content_before=328be01808ba022f after=328be01808ba022f
unchanged`; no run returned exit 4 / INVALID. Example lines (`receipt-pristine.txt`):

```
ENVELOPE start 20:40:08 cwd=/fast/scratch/hyaku/kengaku-r44/R44MutC2V11/base
ENVELOPE end 20:40:10 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Full per-run start/end lines are in the receipts (`receipt-pristine.txt`, `receipt-m1…`–`receipt-m6…`,
`receipt-tally-base/-m1/-m2.txt`, `receipt-fence-base/-m4.txt`).

## Restoration evidence

Mutants were applied only to scratch copies; the lane counter was read, never written.

```
before: 334ce2dac6828f8d7b0d57610f7204db2dcf5c5c2686ed406ab19880abfc82a6  plans/round44_c2_verify.py
after:  334ce2dac6828f8d7b0d57610f7204db2dcf5c5c2686ed406ab19880abfc82a6  plans/round44_c2_verify.py
```

Restored bytes re-detected green twice after the mutant runs (base control in `receipt-tally-base.txt` exit 0,
`receipt-fence-base.txt` exit 0). The frozen control, counter, captures and claims tree under the lane are
untouched; no sibling source was modified.

## Limits

- n=6, one single-edit mutant per named site; other V11 mutations (e.g. threshold `8`→`1`, pin-check removal,
  `timeout` weakening) were not probed this probe.
- m5's catch is doubly red (predictor disagreement AND non-vacuity `nfail=0<8`); the table records the flip.
- The drafted controls are proposals for the L1 to integrate; they are not run by the frozen counter and were
  calibrated only against pristine + their target survivors.
- Host python3 stands in for the image interpreter (named round-44 limit); scratch dir removed after the run.

VERDICT: v11-mutants-caught-3/6
