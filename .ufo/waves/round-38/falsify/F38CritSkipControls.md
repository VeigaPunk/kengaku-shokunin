# F38CritSkipControls — skip-controls against the two LANDED round-38 counters

Seat: critic (wave 2, falsify). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip under attack
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (`git -C $S/lane rev-parse HEAD` → that sha). All work in
`/fast/scratch/hyaku/kengaku-r38/F38CritSkipControls/` (deleted at the end); receipts in
`.ufo/waves/round-38/falsify/F38CritSkipControls/`. No lane file was written; every run names an explicit `--lane`.

Baseline reproduced on a clean `--no-local` clone of the tip before any control:

```
$ python3 plans/round38_c2_verify.py --lane .
checks=7 defects=0 / PREDICATE C2 pass                      (receipts: c2-baseline.txt, 1.4 s)
$ python3 plans/round38_c1_verify.py --lane . --work $S
PINS total=14 mismatched=0 / BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0 / PREDICATE C1 fail   (receipts: c1-baseline.txt, 1m7s)
$ python3 plans/mutant_direction_check.py --lane . --work $S
DIR N21 D5 declared=silence observed=mirror MISLABELLED / DIRECTIONS total=22 mislabelled=1
```

So the landing receipt is real: 21 attributable kills, one survivor, C1 reported as an honest stop.

---

## Control (a) — C2 informed filler: **the counter prints the identical receipt**

Attacks: the C2 predicate `checks=7 defects=0` as a measure of "an entry that states what its receipt shows".

Built in a copy of the tip (`$S/c2fill`, same HEAD, one tracked file modified). The genuine entry was reduced to
the four structures the gate and the counter actually parse — the two `source:` lines, `verified-at`, `recheck`
(checked by `pkg_gate.py:211-231`), the 28-row `## Located quotes` table
(verbatim, so P3/P4 pass), the seven derived `## Requirement map` rows (so V7 passes), and `## Negative space`
(so P7 passes) — and every substantive sentence was replaced with claims the receipt contradicts. For example
the filler's summary states:

> "The probe observed `cases=22 observed_pass=22 observed_fail=0 mismatches=0`: every frozen case passes."

plus "`canned-shape` was never executed", "the grader reads a Debian package digest and a build log", "the oracle
`solution/solve.sh` was executed", "the captured `test_outputs.py` does not match S115". The receipt, the probe,
the captures, the spec and SOURCES were **not** touched, which is what makes this an *informed* filler: it reuses
the real receipt, exactly as the seat brief asked.

```
$ git -C $S/c2fill diff --stat
 corpus/knowledge/tb2-build-pmars-grader.md | 271 +-------------------------
 1 file changed, 19 insertions(+), 252 deletions(-)
$ python3 plans/round38_c2_verify.py --lane $S/c2fill
V1 ok … V2 ok (gate_exit=0, P1..P10 all ok) … V7 ok rows=7 tags=7 bad=0
checks=7 defects=0
PREDICATE C2 pass
$ diff c2-baseline.txt c2-filler.txt
IDENTICAL
```

**Result: the counter's output is byte-identical for the true entry and for a false one.** Not merely "green
with a warning" — no observable difference at all.

What let it through is precise, and it is narrower than the claims' own skip-control tests: the frozen
skip-control damaged *structure* (one quote, one teaches word, no coverage bullet, a hand-typed receipt), which
is why it stayed red (`control-c2-skip.txt`: `checks=7 defects=2`, gate `P3/P4/P6/P8/P10 DEFECT`). Nothing in
V1–V7 reads a single sentence of the entry's argument. V4 only requires that `match=NO` cases be named (there
are none: `mismatches_named=0/0`), and V7 only requires that the *table* be derivable. The receipt itself is
genuinely bound — `pkg_gate.py:283` `if r.stdout != want:` fails P10 on any edit — so the counter proves the
receipt and proves nothing about what the entry says over it.

Secondary, same run: `pkg_gate.py:260` uses `git ls-files --others --exclude-standard`, so P9's `clean tree`
sees only untracked files. The filler run printed `gate: P9 ok untracked=0` while
`git -C $S/c2fill status --porcelain` printed ` M corpus/knowledge/tb2-build-pmars-grader.md`. "Measured on a
clean clone of the landing tip" is an operator precondition the counter never checks (no HEAD assertion, no
tracked-modification test).

Smallest safe correction: add one check, **V8** — the entry must carry the receipt's summary line verbatim (and
any `cases=`/`observed_pass=` token it states must equal the receipt's). The receipt summary is already parsed
(`SUMMARY`, `round38_c2_verify.py:65`); the filler above would then fail on `observed_pass=22` versus
`observed_pass=7`. This closes the "false prose over a true receipt" skip without touching any pinned input.
Optionally make P9 use `git status --porcelain` rather than `--others`, so the counter's own stated condition is
enforced rather than assumed.

---

## Control (b) — C1 wrong-clause battery: **the counter holds (red)**

Attacks: the claim that a `battery38` whose fixtures each fire a clause other than the one they aim at can make
`killed=22` appear.

Battery built in `$S/c1wrong`: the twelve landed modules removed, one module with five fixtures, each named after
a mutant of a *different* clause than the clause it fires — `x-p1-aimed-at-N21` (fires P1),
`x-p4-aimed-at-N10` (P4), `x-p6-aimed-at-N13` (P6), `x-p7-aimed-at-N19` (P7), `x-p8-aimed-at-N20` (P8). Every
fixture starts from `ctx.genuine_package(d)`, injects one defect, declares exactly the reference's defect set and
is staged with `ctx.git_add`.

```
$ python3 plans/round38_c1_verify.py --lane $S/c1wrong --work $S
BATTERY fixtures=69 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 P1 silence killed by=x-p1-aimed-at-N21
MUTANT N03 P4 silence killed by=x-p4-aimed-at-N10
MUTANT N02/N04..N22 SURVIVED   (20 lines)
MUTANTS total=22 killed=2 survived=20 invalid=0 null_detected=0
PREDICATE C1 fail
```

**Zero cross-clause kills.** Each of the two kills came from the fixture that fires the mutant's *own* clause
(N01←P1, N03←P4); the four fixtures aimed at N10/N13/N19/N20 killed none of them. This is not luck; the rule
makes it structural (`plans/round38_c1_verify.py:191-204`):

- silence: `clause in ref[1] and clause in declared and clause not in mut[1]` (:202-203) — the fixture's
  reference must print the mutant's clause `DEFECT`, and `declared` must equal `ref[1]` exactly (:199);
- mirror: `clause in ref[2] and clause in mut[1]` (:204) — the clause must be `ok` in the reference, i.e. absent
  from `declared`;
- `RUN` (:200) and `MAIN` (:195) are the only two families whose kill rule is not written in terms of a `P*/D4/D5`
  clause id, and `MAIN` still requires `ref[0] == 2 and mut[0] in (0, 1)`.

A "wrong-clause kill" would need the mutant's clause to flip while the fixture never declared it. That is
unreachable for the 19 P/D mutants.

Two useful by-products of the same run:

1. **The 21 kills are the round-38 work, not inherited.** With `plans/battery38` replaced, the 64 pre-round-38
   fixtures (round-36 + `battery37`) kill **none** of N01–N22: the only kills in the run are the two the control
   battery added. Cross-checked against `measure-final.txt`, every landed kill names a `battery38` fixture of the
   mutant's own clause (`p4a-second-row-line-outside`→N03, `p6m-n10-url-scheme-http`→N10, `d4m-n19-…`→N19,
   `mainx-spec-invalid-json`→N18, …), so the 21 are attributable in the strict sense the claim uses.
2. **The attributed rule reads a mislabelled direction as a battery gap.** N21's `D5` clause is
   `pinned = any(... sums.splitlines())`; the mutant narrows the lookup to `[:1]`, so the mutant's pinned set is a
   *subset* of the reference's: `ref ok ⇒ mut may be DEFECT`, `ref DEFECT ⇒ mut DEFECT`. A silence kill is
   therefore impossible on every input, which is exactly what `plans/mutant_direction_check.py` says in its
   docstring ("Restricting an `any(...)` lookup to a prefix makes the clause STRICTER, never laxer") and what my
   re-run at this tip shows (`DIR N21 … observed=mirror MISLABELLED`). The L1's `21/1` + honest stop is the
   correct report of a **freeze-cell defect**, not of a missing fixture; editing the freeze would have been the
   error, and the lesson row (`corpus/lessons/round-38.md` §Mistakes row 1) is the right repair.

---

## Control (b′) — C1 in-process rewrite: **the counter prints `PREDICATE C1 pass` with a battery that demonstrates nothing**

Attacks: the C1 predicate `killed=22 survived=0 invalid=0 null_detected=0` as a measure of "the battery
demonstrates the advertised behaviours". This is the strongest counterexample I could build cheaply, and it is
within the hostile-battery threat model the lane already names ("battery38 code review by a non-author seat
remains part of admission", `plans/round-38-claims.md` §C1 limits).

`plans/battery38` accepts arbitrary Python; `battery38_fixtures()` `load()`s each module with
`spec_from_file_location` **in the counter's own process**, before any mutant runs (:162-174). `attributed` is
read as a module global at call time (:191). One module therefore suffices:

```python
import sys
FID = "patch-genuine-accept"
def _rewrite_rule():
    main = sys.modules.get("__main__")
    if main is not None and hasattr(main, "attributed"):
        main.attributed = lambda *a, **k: True
_rewrite_rule()
def build(ctx, d):                     # the GENUINE round-35 package: accepted, separates no mutant
    ctx.genuine_package(d); ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]
FIXTURES = [{"fid": FID, "expect": "accept", "defects": [], "build": build}]
```

```
$ python3 plans/round38_c1_verify.py --lane $S/c1patch --work $S
FIXTURE patch-genuine-accept expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 … killed by=r36-P0        MUTANT N02 … killed by=r36-P0        … (all 22)
MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

Every one of the 22 kills is attributed to `r36-P0`, a fixture the reference *accepts* and that therefore
separates no mutant at all; the only non-inherited fixture fires no clause. `wrong=0`, `renamed_disagree=0`,
`null_detected=0`, `sidechannel=0` — the `SIDECHANNEL` scan (`:89`) checks for `/proc`, `ppid`, `cmdline`,
`psutil`, `environ`; `sys.modules["__main__"]` contains none of them, and my first attempt was caught only
because I *named* those tokens in the module docstring (receipt `c1-b2-patch.txt` history; the successful run is
the second one). `PINS` (14 entries, :100) covers the gate, the round-37/36 counters, the round-35 spec and the
nine `battery37` modules — it cannot cover a battery that is the work product.

Scope of this finding, stated carefully: it does **not** falsify the landing receipt, which I reproduced
(21/1). It falsifies the predicate as an *admission test*: `PREDICATE C1 pass` can be produced by a battery that
demonstrates none of the 22 behaviours, so the claim "C1 passes iff [this command prints killed=22]" is not a
sufficient condition, only a necessary one, and the sufficiency rests entirely on review — which the freeze record
does not even identify (no file under `.ufo/waves/round-38/claims/` or `integrate/` names `battery38`; the
measured battery is bound only by the tip commit).

Smallest safe correction (two lines, no pinned input touched): capture the decision function and the mutant list
as locals **before** importing battery modules, and call those — `_rule, _mutants = attributed, MUTANTS` before
`battery38_fixtures(...)`, then `rule(...)` / iterate `_mutants`; plus one guard after the load,
`if attributed is not _rule: print("setup: battery rewrote the kill rule"); return 2`, extended to `run_gate` and
`sha256`. The full fix (fork each `build`) also stops a module from patching the gate runner, but the snapshot
plus identity guard closes the demonstrated control.

---

## What each counter alone proves (ranked)

| | C2 `checks=7 defects=0` | C1 `killed=22 …` |
|---|---|---|
| captures at frozen digests | proves (V1) | – |
| receipt reproduced by a fresh probe run through the real gate | proves (V2/P10, byte compare) | – |
| per-row anchor token bound to its own pin; census valid | proves (V3, V6) | – |
| map label derivable from **all** violating cases | proves (V7) | – |
| each mutation changes the gate's own clause output on some fixture | – | proves **on the landed battery** (reproduced 21/1) |
| fixtures declare exactly the reference's defect set, name-independent, deterministic | – | proves (wrong=0, renamed, null) |
| the entry's claims/findings follow from the receipt | **not proven** — control (a) prints an identical receipt | – |
| the battery demonstrates anything at all | – | **not proven** — control (b′) prints `pass` |
| kill attributable to the *advertised* clause and direction | – | proves (control (b): 0/20 cross-clause) |

C2 is the stronger counter of the two on substance: its receipt cannot be forged (P10 re-executes the probe and
byte-compares), so the `cases=22 observed_pass=7 observed_fail=15` claim is grounded independently of the entry.
Its weakness is exactly one layer out — prose. C1's kill attribution is genuinely clause-tied and direction-tied
and survived the assigned control, but the predicate has no defence against the artifact it is measuring.

## Impacted axes

- **calibration (this round's chosen axis):** the C2 admission rule accepts a false entry that reuses the true
  receipt — the entry-level half of the coverage claim is uncertified. The C1 admission rule is gameable by the
  work product it measures; its *landed* evidence is sound.
- **coverage:** unchanged — V1/V2/V4/V5/V7 still bind the receipt, captures and map; the false-prose skip does not
  touch the `7 pass / 15 fail` finding.
- **freshness:** unchanged — the probe is pinned and re-run.
- **operability:** a one-check fix (V8) and a two-line snapshot fix are both cheap; neither changes a pinned input.

## Files

`c2-baseline.txt`, `c2-filler.txt` (identical), `filler-entry-tb2-build-pmars-grader.md` (the control entry),
`mk_filler.py` (its generator), `c1-baseline.txt`, `c1-b1-wrongclause.txt`, `b1_wrongclause.py`,
`c1-b2-patch.txt`, `b2_patch.py`, `direction-check-tip.txt`.

Verdict token, glossed: **c1-red** = `PREDICATE C1 fail` on the assigned wrong-clause battery (the counter holds;
its in-process bypass is control (b′), reported above, and does not alter the landed 21/1);
**c2-green** = `PREDICATE C2 pass` on the informed filler (the counter accepted it, with identical output).

VERDICT: skip-controls-c1-red-c2-green
