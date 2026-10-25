# r10 scout — served-model surface: cmdline ceiling closed

Ticket: PROVINCE.md ceiling "the served-model surface (`:34113` flags: `--cont-batching`, `-np`) is documented from behaviour, never from the process cmdline" (verbatim source below).
Method: no root, no sudo, uid 1000, read-only probes + /proc + user-unit file. Nothing in the repo was written.

## 1. Endpoint probes (verbatim)

`curl -s -m 5 http://127.0.0.1:34113/v1/models` → 872 bytes, full payload (`/tmp/kengaku-r10/models-34113.json`):

```json
{"models":[{"name":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","model":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","modified_at":"","size":"","digest":"","type":"model","description":"","tags":[""],"capabilities":["completion"],"parameters":"","details":{"parent_model":"","format":"gguf","family":"","families":[""],"parameter_size":"","quantization_level":""}}],"object":"list","data":[{"id":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","aliases":["/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf"],"tags":[],"object":"model","created":1790633228,"owned_by":"llamacpp","meta":{"ftype":"IQ2_XXS - 2.0625 bpw","n_ctx":16384,"n_ctx_train":262144,"n_embd":2048,"n_params":30532122624,"n_vocab":151936,"size":10327717888,"vocab_type":true}}],"object":"list"}
```

`curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` → `200`; body `{"status":"ok"}`; curl exit 0; wall 0.45 ms.
Note: probe is `/health` (llama.cpp native). The OpenAI-style `/v1/health` is **not** what PROVINCE cites; PROVINCE's row names `/health` — matches.

## 2. Serving process (no root needed — all three finders succeeded)

| Command | Output |
|---|---|
| `pgrep -af llama` | `1299 /home/vgpnk/.local/bin/llama-server ...` (exit 0) |
| `pgrep -af server` | hit 1299 (plus unrelated s6/jicofo/swayosd rows) (exit 0) |
| `ss -ltnp \| grep 34113` | `LISTEN 0 512 127.0.0.1:34113 0.0.0.0:* users:(("llama-server",pid=1299,fd=16))` (exit 0) |
| `tr '\0' ' ' < /proc/1299/cmdline` | readable, exit 0 — **no permission failure occurred** |
| `ls -l /proc/1299/exe` | `-> /home/vgpnk/.local/bin/llama-server` |
| `ps -o pid,ppid,user,etime,lstart -p 1299` | `1299 1225 vgpnk 16:11:34 Mon Sep 28 02:55:28 2026` |

**pid 1299, parent 1225 = `/usr/lib/systemd/systemd --user`** (i.e. a *user* service, hence /proc is fully readable to uid 1000).

### Full cmdline (41 argv tokens, verbatim, `\0`→space)

```
/home/vgpnk/.local/bin/llama-server --chat-template-file /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja --no-context-shift --no-cors-credentials --cors-origins http://127.0.0.1:8080 --host 127.0.0.1 --jinja --metrics --port 34113 --slots --no-webui --no-webui-mcp-proxy --alias /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --no-agent --ctx-size 16384 --cont-batching --cache-type-k q4_0 --cache-type-v q4_0 --flash-attn on --fit off --kv-unified --model /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --n-gpu-layers 999 --parallel 2 --split-mode none --timeout 900
```

`timeout 5 /home/vgpnk/.local/bin/llama-server --version` → `version: 0.3.0-dev (build 1, commit d7bd3bf)` / `built with GNU 16.2.1 for Linux x86_64`.

## 3. Second, independent source: the supervising unit (not just a cmdline snapshot)

`grep -rln 34113 ~/.config/systemd/user/` → `/home/vgpnk/.config/systemd/user/qwen-coder.service`
`systemctl --user status qwen-coder --no-pager` → `● qwen-coder.service - THE TICK Qwen3-Coder-30B-A3B-Instruct 2x16K`; `Loaded: ... enabled`; `Active: active (running) since Mon 2026-09-28 02:55:28 -03; 16h ago`; `Main PID: 1299 (llama-server)`; `Environment="CUDA_VISIBLE_DEVICES=0"`, `PATH=/home/vgpnk/.local/bin:...`.

Mechanical equality check (unit `ExecStart` after `\`-continuation join, `shlex.split` vs `/proc/1299/cmdline` split on `\0`):

```
unit_tokens 41 proc_tokens 41
EXACT_MATCH True
```
→ the unit is the *provenance* of the live argv, and the live argv is byte-equal to it. This makes the flag list durable across restarts (`Restart=on-failure`, `RestartSec=15`), unlike a one-shot `ps` reading.

## 4. Drift verdict vs PROVINCE.md

PROVINCE.md:14 (`read`): "Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` (Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, `owned_by=llamacpp`, `n_ctx=16384`)"

| PROVINCE claim | Recomputed evidence | Verdict |
|---|---|---|
| model Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS | `/v1/models` `id` = `.../Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`; cmdline `--model` identical string; unit `--model` identical | **MATCH** |
| `owned_by=llamacpp` | `/v1/models` `owned_by":"llamacpp"`; `/proc/1299/exe → .../llama-server` | **MATCH** |
| `n_ctx=16384` | `/v1/models` `meta.n_ctx=16384`; cmdline `--ctx-size 16384`; `/slots` 2× `n_ctx:16384` | **MATCH** (3-way) |
| port/host | cmdline `--port 34113 --host 127.0.0.1`; `ss` listener `127.0.0.1:34113` pid 1299 | **MATCH** |
| `--cont-batching` | present explicitly in argv + unit (llama.cpp also defaults it on in this build) | **MATCH** |
| `-np` (shorthand) | argv carries the long form **`--parallel 2`**; `-np` as a literal token does **not** appear | **MATCH (shorthand)** — the short spelling is the long flag's alias, not a separate flag |
| "(flags) documented from behaviour, never from the process cmdline" | cmdline now read: `tr '\0' ' ' < /proc/1299/cmdline` exit 0 | **CEILING CLOSED** — the flags are now sourced at process level |

**No drift.** All four PROVINCE-asserted facts reproduce, and the two flags it could only infer behaviourally are now literally in argv.

Behavioural cross-check that independently corroborates `--parallel 2` without spending a generation: `curl -s -m 5 http://127.0.0.1:34113/slots` → HTTP 200, JSON **array of 2** slot objects, each `"n_ctx":16384`, `is_processing:false`; `curl -s -m 5 http://127.0.0.1:34113/props` → HTTP 200, `total_slots=2`, `model_path` = same gguf path. That matches `--parallel 2 --kv-unified` (unified KV ⇒ each slot reports the **full** 16384, not 16384/2).

## 5. Facts the repo never names (new, for the L1 — not drift, but interpretation-relevant)

Flags present in argv/unit but absent from every PROVINCE/SKILL/SCORECARD mention I grepped (`grep -rn "cont-batching\|cont_batching\|continuous batching\|-np" corpus/evidence/ PROVINCE.md SKILL.md SCORECARD.md -i` → only the ceiling line itself + one unrelated llama.cpp issue #7052 hit):

- `--cache-type-k q4_0 --cache-type-v q4_0` — **KV cache is 4-bit-quantised**. Every round-8/9 horizon/replication result was produced under KV quantisation; if a future probe assumes f16 KV, that is an unstated premise.
- `--flash-attn on --fit off --kv-unified` — unified KV (shared across the 2 slots; see /slots above), so a 2-slot server does **not** halve per-slots context. Any "8 slots / 8 concurrent draws" reading of previous rounds must not assume `16384/parallel`.
- `--n-gpu-layers 999 --split-mode none --cache-type-*` on `NVIDIA GeForce RTX 5070, 11170 MiB` (`nvidia-smi --query-gpu=memory.used --format=csv,noheader`) — 65.4 MB RSS / **10.3 GB peak** per `systemctl --user status`; full offload.
- `--timeout 900`, `--no-context-shift` (no context shifting ⇒ long transcripts hard-stop rather than slide — relevant to the horizon probe's truncation semantics), `--chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja` + `--jinja` (a **custom, non-upstream** template; `/props` returns it, header reads "Copyright 2025-present Unsloth. Apache 2.0 License."), `--alias` = the model path (hence `id` is a filesystem path, not a friendly name), `--metrics --slots --no-webui --no-webui-mcp-proxy --no-agent`, `--cors-origins http://127.0.0.1:8080 --no-cors-credentials`.

Minor unexplained (UNVERIFIED, flagged not claimed): `ls -l` on the gguf → **10,333,691,040 B** vs `/v1/models` `meta.size` → **10,327,717,888 B** (Δ 5,973,152 B). I did not md5 a 10 GB file. Likely GGUF trailer/alignment padding omitted from `meta.size`; cause not proven.

## 6. Proposal for the L1 (a repo edit — I did not apply it)

Replace the SCORECARD.md:60 ceiling tail ("the served-model surface (`:34113` flags: `--cont-batching`, `-np`) is documented from behaviour, never from the process cmdline") with a process-level pin, e.g.:

> the served-model surface is pinned at process level: pid 1299 argv == `~/.config/systemd/user/qwen-coder.service` `ExecStart` (41 tokens, `EXACT_MATCH True`), carrying `--port 34113 --host 127.0.0.1 --ctx-size 16384 --cont-batching --parallel 2 --kv-unified --cache-type-k q4_0 --cache-type-v q4_0`, re-checkable with `tr '\0' ' ' < /proc/$(pgrep -f 'llama-server.*34113')/cmdline`.

And add to PROVINCE.md:14's surface cell: `--parallel 2` (shorthand `-np`), `--cont-batching`, `--kv-unified`, KV `q4_0` — per the live argv. Caveat for the L1: a grader that pins this from the *filesystem* should pin `qwen-coder.service` (a committed copy or an md5), **not** `/proc`, since /proc is host-state the hermetic grader must not depend on; my in-repo read-only rule means I did not add it.

## 7. Raw command log (all read-only, cwd /tmp/kengaku-r10 unless noted)

```
curl -s -m 5 http://127.0.0.1:34113/v1/models                      # 200, 872 B
curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health   # 200
curl -s -m 5 http://127.0.0.1:34113/slots                          # 200, 2 slots
curl -s -m 5 http://127.0.0.1:34113/props                          # 200, total_slots=2
pgrep -af llama; pgrep -af server; ss -ltnp | grep 34113           # pid 1299 all three
tr '\0' ' ' < /proc/1299/cmdline                                   # 41 tokens
ls -l /proc/1299/exe; ps -o pid,ppid,user,lstart -p 1299
timeout 5 /home/vgpnk/.local/bin/llama-server --version            # 0.3.0-dev d7bd3bf
systemctl --user status qwen-coder --no-pager
python3 (shlex diff unit ExecStart vs /proc/1299/cmdline)          # EXACT_MATCH True
```
Files kept: `/tmp/kengaku-r10/models-34113.json`, `slots.json`, `props.json`.
