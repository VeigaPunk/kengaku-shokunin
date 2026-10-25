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

## Re-probe 2026-10-25 (round 33)

verified-at: 2026-10-25
receipts: corpus/evidence/round33/catalogs/ (raw bytes + sha256 digests committed)
raw: hf.raw.json sha256 3662d3379a412aa4d2362c8f02c9b081bf80e478dd76629c36cd002470241344;
     or.raw.json sha256 69dce7810d1b5e312ba6dec01fa1710647031b28546b724a6e9a779501d96350 — a bounded
     envelope (OpenRouter's response exceeds the 64 KiB cap, so the retained artifact is
     `{"data":[first model verbatim],"meta":{"truncated":true,"observed_models":467,
     "bytes_total":…,"sha256_full":…}}`); `or_models=467` below is the live probe's own
     observed count recorded in that envelope, not a re-parse of truncated bytes
observed (re-derived by `python3 plans/catalog_probe.py --verify --lane .`):
hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0
HF missing fields: author, sha, lastModified, gated — unchanged from the round-32 probe (the
default projection still omits them; `?full=true` restores them). The round-32 zero-delta
predicate stays failed as declared; this block records the byte-retained re-probe.
