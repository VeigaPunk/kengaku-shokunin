source: corpus/SOURCES.md S178 — llama.cpp HTTP server documentation, `tools/server/README.md` at commit `8642541b255bfb5dc39cd351a178be09013a55d6` (the v0.8.0 bump, committed 2026-10-28T11:30:38Z), https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md — fetched 2026-10-28, 2616 lines, sha256 `8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6`; anchors `:190` (`-a, --alias`), `:480` (`GET /health`), `:930` (`GET /props`), `:941` (`n_ctx` beside `params`), `:1019` (`total_slots` defined by `--parallel`), `:1345` (`GET /v1/models`), `:1376` (`id` defaults to the model path, `--alias` overrides). The row `SrcLlamaServer` drafted this round carries the placeholder id `S0??` and leaves id assignment to the L1 (`.ufo/waves/round-51/w1/SrcLlamaServer.md` §4, §limits); `S178` here is the **next free id derived from the committed registry** — `corpus/SOURCES.md` holds 170 rows, the highest is `S177`, and `S178`–`S251` are unallocated (`.ufo/waves/round-51/w1/SrcCensus.md`). The L1 lands the row and this entry together; if the landing assigns a different id, this line changes with it.
verified-at: 2026-10-28 (round 51 — live probes of the three `llama-server` processes on this host, run by `C1ExecEndpoints` and re-run independently by `C1ScribeKnowledge`; receipts `.ufo/waves/round-51/w1/C1ExecEndpoints.md`, `.ufo/waves/round-51/w1/C1ScribeKnowledge.md`)
recheck: 90d (the pin is host state — §When a pin must be re-taken carries the re-take command)

# Served-endpoint identity pin: what to record before citing a model's output

A served model is a **process**, not a model file. Two servers on the same host, both reporting
`owned_by=llamacpp`, can differ in weights, context, slot count, build and sampling defaults, and
the client-visible `model` string identifies none of those. Before any number measured against a
live endpoint is cited, record the pin below at one moment and keep it beside the number.

## The identity-pin decision table

Read every field at the same sitting; a pin assembled across a restart is not a pin. Measured
2026-10-28 on `127.0.0.1:45669` (the live LFM3 server) unless a row says otherwise.

| field | read from | measured value | why it is identity | trap |
|---|---|---|---|---|
| model id | `GET /v1/models` → `data[0].id` | `LFM3-1.7B` | the string a client passes as `model`; it is what the server resolves | the default `id` is the **model path**, not a name — `--alias` is what turns it into `LFM3-1.7B` (docs `:1376`). An id that looks like a path is not a different model. |
| aliases | `data[0].aliases` | `["LFM3-1.7B"]` | how the router and clients address the instance | a single-element list equals the id here; do not infer that aliases are absent on other builds |
| `owned_by` | `data[0].owned_by` | `llamacpp` | names the **serving implementation**, not the weights | `llamacpp` on `:45669` and on `:37323`, but the two are different builds (`b1-39febd2` vs `b1-9ff0d7e90`) and different weights |
| served context | `data[0].meta.n_ctx`, cross-checked against `/props` `default_generation_settings.n_ctx` and argv `--ctx-size` | `32768` in all three places | the context actually allocated | `n_ctx` sits **beside** `params`, not inside it (documented at `:941`, and the measured build agrees: `default_generation_settings` = `{"params": {...}, "n_ctx": 32768}`). Look inside `params` and you find nothing, which invites the false conclusion that the context is unpinned. |
| trained context | `data[0].meta.n_ctx_train` | `262144` | the model's own window | never substitute it for the served context: 262144 trained, 32768 served |
| weights file | `/props` `model_path` (equals argv `--model`) | `/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf` | ties the alias to bytes | the path is not the bytes: a file replaced in place keeps the path (see the digest row) |
| weights digest | `sha256sum` of the file at `model_path` | `8f6b24182258205e9e01e21f1f24a1f208c1e8115578825d202ce39976af20b6` | the only field that survives an in-place weight swap | 1.8 GB read; take it once per pin, not per request |
| weights size | `stat` the file; compare `/v1/models` `meta.size` | file `1846238496` bytes vs `meta.size` `1837991168` | separates the file from the model's own accounting | the two numbers differ by `8247328` bytes on this model — say which one a citation uses |
| quantisation | `data[0].meta.ftype` / `/props` `model_ftype` | `Q8_0` | precision is part of the identity of a measured number | two servers with the same alias at different `ftype` are different subjects |
| process argv | `/proc/<pid>/cmdline`, split on `\0` | 16 tokens (below) | the only place **explicit** flags live: `--jinja`, `--n-gpu-layers 99`, `--ctx-size 32768`, `--alias`, `--port`, `--log-colors off` | argv is silent about defaults. `--parallel` is absent yet `total_slots` is 4. |
| slot count | `/props` `total_slots` | `4` | the concurrency the number was measured under | documented as "defined by `--parallel`" (`:1019`), whose default is `-1` = auto (`:177`): argv alone under-reports the pin |
| build | `/props` `build_info` | `b1-39febd2` | the binary that decided the sampling and template semantics | `:37323` runs `b1-9ff0d7e90` (ollama-bundled) — same `owned_by`, different server |
| generation defaults | `/props` `default_generation_settings.params` | `temperature 0.10000000149011612`, `top_k 50`, `top_p 0.949999988079071`, `min_p 0.05000000074505806`, `repeat_penalty 1.100000023841858`, `seed 4294967295`, `n_predict -1`, `chat_format "Content-only"`, `reasoning_format "none"` | what a request that sends no sampling fields inherits | these are float32 renderings: `0.1` in a note is not `0.10000000149011612` on the wire, and a rounded pin cannot detect a preset edit |
| chat template | `/props` `chat_template` (+ `chat_template_caps`) | Jinja template present; caps `supports_tool_calls true`, `supports_system_role true`, `supports_reasoning_effort false` | the template turns a request into tokens; a template swap changes results with identical weights | `--jinja` is in argv, the template body is not: pin the caps, not just the flag |
| process identity | pid + `/proc/<pid>/stat` field 22 with `/proc/stat` `btime` | pid `242776`, started `2026-10-28T15:18:44Z` | distinguishes a restart that kept the same argv and port | the port is not the process: a restart on the same port is a different pin |

## What is not a pin

- **`created` in `/v1/models`.** Measured three times 2 s apart against one process (pid `242776`
  constant): `1793211893`, `1793211895`, `1793211897`. It advances with the request, so it is a
  response timestamp, not a load time. Recording it as identity makes every later comparison drift.
- **`GET /health` → `{"status":"ok"}`.** Liveness only; it is identical across builds, weights and
  contexts. It tells you a socket answers, never what answers.
- **`owned_by` alone.** `llamacpp` covers all three `llama-server` processes on this host, across two
  builds; it names the implementation family, not the subject.
- **the alias alone.** `LFM3-1.7B` is a name the operator chose; the weights behind it are pinned
  only by `model_path` + digest.
- **a router's `/props` as a model pin.** On `:1234` the same build answers
  `{"role":"router","model_path":"none","default_generation_settings":{"params":null,"n_ctx":0},"max_instances":2,"models_autoload":true}`.
  A router has no single model; pin the loaded instance's own port (`:45669`), or query the router
  with `?model=` (docs `:2153`–`:2156`). The router's `/v1/models` does forward the instance's
  `status.args` and `preset`, but those are the router's cached copy of a load, not a live `/proc`
  reading.

## When a pin must be re-taken

Re-take the whole pin — never patch one field — when any of these changes:

1. **pid or process start time** changed (a restart on the same port is a different subject).
2. **`build_info`** changed.
3. **`data[0].id`, `aliases`, or `model_path`** changed.
4. **weights digest** changed, even if the path did not (in-place replacement).
5. **`total_slots`, `n_ctx`, or any `default_generation_settings.params` field** changed — a preset
   edit is invisible in argv.
6. **`owned_by` at the same port** changed: another server took the port. `:37323` is a live example
   of a different build and a different model behind the same interface.
7. **the model path is scratch.** `:37323` serves
   `/fast/scratch/hyaku/kama-r61-closure/c1/c1-9z8mmjqy/run-pd/models/blobs/sha256-270cba1bd5109f42d03350f60406024560464db173c0e387d91f0426d3bd256d`
   — a pin to a scratch path expires with the scratch tree and can only be cited as a historical
   reading.
8. **the endpoint was absent at the last check and answers again.** `:34113` is absent today
   (`curl: (7) Failed to connect`), and it is the endpoint whose round-10 pin is quoted in
   `PROVINCE.md` §Surfaces. If it returns, the recorded state goes `STALE` — that is the counter
   behaving correctly (`plans/round-51-claims.md` §Limits), not a defect to suppress.

Re-take block (one sitting, same shell):

```sh
P=45669; PID=$(ss -ltnpH "sport = :$P" | grep -o 'pid=[0-9]*' | cut -d= -f2)
curl -sS http://127.0.0.1:$P/health
curl -sS http://127.0.0.1:$P/v1/models
curl -sS http://127.0.0.1:$P/props
tr '\0' '\n' < /proc/$PID/cmdline
awk '{print "pid="$1" starttime="$22}' /proc/$PID/stat
sha256sum "$(curl -sS http://127.0.0.1:$P/props | python3 -c 'import sys,json;print(json.load(sys.stdin)["model_path"])')"
```

Append the new dated reading; **never overwrite** a prior pin. The old pin is what the old numbers
were measured against, and a silently re-pinned entry cannot be audited.

## Limit: a point-in-time pin is host state, not a capability claim

The pin says *which process answered at this moment*. It does not say the model can do anything:

- **No capability follows from it.** The same weights at `Q8_0` with a 4-slot server, a different
  KV-cache quantisation or a different template are different measurement subjects; only a probe
  measures capability. `PROVINCE.md` §Surfaces keeps the round-10 flags (`--parallel 2`, q4_0 KV,
  `--kv-unified`) precisely because they are "an unstated premise of every r8/r9 number" — a premise,
  not a result.
- **It is not weight provenance.** A digest identifies bytes; it says nothing about training data,
  licence, or whether the file is the upstream release.
- **It is not availability.** The pin is true at `verified-at` and false the moment the process
  exits; §When a pin must be re-taken is the expiry rule, and `recheck: 90d` is the outer bound.
- **It is not ownership.** `PROVINCE.md` §Adjacent routes the serving plane and endpoint identity to
  **kama**; this lane keeps the interpretation evidence and never remediates flags. The pin is a
  reading handed to the owner, not a change made in their domain.

## Measured, verbatim (2026-10-28, round 51)

`/proc/242776/cmdline`, `tr '\0' '\n'` — 16 tokens:

```
/home/vgpnk/src/llama.cpp/build/bin/llama-server
--host
127.0.0.1
--jinja
--log-colors
off
--port
45669
--alias
LFM3-1.7B
--ctx-size
32768
--model
/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
--n-gpu-layers
99
```

`GET /v1/models` (`:45669`) — one element, as documented at `:1349` (verbatim, line-wrapped;
`created` is the request timestamp, see §What is not a pin):

```json
{"data":[{"id":"LFM3-1.7B","aliases":["LFM3-1.7B"],"tags":[],"object":"model",
"architecture":{"input_modalities":["text"],"output_modalities":["text"]},
"created":1793211893,"owned_by":"llamacpp",
"meta":{"vocab_type":2,"n_vocab":128000,"n_ctx":32768,"n_ctx_train":262144,
"n_embd":2048,"n_params":1728801600,"size":1837991168,"ftype":"Q8_0"}}]}
```

`GET /props` (`:45669`), identity fields only: `model_alias LFM3-1.7B`, `model_ftype Q8_0`,
`model_path` as above, `build_info b1-39febd2`, `total_slots 4`,
`default_generation_settings.n_ctx 32768`, `endpoint_props false`,
`endpoint_metrics false`, `is_sleeping false`, `modalities {"vision":false,"video":false,"audio":false}`,
`bos_token <|startoftext|>`, `eos_token <|im_end|>`.

Comparison endpoints, same sitting: `:37323` = ollama-bundled `llama-server` build `b1-9ff0d7e90`,
pid `3262613`, `-c 2048 -np 1`, `total_slots 1`, `temperature 0.800000011920929`, `top_k 40`,
`repeat_penalty 1.0`, weights at the kama scratch blob path above. `:1234` = router, build
`b1-39febd2`, `--models-dir /home/vgpnk/models/lfm3 --models-max 2 -c 32768 --jinja`.
`:34113` — connection refused (absent); `:8791` is the ds-flash-shim (`/props` → `unknown path /props`,
`/v1/models` → one id `deepseek-v4.1-flash`, `owned_by ds-flash-shim`), not a llama.cpp server.

## Scope limits

The pin covers the fields above and nothing else. It does not measure throughput, latency, output
quality, or context behaviour under load; it does not check the model against a task; and it does not
say the endpoint should be used. `unmeasured` in this entry would mean "not read this round": every
number above was read from the live processes or the pinned documentation at 2026-10-28, and nothing
was inferred from a prior round's pin.
