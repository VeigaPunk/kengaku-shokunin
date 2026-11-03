# GraderRecon — round 64, w1 (R64-C1 read-only reconnaissance)

Seat dir: `.ufo/waves/round-64/w1/GraderRecon/`. Scratch (`/fast/scratch/hyaku/kengaku-r64/GraderRecon`)
removed after every receipt was copied here. No lane file outside the seat dir was written; the
grader and corpus evidence were read only. Nothing was bound, listened on, or started on 5328/8080.

Verdicts: **S230 OPEN + byte-identical (PASS)**, **S231 OPEN (PASS, with a scope caveat)**,
**host state matches the L1's pre-freeze facts**, **leg reading complete with 8 flags — two of
them vector-critical (F1 K3-leg6, F2 K5-leg6)**.

## 1. S230 — TB2 `kv-store-grpc` grader at pin `2fd12b88`

`curl -sS https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py`
→ `http_code=200 size=6076`; `sha256sum` →
`115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e`, which is exactly the frozen sha,
exactly `SHA256SUMS` line 80, and `cmp` against
`corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` returns 0 (byte-identical).
Bytes kept at `GraderRecon/s230-test_outputs.py`; transcript `GraderRecon/s230-verification.txt`.

Two structural facts found while opening it (they change nothing frozen, they inform the probe):

- The grader dir holds `tests/test.sh` (295 bytes) as well: the upstream runner is
  `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA` with reward 1 iff exit 0 —
  i.e. all seven tests must pass, and pytest runs them all in file order without early stop. That
  is exactly the granularity the frozen leg rule assumes.
- `sys.path.insert(0, "/app")` at line 12 executes at module import, before any test; `/app`
  therefore precedes site-packages for legs 2/6/7's imports.

## 2. S231 — gRPC Python API reference (`grpc.github.io/grpc/python/grpc.html`)

`http_code=200 size=250738`; sha256 `d68676105b4bbf7f701eb3458e95db7efd5fe6129408eba4b574dff23ea083e4`;
bytes at `GraderRecon/s231-grpc-python.html`; quotes and anchors at `GraderRecon/s231-quotes.txt`.

| # | location (page section → anchor) | quote (words) |
|---|---|---|
| 1 | `gRPC Exceptions` → `exception grpc.RpcError` → `#grpc.RpcError` | "Raised by the gRPC library to indicate non-OK-status RPC termination." (10) |
| 2 | `Multi-Callable Interfaces` → `grpc.UnaryUnaryMultiCallable.__call__` → `#grpc.UnaryUnaryMultiCallable.__call__`, `Raises:` field | "Raises: RpcError – Indicating that the RPC terminated with non-OK status." (11); same field continues "…affording the RPC's metadata, status code, and details." (20) |
| 3 | `gRPC Status Code` → `grpc.StatusCode.UNAVAILABLE` → `#grpc.StatusCode.UNAVAILABLE` | "UNAVAILABLE – The service is currently unavailable." (6 + code name) |

**Scope caveat (must not be overstated in the S231 row or the lesson):** the page contains no
literal sentence of the form "UNAVAILABLE surfaces as RpcError". What it contains is (1) RpcError =
non-OK-status RPC termination, (2) a unary call raises RpcError on non-OK status and the raised
object carries the status code, (3) UNAVAILABLE is one `grpc.StatusCode`. The step from those three
to "a dead listener yields RpcError(UNAVAILABLE)" is an inference — so I closed it empirically:
grpcio 1.85.1 in a scratch venv, a client-only unary call to `127.0.0.1:5329` (verified closed by
`ss -ltnH`, never 5328) raised `_InactiveRpcError`, `isinstance(e, grpc.RpcError) is True`,
`e.code() == StatusCode.UNAVAILABLE`, details
`failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:5329: Failed to connect to remote host: Connection refused`
(`GraderRecon/s231-empirical-rpcerror.txt`, probe source
`GraderRecon/s231-empirical-rpcerror-probe.py`).

That is the K5 leg-6 grounding: `except grpc.RpcError` (line 128) tolerates exactly this exception,
which is why K5 leg 6 is frozen P while leg 7 (no `except`, line 154–170) is frozen F.

## 3. Host state (`GraderRecon/host-state.txt`)

`ss -ltn` shows **zero** matching listeners for 5328 and 8080 (`grep -cE '^(5328|8080)$'` on the
port field → 0; 38 listening sockets total, none on either port). `bwrap --version` →
`bubblewrap 0.13.1`; `/usr/bin/python3 --version` → `Python 3.14.8`;
`~/.local/bin/uv --version` → `uv 0.13.0 (x86_64-unknown-linux-gnu)`; `uname -srm` →
`Linux 7.2.11-arch1-1 x86_64`. Matches the L1's pre-freeze facts.

## 4. Leg reading (`GraderRecon/recon/leg-reading.md`)

One paragraph per leg with line-pinned PASS conditions, the mechanism table for all five frozen
vectors, and the controls re-parsed from their committed captures
(`GraderRecon/control-crosscheck.txt`): K2 → `F P F F F F F`, K4 → `P P F F F F F`, both equal to the
frozen rows; K2's leg-5 message contains `Port 5328 is not listening` verbatim (`grep -c -F` → 1);
the K4 control proto (sha `c89bcb1c…a50e0c`) carries all five leg-1 literals once each.

Key structural findings the probe builder must respect:

- Leg 1 is substring matching on five literals (L28–32) — no proto parse; `SetValRequest` and
  `GetValResponse` are not required.
- Leg 3 is existence-only (L59, L62): a K5 P here does **not** imply the modules import.
- Leg 5 is a bare TCP `connect_ex` (L91–96): any listener on 5328 passes, gRPC or not.
- Leg 6's imports (L104–106) are **outside** the try: an import failure is F, not tolerated.
- Leg 6 tolerates **any** RpcError (L128) and converts every other exception — including its own
  value-mismatch assertion — into F (L131–133).
- Leg 7 has no `except` at all (L154–170): demands echo on SetVal **and** overwrite of an existing key.

## 5. Flags — where a frozen vector cell could become ambiguous

1. **F1 (vector-critical) K3 leg 6.** Frozen `P P P P P F F` requires the K3 `SetVal` *response* to
   carry the perturbed value (`1000`), tripping L124. If K3 stores `value+1` but returns the request
   value (`999`), leg 6 passes L123–L124 and the observed row becomes `P P P P P P F` → vector
   mismatch → MISS by kill rule. Build K3 as `store[key]=value+1; return stored`.
2. **F2 (vector-critical) K5 leg 6.** Its P is a property of **importability** of `kv_store_pb2` /
   `kv_store_pb2_grpc` (L105–106), which leg 3 never tests. Stale or gencode-skewed modules make
   leg 6 F and K5 read `P P P P F F F`. Generate K5's modules with the same grpcio-tools/protobuf
   as the venv that runs the grader.
3. **F3 leg 5 is not gRPC-specific.** The frozen predicate only requires 5328 free *at battery
   start*; a server left alive between cases flips K2/K4/K5 leg 5 to P and three vectors at once.
   Kill the recorded PID and re-check the port between cases, and record it — evidence, not a rule
   change.
4. **F4 legs 6/7 have no client deadline** (`stub.SetVal` without timeout): an accept-but-silent
   listener hangs the leg (neither P nor F). Bound each leg's wall clock so a hang is a recorded
   outcome, not a stall.
5. **F5 leg 6 masks its own assertion text** (L131–133), so a K3 value mismatch will read
   "Not a real gRPC server: …" — a receipt-reading trap, not a vector risk.
6. **F6 leg 1 cannot distinguish a compilable proto from a text file** containing the five literals;
   leg 4 likewise only greps `class Server`. Soundness note on S230's scope as written.
7. **F7 one process per case is load-bearing** — `sys.path.insert(0,"/app")` is per import; reuse of
   one process across cases could resolve a previous case's `kv_store_pb2` and report a false P.
8. **F8 leg 2 is environmental** (P in all five cases because the venv carries grpcio); read K2/K3
   rows accordingly.

## 6. Tooling record

- `grpcio 1.85.1` (+ dependency `typing-extensions 4.16.0`) — channel: `uv pip install` into a
  venv created with `uv venv --python /usr/bin/python3` under my scratch — reason: empirically
  confirm that a unary call to a dead loopback port raises `grpc.RpcError` with
  `StatusCode.UNAVAILABLE` (the K5 leg-6 prediction). Venv removed with the scratch dir.
- `uv 0.13.0` already present at `~/.local/bin/uv` — used, not installed.
- No pacman transaction was run; nothing was installed system-wide.

## 7. Residual unknowns

1. The K1/K3/K5 case apps do not exist yet, so their concrete bytes cannot be inspected; only the
   grader-side mechanism is established here (that is the whole question this seat was given).
2. I confirmed `import grpc` works under cp314 and that the RPC failure path is `_InactiveRpcError`;
   I did **not** build the probe venv or generate pb2 modules (out of this seat's scope — the
   ProbeBuild seat owns that, and the L1 dry-ran the install).
3. pytest-vs-driver equivalence is assumed from the frozen shape; pytest's assertion rewriting only
   alters failure messages, not pass/fail, so no vector risk is expected.

## 8. Files (sha256, see `GraderRecon/seat-manifest.txt`)

| file | sha256 (prefix) |
|---|---|
| `GraderRecon/s230-test_outputs.py` | `115de2e9…b1b0e` (= frozen sha) |
| `GraderRecon/s230-verification.txt` | `8002ebc5…` |
| `GraderRecon/s231-grpc-python.html` | `d6867610…83e4` |
| `GraderRecon/s231-quotes.txt` | `88312c5f…` |
| `GraderRecon/s231-empirical-rpcerror.txt` | `65968f3f…` |
| `GraderRecon/s231-empirical-rpcerror-probe.py` | `67c17664…` |
| `GraderRecon/host-state.txt` | `56702923…` |
| `GraderRecon/control-crosscheck.txt` | `5ee514bd…` |
| `GraderRecon/recon/leg-reading.md` | `100b0acd…` |
| `GraderRecon/seat-manifest.txt` | `cdba5f0c…` |
