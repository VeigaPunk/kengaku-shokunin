# FxC3DiffTruth — C3 schema-delta findings (independent live probes)

Seat: L1Kengaku32.FxC3DiffTruth (leaf, no subagents). Lane root:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (HEAD `6084cd3`; drafts uncommitted on disk).
All fetches: 2026-10-25, `curl -sS --max-time 20`, own User-Agent `kengaku-fxc3difftruth/1.0`.
No tools installed/upgraded (curl already present; no pacman/uv/npx use). Scratch: `/tmp/r32f-FxC3DiffTruth/`.

## Probe receipts (raw bytes saved under /tmp/r32f-FxC3DiffTruth/)

| Fetch | URL | bytes | sha256 |
| --- | --- | --- | --- |
| `hf_limit50.json` | `https://huggingface.co/api/models?limit=50` | 27771 | `57b9982201af535df8df6d41f73bdcd7d6e24d56529cb328dedc0681d469ad8f` |
| `hf_full50.json` | `https://huggingface.co/api/models?limit=50&full=true` | 128927 | `8887b65516a6b85f53f8eaf2790acc70b2abbadcf0de5225425255a25aca84ee` |
| `openrouter_models.json` | `https://openrouter.ai/api/v1/models` | 791126 | `65143f9f3c8ff69d9ab28483b6bc26e2f86cebb266b992f345582accf4cd3d25` |

Digests differ from the build-wave receipts (R32CatProbe: `7e05ad8…`/27771 bytes, `618f16e…`/791130 bytes) while byte size for HF matches exactly — live values drift between runs (e.g. first item `likes` 2886→2888, `trendingScore` 1283→1280), confirming these are independent real fetches, not replays.

## (a) HF default projection (`?limit=50`): key-set check

- Top level: JSON list, `len == 50`, all 50 are dicts.
- Union of keys across all 50 items = exactly `{_id, createdAt, downloads, id, library_name, likes, modelId, pipeline_tag, private, tags, trendingScore}` (11 keys) — no unexpected key anywhere in the sample.
- First item key set = exactly those 11 keys; verbatim first item:
  `{"_id":"6ad2e0265a59c8bc18707765","id":"deepseek-ai/DeepSeek-V4.1-Flash-1017","likes":2888,"trendingScore":1280,"private":false,"downloads":85275,"tags":["transformers","safetensors","deepseek_v41","text-generation","image-text-to-text","license:mit","eval-results","endpoints_compatible","8-bit","fp8","region:us"],"pipeline_tag":"image-text-to-text","library_name":"transformers","createdAt":"2026-10-17T02:40:38.000Z","modelId":"deepseek-ai/DeepSeek-V4.1-Flash-1017"}`
- `author`/`sha`/`lastModified`/`gated`: present in **0/50** items.
- `_id`/`createdAt`/`modelId`/`private`: present in 50/50.
- Note: `pipeline_tag` in 45/50 and `library_name` in 44/50 (absent on some items), `id`/`downloads`/`likes`/`trendingScore`/`tags` in 50/50.

## (b) `?full=true` restores the four fields

- `?limit=50&full=true` → list, `len == 50`. `author`, `sha`, `lastModified`, `gated` present in **50/50**; plus `siblings` (50/50). First-item keys (16): the 11 above + `author`,`sha`,`lastModified`,`gated`,`siblings`.
- Deltas are projection-dependent (default projection shrank), not removals — exactly as the draft records.

## (c) OpenRouter (`api/v1/models`): count and first-item fields

- Top-level object keys: `{data, links, total_count}`; `data` len == **467**, `total_count` == 467, `links.next` == null (single page).
- First item (verbatim, full): `{"id":"moonshotai/kimi-k3.1-pro","canonical_slug":"moonshotai/kimi-k3.1-pro-20261023","hugging_face_id":null,"name":"MoonshotAI: Kimi K3.1 Pro","created":1792778188,"description":"Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window. It is built for long-horizon coding, 3D...","context_length":1048576,"architecture":{"modality":"text+image+video->text","input_modalities":["text","image","video"],"output_modalities":["text"],"tokenizer":"Other","instruct_type":null},"pricing":{"prompt":"0.000002","completion":"0.00001","input_cache_read":"0.0000002"},"top_provider":{"context_length":1048576,"max_completion_tokens":943718,"is_moderated":false},"per_request_limits":null,"supported_parameters":["frequency_penalty","include_reasoning","max_tokens","presence_penalty","reasoning","reasoning_effort","response_format","stop","structured_outputs","tool_choice","tools"],"default_parameters":{"top_p":0.95},"supported_voices":null,"knowledge_cutoff":null,"expiration_date":null,"links":{"details":"/api/v1/models/moonshotai/kimi-k3.1-pro-20261023/endpoints"},"benchmarks":{"design_arena":[...],"artificial_analysis":{"intelligence_index":55.1,"coding_index":null,"agentic_index":null}},"reasoning":{"mandatory":false,"default_enabled":true,"supported_efforts":["max","high","low","none"],"default_effort":"max"}}` (benchmarks.design_arena array truncated here; full bytes in receipt).
- Twelve recorded fields present in first item: `id`, `canonical_slug`, `context_length`, `knowledge_cutoff`, `created`, `pricing`, `architecture`, `supported_parameters`, `top_provider`, `per_request_limits`, `hugging_face_id`, `reasoning` — all **True**.
- Across all 467: the twelve are present in 467/467 except `reasoning` in 338/467 (some served models carry no reasoning object; first item has it).
- Baseline before-state (`git show f20a1097:corpus/knowledge/open-model-catalogs.md`) records “460 models observed” and no `verified-at: 2026-10-25`/`S101`/`S102` (grep count 0). → drift **+7** (460→467) confirmed.

## (d) Counts/deltas vs drafted rows S101/S102 (corpus/SOURCES.md lines 116–117, uncommitted)

| Claim in drafted row | My independent probe | Match |
| --- | --- | --- |
| S101: `hf_models=50` | 50 items | ✓ |
| S101: `hf_schema_delta=4` | missing = author, sha, lastModified, gated (4) | ✓ |
| S101: four fields “present only with ?full=true” | 50/50 with full=true; 0/50 default | ✓ |
| S102: `or_models=467` | data len 467, total_count 467 | ✓ |
| S102: `or_schema_delta=0` | none of 12 missing in first item | ✓ |
| S102: 467 vs 09-28 entry’s 460 | baseline git shows 460 | ✓ |

- Counter run on the draft state (`python3 plans/catalog_probe.py --diff --lane .`, lane root) reproduced verbatim the receipt lines the rows cite:
  `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=ok` / `HF missing fields: author, sha, lastModified, gated`.

## Additional defects found (claim mechanics; do not change the delta verdict)

- **F1 — C3 counting command can never exit 0, so the frozen predicate’s “and exits 0” is unsatisfiable.** `main()` returns 0 only when BOTH missing-field lists are empty (`plans/catalog_probe.py:120`). This round’s recorded HF delta *is* the four missing fields, so a correct live run always has `hf_missing = [author, sha, lastModified, gated]` → exit 1, even with a fully refreshed entry (`entry=ok`). Empirically the draft-state run above exited 1. The planned (uncommitted) counter change only adds two selftest guard cases (git diff `plans/catalog_probe.py`) — exit logic unchanged. The freeze control `catalogs-before.txt` also exits 1, so before/after are indistinguishable by exit code (only `entry=stale` vs `entry=ok` textually). Fix would need the counter to accept *recorded*/expected deltas as success (or an explicit expected-delta argument), else the claim cannot pass its own counting command.
- **F2 — cited receipt file does not exist.** Rows S101/S102 and the draft entry cite `corpus/evidence/round32/catalogs/after.txt`; `corpus/evidence/round32/` is absent from the working tree (and the baseline). `entry_ok` only checks that the string `corpus/evidence/round32/catalogs/` appears; no receipt file anchors the row-cited lines (R32CritC3 escape (c)). My independent probe reproduces the quoted numbers, but the drafts’ own evidence chain is ungrounded until `after.txt` (or equivalent) actually lands.

## Residual risk / verification gaps

- HF/OpenRouter are live endpoints; counts, deltas and first-item identity can shift between runs (digests already differ from the build-wave receipts). The schema-level findings (a)–(d) held on both independent runs today.
- “All twelve recorded fields” is verified on the first item (as the counter defines the schema) and on 467/467 for eleven of twelve; `reasoning` is not universal (338/467) — noted, not contradicting the drafted row.
- `corpus/evidence/round32/catalogs/after.txt` receipt: not verifiable (absent); pending lane write.

VERDICT: deltas-confirmed
