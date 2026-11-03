# Leg reading — TB2 `kv-store-grpc` grader (read-only, from committed + live bytes)

Grader: `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py`
sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e`, 6076 bytes, 171 lines.
Live bytes fetched from `raw.githubusercontent.com/harbor-framework/terminal-bench-2@2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py`
are byte-identical (`cmp` rc 0) and hash-identical — see `../s230-verification.txt`.
Upstream runner is `tests/test.sh` (295 bytes): `pip install pytest==8.4.2 requests==2.32.5 psutil==7.0.0 pytest-json-ctrf==0.3.5`
then `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`; reward 1 iff pytest exit 0,
i.e. iff **all seven** tests pass. Pytest runs every test in file order and does not stop on failure,
which is what makes a per-case 7-cell vector well-defined and matches the frozen leg rule
("P iff the test function returns normally; F on any exception").

Module-level facts that apply to every leg: `sys.path.insert(0, "/app")` at line 12 (so `/app`
precedes site-packages on the import path — a file named `/app/grpc.py` would shadow the real
package), and only `socket`, `sys`, `pathlib` are imported at module level; `grpc` is imported
per-leg in legs 2, 6, 7.

## Leg 1 — `test_proto_file_creation` (line 15)

P iff `/app/kv-store.proto` exists (L21) **and** its decoded text contains, as plain substrings,
all five literals asserted at L28–L32: `service KVStore`, `rpc GetVal`, `rpc SetVal`,
`message GetValRequest`, `message SetValResponse`. Nothing is compiled, parsed or imported; the
proto is never handed to protoc, and the checks do **not** require `message SetValRequest`,
`message GetValResponse`, or any field declaration. A file whose only content were a comment
containing those five strings would pass. Consequence for the controls: the frozen K4 leg-1 P is
grounded in committed bytes — `corpus/evidence/round64/control-k4-kv-store.proto`
(sha256 `c89bcb1c…a50e0c`) carries each of the five literals exactly once
(`grep -c -- "<tok>"` → 1, five times; see `../control-crosscheck.txt`).

## Leg 2 — `test_grpc_tools_installation` (line 35)

P iff `import grpc` (L42) completes; the only explicit failure path is `except ImportError` →
`assert False` (L47), and any other exception also counts as F under the frozen leg rule. The
import resolves against the interpreter running the grader — the probe-owned venv that the
receipt names — **not** against `/app`, so this leg is P for every case by probe-environment
construction. It therefore carries no information about the candidate; the frozen vectors say so
explicitly (K2 = `F P F F F F F`). It is also the one leg that could be defeated by import
shadowing (`/app/grpc.py`), which no frozen case contains.

## Leg 3 — `test_protobuf_generation` (line 50)

P iff **both** `/app/kv_store_pb2.py` (L59) and `/app/kv_store_pb2_grpc.py` (L62) exist. Existence
only: the files are never opened, imported, parsed or executed by this leg, so a zero-byte or
stale pair passes here and only fails later, inside legs 6–7's imports.

## Leg 4 — `test_server_file_creation` (line 67)

P iff `/app/server.py` exists (L73) **and** its text contains the literal `class Server` (L80).
Text check only; the module is never imported, so a syntax-broken `server.py` containing that
literal passes this leg.

## Leg 5 — `test_real_grpc_server_running` (line 83)

P iff a TCP connect succeeds: an `AF_INET`/`SOCK_STREAM` socket with `settimeout(5)` (L91–92) does
`connect_ex(("127.0.0.1", 5328))` and asserts `result == 0` (L93–96); the failure message is
`f"Port {port} is not listening - no real gRPC server is running"` — the string the R64-C1
predicate names. The check is **not** gRPC-specific: any listener accepting on `127.0.0.1:5328`
earns P, whether it speaks HTTP, gRPC, or nothing at all. `connect_ex` returns 0 on a completed
handshake only, so a closed port yields `ECONNREFUSED` immediately rather than a 5 s wait.

## Leg 6 — `test_grpc_protocol_handshake` (line 99)

The three imports — `grpc`, `kv_store_pb2`, `kv_store_pb2_grpc` (L104–106) — sit **outside** the
`try:` that begins at L114, so an import failure is an uncaught exception → F; this is exactly the
`ModuleNotFoundError: No module named 'kv_store_pb2'` recorded for K2/K4. Inside the try the leg
builds `KVStoreStub(channel)` (L116), calls
`stub.SetVal(SetValRequest(key="handshake", value=999))` (L120) with **no deadline**, then asserts
`hasattr(response, "val")` (L123) and `response.val == 999` (L124). Three outcome paths:
(i) a proper response with `val == 999` → print, P; (ii) `except grpc.RpcError` (L128) → print, P —
**any** RpcError is a pass, including UNAVAILABLE raised by a dead listener; (iii) `except Exception`
(L131) → `assert False`, F — which also swallows the AssertionError from L124, so a value mismatch
is F with the message text of L133, not of L124. `finally` closes the channel (L135).

## Leg 7 — `test_grpc_server_functionality` (line 138)

Imports at L143–145 are again outside the try, and the channel and stub are built outside it too
(L151–152). Inside `try` (L154) four asserts run in order: `SetVal("test_key", 42).val == 42`
(L157), `GetVal("test_key").val == 42` (L161), `SetVal("test_key", 100).val == 100` (L165),
`GetVal("test_key").val == 100` (L168). There is **no** `except` at all — only `finally:
channel.close()` (L170) — so any exception, RpcError included, propagates and the leg is F. The
leg therefore demands echo semantics on `SetVal` **and** overwrite semantics for an existing key;
a store-if-absent implementation fails at L161/L168, and a `value+1` implementation fails at L157.

## How the frozen vector cells follow from the code (mechanism, not observation)

| case | leg-1 | leg-2 | leg-3 | leg-4 | leg-5 | leg-6 | leg-7 |
|---|---|---|---|---|---|---|---|
| K1 compliant | P: proto text | P: venv | P: both files | P: `class Server` | P: 5328 listening | P: L124 `val==999` | P: four asserts pass |
| K2 empty | F: L21 | P: venv | F: L59 | F: L73 | F: L96 fragment | F: L105 import | F: L144 import |
| K3 wrong-math | P | P | P | P | P | F: L124 (`1000≠999`) → L133 | F: L157 (`43≠42`) |
| K4 proto-only | P: K4 bytes | P | F: L59 | F: L73 | F: L96 | F: L105 import | F: L144 import |
| K5 files-no-server | P | P | P | P | F: L96 | P: L128 RpcError | F: uncaught RpcError |

K2 and K4 rows are not predictions: they are the committed captures, re-parsed with
`json.loads` on the `LEGS` line — `F P F F F F F` and `P P F F F F F`, both matching the frozen
vectors, with K2's leg-5 message containing `Port 5328 is not listening` verbatim
(`grep -c -F` → 1). See `../control-crosscheck.txt`.

S231 grounds the K5 leg-6 cell: the page documents `exception grpc.RpcError` as "Raised by the
gRPC library to indicate non-OK-status RPC termination" (`#grpc.RpcError`), a non-OK unary call as
`Raises: RpcError – Indicating that the RPC terminated with non-OK status … affording the RPC's
metadata, status code, and details` (`#grpc.UnaryUnaryMultiCallable.__call__`), and
`UNAVAILABLE` as a `grpc.StatusCode` documented "The service is currently unavailable"
(`#grpc.StatusCode.UNAVAILABLE`). Closed empirically on this host with grpcio 1.85.1: a unary call
to a dead loopback port raises `_InactiveRpcError`, `isinstance(e, grpc.RpcError) is True`,
`e.code() == StatusCode.UNAVAILABLE` (`../s231-empirical-rpcerror.txt`).

## Flags — where a frozen vector cell could turn ambiguous

**F1 (highest risk) — K3 leg 6 is pinned to an implementation detail, not just "wrong math".** The
frozen `P P P P P F F` holds only if the K3 server's `SetVal` *response* carries the perturbed
value (`1000`), tripping L124. If the K3 fixture stores `value+1` but returns the request value
(`999`), leg 6 takes the success path at L123–L124 and is P, giving `P P P P P P F` — a vector that
differs from the frozen row and, by kill rule, a MISS. The builder must implement
`store[key] = value + 1; return stored`, not "perturb on read".

**F2 — K5 leg 6 is a property of importability, not of presence.** Leg 3 only checks existence, so
K5's leg-3 P says nothing about whether `import kv_store_pb2` (L105) succeeds. If K5's generated
modules are stale or built against a different protobuf gencode version than the probe venv, the
import raises (`ModuleNotFoundError`/`TypeError`) before the `try`, leg 6 becomes F, and the
observed K5 vector becomes `P P P P F F F` instead of the frozen `P P P P F P F`. The K5 fixture
must ship modules generated by the same grpcio-tools/protobuf version as the grader's venv.

**F3 — leg 5 is not gRPC-specific, so between-case teardown is vector-critical.** Any listener on
`127.0.0.1:5328` earns P. The frozen predicate requires the port free only **at battery start**;
it says nothing about between cases. If a case's server is not killed (and the port not re-checked)
before the next case, K2/K4/K5 leg 5 flips to P and three vectors differ at once. The probe should
kill the recorded PID and re-assert `ss -ltn` shows 5328 free between cases, and record that in the
receipt — as extra evidence, without editing the frozen predicate.

**F4 — legs 6 and 7 call `stub.SetVal` with no deadline.** A listener that accepts TCP but never
answers gRPC would hang the leg, which is neither P nor F. Not reachable for the frozen five cases
(K1/K3 are real gRPC servers; K2/K4/K5 refuse or have no listener), but the probe should bound each
leg's wall clock so a hang is recorded as a distinct outcome instead of stalling the battery.

**F5 — leg 6 swallows its own value-mismatch assertion.** L124's AssertionError is caught at L131
and re-raised as `assert False` with the L133 message, so the receipt will read "AssertionError:
Not a real gRPC server: …" where the reader expects "must return the correct value". Cosmetic for
the cell (F either way) but it can be mistaken for an environment fault; the K3 receipt should be
read with that in mind.

**F6 — leg 1 is substring matching.** It cannot distinguish a valid proto from any text carrying
the five literals; and it omits `setValRequest`/`GetValResponse` messages, so a proto that cannot
even be compiled can pass leg 1. Soundness note only (S230's scope is the grader's contract as
written), not a vector risk for K1/K3/K4/K5, whose protos are real.

**F7 — one process per case is load-bearing.** `sys.path.insert(0, "/app")` runs once per module
import. If a probe ever reused one process across cases, leg 6/7 could resolve `kv_store_pb2`
from the previous case's `/app` and report a false P. The claims freeze "one sandbox process per
case"; that is a build requirement, not an optional detail.

**F8 — leg 2's cell is environmental.** It is P for all five cases because the venv carries
grpcio; a reader who takes it as candidate evidence would over-read the vector. Already stated in
the claims; repeated here so the receipt's K2/K3 rows are not misread.

## Residual unknowns (not resolvable from the bytes I may read)

1. The K1/K3/K5 case apps do not exist yet (the probe seat builds them), so their leg-1 text and
   leg-3/4 files cannot be inspected now; only the mechanism above is established.
2. Whether `kv_store_pb2` and `kv_store_pb2_grpc` as generated by grpcio-tools 1.85.1 import
   cleanly under the probe venv is asserted by the L1 dry-run, not by me; I confirmed only that
   `import grpc` works (1.85.1, cp314) and that the RPC path raises RpcError as documented.
3. The upstream harness's pytest invocation is captured in `test.sh`, but the probe's frozen shape
   uses its own `/ctl/driver.py`; exact pytest-vs-driver equivalence for assertion rewriting is
   untested here (pytest only rewrites assertion messages, not pass/fail, so no vector risk).
