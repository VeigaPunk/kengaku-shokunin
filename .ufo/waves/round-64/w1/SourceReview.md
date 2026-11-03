# SourceReview — r64 w1 seat report (S230/S231 non-author source re-open), 2026-11-03

Full deliverable: `.ufo/waves/round-64/w1/SourceReview/source-review.md` (receipts, commands, quotes). Verification log: `.ufo/waves/round-64/w1/SourceReview/verification-log.txt` (sha256 9a53a0ad2498330a0a59ad1470db37f644626f309ec7d970a414a79cf26bc99a). Captured bytes + HTTP headers stored beside it (`s230-test_outputs.py`, `s230-headers.txt`, `s231-grpc-python-api.html`, `s231-headers.txt`).

## S230 — TB2 kv-store-grpc grader at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 — VERIFIED
- Live fetch rc 0 (HTTP/2 200, 6076 bytes); sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` = frozen pinned sha; `cmp` byte-identical to lane capture `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` (rc 0); git blob `2bb04c15ea568ef2ac52cd778ca886a7f02ceff2`.
- Teaches claim holds: seven test functions live in exactly the frozen file order (`:15 :35 :50 :67 :83 :99 :138`); leg-5 fragment live at :96 (`Port 5328 is not listening - no real gRPC server is running`, port=5328 at :88); `except grpc.RpcError` at :128 only inside `test_grpc_protocol_handshake`, `test_grpc_server_functionality` has none — consistent with frozen K5 (leg-6 P, leg-7 F) and K2/K4 non-RpcError failure paths.

## S231 — gRPC Python API reference (grpc.RpcError, status codes) — VERIFIED
- Live fetch rc 0 (HTTP/2 200, 250738 bytes); sha256 `d68676105b4bbf7f701eb3458e95db7efd5fe6129408eba4b574dff23ea083e4`; last-modified Mon, 26 Oct 2026 06:32:10 GMT (unversioned page — digest recorded as the opening observation for recheck).
- Located quote (heading "exception grpc.RpcError", anchor `#grpc.RpcError`): "Raised by the gRPC library to indicate non-OK-status RPC termination." (10 words)
- Corroboration (anchor `#grpc.StatusCode.UNAVAILABLE`): "The service is currently unavailable." (5 words) — together they ground "an unavailable server surfaces as a Python exception on the RPC call", triangulated by the grader's own `except grpc.RpcError` at :128-129.
- Teaches claim holds: RpcError is the exception surface for gRPC status errors.

## Residual
S231 page is not commit-pinned; recheck by re-fetch + re-hash. Both rows are the L1's to write; this seat only opened and verified. Scope kept: two named network opens only, no installs, no ports bound, no lane files edited.
