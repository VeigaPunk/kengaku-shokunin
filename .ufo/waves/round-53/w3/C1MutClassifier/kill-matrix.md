# C1MutClassifier — kill matrix (42 single-edit mutants of the frozen classifier)

Target: `plans/round53_c1_classify.py` sha256 `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` (copy in scratch; the lane file was never edited).

Detectors:

- **D1** — the classifier's own `--selftest` (83 frozen cases), killed when `failures != 0` or the run raises.
- **D2** — `python3 .ufo/waves/round-53/w1/C1ExecAdvCases/check.py <mutant>` (90 adversarial cases / 371 tests), killed when `case_fail != 0` or the run raises.
- **D3** — the population class of the 305 `corpus/evidence/round53/tests-index.json` ids, killed when any id's P1/P0 class moves (capture bytes read from a scratch copy of `corpus/evidence/round52/graders`, sha256-verified identical to the lane's 185 files).

Reason-level columns (R1/R2/R3) count cases where the mutant's `classify_detail()` **reasons** differ from the pristine's, even when the class does not move — the class verdict is what the claim is scored on, but the reason text is what the reports quote.

`site_hits` is the number of times the mutated line executes over the union of the three corpora (measured by `sys.settrace` on the pristine classifier). A `site_hits` of 0 means the corpus never reaches the mutated code: that is a **coverage gap** of the frozen suites, not a dead branch — every such mutant still has a witness source (a program outside the corpus) on which the mutant and the pristine disagree.

Two survivors are **provably equivalent** (no source can separate them, because the mutated code is unreachable by construction): M05 and M23 — see `survivors.md`.

**Totals: 20 of 42 mutants killed by at least one detector; 22 survive all three.**

| mutant | family | D1 | D2 | D3 | moved | disagree | oracle leg | R1 | R2 | R3 | site hits |
|---|---|---|---|---|--:|--:|---|--:|--:|--:|--:|
| `M06-request-param-to-X` | constant / known-value check | K | K | s | 0 | 0 | ok | 1 | 1 | 0 | 2 |
| `M07-boolop-drop-B-branch` | join lattice | s | K | s | 0 | 0 | ok | 0 | 1 | 0 | 61 |
| `M08-existq-B-to-K` | existence query | K | K | K | 10 | 10 | break | 19 | 41 | 26 | 331 |
| `M09-listq-drop-scandir` | listing query | s | K | s | 0 | 0 | ok | 0 | 1 | 0 | 44 |
| `M11-const-cmp-in-assert-allowed` | assertion | K | K | s | 0 | 0 | ok | 2 | 6 | 3 | 37 |
| `M12-record-assert-constant-ok` | assertion | s | K | s | 0 | 0 | ok | 0 | 1 | 4 | 22 |
| `M15-open-write-modes-drop-w` | write vs read | K | K | s | 0 | 0 | ok | 1 | 1 | 3 | 417 |
| `M16-all-over-listing-allowed` | universality | K | s | s | 0 | 0 | ok | 1 | 0 | 0 | 1 |
| `M17-try-handler-never-path-state` | control flow | K | K | s | 0 | 0 | ok | 1 | 1 | 1 | 354 |
| `M20-no-assertion-reason-dropped` | assertion | K | K | K | 1 | 1 | ok | 2 | 10 | 1 | 31 |
| `M26-subscript-pick-is-listing` | subscript | K | s | K | 2 | 2 | ok | 1 | 0 | 2 | 9 |
| `M27-assert-context-flag-off` | assertion | K | K | s | 0 | 0 | ok | 2 | 6 | 3 | 3873 |
| `M28-implicit-setup-off` | helper visit | K | s | s | 0 | 0 | ok | 2 | 0 | 4 | 1980 |
| `M30-module-helper-not-registered` | helper visit | K | K | s | 0 | 0 | ok | 6 | 19 | 60 | 2390 |
| `M32-e_Constant-unknown` | constant / known-value check | K | K | K | 52 | 52 | break | 72 | 87 | 220 | 17366 |
| `M34-exist-q-drop-os-path-exists` | existence query | K | K | K | 10 | 10 | break | 22 | 40 | 30 | 5000 |
| `M35-list-m-drop-iterdir` | listing query | K | K | s | 0 | 0 | ok | 6 | 3 | 3 | 840 |
| `M36-pure-q-drop-pathlib` | constant / known-value check | K | K | K | 43 | 43 | break | 33 | 79 | 159 | 4598 |
| `M37-membership-not-a-predicate` | comparison | K | K | s | 0 | 0 | ok | 3 | 3 | 0 | 18 |
| `M42-tmp-fixtures-dropped` | helper visit | K | s | s | 0 | 0 | ok | 1 | 0 | 0 | 3 |
| `M01-join-KN-to-K` | join lattice | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 0 |
| `M02-join-KL-to-N` | join lattice | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 0 |
| `M03-join-BQ-to-B` | join lattice | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 0 |
| `M04-join_all-empty-to-X` | join lattice | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 1548 |
| `M05-is_num_const-accepts-bool` | constant / known-value check | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 4 |
| `M10-cmp-count-not-flagged` | comparison | s | s | s | 0 | 0 | ok | 7 | 6 | 4 | 35 |
| `M13-record-assert-unknown-ok` | assertion | s | s | s | 0 | 0 | ok | 26 | 52 | 229 | 2852 |
| `M14-unconditional-fail-ok` | assertion | s | s | s | 0 | 0 | ok | 2 | 2 | 29 | 174 |
| `M18-if-exit-guard-without-exits` | control flow | s | s | s | 0 | 0 | ok | 0 | 0 | 5 | 56 |
| `M19-for-break-guard-any` | control flow | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 27 |
| `M21-async-fixture-not-scanned` | async vs sync | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 2486 |
| `M22-async-test-not-a-unit` | async vs sync | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 1920 |
| `M23-decorators-as-body` | decorators | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 1980 |
| `M24-parametrize-listing-K` | parametrize | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 33 |
| `M25-elem-listing-to-K` | element kind | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 1080 |
| `M29-class-chain-no-inheritance` | helper visit | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 462 |
| `M31-is_bool_const-any-constant` | constant / known-value check | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 984 |
| `M33-known-k-modules-drop-os` | constant / known-value check | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 101 |
| `M38-write-count-not-a-count` | write vs read | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 120 |
| `M39-mutate-drops-var` | write vs read | s | s | s | 0 | 0 | ok | 0 | 0 | 1 | 15 |
| `M40-class-attr-self-only` | helper visit | s | s | s | 0 | 0 | ok | 0 | 0 | 0 | 1 |
| `M41-fixture-autouse-dropped` | helper visit | s | s | s | 0 | 0 | ok | 0 | 0 | 4 | 4 |

`K` = killed by that detector, `s` = survived it.

## The counter's own ORACLE leg, run per mutant

`plans/round53_c1_triage.py:leg_oracle()` was imported and run in-process with the classifier redirected to each mutant — the numbers are the frozen counter's, not a re-implementation.

| mutant | counter ORACLE leg | disagree | limit |
|---|---|--:|--:|
| `M06-request-param-to-X` | pass | 0 | 9.2 |
| `M07-boolop-drop-B-branch` | pass | 0 | 9.2 |
| `M08-existq-B-to-K` | FAIL | 10 | 9.2 |
| `M09-listq-drop-scandir` | pass | 0 | 9.2 |
| `M11-const-cmp-in-assert-allowed` | pass | 0 | 9.2 |
| `M12-record-assert-constant-ok` | pass | 0 | 9.2 |
| `M15-open-write-modes-drop-w` | pass | 0 | 9.2 |
| `M16-all-over-listing-allowed` | pass | 0 | 9.2 |
| `M17-try-handler-never-path-state` | pass | 0 | 9.2 |
| `M20-no-assertion-reason-dropped` | pass | 1 | 9.2 |
| `M26-subscript-pick-is-listing` | pass | 2 | 9.2 |
| `M27-assert-context-flag-off` | pass | 0 | 9.2 |
| `M28-implicit-setup-off` | pass | 0 | 9.2 |
| `M30-module-helper-not-registered` | pass | 0 | 9.2 |
| `M32-e_Constant-unknown` | FAIL | 52 | 9.2 |
| `M34-exist-q-drop-os-path-exists` | FAIL | 10 | 9.2 |
| `M35-list-m-drop-iterdir` | pass | 0 | 9.2 |
| `M36-pure-q-drop-pathlib` | FAIL | 43 | 9.2 |
| `M37-membership-not-a-predicate` | pass | 0 | 9.2 |
| `M42-tmp-fixtures-dropped` | pass | 0 | 9.2 |
| `M01-join-KN-to-K` | pass | 0 | 9.2 |
| `M02-join-KL-to-N` | pass | 0 | 9.2 |
| `M03-join-BQ-to-B` | pass | 0 | 9.2 |
| `M04-join_all-empty-to-X` | pass | 0 | 9.2 |
| `M05-is_num_const-accepts-bool` | pass | 0 | 9.2 |
| `M10-cmp-count-not-flagged` | pass | 0 | 9.2 |
| `M13-record-assert-unknown-ok` | pass | 0 | 9.2 |
| `M14-unconditional-fail-ok` | pass | 0 | 9.2 |
| `M18-if-exit-guard-without-exits` | pass | 0 | 9.2 |
| `M19-for-break-guard-any` | pass | 0 | 9.2 |
| `M21-async-fixture-not-scanned` | pass | 0 | 9.2 |
| `M22-async-test-not-a-unit` | pass | 0 | 9.2 |
| `M23-decorators-as-body` | pass | 0 | 9.2 |
| `M24-parametrize-listing-K` | pass | 0 | 9.2 |
| `M25-elem-listing-to-K` | pass | 0 | 9.2 |
| `M29-class-chain-no-inheritance` | pass | 0 | 9.2 |
| `M31-is_bool_const-any-constant` | pass | 0 | 9.2 |
| `M33-known-k-modules-drop-os` | pass | 0 | 9.2 |
| `M38-write-count-not-a-count` | pass | 0 | 9.2 |
| `M39-mutate-drops-var` | pass | 0 | 9.2 |
| `M40-class-attr-self-only` | pass | 0 | 9.2 |
| `M41-fixture-autouse-dropped` | pass | 0 | 9.2 |

Four mutants break the ORACLE leg (M08, M32, M34, M36). The leg's disagreement budget is 3 % of 305 decided tests = 9.2, so a mutant that moves 1–9 population classes stays inside the leg.

## join() lattice — the pairs the classifier actually uses

`join()` is called 4262 times over the three corpora. The pairs `K+N, K+L, N+L, B+Q` are never joined, which is why M01/M02/M03 are equivalent mutants on this corpus (each still has a witness outside it — see the survivors table).

- `K+X`: 3289
- `K+K`: 404
- `K+B`: 81
- `B+B`: 10
- `X+K`: 156
- `X+B`: 2
- `B+K`: 4
- `X+X`: 289
- `N+N`: 4
- `C+X`: 2
- `N+X`: 21

