# PROVENANCE — llama.cpp HTTP server docs, round 51 seat SrcLlamaServer

Fetched bytes: `llamacpp-tools-server-README-v0.8.0.md`
HTTP headers as received: `llamacpp-tools-server-README-v0.8.0.http-headers.txt`
Digest receipt: `llamacpp-tools-server-README-v0.8.0.md.sha256`

| field | value |
|---|---|
| URL (canonical raw) | `https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md` |
| repository | `https://github.com/ggml-org/llama.cpp` |
| pin | annotated tag `v0.8.0` (tag object `c13fcbf684171d5e0bca3fc5c34be6a99174b05f`) dereferences to commit `8642541b255bfb5dc39cd351a178be09013a55d6` (`refs/tags/v0.8.0^{}`) |
| pinned commit date | `2026-10-28T11:30:38Z`, message `llama.cpp : bump version to 0.8.0 (#31309)` |
| access date | 2026-10-28 (response `date:` header `Wed, 28 Oct 2026 18:23:12 GMT`) |
| HTTP status | `HTTP/2 200` |
| bytes | 135608 |
| lines | 2616 |
| sha256 | `8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6` |
| etag | `"80a8ea32c5a7a3c44214e7595a66fbaa9ce9b2bf834f1f920d183554f0b58d7e"` |
| master comparison | `https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md` returned the same 135608 bytes and the same sha256 on 2026-10-28 (`cmp` → `IDENTICAL_TO_TAG`); the tag is pinned anyway so the row does not float |

## Path premise check (the item names `docs/server.md`)

| revision | path | result |
|---|---|---|
| `8642541b255bfb5dc39cd351a178be09013a55d6` | `docs/server.md` | `404 14` |
| `8642541b255bfb5dc39cd351a178be09013a55d6` | `tools/server/README.md` | `200 135608` |
| `master` | `docs/server.md` | `404 14` |
| `master` | `tools/server/README.md` | `200 135608` |

`GET https://api.github.com/repos/ggml-org/llama.cpp/commits?path=docs/server.md&per_page=5` returned
`200` with an empty list (0 commits), so `docs/server.md` has no history in this repository at that
path. The canonical server document at the pinned revision is `tools/server/README.md`.

## Sections read (line numbers in the pinned file)

| section | lines |
|---|---|
| `-m, --model FNAME` flag row | 100 |
| `-a, --alias STRING` flag row | 190 |
| `### GET /health` | 480–494 |
| `### GET /props` | 930–1024 |
| `### GET /v1/models` | 1345–1404 |
| `--alias` / `id` prose | 1376 |

## Quote word counts

Q1 13 · Q2 22 · Q3 11 · Q4 14 · Q5 10 (all ≤ 25).
