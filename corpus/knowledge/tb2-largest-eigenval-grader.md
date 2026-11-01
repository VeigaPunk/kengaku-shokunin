source: S205 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/task.toml — the declared performance objective at `task.toml:6`, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, sha256 `f7b9b7dda446f969a3ce88f61039d216f4d58b5fc5c10ff9faa24e2403bbd830`, accessed 2026-11-01
source: S206 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/tests/test_outputs.py — the timing assert at `tests/test_outputs.py:111` (`assert dt < ref_dt`), the reference pre-capture at `:15` (`_np_linalg_eig = np.linalg.eig`), same commit, sha256 `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce`, accessed 2026-11-01
source: S207 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/solution/solve.sh — the maintainer oracle at `solution/solve.sh:14` (`solver = eigenpy.EigenSolver(matrix)`), same commit, sha256 `8f414e50ce29f21ae26c423d74949b257073e95318ca5f5a95c2d9a90bfe93c2`, accessed 2026-11-01
source: S208 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/instruction.md — the agent-facing speed requirement at `instruction.md:4` and the median protocol at `:5`, same commit, sha256 `6fa938389f99648508e5a9772e0d5e95d1102738c68d1ff61bd65469d76c52ab`, accessed 2026-11-01
verified-at: 2026-11-01 — probe receipt `corpus/evidence/round57/eigen-probe.txt` (sha256 `463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784` at writing) and the in-repo captures named above; oracle reading in `corpus/evidence/round57/eigen-oracle.md`
recheck: 180d — from the lane root re-run the offline probe (`python3 plans/round57_c2_eigen_probe.py --lane .`) and require `mismatches=0 setup=0` and `PREDICATE R57-C2 pass` (the two U cases are observed-only and may flip — their flip is the recorded finding, not drift); re-fetch the four pinned URLs at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and compare sha256 against the pins above; any prediction mismatch on a P/F case, any SETUP, or any pin drift supersedes this entry
writer: kengaku L1, round 57 — second-seat re-read: pending

# Terminal-Bench 2.0 task grader, read and executed: `largest-eigenval`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `largest-eigenval` task's score is three pytest
legs over one candidate function (`from eigen import find_dominant_eigenvalue_and_eigenvector`,
`test_outputs.py:21`): an eigen-pair residual assert, a dominance assert against
`np.linalg.eigvals`, and a **wall-clock speedup assert** — the candidate's median call time
over 100 seeded matrices, timed in an isolated process, must be strictly below the in-grader
reference, which is `np.linalg.eig` itself (`:111`). This is the corpus's first
**performance-gate grader**: the pass/fail boundary is host-relative elapsed time, not a byte
property of the answer. Offline execution of the captured grader against a frozen table of 24
lane-written candidates (3 synthetic implementations × 3 legs × sampled sizes) matched every
static prediction written before the first run: `cases=24 observed_pass=15 observed_fail=9
mismatches=0 setup=0` (`corpus/evidence/round57/eigen-probe.txt`). The fourteenth TB2 task
grader this lane has executed; the frontier count moves 13 → 14 of 89.

## Source labels

S206 is the benchmark maintainers' own grader file: primary for *what the grader checks* and
a self-report for everything else. S208 is the maintainers' own agent-facing requirement text
the grader is mapped against. S205 is the task's machine-readable self-definition (its
`description` names the performance objective). S207 is the maintainers' reference solution —
the oracle for what answers the task rewards, read from maintainer code, not inferred. The
probe receipt is the lane's own re-runnable gate output (tier A for its own scope: these 24
lane-written candidates against this capture under the host Python 3.12/numpy 2.5.4, inside a
bubblewrap sandbox with the capture bound read-only at `/tests` and the `pytest` module
stubbed to a no-op decorator — the probe calls the three test functions directly, so no
pytest-plugin behaviour is exercised; the capture bytes are unmodified and sha-pinned).

## What the grader checks (static reading, `test_outputs.py`)

| Step | Mechanism | Lines |
|---|---|---|
| Candidate import | `os.chdir("/app")` then `from eigen import find_dominant_eigenvalue_and_eigenvector` | :19-21 |
| Anti-monkeypatch | references to `np.random.seed`, `np.linalg.eig`, `np.linalg.eigvals`, `np.random.normal` are captured at import, BEFORE the candidate is imported | :12-16 |
| Correctness leg 1 (pair) | per size 2..10: seed(0), `A = normal(size)`, assert vector nonzero/non-NaN/non-Inf, then `np.allclose(A @ v, value * v)` | :44-59 |
| Correctness leg 2 (dominance) | per size: `np.isclose(np.abs(cand), np.abs(max |eigvals(A)|))` | :62-75 |
| Timing leg (speed) | per size: 100 seeded matrices; reference (`np.linalg.eig` + argmax) and candidate timed per call in a single-worker `ProcessPoolExecutor`; `assert dt < ref_dt` on the medians | :78-111 |
| Runner | `test.sh` runs pytest with the CTRF plugin and maps the pytest exit to a single-bit reward (byte-identical runner to S109's regex-log `test.sh`, sha256 `fc40868b…`) | test.sh |

## Evidence table (24 frozen cases, receipt-verbatim)

Each row is one frozen case of the round-57 probe (case table and predictions frozen with
`plans/round-57-claims.md`, commit `c0e7e100166a0e1ad84fa0283d2972351e41bcc7`, BEFORE the
first capture run; plumbing was proven on a toy grader only). Candidates: `eig-sleep`
(identical LAPACK values plus a fixed 200k-iteration no-op loop, ≥10 ms per call);
`eig-bare` (bare `np.linalg.eig` — algorithmically identical to the grader's reference);
`zero-e1` (returns eigenvalue 0.0 and the unit first column — no eigensolve at all).

| # | Case | Leg | Size | Predicted | Observed (receipt) |
|---|---|---|---|---|---|
| 1-3 | eig-sleep-pair-s{2,5,10} | pair | 2,5,10 | P | P, P, P |
| 4-6 | eig-bare-pair-s{2,5,10} | pair | 2,5,10 | P | P, P, P |
| 7-9 | zero-e1-pair-s{2,5,10} | pair | 2,5,10 | F | F, F, F |
| 10-12 | eig-sleep-dom-s{2,5,10} | dom | 2,5,10 | P | P, P, P |
| 13-15 | eig-bare-dom-s{2,5,10} | dom | 2,5,10 | P | P, P, P |
| 16-18 | zero-e1-dom-s{2,5,10} | dom | 2,5,10 | F | F, F, F |
| 19 | eig-sleep-speed-s2 | speed | 2 | F | F |
| 20 | eig-bare-speed-s2 | speed | 2 | U | F (observed-only) |
| 21 | zero-e1-speed-s2 | speed | 2 | P | P |
| 22 | eig-sleep-speed-s10 | speed | 10 | F | F |
| 23 | eig-bare-speed-s10 | speed | 10 | U | P (observed-only) |
| 24 | zero-e1-speed-s10 | speed | 10 | P | P |

Receipt predicate block, verbatim:

```
cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
PREDICATE R57-C2 pass
```

A second bare post-freeze run (consistency check, `.ufo/waves/round-57/claims/c2-bare-run.txt`)
reproduced `mismatches=0 setup=0` with the U cases now `s2=F s10=F` — the timing leg on a
correctness-identical answer flipped between runs. Recorded, not laundered.

## Mechanism (four properties)

1. **The pass boundary is elapsed time, not answer content.** `eig-sleep` returns
   bit-identical (value, vector) pairs to the grader's own reference — it passes both
   correctness legs at every sampled size — and still fails the task, because its fixed
   per-call loop loses the median race (`:111`). A mathematically exact answer is a graded
   fail. Conversely `zero-e1`, which computes no eigensolve at all, wins the speed leg at
   both sampled sizes: the timing leg alone cannot distinguish "fast because right" from
   "fast because empty" — only the correctness legs do that.
2. **Timing-equal is host noise.** `eig-bare` IS the reference algorithm; its two U cases
   (predictions marked not-derivable-from-static-reading at freeze time) split `F`/`P` within
   one run and flipped to `F`/`F` on re-run. The grader's verdict on a correctness-identical
   answer is therefore not a function of the answer: the same submission can pass or fail by
   scheduler noise. This is the round's calibration finding for benchmark gates: a
   `dt < ref_dt` predicate on a same-cost reference measures the host, then grades the agent.
3. **The gate hardens its own reference.** The numpy functions the timing comparison depends
   on are captured at import time, before the candidate module is imported (`:12-16`), so a
   candidate cannot monkeypatch `np.linalg.eig` to shrink the reference's cost — the
   first anti-monkeypatch capture this corpus has recorded in a grader. The reference also
   runs in a separate isolated process from the candidate (`ProcessPoolExecutor`,
   max_workers=1, `:92-105`).
4. **The declared contract matches the gate.** The instruction states the speed requirement
   and the median protocol in the agent-facing text (`instruction.md:4-5`), and the task
   definition names the performance objective (`task.toml:6`); the maintainer oracle shows
   the intended fast-correct answer is the same eigensolve behind a C++ binding
   (`solve.sh:14`, `eigenpy.EigenSolver`) — lower constant factors, not a different
   algorithm. Declared performance gate, oracle-consistent: this is a *legible* timing gate —
   the failures it produces are the class "correct but slower than LAPACK", and its own
   instruction says so.

## Negative space

This entry does **not** establish:

- **numerical-algorithm guidance** — nothing here says how an agent should make an eigensolve
  faster; the oracle's `eigenpy` choice is the maintainers' self-report of one accepted
  approach, not a validated recipe;
- **task validity** — the timing legs were sampled at sizes {2, 10}, not the full 2..10 grid
  the pytest run uses, and no container, no `test.sh` execution, no agent run, no trajectory;
- **cross-host transfer** — every timing verdict above is this host's (WSL2 Ubuntu-24.04,
  numpy 2.5.4, bwrap-isolated); the recorded P/F of timing cases does not transfer, and the
  U cases' flip between runs is the demonstration;
- **the other 75 unread TB2 task graders** — one task of 89; the frontier count moves
  13 → 14 of 89, nothing more;
- **model or agent performance** — all 24 cases are lane-authored synthetic candidates.

**Falsifier.** This entry is falsified if (a) a re-fetch of the four pinned URLs yields bytes
whose SHA-256 differs from the pins in the `source:` lines; (b) a fresh probe run prints any
P/F mismatch (`mismatches>0`) or any SETUP on the committed capture — in particular if any
eig-sleep/eig-bare pair or dom case observes F, or any zero-e1 pair or dom case observes P;
(c) the captured grader is shown to compare on anything other than the three legs at
`:44-111`, or its reference to be anything other than `np.linalg.eig`; or (d) the maintainer
solution is shown to change the algorithm rather than the constant factors.

## Connections

- `[[tb2-chess-best-move-grader]]` (rounds 55-56) — the thirteenth grader: a full-multiset
  byte-equality gate, the sharpest possible contrast in graded property: chess grades what
  the answer IS (a multiset), largest-eigenval grades how long the answer TOOK (median
  elapsed). The two bound the corpus's grader-property axis: content predicates vs
  cost predicates.
- `[[tb2-password-recovery-grader]]` (round 45) and `[[benchmark-grader-semantics]]` — the
  executed-grader corpus table this entry extends: constant-compare (membership), full-multiset
  equality, dual-runtime, service-state, regex-execution, and now wall-clock performance.
- `[[benchmark-saturation-and-lifecycle]]` — a cost-predicate gate is a saturation hazard the
  saturation literature's discriminative-power lens does not name: hardware drift can
  silently re-grade every historical submission without any benchmark content changing.

## Admission state

`second-seat re-read: pending` — admission is the L1's call; no second-seat report is cited
by this entry. Q1-Q7 checked at write time: triad opens the entry (S205-S206-S207-S208,
verified-at, recheck with dates and actions); every load-bearing claim maps to a tier-A row
or the receipt; quotes ≤25 words with locations; negative space above; oracle labelled
maintainer self-report where it is one; extends `tb2-chess-best-move-grader.md`'s corpus
table (supersedes nothing); entry, `corpus/README.md` index row and the PROVINCE
coverage-map row land in the same commit.
