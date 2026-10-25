# FxEntryAll — complete Q10 second-seat re-read (attempt 1)
writer: KengakuR26-2.FxEntryAll
candidate: `corpus/knowledge/grader-perturbation-audit.md`
draft: `.ufo/waves/round-26/drafts/grader-perturbation-audit.md`
Scope: Q1–Q13, current integrated draft and source/number evidence; advisory only.

## Findings by severity

- **BLOCKER — Q11 bound is asserted but not shown.** Draft lines 74–76 says all nine pooled MP/MC rates clear 0.95, but table lines 61–72 gives only k/n. `corpus/QUALITY.md:82-85` requires the exact two-sided CP95 lower bound for a PASS claim. Independently rederived lower bounds are F1/F2 .985079; F3/F5/F6 .998124; F4 .997858; F7 .998036; G1/G2 .996394. The draft has the F1/F2 composite and D1 intervals, not these pooled bounds. Add the pooled CP95 bounds (or full intervals) before admission.
- **BLOCKER — F1 is misdescribed.** Draft lines 40–42 says F1 removes the last fence's *language label*. Current `plans/grader_perturb.py:403-408` replaces the entire matched fence with its JSON body, removing both delimiters and keeping JSON. The registered result (17 flips) is for full fence stripping; merely removing the label leaves an optional-tag fence parseable and is a different transform. `plans/fixtures/r26/perturb_cases.jsonl` B10-F1 also labels it “remove only the last parseable answer fence.” Reword F1 as stripping only the last matched fence while retaining its body; keep the all-fences distinction.

## Independent number re-read

Commands from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:
- `python3 plans/grader_perturb.py --summary` → exit 0; current output `population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`.
- `python3 plans/fixtures/r26/perturb_oracle.py --root .` → exit 0; independent oracle agrees: F1/F2 1802/1819; F3 1964/1964; F4 1720/1720; F5/F6 1964/1964; F7 1876/1876; D1 909/909; G1/G2 1021/1021.
- Separate `/tmp/fx_rederive.py` replay/counting and independent CP calculation → exit 0: file counts 188/128/320/1328 (sum 1964); PASS/FAIL 1021/943; state/seq/grade_c/valid_latin 1708/240/12/4; unique raw+want+grader 1451, excess duplicates 513. All nine CP intervals: F1/F2 [.985079,.994547], F3/F5/F6 [.998124,1], F4 [.997858,1], F7 [.998036,1], G1/G2 [.996394,1].
- F1/F2 file+pid composite independently = 187/194, CP95 [.927072,.985372], INDETERMINATE. F1/F2 MULTI = 14/31; all 17 baseline-PASS MULTI records flip. All 31 are r8 B records with three “After operation 8/9/10” blocks; F1 selects the penultimate (operation-9) block. Stripping all fences preserves all 31 verdicts, and restores the correct answer on the 17 baseline-PASS records.
- D1 independently = 909/909 capture, CP95 [.995950,1]; composite 129/129, CP95 [.971809,1]; strata FJ1 639/639, FJM 244/244, MULTI 0/0, DANGLE 17/17, BARE 9/9. All 26 DANGLE/BARE cases lack a prior matched fence.
- Four working population files matched base `f11bffbf` and instrument pins: r8 `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204`; r9 `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`; r11 `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`; r12 `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1`.

## Sources and gate criteria

- Re-opened S048 `https://aclanthology.org/2020.acl-main.442.pdf`, SHA-256 `98d15d259acf15136feed5cd5d4921b60cf313704a629901d115fe910fdb00e1`; page 3 extraction locates the 21-word INV sentence at §2.2 / proceedings p.4904 (absent on p.2). S044 v3 Abstract (`https://arxiv.org/abs/2405.11874v3`) supports the RegEx-extraction claim.
- Re-opened S045 PyPI 0.1.0 README and digest-pinned release sdist (SHA-256 `b633c61734b94b33ad971be4b16951eb13524016b69115eeecc980766d03ad16`); README §The two ways an eval lies and `evalmut/operators.py:255-328` (defects), `:614-726` (equivalents) document the prior art. S046 `https://docs.python.org/3/library/re.html` `\s` documentation includes CR in Unicode whitespace. Source scopes/locations support the draft; no source-quote blocker remains.
- Direct S045 prior art supports novelty held at 7, not +1; the draft confines its contribution to this lane’s pinned measurement.
- Q1–Q6: frontmatter triad, source tiers/anchors, limitations/falsifier, source scopes, and extension of the Judge calibration entry/map row are present. Q8/Q9: round-26 Gate records three rejects with reasons and flip conditions.
- Q7/Q13 landing is not yet verifiable: `corpus/lessons/round-26.md:34` remains deferred and no admitting commit was supplied. `README.md` index/coverage rows are in the current worktree diff; admission must land those with the knowledge file and explicitly cite this returned report plus every other Q10 report. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` → expected exit 1 for absent named report support; `python3 plans/gate_timing_check.py --selftest` → exit 0. Run Q13 against the actual admission commit.
- Q12: D1 is explicitly PC/NOT_SCORED, not a robustness PASS; the draft distinguishes correlated finite-population results from future iid generalization. `python3 plans/state_check.py --summary` → exit 0, `mismatch=0`, `superseded=5`, `offline_unverifiable=3`; no state-check selftest coverage is used for this admission verdict.
- Residual documentation gap: `corpus/README.md:268` still inventories round-26 sources only as S043–S047 although S048 is now used by the draft; include S048 before closure. No `lsp` route is mounted (`read xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available; source claims above were checked by direct reads and replay, not grep as semantic proof. No tools installed (the system Python has no pip; existing `pdftotext` was used).

VERDICT: FAIL — do not admit `corpus/knowledge/grader-perturbation-audit.md` until the Q11 pooled CP95 bounds and exact F1 fence-stripping definition are corrected; then verify Q7/Q13 in the actual same-commit landing.

## Post-correction re-read (2026-10-21)

The pre-correction `VERDICT: FAIL` above is preserved. Re-opened only draft lines 40–43 and 62–73 and compared them with `corpus/evidence/round26-calibration/grader-perturb-build-observation.txt:6-24`.
F1 now explicitly strips only the last matched fence's opening/closing markers while retaining JSON and earlier fences; F2 changes only the `json` label. These definitions match the previously inspected instrument implementation and close the F1 description blocker.
The nine displayed CP95 lower bounds match the summary in order: .985079, .985079, .998124, .997858, .998124, .998124, .998036, .996394, .996394. D1's .995950 is correctly labeled NOT_SCORED. Q11 and the corrected F1 definition now pass the scoped content re-read.
The current Q7 same-commit packaging and Q13 report-timing check remain for L1 at the actual admission commit; this is not a full admission verdict. The prior note about `corpus/README.md:268` omitting S048 remains a supporting-index cleanup.

VERDICT: PASS — scoped Q1–Q12 content/number review after the pre-admission corrections; Q7/Q13 actual-commit gates remain pending and outside this scoped verdict.