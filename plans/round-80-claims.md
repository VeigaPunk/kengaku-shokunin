# kengaku round 80 — frozen claims

Lane `kengaku-shokunin`, round 80, hyaku run 15, attempt 1, 2026-11-04. L1 seat `KengakuR80`.
Base revision `dce7c275381c669e6489f1b795b1505d0824c262` (`master`, round-79 verifier spot-check).
Two claims, two distinct axes, each causally separable: R80-C1 is verifiable with R80-C2 unlanded,
and R80-C2 with R80-C1 unlanded. Frozen before any receipt for either claim was produced; the
predicate sentence below is the same sentence in the counter's code and in the round's receipts.

## R80-C1 — coverage (lowest non-retired axis, held at its L0 cap)

**Claim.** The six members the round-79 ledger prices `executed-unlocated`
(`cancel-async-tasks`, `chess-best-move`, `distribution-search`, `largest-eigenval`,
`openssl-selfsigned-cert`, `protein-assembly`) are `executed` at the measured revision: each names a
tracked receipt under `corpus/evidence/round80/` whose first line is the frozen subject shape
`# tb2 <member> grader probe`, whose stamp block names the historical receipt with its sha256, the
instrument with its sha256 at the measured tip, a `LANE_TIP` reachable from the measured tip,
`WORKTREE clean`, `EXIT 0` and the command that replays it, whose `OBSERVATIONS` block equals the
instrument's stdout at the measured tree (`REV <commit>` lines excluded on both sides, because the
block is committed bytes and the measured tip moves), and whose ledger row is `executed` with
`subject=tb2-header`, the receipt's own observation form as `verdict`, and `round=80`; and the
round-79 population gate still exits 0 with `executed=24 unlocated=0`.

**Universe (derived, never listed).** Members whose row in
`plans/grader-population-ledger.json` has `status == "executed-unlocated"` **at `BASE_REV`** — six at
the freeze. The counter reads the base ledger from git (`--base-ledger` overrides, for fixtures only),
so flipping rows in the worktree can never shrink the universe.

**Frozen probe table.** `plans/round80_probes.json` — member → historical receipt, instrument,
argv, per-probe timeout. The gate replays exactly this argv; the driver mints with the same table.

**Counter.** `plans/round80_c1_located_replay.py`

    python3 plans/round80_c1_located_replay.py --lane .                    # verdict, worktree
    python3 plans/round80_c1_located_replay.py --lane . --rev dce7c275     # bytes at a revision
    python3 plans/round80_c1_located_replay.py --selftest --work DIR
    python3 plans/round80_c1_located_replay.py --mutants --work DIR
    python3 plans/round80_c1_located_replay.py --control-flip-ledger-only --work DIR
    python3 plans/round80_c1_located_replay.py --control-header-only --work DIR
    python3 plans/round80_c1_located_replay.py --control-copy-observations --work DIR

Target (after): `TARGET members=6 located=6 reproduced=6 ledger_flipped=6 diverged=<=6 defects=0`,
`PREDICATE R80-C1 pass`, exit 0. Before (`--rev dce7c275`): `located=0 reproduced=0
ledger_flipped=0`, `DEFECTS n>=6`, exit 1.

**Observation forms (frozen).** A receipt's observation block is every line between
`OBSERVATIONS_BEGIN` and `OBSERVATIONS_END`, written verbatim from the instrument's stdout with
`REV <commit>` lines removed (the block is committed bytes, so a commit-dependent line would make
every later replay mismatch). The *observation lines* are those matching one of
`^CASE `, `^case=`, `^cases=`, `^MISMATCH `, `^OBSERVED-U `, `^VECTOR `,
`^PREDICATE R<n>-C<m> (pass|fail)`; the tool's own other lines (e.g. `grader=`, `components_aa=`)
stay in the block and are compared too. The ledger row's
`verdict` is the round-79 observation precedence: `predicate` if any `^PREDICATE ... pass`,
else `vectors` on `^VECTOR `, else `cases` on `^CASE `/`^case=`.

**Historical divergence is reported, never a silent pass.** If the historical receipt's observation
lines differ from the new receipt's blocks, the receipt must carry
`HISTORICAL-DIVERGENCE <n> ...`; the gate reports `historical=differs` and counts it in `diverged`.
It is not a defect (the tip's instrument may have been corrected since the historical round); a
divergence without the note is `DIVERGENCE-UNNOTED`.

**Leading indicator of what this buys.** The round-79 lesson ended with the debt stated as "five
write only a `REV` header and `protein-assembly`'s writer has no `--receipt` option — a
subject-stamped re-mint is round 80's work." This claim discharges exactly that sentence: the six
members' replays become self-locating and independently reproducible at the tip, not re-stamped
assertions.

**Controls (frozen, all must lose).** Each control builds a green fixture from the frozen shapes,
applies one cheap skip, and runs the same check:

- `--control-flip-ledger-only` — flip the six ledger rows to `executed` pointing at the historical
  receipts, mint nothing: dies on `SUBJECT-ABSENT`.
- `--control-header-only` — write the new receipts as subject line + historical bytes, no stamp
  block: dies on `STAMP-MISSING`.
- `--control-copy-observations` — write valid receipts but copy another member's observation block:
  dies on `REPRODUCTION-MISMATCH`.

A control that reaches the target means the counter or the target is wrong; no data is produced
before the three lose.

**Batteries.** `--selftest` cases include a clean green fixture and one red case per check
(subject absent, stamp missing, source-sha mismatch, tool-sha mismatch, receipt untracked,
observations empty/foreign, two members named, ledger not executed, exit nonzero, lane-tip
unreachable, unexplained divergence). `--mutants` applies six attributed data mutations to the green
fixture (flip row, strip stamp, wrong sha, foreign block, drop receipt, second member) and requires
each to be killed.

**Kill rule.** Any `DEFECT` line fails the claim. A row left `executed-unlocated` is not a partial
pass; the target is six or the claim is an honest stop.

## R80-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The round-79 verifier spot-check's six routed defects (`V1`…`V6`,
`corpus/lessons/round-79-verifier-spotcheck.md` §6) are discharged as `corpus/routed-findings.jsonl`
rows `R79-V1`…`R79-V6`: each `status=closed`, `source` resolving to the spot-check line that carries
the id, a `close` naming a tracked repair artifact (never the spot-check itself) whose bytes carry
the id and the row's `evidence_literal`, and a `check` that exits 0 at the tip and **fails** when its
evidence file is reverted to `BASE_REV` (or deleted, for files new this round); and
`corpus/README.md` indexes `lessons/round-79-verifier-spotcheck.md` (absent at base: the index
stops at round-78, so the round-79 closure artifact is a dead file until this round).

**Universe (derived, never listed).** `- **V<n> · ` lines of
`corpus/lessons/round-79-verifier-spotcheck.md` §6 — six at the freeze.

**Counter.** `plans/round80_c2_spotcheck_debt.py`

    python3 plans/round80_c2_spotcheck_debt.py --lane .                 # verdict, worktree
    python3 plans/round80_c2_spotcheck_debt.py --lane . --rev dce7c275  # same checks over that tree
    python3 plans/round80_c2_spotcheck_debt.py --selftest --work DIR
    python3 plans/round80_c2_spotcheck_debt.py --mutants --work DIR
    python3 plans/round80_c2_spotcheck_debt.py --control-presence --work DIR

Target (after): `TARGET ids=6 closed=6 checks_passed=6 indexed=yes`, `PREDICATE R80-C2 pass`,
exit 0. Before (`--rev dce7c275`): six `DEBT-UNREGISTERED`, `DEFECTS n>=6`, exit 1.

**Repairs the rows name (frozen here so the repair cannot be redefined after data).**
- `R79-V1` → `corpus/evidence/round80/v1-r78-c1-at-148801a6.txt`: the retired
  `plans/round78_c1_class_member_ledger.py` re-run with `--rev 148801a6` prints
  `PREDICATE R78-C1 pass` (the spot-check's second repair option), stamped with the current tip.
- `R79-V2` → `corpus/lessons/round-80.md`: dated correction — round-79's "25 `W04` … unchanged in
  both" is wrong; the receipts are 25 before and 26 after (`diff` adds S256's duplicate-URL line).
- `R79-V3` → `corpus/lessons/round-80.md`: dated correction — 13 *unquantified* rows = 12 bare
  `executed` + 1 `recipe-unexecuted`, not "13 bare `executed`".
- `R79-V4` → `corpus/lessons/round-80.md`: dated correction re-anchoring the S254 quote to capture
  lines 2322–2326.
- `R79-V5` → `corpus/lessons/round-80.md`: the S256 duplicate-URL warning is stated and the row is
  kept with a reason (distinct scope: the harness execution model vs the grader bytes).
- `R79-V6` → `corpus/evidence/round80/r79-c1-after.txt` and `r79-c2-after.txt`: the two round-79
  after receipts re-minted at this round's tip through `plans/round78_restamp.py`
  (`plans/round80-restamp.json`), each carrying `LANE_TIP`/`TOOL`/`TOOL_SHA`/`WORKTREE`/`COMMAND`/`EXIT`.

**Control (frozen).** `--control-presence` — register all six ids closed with the spot-check as
`close` and `check` = `true`: must die on `CLOSE-NOT-REPAIR` ×6 + `CHECK-TRIVIAL` ×6,
`target_reached=False`.

**Batteries.** `--selftest` green fixture + red cases (unregistered, trivial check, failing check,
close names the routing file, close without evidence, source line, duplicate row); `--mutants`
six data mutations, each killed.

## Axis and harm statement

R80-C1 moves **coverage** (7, L0-capped; the move is the located replay population, not the number);
R80-C2 moves **calibration** (10, held, exercised). The round touches no other axis: no knowledge
entry is superseded, no sibling scope is absorbed, no declared surface is removed. Any harm on
depth/operability/freshness/adjacency/novelty is a defect of this round, not a trade.

## Frontier step (rides inside the cap; not a claim)

- `corpus/SOURCES.md`: one `own-work` row `S258` for the round-80 located-replay instrument, its
  probe table and the six receipts; census before recorded at freeze
  (`corpus/evidence/round80/census-before.txt`) and re-run at round end.
- One mistake mined into `corpus/lessons/round-80.md` `## Mistakes` with class, evidence pointer,
  captured-by and a fix that can fail.
- `considerthese/`: at most one still-unimplemented proposal touched; the round states which.
- `Assimilation`: governed by the open L0 `kengaku | round-54`; `none` is stated explicitly if the
  id drift keeps it closed.
