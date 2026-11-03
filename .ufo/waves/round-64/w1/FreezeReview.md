# FreezeReview — round 64, r64 w1 (non-author, 2026-11-03)

Freeze: plans/round-64-claims.md @ 859ac24f41061bffde588b9ed5d5adfea5ca8e27 (base tip 5f517fe7).
Method: extracted each claim's sentence (predicate / counting command / kill rules / controls),
read each instrument's code, re-derived every clause, independently re-ran all three counters
from my own scratch (receipts: red-set-reproduction.txt, openedit-sim.txt in this seat dir).
No tools installed (none needed). No git/jj mutations. Read-only over the lane tree.

## Per-claim verdicts

| claim | verdict | sentence-vs-code finding |
|---|---|---|
| R64-C1 (coverage) | **AGREE** | Counter = same sentence, all clauses priced (detail below). |
| R64-C2 (operability) | **AGREE** | Patch is exactly the permitted delta; all three predicate clauses evidenced and independently reproduced. |
| R64-C3 (freshness) | **Major** | Counter's pass path never requires the 29 previously-red entries to classify TRIO-ADDENDUM — the forbidden opening-edit repair prints `PREDICATE R64-C3 pass` exit 0 (empirically demonstrated). Plus one Minor on the observed-result sub-clause. |

## R64-C1 — AGREE

Frozen sentence: pass iff (1) observed 7-leg vector K1–K5 equals the frozen vectors, (2) K2
receipt records leg-5 fragment `Port 5328 is not listening`, (3) receipt records port 5328 free
at battery start, (4) K1 server PID recorded before the handshake leg ran.

- Probe `ProbeBuild/round64_c1_kvstore_probe.py` (sha256 9f56d25d…): grader byte-verified at run
  time (GRADER_SHA256 = 115de2e9…, leg-order drift → SETUP); bwrap argv = the frozen r37/r63
  house shape, network shared (no --unshare-net); `predict_legs()` re-derives all five vectors
  from the case declarations and aborts (SETUP prediction-drift) on any disagreement with the
  frozen literals — verified equal for all five.
- `--check-receipt` prices every clause: vectors in three redundant encodings (VECTOR line, CASE
  observed/expected fields, per-LEG verdicts) must all equal frozen; K2 fragment checked both in
  the `K2-FRAGMENT` line and in `LEG K2 5 frag=`; `PORTFREE before-battery True` + per-case
  before/after required; K1 `server_pid` digits + `pid_before_legs=True` + `server_ready=True` +
  `server_log=SERVER_UP_5328` required; stored PREDICATE must agree with the re-derivation.
- Kill rules executable as written: K2 leg-5 P while port free → battery refuses (SetupError
  `k2-leg5-answered-with-port-free`, exit 2, **no receipt written**) — never grades through a
  foreign listener; any observed vector ≠ frozen → receipt `fail`, exit 1 (MISS as declared);
  frozen vectors are compile-time literals, no re-freeze path.
- Live receipts observed: kvstore-probe.txt shows all five vectors equal to frozen (K1
  P/P/P/P/P/P/P pid=3561122 pid_before_legs=True; K2 F/P/F/F/F/F/F with the exact fragment
  "Port 5328 is not listening - no real gRPC server is running"; K3 P/P/P/P/P/F/F with the
  predicted "Not a real gRPC server…" / "SetVal returned wrong value: 43" fragments; K4
  P/P/F/F/F/F/F; K5 P/P/P/P/F/P/F with `_InactiveRpcError … UNAVAILABLE` uncaught in leg 7 —
  grounding the K5 leg-6-P/leg-7-F prediction in the grader's own except structure);
  determinism.txt: two full batteries, identical VECTOR/PREDICATE lines; selftest.txt 7/7
  negative fixtures; server-log sidecar carries `SERVER UP 5328` per server case.
- My independent re-run: `--check-receipt kvstore-probe.txt` → `CHECK ok cases=5`,
  `PREDICATE R64-C1 pass`, rc 0. `--render-table` prints exactly the frozen vectors.
- Named limitation present in receipt header, selftest note, and docstring.

## R64-C2 — AGREE

Frozen sentence: pass iff (a) escape fixture under PATCHED gate fails with `DETAIL escape=`
present and rc 1, (b) selftest 4 cases (GOOD pass; BAD-COUNT/NO-SECTION/BAD-ESCAPE fail) each
asserting expected verdict + stable finding id, (c) real SKILL section still passes unchanged.

- `GateScopePatch/gate-scope.patch` (sha256 2b3282cc…, 97+/17−) is exactly the permitted delta:
  `_escape_reason` (absolute / `..` segment / normpath escapes root, via is_relative_to);
  `_resolves` returns False on escape; `not escapes` added to the ok clause (fails even if the
  share clause alone would pass); `DETAIL escape=<tokens>` printed first in the fail block;
  selftest extended 3→4 fixtures with verbatim expected finding lines; trio subcommand and all
  other gate behaviour untouched (trio-sanity.txt).
- Clause evidence (receipts/): escape-after.txt — same fixture, driver diff shows only the LANE
  constant retargeted → `ROWS n=16 class_match=True count_mismatch=0 paths total=2 resolved=1
  share=0.50` + `DETAIL escape=/home/vgpnk/.config/uv/uv-receipt.json` + rc 1. selftest-after.txt
  — 4/4, rc 0, BAD-ESCAPE asserts `DETAIL escape=/usr/bin/,../escapee.json` verbatim.
  real-section-after.txt — `ROWS n=16 class_match=True count_mismatch=0 paths total=24
  resolved=24 share=1.00`, rc 0, no escape line. discrimination.txt — unpatched gate counts
  `/usr/bin/` resolved (fails only on `../`), patched gate names both; the asserted line is one
  the unpatched gate never prints. landing-check.txt — patch applies rc 0 to a fresh freeze-tip
  clone, resulting bytes byte-equal the seat's patched module (a98d9c0f…), selftest + real
  section re-run green there, and the lane tree's plans/round63_gate_checks.py still hashes to
  the freeze bytes 797085c2… (write scope respected).
- My independent re-runs: patched-module `--selftest` → 4/4 rc 0; patched-module
  `depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .` →
  `PREDICATE R63-C2 pass` rc 0 with total=24 resolved=24 — matches my own token enumeration of
  the real section (24/24 resolve under the new rule, escape set empty), so clause (c) cannot
  regress on this host.
- Kill rule priced: selftest + real-section receipts carry n / class_match /
  count_mismatch / escape for direct comparison.

## R64-C3 — Major

Frozen sentence: pass iff (a) after-receipt prints `red=0` **with every previously-red entry
carrying a dated round-64 freshness addendum** naming its re-verification command and observed
result, (b) red set at base equaled the frozen 29-entry list (SETUP cross-check in the
red-before receipt), (c) README gains one `lessons/round-$N.md` row for N in 57..62.

- **Major — pass path under-prices clause (a).** `SweepBuild/round64_trio_sweep.py`
  `measure()`: pass ⇔ `not red` (+ every frozen entry still exists as a file). It never requires
  the 29 previously-red entries to classify TRIO-ADDENDUM. Empirical (openedit-sim.txt): a
  scratch lane whose 29 frozen entries were "repaired" by rewriting their OPENING bytes to carry
  the trio — the exact form the frozen kill rule declares dead ("repaired by editing its opening
  bytes instead of appending → the claim is dead") — yields `SWEEP files=29 trio_open=29
  addendum=0 red=0` + `PREDICATE R64-C3 pass`, exit 0. The receipt does surface `addendum=<n>`
  and per-entry `ADDENDUM <rel>` lines, so a reader can see the violation, but the frozen
  counting command's exit semantics do not implement the sentence. **Minimal fix:** in
  `measure()`, on the red==0 path, require every frozen-list entry to classify TRIO-ADDENDUM;
  on any entry classifying OPEN (or RED), print `PREDICATE R64-C3 fail` (rc 1) with a
  `DETAIL not-addendum=<entries>` line. With the intended append-only repair the counting
  command still exits 0 (all 29 classify ADDENDUM, as SweepBuild's after-sim control already
  shows), so this only closes the forbidden path.
- Clause (b) — implemented and evidenced: red set nonempty ⇒ entry-for-entry equality vs the
  frozen list else exit 2 SETUP (controls: short/long/partial/empty/deleted all exit 2);
  sweep-red-before.txt run at the freeze commit in a clone: `SWEEP files=65 trio_open=36
  addendum=0 red=29`, red set == frozen 29, `PREDICATE R64-C3 fail` exit 1, INFO line carries
  the frozen sha fe0498fb… . My independent gate-based reproduction of the red set matches the
  frozen list entry-for-entry (red-set-reproduction.txt), including the two nuance entries
  (`tb2-grader-vacuity-triage.md` keys beyond the 12-line window; `tb2-cancel-async-tasks-grader.md`
  non-line-start `verified-at:` + `recheck:` at line 79) — the sweep imports the gate's own
  `trio_missing` (parity control: `same_object=True`), so no second convention exists.
- Clause (c) — direct grep counting command; before-state verified (before-state.txt sha
  416d9640… : round-53..56 = 1, round-57..62 = 0; live tree still 0 each). No instrument needed.
- **Minor — "and observed result" not priced.** RECHECK_RE only requires a non-empty `recheck:`
  line; an addendum naming a command but no observed result classifies ADDENDUM — the tool's own
  ADDENDUM selftest fixture is command-only. Clause (a) requires the addendum to name the
  command **and observed result**. Minimal fix: also require an observed-result line in the
  block (fixture updated), or an L1 dated amendment assigning result-line presence to the
  closure's re-derivation step (the kill rule already has the closure re-run the command).
- Selftest/fixtures otherwise match the sentence (RED/ADDENDUM/OPEN classify as named; base +
  repaired sweep stages correct); the `--lane .` counting shape verified in a freeze-tip clone
  (relative-lane.txt) and by my own re-run.

## Cross-claim sanity (frozen controls re-derived)

- k2-empty-capture.txt sha256 ae0a78ee… ✓; LEGS `F P F F F F F` == frozen K2 ✓; leg-5 fragment
  "Port 5328 is not listening - no real gRPC server is running" present ✓.
- k4-protoonly-capture.txt sha256 b262cfe5… ✓; LEGS `P P F F F F F` == frozen K4 ✓; the K4 input
  proto sha c89bcb1c… ✓ and contains all five definitions leg 1 asserts (leg-1 P grounded).
- Grader test_outputs.py sha256 115de2e9… ✓; 7 test functions in file order ✓; leg-5 f-string is
  the fragment's exact source; leg-6 imports sit outside the try (ModuleNotFoundError paths in
  K2/K4 captures reproduced); leg-7 has no except arm (K5 leg-7 F grounded).

## Minor — freeze-doc citation path (no rule change)

Claims doc: "Red-before … committed: `corpus/evidence/round64/escape-before.txt`" — that file
does not exist there; the receipt is committed at `.ufo/waves/round-64/claims/escape-before.txt`
(sha256 9f335b5f… as declared, content matches the doc's quoted ROWS/PREDICATE/rc lines). The
predicate does not depend on the path; a dated L1 amendment should correct the citation. No seat
may edit the claims doc, so reported, not fixed.

## Residual risk / verification gaps

- C1: the live battery ran in ProbeBuild's scratch; the L1 must land the receipt at
  `corpus/evidence/round64/kvstore-probe.txt` (the frozen counting command's path) together with
  the `.server-log` sidecar and the probe at `plans/round64_c1_kvstore_probe.py`. I verified the
  counter against the seat copy; post-integration re-run is the L1's closure step.
- C2: the patched gate is not yet in the lane tree (by design — L1 integrates the patch); my
  clause (a)/(b)/(c) reproductions ran against the seat's patched module and the landing-check
  clone, both byte-identical to what `git apply` produces at the freeze tip.
- C3: after the Major fix, the after-receipt must show `addendum=29` with every `ADDENDUM` line
  a frozen entry; the closure still owns re-running each addendum's named command (kill rule).
