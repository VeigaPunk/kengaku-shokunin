# CriticClaims — R93-C1 / R93-C2 hostile closure review (round 93, seat report)

Reviewed at: BASE `28e9f8bf`, P1 `17cb9337`, P2 `0e77e98f`, F `d8d0a4b8`, T `22972a31` (frozen
tip). Method: independent re-execution of both frozen predicates in a `git clone --shared`
scratch clone, plus seven purpose-built attacks (stub probes, forged mini-lane, ledger swap,
mutated gate, committed forgery re-run). No instrument was modified in the lane; all attacks
live in scratch commits. Raw receipts: `receipts/` beside this file. No tools were installed
(no pacman, no uv, no downloads); host sysctls untouched (`user.max_user_namespaces=122865`,
read-only check).

## 0. Freeze-integrity audit (all positive)

- `git log F..T` holds exactly one commit (`22972a31`) touching only `corpus/SOURCES.md` (+7),
  `corpus/evidence/round93/scheme-probe.txt` (+22) and `plans/grader-population-ledger.json`
  (7 lines, exactly the one-member flip). Zero commits touch any tabled instrument, the claims
  file, the case table, or `.ufo/waves/round-93/` (receipts/history-f-t.txt).
- All 9 tabled sha256 recomputed from blobs: equal at P1, equal to the F table, equal at T
  (receipts/table-hashes.txt). Controls and dry runs are committed at P2, before F.
- The assignment's "run the C2 counter or `git log F..T -- plans/`" — both run; both clean.
- **No instrument changed after F.** The round-92 root failure does not recur.

## 1. R93-C1 (coverage) — verdict: VERIFIES

My own full re-run at T (4m6s, bwrap, userns 122865, Python 3.14.8): `LEGS L1..L9 pass`,
`TARGET executed_rows=37 member=schemelike-metacircular-eval located=1 executed=1 cases=8
legs=40 mismatches=0 defects=0`, `PREDICATE R93-C1 pass`, rc 0 (receipts/e3-...). This
reproduces L1's `c1-tip.txt` line-for-line.

Cheapest controls, built and run:

- **Post-F probe substitution (E1-A/E1-B).** A stub probe that never runs the grader, committed
  after F: its echoed OBSERVATIONS block satisfies L6 exactly; L8+L9 (E1-A) and then only L8
  (E1-B, receipt stamp corrected) stay red, rc 1. The frozen-instruments table — read by the
  counter from the blob at the commit that added the claims file, not from the mutable tree —
  is the single load-bearing tripwire, and it holds.
- **Forged mini-lane (E2).** A fresh two-commit repo with the full T tree, the stub probe, the
  table row and receipt stamps blessed to the stub, and its own LANE_TIP: the real, unmodified
  counter prints all nine legs pass and `PREDICATE R93-C1 pass`, rc 0. This is the do-nothing
  control reaching the frozen predicate; it requires control of the entire lane content and
  history, i.e. it is outside the post-F tamper model the round defends against, but it bounds
  what the counter can mean.
- **Ledger swap (E4).** Two non-claimed members swapped wholesale (executed `build-pmars` ↔
  unexecuted `adaptive-rejection-sampler`), preserving every aggregate L7 checks: full counter,
  full 4-minute real-probe re-run included, prints all legs pass, rc 0.

**What C1 therefore proves** (and all of it is real, executed, and reproducible by a second
party): the tree at T holds byte-identical frozen instruments (L4/L8, anchored at F's blob);
the committed receipt is the product of exactly those bytes re-run from a `git archive` of T
(L6); the grader behavior is stable across dry run → official run → counter re-run, including
the 60 s timeout wall (C06) and the seven mispredicted-then-frozen C08 legs (L5); the ledger
flip and the four class cells match the claims text (L7); the capture pins match the counter,
probe, receipt, and the S290–S292 fetch receipts (L2; quadruple sha agreement, including
`fbb84e3c…` byte-identical to the lane capture per SOURCES).

**What C1 does not prove**, and the claims text already discloses the biggest part:

- The eight frozen vectors are *observations*, not predictions: dryrun-2 shows C08
  `predicted=F,60,3,63,0 observed=F,56,7,63,0 ok=False` and the final table freezes the
  observed value. L5 can only fail if probe behavior changed between the pre-freeze dry run
  and the official run — it is a run-to-run stability leg, not a mechanistic-prediction leg.
  Disclosed in the claims ("only the vectors are frozen"); info, not a defect.
- "located" rests on the S290 census and the capture pins; the counter cannot independently
  confirm that `2fd12b88`'s `test_outputs.py` is what GitHub served on 2026-11-05 (same trust
  frame as round 92's disclosed "grades captured bytes, not the TB2 harness" limit).
- Execution provenance: see E2 — with full lane control the predicate is reachable without any
  grader ever running (finding R93-C1-F1).

No leg failed, no DEFECT line, `executed_rows=37`, no mismatch at T; the kill rule is not
triggered. The C1 sandbox-outage channel is real (`--bwrap /nonexistent/bwrap` → rc 2, P2
control), the do-nothing control at BASE fails 9/9 legs (P2 control), and the ledger-only
forgery passes only L7 (P2 control) — all three re-read from the P2 receipts and consistent.

## 2. R93-C2 (calibration + capability) — verdict: VERIFIES

My own full re-run at T: `W1 pass`, `W2` 5/5 cells ok, `W3 pass`, `W4 pass freeze=d8d0a4b8
summary=(9, 9, 0)` with all nine instruments `touched=0 verdict=intact`, `TARGET legs_passed=4
of 4`, `PREDICATE R93-C2 pass`, rc 0 (receipts/e5-...). W1's census (4,1,3; exactly
`round92_c1_replay.py` intact) reproduces the round-92 verifier spot-check's independently
measured freeze breach (its `git diff --stat f0018773 1df76536 -- plans/` names the same
edited instruments) — the calibration number is a true re-measurement of adjudicated history,
not a self-grade.

- **Calibration move or operability tool?** Both, honestly labeled: the calibration axis is
  declared *held at ceiling 10*, so nothing is counted up; W1/W4's broken-counts are
  confirmatory (W1 = the already-adjudicated M8 breach; W4 = this round's own tripwire), and
  the actual new content is the capability (the gate). W3 (battery runs) is explicitly demoted
  as worthless evidence, correctly — both `bytes_only` and `log_only` print
  `SELFTEST cases=10 ok=10` unconditionally while being broken gates. Discrimination is carried
  by W1+W2, and my E7 re-run of the committed `always_intact` forgery through the counter path
  confirms it is caught on exactly those legs (W1 4,4,0; W2 three cells RED; rc 1).
- **Do-nothing / cheaper controls.** The committed four forgeries (P2 receipts) plus my E7
  cover always-intact, always-broken, bytes-only (misses edit-then-revert), log-only (misses
  lying table). My cheaper control **gate2** — the real gate with one line changed so the
  claims table is read from the working tree instead of the freeze blob — passes the full
  counter 4/4, rc 0 (E6). Neither W1–W4 nor battery cases B01–B10 ever edit the table after
  the freeze, so the counter cannot see where the gate reads the table it audits (finding
  R93-C2-F1). The shipped gate is honest — `evaluate()` reads `blob(root, freeze, claims)`,
  source-verified — so this does not flip R93-C2 this round; it is a fixable
  counter-completeness defect (add a post-freeze-table-edit battery case and one W2 variant).
- **Causally separable as claimed? Yes, verified in code and by execution.** The C1 counter
  never invokes the gate (my E1–E4 runs exercised C1 with no gate on any path), and the C2
  counter never reads the receipt, the ledger, or any probe output (my E5–E7 runs touched
  only gate bytes, fixture repos, and lane history). The one shared invariant — no post-F
  instrument change — is implemented twice by independent parsers (the counter's
  `frozen_table()` vs the gate's `parse_table()`), so a post-F edit fails both claims by
  construction (L8 and W4 simultaneously). That is redundant coverage, not causal coupling.
- **Universal clauses the counter does not enumerate** (all routed, none flips this round):
  1. the gate's table-read location (E6);
  2. the ledger beyond aggregates — `plans/grader-population-ledger.json` is not in the
     frozen table and nothing pins non-claimed entries to F (E4);
  3. the claims file's own prose — post-F edits to predicate wording would be invisible to
     every leg (no commit touched it F..T here — verified);
  4. pre-freeze byte substitution / full lane forgery (E2) — the trust anchor is the P1→P2→F
     procedure plus SOURCES, not any post-F instrument.

## 3. Findings

- **R93-C1-F1 (minor, route 94).** Forged mini-lane with an echo-stub probe reaches
  `PREDICATE R93-C1 pass` rc 0 (receipts/e2-...). The counter authenticates internal
  consistency, not provenance. Fix direction: a fleet-side pin of F (e.g. the round report
  quoting the claims-file blob sha, checked by the integrator outside the lane), so a forged
  lane cannot reuse the round's history. No effect on this round's verdict: real-lane history
  audited clean (§0), and post-F substitution in the real lane is caught (E1-A/E1-B).
- **R93-C1-F2 (minor, route 94).** L7 audits only aggregates (executed_total, the claimed
  member's status/round/classes, four class cells); a two-member swap preserving them passes
  the full counter including a real 4-minute probe re-run (receipts/e4-...). Fix direction:
  require `diff F..T` on the ledger to touch only the claimed member's entry. The actual
  F..T ledger diff is exactly the one-member flip (receipts/history-f-t.txt), so this round's
  flip is honest.
- **R93-C1-F3 (info).** L5 is a stability leg, not prediction: vectors := dry-run observations
  (dryrun-2.txt C08 predicted 60/3, observed 56/7, frozen as predicted). Disclosed in the
  claims text; no repair needed, but round 94 should not let "mismatches=0" be paraphrased as
  "predictions confirmed from mechanism".
- **R93-C2-F1 (minor, route 94).** Counter accepts a gate that audits a mutable table
  (gate2, receipts/e6-...). Fix: battery case "table edited post-freeze must still be judged
  per the freeze blob" + one W2 fixture that edits claims.md after the freeze commit.
- **R93-C2-F2 (info).** C2's calibration content is confirmatory, not additive (axis at
  ceiling; W1 re-measures adjudicated M8). Correctly framed by the claims; keep the capability
  row, not a calibration move.

## 4. Verdicts

- **R93-C1: verifies.** Frozen predicate reproduced end-to-end by an independent executor at
  T; every kill-rule channel exercised and behaving (base fail, forgery fail, sandbox rc 2,
  substitution caught); no verdict-flipping defect found. Epistemic scope as in §1.
- **R93-C2: verifies.** Counter reproduced 4/4 at T; W1 matches the independent round-92
  spot-check; forgeries discriminated; separability claim accurate; no verdict-flipping
  defect found. Counter-completeness gaps routed (R93-C2-F1, plus C1-F1/F2 shared anchor).

Main-agent checks already done here, no need to repeat: predicate re-runs at T (both claims),
9-instrument hash audit P1/F/T, F..T history and ledger-diff audit, forgery discrimination
re-run. Not done (out of seat scope): live re-fetch of S290–S296 URLs; jj state inspection.
