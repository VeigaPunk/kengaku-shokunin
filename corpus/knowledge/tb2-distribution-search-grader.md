# Terminal-Bench 2.0 `distribution-search` — the corpus's first tolerance-band grader

source: S209 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/task.toml — the task's machine-readable self-definition (dual-KL construction objective)
source: S210 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/tests/test_outputs.py — the executed scoring predicate (the decisive dual-tolerance leg)
source: S211 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/solution/solve.sh — the maintainer oracle (three-level count-scan Newton)
source: S212 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/instruction.md — the agent-facing instruction (LLM-confidence framing, tolerance declared)
verified-at: corpus/evidence/round58/kl-probe.txt sha256 3c93e06a88a6ec8e77b0ed1b81ad298a492513e3f5e7c9f20d6641da5ee53c1f (probe `plans/round58_c2_kl_probe.py --lane .`, cases=12 legs=48 mismatches=0 setup=0 predicted_u=0, PREDICATE R58-C3 pass, exit 0, at tip c39d0e40)
recheck: 180d — from the lane root re-run `python3 plans/round58_c2_kl_probe.py --lane . --work <scratch> --receipt corpus/evidence/round58/kl-probe.txt` and compare the receipt's CASE lines with the frozen table in `plans/round-58-claims.md` (any drift is a mismatch line)

## The class, worded narrowly

The decisive leg is a **numeric tolerance band on two aggregated functionals of the
answer**: the grader loads `/app/dist.npy` and asserts |KL(P||U) − 10.0| ≤ 1e-3 AND
|KL(U||P) − 10.0| ≤ 1e-3 over a 150,000-atom simplex (S210, `test_kl_divergences`). Nothing
about the answer's shape, provenance, or construction is graded — any distribution inside
the dual band passes. Named against the lane's fourteen executed exemplars, this is the
**dual-tolerance distributional gate** class — the corpus's first grader whose pass
condition is a numeric band rather than an exact comparison (membership/multiset/regex/
service/dual-runtime/exact-set/wall-clock ordering are all exact predicates). The words
"tolerance" and "divergence" appear in earlier entries only as incidental prose (checked
before the freeze; e.g. polyglot's "toolchain tolerance" is about gcc warnings).

The task sits in the lane's home domain: the instruction frames the construction as LLM
confidence metrics via KL divergence (S212), and the maintainer oracle (S211) solves it as
a three-level Newton system over integer atom counts (A heavy, B middle, C light atoms with
shared masses) — the answer is an explicit inverse construction, and the count-scanning
search implies the solution set is a neighbourhood, not a point.

## Probe findings (frozen predictions, all 48 confirmed on the first run)

The probe (`plans/round58_c2_kl_probe.py`, frozen with `plans/round-58-claims.md` at
d6bc6027 BEFORE the first capture run, sha256 `51c192f2…760`) executed the captured grader
against 12 lane-written candidates spanning the constraint system's boundary cases:

1. **Leg 4 is scale-blind.** `test_kl_divergences` renormalizes (`P = P / P.sum()`) before
   measuring: a ×1.001-scaled simplex (`sumdrift`) and a raw-integer-counts array
   (`intcounts`, max ≈ 4.5e11) both FAIL the raw-array validity leg and then PASS both KL
   legs. The normalization leg and the divergence leg measure different things, and the
   divergence leg is invariant to exactly the error the validity leg catches.
2. **The validity leg is load-bearing for leg 4's domain.** `P.min() > 0` guards
   `np.log`: a 0.0 atom (`minzero`) sends kf to nan (0·log 0) and kb to +inf; a negative
   atom (`negatom`) makes both nan. Without leg 3, leg 4 would fail anyway — but through
   float nan semantics, not through its band.
3. **The 1-D shape constraint is leg-2-only.** `P.size` and the `np.sum` reductions are
   shape-agnostic: the solution reshaped (2, 75000) (`twod`) fails only the ndim check and
   passes validity plus both KL legs.
4. **The band accepts a neighbourhood.** Raising the solution's middle level by a relative
   5.2e-4 (`tolbnd`) yields a DIFFERENT distribution with kf err ≈ 5.1e-4 and kb err ≈
   3.5e-5 — both inside the band. Combined with the oracle's count-scanning search, the
   gate underdetermines the answer: the grader certifies a property, not an artifact.
5. **Determinism contrast with the round-57 timing gate.** No wall-clock leg, no
   reference race: every case is decidable from float64 arithmetic on the constructed
   array, and the freeze carries ZERO U marks — 48 full-commitment predictions, all
   confirmed on the first run (the r57 eigen probe needed U marks for its two
   host-noise cases and observed three different U splits across runs).
6. **The oracle is honest and reachable.** The maintainer solver (S211) was extracted and
   re-run at authoring time; its accepted point (A=2, B=6325, C=143673; ph/pm/pl frozen in
   `corpus/evidence/round58/kl-oracle.md`) reproduces elementwise kf error 0.0 and kb error
   5.3e-15 on the grader's own reduction path.

## What it refuses (unchanged)

The task image (`alexgshaw/distribution-search:20251031`), the harness, real submissions,
runtime task validity, contamination, model behaviour, and the remaining 74 unread TB2 task
graders. Frontier: **15 of 89** TB2 task graders read (this is the fifteenth).
