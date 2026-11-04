# kengaku round 84 — frozen claims

2026-11-04, hyaku run 15, attempt 1; L1 KengakuR84 holds the planner seat. All times UTC unless an offset is written.
Base revision: `4087b2f8369fb0c317a8460725a607681ff2fd7f` (master, round-83 closure tip; clean, ahead=0).
Two causally separable claims on two distinct axes. Coverage is the lowest non-retired axis (score 7, L0 cap
`kengaku | round-25/33/51` still open, nothing assumed answered); calibration is 10 (held at ceiling, exercised).
No stagnation waiver. No novelty construct, score increase or serving-plane claim is made.

## R84-C1 — coverage: second offline replay, `gcode-to-text`

Predicate R84-C1: the base-unexecuted `gcode-to-text` member has exactly one located, host-pinned receipt
`corpus/evidence/round84/gcode-to-text-probe.txt` whose frozen case vectors (`plans/round84-cases.json`) reproduce
the captured grader's two test functions with zero mismatches, and the population ledger marks that receipt executed in round 84.

Subject: `corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py`, sha256
`6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6` (ledger pin prefix `6b049dc626aa103b`). Two functions in
definition order: `test_hello_file_exists` (leg `exists`: `/app/out.txt` exists) and `test_hello_file_content` (leg `content`:
`read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}"`). The grader runs unmodified inside bubblewrap: `/usr` and `/etc`
read-only, the case directory bound as `/app`, the grader read-only at `/tests`. No reimplementation, no function patch,
no mocked `Path`/`open`, no host `/app` write. AssertionError or FileNotFoundError = F; normal return = P; any other
exception = setup defect (counts as a defect, never as a red witness).

Frozen case table (8 cases, 2 legs each, predicted vector `exists/content`):

| id | staged `/app/out.txt` content | predicted |
|---|---|---|
| missing | file absent | F/F |
| empty | `""` | P/F |
| exact | `flag{gc0d3_iz_ch4LLenGiNg}` | P/P |
| padded | ` \n` + exact + `\t\n` | P/P |
| uppercase | `FLAG{GC0D3_IZ_CH4LLENGING}` | P/F |
| suffix | exact + `x` | P/F |
| prefix-only | `flag{gc0d3_iz_` | P/F |
| wrong-flag | `flag{gc0d3_iz_ch4LLenGiNx}` | P/F |

Counter: `python3 plans/round84_c1_replay.py --lane . [--rev REV] --work DIR`. Probe tool: `plans/round84_gcode_probe.py`
(accepts `--lane DIR --work DIR`); the instrument prints `CASE <id> predicted=<vector> observed=<vector>`, a summary
`cases=8 mismatches=0`, and `PREDICATE R84-PROBE pass`.

Target: `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`, `PREDICATE R84-C1 pass`, exit 0.
Before (BASE): `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=>=1`, `PREDICATE R84-C1 fail`, exit 1.
Counting outputs at BASE and after are the population-gate figures: executed 27 → 28, unexecuted 61 → 60;
file-artifact class 19 of 76 → 20 of 76.

Receipt stamp (all required): MEMBER, SUBJECT_CAPTURE, SUBJECT_SHA, CASE_TABLE_SHA, TOOL, TOOL_SHA, HOST_PYTHON,
HOST_OPENSSL, LANE_TIP, WORKTREE clean, COMMAND (reconstructed argv, never executed from the receipt), EXIT 0, and an
OBSERVATIONS_BEGIN/END block.

Controls, executed before any real scoring and committed as receipts: do-nothing (no receipt at the revision), ledger-only
(executed flag, absent receipt), fabricated observations (complete stamp, wrong CASE vectors). Each must print
`target_reached=False`. Mutants of the counter must each be killed with a finding-specific nonzero exit.

Kill rule: any observed vector ≠ predicted, any setup exception, any missing receipt field, any control reaching
target, or a receipt whose subject sha differs from the pin → claim fails at that revision (honest stop, no retune).
Exit codes: 0 pass, 1 fail, 2 could-not-evaluate.

Sourced claim: the subject is cited to a new `corpus/SOURCES.md` row S271 (the pinned upstream
`gcode-to-text/tests/test_outputs.py`, opened 2026-11-04 at the pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`), recorded in
`corpus/lessons/round-84.md` Gate. The row supports member replay only, not a solved-task or model claim.

## R84-C2 — calibration: round-83 admission-bar debt in the admitted knowledge entry

Motivation: the outside round-83 closure (`corpus/lessons/round-83-verifier-spotcheck.md`, routed R83-V1 and R83-V2) found three
admission-bar defects in `corpus/knowledge/tb2-code-from-image-offline.md` that the round-83 self-assessment reported as clean
(its freshness axis "held 10" and its admission "landed"). These are the self-assessment mismatches this claim measures.

Predicate R84-C2: the knowledge entry `corpus/knowledge/tb2-code-from-image-offline.md` (admitted under round 83) carries zero
Q1, Q21 and Q13 admission-bar defects at the measured revision, where:
- **Q1** — its first three lines are `source:`, `verified-at:` and `recheck:`, and `recheck:` names an ISO date or cadence and a re-check action;
- **Q21** — its `source:` line carries a 40-hex commit pin and its `recheck:` line names that pin or the re-pin cadence;
- **Q13** — the successor admission in `corpus/lessons/round-84.md` `## Gate` cites, by repo-relative path, a second-seat re-read report
  that exists in the admitting tree, whose role is one of reviewer/scout/critic/sentinel/revenger, and whose writer differs from the candidate writer
  (checked by `plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV`, exit 0).

The round-83 Gate and filed bytes are not rewritten; the correction is a dated paragraph in the round-84 lesson. The successor
re-admission cites reports committed under `.ufo/waves/round-84/` by this round's wave seats, never a backdated landing-time review.

Counter: `python3 plans/round84_c2_admission.py --lane . [--rev REV] --work DIR` (selftest, mutants and a filler control included).

Target: `TARGET entries=1 q1=0 q21=0 q13=0 defects=0`, `PREDICATE R84-C2 pass`, exit 0.
Before (BASE 4087b2f8): `TARGET entries=1 q1=1 q21=1 q13=1 defects=3`, `PREDICATE R84-C2 fail`, exit 1.
Controls: do-nothing (BASE bytes) must keep `defects=3`; a fabricated-fixture entry that repairs only the recheck date (no pin, no Gate path) must keep `q21=1 q13=1`.

Kill rule: any remaining defect, a base-insensitive check (BASE not red), a Gate path whose report is absent from the tree, or a
report whose writer equals the candidate writer → claim fails. Frozen claim sentences, counter predicate and target are not edited after the wave scores.

Freshness is restored to its held value by this repair; that is recorded as restoration, not a new gain. Quality and expansion are not claimed for this claim.

## Frontier and wave contract (round 84)

- Shape: ONE v1 wave, 12 seats, policy `scripts/hyaku/ufo-wave-policy.json` (band 8–16). Attack seats (reviewer ×2, critic, mutation-tester) = 4/12 (≥25 %). Connector seats: 1.
- Planner seat: the L1 (KengakuR84). A bounded data walk rides the scout (`ScoutR84`).
- Routing via `task.agentModelOverrides` only; no model passed.
- Considerthese: `considerthese/2026-10-26.md` §Self-improvement suggestions 2 (one standing TB2 admission counter with a filler control). Mined; the C2 counter's
  filler control (BASE bytes must stay red) is its per-entry form. Lands as a QUALITY criterion, not as a general standing counter.
- Assimilation: none. `merge/kengaku/` (175 staged rows, 65 knowledge entries) is not drawn on by these frozen claims; it remains unadopted backlog.
- Mistake mined: R83-V1 and R83-V2 (admission-bar gaps the lane's own gate did not catch). Evidence: `corpus/lessons/round-83-verifier-spotcheck.md`
  §Routed defects. Captured-by: none. Fix: the R84-C2 counter, shown red on BASE and on a repair that fixes only the date.
