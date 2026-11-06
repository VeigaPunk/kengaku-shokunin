# ExecC1 — R99-C1 independent re-measurement

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, T `f72a8bc7`, BASE `2233a661`, scratch `/fast/scratch/hyaku/kengaku-r99/ExecC1` (removed after receipts copied). No production edits, no commits, no task calls.

Tooling: `uv` 0.13.0 (existing). Own venv `uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2 scipy==1.16.1` → numpy 2.5.4. (Pacman guard noted; no pacman used.)

## Verdicts

- **C1-T: PASS (claim met)** — frozen counter at T printed `REV f72a8bc7…`, all legs L1–L11 pass, exact TARGET line (`executed_rows=43 … defects=0`), `PREDICATE R99-C1 pass`, rc=0. Evidence: `.ufo/waves/round-99/w1/ExecC1/c1-T.txt`.
- **C1-BASE: FAIL (do-nothing control, as expected)** — same counter with `--rev 2233a661…` printed `PREDICATE R99-C1 fail`, rc=1 (all legs fail: receipt/probe/case-table absent at BASE, ledger still 42/33). At the BASE checkout the counter file itself is absent (rc=2). Evidence: `.ufo/waves/round-99/w1/ExecC1/c1-BASE2.txt`, `commands.txt`.
- **Probe determinism: CONFIRMED** — two independent probe runs from a `git archive` of T; OBSERVATIONS blocks byte-identical to each other and to committed `corpus/evidence/round99/bnfit-probe.txt` (diff empty). Evidence: `probe-run1.txt`, `probe-run2.txt`, `obs1.txt`, `obs2.txt`, `obs-committed.txt`.
- **Gap C03 marginal-only: REPRODUCED** — U,R,Y,M=0.0, D~N(true_mean,true_std) seeded RNG (own seed 20261106, KS stat 0.007433 p 0.636): captured `test_outputs.py` under real pytest (path-rewritten copy) → 9 passed, rc=0. Evidence: `C03-pytest.txt`, `build_gaps.py`.
- **Gap C07 dup-edges-extra: REPRODUCED** — learned edges each listed twice + extra `weight` column: 9 passed, rc=0. Evidence: `C07-pytest.txt`.
- **Gap C11 KS band edge (+0.045 sd): REPRODUCED** — KS statistic 0.018001, p=0.003028 ≥ 0.001: 9 passed, rc=0 (matches frozen prediction D=0.0180, p=0.0030). Evidence: `C11-pytest.txt`, `commands.txt`.
- **Gap C12 KS band edge (+0.050 sd): REPRODUCED** — KS statistic 0.019995, p=0.000664 < 0.001: 8 passed / 1 failed (`test_sampled_data`), rc=1 (matches D=0.0200, p=0.00066). Evidence: `C12-pytest.txt`.

## Notes

- Independent gap builders use own derivations (own seed for C03; own dup/weight construction; own quantile-grid code), sharing only the frozen true_mean/true_std constants from `test_outputs.py` and the prediction targets in `plans/round99-cases.json`.
- C11/C12 KS values are deterministic functions of the quantile grid; probe's own comment confirms the design (dry-run-1 lesson M1). My run reproduces them exactly.
- No defects found in the counter or probe beyond the frozen claims' own located gaps, which are the subject of the claim.

Report: `.ufo/waves/round-99/w1/ExecC1.md`
