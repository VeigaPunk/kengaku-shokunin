author: kengaku (L1 KengakuR90, hyaku run 15 attempt 1)

# Kengaku round 90 — lesson

Lane `kengaku-shokunin`, branch `master`. Frozen claims commit A `45171d23` (`plans/round-90-claims.md`, `plans/round90-cases.json`); instruments and external pin ledger commit B `664435cf`; receipt and ledger flip commit C `a2b22609`; the measured tip and the triage/source commits are named in LOG.md and the round report. Wave evidence: `.ufo/waves/round-90/w1/` (12 seats).

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened here, with URL, access date and a located quote).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S279 `merge-diff-arc-agi-task/tests/test_outputs.py` @ `2fd12b88` (member replay only) | **admit** (tier A, scope `member replay only`) | 2026-11-05, HTTP 200, 3034 B, sha256 `2754ba6c…85c149`, byte-identical to the round-52 capture (`cmp`) | line 13: `assert git_path.exists(), "Git repository does not exist in /app/repo"` (12 words) | the captured module defines five named test functions (lines 10, 16, 34, 40, 52) over a git repository, `algo.py` and `/tests/test.json`; it is the sole source of the eight frozen predicted vectors (`plans/round90-cases.json`), so the claim rests on it | the pinned grader bytes change at `2fd12b88` |
| S280 `merge-diff-arc-agi-task/tests/test.sh` @ `2fd12b88` (harness wrapper) | **reject** | 2026-11-05, HTTP 200, 620 B, sha256 `c9052954…ab8af8ab9d2`, byte-identical to the capture | line 5: `apt-get install -y curl git` (network install); line 18: `uvx \` (pytest run) | the wrapper adds no grader semantics beyond `test_outputs.py` (S279), and its replay needs apt, curl and uv over the network, which the offline replay forbids | a claim about verifier-harness behaviour (reward.txt mapping, pytest exit semantics) opened as its own replay with the network legs pinned |

The scout seat's independent gate note (`.ufo/waves/round-90/w1/ScoutS279/`) is a second reading of the same bytes; this lesson's rows rest on this lane's own fetch above.

Round-start census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`): exit 0, `kengaku ok`, 270 rows. Round-end census: recorded in LOG.md with the rows after S279/S280.

Spot-check (LEARNING.md discernment, round 89's routed defect R89-D4): this round logs one admit and one reject with reasons above; the non-author check of these gate decisions is the round-90 verifier spot-check, not this lesson.

## Mistakes

Class · evidence pointer · captured-by · fix. Each fix is named with the evidence it was shown against; fixes that are not yet able to fail are routed, not claimed.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **unwired-tripwire** | `plans/routed_open.py` (round 41) and 133 rows in `corpus/routed-findings.jsonl`; no freeze step calls it. At BASE `python3 plans/round90_burndown.py --lane . --rev dcdd494e… --work DIR --freeze-round 90` → `freeze=refused oldest_pending_round=39 pending=33 malformed_unresolved=1`, rc 1 (`.ufo/waves/round-90/L1/base-batteries.txt`) | none: the round-39 Q30 lesson wired `order_check.py` into `round_close.py`, never the burn-down | R90-C3 gate `plans/round90_burndown.py` with the freeze rule and a selftest; triage of every pending row (below). The freeze wiring is for round 91 |
| M2 | **schema-drift** | `corpus/routed-findings.jsonl:125` (`R82-F1`): `source` is the prose `corpus/lessons/round-82.md ## Corrections (R81-V2)`; `routed_open.py` reports `DEFECT line=125 source must read <path>:<line>` (`ROWS total=133 invalid=1`) | the validator caught it; nothing read its output | the gate counts an unresolved malformed row as pending; the triage supersedes it with a well-formed row (its status stays open: the QUOTE_RE repair it names never landed) |
| M3 | **prediction-class** | frozen C2 BASE prediction `PIN-MISMATCH absent` rc 1; measured `DEFECT SETUP unreadable plans/counter-pins-r90.json` rc 2 (the pin ledger is absent at BASE). Frozen C1 BASE prediction `defects=5`; measured `defects=10`; frozen C3 BASE prediction `pending=27`; measured `pending=33` | Q66 checked the figure's source, not the exit class or the count | recorded as mispredicts in SCORECARD and the report; the frozen text is not repaired. Fail-closed holds on C2 (rc 2, no pass line) |
| M4 | **frozen-text self-contradiction** | `plans/round-90-claims.md` states the tip's `git diff --stat B tip -- plans/` must print nothing; the frozen C1 predicate requires the ledger flip (`plans/grader-population-ledger.json`), which lands at commit C after B | none | disclosed in the report and an L0 question; the pinned counters are byte-identical to B at every later tip (checked by C2 and `git diff`) |
| M5 | **predicate-implementation gap** | the frozen C2 predicate conjoins "the selftest battery exits 0"; `plans/round90_counter_pin.py` runs its selftest only under `--selftest`. The frozen C3 predicate requires "at least six seeded rows with opened_round in 83–89"; the gate prints `seeds_83_89=N` and does not gate on it. The gate's PREDICATE also requires zero DEFECT lines, so a malformed row that a valid resolution supersedes still blocks pass (ExecC3Triage: "C3 PASS IS UNREACHABLE"; SentinelForge FE-1) | the wave's ReviewerPredicate and ExecC3Triage seats, both attacking predicate-vs-implementation identity | **not repaired after scoring.** Both pinned counters are in C2's pin set and the frozen kill rule voids C2 on any post-B edit. The C2 conjunction and the C3 seed count are evaluated from the counter outputs and stated as such in the report. The fix goes to round 91 under a new frozen predicate |
| M6 | **format drift in a smoke run** | the first probe smoke joined observed letters with `/` (`observed=P/P/P/P/P`) against frozen vectors `PPPPP`: content matched, format did not; rc 1, `mismatches=8` | the smoke run itself | `"".join(...)` in `plans/round90_polydiff_probe.py`; the re-run is green (`cases=8 legs=40 mismatches=0`); no frozen artifact was scored in the broken form |
| M7 | **vacuous fixture** | the first C2 selftest T4 (clean green) fixture carried only the counter: `SELFTEST clean-green RED` (red for the wrong reason, a missing pin set) | the selftest itself | T4 carries the six frozen pin paths and the record table; `clean-green green` |
| M8 | **selftest red for the wrong reason** | MutTesterR90 F-C3-1: the C3 selftest case `closed-check-fails` is red by `AttributeError` (the `FileLane` stand-in has no `root`), not by its failing check; the same stand-in breaks every closed-with-check path in the `--file` route | the wave's MutTesterR90 seat (its mutant C3-CFD survives the selftest) | routed to round 91: the selftest must prove the check path can fail, by a red that names the check |
| M9 | **fail-open fallback in the selftest** | `plans/round90_counter_pin.py` `selftest()` reads the record table from `lane_root` and, when absent, substitutes the synthetic bytes `record-v1\n`; ReviewerPredicate reproduced a red T4 from a fleet-root cwd (the invocation was the seat's, not the instrument's) | ReviewerPredicate's trace | routed to round 91: fail closed (a setup defect) when a frozen input is absent |
| M10 | **chain-of-custody gap** | `plans/round90_counter_pin.py` is not in the pin set; SentinelForge H-1: an edit to the checker alone (`elif False`) passes C2 with the pin ledger byte-identical to B. The claim text names the rewrite of the pin ledger as the residual and did not name the checker | SentinelForge (forgery 3b) | disclosed here and in the report; the residual is wider than the claim stated. Routed to round 91: pin the checker, or move the checker's verdict into a pinned gate |
| M11 | **override path lets a close pass its own check** | SentinelForge H-2a and forgery 4b: `plans/round90_burndown.py` runs the resolution row's `check` in place of the base row's (`deciding.get("check") or base.check`); a resolution with `check: "true"` clears a base check. The frozen predicate names "its check", so the override is what the predicate states; the gate cannot judge check quality | SentinelForge | every closed triage row carries its own check, which overrides the base row's check (R42-R2 because its base check is stale; the others because the base check was not the closing evidence). Round 91 prints each override and requires the base check too |
| M12 | **misroot: seat probes written at the fleet root** | `run_check_probe.py` and `run_check_probe2.py` at the fleet root, untracked, written by the ReviewerPredicate seat (their content names its scratch path `/fast/scratch/hyaku/kengaku-r90/ReviewerPredicate/`); the lane's own rule is the seat's absolute-path bound, which these probes did not cross | the misroot sweep before the report (`git -C /home/vgpnk/Projects/shokunin status --porcelain`) | copied byte-exact into the lane at the same relative path (`cmp` ok), committed (`a0d57153`), fleet copies deleted; the seat bound is restated in every wave context |

## Triage of the routed-findings ledger (considerthese item 1, `considerthese/2026-10-26.md`)

The ExecC3Triage seat (`.ufo/waves/round-90/w1/ExecC3Triage/`, 34 resolution drafts, 46 seed drafts, 80 numbered verdicts, 19 receipts) re-derived each pending row's truth against the tree at `a2b22609`. The lane takes its drafts as the record, with the counts below. The six closes are the seat's re-derivations; this lesson does not independently re-verify them, and the round spot-check is the place that samples them:

- **Closed with evidence (6):** R42-R2 (its base check is stale; the close is supported by its children R42-R2.1 and R42-R2.2), R42-R3-33 and R42-R3-37 (judgment closes; residuals carried in the rows), R45-S5-7b, R45-S5-7d, R45-S5-7e (each check re-run today against landed artifacts). R45-S5-7c and R42-R3-09 pass their checks only because the check asserts the defect is present, so they are not closed.
- **Refused, recorded accepted-risk dispositions (23):** the rows' own `disposition: accepted-risk` (the lane's own earlier decision) restated as `refused` with the recorded blocker quoted. This maps the lane's own disposition onto the gate's decided state; it is not a fix, and the freeze count does not measure fixing (SentinelForge H-2c, M-2).
- **Blocked on another owner (4):** R51-R1 (kama), R51-R2 (protocol), R51-R3 (integrator/operator), R51-R4 (kama). Blocked is pending under the gate.
- **Open (1):** R82-F1 — superseded by a well-formed row; status open because the QUOTE_RE repair named in its blocker has not landed.
- **Seed rows for rounds 83–89 (46, report-only in the triage; appended to the ledger as base rows):** 14 closed with a located evidence string, 29 open (no closure located in this pass; not proven absent), 3 blocked. Seeds opened 83–87 that remain open keep the freeze refused under the predicate's "no pending before round 88".

The gate's figures after the triage are measured at the round's tip and recorded in SCORECARD.md (C3 row), not restated here.

## Routed to round 91

1. **Instrument amendments under a new frozen predicate** (none of these is applied to the round-90 counters, which are pinned; the kill rule voids C2 on any post-B edit):
   - C3: a superseded malformed row emits no DEFECT; a freeze is refused whenever any check fails, not only when pending rows are old; checks run once per finding; the seed clause `seeds_83_89 >= 6` is in the PREDICATE line; the `--file` route gives the check runner a `root`; every override check is printed and the base check runs too.
   - C2: the selftest runs inside the predicate path; the checker is pinned (M10); the selftest fails closed when a frozen input is absent (M9); the printed `PIN-OK` the frozen prediction names is either emitted or dropped from the prediction.
   - C1: the `executed=` field of the TARGET line is 1 only when the predicate passes (ExecC1Battery F1).
   - Every selftest case must be red for its named reason (M8).
2. **The C2 pin residual**: the operator decides whether a one-commit rewrite of the pin ledger is acceptable, or the pins need an anchor outside the tree (a signed tag or a receipt outside the repository).
3. **The triage backlog**: the 29 open seeds and the 4 blocked rows need owners or closures; R82-F1 needs its QUOTE_RE repair (`plans/anchor_line_check.py`, round 83's own routed item) with its own counter.
4. **Coverage**: the next offline member from ScoutR89's class arithmetic that the ledger's own captured bytes show offline-clean (the blocked members are network, LaTeX or VM bound and stay blocked).
5. **Assimilation**: none this round. `merge/kengaku/` stays held by L0 `kengaku | round-54`.

## Honest limits of this round's evidence

- The C1 replay grades a lane-authored fixture (the git repository, the algo module and the test input are fixtures), so the eight vectors describe the captured bytes on this host's toolchain, not Terminal-Bench's harness or a real submission. Its receipt stamp's `TOOL_SHA`, `CASE_TABLE_SHA` and `HOST_*` fields are not checked by its legs (SentinelForge forgery 1b passes with a decorative stamp; the frozen legs L1–L8 do not name those fields).
- `test_both_bundles_fetched` greps branch names; the fixture proves name presence, not that a bundle was fetched.
- The triage refusals and closes are the lane's judgments, recorded with their quoted evidence; a non-author check of them is the round-90 spot-check's job.
