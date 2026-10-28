# R50C1ScribeLimit — R50-C1 instrument: named limits (scribe)

REV 3b02d573d58cc6d2e0d27ef92ac0815354912252 (freeze; measured on a `git clone --shared`)
Lane tip checked 5c56819f7964f4af19c960de08a49cd8f95781ce; `git merge-base --is-ancestor 3b02d573… HEAD` exit 0 (FREEZE_IS_ANCESTOR).

Axes named: **novelty** (R50-C1), single item — the exact named limits of `plans/round50_c1_verify.py`.
No admission is claimed; nothing in SCORECARD/LOG/corpus was touched.

## Commands run (read-only; clone in scratch, now removed)
```
git rev-parse HEAD                                             -> 5c56819f7964f4af19c960de08a49cd8f95781ce
git merge-base --is-ancestor 3b02d573… HEAD                     -> exit 0
git clone --shared <lane> lane-clone && git -C lane-clone checkout 3b02d573…  -> 3b02d573d58cc6d2e0d27ef92ac0815354912252
sha256sum lane-clone/plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
  -> 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  fixture_fence.py
      f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  round50_c1_verify.py
      b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  population.txt
python3 -c 'len(spec["mutants"])'                              -> n=23  candidate_fence_sha256=b687b1d9…
glob counts (lane-clone): refusals46/*.py=20, sealed46/*.py=12, sealed50 is_dir=False
git --version                                                  -> 2.56.0
```

## Deliverable — named limits of the R50-C1 instrument (≤40 lines)

1. **Outside-`d` reads while deciding — NOT measured.** Reason: `plans/round50_c1_verify.py` `verdicts()` imports the fence and calls `breach()` in-process; no tracer. Counter instead: `plans/round46_c1_verify.py` legs B1–B6 (`strace -f -y` started outside the sandbox) — supplementary, not part of the predicate.
2. **io_uring SQE opens/reads — NOT measured.** Reason: io_uring emits no traced syscall; `plans/round46_c1_verify.py` names this B7 and does not block `io_uring_*`. No committed counter measures it; would need an io_uring-aware probe (seccomp/BPF).
3. **Host paths outside the scratch root (`/etc`, `/proc`, `/sys`) — NOT counted.** Reason: round-46 counts only paths under the scratch root; round-50 observes no paths at all and does not validate `--work` (default `tempfile.mkdtemp(dir=None)`, i.e. `$TMPDIR`).
4. **States a third-party tool writes — NOT measured.** Reason: fixtures are built by host git only (`plans/honest50/build_honest_population.py` `gitdir_inside`/`git_state`); `plans/round-50-claims.md` defines the population as "states git itself writes". No counter exists for libgit2/jj/IDE-written stores.
5. **Host git version drift — NOT measured as agreement.** Reason: identity pins (`plans/honest50/population.txt` `tree_sha256` rows) surface drift only as `POPULATION-MISMATCH`/`BUILD-ERROR`, never as a fence measurement across versions; the run is anchored at git 2.56.0. Host-sensitive surfaces named in `plans/round-50-claims.md`: `hooks/*.sample`, `info/exclude`, `git worktree --relative-paths` ≥ 2.48.
6. **Admission decisions only.** Post-admission behaviour and the fence CLI (`plans/fixture_fence.py` `main`, exit status, stdout protocol) are unexercised; only `breach(d, argv, tool)` truthiness is scored.
7. **Frozen denominators.** A hostile shape absent from `plans/refusals46/` (20) or `plans/sealed46/` (12) is unmeasured. The `SEALED ≥ 18` literal is enforced only when `plans/sealed50/` exists (`if (lane / "plans/sealed50").is_dir()`); the directory is absent at the measured revision, so the leg currently scores 12.
8. **Mutant floor, not correctness.** 12 of 23 rows is a floor: up to 11 survivors still print `verdict=met`. Rows target a different candidate fence (`candidate_fence_sha256=b687b1d9…`); Q38 witness of kill direction is an S2 obligation (`plans/round-50-claims.md`), not a counter output.
9. **Refusal reasons not asserted.** Only non-None `breach()` is scored; `why` is truncated to 200 chars for display. A fence refusing for the wrong reason passes.
10. **Index identity masked.** `plans/honest50/population.txt` line 4 masks `.git/index` and `.git/worktrees/*/index` (volatile stat cache), so index-only differences are unmeasured.
11. **Testing overrides bind the receipt to their inputs.** `--fence`, `--allow-dirty`, `--skip-mutants` (`plans/round50_c1_verify.py` argparse) print the predicate of the inputs named, never a receipt for the frozen run.
12. **Clean-tree binding.** Default mode fails on any `git status --porcelain` line, so the predicate measures a clone of the tip, not the live checkout.

## Limits of this report
Read-only clone of the freeze; no counter executed (item drafts limits, does not score). Line-number citations omitted by design; paths only, per item. Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ScribeLimit` removed before yield.

VERDICT: deliverable drafted — 12 named limits, each with reason and the file/counter that would measure it instead; no new factual claims; no admission asserted.
