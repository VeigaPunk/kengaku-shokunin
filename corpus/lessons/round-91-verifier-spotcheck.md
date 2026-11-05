author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 91 — non-author verifier spot-check

Reviewed lane tip: `f06d0b65d85b650ba459f2db47e3bf10ffa4b732` (BASE `59764383d4dd33d58faa50daad4c06d0cde410aa`). Report: `.ufo/reports/round-91/kengaku.md` (commit `b653cc6de7d6a5d83d599ed03f58cae34e102a72`, author `kengaku-shokunin <kengaku@shokunin.local>`). Driver digest (`.ufo/watchdog.log`, copied 2026-11-05): `2026-11-05T07:41:55-03:00 launch kengaku round=91 pgid=154382 driver=hyaku-inline attempt=1`; `2026-11-05T09:34:10-03:00 complete kengaku round=91; hyaku-inline attempt=1`. No `lane-dead-no-report kengaku round=91` line.

Method. Plain measurements over committed bytes (`git show`, `git diff --numstat`, `sha256sum`, `git rev-parse`, `git cat-file`, `wc`, `grep`, `jq`-equivalent Python reads). Lane counters, gates and selftests were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed transcript `.ufo/waves/round-91/L1/measured.txt` was read and graded evidence-verified. Live re-fetches were run for S281 and S282 only.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report commit attribution | `git log --format='%an %H' -- .ufo/reports/round-91/kengaku.md` → `kengaku-shokunin \| kengaku@shokunin.local \| b653cc6de7d6a5d83d599ed03f58cae34e102a72` | lane identity ✓ |
| `## SHONEN` heading | `grep -c '^## SHONEN' report` → `1`; four `[~]` lines | ✓ one line per box |
| cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `cd0c116e 386184a6 b836a862 a8de3e69 cefabd44 f06d0b65 59764383` | all `ancestor` ✓ |
| lane pushed, no leftovers | `jj-lane.sh state …` → `local=f06d0b65… remote=f06d0b65… ahead=0 behind=0`; `git status --porcelain` empty | ✓ |
| remote tip | `git ls-remote origin refs/heads/master` → `f06d0b65…` | ✓ |
| dispatch evidence | watchdog launch 07:41:55 and complete 09:34:10 (digest above) | ✓ dispatched and terminated |
| wave shape | `w1-results.json`: 11 seats, one v1 wave; executor 4, scout 1, connector 1, scribe 1, reviewer 1, critic 1, mutation-tester 1, sentinel 1; planner held by L1 | attack share 4/11 = 36% (≥25%) ✓; connectors 1 (≤2) ✓; L2 floor (8 roles incl. planner in L1) ✓ |
| prompt template contract | `.ufo/prompts/kengaku-round-91.md` §1–§7 present; round-level items (MISSION/AXES binding, 1–3 claims, ≥8 L2 in one wave, commit-then-push, push scope, L0 channel) and the five child-lane items (report path, commit-before-report, SHONEN heading, commit-hash citation, write scope) all embedded | ✓ |
| report sections | `## Work performed`, `## Landed changes`, `## Before → after measurements`, `## Sources & frontier`, `## Trend verdicts`, `## SHONEN`, `Stale-lane` line | ✓ |

Conformance defects (status-neutral, named in round notes; none changes status `ok`):
- The report's wave bullet says ExecC2Battery ran "14 controls"; the seat's `controls.txt` lists controls 1–8 plus sub-controls 5b, 5c, 6b, 7b, 7c. The report already discloses this in "Work not done"; an erratum is owed in the lane's next round.
- The frozen claim text gives function ranges "lines 16–42 and 45–48"; the committed grader defines them at lines 11 and 46 (`grep -n '^def ' ` over the bytes; the lesson's M2 says the same). Disclosed; not repaired after freeze, which is correct.
- The frozen claims' round-shape line (executor 3, labrat 1, attack 5 of 12) does not match the dispatched spec. Self-disclosed as a divergence.

## 2. Claims — re-derivation at `f06d0b65`

**R91-C1 — coverage — NOT MET on its frozen predicate.**
- Re-measured: executed ledger rows (`plans/grader-population-ledger.json`, `members[*].status == "executed"`): BASE `59764383` → 34 of 88; tip `f06d0b65` → 35 of 88; the new row is `modernize-scientific-stack` with `round: 91`, receipt `corpus/evidence/round91/modernize-probe.txt`. The ledger move is real.
- Re-measured: receipt `corpus/evidence/round91/modernize-probe.txt` carries 10 `CASE … ok=True` lines and 0 `id=` tokens (`grep -c '^CASE .* ok=True'` → 10; `grep -c 'id='` → 0).
- Evidence-verified (committed transcript, not re-run): `TARGET executed_rows=35 … executed=0 cases=10 legs=20 mismatches=10 defects=10`, ten `DEFECT L5 receipt names unknown case ?`, `PREDICATE R91-C1 fail`, rc 1.
- Root cause confirmed by reading `plans/round91_c1_replay.py` (lines 80–84): case ids are read from `key=value` tokens (`parts.get("id","?")`), while the CASE lines carry the id positionally (token 1). The predicate is therefore unmet at the tip by a counter defect the lane itself found (M7). Routed.
- Axis: coverage held at its L0 cap 7 per SCORECARD; the ledger move gets no axis credit because the claim does not verify. **Verdict: unchanged.**

**R91-C2 — calibration — MET on its frozen predicate (verified; caveat routed).**
- Re-measured by plain hash over committed bytes at the tip: `plans/counter-pins-r91.json` has 16 entries (kinds `sha` and `blob`); all 16 match (`sha256` of `git show f06d0b65:<path>` equal to the pin; blob entries equal `git rev-parse f06d0b65:<path>`). An absent path would be a mismatch; none is absent.
- Evidence-verified (committed transcript): BASE `DEFECT SETUP unreadable plans/counter-pins-r91.json`, `PREDICATE R91-C2 could-not-evaluate`, rc 2 (fail-closed); tip `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, `PREDICATE R91-C2 pass`, rc 0.
- Caveat, verified in source: `plans/round91_counter_pin.py` exposes `--skip-selftest` (lines 16, 115, 129). The predicate sentence says the selftest battery "run in the same invocation". The default-path pass holds; the flag is an escape the counter offers, which the lane's own controls measured (control 6, control 5b). Routed to round 92 as M9. The claim's residuals (one-commit checker-plus-pin rewrite; in-tree pin) are disclosed by the claim.
- Score ceiling 10 held. **Verdict: improved** (before unreadable → after 16/16 pinned, with the default-path predicate met).

**R91-C3 — operability (+ capability `routed-findings freeze gate v2`) — NOT MET on its frozen predicate.**
- Re-measured: `corpus/routed-findings.jsonl` 213 → 253 lines (`git diff --stat 59764383 cefabd44` → 40 insertions, 0 deletions). The 40 new rows: `closed` 13, `blocked` 24, `refused` 3 (counted from the `+` lines of that diff). This matches the report's triage counts.
- Evidence-verified (committed transcript): BASE and tip `freeze=refused`, tip `pending=1`, `DEFECT override-unjustified` for R42-R2, R42-R3-33, R42-R3-37, `PREDICATE R91-C3 fail`, rc 1. The selftest run is 13/13 green (`--selftest`, rc 0).
- Structural confirmation, in source: `plans/round91_burndown.py` calls `selftest()` only under `--selftest` (lines 398–399); the default predicate path does not run it (M8). `run_check` uses `cwd=lane_root` (line 118), so checks read the working tree, not the measured revision (M11). Both routed.
- Capability: not entered (the gate's predicate is not met). **Verdict: unchanged** (operability held at ceiling 10; the gate refuses at BASE and at tip; the backlog move is not a verified capability).

**R91-F1 — companion (no claim slot; the R82-F1 QUOTE_RE repair).** Evidence-verified only: transcript `PARSED S260=1,S261=2,S265=1,S266=2`, `PREDICATE R91-F1 pass`, rc 0. The four blind-spot rows still carry no capture pin (M5). Not graded as an axis claim.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| novelty | unchanged | no move claimed; SCORECARD diff is insertion-only (`git diff --numstat 59764383 f06d0b65 -- SCORECARD.md` → `26 0 SCORECARD.md`) |
| depth | unchanged | no move claimed; no `SKILL.md` change in the claim set |
| freshness | unchanged | S281 and S282 re-fetched this round (no knowledge entry re-verified) |
| adjacency | unchanged | no move claimed; connector scan absorbed nothing (report) |
| coverage | unchanged | C1 not met; ledger move 34→35 real but uncredited |
| calibration | improved | C2 met on its frozen predicate; pins re-derived 16/16 |
| operability | unchanged | C3 not met; gate refuses at BASE and tip |

No axis is harmed. Every owned score is held at its ceiling or cap; `git diff --numstat` shows zero deletions in SCORECARD.md.

**Admission.** C1 and C3 do not verify, so the round is **not admitted** (`admitted: false`). The lane's honest stop is correct, and the report says so.

## 4. Spot-check table (LEARNING.md discernment)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S281 `modernize-scientific-stack/tests/test_outputs.py` @ `2fd12b88` | **admit** (tier A, member replay only) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py`, re-fetched 2026-11-05: HTTP 200, 2330 B, sha256 `0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977`; committed capture `corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py` same sha256 (`cmp` identical) | **agree** | line 27 is `assert "Station 101" in output, "Must output Station 101 results"` — byte-exact to the row's quote; `wc -w` = 10 (≤25 ✓); `def` at lines 11 and 46 match the lesson's grounding. Admit is correct for a member replay; the row is scoped `member replay only` so it teaches no solved-task claim. |
| S282 `modernize-scientific-stack/tests/test.sh` @ `2fd12b88` | **reject** | same base URL, `tests/test.sh`, re-fetched: HTTP 200, 721 B, sha256 `e868c85466ebf4815e2e4efbd252bf50ad979bceb14325a9377b1bbf852f0281` | **agree** | line 5 `apt-get install -y curl` (network install; `wc -w` = 4). The wrapper adds no grader semantics beyond S281, and its replay needs network installs the offline replay forbids. The reject reason and the flip condition are both stated. |
| SOURCES row S281 quote (≤25 words) | — (row check) | `corpus/SOURCES.md:297` | **agree** | quote 10 words, located at `test_outputs.py:27`, matching the re-fetched bytes. |
| SOURCES row S282 quote (≤25 words) | — (row check) | `corpus/SOURCES.md:298` | **agree** | quote 4 words, located at `test.sh:5`, matching the re-fetched bytes. |
| triage close R84-V9-R91 (judgment close, not a gate decision) | close, disposition `fixed-verified` | `plans/round-91-claims.md:4` (`Base: \`59764383…\``); `git cat-file -e 59764383…^{commit}` rc 0 | **agree on the close; disagree with the disposition word** | the freeze defines its before against an existing revision, which is what R84-V9 asked a successor freeze to do. The disposition `fixed-verified` overstates a judgment; the lane's own M14 says so. Append-only: the lane should add a correction row, not edit this one (routed). |
| triage close R84-V2-R91 (freeze hygiene) | close | `git cat-file -e cd0c116e…:plans/round91-cases.json` rc 0; at BASE `59764383…` rc 128 | **agree** | the case table is committed at the freeze commit and absent at BASE, as the close states. |

Sample: ≥1 admit (S281) and ≥1 reject (S282) re-opened ✓. Two gate decisions agreed on both polarities. Two triage closes checked; one disagreement on wording, recorded.

## 5. Trend verdicts (LEARNING.md)

- **expansion: unchanged.** `git diff --stat 59764383 f06d0b65 -- corpus/knowledge` prints nothing; no knowledge entry was admitted. S281 is a source row, not an admitted entry; the ledger move is coverage counted in the ledger, not expansion.
- **quality: unchanged.** No admitted entry was re-verified, deepened or superseded this round (the knowledge diff is empty). QUALITY Q70–Q72 are criteria grounded in M3–M5; a criterion added is not a measured entry-quality move.
- **discernment: improved.** This integrator's outside spot-check agrees with the gate on the admit (S281) and on the reject (S282) — the LEARNING.md condition for `improved`. The sample is two gate decisions and two triage closes; the one disagreement (the `fixed-verified` label on the R84-V9-R91 judgment close) is recorded by the lane in M14 and is routed for a correction row.

## 6. Routed defects for the lane (round 92)

Verified in committed source unless marked otherwise.

1. **C1 case-id parser (M7).** `plans/round91_c1_replay.py` `parse_receipt()` (lines 80–84) reads `id` from `key=value` tokens; the receipt has no `id=` token. Fix under a new frozen predicate, with the probe receipt's ten `ok=True` lines as the red-then-green witness.
2. **C1 unguarded host probe (M12).** `plans/round91_c1_replay.py` line 243 `subprocess.run(["openssl","version"])` is unguarded. Every host probe in the counter must emit `DEFECT SETUP` on failure.
3. **C3 selftest outside the predicate path (M8).** `plans/round91_burndown.py` lines 398–399 run `selftest()` only under `--selftest`. Run it in the default predicate path and fail on any red case.
4. **C3 checks read the working tree (M11).** `plans/round91_burndown.py` line 118 `cwd=lane_root`. Run checks in a `git worktree` at the measured revision.
5. **C2 `--skip-selftest` escape (M9).** `plans/round91_counter_pin.py` lines 16, 115, 129, 256. The predicate says the selftest runs in the same invocation; the escape defeats that. Remove it from the predicate path, or pin its absence. Also pin the selftest's expected-rc table in the predicate path.
6. **R82-V8 clone-path default (M6).** `plans/round83_c2_checks.py` line 168 `R83_FLEET_REPO` defaults to `origin.parent`. Unchanged this round; route to a `SHOKUNIN_ROOT`-pinned checker with its own counter.
7. **Gate closure rules (M10, M13).** A closing check must reference the row's own evidence path; a blocked owner must resolve to a lane id; supersede chains need a chain-aware rule with its own selftest case (eight round-91 rows supersede round-90 rows, and the one-level gate ignores them).
8. **Disposition wording (M14).** Add an append-only correction row for R84-V9-R91 (`fixed-verified` on a judgment close). Do not edit the existing row.
9. **Blind-spot capture pins (M5).** S260, S261, S265, S266 carry no capture pin; capture them through supersede rows, one per row.
10. **Carry-over.** Round-90 routed C1 and C3 defects were routed to round 91 and not landed there (the frozen-rule reasons are in the report). They are routed again above. Not a conformance defect; recorded as repeated routing.
11. **Erratum owed.** The "14 controls" wording in the report's wave bullet (see §1).

## 7. Notes for the operator (not a lane write)

- SHONEN boxes: from committed bytes, box 2 (end-to-end task in `LOG.md` plus receipt `corpus/evidence/round91/modernize-probe.txt`) and box 4 (`PROVINCE.md` Adjacent section) look checkable by a non-author. Promotion is operator-owned; no `[x]` was written here.
- Lane counters and gates were evidence-verified from the committed transcript, not re-executed; this is the protocol's required posture for sibling gates.
