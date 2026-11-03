source: S230 (TB2 kv-store-grpc grader at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6) — corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py; and S231 (gRPC Python API reference, grpc.RpcError) — https://grpc.github.io/grpc/python/grpc.html#grpc.RpcError
verified-at: 2026-11-03
recheck: sha256sum corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py  # 115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e

# TB2 `kv-store-grpc` — a network-service grader replayed offline against a lane-built gRPC server

## What the grader asserts

The grader is Terminal-Bench 2.0 task `kv-store-grpc`'s `tests/test_outputs.py` at pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`: sha256
`115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` — the lane's committed
capture `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` and
`corpus/evidence/round52/graders/SHA256SUMS` line 80 (`./kv-store-grpc/tests/test_outputs.py`).
Seven test functions, graded in file order (S230 line numbers):

| # | leg (S230 line) | PASS condition (the grader's own asserts) |
|---|---|---|
| 1 | `test_proto_file_creation` :15 | `/app/kv-store.proto` exists (:21) **and** its text contains `service KVStore` (:28), `rpc GetVal` (:29), `rpc SetVal` (:30), `message GetValRequest` (:31), `message SetValResponse` (:32) |
| 2 | `test_grpc_tools_installation` :35 | `import grpc` succeeds (:42, inside `try:` :40); an `ImportError` asserts false with `grpcio was not installed by the agent` (:47) |
| 3 | `test_protobuf_generation` :50 | `/app/kv_store_pb2.py` (:59) **and** `/app/kv_store_pb2_grpc.py` (:62) both exist |
| 4 | `test_server_file_creation` :67 | `/app/server.py` exists (:73) **and** its text contains `class Server` (:80) |
| 5 | `test_real_grpc_server_running` :83 | TCP `connect_ex(("127.0.0.1", 5328))` returns 0 (:88,:93); else `AssertionError: Port 5328 is not listening - no real gRPC server is running` (:96) |
| 6 | `test_grpc_protocol_handshake` :99 | `stub.SetVal(key="handshake", value=999)` (:120) returns a response whose `.val == 999` (:123-124) — **or** the call raises `grpc.RpcError`, which is caught and tolerated (:128-130) |
| 7 | `test_grpc_server_functionality` :138 | `SetVal(42)`→42, `GetVal`→42, `SetVal(100)`→100, `GetVal`→100 (:156-168); **no** `RpcError` tolerance — only `finally: channel.close()` (:170-171) |

Leg rule (frozen in `plans/round-64-claims.md`): **P** iff the test function returns
normally, **F** on any exception. Leg 2 is P for every case by probe-environment
construction (the probe's venv carries grpcio) — part of the frozen vector, not an accident.

## Why this is a `network-service` grader (and why the class row is the one that flips)

The round-62 census receipt prices the task into the `network-service` class:
`corpus/evidence/round62/class-survey.txt` line 11 — `CLASS network-service count=8
members=filter-js-from-html,git-multibranch,headless-terminal,hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server`.
The census's frozen detector is a line regex over the grader text
(`plans/round62_c1_class_survey.py` :93 — `\bsocket\.|\brequests\.(get|post)\b|\burllib\b|http\.client|\burlopen\b|localhost:[0-9]|127\.0\.0\.1`)
and the grader's own bytes carry `127.0.0.1` and `port = 5328` (S230 :88,:93,:109).
It cannot be replayed as a file-artifact grader: two of its seven legs (5 and 6) reach a
live loopback service.

Two scope facts the census also records, kept here so the class row is not over-read:
the same census prices `kv-store-grpc` under **file-artifact** as well (line 7 — the
classifier is multi-label, not exclusive), and at base `kv-store-grpc` was **not**
executed — `grep -c kv-store-grpc corpus/evidence/round52/graders/executed17.lst` → `0`,
rc 1 (receipt `.ufo/waves/round-64/claims/before-state.txt`), with the census line
`EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12
classes-uncovered=network-service,process-environment,db-state,container-image`
(class-survey.txt line 21).

## The frozen five-case × seven-leg prediction

`plans/round-64-claims.md` lines 65-71 freeze five cases and their vectors (K1 compliant,
K2 do-nothing control, K3 wrong-math, K4 proto-only control, K5 files-complete / no
server):

| case | setup | frozen vector (legs 1-7) |
|---|---|---|
| K1 | compliant: proto + generated pb2 + `server.py` (echo semantics) + server running on 5328 | `P P P P P P P` |
| K2 | do-nothing control (L1-measured pre-freeze): empty `/app`, no server | `F P F F F F F` |
| K3 | wrong-math: server stores `value+1` on SetVal | `P P P P P F F` |
| K4 | proto-only control (L1-measured pre-freeze): only `kv-store.proto` present | `P P F F F F F` |
| K5 | files-complete, server never started | `P P P P F P F` |

**Predicate R64-C1 (frozen, `plans/round-64-claims.md` lines 92-96):** pass iff, in the
receipt of record, the observed 7-leg vector for each case K1-K5 equals the frozen vector
above, **and** the K2 receipt records the captured leg-5 failure fragment `Port 5328 is not
listening`, **and** the receipt records that port 5328 was free at battery start and that
the K1 server PID was recorded by the probe before the handshake leg ran.

Counting command (`plans/round-64-claims.md` line 99):
`python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt; echo $?`
→ last line `PREDICATE R64-C1 pass`, exit 0.

### The two pre-freeze controls, with their committed digests

K2 and K4 were measured **before** the freeze and their bytes are committed:

- `corpus/evidence/round64/k2-empty-capture.txt` — sha256
  `ae0a78ee657108a697fae965dc71e7d79f80cd9850d9ec00b2261ba2476f9887`; `LEGS` vector
  `F P F F F F F`. Its leg-5 line is the frozen fragment source:
  `["test_real_grpc_server_running", "F", "AssertionError: Port 5328 is not listening - no real gRPC server is running"]`.
- `corpus/evidence/round64/k4-protoonly-capture.txt` — sha256
  `b262cfe5791cfb93d115a021a8ed392b5a60c07c8f6426dfb8b5b1f9964e4bdb`; `LEGS` vector
  `P P F F F F F`.
- the K4 input bytes `corpus/evidence/round64/control-k4-kv-store.proto` — sha256
  `c89bcb1c3b3da00b437a721d7f9d7b76bd778ca567ca1c077f21339fc8a50e0c` (a `service KVStore`
  with `GetVal`/`SetVal` and the four request/response messages).

K2 is not K1: its vector differs in 6 of 7 legs, so a do-nothing run cannot satisfy the
frozen predicate.

## The K5-leg-6 vs K3-leg-6 asymmetry, in the grader's own `except` structure

The handshake leg is the only leg with an exception handler. S230 :128-133:

```python
    except grpc.RpcError:
        # gRPC errors are expected and indicate real gRPC protocol
        print("✓ gRPC protocol detected")
    except Exception as e:
        # Any other exception means it's not a real gRPC server
        assert False, f"Not a real gRPC server: {e}"
```

`test_grpc_server_functionality` (:138) has **no** `except` clause at all — only
`finally: channel.close()` (:170-171). Three consequences, all observable in the vectors:

1. **K5 leg 6 = P, leg 7 = F.** With the files complete but no server, the handshake's
   `stub.SetVal` cannot succeed, so a transport error is raised — and the receipt shows leg 6
   surfacing **no** exception (`LEG K5 6 test_grpc_protocol_handshake P exc=- frag=-`), which
   is only consistent with the `except grpc.RpcError` arm swallowing it and the leg
   returning normally. Leg 7 has no such arm, so the same error propagates and the leg
   fails, and the receipt names it exactly: `LEG K5 7 test_grpc_server_functionality F
   exc=_InactiveRpcError frag=<_InactiveRpcError of RPC that terminated with: status =
   StatusCode.UNAVAILABLE ... Connection refused>`. S231 is the ground for that exception
   type: `grpc.RpcError` is "Raised by the gRPC library to indicate non-OK-status RPC
   termination" (S231, heading `exception grpc.RpcError`), and `UNAVAILABLE` is "The service
   is currently unavailable" (S231, heading `UNAVAILABLE`) — a non-OK status, hence an
   `RpcError`. (The S231 quotes are the located quotes of the S231 row, opened live by the
   round's recon and source-review seats; see their receipts in
   `.ufo/waves/round-64/w1/GraderRecon/s231-quotes.txt` and
   `.ufo/waves/round-64/w1/SourceReview/source-review.md`.)
2. **K3 leg 6 = F, not P.** The wrong-math server answers, so no `RpcError` is raised; the
   `assert response.val == 999` (:124) fires `AssertionError`, which is *not* an
   `RpcError`, so it lands in `except Exception` and is re-raised as
   `Not a real gRPC server: gRPC server must return the correct value` (:133). Leg 7 fails
   on its own arithmetic (`SetVal returned wrong value: 43`, :157).
3. **K2/K4 legs 6 and 7 = F with `ModuleNotFoundError`, not tolerated.** In leg 6 the
   `import kv_store_pb2` / `import kv_store_pb2_grpc` statements sit at S230 :105-106,
   **outside** the `try:` that opens at :114; in leg 7 the same two imports are at :144-145,
   outside the `try:` at :154. A missing generated module therefore raises before any
   handler can see it: `ModuleNotFoundError: No module named 'kv_store_pb2'`.

So the handshake leg tolerates a *transport* failure and fails a *semantic* one; that is
the whole difference between K5 leg 6 and K3 leg 6, and it is a property of the grader's
`except` structure, not of the candidate.

## The named limitation of `--check-receipt`

`--check-receipt` re-derives **text fields only**; it cannot prove a live run (carried
r63 routed defect 4, `plans/round-64-claims.md` lines 102-105). The live evidence is the
server-side log the probe captures from the process it started — receipt field `server_log`
plus `server_pid` — copied into the wave evidence dir beside the receipt as the
`<receipt>.server-log` sidecar. Wherever the checker is cited, this limitation is named.

## The scored run (observed)

The receipt of record is the hardened battery at the frozen counting path
`corpus/evidence/round64/kvstore-probe.txt` (sha256
`7aa652e590b31b30d87194b2ecae446203ef32153de03497debb121ddd227303`; the live-evidence
sidecar `corpus/evidence/round64/kvstore-probe.txt.server-log`, sha256
`b19d39b44cdbda85024dd729e8ac2b5e206ad69ece348f016018aee076148898`). It records:

```
VECTOR K1=P/P/P/P/P/P/P
VECTOR K2=F/P/F/F/F/F/F
VECTOR K3=P/P/P/P/P/F/F
VECTOR K4=P/P/F/F/F/F/F
VECTOR K5=P/P/P/P/F/P/F
PREDICATE R64-C1 pass
```

— the five observed vectors equal the five frozen vectors above. The same receipt records
`PORTFREE before-battery True` (and `PORTFREE before|after <case> True` for each case), the K1
`server_pid=3721648` with `pid_before_legs=True`, the K3 `server_pid=3722817` with
`pid_before_legs=True`, the K2 leg-5 fragment line
`K2-FRAGMENT Port 5328 is not listening - no real gRPC server is running`, and the
per-leg exception class and message fragment for every leg (e.g. K3 leg 6
`AssertionError: Not a real gRPC server: gRPC server must return the correct value`; K5
leg 7 `_InactiveRpcError ... StatusCode.UNAVAILABLE ... Connection refused`).

The receipt was produced by the install-hardened probe (`plans/round64_c1_kvstore_probe.py`,
sha256 `a1ccb82d5166fdf2332a0d61173621bf5b27955c56b779394e7f889e301c7907`). Its predecessor
runs — the wave's first battery and its determinism rerun, with the ambient install environment
— are kept byte-for-byte under `corpus/evidence/round64/prehardening/`. Their predicate lines are
identical to the hardened run's (five `VECTOR` lines and `PREDICATE R64-C1 pass`). Measured
(`diff prehardening/kvstore-probe.txt kvstore-probe.txt`, 4 changed lines): the two receipts
differ only in the K1 and K3 `server_pid` fields of their CASE lines; the install environment
is not a receipt field and is not in the diff. Determinism claimed from
the pre-hardening pair only: `grep -E '^(VECTOR|PREDICATE)'` on both pre-hardening receipts and
`cmp` gives rc 0. The hardened receipt is a single run, and no second hardened run is claimed.

The probe's own selftest receipt (`corpus/evidence/round64/selftest.txt`, sha256
`690088eaf105fc1e24a3bbad5d8ef9937757aaa46bd2b54d220e43d43e857fae`) ends `SELFTEST pass`,
rc 0, over seven cases (render-table, valid-receipt, tampered-vector, no-server-pid,
port-not-free, no-k2-fragment, missing-receipt) — including the `missing-receipt` case exiting
2 (`SETUP receipt-missing ...`).


## The pypi-server R63-C1 MISS of record is unchanged

This entry changes nothing about the previous network-service replay.
`corpus/knowledge/tb2-network-service-offline-grader.md` (S228/S229, `pypi-server`) and
its receipt of record `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt`
stand as they are: R63-C1 is a **MISS** on the frozen stderr clause, the amended-detector
runs are evidence only, and the L0 question `kengaku | round-63` stays open. The
`network-service` class row in SKILL.md's decision table was and remains
`recipe-unexecuted` **for pypi-server**; what round 64 adds is a second, independent
member (`kv-store-grpc`) executed under its own frozen predicate. The r63 depth gate's
counts are untouched by this entry.

## NOT claimed

- **No claim that the grader is solvable by any model.** This entry prices a *replay*: the
  probe stands up the service the grader expects and reads the grader's own verdict. It
  says nothing about whether a model can pass `kv-store-grpc`.
- **No claim about the task's own `tests/test.sh` wrapper** (`SHA256SUMS` line 81,
  `c348467a076bf614d0a850e25b2263f85bbf7b4c7a8d344fbd5454a0611a0df8`) — the lane's capture
  holds it as bytes, but it was not opened, read or characterized here.
- **No claim that the other seven `network-service` graders are replayable.** Only
  `kv-store-grpc` was executed this round; `pypi-server`'s own replay remains a MISS of
  record.
- **No claim about the host's 5328 beyond the port discipline.** The probe records
  `ss -ltn` free before the battery and after every case and refuses
  (`SETUP port-5328-occupied`, exit 2) rather than grading through a foreign listener; the
  only listener on 5328 during the run was the one the probe started, killed by the probe.
- **No claim that S231's bytes are pinned.** The gRPC Python API reference is a live
  unversioned docs page; its digest (`d68676105b4bbf7f701eb3458e95db7efd5fe6129408eba4b574dff23ea083e4`,
  opened 2026-11-03 by the round's recon and source-review seats) is an observation of one
  opening, not a stable pin.
- **No claim that `--check-receipt` proves a live run** — see the named limitation above.

## Carried forward

The entry extends `corpus/knowledge/tb2-network-service-offline-grader.md` (the first
network-service replay, pypi-server) and `corpus/knowledge/tb2-grader-class-census.md`
(the 16-class census that prices this grader). It adds the class's second executed member
and the first replay of a `network-service` grader whose service dependency is a real gRPC
server the lane builds (proto + `grpcio-tools` generation + `server.py`).
