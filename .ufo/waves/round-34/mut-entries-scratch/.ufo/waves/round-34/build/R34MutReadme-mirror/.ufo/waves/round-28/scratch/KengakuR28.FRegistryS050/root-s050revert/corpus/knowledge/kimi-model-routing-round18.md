# Kimi secondary-model routing — round 18 (2026-10-15)

Digest of the parent-fleet round 18 (`../`, i.e. `/home/vgpnk/Projects/shokunin`,
branch `master`): a live census of `~/.kimi-code/config.toml`, a definitions
audit, an n=2 TTFT/TPS battery over the live 17-entry `[secondary_model.models]`
pool, a codex fast-mode probe, an opencode-go/deepseek-v4.1-flash probe, and
the resulting 13-entry routing table. Six missions merged (verified 2026-10-15
with `git -C /home/vgpnk/Projects/shokunin log --oneline`):

| mission | artifact tree (parent repo) | merge |
|---|---|---|
| M1 census | `research/round-18-kimi-model-routing/census/` | `4738fee` |
| M2 definitions audit | `research/round-18-kimi-model-routing/definitions/` | `7e2c473` |
| M3 capability battery | `research/round-18-kimi-model-routing/battery/` | `c2174a5` |
| M5 codex fast-mode probe | `research/round-18-kimi-model-routing/fastmode/` | `db82042` |
| M6 opencode-go probe | `research/round-18-kimi-model-routing/battery-opencode/` | `bd0c690` |
| M4 routing table + report | `research/round-18-kimi-model-routing/routing/` | `fbae972` |

Fleet report: `../.ufo/reports/round-18/kengaku.md` — byte-identical to
`routing/kengaku-round18-report.md` (`diff -q` exit 0; report committed at
`389ede4`). Local evidence index: `corpus/evidence/round18-kimi-routing/README.md`.
This entry is a digest: every number below cites the parent trees; the bytes
stay there.

**Config pins.** M1's re-baselined census and the M2/M3/M5/M6 measurements all
refer to json-canonical digest `61f22a2bbe52d616` (file sha256 `e3c223e0…`):
13 providers, 143 `[models.*]` entries, 17 pool entries, 6 shim units. At M4
the live file had drifted to `c5f12997…` / canonical `2c61f6bb`; the drift is
confined to 10 `capabilities` fields (`9×devin/*` and `cascade/glm-5.3-flash`
gained `tool_use`), and the 17 pool ids are identical, so M3's per-entry
numbers apply to live entries (`routing/kimi-secondary-models-round18.toml`
header; `definitions/ANALYSIS.md` "Drift notice"). The config is live and
drifted repeatedly that day (32 backups under `~/.kimi-code/`, 21 dated
2026-10-15 — `routing/APPLY.md`). **No mission modified the live config**; the
routing table is a recommendation with an operator runbook (splice region:
live lines 1483–1504).

## What was measured and why

- **New models/providers test** — census scope: every provider and `[models.*]`
  entry probed live; the config had been rewritten mid-flight
  (`2026-10-15T08:26:02-03:00`) and the census was re-baselined against the new
  revision (`census/ANALYSIS.md` §1 provenance).
- **TTFT/TPS headline** — M3's binding method: TTFT = request send → first
  decoded content token on a streaming request; TPS = `(completion_tokens − 1)
  / (last-delta time − first-delta time)` with the server `usage` block as the
  numerator; a decode span under 50 ms is reported as a burst, not as
  throughput (`battery/ANALYSIS.md` §1).
- **The assigned pool** — M3 measured exactly the 17 ids in the live
  `[secondary_model.models]` table: 188 of 188 requests, window
  2026-10-15T11:59:13Z → 12:02:41Z, 0 re-grade mismatches over 158 records
  (`battery/ANALYSIS.md` header).
- **Codex fast mode** — user ask quoted verbatim: *"can we try enabling
  priority servicing tier (fast mode) on codex models"* (`fastmode/ANALYSIS.md`
  §1).
- **opencode-go gap** — the lane was absent from the pool table, "which is why
  the M3 battery never reached it" (`battery-opencode/ANALYSIS.md` header); M6
  measured it directly.
- **Lane-policy revision** (operator directive 2026-10-15, recorded verbatim):
  *"the opencode-go should be used for deepseek v4.1 flash only, i have a zai
  subscription and devin is the secondary provider for the glm 5.3 flash"*
  (`routing/kengaku-round18-report.md` §10). Applied in M4.

## Headline numbers

M3, n=2 reps per model, fixed short prompt, perf `max_tokens` 256
(`battery/ANALYSIS.md` §2); the M6 row was measured with byte-identical probe
machinery (`battery-opencode/ANALYSIS.md` §1–2):

| model | bucket | status | TTFT med ms | TPS med | pass |
|---|---|---|---|---|---|
| `hyper/deepseek-v4.1-flash` | FAST | 200 | 2081 | 375.91 | 8/9 |
| `alibaba-token-plan/deepseek-v4.1-flash` | FAST | 200 | 2251 † | 226.72 | 8/9 |
| `zai-coding-plan/glm-5.3-flash-low` | FAST | 200 | 2796 † | 138.21 | 7/9 |
| `cascade/deepseek-v4.1-flash` | FAST | 200 | 3179 | burst | 8/9 |
| `cascade/glm-5.3-flash` | FAST | 200 | 4952 | burst | 8/9 |
| `alibaba-token-plan-2/deepseek-v4.1-flash` | FAST | 429 | — | — | 0/9 |
| `alibaba-token-plan-3/deepseek-v4.1-flash` | FAST | 429 | — | — | 0/9 |
| `cursor/composer-2.5` | VERY-FAST | 200 | 7198 | burst | 7/9 |
| `cursor/cursor-grok-4.5-low-fast` | VERY-FAST | 200 | 8275 | burst | 8/9 |
| `zai-coding-plan/glm-5-turbo` | MIDDLE | 200 | 2957 | 157.07 | 8/9 |
| `xai-oauth/grok-4.5` | MIDDLE | 200 | 3476 | 66.71 | 9/9 |
| `hyper/qwen3.8-flash` | MIDDLE | 200 | 4868 | 178.96 | 9/9 |
| `alibaba-token-plan/qwen3.8-flash` | MIDDLE | 200 | 13282 | 235.56 | 9/9 |
| `alibaba-token-plan-2/qwen3.8-flash` | MIDDLE | 429 | — | — | 0/9 |
| `alibaba-token-plan-3/qwen3.8-flash` | MIDDLE | 429 | — | — | 0/9 |
| `openai-codex/gpt-6.1-sol` | STRONG | 200 | 2212 | 64.46 | 9/9 |
| `openai-codex/gpt-6.1-sol-high` | STRONG | 200 | 2878 | 70.82 | 9/9 |
| `opencode-go/deepseek-v4.1-flash` (M6; not in pool) | — | 200 | 4157 ‡ | 327.29 | 8/9 |

† no content token inside the budget: the lane spent the whole `max_tokens`
budget on reasoning and never emitted content; the cell is first-decoded-token
time (M3 §2). ‡ mixed basis: rep 1 first-decoded (3356 ms), rep 2 content
(4958 ms); content-only figure 4958 ms (M6 §2). "burst" = whole answer flushed
in one burst (decode span < 50 ms); no client-side TPS derivable, excluded from
TPS rankings.

**Measured bucket order** (TTFT medians, `battery/ANALYSIS.md` §4): STRONG
2545 ms < FAST 2796 ms < MIDDLE 4172 ms < VERY-FAST 7736 ms. FAST vs MIDDLE
holds; MIDDLE vs STRONG, FAST vs STRONG and VERY-FAST vs MIDDLE are inverted —
"bucket labels in this config describe intended role, not measured latency."
Prediction scoring (filed ex-ante): ordering 7 hit / 7 miss, global 5 hit /
1 miss; TTFT point-error median 1048 ms over 13 models (M3 §7). 10 probes
failed on their merits; 40 more were never attempted after a lane-level abort
(the four key-2/3 entries, 0/9 each). Four lanes are burst-only (M3 §9).

## Key defects found (M1/M2)

- **Token-plan keys 2 and 3 are quota-dead for the whole lane** — chat returns
  429 `insufficient_quota` with resets **10-23 16:00:00 UTC** (key 2) and
  **10-28 16:00:00 UTC** (key 3); `/models` still answers 200 on both, so an
  endpoint listing is not evidence of usable quota (`census/ANALYSIS.md` D2).
  M3 measured all four affected pool entries at 0/9 (auth class).
- **Two declared fields do not exist in this client**: `off_effort` (10
  entries) and `max_input_size` (9 entries) have **0 occurrences** in the
  client binary and **0 wire effect** (`definitions/ANALYSIS.md` §1, §3 rule 1).
- **The global `[thinking] effort = "max"` overrides every model default and is
  not clamped to `support_efforts`** — 31 entries are sent a value they do not
  declare (DEF-3b). Lanes that validate the field (token-plan, codex,
  opencode-go) accepted `max`; lanes that ignore it (hyper, zai, xai, cursor)
  show vacuous acceptance (`definitions/ANALYSIS.md` §4.1). Consequence:
  `zai-coding-plan/glm-5.3-flash-low`'s LOW pin cannot reach the wire today.
- **`reasoning_key` defects** — 2 entries declare `reasoning_content` while the
  lane returns `reasoning`/`reasoning_details` (DEF-9: `opencode-go/kimi-k3`,
  `opencode-go/mimo-v2.5`); 9 declare nothing while the lane returns
  `reasoning_content` (DEF-10: the 6 probed `hyper` models plus
  `cascade/deepseek-v4.1-flash`, `cascade/glm-5.3-flash`, `xai-oauth/grok-4.5`)
  (`definitions/ANALYSIS.md` §4.4).
- **42 of 143 entries route to lanes that cannot serve them at audit time** —
  4 on `managed:kimi-code` (401 on every path; empty OAuth store; includes
  `default_model = kimi-code/kimi-for-coding`), 19 on `alibaba-token-plan-2`,
  19 on `alibaba-token-plan-3` (`definitions/ANALYSIS.md` §5 class D; census
  D1/D2).
- Also load-bearing: `kimi doctor config` validates no model-level keys, so its
  silence is not correctness evidence (`definitions/ANALYSIS.md` §1); the devin
  cold start blocked a first chat past 300 s once, and devin legs billed
  ~12.2k/~11.7k prompt tokens for the identical short prompt (census D7/D9);
  both cursor lanes failed the tool probe and "chat-only" cannot be expressed
  in config (definitions §4.2, §3 rules 5–6).

## Routing policy outcome (M4)

- `routing/kimi-secondary-models-round18.toml` replaces the 17-entry pool with
  **13 live entries**: 11 retained with role text rewritten from the
  measurements (two demoted — `cascade/glm-5.3-flash` FAST → fallback-only,
  `alibaba-token-plan/qwen3.8-flash` → batch-only), **4 quarantined** (the
  token-plan key-2/3 quadruple; re-entry only after the reset AND a passing
  chat probe), **2 dropped** (both cursor lanes), and **2 verify-first adds**
  from the wider catalog (`xai-oauth/grok-4.7`, `opencode-go/deepseek-v4.1-flash`)
  with census/M6 evidence and explicitly no bucket promotion.
- Ladders (measured): FAST `hyper/deepseek-v4.1-flash` 2081 ms → token-plan
  key 1 2251 ms → `zai/glm-5.3-flash-low` 2796 ms →
  `cascade/deepseek-v4.1-flash` (chain opencode-go→hyper→devin; `default_model`
  unchanged) → `cascade/glm-5.3-flash` (fallback-only). MIDDLE
  `zai/glm-5-turbo` → `xai/grok-4.5` → `hyper/qwen3.8-flash` →
  `alibaba-token-plan/qwen3.8-flash` (batch) → `opencode-go/deepseek-v4.1-flash`
  (verify-first overflow). STRONG `gpt-6.1-sol` → `gpt-6.1-sol-high` →
  `grok-4.7` (verify-first); the single-provider risk is named in-file (both
  measured STRONG lanes share one shim and one upstream model id).
- **Lane policy applied**: opencode-go is admitted for `deepseek-v4.1-flash`
  only — its GLM lane is not in the table at all; `glm-5.3-flash` is described
  as zai-primary → devin-secondary, with an operator check attached because
  M2's tool probe was answered by the devin leg in pass 1 and the zai leg in
  pass 2 (the live shim may be devin-first; it was neither inspected nor
  edited).
- **Codex fast mode (M5): no-go for now.** `service_tier:"priority"` is
  accepted (200) while `flex`/`fast`/`auto`/an invalid control all return 400 —
  but every serviced response echoes `auto`→`default`, no quota/usage field
  moves (credits balance static at 62500, used-percent static at 1), and the
  +14.00 TPS delta vs the M3 baseline is not separable from noise at n=2
  (`priority`'s slowest rep falls below every `default` rep). The kimi client
  cannot send the field at all, so no fast-mode entry exists. Conditional
  protocol before any flip: n ≥ 10 interleaved `default`/`priority`, both sol
  pins, independent applied-tier confirmation, plus a shim-side
  `SHIM_SERVICE_TIER` injection (filed idea, not implemented)
  (`fastmode/ANALYSIS.md` §1, §7).
- The table was **not applied**: `routing/APPLY.md` is the operator runbook
  (pinned-hash preflight, timestamped backup, dry-run-verified
  `splice_secondary.py`, reload checks, rollback). Routing hygiene: 0 hits,
  exit 0 (`routing/HYGIENE.md`).

## Artifact pointers (parent repo, `../`)

- **census/** (M1, `4738fee`): `ANALYSIS.md` (inventory, defects D1–D9, usage
  evidence, TTFT/TPS smoke), `manifest.json`, `raw/`, `scripts/`,
  `HYGIENE.md` (CLEAN, 0 hits, exit 0).
- **definitions/** (M2, `7e2c473`): `ANALYSIS.md`, `audit-table.md` +
  `audit-table.json` (all 143 entries with findings), `config-corrections.toml`
  (56 splice-ready blocks + quarantine + verify-later), `HYGIENE.md`
  (25 files scanned, 0 hits, exit 0).
- **battery/** (M3, `c2174a5`): `ANALYSIS.md`, `SELECTION.md` (26→17 pool
  diff), `SMOKE.md`, `predictions/`, `raw/` + `smoke/` (402 files),
  `HYGIENE.md` (402 scanned, 0 hits, exit 0).
- **battery-opencode/** (M6, `bd0c690`): `ANALYSIS.md`, `predictions/`,
  `raw/`, `smoke/` (44 files), `HYGIENE.md` (44 scanned, 0 hits, exit 0).
- **fastmode/** (M5, `db82042`): `ANALYSIS.md`, `raw/` (run1/run2 captures,
  discovery and echo evidence), `scripts/` (14 files), `HYGIENE.md`
  (14 scanned, 0 hits, exit 0).
- **routing/** (M4, `fbae972`): `kimi-secondary-models-round18.toml`
  (13-entry payload + evidence ledger + ladders + limits), `APPLY.md`,
  `splice_secondary.py`, `hygiene_check.py`, `HYGIENE.md` (7 scanned, 0 hits,
  exit 0), `kengaku-round18-report.md`.
- **Fleet report**: `../.ufo/reports/round-18/kengaku.md` (identical copy;
  committed `389ede4`, merge `fbae972`).
- Per-tree file counts and hygiene-gate detail:
  `corpus/evidence/round18-kimi-routing/README.md`.

## Limits

- n=2 reps per model for TTFT/TPS; one correctness draw per probe. Every
  number is a signal, not a benchmark score (`battery/ANALYSIS.md` §9).
- Burst-flushed lanes cannot be ranked on client-side throughput; the fix is
  shim-side incremental flushing, outside this round's scope.
- Fixed short prompt: long-context ranking may differ.
- Verify-first entries carry census smoke / single-measurement evidence only
  and must not be promoted without an M3-style battery run (`routing/APPLY.md`
  Step 6).
- The pool is an operator artifact: the live config still holds the 17-entry
  pool until the operator runs `routing/APPLY.md`.
- This entry digests the parent trees; regenerate numbers from the merge
  commits above, not from this text.
