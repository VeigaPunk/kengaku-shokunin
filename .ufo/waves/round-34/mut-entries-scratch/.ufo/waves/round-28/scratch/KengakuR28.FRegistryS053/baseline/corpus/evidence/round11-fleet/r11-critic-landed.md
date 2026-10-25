# Round-11 landed adversarial re-run

All computations below use committed bytes only. The independent calculation used `/tmp/r11_critic.py` (fresh stdlib implementation; it did not import `grader.py` or `recompute_r11.py`). No chat-completions request was issued.

1. **Census and request count — REPRODUCE.** Command: `python3 /tmp/r11_critic.py`. Observed output: `census {'descriptors': 1, 'meta': 64, 'A-CKPT4710': 192, 'A-CKPT710': 128, 'A-CKPT710-ack': 512, 'A-CKPT4710-ack': 448} total 1473 requests 1409`. The graded/filler/ack decomposition is 1/64/320/960/128/0 as stated.

2. **Observed table — REPRODUCE.** Command: `python3 /tmp/r11_critic.py`. Observed: `A-CKPT4710 passes 29 meanfinal 0.75 all 0.6927083333333334`; `A-CKPT710 passes 21 meanfinal 1.078125 all 1.0625`. Rounded values reproduce 29/64 + 21/64, 0.750 + 1.078, and 0.693 + 1.062.

3. **Paired effect and t statistic — REPRODUCE.** Command: `python3 /tmp/r11_critic.py`. Observed: `diff sd n t 0.3515625 0.8197932738835821 64 3.430742956302176`. Thus +0.352, SD 0.820, n=64, and t=+3.431 reproduce. A normal-tail cross-check for |t|=3.430743 gives two-sided p approximately 0.00060; the stored exact t-tail p=0.0011 is consistent with finite-df correction, not a contradiction. The corresponding 95% finite-df interval rounds to [+0.147,+0.556].

4. **Sign test — REPRODUCE.** Command: `python3 /tmp/r11_critic.py`. Observed: `sign 26 7 31`. The exact two-sided binomial calculation on 33 non-ties gives p=0.0013 and positive direction.

5. **McNemar — REPRODUCE.** Command: `python3 /tmp/r11_critic.py`. Observed: `mcnemar 13 5`. Exact two-sided McNemar p rounds to 0.0963.

6. **Finish and acknowledgement audits — REPRODUCE.** Command: `python3 - <<'PY' ...` (fresh scan of every JSONL record, checking finish/parse fields and lowercased raw prefix). Observed output: `finish length 0/320 parse_fail 0/320; ack 4710 220/448=49.1%; ack 710 330/512=64.5%`. This matches the landed analysis.

7. **Prediction scoring and Brier — REPRODUCE.** Command: `python3 - <<'PY' ...` (fresh arithmetic). Observed output: `passes errors 14/64=0.21875, 8/64=0.125; diff error abs(0.3515625-0.350)=0.0015625; brier=(0.0484+0.2500+0.1600)/3=0.1528`. Rounded outputs are 0.219, 0.125, 0.002, and 0.153.

8. **Mechanical verdict rule — REPRODUCE.** Command: `python3 - <<'PY' ...` reading `predictions-r11.md` §Preregistered verdict rule. Observed output: `diff>0=True p<0.05=True sign_direction=+1 t_direction=+1 => branch 1 ESTABLISHED`. The emitted `PREREGISTERED VERDICT: ESTABLISHED` agrees exactly; no sign-direction downgrade applies. McNemar remains descriptive because p is not below 0.05.

9. **Bundle hashes and ordering — REPRODUCE.** Command: `sha256sum corpus/evidence/round11-power/{probe_plan_r11.md,power_analysis_r11.md,predictions-r11.md}`. Observed: `d7fbeebe118ab2ea959d63c53e3f2d0a6eeec53b11dc155661d636c2a6ef27bf`, `ecfe96deb0b378303ae9a58e4445601682f0000367fdf1e75d6c4ed10176208e`, `e912085ce0283dd4a0cd5c2de31dde937f69d38e12e9e4970a3470d23c46a902`, exactly matching `prereg-bundle.sha256`. Command: `cat ordering.log`. Observed: pre/post `23:10:20Z`; run-script hashes `23:28:37Z`; main launch `23:28:57Z`; first request timestamp `23:28:57Z`; descriptors is JSONL record index 0. All required ≤ relations hold.

10. **Independent raw re-parse spot check — REPRODUCE.** Command: `python3 /tmp/r11_critic.py` (fresh `extract_json_block`, fresh `gen_problem(3000+pid*41)`, fresh state simulation and wrong-key count, deterministic random seed 11). Observed: `spotcheck 40 / 40`. Every sampled stored got/want/ok/nwrong re-derived from raw and regenerated meta truth.

11. **Repo replay gate — REPRODUCE.** Command: `python3 grader.py; echo grader_exit=$?`. Observed: `CHECKS n=280 mismatches=0 errata_pinned=1`, `grader_exit=0`. Command: `python3 grader.py --selftest; echo selftest_exit=$?`. Observed: `SELFTEST ALL PASS S0...S6`, `selftest_exit=0` (the concrete output reports each S0–S6 PASS).

12. **Overclaim audit — FALSIFIED CLAIMS LISTED, numerical lane remains clean.** Command: `python3 - <<'PY' ...` cross-checking every sentence in `corpus/knowledge/bench-arena-round11-power.md` against the landed numbers and the final guidance in `r11-prior-art-prereg.md`. Most wording is appropriately scoped (single served unit, no cross-model/cross-stack generalization; pass-rate dose explicitly not established). The following claims overreach the guidance and should not be repeated: (a) the novelty-pricing sentence `C3 instrument ... NOVEL-instrument ...`—the prior-art artifact's M1 guidance says the hashed-preregistration composition is INCREMENTAL and gives no basis for NOVEL; (b) `no source manipulates emission DENSITY with severity magnitude` is an exhaustive negative claim not established by the fetched-source set and should be phrased `no source found in this search`; (c) `paired contrast replicated` across r8/r9/r11 is stronger than the guidance permits for a single local served stack and should say `the r11 paired contrast reproduced the preregistered direction`; (d) `q4_0 KV measurably perturbs outputs` is supported by cited prior-art measurements but is not itself an r11 causal identification, so it must remain method context rather than an r11 finding. These are wording defects, not falsifications of the stored r11 arithmetic.

## Final assessment

All ten requested landed-number/verdict/order/raw-byte checks reproduce. The only identified defects are overclaim wording items listed in §12; they do not alter the stored statistics or the mechanical preregistered branch.

LANDED VERDICT: CLEAN
