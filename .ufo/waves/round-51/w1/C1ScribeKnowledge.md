# C1ScribeKnowledge — served-endpoint identity pin (scribe, round 51)

**Axes named:** freshness (primary — the entry pins what a live endpoint *is* at a date, and the
re-take rule is the freshness mechanism); adjacency secondary (the entry routes serving-plane
ownership to `kama` and cites a new SOURCES row instead of absorbing the doc).

**Deliverable:** `.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md` — a
draft of `corpus/knowledge/served-endpoint-identity-pin.md` for the L1 to land. The lane tree was
not touched (read-only); the draft sits beside this report as the sibling fragment.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7  (lane HEAD when measured; stage-1 freeze e07f131cf7037e58a21db6e1f3986cf401ad257c)
REV 8642541b255bfb5dc39cd351a178be09013a55d6  (llama.cpp doc pin the entry cites)

## 1. What the draft contains

Provenance trio first, then the three required parts:

1. **Identity-pin decision table** (16 rows): model id, aliases, `owned_by`, served context
   (`meta.n_ctx` × `/props` `default_generation_settings.n_ctx` × argv `--ctx-size`), trained context,
   weights file, weights digest, weights size (file vs `meta.size`), quantisation, process argv, slot
   count, build, generation defaults, chat template + caps, process identity (pid + start time).
2. **What is not a pin** — `created`, `/health`, `owned_by` alone, alias alone, a router's `/props`.
3. **When a pin must be re-taken** — 8 triggers, plus a tested one-sitting re-take block, plus the
   append-never-overwrite rule.
4. **Limit** — a point-in-time pin is host state: no capability, no weight provenance, no
   availability, no ownership (serving plane routes to `kama` per `PROVINCE.md` §Adjacent).

## 2. Commands run (exact)

```sh
# doc anchor, re-verified independently of the SOURCES seat
curl -sS -o doc.md https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md
sha256sum doc.md && wc -l doc.md
cmp -s doc.md .ufo/waves/round-51/w1/SrcLlamaServer/llamacpp-tools-server-README-v0.8.0.md

# live endpoint :45669
curl -sS --max-time 5 http://127.0.0.1:45669/health
curl -sS --max-time 5 http://127.0.0.1:45669/v1/models
curl -sS --max-time 5 http://127.0.0.1:45669/props
tr '\0' '\n' < /proc/242776/cmdline
awk '{print "pid="$1" comm="$2" state="$3" starttime="$22}' /proc/242776/stat
getconf CLK_TCK                       # 100, for the start-time derivation
sha256sum /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
stat -c '%n size=%s mtime=%y' /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf

# stability test: is `created` an identity field?
for i in 1 2 3; do curl -sS http://127.0.0.1:45669/v1/models | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data'][0]['created'])"; sleep 2; done
ss -ltnp | grep 45669

# comparison endpoints
tr '\0' '\n' < /proc/3262613/cmdline ; curl -sS http://127.0.0.1:37323/props
tr '\0' '\n' < /proc/1706355/cmdline ; curl -sS http://127.0.0.1:1234/props
curl -sS --max-time 4 http://127.0.0.1:34113/health        # absent
curl -sS --max-time 4 http://127.0.0.1:8791/v1/models ; curl -sS http://127.0.0.1:8791/props

# re-take block in the entry, executed to prove it works
P=45669; PID=$(ss -ltnpH "sport = :$P" | grep -o 'pid=[0-9]*' | cut -d= -f2)
awk '{print "pid="$1" starttime="$22}' /proc/$PID/stat
sha256sum "$(curl -sS http://127.0.0.1:$P/props | python3 -c 'import sys,json;print(json.load(sys.stdin)["model_path"])')"

# registry state for the S-number derivation
git show HEAD:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'     # 170
git show HEAD:corpus/SOURCES.md | grep -E '^\| *S[0-9]{3,} *\|' | tail -1
```

## 3. Observed outputs (verbatim, the ones the entry cites)

```
$ sha256sum doc.md && wc -l doc.md
8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6  doc.md
2616 doc.md
$ cmp -s doc.md <SrcLlamaServer capture> && echo IDENTICAL
IDENTICAL
```

```
$ tr '\0' '\n' < /proc/242776/cmdline            # 16 tokens
/home/vgpnk/src/llama.cpp/build/bin/llama-server
--host 127.0.0.1 --jinja --log-colors off --port 45669 --alias LFM3-1.7B
--ctx-size 32768 --model /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
--n-gpu-layers 99
```

```
$ curl :45669/v1/models | python3 -m json.tool (extract)
id LFM3-1.7B | aliases ["LFM3-1.7B"] | owned_by llamacpp
meta: vocab_type 2, n_vocab 128000, n_ctx 32768, n_ctx_train 262144, n_embd 2048,
      n_params 1728801600, size 1837991168, ftype Q8_0
```

```
$ curl :45669/props (identity fields)
model_alias LFM3-1.7B | model_ftype Q8_0 | model_path /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
build_info b1-39febd2 | total_slots 4 | default_generation_settings.n_ctx 32768
endpoint_props false | endpoint_metrics false | is_sleeping false
modalities {"vision": false, "video": false, "audio": false}
bos_token <|startoftext|> | eos_token <|im_end|>
chat_template_caps supports_tool_calls true, supports_system_role true, supports_reasoning_effort false
params: temperature 0.10000000149011612, top_k 50, top_p 0.949999988079071,
        min_p 0.05000000074505806, repeat_penalty 1.100000023841858, seed 4294967295,
        n_predict -1, chat_format "Content-only", reasoning_format "none"
```

```
$ created sampled 3× at 2 s spacing, pid constant 242776
1793211893
1793211895
1793211897
```

```
$ awk starttime + btime, HZ=100
pid=242776 starttime=17342423  -> start_epoch 1793200724 = 2026-10-28T15:18:44Z
$ stat + sha256sum of the weights
size=1846238496  (meta.size in /v1/models is 1837991168; delta 8247328)
8f6b24182258205e9e01e21f1f24a1f208c1e8115578825d202ce39976af20b6
```

```
$ :37323  ollama-bundled llama-server, build b1-9ff0d7e90, pid 3262613
model_path /fast/scratch/hyaku/kama-r61-closure/c1/c1-9z8mmjqy/run-pd/models/blobs/sha256-270cba1b…
-c 2048 -np 1 | total_slots 1 | temperature 0.800000011920929, top_k 40, repeat_penalty 1.0
$ :1234   router, build b1-39febd2, argv --models-dir /home/vgpnk/models/lfm3 --models-max 2 -c 32768 --jinja
{"role":"router","model_path":"none","default_generation_settings":{"params":null,"n_ctx":0},"max_instances":2,"models_autoload":true}
$ :34113  curl: (7) Failed to connect to 127.0.0.1:34113 after 0 ms: Could not connect to server
$ :8791   {"object":"list","data":[{"id":"deepseek-v4.1-flash","object":"model","created":0,"owned_by":"ds-flash-shim"}]}
          /props -> {"error": {"message": "unknown path /props"}}
```

```
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,} *\|'
170
$ ... | tail -1
| S177 | git-fetch (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc …
```

## 4. One correction made during drafting (verification trail)

The first draft asserted "`/props` does not report `n_ctx` on b1-39febd2". That was wrong: I had
looked inside `default_generation_settings.params` only. The measured object has
`default_generation_settings = {"params": {...}, "n_ctx": 32768}` — `n_ctx` sits **beside** `params`,
exactly as the doc example shows at `:941`. The entry now records the correct read path and turns the
mistake into the row's trap ("look inside `params` and you find nothing"). Recorded here because a
silently fixed error is not auditable.

## 5. Findings for the L1 (freshness / integration)

1. **The SOURCES seat left the row id as `S0??`** (`.ufo/waves/round-51/w1/SrcLlamaServer.md` §4:
   "assigning the next id is the integration owner's call"). My item asks for the S-number the SOURCES
   seat proposes, so I derived it and said so in the entry: the committed registry holds **170** rows,
   the highest is **S177**, and **S178–S251** are unallocated (`.ufo/waves/round-51/w1/SrcCensus.md`,
   `STAGED_UNIQUE=175`, `S178–S251` = 74 ids beyond the registry's highest). `S178` is therefore the
   next free id; the entry's `source:` line states this derivation and says it changes with the
   landing if the L1 assigns differently.
2. **A pin-relevant fact the C1 surface row should not lose:** the new live endpoint `:45669` is a
   *different subject* from the `:34113` row that is `DRIFT` today. Same `owned_by` (`llamacpp`),
   different build, different weights, different context (32768 vs the 16384 recorded for `:34113`),
   and no `--parallel` flag in argv although `total_slots` is 4. If the new PROVINCE row quotes
   `:34113`'s round-10 pin without re-dating it, C1 will trade one `DRIFT` for another.
3. **`:37323` is a kama-owned process serving a kama scratch blob.** Its model path is under
   `/fast/scratch/hyaku/kama-r61-closure/…`. Any pin citing it is historical the moment that scratch
   tree is removed — worth a dated marker if it ever enters a surface row.
4. **`created` is not identity.** Measured: three samples 2 s apart, `+2` per sample, pid constant.
   If any counter or receipt records `data[0].created` as a pin, it will drift on every read.

## 6. Limits

- The entry pins **one** endpoint (`:45669`) in full and three others only for comparison. It does
  not measure throughput, latency, output quality, or behaviour under load, and it makes no
  capability claim — that is the entry's own §Limit.
- `n_ctx` on `:37323` was taken from argv (`-c 2048`) and `/props` (`total_slots 1`); its
  `/v1/models` `meta` was not read this sitting. The entry does not cite a `:37323` `meta.n_ctx`.
- Weights digest is of the file at `model_path` at 2026-10-28T18:28Z; a re-take is required if the
  file's mtime (2026-10-28 11:51:12 -0300) changes.
- The lane tree was not modified; `git status` was not used as verification of anything but the
  untracked `.ufo` wave dirs.
- No tool was installed or upgraded this seat (nothing was needed; PACMAN guard untouched).

## 7. Observed lane state (not mine — recorded, not acted on)

`git status --porcelain --untracked-files=no` at 2026-10-28T18:33Z reported one tracked
modification, in a **frozen** C2 instrument:

```
 M plans/round51_routing.py
 plans/round51_routing.py | 18 +++++++++++++-----
 1 file changed, 13 insertions(+), 5 deletions(-)
 mtime=2026-10-28 15:33:21.513675706 -0300
```

This seat did not write it and did not run it. The three semantic changes visible in the diff, for
the L1 / canonical judge:

1. `load_owners()` — the owner universe is widened from `FALLBACK_OWNERS` + `shokunin.conf` HCL-style
   blocks to `FALLBACK_OWNERS` + `id|repo|axes` rows + every `*-shokunin` directory on disk. The last
   clause makes `owner` validation depend on the fleet tree's current contents, not the frozen
   contract.
2. Check execution cwd — `cwd=str(tmp)` → `cwd=str(lane)`. Every ledger `check` now runs **inside the
   lane**, which changes which checks can pass (this is the difference between "a check that needs
   the lane" failing and passing).
3. Check timeout — `60` → `90` seconds.

Points 2 and 3 change the counter's measured quantity against `plans/round-51-claims.md` §Limits
("71 short shell commands … with a 60 s timeout each in a scratch cwd"). Whether that is the L1's
intended repair or a seat overstepping read-only bounds is not this seat's call; recorded verbatim
because C2's before/after comparison depends on it.

## 8. Scratch

`/fast/scratch/hyaku/kengaku-r51/C1ScribeKnowledge` held the probe captures (`health.json`,
`models.json`, `props.json`, `props-1234.json`, `props-37323.json`, `cmdline*.txt`, `doc.md`,
`gguf.sha256`). Every number the entry cites is reproduced verbatim in §3 above, so the scratch tree
carries no unique evidence; it is removed before yield.

VERDICT: Drafted `corpus/knowledge/served-endpoint-identity-pin.md` as
`.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md` — provenance trio first
(`source:` = S178 derived from the committed registry because the SOURCES seat left `S0??`, URL +
commit + sha256 + seven line anchors; `verified-at:` 2026-10-28; `recheck:` 90d), then the 16-row
identity-pin decision table, the not-a-pin list, 8 re-take triggers with a tested re-take block, and
the host-state-not-capability limit. Every number comes from my own re-run of `C1ExecEndpoints`'s
probes on the live processes or from the sha256-pinned doc at `8642541b…`; one mid-draft error
(`n_ctx`'s location in `/props`) was caught by re-reading the measured object and is disclosed in §4.
Lane untouched by this seat (one foreign modification to `plans/round51_routing.py` observed and
reported in §7); scratch removed.
