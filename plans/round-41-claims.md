# Round 41 — frozen claims (kengaku, hyaku run 9, 2026-10-26)

Baseline lane tip `e50c134556b4ba48e29dc7ff364e90d6ef07a3f3` (the round-40 non-author spot-check). L1 `KengakuR41`
holds the canonical planner seat. Written and frozen before any `plans/battery41` fixture exists and before the
first recorded run of `plans/constraints_probe.py`.

**Order of operations (QUALITY Q30; checked by `plans/order_check.py`, now inside the C2 counter as V8).** Before
this file was committed the probe ran only as `--dry` (no sandbox) and `--stage-check` (builds each case's end
state in the sandbox and prints stage exit codes only; the grader module is never imported):
`stagecheck cases=25 failed=0` (`.ufo/waves/round-41/claims/c2-stage-check.txt`). The C2 do-nothing control runs
the gate with `--rerun`, but with no receipt on disk the gate's P10 returns `receipt unreadable` before it executes
anything. **Disclosed prior observation (round-40 wave-2 `F40CritPlanNext` D8):** the first 16 of the 25 cases are
the round-40 planning seat's pilot, already graded on this host (`.ufo/waves/round-40/build/R40PlanNext/cs/
run1.txt`, `cases=16 observed_pass=3 observed_fail=13 mismatches=2`). Their predictions are carried VERBATIM,
including the two the pilot observed wrong (`later-valid-wed-1105`, `seconds-30`: predicted fail set E, observed
C,E), so the first recorded run re-observes those 16; the 9 new cases were never graded before this freeze.

Axis state carried (SCORECARD round 40): calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8,
adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. **Coverage is chosen** for the lowest-axis claim
(tie-break as in rounds 35–40: a pinned local source and an offline sandbox exist). Novelty 7 has no candidate this
round: the sharpest finding of the chosen grader (tests 2–3 read the first `DTSTART` of the file) is published as
TB2.1 PR #245 (`R40PlanNext.md` §3.2), so the round claims no novelty and prices any unpublished case as a rider for
the falsify wave's prior-art seats, not as a claim (`F40CritPlanNext` D5). Coverage stays capped at 7 by the open L0
question `kengaku | round-33`, so C2 is judged on its counter, not on a score move. No stagnation waiver. Controls
are committed with this file under `.ufo/waves/round-41/claims/`.

## C1 — calibration: what `tip_receipts.py` and the `sources_adopt.py` CLI advertise and no committed fixture demonstrates

- **Surface:** `plans/tip_receipts.py` (`e4f49714…`, landed `ec172168`, never mutation-priced; `considerthese/
  2026-10-26.md` lesson 3) and the CLI half of `plans/sources_adopt.py` (`38492bf1…`; its `--selftest` drives the
  library functions, `main()` was killed 2 of 32 by `R40PlanNext`'s harness), both unedited this round, and what each
  advertises: `tip_receipts.py`'s docstring, the `sources-adopt` registry row (`SKILL.md:573`, eight exit codes) with
  the parser messages in `main()`.
- **Self-assessment vs observed state (the calibration count):** the number of frozen mutants that no committed
  fixture kills ATTRIBUTABLY in its declared direction. List: 23 (receipts 13: T01–T13; sources 10: S01–S09, S11).
  Every mutant's `adv` cell quotes the advertising sentence with file:line and carries an `adv_kind` (round-40
  closure R4): 21 `direct`, 2 `indirect` (T06 — an unavailable control is a "failed control"; S11 — main() refuses a
  non-`mined` requested row with exit 5), 0 `none`; the counter prints that split on its `ADVERTISED` line.
  `S10` (`check()`'s requested-id refusal) was withdrawn before freeze as rc-equivalent: `claims/s10_equivalence.txt`
  `ref_rc=5 mut_rc=5`.
- **Directions (QUALITY Q29):** declared per mutant in the counter; every one witnessed before freeze by
  `claims/witness/w_receipts.py` and `w_sources.py` run through the frozen counter in development mode
  (`claims/witness-run.txt`: 23 of 23 killed in their declared directions, `wrong=0 tampered=0 sidechannel=0`). The
  sources tool needs exact exit pairs (`2>0`, `2>1`, `2>5`, `2>9`, `3>0`, `5>0`), a direction class new this round.
- **Counter:** `python3 plans/round41_c1_verify.py --lane .` (docstring = the full rule). New over the round-40
  counter (closure R1/R2, `F40CritPlanNext` D1–D4, `R40CritC1Counter` A1/A2, `R40SentinelCounter`, `R40RevCounters`):
  every module built in `bwrap --ro-bind / /` with the lane hidden and only its own fixture dir and tmp writable, no
  lane clone handed to fixtures; every tool run under `--ro-bind / /` with only its work and tmp dirs writable, a fixed
  system PATH (nothing under `~/.local/bin` is reachable or writable), `--unshare-net`; content-digest fingerprints;
  `build()` must return a list of str; the predicate binds `TOTAL = 23` and `FLOORS = {receipts: 13, sources: 10}`.
  The two tools are clean of the round-40 D3/D4 objection: neither needs `uv` or a writable home (`tip_receipts` runs
  `python3` stubs in fixture lanes; `T08` relies on `uv` being absent from the fixed PATH).
- **Frozen predicate:** C1 passes iff `python3 plans/round41_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=23 killed=23
  survived=0 invalid=0 null_detected=0`, then `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, then `PINS-AFTER
  mismatched=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c1-nothing.txt` — no `plans/battery41`:
  `BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`, `MUTANTS-BY-TOOL receipts=0/13 sources=0/10`,
  `PREDICATE C1 fail`, exit 1.
- **Other controls:** `control-c1-no-mutants.txt` (the discriminating control `F40CritPlanNext` D2 asked for: a copy
  of this counter with `MUTANTS = []` — patch `control-c1-no-mutants.patch` — and a 22-fixture battery present →
  `MUTANTS total=0`, `PREDICATE C1 fail`, exit 1); `control-c1-witness-as-battery.txt` (the witness modules copied
  into a scratch mirror's `plans/battery41` → `PREDICATE C1 pass`: the predicate is reachable, by witnessed work);
  `control-c1-tool-edited.txt` (one appended line in `tip_receipts.py` → `PINS mismatched=1`, its 13 mutants
  `invalid`, fail); `control-c1-hostile.txt` (a module that tries the round-40 host-write vectors: its build's write
  under `$HOME` → `OSError`, its read of the lane's `tip_receipts.py` → `FileNotFoundError` (lane hidden), its probe
  stub's write during the tool run → `write=denied`; no marker file exists after the run; the token scan flags it).
- **Work:** `plans/battery41/*.py` single-purpose fixtures (wave-1 executors), contract in the counter docstring. The
  battery may not import, copy or read the witness modules; reviewers check that.
- **Kill rule:** any survivor, invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0`, a per-tool
  count other than 13/13 and 10/10, or a pin mismatch before or after the run → C1 not admitted, reported as an honest
  stop. A mutant later shown equivalent is reported as a limit, never removed or relabelled. The two tools are not
  edited this round.
- **Limits named now:** a kill records a result difference in the declared direction, not the fixture's intent; the
  side-channel scan is a token heuristic, so non-author code review of battery41 stays part of admission; a module
  can still read other copies of the tools on the read-only host. `tip_receipts.py`'s six `F40TipReceipts` defects
  (two false-red shapes, a green run with no possible tamper control) are not mutants and are not repaired here.

## C2 — coverage: the pinned TB2 `constraints-scheduling` grader, a seventh grader class (an embedded scheduling model)

- **Surface:** `corpus/knowledge/` (new entry `tb2-constraints-scheduling-grader.md`), `corpus/SOURCES.md` (S122
  `tests/test_outputs.py`, S123 `instruction.md`, terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  opened 2026-10-26 15:19 -03 by the L1; S124 TB2.1 PR #245 tier B for prior art, to be opened in wave 1), README
  index row + coverage bullet, PROVINCE paragraph; one §Frontier TB2 sub-bullet narrowed by one task (7 of 89). Edge
  class new to the lane: the verdict is computed by a scheduling model embedded in the grader (`_hard_ok`,
  `_overlap`, a minute-granularity earliest-slot scan) over three sha256-pinned input calendars, and the graded
  artefact is an ICS file the grader reads with regexes, not an ICS parser.
- **Probe (frozen):** `plans/constraints_probe.py` (digest in `frozen-digests.txt`), 25 cases, predictions and
  `violates=` tags in `corpus/evidence/round41/constraints-dry-cases-freeze.txt` (`cases=25 predicted_pass=6
  predicted_fail=19`); every case graded twice on the same end state (`regrade=`). Captures
  `corpus/evidence/round41/tb2-constraints-scheduling/` (10 files + `SHA256SUMS`). Receipt (first recorded run,
  committed after this file): `corpus/evidence/round41/constraints-probe.txt`.
- **Counter:** `python3 plans/round41_c2_verify.py --lane .` — the round-40 counter's V1–V7 re-pointed at this
  package (spec `plans/pkg-spec-r41.json`, gate, probe, dry table and captures pinned; no V1–V7 check relaxed) plus
  V8, the order gate on this claims file and the receipt (`F40CritPlanNext` D9: a green round-40 run cannot be
  re-filed), and `--work` created before use (D10(b)).
- **Frozen predicate:** C2 passes iff `python3 plans/round41_c2_verify.py --lane .` prints `checks=8 defects=0`,
  then `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `claims/control-c2-nothing.txt` — `checks=8 defects=5` (V2, V3, V4,
  V7, V8), `PREDICATE C2 fail`, exit 1; the embedded gate's P10 reads `receipt unreadable` (the probe never ran).
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); they are reported, never edited out of the table — the two pilot
  mismatches are expected to recur and are not corrected.
- **Limits named now:** host python3 stands in for the image's `uvx -p 3.13` pytest; the image is never pulled;
  recipes run unprivileged. The decoy finding (tests 2–3 read the first `DTSTART`) is published (TB2.1 PR #245), so
  the entry claims a probed instance only. Known informed-filler limit of V1–V7 carried from rounds 37–40
  (`considerthese/2026-10-26.md` proposal 2, not taken this round).

## Separability

C1 reads only the two tools, `plans/battery41` and fixtures it builds from nothing (no lane clone this round); C2
reads only its captures, spec, gate, probe, receipt, entry, SOURCES, README and the git history of this file and the
receipt. Neither counter reads the other's work product: each passes with the other's work wholly absent.

## Frontier step (not a claim)

- Sourced claim: C2 (S122/S123 opened this round; S124 to be opened in wave 1).
- Mined mistake (`corpus/lessons/round-41.md`): the round-41 plan's predicate as landed in round 40 was satisfiable
  with zero round-41 work (`F40CritPlanNext` D1, `counter-vacuous` run A: `MUTANTS total=0 … PREDICATE C1 pass`).
  Captured-by: none (no rule required a do-nothing control that keeps the battery and empties the list). Fix: the
  `TOTAL`/`FLOORS` binding in this counter, shown able to fail by `control-c1-no-mutants.txt`.
- considerthese: `2026-10-26.md` proposal 1 (routed-findings burn-down) as a rider — one append-only file and one
  printed `routed_open=<n> oldest_round=<r>` line, outside every pinned ledger (`F40CritPlanNext` D7).
- Routed items from `corpus/lessons/round-40-verifier-spotcheck.md` §5: R1 (C1 counter soundness — this counter),
  R2 (host safety — this counter's read-only envelope plus the wave rule), R3 (registry rows for
  `plans/round_close.py` and the tip-receipts derived mapping — wave 1), R4 (adv cells only where present — this
  list's `adv_kind`), R5 (carried: the order class into a ledger stays blocked while `plans/ledger_tip.py` is pinned
  by round-40 C1, recorded `open, blocked` in the rider's file; `round40_c2_verify.py --work` traceback fixed in the
  round-41 counter, the frozen round-40 counter untouched; report census lines print the W04 count).
