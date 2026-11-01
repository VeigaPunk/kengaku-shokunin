# Round 57 — kengaku frozen claims (frozen before data, 2026-11-01)

author: kengaku L1 (round 57, Windows host). Base `c9ce9a713de770b2cb0c594fe3f9ad5019b64e0f`
(the round-56 verifier spot-check tip). Measurement environment: WSL2 Ubuntu-24.04 — python
3.12.3, bwrap 0.9.0, git 2.56, numpy 2.5.4 (system), biopython 1.85; `uv` absent; **no
environment mutation this round** (the r56 A3.4 canonical counter environment is preserved
as found; the new eigen probe stubs the `pytest` module in-sandbox rather than provisioning
it, see the probe docstring). Wave A (the R56-V1 fix) landed at `f754593b` BEFORE this
freeze; this freeze commit carries the C2 instrument and the C2 sources.

## Claim C1 — operability: the branch tip's whole advertised self-assessment surface re-runs green (the R56-V1 repair)

- Axis: operability (9). Distinct from C2's coverage. Causally separable: C1 verifies from
  the two counters alone; it does not read anything from C2.
- Before (measured this round at base `c9ce9a71`, WSL, clean clone, receipts
  `.ufo/waves/round-57/fix/`): `python3 plans/round52_c2_registry.py --lane <clone>` →
  `ADVERTISED total=83 / REGISTERED total=82 rows=84`, `MISSING plans/round56_landcheck.py`,
  `PREDICATE R52-C2 fail`, exit 1; `python3 plans/round55_c2_entryargv.py --lane <clone>
  --source <clone> --work <scratch> --jobs 6 --timeout 900` → `executed=83 timeout=0
  mismatched=0 evidence_missing=0 laundered=2` (`LAUNDERED round52-c2`,
  `LAUNDERED routed-findings`), `PREDICATE R55-C2 fail`, exit 1.
- Falsifiable after: at the round's final pushed tip both counters exit 0 —
  `MISSING 0` / `PREDICATE R52-C2 pass`, and `laundered=0` with `TIPSTATE` observed equal to
  declared / `PREDICATE R55-C2 pass` — with every instrument advertised anywhere in
  SCORECARD/SKILL/LOG/corpus registered in the same tip (no head-vs-measured-revision gap;
  that gap is exactly what the round-56 verifier's R56-V1 caught).
- Fix (wave A, `f754593b`): landcheck registry row + landcheck ledger row (the r54/r55
  counters enforce registry↔ledger bijection: `missing`/`extra` both must be empty), plus
  the R56-F2 findings row's `source` field corrected to the strict `<path>:<line>` shape
  (`corpus/lessons/round-56.md:60`) — the second laundering root cause the round-56 close
  landed unfixed (R56-F1's identical defect was fixed in-round; F2's was not).
- Declared verdict shape: operability 9→10 (the property "every advertised command is
  registered and green at the branch tip" is exactly what the two counters measure; at 9 the
  r56 close held it only at the measured revision, not at the tip).
- Do-nothing control: the committed before-receipts show the same commands red at base — a
  round that changed nothing cannot turn them green (the regression is in the tip's bytes;
  only landing the rows fixes it).

## Claim C2 — coverage (lowest non-retired owned axis, 7, L0-capped): the fourteenth TB2 task grader read and executed offline

- Axis: coverage (7 — held by the lane's own L0 design since round 25/33; the score cannot
  honestly move while that L0 question stands, so the claim's verdict shape is "predicate
  met, score held", the admitted r56-C3 shape). Distinct axis; does not depend on C1.
- Target: `largest-eigenval` (terminal-bench-2 @ pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`)
  — the corpus's first wall-clock-performance gate. 14 of 89 after this round.
- Sources opened this round (frozen pins, fetched 2026-11-01, sha256 over fetched bytes):
  - S205 `task.toml` `f7b9b7dda446f969a3ce88f61039d216f4d58b5fc5c10ff9faa24e2403bbd830`
    (`task.toml:6` description quote);
  - S206 `tests/test_outputs.py` `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce`
    (the timing assert at `:111`, the reference capture at `:15`);
  - S207 `solution/solve.sh` `8f414e50ce29f21ae26c423d74949b257073e95318ca5f5a95c2d9a90bfe93c2`
    (the maintainer oracle: `eigenpy.EigenSolver` at `:14`);
  - S208 `instruction.md` `6fa938389f99648508e5a9772e0d5e95d1102738c68d1ff61bd65469d76c52ab`
    (`:4` "consistently runs faster than the reference numpy solution"; `:5` median wording).
  Capture bytes committed at `corpus/evidence/round57/tb2-eigenval/` (no token-pattern
  content; the GH013 lesson does not apply — these five files are push-protection-clean).
- Instrument: `plans/round57_c2_eigen_probe.py` sha256
  `4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105` (frozen with this
  commit; bwrap envelope as the r55 chess probe; capture byte-copy bound read-only at
  `/tests`; capture sha refused on drift; pytest module stubbed no-op; `python3 -I` in
  sandbox).
- **Frozen predictions — written from static readings BEFORE the first capture run.** The
  plumbing was proven with a toy grader + toy candidates only (bwrap, numpy import,
  ProcessPoolExecutor fork, P/F verdict split — toy receipt in this round's wave receipts);
  the capture was never executed before this commit.
  Static readings per capture function: `test_eigen_pair` asserts a returned pair satisfies
  `np.allclose(A @ v, value * v)` (true for `np.linalg.eig` pairs on dense non-defective
  matrices; defectiveness has probability 0 under normal(0,1) entries) and refuses zero
  vectors first; `test_dominance_eigenvalue` asserts `np.isclose(|candidate value|,
  |largest |eigenvalue|| by `np.linalg.eigvals`)`; `test_speedup` builds 100 seeded
  `normal(0,1)` matrices per size, times reference (`np.linalg.eig` itself, ~microseconds at
  sizes ≤10) and candidate in an isolated single-worker process, and asserts
  `candidate_median < reference_median` (`:111`).

  | case | candidate | leg | sizes | prediction | static reading |
  |---|---|---|---|---|---|
  | eig-sleep-pair | eig + 200k no-op loop | pair | 2,5,10 | P | identical LAPACK pairs satisfy the residual assert |
  | eig-sleep-dom | | dom | 2,5,10 | P | identical values array → identical argmax → `isclose` on equal floats |
  | eig-sleep-speed | | speed | 2,10 | F | a fixed ≥10 ms-per-call loop against a ~µs reference median |
  | eig-bare-pair | np.linalg.eig, bare | pair | 2,5,10 | P | same as above |
  | eig-bare-dom | | dom | 2,5,10 | P | same as above |
  | eig-bare-speed | | speed | 2,10 | **U** | the candidate IS the reference algorithm; `dt < ref_dt` between two medians of identical code is host noise — not derivable from the grader's static semantics; executed and reported observed-only, never a mismatch |
  | zero-e1-pair | returns (0.0, e1) | pair | 2,5,10 | F | `A @ e1` is the matrix's first column — nonzero w.p. 1 for dense `normal(0,1)` |
  | zero-e1-dom | | dom | 2,5,10 | F | `|0|` against the largest `|eigenvalue|` of a dense normal matrix — `isclose` false w.p. 1 |
  | zero-e1-speed | | speed | 2,10 | P | builds one vector and returns — strictly less work per call than a LAPACK eigensolve on the same matrix |

  24 cases total: 22 P/F + 2 U. Predicate: every P/F prediction equals its observed verdict
  and no case observes SETUP (`PREDICATE R57-C2 pass`, exit 0); any mismatch → exit 1; any
  SETUP → exit 2.
- After (falsifiable): probe receipt at the freeze tip — `cases=24 observed_pass=<p>
  observed_fail=<f> mismatches=0 setup=0`, `PREDICATE R57-C2 pass`, exit 0; the three
  grader-class findings recorded from the observed table (exact-but-slow fails; timing-equal
  is host-noise; maximally-wrong wins the speed leg); PROVINCE names the fourteenth grader
  (14 of 89); SOURCES rows S205–S208 census-clean; knowledge entry + corpus index row.
- Do-nothing control: `grep -c 'fourteenth' PROVINCE.md` → 0 at base; S205–S208 absent at
  base (`grep -c S205 corpus/SOURCES.md` → 0); the probe instrument does not exist at base.
- Sizing (§9): needs live pinned fetches, a sha-refusing offline executor, and bwrap; a
  do-nothing control cannot produce any of these.

## Falsifier for the whole freeze

If the capture bytes re-fetched at the pin differ from the committed sha256 pins, or the
probe's first committed receipt shows any P/F mismatch or SETUP, or the two counters at the
final tip print anything but pass, the corresponding claim is falsified and the round
reports it honestly.

## Environment scoping (A3.4 discipline, carried)

Canonical counter environment: WSL Ubuntu-24.04, master checkout measurement clones, uv
absent, pytest absent (the probe stubs pytest in-sandbox; no provision happened this round).
The controls instrument's uv-present receipts remain scoped side-runs per A3.4.
