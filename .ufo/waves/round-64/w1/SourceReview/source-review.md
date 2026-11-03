# SourceReview (r64 w1, seat SourceReview-2) — S230/S231 non-author source re-open

Date: 2026-11-03. Both named network opens only; no tool installs (system curl 8.23.0, git 2.56.0, python 3.14.8; pacman untouched per guard; no ports bound; no git mutations). Frozen claims doc read in full; no rule changed.

Receipts in this seat dir:
- `s230-test_outputs.py` (6076 bytes) + `s230-headers.txt` (HTTP 200, content-length 6076)
- `s231-grpc-python-api.html` (250738 bytes) + `s231-headers.txt` (HTTP 200, last-modified Mon, 26 Oct 2026 06:32:10 GMT)
- `verification-log.txt` (sha256 9a53a0ad2498330a0a59ad1470db37f644626f309ec7d970a414a79cf26bc99a) — every observed value below with its command.

## S230 — TB2 kv-store-grpc grader at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 — VERDICT: verified

- URL fetched: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py (`curl -fsSL`, rc 0, HTTP/2 200, x-github-request-id 57F8:1EB85A:37262:4E6FD:6AEA31A3, date Tue, 03 Nov 2026 19:12:05 GMT).
- sha256 of live bytes: `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` — equals the frozen pinned sha in plans/round-64-claims.md (= corpus/evidence/round52/graders/SHA256SUMS line 80 value).
- `cmp` vs lane capture `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` → rc 0, byte-identical (both 6076 bytes; lane copy hashes to the same digest). Git blob id of captured bytes: `2bb04c15ea568ef2ac52cd778ca886a7f02ceff2` (`git hash-object`).
- Seven-leg contract read from the live bytes (`grep -n '^def test_'`): `test_proto_file_creation` :15, `test_grpc_tools_installation` :35, `test_protobuf_generation` :50, `test_server_file_creation` :67, `test_real_grpc_server_running` :83, `test_grpc_protocol_handshake` :99, `test_grpc_server_functionality` :138 — seven functions, exactly the frozen file order.
- Leg-5 fragment live at :96 with `port = 5328` (:88): `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"` — matches the frozen K2 leg-5 fragment `Port 5328 is not listening`.
- Except structure grounds the frozen K5 vector: `except grpc.RpcError:` at :128 exists ONLY inside `test_grpc_protocol_handshake` (comment :129 "gRPC errors are expected and indicate real gRPC protocol"); `test_grpc_server_functionality` (:138) has no RpcError handler — so a no-server run yields leg-6 P (UNAVAILABLE is an RpcError) and leg-7 F, while non-RpcError paths (ModuleNotFoundError on `import grpc` / `import kv_store_pb2`) fail — consistent with frozen K2/K4 vectors.
- Teaches claim "the grader's seven-leg contract" holds against the live bytes at the pin.

## S231 — gRPC Python API reference, grpc.RpcError / status codes — VERDICT: verified

- URL fetched: https://grpc.github.io/grpc/python/grpc.html (`curl -fsSL`, rc 0, HTTP/2 200, content-length 250738, last-modified Mon, 26 Oct 2026 06:32:10 GMT). Unversioned live docs page; the recorded digest + last-modified bound this opening for recheck.
- sha256 of live bytes: `d68676105b4bbf7f701eb3458e95db7efd5fe6129408eba4b574dff23ea083e4`.
- Primary located quote — heading "exception grpc.RpcError", anchor `#grpc.RpcError` (HTML offset 97918):
  > "Raised by the gRPC library to indicate non-OK-status RPC termination." (10 words)
- Corroborating quote — heading "UNAVAILABLE", anchor `#grpc.StatusCode.UNAVAILABLE` (offset 61563):
  > "The service is currently unavailable." (5 words)
- Grounding check: UNAVAILABLE is a StatusCode naming the unavailable-server condition; RpcError is what the library raises on non-OK-status RPC termination — so an unavailable server surfaces as a Python exception on the RPC call. Triangulated by the grader's own bytes (S230 capture :128-129, where the handshake leg treats `grpc.RpcError` as the expected gRPC error surface).
- Teaches claim "RpcError is the exception surface for gRPC status errors" holds against the live bytes.

## Residual risk / gaps
- S231 is not commit-pinned (GitHub Pages serves latest); a future recheck must re-hash and may see a new digest — the anchor text quoted is stable class documentation, but the row should carry today's digest as the opening observation.
- No LSP/gate/judgment artifacts touched; this seat opened sources and reports only. Rows S230/S231 themselves are written by the L1.
