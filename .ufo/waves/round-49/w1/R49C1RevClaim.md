# R49C1RevClaim — adversarial review: R49-C1 falsifiability, kill-rule coverage, causal separability

Seat: R49C1RevClaim (reviewer) · Claim served: R49-C1 (calibration) · Wave: round-49/w1
Axes named: **calibration** (judged axis); assessed against counter-integrity, kill-rule coverage, and C1↔C2 causal separability.
Revision inspected: REV `9d2900af41e4d1fc6022eff99010436fde6dbd93` (stage-1 freeze; committed lane tree).
Scope held: read-only; no scored counter/probe run (counter `plans/round49_c1_verify.py` absent at base by design; literals `<P><H><S><B><M>` unbound until stage 2 — any r46-counter run would measure the wrong contract). No C1/C2 admission claimed.

## 0. Precondition: stage-1 freeze exists in the committed tree and predates measurement

- `git log -1 9d2900af…` → `2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 …` — freeze commit is in the committed tree and predates this review.
- `git log -- plans/round-49-claims.md` → the freeze commit is the *only* commit touching the claims file; `git diff 9d2900af… HEAD -- plans/round-49-claims.md` → empty; worktree sha256 `7292f4e0…` == `git show 9d2900af…:plans/round-49-claims.md` sha256 `7292f4e0…`. **No freeze amendment exists.**
- `git diff --stat 3a548330… 9d2900af…` → `plans/round-49-claims.md | 167 +++…` only. The "base fence @ `3a548330`" control and the fence at the freeze are the same blob (`a2b128ae…`); no base/fence ambiguity.
- Artifact existence at `9d2900af…`: `plans/refusals46`=20 files, `plans/sealed46`=12, `battery42/43/44`=5+7+10=22 module files; `plans/honest49/`, `plans/sealed49/`, `plans/mutants49/` absent (stage-2 targets, as declared); `plans/round49_c1_verify.py` / `round49_c2_verify.py` absent (wave-1 artifacts, as declared); the 16 rebuilt honest classes are **committed** at `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/{r46novel,novel48}/n01–n16.py` — the "16 novel honest classes of `w1/R48C1ExecHonest/`" exist as tree bytes, not just a report claim.

## 1. Commands run (all `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin`, B=9d2900af…)

```
git log -1 --format='%H %cI %s' 9d2900af…          → (shown above)
git diff 9d2900af… HEAD -- plans/round-49-claims.md  → empty
sha256sum of committed vs worktree claims file      → both 7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83
git ls-tree B -- plans/{fixture_fence,round46_c1_verify,round46_c3_verify,order_check,polyglot_c_py_probe}.py
  → a2b128ae… / 415b4070… / 814bf4a3… / d298b6c0… / f3847115…
git ls-tree -r B -- plans/{refusals46,sealed46,battery42..44,honest49,sealed49,mutants49}  → counts above
git show B:plans/round46_c1_verify.py | grep -nE 'pkg_gate|filler|pkg-spec|polyglot|order_check|c3_verify|mutants4' → rc=1 (no C2 refs)
git show B:plans/round46_c3_verify.py | grep -nE 'fixture_fence|battery4|refusals4|sealed4|honest|c1_verify|mutants4|round44' → rc=1 (no C1 refs)
git show B:plans/round44_c1_verify.py | sha256sum   → 6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad == committed pin
git show B:plans/order_check.py | sha256sum       → 948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc == committed pin
git show B:.ufo/waves/round-48/w1/R48C1ExecCounter.md | grep 'REV|HONEST fixtures=120'
  → `REV abb08e283a0eba0eb469fbc8d2f4d7cb2f49c359`; `HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0`
```

## 2. Findings by severity

### F1 (medium) — BENIGN-ADMIT vs `clean=<S>` is under-specified; only the admit-all control resolves it
Delta (b) reclassifies a hostile-module admission with `touches=0` as `BENIGN-ADMIT` — "counted separately, never a leak" (claims L58–60) — while the frozen predicate still demands `REFUSALS … clean=20` and `SEALED … clean=<S>` (L74–76) and the Work bullet still requires hostile modules to "stay refused" (L86). The r46 rollup this counter inherits (`round46_c1_verify.py:565–585`) counts *any* ADMIT/ERROR as `LEAKED`; the v3 counter must diverge from inherited code here, and the freeze never states whether BENIGN-ADMIT counts toward `clean` or `contradicted`. Two readings exist; only one is self-consistent: **if BENIGN-ADMIT counted toward `clean`, the frozen admit-all must-fail control could not fail** — admit-all yields `touches=0` everywhere, printing `clean=20 clean=<S>`. So the controls force `BENIGN-ADMIT ∉ clean`. Falsifiability survives *via the control set*, but the freeze text leaves a live stage-2 implementation trap: a counter implementing the wrong reading freezes an unsatisfiable-by-construction control set → honest stop. Recommendation to L1/stage-2: implement BENIGN-ADMIT as non-clean **and** fold it into `contradicted` — under the r46 advertised definition ("refused AND touches nothing outside"), a benign admit *is* a contradiction; leaving it out of `contradicted` prints `CALIBRATION … contradicted=0` while the predicate fails on `clean`, an audit-confusing pass-shaped line.

### F2 (medium-low) — MUTANTS floor `<M>/2` is gameable, ambiguous for odd M, and blind to equivalent mutants
- Floor is a *fraction*, not a difficulty bound: a mutation-tester wave can satisfy `caught ≥ <M>/2` with trivially catchable mutants (syntax errors, wholesale deletions) while the battery never probes subtle regressions (weakened allowlist key, widened path check). The r46 observed 2/13 justifies a floor; it does not bound mutant *quality*. Per-mutant receipts are required (L70–72) and mitigate post-hoc audit, but nothing in the kill rule rejects a weak battery.
- `floor=<M>/2` never states integer semantics: `<M>` odd → floor `<M>/2` (round-down) vs ⌈`<M>`/2⌉ differ by one mutant — a live stage-2 spec gap on a kill-rule threshold.
- Equivalent mutants are *uncaught by construction* (a mutant preserving behaviour keeps the clean signature). If a hostile wave authors >50% equivalent mutants, a *correct* fence fails the floor — a false-negative hazard that kills the claim for reasons orthogonal to fence quality.

### F3 (low) — shared pinned input `plans/order_check.py` spans both claims; "share no input" is imprecise
C1's counter chain digest-pins `plans/order_check.py` (`round44_c1_verify.py` pin `948d5e1d…`, verified == blob at `9d2900af…`); C2 runs it in its V8 leg (`round46_c3_verify.py:417`) and names it read-only in the separability table (claims L152). So the two claims *do* share one input; the separability sentence "the counters share no input" (L152–153) is false at the pin level. Harm is bounded: both uses are read-only/digest-verified and neither claim writes the file — but any third-party or accidental edit to `order_check.py` reds **both** predicates simultaneously (C1 `pins=` fail; C2 V15/V8), violating the stated property "a C1 failure cannot green or red any C2 leg and vice versa" at one shared file. Record as an omnibus invariant dependency, not a separability violation.

### F4 (low) — wave-1 novel honest classes carry no explicit per-module digest-pin clause
Delta (a) demands per-module digests only for "the 16" rebuilt classes; the wave-1-authored classes are named only by count fold into `<H>` (L56–57). Inherited `pin_issues` mechanics should still force pins (`:unpinned` → `PINS mismatched>0` → fail), and `fixtures=<H>` count-binds the leg — so the mechanics close it — but the freeze text under-specifies: an unpinned committed honest file could be byte-swapped post-stage-2 without tripping `<H>` if the v3 author narrows `pin_issues` to declared sets. Also: novel classes are authored "against the *base* fence description"; if a wave-1 seat authors a class the base *correctly* refuses (e.g., genuinely out-of-`d` store), it lands in `<H>` and the predicate becomes unsatisfiable through no fence fault — a claim-killing author-error class the stage-2 pin step should gate on (each novel class demonstrably admissible under the mount-boundary rule before `<H>` is frozen).

### F5 (informational) — single stage-2 amendment commit couples freeze logistics
Stage 2 is "one amendment commit" filling both claims' literals (L19–24). A malformed amendment blocks both claims' freeze simultaneously; predicates stay separable (each measures on a clean clone of the landing tip), so this is a sequencing exposure, not a counter coupling.

## 3. Falsifiability under the frozen kill rule — assessment

The predicate is fully observable: every line is counter-printed and exit-status-bound; literals `<P><H><S><B><M>` are stage-2-pinned; non-vacuity is preserved (`REFUSALS total=20` hard-coded; `<M> ≥ 12` floor bound; `fixtures=<H>` exact-bound); the six must-fail controls (no-fence, base fence @ `3a548330`, r45 keyed, admit-all, refuse-all, name-keyed) exercise every leg including the base-fence honest-leg failure (8/120 measured, `REV abb08e2…`). Kill-rule coverage is complete for the four failure families (predicate line off; traced outside access admitted; honest refusal; mutant floor unmet). **The claim remains falsifiable.** Residual weaknesses are F1–F4: none remove a falsifiable branch, but F1/F2 can produce a *wrong-sign* verdict (false-fail from mis-classified BENIGN-ADMIT or equivalent mutants; false-confidence from a weak battery).

## 4. Claim widening — none found

Predicate-line shape is a strict superset of the r46 contract plus *declared* deltas (BENIGN informational line, MUTANTS leg); population growth is by declared mechanism, not silent scope creep; the measured 8/120 replaces the unreproducible 9/9 honestly (claims L15–16); the behavioural reclassification narrows what counts as a leak but — per F1 — the controls pin the non-widening reading.

## 5. Dependence on C2 artifacts — none

C1 inputs: `fixture_fence.py`, `round46_c1_verify.py`→`round44_c1_verify.py` (digests verified), `refusals45/46`, `sealed46`, `battery42–44`, `honest49`, `sealed49`, `mutants49/c1-mutants.json`, `w1/R48C1ExecHonest/*`. Verified: `round46_c1_verify.py` contains zero references to any C2 path (grep rc=1); `round46_c3_verify.py` contains zero C1 refs (grep rc=1). Sole shared artifact: `plans/order_check.py`, read-only on both sides (F3). C1's predicate does not read `mutants49/plan.json`, the probe, pkg-spec, dry table, receipt, or `corpus/evidence/round49/*`.

## 6. Residual risk and verification gaps

- Static review only: whether the *written* v3 counter implements F1's consistent reading and F2's floor semantics is a stage-2 verification gap — the claims receipts under `.ufo/waves/round-49/claims/` must show admit-all **failing** `clean` (not merely printing BENIGN lines) to prove the classification landed correctly.
- Stage-2 amendment has not happened; `<P><H><S><B><M>` unbound — cannot re-run the predicate (correctly impossible at this stage).
- Mutant battery quality is unverifiable until `c1-mutants.json` lands with per-mutant payload+digest+description.
- No external sources opened; no URL/quote obligations incurred (all evidence is committed lane bytes).

## 7. Limits

No counter/probe execution (correct — nothing scored exists yet); review is of frozen text + committed counter chain at REV `9d2900af…`; F4's pin-gap severity depends on the unwritten v3 `pin_issues` scope.

## VERDICT

**R49-C1 remains falsifiable and causally separable under the frozen kill rule including the MUTANTS floor — PASS, with conditions.** No claim widening detected; no C2 artifact dependence beyond the shared read-only digest-pinned `plans/order_check.py` (F3). Conditions before scoring: stage-2 must (a) implement BENIGN-ADMIT as non-clean and fold it into `contradicted` — else the frozen admit-all control is unsatisfiable (F1); (b) define `<M>/2` integer semantics and record per-mutant kill evidence; prefer a hard bound on trivial/equivalent mutants (F2); (c) pin every `honest49` module digest including wave-1 novels and validate each novel class is truly admissible under the mount-boundary rule (F4). Findings are stage-2 resolvable; none requires re-freezing a predicate line.

Scratch: `/fast/scratch/hyaku/kengaku-r49/R49C1RevClaim` (TMPDIR); only one file written (`r46c1.py` read copy); removed before yield.
