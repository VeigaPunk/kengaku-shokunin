# R32 Catalog Probe (C3) — live HF + OpenRouter model catalog probe

- Access date: 2026-10-25 (all fetches this date).
- Method: `curl -sS --max-time 20` on both endpoints; raw JSON saved under
  `/tmp/r32-R32CatProbe/` (cleaned after handoff; no production files touched).
- Prior baseline entry: `corpus/knowledge/open-model-catalogs.md` (probed 2026-09-28).
- No tools installed/upgraded this round (curl was sufficient; no pacman/uv/npx use).

## Raw receipts (digests + byte counts)

| File | sha256 | bytes |
| --- | --- | --- |
| `hf_models_limit50.json` (`GET https://huggingface.co/api/models?limit=50`) | `7e05ad8fd31f327efcef8400079b5c0f25f24e80c7aad5877841653c282fe681` | 27771 |
| `openrouter_models.json` (`GET https://openrouter.ai/api/v1/models`) | `618f16e462e0eb5ff593edcc3699408116aee482b4ec4f118f783ceb31ad3fcc` | 791130 |
| `hf_models_full3.json` (verification: `?limit=3&full=true`) | `fecafca4f19bdb3f16cb36a316ba6c30a7e297928e58d324b45b677b7a6ae944` | 9238 |

## (a) Model counts

- Hugging Face: `?limit=50` returned **50** items (JSON top-level list; len == 50).
- OpenRouter: response is an object `{data, total_count, links}`; `data` len == **467**,
  `total_count` == **467**, `links.next` == null (single page, no pagination needed).
  Prior entry (2026-09-28) recorded 460 → **drift +7**.

## (b) HF field presence (2026-09-28 entry fields) in first item

Default `?limit=50` response (no `full=true`), first item keys:
`_id, createdAt, downloads, id, library_name, likes, modelId, pipeline_tag, private, tags, trendingScore`.

| Field | Present in first item? |
| --- | --- |
| `id` | yes |
| `author` | **no** (absent in 0/50 items) |
| `sha` | **no** (absent in 0/50 items) |
| `lastModified` | **no** (absent in 0/50 items) |
| `downloads` | yes |
| `likes` | yes |
| `trendingScore` | yes |
| `pipeline_tag` | yes |
| `library_name` | yes |
| `tags` | yes |
| `gated` | **no** (absent in 0/50 items) |

Verification: with `full=true` (`?limit=3&full=true`), **all 11 fields are present**, plus
`siblings[]`. So the deltas are projection-dependent (default projection shrank), not removals.
New fields observed in default projection (not in the 2026-09-28 entry): `_id`, `createdAt`,
`modelId`, `private`.

## (c) OpenRouter field presence (2026-09-28 entry fields) in first item

First item keys (21): `architecture, benchmarks, canonical_slug, context_length, created,
default_parameters, description, expiration_date, hugging_face_id, id, knowledge_cutoff,
links, name, per_request_limits, pricing, reasoning, supported_parameters, supported_voices,
top_provider`.

| Field | Present in first item? |
| --- | --- |
| `id` | yes |
| `canonical_slug` | yes |
| `context_length` | yes |
| `knowledge_cutoff` | yes |
| `created` | yes |
| `pricing` | yes |
| `architecture` | yes |
| `supported_parameters` | yes |
| `top_provider` | yes |
| `per_request_limits` | yes |
| `hugging_face_id` | yes (null for this item) |
| `reasoning` | yes |

All 12 checked fields present — **no missing fields vs the 2026-09-28 entry**.

## (d) Sample JSON items (first model per source, verbatim)

### Hugging Face — first item of `?limit=50` (default projection)

```json
{
  "_id": "6ad2e0265a59c8bc18707765",
  "id": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
  "likes": 2886,
  "trendingScore": 1283,
  "private": false,
  "downloads": 85275,
  "tags": [
    "transformers",
    "safetensors",
    "deepseek_v41",
    "text-generation",
    "image-text-to-text",
    "license:mit",
    "eval-results",
    "endpoints_compatible",
    "8-bit",
    "fp8",
    "region:us"
  ],
  "pipeline_tag": "image-text-to-text",
  "library_name": "transformers",
  "createdAt": "2026-10-17T02:40:38.000Z",
  "modelId": "deepseek-ai/DeepSeek-V4.1-Flash-1017"
}
```

### OpenRouter — first item of `data`

```json
{
  "id": "moonshotai/kimi-k3.1-pro",
  "canonical_slug": "moonshotai/kimi-k3.1-pro-20261023",
  "hugging_face_id": null,
  "name": "MoonshotAI: Kimi K3.1 Pro",
  "created": 1792778188,
  "description": "Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window. It is built for long-horizon coding, 3D...",
  "context_length": 1048576,
  "architecture": {
    "modality": "text+image+video->text",
    "input_modalities": ["text", "image", "video"],
    "output_modalities": ["text"],
    "tokenizer": "Other",
    "instruct_type": null
  },
  "pricing": {
    "prompt": "0.000002",
    "completion": "0.00001",
    "input_cache_read": "0.0000002"
  },
  "top_provider": {
    "context_length": 1048576,
    "max_completion_tokens": 943718,
    "is_moderated": false
  },
  "per_request_limits": null,
  "supported_parameters": [
    "frequency_penalty", "include_reasoning", "max_tokens",
    "presence_penalty", "reasoning", "reasoning_effort",
    "response_format", "stop", "structured_outputs",
    "tool_choice", "tools"
  ],
  "default_parameters": { "top_p": 0.95 },
  "supported_voices": null,
  "knowledge_cutoff": null,
  "expiration_date": null,
  "links": {
    "details": "/api/v1/models/moonshotai/kimi-k3.1-pro-20261023/endpoints"
  },
  "benchmarks": { "design_arena": [...], "artificial_analysis": { "intelligence_index": 55.1, "coding_index": null, "agentic_index": null } },
  "reasoning": {
    "mandatory": false,
    "default_enabled": true,
    "supported_efforts": ["max", "high", "low", "none"],
    "default_effort": "max"
  }
}
```

(OpenRouter `benchmarks.design_arena` array truncated in the paste for brevity — full bytes
are in the receipt `openrouter_models.json`; the first item's design_arena entries are 4
objects with `arena/category/elo/win_rate/rank`.)

## (e) Surprises / schema changes

1. **HF default projection shrank.** `author`, `sha`, `lastModified`, `gated` are absent from
   the default `?limit=50` response (0/50 items). They reappear with `full=true` (verified on
   `?limit=3&full=true`: all 11 fields + `siblings[]`). The 2026-09-28 entry listed them as
   observed per-model fields — that observation must now be qualified as "with `full=true`".
2. **HF new fields** in the default projection: `_id`, `createdAt`, `modelId`, `private`
   (not in the 2026-09-28 entry).
3. **OpenRouter count drift**: 460 → 467 (**+7**).
4. **OpenRouter additive schema growth** (no removals): items now carry `benchmarks`
   (design_arena / artificial_analysis), `default_parameters`, `description`, `expiration_date`,
   `links`, `name`, `supported_voices`. `pricing` gained `input_cache_read` (was
   `prompt`/`completion`). `architecture` gained `input_modalities`/`output_modalities`
   (prior entry listed `modality`/`tokenizer`/`instruct_type` — all still present). `reasoning`
   is now an object (`mandatory`/`default_enabled`/`supported_efforts`/`default_effort`)
   rather than a bare flag. Top level gained `total_count` and `links`.

## Impact for C3 catalog refresh

- The refresh of `corpus/knowledge/open-model-catalogs.md` should (i) update the HF field list
  to note the `full=true` requirement for `author`/`sha`/`lastModified`/`gated`/`siblings[]` and
  the new `_id`/`createdAt`/`modelId`/`private` fields; (ii) update OpenRouter count 460 → 467
  and append the new item fields (`benchmarks`, `default_parameters`, `supported_voices`,
  `expiration_date`, `links`, `name`, `pricing.input_cache_read`,
  `architecture.input_modalities`/`output_modalities`, object-form `reasoning`).

VERDICT: probe-complete
