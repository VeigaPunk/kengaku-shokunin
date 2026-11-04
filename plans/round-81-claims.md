# kengaku round 81 — frozen claims

Lane `kengaku-shokunin`, round 81, hyaku run 15, attempt 1, 2026-11-04. L1 seat `KengakuR81`.
Base revision `4e833e9fee8022d24559535178c6fe32b2cd62f1` (`master`, round-80 verifier spot-check).
Two claims, two distinct axes, each causally separable: R81-C1 is verifiable with R81-C2 unlanded,
and R81-C2 with R81-C1 unlanded. Frozen before any receipt for either claim was produced; the
predicate sentence below is the same sentence in the counter's code and in the round's receipts.

## R81-C1 — coverage (lowest non-retired axis, held at its L0 cap)

**Claim.** The population members the frozen selection rule derives at the base revision — the
`unattempted`, stdlib-only, file-artifact/serialization-schema members whose round-52 grader capture
carries the **maximum assert count** (eleven candidates, maximum 5, carried by
`log-summary-date-ranges` and `vulnerable-secret`) — are `executed` at the measured revision: each
names a tracked receipt `corpus/evidence/round81/<member>-probe.txt` whose first line is the frozen
subject shape `# tb2 <member> grader probe`, whose stamp block names the committed round-52 grader
capture with its sha256 at the measured tree (`SUBJECT_CAPTURE`/`SUBJECT_SHA`), the instrument with
its sha256 at the measured tree (`TOOL`/`TOOL_SHA`), the replay environment (`HOST_PYTHON` = the
probe interpreter's `python3 -V` first line, `HOST_OPENSSL` = `openssl version` or `absent`), a
`LANE_TIP` reachable from the measured tip, `WORKTREE clean`, the `COMMAND` that replays it,
`EXIT 0`, and the driver (`MINTED_BY` + `MINTED_BY_SHA`); whose `OBSERVATIONS` block equals the
frozen instrument's stdout at the measured tree under the frozen projection; and whose ledger row is
`executed` with `subject=tb2-header`, the receipt's own observation form as `verdict`, and
`round=81`; and the round-79 population gate still exits 0 with `executed=26 unlocated=0`.

**Universe (derived, never listed).** Read `plans/grader-population-ledger.json` from `BASE_REV`
(git), keep rows with `status == "unexecuted"` and `reason == "unattempted"`, class set ⊆
{`file-artifact`, `serialization-schema`}, whose `corpus/evidence/round52/graders/<member>/tests/
test_outputs.py` exists at `BASE_REV` and imports stdlib modules only, then keep the candidates at
the maximum `^\s*assert\b` count. The counter prints the candidate table (`CANDIDATES n=11 …`) and
the derived universe every run, so a flattering cut of the set cannot hide in the code.

**Frozen probe table.** `plans/round81_probes.json` — member → instrument, argv, timeout. The gate
replays exactly this argv; the driver mints with the same table.

**Counter.** `plans/round81_c1_new_members.py`

    python3 plans/round81_c1_new_members.py --lane .                    # verdict, worktree
    python3 plans/round81_c1_new_members.py --lane . --rev 4e833e9f     # bytes at a revision
    python3 plans/round81_c1_new_members.py --selftest --work DIR
    python3 plans/round81_c1_new_members.py --mutants --work DIR
    python3 plans/round81_c1_new_members.py --control-flip-ledger-only --work DIR
    python3 plans/round81_c1_new_members.py --control-header-only --work DIR
    python3 plans/round81_c1_new_members.py --control-copy-observations --work DIR

Target (after): `TARGET members=2 located=2 reproduced=2 ledger_flipped=2 defects=0`,
`PREDICATE R81-C1 pass`, exit 0. Before (`--rev 4e833e9f`): `located=0 reproduced=0
ledger_flipped=0`, `DEFECTS n=2` (`RECEIPT-UNTRACKED` ×2), exit 1.

**Observation forms (frozen).** A receipt's observation block is every line between
`OBSERVATIONS_BEGIN` and `OBSERVATIONS_END`; every non-empty line must match one of `^CASE `,
`^case=`, `^cases=`, `^MISMATCH `, `^OBSERVED-U `, `^VECTOR `, `^PREDICATE R<n>-C<m> (pass|fail)`.
The compared projection drops `REV <hex>` lines, `cases=` and `OBSERVED-U` lines, and any
`CASE`/`case=` line whose predicted field contains `U` (the round-80 A2 rule, kept because the
projection is the part a deterministic replay can promise). The ledger row's `verdict` is
`predicate` if any `^PREDICATE … pass`, else `vectors` on `^VECTOR `, else `cases`.

**Environment pin (this round's addition, and why it is in the predicate).** A replay's numbers are
a function of the interpreter and the crypto/userland it calls; the round-80 receipts recorded the
stack only inside observations. A receipt minted under a *different* `python3 -V` or `openssl
version` is therefore not the measurement it claims (`HOST-PYTHON-MISMATCH` /
`HOST-OPENSSL-MISMATCH`), and a reader can re-run the pin. This is a *successor* predicate, never
an amendment of round 80's: round 80's receipts and its counter are untouched.

**Controls (frozen, all must lose).** Each builds a green fixture from the frozen shapes, applies
one cheap skip, and runs the same check:

- `--control-flip-ledger-only` — flip the ledger rows to `executed`, mint nothing: dies on
  `RECEIPT-UNTRACKED`.
- `--control-header-only` — write subject line + `MEMBER`/`EXIT` only, no stamp block: dies on
  `STAMP-MISSING`, `SUBJECT-SHA-MISMATCH`, `TOOL-PATH`, …
- `--control-copy-observations` — valid receipts carrying another member's case table: dies on
  `REPRODUCTION-MISMATCH`.

A control that reaches the target means the counter or the target is wrong; no data is produced
before the three lose.

**Batteries.** `--selftest` 11 cases (green + one red per check family: dropped receipt, stripped
stamp line, wrong subject sha, wrong tool sha, host python drift, nonzero exit, wrong ledger round,
wrong ledger status, foreign block, empty block). `--mutants` applies ten attributed data mutations
to the green fixture and requires each to be killed.

**Kill rule.** Any `DEFECT` line fails the claim. A member left `unexecuted` is not a partial pass;
the target is two or the claim is an honest stop.

## R81-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The round-80 verifier spot-check's six routed defects (`U1`…`U6`,
`corpus/lessons/round-80-verifier-spotcheck.md` §5) are discharged as `corpus/routed-findings.jsonl`
rows `R80-U1`…`R80-U6`: status `closed`, a `source` resolving to the spot-check line that carries
the short id, a `close` naming a tracked repair artifact (never the spot-check) whose bytes carry
the id and the row's `evidence_literal`, a `check` that exits 0 at the tip and fails when the
repair is reverted to `4e833e9f` (or deleted, for files new this round), and `corpus/README.md`
indexes the round-80 spot-check.

**Repairs (one per id; the artifact named by `close` carries the id literally).**

| id | defect | repair artifact | what the check re-derives |
|---|---|---|---|
| R80-U1 | S258's anchor pins the pre-A3 receipt bytes | `corpus/lessons/round-81.md` + the superseding `SOURCES.md` row | the six committed round-80 receipt sha256 prefixes and the `lines 3-12` stamp range are the ones a superseding row states; the superseded text is named |
| R80-U2 | R80-C1's after receipt is a dirty-worktree run | `SCORECARD.md` (dated erratum row) | the erratum names `gates-clean.txt` @ `e985e56a` as C1's comparable measurement and says `c1-after.txt` is dirty |
| R80-U3 | census row counts have no producing command | `corpus/evidence/round81/census-rows.txt` | the frozen `grep -cE` count re-runs to the two recorded values (249 at `dce7c275`, 250 at `507d249b`) |
| R80-U4 | M80-1's fix asserted, not shown able to fail; criterion missing | `corpus/evidence/round81/r80-u4-red-before.txt` + `corpus/QUALITY.md` criterion | the red-before run's failure text is committed and a QUALITY criterion cites it |
| R80-U5 | two round-80 gates have no registry row | `SKILL.md` gate registry | both gate names, entry commands, self-test spellings, pinned-value paths and owners are present |
| R80-U6 | `REMINT minted=6 failed=0` has no receipt; README says M80-1 only | `corpus/lessons/round-81.md` + `corpus/README.md` row | the lesson cites the six receipts (not the uncommitted driver line) and the README row names M80-1/M80-2 |

**Counter.** `plans/round81_c2_spotcheck_debt.py`

    python3 plans/round81_c2_spotcheck_debt.py --lane .                  # verdict, worktree
    python3 plans/round81_c2_spotcheck_debt.py --lane . --rev 4e833e9f   # bytes at a revision
    python3 plans/round81_c2_spotcheck_debt.py --selftest --work DIR
    python3 plans/round81_c2_spotcheck_debt.py --mutants --work DIR
    python3 plans/round81_c2_spotcheck_debt.py --control-presence --work DIR

Target (after): `TARGET ids=6 closed=6 checks_passed=6 indexed=yes`, `DEFECTS n=0`,
`PREDICATE R81-C2 pass`, exit 0. Before (`--rev 4e833e9f`): six `DEBT-UNREGISTERED`,
`INDEX … indexed=no`, `DEFECTS n=7`, exit 1.

**Sensitivity (frozen, mechanical).** After the checks pass, the counter reverts every row's
`evidence_path` to its `4e833e9f` bytes (or deletes it when new) in a copy of the tree and requires
that row's check to FAIL there (`CHECK-NOT-REPAIR-SENSITIVE` otherwise). A repair no check can
distinguish from its absence is not a repair.

**Controls (frozen).** `--control-presence` registers all six ids as `closed` with the spot-check
as `close` and `check=true`: dies on `CLOSE-NOT-REPAIR` ×6 + `CHECK-TRIVIAL` ×6.
`--selftest` 9 cases; `--mutants` 4 attributed mutations, each killed.

**Kill rule.** Any `DEFECT` line fails the claim; an id left `open` is an honest stop, not a
partial pass.

## Why these two axes

`coverage` is the lane's lowest non-retired axis (7, L0-capped while declared surfaces are absent);
`calibration` is at ceiling 10 and stays there — the round exercises it by closing the outside
review's findings with checks that fail at base. Neither claim touches the other's evidence:
R81-C1's receipts and ledger rows are new files plus two ledger rows; R81-C2's repairs are the
spot-check's own ids. No axis is harmed: the round's lane diff is additive except the two ledger
rows, the index/registry rows and the dated errata the spot-check itself routed.
