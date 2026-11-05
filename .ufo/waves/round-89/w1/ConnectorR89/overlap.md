# R89 ConnectorR89 — sibling-overlap scan (read-only, report only)

Seat: ConnectorR89 (leaf; no subagents). Judged on coverage and calibration.
Scope: the 20 sibling lanes `/home/vgpnk/Projects/shokunin/*-shokunin` minus `kengaku-shokunin`.
Writes: this file only. Reads: `grep`/`glob` over the sibling trees with `gitignore=false`
(so `.ufo/` and `corpus/` are included), plus read-only `git log --diff-filter=A` and `git rev-parse`
in the sibling repos for dating. Nothing was edited, staged, committed or run in any sibling.
Nothing absorbed. Dates are first-add commit dates of the file, not dates of the sha or the
clause inside it.

Frozen claims were read in full first (`plans/round-89-claims.md`, `#EDFB`). No frozen element
looked wrong to this scan; no edit was made to one.

## Summary

| Mechanism | Sibling hits | Verdict | Fleet-first (earliest dated hit located here) | Shared-standard holder (proposal) |
|---|---|---|---|---|
| (a) claims-figure extractor that re-derives or re-runs historical instruments | 6 | DUPLICATE (partial: no record table, no KNOWN tuple) | mori `round-44/figures.tsv` 2026-10-25 (figure at rev); kama `round-27` `CriticBoundaryLegProbe/harness.py` 2026-10-23 (pinned counter re-run) | tameshi (`tools/selfstate-freshness.py`) |
| (b) counter pins its probe or tool by sha256 constant | 13 | DUPLICATE (the mechanism is common; R89-C1 L9 is not novel fleet-wide) | kama `round-21/.../RegressSkillGates/sweep.py` 2026-10-21 (`PROBE_SHA`/`TOOL_SHA` passed as expected digests) | tameshi (`tools/mutate-and-run.sh` pin discipline) |
| (c) receipt with `OBSERVATIONS_BEGIN`/`OBSERVATIONS_END` markers | 0 | NEW-MECHANISM (absent in all 20 siblings) | none in siblings | none exists; tameshi if a standard is wanted |
| (d) replay of `polyglot-rust-c`, or one grader under two toolchains | 0 for polyglot-rust-c; 0 for rustc+g++ replay; 1 nearest (multi-toolchain runner) | NEW-MECHANISM | none in siblings; TB2 grader-replay probe is kengaku-owned (round 35) | tameshi (runner) for multi-toolchain legs; kengaku for TB2 grader replay |

Headline for the L1: the sha-pinned tool/counter (C1 L9) and the figure-at-rev extractor (C2) are
both already present elsewhere in the fleet, so neither is a fleet-first mechanism. The
`polyglot-rust-c` replay with rustc and `g++ -x c++` on one source, and the OBSERVATIONS delimiter
pair, are not present in any sibling.

## (a) claims-figure extractor that re-derives or re-runs historical instruments

Hits (classified DUPLICATE: the mechanism is already present in that lane; none of these has the
R89-C2 record-table or KNOWN-tuple layer, so they are partial).

A1. tameshi-shokunin `tools/selfstate-freshness.py:2-13, 27-37, 40-43` (commit `4e610748`, 2026-11-03).
Each row pins an instrument revision, extracts it with `git cat-file blob <rev>:<path>`, runs it with
`python3 -I -X utf8`, and matches the figure against the SCORECARD capability row. Its `expect: stale`
rows are declared divergences that are measured on every sweep, which is the same shape as the frozen
KNOWN set in R89-C2.
Class: DUPLICATE. The pinned-revision historical-instrument rerun plus declared expected-stale figure is
already in tameshi. It lacks a record-table pin and a `(claim, key, claimed, measured)` tuple check.
Plan text: `tameshi-shokunin/plans/round-75.plan.md:101-111` ("extracted from git objects at its rev
and run `python -I -X utf8`"; "setup refusal (exit 2), never a pass").

A2. tameshi-shokunin `tools/arm-liveness.py:16-19, 108-110` (commit `e8e0f0e9`, 2026-11-02). The
instrument is extracted with `git show <instrument_rev>:<path>` and re-executed, and the row passes only
when the tally moves against a baseline.
Class: DUPLICATE. It is the historical-instrument rerun half of the mechanism, not a figure extractor.

A3. tameshi-shokunin `tools/figure-attribution.py:27, 89-90, 93, 104` (commit `1a063d5f`, 2026-11-02).
A record figure must be a byte substring of both the record and its named receipt, read at pinned
revisions with `git show rev:path`, with `expect attributed|misattributed`.
Class: DUPLICATE. The pinned-revision figure binding is present. It does not re-run any counter.

A4. kasegi-shokunin `corpus/instruments/figure-audit.py:2-25, 46-50` and
`corpus/instruments/figure-audit-ledger.json:10-18, 74-79, 216-221` (instrument commit `c9df68e`,
2026-11-01). Each ledger figure has a `rev`, a `derive` of the form `git show <rev>:<path> | grep -cE ...`,
and a `want`, compared as a whole value with a stale verdict.
Class: DUPLICATE. Rev-pinned figure re-derivation with whole-value comparison and a stale class is
present. The derives I read are read-only greps, not counter reruns. The commit message's "9 re-runs
the frontier counter" was not found in the ledger entries I read (no `python` derive in the ledger).
This is a sibling commit-message discrepancy, recorded as an observation only.

A5. mori-shokunin `.ufo/waves/round-44/figures.tsv:1-2, 5-7` and `.ufo/waves/round-44/fixtures/figures-r43.tsv:7-18`
(commit `5157cdda`, 2026-10-25). Rows `F01 245 registry git show @REV@:corpus/SOURCES.md | grep -cE ...`
and similar: a claimed figure with a re-derivation at a measured revision.
Class: DUPLICATE. The fleet-first figure-at-rev ledger (earliest dated hit located here) is in mori.
It is a derive ledger with no stale-expectation verdict and no historical counter.

A6. kama-shokunin `.ufo/waves/round-27/residual/out/CriticBoundaryLegProbe/harness.py:15, 44, 49`
(commit `4d2e74f4`, 2026-10-23). The harness asserts the sha of a round-27 counter and of its scratch copy
before importing it, then runs it over round-26 shortcut receipts.
Class: DUPLICATE (partial). It re-runs a pinned counter over a historical artifact. It is not a
figure-claim extractor.

## (b) counter pins its probe or tool by sha256 constant

Hits. Each is a sha256 constant that the script enforces at run time unless noted. Subject-pin hits are
marked as such. All are classified DUPLICATE: the constant-pin, refuse-on-mismatch mechanism is present.

B1. kama-shokunin `.ufo/waves/round-21/build/out/RegressSkillGates/sweep.py:43-44, 92-93, 117-118`
(commit `1471344b`, 2026-10-21). `PROBE_SHA` and `TOOL_SHA` are constants passed to the probe as
`--expect-probe-sha256` and `--expect-tool-sha256`. This is the fleet-first probe pin in this scan.
Class: DUPLICATE. The closest form to R89-C1 L9: the probe's expected bytes are fixed by a constant.

B2. chousa-shokunin `.ufo/waves/round-31/controls/MutOracleC2/v2/detect.py:16, 38-39` (commit `86188116`,
2026-10-23). `EXPECTED_COUNTER_SHA256`; the run raises `counter no longer matches frozen v2 hash` on mismatch.
Class: DUPLICATE. This is the refuse-on-mismatch form of the same pin.

B3. chousa-shokunin `.ufo/waves/round-31/falsify/MutC1Grammar/probe.py:25, 75` (commit `23536590`,
2026-10-23). `COUNTER_SHA`; `assert sha(COUNTER) == COUNTER_SHA, 'frozen counter changed'`.
Class: DUPLICATE.

B4. chousa-shokunin `.ufo/waves/round-33/w1/CtlC1BraceDepth/run-control.py:16, 34` (commit `96be7925`,
2026-10-23). `FROZEN_COUNTER_SHA`; `assert sha(COUNTER) == FROZEN_COUNTER_SHA`.
Class: DUPLICATE.

B5. kake-shokunin `.ufo/waves/round-64/c64_quote_tool.py:55, 154` (commit `4c8295fa`, 2026-10-27).
`FROZEN_TOOL_SHA` for `scripts/quote_class.py`, compared before the tool runs.
Class: DUPLICATE. This pins the tool that is executed, which is the L9 shape.

B6. kotoba-shokunin `verifiers/check_erratum_absorption.py:15-16, 82-86` (commit `3e7aed9`, 2026-10-23).
`COUNTER_SHA256` checked and then asserted against the digest of the counter it checks.
Class: DUPLICATE.

B7. kama-shokunin `.ufo/waves/round-27/residual/out/CriticBoundaryLegProbe/harness.py:15, 44, 49`
(commit `4d2e74f4`, 2026-10-23). Counter and scratch-copy assertions (see A6).
Class: DUPLICATE.

B8. kaidoku-shokunin `.ufo/waves/round-82/w1/ReviewerC1/evidence/conjunction-gate-reviewed.py:26-29`
(commit `0f8ce2ea4`, 2026-11-04) and `.ufo/waves/round-85/w1/ExecSourceBind/candidate/tools/round-82/conjunction-gate.py:26-29`
(same constants). `COUNTER_SHA256` and `BINDER_SHA256` are defined. I did not read the call sites.
Class: DUPLICATE (the constants are the same mechanism; enforcement not verified).

B9. kaidoku-shokunin `.ufo/waves/round-50/w1/C2CounterBuild/tools/round-50/selftest-r49-c2.py:32`
(commit `8ccc05e6b`, 2026-10-28). `COUNTER_SHA` is defined. The grep found no other reference in that file,
so the constant appears unused there.
Class: DUPLICATE (pinned constant, enforcement absent in this file; noted, not counted as a clean pin).

B10. kake-shokunin `.ufo/waves/round-43/make_w1_spec.py:13, 26` (commit `eddbbf60`, 2026-10-23).
`COUNTER_SHA` written into the spec text, not enforced by the generator.
Class: DUPLICATE (pinned in text; not an enforcing counter).

B11. kama-shokunin `.ufo/waves/round-27/w1a3/out/ExecOfflineEchoReplay/harness.py:28-29`
(commit `d183ec57`, 2026-10-23). `COUNTER_SHA256` and `R26_SHA256`; enforcement not read.
Class: DUPLICATE (constant pins; enforcement not verified).

B12. tameshi-shokunin `tools/mutate-and-run.sh:122-126` and `:614-628` (tool commit `53e74a89`,
2026-10-14; the `PIN_*`/`REV_*` constants were not dated). Each leg is materialized with `git show <rev>:<path>`;
its sha256 must equal the recorded pin, otherwise setup refusal.
Class: DUPLICATE. This pins subject bytes, not the probe; the probe-pin form is B1 to B6.

B13. audio-shokunin `corpus/live/r88-simplifier/proofs/static-proofs.py:18-19, 40-41, 244-245`
(commit `bbcb0c5b`, 2026-10-16). `PIN_SHA` (measured blob) and `FOLD_SHA`, checked in `S1a` and `S11c`.
Class: DUPLICATE. It pins the subject, not the probe. It is the earliest dated sha-constant hit found,
but it is a subject pin.

Pattern note: the sha-constant grep returned 93 files. I read the first page and the targeted follow-ups.
The list is a sample, not an exhaustive enumeration.

## (c) receipt with OBSERVATIONS_BEGIN / OBSERVATIONS_END markers

Exact-marker grep (`OBSERVATIONS_BEGIN|OBSERVATIONS_END`, 20 sibling trees, gitignore off): **0 hits**.

Near-misses, not counted as the mechanism:
- Prose headings only: `kaidoku-shokunin/.ufo/waves/arc2-loop1-round2/CR4.md:200`,
  `arc2-loop1-round3/CR3.md:309`, `arc2-loop1-round4/C3.md:342`, `arc2-loop1-round4/S1.md:644`
  (`**OBSERVATIONS**` section headings, no begin/end pair).
- A Python variable inside an embedded probe source: `chousa-shokunin/.ufo/waves/round-31/controls/CtlDeterminism31/c1-probe-sources.json:20`
  (`OBSERVATIONS = ('supported',)`).

Class: NEW-MECHANISM. No sibling receipt delimits its observation block with begin and end markers. The
near-misses are prose or code identifiers and do not bind a receipt to a delimited block. Fleet-first: none
in siblings. Shared-standard holder: none exists; if a fleet standard is wanted, tameshi is the lane that
already owns receipt-family counters (`tools/arm-liveness.py`).

## (d) replay of polyglot-rust-c, or one grader under two toolchains

Grep `polyglot-rust|polyglot_rust|rust-c\b|polyglot-c\b` over 20 sibling trees: no sibling-owned hit.
The only hits are quotations of kengaku-owned commits and paths, which are not sibling mechanisms:
- `tabi-shokunin/.ufo/waves/round-36/w1/ConnDeltaScan/scan.md:269-273` (kengaku commit subjects, `polyglot-c-py` probe run).
- `kasegi-shokunin/.ufo/waves/round-44/wave2/R44W2Scout01.md:577-578` (kengaku `tb2-polyglot-c-py-grader.md` path).
- `kumitate-shokunin/.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json:386`
  (kengaku `plans/tb2_grader_probe.py`).
- `kaidoku-shokunin/.ufo/waves/round-69/w1/ConnectorCross/sweep/s4-receipt.txt:198` (kengaku SKILL row `tb2-grader-probe`).

Grep `g\+\+.{0,60}-x|-x c\+\+|rustc.{0,80}(popen|subprocess|run\()` over sibling `**/*.py`: **0 hits**.

Nearest mechanism (not the same): `tameshi-shokunin/tools/mutate-and-run.sh:9-18` replays legs in two
toolchains (bash: kagi `checklist-run.sh`, `drift-pins.sh`; node: kumitate `claims-check.mjs`, `round-gate.mjs`,
`sources-check.mjs`, `cite-check.mjs`). Each leg runs one grader in one toolchain, so no grader is replayed
under two toolchains against one source.

Class: NEW-MECHANISM for "one source, two toolchains, outputs compared". The fleet-first TB2 grader-replay
probe is kengaku-owned (round 35, `plans/tb2_grader_probe.py`, named in the kumitate and kaidoku hits above).
Shared-standard holder: tameshi for the multi-toolchain runner pattern; kengaku for the TB2 grader-replay probe.

## Method limits

- Greps were pattern-based over the 20 sibling trees. The (a) and (b) patterns returned more files than
  one page; I read the first page and targeted follow-ups. The (a) and (b) lists are samples.
- Enforcement was not read for B8 to B11. They are classified on their constants.
- Dates are first-add commit dates via `git log --diff-filter=A --reverse`. They do not date the clause inside each file.
- This scan did not inspect kengaku's own history beyond the sibling quotations above.

## Observations (not findings in scope)

- `kasegi-shokunin` commit `c9df68e` (2026-11-01) says "9 re-runs the frontier counter"; the ledger entries
  I read (`figure-audit-ledger.json:74-79, 216-221`) use `git show | grep -c` derives. The commit message and
  the bytes disagree. Sibling-owned; not edited.
- No frozen claims file, case table, record table or counter was inspected for correctness by this seat;
  the scan is limited to sibling overlap.

## Scratch

No scratch directory was created. Nothing was cloned. No sibling file was written.
