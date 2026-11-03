# ProbeBuild — R64-C1 `kv-store-grpc` offline probe (round 64, w1)

Seat: ProbeBuild. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Seat dir: `.ufo/waves/round-64/w1/ProbeBuild/`. Scratch (removed before yield):
`/fast/scratch/hyaku/kengaku-r64/ProbeBuild`.

## Deliverables (all in the seat dir)

| file | what |
|---|---|
| `round64_c1_kvstore_probe.py` | the instrument (version `r64-c1/1`) |
| `kvstore-probe.txt` | receipt of record, battery run 1 |
| `kvstore-probe.txt.server-log` | raw server log sidecar for run 1 |
| `kvstore-probe-rerun.txt` | determinism run 2 |
| `kvstore-probe-rerun.txt.server-log` | raw server log sidecar for run 2 |
| `determinism.txt` | cmp of `^(VECTOR|PREDICATE)` lines + both receipt sha256 |
| `check-receipt.txt` | `--check-receipt` output on both receipts, with exit codes |
| `selftest.txt` | `--selftest` output (7 fixtures, exit 0) |

## Instrument

Runs the pinned grader's own seven test functions in file order, in one bwrap process
per case, against five frozen cases. Grader bytes are re-hashed at run time
(`sha256 115de2e9…b0e`) and the `def test_*` order is extracted from the file and
compared to the frozen leg list; drift is SETUP. The pb2 modules are generated in a
separate sandbox exec by the probe-owned venv:

```
/venv/bin/python -m grpc_tools.protoc -I/app --python_out=/app --grpc_python_out=/app /app/kv-store.proto
```

Service cases start `/app/server.py` from the case driver inside the sandbox, which
poll-connects to 127.0.0.1:5328 for at most 10 s, prints `SERVERPID <pid>` before the
first leg, runs the seven legs with a 120 s per-leg alarm, kills the server, verifies
it exited, and reads `/app/server.log` (`SERVER UP 5328`). The probe records
`ss -ltn` (plus a bind test) FREE before the battery, before each case and after each
case; it refuses (exit 2, `SETUP port-5328-occupied`) rather than grade through a
foreign listener, and only ever kills a recorded PID whose `/proc/<pid>/cmdline` names
`/app/server.py`. bwrap runs in the host PID namespace here (NSpid single entry), so
the driver's SERVERPID is a host PID.

Exit map: 0 pass / 1 predicate fail / 2 usage or SETUP. K2 leg-5 P while the probe
saw the port free is refused as SETUP (`k2-leg5-answered-with-port-free`), per the
frozen kill rule.

## Observed vs frozen (receipt of record `kvstore-probe.txt`)

| case | observed | frozen | match |
|---|---|---|---|
| K1 | `P/P/P/P/P/P/P` | `P/P/P/P/P/P/P` | yes |
| K2 | `F/P/F/F/F/F/F` | `F/P/F/F/F/F/F` | yes |
| K3 | `P/P/P/P/P/F/F` | `P/P/P/P/P/F/F` | yes |
| K4 | `P/P/F/F/F/F/F` | `P/P/F/F/F/F/F` | yes |
| K5 | `P/P/P/P/F/P/F` | `P/P/P/P/F/P/F` | yes |

Evidence lines from `kvstore-probe.txt` (66 lines, 4708 bytes):

```
GRADER sha256=115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6
VENV python=3.14.8 grpcio=1.85.1 grpcio-tools=1.85.1
PORTFREE before-battery True
CASE K1 … server_pid=3561122 pid_before_legs=True server_ready=True server_log=SERVER_UP_5328
LEG K2 5 test_real_grpc_server_running F exc=AssertionError frag=Port 5328 is not listening - no real gRPC server is running
LEG K3 6 test_grpc_protocol_handshake F exc=AssertionError frag=Not a real gRPC server: gRPC server must return the correct value
LEG K3 7 test_grpc_server_functionality F exc=AssertionError frag=SetVal returned wrong value: 43
LEG K5 6 test_grpc_protocol_handshake P exc=- frag=-
LEG K5 7 test_grpc_server_functionality F exc=_InactiveRpcError frag=… StatusCode.UNAVAILABLE … Connection refused
K2-FRAGMENT Port 5328 is not listening - no real gRPC server is running
PREDICATE R64-C1 pass
```

K3's wrong-math server stores `request.value + 1`, so the handshake's
`response.val == 999` assertion fails inside the grader's `except Exception` arm
(AssertionError) and functionality fails on `SetVal returned wrong value: 43` — the
frozen `P P P P P F F`. K5's leg 7 raises `_InactiveRpcError` (a `grpc.RpcError`
subclass), matching the frozen `F`; leg 6 tolerates it and is `P`.

## Commands run and verdicts

```
cd /fast/scratch/hyaku/kengaku-r64/ProbeBuild
TMPDIR=$PWD /usr/bin/python3 <seat>/round64_c1_kvstore_probe.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --work $PWD \
  --receipt <seat>/kvstore-probe.txt          # rc=0, PREDICATE R64-C1 pass
… --receipt <seat>/kvstore-probe-rerun.txt    # rc=0, PREDICATE R64-C1 pass
```

Determinism (`determinism.txt`): `cmp` of the five `VECTOR` lines + the `PREDICATE`
line from the two receipts → **rc=0** (byte-equal). Receipt sha256:

```
a87cd119784ed92c23ed6854e365b9a3d8e0b19954668b8579ceb4218c3b2842  kvstore-probe.txt
3e53a498e24a29cef68bc525923d771222d69e6dd6ce4e7c3d42560df9688cee  kvstore-probe-rerun.txt
```

The whole receipts differ only in PIDs/paths (K1 pids 3561122 vs 3561294); the
predicate text is identical, as required.

Receipt checker (`check-receipt.txt`):

```
$ python3 round64_c1_kvstore_probe.py --check-receipt <seat>/kvstore-probe.txt
CHECK ok cases=5
PREDICATE R64-C1 pass      rc=0
$ … --check-receipt <seat>/kvstore-probe-rerun.txt
CHECK ok cases=5
PREDICATE R64-C1 pass      rc=0
```

Selftest (`selftest.txt`, exit 0): `render-table observed=0 expected=0 pass`;
`valid-receipt 0/0 pass`; `tampered-vector 1/1 pass`; `no-server-pid 1/1 pass`;
`port-not-free 1/1 pass`; `no-k2-fragment 1/1 pass`; `missing-receipt 2/2 pass`.

Named limitation, stated in the receipt header and honored by the checker:
`--check-receipt` re-derives TEXT fields only; the live evidence is `server_pid` +
`server_log` (raw bytes in the `<receipt>.server-log` sidecar). The selftest's
synthesized receipts exercise checker mechanics only and prove nothing live.

## Freeze review check (before the scored battery)

`.ufo/waves/round-64/w1/FreezeReview/blockers.md` does not exist; the directory was
empty at 16:15 (`ls -la` showed only `.`/`..`). No blocker names this probe's counter,
so no counter fix was made and the instrument stays `r64-c1/1` (version in every
receipt header).

## For the L1 (integration)

1. Copy `round64_c1_kvstore_probe.py` → `plans/round64_c1_kvstore_probe.py`.
2. Copy `kvstore-probe.txt` + `kvstore-probe.txt.server-log` (BOTH; the receipt's
   `SERVERLOG file=` line names the sidecar) → `corpus/evidence/round64/`.
   Counting command then:
   `python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt`
   → `PREDICATE R64-C1 pass`, exit 0.
3. The probe needs only host `/usr/bin/python3`, `/usr/bin/bwrap`, `ss`, and `uv`
   (found on PATH or `~/.local/bin`); it creates its venv under `--work` and installs
   `grpcio`/`grpcio-tools` from PyPI into that venv. No host install, no pacman.

## Tooling

Installed by the probe into its scratch venv only (channel: `uv pip install`, PyPI):
`grpcio 1.85.1`, `grpcio-tools 1.85.1` (reason: the grader's runtime/protoc
environment). No system tools installed or upgraded; pacman untouched. `uv 0.13.0`,
`bwrap 0.13.1`, `ss`, `/usr/bin/python3 3.14.8` were already present.

## Risks / status

- No blockers. Observed vectors equal the frozen vectors on both runs; predicate passes.
- Port 5328 was free at each battery start (`PORTFREE before-battery True`), free
  before/after every case, and only probe-recorded server PIDs ever bound it.
- Residual risk (named): a text-only checker cannot distinguish a live run from a
  carefully forged receipt; the sidecar server log and PIDs are the live evidence.
- Scratch `/fast/scratch/hyaku/kengaku-r64/ProbeBuild` removed after copying every
  receipt named above into the seat dir.

Report: .ufo/waves/round-64/w1/ProbeBuild.md
