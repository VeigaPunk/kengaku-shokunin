# Round 57 — largest-eigenval identity receipts and the maintainer oracle (S205–S208)

author: kengaku L1, round 57 (Windows host), 2026-11-01.

## Identity (sha256 over fetched bytes, curl GET of the pinned raw URLs)

| file | sha256 | bytes |
|---|---|---|
| `largest-eigenval/task.toml` (S205) | `f7b9b7dda446f969a3ce88f61039d216f4d58b5fc5c10ff9faa24e2403bbd830` | 1032 |
| `largest-eigenval/instruction.md` (S208) | `6fa938389f99648508e5a9772e0d5e95d1102738c68d1ff61bd65469d76c52ab` | 716 |
| `largest-eigenval/tests/test_outputs.py` (S206) | `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce` | 3951 |
| `largest-eigenval/tests/test.sh` | `fc40868bee6cbcfd6e906b0522dda9a778064ea9876e64a40a377d66087a174b` | 469 |
| `largest-eigenval/solution/solve.sh` (S207) | `8f414e50ce29f21ae26c423d74949b257073e95318ca5f5a95c2d9a90bfe93c2` | 650 |

All fetched 2026-11-01 at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; the capture bytes
are committed at `corpus/evidence/round57/tb2-eigenval/` (push-protection-clean content —
the r52 GH013 lesson does not apply to these five files; no token-pattern bytes).

## Located quotes (at most 25 words each; cited in the SOURCES rows)

- `task.toml:6` — "optimize eigenvalue computation by implementing a faster alternative to
  numpy's default algorithm while maintaining mathematical correctness" (16 words)
- `tests/test_outputs.py:111` — `assert dt < ref_dt` (4 words); `:15`
  `_np_linalg_eig = np.linalg.eig` (4 tokens, the pre-capture against monkeypatching)
- `solution/solve.sh:14` — `solver = eigenpy.EigenSolver(matrix)` (4 words)
- `instruction.md:4` — "Optimize the function such that it consistently runs faster than the
  reference numpy solution in /app/eval.py" (17 words); `:5` "We will run multiple tests and
  take the median time per call" (12 words)

## The oracle reading (S207 + S208)

The maintainer's reference solution replaces the stub with a C++-binding full eigensolver:
`import eigenpy` (`solve.sh:9`), `solver = eigenpy.EigenSolver(matrix)` (`:14`),
`eigenvalues = solver.eigenvalues()` (`:15`), argmax over `np.abs` (`:18`), returning
`eigenvalues[idx], eigenvectors[:, idx]` (`:19`) — the same algorithm class as the grader's
in-file reference (`np.linalg.eig`, `test_outputs.py:15` + `ref_solution` at `:31-35`), with
lower constant factors. The instruction states the speed requirement and the protocol in the
agent-facing text (`instruction.md:4-5`). Together: the task rewards engineering the SAME
eigensolve to run faster than numpy's own call — the correctness legs stay, speed decides.
A mathematically exact answer that is slower than LAPACK fails (`test_outputs.py:111`); a
faster-but-wrong answer fails the correctness legs but wins the speed leg.

## Probe receipts (round 57)

- First capture run (the only receipt of record):
  `corpus/evidence/round57/eigen-probe.txt`, sha256
  `463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784` —
  `cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0`,
  `OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P`, `PREDICATE R57-C2 pass`, exit 0.
- Plumbing selftest (toy grader, capture untouched): `.ufo/waves/round-57/claims/c2-selftest.txt`
  — `SELFTEST cases=2 failures=0`, exit 0.
- Second bare run (consistency check, post-freeze): `.ufo/waves/round-57/claims/c2-bare-run.txt`
  — `cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0`,
  `OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F`, `PREDICATE R57-C2 pass`, exit 0,
  6.23 s. The U cases flipped between runs (s10: P→F) — the timing leg on a
  correctness-identical answer is a coin flip across runs; recorded, not laundered.
- Capture sha-refusal kill (one byte appended to the capture in a judge-owned clone):
  `.ufo/waves/round-57/claims/c2-sha-kill.txt` —
  `SETUP grader sha256 418ba750…cc122 != frozen pin cdc58e3a…168ce`, exit 2.

## Negative space

No task image, no container, no agent run, no model behaviour, no task validity, no
contamination measurement; the probe executes the captured scoring code on lane-written
synthetic candidates only. The timing-leg verdicts are host-relative: the recorded P/F of
the timing cases on this host do not transfer to other hosts (that non-transferability is
the finding, not a defect of the record).
