source: S178 — llama.cpp server API reference, `tools/server/README.md` @ tag `b7200` (commit `ab49f094d29057b2c4d2b0f1e822c9140df1b0e1`), anchors `:1157-1163` and `:758-770`; local probe receipt `corpus/evidence/round51/surfaces/endpoints.txt`
verified-at: 2026-10-28
recheck: 90d

# Served-endpoint identity pin — what to record so a model number means something

A local OpenAI-compatible server answers `/v1/models` with an `id` that is **not** a stable
model identity: the upstream server documentation states that by default the `id` field is the
path to the model file given to `-m`, and only `--alias` changes it
(`tools/server/README.md:1163` @ `b7200`). Two servers can therefore serve different weights
under the same `id`, and the same weights under two `id`s. Any capability number taken from such
an endpoint inherits that ambiguity unless the pin below is recorded next to it.

## The pin (six fields, all captured at one instant)

| Field | Where it comes from | Why it is in the pin |
|---|---|---|
| `id` + `owned_by` | `GET /v1/models` | what a client sees; alone it identifies nothing |
| alias / model path | server argv (`--alias`, `--model`) or `/props.model_path` | the weights actually loaded |
| context + slots | `/props` → `default_generation_settings.n_ctx`, `total_slots` | the window and concurrency the number was taken under |
| generation defaults | `/props` → `default_generation_settings.params` (temperature, top_k/top_p, seed) | sampling defaults change capability at fixed prompts |
| build | `/props.build_info` | the server binary revision; behaviour drifts between builds |
| owning process | `/proc/<pid>/cmdline`, tokenised | the argv is the only place flags like `--jinja`, `--kv-unified`, `--parallel` appear |

The upstream docs define the surfaces the pin reads: `/v1/models` returns "information about the
loaded model" (`:1157-1159`), `/props` is "read-only by default" and returns the server's global
properties including `default_generation_settings` (`:758-770`), and `/health` is a public check
(`:404-406`).

## Measured pin on this host (2026-10-28, capture-time only)

| Field | Value |
|---|---|
| direct server | `http://127.0.0.1:45669` — `id` `LFM3-1.7B`, `owned_by=llamacpp` |
| router | `http://127.0.0.1:1234` — `lfm3-server.service`, `--models-dir /home/vgpnk/models/lfm3 --models-max 2`, lists 5 model ids |
| alias / path | `--alias LFM3-1.7B`, `--model /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf` |
| context / slots | `n_ctx=32768`, `total_slots=4` |
| generation defaults | `temperature=0.1`, `top_k=50`, `top_p=0.95`, `seed=4294967295` (server defaults) |
| build | `b1-39ebd2` |
| process | pid 242776, 16 argv tokens, `--jinja --log-colors off --n-gpu-layers 99` |

Receipt: `corpus/evidence/round51/surfaces/endpoints.txt`. The predecessor endpoint
`:34113` (Qwen3-Coder-30B-A3B UD-IQ2_XXS) returns HTTP 000 at the same instant and no socket
listens; its round-10/11 process pins (pid 1299, 41 argv tokens) stay historical capture-time
facts, not live state.

## Decision rules

1. **A number without a pin is unlabelled.** Record the six fields beside every measurement
   taken from a served endpoint; a bare `id` does not satisfy this entry.
2. **A pin is host state, not a capability claim.** It says what answered at an instant; it does
   not say what the model can do. Re-take it, do not extend it.
3. **Flag authority is not this lane's.** Which flags the server runs with belongs to the
   serving plane (`PROVINCE.md` §Refusals, owner `kama`); this lane records the flags it observed
   and the capability interpretation only.
4. **Two endpoints, one pin each.** A router that lists several ids and a direct server that
   serves one are two pins; the router's list is a catalogue, not a statement about what is
   loaded.

## Limits

- Point-in-time: the values above were measured once, on one host, at 2026-10-28; a restart
  changes `build_info`, slots and defaults. `plans/round51_surfaces.py` re-probes the endpoint
  surfaces, and a moved endpoint legitimately turns the recorded state `STALE`.
- The `/props` defaults are the server's, not the harness's: a request that sets `temperature`
  overrides them, and the pin then describes the server, not the run.
- No generation request was sent for this entry; every field is metadata. Capability numbers
  taken from this endpoint are still unmeasured.
