# Round 51 · SrcLlamaServer — llama.cpp server docs, one SOURCES row

Seat: `SrcLlamaServer` (scribe). Axes named: **adjacency** (assigned); **freshness** observed but
not claimed. Lane `kengaku-shokunin`, read-only. Scope: open the primary llama.cpp HTTP server
documentation at a pinned revision, read `/v1/models`, `/props`, `/health`, `--alias`/`--model`,
propose one tier-A `docs` row in contract-v1 shape, save the bytes with a sha256.

## 0. Binding inputs read before any measurement

| path | what was read |
|---|---|
| `plans/round-51-claims.md` | full file (C1 freshness 8→9, C2 adjacency 8→9, predicates, controls, limits) |
| `plans/round51_surfaces.py` | header/predicate docstring + `tip_rev`/manifest plumbing (the C1 counter; my item names no instrument, so the C1 instrument is the one that touches this row's surface) |
| `plans/round51-surfaces.json` | all 19 entries; `SF03` is the served-model row (`http://127.0.0.1:34113` — `/v1/models`, probe `/health`, state `absent`), `SF14` `count_claim: 25` |
| `corpus/SOURCES.md` | header + contract-v1 registry (tiers, kinds, 11 columns, `queued|mined|rejected` statuses) |

Lane revision at read time (read-only `git rev-parse`): `4090c3db79d11279ab5e5121ba25e74aa316e6e7`
(`round-51: v2 wave spec (64 seats) + validated dispatch payload`); stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c` exists (`git cat-file -t` → `commit`).

## 1. Commands run (verbatim)

```sh
git ls-remote --tags https://github.com/ggml-org/llama.cpp | tail -8
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/server.md
curl -sS "https://api.github.com/repos/ggml-org/llama.cpp/git/trees/8642541b255bfb5dc39cd351a178be09013a55d6?recursive=0" -o tree.json
curl -sS "https://api.github.com/repos/ggml-org/llama.cpp/commits?path=docs/server.md&per_page=5" -o hist.json
curl -sS "https://api.github.com/repos/ggml-org/llama.cpp/commits/8642541b255bfb5dc39cd351a178be09013a55d6" -o commit.json
curl -sS -D headers.txt -o <wave>/llamacpp-tools-server-README-v0.8.0.md -w 'http=%{http_code} bytes=%{size_download}\n' \
  https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md
sha256sum <wave>/llamacpp-tools-server-README-v0.8.0.md
curl -sS -o master-readme.md -w 'http=%{http_code} bytes=%{size_download}\n' \
  https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md && sha256sum master-readme.md
cmp -s master-readme.md <wave>/llamacpp-tools-server-README-v0.8.0.md && echo IDENTICAL_TO_TAG
for r in 8642541b255bfb5dc39cd351a178be09013a55d6 master; do for p in docs/server.md tools/server/README.md; do \
  printf '%s %s ' "$r" "$p"; curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' \
  "https://raw.githubusercontent.com/ggml-org/llama.cpp/$r/$p"; done; done
grep -nE '^#+ .*(/v1/models|/props|/health|alias|model)' <wave>/llamacpp-tools-server-README-v0.8.0.md
grep -n '--alias\|--model ' <wave>/llamacpp-tools-server-README-v0.8.0.md
grep -n 'This endpoint is public\|/v1/health` also works\|HTTP status code 503\|HTTP status code 200\|"status": "ok"\|one single element\|n_ctx_train\|"owned_by"\|total_slots\|"model_path"\|"build_info"\|is_sleeping\|By default, model `id`\|set a custom value for model' <wave>/llamacpp-tools-server-README-v0.8.0.md
sed -n '100p;190p;1376p' <wave>/llamacpp-tools-server-README-v0.8.0.md
sed -n '482p;489,492p;1019p;1349p;1376p' <wave>/llamacpp-tools-server-README-v0.8.0.md
python3 -c '<str.split() word counts for Q1..Q5>'
grep -n "llama.cpp\|llama-server" corpus/SOURCES.md
grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md
date -u +%Y-%m-%dT%H:%M:%SZ
```

`<wave>` = `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-51/w1/SrcLlamaServer`.

## 2. Observed outputs (verbatim where they are evidence)

### 2.1 The item's path premise is wrong

```
8642541b255bfb5dc39cd351a178be09013a55d6 docs/server.md 404 14
8642541b255bfb5dc39cd351a178be09013a55d6 tools/server/README.md 200 135608
master docs/server.md 404 14
master tools/server/README.md 200 135608
```

`GET /repos/ggml-org/llama.cpp/commits?path=docs/server.md&per_page=5` → `200`, empty list (0
commits): the API reports no commit touching that path, and the file is absent at both revisions
tested. The repo's `docs/` tree at the pin (70 blobs) holds
`android.md`, `autoparser.md`, `backend/*`, `build-profiling.md`, `multimodal.md`,
`function-calling.md`, … and no server page. **The canonical server document at the pinned
revision is `tools/server/README.md`.** I read that file and record the discrepancy as a finding
(§6.1) rather than silently substituting.

### 2.2 Pin

```
6ebec9ad2a90f270f0db4a8669c18511d2e82995	refs/tags/v0.8.0
8642541b255bfb5dc39cd351a178be09013a55d6	refs/tags/v0.8.0^{}
```

Pinned commit metadata (`/commits/8642541b…`): `8642541b255bfb5dc39cd351a178be09013a55d6`,
`2026-10-28T11:30:38Z`, message `llama.cpp : bump version to 0.8.0 (#31309)`.

### 2.3 Fetch receipt

```
http=200 bytes=135608
8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6  <wave>/llamacpp-tools-server-README-v0.8.0.md
2616 <wave>/llamacpp-tools-server-README-v0.8.0.md
HTTP/2 200
etag: "80a8ea32c5a7a3c44214e7595a66fbaa9ce9b2bf834f1f920d183554f0b58d7e"
content-length: 135608
date: Wed, 28 Oct 2026 18:23:12 GMT
```

Master comparison, same instant:

```
http=200 bytes=135608
8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6  master-readme.md
IDENTICAL_TO_TAG
```

### 2.4 Section anchors (line numbers in the pinned 2616-line file)

```
480:### GET `/health`: Returns health check result
930:### **GET** `/props`: Get server global properties.
1026:### POST `/props`: Change server global properties.
1345:### GET `/v1/models`: OpenAI-compatible Model Info API
100:| `-m, --model FNAME` | model path to load<br/>(env: LLAMA_ARG_MODEL) |
190:| `-a, --alias STRING` | set model name aliases, comma-separated (to be used by API)<br/>(env: LLAMA_ARG_ALIAS) |
1376:By default, model `id` field is the path to model file, specified via `-m`. You can set a custom value for model `id` field via `--alias` argument. For example, `--alias gpt-4o-mini`.
```

Section ranges resolved by the next heading: `/health` L480–494, GET `/props` L930–1024,
`/v1/models` L1345–1404.

### 2.5 Registry state (adjacency context)

`grep -n "llama.cpp\|llama-server" corpus/SOURCES.md` → no hits: **no llama.cpp row exists in the
registry**. `grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md` → `170` (the C1 `SF14`
`count_claim` is 25; the 170/25 gap is the recorded NUMBER-DRIFT, re-measured here, not new).

Host clock at measurement: `2026-10-28T18:26:34Z`; access date recorded as **2026-10-28**.

## 3. Grounding quotes (each ≤25 words, located in the pinned revision)

| # | lines | quote | words |
|---|---|---|---|
| Q1 | L1376 (2nd sentence) | "You can set a custom value for model `id` field via `--alias` argument." | 13 |
| Q2 | L1349 | "The returned list always has one single element. The `meta` field can be `null` (for example, while the model is still loading)." | 22 |
| Q3 | L482 | "This endpoint is public (no API key check). `/v1/health` also works." | 11 |
| Q4 | L1019 | "`total_slots` - the total number of slots for process requests (defined by `--parallel` option)" | 14 |
| Q5 | L491 | "the model is successfully loaded and the server is ready." | 10 |

Q1 is the row-cell quote (the crux: the served model's `id` is not intrinsically a model name).
Q2–Q5 ground the remaining clauses of `teaches`; all five sit in the same sha256-pinned revision,
so the row's `teaches` is grounded clause by clause, not by paraphrase.

Also observed, same revision, used only in §6 (not in the row's `teaches`): L941
`"n_ctx": 1024` inside `default_generation_settings`; L1005–L1014 `/props` fields
`total_slots`/`model_path`/`build_info`/`is_sleeping`; L1392 `"owned_by": "llamacpp"`; L1396
`"n_ctx_train": 131072`; L932 "By default, it is read-only. To make POST request to change global
properties, you need to start server with `--props`".

## 4. Proposed SOURCES row (contract-v1, 11 columns; NOT written to the lane)

```
| S0?? | llama.cpp HTTP server (`llama-server`) API documentation — https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md | docs | A | the llama.cpp server's own `/v1/models`, `/props` and `/health` contracts, and the `--model`/`--alias` flags that name the served model | `tools/server/README.md` L100, L190, L480-494, L930-1024, L1345-1404 at tag v0.8.0 (commit `8642541b255bfb5dc39cd351a178be09013a55d6`, sha256 `8fd5abde`) | `/v1/models` returns exactly one entry, whose `id` is the `-m` file path unless `--alias` renames it; `/props` reports `model_path`, `total_slots` (`--parallel`), `build_info`; `/health` is public and answers 503 while loading, else 200 ok | queued | 2026-10-28 | on-release | — |
```

Column check (11): `id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by`. No `|` appears inside any cell. `kind=docs`, `tier=A` (the maintainers' own
document at the code revision it documents), `status=queued` (no knowledge entry cites it yet),
`recheck=on-release` (the doc floats with the repo; re-open at each tagged release, the value
already used by S005/S006), `used-by=—` (honest: nothing cites it yet — if the L1 cites it from
`PROVINCE.md`'s served-model row, that path belongs in this cell at landing, not before).

`teaches` is a distillation of Q1–Q5; it deliberately drops the doc's model-catalog/router material
(`/models`, `/models/load`, L2197+) because the lane's surface is a single served endpoint.

## 5. Saved bytes

| file (under `<wave>`) | bytes | sha256 |
|---|---|---|
| `llamacpp-tools-server-README-v0.8.0.md` | 135608 | `8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6` |
| `llamacpp-tools-server-README-v0.8.0.md.sha256` | 105 | receipt line, `sha256sum` output |
| `llamacpp-tools-server-README-v0.8.0.http-headers.txt` | 897 | raw response headers incl. `date: Wed, 28 Oct 2026 18:23:12 GMT` and `etag` |
| `PROVENANCE.md` | — | URL, pin, access date, path-premise probe table, section ranges, word counts |

URL actually opened:
`https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md`

## 6. Findings for the L1 (adjacency)

1. **Premise defect, routed:** the round-51 item names `docs/server.md`. It does not exist at the
   pinned tag or at `master` (`404 14`; zero commits at that path). Canonical path is
   `tools/server/README.md`. Any lane artifact citing `docs/server.md` for llama.cpp server
   behaviour cites a non-existent path.
2. **`/v1/models` is a one-element list (Q2).** It reports the single loaded model, not a catalog;
   a reading that treats it as a model catalog is wrong at this revision. The router's catalog is
   `GET /models` (L2197) — a different endpoint.
3. **`id` is a file path unless `--alias` (Q1).** Consequence for `PROVINCE.md`'s served-model row:
   the round-10 cmdline passes `--alias /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`,
   i.e. an alias whose value is itself a path. An observed `id` that looks like a path therefore
   does **not** prove the `-m` default; identity from `/v1/models` alone is ambiguous without the
   process cmdline. The doc permits arbitrary alias strings (`--alias gpt-4o-mini`, L1376).
4. **`owned_by=llamacpp` confirmed (L1392).** The lane's `owned_by=llamacpp` reading of
   `:34113` matches the documented example value.
5. **Runtime `n_ctx` is a `/props` field, not a `/v1/models` field.** `default_generation_settings.n_ctx`
   (L941) is the runtime context; `/v1/models` exposes `meta.n_ctx_train` (L1396, example 131072 =
   training context). The lane's `n_ctx=16384` claim on `:34113` is re-checkable through `/props`
   (or `/slots`), not through `/v1/models` — relevant to how a future C1 probe for that surface is
   specified.
6. **`/props` also carries the process identity the lane has been reading from `/proc`:**
   `model_path` (same as `-m`, L1006), `total_slots` (`--parallel`, L1019), `build_info` (L1013),
   `is_sleeping` (L1014). POST `/props` requires `--props` at startup (L932) — the served unit does
   not pass it, so a POST probe against `:34113` would fail for a documented reason, not a defect.
7. **`/health` semantics for C1:** public, no API key (Q3); `503` `{"error":{"code":503,...}}` while
   loading, `200 {"status": "ok" }` when ready (L486–L492). `SF03`'s probe URL
   `http://127.0.0.1:34113/health` is the documented native path, and `/v1/health` is also valid —
   a future probe that used `/v1/health` would not be wrong.
8. **No duplicate row:** `corpus/SOURCES.md` has no llama.cpp row (0 hits), so this proposal does
   not collide with an existing id. The registry count re-measured at 170 rows, consistent with
   the recorded `SF14` NUMBER-DRIFT (row says 25).

## 7. Limits

- Only the upstream document was opened. **llama.cpp source (`tools/server/server.cpp`) was not
  read**, so every claim here is the maintainers' statement, not implementation-verified behaviour.
- **Version skew is real and declared:** the doc is pinned at `v0.8.0` (commit `8642541b…`,
  committed `2026-10-28T11:30:38Z`), while the lane's recorded local binary is
  `0.3.0-dev (build 1, commit d7bd3bf)` (`corpus/evidence/round10-fleet/r10-scout-endpoint.md:36`).
  Fields and flags documented here may not exist on that build; the row teaches the documented
  contract at the pin, not the local server's behaviour.
- `master` and the tag returned identical bytes today (`IDENTICAL_TO_TAG`); the row pins the tag so
  it does not float, but the doc is a moving target and `recheck=on-release` is the honest cadence.
- No live endpoint probe was run (out of scope for this seat; `SF03` is `absent` per the C1 before
  receipt). Nothing here asserts `:34113` is up.
- Word counts are `str.split()` counts over the quoted text as fetched.
- The row id is left as `S0??`; assigning the next id is the integration owner's call.

## 8. Files touched / scratch

- Written: `<wave>/SrcLlamaServer.md` (this report), `<wave>/SrcLlamaServer/PROVENANCE.md`,
  `<wave>/SrcLlamaServer/llamacpp-tools-server-README-v0.8.0.md`,
  `…md.sha256`, `…http-headers.txt`. All inside the seat's named wave dir.
- Scratch: `/fast/scratch/hyaku/kengaku-r51/SrcLlamaServer` (TMPDIR; `tree.json`, `hist.json`,
  `commit.json`, `headers.txt`, `master-readme.md`) — **removed before yield**; the sha256 and
  header receipt were copied into the wave dir first, so nothing citable lives in scratch.
- Not written: any `plans/*`, `corpus/*`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`.
  No commit, no push, no mutating git/jj command (only `rev-parse`, `log`, `cat-file`, `show`).
- Tooling: no installs, no package manager. `curl`, `git ls-remote`, `sha256sum`, `cmp`,
  `python3` stdlib only.

REV 8642541b255bfb5dc39cd351a178be09013a55d6
REV-LANE 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: Opened the llama.cpp server doc at pinned tag v0.8.0 (commit 8642541b…, 135608 bytes, sha256 8fd5abde…, access 2026-10-28 18:23:12 GMT) — but not at the item's `docs/server.md`, which 404s at both the pin and master; the canonical path is `tools/server/README.md`. One tier-A `docs` row in contract-v1 shape is drafted with five located quotes (all ≤25 words) covering `/v1/models`, `/props`, `/health` and `--alias`/`--model`; bytes and digest saved in the wave dir; the path premise and the `n_ctx`-lives-in-`/props` consequences are reported as findings for the L1.
