# ClaimFalsifier — r66 w1 seat report (2026-11-03)

Falsification attacks on R66-C1 (frozen tensor probe receipt checker) and R66-C2
(round-65 gate strict proposal), all fixtures under
`/fast/scratch/hyaku/kengaku-r66/ClaimFalsifier/` (removed on exit). Full log with
commands, exit codes and per-attack detail:
`.ufo/waves/round-66/w1/ClaimFalsifier/attacks.md`; machine receipts in
`.ufo/waves/round-66/w1/ClaimFalsifier/attempts/` (13 check transcripts + the A4 cheat
junit, runner and case file). No tools installed. Nothing in the lane was written except
this seat's two files. No edits to any frozen artifact, the fabricated fixture, or the
proposed gate; the strict proposal was invoked read-only in place and from a scratch copy.

## Verdicts

- **A1 — KILLED-BY-COUNTER.** One flipped byte in a copied `junit/k1-ref.xml` →
  `CHECK defect: k1-ref junit_sha does not match committed junit bytes`, exit 1
  (`attempts/a1-junit-byte-flip.txt`). Caveat named: the junit clause hashes bytes at
  `receipt.parent/junit/` against the sha written **in the receipt**, never against the
  committed junit dir; bytes+sha rewritten together are accepted, exit 0
  (`attempts/a1-coordinated-rewrite.txt`).
- **A2 — KILLED-BY-COUNTER.** K2's VECTOR line forged to K1's all-P vector, junit
  untouched → `CHECK defect: k2-none vector differs from the frozen table`, exit 1
  (`attempts/a2-k2-vector-forgery.txt`). The refusing clause is the frozen-table
  comparison; the junit clause stays silent.
- **A3 — KILLED-BY-COUNTER.** Header comment of the fabricated fixture rewritten (body
  byte-identical); strict still exits 1 with the same 8 value-based defects
  (`toolchain-not-well-formed` ×4, `toolchain-banner-count` ×3, `probe-binding-missing`)
  — in place, on the header-rewritten copy, and via a scratch copy of the proposal (its
  `lane_root()` fallback correctly binds the committed probe sha `f44b7283…db4eb`).
  Side conditions green: strict on the committed R65 receipt exit 0; default modes on
  committed and fabricated receipts both still `PREDICATE R65-C1 pass`, exit 0.
- **A4 — LIMIT.** A K1 variant whose `ColumnParallelLinear` keeps the whole master weight
  as a buffer and reconstructs the full output locally (zero collectives, doubled memory)
  passes 13/13 with a vector **identical to K1's committed junit vector**
  (`attempts/a4-cheat-junit.xml`). The grader sees API-level facts only: file existence,
  `weight`/`bias` parameter values (a naive master-weight forward would die on the grad
  assertion with `weight.grad is None`), forward outputs and grad slices vs an
  `nn.Linear` reference. It cannot see collectives, memory, or latency: sharding
  semantics are verified at the API surface, not sharded execution. Documented limit of
  the grader, not a probe defect.
- **A5 — KILLED-BY-COUNTER (K2/K3 can never appear passing), with one named LIMIT.**
  Refused: K2-only receipt (4× `has no VECTOR line`, kill-rule (d) holds); K3 forged
  all-P; K2 forged all-P (= A2) — all exit 1 by the table/completeness clauses. Accepted
  but honest: a hand-built receipt from the frozen table + committed shas with **no run**
  passes (`attempts/a5-r2-handbuilt-table-receipt.txt`, exit 0) while showing K2 all-F /
  K3 exists-only — the predicate only passes with K2/K3 failing; and a K2 junit swapped
  for K1's 13-pass bytes (receipt sha updated) passes with the VECTOR still claiming
  all-F (`attempts/a5-r3-k2-junit-swap.txt`, exit 0) — junit content is never parsed
  against VECTOR claims. LIMIT: `--check-receipt` proves text-vs-table and
  sha-vs-bytes-at-named-paths, not that a run happened (same self-attestation class as
  C2's named limitation; C1's junit binding is stronger but is not proof-of-execution).

## Net

Neither claim is falsified. R66-C1's checker refused every tampering and vector-forgery
construction put to it; R66-C2's strict gate refuses the header-laundered fixture and its
default-mode pins are unchanged. Two calibration limits should stand in the round record:
(a) grader blindness to sharded execution (A4), (b) receipt self-attestation — no
proof-of-execution, junit bound by sha only (A1 caveat, A5-4/5).
