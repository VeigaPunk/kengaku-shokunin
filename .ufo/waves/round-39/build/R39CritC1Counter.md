# R39CritC1Counter — attacking `plans/round39_c1_verify.py` (critic, round 39 wave 1)

Seat: critic. Target: the frozen C1 counter `plans/round39_c1_verify.py` (digest pinned at
`ea638822…` for the gate; counter frozen at `088f7c3`). Clone:
`/fast/scratch/hyaku/kengaku-r39/R39CritC1Counter/lane` (`git rev-parse --show-toplevel` verified before
every write). Attack modules and run logs: this directory. Nothing in the lane's `plans/`, `corpus/` or
top-level files was touched outside the clone.

## Axes named before the work

1. **Calibration credit** — does a printed `MUTANTS total=7 killed=7` prove seven demonstrated behaviours?
2. **Instrument soundness** — is each line of the receipt (PINS, BATTERY, null_detected) a measurement that
   holds for the run it is printed in?
3. **Attackability under the round's own write surface** — is a false pass reachable from `plans/battery39/`
   alone (an executor's legitimate surface), or only from a frozen tree?
4. **Input closure** — are the 26 pins exactly the inputs read?

Every run is one command, ~22–25 s:

```
cd <clone> && python3 plans/round39_c1_verify.py --lane . --work <scratch>/w
```

## 0. Baseline reproduction (the frozen do-nothing control)

`run-baseline.txt` — `PINS total=26 mismatched=0`, `BATTERY fixtures=86 wrong=0 renamed_disagree=0
sidechannel=0`, `MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0`, `PREDICATE C1 fail`,
exit 1. Byte-for-byte the same four lines as `.ufo/waves/round-39/claims/control-c1-nothing.txt`
(killed by `d5m-n21-manifest-row-2`, `p23-p2-receipt-deleted`, `r36-P0`; survivors M02, M03, M04, M07).
After every attack below the clone was restored and `run-clean-restore.txt` prints `killed=3` again, so
each result is attributable to its module.

## 1. Result table (six attacks, one MUTANTS line each)

| # | Attack | Reachable from | Observed terminal line | Verdict |
|---|---|---|---|---|
| A1 | post-`null` `--spec` flip (4 fixtures) | `plans/battery39/` only | `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0` + `PREDICATE C1 pass`, exit 0 | **counterexample** |
| A6 | A1 with the flip moved one phase earlier (`gates/null.py`) | `plans/battery39/` only | `killed=7 … null_detected=4` + `PREDICATE C1 fail` | control (caught) |
| A3 | `run_gate` patch from an unpinned tenth `plans/battery37/*.py` | `plans/battery37/` | `PINS total=26 mismatched=0` / `BATTERY fixtures=88 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0` / `PREDICATE C1 pass`, exit 0 | **counterexample** |
| A4 | build child rewrites two pinned lane files after the PINS line | `plans/battery39/` only | `PINS total=26 mismatched=0 … PREDICATE C1 pass`, exit 0, while `sha256sum` shows both files off their pins | **soundness defect** |
| A5 | child authors the parent's fixture table (stdout hijack) and steers `dir` | `plans/battery39/` only | `BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0`, `FIXTURE a5-forged-table-row … ok` | **contract defect** |
| A2 | duplicate `fid` (same module and cross-module) | `plans/battery39/` only | `SETUP duplicate fixture id`, exit 2, after `PINS total=26 mismatched=0` | defended |

Four of six were accepted by the counter; two were stopped (one by design, one by the null control).

## 2. A1 — `killed=7` with zero honest fixtures, from a battery39 module alone (headline)

`crit_a1_flip.py` (this directory) builds four fixtures that are honest about the **reference** run and
about nothing else: each declares exactly the defect set the unmodified gate prints on it as built
(`FIXTURE a1b-… ok` for all four). A daemon started by the module — `subprocess.Popen(...,
start_new_session=True, stdout/stderr=DEVNULL)`, registered in the build child's `atexit` — polls
`<work>/gates/M*.py`, the counter's own mutant-phase marker, and then `os.replace`s each fixture's own
`--spec` with a variant in which that fixture's clause passes.

`run-a1.txt`:

```
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
FIXTURE a1b-p1-second-instrument expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok
FIXTURE a1b-p3-word-bound expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE a1b-p7-two-source-lines expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE a1b-d5-quote-swapped expect=accept declared=- observed_rc=0 observed_defects=- ok
MUTANT M01 D5 mirror killed by=d5m-n21-manifest-row-2
MUTANT M02 P1 silence killed by=a1b-p1-second-instrument
MUTANT M03 P3 silence killed by=a1b-p3-word-bound
MUTANT M04 P7 silence killed by=a1b-p7-two-source-lines
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted
MUTANT M06 MAIN rc-mirror killed by=r36-P0
MUTANT M07 D5 mirror killed by=a1b-d5-quote-swapped
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

exit 0. All four survivors are killed by a fixture whose declared leg is produced by the swap.

**The mechanism, with no mutant in the loop** (standalone run, frozen gate, one fixed tree, two specs):

```
spec-quote-words-3-10.json: rc=1 P1 ok pinned=3 mismatched=0 P3 DEFECT … out_of_word_range=7
spec-frozen.json:           rc=0 P1 ok pinned=3 mismatched=0 P3 ok     … out_of_word_range=0
d5spec-quote-present.json:  rc=0 D5 ok directional=True digest_pinned=True bad=0
d5spec-quote-absent.json:   rc=1 D5 DEFECT directional=False digest_pinned=True bad=['quote absent from the capture']
```

P1/P3/P7/D5 read the spec only (`pkg_gate.py:112` `c_instruments` reads `frozen_instruments`;
`:123` `c_quote_shape` reads `entry_rules.quote_words`; `:211` `c_provenance` iterates `spec["rows"]`;
`:352` the D5 flat compare uses `d5["quote"]`). Nothing about the mutant is involved in either leg.

**Root cause (frozen counter).** `ref[j]` is captured once, for every fixture, before any mutant exists
(`round39_c1_verify.py:313-325`); the mutant loop re-runs the same fixture directory (`:357-368`) and
never re-reads the fixture state or re-runs the reference after the mutant run. `null_detected` (`:340`)
re-runs the *unmutated* gate over all fixtures — but it is executed **before** the mutant loop, so it
brackets only the ref→null window.

**Boundary proof (A6).** The same module with the marker changed to `gates/null.py` (`crit_a6_nullwindow.py`)
gives the same seven kills and `null_detected=4`, `PREDICATE C1 fail` (`run-a6-nullwindow.txt`). So the
null instrument is the right instrument and the flip *is* the cause; it simply does not cover the phase
the kills are scored in.

**Severity.** This is not the named limit "a kill records a result difference in the declared direction, not
the fixture's intent" (`plans/round-39-claims.md:59`). Intent is about what the fixture *means*; here the
mutant's code is not the cause of the measured difference at all — the input changed mid-run. That is a
nondeterminism the counter says it detects.

**Smallest safe correction.** When `exhibits(...)` first returns true for a mutant, re-run the *reference*
gate on that same fixture and require the tuple to still equal `ref[j]`; if it differs, do not count the
kill and print `MUTANT <id> … invalid(nondeterministic fixture)`. Cost: ≤7 extra gate runs per invocation
(one per kill), no change to any other check. Equivalent and equally small: move the `null_gate` run
inside the mutant loop, immediately before each mutant's fixture loop.

## 3. A2 — did the out-of-process build stop the round-38 in-process patch? (no)

Two facts from the frozen files:

* `plans/round39_c1_verify.py:191` (`for f in sorted(bdir.glob("*.py"))`) and `plans/round37_c1_verify.py:262`
  (same glob) mean both battery directories are read as **directory contents**, not as a pinned name set.
* `plans/round37_c1_verify.py:258-267` `battery37_fixtures` does `spec.loader.exec_module(mod)` — **in the
  counter's own process**. Only battery38/battery39 go through `--build-module`.

So a tenth file in `plans/battery37/` is executed inside the counter and is covered by no pin.
`zz_inproc.py` (this directory) does exactly the round-38 move — `sys.modules["__main__"].run_gate =
_forged` — and answers for its two fixtures only (every other fixture falls through to the real gate), so
`wrong`, `renamed_disagree` and `null_detected` all stay 0. `run-a3-inproc.txt`:

```
PINS total=26 mismatched=0
BATTERY fixtures=88 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 D5 mirror killed by=a3z-forged-d5-accept
MUTANT M02 P1 silence killed by=a3z-forged-reject
MUTANT M03 P3 silence killed by=a3z-forged-reject
MUTANT M04 P7 silence killed by=a3z-forged-reject
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted
MUTANT M06 MAIN rc-mirror killed by=r36-P0
MUTANT M07 D5 mirror killed by=a3z-forged-d5-accept
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

exit 0, with no real gate ever run for those two fixtures. Even the docstring's sentence "A module
therefore cannot patch this counter's `run_gate` (round-38 `R38CritClaims` §2)" (`:40-41`) holds for
battery38/39 only; the class it describes is still open one directory to the left, and
`control-c1-hostile-inproc.txt` re-tests only the closed vector.

Two smaller consequences of the same gap: the `SIDECHANNEL` token scan covers battery38/39 sources only, so
a battery37 file also escapes that heuristic; and `PINS total=26` is not a **closed** input set for either
battery directory (drops in, runs, unhashed).

**Smallest safe correction.** (a) Compare the *sets*: `{f.name for f in bdir.glob("*.py")}` against the
pinned names for `plans/battery37` and `plans/battery38` (one line each, counted in `mism`). (b) Load
battery37 the same way battery38/39 are loaded (`--build-module` + JSON), which retires the in-process exec
entirely. (a) closes A3 on its own; (b) closes the class.

## 4. A4 — `PINS mismatched=0` is a one-shot pre-check

`main()` hashes the pins at `:261`, before any battery module runs (`:281`), and never again. The gate
source is read into memory at `:263`, before the children too, and the run's gate copies are written from
that memory at `:309`. `crit_a4_pinwrite.py` (a battery39 build child) appends one line to
`plans/pkg_gate.py` and to `plans/round37_c1_attribution.py`. `run-a4-pinwrite.txt`:

```
PINS total=26 mismatched=0
BATTERY fixtures=93 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

then, in the same clone immediately afterwards:

```
07c6295b07d9cc839cf7b0816922900b7b9c61a06060909642ca652ce7de82b6  plans/pkg_gate.py
70a1e7e678e4dc6b673592f82f41725090df36b410964d4e66420662680f3d40  plans/round37_c1_attribution.py
pins_now_mismatched= ['plans/pkg_gate.py', 'plans/round37_c1_attribution.py']
```

(pins are `ea638822…` and `7064cf1a…`). A *second* invocation of the counter does catch it — but the frozen
predicate is one invocation, so `PINS mismatched=0` in the receipt is compatible with a landing tip whose
gate is no longer the frozen gate. That matters for the C1 kill rule ("any … pin mismatch at landing") and
for C2, which shares the gate digest.

**Smallest safe correction.** Recompute the same `mism` list after the mutant loop and require it empty
before printing `PREDICATE C1 pass` (and print `PINS final total=26 mismatched=0` in the receipt so the
measurement is visible).

## 5. A5 — the fixture table is attacker-authored JSON, and `dir` is trusted

The contract sentence (`:39-41`) says the child "hands back only JSON (fid, expect, defects, argv)". The
child also emits `dir` (`:181-183`), the parent trusts it for `d.is_dir()` (`:293`) and for the
`--spec`-inside-`d` test (`:297`), and then `shutil.copytree(d, nd, …)` (`:332`). `module_fixtures` accepts
the child's output if exactly one line starts with `BUILT ` (`:202`) — and a module can own that line:
`crit_a5_stdout.py` replaces `sys.stdout` at import, so the child's own `BUILT` goes to a sink, and writes
one of its own at `atexit`. `run-a5-stdout.txt`:

```
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
FIXTURE a5-forged-table-row expect=accept declared=- observed_rc=0 observed_defects=- ok
```

accepted, with `dir` = an ancestor of the graded tree and `--root` = a subtree of it. Consequences:
`d` is never confined to `<work>/fx`; `--root` is never required to equal `d`, so a fixture may grade any
tree; and a `dir` of `/` passes validation and is `copytree`-ed — a disk-fill hazard that fails *after*
the copy, not before. (I did not run that variant: `copytree("/")` is destructive on the host. The
validation predicate is read at `:293-297`; no confinement check exists anywhere in `main`.)

**Smallest safe correction.** Require `d.resolve().is_relative_to((root / "fx").resolve())`; require the
resolved `--root` to equal `d`; and take `dir` out of the child's JSON — the parent already knows the
directory it created for fixture *k*, so it should use that and ignore the reported path.

## 6. A2 (duplicate fid) and the rc-leg question — both closed as stated

* Duplicate `fid` (two fixtures in one module, and the same `fid` across modules) → `SETUP duplicate fixture
  id`, exit 2 after `PINS total=26 mismatched=0` (`run-a2.txt`, `run-a2.err`). The check is global over
  `built` (`:302-305`). Only `fid` is deduplicated: two fixtures may still share a directory or a `--root`,
  which no check forbids.
* "A fixture whose declared `expect` disagrees with its intent", for the rc legs: the `wrong` accounting
  (`:316-325`) binds `expect` and `defects` to the **reference** result (`rc == want_rc`, `res[1] ==
  declared`), so `expect` cannot disagree with reference behaviour; `exhibits` for `rc-silence`/`rc-mirror`
  (`:230-237`) then reads only `expect` and the two exit codes. The residual dishonesty is therefore not in
  `expect` but in changing the input between the ref and mutant runs — which is A1.

## 7. Are the 26 pins all inputs the counter reads?

`PINS` = 1 gate + `round37_c1_verify.py` + `round36_c1_verify.py` + `pkg-spec-r35.json` +
`round37_c1_attribution.py` + 9 × `battery37/*.py` + 12 × `battery38/*.py` = 26.

* Read: gate (`:263`), r37 (`:264`), r36 (r37 `load_r36`, `:219-226`), r35 spec (r37 `Ctx.__init__`,
  `:192-196` → `r36.load_spec`), 9 battery37 (r37 `:262` glob), 12 battery38 (`:191` glob). **25 of 26.**
* **Not read: `plans/round37_c1_attribution.py`.** `grep -n "c1_attribution\|ATTRIB" plans/round37_c1_verify.py
  plans/round36_c1_verify.py plans/round39_c1_verify.py` returns only the `PINS` entry (`:76`) and the
  docstring. It is a no-change guard, which is defensible, but the docstring lists it among the 26 pins and
  the claims' "pins 26 inputs" is then one input short of true.
* The set is **not closed**: the two battery globs mean a file added to either directory is executed
  (battery37 in-process) and never hashed (§3). `plans/battery39` is unpinned by design — that is the work
  product — which is why the claims' "battery39 code review by a non-author seat remains part of admission"
  carries the full weight for A1, A4 and A5, and why A3 (a battery37 file) is *outside* even that review.

## 8. What the wave-2 verdict should record

Ranked by what they cost the C1 claim:

1. **A3** — the round-38 in-process class is still open through `plans/battery37/`, and the pin set does not
   notice an added file. A frozen claim sentence ("A module therefore cannot patch this counter's
   `run_gate`", `round39_c1_verify.py:40-42`) is false for that directory. Fixable in ≤4 lines (§3) but
   *the counter is frozen*: this needs an L1 decision — a round-40 re-freeze with the closure, or a recorded
   limit plus a mandated non-author review of every new `plans/battery37`/`battery38` file.
2. **A1** — `killed=7` is reachable from `plans/battery39/` alone with four fixtures that demonstrate
   nothing. Fixable in ≤7 lines (§2), same re-freeze constraint. Until then, a `PREDICATE C1 pass` receipt
   is not sufficient evidence for M02/M03/M04/M07; the accepting fixtures' *build code* must be read and
   must show no state that changes between phases (which is a reviewable property, unlike intent).
3. **A4** — `PINS mismatched=0` does not hold for the run in which it is printed. Fix: one re-hash before
   the predicate.
4. **A5** — `dir`/`--root` trust and the `copytree` hazard. Not a kill by itself; a robustness and
   confinement defect, and a truth-of-docstring defect.
5. Pin audit: 25/26 read; the set is not closed (§7).

**No axis is improved by any of these attacks**: they attack calibration, and the only moves I recommend are
the four smallest corrections above. If the L1 accepts `killed=7` on a battery39 whose builds contain no
cross-phase state change, A1/A4/A5 are neutralised by review; A3 is not, because it is outside the
battery39 surface and outside the pin set.

## 9. Limits of this review

* All runs are on a shared clone of the landing tip in this guest, host python; the counter's own 900 s
  child timeout and 22–25 s wall time were never near.
* A1/A6 depend on the daemon winning a race against the counter's phase transition. Observed on every one
  of the four runs that used it (A1 twice, A6, and A4's combined run); the marker is the counter's own
  `gates/*.py` file, so the race window is a full mutant's fixture loop (seconds), not microseconds.
* I did not run `dir="/"` (destructive `copytree`) — that claim is read from `:293-297` and `:332`, not
  measured.
* I did not test daemons against `PINS`, `ref_digest` (`:369`) or the `--only`/`--battery-dir` dev flags;
  the dev-flag path prints `PREDICATE C1 n/a` and cannot be mistaken for the frozen predicate.
* Tool installs: none. Scratch removed after the report was written.

## 10. Artifacts (this directory)

`crit_a1_flip.py` (A1), `crit_a6_nullwindow.py` (A6), `zz_inproc.py` (A3, goes to `plans/battery37/`),
`crit_a4_pinwrite.py` (A4), `crit_a5_stdout.py` (A5), and the raw logs `run-baseline.txt`, `run-a1.txt`,
`run-a2.txt`/`.err`, `run-a3-inproc.txt`, `run-a4-pinwrite.txt`, `run-a5-stdout.txt`,
`run-a6-nullwindow.txt`, `run-clean-restore.txt`. Each is replayed by placing the module in the stated
directory of a clean clone and running the one command in §0.

VERDICT: c1-counter-attacks-4/6
