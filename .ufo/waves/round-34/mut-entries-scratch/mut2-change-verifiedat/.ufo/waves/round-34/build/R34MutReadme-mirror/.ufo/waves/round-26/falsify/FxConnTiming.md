# FxConnTiming — Q13 boundary falsification

Axes: **calibration** (Q13 check validity); novelty/coverage unchanged; no numeric score change claimed. Scope: integrated revision `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` (`.ufo/waves/round-26/integration-revision.txt:1`).

## Evidence and reopened criteria

- Kengaku Q13 (`corpus/QUALITY.md:97-109`) is framed as a structural check of the selected landing commit's Gate-cited report; it says report presence is not endorsement and leaves Q9/Q10 resolution to the author. Round-26 lesson explicitly reserves the outside admit/reject spot-check to orchestrator closure (`corpus/lessons/round-26.md:39-41`). This is not an outside-verifier result.
- Reopened Kumitate boundary (`.ufo/waves/round-26/build/ConnKumitate.md:7-20`; `kumitate-shokunin/PROVINCE.md:3-6,28`): commit-tree support is Kengaku-local; collector `reportPresent` is a different, current collection-time fact. No dispatcher, collector, or fleet-policy change is warranted.
- Reopened Kagi QM13 (`.ufo/waves/round-26/build/ConnKagi.md:7-24`; `kagi-shokunin/corpus/QUALITY.md:72`): calibration needs a known-bad admit to fail and a bounded valid control to pass; outside agreement remains a non-author duty. The reviewer positive control below passes, but the non-reviewer negative control falsely passes.
- **Surviving false-pass:** Q13 says “registered reviewer-like seat” (`corpus/QUALITY.md:105-106`), but `plans/gate_timing_check.py:328-329` rejects only `scribe`/`executor`. The committed falsify registry includes distinct `connector`, `critic`, `scout`, and `mutation-tester` roles (`.ufo/waves/round-26/falsify/swarm-registry.json`; e.g. `FxConnTiming` is `connector`). The checker selftest registers only reviewers (`plans/gate_timing_check.py:478-484`) and has no negative role cases (`:491-508`).
- Structural limit, not endorsement: the checker uses the caller-supplied `--commit`; a later tree can pass although the actual admission tree failed (`.ufo/waves/round-26/falsify/FxGateCommit.md:5-21`). Q13's “admitting commit” is therefore a caller precondition; establish that hash independently. The round-26 candidate remains draft-only and Gate-deferred (`integration-revision.txt:5`; `corpus/lessons/round-26.md:27-34`).

## One bounded move

Replace the denylist with an explicit Kengaku-local allowlist of roles designated to perform this candidate's Q10 re-read (at minimum `reviewer` for the current round); add connector/critic/scout/mutation-tester registered-role fixtures that must fail, while retaining a reviewer same-commit green control. Keep this a commit-tree support check: do not inspect the review's stance, change fleet orchestration, or count these seats as outside verification.

Risk: a coarse role allowlist could reject a specialist explicitly assigned to a genuine Q10 re-read; name any permitted exception in the local contract rather than accepting every non-scribe/executor role. Even a reviewer-role PASS proves neither source/number correctness nor resolved findings, and never substitutes for orchestrator closure.

## Verification

- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --selftest` → `[selftest] ALL PASS (arbitrary lesson basename, generic-only/variant red, explicit/bare citation, missing/unresolved citation, registry/mode/return/self-review/unknown-writer checks)`; exit **0**.
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --repo /tmp/kengaku-r26-gate-fxplaceholder.AiekC5/q13-role-fixtures/non-reviewer-connector --lesson corpus/lessons/round-26.md --commit 3f728bab4f631de1b6b240adee2ca560a9bb7b77` → `PASS line 7 Gate admit: candidate='knowledge/grader-perturbation-audit.md'`; summary `admissions=1 passed=1 failed=0`; exit **0** (false accept; expected red for connector role).
- Same checker with `--repo /tmp/kengaku-r26-gate-fxplaceholder.AiekC5/q13-role-fixtures/valid-reviewer-control --lesson corpus/lessons/round-26.md --commit f0102b3f9826c37162d4bbb60d402e73c11da9a6` → `PASS line 7 Gate admit: candidate='knowledge/grader-perturbation-audit.md'`; `passed=1 failed=0`; exit **0** (valid control).
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` (cwd lane) → generic “wave-2 seats” cited paths `none`, `second-seat-reports=0`, exit **1**. This known-bad red does not catch the role false-pass above.
- Install/update: none.

VERDICT: Reopen Q13 calibration: it is correctly bounded away from fleet orchestration and outside verification, but the integrated checker admits a registered connector as reviewer-like support (reproduced, exit 0); require explicit Q10-role eligibility and negative role controls before relying on it for admission.