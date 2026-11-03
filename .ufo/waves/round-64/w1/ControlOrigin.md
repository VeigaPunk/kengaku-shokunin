# ControlOrigin — independent re-derivation of the pre-freeze controls (round 64, w1)

Seat: ControlOrigin. Scope: guard against L1 control fabrication by rebuilding the K2/K4
controls from the claims doc text alone, with a runner I wrote, in my own venv, inside the
house bwrap shape. Nothing here edits a frozen rule; no frozen vector was re-frozen.

## Verdicts

| control | frozen vector | committed capture | my observation | verdict |
|---|---|---|---|---|
| K2 (empty `/app`, no server) | `F P F F F F F` | `F P F F F F F` | `F P F F F F F` | **MATCH** |
| K4 (only committed `kv-store.proto` bytes) | `P P F F F F F` | `P P F F F F F` | `P P F F F F F` | **MATCH** |

Leg-level: **14/14 legs exact** (function name, P/F, exception class, message string) across the
two cases — `receipts/comparison.txt` `SUMMARY legs_compared=14 exact_matches=14 mismatches=0`.
Divergence: **none**. No finding against the freeze's controls.

Frozen K2 leg-5 fragment `Port 5328 is not listening - no real gRPC server is running`:
observed verbatim in both K2 and K4 (`LEG5_FRAGMENT_CONTAINED_K2 True`,
`LEG5_FRAGMENT_CONTAINED_K4 True`). Legs 6 and 7 fail on `ModuleNotFoundError: No module named
'kv_store_pb2'` in both, matching the captures and the claims' statement that only `grpc.RpcError`
is tolerated by leg 6's `except` structure.

## Rig (mine, built from the claims doc text; the L1 probe driver was never opened)

- `receipts/driver.py` (sha256 `86fdbdb403093e6fd1294c83175c031c1dc3ada99744b4f3e20a9c6a8b77236d`):
  loads `/tests/test_outputs.py` via `importlib.util.spec_from_file_location`, derives the leg
  order from the module source with `ast` (top-level `def test_*`, source order) — not a
  hard-coded list and no pytest/harness import — calls each function in one process, records
  `P` on normal return and `F` on any `BaseException` with class, message and the failing source
  line, then prints `LEGS`, `LEGS_VECTOR`, `LEG5_MESSAGE`, `LEG6_MESSAGE`. It also prints the
  in-sandbox grader sha256, which matched the pin.
- venv: `uv venv --python /usr/bin/python3` in scratch, then `uv pip install grpcio==1.85.1
  grpcio-tools==1.85.1` → resolves `protobuf==7.36.2` (`receipts/pip-freeze.txt`). cp314 venv,
  as the claims require (`--python /usr/bin/python3`; a uv-managed default python resolves
  outside the sandbox).
- Sandbox: the house shape verbatim —
  `bwrap --die-with-parent --new-session --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin --symlink usr/lib /lib --symlink usr/lib /lib64 --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --dir /app --bind <case-app> /app --dir /tests --ro-bind <grader> /tests/test_outputs.py --dir /venv --ro-bind <venv> /venv --dir /ctl --ro-bind driver.py /ctl/driver.py -- /venv/bin/python /ctl/driver.py`
  with network shared (no `--unshare-net`).
- Case inputs: K2 = empty dir (`find` listed no files); K4 = a dir holding exactly one file,
  the committed `control-k4-kv-store.proto` copied in as `kv-store.proto`, sha256
  `c89bcb1c3b3da00b437a721d7f9d7b76bd778ca567ca1c077f21339fc8a50e0c` (matches the freeze).
- Port discipline: `ss -ltn` showed no listener on 5328 (or 8080) before and after; this seat
  never bound, listened on, or started a server; grader leg 5 only does `connect_ex` and got the
  refusal it asserts on. Two unrelated host python listeners on 39101/39102 were observed and
  untouched.

## Evidence chain (commands → receipts, all written by this seat)

- `sha256sum` of grader / both captures / K4 proto → all four equal the frozen pins
  (`receipts/host-state.txt`; grader `115de2e9…b1b0e`, K2 `ae0a78ee…9887`, K4 `b262cfe5…4bdb`,
  proto `c89bcb1c…5e0c`).
- K2 bwrap run → `receipts/k2-run.txt` (`LEGS_VECTOR F P F F F F F`, `BWRAP_RC 0`,
  in-sandbox `GRADER_SHA256 115de2e9…`).
- K4 bwrap run → `receipts/k4-run.txt` (`LEGS_VECTOR P P F F F F F`, `BWRAP_RC 0`).
- Comparison → `receipts/comparison.txt` (per-leg MATCH lines + summary + fragment containment).
- Environment/pins → `receipts/host-state.txt`; driver → `receipts/driver.py`; packages →
  `receipts/pip-freeze.txt`.

## Supplementary discriminator (not a claims control, changes no frozen vector)

To test that K4 leg-1 `P` derives from the committed bytes rather than from file existence alone,
I ran one extra sandbox case with the same proto minus the `rpc SetVal` line (359 vs 413 bytes):
vector `F P F F F F F` with leg-1 `AssertionError: Proto file must define SetVal RPC`
(`receipts/k4mut-run.txt`). This shows leg 1 really reads the content, so the committed K4 `P`
is content-earned — consistent with, and no evidence against, the freeze.

## Independent observations worth recording (no action requested)

1. `test_grpc_tools_installation` (leg 2) does not verify grpcio-tools at all — it imports
   `grpc` and prints the check mark. In every case it measures the probe's own venv, so its `P`
   is environment-constructed exactly as the claims state; the claim does not rely on it for
   substance.
2. Legs 6/7 import `kv_store_pb2` from `/app` (module `sys.path.insert(0, "/app")` in the
   grader), so any case without generated bindings fails before touching the network — the
   K2/K4 `ModuleNotFoundError` captures are therefore order- and environment-explained, not
   port-related.
3. K2 differs from K1 (`P P P P P P P`) in 6 of 7 legs, matching the claims' do-nothing-control
   argument: a do-nothing run cannot satisfy the frozen predicate.

## Tooling record

- Installed / resolved in scratch only, channel `uv pip` (PyPI): `grpcio 1.85.1`,
  `grpcio-tools 1.85.1`, `protobuf 7.36.2`, `setuptools 84.2.1`, `typing-extensions 4.16.0`.
  Reason: grader leg 2 imports grpc and legs 6/7 need the gRPC runtime in the case venv.
- No PATH tool created or modified; no pacman transaction (host guard); no system tool upgraded.

## Confidence

**High** that the two committed control captures are genuine and reproducible from committed
bytes on this host: exact 14/14 leg equality including exception classes and messages, matching
grader sha inside the sandbox, frozen fragment reproduced verbatim, and content-sensitivity of
leg 1 demonstrated. A fabricated capture would have to reproduce the grader's exact assertion
strings and exception types per leg, which the mutation probe shows are content-dependent.
