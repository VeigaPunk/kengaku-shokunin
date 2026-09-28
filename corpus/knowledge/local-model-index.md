# Local model index (Bailian)

Source: `~/.bailian/skills/bailian-docs-llm-wiki/models/` — `index.md` header states: 180 model families, 413 backbone models, generated 2026-09-11 (verified `head` 2026-09-28). Sync state: `~/.bailian/wiki-sync-state.json` (`lastChecked` epoch ms + contentHash).

## Files and join

- `index.json` — global stats + capability/vendor distribution + lightweight family list.
- `families.jsonl` — one family per line with `items[]` summaries.
- `models.jsonl` — one backbone model per line: `model`, `name`, `family`, `familyName`, `provider`, `capabilities[]` (TG/Reasoning/VU/...), `features[]` (cache, function-calling, model-experience), `contextWindow`, `maxInputTokens`, `maxOutputTokens`, `inferenceMetadata`, pricing, QPM, `profile`.
- `groups/<slug>.json` — full family detail incl. call code and input schema.

Join: `models.jsonl[].family == families.jsonl[].slug == index.json.families[].slug`.

## `profile` semantics (from index.md)

Fields: `oneLinePositioning`, `scenes`, `notSuitableFor`, `familyTier`
(flagship/balanced/lightweight), `familyComparison`, `callModes`,
`pipelineRole`. Tri-state: missing = unknown, `null` = not applicable
(tier/comparison only), populated = known. `notSuitableFor: []` = no
known limit. `profileCompleteness: "structured-only"` = profile never
read docs; trust mechanical fields only. Hard specs (price, QPM,
contextWindow, openSource) live in top-level row fields, not profile.

## Falsifiable claim

For any model-selection question inside this province, `models.jsonl`
one-line-per-model scans beat wiki prose for spec lookups; wiki prose
beats it for rationale. Verified shape on `kimi-k2-thinking` /
`kimi-k2.5` / `kimi-k2.6` rows (contextWindow 262144, maxOutputTokens
16384 observed).
