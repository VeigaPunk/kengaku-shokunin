# SourcesScribeR80 — source-row draft

## Behavior and axes

Coverage: define the six located replay receipts without enlarging execution scope. Calibration: distinguish stamped historical assertions from independently exercised evidence. Report-only work; no SOURCES.md edit and no claim-counter execution.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`. Measured master: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (integration has advanced). Receipt bytes below were read from that exact committed tree, not inferred from its stamp.

## Findings / conflict

Assignment says: “Draft `S258` (the next free id — verify with `grep -oE '^ (0, 3)\|[[:space:]]*S[0-9](3,)' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -3`)”.

Observed conflict: S258 already exists at corpus/SOURCES.md:274. S256/S257/S258 occupy lines 272/273/274. Do not append a duplicate S258. The requested row below is a report-only alternative for the integrator, not a new admission. The supplied regex uses literal `(0, 3)` and `(3,)`, not repetition braces; it is not a sound source-id census. Used the specialized search tool with corrected anchored pattern `^ {0,3}\\|[[:space:]]*S[0-9]{3,}` over lines 271–274 instead; observed S255, S256, S257, S258. No assertion that S258 is free or that a later id is free.

The existing S258 teaching has no explicit short quotation and its anchor points only to the subject header. The proposed row adds a verbatim located stamp quote, identifies the stamp range and TARGET construction, and avoids asserting a fresh rerun by this seat.

## Draft row — exactly 11 columns

| S258 | kengaku round-80 located-replay instruments — corpus/evidence/round80/<member>-probe.txt (six), plans/round80_probes.json, plans/round80_c1_located_replay.py | own-work | A | the lane's own located offline replays for cancel-async-tasks, chess-best-move, distribution-search, largest-eigenval, openssl-selfsigned-cert and protein-assembly; frozen probe table and replay gate; extends S257, not S256's container-run scope | corpus/evidence/round80/cancel-async-tasks-probe.txt:3–10 (receipt stamp; exact quote at line 7), sha256 7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e at 6669fe72e59718acc1a0f32a92849a544b0b2f1c; plans/round80_c1_located_replay.py:350–352 (TARGET construction) | “LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235”; a located replay identifies its subject, stamps historical-source and instrument hashes, command and exit, and carries observations for fresh comparison through the frozen table at the measured tip; the stamp alone does not establish that comparison | mined | 2026-11-04 | 90d | corpus/lessons/round-80.md, SCORECARD.md |

Quote is the exact two-token receipt line 7, within the 25-word limit. The stored LANE_TIP is not relabelled as this seat's measured master. `mined` is the requested proposed registry status, not a claim that this scribe admitted anything.

## Reject candidate and flip condition

Rejected: “These six located offline replays establish six successful containerized Terminal-Bench runs.” A subject header, digest stamps and matching offline stdout do not establish the container harness execution surface. S256 scopes that distinction separately (corpus/SOURCES.md:272; pinned README capture corpus/evidence/round79/sources/tb2-readme.md:24). Flip only on tracked evidence of actual containerized harness runs for these six members, identifying task and harness revisions, environment, commands, exit/results and provenance at the measured revision; do not infer it from the offline replay gate.

## Commands and observed outcomes

1. First read, before any command: full plans/round-80-claims.md:1–155. Also read SOURCES.md:1–22, :272–274, QUALITY.md Q1–Q7 (:15–60), plans/round80_probes.json:1–43, receipt :1–27, and gate :345–359. Specialized source search returned S256 at 272, S257 at 273, S258 at 274. Gate source constructs TARGET at 350–352; reading that code is not a gate pass.
2. Exact shell invocation (exit 0):
   ```sh
   S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r80/SourcesScribeR80"; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT; git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
   ```
   Output: `6669fe72e59718acc1a0f32a92849a544b0b2f1c`. Scratch cleanup was attached to shell EXIT; no clone or fixture was needed.
3. Exact command (exit 0):
   ```sh
   git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:corpus/evidence/round80/cancel-async-tasks-probe.txt
   ```
   Committed output excerpt (lines 3–10):
   ```text
   SOURCE_RECEIPT corpus/evidence/round61/cancel-async-probe.txt
   SOURCE_SHA 3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a
   TOOL plans/round61_c1_cancel_probe.py
   TOOL_SHA 92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87
   LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235
   WORKTREE clean
   COMMAND /usr/bin/python3 plans/round61_c1_cancel_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/remint-work/cancel-async-tasks.work --receipt /fast/scratch/hyaku/kengaku-r80/remint-work/cancel-async-tasks.out.txt
   EXIT 0
   ```
   Stored observation summary (line 25): `cases=12 legs=72 mismatches=0 setup=0 predicted_u=0`; stored line 26: `PREDICATE R61-C1 pass`. These are receipt contents, not this seat's execution evidence.
4. Exact command (exit 0):
   ```sh
   git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 6669fe72e59718acc1a0f32a92849a544b0b2f1c:corpus/evidence/round80/cancel-async-tasks-probe.txt | sha256sum
   ```
   Output: `7923b6dc39a1c201bd92ab3e4b6651a4c5ff83bc9a5606a1162a29bb6aa7f74e  -`.

## Gates, touched surfaces and limits

Q1: proposed date/cadence supplied; this is a source-row draft, not a new knowledge entry. Q2/Q5: own-work tier A is restricted to the lane's own rerunnable instrument scope, not independent benchmark truth. Q3: exact two-word located quote retained. Q4: explicit container-run rejection and flip. Q6: extends S257; does not duplicate S256's scope. Q7: used-by destinations are requested integration targets; no same-commit discoverability/admission claim is made by this report.

Only persistent write: `.ufo/waves/round-80/w1/SourcesScribeR80.md`. No product, registry, plan, lesson or scorecard edits; no git mutations, tool installs, other runtime, subagent, container run, gate rerun, instrument replay or checks of all six receipt digests. No failed commands occurred. Main integrator must use its actual C1 execution evidence for reproduction and population-gate outcomes; this report supplies no such pass.

Self-evaluation: accuracy 4/5 (committed quote/digest grounded, all-six replay not independently exercised by scope); completeness 4/5 (requested free-id premise conflicts with existing S258, explicitly retained rather than silently renumbered); clarity 4/5 (proposed status versus admission is distinguished, provenance is necessarily detailed); actionability 4/5 (paste-ready alternative, duplicate-id resolution remains with integrator); conciseness 4/5 (command provenance adds length). Overall 4.0/5. Priority: resolve existing-row integration without duplicating S258; retain separate execution evidence. User-agreement self-check: likely yes, because the draft and limits are explicit.
