ATTACKS: committed C1 receipt `attrib-calibration-summary.txt` — byte-exact rerun from pristine 8ea41f9ed, plus determinism, provenance, non-vacuity, and live-drift probes.

## Result of the assigned rerun — PASSES
- Pristine copy: `git -C kengaku-shokunin archive 8ea41f9ed | tar -x -C /tmp/k25w2-ReRunCalibSummary` (HEAD confirmed 8ea41f9ed).
- `python3 plans/attrib_calibration.py --summary` (cwd=copy, Python 3.14.8): exit=0, stderr empty, 49 lines / 9036 bytes.
- `cmp run1.out corpus/evidence/round25-calibration/attrib-calibration-summary.txt` → "EOF on run1.out after byte 9036": run output is a pure byte-prefix of the receipt; receipt = output + exactly one trailing line `exit=0` (diff: `49a50 > exit=0`). No other byte differs → within the allowed trailing-exit-line carve-out. Receipt line 1..49 (incl. TOTAL, mismatches=0) byte-identical.

## Determinism / environment — no counterexample
- 6 runs identical: sha256 `b009794d9a34bdcb…` under PYTHONHASHSEED=0 / 424242 / random, LC_ALL=C / de_DE.UTF-8, TZ=Pacific/Kiritimati.
- Interpreter portability: uv cpython-3.12.15 from foreign cwd (/tmp) → same sha `b009794d…`, exit 0; py3.14.8 == py3.12.15 byte-identical. Output has no cwd/root leak in --summary mode (no `attrib_calibration: root …` header line).
- Side effects: `find . -newer <marker>` after a run → zero files touched; `--summary` is read-only.

## Receipt provenance — committed content is what reruns
- sha256 `b7bdc0602dd070a3c…` identical for live file, archive copy, and `git show 8ea41f9ed:<path>` blob.

## Non-vacuity (mutation probe, scratch copy only) — instrument bites
- Edited one stored line: `corpus/evidence/attrib-r21-impl-ds-trials.log:297` `ACCURACY: 20/20 = 1.000 … -> PASS` → `19/20 = 0.950 … -> PASS`.
- Rerun: exit=1, stderr 230 B: `MISMATCH attrib-r21-impl-ds-trials.log: sha256 990e4c8f… != frozen 1dddb3d6…` AND `MISMATCH …:297 accuracy: stored=[19,20,'0.950','PASS'] recomputed=[20,20,'1.000','PASS']`; TOTAL `mismatches=2`. Both the frozen-sha manifest and stored-line re-derivation independently detect tampering.

## Finding (observation, not a receipt break): live tree drifts from the committed instrument
- `git status --porcelain`: ` M plans/attrib_calibration.py` (+10 other dirty paths) at 8ea41f9ed.
- Live script adds uncommitted "Amendment 2 (round-25 falsify, CritSpecificity)" non-firing-specificity logic (plans/attrib_calibration.py:447-451,633-634 in worktree).
- Live script + live root → exit 0 but output differs from committed receipt in exactly 5 specificity lines (`interval=PASS` → `interval=- non-firing`) and TOTAL `PASS=12` → `PASS=7`.
- Isolation: committed script + live root → sha `b009794d…` exit 0 → live P1 evidence files are UNDRIFTED; divergence is 100% script drift.
- Consequence: the receipt is reproducible at the committed tip but NOT from the current live worktree; if Amendment 2 lands, C1 summary + TOTAL PASS counts must be re-minted.

## Residual risk / gaps
- Did not run `--selftest` (out of scope; covered by StateSelftestExec seat) and did not re-mint timestamps/authorship of the receipt — byte-match is the criterion and it holds.
- Live untracked extra `plans/fixtures/r25/l0_filed_check/queue-prose-mention.md` and dirty docs (LOG/PROVINCE/SCORECARD/SOURCES) are wave-in-flight state, not C1 inputs.

VERDICT: SURVIVES — committed C1 summary receipt reruns byte-exactly from pristine 8ea41f9ed (only the allowed trailing `exit=0` line differs), environment/interpreter-stable, tamper-detecting; sole finding is uncommitted Amendment-2 worktree drift that will force a re-mint if landed.
INSTALLS: uv python install 3.12 (cpython-3.12.15, official Astral standalone channel; reason: cross-interpreter determinism probe). No pacman transactions (host-wide pause respected).
