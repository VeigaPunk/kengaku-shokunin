# r12 endpoint + host freshness — ScoutEndpointFresh (scout)

**Agent:** ScoutEndpointFresh — role: scout, freshness re-verification.
**Task restatement:** re-measure, before the r12 run, every host surface round 12
touches (served endpoint identity, `llama-server` process pin, r10's on-disk-vs-
`meta.size` open item, `~/Projects/bounties/` route telemetry, `~/bench-arena/`,
`llm-wiki`, host capacity), each with the verbatim command and its real output,
and land a per-surface `DRIFT`/`NO-DRIFT` verdict plus a run `GO`/`NO-GO`.

**Session:** all commands run 2026-09-29T00:44Z–00:58Z (host clock `-03`, so
21:44–21:58 local), from repo root `/home/vgpnk/projects/shokunin/kengaku-shokunin`
(HEAD unchanged during the session; no repo file was written except this one).
**Endpoint traffic generated: exactly two `GET`s** (`/v1/models`, `/health`) — no
`chat/completions`, no `/metrics`, no `/props`, ever. No 10 GB hash run.
**Determinism:** every script below is stdlib-only Python 3; all reported numbers
are integer accumulations and a `sort_keys=True` JSON canonicalisation, so
`PYTHONHASHSEED` is not observable in any output (no set/dict-order-dependent
arithmetic). No third-party imports.

**Committed reference compared against:** first line of
`corpus/evidence/round11-power/results-r11.jsonl` (the `cell:"descriptors"`
record) and `PROVINCE.md` §Surfaces (`PROVINCE.md:8-20`, process-level pin in
`:15`).

---

## 1. Endpoint identity — `GET /v1/models` + `GET /health`

### 1.1 Commands

```
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sS -o /tmp/r12f-models.json -w 'HTTP_STATUS=%{http_code} bytes=%{size_download} time=%{time_total}\n' http://127.0.0.1:34113/v1/models
curl -sS -i http://127.0.0.1:34113/health | head -20
```

### 1.2 Output (verbatim)

```
2026-09-29T00:44:25Z
HTTP_STATUS=200 bytes=872 time=0.009073
--- /health ---
HTTP/1.1 200 OK
Server: llama.cpp
Access-Control-Allow-Origin: http://127.0.0.1:8080
Content-Type: application/json; charset=utf-8
Content-Length: 15
Keep-Alive: timeout=5, max=100

{"status":"ok"}
```

`GET /v1/models` → **HTTP 200, 872 body bytes**; `GET /health` → **HTTP 200**,
body `{"status":"ok"}` (15 B, matching the declared `Content-Length`).

### 1.3 The served model id, byte-for-byte vs the r11 `descriptors` record

Command (stdlib; compares live capture to the committed r11 first line):

```
python3 - <<'PY'
import json, hashlib
live = json.load(open("/tmp/r12f-models.json"))
r11  = json.loads(open("corpus/evidence/round11-power/results-r11.jsonl").readline())["models_json"]
lid, rid = live["data"][0]["id"], r11["data"][0]["id"]
print("live id :", lid); print("r11  id :", rid); print("ID EXACT_MATCH:", lid == rid)
print("models[0].name equal:", live["models"][0]["name"] == r11["models"][0]["name"])
print("meta live:", live["data"][0]["meta"]); print("meta r11 :", r11["data"][0]["meta"])
print("meta equal:", live["data"][0]["meta"] == r11["data"][0]["meta"])
print("data[0] equal:", live["data"][0] == r11["data"][0])
print("models[] equal:", live["models"] == r11["models"])
PY
```

Output:

```
live id : /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
r11  id : /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
ID EXACT_MATCH: True
models[0].name equal: True
meta live: {'vocab_type': True, 'n_vocab': 151936, 'n_ctx': 16384, 'n_ctx_train': 262144, 'n_embd': 2048, 'n_params': 30532122624, 'size': 10327717888, 'ftype': 'IQ2_XXS - 2.0625 bpw'}
meta r11 : {'vocab_type': True, 'n_vocab': 151936, 'n_ctx': 16384, 'n_ctx_train': 262144, 'n_embd': 2048, 'n_params': 30532122624, 'size': 10327717888, 'ftype': 'IQ2_XXS - 2.0625 bpw'}
meta equal: True
data[0] equal: False
models[] equal: True
```

**Verdict on identity: `EXACT_MATCH`, byte-for-byte**, on `data[0].id`,
`data[0].aliases[0]`, `models[0].name`, the whole `models[]` array, and the whole
`meta` object (`n_vocab` 151936, `n_ctx` 16384, `n_ctx_train` 262144, `n_params`
30532122624, `size` 10327717888, `ftype` `IQ2_XXS - 2.0625 bpw`).

Found while comparing: `data[0]` is **not** whole-object equal, and the *only*
differing key is `created`. Measured values:

```
r10 capture corpus/evidence/round10-fleet/models-34113.json : created=1790633228 -> 2026-09-28T22:07:08Z
r11 descriptors (committed)                                 : created=1790638137 -> 2026-09-28T23:28:57Z
this session's /v1/models fetch (ts 2026-09-29T00:44:25Z)    : created=1790642665 -> 2026-09-29T00:44:25Z
```

`created` equals the **request time** to the second in both cases where a
timestamp was recorded in-band (r11's `request_ts` `23:28:57Z` ↔ `created`
`1790638137` → `0 s` delta; this session's `00:44:25Z` ↔ `1790642665` → `0 s`
delta). It is not the process start (process started 2026-09-28T05:55:28Z,
epoch ≈ 1790574928) and not the model file mtime (2026-08-29). Therefore a
whole-body byte/hash comparison of `/v1/models` across rounds **must** expect to
fail on `created`; identity comparison must be restricted to `id`/`aliases`/
`models`/`meta` (or mask `created`). `[INFERENCE-moderate]` on the *mechanism*
("server stamps now"); the two 1-second-exact coincidences are the evidence and
no upstream source line for that field is cited here.

### 1.4 Verbatim body of the live `/v1/models` capture (872 B, all of it)

The capture itself lived in `/tmp`; it is reproduced here in full so the number
is reproducible from this committed artifact. Integrity of the copy below:

```
md5    cd90917cebd85cf9102bb97ec3f5fa50
sha256 9267e1eecc9557958655ce41642daf70fae4ef2f00d4c60abad3d3f6582009c2
wc -c  872
```

```
{"models":[{"name":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","model":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","modified_at":"","size":"","digest":"","type":"model","description":"","tags":[""],"capabilities":["completion"],"parameters":"","details":{"parent_model":"","format":"gguf","family":"","families":[""],"parameter_size":"","quantization_level":""}}],"object":"list","data":[{"id":"/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf","aliases":["/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf"],"tags":[],"object":"model","created":1790642665,"owned_by":"llamacpp","meta":{"vocab_type":true,"n_vocab":151936,"n_ctx":16384,"n_ctx_train":262144,"n_embd":2048,"n_params":30532122624,"size":10327717888,"ftype":"IQ2_XXS - 2.0625 bpw"}}]}
```

Note `models[0].size` is the empty string `""` (unchanged from r11/r10) — the
non-empty size lives only in `data[0].meta.size`.

---

## 2. Process pin — `llama-server` pid, argv, unit, listener

### 2.1 Commands and outputs

```
pgrep -f llama-server ; pgrep -af llama-server
```

```
1299
1299 /home/vgpnk/.local/bin/llama-server --chat-template-file /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja --no-context-shift --no-cors-credentials --cors-origins http://127.0.0.1:8080 --host 127.0.0.1 --jinja --metrics --port 34113 --slots --no-webui --no-webui-mcp-proxy --alias /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --no-agent --ctx-size 16384 --cont-batching --cache-type-k q4_0 --cache-type-v q4_0 --flash-attn on --fit off --kv-unified --model /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --n-gpu-layers 999 --parallel 2 --split-mode none --timeout 900
```

```
ps -o pid,ppid,lstart,etime,rss,vsz,nlwp -p 1299
```

```
    PID    PPID STARTED                  ELAPSED    RSS      VSZ NLWP
   1299    1225 Mon Sep 28 02:55:28 2026 18:48:56 68956 69152016   40
```

```
tr '\0' '\n' < /proc/1299/cmdline | cat -n
```

(41 tokens, verbatim, output truncated here only in the sense that it is the
entire file — nothing omitted):

```
     1	/home/vgpnk/.local/bin/llama-server
     2	--chat-template-file
     3	/home/vgpnk/.config/llama/qwen-coder-godspeed.jinja
     4	--no-context-shift
     5	--no-cors-credentials
     6	--cors-origins
     7	http://127.0.0.1:8080
     8	--host
     9	127.0.0.1
    10	--jinja
    11	--metrics
    12	--port
    13	34113
    14	--slots
    15	--no-webui
    16	--no-webui-mcp-proxy
    17	--alias
    18	/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
    19	--no-agent
    20	--ctx-size
    21	16384
    22	--cont-batching
    23	--cache-type-k
    24	q4_0
    25	--cache-type-v
    26	q4_0
    27	--flash-attn
    28	on
    29	--fit
    30	off
    31	--kv-unified
    32	--model
    33	/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
    34	--n-gpu-layers
    35	999
    36	--parallel
    37	2
    38	--split-mode
    39	none
    40	--timeout
    41	900
```

`/proc/1299/cmdline` raw byte string: **632 bytes**, **41 tokens**, md5 of the raw
NUL-separated bytes `e6642361e60173c15705a8108e547efa`.

### 2.2 Token-by-token diff vs the r11 `descriptors.server.argv`

```
python3 - <<'PY'
import json
toks = [t.decode() for t in open("/proc/1299/cmdline","rb").read().split(b"\0") if t]
argv11 = json.loads(open("corpus/evidence/round11-power/results-r11.jsonl").readline())["server"]["argv"]
print("live tokens:", len(toks), "r11 tokens:", len(argv11))
if toks == argv11:
    print("ARGV DIFF: EXACT_MATCH (41/41 tokens identical, order included)")
else:
    print("ARGV DIFF: MISMATCH")
    for i in range(max(len(toks), len(argv11))):
        a = toks[i] if i < len(toks) else "<missing>"; b = argv11[i] if i < len(argv11) else "<missing>"
        if a != b: print(f"  idx {i}: live={a!r} r11={b!r}")
PY
```

Output:

```
live tokens: 41 r11 tokens: 41
ARGV DIFF: EXACT_MATCH (41/41 tokens identical, order included)
```

**`EXACT_MATCH` — 0 differing tokens, same order, same length (41).** Every
r10/r11-flagged flag is present and unchanged: `--parallel 2` (no literal `-np`),
`--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k q4_0`,
`--cache-type-v q4_0`, `--flash-attn on`, `--no-context-shift`,
`--n-gpu-layers 999`, `--split-mode none`, `--timeout 900`,
`--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja`, plus
`--no-webui-mcp-proxy` / `--no-agent` / `--fit off` (newer flags, identical in
both).

### 2.3 systemd unit (read-only) and its `ExecStart`

```
systemctl --user cat qwen-coder.service
```

```
# /home/vgpnk/.config/systemd/user/qwen-coder.service
[Unit]
Description=THE TICK Qwen3-Coder-30B-A3B-Instruct 2x16K
After=network.target
StartLimitIntervalSec=300
StartLimitBurst=3
[Service]
Type=simple
Restart=on-failure
RestartSec=15
Environment="PATH=/home/vgpnk/.local/bin:/usr/local/bin:/usr/bin"
Environment="CUDA_VISIBLE_DEVICES=0"
ExecStart=/home/vgpnk/.local/bin/llama-server \
  --chat-template-file /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja \
  --no-context-shift --no-cors-credentials \
  --cors-origins http://127.0.0.1:8080 \
  --host 127.0.0.1 --jinja --metrics --port 34113 --slots \
  --no-webui --no-webui-mcp-proxy \
  --alias /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf \
  --no-agent --ctx-size 16384 --cont-batching \
  --cache-type-k q4_0 --cache-type-v q4_0 --flash-attn on --fit off --kv-unified \
  --model /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf \
  --n-gpu-layers 999 --parallel 2 --split-mode none --timeout 900
[Install]
WantedBy=default.target
```

Rendered by the manager (`systemctl --user show -p ExecStart -p ExecMainPID -p
ActiveEnterTimestamp qwen-coder.service`, `argv[]` field):

```
ExecMainPID=1299
ActiveEnterTimestamp=Mon 2026-09-28 02:55:28 -03
ExecStart={ path=/home/vgpnk/.local/bin/llama-server ; argv[]=/home/vgpnk/.local/bin/llama-server --chat-template-file /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja --no-context-shift --no-cors-credentials --cors-origins http://127.0.0.1:8080 --host 127.0.0.1 --jinja --metrics --port 34113 --slots --no-webui --no-webui-mcp-proxy --alias /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --no-agent --ctx-size 16384 --cont-batching --cache-type-k q4_0 --cache-type-v q4_0 --flash-attn on --fit off --kv-unified --model /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf --n-gpu-layers 999 --parallel 2 --split-mode none --timeout 900 ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=… (tail of the ExecStart structure field elided by the manager's own rendering)
```

Token-by-token diff, unit `argv[]` vs `/proc/1299/cmdline` **and** vs the r11
`descriptors.server.argv` (one script, three-way):

```
unit argv tokens: 41 | /proc tokens: 41
EXACT_MATCH: True
unit == r11 descriptors argv: True
```

**Three-way `EXACT_MATCH`: unit `ExecStart` == live `/proc/1299/cmdline` == r11
`descriptors.server.argv`, 41 tokens each.** The unit is `enabled`, `active
(running) since Mon 2026-09-28 02:55:28 -03` (18 h 50 min at measurement), unit
file mtime `2026-09-08 20:43:13 -0300` (unchanged since before r11); template
`/home/vgpnk/.config/llama/qwen-coder-godspeed.jinja`, 6818 B, mtime
`2026-08-29 03:35:28 -0300`.

### 2.4 Listener ownership for :34113

```
ss -ltnp | grep -E '34113|State'
```

```
State  Recv-Q Send-Q               Local Address:Port  Peer Address:Port Process
LISTEN 0      512                      127.0.0.1:34113      0.0.0.0:*    users:(("llama-server",pid=1299,fd=16))
```

**Exactly one listener on :34113, owned by `llama-server` pid 1299 (fd 16),
bound to `127.0.0.1` only** — no `0.0.0.0`, no `[::1]` (the process's own logged
CORS origin is `http://127.0.0.1:8080`, matching `--cors-origins`).

---

## 3. Round-10 open item closed — on-disk gguf vs `/v1/models` `meta.size`

### 3.1 Re-measurement (the brief's core requirement)

```
stat -c %s /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
stat -c 'size=%s mtime=%y ctime=%z blocks=%b blksize=%B' /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf
```

```
10333691040
size=10333691040 mtime=2026-08-29 02:39:38.068184831 -0300 ctime=2026-08-29 02:39:38.097320438 -0300 blocks=20182992 blksize=512
```

Served `meta.size` (live, §1.3): **10 327 717 888**.

| quantity | bytes |
|---|---:|
| on disk (`stat -c %s`) | **10 333 691 040** |
| `/v1/models` `meta.size` | **10 327 717 888** |
| Δ | **5 973 152** |

**The Δ persists, byte-for-byte the same 5 973 152 B that round 10 recorded**
(`corpus/evidence/round10-fleet/r10-scout-endpoint.md:78`: "`ls -l` on the gguf →
**10,333,691,040 B** vs `/v1/models` `meta.size` → **10,327,717,888 B** (Δ
5,973,152 B) … cause not proven"). The file is also unchanged in mtime/ctime
(2026-08-29 02:39:38), i.e. the artifact itself did not move between r10 and now.

### 3.2 The Δ, explained — measured, not inferred (no 10 GB hash)

The GGUF header region is ~5.7 MB, so the whole header can be parsed in
milliseconds without ever touching tensor data. Script (reproduce verbatim;
stdlib only; reads the file strictly sequentially and stops at the end of the
tensor-info table, i.e. **never reads a payload byte**):

```python
import struct, os
PATH = "/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf"
f = open(PATH, "rb")
def u32(): return struct.unpack("<I", f.read(4))[0]
def u64(): return struct.unpack("<Q", f.read(8))[0]
def s64():
    n = u64(); return f.read(n)
SIZ = {0:1,1:1,2:2,3:2,4:4,5:4,6:4,7:1,10:8,11:8,12:8}   # gguf_metadata_value_type fixed widths
def val(t):
    if t in SIZ: return f.read(SIZ[t])
    if t == 8: return s64()                              # STRING
    if t == 9:                                           # ARRAY
        et = u32(); n = u64()
        if et == 8: return sum(len(s64()) for _ in range(n))   # ARRAY of STRING
        if et == 9:                                      # ARRAY of ARRAY
            for _ in range(n):
                it = u32(); m = u64()
                if it == 8: [s64() for _ in range(m)]
                else: f.read(SIZ[it]*m)
            return None
        f.read(SIZ[et]*n); return None
    raise ValueError(t)
assert f.read(4) == b"GGUF"
ver = u32(); n_tensors = u64(); n_kv = u64(); start_kv = f.tell()
kvd = {}
for _ in range(n_kv):
    k = s64().decode("utf-8", "replace"); t = u32(); kvd[k] = val(t)
kv_bytes = f.tell() - start_kv
start_ti = f.tell()
# ggml_type -> (block_size, type_size); IQ2_XXS = (256, 66) -> 2.0625 bpw
BS = {0:(1,4),2:(32,18),3:(32,20),6:(32,22),7:(32,24),8:(32,34),9:(32,36),10:(256,84),
      11:(256,110),12:(256,144),13:(256,176),14:(256,210),15:(256,292),16:(256,66),
      17:(256,74),18:(256,98),19:(256,50),20:(32,18),21:(256,110),22:(256,82),
      23:(256,136),24:(1,1),25:(1,2),26:(1,4),27:(1,8),28:(1,8),29:(256,56),30:(1,2)}
tot_raw = 0; pad = 0; padn = 0; npar = 0
for _ in range(n_tensors):
    nm = s64(); nd = u32(); ne = [u64() for _ in range(nd)]; ty = u32(); off = u64()
    p = 1
    for d in ne: p *= d
    npar += p
    blk, tsz = BS[ty]; raw = (ne[0]//blk)*tsz
    for d in ne[1:]: raw *= d
    tot_raw += raw; q = (-raw) % 32; pad += q; padn += (q > 0)
ti_bytes = f.tell() - start_ti
data_offset = (-f.tell()) % 32 + f.tell()
print("version:", ver, "n_tensors:", n_tensors, "n_kv:", n_kv)
print("header bytes        :", start_kv)
print("KV region bytes     :", kv_bytes)
print("tensor-info bytes   :", ti_bytes)
print("align pad bytes     :", data_offset - f.tell())
print("data_offset         :", data_offset)
print("sum raw tensor bytes:", tot_raw, "| per-tensor align pad:", pad, f"({padn} tensors)")
print("sum params          :", npar)
print("disk size           :", os.stat(PATH).st_size)
print("CHECK data_offset+sum_raw == disk :", data_offset + tot_raw == os.stat(PATH).st_size)
print("CHECK sum_raw == meta.size        :", tot_raw == 10327717888)
print("CHECK sum_params == meta.n_params :", npar == 30532122624)
print("tokenizer.ggml.tokens payload bytes:", kvd.get("tokenizer.ggml.tokens"))
print("tokenizer.ggml.merges payload bytes:", kvd.get("tokenizer.ggml.merges"))
```

Output (verbatim):

```
version: 3 n_tensors: 579 n_kv: 44
header bytes        : 24
KV region bytes     : 5936743
tensor-info bytes   : 36376
align pad bytes     : 9
data_offset         : 5973152
sum raw tensor bytes: 10327717888 | per-tensor align pad: 0 (0 tensors)
sum params          : 30532122624
disk size           : 10333691040
CHECK data_offset+sum_raw == disk : True
CHECK sum_raw == meta.size        : True
CHECK sum_params == meta.n_params : True
tokenizer.ggml.tokens payload bytes: (1372760, 151936)
tokenizer.ggml.merges payload bytes: (1520452, 151387)
```

**The Δ is fully accounted for, residual 0.**

- `data_offset` = **5 973 152** = 24 (header) + 5 936 743 (KV metadata) + 36 376
  (579 tensor-info entries) + 9 (align to 32 B). The GGUF tensor-data region
  starts there.
- Σ raw tensor bytes = **10 327 717 888**, which is **exactly** the served
  `meta.size`. (Per-tensor 32-B alignment contributes **0** pad bytes here — every
  tensor's `ggml_nbytes` is already a multiple of 32 — so the two sizes are equal.)
- disk = `data_offset` + Σ tensors = 5 973 152 + 10 327 717 888 = **10 333 691 040** — the
  `stat` size, exactly, and we can state it as an identity because the two
  independently obtained numbers (stat, server) reproduce it with residual 0.
- Cross-check on the same parse: Σ of `ne` products = **30 532 122 624** = served
  `n_params`, exactly.
- Where the 5 973 152 B go: the GGUF KV region is **5 936 743 B**, dominated by the
  tokenizer blobs — `tokenizer.ggml.tokens` = 1 372 760 B of payload across
  151 936 strings, `tokenizer.ggml.merges` = 1 520 452 B across 151 387 strings
  (2 893 212 B ≈ 2.76 MiB of the 5.66 MiB KV region), plus the tensor-info table
  (36 376 B) and the 9-byte alignment gap.

**Semantics of `meta.size` (upstream, fetched 2026-09-29, `HTTP 200`):**

- `https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-model.cpp`
  (`HTTP 200`, 158 953 B): `uint64_t llama_model_size(const llama_model * model)
  { return model->size(); }` at `:3227-3229`; `llama_model::size()` returns
  `pimpl->n_bytes` at `:1975-1976`; `pimpl->n_bytes = ml.n_bytes` at `:1292` and
  `:1477`; `llama_model_n_params` at `:3250`.
- `https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-model-loader.cpp`
  (`HTTP 200`, 78 376 B): `n_bytes += ggml_nbytes(cur);` at `:592`, `:658`,
  `:709` — i.e. `meta.size` is the **sum of tensor payload bytes**, not the file
  size; and that same accumulator is printed as `file size = %.2f MiB …` at
  `:1806-1809`, which is exactly the naming that made r10's Δ look unexplained.

`[INFERENCE-light]` on the exact upstream line numbers (fetched from `master`
without a commit pin; the fetched bytes are ephemeral, the line numbers are as
observed in that fetch). The load-bearing claim — `meta.size` is the tensor-byte
sum, and disk = `data_offset` + that sum — is **measured**, not inferred: it is
the residual-0 identity above plus the two exact matches against server-reported
integers.

**Verdict: `NO-DRIFT` on the artifact** (same 10 333 691 040 B, same mtime), and
the r10 open item is **CLOSED by arithmetic** — what would have been needed to
explain it (a 10 GB hash) is not needed; a 5.7 MB header parse suffices. The r10
note's own guess ("Likely GGUF trailer/alignment padding omitted from
`meta.size`") is half right: it is the **leading** metadata region (`data_offset`),
not a trailer, and tensor alignment happens to contribute zero here.

---

## 4. Route telemetry surface — `~/Projects/bounties/`

```
test -d ~/Projects/bounties && echo PRESENT || echo ABSENT
ls -la ~/Projects/bounties
```

```
ABSENT
ls: cannot access '/home/vgpnk/Projects/bounties': No such file or directory
```

The brief's prescribed sweep, exactly:

```
find ~ -maxdepth 4 -name 'telemetry.jsonl' -path '*ledger*'
```

```
(no output)   exit=0
```

Widened sweeps (stderr suppressed; `-xdev` keeps it on the `/home` device):

```
find ~ -xdev -name 'telemetry.jsonl' -path '*ledger*'        -> (no output)
find ~ -xdev -name 'telemetry.jsonl' -printf '%s %TY-%Tm-%Td %TH:%TM %p\n'
find ~ -xdev -type d -name 'bounties*'
```

```
4680 2026-09-20 21:07 /home/vgpnk/Projects/webzites/reports/exec-speedrun/telemetry.jsonl
8267 2026-09-20 21:49 /home/vgpnk/Projects/webzites/reports/speedrun-dry/telemetry.jsonl
1119225 2026-09-16 18:52 /home/vgpnk/.bailian/telemetry.jsonl
--- bounties* dirs ---
/home/vgpnk/.grok/memory/bounties-17da6cb9
```

Named-match triage: the three `telemetry.jsonl` files above are **not** route
telemetry — two are `webzites` benchmark reports, one is `~/.bailian` (the
client CLI telemetry already listed separately in `PROVINCE.md:16`), and **none
sits under a `ledger/` directory**. `~/.grok/memory/bounties-17da6cb9/` is a
grok memory index (`MEMORY.md` 106 B + `index.sqlite` 77 824 B, mtime 2026-09-05),
not the `bounties` project tree and not a ledger. `~/Projects/` contains no
`bounties` entry (checked `ls -la ~/Projects/`; 30+ entries, none named
`bounties`). The `.ufo/scopes/*/ledger/` directories that exist under
`~/nc8r6-ExLibRouteCheck/` hold `ledger.json`/`ledger.archive.*.json` only — no
`telemetry.jsonl` (checked one representative listing).

Caveat for honesty: the unbounded `find`s exit **1**, not 0 — one unreadable
directory under `~/nc8r6-ExLibRouteCheck/.ufo/scopes/tmp-r35-eacces-1488153`
(`find` reports `Permission denied (os error 13)`; the name suggests a deliberate
EACCES fixture). Everything else on the `/home` device was traversed.

**Verdict: `ABSENT` (unchanged) — still no drift *carrier*, so PROVINCE's
coverage cap on the route-telemetry surface stays.** The r11 finding ("whole
`~/Projects/bounties/` tree gone, no relocation found") is reproduced: no
relocation exists anywhere under `~` on this device.

---

## 5. `~/bench-arena/` and `~/Projects/webzites/repos/llm-wiki`

### 5.1 bench-arena — present, frozen

```
ls -la ~/bench-arena
```

```
total 76
drwxr-xr-x 1 vgpnk vgpnk   296 Aug 29 03:58 .
drwx------ 1 vgpnk vgpnk  4590 Sep 27 20:07 ..
-rw-r--r-- 1 vgpnk vgpnk 43187 Aug 29 03:15 generate_new_domains.py
-rwxr-xr-x 1 vgpnk vgpnk  1199 Aug 29 03:29 grade.sh
drwxr-xr-x 1 vgpnk vgpnk    54 Aug 29 03:27 graded
-rwxr-xr-x 1 vgpnk vgpnk  4379 Aug 29 03:25 loop.sh
drwxr-xr-x 1 vgpnk vgpnk    54 Aug 29 03:25 out
-rw-r--r-- 1 vgpnk vgpnk  1017 Aug 29 03:15 report-grok45.csv
-rw-r--r-- 1 vgpnk vgpnk  3388 Aug 29 03:30 report-qwenlocal-v2.v2.csv
-rw-r--r-- 1 vgpnk vgpnk  1017 Aug 29 03:06 report-qwenlocal.csv
drwxr-xr-x 1 vgpnk vgpnk  4472 Aug 29 03:15 staging
drwxr-xr-x 1 vgpnk vgpnk  1126 Aug 29 02:56 tasks
-rw-r--r-- 1 vgpnk vgpnk  4501 Aug 29 03:30 telemetry-qwenlocal-v2.csv
```

```
find ~/bench-arena -newermt '2026-09-28 20:00' -type f | wc -l
```

```
0
```

Newest files (top 10 by mtime, `find ... -printf '%T@ …' | sort -rn`):

```
1787985059 2026-08-29 03:30:59 /home/vgpnk/bench-arena/telemetry-qwenlocal-v2.csv
1787985055 2026-08-29 03:30:55 /home/vgpnk/bench-arena/report-qwenlocal-v2.v2.csv
1787985055 2026-08-29 03:30:55 /home/vgpnk/bench-arena/graded/qwenlocal-v2/33-metaclass-shadowing.sol
1787985055 2026-08-29 03:30:55 /home/vgpnk/bench-arena/graded/qwenlocal-v2/32-loop-closures.sol
   … (8 more, all 2026-08-29 03:29–03:30)
```

**Present, frozen since 2026-08-29 03:30:59** — **0** files newer than the
2026-09-28 20:00 cutoff. Every `PROVINCE.md:13` row member (`tasks/`, `grade.sh`,
`loop.sh`, `report-grok45.csv`, `report-qwenlocal*.csv`,
`telemetry-qwenlocal-v2.csv`) resolves. **Verdict: `NO-DRIFT`.**

### 5.2 llm-wiki — resolves, no eval-relevant churn

```
test -d ~/Projects/webzites/repos/llm-wiki && echo IS_DIR; readlink -f ~/Projects/webzites/repos/llm-wiki
for p in wiki/ai/agents-and-engineering wiki/karpathy wiki/ai/foundations wiki/ai/alignment-and-training wiki/ai/books wiki/ai/scaling-and-forecasting Home.md raw; do printf '%-45s ' "$p"; test -e ~/Projects/webzites/repos/llm-wiki/$p && echo PRESENT || echo ABSENT; done
find ~/Projects/webzites/repos/llm-wiki -newermt '2026-09-28 20:00' -type f | wc -l
```

```
IS_DIR
/home/vgpnk/Projects/webzites/repos/llm-wiki
wiki/ai/agents-and-engineering                PRESENT
wiki/karpathy                                 PRESENT
wiki/ai/foundations                           PRESENT
wiki/ai/alignment-and-training                PRESENT
wiki/ai/books                                 PRESENT
wiki/ai/scaling-and-forecasting               PRESENT
Home.md                                       PRESENT
raw                                           PRESENT
0
```

Newest 12 entries (mtime, descending):

```
2026-09-28 15:58 /home/vgpnk/Projects/webzites/repos/llm-wiki/.git/index
2026-09-20 23:11 /home/vgpnk/Projects/webzites/repos/llm-wiki/.git/FETCH_HEAD
2026-09-20 22:50 …/wiki/psychology/intelligence-analysis/structured-analytic-techniques.md
2026-09-20 22:50 …/wiki/psychology/intelligence-analysis/heuer-psychology-of-intelligence.md
   … (9 more, all 2026-09-20 22:50, all under wiki/psychology/)
```

All eight `PROVINCE.md:12` eval-relevant paths resolve; **0** files newer than the
cutoff. The only sub-cutoff entry is `.git/index` (2026-09-28 15:58 — a git
operation, not content), and the newest *content* is 2026-09-20 (psychology pages,
outside the eval-relevant subtrees). The `~/wikillm/llm-wiki` non-existence claim
in `PROVINCE.md:12` was not re-tested (not in the brief). **Verdict: `NO-DRIFT`.**

---

## 6. Host capacity for a ~4 000-request sequential run

```
free -m ; free -b ; cat /proc/loadavg ; uptime
df -h /home/vgpnk/projects/shokunin/kengaku-shokunin ; df -B1 /home/vgpnk/projects/shokunin/kengaku-shokunin
findmnt -no SOURCE,FSTYPE,SIZE,AVAIL,TARGET /home ; findmnt -no SOURCE,FSTYPE,SIZE,AVAIL,TARGET /scratch
swapon --show
nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,driver_version --format=csv
ss -tnp | grep -E '34113|State'
```

Output (verbatim):

```
               total        used        free      shared  buff/cache   available
Mem:           30978       21064         327         274       10323        9913
Swap:          54212       20630       33582

2.64 6.29 22.94 8/4057 2967085
 21:45:04 up 18:49,  1 user,  load average: 2.64, 6.29, 22.94

Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  930G  241G  559G  31% /home

/dev/nvme1n1p2[/@home] btrfs 929.5G 559.9G /home
/dev/nvme0n1p1 btrfs 931.5G 860.3G /scratch

NAME           TYPE      SIZE  USED PRIO
/swap/swapfile file     30.3G    3G    0
/dev/zram0     partition 22.7G 21.4G  100

name, memory.total [MiB], memory.used [MiB], memory.free [MiB], utilization.gpu [%], temperature.gpu, driver_version
NVIDIA GeForce RTX 5070, 12227 MiB, 11151 MiB, 641 MiB, 4 %, 40, 610.57.04

State Recv-Q Send-Q               Local Address:Port  Peer Address:Port Process
LISTEN 0      512                      127.0.0.1:34113      0.0.0.0:*    users:(("llama-server",pid=1299,fd=16))
```

- **RAM:** 32 483 405 824 B total (30 978 MiB), **12 207 316 992 B available**
  (≈11.4 GiB), `used` 20 276 088 832 B; `free` is only 447 029 248 B but
  `buff/cache` holds 12 661 841 920 B, so the allocatable figure is the
  `available` column: **≈11.4 GiB**. Swap: 56 846 331 904 B total (30.3 G
  swapfile + 22.7 G zram), **26 200 846 336 B in use** (≈21.4 GiB of that on
  zram — compressed RAM, not disk).
- **GPU:** 1× RTX 5070, **12 227 MiB total, 11 151 MiB used, 641 MiB free**, 4 %
  util, 40 °C, driver 610.57.04. `nvidia-smi` process table attributes
  **10 522 MiB** to llama-server pid 1299 plus **≈350 MiB** of desktop
  compositors (Hyprland 187 + walker 95 + 3× alacritty 21 + Xwayland 3 MiB); the
  remaining ≈280 MiB is not attributed in the truncated process table — i.e. the
  model + q4_0 KV cache for `--parallel 2` is
  already resident; a run reusing this server consumes **no new VRAM**.
- **Load:** `2.64 6.29 22.94`, 8 runnable of 4 057 threads; `up 18:49`; the top
  CPU consumers are fleet siblings (`MainThread` 42 %, several `omp` 12–24 %).
- **Disk:** repo filesystem is `/dev/nvme1n1p2[/@home]` (btrfs), **559.9 G
  available** of 929.5 G (31 % used); the repo tree is 3.6 M.
  `/scratch` (where the model lives) has 860.3 G available. No disk pressure.
- **Other clients on :34113: none.** `ss -tnp` shows only the LISTEN line —
  **0 established connections** to `:34113`, and
  `ss -tan state established | grep -c 34113` → `0`. Corroborated by the unit's
  journal: `journalctl --user -u qwen-coder.service --since '45 min ago'` →
  `-- No entries --`, and the last logged slot activity is
  `2026-09-28T20:33:17-03:00` (= `23:33:17Z`, the tail of the r11 run) —
  **≈1 h 12 min idle** at measurement. Unrelated established sockets exist
  (omp/`127.0.0.1:8790`, assorted outbound TLS) but none touch the endpoint.

---

## 7. Verdicts

| # | Surface | Verdict | Evidence |
|---|---|---|---|
| 1 | `/v1/models` + `/health` identity | **NO-DRIFT** | id/aliases/`models[]`/`meta` byte-identical to r11 `descriptors`; `HTTP 200`/`200`; only `created` differs, and it equals the request time (`0 s` delta twice) |
| 2 | `llama-server` process pin | **NO-DRIFT** | pid **1299** unchanged since 2026-09-28 02:55:28; `/proc/1299/cmdline` **41/41 `EXACT_MATCH`** vs r11 `server.argv` *and* vs unit `ExecStart`; single listener `127.0.0.1:34113` owned by pid 1299 (fd 16) |
| 3 | on-disk gguf vs `meta.size` | **NO-DRIFT (artifact)**; Δ **persists** but is **now explained with residual 0** | disk 10 333 691 040 (mtime 2026-08-29 unchanged) = `data_offset` 5 973 152 + Σ tensors 10 327 717 888 (== `meta.size`); Σ `ne` = 30 532 122 624 (== `n_params`); r10 open item closed without a 10 GB hash |
| 4 | route telemetry `~/Projects/bounties/ledger/telemetry.jsonl` | **ABSENT → stays absent** | `test -d` ABSENT; prescribed sweep empty; no `ledger/telemetry.jsonl`, no `bounties` tree, no relocation anywhere under `~` on the `/home` device; coverage cap stays |
| 5 | `~/bench-arena/` | **NO-DRIFT** | present, 0 files newer than 2026-09-28 20:00, newest 2026-08-29 03:30:59 |
| 5b | `~/Projects/webzites/repos/llm-wiki` | **NO-DRIFT** | resolves; all 8 eval-relevant subpaths present; 0 files newer than cutoff; newest content 2026-09-20 (`.git/index` 2026-09-28 15:58 is a git op, not content) |
| 6 | host capacity (4 000-request sequential run) | **ADEQUATE, with 2 conditions** | RAM available ≈11.4 GiB; disk 559.9 G free on the repo fs; endpoint idle, 0 other clients; GPU 641 MiB free but model already resident |

### `GO / NO-GO for the r12 run`

**GO.** Reasons, in descending weight:

1. **Identity is bit-stable.** Model id, aliases, `models[]`, and the whole `meta`
   block are byte-identical to the r11 `descriptors` record; `n_ctx=16384`,
   `n_params=30532122624`, `size=10327717888` all match.
2. **The stack pin holds at the strongest level available**: `/proc` cmdline ==
   systemd `ExecStart` == r11 pre-run argv, 41/41 tokens, including both
   preregistration flags (`--cache-type-k/v q4_0`, `--kv-unified`, `--parallel 2`)
   and the custom `qwen-coder-godspeed.jinja` template. The **same process** (pid
   1299, up 18 h 50 m) served r11, so the run reproduces the r11 unit exactly
   rather than a restarted near-neighbour.
3. **No competing client**: 0 established connections to `:34113`, listener is
   127.0.0.1-only, journal silent for 45 min (last activity = r11's tail at
   23:33:17Z). The run's sequential single-slot assumption (plan §2.1) is
   unviolated.
4. **Capacity suffices** for the plan's pinned 4 002 HTTP calls: ≈11.4 GiB
   allocatable RAM (the run reuses the resident model; nothing new is loaded),
   559.9 G free disk, ample `/scratch`, and only ~12–25 min of wall time.

Two conditions (not blockers, but they belong in the run's deviation log):

- **VRAM headroom is 641 MiB.** The GPU is effectively saturated by pid 1299
  (10 522 MiB) + desktop compositors. This only bites if a *new* GPU consumer
  starts mid-run; the run itself adds none.
- **Host load is 2.64/6.29/22.94 with ~24 GiB swap in use** (mostly zram) from
  sibling agents. Sequential single-slot execution means no correctness coupling,
  but per-request `wall_s` will be noisier than on an idle host — expect the
  wall-clock estimate to drift upward, and do not read `wall_s` as a per-round
  comparison.

---

## UNMEASURED

- **`/health` body vs r11.** No committed r11 `/health` capture exists (searched
  `corpus/evidence/round11-fleet/` and `round11-power/` — only `/v1/models` bytes
  were stored). This session's body is captured verbatim above (`{"status":"ok"}`,
  HTTP 200), but there is no r11 counterpart to diff against. `PROVINCE.md:15`'s
  "/health 200 each round" is a status-code claim, and the status code is
  re-verified.
- **md5/sha256 of the 10 GB served file.** Deliberately not run (brief: "do NOT
  start a 10 GB hash run"). The *byte count* is verified via `stat` and closes
  exactly against `data_offset` + Σ tensors.
- **Mechanism behind `created`.** Presented as `[INFERENCE-moderate]`: two
  responses whose `created` equals the in-band `request_ts` to the second (r11 and
  this session), and none matching process start or file mtime. No upstream source
  line for that field was cited.
- **Upstream line numbers** for `llama_model_size` / `n_bytes` accumulation
  (`[INFERENCE-light]`): fetched from `master` (`HTTP 200`) without a commit pin;
  line numbers are as observed in that fetch.
- **Historical `bounties` content.** Gone; the question "did it relocate" is
  answered no (measured), but the historical telemetry bytes cannot be
  re-measured.
- **One unreadable directory** under
  `~/nc8r6-ExLibRouteCheck/.ufo/scopes/tmp-r35-eacces-1488153` (EACCES) — the
  only place under `~` on the `/home` device my sweeps could not traverse;
  `find`'s exit status is 1 for that reason alone.
- **Stability of the 641 MiB VRAM / load figures** over the run window (instant
  samples, not a series).