# C1 raw-format census

Axis: **novelty** (input-format census for the registered grader perturbation audit; this is not a novelty/prior-art verdict).

## Observed

Scope: every JSONL record with an `ok` key (true and false) across the four frozen C1 files. In total 1,964 records: 1,021 `ok=true`, 943 `ok=false`; every selected record had `raw` as a string. Counts are per file × `cell`. **Confidence: high** for these observed string-level counts.

Definitions: `JSON/bare/none` counts matched fenced blocks, where the first matched block is labelled `json`, has no label, or no block matches, respectively; `other` was zero. A single trailing fence with no matching opener is counted `none` and shown separately as `orphan`. `multi` means >1 matched fenced block. Prose flags count non-whitespace outside parseable JSON after fence-marker lines are removed; bracket means any `()[]{}` in that prose. `trunc` means nonempty raw with no parseable JSON object/array candidate; `empty` means whitespace-only. All counts are records, not numbers of occurrences.

Commands: ran `python3 -c` one-liners from `/tmp` (no files written), concurrently, using these four absolute inputs:
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon/results.jsonl`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round9-replication/results-r9.jsonl`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round11-power/results-r11.jsonl`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round12-ladder/results-r12.jsonl`

Each pass used `json.loads` per nonblank JSONL line and selected `'ok' in record`; the census pass paired fence blocks with `r"```([^\\r\\n`]*)[ \\t]*\\r?\\n(.*?)```"` (`re.S`) and searched raw with `json.JSONDecoder.raw_decode` for JSON spans. The first pass also counted rows by cell, `ok` values, and missing/non-string `raw`.

| file | cell | n (ok T/F) | JSON/bare/none | multi | CRLF | prose pre/post | bracket prose | empty/trunc | orphan |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| r8 | A-CKPT | 30 (13/17) | 24/0/6 | 0 | 0 | 0/0 | 0 | 0/0 | 6 |
| r8 | A-INC | 100 (81/19) | 100/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r8 | A-MONO | 10 (0/10) | 10/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r8 | B-clean-hint | 8 (6/2) | 8/0/0 | 8 | 0 | 8/0 | 0 | 0/0 | 0 |
| r8 | B-clean-plain | 8 (6/2) | 8/0/0 | 7 | 0 | 7/0 | 0 | 0/0 | 0 |
| r8 | B-corrupt-hint | 8 (3/5) | 8/0/0 | 8 | 0 | 8/0 | 0 | 0/0 | 0 |
| r8 | B-corrupt-plain | 8 (3/5) | 8/0/0 | 8 | 0 | 8/0 | 0 | 0/0 | 0 |
| r8 | C-MONO | 4 (4/0) | 4/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r8 | C-benign | 4 (1/3) | 4/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r8 | C-conflict | 4 (4/0) | 4/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r8 | C-norule | 4 (4/0) | 4/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r9 | A-CKPT4710 | 24 (10/14) | 24/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r9 | A-CKPT710 | 16 (5/11) | 14/0/2 | 0 | 0 | 0/0 | 0 | 0/0 | 2 |
| r9 | A-INC | 80 (60/20) | 80/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r9 | A-MONO | 8 (0/8) | 8/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r11 | A-CKPT4710 | 192 (95/97) | 180/0/12 | 0 | 0 | 0/0 | 0 | 0/0 | 12 |
| r11 | A-CKPT710 | 128 (41/87) | 118/0/10 | 0 | 0 | 0/0 | 0 | 0/0 | 8 |
| r12 | A-CKPT10 | 64 (10/54) | 64/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r12 | A-CKPT4710 | 192 (94/98) | 183/0/9 | 0 | 0 | 0/0 | 0 | 0/0 | 9 |
| r12 | A-CKPT710 | 128 (40/88) | 118/0/10 | 0 | 0 | 0/0 | 0 | 0/0 | 8 |
| r12 | A-INC | 640 (522/118) | 631/0/9 | 0 | 0 | 0/0 | 0 | 0/0 | 9 |
| r12 | A-MONO | 64 (2/62) | 64/0/0 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |
| r12 | T-DENSE | 144 (10/134) | 93/0/51 | 0 | 0 | 0/0 | 0 | 0/0 | 3 |
| r12 | T-SPARSE | 96 (7/89) | 60/0/36 | 0 | 0 | 0/0 | 0 | 0/0 | 0 |

Total: 1,819 JSON-fenced, **0 bare-fenced**, 145 no matched fence; 31 records have multiple fenced blocks; 57 have an unmatched fence marker. CRLF=0, prose before/after=31/0, bracket characters in prose=0, empty=0, syntactically truncated=0. All selected records reported `finish=stop` in the per-file summaries.

Example evidence: `round8-horizon/results.jsonl:25` is an unfenced JSON object followed by a lone closing ```; `round8-horizon/results.jsonl:221` has three JSON-fenced progress snapshots preceded by prose. `grader.py:121-134` confirms the response extractor selects the last valid fenced block, then falls back to reversed brace/bracket candidates.

## Inference

The frozen population includes observed prose-prefixed, multi-snapshot responses (31 rows), plus unfenced responses and stray closing delimiters (145 and 57 rows). These formats are directly relevant to the C1 format-robustness census, but the multi-snapshot R8 progress history is not itself proof of the registered D1 previous-truth distractor condition.

## Remaining unknowns

This census does not re-grade records, estimate perturbation intervals, establish semantic completeness beyond parseable JSON / observed `finish=stop`, or search prior art. It therefore supports test-shape selection only and makes no novelty-score claim.

Installs: none.

VERDICT: census complete; no matched bare fences, with 31 multi-block and 57 orphan-marker records identified; no empty or syntactically incomplete JSON raws found.
