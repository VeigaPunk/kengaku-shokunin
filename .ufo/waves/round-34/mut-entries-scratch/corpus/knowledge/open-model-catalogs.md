source: S101 — https://huggingface.co/api/models — list endpoint first probed 2026-10-25; bounded raw re-probe in `corpus/evidence/round33/catalogs/`
source: S102 — https://openrouter.ai/api/v1/models — model-list endpoint first probed 2026-10-25; bounded raw re-probe in `corpus/evidence/round33/catalogs/`
verified-at: 2026-10-25
recheck: 180d — run `python3 plans/catalog_probe.py --capture --lane .` followed by `--verify`; re-locate the fields in the committed raw responses under `corpus/evidence/round33/catalogs/` before citing (next due 2027-04-23)
writer: KengakuR32 (base); re-probe receipts and freshness block updated by KengakuR33 (round 33)

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
- **Refresh 2026-10-25 (first returned record):** the default list's first
  model object lacks `author`, `sha`, `lastModified` and `gated`; `?full=true`
  restored those fields in the probe. `catalog_probe.py` measures the schema
  delta from `data[0]` only, so this does not establish that those fields are
  absent from every one of the 50 returned records. Other field-presence
  variation among records is not counted by this probe.
- Use for: open-weight existence/versioning (sha), license via `tags`,
  GGUF availability (`filter=gguf`, `siblings` filenames carry quant e.g.
  `IQ2_XXS`), popularity triage (`downloads`/`trendingScore`).
- Model card detail: `GET /api/models/{id}?full=true`; raw card at
  `/{id}/raw/main/README.md`.

## OpenRouter — `GET https://openrouter.ai/api/v1/models`

- 460 models observed (09-28); the OpenRouter API reported `total_count=467`
  on 2026-10-25. That request used `?limit=10`, returning ten sample records
  plus the total-count field. `catalog_probe.py` reports `total_count` as
  `or_models` and checks the twelve listed fields only on the first returned
  object; it does not enumerate the complete catalog in its bounded receipt.
- Per-model fields inspected: `id` (`vendor/model`), `canonical_slug`,
  `context_length`, `knowledge_cutoff`, `created`, `pricing`
  (`prompt`/`completion` per-token USD), `architecture`, `supported_parameters[]`,
  `top_provider`, `per_request_limits`, `hugging_face_id`, `reasoning`.
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
raw: hf.raw.json sha256 96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121 (27,698 B);
     or.raw.json sha256 9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5 (16,010 B).
     OpenRouter response was fetched with `?limit=10`; the complete response carries 10 model
     objects plus `total_count=467`, so `or_models=467` re-derives from that retained response.
     Both complete response bodies are under the 64 KiB cap.
observed (re-derived by `python3 plans/catalog_probe.py --verify --lane .`):
hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0
HF delta is measured from the first returned record (`author`, `sha`, `lastModified`, `gated`),
not a per-field union across all 50 models. The OpenRouter response has ten returned models and
`total_count=467`, so `or_models` is the API-reported total from the committed JSON field. The
round-32 zero-delta predicate stays failed as declared; this block records the byte-retained re-probe.
