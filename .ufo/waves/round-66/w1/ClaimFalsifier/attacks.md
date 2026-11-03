# ClaimFalsifier — round-66 wave w1, attacks on R66-C1 and R66-C2 (2026-11-03)

Seat: ClaimFalsifier-4. All fixtures were built and run under
`/fast/scratch/hyaku/kengaku-r66/ClaimFalsifier/` (removed on exit; receipts copied to
`attempts/` beside this file). The frozen probe, the frozen cases, the frozen table, the
fabricated fixture and the proposed strict gate were never edited. Baseline before any
mutation: `--check-receipt` on an unmodified scratch copy of
`corpus/evidence/round66/tensor/receipt.txt` printed `CHECK ok cases=5` /
`PREDICATE R66-C1 pass`, exit 0 — the copy was faithful before attacking.

Checks used the frozen probe `plans/round66_c1_tensor_probe.py` (sha
`c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`, the receipt's `PROBE`
line) and the proposed gate
`.ufo/waves/round-66/w1/ReceiptGateBuild/proposed/round65_c1_sqlite_probe.py` (sha
`cd70ed6120da66fc28f15dd14b0fd559af91825cdcb2f9ccaf3027896345f7bc`), both invoked
read-only in place. No tools were installed (tooling-only rule: nothing needed).

## A1 — junit bytes changed after the receipt was written: KILLED-BY-COUNTER (with a named caveat)

Construction: copied `receipt.txt` + `junit/` into scratch; flipped byte 0 of
`junit/k1-ref.xml` (`<` → `>`); ran `--check-receipt` against the copied receipt.

- `attempts/a1-junit-byte-flip.txt`: `CHECK defect: k1-ref junit_sha does not match
  committed junit bytes`, `PREDICATE R66-C1 fail`, **exit 1**. Refused.

Caveat (LIMIT, named because the attack probes exactly this clause): the junit clause
compares the bytes at `receipt.parent/junit/<case>.xml` against the `junit_sha` **written
in the receipt itself** — never against the committed `corpus/evidence/round66/tensor/junit/`
directory (that constant is used only by `--selftest`). A coordinated rewrite — same byte
flip **plus** updating the receipt's `k1-ref ... junit_sha=` to the new sha — is accepted:
`attempts/a1-coordinated-rewrite.txt`: `CHECK ok cases=5`, **exit 0**. Post-hoc tampering
of junit bytes alone is caught; tampering together with the receipt is not, because the
checker never parses junit content (see A5-R3). The receipt is self-attesting for junit
bytes exactly as R66-C2's named limitation says receipts are self-attesting for values.

## A2 — K2's VECTOR replaced by a copy of K1's vector, junit bytes untouched: KILLED-BY-COUNTER

Construction: in the scratch copy, rewrote the `VECTOR k2-none …` line's 13 outcome tokens
to K1's all-P values, kept `frozen=match` and every CASE/junit byte unchanged.

- `attempts/a2-k2-vector-forgery.txt`: `CHECK defect: k2-none vector differs from the
  frozen table`, `PREDICATE R66-C1 fail`, **exit 1**. Refused.
- What actually refuses it: the **frozen-table clause** (`plans/round66_c1_tensor_probe.py`
  `check_receipt()` compares each VECTOR line's tokens against `FROZEN_TABLE[case]`). The
  junit clause is silent — the junit bytes were untouched, so their sha still matches. The
  `frozen=match` suffix is also checked textually, but the refusal here is the table
  comparison, not the suffix and not the junit sha.

## A3 — strict gate after rewriting only the fabricated receipt's header: refused, exit 1

Construction: copied the fabricated fixture to scratch; rewrote only its two header
comment lines (the `# FABRICATED RECEPT …` marker) to innocuous text; body proven
byte-identical below the header. Ran `--strict` three ways.

- In place, unmodified fixture: `attempts/a3-strict-fabricated-unmodified.txt` — **exit 1**,
  `PREDICATE R65-C1 strict-fail`, defects: `toolchain-not-well-formed` ×4 (gcc/gcov/bwrap/
  python all say `fabricated`), `toolchain-banner-count` ×3 (no `CC `/`GCOV `/`BWRAP `
  banner lines), `probe-binding-missing` (no `PROBE sha256=` / `# instrument … version=`).
- Header rewritten: `attempts/a3-strict-fabricated-header-rewritten.txt` — **exit 1**,
  byte-for-byte the same eight defects. The strict gate has **no header-based finding**;
  refusal is purely value-based, so rewriting the marker defeats nothing.
- Via a scratch copy of the proposal: `attempts/a3-strict-via-scratch-probe-copy.txt` —
  **exit 1**, same defects; the proposal's `lane_root()` fallback finds the committed
  bytes, so a scratch copy is a sound checker (it printed the committed probe sha
  `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb`, which equals
  `sha256 plans/round65_c1_sqlite_probe.py`, re-measured).

Side conditions for C2's kill rules (b)/(c), all green:
`attempts/c2-strict-committed-r65.txt` — strict over `corpus/evidence/round65/sqlite-gcov-probe.txt`
→ `CHECK ok cases=5 strict=yes`, `PREDICATE R65-C1 strict-pass`, exit 0;
`attempts/c2-default-committed-r65.txt` — default over the committed receipt →
`PREDICATE R65-C1 pass`, exit 0; `attempts/c2-default-fabricated.txt` — default over the
fabricated fixture → `PREDICATE R65-C1 pass`, exit 0 (red-before reproduced; default mode
unchanged). Verdict: **KILLED-BY-COUNTER** — strict refuses the header-laundered fixture
and the frozen C2 counting commands hold.

## A4 — column layer returning the reference output via master_weight: LIMIT (probe cannot tell it apart)

Construction (`attempts/a4-cheat-parallel_linear.py`): a K1 variant whose
`ColumnParallelLinear` registers the **whole master weight** as a non-gradient buffer and
reconstructs the full output locally — the local block from the sharded `self.weight`
parameter, the other ranks' blocks from the buffered master rows, concatenated in rank
order. **No all-gather is ever issued**; memory is doubled, which is the exact cost tensor
parallelism exists to avoid. `RowParallelLinear` is the faithful K1 build. The grader was
run against it in scratch with the probe's own bwrap command shape
(`attempts/a4-run_cheat.py`), under the shared probe lock, port checked free first.

- `attempts/a4-cheat-junit.xml`: rc=0; outcome vector `exists=P` and all 12 layer tests
  `P` — **IDENTICAL key-by-key to K1's committed junit vector** (runner output recorded in
  this file's build log; both vectors all-P, `IDENTICAL`). 

Verdict: **LIMIT — a documented limit of the grader, not a failure of the probe.** If the
outputs agree, the probe cannot tell the cheat from K1: its only per-case evidence is the
13 boolean outcomes (plus rc), and a receipt built from the cheat run would carry
all-P vectors, pass the frozen-table check, and differ only in `case_sha`/`junit_sha`,
which identify bytes, not behaviour. What the grader **can** see: that
`/app/parallel_linear.py` exists; the values of parameters named `weight`/`bias` (so the
cheat must still expose a correct shard — this is why a *naive* master-weight cheat, whose
forward ignores `self.weight` and whose `weight.grad` therefore stays `None`, dies in the
backward assertion with a `TypeError`, a different vector, at ws 2 and 4); forward output
values vs an `nn.Linear` reference (atol 1e-5); and the corresponding grad slices. What it
**cannot** see: whether any collective actually ran, the doubled memory footprint, or
latency — i.e. it verifies sharding semantics at the API surface, not sharded execution.
The frozen table is discriminating for behaviour (K3/K4/K5 all fail it), but two
implementations with identical API-level behaviour are indistinguishable by design.

## A5 — can K2 or K3 ever pass the R66-C1 predicate in any buildable receipt: KILLED-BY-COUNTER (no), with one named LIMIT

Constructions tried, all in scratch (every `--check-receipt` against the frozen probe):

1. K2-only receipt (kill-rule (d) shape; only k2's VECTOR line present, other lines
   well-formed): `attempts/a5-r0-k2only-receipt.txt` — refused, exit 1, four defects
   `k1-ref/k3-stub/k4-col-nogather/k5-row-noreduce has no VECTOR line`.
2. K3's VECTOR forged to all-P (junit untouched): `attempts/a5-r1-k3-vector-forgery.txt`
   — refused, exit 1, `k3-stub vector differs from the frozen table`.
3. K2's VECTOR forged to all-P with K2's real (all-F) junit: refused — this is exactly A2.
4. Hand-built receipt written entirely from the frozen table + committed case/junit shas,
   **no run of any kind**: `attempts/a5-r2-handbuilt-table-receipt.txt` — **accepted**,
   exit 0, `CHECK ok cases=5`, `PREDICATE R66-C1 pass` — but it shows K2 all-F and K3
   `exists=P` + 12×F, i.e. the predicate only passes when K2/K3 are shown **failing**.
5. Junit-content swap: K2's junit file replaced by K1's 13-pass junit bytes, receipt's
   `k2-none junit_sha` updated to those bytes, VECTOR kept at the table's all-F:
   `attempts/a5-r3-k2-junit-swap.txt` — **accepted**, exit 0.

Verdict: no construction makes K2 or K3 **pass** in an accepted receipt — every
passing-behaviour forgery (3 constructions) is refused by the frozen-table clause, and a
receipt missing cases is refused by the VECTOR-completeness clause. The LIMIT that the
constructions expose: `--check-receipt` proves text-vs-table and sha-vs-bytes-at-named-
paths, **not that a run happened** (construction 4 passes with zero live-run data) and the
junit bytes are bound to the receipt's own sha, never parsed against the VECTOR claims
(construction 5 passes with a K2 junit that actually contains 13 passes). This is the same
self-attestation class R66-C2 names for strict; C1's junit binding is stronger than C2's
value binding but is not a proof-of-execution. Not a refusal defect: the predicate's
frozen table and the receipt of record remain the authority, and both attacks on
*existing* receipts (A1) and *forged vectors* (A2, A5-2/3) are refused.

## Roll-up

| Attack | Construction | Verdict | Marking |
|---|---|---|---|
| A1 | junit byte flip after the fact | refused, exit 1 (`k1-ref junit_sha does not match`) | KILLED-BY-COUNTER (+ LIMIT: bytes+sha rewrite accepted) |
| A2 | K2 VECTOR ← K1's vector | refused, exit 1 (`k2-none vector differs from the frozen table`) | KILLED-BY-COUNTER |
| A3 | strict after header rewrite | refused, exit 1, 8 value-based defects, unchanged by the header | KILLED-BY-COUNTER |
| A4 | communication-free master-weight column layer | 13/13 P, vector identical to K1 | LIMIT (grader sees API behaviour, not sharded execution) |
| A5 | K2/K3 passing receipts | every passing forgery refused; hand-built no-run receipt accepted with K2/K3 failing | KILLED-BY-COUNTER (+ LIMIT: no proof-of-execution; junit content unparsed) |

Neither claim is falsified: R66-C1's predicate refused every tampering and forgery
construction put to it (A1, A2, A5-1/2/3), and R66-C2's strict gate refuses the
header-laundered fabricated fixture while the default-mode regression pins hold (A3). Two
true limits are named for calibration: the grader cannot see sharded execution (A4), and
neither `--check-receipt` can prove a run happened (A5-4/5, A1 caveat).
