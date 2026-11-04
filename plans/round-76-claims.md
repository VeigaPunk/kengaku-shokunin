# Round 76 — kengaku — declared claims (frozen before data)

Base: `fda63968f29f8f58dc2b28831acac879405b8326` (round-75 verifier spot-check).
Frozen 2026-11-04 by L1 `KengakuR76`. Nothing below may be re-worded after a seat has scored it
(PROTOCOL §9): predicate, counter, target, control and kill rule are the same sentence here, in the
counter's code and in the receipt label.

Round shape: ONE v1 wave, 14 seats (executor 3, scribe 3, scout 1, connector 1, reviewer 2,
critic 1, mutation-tester 1, labrat 1, sentinel 1). Attack roles 5/14 = 36 % (≥25 %); connector 1.
The L1 holds the §3 planner seat (validator rejects `planner`); the planning data-walk rides the
scout item.

## R76-C1 — coverage (lowest non-retired axis, L0-capped at 7): every surface `PROVINCE.md` declares is resolved live, and each row's dated declaration must agree

**Claim.** The `## Surfaces` table stops being prose a seat re-checks by hand: a new in-repo gate
(`plans/round76_c1_surface_resolver.py`) parses every row, resolves its first declared path or
localhost endpoint live (`test -e` semantics for paths, an HTTP status for endpoints; brace
alternatives expanded), and requires a dated `ABSENT YYYY-MM-DD` marker exactly where the host
answers absent — no marker where absent, no marker where present, and no present-tense prose
("relocated intact", "all resolve at") on an absent row. Every defect carries its class and row
number, so the table can be repaired from the gate's own output.

**Axis named by the surface it moves.** Coverage is scored as "PROVINCE.md lists every surface; none
unexplored without reason"; the surface this round moves is *the declaration's verifiability* — from
a row of prose to a verdict per row. It is not a re-score of the index gate (that is round 75's
instrument and stays as it is).

**Before** (`corpus/evidence/round76/c1-before.txt`, `--rev fda63968`):
`SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=9 disagree=2`,
`DEFECT STALE-TEXT 2` (`~/archive/bench-arena` still says "relocated intact"),
`DEFECT UNDECLARED-ABSENT 4` (`http://127.0.0.1:45669` returns 000 with no dated marker),
`PREDICATE R76-C1 fail`, rc 1. The instrument itself is absent at base
(`git cat-file -e fda63968:plans/round76_c1_surface_resolver.py` → 128).

**Target (after).** At the landing tip, the frozen command prints
`SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=11 disagree=0`,
no `DEFECT` line, `PREDICATE R76-C1 pass`, rc 0 — with the two PROVINCE rows repaired in place as
dated supersessions (the row-2 stale phrase, the row-4 undeclared absence) and a PROVINCE row
declaring the gate.

**Counting command.** `python3 plans/round76_c1_surface_resolver.py --lane .`

**Control that must lose** (`corpus/evidence/round76/c1-control-declared.txt`): trust the row's own
text instead of resolving the surface — `CONTROL-SKIP rows=11 disagreements=1 target_reached=False`,
`PREDICATE R76-C1-control pass` (the control's assertion holds: the skip cannot reach `disagree=0`,
because row 4 claims present and the host answers 000). A declaration-only counter would print
`disagree=0` on today's bytes.

**Kill rules.** (a) any `DEFECT` line; (b) any `SURFACE … prose` row (a declared surface with no
resolvable anchor) unless PROVINCE carries an explicit anchor for it; (c) `AGREE disagree=` not
equal to the defect count. Selftest battery 7 arms (6 red), mutant matrix 5/5 expected-id kills
(`corpus/evidence/round76/c1-selftest.txt`, `c1-mutants.txt`).

**Causal separability.** C1 needs no part of C2: it reads PROVINCE and the host, and its target
holds whether or not any round-75 routed defect is discharged. The two rows it repairs are outside
C2's universe (R75-D1…D7 are ledger rows and correction texts, not surface rows).

## R76-C2 — calibration (held at ceiling 10, exercised): the closure's routed defects become a burn-down — registered, discharged by re-derived values, closed on an ancestor commit

**Claim.** `corpus/routed-findings.jsonl` becomes the register for the newest closure's routed
defects, and each discharge is priced by a leg that re-derives its value at check time: the
round-75 stamp (`9f8f0f21…`), the final-rule index counts at the round-75 freeze
(`60 = 4/36/20`, derived natively from rendered README rows + `git ls-tree`), the selftest counts
the two round-75 gates actually print (`cases=8 red=7`, `arms=5`), the two round-74 gate receipts at
the tip, and S252's three `merge-base --is-ancestor` exit states (0 ancestor / 1 not-ancestor /
other = error) for every `close_commit`. The gate `plans/round76_c2_defect_discharge.py` also
refuses a trivial `check` (no committed path + no literal) and a `status: closed` row whose
`close_commit` does not resolve.

**Before** (`corpus/evidence/round76/c2-before.txt`, `--rev fda63968`):
`SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=0 wrong=14`,
seven `LEDGER … MISSING-ROW`, `PREDICATE R76-C2 fail`, rc 1 — the closure's seven defects never
entered the ledger.

**Target (after).** At the landing tip: `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7
legs_passed=7 legs_pending=0`, no `DEFECT`/`LEG-FAIL` line, `PREDICATE R76-C2 pass`, rc 0.

**Counting command.** `python3 plans/round76_c2_defect_discharge.py --lane .`

**Control that must lose** (`corpus/evidence/round76/c2-control-status.txt`): register all seven ids
as `status: closed` with a trivial `check` and no discharge text —
`CONTROL rows_claimed_closed=7 trivial_checks=1 failed_legs=3`, `PREDICATE R76-C2-control pass`
(the status-only skip is caught by the legs and by `CHECK-TRIVIAL`).

**Kill rules.** (a) any `MISSING-ROW`, `OPEN`, `NO-CLOSE-COMMIT`, `CLOSE-NOT-ANCESTOR`,
`CLOSE-UNRESOLVED`, `CHECK-TRIVIAL` defect; (b) any failing leg (D1–D7); (c) a printed
`discharged=` that differs from the comma of ok rows. Selftest 10 arms (9 red), git three-state arms
3/3, mutant matrix 8/8 expected-id kills.

**Causal separability.** C2 changes the ledger and five correction blocks; it does not touch
`PROVINCE.md`, and C1's target does not depend on any ledger row. A do-nothing round reaches
neither: `registered=0` at base, `disagree=2` at base.

## Sources and frontier (§2b)

- **S252 (admitted this round)** — Git `git-merge-base` documentation for `--is-ancestor`:
  https://git-scm.com/docs/git-merge-base, opened live 2026-11-04, capture
  `corpus/evidence/round76/sources/git-merge-base.html` (HTTP 200, 41 397 B, sha256
  `46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644`), located quote at capture
  line 1703, 25 words: "Check if the first <commit> is an ancestor of the second <commit>, and exit
  with status 0 if true, or with status 1 if not." It grounds R76-C2's `close_commit` leg and its
  three-state distinction (rule (a) above); the neighbouring sentence ("Errors are signaled by a
  non-zero status that is not 1") is why `CLOSE-NOT-ANCESTOR` and `CLOSE-UNRESOLVED` are separate
  defects. Used by this file and `corpus/lessons/round-76.md`.
- **Rejected this round** — "a commit id in a row's `close` text proves the discharge is on the
  branch". S252 proves an object id resolves; ancestry is `merge-base --is-ancestor` and its exit
  status 1 is a *negative answer*, not an error. Flip: store `close_commit` as its own field, run
  the three-state test, and keep the human-readable `close` as the dated reason.
- **Frontier.** `corpus/README.md` §Frontier ground this round touches: nothing new is entered —
  the round repairs the lane's declaration and burn-down instruments. `considerthese/2026-10-26.md`
  proposal 1 (routed-findings burn-down) is implemented by R76-C2 and cited in
  `corpus/lessons/round-76.md`; it lands as a `QUALITY.md` criterion. Assimilation: none.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ rc 0 at round start (`corpus/evidence/round76/census-before.txt`), 243 rows, 25 `W04`
duplicate-URL warnings (unchanged from round 75). After state must be rc 0 with 244 rows.

## Amendment A1 (2026-11-04, before any after-state data) — the C2 Before line names the receipt's actual tallies

The R76-C2 **Before** line above reads `legs_pending=0 wrong=14`. The committed receipt
`corpus/evidence/round76/c2-before.txt` prints `SCOPE ids=7 registered=0 closed=0 open=7 discharged=0
legs_passed=0 legs_pending=2 wrong=12`: legs D4 and D5 print `PENDING` at a revision before their
inputs exist (the two round-75 selftests and the correction block), by the counter's frozen PENDING
rule, and `wrong=12` counts the twelve printed defects (seven `MISSING-ROW`, five `LEG-FAIL`).
Predicate, target, control and kill rules are unchanged; only the Before prose is corrected to the
receipt. Found by seat `ScribeLessonR76` reading the receipt against this file — the R75-D2 class,
caught before it could ship.

## Amendment A2 (2026-11-04, implementation defect, predicate unchanged) — `emit()` honours `--work`

Seats `ScribeCorrectionsR76` and `C2ReplayR76` independently found that `emit()` in
`plans/round76_c2_defect_discharge.py` created `/fast/scratch/hyaku/kengaku-r76/c2` regardless of
`--work` — the §7 scratch rule ("no hardcoded `/tmp` or fixed scratch root in a committed tool"). The
gate now takes `args.work` and creates only that path. Predicate, target, control, kill rules and every
leg are unchanged; the before/control receipts' bytes are unaffected (the scratch path is not printed)
and were regenerated after the fix so every committed receipt comes from the same gate revision.

## Amendment A3 (2026-11-04, control plumbing, predicate unchanged) — the C1 control reads the revision it claims

Seat `C1ReplayR76` showed `--control-declared` resolved PROVINCE from the module path and ignored
`--lane`/`--rev`: on repaired bytes it printed `disagreements=0 target_reached=True`, so the committed
control receipt could not be re-derived after the repair (the R74-D1 replayability class). The control
now takes `--lane`/`--rev`, prints `PROVINCE_REV`, and its receipt stamps the revision it read. The
regenerated receipt at `--rev fda63968` prints `PROVINCE_REV fda63968`,
`declared=present live=absent 4 http://127.0.0.1:45669`, `disagreements=1 target_reached=False`,
`PREDICATE R76-C1-control pass`, rc 0. The control's discriminating power is a property of the state it
reads; the repaired table has nothing left to catch, which is the claim passing, not the control failing.
Predicate, target, kill rules and both claim counters are unchanged.

## Amendment A4 (2026-11-04, rule strengthened before the after-state, target unchanged) — the stale-prose scan reads the whole row

Seat `C1ReplayR76` found a present-tense claim the frozen rule missed: row 3 (`:34113`) carries
`identity re-probed via /v1/models + /health 200 each round` and `identity re-probed each round` in two
cells while its own live probe answers 000 — and the scan read `cells[1]` with a fixed vocabulary that
did not contain the phrase. The rule now scans the **whole row** for present-tense tokens and the
vocabulary gained `identity re-probed` and `re-probed each round`; a row cannot say ABSENT in one cell
and "re-probed each round" in another. The self-test gained the third-cell arm (`cases=8 red=7`) and the
mutant matrix a sixth (`6/6`).

Consequence, stated as the R75-D3 rule requires: the before state was **re-measured under the final
rule** at `fda63968`, so no cross-version comparison is hidden. `corpus/evidence/round76/c1-before.txt`
now prints `SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=8 disagree=3` with three
defects (`STALE-TEXT` rows 2 and 3, `UNDECLARED-ABSENT` row 4), superseding the `agree=9 disagree=2`
line above, which was measured before the scan reached row 3. Predicate, target (`AGREE disagree=0`),
control and kill rules are unchanged; the rule moved only in the direction that makes the claim harder.

## Amendment A5 (2026-11-04, hardening from the wave, target unchanged) — the resolver confines its probes and the ledger binds evidence to the close commit

The wave found two classes the frozen counters did not price; both are repairs that can only add
defects, so the target (`AGREE disagree=0`, `discharged=7 legs_passed=7`) is untouched and the before
state is re-measured under the final rule.

**R76-C1 (`ReviewerC1R76`, `SentinelR76`, `LabratR76`).** (1) Endpoint probing is confined to
loopback authorities (`127.0.0.1`, `localhost`, `::1`) and a redirect that leaves loopback is refused —
a committed row could otherwise steer a GET at a remote or internal service (`NONLOCAL-ANCHOR`), which
is what the Sentinel's intercepted `http://192.0.2.1/sentinel` and its real loopback→hostname redirect
demonstrated. (2) A path token containing a `..` segment is refused (`ESCAPE-ANCHOR`). (3) Brace
expansion is capped at 64 targets and a `RecursionError` becomes a defect (`OVERFLOW-ANCHOR`) — the
Sentinel's 12-group token produced 4096 targets and a deep nesting raised uncaught. (4) A malformed URL
(over-long IDNA label) becomes `MALFORMED-ANCHOR` rather than a traceback. (5) An impossible
`ABSENT YYYY-MM-DD` date is `MALFORMED-DATE` (`date.fromisoformat`). (6) Duplicate identities are
`DUPLICATE-SURFACE`. (7) The receipt now prints `IDENTITIES n= unique= sha256=`, and
`--expect-manifest <sha>` fails on a changed declaration (`MANIFEST-DRIFT`) — the scope-shrink guard the
Reviewer asked for: deleting the absent rows is visible to any caller that pins the manifest, while the
frozen row-local predicate itself stays what it says. The selftest is `cases=12 red=11` and the mutant
matrix `9/9`. The labrat's H1 (any non-000 status counts as present, including 404/500, and identity is
never checked) is **confirmed and kept as a stated limit**: the frozen claim promises an HTTP status, not
service identity; `SURFACE … present (http=404)` is the honest verdict under it.

**R76-C2 (`ConnectorR76`).** An ancestor `close_commit` is not provenance: R75-D6's close named
`6977019b`, an ancestor that does not contain the receipts (they landed in `f0d52322`). Each row now
carries `evidence_path` + `evidence_literal`; the leg reads the file **at that commit** and requires the
literal there (`NO-EVIDENCE-FIELD`, `EVIDENCE-ABSENT-AT-CLOSE`, `EVIDENCE-LITERAL-MISSING`), and the
`close_commit` of D5/D6 is corrected to `f0d52322` where their evidence actually landed. The selftest is
`cases=11 red=10` and the mutant matrix `9/9`.
