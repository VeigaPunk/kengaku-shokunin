# ExecC3TriageB — routed-findings triage, half B (drafts only)

Seat `ExecC3TriageB`, round 91, wave w1. Lane clone `$S/lane` at `a8de3e69` (detached, `git clone --shared`). The ledger `corpus/routed-findings.jsonl` (213 rows, all parse) was read, not edited. Resolution rows are in `resolutions.jsonl` (16 rows, one per finding, each `supersedes` its base id).

Verification run for all rows (from the clone root):
- Parse: 16 rows, one JSON object per line; no new id collides with an existing ledger id; no cell contains a pipe.
- Source: `git show a8de3e69:<path>` then the line at `<line>` is non-blank for all 16 rows (python, `git show` per row; all True).
- Checks: each closed row's `check` run with `bash -c` from the clone root; exit 0 for the seven closed rows.
- Able to fail: each closed check re-run with its anchor token replaced by an absent token; exit 1 for all seven.

Verdict summary (16 rows): closed 7 (R87-V5, R89-A2-4, R89-A2-6, R89-A2-7, R89-D2, R89-D3, R89-D6); blocked 8 (R87-V6, R88-2, R88-3, R89-A2-1, R89-A2-2, R89-A2-3, R89-A2-5, R89-D4); refused 1 (R87-V1).

## 1. R87-V1 — refused (owner kengaku retained)

- Source `corpus/lessons/round-87-verifier-spotcheck.md:125` non-blank.
- `.ufo/l0-questions.md:312` (fleet root, read only) still reads "Decision wanted: should the drain flag block the spawn of an already-launched round's wave (no answer assumed; the lane keeps waiting on the handoff)." No answer exists.
- `test -e .ufo/waves/round-88/w1.ready.dispatched` at `a8de3e69` exists (content timestamp 2026-11-05T02:37:11). The next-round dispatch clause of V1 is met by round 88.
- Decision: refused with the quoted standing L0 question. The round-87 non-dispatch is historical; the operator question governs it. No check (null).

## 2. R87-V5 — closed

- Command: `grep -q -F 'coverage stays at **7** (L0 cap)' SCORECARD.md`; exit 0.
- Observed: the Round 87 section's C1 row reads "met on its frozen predicate; coverage stays at **7** (L0 cap)" beside "Ledger executed 30 → 31".
- Negative: anchor replaced by `zzz-absent`; exit 1.

## 3. R87-V6 — blocked (owner kengaku)

- Command: `grep -n -i stale .ufo/reports/round-87/kengaku.md` (fleet root, read only); exit 0.
- Observed line 83: "Stale-lane: no other mission of this lane is open; round 87 attempt 1 is the only open mission." The mission is named but not stated as progressing or silent.
- Decision: blocked; the correction is a dated line in the round-91 report, because the filed round-87 report is append-only.

## 4. R88-2 — blocked (owner kengaku)

- Command: `grep -c 'four SELFTEST' LOG.md`; exit 1 (count 0).
- Command: `git grep -n 'four SELFTEST' a8de3e69`; exit 0. Matches: `corpus/lessons/round-88-verifier-spotcheck.md:69`, the round-88 lesson's own line, and round-90 wave triage copies. No correction in `LOG.md` or `corpus/lessons/round-89.md`.
- Side note: `grep -n -i 'selftest pass\|SELFTEST.*five\|five.*SELFTEST' LOG.md` matches five lines, none of them a correction for "four SELFTEST pass lines".
- Decision: blocked; the append-only correction is owed by the lane.

## 5. R88-3 — blocked (owner kengaku)

- Observed: the forged-probe pin is the constant `TRUSTED_TOOL_SHA` at `plans/round89_c1_replay.py:46`, checked at leg L9-tool (line 169). The external counter pin ledgers are `plans/counter-pins-r90.json` and `plans/counter-pins-r91.json`.
- Command: `grep -n TRUSTED_TOOL_SHA plans/counter-pins-r91.json`; exit 1 (no match). The round-91 claim text places `TRUSTED_TOOL_SHA` in `counter-pins-r91.json`; at `a8de3e69` it is not there. Recorded as an observation for the round-91 integrator; not a resolution input.
- Decision: blocked; the residuals R89-A2-1, -2, -3 and -5 are still open.

## 6. R89-A2-1 — blocked (owner kengaku)

- Command: `grep -n ancestor plans/round91_counter_pin.py`; exit 1 (no match).
- Observed: `merge-base --is-ancestor` appears only in `plans/round89_c1_replay.py:92` and `plans/round90_c1_replay.py:104`, which check the receipt `LANE_TIP`, not pins.
- Decision: blocked; fix owned by the lane's round-91 C2 instrument.

## 7. R89-A2-2 — blocked (owner kengaku)

- Command: `grep -n -i after plans/round89_claim_figures.py`; exit 0. Matches: line 104 (`SPAN_END_RE` regex), line 137 (stop tuple), line 438 (fixture string "25 before and 26 after").
- Observed: no comparison of after-figures to the measured output. The `ids=8` → `ids=9` case at `plans/round-85-claims.md:106` is not exercised.
- Decision: blocked.

## 8. R89-A2-3 — blocked (owner kengaku)

- Command: `grep -n -i surviv .ufo/waves/round-89/w1/MutTesterR89/mutants.md`; exit 0.
- Observed: M1 (line 16), M2 (line 17), M3 (line 18) and M4 (line 19) are recorded "survived" on the tip predicate. `corpus/lessons/round-89.md:118` also names M5, M7 and C2 N1, N4, N6 as unkilled by the tip predicate.
- Decision: blocked; no kill fixture is landed for them.

## 9. R89-A2-4 — closed

- Command: `grep -q 'Mistake 10' LOG.md && grep -q 'R89-D2: the control named' LOG.md && grep -q 'R89-D6: the SCORECARD C2 row' LOG.md`; exit 0.
- Observed: LOG.md:3405 carries Mistake 10 (frozen-text defects, reported, not repaired); the Round 90 Corrections paragraph carries R89-D2 and R89-D6.
- Not claimed: the repair itself, which is the operator ruling in `.ufo/l0-questions.md:319`.
- Negative: anchor `Mistake 10` → `zzz-absent`; exit 1.

## 10. R89-A2-5 — blocked (owner kengaku)

- Observed: no lane evidence of the Sentinel L1–L6 hostile-case re-test (120 s stall, empty or dot paths, control red meaning rc not zero, literal `claims=17`, working-tree prior counters, `/proc` stdout reach). The ledger note already says "not evidenced".
- Decision: blocked; not re-run here (leaf seat, scope limited to this half).

## 11. R89-A2-6 — closed

- Command: `grep -q '^HOST_USERNS ' corpus/evidence/round90/merge-diff-probe.txt && grep -q '^HOST_USERNS ' corpus/evidence/round91/modernize-probe.txt`; exit 0.
- Observed: `corpus/evidence/round90/merge-diff-probe.txt:10` `HOST_USERNS 122865`; `corpus/evidence/round91/modernize-probe.txt` `HOST_USERNS 122865`.
- Negative: anchor → `^ZZZ_ABSENT `; exit 1.

## 12. R89-A2-7 — closed (not a finding)

- Command: `grep -q 'merge-diff-arc-agi-task' .ufo/waves/round-89/w1/ScoutR89/next.md && grep -q 'merge-diff-arc-agi-task' corpus/lessons/round-90.md`; exit 0. (`grep -c merge-diff-arc-agi-task .ufo/waves/round-89/w1/ScoutR89/next.md` → 13.)
- Observed: the candidate list names the member; round 90 executed it (lesson Gate, S279).
- Decision: the row's own text says "not a defect"; the list is a planning input and was consumed.
- Negative: anchor → `zzz-absent`; exit 1.

## 13. R89-D2 — closed

- Command: `grep -q 'R89-D2: the control named' LOG.md && grep -q -F 'selftest-in-path' plans/round89_claim_figures.py`; exit 0.
- Observed: `plans/round89_claim_figures.py:546` is `"selftest-in-path": {"selftest_fn": …}`; the LOG Round 90 Corrections paragraph carries the R89-D2 text.
- Negative: anchor `selftest-in-path` → `zzz-absent`; exit 1.

## 14. R89-D3 — closed

- Command: `grep -q 'R89-D3: the round-88 before-count is 1 of 3 measured at BASE' LOG.md`; exit 0.
- Observed: the correction paragraph is present in the LOG.md Round 90 entry.
- Negative: anchor `is 1 of 3 measured` → `is 9 of 9 measured`; exit 1.

## 15. R89-D4 — blocked (owner kengaku)

- Command: `grep -n -i reject corpus/lessons/round-89.md`; exit 0 with one line (line 34, the census word "rejected"). No reject or deferral row in the round-89 Gate.
- Observed: the reason sits only in `.ufo/waves/round-89/w1/ScribeR89/knowledge-draft.md:70` ("second-seat re-read: pending (R3)").
- Observed: the round-90 Gate reject row (S280, `corpus/lessons/round-90.md:14`) is a different source. The ledger note "closed in round 90" does not meet the defect text, which asks for a row in the round-89 Gate.
- Decision: blocked; the lane appends the row to the round-89 Gate. Not closed.

## 16. R89-D6 — closed

- Command: `grep -q 'R89-D6: the SCORECARD C2 row' LOG.md && ! git cat-file -e d1c4f1b0:plans/round89-q66-records.json 2>/dev/null`; exit 0.
- Observed: the correction paragraph is present; `git cat-file -e d1c4f1b0:plans/round89-q66-records.json` exits 128 (path absent at that commit), so the frozen "freeze-commit blob" does not exist. The record-table blob `163f2843` is pinned at `plans/counter-pins-r90.json:5`.
- Negative: `d1c4f1b0:` → `a8de3e69:` in the check; exit 1.

## Limits

- No closed row rests on an unrun check. Seven closes, each checked at `a8de3e69` and negative-tested.
- Blocked owners are `kengaku` (the lane holds each fix). The operator is not named as an owner, because a blocked owner must name a lane or seat.
- The seat wrote no ledger rows, made no commits, and ran no mutating git in the lane. Scratch `$S` is removed on exit.

Tooling: none installed. Commands: `git`, `grep`, `sed`, `python3` (standard library only).
