# Round 27 — extraction-policy entry placement

Axes: novelty (the registered mapping is novelty → canonical coverage/constructs); calibration.

## Observed placement

- `corpus/README.md:27-62` is the “What’s here” knowledge table. Insert one row for `knowledge/extraction-policy-comparison.md` immediately after the existing grader audit row at `:62`, before the lessons rows. Describe the frozen-response extraction-policy comparison and point to the landed own-work instrument/result plus this round’s policy-source rows; do not make it an unlanded draft citation.
- Add a distinct measured-depth coverage-map bullet immediately after `corpus/README.md:230` (the round-26 “Grader robustness / response-format invariance” row) and before `:231` (benchmark saturation). Label it extraction-policy sensitivity; link the new entry and its instrument; say it extends the grader-robustness ground on the same 1964 responses. Keep the round-26 row intact.
- Append an indented `Partly discharged round 27 (2026-10-21)` sub-bullet under “Judge calibration applied inward” (`corpus/README.md:257`), after the round-26 sub-bullet at `:260`. Suggested scope: the new entry supersedes only the phrase “a separately designed parser-policy comparison remain open” at `:260`, and only for the frozen 1964-response population. Explicitly retain “New formats, future generalization” as open; state that this is not S011 human-label sensitivity/specificity calibration. Do not rewrite the round-26 line.
- To keep discoverability coupled, land the knowledge row, coverage row, and this frontier sub-bullet in the same admitting commit as the entry and the cited second-seat reports (QUALITY Q7/Q13/Q14; `corpus/QUALITY.md:56-60,97-119`). `state_check.py`’s frozen P2e/P3e populations do not automatically verify a new knowledge path; P2e explicitly labels out-of-population additions `OUT_OF_POPULATION` (`plans/state_check.py:1227-1255`).

## Related indexes / boundary

- If landed, add `lessons/round-27.md` after the round-26 lesson row at `corpus/README.md:96`; add round-27 evidence directories/files in an EOF “Round-27 supporting artifacts” block after current line 285, following the round-26 block at `:264-285`. Keep the existing round-26 P4b table content unchanged.
- `corpus/SOURCES.md:65-70` ends at S048 and `:72` begins Paths; round-27 source rows belong after S048 and before Paths (next ID S049). Pre-registration requires rows opened this round for each named harness policy and a row for the measured own-work result (`plans/round-27-claims.md:73-83`). P4e checks S043–S048 `used-by` cells (`:117-123`): if the new entry cites any of those IDs, account for the resulting changed cell and the required full R27-E supersession; do not silently alter their frozen claim. `R27-E` format is strict and unique across SCORECARD/PROVINCE/README (`plans/state_check.py:252-262,554-592`).
- PROVINCE’s Core already distinguishes the existing grader replay gate from the attribution instrument (`PROVINCE.md:102-118`); no new endpoint or model capability is measured. Its Frontier summary at `:121-127` still broadly says judge calibration of grader/attribution outputs is open. If revised, preserve that S009–S012 calibration remains open and limit any parser-policy discharge to this round’s fixed corpus; keep the absent-source and endpoint statements intact.

## Text the entry must not contradict

- `plans/round-27-claims.md:21-57,73-83`: responses/truths/graders stay fixed; only E0–E8 extraction policies vary; policy-source requirements are specific. Do not describe the exercise as response perturbation or actual replay of a named harness unless that replay is observed.
- `corpus/knowledge/grader-perturbation-audit.md:10-22,89-109`: verdict invariance is conditional on extraction policy; published testing/tooling prior art exists; novelty remains held at 7; E0’s historical choice is not proven wrong; no grader repair, future-response guarantee, new-format coverage, or natural format frequency follows.
- `corpus/knowledge/llm-judge-calibration.md:9-14,40-50,68-73`: S011 correction requires human labels and sensitivity/specificity. Parser-policy verdict flips are not judge calibration or evidence that a raw judge pass fraction is calibrated.
- `corpus/README.md:260`, `SCORECARD.md:244,754-760,779-781`: round-26 residual generalization/new formats and the novelty-7 hold remain; no method-novelty credit without supporting prior-art evidence. `PROVINCE.md:30-32,136-139` routes prompt/skill-craft implications to kotoba and the research method to chousa; this lane’s audit does not establish model format-compliance or reusable testing methodology.

## Gaps / confidence

- High confidence: the index insertion points and relevant scope limits above are directly present at the cited lines. `grader.py:121-134` confirms E0’s last-fence, then reverse-order bare-candidate extraction; its observed SHA-256 matches PROVINCE’s `90c87c88…ae941f` pin.
- LSP unavailable: `read xd://lsp` returned “No such tool”; findings use source-text anchors, not semantic LSP results. No public sources were opened and no tools were installed in this seat.

VERDICT: Add the entry beside the round-26 grader audit in both README indexes, append a narrowly scoped round-27 Frontier sub-bullet, and preserve the calibration/generalization limits above. Installs: none.