# Round 90 — frozen claims (kengaku)

Frozen in commit A (this file and `plans/round90-cases.json`), before any instrument, receipt or
score exists. Base: `dcdd494ef4b4a6c0ae349ecb597527124ee54f91` (round-89 spot-check landing,
`master`). Measured tip: the commit that lands the receipt, the ledger flip, S279 and the triage
resolutions — never a commit whose bytes changed after the first score, and never a tip whose
`plans/` bytes differ from the pin commit B (`git diff --stat B tip -- plans/` must print nothing).
Nothing below may be edited after freeze; a frozen element that looks wrong is reported, not
repaired.

Three claims, causally separable: C1 reads the replay surface (grader bytes, case table, probe,
receipt, ledger row); C2 reads counter/pin bytes at a revision and the round-89 record table; C3
reads `corpus/routed-findings.jsonl` and its own gate output. No claim reads another claim's
receipt or evidence. Shape: ONE v1 wave, 8–16 seats, attack seats ≥ 25 %.

Measurement note (Q66 applied to this file): every BEFORE figure below is a prediction until the
do-nothing control measures it at BASE. Measured figures are recorded in the report; a mismatch
between a prediction and the measured figure is recorded as a mispredict, never repaired in place.

## R90-C1 — coverage (lowest non-retired axis, held at its L0 cap 7): an eighth located offline replay, `merge-diff-arc-agi-task`

**Move:** a located offline replay of the Terminal-Bench 2.0 grader `merge-diff-arc-agi-task` by
the round-90 counter `plans/round90_c1_replay.py` over the frozen eight-case table
`plans/round90-cases.json`, with the probe bytes pinned by sha (the round-89 L9 pattern). The
captured grader (`corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py`,
sha256 `2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149`) defines five test
functions over a graded state that is a git repository plus a Python module plus a JSON test-input
file: repo initialized, both bundle branches present, `algo.py` exists with a callable `map`, and
`map` reproduces `/tests/test.json`'s examples elementwise. The member carries classes
`file-artifact`, `git-plumbing`, `serialization-schema`, `stdout-inspection`, `subprocess-exec`;
`git-plumbing` (1 of 3 at BASE) is the thinnest executed-or-not class cell in the ledger and this
is its first executed member since the ledger began; the case table adds a serialization-drift case
class (corrupt JSON input) the executed set has not held.

- **Before (BASE `dcdd494e`, predicted):** `TARGET executed_rows=33 member=merge-diff-arc-agi-task located=1 executed=0 cases=0 legs=0 mismatches=0 defects=N`, `PREDICATE R90-C1 fail`, exit 1, where N is measured by the do-nothing control (predicted N=5: receipt absent, case table absent at BASE, no vectors, ledger unflipped, probe bytes absent). Ledger at BASE (measured by `python3 -c` over `plans/grader-population-ledger.json` on 2026-11-05): members 88, executed 33; `git-plumbing` 1 of 3; `serialization-schema` 3 of 10; `file-artifact` 24 of 76; `stdout-inspection` 9 of 29; `subprocess-exec` 11 of 45.
- **After (measured tip, predicted):** `TARGET executed_rows=34 member=merge-diff-arc-agi-task located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R90-C1 pass`, exit 0. Ledger: executed 33 → 34 of 88; `git-plumbing` 1 of 3 → 2 of 3; `serialization-schema` 3 of 10 → 4 of 10; `file-artifact` 24 of 76 → 25 of 76; `stdout-inspection` 9 of 29 → 10 of 29; `subprocess-exec` 11 of 45 → 12 of 45.
- **Legs (frozen list L1–L8):** L1 the receipt `corpus/evidence/round90/merge-diff-probe.txt` exists and is committed at the measured revision; L2 the captured grader bytes at the measured revision hash to `2754ba6c…85c149` and the receipt's `SUBJECT_SHA` equals it; L3 the receipt's `LANE_TIP` is an ancestor of the measured revision (`git merge-base --is-ancestor`); L4 `plans/round90-cases.json` at the measured revision is byte-identical to the freeze commit A's; L5 every case's receipt-observed vector equals its frozen predicted vector; L6 the probe re-run from an extraction of the measured tree reproduces the receipt observation block; L7 the ledger at the measured revision carries `merge-diff-arc-agi-task` `executed` with the after-cell values above; L8 the probe bytes at the measured revision hash to the counter's pinned `TRUSTED_TOOL_SHA`.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R90-C1` line and the report):** pass iff the captured grader bytes at the measured revision hash to the frozen subject SHA, the frozen case table is byte-identical to the freeze commit's table, the receipt is committed at the measured revision and its `LANE_TIP` is an ancestor of that revision, every case's observed vector equals its frozen predicted vector, the probe re-run reproduces the receipt observation block, the ledger flips the member to executed with the five class cells incremented by one, and the probe bytes hash to the counter's pinned `TRUSTED_TOOL_SHA`.
- **Kill rule:** any leg L1–L8 failing at the measured tip makes the claim unmet; so does any mismatch between the probe re-run and the receipt, and so does a probe whose bytes differ from `TRUSTED_TOOL_SHA`. Editing the case table or this file after commit A voids the claim.
- **Controls:** do-nothing = the counter at BASE must exit 1 with `PREDICATE R90-C1 fail`. Ledger-only control (ledger row flipped, receipt absent) must fail at L1. Forged-tip control (receipt `LANE_TIP` replaced by a commit that is not an ancestor of the measured revision) must fail at L3. Forged-probe control (the probe's grader call replaced by an echo of the predicted vectors, receipt regenerated from it) must fail at L8. Separation: reverting C2's pin file and tool leaves the C1 counter's verdict unchanged, and reverting C1's receipt and ledger row leaves C2's verdict unchanged. Each control's exit code and defect lines are committed under `.ufo/waves/round-90/` before the measured tip is scored.
- **Sourced:** the grader bytes are row `S279` in `corpus/SOURCES.md`, opened in this round: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py` (fetch + byte-compare against the round-52 capture + located quote recorded in the round lesson's `## Gate` before admission).
- **Honest limits:** (a) the eight cases yield **seven** distinct predicted vectors (`PPPPPP`, `FFPPP`, `PFPPP`, `PPFEE`, `PPPEE`, `PPPPF`, `PPPPE`; `PPPPF` occurs twice), not eight; (b) the vector is a statement about the captured bytes plus this probe harness on this host's toolchain (git, python3), not about Terminal-Bench's own harness; (c) `test_both_bundles_fetched` greps branch *names*, so the cases prove name presence, never that a bundle was fetched — the graded state is lane-authored, as in every replay of this series; (d) the counter is pinnable by one commit that also rewrites the pin ledger (C2's disclosed limit).

## R90-C2 — calibration (held at ceiling 10): the counters pinned externally, closing the round-89 self-pin hole

**Move:** `plans/counter-pins-r90.json` + `plans/round90_counter_pin.py`. Round 89's `TRUSTED_TOOL_SHA`
pins the probe from inside the counter that an adversary could rewrite; SentinelR89 H1–H3 and lesson
Mistake 9 name the hole, and spot-check defect 1 asks for a blob-sha pin of the round-89 record
table. The pin ledger lists, per frozen instrument, the sha256 of its bytes at pin commit B; the
checker verifies, at any revision, that every listed path's bytes there hash to its pin and that the
record table's git blob at the measured revision equals the pinned blob. The r89 spot-check's
"freeze-commit blob" is **corrected here, before data**: `plans/round89-q66-records.json` does not
exist at the r89 freeze commit `d1c4f1b0` (`git cat-file -e` exits 128), so the pin anchors to the
table's creating commit `0e6bb05f` (blob `163f284316141a831484dacb7f69ad4cbbaadfb3`, unchanged to
the round-90 base). r89's frozen text is not edited; this correction is the round-90 record.

Pinned paths at commit B: `plans/round88_claim_figures.py`, `plans/round89_c1_replay.py`,
`plans/round89_claim_figures.py`, `plans/round90_c1_replay.py`, `plans/round90_polydiff_probe.py`,
`plans/round90_burndown.py`, and the record-table blob entry
`{"path": "plans/round89-q66-records.json", "blob": "163f284316141a831484dacb7f69ad4cbbaadfb3", "anchor_commit": "0e6bb05f3a6c2d9a96bb26db31a4fd39f58c2619"}`.

- **Before (BASE `dcdd494e`, predicted):** `python3 plans/round90_counter_pin.py --lane . --rev dcdd494e… --work DIR` exits 1 printing `PIN-MISMATCH absent` for every path created this round (fail-closed on absence — never an awk zero); the four pre-existing counters match (bytes unchanged since the round-89 tip) and are printed `PIN-OK`.
- **After (measured tip, predicted):** the same command at the measured tip exits 0 printing `PINS checked=7 matched=7 mismatched=0`, `RECORD-TABLE blob=163f2843… matched`, `PREDICATE R90-C2 pass`; `--selftest` exits 0 with every red case red.
- **Predicate (one sentence, identical in this file, the checker's `PREDICATE R90-C2` line and the report):** pass iff at the measured revision every path in `plans/counter-pins-r90.json` exists and hashes to its pinned sha256 (an absent path is a mismatch, never a skip), the record table's blob at the measured revision equals the pinned blob, and the selftest battery exits 0 with every declared red case red while the unmodified tree is green.
- **Kill rule:** any `PIN-MISMATCH` at the measured tip; any selftest case that stays green; any edit to the pinned files, the pin ledger or this file after commit B; any edit to `plans/routed_open.py` (round-41 instrument, out of scope by name). An adversary who can write the tree can still rewrite the pin ledger itself in one commit — that residual is the round-89 disclosure, narrowed but not eliminated, and is not hidden.
- **Controls:** do-nothing at BASE (above); able-to-fail = `--selftest` red cases (a modified counter byte in a two-commit fixture repo, and a modified record-table blob, each must print the mismatch and exit 1); positive = the unmodified tip green. Separation as in C1.
- **Axis note:** calibration held at its ceiling of 10 (round-86/87/88/89 precedent): a count move at the ceiling is recorded, not added to the score.

## R90-C3 — operability (held at ceiling 10) + capability acquisition: the routed-findings freeze gate landed and wired

**Move:** the considerthese item 1 (`considerthese/2026-10-26.md`, "Self-improvement suggestions"
proposal 1) burn-down completed. Since round 41 the lane has had `plans/routed_open.py` and a
133-row `corpus/routed-findings.jsonl`, but nothing in the freeze path invoked it: 27 findings
opened rounds 39–82 still sit open or blocked, one ledger row (line 125, `R82-F1`) is malformed
under the ledger's own schema, and no routed finding from rounds 83–89 has a row — "routed to
round N+1" is where findings went to die. This round lands: (a) resolution rows for all 27 pending
rows opened ≤ 82 and for the malformed `R82-F1` row, each carrying closing evidence or a named
blocker, with the row's own `check` command (where present) passing when the status is closed;
(b) seed rows for every routed finding in the round-83 through round-89 verifier-spot-check
routed-defect sections and the round-89 lesson's attempt-2 routing list that lacks a row (the six
`R89-D1…D6` spot-check defects are enumerated below and close inside this round); (c) the gate
`plans/round90_burndown.py` which computes pending and oldest-open from supersede-aware rows,
runs every closed resolution row's `check`, and applies the standing freeze rule: a freeze of
round N is refused while the oldest pending finding is opened before N−2.

The six round-89 spot-check defects (§7 of `corpus/lessons/round-89-verifier-spotcheck.md`), seeded and closed this round: `R89-D1` element (d) unimplemented → closed by C2's record-table blob pin; `R89-D2` control name drift → closed by the correction note in LOG.md (frozen text untouched); `R89-D3` round-88 before-count stated two ways → closed by the correction entry in LOG.md ("1 of 3 measured; the fourth not measured at BASE; fixture-c red was a parse failure, not the KNOWN check"); `R89-D4` round-89 gate logged no reject → closed by this round's `## Gate` carrying ≥ 1 admit and ≥ 1 reject with reasons; `R89-D5` Mistake 9 counter pin → closed by C2; `R89-D6` SCORECARD C2 row limitation → closed by the correction row in SCORECARD.md.

- **Before (BASE `dcdd494e`, predicted):** `python3 plans/round90_burndown.py --lane . --rev dcdd494e… --work DIR --freeze-round 90` exits 1 printing `freeze=refused oldest_pending_round=39 pending>=27 malformed_unresolved=1 seeds_83_89=0`, `PREDICATE R90-C3 fail` (at BASE the gate reads the BASE ledger: 27 pending rows, oldest 39, the malformed row unresolved, no 83–89 seeds).
- **After (measured tip, predicted):** the same command at the measured tip exits 0 printing `freeze=admitted pending=0 oldest_pending_round=- malformed_unresolved=0 seeds_83_89>=6 resolutions>=28`, `PREDICATE R90-C3 pass`; `--selftest` exits 0 with every red case red.
- **Predicate (one sentence, identical in this file, the gate's `PREDICATE R90-C3` line and the report):** pass iff the gate over the measured tip exits 0 with `freeze=admitted`, no pending finding opened before round 88, no malformed row left unresolved, at least six seeded rows with `opened_round` in 83–89, and every resolution row carrying closing evidence or a named blocker with its `check` (where present) exiting 0 — while the same gate over BASE exits 1 with `freeze=refused`.
- **Kill rule:** any resolution row whose status, evidence or `check` is false to the tree (a closed row whose work is absent is a fabrication-class defect); any pending row left unresolved without a named standing blocker; any unresolved malformed row; a selftest case that stays green; any edit to a pre-existing ledger row in place (append-only; corrections are new rows). The gate refuses (exit 1) is itself the honest outcome if triage cannot truthfully resolve a row: an honest stop is recorded, never a fabricated close.
- **Controls:** do-nothing at BASE (above); able-to-fail = `--selftest` red cases (a ledger with an old open row refuses; a ledger with a closed row whose `check` fails is a defect; a supersede of a nonexistent id is a defect); positive = the triaged tip green. Separation: removing C1's receipt or C2's pin file leaves the C3 verdict unchanged.
- **Wiring:** from round 91 the freeze step of any new coverage claim must cite a `freeze=admitted` run at `--freeze-round <N>`; the round-90 freeze predates the gate and demonstrates the rule by the BASE refusal.
- **Capability row:** `routed-findings freeze gate` — what it can now do: refuse a round freeze while routed findings older than two rounds sit unresolved (`plans/round90_burndown.py --freeze-round N`); enters `SCORECARD.md` capabilities this round.
- **Axis note:** operability held at its ceiling of 10 (ceiling precedent); the capability row is the claim's landing, not a score bump.

## Frontier step (not a claim)

`corpus/SOURCES.md` gains `S279` (the `merge-diff-arc-agi-task` grader bytes, tier A for scope
"member replay only", status `mined`, used-by the round-90 lesson and the C1 claim), opened this
round with the fetch + byte-compare + located quote recorded in the round lesson's `## Gate`
before admission. The gate also carries at least one rejection with reason and flip (the round-89
defect `R89-D4` closure). Census before → after by
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0 required
at round end). Census before (2026-11-05, measured, this round): exit 0, `kengaku ok`, 270 rows.

Assimilation (`§10`): ONE considerthese proposal mined and implemented —
`considerthese/2026-10-26.md` proposal 1, via C3. `merge/kengaku/` stays blocked by L0
`kengaku | round-54`; nothing is adopted from it.

## Mistakes mined (not claims)

1. Class `unwired-tripwire`: the burn-down tool and ledger existed since round 41 but no freeze
   step invoked them, so 27 findings aged 40+ rounds unresolved and six spot-check generations
   went unseeded. Captured-by: none (the round-39 Q30 lesson wired `order_check.py` into
   `round_close.py` but never `routed_open.py`). Fix: C3, with the freeze-citation wiring above.
2. Class `schema-drift`: ledger row 125 (`R82-F1`) carries a prose `source` cell
   (`corpus/lessons/round-82.md ## Corrections (R81-V2)`) that passes eyeballing and fails the
   ledger's own parser (`source must read <path>:<line>`). Captured-by: `routed_open.py`
   validation (it caught the row; nothing read its output). Fix: supersede by a well-formed
   resolution row; the C3 gate refuses while a malformed row is unresolved.

## Exploratory claims

None.

## Round shape

ONE v1 wave (policy band 8–16, `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`),
12 seats: executor 3, scout 1, connector 1, scribe 1, reviewer 1, critic 1, mutation-tester 1,
sentinel 1, labrat 1. Attack seats (reviewer, critic, mutation-tester, sentinel, labrat) 5 of 12.
The planner seat is the L1 (validator rejects planner as a swarm role). No residual call planned;
any residual is one ordinary task call of ≤ 4 seats, counted in the round total.
