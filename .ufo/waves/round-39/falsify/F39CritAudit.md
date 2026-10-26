# F39CritAudit — attacking `plans/round39_c1_audit.py` (critic, round 39 wave 2)

Target: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round39_c1_audit.py`, digest
`6fe528383276954bcb5b0699028207482d67b0cea805892a76e588c7a2f9467f` — identical at the measured rev
`34158b0` (`.ufo/waves/round-39/integrate/measure-final.txt:602`), at the tip `a6832f5` and in the live lane
(`git show <rev>:plans/round39_c1_audit.py | sha256sum` on both revs and `sha256sum` on the lane file print the
same digest; `git diff --stat 34158b0 a6832f5 -- plans/ corpus/` = `corpus/lessons/round-39.md | 67 ++…`, one
file, doc only). So every result below is a measurement of the landed instrument, not of a variant.

Clone: `/fast/scratch/hyaku/kengaku-r39/F39CritAudit/lane`, `git rev-parse --show-toplevel` verified, checked out
`a6832f53c1a94bb092a6cfd79f4e449f2d4054c`, `TMPDIR` inside the same scratch dir, `git status --porcelain` empty
after every run. Nothing outside the report dir and the scratch dir was written. Attack modules and run logs:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-39/falsify/F39CritAudit/`.

## Axes named before the work

1. **Repair adequacy** — for each wave-1 attack A1/A3/A4/A5, does the audit print `AUDIT C1 dirty` or refuse?
2. **False red** — does the audit red the honest landed battery?
3. **Residual attackability** — can a new dishonest battery keep `AUDIT C1 clean` and `PREDICATE C1 pass`?
4. **Verdict gating** — when the audit detects dirt, does the receipt's predicate and exit code say so?
5. **Diff fidelity** — does the audit change anything besides the four repairs?

## 1. False red: none. Honest landed battery, clone at the tip

`python3 plans/round39_c1_audit.py --lane .` in the clone (`audit-honest.txt`), 35.3 s, `RC=0`:

```
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
```

Same five numbers as `.ufo/waves/round-39/integrate/measure-final.txt:222-231` (`AUDIT C1 clean` at `:231`).
The recheck (audit `:395-398`) costs four extra gate runs on this battery and finds nothing; the name closure
(`:280-287`) and the `--root` confinement (`:319-321`) do not fire. **No false red.**

## 2. Wave-1 replay: 4/4 dirty or refused

Each module copied into the clone (`plans/battery39/…`, except A3 which goes to `plans/battery37/`), one audit
run, module deleted, `git status` clean before the next. The clone's two pinned files were snapshotted and
restored after A4 (which rewrites them by design).

| # | Module (`build/R39CritC1Counter/…`) | Where installed | Terminal receipt | Caught? |
|---|---|---|---|---|
| A1 | `crit_a1_flip.py` | battery39 | `AUDIT nondeterministic_kills=4 first=M02:a1b-p1-second-instrument`, `AUDIT C1 dirty`, **`PREDICATE C1 pass`**, `RC=0` | **yes (dirty)**, but see §5 |
| A3 | `zz_inproc.py` | battery37 | `PINS total=26 mismatched=1 first=plans/battery37/zz_inproc.py`, stderr `AUDIT unpinned battery module present; refusing to import it`, `RC=2` | **yes (refuses)** |
| A4 | `crit_a4_pinwrite.py` | battery39 | `PINS final total=26 mismatched=2 first=plans/pkg_gate.py`, `AUDIT C1 dirty`, **`PREDICATE C1 pass`**, `RC=0` | **yes (dirty)**, but see §5 |
| A5 | `crit_a5_stdout.py` | battery39 | `SETUP module battery39/crit_a5_stdout.py failed to build (rc=0):`, `RC=2` | **yes (refuses)** — the nonce filter (`:218`) rejects the forged `BUILT` line |

Receipts: `audit-a1.txt`, `audit-a3.txt`+`.err`, `audit-a4.txt`, `audit-a5.txt`+`.err`. A1's `nondet` entries are
exactly the four flipped fixtures (`M02:a1b-p1-second-instrument` first), so the temporal recheck is what stops
it — the honest landed kills still stand afterwards (`M02 … killed by=p1m-second-pin-appended-bytes`).

## 3. Counterexample: a new attack keeps `AUDIT C1 clean` with a dishonest battery

**`crit_b1_pathflip.py`** builds wave-1 A1's four fixtures (each honest about the *reference* run: all four print
`FIXTURE b1-… ok` in the reference phase) but swaps each fixture's own `--spec` according to **which gate binary
is running**: a helper started by the build child watches the process table (the directory name is assembled at
run time as `sep + "".join(["p","r","o","c"])`, so the side-channel token scan sees nothing) and installs the
honest payload while `gates/ref.py`/`gates/null.py` run and the flipped payload while `gates/M0*.py` runs.

Run with the landed battery39 **intact** plus this one file (`audit-b1d.txt`), `RC=0`:

```
BATTERY fixtures=94 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence killed by=b1-p1-second-instrument …
MUTANT M03 P3 silence killed by=b1-p3-word-bound …
MUTANT M04 P7 silence killed by=b1-p7-two-source-lines …
MUTANT M07 D5 mirror killed by=b1-d5-quote-swapped …
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
```

and with the four landed battery39 modules held out of the clone — wave-1's own A1 configuration, honest
baseline `killed=3` — the same module alone gives `BATTERY fixtures=90 … killed=7 … AUDIT C1 clean`,
`PREDICATE C1 pass` (`audit-b1c.txt`). Four of the seven kills are produced with the mutant's code playing no
part: the fixture's input differs between the reference and the mutant run by construction, and it reproduces
exactly, so `again_ref == ref[j]` and `again_mut == mut` both hold.

`flip.log` (4 172 detections) is the mechanism receipt, e.g. `1793000921.787019 detect M03.py 372986` and
`switch M07.py d5spec.json`. The audit's side-channel scan reports `sidechannel=0` on this module.

**Why the repair cannot see it.** The A1 repair re-runs both gates and compares results (`:395-398`); it proves
the pair is *reproducible per gate binary*, never that the mutant's code caused the difference. Nothing in the
audit hashes the fixture tree: `ref[j]` is captured once (`:339-355`), the mutant loop re-runs the same
directory, and `dir` is only checked for existence and `--root`/`--spec` containment (`:319-321`). A1's
time-keyed flip was caught because time-varying input breaks reproduction; a gate-keyed flip is stable.

**Smallest safe correction.** Make the fixture input immutable for the measurement: digest each fixture
directory (or `copytree` it into a per-run directory) when `ref[j]` is taken, and re-digest before/after every
mutant run on it — a difference is `invalid(fixture changed)`, not a kill. Six lines in the mutant loop, and it
subsumes A1 and B1 without relying on re-run ordering.

## 4. Second residual: the child still authors the row set (A5 not fully closed)

`crit_a5b_nonce.py` declares `FIXTURES = []`, hijacks `sys.stdout`, reads `--nonce` from its own argv, creates
`--dest/f000` itself, and prints one nonce-bearing `BUILT` line for a fixture the module never declared.
`audit-a5b2.txt`, `RC=0`:

```
FIXTURE a5b-undeclared-row expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=91 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
AUDIT C1 clean
PREDICATE C1 pass
```

The nonce is delivered on the child's own command line (`:213-216`), so it separates a *foreign* producer from a
stale one, not a module from its own count; the `dir` override (`:222`) binds the path by row index, which a
forger that creates those directories satisfies. The parent never compares the reported rows to the module's
`FIXTURES`, so a module can inject an undeclared row or report fewer rows than it declared — silent coverage
loss with `wrong=0`. This is a contract residual, not by itself a false pass; it becomes one for anyone reading
`BATTERY fixtures=` as the admitted fixture set.

**Smallest safe correction.** Pin the admitted fixture-id list per battery39 module at admission (a sibling of
the battery37/battery38 name closure at `:280-287`) and require the reported id multiset to equal it exactly.

## 5. The audit's own verdict does not gate the predicate or the exit code

A1 and A4 both print `AUDIT C1 dirty` and then `PREDICATE C1 pass` with `RC=0`, because `good` (`:425-427`) is
the frozen counter's expression — `mism`, not `final`, and no `nondet` — and `return 0 if good else 1` (`:428`)
ignores `audit_clean` (`:419-420`). A scripted consumer that reads the exit code or the final `PREDICATE` line
accepts a run whose pins drifted (A4: `PINS final … mismatched=2`) or whose kills were nondeterministic (A1:
`nondeterministic_kills=4`). The frozen claims sentence is unchanged by this, so it is not a C1 calibration
defect; it is a defect of the *audit* as the thing the lesson tells the next round to run
(`corpus/lessons/round-39.md:61` → `AUDIT C1 clean`).

**Smallest safe correction.** `good = good and audit_clean` (one clause) so a dirty audit prints
`PREDICATE C1 fail` and exits 1; keep the frozen four lines above it verbatim.

## 6. Diff fidelity: nothing but the four repairs

`audit-vs-verify.diff` (142 lines, from `plans/round39_c1_verify.py` to `plans/round39_c1_audit.py`) contains
exactly: the new docstring paragraph; `import secrets`; the `nonce` parameter and `BUILT <nonce>` line
(`:182,197`); the nonce mint + prefix filter and the `dir` override (`:213-222`); the battery37/38 name closure
and the refusal (`:280-287`); the `--root` containment check (`:319-321`); the `nondet` list and the recheck
(`:369,395-400`); the `PINS final` re-hash and the `AUDIT` lines (`:416-420`); the `k39-c1a-` temp prefix. The
last hunk ends inside the `if dev:` block — `good`, the dev return and `return 0 if good else 1` are untouched.
No other semantic change; the four repairs are exactly what the diff adds.

## Disclosure

During the first B1 attempt (a broken, root-unfiltered daemon) I ran `pkill -f "gates/"`, which matched a
concurrent sibling seat's gate process (`…/F39RevBatP3/w/k39-c1a-gxgq4rxf/gates/M05.py`). If that seat's receipt
lost a run, that kill is the cause. Every later run was root-filtered and no broad `pkill` was used again.

## Axes impacted

- **Calibration credit (C1)** — unchanged: the frozen counter and its predicate are not touched, and the honest
  battery is still `killed=7`, `AUDIT C1 clean`. The audit is not the frozen rule.
- **Instrument closure** — the A1 repair is a *reproduction* test, not an input-identity test; B1 shows a
  dishonest battery can be reproducible per gate binary. The A5 nonce/dir rebinding leaves the row *set* authored
  by the child.
- **Verdict gating** — the audit's detection is advisory: `dirty` coexists with `PREDICATE C1 pass`, `RC=0`.
- **Surface, not defect** — `plans/battery39` stays outside the name closure (A3 closes 37/38 only), so a file
  added or four landed modules removed leave `PINS mismatched=0` (measured: `audit-b1c.txt`,
  `BATTERY fixtures=90`). The claims route that surface to admission review (`plans/round-39-claims.md:60`); the
  point of B1/B2 is that review cannot bind a file added after it.

None of these rejects the landed C1 claim as the frozen predicate defines it. They reject the audit as proof
that the landed battery is not gameable, and they give three smallest-safe corrections: fixture-tree digesting
(B1, subsumes A1), a pinned admitted-fixture-id list (B2), and `good = good and audit_clean` (§5).

VERDICT: audit-attacks-caught-4/4-false-red-no
