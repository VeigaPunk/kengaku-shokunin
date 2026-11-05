# kengaku round 92 — frozen claims and case table

Frozen at commit A of round 92. Author: kengaku (L1 KengakuR92, hyaku run 15 attempt 1).
Base: `4ba56182307ccda1ec436bfe3d61cb3d92e56608` (lane tip at round start; clean, pushed).
Case table: `plans/round92-cases.json` (sha256 `2249d5c0ea90930a5c36300b47a4b991d41ae9c5ff400deba5adf9be28d5a693`).
Frozen-rule discipline: after this commit the predicates, counting commands, targets and kill
rules below do not change; an element that looks wrong after the first measurement is reported
as a mispredict, never repaired in place. Instruments land at commit B; the official receipt
and the ledger flip at commit C; measured tips are named in LOG.md.

## Round shape (declared before dispatch)

One v1 wave (band 8-16), ≥25 % attack seats, ≤2 connector seats; residual ≤4 seats in one
ordinary call if any. Planned roster 12 seats: 3 executor, 1 scout, 1 connector, 1 scribe,
2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel — attack share 5/12 = 42 %. The §3
planner seat is held by the L1 (validator rule); a bounded planning data-walk rides the
scout/connector items. No `model` is passed; routing is the host table.

## R92-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A tenth located offline replay of a pinned Terminal-Bench 2.0 grader:
`llm-inference-batching-scheduler` @ `2fd12b88` (classes `crypto-credential`,
`file-artifact`, `filesystem-metadata`, `serialization-schema`), replayed offline through
`plans/round92_bs_probe.py` with 10 deterministic cases × 6 grader-function legs; the
population ledger flips the member to `executed` (round 92).

**Frozen predicate.** At the measured tip T: `python3 plans/round92_c1_replay.py --lane . --rev T --work DIR`
prints `TARGET executed_rows=36 member=llm-inference-batching-scheduler located=1 executed=1
cases=10 legs=60 mismatches=0 defects=0`, then `PREDICATE R92-C1 pass`, exit 0.
At BASE `4ba56182`: the same counter prints `TARGET executed_rows=35 … executed=0 …` and
`PREDICATE R92-C1 fail`, exit 1. Class cells after: `filesystem-metadata` 4 of 10,
`crypto-credential` 4 of 12, `serialization-schema` 5 of 10, `file-artifact` 27 of 76
(each asserted by the counter's L7 leg from the committed ledger bytes).

**Do-nothing control.** The round-91 counters at BASE (committed receipt
`.ufo/waves/round-92/L1/base-batteries.txt`, measured before this freeze):
`round91_c1_replay` rc 1 with 10 `DEFECT L5 receipt names unknown case ?` (the member unexecuted
at BASE AND the instrument defect M7); the ledger at BASE holds executed_rows=35. A control that
skips the round's work cannot reach executed_rows=36 or a green counter.

**Counting command.** `python3 plans/round92_c1_replay.py --lane . --rev T --work DIR`
(standard input pinning per §9: TARGET line names the exact values).

**Predictions (filed before the official run).** The receipt at T shows 10 CASE lines, all
`ok=True`, mismatches=0. The 10 predicted vectors in `plans/round92-cases.json` were confirmed
by a pre-freeze scratch dry-run (probe TOOL_SHA `db02dd4728067f702b0afecd84b6d28eee3d1ab76db986923b23a6086cf4d741`
at that dry run; the shipped probe may differ only by the stamp/paths — the case table sha
`2249d5c0…` is identical). The official receipt runs at the tip after commit B.

**Source (sourced claim, CORPUS rule 1).** S283 (grader `tests/test_outputs.py` @ `2fd12b88`,
tier A, scope `member replay only`), S284 (`tests/cost_model_for_tests.py`, the relative-import
sibling the grader needs), S285 (the two task input-data files, `dataset`, tier A member replay
only — their sha256 values are pinned inside the grader itself), S286 (`tests/test.sh`,
REJECTED — its replay needs apt/curl/uv network installs the offline replay forbids).
Rows land with commit C; the lesson's `## Gate` carries URL, access date and located quotes.

**Kill rule.** Any DEFECT line, any mismatch, or `executed_rows` ≠ 36 at the measured tip fails
the claim; a mispredict is recorded honestly (no predicate edits after this freeze).

## R92-C2 — calibration (held at ceiling 10; instrument conformance, routed defects 1/2/5)

**Claim.** The three routed round-91 counter defects are repaired under this new frozen
predicate, each with a red-before witness: (a) **M7** — `plans/round91_c1_replay.py`
`parse_receipt()` reads the case id from `key=value` tokens while the receipt carries it
positionally; (b) **M12** — the same counter's `openssl` host probe is unguarded (a missing
binary crashes the counter with a traceback, rc 1, no PREDICATE line, instead of the contracted
`DEFECT SETUP` rc 2); (c) **M9** — `plans/round91_counter_pin.py` exposes `--skip-selftest`
in its predicate path and its selftest expectations are in-checker code, not a pinned input.

**Frozen predicate.** `python3 plans/round92_c2_conformance.py --lane . --rev REV --work DIR`
runs each check against a rev-controlled checkout of the counter bytes and prints, at the
measured tip T: `M7-CASE-PARSER pass`, `M12-HOST-PROBE-GUARD pass`, `M9-SELFTEST-ESCAPE pass`,
`PREDICATE R92-C2 pass`, exit 0. At BASE `4ba56182`: `PREDICATE R92-C2 fail`, exit 1, with all
three checks red. Each check's verdict condition:
- **M7**: at REV=BASE the BASE counter bytes exit 1 with ten `DEFECT L5 receipt names unknown
  case ?` on the committed receipt `corpus/evidence/round91/modernize-probe.txt`; at REV=T the
  amended counter bytes exit 0 with `PREDICATE R91-C1 pass` on the SAME receipt bytes (the ten
  `ok=True` CASE lines are the red-then-green witness; no receipt byte changes).
- **M12**: at REV=BASE, run the BASE counter with `openssl` masked from PATH → the run dies
  unguarded (rc 1, no `PREDICATE R91-C1` line in stdout); at REV=T the amended counter prints
  `DEFECT SETUP` and `PREDICATE R91-C1 could-not-evaluate`, rc 2 (fail-closed).
- **M9**: at REV=BASE the checker bytes contain `--skip-selftest` and
  `plans/round92-selftest-expectations.json` does not exist at BASE → red; at REV=T the checker
  bytes contain no `--skip-selftest`, the expectations table exists, its sha256 is pinned as an
  entry in `plans/counter-pins-r91.json`, the entry matches the table bytes at T, and the
  amended checker's default run at T prints `PINS checked=17 matched=17 mismatched=0` and
  `SELFTEST cases=9 red-green-ok=9`, rc 0 (the ninth case `expectations-tampered` red-greens
  the table pin: tampered table bytes → `DEFECT SETUP expectations-pin mismatch`, rc 2).
  The known residual (checker plus pin ledger rewritten in one commit still passes) stays
  disclosed and operator-owned (L0 `kengaku | round-91`, question on in-tree pins) — this
  claim does not close it.

**Do-nothing control.** At BASE the round-91 C2 counter alone is green (committed receipt:
`base-batteries.txt` shows `PREDICATE R91-C2 pass` rc 0 at BASE) — the r91 predicate is
reachable with no work, which is exactly why the M9/M7/M12 conjuncts above are the claim.

**Kill rule.** A red sub-check at the tip, or a green one at BASE, fails the claim; the
pin-ledger regeneration at commit B is disclosed before any measurement (the checker's own
self-pin moves to the amended bytes — B2-style move, one disclosed regeneration, no scoring
before it).

## R92-C3 — operability (held at ceiling 10; freeze gate v3, capability successor)

**Claim.** `plans/round92_burndown.py` (gate v3) repairs the routed gate defects and is
measured on the real ledger: (a) **M13** — chain-aware supersede (a supersede of a supersede
resolves through the chain; its own selftest case proves a two-level chain resolves to the
chain-end status); (b) **M10** — a closed row's effective check must be non-vacuous (not
`true`/`:`/`exit 0` and carrying a path token or a file operator) and an override row's check
must share at least one path token with the row's `close`, `source`, or the base row's check;
a blocked row's owner must resolve to a lane id in `shokunin.conf`; (c) **M11** — closing
checks run inside a `git worktree` at the measured revision (`--work` scratch), never in the
caller's working tree; (d) **M8** — the gate's selftest runs inside the default predicate path
and any red case fails the PREDICATE; (e) **M6** — the R82-V8 fleet-repo resolution in
`plans/round83_c2_checks.py` reads `SHOKUNIN_ROOT` (or `R83_FLEET_REPO`) first, `origin.parent`
fallback, so the check is not clone-path dependent.

**Frozen predicate.** After the round-92 triage rows land append-only (a correction row for the
R84-V9-R91 disposition word — routed round-91 spot-check defect 8 — plus any rows the new M10
rules require), at measured tip T: `python3 plans/round92_burndown.py --lane . --rev T --work
DIR --freeze-round 92` prints `freeze=admitted pending=0` with `malformed_unresolved=0`,
`unowned_blocked=0`, no `DEFECT` lines, `SELFTEST cases=M red-green-ok=M` in the same
invocation, and `PREDICATE R92-C3 pass`, exit 0. At BASE `4ba56182`: the same gate prints
`freeze=refused oldest_pending_round=82 pending=1` with the three `override-unjustified`
DEFECTs (the one-level resolver names the R90 rows as deciding), rc 1.

**Do-nothing control.** The v2 gate at BASE (committed receipt: `freeze=refused … pending=1 …
overrides=3`, rc 1) and — decisive — the pre-audit showing the CHAIN-AWARE state at BASE
already resolves `pending` to 0: no ledger row can manufacture the v3 predicate without the
code repairs; the v2 gate at the tip (receipt committed with the wave evidence) still refuses.

**Kill rule.** Any check failing at the tip worktree, any red selftest case, or
`freeze=refused` at the tip fails the claim → honest stop with the DEFECT list. A check that
breaks because a round-92 registry edit changed a counted surface is a named conflict, not a
silent pass: the gate stops and the report carries it.

## Companion work (no claim slot)

- **F2 — capture pins (routed round-91 defect 9).** Supersede rows in `corpus/SOURCES.md` give
  the four blind-spot rows' surviving chain tips capture sha pins; `plans/round92_f2_counter.py`
  (successor of `round91_f1_counter.py`) prints the before/after `ANCHORLINE` lines and
  `WRONG-LINE-CAUGHT True` at the tip, rc 0; at BASE it prints no `CAPTURE-PINNED` lines, rc 1.
- **M14 correction row** — append-only `routed-findings.jsonl` row correcting the R84-V9-R91
  disposition word (`fixed-verified` overstated a judgment close).
- **L0** — the open round-90/91 questions stay open; this round routes around them (the re-freeze
  route for instrument defects is the round-91 L0 question's stated successor path).
