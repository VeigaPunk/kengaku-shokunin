# C1MutClassifier — wave 3 (round 53) mutation test of the frozen classifier

Seat: `C1MutClassifier` (mutation-tester, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Lane HEAD at the time of the run: **`9ead4476bf55b1ea6490d0204b668195db4a4d1d`** (the lane advanced from the build-time tip
`b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` while this seat worked; a fresh `git clone --shared` was taken at
`9ead4476` and every measurement below was made on that clone).
Target: `plans/round53_c1_classify.py`, sha256
`935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` — identical at `9ead4476` and at the build-time tip
(`git log -- plans/round53_c1_classify.py` → one entry, `d40b7055`).

**This seat does not admit or reject R53-C1.** It reports which of the frozen instruments kill which mutants and where the
frozen test suites are silent. The classifier file was never edited in place; every mutant is a copy under the seat's
scratch directory.

---

## 1. Result

**42 single-edit mutants** of the frozen classifier, across 15 behaviour families, scored against three detectors.

| | count |
|---|--:|
| mutants built | 42 |
| **killed by at least one detector** | **20 (47.6 %)** |
| **survive all three detectors** | **22 (52.4 %)** |
| survivors that are *provably equivalent* (no source can separate them) | 2 (M05, M23) |
| survivors with a **concrete witness** source on which the mutant and the pristine disagree | 20 |
| mutants that break the counter's own ORACLE leg | 4 (M08, M32, M34, M36) |
| mutants that move the population class of the 305 ids | 6 (M08, M20, M26, M32, M34, M36) |
| mutants the classifier's own `--selftest` kills (D1) | 17 |
| mutants the 90-case adversarial set kills (D2) | 16 |
| mutants the population-class check kills (D3) | 6 |

**Headline findings.**

- **F1 — the ORACLE leg is not a class-level detector.** The counter's ORACLE leg tolerates up to `0.03 × 305 = 9.2`
  disagreements. Mutants M20 (1 id moves) and M26 (2 ids move) change the population class and are still *inside* the
  leg's budget, so the counter's ORACLE leg prints `pass` for them. Only a class-level detector (D3) sees them.
- **F2 — the frozen classifier selftest (83 cases) and the adversarial set (90 cases / 371 tests) together kill 20 of 42
  mutants.** Twenty-two defect sites in the classifier have no case in either suite that distinguishes them from the
  pristine; of those twenty-two, **20 have a one-to-five-line witness program that does** (all twenty witnesses are in
  `survivors.md`) and 2 are provably equivalent (M05, M23 — see F4). Twelve of the twenty witnesses move the *class*,
  not merely the reason text.
- **F3 — three mutated sites are never reached by any of the three corpora; the other nineteen are reached but their
  effect is invisible on this corpus.** The line-hit probe shows `site_hits = 0` for exactly **M01, M02 and M03** — the
  three `join()` lattice cases `{K,N}`, `{K,L}/{N,L}`, `{B,Q}`. `join()` is called 4262 times over the three corpora and
  never with those pairs (`join-pairs.json`), so no case in the frozen 83-case selftest, the 90-case adversarial set, or
  the 305-id population can distinguish a broken lattice from a correct one.
  The other nineteen survivors have their mutated line execute 1 to 2852 times, yet the classifier's output is unchanged
  on every corpus case. The mechanism differs per family and was checked individually: an earlier branch in the same
  `elif` chain shadows the mutation (M05: `is_bool_const()` is tested first); the mutated condition is never true on
  this corpus (M04: `join_all()` *is* called with an empty list 100 times, but always from `call_func` on a helper with
  no `return`, whose result is never asserted on; M19: the break guard is never a non-path kind here); or the class
  verdict is unchanged although the reason text changes (M10, M13, M14, M18, M21, M25, M38, M39).
- **F4 — two mutants are provably equivalent, not coverage gaps.** M05 (`is_num_const` accepting a bool) is unreachable
  because `assign_name()` tests `is_bool_const()` first in the same `elif` chain; M23 (decorators treated as body) is
  unreachable because `exec_stmts()` dispatches on the statement type and `Run` has no `s_Call` handler, so a decorator
  expression in the body list is silently ignored.
- **F5 — the counter's FREEZE leg is closed against wave-1's F1.** Re-measured: a joint edit of the classifier *and* its
  recorded digest in a later commit now prints `classifier_and_freeze_one_commit=NO labels_after_freeze_and_untouched=NO`
  and `PREDICATE R53-C1 fail`. A1 closed it.
- **F6 — the counter's own `--selftest` does not kill a widened CONFIRM span.** `end_lineno + 1` and `lineno + 1`
  mutations of `span = norm("\n".join(src[t["lineno"] - 1:t["end_lineno"]]))` both leave the counter's selftest at
  `cases=47 failures=0`; `end_lineno - 1` is killed (23 failures). The widening is the dangerous direction. It could not
  be turned into a live real-tree attack on this corpus (see §5), so it is reported as a coverage finding, not a landing.

---

## 2. The pristine classifier, re-run (required)

```
$ python3 lane/plans/round53_c1_classify.py --selftest
cases=83 failures=0
exit=0
```
(the pristine `--selftest` prints only the summary line; `failures=0` is the whole tail)

Adversarial set, pristine:

```
$ python3 lane/.ufo/waves/round-53/w1/C1ExecAdvCases/check.py lane/plans/round53_c1_classify.py -q
CLAUSE cl1      cases=8 case_fail=0 tests=23 test_fail=0
CLAUSE cl2      cases=16 case_fail=0 tests=100 test_fail=0
CLAUSE cl2n     cases=2 case_fail=0 tests=16 test_fail=0
CLAUSE cl3      cases=5 case_fail=0 tests=42 test_fail=0
CLAUSE cls      cases=6 case_fail=0 tests=20 test_fail=0
CLAUSE code     cases=4 case_fail=0 tests=16 test_fail=0
CLAUSE ex       cases=9 case_fail=0 tests=16 test_fail=0
CLAUSE fail     cases=4 case_fail=0 tests=17 test_fail=0
CLAUSE reach    cases=19 case_fail=0 tests=59 test_fail=0
CLAUSE struct   cases=7 case_fail=0 tests=17 test_fail=0
CLAUSE u        cases=4 case_fail=0 tests=14 test_fail=0
CLAUSE unittest cases=6 case_fail=0 tests=31 test_fail=0
TOTAL cases=90 case_fail=0 tests=371 test_fail=0
AMBIGUOUS follows_A=29 follows_B=17 of 47
```

Population at the pristine classifier: **305 ids, 0 unclassified, P1=52, P0=253**, and the counter's own ORACLE leg
against the pristine classifier prints exactly the landed receipt:

```
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52
unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
```

---

## 3. The kill matrix

Full table with all 42 rows, all columns and every witness:
`.ufo/waves/round-53/w3/C1MutClassifier/kill-matrix.md` (machine-readable: `kill-matrix.json`).
Every survivor with the case that should have killed it: `.ufo/waves/round-53/w3/C1MutClassifier/survivors.md`.

### 3.1 Detectors

| id | what it runs | kill condition |
|---|---|---|
| **D1** | `python3 <mutant> --selftest` (the classifier's own 83 frozen cases) | `failures != 0` or the run raises |
| **D2** | `python3 .ufo/waves/round-53/w1/C1ExecAdvCases/check.py <mutant>` (90 cases / 371 tests) | `case_fail != 0` or the run raises |
| **D3** | the mutant's class for each of the 305 `corpus/evidence/round53/tests-index.json` ids | any id's P1/P0 class moves |

D3 reads the capture bytes from a scratch copy of `corpus/evidence/round52/graders`; the copy was sha256-verified
byte-identical to the lane's 185 files before use (`files 185 bad 0`).

### 3.2 The matrix (abbreviated — the full table is in `kill-matrix.md`)

`K` = killed, `s` = survived. `moved` = population ids whose class moves. `disagree` = the counter's ORACLE-leg
disagreement count. `site hits` = executions of the mutated line over the three corpora.

| mutant | family | D1 | D2 | D3 | moved | disagree | ORACLE leg | site hits |
|---|---|---|---|---|--:|--:|---|--:|
| `M06-request-param-to-X` | constant check | K | K | s | 0 | 0 | pass | 2 |
| `M07-boolop-drop-B-branch` | join lattice | s | K | s | 0 | 0 | pass | 61 |
| `M08-existq-B-to-K` | existence query | K | K | K | 10 | 10 | **break** | 331 |
| `M09-listq-drop-scandir` | listing query | s | K | s | 0 | 0 | pass | 44 |
| `M11-const-cmp-in-assert-allowed` | assertion | K | K | s | 0 | 0 | pass | 37 |
| `M12-record-assert-constant-ok` | assertion | s | K | s | 0 | 0 | pass | 22 |
| `M15-open-write-modes-drop-w` | write vs read | K | K | s | 0 | 0 | pass | 417 |
| `M16-all-over-listing-allowed` | universality | K | s | s | 0 | 0 | pass | 1 |
| `M17-try-handler-never-path-state` | control flow | K | K | s | 0 | 0 | pass | 354 |
| `M20-no-assertion-reason-dropped` | assertion | K | K | K | 1 | 1 | pass | 31 |
| `M26-subscript-pick-is-listing` | subscript | K | s | K | 2 | 2 | pass | 9 |
| `M27-assert-context-flag-off` | assertion | K | K | s | 0 | 0 | pass | 3873 |
| `M28-implicit-setup-off` | helper visit | K | s | s | 0 | 0 | pass | 1980 |
| `M30-module-helper-not-registered` | helper visit | K | K | s | 0 | 0 | pass | 2390 |
| `M32-e_Constant-unknown` | constant check | K | K | K | 52 | 52 | **break** | 17366 |
| `M34-exist-q-drop-os-path-exists` | existence query | K | K | K | 10 | 10 | **break** | 5000 |
| `M35-list-m-drop-iterdir` | listing query | K | K | s | 0 | 0 | pass | 840 |
| `M36-pure-q-drop-pathlib` | constant check | K | K | K | 43 | 43 | **break** | 4598 |
| `M37-membership-not-a-predicate` | comparison | K | K | s | 0 | 0 | pass | 18 |
| `M42-tmp-fixtures-dropped` | helper visit | K | s | s | 0 | 0 | pass | 3 |
| `M01-join-KN-to-K` | join lattice | s | s | s | 0 | 0 | pass | **0** |
| `M02-join-KL-to-N` | join lattice | s | s | s | 0 | 0 | pass | **0** |
| `M03-join-BQ-to-B` | join lattice | s | s | s | 0 | 0 | pass | **0** |
| `M04-join_all-empty-to-X` | join lattice | s | s | s | 0 | 0 | pass | 1548 |
| `M05-is_num_const-accepts-bool` | constant check | s | s | s | 0 | 0 | pass | 4 |
| `M10-cmp-count-not-flagged` | comparison | s | s | s | 0 | 0 | pass | 35 |
| `M13-record-assert-unknown-ok` | assertion | s | s | s | 0 | 0 | pass | 2852 |
| `M14-unconditional-fail-ok` | assertion | s | s | s | 0 | 0 | pass | 174 |
| `M18-if-exit-guard-without-exits` | control flow | s | s | s | 0 | 0 | pass | 56 |
| `M19-for-break-guard-any` | control flow | s | s | s | 0 | 0 | pass | 27 |
| `M21-async-fixture-not-scanned` | async vs sync | s | s | s | 0 | 0 | pass | 2486 |
| `M22-async-test-not-a-unit` | async vs sync | s | s | s | 0 | 0 | pass | 1920 |
| `M23-decorators-as-body` | decorators | s | s | s | 0 | 0 | pass | 1980 |
| `M24-parametrize-listing-K` | parametrize | s | s | s | 0 | 0 | pass | 33 |
| `M25-elem-listing-to-K` | element kind | s | s | s | 0 | 0 | pass | 1080 |
| `M29-class-chain-no-inheritance` | helper visit | s | s | s | 0 | 0 | pass | 462 |
| `M31-is_bool_const-any-constant` | constant check | s | s | s | 0 | 0 | pass | 984 |
| `M33-known-k-modules-drop-os` | constant check | s | s | s | 0 | 0 | pass | 101 |
| `M38-write-count-not-a-count` | write vs read | s | s | s | 0 | 0 | pass | 120 |
| `M39-mutate-drops-var` | write vs read | s | s | s | 0 | 0 | pass | 15 |
| `M40-class-attr-self-only` | helper visit | s | s | s | 0 | 0 | pass | 1 |
| `M41-fixture-autouse-dropped` | helper visit | s | s | s | 0 | 0 | pass | 4 |

### 3.3 The counter's own ORACLE leg, per mutant

`plans/round53_c1_triage.py:leg_oracle()` was imported and run **in process** with the classifier redirected to the
mutant — the numbers are the frozen counter's own, not a re-implementation (`counterleg.py`, output
`counter-oracle.json`).

Four mutants break the leg: **M08** (`disagree=10`), **M32** (`disagree=52`), **M34** (`disagree=10`), **M36**
(`disagree=43`) — all `disagree > limit 9.2`.

Two mutants move the population class but **stay inside** the leg's budget: **M20** (`disagree=1`) and **M26**
(`disagree=2`) → the counter's ORACLE leg prints `pass` for both. This is the concrete form of F1.

### 3.4 `join()` lattice — the pairs the classifier actually uses

`join()` is called **4262** times over the three corpora. The pairs actually joined:

| pair | calls | lattice case |
|---|--:|---|
| K+X | 3289 | unmatched → X |
| K+K | 404 | identity |
| X+X | 289 | identity |
| X+K | 156 | unmatched → X |
| K+B | 81 | {K,B} → B |
| N+X | 21 | unmatched → X |
| B+B | 10 | identity |
| B+K | 4 | {K,B} → B |
| N+N | 4 | identity |
| X+B | 2 | unmatched → X |
| C+X | 2 | unmatched → X |

**Never joined: `K+N`, `K+L`, `N+L`, `B+Q`.** M01, M02 and M03 flip exactly those three results, so no case in the
frozen 83-case selftest, the 90-case adversarial set, or the 305-id population can separate them from the pristine. The
witnesses in `survivors.md` are programs *outside* the corpus that do.

---

## 4. Every survivor, with the case that should have killed it

Full text with the witness source and the pristine/mutant outputs: `.ufo/waves/round-53/w3/C1MutClassifier/survivors.md`.
Summary (each witness is a program the pristine and the mutant classify differently):

| mutant | witness (source) | pristine → mutant | kind |
|---|---|---|---|
| `M01-join-KN-to-K` | ternary of a constant and a name picked out of a listing | P1 → P0 | class |
| `M02-join-KL-to-N` | ternary of a constant and a listing, compared to a name | P0 → P1 | class |
| `M03-join-BQ-to-B` | ternary of an existence predicate and a qualified-predicate generator, compared | P0 → P1 | class |
| `M04-join_all-empty-to-X` | a helper whose body returns nothing | P0 → P0, reason list differs | reason |
| `M05-is_num_const-accepts-bool` | **none — provably equivalent** | — | — |
| `M10-cmp-count-not-flagged` | `assert len(os.listdir(D)) == 3` | P0 → P0, reason changes | reason |
| `M13-record-assert-unknown-ok` | an assertion whose only dependency is an unknown value | P0 → P0, reason changes | reason |
| `M14-unconditional-fail-ok` | an unconditional `pytest.fail` | P0 → P0, reason changes | reason |
| `M18-if-exit-guard-without-exits` | `if os.path.exists(OUT): pass` then `pytest.fail` | P0 → **P1** | class |
| `M19-for-break-guard-any` | a `for/else` whose break is guarded by a count comparison | P0 → P0, reason changes | reason |
| `M21-async-fixture-not-scanned` | an async fixture that runs a command | P0 → P0, reason changes | reason |
| `M22-async-test-not-a-unit` | an `async def test_f()` | P1 → **absent** | class |
| `M23-decorators-as-body` | **none — provably equivalent** | — | — |
| `M24-parametrize-listing-K` | a parametrize whose values are a listing, compared to a name | P1 → **P0** | class |
| `M25-elem-listing-to-K` | a loop over a listing whose element is compared to a name | P0 → P0, reason changes | reason |
| `M29-class-chain-no-inheritance` | a test class inheriting a helper from a same-file base class | P1 → **P0** | class |
| `M31-is_bool_const-any-constant` | `n = 0` then `if os.path.exists(OUT): n = 1`, then `assert n` | P0 → **P1** | class |
| `M33-known-k-modules-drop-os` | `x = os` then `if x: assert os.path.exists(OUT)` | P1 → **P0** | class |
| `M38-write-count-not-a-count` | `n = Path(OUT).write_text('x')` then `assert n == 1` | P0 → P0, reason changes | reason |
| `M39-mutate-drops-var` | `x = []` then `x.append(os.listdir(D))` then `assert x` | P1 → **P0** | class |
| `M40-class-attr-self-only` | a class attribute on a base class, read on the subclass | P1 → **P0** | class |
| `M41-fixture-autouse-dropped` | an autouse fixture that runs a command | P0 → **P1** | class |

**The two provably-equivalent survivors, with the proof:**

- **M05** — `assign_name()` reads
  `if is_bool_const(vnode): k = B` / `elif is_num_const(vnode) is not None: k = C`.
  `is_bool_const()` is tested **first**, and it accepts exactly the bool constants that the mutant's loosened
  `is_num_const()` would also accept. The removed `not isinstance(n.value, bool)` guard in `is_num_const()` is therefore
  unreachable. No source can distinguish the two.
- **M23** — the mutant changes `r.exec_stmts(fd.body, fr)` to
  `r.exec_stmts(list(fd.decorator_list) + list(fd.body), fr)`. `exec_stmts()` dispatches each element through
  `stmt()`, which looks up `s_<TypeName>`; a decorator is an `ast.Call` / `ast.Attribute` expression, **not** a statement,
  and `Run` has no `s_Call` handler (`'def s_Call' in source` → `False`). The decorator is therefore silently ignored —
  the mutant is a no-op on every input.

---

## 5. Counter-side probes (the classifier-side matrix cannot answer these)

### 5.1 FREEZE against a committed classifier mutation

On a scratch copy of the lane, with the M08 mutant classifier **committed** (so the tree is clean and the FREEZE leg is
evaluable):

```
FREEZE clean=yes classifier_and_freeze_one_commit=NO classifier_sha=BAD label_files_pinned=ok shards_pinned=ok
labels_after_freeze_and_untouched=NO authors=4
ORACLE not evaluable (pins or freeze failed)
PREDICATE R53-C1 fail
exit=1
```

**A committed classifier mutation is stopped by the FREEZE pin before the ORACLE leg runs.** That is the intended
behaviour and it holds at the A1 counter.

### 5.2 Re-attack of wave-1's finding F1 (joint classifier + digest edit)

Three variants, each committed on its own scratch copy:

| variant | commits touching classifier / freeze file | FREEZE line | outcome |
|---|---|---|---|
| F1a classifier **and** digest edited | 2 / 2 | `classifier_and_freeze_one_commit=NO … labels_after_freeze_and_untouched=NO` | `PREDICATE R53-C1 fail`, exit 1 |
| F1b classifier only | 2 / 1 | `classifier_and_freeze_one_commit=NO classifier_sha=BAD` | `PREDICATE R53-C1 fail`, exit 1 |
| F1c digest only | 1 / 2 | `classifier_and_freeze_one_commit=NO labels_after_freeze_and_untouched=NO` | `PREDICATE R53-C1 fail`, exit 1 |

**Wave-1's F1 is closed by A1.** The joint edit no longer passes FREEZE.

### 5.3 The counter's own `--selftest` against an `end_lineno` off-by-one

The classifier never reads `end_lineno`; the counter's CONFIRM leg does
(`span = norm("\n".join(src[t["lineno"] - 1:t["end_lineno"]]))`). Three mutations of that slice, each on its own copy
of the lane, run through the counter's own selftest:

| variant | counter `--selftest` |
|---|---|
| `end_lineno - 1` (span narrowed) | exit 1, `SELFTEST cases=47 failures=23` — **killed** |
| `end_lineno + 1` (span widened) | exit 0, `SELFTEST cases=47 failures=0` — **survives** |
| `lineno` start shifted by one | exit 0, `SELFTEST cases=47 failures=0` — **survives** |
| pristine | exit 0, `SELFTEST cases=47 failures=0` |

The widening is the dangerous direction and the counter's frozen fixture suite does not detect it. **It could not be
turned into a live attack on this corpus**: I built the real-tree forgery (a `confirmations.json` whose quote is taken
from the line immediately after each test's `end_lineno`) and it produced **0 usable rows** — for all 20 confirmed tasks
the line after `end_lineno` is a blank line shorter than the 20-character quote floor
(`rows=20 forged with a next-line quote=0`). So this is reported as a **coverage finding**, not a landing.

### 5.4 Why the counter's ORACLE leg cannot see a class change

Independently of the mutants, the ORACLE leg's disagreement budget (`0.03 × 305 = 9.2`) means the leg is a *statistical*
detector, not a class-level one. A classifier that misclassifies up to 9 of the 52 P1 tests keeps the leg at `pass`.
M20 and M26 are exactly that case (1 and 2 ids moved, leg still `pass`). The D3 population-class check is the detector
that catches them; it is not part of the frozen predicate.

---

## 6. Commands run

All under `/fast/scratch/hyaku/kengaku-r53/C1MutClassifier/` (TMPDIR set explicitly; scratch removed at exit).

```sh
# 0. lane clone (must print the scratch path)
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane rev-parse --show-toplevel      # -> /fast/scratch/hyaku/kengaku-r53/C1MutClassifier/lane
git -C lane rev-parse HEAD                  # -> 9ead4476bf55b1ea6490d0204b668195db4a4d1d
sha256sum lane/plans/round53_c1_classify.py # -> 935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6

# 1. capture bytes into scratch, then verify byte-identity with the lane
cp -r /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/. capture/
python3 - <<'EOF'   # sha256 every file of both trees
...                 # -> files 185 bad 0
EOF

# 2. build the 42 mutants (each replacement asserted to occur exactly once; each file re-parsed)
python3 mutate.py build            # -> built 42 mutants + pristine

# 3. the kill matrix (D1 selftest, D2 adversarial set, D3 population class)
python3 mutate.py run              # -> 42 rows, kill matrix, results.json

# 4. reason-level attribution (class + reasons, per case) and the counter's own ORACLE leg
python3 attrib.py                  # -> attribution.json
python3 counterleg.py              # -> counter-oracle.json  (imports leg_oracle(), redirects the classifier)

# 5. reachability: line-hit counts of every mutated site over the three corpora
python3 reach.py                   # -> reachability.json
python3 joinprobe.py               # -> join-pairs.json  (the join() lattice pairs actually used)

# 6. witnesses for the survivors: targeted grid, combinatorial fuzzer, targeted constructions
python3 witness.py                 # -> witnesses.json
python3 fuzz.py                    # -> fuzz-witnesses.json
python3 witness2.py                # -> witnesses2.json

# 7. counter-side probes (scratch copies of the lane; commits only inside those copies)
python3 countermut.py              # -> counter-mutants.json  (FREEZE + end_lineno off-by-one)
python3 f1probe.py                 # -> f1-probe.json         (F1 re-attack)
python3 spanprobe.py               # -> span-probe.json      (real-tree quote forgery, attempt 1)
python3 spanprobe2.py              # -> span-probe2.json     (real-tree quote forgery, attempt 2)

# 8. merge into the deliverables
python3 matrix.py                  # -> kill-matrix.md / kill-matrix.json / survivors.md
```

---

## 7. Files produced (absolute paths)

Under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1MutClassifier/`:

| file | what it is |
|---|---|
| `kill-matrix.md` | the 42-row kill matrix with every column and the ORACLE-leg table |
| `kill-matrix.json` | the same, machine-readable |
| `survivors.md` | every survivor with the witness source and the pristine/mutant outputs |
| `results.json` | the class-level matrix (D1/D2/D3) as measured |
| `attribution.json` | the reason-level diffs (R1/R2/R3) per mutant, with the first differing case named |
| `counter-oracle.json` | the counter's own ORACLE-leg output per mutant |
| `reachability.json` | line-hit counts and per-case hits for all 42 mutated sites |
| `join-pairs.json` | the `join()` lattice pairs actually used over the three corpora |
| `witnesses.json`, `fuzz-witnesses.json`, `witnesses2.json` | the witness constructions per survivor |
| `counter-mutants.json`, `f1-probe.json` | the counter-side probe receipts |
| `spanprobe-receipt.txt`, `spanprobe2-receipt.txt` | the two real-tree CONFIRM-span forgery attempts (both negative, 0 usable rows) |
| `mutants-manifest.json` | the 42 mutants with family and note |
| `mutants/` | the 42 mutant sources + `pristine.py` |
| `mutate.py`, `attrib.py`, `reach.py`, `fuzz.py`, `witness.py`, `witness2.py`, `counterleg.py`, `matrix.py`, `joinprobe.py`, `countermut.py`, `f1probe.py`, `spanprobe.py`, `spanprobe2.py` | the harness (re-runnable) |

This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1MutClassifier.md`.

---

## 8. Scope, blindness, writes

- **Writes**: only the seat directory above, plus scratch under
  `/fast/scratch/hyaku/kengaku-r53/C1MutClassifier/` (removed before yield). The lane tree was never edited: the
  classifier file was copied into scratch and the mutants were written there; `sha256sum` of the lane's
  `plans/round53_c1_classify.py` is `935db122…` before and after this seat. The only commits anywhere were inside the
  throw-away scratch copies of the lane used for the counter-side probes (§5); the lane itself was never committed to,
  and no `git commit/add/push/stash/checkout/reset/pull` was run against it or against the fleet repo.
- **Read**: the claims file, the facts file, `plans/round53_c1_classify.py`, `plans/round53_c1_triage.py`,
  `.ufo/waves/round-53/w1/C1ExecAdvCases/{check.py,cases.json}`, the eight label seats' `labels.json` and the eight
  shard files (needed to recompute the ORACLE leg's `decided` set), `corpus/evidence/round53/tests-index.json`,
  `corpus/evidence/round53/confirmations.json`, `corpus/evidence/round52/graders/**`, and the wave-1 reports of
  `C1ExecClassifier` and `C1MutCounter`. I did **not** open any `C1ConfRead*` report or any wave-2 confirmation file.
- **Tools**: none installed or upgraded. Only the Python 3 standard library (`ast`, `importlib`, `subprocess`,
  `json`, `sys.settrace`) was used.
- **Tooling note (as required by the report contract):**
  `tool: read` — the `read` tool elided large regions of `plans/round53_c1_classify.py` ("…1489ln elided…"); the full
  source was re-read with `:raw` line-range selectors, and every mutation target was asserted to occur **exactly once**
  in the pristine source by the builder before a mutant was written.

## 9. What the L1 should take from this

1. **The frozen classifier suites are not a safety net for the classifier.** 22 of 42 single-edit mutants survive both
   the 83-case selftest and the 90-case adversarial set, and 20 of them have a one-to-five-line witness that separates
   them from the pristine. If the round wants the classifier's own tests to be a defence, the twenty witnesses in
   `survivors.md` are the ready-made cases; the highest-value additions are the twelve whose witness moves the **class**
   rather than only the reason text — **M01, M02, M03, M18, M22, M24, M29, M31, M33, M39, M40, M41** (each ≤ 6 lines).
2. **The ORACLE leg is a statistical detector, not a class-level one.** It tolerates 9 misclassifications of 52. A
   class-level check on the 305 ids (D3) is what catches M20 and M26; the frozen predicate has no such leg.
3. **Wave-1's F1 is closed** against the A1 counter — the joint classifier+digest edit now fails FREEZE.
4. **The counter's CONFIRM-span selftest is asymmetric**: narrowing the span is killed, widening it is not. It could not
   be landed on this corpus (the line after every confirmed test is blank), but a future corpus with a non-blank
   following line would be exposed. That is a gap in the counter's fixture suite, not in the classifier.

**Nothing in this report changes the contract, and no claim is admitted or rejected here.**
