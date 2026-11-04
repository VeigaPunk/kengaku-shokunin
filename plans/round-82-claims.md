# kengaku round 82 — frozen claims

Lane `kengaku-shokunin`, round 82, hyaku run 15, attempt 1, 2026-11-04. L1 seat `KengakuR82`.
Base revision `a3a03ac31451e58f1742b9bccb73b72c2d90a95c` (`master`, round-81 verifier spot-check).
Three claims, three distinct surfaces, each causally separable: C1's universe is pinned to bytes at
`BASE_REV` and never reads C2's or C3's new files; C2's universe is the round-81 spot-check's ids and
never reads C1's rows; C3's universe is the ledger's `executed` rows and its own frozen map. Frozen
before any receipt for any claim was produced; each predicate sentence below is the same sentence in
the counter's code and in the round's receipts.

Freeze-time do-nothing controls (plain measurement, no round counter):
`corpus/evidence/round82/freeze-controls.txt` — C1 leaves 4 `MISSING` + 2 `UNCLASSIFIED`, C2 leaves
7 `DEBT-UNREGISTERED`, C3 has no gate, no map and no receipt. None of the three targets is reachable
by doing nothing.

## R82-C1 — coverage (lowest non-retired axis, held at its L0 cap)

**Claim.** Every `plans/**/*.py` file that exists at `BASE_REV`, sits outside `plans/fixtures/`, and
is referenced as a literal path by a claim-bearing document (`SCORECARD.md`, `LOG.md`,
`corpus/README.md`, all read at `BASE_REV`) either (a) is named by a row of `SKILL.md`'s
`## Gate/probe registry` at the measured tip, or (b) is listed in the counter's frozen `EXCLUSIONS`
table with the reason class `support-module`, which the counter verifies from the file's own bytes
at `BASE_REV` (no `argparse` import **and** no `__main__` block — a file that can be run as a CLI
cannot be excluded); and every registry row's **entry cell** names a Python script that exists at
`BASE_REV`, so the audit's reverse direction stays clean.

**Universe (derived, never listed).** The counter reads the three documents and `SKILL.md` from
`BASE_REV` with `git show` and the file list from `git ls-tree -r --name-only BASE_REV`; it prints
the derived set (`UNIVERSE documents=3 instruments=<n> referenced=<n> registered=<n>`) every run.
`plans/fixtures/` is excluded by rule (the lane has treated that tree as support code since round 52,
`plans/round52_c2_registry.py:35`), not per-file.

**Counter.** `plans/round82_c1_plans_registry.py`

    python3 plans/round82_c1_plans_registry.py --lane .                     # verdict over BASE_REV
    python3 plans/round82_c1_plans_registry.py --lane . --tip <rev>         # rows read at another tip
    python3 plans/round82_c1_plans_registry.py --selftest --work DIR
    python3 plans/round82_c1_plans_registry.py --mutants --work DIR
    python3 plans/round82_c1_plans_registry.py --control-empty-rows --work DIR
    python3 plans/round82_c1_plans_registry.py --control-exclude-cli --work DIR
    python3 plans/round82_c1_plans_registry.py --control-name-only --work DIR

Target (after): `TARGET missing=0 unclassified=0 excluded=2 rows=<133+4> entry_missing=0`, then
`PREDICATE R82-C1 pass`, exit 0. Before (BASE_REV bytes, nothing added): `MISSING 4`, `UNCLASSIFIED 2`,
`DEFECTS n=6`, exit 1.

**Row quality (frozen, applied to rows added this round by name).** Eight non-empty cells; `kind` ∈
{`gate`, `probe`}; the entry cell names an existing script that parses with `ast.parse`; a `gate`
row's verdict map declares `0` and (`1` or a `failed` class), a `probe` row's map declares `0`; the
self-test cell either names a `plans/*.py` script plus a flag string that occurs in that script's
source, or says `none declared`; pinned-values and write-scope cells non-empty and not `n/a`.

**Controls (frozen, all must lose).** Each builds a green fixture from the frozen shapes, applies
one cheap skip, and runs the same check:

- `--control-empty-rows` — four rows with a name and an entry only, other cells `n/a`: dies on
  `INCOMPLETE`, `SELFTEST-UNBACKED`.
- `--control-exclude-cli` — puts the four CLI scripts in the `EXCLUSIONS` table instead of writing
  rows: dies on `EXCLUSION-CLI` (a file with `argparse` + `__main__` cannot be a support module).
- `--control-name-only` — declares the four rows in prose (a `plans/*.md` note) without registry
  rows: dies on `MISSING` (prose is not a row; the reverse reading of R73-C1).

A control that reaches the target means the counter or the target is wrong; no data is produced
before the three lose.

**Batteries.** `--selftest` ≥8 cases (a green fixture plus one red per check family: dropped row,
empty cell, unknown kind, missing script, unbacked self-test, CLI script in EXCLUSIONS, broken entry
cell). `--mutants` applies ≥6 attributed data mutations to the green fixture and requires each killed.

**Kill rule.** Any `DEFECT` line fails the claim. Four CLI instruments without a row is not a partial
pass; the target is `missing=0 unclassified=0`.

## R82-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The round-81 verifier spot-check's seven routed defects (`V1`…`V7`,
`corpus/lessons/round-81-verifier-spotcheck.md` §5) are discharged as `corpus/routed-findings.jsonl`
rows `R81-V1`…`R81-V7`: status `closed`; a `source` resolving to the spot-check line that carries the
short id; a `close` naming a tracked repair artifact (never the spot-check itself) whose bytes carry
the id **and** the row's `evidence_literal`; a `check` that exits 0 at the tip and **fails** when its
repair artifact is reverted to `BASE_REV` (sensitivity leg); and `corpus/README.md` indexes the
round-81 spot-check.

**Universe (derived, never listed).** The newest `corpus/lessons/round-*-verifier-spotcheck.md` by
round number, its `- **V<n> · …**` lines under `## 5. Routed defects`; ids are registered as
`R81-V<n>` (the round whose work the spot-check closed). The counter prints
`UNIVERSE spotcheck=<path> ids=7 <csv>` every run.

**Counter.** `plans/round82_c2_closure_debt.py` (the checks themselves live in
`plans/round82_c2_checks.py`, one `u<k>` subcommand per id, as round 81 did).

    python3 plans/round82_c2_closure_debt.py --lane .                  # verdict, worktree
    python3 plans/round82_c2_closure_debt.py --lane . --rev <rev>      # same checks over that tree
    python3 plans/round82_c2_closure_debt.py --selftest --work DIR
    python3 plans/round82_c2_closure_debt.py --mutants --work DIR
    python3 plans/round82_c2_closure_debt.py --control-presence --work DIR

Target (after): `TARGET ids=7 closed=7 checks_passed=7 indexed=yes`, `DEFECTS n=0`,
`PREDICATE R82-C2 pass`, exit 0. Before (BASE_REV): seven `DEBT-UNREGISTERED`, `INDEX-MISSING`,
`DEFECTS n=8`, exit 1.

**Repairs (the claim's substance; each is a tracked artifact the counter's `check` re-derives).**

- **V1** — `corpus/evidence/round81/c2-after.txt` is a `WORKTREE clean` run of
  `plans/round81_c2_spotcheck_debt.py`, re-minted from a clean tree; the round-81 lesson's C2
  paragraph states the receipt rule (M81-2/Q58 extended to C2 receipts) as a dated correction.
- **V2** — every quote word-count and anchor range the round-81 lesson and `corpus/SOURCES.md`
  S260/S261 state equals a mechanically recomputed value (whitespace-split words of the quoted text;
  the receipt's actual stamp/observation line numbers).
- **V3** — `corpus/knowledge/tb2-file-artifact-replay-classes.md` opens with `source:`,
  `verified-at:`, `recheck:`.
- **V4** — `plans/round81_c2_spotcheck_debt.py`'s mutant-docstring count equals the number its own
  `--mutants` battery prints (`real=<n>`), either by adding the missing mutants or by correcting the
  docstring; the check recomputes both sides.
- **V5** — the stray `--lane/` directory is gone (`test ! -e ./--lane`), recorded in the lesson.
- **V6** — this round's wave carries a live `mutation-tester` seat and an attack share ≥25 % over the
  campaign list (reviewer, critic, mutation-tester, labrat); the L1 holds the planner seat under the
  orchestrator's 2026-10-19 ruling (the validator rejects `planner`), with a bounded data-walk riding
  a scout item. The check reads `.ufo/waves/round-82/w1-results.json`.
- **V7** — `corpus/evidence/round81/determinism.txt` carries the producing `COMMAND` and the `REV` it
  was measured at, so its two hashes are re-derivable.

**Kill rule.** Any `DEFECT` line fails the claim. A `close` naming the spot-check, a `check` that
passes on `true`, or a check that still passes with its repair reverted is a failure, not a partial
pass.

## R82-C3 — capability acquisition (freshness instrument, no axis-score move)

**Claim.** The lane gains `sweep-at-one-tip`: one gate that takes every `executed` member of
`plans/grader-population-ledger.json`, locates its replay instrument through the frozen map
`plans/round82-sweep-map.json` (26 members, each with the instrument, the argv derived from that
instrument's own `--help` at `BASE_REV`, and the receipt), runs each instrument once at one measured
tip under a per-member timeout, classifies each member into exactly one status
(`reproduced` | `diverged:<n>` | `unrunnable:<code>`), and prints a per-class histogram; the receipt
`corpus/evidence/round82/sweep.txt` carries one `MEMBER <name> status=… exit=… secs=… argv=…` line
per member plus `HISTOGRAM` and `HISTOGRAM-CLASS` lines; two runs at the same tip agree on every
member's status and divergence count (determinism is claimed on the classification, never on bytes
that embed a pid or a port); and every receipt `COMMAND` equals the argv the gate reconstructed from
the frozen map (`COMMAND-MISMATCH` otherwise — the round-81 F2 ruling), writes are staged until every
member has a status line (`STAGED-WRITE`), and `--verify-at-tip` re-runs the gate's own `--selftest`
battery at the measured tree (round-80 plan item 4).

**Comparison projection (frozen).** From both the committed receipt and the run's stdout keep only
lines matching `^(CASE |case=|TEST |VECTOR |LEG |regrade )`; then drop `cases=` lines, lines starting
`OBSERVED-U `, and any `CASE`/`case=` line whose predicted field contains `U` — the round-80 A2 /
round-81 projection, reused unchanged. `reproduced` iff the run's exit code equals the receipt's
stamped `EXIT` and the projections are equal; `diverged:<n>` otherwise (`n` = differing projection
lines); `unrunnable:<code>` when the instrument exits non-zero, times out, or writes no observation
line. Every classification is reported; nothing is laundered into `reproduced`.

**Counter.** `plans/round82_c3_sweep.py`

    python3 plans/round82_c3_sweep.py --lane . --check                 # verdict over committed bytes
    python3 plans/round82_c3_sweep.py --lane . --run --work DIR        # the sweep itself (writes the receipt)
    python3 plans/round82_c3_sweep.py --lane . --verify-at-tip --work DIR
    python3 plans/round82_c3_sweep.py --selftest --work DIR
    python3 plans/round82_c3_sweep.py --mutants --work DIR
    python3 plans/round82_c3_sweep.py --control-ledger-copy --work DIR
    python3 plans/round82_c3_sweep.py --control-exit-only --work DIR
    python3 plans/round82_c3_sweep.py --control-fabricated-line --work DIR

Target (after): `TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=0`,
`PREDICATE R82-C3 pass`, exit 0. Before (BASE_REV): the gate, the map and the receipt are absent; no
line of the target can be printed.

**Controls (frozen, all must lose).** `--control-ledger-copy` (statuses copied from the ledger, no
run: dies on `NO-RUN`); `--control-exit-only` (exit codes compared, projections ignored: dies on
`PROJECTION-UNCHECKED`); `--control-fabricated-line` (a receipt line whose observation the current
instrument does not emit: dies on `VERIFY-MISMATCH`).

**Batteries.** `--selftest` ≥10 cases; `--mutants` ≥8 attributed mutations of the receipt and the map
(each killed).

**Kill rule.** Any `DEFECT` line fails the claim; a status line without `exit=`/`secs=`/`argv=`, a
member without a status line, or a histogram that does not sum to 26 is a failure. The capability
enters the SCORECARD capabilities table only when `--check` exits 0 at the tip and `--verify-at-tip`
reproduces the receipt's classification.

## Shared rules

- Route: every seat is dispatched by the host route table (`task.agentModelOverrides`); never pass
  `model`.
- Write scope: seats write only their report file, their scratch dir and (where named) one deliverable
  under `.ufo/waves/round-82/w1/`; the L1 integrates every lane file.
- Honesty: an unrun check has not passed; a divergence is reported with its member name and line
  count, never smoothed.
