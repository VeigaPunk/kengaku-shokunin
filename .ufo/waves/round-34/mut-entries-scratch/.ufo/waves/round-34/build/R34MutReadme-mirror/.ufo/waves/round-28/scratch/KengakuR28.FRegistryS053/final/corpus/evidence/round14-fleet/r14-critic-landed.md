# Round 14 landed-evidence critique

Independent audit of `corpus/evidence/round12-ladder/results-r12.jsonl`.  The
recompute below was fresh stdlib-only code written for this audit; it did not
import `recompute_r12.py`:

```sh
python3 /tmp/r14critic_verify.py
```

`/tmp/r14critic_verify.py` is only the execution harness; the committed inputs
and every cited output below are in-repo.  The commands are rerunnable from the
repository root.  `[INFERENCE]` is used where the evidence is not directly
observable at the stored timestamp resolution.

## Claims and independent outputs

1. **Census — REPRODUCE.** Command: `python3 /tmp/r14critic_verify.py`. Output:
   `CENSUS: {'descriptors': 1, 'meta': 64, 'meta2': 48, 'filler': 416, ...}`;
   the full cell tally is 4114 records and `CENSUS_ERRORS: 0`.
2. **A-INC final census — REPRODUCE.** Output: `ARM A-INC: pass 48/64 ...
   mean_final_nwrong=0.2969 mean_shared=0.2760`.
3. **A-CKPT4710 final census — REPRODUCE.** Output: `ARM A-CKPT4710: pass
   28/64 ... mean_final_nwrong=0.8125 mean_shared=0.7135`.
4. **A-CKPT710 final census — REPRODUCE.** Output: `ARM A-CKPT710: pass 21/64
   ... mean_final_nwrong=1.0469 mean_shared=1.0391`.
5. **A-CKPT10 final census — REPRODUCE.** Output: `ARM A-CKPT10: pass 10/64
   ... mean_final_nwrong=1.5938 mean_shared=1.5938`.
6. **A-MONO final census — REPRODUCE.** Output: `ARM A-MONO: pass 2/64 ...
   mean_final_nwrong=2.2500 mean_shared=2.2500`.
7. **Transport final censuses — REPRODUCE.** Output: `ARM T-DENSE: pass 2/48
   ... mean_final_nwrong=4.5833 mean_shared=4.4375`; `ARM T-SPARSE: pass
   2/48 ... mean_final_nwrong=4.7708 mean_shared=4.6146`.
8. **E1 listwise block selection — REPRODUCE.** Output: `E1: n_blocks=64`;
   all four ladder arms had final-turn records for every block.
9. **E1 Page L and expectation — REPRODUCE.** Output: `L=1773.0 E_L=1600.0`.
10. **E1 Page variance/z — REPRODUCE.** Output: `Ssum=201.0000
    varA(5/3*S)=335.0000 zA=+9.4520 pA=3.324e-21`.  This is the
    sum-of-ranks form using midranks for ties; `varA` is the documented
    per-block sample-variance form (equivalent to the committed `var_L=335`).
11. **E2 paired difference — REPRODUCE.** Output: `E2: diff=+0.2969 sd=0.7545
    n=64 t=+3.1480 df=63 p=0.002512 CI=[0.108,0.485]`.
12. **E2 exact sign test — REPRODUCE.** Output: `sign W/L/T=24/7/33
    sign_p=0.003327`.
13. **E2 final McNemar — PARTIAL (label orientation only).** Output:
    `E2_MC: b=5 c=12 p=0.1435`; the committed line says `b=12 c=5 p=0.1435`.
    The unordered discordant counts and p-value reproduce exactly, but the
    b/c names are transposed under my explicit convention (b = 710 pass /
    4710 fail). This does not alter the reported verdict.
14. **E3 adjacent 4710 minus INC — REPRODUCE.** Output: `E3a: diff=+0.4375
    sd=0.6024 n=64 t=+5.8102 p=2.226e-07` (file rounds diff/p to +0.438/0.0000).
15. **E3 adjacent 710 minus 4710 — REPRODUCE.** Output: `E3b: diff=+0.2969
    sd=0.7545 n=64 t=+3.1480 p=0.002512`.
16. **E3 adjacent 10 minus 710 — REPRODUCE.** Output: `E3c: diff=+0.5469
    sd=0.8716 n=64 t=+5.0196 p=4.517e-06`.
17. **E4 MONO minus CKPT10 — REPRODUCE.** Output: `E4: diff=+0.6562 sd=1.1577
    n=64 t=+4.5348 p=2.642e-05 sign W/L/T=34/8/22`.
18. **E5 SPARSE minus DENSE — REPRODUCE.** Output: `E5: diff=+0.1771 sd=1.0693
    n=48 t=+1.1473 p=0.2571 sign W/L/T=22/16/10`.
19. **Re-grade and truth replay — REPRODUCE.** Commands: `python3
    /tmp/r14critic_verify.py`; independently replayed operation semantics. Output:
    `REGRADE: 1328 graded; stored-field mismatches=0`; `TRUTH: f1 replay
    mismatched pids=0/64; f2 replay mismatched pids=0/48`.
20. **Raw-output parse audit — REPRODUCE.** Command:
    `python3 - <<'PY' ...` (the lenient raw parser strips optional fences and
    uses `JSONDecoder.raw_decode`). Output: `lenient re-parse 1328: fail=0
    got_mismatch=0`. The initial strict parser's 29 failures were malformed
    trailing-fence cases; they were all recovered, not data mismatches.
21. **Finish audit — REPRODUCE.** Output: `FINISH: finish=length 0/1328`.
22. **Forecast pass Brier — REPRODUCE.** Output: `E6_PASS_BRIER:
    pooled=0.1288 N=416`; arm outputs are `A-INC 0.1959`, `A-CKPT4710
    0.1294`, `A-CKPT710 0.1155`, `A-CKPT10 0.0743`, `A-MONO 0.0734`,
    `T-DENSE 0.2092`, `T-SPARSE 0.1220`.
23. **Forecast sign Brier — REPRODUCE.** Output: `E6_SIGN_BRIER:
    pooled=0.2469 N=304`; per contrast: `E3a 0.2500`, `E3b 0.2354`,
    `E3c 0.2500`, `E4 0.2500`, `E5 0.2500`.
24. **Forecast BSS and calibration — REPRODUCE.** Outputs: `E6_BSS_PASS:
    BSS=+0.0447`; `E6_BSS_SIGN: BSS=-0.0106`; `E6_BSS_RL: BSS=-1.2604`;
    `E6_BSS_ALL: BSS=+0.0049`; `E6_CALIB_PASS: slope=+0.8427
    intercept=-0.7511`; `E6_CALIB_ALL: slope=+0.8427 intercept=-0.3491`.
25. **E6 event totals and realized outcomes — REPRODUCE.** Output:
    `RL_OUT: RL1-7 realized=[1, 1, 1, 1, 1, 0, 1]`; `E6_BRIER_RL: 0.2768
    N=7`; `E6_BRIER_ALL: 0.1796 N=727`.
26. **Run-log summary cells — REPRODUCE.** Command: `sed -n '418,427p'
    corpus/evidence/round12-ladder/run.log`. Output lines: `A-INC: 48/64`,
    `A-CKPT4710: 28/64`, `A-CKPT710: 21/64`, `A-CKPT10: 10/64`, `A-MONO:
    2/64`, `T-DENSE: 2/48`, `T-SPARSE: 2/48`, `wall_total_s: 701.6`, `EXIT=0`.
    The seven cells match the independent census exactly.
27. **Run-log execution coverage — REPRODUCE.** Command: the independent
    run-log enumeration in the audit harness. Output: `progress lines: 416;
    each (arm,pid) exactly once: f1 True f2 True total 416`.
28. **Prediction input hashes — REPRODUCE.** Command: `sha256sum -c
    corpus/evidence/round12-ladder/prereg-bundle.sha256`. Output: all nine
    entries `OK` (the harness prints each `...: OK`).

## Regeneration comparison

Command:

```sh
python3 corpus/evidence/round12-ladder/recompute_r12.py \
  --results corpus/evidence/round12-ladder/results-r12.jsonl \
  --out /tmp/r14-analysis-regen.md
md5sum /tmp/r14-analysis-regen.md corpus/evidence/round12-ladder/analysis_r12.md
cmp /tmp/r14-analysis-regen.md corpus/evidence/round12-ladder/analysis_r12.md
```

Observed:

```text
e8d5e458ae03aac64cec442dd64ac499  /tmp/r14-analysis-regen.md
029c3bcdcf11209d575734742bf239f6  corpus/evidence/round12-ladder/analysis_r12.md
... differ: char 4721, line 66
```

**Verdict: PARTIAL, not byte-identical.** `diff` shows the sole difference is
line 66's absolute path casing: regenerated `/home/vgpnk/Projects/...` versus
committed `/home/vgpnk/projects/...`; the SHA and all substantive analysis
bytes are identical. The lowercase path does not exist on this workstation,
so exact byte identity cannot be obtained without mutating evidence or
creating an unrelated path alias.

## Ordering chain and hashes

Command: `python3 /tmp/r14critic_verify.py`, plus
`sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256`.
Observed bundle output: all 9/9 `OK`. Run-script lines from
`ordering.log` match working-tree SHA256 bytes:

```text
probe_r12.py 1871697f5c3410adf3c17297138e76416cdeb63194038324eec067abe6b90662
run_r12.py   3beb91ea705a85636bd232074a5c71b9c64f8aa5b9995f3e3376aa849fdecddf
```

Observed current hashes: `results-r12.jsonl sha256=
ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1 md5=
9dd8aa2b6a7aa7890aa802c37d5af0f9`; `run.log sha256=
361141901ae823afd003c6b4cc95d25b5c8681121c783a7fa9745ffc2b53d60e md5=
700d1ddd2ece50d7bdedd55859c59f3a` (the md5 suffix is recorded exactly by
`md5sum`; see command output in the harness).

`ordering.log` records `pre-hash 2026-09-29T01:16:08Z`, run-script hashes at
that same time, and `main-run-launch 2026-09-29T01:19:59Z`. Independent scan
of all 4002 `request_ts` values gives `min_ts=2026-09-29T01:19:59Z`,
`max_ts=2026-09-29T01:31:41Z`, and `request_ts < launch: 0`.

**Ordering verdict: PARTIAL.** The nondecreasing chain is reproduced, but the
requested strict relation `pre-hash < launch < first request_ts` is not
observable: launch equals the earliest recorded request timestamp to 1-second
precision (`01:19:59Z`). This is `[INFERENCE]` only as a claim about actual
sub-second event order; the stored evidence proves `launch <= first request_ts`,
not strict `<`.

## Gaps

* The regeneration is not byte-identical solely because of an absolute path
  spelling/case in one generated provenance line; all substantive bytes match.
* `ordering.log` has one-second timestamp granularity, so it cannot establish
  a strict launch-before-first-request relation when both serialize to
  `01:19:59Z`.
* The E2 McNemar b/c labels are transposed relative to the explicit convention
  used here; the unordered discordant counts and p-value are exact.
* `run.log wall_total_s=701.6` is a logged wall-clock total, not the sum of
  per-record `wall_s` (the independent sum is 703.8); it is therefore verified
  as the logged summary cell and not derived as an additive record sum.
