# C1ExecEndpoints — round 51, w1 executor (ENDPOINT surfaces)

Seat: `C1ExecEndpoints` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axis worked: **freshness** (R51-C1) — this seat independently probes every endpoint surface
PROVINCE.md declares or that resolves on this host, so that C1's endpoint rows (`SF03` :34113,
`SF16` :8791) and the round-51 *new* served-endpoint row rest on a measurement that does not come
from the counter's own probe. Scope: endpoints only. No production file was read-modified; this
report is the only write.

Read first, in full: `plans/round-51-claims.md`, then the frozen C1 instrument
`plans/round51_surfaces.py` and manifest `plans/round51-surfaces.json`.

## Axes named (Godspeed)

1. **freshness** — endpoint rows must state what resolves *today*, at the tip, with a date.
2. **identity** — an endpoint row is only useful if it pins *which* server answered: model id,
   `owned_by`, `n_ctx`, generation defaults, and the owning process argv. Reachability alone is
   the defect class this seat exists to remove.
3. **cheapness** — read-only GETs and `/proc` reads only; no completion traffic, no mutation.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Stage-1 freeze commit `e07f131cf7037e58a21db6e1f3986cf401ad257c` is an ancestor of HEAD
(`git merge-base --is-ancestor e07f131 HEAD` → true); HEAD is one commit later
(`4090c3d round-51: v2 wave spec (64 seats) + validated dispatch payload`). Every endpoint
measurement below was taken at `4090c3d`, 2026-10-28T15:2x-03:00.

Working tree at measurement time carried sibling-seat edits (not mine, not touched):

```
 M plans/round42_c1_verify.py
 M plans/routed_open.py
 M plans/scratch_guard.py
?? .ufo/waves/round-50/w1.ready
?? .ufo/waves/round-50/w1.ready.partial
```

## Commands run (exact)

```sh
ss -ltnp | head -40
ss -ltn 'sport = :34113'
ss -ltnp 'sport = :8791'      # and :1234, :45669, :37323 individually
curl -sS -m 5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:34113/health
curl -sS -m 5 http://127.0.0.1:34113/v1/models
for p in 1234 37323 45669 8791; do
  curl -sS -m 8 "http://127.0.0.1:$p/v1/models" -o probe/models-$p.json -w "models-$p HTTP %{http_code}\n"
  curl -sS -m 8 "http://127.0.0.1:$p/health"   -o probe/health-$p.json -w "health-$p HTTP %{http_code}\n"
  curl -sS -m 8 "http://127.0.0.1:$p/props"    -o probe/props-$p.json  -w "props-$p HTTP %{http_code}\n"
done
tr '\0' '\n' < /proc/<pid>/cmdline          # 242776 3262613 1706355 1515 (+ shim family 1511-1518)
ps -o pid,ppid,comm,args --ppid 1706355
readlink /proc/1515/cwd ; sha256sum ~/.local/share/ds-flash-shim/shim.py
python3 plans/round51_surfaces.py --lane .   # frozen counter, read-only, for cross-check
```

Socket→process ownership was cross-checked *independently of `ss`* by matching the listening
socket inode in `/proc/net/tcp` against `/proc/<pid>/fd/*`:

```
/proc/net/tcp 45669 0A 0100007F:B265 1000 1497587421
/proc/net/tcp 8791  0A 0100007F:2257 1000 24065
/proc/net/tcp 37323 0A 0100007F:91CB 1000 1309190774
/proc/net/tcp 1234  0A 0100007F:04D2 1000 1478639884
INODE->PID {'24065': ['1515'], '1497587421': ['242776'], '1478639884': ['1706355'], '1309190774': ['3262613']}
```

No `/proc/net/tcp` or `/proc/net/tcp6` entry exists for port `0x8541` (34113) — the absence is
not an `ss` artefact.

## Result 1 — `:34113` is absent (confirms SF03 `state=absent`)

```
$ ss -ltn 'sport = :34113'
State Recv-Q Send-Q Local Address:Port Peer Address:Port
                                            (header only, 57 bytes, rc=0)

$ curl -sS -m 5 http://127.0.0.1:34113/health
curl: (7) Failed to connect to 127.0.0.1:34113 after 0 ms: Could not connect to server   (rc=7)

$ curl -sS -m 5 http://127.0.0.1:34113/v1/models
curl: (7) Failed to connect to 127.0.0.1:34113 after 0 ms: Could not connect to server   (rc=7)
```

The `## Surfaces` row that declares `http://127.0.0.1:34113` (`/v1/models`, `/health`,
`/v1/chat/completions`, Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS, `owned_by=llamacpp`,
`n_ctx=16384`, pid 1299) is **stale in every clause**: no socket, no process, no model. Its
`prose` must go `absent` and it needs a dated `ABSENT 2026-10-28` marker (C1 `DRIFT`/`UNVERDICTED`
treatment). The `n_ctx=16384` figure has no live referent anywhere on this host — the only live
`n_ctx` values are 32768 (LFM3-1.7B) and 2048 (the kama scratch model), plus the router's `0`.

## Result 2 — `:8791` is present (confirms SF16), and it publishes **no** generation defaults

```
$ ss -ltnp 'sport = :8791'
LISTEN 0  512  127.0.0.1:8791  0.0.0.0:*  users:(("python3",pid=1515,fd=3))

GET /v1/models  -> HTTP 200
{"object": "list", "data": [{"id": "deepseek-v4.1-flash", "object": "model", "created": 0, "owned_by": "ds-flash-shim"}]}

GET /health     -> HTTP 200
{"ok": true, "service": "ds-flash-shim", "port": 8791, "legs": ["alibaba-token-plan", "hyper", "opencode-go"]}

GET /props      -> HTTP 404
{"error": {"message": "unknown path /props"}}

GET /           -> HTTP 200, body identical to /health
GET /version    -> HTTP 404  {"error": {"message": "unknown path /version"}}
GET /v1/models/deepseek-v4.1-flash -> HTTP 404  {"error": {"message": "unknown path /v1/models/deepseek-v4.1-flash"}}

argv  (/proc/1515/cmdline, NUL-tokenised, 2 tokens): /usr/bin/python3
                                          /home/vgpnk/.local/share/ds-flash-shim/shim.py
pid 1515  ppid 1494 (/usr/lib/systemd/systemd --user)  cwd /home/vgpnk
sha256 42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  ~/.local/share/ds-flash-shim/shim.py
       (16957 bytes, mtime 2026-10-15 14:15:50 -0300) — matches the SF15 pin 42d86d99
```

**Identity-pin consequence for the new row:** `:8791` exposes a model *listing* and a service
identity, but **no `n_ctx` and no generation defaults** — `/props` is 404, not a llama.cpp server.
Any row that states `n_ctx` or sampling defaults for the 8791 surface would be a fabricated
reading. `owned_by` is the shim, not a model vendor: `ds-flash-shim`.

## Result 3 — the two live model servers on this host

`ss -ltnp` shows **three** `llama-server` processes, not two: one *router* and **two
model-serving instances** (the "two live servers" this item names). The router is the parent of
one of them.

```
$ ss -ltnp 'sport = :1234'   LISTEN 0 512 127.0.0.1:1234   users:(("llama-server",pid=1706355,fd=18))
$ ss -ltnp 'sport = :45669'  LISTEN 0 512 127.0.0.1:45669  users:(("llama-server",pid=242776,fd=19))
$ ss -ltnp 'sport = :37323'  LISTEN 0 512 127.0.0.1:37323  users:(("llama-server",pid=3262613,fd=3))

$ ps -o pid,ppid,comm,args --ppid 1706355
  242776 1706355 llama-server /home/vgpnk/src/llama.cpp/build/bin/llama-server --host 127.0.0.1 --jinja
                              --log-colors off --port 45669 --alias LFM3-1.7B --ctx-size 32768
                              --model /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf --n-gpu-layers 99
```

So `:45669` is a **child of the `:1234` router** (`--models-dir /home/vgpnk/models/lfm3
--models-max 2 --models_autoload`), and `:37323` is an independent `ollama v0.40.11` llama-server
under `systemd --user`.

### 3a. `:45669` — `LFM3-1.7B` (llama.cpp b1-39febd2, router-spawned)

```
/v1/models -> HTTP 200
{"data":[{"id":"LFM3-1.7B","aliases":["LFM3-1.7B"],"tags":[],"object":"model","owned_by":"llamacpp",
 "created":1793211407,"architecture":{"input_modalities":["text"],"output_modalities":["text"]},
 "meta":{"vocab_type":2,"n_vocab":128000,"n_ctx":32768,"n_ctx_train":262144,"n_embd":2048,
         "n_params":1728801600,"size":1837991168,"ftype":"Q8_0"}}]}

/health -> HTTP 200  {"status":"ok"}

/props  -> HTTP 200  build_info "b1-39febd2", total_slots 4, model_alias "LFM3-1.7B",
                     model_ftype "Q8_0", is_sleeping false, cors_proxy_enabled false,
                     model_path "/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf",
                     default_generation_settings.n_ctx = 32768
generation defaults (default_generation_settings.params):
  temperature 0.10000000149011612   top_k 50      top_p 0.949999988079071
  min_p 0.05000000074505806         repeat_penalty 1.100000023841858   repeat_last_n 64
  seed 4294967295                   n_predict -1  max_tokens -1        n_keep 0  n_discard 0
  typical_p 1.0   xtc_probability 0.0   dry_multiplier 0.0   mirostat 0   speculative.types "none"
  chat_format "Content-only"        reasoning_format "none"   backend_sampling false
  samplers ["penalties","dry","top_n_sigma","top_k","typ_p","top_p","min_p","xtc","temperature"]
```

`/proc/242776/cmdline` (NUL-tokenised), exactly 16 tokens:
`/home/vgpnk/src/llama.cpp/build/bin/llama-server`, `--host 127.0.0.1`, `--jinja`,
`--log-colors off`, `--port 45669`, `--alias LFM3-1.7B`, `--ctx-size 32768`,
`--model /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf`, `--n-gpu-layers 99`.
Started `Wed Oct 28 12:18:44 2026`. Model file on disk 1,846,238,496 bytes, mtime
`2026-10-28 11:51:12 -0300`; the server's `meta.size` says 1,837,991,168 (tensor bytes vs file
bytes — the two numbers differ by 8,244,328 and are **not** interchangeable in a row).

### 3b. `:37323` — anonymous ollama blob model (llama.cpp b1-9ff0d7e90) — **model file is gone**

```
/v1/models -> HTTP 200
{"models":[{"name":"/fast/scratch/hyaku/kama-r61-closure/c1/c1-9z8mmjqy/run-pd/models/blobs/sha256-270cba1bd5109f42d03350f60406024560464db173c0e387d91f0426d3bd256d", ...}],
 "object":"list","data":[{"id":"/fast/scratch/hyaku/kama-r61-closure/c1/c1-9z8mmjqy/run-pd/models/blobs/sha256-270cba1bd5109f42d03350f60406024560464db173c0e387d91f0426d3bd256d",
 "owned_by":"llamacpp","aliases":["/fast/scratch/.../sha256-270cba1b…256d"],
 "meta":{"vocab_type":1,"n_vocab":512,"n_ctx":2048,"n_ctx_train":2048,"n_embd":64,
         "n_params":292800,"size":1171200,"ftype":"(guessed) all F32"}}]}

/health -> HTTP 200  {"status":"ok"}

/props  -> HTTP 200  build_info "b1-9ff0d7e90", total_slots 1, is_sleeping false,
                     model_ftype "(guessed) all F32",
                     model_path = the same /fast/scratch/hyaku/kama-r61-closure/... blob path,
                     default_generation_settings.n_ctx = 2048
generation defaults: temperature 0.800000011920929, top_k 40, top_p 0.949999988079071,
  min_p 0.05000000074505806, repeat_penalty 1.0, repeat_last_n 64, seed 4294967295,
  n_predict -1, max_tokens -1, chat_format "Content-only", reasoning_format "none",
  samplers identical to 3a, mirostat 0, typical_p 1.0, xtc_probability 0.0
```

`/proc/3262613/cmdline` (NUL-tokenised), 28 tokens:
`/home/vgpnk/.local/opt/ollama-v0.40.11/lib/ollama/llama-server`, `--model <blob path>`,
`--port 37323`, `--host 127.0.0.1`, `--no-webui`, `--offline`, `-c 2048`, `-np 1`,
`--log-verbosity 4`, `--no-log-prefix`, `--no-log-timestamps`, `--load-mode none`,
`--flash-attn auto`, `-b 512`, `-ub 512`, `--context-shift`, `--keep 4`.
Started `Wed Oct 28 07:44:41 2026` (uptime 07:38:16 at measurement), ppid 1494 = `systemd --user`.

**Freshness defect observed (not this seat's to fix):** the model path this server reports in
`/v1/models` and `/props` **does not exist**:

```
$ stat -c '%s %y' /fast/scratch/hyaku/kama-r61-closure/c1/c1-9z8mmjqy/run-pd/models/blobs/sha256-270cba1b…256d
stat: cannot stat '…': No such file or directory (os error 2)
```

i.e. a live, `/health`-green, `--offline` server is serving a model whose blob was deleted from a
**sibling lane's scratch tree** (`kama-r61-closure`). It answers metadata but its identity pin
points at an absent file. It is not a kengaku surface and must not become one.

### 3c. `:1234` — llama.cpp **router** (parent of 3a), not a model server

```
/v1/models -> HTTP 200, 5 catalog entries, exactly 1 loaded:
  LFM3-1.7B                          owned_by llamacpp  context_length 262144  status loaded
    status.args -> the :45669 argv above (--port 45669 --ctx-size 32768 …)
  LFM3-1.7B-Uncensored               unloaded   context_length 262144
  LFM3-Omni-2B                       unloaded   context_length 128000  (text+image+audio)
  LFM3-VL-2B                         unloaded   context_length 128000
  LiquidAI/LFM3-1.7B-GGUF:Q8_0       unloaded   context_length 262144

/health -> HTTP 200  {"status":"ok"}

/props  -> HTTP 200
{"role":"router","max_instances":2,"models_autoload":true,"model_alias":"llama-server",
 "model_path":"none","default_generation_settings":{"params":null,"n_ctx":0},
 "ui_settings":{},"build_info":"b1-39febd2","cors_proxy_enabled":false}
```

`/proc/1706355/cmdline`, 14 tokens: `/home/vgpnk/src/llama.cpp/build/bin/llama-server`,
`--models-dir /home/vgpnk/models/lfm3`, `--models-max 2`, `--host 127.0.0.1`, `--port 1234`,
`-ngl 99`, `-c 32768`, `--jinja`. Started `Wed Oct 28 11:52:04 2026`.

**Pin trap:** the router's `/props` answers 200 with `"params": null, "n_ctx": 0`. A row that
reads `n_ctx` from `:1234/props` records `0` and a row that reads generation defaults records
`null`. Neither is a model's identity; the model identity lives on the child port.

## Identity-pin block (for the new PROVINCE surface row)

Paste-ready. Every value below was read at `REV 4090c3d`, 2026-10-28, from the URLs and
`/proc` paths shown. Nothing here is inferred.

```
SURFACE  Served model identity (round 51, first identity-verified endpoint row)
ENDPOINT http://127.0.0.1:8791
PROBE-1  curl -sS -m 5 http://127.0.0.1:8791/v1/models   -> HTTP 200
         {"object":"list","data":[{"id":"deepseek-v4.1-flash","object":"model",
          "created":0,"owned_by":"ds-flash-shim"}]}
         model id   deepseek-v4.1-flash      (1 entry, no aliases field)
         owned_by   ds-flash-shim
PROBE-2  curl -sS -m 5 http://127.0.0.1:8791/health      -> HTTP 200
         {"ok":true,"service":"ds-flash-shim","port":8791,
          "legs":["alibaba-token-plan","hyper","opencode-go"]}
PROBE-3  curl -sS -m 5 http://127.0.0.1:8791/props       -> HTTP 404
         {"error":{"message":"unknown path /props"}}
         => n_ctx: NOT PUBLISHED.  generation defaults: NOT PUBLISHED. (not a llama.cpp server)
PROBE-4  ss -ltn 'sport = :8791'  -> LISTEN 127.0.0.1:8791
         socket inode 24065 (0x2257 in /proc/net/tcp) -> pid 1515
PROBE-5  tr '\0' '\n' < /proc/1515/cmdline
         /usr/bin/python3
         /home/vgpnk/.local/share/ds-flash-shim/shim.py
         ppid 1494 (/usr/lib/systemd/systemd --user)   cwd /home/vgpnk
PROBE-6  sha256sum ~/.local/share/ds-flash-shim/shim.py
         42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386
         (16957 bytes, mtime 2026-10-15 14:15:50 -0300)
OWNER    endpoint health is kama's ground (../shokunin.conf line 52:
         "kama|kama-shokunin|operability + calibration (local model serving and endpoint health)").
         This row declares REACHABILITY + IDENTITY only; it does not claim serving-plane ownership.
ABSENT   34113: no socket, curl rc=7, no 0x8541 entry in /proc/net/tcp{,6}  -> ABSENT 2026-10-28
```

Matching manifest entry the L1 can add (probe kind `http`, the only C1 kind that machine-checks a
live endpoint without asserting an unverified digest):

```json
{
  "id": "SF20",
  "section": "### Core",
  "anchor": "| Served model identity (round 51) | `curl -sS http://127.0.0.1:8791/v1/models`",
  "state": "present",
  "prose": "present",
  "probe": {"kind": "http", "urls": ["http://127.0.0.1:8791/v1/models"]},
  "why": "round-51 identity-verified endpoint: id deepseek-v4.1-flash, owned_by ds-flash-shim, no /props (404); proves reachability+identity, not serving quality"
}
```

Three constraints the block imposes on the row text (all measured, not stylistic):
1. It must **not** state `n_ctx` or sampling defaults for `:8791` — `/props` is 404.
2. It must **not** state a `context_length` for `deepseek-v4.1-flash` — the shim's `/v1/models`
   omits the field (unlike the llama.cpp servers, which publish `context_length` on `:1234` and
   `meta.n_ctx` on the child ports).
3. If the L1 instead anchors the new row on a llama.cpp instance, the pin must name the **child**
   port (`:45669`, `n_ctx=32768`, `LFM3-1.7B`, `owned_by=llamacpp`, b1-39febd2) and never
   `:1234`, whose `/props` reports `n_ctx 0` / `params null`, and never `:37323`, whose model blob
   is absent from disk and belongs to kama's scratch.

## Counter cross-check (frozen command, read-only)

```sh
python3 plans/round51_surfaces.py --lane .      # exit 1
```

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3   (SF01, SF02, SF03)
STALE 0
UNVERDICTED 1   (SF04)
NUMBER-DRIFT 1  (SF14 claims 25, probe says SOURCES rows=170)
ANCHOR-DUP 0 / ANCHOR-MISSING 0 / UNCOVERED 0 / SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

My independent probe agrees with the counter on both endpoint entries: `SF03` (`state=absent`,
`prose=present` → `DRIFT`) and `SF16` (`state=present`, `port` probe) are correct as recorded, and
`PROBES absent=6` includes `SF03`. The counter's `STALE 0` for the endpoint rows is therefore
*corroborated*, not merely self-consistent: `:34113` refuses TCP and `:8791` accepts it, measured
outside the counter with `ss`, `curl` and `/proc/net/tcp`.

## Adjacent observation (outside this item's scope, recorded so it is not re-litigated blind)

The PROVINCE `### Core` row "Live probe endpoint" says "`:8793` not probed this round". At this
tip it *does* resolve — the whole `8787–8796` family is the shim plane, all `HTTP 200` on
`/v1/models`:

```
8787 devin-shim       swe-2, swe-2-high/medium/max, deepseek-v4-1-flash-high, …
8788 cursor-shim      auto, gpt-5.3-codex-*, context_length 200000, owned_by cursor
8789 oauth-shim       gpt-6.1-sol, gpt-6-luna, owned_by shim
8790 oauth-shim       grok-4.20-*, context_length 1000000
8791 ds-flash-shim    deepseek-v4.1-flash, owned_by ds-flash-shim     <- SF16 surface
8793 glm-flash-shim   glm-5.3-flash, owned_by glm-flash-shim
8795 claude-shim      claude-opus-5-5, claude-opus-5-5-1m, …, owned_by claude
8796 antigravity-shim gemini-3.8-flash, gemini-3.5-flash, gemini-2.5-pro, …, owned_by antigravity
```

All eight are `python3|python …/<name>-shim/shim.py` children of pid 1494 (`systemd --user`).
This is a freshness finding for the L1, not a row I am authorised to add: the `:8793` clause is
dated to round 24 and is now false; either it is dated `2026-10-28` as re-verified, or it is
dropped from the row. I did not probe any shim's completion path and generated no model traffic.

## Limits

- Point-in-time, single host, single netns: measured 2026-10-28T15:2x-03:00 at `REV 4090c3d`.
  Any endpoint can move; C1's `STALE` is the correct detector, and this block is not a standing
  guarantee.
- Metadata only. No `/v1/chat/completions` or `/v1/completions` call was made against any server,
  so this seat cannot distinguish "listed" from "actually completes". PROVINCE refuses the
  serving plane and `shokunin.conf:52` assigns endpoint health to `kama`; generating traffic would
  also have crossed that boundary.
- `/props` fields are the server's *defaults*, not any run's effective settings; a request may
  override every one of them. `total_slots` is a slot count, not a concurrency measurement.
- `/proc/<pid>/cmdline` shows launch argv only. It does not prove the running binary matches
  `/home/vgpnk/src/llama.cpp/build/bin/llama-server` on disk (no digest of the binary was taken),
  nor that a systemd unit's ExecStart matches argv.
- `owned_by` is self-reported by the server (`llamacpp`, `ds-flash-shim`); it is an identity
  label, not an authorisation claim.
- The `legs` array on `:8791/health` names upstream providers. I recorded names only and read no
  credential material.
- I did not verify that `:45669`'s on-disk gguf matches the loaded weights (file 1,846,238,496 B
  vs `meta.size` 1,837,991,168 B — recorded, unexplained, not asserted as a defect).
- Two servers I did *not* enumerate: `zcode-host-local` (`:43835`), `kimi-webbridge` (`:10086`),
  `omp` (`:43367`), `node` (`:3000`), `MainThread` (`:3100/:3101/:3104`, `:40711/:41649`). None
  answered the OpenAI-compatible shape this item names and none is a declared kengaku surface, so
  probing them would be scope widening.

## Defects / risks handed to the L1

1. `SF03` (`:34113`) is dead in all clauses — the row needs `prose=absent` plus `ABSENT 2026-10-28`
   and must stop asserting `n_ctx=16384` as a live reading.
2. The `### Core` "Live probe endpoint" row's "`:8793` not probed this round" is stale; `:8793`
   resolves (`glm-5.3-flash`, `owned_by glm-flash-shim`).
3. A new row pinned to `:1234` or `:37323` would be a fresh defect: `:1234/props` reports
   `n_ctx 0`/`params null` (router), and `:37323`'s model blob is **absent from disk** while the
   server stays `/health`-green.
4. `:37323` is a live `--offline` llama-server holding a deleted model inside another lane's
   scratch (`/fast/scratch/hyaku/kama-r61-closure/…`). Cross-domain: route to `kama`, do not
   absorb.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C1ExecEndpoints` was created, used for the probe
captures and the counter log, and **removed before this report was finalised**; every output this
report cites is inlined verbatim above. No clone was needed (read-only lane work; no git fixture
was created, so no `git -C "$D"` assertion applies). No tool was installed for this item.

VERDICT: PASS — every ENDPOINT surface named by this item is independently measured at
`REV 4090c3d`: `:34113` is absent by three independent methods (`ss`, `curl` rc=7, no `0x8541` in
`/proc/net/tcp{,6}`), confirming SF03's `state=absent` and its `prose=present` drift; `:8791`
listens (pid 1515, `ds-flash-shim`, shim sha256 `42d86d99…15a386`) and publishes model id
`deepseek-v4.1-flash` / `owned_by ds-flash-shim` but **no** `n_ctx` and **no** generation defaults
(`/props` 404); the host's two live model servers are `:45669` (`LFM3-1.7B`, `owned_by llamacpp`,
`n_ctx 32768`, 4 slots, temp 0.1, top_k 50, repeat_penalty 1.1, b1-39febd2, child of the `:1234`
router, argv captured) and `:37323` (ollama v0.40.11 llama-server, anonymous blob id, `n_ctx 2048`,
1 slot, temp 0.8, top_k 40, repeat_penalty 1.0, b1-9ff0d7e90, model file absent on disk). The
identity-pin block above is the citable evidence for the new PROVINCE surface row; it forbids
claiming `n_ctx`/defaults for `:8791` and forbids anchoring on the router or on the kama-owned
blob server.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
