# Round 82 — verifier spot-check (kengaku)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC)
lane: `kengaku-shokunin`
base `a3a03ac31451e58f1742b9bccb73b72c2d90a95c` (round-81 verifier spot-check)
lane tip `a44b2f083ee8b4115aea64598646f4bd9e3c1470` (`git -C kengaku-shokunin ls-remote origin
refs/heads/master` → the same hash)
report `.ufo/reports/round-82/kengaku.md` @ `c839b658102dbcc401c78bbb7ea3bb47f11a333d`
dispatch/complete digest (mutable `.ufo/watchdog.log`, copied):
`2026-11-04T06:26:48-03:00 launch kengaku round=82 pgid=619086 driver=hyaku-inline attempt=1`;
`2026-11-04T07:43:05-03:00 complete kengaku round=82; hyaku-inline attempt=1`.

This file is integrator work, not lane work: I did not author the round and changed no lane-authored
file. Every number below was re-derived by me over committed bytes (`git show`, `git archive`,
`grep`, `awk`, `python3`), never by executing the lane's counters: the Gate standard's Closure
consequence binds the integrator to verify a gate's committed evidence, never to run a sibling's
gate. The commands below are the re-runnable form.

## 1. Step-1 conformance

| item | result |
|---|---|
| report identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-82/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> c839b658 round-82: kengaku report`. Committer time `2026-11-04T07:42:20-03:00`, 54 s after the cited lane tip `a44b2f08` (`07:41:26-03:00`): the report lands last. (The author date `07:39:50` is the jj change's creation time preserved by `export from jj`; the shipped bytes postdate the tip.) |
| SHONEN heading | `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box, each with a path pointer; no `[x]` |
| cited commits | 4/4 exist and are ancestors of `master`: `12f1029a`, `c804dd41`, `82fe89d5`, `a44b2f08`; `git merge-base --is-ancestor <hash> master` returned 0 for each (`a44b2f08` is the tip itself) |
| lane state | `jj-lane.sh state` → `branch=master local=a44b2f08… remote=a44b2f08… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty — no uncommitted round work |
| prompt fidelity | `.ufo/prompts/kengaku-round-82.md` (704 lines, committed @ `fcf16865`) carries sections 1–5 of the shipped template — mission/axes binding, claims, the frontier step, `## 3` L2 floor `at least 8 L2 subagents in ONE batched AgentSwarm call`, `## 4` report contract with the required sections and the `SHONEN` heading, `## 5` commit-then-push and push scope and the L0 side channel — plus the hyaku §6 addendum. The five child-lane items are present: report path `…/round-82/kengaku.md`, commit-before-report, `SHONEN` heading check, commit-hash citation rule, lane write scope. L2 floor 8 matches `MISSION.md` §L2 concurrency; the run-15 addendum routes roles through the host table; the wave is 12 seats, inside `ufo-wave-policy.json` `waveMinLanes=8`/`waveMaxLanes=16` |
| wave | one v1 wave: `w1-dispatch.json` 12 items, `w1-results.json` `seats=12` / 12 rows / no residual `task` call; roles executor 5, scribe 2, scout 1, connector 1, reviewer 1, critic 1, mutation-tester 1. Attack seats 3/12 = 25.0 % (campaign list reviewer/critic/mutation-tester/labrat) ≥ 25 %; connector 1 ≤ 2. Two seats have no structured result (`SweepGateR82` empty, `RegistryCounterR82` a partial transcript), both named dead in the report and carried by the L1 |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN — the contract's sections in order, then Round shape/Extras |
| marker vs report | not a marker: 207 lines, three claims each with a counting command and a committed receipt, evidence pointers per work item, all required sections present |

No step-1 defect bars admission. The evidence-standard defects found are routed in §6.

## 2. Claims — re-derived, not evidence-read

### R82-C1 / coverage — the registry's unmeasured direction

A 40-line `python3` replica of the counter's `parse_rows` (line starts `| \``, `strip('|').split('|')`
== 8 cells) run over `git show BASE:TIP` bytes:

```
UNIVERSE documents=3 instruments=313 referenced=133 registered=131 base_scripts=138   # BASE a3a03ac3
UNIVERSE documents=3 instruments=313 referenced=133 registered=141 base_scripts=144   # TIP  a44b2f08
ROWS registry=143 base=133
MISSING 0 / UNCLASSIFIED 0 / excluded=2 (plans/fixture_fence.py, plans/policy_cases.py)
entry scripts absent at BASE: only the four round-82 counters (present at TIP)
```

Both header lines reproduce `c1-before.txt:1` and `c1-final.txt:1` character-for-character. The six
base defects are byte-classified from base bytes (`git show a3a03ac3:<path> | grep -c argparse|'if __name__'`):
`fixture_fence.py` 0/0 and `policy_cases.py` 0/0 (support modules → exclusions); `log_appendonly.py`
2/1, `round37_c1_attribution.py` 2/1, `round66_registry_check.py` 3/1, `round80_c1_remint.py` 2/1
(CLI → rows). Ten rows added, all eight cells non-empty, all entry scripts present at the tip:
`log-appendonly`, `round37-c1-attribution`, `round66-registry-check`, `round80-c1-remint`,
`round81-log-summary-probe`, `round81-vulnerable-secret-probe`, `round82-c3-sweep`,
`round82-c1-plans-registry`, `round82-c2-closure-debt`, `round82-c2-checks`. **Verified: before
`DEFECTS n=6` (`missing=4 unclassified=2`) → after `missing=0 unclassified=0 excluded=2 rows=143
entry_missing=0`.** The claim's counter receipts (`c1-selftest.txt`: `cases=8 red=7 failures=0`;
`c1-mutants.txt`: `real=7 killed=7 survived=0`; `c1-controls.txt`: three `target_reached=False`)
were read, not executed.

### R82-C2 / calibration — the round-81 spot-check's V1…V7 discharged

```
UNIVERSE spot-check lines carrying V1…V7: corpus/lessons/round-81-verifier-spotcheck.md:195,200,205,208,211,213,218
rows R81-V1…R81-V7: 7, all status=closed, close=corpus/lessons/round-82.md ## Corrections (R81-V<n>),
  evidence_literal present in both close artifact and evidence_path: 7/7
corpus/README.md indexes the round-81 spot-check: yes
BASE: R81-V rows 0 (routed-findings 117 rows), README index no, WORKTREE dirty, no provenance trio,
  docstring Six vs battery real=4, determinism.txt without COMMAND/REV
```

Every `source` line number equals the spot-check line that carries that id; every `evidence_literal`
recomputed in its artifact. The sensitivity leg's committed receipt is `SENSITIVITY n=7
failed_at_base=7` (`c2-sensitivity.txt`), and I re-derived each base-side failure independently: u1
base receipt reads `WORKTREE dirty (1 paths)`; u2 base has no S265/S266; u3 base entry has no
`source:`/`verified-at:`/`recheck:` head; u4 base docstring says `Six` while `MUTANTS` holds 4 (tip:
6); u5 base lesson carries no `--lane/` record and the untracked dir is absent from any tree; u6 base
has no `.ufo/waves/round-82/w1-results.json`; u7 base `determinism.txt` has neither `COMMAND` nor
`REV`. **Verified: base `DEFECTS n=8` → tip `ids=7 closed=7 checks_passed=7 indexed=yes`,
`DEFECTS n=0`.** Batteries read, not executed: `cases=7 red=6 failures=0`, `real=6 killed=6
survived=0`, control `target_reached=False`.

### R82-C3 / capability acquisition — `sweep-at-one-tip`

```
ledger statuses: executed=26 unexecuted=62; map keys == executed set: True (26/26, no extras)
sha256(plans/round82-sweep-map.json)    = 7afc34ba…1ce0fbaf  (receipt line 2, and identical at c804dd41 and tip)
sha256(plans/grader-population-ledger.json) = 15fb159d…387e1f44 (receipt line 3, identical at both)
sweep.txt MEMBER lines 26, unique names; statuses reproduced=18 diverged=7 unrunnable=1
PROJECTION lines 26; HISTOGRAM status total=26; HISTOGRAM-CLASS sum=59
divergence counts 25+50+12+30+6+12+10 = 145 over 7 members
```

The receipt was minted from a clean `git clone --shared` at `c804dd41` (`LANE_TIP`, `WORKTREE
clean`), and the map/ledger bytes it pins are unchanged at the tip, so the census applies to the
cited tree. `c3-check.txt` at the tip reports `TARGET members=26 located=26 status_lines=26
histogram_total=26 mismatches=0`, `PREDICATE R82-C3 pass`. `determinism.txt` carries two `COMMAND`
lines, a `REV`, and `disagreements=0`, with the harvest seat's independent two-pass projection
recorded and its different observation source explained (not averaged). Batteries/controls read:
`cases=12 red=11 failures=0`, `real=11 killed=11 survived=0`, three `target_reached=False`. The
capability row enters `SCORECARD.md` in the same round with a passing demonstration: yes.

## 3. Discernment spot-check (LEARNING.md)

Sample: both admits and the round's single reject, re-opened live at the pin (2026-11-04, UTC), plus
the two supersede rows recomputed.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S262 · TB2 per-task grading entry (`log-summary-date-ranges/tests/test.sh`) | admit, tier A | live `curl` of `…/2fd12b88…/log-summary-date-ranges/tests/test.sh` → HTTP 200, 608 B, sha256 `4770437ea96c…c334`; identical to the committed capture and to `sqlite-with-gcov`'s | **agree** on the admit; **disagree** on the stated length (`6 words`, S262 anchor and lesson Gate:25) | the quote at `:18-22` is verbatim and the `reward.txt` line is at `:26`; the second quote is 4 whitespace-split tokens, not 6 — the row's own convention (V2 of round 81) is that a stated count recomputes |
| S263 · same entry, request variant (`nginx-request-logging/tests/test.sh`) | admit, tier A | live `curl` → HTTP 200, 634 B, sha256 `27761195f53c…52e7`; quotes at `:20` and `:22` verbatim | **agree** on the admit; **disagree** on `1 word` for `-w requests==2.32.4` (lesson Gate:30) | it is 2 whitespace-split tokens; the source, tier, scope and `teaches` all hold |
| S264 · harness `pyproject.toml` at the pin | reject, kept with flip | live `curl` → HTTP 404, 14 B `404: Not Found`; `run-tests.sh` and `tests/run-tests.sh` also 404/14 B | **agree** | no locator, no anchor; the reject states the flip (a revision that carries the file) and does not claim the harness has no packaging |
| S265/S266 · supersede rows for S260/S261 | admit as supersede | receipt bytes and the two pinned instruction lines recomputed | **agree** | S265's quote is 7 tokens (claimed 7), S266's are 12 and 13 (claimed 12/13); S260/S261 keep their bytes (Q34) and `anchor_line_check`'s blind spot is itself routed as R82-F1 |
| R82-F1 · gate blind spot (open row) | routed by the lane's own connector | `plans/anchor_line_check.py` `QUOTE_RE` + the four affected rows | **agree** | the row is open with a blocker and a check; it is the round's own catch, not a self-clean |

The census gate: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → `rc=0`, final line `kengaku ok …/corpus/SOURCES.md`, **27
`W04`** lines (see V2 below). `corpus/SOURCES.md` rows 253 → 258 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`),
5 additions / 0 deletions, no malformed row (`NF!=13` → 0).

## 4. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | registry audit 6 defects → 0 over a derived 133-instrument universe; four CLI instruments rowed, two support modules excluded on byte proof; rows 133 → 143; score held 7 at the L0 cap by declaration |
| calibration | **improved** | the round-81 spot-check's seven routed ids registered, closed, evidence-resolving and base-failing (re-derived above); `SENSITIVITY n=7 failed_at_base=7`; score held 10, exercised |
| freshness | **improved** | the capability claim lands a population-wide measurement the lane did not have: 26/26 executed members replayed at one tip, 18 reproduced / 7 diverged / 1 unrunnable, deterministic across two runs; score held 10 |
| depth | unchanged | five tier-A SOURCES rows (S262/S263 live-verified, S264 live-rejected, S265/S266 recomputed) and one new knowledge entry (`tb2-replay-sweep-at-one-tip.md`); score held 10 |
| operability | unchanged | three new gates with selftest/mutant/control receipts (evidence-verified, not executed); score held 10 |
| adjacency | unchanged | `ConnectorR82` sibling scan found no duplicate registry/spot-check/sweep gate and no SOURCES id/URL collision; no cross-domain artifact absorbed; score held 9 |
| novelty | unchanged | three instruments, no new domain construct claimed; score held 8 |

No axis harmed: `git diff a3a03ac3 a44b2f08 -- SCORECARD.md` is `64 0` (append only), and every score
line at the base is unchanged in value (coverage 7, calibration 10, operability 10, depth 10,
freshness 10, adjacency 9, novelty 8).

## 5. Trend verdicts

- **expansion: improved.** Five tier-A registry rows enter (three admitted, one rejected-and-kept,
  two supersede rows), one new knowledge entry lands on uncovered ground
  (`knowledge/tb2-replay-sweep-at-one-tip.md`, citing the round's own S262/S263/S264), and the
  executed population gains its first full replay census (26 members, each status named). Rows
  253 → 258; census rc 0.
- **quality: improved.** Three gates land with selftest + mutant + control batteries; seven round-81
  repair debts are discharged with checks that fail on the base tree; the round catches two of its
  own defects mid-flight (M82-2's pipe-split row, M82-1's probe sidecar writes) and routes its own
  gate blind spot (R82-F1). The fresh count-annotation defects (V1) are record defects routed below,
  not admitted-entry falsifications: the admitted rows' `source`, `anchor` quotes, tier and `teaches`
  all verify.
- **discernment: improved.** The outside spot-check agrees on both admits and the reject (V1's
  disagreement is with a count annotation, not with the gate's decision to admit); the round refused
  to call a 7-diverged, 1-unrunnable sweep green, explained the two implementations' different
  observation source instead of averaging, and reported the V2-versus-Q34 locus deviation against its
  own frozen sentence. The record-accuracy blemishes (V1–V8) are calibration debt routed, not
  unlearned gate disagreements.

## 6. Routed defects (the lane must correct next round)

- **V1 · two fresh quote count annotations do not recompute.** S262's `anchor` says
  `"echo 1 > /logs/verifier/reward.txt" (6 words)` — 4 whitespace-split tokens; S263's says
  `"-w requests==2.32.4" (1 word)` — 2 tokens. The same numbers repeat in
  `corpus/lessons/round-82.md:25,30` and the report's Sources & frontier. This is the exact V2 class
  the round discharged; `plans/round82_c2_checks.py:u2` scans only S265/S266 and the round-81 lesson,
  so it cannot see them. Fix as supersede rows (Q34) plus a dated correction, and extend the u2 scan
  to the round-82 Gate rows.
- **V2 · the report's after-census W04 count is wrong, and no after receipt is committed.** Report
  line 151 says `26 W04` after; at `a44b2f08` the validator prints **27** (the 27th is S266's
  duplicate of S261's URL). `corpus/evidence/round82/` holds only `census-before.txt` (26), while
  `corpus/README.md:966` describes "the census before/after". Commit the after capture and state 27,
  or drop the row.
- **V3 · the dead/revived seat count contradicts its own list.** `LOG.md:3206` and
  `SCORECARD.md:3884` say "Five seats died"; the LOG sentence then names **six** seats
  (`SweepGateR82`, `SweepHarvestR82`, `ReviewerR82`, `CriticR82`, `MutationR82`,
  `RegistryCounterR82`), and the report says two never recovered + four revived (= six affected).
  Reconcile with a counting command over `w1-results.json`/the mission log.
- **V4 · Landed-changes attribution names a commit that does not carry two files.**
  `plans/round82_c2_closure_debt.py` and `plans/round82_c2_checks.py` were added at `82fe89d5`
  (`git log --diff-filter=A`), not `c804dd41` as the report's Landed changes row and `LOG.md:3172`
  say. Correct through a new LOG/lesson entry naming the superseded sentence.
- **V5 · the round-82 lesson is not indexed and the spot-check index row is malformed.**
  `corpus/README.md` has no `lessons/round-82.md` row (`grep -n round-82` → only the evidence bullet),
  while the report's SHONEN box 3 says the README indexes it; and README:931 (the
  `round-81-verifier-spotcheck` row) carries two cells in a three-column table. Add the row and the
  missing cell — the lane's own `plans/round75_c1_index_parity.py` is the check.
- **V6 · `## Gate` does not enumerate the two new supersede rows, and S264's `teaches` shape is off
  contract.** SOURCES rule 1 requires the Gate to record, for **every** new row, URL, access date and
  a located quote; S265/S266 appear only under `§Corrections`. S264's `teaches` cell also omits the
  contract's `REJECTED: <reason>; flip: <what would change the verdict>` shape (the reason sits in
  `scope`, the flip in the lesson).
- **V7 · SHONEN box 1's pointer overstates the new rows.** It says the ten added rows each carry a
  self-test, but `round37-c1-attribution`, `round80-c1-remint` and `round82-c2-checks` declare
  `none declared` (the round's own `c1-final.txt` prints `selftest=none` for them).
- **V8 · report time units mix local and Z.** `RegistryCounterR82 (died ~07:24Z)` precedes the
  launch `06:26:48-03:00` (= `09:26:48Z`) by two hours; the value is local time written with a `Z`
  suffix. State one convention.

Observations (not defects): four pre-existing registry rows (`round63-c1-pypi-probe`,
`round63-gate-checks`, `round64-c1-kvstore-probe`, `round64-trio-sweep`) omit the closing `|` at both
base and tip — legal GFM, but counted only because the parser strips a missing terminator; the
`R80-U1` routed-findings line was re-encoded (literal Unicode → `\u` escapes, content identical);
the round-81 lesson's two counts were corrected in place, which lessons permit as lane-owned files
but the SOURCES discipline did not — state the rule next round.

## 7. Promotion note

`SHONEN.md` still carries four `[~]` assertions and no `[x]`: the lane has not claimed a non-author
verification, and promotion remains operator-owned. This spot-check did not write any mark into
`SHONEN.md`. Boxes 2 and 4 now have checkable evidence (the sweep census + LOG entry; the connector's
sibling scan), so a non-author promotion review is executable; boxes 1 and 3 still rest on the
registry and lesson-index debt above.
