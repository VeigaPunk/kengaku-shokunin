# FxFamilyF3 — round 26 FALSIFY

Axes: F3 transform fidelity; frozen-population eligibility; format strata; composite sensitivity; D1 policy framing.

## Finding — MEDIUM: oracle F3 is not the amended compact↔indented transform

Amendment 1 defines F3 as compact↔indented serialization (`plans/round-26-claims.md:183-187`); core flips serialization in `_dump_like(..., flip=True)` (`plans/grader_perturb.py:307-322,419-423`). The independent oracle instead calls `_replace_extracted` (`plans/fixtures/r26/perturb_oracle.py:293-294`), which chooses `indent=2` exactly when the existing fenced body already has line breaks, otherwise compact (`:231-238`). Thus it retains the existing layout class rather than flipping it. Its bare-answer path also replaces the whole raw response (`:238`), not only the selected answer span.

Concrete frozen case: `corpus/evidence/round8-horizon/results.jsonl:38` (A-INC, pid 2, turn 7, baseline PASS, FJM). Independent replay observed multiline source; core F3 emits a compact answer; oracle retains multiline; all three parse to the same object. The independent raw scan found oracle/core transformed text differs on 1964/1964 records, while oracle's extracted answer remains unchanged on all 1964. A small fenced indented edge with no newline before the closing fence is an exact oracle no-op; `family_counts` counts any non-`None` transform without rejecting identity (`perturb_oracle.py:322-344`). Matching n/k therefore does not independently validate Amendment 1's exact F3 transform. Correct/qualify this oracle claim before using it as exact-transform corroboration.

## Frozen-raw F3 result

Independent recomputation read the four absolute frozen JSONL paths, checked their SHA-256 pins, reconstructed meta truth and baseline replay, and independently implemented F3 span/flip/re-grade. The computation imports only `grader.py` for canonical extraction/grading; it does not use the audit summary, `build_population`, or the oracle population/count routines.

Command: `python3 /tmp/r26_f3_independent.py` — **EXIT=0**. Output: pins all match; candidates 1964, baseline-replayed included 1964, excluded 0; extracted values dict 1720/list 244; F3 **n=1964, k=1964**; null extractions 0, missing spans 0, no-op transforms 0, parsed-answer changes 0. All 1964 core transformations changed raw text and retained the extracted value.

Format n/k (baseline PASS + FAIL records): FJ1 1296/1296 (710+586); FJM 492/492 (268+224); MULTI 31/31 (17+14); DANGLE 57/57 (17+40); BARE 88/88 (9+79). No stratum has an observed flip. The file composite is **210/210**, 0 failed units; unit is file+pid, except C cells file+cell+rep (`grader_perturb.py:484-487`). This is finite-population invariance, not future-input assurance; MULTI and DANGLE nominal CP95 lower bounds are below .95, and raw+want+grader has 513 excess duplicates.

Commands/results: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary` — EXIT=0; `FAMILY F3 kind=MP n=1964 k=1964`; classes and composite exactly as above. `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — EXIT=0; `F3 kind=MP n=1964 k=1964`. Agreement is count-only, not transform fidelity. Relevant draft sentences: `grader-perturbation-audit.md:42-44,56-65`.
Selftest: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary --selftest` — EXIT=0; F3 PASS; 10 families, 0 failed; mutation-catch 12/12.

## D1 and verification gaps

Draft D1 wording (`grader-perturbation-audit.md:50-52`) is correct: D1 is policy-conformance capture, not MP correctness invariance. Core gates it on baseline PASS, turn>1, state/sequence grader, excludes A-MONO/B/C and unchanged previous truth, and scores capture of previous truth (`grader_perturb.py:438-449,490-496`; Amendment 1 `round-26-claims.md:188-191`).

No LSP device/server is mounted (`read xd://lsp` returned “No such tool”); semantic references/definition/diagnostics were unavailable. Source locations here are direct file reads, not LSP findings. Residual scope is the four frozen, pinned populations only.

VERDICT: HOLD (advisory): scoped core F3 invariance is supported; qualify or repair/re-run the independent oracle's F3 transform before treating its matching count as exact-transform corroboration or admitting that draft claim.