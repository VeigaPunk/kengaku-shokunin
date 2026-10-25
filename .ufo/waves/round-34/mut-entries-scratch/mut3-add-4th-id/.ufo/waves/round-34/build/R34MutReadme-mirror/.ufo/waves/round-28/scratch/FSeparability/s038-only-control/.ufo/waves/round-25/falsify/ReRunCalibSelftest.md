ATTACKS: C1 failure capability — rerun of plans/attrib_calibration.py --selftest at tip 8ea41f9ed plus per-red-case vacuity hunts (detector-kill mutations in scratch copies).

Setup: pristine `git archive 8ea41f9ed` extracted to /tmp/k25w2-ReRunCalibSelftest; script sha256 92aa8739… == tip blob; live lane read-only. No installs (system python3 3.14.8 only).

REPRODUCE
- `python3 plans/attrib_calibration.py --selftest` (tip archive): 14 checks, 0 failed, exit 0; two runs byte-identical.
- Tip-committed receipt corpus/evidence/round25-calibration/attrib-calibration-selftest.txt == fresh rerun byte-for-byte except the author-appended `exit=0` line; carries all 7 red lines. Claims:62-63 registers 3 red capabilities; the script ships 7 (R1,R1b,R2,R3,R4,R5,R6) — superset, honest.

PER-CASE VERDICT (probe_reds.py dumps each red tree's complete mismatch set)
- R1 flip GT cell — GENUINE, over-determined: 6 mismatches across 4 independent detectors (rows:correct@15, gt_counts@29, accuracy@30, score_summary.correct/accuracy/gt_counts@31). Killing the rows:correct detector in a scratch copy leaves R1 passing (14/0) via the other three — redundancy, not vacuity. Predicate is exit-code-only (no reason assert); safe because F2 pins green at exit 0 and `_mutate()` raises unless the anchor occurs exactly once (no silent no-op).
- R1b GT+correct flipped, stored kept — GENUINE: rows self-consistent so rows:correct correctly stays silent; 5 mismatches (gt_counts; accuracy [17,17,'1.000','PASS'] vs [16,17,'0.941','PASS']; 3×score_summary). Exit-code-only predicate, same mitigations.
- R2 CP anchor +1e-6 — GENUINE and precise: perturbs the WANT value against tol 1e-9 and requires exactly one new failure named "cp lo 7/50 scipy" (count==1 blocks mass-failure masking).
- R3 duplicate counted twice — GENUINE but META: in-process `analyze(green, dedup=False)` vs hand-derived FX totals → 4 failures (correct 89≠69, duplicates 0≠1, scored_trials 99≠79, unique_samples 7≠6). `bool()` predicate only; never exercises CLI exit propagation (that path is F1/F2 with dedup=True default).
- R4 stored FAIL→PASS — GENUINE and PRECISE: exactly 1 mismatch (accuracy verdict word; k/n/point identical), the only detector that can see it. Killing `_point_verdict` re-derivation in a scratch copy → R4 FAIL (exit 0) while F1/F2/G1 stay green, and the selftest correctly prints FAIL and exits 1.
- R5 one byte on frozen receipt — GENUINE, reason-checked: requires exit 1 AND "sha256" in the first stderr line ("attrib-r23-stream.log: sha256 ae55c6aa… != frozen afaae9dd…"). G1 green control runs in the same pass; killing the sha comparison → R5 FAIL. Covers 1 of 9 receipts (G1 hashes all 9).
- R6 empty population — GENUINE, reason-checked: exit 2, no vacuous PASS; killing the population gate → R6 FAIL with exit 0.

HARNESS
- Broken red cases surface: every detector-kill run printed `selftest FAIL <id>` and exited 1. `_mutate` raising on anchor count≠1 means a future edit that orphans a mutation anchor cannot pass silently.

RESIDUAL GAPS (low)
- R1/R1b/R4/R3 assert the outcome (exit code / non-empty) not the failure REASON; the reason is verified only by the printed detail a human reads. Causality is pinned today by F2 + count==1 anchors, but a regression making e.g. R4 exit 1 via an unrelated parse error would still print ok.
- No red case flips a TARGET/BODY/STREAM TARGET/score_summary stored line (green-covered in F1; same chk machinery R4 exercises). R3 never reaches the CLI.

SIDE OBSERVATION (not judged here)
- Live working tree ≠ tip: plans/attrib_calibration.py sha 42439ebc… (adds rg_bound3, Amendment-2 non-firing specificity rule, per-estimate iid_fragile; live selftest 18 checks 0 failed; working-copy receipt shows a 6-value A3). In-flight wave-2 amendment; C1-at-tip conclusions above are unaffected.

VERDICT: SURVIVES — all seven red cases genuinely exercise the failures they name (R4/R5/R6 proven by detector-kill, R1/R1b over-determined, R2 precise); no vacuous red found; committed receipts reproduce at the tip.
Installs: none (system python3 only).
