# R39DirCheckLeg — a redundant leg for the N21 direction signal (round-39 wave 1, executor)

Seat R39DirCheckLeg, executor. Target: round-38 closure R2 last clause (`corpus/lessons/round-38-verifier-spotcheck.md` §5
R2: "the direction check's mislabel signal has one path (m1, m2 survive) — add a redundant leg before it is load-bearing").
Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip `750473847af9c7a461487ba3a589b5519fac5ed8`
(`git -C lane rev-parse HEAD`), read through a `git clone -q --shared` at
`/fast/scratch/hyaku/kengaku-r39/R39DirCheckLeg/lane` (`rev-parse --show-toplevel` = that path; `status --porcelain | wc -l` → `0`).
No lane file was written: the real lane's `plans/mutant_direction_check.py` is still
`7e0e2b789819cc95cbc0b28bce3ae110d6907f62bd1109f90108e077deaa2c14` (identical to the hash F38MutDirection recorded before and
after its own attack), `plans/round38_c1_verify.py` `8069739990c7d3a87f34f4398ea5dc78821193d9fa55499e11e28c84e79c0a4f`, and
`plans/pkg_gate.py` `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (= the frozen claim's `ea638822…`).

Axes named: **calibration** (the tool must reproduce the landed N21 verdict byte-for-byte on the real input) and
**operability** (a destroyed leg must not turn the run green; a broken invocation must not exit like a detection).

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-39/build/R39DirCheckLeg/mutant_direction_check.py`
— 182 lines, `sha256 e471630abd27da4147c69d3feccdf6e5ad7969a47eae2fa053423636a412b09b`, `python3 -m py_compile` ok,
CLI unchanged (`--lane`, `--counter`, `--work`), drop-in replacement for `plans/mutant_direction_check.py`.
Full source diff: `receipts/diff-old-to-new.patch` (188 lines: 7 hunks, 104 added / 20 removed).

Three edits:

1. **`second_leg(clause, direction, fx, argv, ref, mut)`** — a second derivation of the same witness set, written from
   the raw `(rc, DEFECT set, ok set)` triples, calling **neither** `c.attributed` **nor** any loop the first leg uses and
   naming no `dname`. It carries its own `FAMILY = {"D4": "d4-line", "D5": "d5-line"}` copy.
2. **Verdict merge** — leg 1 (the round-38 path, kept verbatim so a one-line edit to it stays measurable) and leg 2
   decide independently; `MISLABELLED` from **either** leg is the verdict, `ok` only when both say `ok`, and
   `LEGS-DISAGREE` when one leg cannot decide (`ok` vs `UNWITNESSED`) — exit 3, never a pass. A `legs=<a>,<b>` tail is
   appended to the `DIR` line whenever the two legs did not agree.
3. **Closed-failure setup** — a counter that does not expose the round-38 list surface
   (`battery38_fixtures`/`attributed`/`FAMILY`/6-column `MUTANTS`) and a missing/unwritable `--work` parent both exit
   **2** with one `SETUP` line, instead of an `AttributeError` traceback or a `FileNotFoundError` exiting 1 — the code
   that means "mislabel found" (F38MutDirection §4).

Exit codes after the change: `0` all ok · `1` some mutant `MISLABELLED` (QUALITY Q29's sentence "exit 1 iff `m > 0`"
still holds exactly) · `2` setup failure · `3` instrument cannot decide (`INVALID` row `old`-string no longer matches the
gate once, or legs disagree without a mislabel).

## 2. Why merging the *verdict* is the redundancy that matters

F38MutDirection's m1 and m2 both attacked the **observation** path (`for dname in ("silence", "mirror")` and
`if direction in seen:`). A redundant *collection* alone still leaves the final `if direction in seen:` as a single point
of failure — m2 would still flip N21 to `ok`. So the second leg is decided **after** its own independent collection and
the printed verdict is the stronger of the two: mutating one leg changes that leg's vote, and the other leg's
`MISLABELLED` still wins. Both mutants therefore leave the landed N21 line intact (`observed=mirror MISLABELLED`, exit 1),
which is the invariant under attack, and each also leaves a visible fingerprint (`legs=…`, a non-zero `disagree` count) —
so a plain output-diff mutation test catches them too, independently.

## 3. The three F38MutDirection mutants, old vs fixed copy

Copy of the old file and the mutants (each exactly one line from its base) live in the scratch only; the old-m* hashes
reproduce F38MutDirection's table exactly (`16955799…`, `482b5aa4…`, `7b4e2aa6…`), so these are the same mutants, not
lookalikes. Runs:

```
python3 <copy>.py --lane "$S/lane" --work "$S/w-<tag>"        # S=/fast/scratch/hyaku/kengaku-r39/R39DirCheckLeg
```

| copy | mutation (one line) | `DIR N21` | `DIRECTIONS` | exit |
|---|---|---|---|---|
| old | — | `declared=silence observed=mirror MISLABELLED` | `mislabelled=1` | 1 |
| old-m1 | `("silence", "mirror")` → `("silence",)` | `observed=- UNWITNESSED` | `mislabelled=0` | **0 — survives** |
| old-m2 | `if direction in seen:` → `if seen:` | `observed=mirror ok` | `mislabelled=0` | **0 — survives** |
| old-m3 | `verdict = "UNWITNESSED"` → `verdict = "ok"` | unchanged | `mislabelled=1` | 1 |
| new | — | `declared=silence observed=mirror MISLABELLED` | `mislabelled=1` | 1 |
| new-m1 | same line as old-m1 | `observed=mirror MISLABELLED legs=UNWITNESSED,MISLABELLED` | `mislabelled=1` | **1 — caught** (`disagree=3`) |
| new-m2 | same line as old-m2 | `observed=mirror MISLABELLED legs=ok,MISLABELLED` | `mislabelled=1` | **1 — caught** (`disagree=0`) |
| new-m3 | `first = "UNWITNESSED"` → `first = "ok"` (analog) | unchanged | `mislabelled=1` | 1 |

Receipts (this dir's `receipts/`): `old-baseline.txt`, `old-m1-ignore-mirror.txt`, `old-m2-any-direction.txt`,
`old-m3-unwitnessed-ok.txt`, `new-baseline.txt`, `new-m1-ignore-mirror.txt`, `new-m2-any-direction.txt`,
`new-m3-unwitnessed-ok.txt`, one table of the eight: `mutation-evidence.txt` (with every copy's sha256).

**m1** (new copy): leg 1 loses the mirror observation — N02/N08/N15 fall to `LEGS-DISAGREE`, N21's leg 1 says
`UNWITNESSED` — and leg 2 still reports `MISLABELLED` on N21, so the run stays exit 1 with the frozen line intact.
**m2** (new copy): leg 1 accepts any observation as the declared one (`ok`), leg 2 keeps the strict comparison and the
verdict is `MISLABELLED`, exit 1.
**m3** (new copy): on this input the output is byte-identical to the new baseline — same as F38 recorded for the old copy:
no mutant is `UNWITNESSED` on the landed tree, so the branch never fires and the mutant is caught only in the
invariant sense (run still red on N21). The new `LEGS-DISAGREE` path would red it on any input that does exercise
`UNWITNESSED`; no such input exists here, so I do not claim more than that.

**Count: 3/3 caught** (m1, m2 caught where the old copy let them through; m3 unchanged).

## 4. Invariant at the lane tip (calibration)

```
$ python3 <new copy> --lane "$S/lane" --work "$S/w-newbase"        # twice
DIR N21 D5 declared=silence observed=mirror MISLABELLED
LEGS mutants=22 disagree=0 invalid=0
DIRECTIONS total=22 mislabelled=1
EXIT=1                                                            # both runs, byte-equal
```

- The new copy's 22 `DIR` lines and its `DIRECTIONS total=22 mislabelled=1` line are byte-identical to the landed
  round-38 receipt (`.ufo/waves/round-38/integrate/direction-check.txt:3-25`); the only added line is
  `LEGS mutants=22 disagree=0 invalid=0`. Receipt: `receipts/calibration-lines.txt`.
- The old copy run at the round-39 tip reproduces that same 23-line block byte-for-byte — nothing moved between
  `d93b7d6` and `7504738` for this tool.
- Two consecutive runs of the final source are byte-equal (`new-baseline.txt` == `new-baseline-rerun.txt`); ~55 s
  wall per run (`time` on the first: `real 0m55.9s`), the same cost as before, since leg 2 reuses the gate runs leg 1
  already performs.

## 5. Operability

| invocation | old copy | fixed copy | receipt |
|---|---|---|---|
| `--counter plans/round39_c1_verify.py` | `AttributeError: module 'kengaku_counter' has no attribute 'battery38_fixtures'`, uncaught, **exit 1** | `SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed non_6_tuple_rows=7 …`, exit 2 | `receipts/old-r39counter-traceback.txt`, `receipts/new-r39counter-guard.txt` |
| `--work /nonexistent-work-parent` | `FileNotFoundError` traceback, **exit 1** | `SETUP FileNotFoundError: …`, exit 2 | `receipts/old-setup-crash.txt`, `receipts/new-setup-crash.txt` |
| frozen row no longer matches the gate once | `observed=invalid`, not counted, can exit 0 | `INVALID`, counted, exit 3 | code path |
| one leg destroyed | signal gone, exit 0 | signal held, exit 1 | §3 |

Both failure modes were measured on both copies here (`receipts/old-*-crash.txt`, `receipts/old-r39counter-traceback.txt`,
`receipts/new-*.txt`); the round-39 counter incompatibility was also measured independently by seat `R39CritClaims`
(`.ufo/waves/round-39/build/R39CritClaims/receipt-direction-check-r39.txt`), who then re-verified this copy
(`SETUP … rc=2`, sha256 `e471630a…`). With the guard its failure is now named
instead of a traceback. I did **not** port the tool to the round-39 list: `plans/round39_c1_verify.py` loads its fixtures
through a child process (`module_fixtures`) and its `MUTANTS` rows carry a 7th `witness` column, i.e. a different
contract, and that counter already prints `exhibits=` on survivors — the same redundancy inside the counter. Routing it
to the L1 rather than widening this seat (see §7).

## 6. Limits (stated, not hidden)

- Leg 2 carries its own copy of the clause-family map (`D4`/`D5`); a future frozen mutant with a different subcommand
  family must be added to **both** legs, otherwise the legs disagree (red, exit 3) rather than silently passing.
- Leg 2 re-implements the counter's attributed rule from the raw triples; it is an independent *implementation*, not an
  independent *semantics*. A fault in the round-38 kill rule itself would be reproduced by both legs.
- `UNWITNESSED` remains unexercised by this input (§3 m3), so the branch added for it is untested here.
- The fixed copy still defaults to the round-38 list and `plans/battery38`; it is not a round-39 instrument.

## 7. For the L1 (lane files I may not touch)

- **Landing the copy** changes the gate's stdout by one `LEGS …` line, so the round-38 receipt
  `.ufo/waves/round-38/integrate/direction-check.txt` must stay historical; commit a fresh
  `.ufo/waves/round-39/integrate/direction-check.txt` from the landed copy (22 `DIR` lines + `LEGS` + `DIRECTIONS`,
  exit 1).
- **Doc deltas, recommended and cheap** (no frozen sentence is contradicted today): `SKILL.md:585` row
  `mutant-direction-check` — add "exit 2 setup · exit 3 instrument cannot decide · `LEGS …` line"; `corpus/README.md:452`
  and `corpus/QUALITY.md` Q29 — note the second leg and the `legs=` tail. Q29's "exit 1 iff `m > 0`" stays literally
  true.
- **Routed finding (not this seat):** if the direction check is wanted for the round-39 list it needs a port to
  `module_fixtures` + 7-tuple rows + the `rc-silence`/`rc-mirror` directions; today it exits 2 on that counter. Its
  round-38 list surface is unchanged and still reds on N21.
- Round-38 lesson `corpus/lessons/round-38.md:71` ("expect `N21 … MISLABELLED`, every other mutant `ok`") still holds
  for the fixed copy.

## 8. Scratch and tools

Scratch `/fast/scratch/hyaku/kengaku-r39/R39DirCheckLeg` (clone + mutant copies + `--work` dirs) removed at the end of
this seat; the receipts above were copied here first. Every full checker run ran under `TMPDIR=$S` / `--work $S/…`.
No tool installed, upgraded or downloaded (nothing was needed; the workstation's `python3` is 3.14). No `git add`,
commit, checkout, reset or stash anywhere; the scratch clone was never committed.

VERDICT: direction-check-mutants-3/3
