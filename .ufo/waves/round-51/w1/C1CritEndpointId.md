# C1CritEndpointId — endpoint identity probe (critic seat, round 51 / hyaku 11)

Item: falsify "the model id and digest served on `127.0.0.1:45669` are the same object the router
on `127.0.0.1:1234` reports, and both match the argv in `/proc`".
Bound: read-only HTTP only — no generation requests, no model calls, no model selection.

## Axes named (before the probe)

- **A1 — identity-string agreement**: do id / digest / argv name one object across the child
  endpoint, the router's report, and `/proc`?
- **A2 — freshness of the declaration**: is the live served endpoint a surface `PROVINCE.md`
  declares and the frozen counter can machine-check at the tip?
- **A3 — evidence cost and provenance**: what can a truthful pin for that surface actually be
  built from, and what does it cost the counter?

## Revision measured

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane tip `master`, clean tree except untracked
wave files). The frozen instruments are byte-identical to the stage-1 freeze commit
`e07f131cf7037e58a21db6e1f3986cf401ad257c` — no instrument drift:

```
plans/round51_surfaces.py  freeze=6107c605925310ed64433b1f27d3459e8836ed43 tip=6107c605925310ed64433b1f27d3459e8836ed43
plans/round51-surfaces.json freeze=154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6 tip=154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6
plans/round51_routing.py   freeze=043533d1a9599b8a9efda155812899d382384fbf tip=043533d1a9599b8a9efda155812899d382384fbf
git diff --stat e07f131..HEAD -- plans/ PROVINCE.md   →  (empty)
```

## Commands run (exact, in order)

```sh
ss -ltnp | grep -E '45669|1234'
curl -sS -m 5 http://127.0.0.1:45669/v1/models -o probe/m45669.json
curl -sS -m 5 http://127.0.0.1:1234/v1/models  -o probe/m1234.json
curl -sS -m 5 http://127.0.0.1:45669/props     -o probe/props45669.json
curl -sS -m 5 http://127.0.0.1:1234/props      -o probe/props1234.json
tr '\0' ' ' < /proc/242776/cmdline ; tr '\0' ' ' < /proc/1706355/cmdline
grep -o '"digest"[^,}]*' m45669.json m1234.json props45669.json props1234.json
curl -sS -m 5 http://127.0.0.1:{45669,1234}/api/tags     # both 404
curl -sS -m 5 http://127.0.0.1:{45669,1234}/health       # both {"status":"ok"} 200
curl -sS -m 5 http://127.0.0.1:45669/slots               # 200, 4 slots
curl -sS -m 5 http://127.0.0.1:1234/slots                # 400 "model name is missing"
curl -sS -m 5 http://127.0.0.1:45669/metrics             # 501 not enabled
stat -c '%n %s %y' /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
sha256sum /home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf
# 3× timed GET /v1/models on 45669, 20 s apart (created drift)
# element-wise compare: json(1234).data[0].status.args vs /proc/242776/cmdline split on NUL
```

## Observed — three identity strings side by side

| attribute | `:45669` (`/v1/models`, `/props`) | `:1234` router (`/v1/models` `status.args`) | `/proc` argv | agreement |
|---|---|---|---|---|
| id | `LFM3-1.7B` (`data[0].id`, `models[0].name/model`) | `LFM3-1.7B` (`data[0].id`) | `--alias LFM3-1.7B` (pid 242776) | **agree** |
| **digest** | `"digest":""` in legacy `models[0]`; **no** `digest` key in `data[0]` | **absent** — `grep -o '"digest"'` on the whole body: 0 occurrences | none in argv | **NOT COMPARABLE** |
| model path | `/props.model_path` = `/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf` | `status.args` `--model` = same string | pid 242776 `--model` = same string | **agree** |
| argv equality | — | `status.args == /proc/242776/cmdline` → **True**, 16/16 elements | 16 elements | **byte-exact** |
| build | `/props.build_info` = `b1-39febd2` | `build_info` = `b1-39febd2` | binary `/home/vgpnk/src/llama.cpp/build/bin/llama-server` | agree |
| ftype / n_ctx | `Q8_0` / `32768` | `meta` block **identical** to child `meta` | `--ctx-size 32768` | agree |
| `aliases` | `["LFM3-1.7B"]` | `[]` | — | field diverges, value agrees |
| `created` | `1793211699` … | same value | — | **agree but not identity** (clock, below) |
| own `/props` | `role` absent (model server) | `role:"router"`, `model_path:"none"`, `model_alias:"llama-server"` | pid 1706355: `--models-dir /home/vgpnk/models/lfm3 --models-max 2 … --port 1234`, **no `--model`** | router does not present itself as the model |

Verbatim identity strings:

```
45669 data[0].id       = "LFM3-1.7B"      aliases ["LFM3-1.7B"]   created 1793211699
45669 models[0].digest = ""
1234  data[0].id       = "LFM3-1.7B"      aliases []              created 1793211699
1234  data[0].status   = {"value":"loaded","args":["/home/vgpnk/src/llama.cpp/build/bin/llama-server",
                        "--host","127.0.0.1","--jinja","--log-colors","off","--port","45669",
                        "--alias","LFM3-1.7B","--ctx-size","32768","--model",
                        "/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf","--n-gpu-layers","99"],
                        "preset":"[LFM3-1.7B]\njinja = 1\n…"}
/proc/242776/cmdline   = the same 16 tokens, in the same order (equality True)
/proc/1706355/cmdline  = [...,"--models-dir","/home/vgpnk/models/lfm3","--models-max","2",
                        "--host","127.0.0.1","--port","1234","-ngl","99","-c","32768","--jinja"]
45669 /props           = {"model_alias":"LFM3-1.7B","model_ftype":"Q8_0","model_path":
                        "/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf",
                        "build_info":"b1-39febd2","total_slots":4, …}
1234  /props           = {"role":"router","max_instances":2,"models_autoload":true,
                        "model_alias":"llama-server","model_path":"none",
                        "build_info":"b1-39febd2", …}
```

Listener pinning (one process per port, so no ambiguity about which child the router names):

```
LISTEN 127.0.0.1:45669 users:(("llama-server",pid=242776,fd=19))   starttime=17342423
LISTEN 127.0.0.1:1234  users:(("llama-server",pid=1706355,fd=18))  starttime=17182432
```

## Counterexamples (strongest first)

1. **`created` is a clock, not an identity.** It is the one numeric field that agrees exactly
   across both endpoints and reads like a load timestamp — and it moves with the wall clock.
   Three timed samples, 20 s apart, `created` decoded == `date -u` to the second:

   ```
   at 18:21:39Z  created=1793211699 (18:21:39Z)
   at 18:21:59Z  created=1793211719 (18:21:59Z)
   at 18:22:19Z  created=1793211739 (18:22:19Z)
   ```

   Earlier batches likewise: 1793211410 → 1793211435 → 1793211513, always == request time.
   So "both endpoints agree on `created`" is evidence of a shared clock, nothing more; and a
   declared row whose prose cites `created` would go `STALE`/`DRIFT` on every counter run.

2. **The digest conjunct is not merely unverified — it is unavailable.** The only digest-shaped
   field anywhere is the empty string on the child's legacy array (`"digest":""`); the router
   body contains zero occurrences of the word. Comparing `""` against *absent* is not agreement.
   The claim "the digest served on 45669 is the same object the router reports" has no referent.

3. **"both match the argv in `/proc`" holds for the child only.** `status.args` equals
   `/proc/242776/cmdline` byte-for-byte (16/16), but the router's own argv (pid 1706355) carries
   `--models-dir /home/vgpnk/models/lfm3` and no `--model`: it matches at directory granularity,
   not token equality. Any prose that says "both processes' argv match" is false as written.

4. **A 200 from `/health` does not identify the object.** Both ports answer `{"status":"ok"}`;
   the router answers with `role:"router"`, `model_path:"none"`. A surface probe that only
   asserts "endpoint answers 200" (the frozen `http` probe kind) cannot tell the model server
   from the router — which is exactly the identity this seat was asked to test.

5. **The artifact digest that does exist is not the server's.** `sha256sum` of the argv-named
   file is `8f6b24182258205e9e01e21f1f24a1f208c1e8115578825d202ce39976af20b6`
   (size `1846238496`); it inherits the argv's trust, not the endpoint's. And `meta.size` is
   `1837991168` (tensor bytes) ≠ file size — so `size` is not an artifact identity either.

## Impact on the C1 claim (freshness 8 → 9)

The `## Surfaces` table has exactly one served-model row today, `SF03`, anchored on
`http://127.0.0.1:34113` — recorded `state=absent`, `prose=present`, and it is one of the three
`DRIFT` rows in the before receipt (`REV 297e179…`, `DRIFT 3`, `PREDICATE R51-C1 fail`, exit 1).
The endpoint that *is* live (`:45669` + router `:1234`) is declared nowhere, so the counter cannot
see it (`UNCOVERED` is 0 only because the row does not exist). The "one new declared surface"
in the after target must therefore carry the identity at the granularity the evidence supports:

- **Truthful**: id `LFM3-1.7B`; `model_path` `/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf`;
  `ftype Q8_0`; `n_ctx 32768`; `build_info b1-39febd2`; router `:1234` reports the same id and its
  `status.args` equals the child's `/proc` argv (16/16 tokens); child pid 242776, router pid 1706355.
- **Not truthful**: any served digest (none is served), any claim that the router's own argv names
  the model file, any pin on `created`.

## Smallest safe correction

1. Anchor the new row on the port literal (`http://127.0.0.1:45669`), not on the shared
   `` `/v1/models` `` text — the latter would `ANCHOR-DUP` against `SF03`.
2. Manifest entry: probe `port` (45669) or `http` on `http://127.0.0.1:45669/health`; `state`
   `present`. Do **not** add a `sha256` pin for the 1.85 GB gguf this round: `probe()` in the
   frozen `plans/round51_surfaces.py` does `hashlib.sha256(f.read_bytes())`, i.e. a whole-file
   allocation on every counter run; a streaming hash would edit a frozen instrument. If a digest
   is wanted later, it belongs on a file row with a streaming read.
3. State the router relationship in prose as "`:1234` `status.args` == `:45669` `/proc` argv",
   and leave `created`, `aliases`, and `size` out of the row.

## Limits

- Point-in-time probes on this host only; `:45669` and `:1234` may disappear, which would flip a
  `present` row to `STALE` — intended counter behaviour, not a defect.
- No generation request, no model call, no model selection was made; `/slots`, `/health`,
  `/props`, `/v1/models` GETs only. `/api/tags` (the Ollama-compat path that could carry digests)
  is 404 on both ports, so no digest could be obtained from either endpoint.
- I did not run the frozen counter (read-only seat); the C1 before numbers are cited from
  `.ufo/waves/round-51/claims/c1-before.txt` at `REV 297e17927ba9342a87ba27a48cc5270a001de7cb`.
- No tool was installed or upgraded (nothing was needed; no pacman transaction attempted).
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1CritEndpointId` was created, used, and removed
  before yield; nothing in this report cites a `/tmp` or scratch path as evidence.

VERDICT: FALSIFIED — the id conjunct holds (`LFM3-1.7B` on `:45669`, on `:1234`, and `--alias`
in `/proc`), the argv conjunct holds for the child (router `status.args` is byte-identical to
`/proc/242776/cmdline`, 16/16, and `/props` names the same `model_path`/`ftype`/`build_info`),
but the **digest conjunct fails**: `:45669` serves `"digest":""` and `:1234` serves no digest
field at all, so no digest identity exists to match — and the one agreeing numeric field,
`created`, is request wall-clock, not model identity. The new declared surface must assert
id + path + argv equality, never a served digest.
