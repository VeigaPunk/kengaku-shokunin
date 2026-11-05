# Round 91 — frozen claims (kengaku)

Frozen in commit A (this file and `plans/round91-cases.json`), before any instrument, receipt or
score exists. Base: `59764383d4dd33d58faa50daad4c06d0cde410aa` (round-90 verifier spot-check
landing, `master`). Measured tip: the commit that lands the receipt, the ledger flip, the triage
resolutions and the source rows — never a commit whose pinned bytes changed after the first
score. Pinned-set tip rule (scoped, fixing the round-90 self-contradiction M4): at the measured
tip, `git diff --stat B <tip> -- plans/round91_modernize_probe.py plans/round91_c1_replay.py
plans/round91_counter_pin.py plans/round91_burndown.py plans/round91_f1_counter.py
plans/anchor_line_check.py plans/round83_c2_checks.py plans/counter-pins-r91.json
plans/round91-cases.json plans/round-91-claims.md` must print nothing;
`plans/grader-population-ledger.json` and `corpus/routed-findings.jsonl` are exempt by name
because C1 requires the ledger flip and C3 requires the triage rows. Nothing below may be edited
after freeze; a frozen element that looks wrong is reported, not repaired.

Three claims, causally separable: C1 reads the replay surface (grader bytes, case table, probe,
receipt, ledger row); C2 reads pin/counter bytes at a revision and the case-table blob; C3 reads
`corpus/routed-findings.jsonl` and its own gate output. No claim reads another claim's receipt
or evidence. Shape: ONE v1 wave, 8–16 seats, attack seats ≥ 25 %, at most one connector seat.

Measurement note (Q66/Q67 applied to this file): every BEFORE figure below is a prediction until
the do-nothing control measures it at BASE. Measured figures are recorded in the report; a
mismatch between a prediction and the measured figure is recorded as a mispredict, never repaired
in place. Every count whose unit is host-defined is predicted with its formula, never as a bare
number (round-90 M3 class: the frozen `legs=8` prediction vs measured 40).

## R91-C1 — coverage (lowest non-retired axis, held at its L0 cap 7): a ninth located offline replay, `modernize-scientific-stack`, with the round-90 C1 instrument defects closed

**Move:** a located offline replay of the Terminal-Bench 2.0 grader `modernize-scientific-stack`
by the round-91 counter `plans/round91_c1_replay.py` over the frozen ten-case table
`plans/round91-cases.json`, with the probe bytes pinned by sha (`TRUSTED_TOOL_SHA` in
`plans/counter-pins-r91.json`). The captured grader
(`corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py`, sha256
`0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977`) defines two test functions
over a staged `/app`: `test_modernized_code_runs` (lines 16–42: script exists, CSV exists, the
script runs with exit 0, stdout names Station 101 and Station 102 and the phrase
"mean temperature", and the parsed means land within 0.1 of −15.5 and 30.3) and
`test_dependency_file_exists` (lines 45–48: `/app/requirements.txt` or `/app/pyproject.toml`
exists). The member carries classes `file-artifact`, `filesystem-metadata`, `numeric-band`,
`stdout-inspection`, `subprocess-exec`; `filesystem-metadata` (2 of 10) is the ledger's thinnest
executed-fraction class and has not moved since the round-80 freeze — this is its first executed
member. The case table adds a tolerance-boundary pair and a timeout class (E leg) the executed
set has not held. The round-90 routed defects closed inside this claim: the TARGET line's
`executed=` field is 1 only when every leg passes (r90 ExecC1Battery F1); the receipt stamp's
`TOOL_SHA`, `CASE_TABLE_SHA`, `HOST_PYTHON`, `HOST_OPENSSL` and `HOST_USERNS` are checked by leg
L9 (r90 SentinelForge forgery 1b passed with a decorative stamp); a sandbox outage at the L6
re-run is `DEFECT SETUP sandbox-unavailable` + `PREDICATE could-not-evaluate` exit 2, never a
silent pass (r90 CriticFalsify F-7); legs are predicted with their formula, 10 cases × 2
functions = 20 (r90 M3).

- **Before (BASE `59764383`, predicted):** `TARGET executed_rows=34 member=modernize-scientific-stack located=1 executed=0 cases=0 legs=0 mismatches=0 defects=N`, `PREDICATE R91-C1 fail`, exit 1, where N is measured by the do-nothing control (predicted class: fail-closed absences — receipt absent at BASE, case table absent at BASE, member unexecuted in the ledger, pin ledger absent so L8 cannot read a `TRUSTED_TOOL_SHA`). Ledger at BASE (measured 2026-11-05 by `python3 -c` over `plans/grader-population-ledger.json`): members 88, executed 34; `filesystem-metadata` 2 of 10; `numeric-band` 3 of 10; `stdout-inspection` 10 of 29; `file-artifact` 25 of 76; `subprocess-exec` 12 of 45.
- **After (measured tip, predicted):** `TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=1 cases=10 legs=10*2=20 mismatches=0 defects=0`, `PREDICATE R91-C1 pass`, exit 0. Ledger: executed 34 → 35 of 88; `filesystem-metadata` 2 → 3 of 10; `numeric-band` 3 → 4 of 10; `stdout-inspection` 10 → 11 of 29; `file-artifact` 25 → 26 of 76; `subprocess-exec` 12 → 13 of 45.
- **Legs (frozen list L1–L9):** L1 the receipt `corpus/evidence/round91/modernize-probe.txt` exists and is committed at the measured revision; L2 the captured grader bytes at the measured revision hash to `0c24195f…02a977` and the receipt's `SUBJECT_SHA` equals it; L3 the receipt's `LANE_TIP` is an ancestor of the measured revision (`git merge-base --is-ancestor`); L4 `plans/round91-cases.json` at the measured revision is byte-identical to the freeze commit A's; L5 every case's receipt-observed vector equals its frozen predicted vector; L6 the probe re-run from an extraction of the measured tree reproduces the receipt observation block (a missing or failing sandbox is a SETUP defect with exit 2, never a pass); L7 the ledger at the measured revision carries `modernize-scientific-stack` `executed` round 91 with the after-cell values above; L8 the probe bytes at the measured revision hash to the counter's `TRUSTED_TOOL_SHA` pin in `plans/counter-pins-r91.json`; L9 the receipt's `TOOL_SHA` equals the probe bytes' hash at the measured revision, its `CASE_TABLE_SHA` equals the case-table hash there, and its `HOST_PYTHON`, `HOST_OPENSSL` and `HOST_USERNS` equal the host's current `python3 -V` first line, `openssl version` first line (or `absent`) and `/proc/sys/user/max_user_namespaces`.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R91-C1` line and the report):** pass iff legs L1–L9 all pass at the measured revision, and the TARGET line prints `executed=1` only in that case — while the same counter at BASE exits 1 printing `PREDICATE R91-C1 fail`.
- **Kill rule:** any leg L1–L9 failing at the measured tip makes the claim unmet; so does any mismatch between the probe re-run and the receipt, and so does a probe whose bytes differ from `TRUSTED_TOOL_SHA`. A TARGET line printing `executed=1` alongside any failing leg is a defect the claim does not survive. Editing the case table or this file after commit A voids the claim.
- **Controls:** do-nothing = the counter at BASE must exit 1 with `PREDICATE R91-C1 fail`. Ledger-only control (ledger row flipped, receipt absent) must fail at L1. Forged-tip control (receipt `LANE_TIP` replaced by a commit that is not an ancestor of the measured revision) must fail at L3. Forged-stamp control (a receipt whose `TOOL_SHA` names bytes that do not match the probe at the measured revision) must fail at L9. Decorative-stamp control (a receipt with the right `TOOL_SHA` but a `HOST_PYTHON` line no interpreter prints) must fail at L9. Executed-gating control (a failing receipt whose recorded TARGET carries `executed=1`) must make the counter exit 1. Separation: reverting C2's pin ledger leaves the C1 counter's verdict unchanged except at leg L8, which reads only the probe pin and is exercised positive at the measured tip; reverting C1's receipt and ledger row leaves C2's verdict unchanged. Each control's exit code and defect lines are committed under `.ufo/waves/round-91/` before the measured tip is scored.
- **Sourced:** the grader bytes are row `S281` in `corpus/SOURCES.md`, opened in this round: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py` (live fetch 2026-11-05, HTTP 200, 2330 B, sha256 `0c24195f…02a977`, byte-identical to the round-52 capture by `cmp`; located quote recorded in the round lesson's `## Gate` before admission).
- **Honest limits:** (a) the ten cases yield three distinct predicted vectors (`PP`, `FP`, `PF`) — the discriminating content is which assert fires and the E-leg timeout, not the two-letter shape; (b) the vector is a statement about the captured bytes plus this probe harness on this host's toolchain (python 3.14.8, bwrap 0.13.1), not about Terminal-Bench's own harness; (c) the graded state is lane-authored (script, CSV, dependency file are fixtures), as in every replay of this series; (d) the probe stages case trees read-only into a bwrap namespace bound at `/app`; it never writes the host `/app`; (e) the counter is pinnable by one commit that also rewrites the pin ledger — the disclosed C2 residual, narrowed by the checker self-pin but not eliminated.

## R91-C2 — calibration (held at ceiling 10): the pin set extended to the checker itself, the selftest inside the predicate path, and fail-closed absence

**Move:** `plans/counter-pins-r91.json` + `plans/round91_counter_pin.py`. Round 90's disclosed
residuals (SentinelForge H-1: a checker-only edit passes C2; M9: the selftest substituted
synthetic bytes for an absent record table; M5: the selftest ran only under `--selftest`, outside
the predicate path) are closed here under a new frozen predicate. The pin ledger carries: sha
entries for the six round-90 pinned counters (carry-forward: `plans/round88_claim_figures.py`,
`plans/round89_c1_replay.py`, `plans/round89_claim_figures.py`, `plans/round90_c1_replay.py`,
`plans/round90_polydiff_probe.py`, `plans/round90_burndown.py`), sha entries for the five
round-91 instruments plus the two repaired repair-targets (`plans/round91_c1_replay.py`,
`plans/round91_modernize_probe.py`, `plans/round91_counter_pin.py` — the checker's own entry,
`plans/round91_burndown.py`, `plans/round91_f1_counter.py`, `plans/anchor_line_check.py`,
`plans/round83_c2_checks.py`), and blob entries for `plans/round89-q66-records.json` (blob
`163f284316141a831484dacb7f69ad4cbbaadfb3`, anchor `0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619`,
carry-forward), `plans/round90-cases.json` (blob at the round-90 freeze commit `45171d23…`) and
`plans/round91-cases.json` (blob at this round's freeze commit A). The checker verifies, at any
revision, that every listed path's bytes there hash to its pin (an absent path is a
`PIN-MISMATCH absent`, never a skip — M9), that every blob entry's blob id at the measured
revision equals the pin and exists at its anchor commit, that the checker's own running bytes
(`Path(__file__)`) match its own pin, and — in the same default run, before the PREDICATE line —
that its selftest battery is green on the unmodified tree and red for every case's named reason
(M5: the selftest runs inside the predicate path; Q69: every red names its defect).

- **Before (BASE `59764383`, predicted):** `python3 plans/round91_counter_pin.py --lane . --rev 59764383… --work DIR` exits 2 printing `DEFECT SETUP unreadable plans/counter-pins-r91.json` and `PREDICATE R91-C2 could-not-evaluate` (fail-closed on the absent pin ledger — never an awk zero, never a synthetic substitute).
- **After (measured tip, predicted):** the same command at the measured tip exits 0 printing one `PIN-OK <path>` per pinned entry, `PINS checked=K matched=K mismatched=0`, `SELFTEST cases=C red-green-ok=C` and `PREDICATE R91-C2 pass` (K and C printed as measured; K is predicted as 13 sha entries + 3 blob entries = 16, C as 6 fixture cases — both are predictions until measured).
- **Predicate (one sentence, identical in this file, the checker's `PREDICATE R91-C2` line and the report):** pass iff at the measured revision every path in `plans/counter-pins-r91.json` exists there and hashes to its pinned sha256 (an absent path is a mismatch, never a skip), every blob entry's blob id at the measured revision equals its pin and the blob exists at the entry's anchor commit, the checker's own running bytes match its own pin, and the selftest battery run in the same invocation exits 0 with every declared red case red for its named reason while the unmodified tree is green.
- **Kill rule:** any `PIN-MISMATCH` at the measured tip; any selftest case that stays green or is red for a reason other than its named defect; any edit to a pinned file, the pin ledger or this file after commit B; any edit to `plans/routed_open.py` (round-41 instrument, out of scope by name). An adversary who can write the tree can still rewrite the checker and its pin entry together in one commit — that residual is narrowed (the running bytes are checked against the pinned revision bytes) but not eliminated (commit B itself is only anchored by this frozen file and the pushed history), and is not hidden.
- **Controls:** do-nothing at BASE (above). Able-to-fail = the selftest's own red cases (a two-commit fixture repo whose second commit mutates one pinned counter byte, one pinned blob's content, or deletes one pinned path, each must print the named mismatch and exit 1), plus a tampered-pin fixture (a pin value edited in an otherwise green ledger must mismatch). Positive = the unmodified tip green. Separation as in C1.
- **Axis note:** calibration held at its ceiling of 10 (round-86/87/88/89/90 precedent): a count move at the ceiling is recorded, not added to the score.

## R91-C3 — operability (held at ceiling 10) + capability: the amended routed-findings freeze gate admits, and the backlog is burned down to owned states

**Move:** `plans/round91_burndown.py` (successor gate; the round-90 counters are pinned and are
not edited) plus the triage that takes the ledger to the admitted state. The round-90 gate's
routed defects closed inside this claim: a well-formed resolution that supersedes a named-invalid
row clears it and emits no DEFECT (r90 `PASS IS UNREACHABLE` / FE-1); the freeze verdict is
`refused` whenever any check fails, not only when pending rows are old (r90 ExecNoWork: `admitted`
printed with check failures); the seed clause is computed inside the PREDICATE, not only printed
(r90 M5); every check override is printed together with its base check's result and requires a
non-empty `override_reason` (r90 SentinelForge H-2a/M11); the `--file` route gives the check
runner a real root so its selftest exercises the same read path (r90 MutTester F-C3-1, Q63/Q69);
checks run once per finding, not once per row (r90 routing item 1); every selftest case is red
for its named reason (Q69). The gate's decided-state mapping (frozen here, before data; the
operator's L0 answer is routed around, not assumed): `pending` counts effectively-open rows only;
`blocked` rows are parked, not pending, and every blocked row must carry a non-empty `owner`
naming the lane or seat that holds the fix; `refused` rows stay decided (the round-90 record
stands; the L0 `kengaku | round-90` triage-mapping question stays open and this round does not
reclassify those rows). The freeze rule for round N: refuse while any effectively-open finding
was opened before N−2, or any blocked row lacks an owner, or any check failed, or any malformed
or schema-invalid row is unresolved. The burn-down this round: resolutions for the 29 open seeds
opened 83–87 and 89 (closed with a located evidence string, refused with a quoted standing
blocker, or re-owned as blocked+owner), the four blocked R51 rows named to their owners
(kama×2, protocol, integrator/operator), `R82-F1` closed by the QUOTE_RE repair
(`plans/anchor_line_check.py` learns the curly-quote and `line N` anchor shapes; its own counter
`plans/round91_f1_counter.py` proves the four blind-spot rows S260/S261/S265/S266 now parse and
the cited set includes them), `R82-V8`'s path-dependent check repaired (`plans/round83_c2_checks.py`
derives the fleet root from the lane root's parent, not `origin.parent`; the resolution row's
check passes from a clone cwd), seed rows for the round-90 spot-check's routed defects (§6 items
1–3), and fresh rows for anything the round-91 wave itself routes. From round 92 the freeze step
of any new coverage claim must cite a `freeze=admitted` run at `--freeze-round N` (the wiring the
round-90 claim promised; round 91's own freeze predates the triage and demonstrates the BASE
refusal instead).

- **Before (BASE `59764383`, predicted):** `python3 plans/round91_burndown.py --lane . --rev 59764383… --work DIR --freeze-round 92` exits 1 printing `freeze=refused` with `pending>=29` (the 29 open seeds), `malformed_or_invalid_unresolved>=1` (the R82-F1 family), `DEFECT` lines for unresolved invalid rows, and `PREDICATE R91-C3 fail`.
- **After (measured tip, predicted):** the same command at the measured tip exits 0 printing `freeze=admitted pending=<open rows opened in round 91 only> parked=<blocked rows, all owned> resolutions>=35 seeds_83_90>=46 checks_run>=117 overrides=<printed, all with override_reason>`, `SELFTEST cases=9 red-green-ok=9` and `PREDICATE R91-C3 pass`. Every count is a prediction until the measured run prints it.
- **Predicate (one sentence, identical in this file, the gate's `PREDICATE R91-C3` line and the report):** pass iff the gate over the measured revision at `--freeze-round 92` exits 0 with `freeze=admitted`, no effectively-open finding opened before round 91, every effectively-blocked row carrying a non-empty `owner`, no malformed or schema-invalid row left unresolved, every effectively-closed row's check exiting 0 with checks run once per finding, every check override printed with its base check's result and carrying a non-empty `override_reason`, at least six seeded rows with `opened_round` in 83–90, and the selftest battery green with every red case red for its named reason — while the same gate over BASE exits 1 with `freeze=refused`.
- **Kill rule:** any resolution row whose status, evidence, `check` or `owner` is false to the tree (a closed row whose work is absent is a fabrication-class defect); any pending row left unresolved without a named standing blocker; any unresolved malformed row; a selftest case that stays green or is red for an unrelated reason; any edit to a pre-existing ledger row in place (append-only; corrections are new supersede rows). The gate refusing (exit 1) is itself the honest outcome if triage cannot truthfully resolve a row: an honest stop is recorded, never a fabricated close.
- **Controls:** do-nothing at BASE (above). Able-to-fail = the selftest's red cases (an old open row refuses; a closed row whose check fails is a defect; a supersede of a nonexistent id is a defect; a blocked row without an owner refuses; an override without `override_reason` refuses; a malformed row a valid resolution supersedes no longer defects; a seed-starved ledger refuses the seed clause; a failing check refuses the freeze; an override whose base check fails and which carries a reason is printed, not a defect). Positive = the triaged tip green. Separation: removing C1's receipt or C2's pin ledger leaves the C3 verdict unchanged.
- **Capability row:** `routed-findings freeze gate v2` — refuses a freeze while an old finding is open, a blocked row is unowned, a check fails, or a malformed row is unresolved; runs each closed row's check once; prints every override with its base check; enters `SCORECARD.md` capabilities this round.
- **Axis note:** operability held at its ceiling of 10 (ceiling precedent); the capability row and the admitted freeze are the claim's landing, not a score bump.

## Frontier step (not a claim)

`corpus/SOURCES.md` gains `S281` (the `modernize-scientific-stack` grader bytes, tier A for scope
"member replay only", status `mined`, used-by the round-91 lesson and the C1 receipt) and one
rejection row (`S282`, the member's `tests/test.sh` verifier wrapper — fetched live 2026-11-05,
HTTP 200, 721 B, sha256 `e868c85466ebf4815e2e4efbd252bf50ad979bceb14325a9377b1bbf852f0281`;
rejected: network-bound apt/uv wrapper with no grader semantics beyond S281; flip: a claim about
verifier-harness behaviour opened as its own replay). Both rows carry URL, access date and a
located quote in the round lesson's `## Gate` before admission. Census before → after by
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0 required
at round end). Census before (2026-11-05, measured, this round): exit 0, `kengaku ok`, 272 rows.

Assimilation (`§10`): none. `merge/kengaku/` stays held by L0 `kengaku | round-54`; nothing is
adopted. considerthese: none mined this round — item 1 of `considerthese/2026-10-26.md` was
mined in round 90 and its residual (the freeze wiring and gate conformance) is exactly C3 here;
no other proposal is implemented this round.

## Mistakes mined (not claims)

1. Class `prediction-unit` (round-90 M3 continuation): the round-90 C1 prediction said `legs=8`
   while the probe emitted five legs per case (`legs=40`) — a count whose unit the frozen text
   never derived. Captured-by: none (Q66 checked the figure's source, not its unit or arity).
   Fix: this round's claims predict every host-defined count with its formula
   (`legs=10*2=20`), and the do-nothing control measures the rest.
2. Class `predicate-implementation gap` (round-90 M5/F-13 class): the round-90 gate printed the
   seed count and the override results but gated on neither, and a superseded malformed row
   still emitted the DEFECT that blocked pass forever. Captured-by: the wave's
   ReviewerPredicate/ExecC3Triage/SentinelForge seats. Fix: R91-C3 — the successor gate computes
   every clause its predicate states and shows each clause able to fail in its selftest.

## Exploratory claims

None.

## Round shape

ONE v1 wave (policy band 8–16, `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`),
12 seats: executor 5, scout 1, connector 1, scribe 1, reviewer 1, critic 1, mutation-tester 1,
sentinel 1. Attack seats (reviewer, critic, mutation-tester, sentinel) 4 of 12 = 33 % ≥ 25 %.
Connector seats 1 (≤ 2). The planner seat is the L1 (the validator rejects planner as a swarm
role). No residual call planned; any residual is one ordinary task call of ≤ 4 seats, counted in
the round total.
