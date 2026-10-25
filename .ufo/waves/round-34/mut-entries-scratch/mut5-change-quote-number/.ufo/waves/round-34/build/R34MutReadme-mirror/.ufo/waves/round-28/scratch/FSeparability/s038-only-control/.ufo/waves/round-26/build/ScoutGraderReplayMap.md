# Grader replay map

Axis: novelty (C1's construct is verdict robustness under response-format perturbation).
Method: searched `grader.py` for every `extract_json_block(` call; read only those call paths and the requested S7 fixture range. `read xd://lsp` returned “No such tool” and listed mounted devices without LSP, so semantic navigation was unavailable; findings below use literal source/search evidence, not semantic proof.

## Stored-response replays

Data bindings: `grader.py:66-75` maps `r8_jsonl`, `r9_jsonl`, `r11_jsonl`, `r12_jsonl` to the four requested evidence files; main dispatch loads and grades them at `:5711-5718`.

- **r8 — `corpus/evidence/round8-horizon/results.jsonl`:** `replay_a_records` (`:367-398`; called by `grade_r8` `:413-416`) selects every `A-*` cell except `*-ack` with `ok`; `:386-387` extracts `raw` then applies `grade_state`. Covers `A-INC`, `A-CKPT`, `A-MONO`. Additional B replay (`:417-480`): `B-clean-hint`, `B-clean-plain`, `B-corrupt-hint`, `B-corrupt-plain`; `:436` extracts, `:468-476` re-derives `ok` by `got == want` plus outcome/healed (strict equality, not a call to `grade_state`). Summary repeats extraction for A-MONO (`:517-519`), B (`:520-527`), and C (`:528-535`).
- **r8 C cells:** `C-conflict`, `C-benign`, `C-norule` use `grade_c` at `:482-497` (`:492` grader, `:496` stored-got check). `C-MONO` instead uses `valid_latin` at `:498-504` (`:500-502`), repeated in summary at `:533-535`.
- **r9 — `corpus/evidence/round9-replication/results-r9.jsonl`:** same `replay_a_records`/`grade_state` path (`:367-398`, call `:584-586`), covering `A-INC`, `A-CKPT4710`, `A-CKPT710`, `A-MONO`. Final-turn stats explicitly regrade at `:593-605`; `recompute_final_ok` (`:564-566`) is reused for sign/onset/failure analyses (`:634-636`, `:676-685`, `:701-730`). `:701,704,724,726` also reparse final responses for parse/state-error counts.
- **r11 — `corpus/evidence/round11-power/results-r11.jsonl`:** `_replay_graded` (`:1006-1038`; called `:1421-1426`) selects `A-CKPT4710` and `A-CKPT710`; `:1026-1031` extracts and applies `grade_state`. Analysis regrades final/all-turn statistics at `:1173-1186`, shared-turn nwrong at `:1230-1237`, and final verdict via `recompute_final_ok` at `:1285-1288`; `:1301-1309` only classifies parser failures (`:1303`), not verdicts.
- **r12 — `corpus/evidence/round12-ladder/results-r12.jsonl`:** `_check_replay` (`:2463-2510`; called by `grade_r12` `:4062-4065`) selects `GRADED_CELLS` with stored `ok` (`:2465-2474`); `:2488-2500` uses `grade_state` for family-1 dicts and `grade_seq` for family-2 lists. Cells are fixed at `:1560-1569`: `A-INC`, `A-CKPT4710`, `A-CKPT710`, `A-CKPT10`, `A-MONO`, `T-DENSE`, `T-SPARSE`. Secondary verdict replays: final-turn run.log totals (`:2728-2745`); all-turn analysis maps (`:2976-2992`, consumed by `_recompute_r12` `:3081-3092`). `:3241-3244` only rechecks parse-failure counts.
- **Other extractor occurrence:** `:4615-4618` builds a run.log summary from the generated S7 fixture records; synthetic only, not a replay of the committed r12 population.

## Selftest synthetic fallback fixtures (`grader.py:4345-4500`)

`_fence` wraps JSON in a ```json fence (`:4347-4348`). `_perturb_dict` changes the first sorted `k` values by `+100+j` (`:4351-4355`); `_perturb_list` appends `*` to its first `k` elements (`:4358-4362`). In `_build_r12_fixture`'s `graded` generator (`:4468-4488`), the usual raw is fenced (`:4483`); three parser-edge fixtures are explicit: unparseable `"no json here at all"` for final `T-SPARSE` (`:4470-4475`), unfenced bare JSON object for family-1 `A-INC`, first fixture pid, turn 1 (`:4478-4479`), and bare JSON array for family-2 `T-DENSE`, first fixture pid, turn 4 (`:4480-4482`). These are fabricated S7 fixtures, not stored model responses.

## Coverage boundary

`jq -s 'group_by(.cell)|map({cell:.[0].cell,raw_ok:(map(select(has("raw") and has("ok")))|length)})' <file>` observed 188 r8, 128 r9, 320 r11, and 1,328 r12 raw+ok rows. Every such cell has a source-level verdict replay path above; there is no P1 raw+ok cell with no existing `grader.py` regrade. Ack, filler, meta, descriptor, and error records without stored `ok` are outside that P1 candidate population.

**Instrument-contract gap:** the shared `Rec.grader` enum is only `{state,seq,c}`. Four r8 `C-MONO` raw+ok records have an existing source replay, but that replay is `valid_latin` (`:500-504`), not any permitted enum grader. Thus these four records have no representable baseline regrade in the specified instrument interface unless explicitly excluded or the contract is extended. B cells are source-replayed by exact equality (`:468-476`); that boolean is equivalent to `grade_state`'s exact-equality verdict for dict state, but this equivalence is inference from `grade_state` `:221-225`, not an explicit call there.

Baseline-match/exclusion outcomes were not executed; the counts above are raw+ok census only. No tools installed or updated.

VERDICT: Source replays cover every raw+ok candidate cell; the C1 `Rec.grader` interface omits the source-replayed `C-MONO` (`valid_latin`) grader, leaving its four r8 records unrepresentable in the instrument.
