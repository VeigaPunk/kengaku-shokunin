# F40CritPlanNext — attack on the round-41 plan (kengaku r40, wave 2, critic)

Seat: F40CritPlanNext (critic, leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read at
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch `master`) through a scratch clone
`/fast/scratch/hyaku/kengaku-r40/F40CritPlanNext/lane`; `git -C "$S/lane" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r40/F40CritPlanNext/lane` before any write. Nothing in the lane was edited, staged or committed.
Receipts in `.ufo/waves/round-40/falsify/F40CritPlanNext/`; scratch removed at the end (§5).

**Target under attack.** `SCORECARD.md:1484-1498` `### Planned (round 41)` (the landed plan) and its source
`.ufo/waves/round-40/build/R40PlanNext.md` (the draft, §6 paste block; where the landed text and the draft differ, the
difference is itself a finding). Nothing here judges a score: each item names the plan sentence it attacks.

Axes named before work (Godspeed): **X1 predicate integrity** — is the round-41 frozen predicate red on an artifact that
does no round-41 work; **X2 repair feasibility** — do the plan's stated C1 repairs keep the landed battery green;
**X3 axis discipline** — is the claim on the lane's own lowest non-retired axis with a stated reason; **X4 routed closure** —
does every routed item get an owner and a predicate; **X5 re-observation honesty** — can an already-observed run be filed as
the round's first recorded run; **X6 province/adjacency** — do the candidates stay in-domain and cite the fleet precedents
PROVINCE names. X1 and X2 ran first (executable); X6 last.

## 0. Answer to the assigned question — which candidate a do-nothing control could reach

**Calibration, measured.** A round-41 counter copy with the landed `plans/battery40` battery and **zero new mutants**
prints the full green predicate and exits 0:

```
$ bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid \
    --die-with-parent python3 $S/r/counter-vacuous.py --lane $S/lane --work $S/work-a
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
exit=0                                                    (receipt runA-vacuous.txt, 49.5 s)
```

The only edit to the counter is four appended lines (`counter-vacuous.patch`: `MUTANTS = []`, `TOTAL = 0`). The plan's
drafted predicate is `MUTANTS total=<n> killed=<n> survived=0 invalid=0 null_detected=0` (`R40PlanNext.md:336`) with `<n>`
unbound, and the counter's only non-vacuity guard is a self-consistency check against a literal the same author sets
(`plans/round40_c1_verify.py:225` `TOTAL = 21`; `:567` `len(MUTANTS) == TOTAL and ... killed == TOTAL`). So the candidate a
do-nothing control reaches is **calibration (C1)**, and the second is the **rider/Carried** block, which has no predicate at
all (§2 D7/D6). Coverage is *not* reachable by a do-nothing counter — its V1/V2 checks are path-bound to
`corpus/evidence/round40/` (`plans/round40_c2_verify.py:48-65`) — but it is reachable by re-filing an already-green run
(§2 D9).

## 1. Controls re-run (the plan's own priced control, and the control it should have priced)

**The plan prices one control**: "Before (do-nothing control, measured at freeze): no `plans/battery41` → `killed=0`"
(`R40PlanNext.md:337`; the landed block drops even this). Re-run on a clean clone of the tip with the battery removed:

```
$ mv plans/battery40 plans/battery40.off && python3 plans/round40_c1_verify.py --lane . --work $S/work-b
PINS total=3 mismatched=0
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=0 survived=21 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1                                                    (receipt runB-nobattery.txt, 3.2 s)
```

That control is red **only because the round-40 mutant list is non-empty**. It does not test vacuity: the same predicate is
green when the list is empty (§0). The round-41 control that discriminates is "no *new* mutants, battery present" — my run A —
and the plan must freeze it red.

**The second control pair (X2).** The landed plan adopts "clean PATH for tool runs, read-only host fs with only the fixture
root writable" (`SCORECARD.md:1489-1490`), which is wave-1's repair table (`R40SentinelCounter.md:170`, `--ro-bind / /` +
`--bind <root> <root>`). Both halves break a pinned fixture chain:

```
$ bwrap --ro-bind / / --bind $S $S --dev /dev --proc /proc --tmpfs /tmp --tmpfs /run --unshare-pid \
    --die-with-parent python3 plans/ledger_tip.py --source $S/lane --work $S/lw-ro
R35-D1 status=closed observed=fail agree=NO fixtures=14 ... tip_package_rc=1 ledger=corpus/defects-round35.jsonl kind=live
rows=9 closed=9 observed_pass=8 mismatches=1
exit=1                                                    (receipt ledger-ro.txt, 5.0 s)

$ <same command under the current wave-2 envelope: --dev-bind / />
rows=9 closed=9 observed_pass=9 mismatches=0
exit=0                                                    (receipt ledger-dev.txt, 4.2 s)

$ <current envelope, PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin>
R35-D1 ... agree=NO ... tip_package_rc=1
rows=9 closed=9 observed_pass=8 mismatches=1
exit=1                                                    (receipt ledger-barepath.txt, 5.3 s)

$ bwrap --ro-bind / / ... env HOME=/home/vgpnk uv run --no-project python3 -c "print(1)"
error: Could not acquire lock / Read-only file system (os error 30) at path "/home/vgpnk/.cache/uv/.tmp..."
uv exit=2                                                 (receipt uv-under-ro-root.txt)
```

Chain: `plans/round36_c1_verify.py:267-275` (`r35_d1` → `run_gate`) → `plans/pkg_gate.py:276`
`cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe`; `import Bio` fails on this host
(`python3 -c "import Bio"` → `ModuleNotFoundError`), so `uv` is the only path. The counter's own docstring records the same
dependency as the reason it keeps PATH and HOME: "with a bare PATH it exits 1 — measured at the freeze"
(`plans/round40_c1_verify.py:64-65`).

**Other re-runs (no-harm):** `plans/round40_c2_verify.py --lane .` at the tip → `checks=7 defects=0`, `PREDICATE C2 pass`,
exit 0 (6.8 s); `plans/tip_receipts.py --lane . --list` → exit 0 with both new receipts mapped
(`git-leak-probe.txt ... origin=derived`, `db-wal-probe.txt ... origin=derived`); `git diff --stat ec17216 ec1005a2 -- plans/`
→ empty, so the landing measurement at `ec17216` holds byte-for-byte at the tip.

## 2. Defects

Each row: the plan sentence attacked, the receipt, the smallest safe correction. Directions: [M] measured now, [I] inference
from two measured facts.

### D1 — the round-41 predicate is satisfiable with zero round-41 work [M] — X1

- Attack: `SCORECARD.md:1486-1491` "mutation-test the next undemonstrated tripwire surface — the landed
  `plans/tip_receipts.py` … and the CLI half of `plans/sources_adopt.py`".
- Evidence: §0 run A — `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0, with
  the landed battery and no new mutant. `R40PlanNext.md:336` leaves `<n>` unbound.
- Impact: a round-41 C1 receipt can be green without one mutant of either named tool, and the SKILL registry row for
  `round41-c1-mutants` would read exactly like a real pass.
- Smallest correction: freeze the predicate with three bounds the counter cannot self-satisfy — `PINS total=5 mismatched=0`
  (the two new tools pinned), `MUTANTS total=<N>` with `N>0`, and a per-tool floor (e.g. `tip_receipts>=6`, `sources>=4`),
  plus the named battery module set. `len(MUTANTS)==TOTAL` alone is not a floor.

### D2 — the plan's priced control cannot see D1 [M] — X1

- Attack: `R40PlanNext.md:337` "Before (do-nothing control, measured at freeze): no `plans/battery41` → `killed=0`".
- Evidence: §1 run B — red at `killed=0 survived=21`, i.e. red only because the list is the round-40 list. Run A (the
  discriminating shape) is green.
- Smallest correction: price two controls, both red: (a) no battery → `fixtures=0`, `killed=0`; (b) battery present, no new
  mutants → must print `PREDICATE C1 fail` under D1's floors. (b) is the control that would have caught D1.

### D3 — the isolation repair, as worded, reds the landed battery [M] — X2

- Attack: `SCORECARD.md:1489-1490` "read-only host fs with only the fixture root writable".
- Evidence: §1 — `ledger_tip.py` under that envelope prints `R35-D1 ... agree=NO ... tip_package_rc=1`, `mismatches=1`,
  exit 1; `uv` cannot create its cache under `--ro-bind / /` (exit 2).
- Impact: the battery's `defects` is "the exact class set the reference must print" (`plans/round40_c1_verify.py:39-43`), so
  the three `l_rows` fixtures that keep the closed `r35_d1` row gain `NO:R35-D1` and print `wrong` on the first round-41
  run: `wrong>=3` → `PREDICATE C1 fail`, a red landing caused by the repair, not by a survivor. [I from the two measured
  facts: fixture contract + ledger output under the repair envelope.]
- Smallest correction: name the writable set in the repair — `UV_CACHE_DIR=<work>/uv-cache` bound rw (or a pre-seeded
  `Bio`), and state which paths outside the fixture root stay writable. Cite kumitate's runner as PROVINCE already requires
  (`PROVINCE.md:465-466`: "kumitate's `cap-run.mjs` (`--ro-bind / /`) is the cited stronger form a round-41 counter would
  need") instead of re-deriving the envelope in-lane.

### D4 — the clean-PATH half of the repair reds the same fixture [M] — X2

- Attack: `SCORECARD.md:1489` "clean PATH for tool runs".
- Evidence: §1 bare-PATH run — `R35-D1 ... agree=NO`, `mismatches=1`, exit 1. The counter already documents this:
  "with a bare PATH it exits 1 — measured at the freeze" (`plans/round40_c1_verify.py:64-65`).
- Smallest correction: "clean PATH" must be defined as the caller PATH minus nothing that the pinned checks need, or the
  sandbox must bind `~/.local/bin` (the wave-2 host-safety envelope does exactly that). Do not adopt "clean PATH" as a
  blanket rule; it contradicts the tool's own frozen limit.

### D5 — the claim axis is not the lane's lowest non-retired axis, and no reason is given [M] — X3

- Attack: `SCORECARD.md:1486` "**Calibration (8):**".
- Evidence: the round-40 axis state is `calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8,
  adjacency 8` (`SCORECARD.md:1454`, `plans/round-40-claims.md:16-17`), and the lane's rule is "Lowest non-retired axis:
  coverage 7, tied with novelty 7; coverage chosen" with "No stagnation waiver" (`SCORECARD.md:1454`). The landed block
  never says which axis the round claims, or why novelty 7 (uncapped) is skipped; the draft asked for exactly this
  confirmation (`R40PlanNext.md:319` "L1 to confirm against the round-40 axis table").
- Smallest correction: one sentence in the block — claim axis coverage 7 (capped by L0 `kengaku | round-33`, no score move)
  or novelty 7, with the reason novelty 7 has no candidate (`R40PlanNext.md:311` "[INFERENCE: a novelty claim would need an
  unpublished grader finding; none was found this seat]").

### D6 — the one item routed to round 41 is carried with an unscheduled precondition [M] — X4

- Attack: `SCORECARD.md:1496-1497` "Carried: the order class into a separately frozen ledger once battery40's ledger
  declarations can move (R3)".
- Evidence: the routed item is `corpus/lessons/round-40.md:55-57` — "Routed to round 41 (a separately frozen ledger the tool
  reads, after this battery is re-declared)". Nothing in the plan schedules that re-declaration: the calibration bullet
  re-freezes "the round-40 counter's limits" (`SCORECARD.md:1488-1491`) and never says battery40's ledger fixtures move, and
  no bullet names an owner for `plans/ledger_tip.py` (pinned by C1 at `plans/round40_c1_verify.py:96-100`).
- Impact: R3's precondition is untouched by construction, so the item is carried a third time; round 40's own block carried
  it once already (`SCORECARD.md:1420`).
- Smallest correction: either name the owner and the fixture re-declaration inside the C1 bullet (edit `ledger_tip.py` +
  re-pin + re-declare the `l_rows` sets in one freeze, per Q30), or delete the Carried line and record R3 in the rider as
  `open, blocked` with the pin as the blocker.

### D7 — the rider has no artifact, no predicate and no owner [M] — X4

- Attack: `SCORECARD.md:1497-1498` "`considerthese/2026-10-26.md` proposal 1 … priced as a rider (`R40PlanNext` §4: 71
  routed items vs 5 ledger rows)".
- Evidence: the draft's rider printed a line and seeded rows — "print `routed_open=<n> oldest_round=<r>` in the round close"
  (`R40PlanNext.md:356`) — and the landed block drops both. A do-nothing round prints the same sentence again. Also the
  draft's cheapest form is not free: appending rows to `corpus/defects.jsonl` moves the battery's `NO:` sets — the very
  blocker the lesson records for R3 (`corpus/lessons/round-40.md:56-57`).
- Smallest correction: keep one printed line (`routed_open=<n> oldest_round=<r>`) and one file, and say the rows go to a
  sibling append-only file that `ledger_tip.py` does not read (so the C1 pin is untouched) or defer the rider to the round
  that re-declares the ledger fixtures (D6).

### D8 — the pilot's already-observed cases are not marked as prior observations [M] — X5

- Attack: `SCORECARD.md:1492-1495` "`R40PlanNext` pilot `cases=16 … mismatches=2`".
- Evidence: the pilot's predictions are frozen and two of them are known wrong: `cs/dry-table.txt` carries
  `later-valid-wed-1105 pred_fail=E` and `seconds-30 pred_fail=E` against observed `C,E`
  (`R40PlanNext.md:233`). The landed block does not say whether the round-41 dry table carries those predictions
  verbatim (honest) or fixes them (post-observation).
- Impact: rounds 38-40 all carry a "Disclosed ordering" sentence in PROVINCE for exactly this (round-38:
  "a control-time gate rerun had already executed the probe once before the freeze"); round 41 has no such statement, so
  the round's "first recorded run" would be a re-observation of two cases.
- Smallest correction: state that the 16 cases are re-frozen with the pilot's predictions verbatim and the two mismatches
  carried, or add the disclosure line naming the two cases as re-observed.

### D9 — coverage names no round-41 receipt, counter or dry table, so a green round-40 run can be re-filed [M] — X5

- Attack: `SCORECARD.md:1492-1495` — the whole coverage bullet.
- Evidence: no receipt path, no counter name, no predicate, no dry-table id in the landed text (the draft had "counter =
  round 40's V1–V7" and "receipt checked by `plans/order_check.py`", `R40PlanNext.md:349-350`). The round-40 C2 counter is
  green at the tip right now (`checks=7 defects=0`, exit 0, §1), and the pilot's `cases=16 observed_pass=3 observed_fail=13`
  line already exists — either could be filed as the round-41 evidence.
- Impact: the coverage claim has no artifact that a non-author can distinguish from a round-40 re-run; round 40's own
  predicate (`checks=7 defects=0`) is not carried.
- Smallest correction: name the round-41 probe, dry table, receipt path (`corpus/evidence/round41/…`), the counter and its
  predicate, and require the `cases=` line to be produced after the freeze commit.

### D10 — two landed counter defects a copied round-41 counter inherits [M] — X1/X2

- Attack: `SCORECARD.md:1488-1489` "with the round-40 counter's limits repaired".
- Evidence (a): the derived-mapping clause's mutants are unpriced — `R40PlanNext.md:158` says so; the landed block says
  "its round-40 derived-mapping clause included" (`SCORECARD.md:1487`) without a witness, and Q29 requires a witness per
  frozen mutant before freeze. The eight draft `tip_receipts` `old` strings all still occur exactly once at the tip
  (measured: T01-T08 each `count=1`), so the draft list survives the edit — the *new* clause's mutants are the unpriced ones.
- Evidence (b): the M2 class (`--work` absent → traceback) recurs in the counter the plan copies from:
  `plans/round40_c2_verify.py:266` `with tempfile.TemporaryDirectory(prefix="k40-c2-", dir=a.work) as work:` with no
  `mkdir` — the lesson records the class as unfixed (`corpus/lessons/round-40.md:37`).
- Smallest correction: state that derived-mapping mutants enter the frozen list only if witnessed (Q29), and that the new
  C2 counter creates `--work` before `TemporaryDirectory`.

## 3. Province and routed-list cross-check

| candidate | PROVINCE verdict | routed list (round-40 lesson) |
|---|---|---|
| C1 calibration (tip_receipts + sources_adopt CLI) | in-domain: mutation test of the lane's own tripwires is "kengaku's instrument for its own self-assessment" (`PROVINCE.md:460-464`); method stays tameshi's, runner stays kumitate's — the plan cites wave-1 attack reports but not the kumitate precedent PROVINCE names for the round-41 counter (`PROVINCE.md:465-466`) | no routed item depends on it; R4 (counter soundness) landed in round 40 |
| C2 coverage (`constraints-scheduling`) | in-domain: §Frontier "agentic benchmark task-spec audits (Terminal-Bench 2.0 …)" (`PROVINCE.md` §Frontier); no refusal touched by the bullet | none; the plan's S122/S123 are free ids (`corpus/SOURCES.md` ends at S121, measured) |
| rider (defects.jsonl burn-down) | in-lane operability; the plan does not touch a refused surface | R3 is the only item routed to round 41 (`corpus/lessons/round-40.md:55-57`); it is carried without a scheduled precondition (D6) |
| missing PROVINCE clause | the round-41 paragraph must narrow the grader count (7 read → 8) and carry the routing clause round 40 carried for SQLite — "What SQLite actually stores in a WAL … routes rather than being absorbed" (`PROVINCE.md:439`); the calendar/ICS analogue (what a correct schedule is) is not in the plan | — |

Draft-vs-landed drift found while checking: the draft's row ids are `S121`/`S122` (`R40PlanNext.md:341`) — `S121` is already
the TB2.1 PR #3 row landed this round (`corpus/SOURCES.md:136`). The landed text corrects this to `S122`/`S123`
(`SCORECARD.md:1494`); the draft block must not be pasted as-is.

## 4. What held (no-harm, measured)

| check | command | result |
|---|---|---|
| landing measurement transfers to the tip | `git diff --stat ec17216 ec1005a2 -- plans/` | empty (plans byte-identical) |
| round-40 C2 counter at the tip | `python3 plans/round40_c2_verify.py --lane . --work …` | `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 |
| tip_receipts derived mapping | `python3 plans/tip_receipts.py --lane . --list` | both new receipts `origin=derived`, exit 0 |
| draft mutant strings survive the fix | occurrence count in the tip file | T01-T08 each `count=1` |
| battery still honest under the current envelope | `ledger_tip.py --source … --work …` | `rows=9 closed=9 observed_pass=9 mismatches=0`, exit 0 |
| the 21 fixtures still run | run A | `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0` |

## 5. Limits and hygiene

- Run A's green predicate is measured on a *copy* of the landed counter with `MUTANTS=[]`, `TOTAL=0` (patch kept); it
  prices the predicate shape, not a counter a seat has written.
- The "three `l_rows` fixtures go `wrong`" consequence of D3 is [I] from two measured facts (the ledger's output under the
  repair envelope, and the fixture contract's "exact class set"); I did not edit the counter to re-sandbox its children and
  measure the `wrong` count directly.
- Host load was high (as in wave 1); the only timings quoted are wall times of single commands.
- All C1/C2/tool invocations ran inside the mandated bwrap envelope with `--lane` on my own clone; the repair-envelope and
  ro-root uv runs are the two deliberate envelope variants, both on my clone. No write outside
  `.ufo/waves/round-40/falsify/F40CritPlanNext/` and `/fast/scratch/hyaku/kengaku-r40/F40CritPlanNext/`; no pacman, no
  service, no `systemd-run`, no process left running; the two neutralized wave-1 attack modules were never executed; scratch
  removed before yield.

VERDICT: plan41-attack-10-defects
