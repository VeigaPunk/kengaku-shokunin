source: S101 — https://huggingface.co/api/models — the lane's own probe of the list endpoint, 2026-10-25 (receipt: corpus/evidence/round32/catalogs/after.txt)
source: S102 — https://openrouter.ai/api/v1/models — the lane's own probe of the model list, 2026-10-25 (receipt: corpus/evidence/round32/catalogs/after.txt)
verified-at: 2026-10-25
recheck: 180d — re-run `python3 plans/catalog_probe.py --diff` and re-locate the receipts at corpus/evidence/round32/catalogs/ before citing this entry (next due 2027-04-23)
writer: KengakuR32 (refresh of the 2026-09-28 probe)

# Open model catalogs (non-Bailian)

Bailian index (`local-model-index.md`) covers one provider family. For
cross-provider comparison and open-weight hunting, two public JSON APIs
verified reachable and schema-probed 2026-09-28 (no auth needed for reads);
re-probed 2026-10-25 — build (A) below, with the receipts under
`corpus/evidence/round32/catalogs/` and the probe tool `plans/catalog_probe.py`.

## Hugging Face — `GET https://huggingface.co/api/models`

- Params: `?search=<q>&limit=<n>&full=<bool>&sort=downloads|likes|trendingScore`,
  `?author=`, `?pipeline_tag=`, `?filter=gguf` (GGUF weights subset).
- Per-model fields observed (2026-09-28): `id`, `author`, `sha`, `lastModified`,
  `downloads`, `likes`, `trendingScore`, `pipeline_tag`, `library_name`,
  `tags[]`, `gated`, `siblings[]` (file list when `full=true`).
- **Refresh 2026-10-25:** the default list projection no longer returns
  `author`, `sha`, `lastModified` or `gated` — they are present with
  `?full=true`, which the 09-28 description did not require for them. The
  default projection observed on 2026-10-25 carries `id`, `downloads`,
  `likes`, `trendingScore`, `pipeline_tag`, `library_name`, `tags`, `_id`,
  `createdAt`, `modelId`, `private`. Recipe change: for those four fields, ask
  for `?full=true`.
- Use for: open-weight existence/versioning (sha), license via `tags`,
  GGUF availability (`filter=gguf`, `siblings` filenames carry quant e.g.
  `IQ2_XXS`), popularity triage (`downloads`/`trendingScore`).
- Model card detail: `GET /api/models/{id}?full=true`; raw card at
  `/{id}/raw/main/README.md`.

## OpenRouter — `GET https://openrouter.ai/api/v1/models`

- 460 models observed (09-28); **467 on 2026-10-25**. Per-model: `id`
  (`vendor/model`), `canonical_slug`, `context_length`, `knowledge_cutoff`,
  `created`, `pricing` (`prompt`/`completion` per-token USD), `architecture`
  (`modality`, `tokenizer`, `instruct_type`), `supported_parameters[]`,
  `top_provider` (context/uptime knobs), `per_request_limits`,
  `hugging_face_id` (when open-weight twin exists), `reasoning` flag. All
  twelve fields still present on 2026-10-25.
- Use for: cross-vendor price/context comparisons, knowledge-cutoff
  checks, per-request limit discovery, finding the HF twin of a served
  model via `hugging_face_id`.

## Local inventory (this host)

- llama-server model file path is the catalog: `/scratch/models/` GGUFs
  (observed `qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`
  served on `127.0.0.1:34113` via `qwen-coder.service`).
- `GET <server>/v1/models` returns the served id — always prefer this
  over provider config (`qwen-local` entry pointed at dead `8080` while
  server ran `34113`; verify endpoint before trusting config).

## Rules

- HF `downloads`/`likes` are cumulative, not velocity — use
  `trendingScore` for recency signals.
- OpenRouter `pricing` values are strings in USD per token; multiply by
  1e6 for the quoted per-million-token rate.
- `hugging_face_id` presence on OpenRouter ≈ open-weight twin exists —
  cheapest path to a local reproduction of an API result.
