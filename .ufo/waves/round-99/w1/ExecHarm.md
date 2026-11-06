# ExecHarm — harm battery BASE 2233a661 vs T f72a8bc7 (round 99)

Method: isolated `git clone --shared` checkouts at BASE and T under
`/fast/scratch/hyaku/kengaku-r99/ExecHarm` (TMPDIR there); every listed check run
in both trees via its SKILL.md registry entry; diffs computed on full logs.
R97 venv: py3.13 + rdflib 7.1.4 + pytest 8.4.1 (`uv`, scratch venvs, official
PyPI channel). R98 venv: py3.13 + chess 1.11.2 + pytest 8.4.1. No production
edits, no commits, no pacman (guard respected).

Verdict key: **no-harm** = same verdict at BASE and T on identical defect
lines (only expected counters move); **pre-existing-red** = red at BASE too;
**NEW** = new DEFECT line or green→red introduced by R99 bytes.

## Verdict list (one line per assigned check)

- `hermetic-grader` (`python3 grader.py`): BASE rc=0 PASS, T rc=0 PASS, no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/grader-{BASE,T}.log`
- `round98-c1-replay`: BASE rc=0 PASS (fresh run `r98c1-BASE3.log`, L1–L10 pass), T rc=1 fail (two runs, see below), **green→red but expected supersession, not candidate-byte harm**. T failures: L7 `set_added=['bn-fit-modify','regex-chess']` — the leg requires `rev_set == base_set|{regex-chess}` against round-98 BASE `49a1c4f1`, so R99's correctly-ledgered `bn-fit-modify` mechanically breaks it (the ledger flip is R99-C1's own claim). L6 `rerun rc=1` is environmental: the probe needs >>60s under bwrap on this loaded host (manual rerun timed out at 60s with no case mismatch; BASE3 run passed at ~255s). Class: timing/environmental, secondary. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r98c1-BASE3.log`, `r98c1-T.log`, `r98c1-T2.log`
- `round98-c2-nested-bind`: BASE rc=0 pass (`pop=39 cleared=39`), T rc=0 pass, no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r98c2-{BASE,T}.log`
- `round97-c1-replay`: BASE rc=1 fail, T rc=1 fail, identical defect (`L6 rerun rc=0 obs=36 equal=False`) → pre-existing-red, no NEW line. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r97c1-{BASE,T}.log`
- `round52-c2`: BASE rc=1 fail, T rc=1 fail, identical 19 MISSING (rounds 87–92 scripts absent from tree since they were never landed as files), only `REGISTERED total` 173→177 (four new round99 rows) → pre-existing-red, no NEW line. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r52c2-{BASE,T}.log`
- `round63` depth (`round63_gate_checks.py depth`): BASE rc=1 fail, T rc=1 fail, identical (`DETAIL unresolved=ledger=...`), and `trio` fails identically at both → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r63depth-{BASE,T}.log`
- `round68` capability table: BASE rc=0 pass, T rc=0 pass, no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r68cap-{BASE,T}.log`
- `round72-c2`: BASE rc=0 pass, T rc=0 pass, no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r72c2-{BASE,T}.log`
- `round73-c2`: BASE rc=0 pass, T rc=0 pass (only `INSTRUMENTS total` 174→178), no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r73c2-{BASE,T}.log`
- `round74-c1`: BASE rc=1 fail, T rc=1 fail, identical 18 MISSING, counts 174→178 → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r74c1-{BASE,T}.log`
- `round74-c2`: BASE rc=1 fail, T rc=1 fail, identical single defect (`MALFORMED-ROW round88-fixgit-probe`), counts 174→178 → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r74c2-{BASE,T}.log`
- `round75-c2`: BASE rc=1 fail, T rc=1 fail, identical two defects (same `MALFORMED-ROW` + `round77-remint...flag-not-declared`), counts 174→178 → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r75c2-{BASE,T}.log`
- `round78-c1`: BASE rc=1 fail, T rc=1 fail, identical 121 defects; only `file-artifact k=33→34` (expected ledger flip) → pre-existing-red, no NEW line. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r78c1-{BASE,T}.log`
- `round79-c1`: BASE rc=1 fail, T rc=1 fail, identical single defect (`SUBJECT-MISMATCH mteb-retrieve`); `executed=42→43` expected → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r79c1-{BASE,T}.log`
- `round82-c1`: BASE rc=1 fail (25 defects, all MISSING), T rc=1 fail (29 defects), **4 NEW lines**: `ROW-SELFTEST-UNBACKED` × 4 (`round99-bnfit-probe`, `round99-c1-replay`, `round99-c2-rowscoped-bind`, `round99-provenance-build`) — the four new registry rows' selftest cell reads `none — no self-invocation mode; ...` but the gate requires the literal phrase `none declared` or a `python3 <script>` selftest command. **Not green→red** (gate red at BASE too) and the wording matches the established r96/r97/r98 row phrasing (those rows would flag identically if judged), so the class is pre-existing convention debt surfaced by new rows, not an R99 regression. Flagged per the "any new DEFECT line" rule; routed, no repair. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r82c1-{BASE,T}.log`
- `anchor-digest-check`: BASE rc=1 `rows=325 tokens=209 defects=45`, T rc=1 `rows=333 tokens=217 defects=33` — **zero new DEFECT lines** (`comm` empty); exactly the 12 C2 population rows (S173–S177, S180, S220, S225, S270, S285, S293, S306) cleared, no others touched → improvement, no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/anchor-{BASE,T}.log`
- `freeze-integrity` r93 (`round93_freeze_integrity.py`, F=d8d0a4b8): BASE rc=1 fail, T rc=1 fail, byte-identical (`plans/round93_c1_replay.py` `touched=2`, commits `09717e49` + `3f300cbd` both round 96 — the latter is the documented Q78 revert) → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r93fi-{BASE,T}.log`
- `freeze-integrity` r94 (v2, F=844c504e): BASE rc=1 fail, T rc=1 fail, identical (`plans/round94_c1_replay.py` `touched=2`, same round-96 commits) → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r94fi-{BASE,T}.log`
- `freeze-integrity` r95 (`round95_c2_counter.py` driving `round94_freeze_integrity.py`, F=d9cd18a7): BASE rc=1 fail (W1–W3,W5 pass, W4 fail `round95_c1_replay.py touched=2`), T rc=1 fail, identical → pre-existing-red. Evidence: `.ufo/waves/round-99/w1/ExecHarm/r95c2-{BASE,T}.log`
- `git diff --name-status F T`: exactly the 11 candidate-bytes files (SKILL.md, ledger, SOURCES.md, 8× `corpus/evidence/round<N>/PROVENANCE.md`) plus `corpus/evidence/round99/bnfit-probe.txt` → matches claims receipt rule; all 11 candidate sha256 re-verified equal to the `plans/round-99-claims.md` table at T; all 18 frozen-instruments intact at T. Evidence: `.ufo/waves/round-99/w1/ExecHarm/git-diff-F-T.txt`
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: rc=0 `kengaku ok` at current tree → no-harm. Evidence: `.ufo/waves/round-99/w1/ExecHarm/census.log`

## Summary

No green→red caused by candidate bytes. The one mechanical green→red
(`round98-c1` L7) is the older counter's set-equality leg doing its job
against R99-C1's own ledger addition (supersession). All other reds are
identical at BASE and T (pre-existing: round-96 touches on r93–r95 freeze
instruments, long-standing missing round 87–92 scripts, owner-row wording,
and the `r97c1` L6 rerun drift). The four new `r82c1` SELFTEST-UNBACKED
lines ride on R99's own registry rows and match the r96–r98 phrasing
convention; gate was red before and after. Gate findings 45→33 via exactly
the 12 claimed rows; nothing else moved.

Tooling installs (recorded per RULES.md): `uv 0.13.0` venvs under scratch
(`G97`: rdflib 7.1.4, pytest 8.4.1; `G98`: chess 1.11.2, pytest 8.4.1) via
`uv pip install` from official PyPI — reason: r97/r98 grader venv pins.
No pacman transactions (guard respected).
