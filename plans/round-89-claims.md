# Round 89 — frozen claims (kengaku)

Frozen in commit A (this file and `plans/round89-cases.json`), before any instrument, receipt or score exists.
Base: `192e809d582ecbd544798cbc03da1666a0de23f7` (round-88 closure, `master`). Measured tip: the commit that lands
the receipt, ledger row and corpus edits (named in the round report), never a commit whose bytes changed after the
first score. Nothing below may be edited after freeze; a frozen element that looks wrong is reported, not repaired.

Two claims, causally separable: C1 reads the replay surface (grader bytes, case table, probe, receipt, ledger row);
C2 reads the Q66 claims corpus and the round-88 instrument's record table. Shape: one v1 wave (attack seats ≥25 %).

Measurement note (Q66 applied to this file): every BEFORE figure below is a prediction until the do-nothing control
measures it at BASE. The measured figures are recorded in the report, and a mismatch between a prediction and the
measured figure is recorded as a mispredict, never repaired in place.

## R89-C1 — coverage (lowest non-retired axis, held at its L0 cap 7)

**Move:** a seventh located offline replay of a Terminal-Bench 2.0 grader, `polyglot-rust-c`, by the round-89 replay
counter `plans/round89_c1_replay.py` over the frozen eight-case table `plans/round89-cases.json`. The grader lists
`/app/polyglot`, requires exactly `["main.rs"]`, compiles the file with `rustc` and `g++ -x c++` through `os.popen`
(stderr and status discarded), then runs both binaries on five sizes with `check=True`. The member carries classes
`shell-exec`, `stdout-inspection` and `subprocess-exec`; the first two are the thinnest executed classes in the ledger
(`shell-exec` 1 of 6, `stdout-inspection` 8 of 29 at BASE). The class of the case table is new: a single source
compiled by two toolchains, graded through a subprocess whose failure mode (`CalledProcessError`) is outside the two
graded refusals.

- **Before (BASE `192e809d`, predicted):** `TARGET executed_rows=32 member=polyglot-rust-c located=0 executed=0 cases=0 legs=0 mismatches=0 defects=N`, `PREDICATE R89-C1 fail`, exit 1, where N is measured by the do-nothing control. Ledger at BASE (measured by `python3 -c` over `plans/grader-population-ledger.json` on 2026-11-05): executed 32 of 88 members; `shell-exec` 1 of 6; `stdout-inspection` 8 of 29; `subprocess-exec` 10 of 45.
- **After (measured tip, predicted):** `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`, exit 0. Ledger: executed 32 → 33; `shell-exec` 1 of 6 → 2 of 6; `stdout-inspection` 8 of 29 → 9 of 29; `subprocess-exec` 10 of 45 → 11 of 45.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R89-C1` line and the report):** pass iff the captured grader bytes at the measured revision hash to the frozen subject SHA, the frozen case table is byte-identical to the freeze commit's table, the receipt at the measured revision re-derives under legs L1–L9, the probe re-run from an extraction of the measured tree reproduces the receipt observation block, the probe's bytes hash to the counter's pinned `TRUSTED_TOOL_SHA`, and the observed vector of all eight frozen cases equals its predicted vector.
- **Kill rule:** any leg L1–L9 failing at the measured tip makes the claim unmet; so does any mismatch between the probe re-run and the receipt, and so does a probe whose bytes differ from `TRUSTED_TOOL_SHA` (the round-88 forged-probe hole: an echo probe that reproduces its own receipt). Editing the case table after commit A voids the claim.
- **Do-nothing control:** the counter at BASE must exit 1 with `PREDICATE R89-C1 fail`. Ledger-only control (ledger row flipped, receipt absent) must fail L1. Forged-receipt control (stamp `LANE_TIP` replaced by a commit that is not an ancestor of the measured revision) must fail L3. Forged-probe control (the probe's grader call replaced by an echo of the predicted vector, receipt regenerated from it) must fail L9. Each control's exit code and defect lines are committed under `.ufo/waves/round-89/` before the measured tip is scored.
- **Sourced:** the grader bytes are row `S278` in `corpus/SOURCES.md`, opened in this round (2026-11-05):
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py`
  returned HTTP 200, 1638 bytes, sha256 `baed5e4d…92f9`, byte-identical to the round-52 capture; line 19 `assert polyglot_files == ["main.rs"], (`.
- **Honest limits:** (a) the case table yields **three** distinct predicted vectors (P, F, E), not eight; (b) a receipt whose observation block is correct and whose stamp names the measured tip is not distinguishable by observation from a freshly minted one — L9 pins the probe bytes, not the author; (c) the probe runs the grader in bubblewrap, not in a Terminal-Bench container, and the toolchain is the host's (`rustc 1.99.1`, `g++ 16.2.1`), so the vector is a statement about this host's toolchain.

## R89-C2 — calibration (held at ceiling 10): the Q66 counter-side check made sound on its four round-88 attack fixtures

**Move:** `plans/round89_claim_figures.py` replaces the round-88 instrument (`plans/round88_claim_figures.py`, not edited).
Four changes, each answering a named round-88 attack finding: (a) the KNOWN check compares `(claim, key, claimed, measured)`,
so a doctored claimed value is `UNEXPECTED`; (b) the extracted record set is compared against the pinned table
`plans/round89-q66-records.json` (every record's claim, kind, key, op and claimed value), so a deleted before-figure or a
doctored claimed value is a defect; (c) the selftest battery runs inside the predicate path; (d) the record table is
itself pinned to its blob sha at the freeze commit.

- **Before (BASE `192e809d`, predicted):** the round-88 counter's fixtures are the attack wave's controls: a doctored
  `defects=7` → `defects=9` for R87-C1 passes (`PREDICATE R88-C2 pass`, ExecCtrlR88 control B); a deleted R85-C1 Before
  sentence passes (control C). The round-89 control battery, run against `plans/round88_claim_figures.py` at BASE,
  measures these two as green; the count of red controls is therefore predicted to be 0 of 4.
- **After (measured tip, predicted):** `plans/round89_claim_figures.py --controls` prints four `CONTROL <id> red`
  lines (doctored-claimed, deleted-figure, doctored-key, selftest-removed-from-path) and `CONTROL tip green`;
  `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0` and `DEFECTS n=0` at the tip, with
  `PREDICATE R89-C2 pass`, exit 0.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R89-C2` line and the report):** pass iff
  at the measured revision every extracted before-figure record equals the pinned record table, the mismatch set equals
  the frozen KNOWN set `{(R87-C1, kv:defects, claimed=7, measured=3)}` exactly, the selftest battery exits 0, and all four
  control fixtures are red while the unmodified tip is green.
- **Kill rule:** any `DEFECT F*` line at the tip, any record-table divergence at the tip, any control fixture that stays
  green, a selftest failure, or any edit to a frozen claims file, case table, record table, counter or this instrument
  after commit A makes the claim unmet.
- **Controls:** do-nothing = the round-88 counter run on the round-89 control fixtures (predicted green on the two attack
  fixtures, per above); able-to-fail = the four control fixtures (`CONTROL`); separation = the C2 counter is unaffected by
  a C1 receipt removal. Transcripts are committed under `.ufo/waves/round-89/L2/`.
- **Axis note:** calibration held at its ceiling of 10 (the round-86 and round-88 precedent): a move at the ceiling is
  recorded as a count, not added to the score. Operability and freshness are not claimed.

## Frontier step (not a claim)

`corpus/SOURCES.md` gains `S278` (grader bytes for `polyglot-rust-c`, tier A for scope "member replay only", status
`mined`, used-by the round-89 lesson and `corpus/evidence/round89/`). Census before → after by
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0 required at round end).
Census before (2026-11-05, measured): exit 0, `kengaku ok`, 269 rows.

## Mistake mined (not a claim)

Class `figure-not-measured` (the round-88 attack wave's KNOWN-check and deleted-figure findings): a before-figure
validated only by its own extraction net is not a guard. Captured-by: none until this round (QUALITY.md Q66, executable
half not yet sound). Fix: C2 above, with the four controls shown able to fail.

## Exploratory claims

None. Assimilation: none — `merge/kengaku/` remains blocked by L0 `kengaku | round-54`. considerthese item 1
(`considerthese/2026-10-26.md`, routed-findings burn-down) is mined in the round-89 lesson; it is not implemented here.
