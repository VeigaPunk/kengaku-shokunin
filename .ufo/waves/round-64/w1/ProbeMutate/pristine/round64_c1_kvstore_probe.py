#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `kv-store-grpc` grader (round 64, C1).

Runs the grader's own seven test functions -- never a copy, never a rewrite -- in file
order inside a bubblewrap sandbox, against five frozen candidate cases and a real gRPC
server the probe itself launches on 127.0.0.1:5328, the port the grader hardcodes.  The
grader under execution is the lane capture

    corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py
    sha256 115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e
    (corpus/evidence/round52/graders/SHA256SUMS line 80)

byte-verified at run time against GRADER_SHA256 and bound read-only at
/tests/test_outputs.py; a byte drift, or a change in the file's `def test_...` order,
is a SETUP error, never a run.

Leg rule (frozen in plans/round-64-claims.md): P iff the test function returns
normally; F on any exception.  All seven legs of a case run in ONE sandbox process, in
file order, so they share the process state a harness would share with them.

Frozen vectors (plans/round-64-claims.md, R64-C1):

    K1 compliant          P P P P P P P
    K2 do-nothing control F P F F F F F
    K3 wrong-math         P P P P P F F
    K4 proto-only control P P F F F F F
    K5 files, no server   P P P P F P F

The expected vector is DERIVED at run time by predict_legs() from the case
declarations and compared to the frozen literal; a derivation that disagrees with the
freeze aborts the battery (SETUP prediction-drift) instead of grading (r59 lesson M-1).

Design notes, each one why a piece exists:

  * The sandbox shape is the r37/r63 house shape: host /usr read-only, /bin,/sbin,/lib,
    /lib64 symlinked into it, host /etc read-only, /proc and /dev mounted, /tmp a
    tmpfs, the case directory bound writable at /app, the grader read-only at
    /tests/test_outputs.py, the probe-owned venv at /venv, the case driver at
    /ctl/driver.py.  `PYTHONDONTWRITEBYTECODE=1` keeps the read-only venv quiet.
  * Network is SHARED (no --unshare-net): the grader's legs must reach
    127.0.0.1:5328, so the server is a host-loopback listener owned by the probe.
    Because of that, the probe records `ss -ltn` (and a bind test) FREE before the
    battery and before/after every case, and REFUSES (exit 2, SETUP
    port-5328-occupied) rather than grading through a foreign listener.
  * The server is started by the case driver INSIDE the sandbox (so it shares the
    leg process's sandbox), from /app/server.py, and writes exactly one start line to
    /app/server.log: `SERVER UP 5328`.  The driver prints SERVERPID before the first
    LEGJSON line -- that ordering, recorded in the receipt as
    `pid_before_legs=True`, is the frozen predicate's "PID recorded before the
    handshake leg ran".  The driver kills the server by its own PID after the legs
    and verifies it exited; the probe additionally checks the port is free after
    every case and only ever kills the recorded PID (and only after checking its
    /proc/<pid>/cmdline names /app/server.py).
  * The pb2 modules are generated in a SEPARATE sandbox exec by the probe-owned venv:
    `/venv/bin/python -m grpc_tools.protoc -I/app --python_out=/app
    --grpc_python_out=/app /app/kv-store.proto`.  Generation is a case-setup step,
    not a graded leg, so a generation failure is SETUP, never a leg.
  * K2 is the do-nothing control and K4 the proto-only control; both were measured
    before the freeze (corpus/evidence/round64/k2-empty-capture.txt,
    k4-protoonly-capture.txt).  K2's leg 5 is the one frozen grader-printed fragment
    this predicate names: `Port 5328 is not listening - no real gRPC server is
    running`.  If K2 leg 5 is P while the probe saw the port free, the counter or the
    port discipline is wrong: the battery refuses (exit 2) instead of grading.
  * K3's wrong-math server stores `request.value + 1`; the handshake's
    `response.val == 999` assertion then fails inside the grader's
    `except Exception` arm, which re-raises AssertionError -- hence legs 6 and 7 F.
  * K5 has every file but no server: leg 6 is the frozen prediction that the
    handshake tolerates `grpc.RpcError` (UNAVAILABLE included) while leg 7 does not
    (no except arm), so K5 is P P P P F P F, not the K2/K4 shape.
  * Every observed value in the receipt carries the command that produced it: the
    receipt records the grader sha256+pin, the venv's grpcio / grpcio-tools versions,
    the port-free observations, the per-case driver invocation, the per-leg
    exception class and message fragment, and the server log sidecar.

Measured on this host while building the instrument (Arch, 2026-11-03): bwrap 0.13.1
at /usr/bin/bwrap, host python 3.14.8, uv 0.13.0.  bwrap runs in the HOST PID
namespace here (`/proc/self/status` NSpid has one entry), so the SERVERPID the driver
prints is a host PID; the post-case cleanup can therefore verify
/proc/<pid>/cmdline before signalling.  /dev/shm is present inside the house shape.
The probe-owned venv resolves grpcio 1.85.1 and grpcio-tools 1.85.1 for cp314, and
`grpc_tools.protoc` writes /app/kv_store_pb2.py and /app/kv_store_pb2_grpc.py, the
two names the grader's leg 3 requires.

Named limitation (r63 routed defect 4, carried, frozen): `--check-receipt` re-derives
TEXT fields only and cannot prove a live run.  The live evidence is the server-side
log the probe captures from the process it started (receipt field `server_log` +
`server_pid`, raw bytes in the sidecar `<receipt>.server-log`).

Run as:

  python3 plans/round64_c1_kvstore_probe.py --lane <lane> --work <scratch> \
      --receipt <path>                       # the battery (K1..K5) + receipt
  python3 plans/round64_c1_kvstore_probe.py --check-receipt <receipt>
  python3 plans/round64_c1_kvstore_probe.py --selftest --work <scratch>
  python3 plans/round64_c1_kvstore_probe.py --render-table

Exit map: 0 pass, 1 predicate fail, 2 usage or missing/foreign input (SETUP line).
A battery that aborts on a SETUP condition writes no receipt: the receipt is only
written by a battery that actually placed all five cases.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import signal
import socket
import subprocess
import sys
import time

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py"
GRADER_SHA256 = "115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e"
PORT = 5328
BWRAP = "/usr/bin/bwrap"
PROBE_VERSION = "r64-c1/1"
LEG_NAMES = (
    "test_proto_file_creation",
    "test_grpc_tools_installation",
    "test_protobuf_generation",
    "test_server_file_creation",
    "test_real_grpc_server_running",
    "test_grpc_protocol_handshake",
    "test_grpc_server_functionality",
)
FROZEN_VECTORS = {
    "K1": ("P", "P", "P", "P", "P", "P", "P"),
    "K2": ("F", "P", "F", "F", "F", "F", "F"),
    "K3": ("P", "P", "P", "P", "P", "F", "F"),
    "K4": ("P", "P", "F", "F", "F", "F", "F"),
    "K5": ("P", "P", "P", "P", "F", "P", "F"),
}
K2_LEG5_FRAGMENT = "Port 5328 is not listening"
K2_LEG5_FULL = "Port 5328 is not listening - no real gRPC server is running"
LEG_TIMEOUT = 120        # per-leg alarm inside the driver
PROTOC_TIMEOUT = 120     # one sandbox exec
DRIVER_TIMEOUT = 900     # one sandbox exec, 7 legs

# Frozen literal candidate sources (the probe's own, never the grader's).
PROTO_TEXT = """syntax = "proto3";

package kvstore;

service KVStore {
  rpc GetVal (GetValRequest) returns (GetValResponse);
  rpc SetVal (SetValRequest) returns (SetValResponse);
}

message GetValRequest {
  string key = 1;
}

message GetValResponse {
  int32 val = 1;
}

message SetValRequest {
  string key = 1;
  int32 value = 2;
}

message SetValResponse {
  int32 val = 1;
}
"""

SERVER_PY = '''import sys
from concurrent import futures

import grpc

import kv_store_pb2
import kv_store_pb2_grpc

STORE = {}


class Server(kv_store_pb2_grpc.KVStoreServicer):
    def SetVal(self, request, context):
        value = request.value
        STORE[request.key] = value
        return kv_store_pb2.SetValResponse(val=value)

    def GetVal(self, request, context):
        return kv_store_pb2.GetValResponse(val=STORE.get(request.key, 0))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    kv_store_pb2_grpc.add_KVStoreServicer_to_server(Server(), server)
    bound = server.add_insecure_port("127.0.0.1:5328")
    if bound != 5328:
        print("BIND FAILED %s" % bound, file=sys.stderr)
        return 1
    server.start()
    with open("/app/server.log", "w", encoding="utf-8") as fh:
        fh.write("SERVER UP 5328\\n")
    server.wait_for_termination()
    return 0


if __name__ == "__main__":
    sys.exit(serve())
'''

SERVER_WRONG = SERVER_PY.replace(
    "        value = request.value\n",
    "        value = request.value + 1\n")
assert SERVER_WRONG != SERVER_PY

DRIVER_SRC = '''import json
import signal
import socket
import subprocess
import sys
import time

PORT = 5328
LEG_NAMES = @LEG_NAMES@


class LegTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise LegTimeout("leg exceeded @LEG_TIMEOUT@ seconds")


def port_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.25)
    try:
        return sock.connect_ex(("127.0.0.1", PORT)) == 0
    finally:
        sock.close()


def start_server():
    log = open("/app/server.log", "wb")
    proc = subprocess.Popen([sys.executable, "/app/server.py"], cwd="/app",
                            stdout=log, stderr=log)
    log.close()
    print("SERVERPID %d" % proc.pid, flush=True)
    deadline = time.time() + 10.0
    while time.time() < deadline:
        if proc.poll() is not None:
            print("SERVER READY False rc=%d" % proc.returncode, flush=True)
            return proc, False
        if port_listening():
            print("SERVER READY True", flush=True)
            return proc, True
        time.sleep(0.1)
    print("SERVER READY False timeout=10s", flush=True)
    return proc, False


def stop_server(proc):
    if proc is None:
        print("SERVER KILL none", flush=True)
        return
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
    print("SERVER KILL pid=%d rc=%s" % (proc.pid, proc.poll()), flush=True)


def run_leg(module, name):
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, float(@LEG_TIMEOUT@))
    try:
        getattr(module, name)()
        return "P", "-", "-"
    except Exception as exc:
        text = " ".join(str(exc).split()) or "-"
        return "F", type(exc).__name__, text[:300]
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def main(argv):
    want_server = "--start-server" in argv
    proc = None
    if want_server:
        proc, ready = start_server()
        if not ready:
            stop_server(proc)
            return 3
    sys.path.insert(0, "/tests")
    try:
        import test_outputs
    except Exception as exc:
        print("DRIVER IMPORT-FAILED %s: %s" % (type(exc).__name__, exc), flush=True)
        stop_server(proc)
        return 4
    summary = []
    vector = []
    for index, name in enumerate(LEG_NAMES, 1):
        verdict, exc_name, frag = run_leg(test_outputs, name)
        vector.append(verdict)
        detail = "" if verdict == "P" else "%s: %s" % (exc_name, frag)
        summary.append([name, verdict, detail])
        print("LEGJSON " + json.dumps({"i": index, "name": name,
                                       "verdict": verdict,
                                       "exc": exc_name, "frag": frag}), flush=True)
    print("LEGS " + json.dumps(summary), flush=True)
    print("VECTOR " + " ".join(vector), flush=True)
    if want_server:
        stop_server(proc)
    try:
        with open("/app/server.log", "r", encoding="utf-8", errors="replace") as fh:
            log_text = fh.read().strip()
    except OSError:
        log_text = "(no server.log)"
    print("SERVER LOG " + (log_text or "(empty)"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''
DRIVER_SRC = DRIVER_SRC.replace("@LEG_NAMES@", repr(LEG_NAMES)).replace(
    "@LEG_TIMEOUT@", str(LEG_TIMEOUT))
assert "@LEG_" not in DRIVER_SRC


class SetupError(Exception):
    """A condition the probe refuses to grade through: exit 2, SETUP line."""


class Case:
    """One battery case, declared so predict_legs() can derive its vector."""

    def __init__(self, name, setup, server, server_src, note):
        self.name = name
        self.setup = setup            # "empty" | "proto" | "files"
        self.server = server          # start the server inside the case driver?
        self.server_src = server_src  # literal written as /app/server.py
        self.note = note


CASES = (
    Case("K1", "files", True, SERVER_PY,
         "compliant: proto + generated pb2 + server.py (echo) + server running on 5328"),
    Case("K2", "empty", False, None,
         "do-nothing control: empty /app, no server"),
    Case("K3", "files", True, SERVER_WRONG,
         "wrong-math: server stores value+1 on SetVal"),
    Case("K4", "proto", False, None,
         "proto-only control: only kv-store.proto present"),
    Case("K5", "files", False, SERVER_PY,
         "files complete, server never started"),
)


def predict_legs():
    """Derive each case's 7-leg vector from its declarations, in the frozen leg rule.

    Leg 1 needs the proto file; leg 2 is P by the probe-owned venv (the frozen
    vector says so); leg 3 needs the generated pb2; leg 4 needs server.py with
    `class Server`; leg 5 needs a listener on 5328.  Leg 6 tolerates grpc.RpcError
    (so a missing server still passes it) but not a wrong answer or a missing
    generated module; leg 7 tolerates neither.  The derivation must equal the
    frozen literal or the battery refuses.
    """
    out = {}
    for case in CASES:
        has_proto = case.setup in ("proto", "files")
        generated = case.setup == "files"
        has_server_py = case.setup == "files"
        vector = ["P" if has_proto else "F",                     # proto file exists
                  "P",                                           # grpcio in the venv
                  "P" if generated else "F",                     # pb2 files exist
                  "P" if has_server_py else "F",                 # server.py + class Server
                  "P" if case.server else "F"]                   # 5328 listening
        if not generated:
            vector += ["F", "F"]                                 # ModuleNotFoundError
        elif case.server:
            echo = case.server_src == SERVER_PY
            vector += ["P" if echo else "F",                     # handshake answers
                       "P" if echo else "F"]                     # functionality answers
        else:
            vector += ["P", "F"]                                 # RpcError: tolerated / not
        out[case.name] = tuple(vector)
    return out


# --- probe-owned environment -------------------------------------------------

def find_uv():
    uv = shutil.which("uv")
    if uv:
        return uv
    local = pathlib.Path.home() / ".local" / "bin" / "uv"
    if local.is_file():
        return str(local)
    raise SetupError("uv-absent")


def ensure_venv(work):
    venv = pathlib.Path(work) / "venv"
    py = venv / "bin" / "python"
    if py.is_file():
        return venv
    uv = find_uv()
    proc = subprocess.run([uv, "venv", "--python", "/usr/bin/python3", str(venv)],
                          capture_output=True, text=True)
    if proc.returncode != 0 or not py.is_file():
        raise SetupError("venv-creation-failed rc=%d %s"
                         % (proc.returncode, proc.stderr.strip()[-300:]))
    return venv


def install_grpc(venv):
    """Install grpcio + grpcio-tools into the probe-owned venv; return version text."""
    uv = find_uv()
    py = venv / "bin" / "python"
    proc = subprocess.run([uv, "pip", "install", "--python", str(py),
                           "grpcio", "grpcio-tools"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SetupError("grpcio-install-failed rc=%d %s"
                         % (proc.returncode, proc.stderr.strip()[-300:]))
    code = ("import importlib.metadata as m; "
            "print(m.version('grpcio'), m.version('grpcio-tools'))")
    proc = subprocess.run([str(py), "-c", code], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SetupError("grpcio-version-probe-failed %s"
                         % proc.stderr.strip()[-300:])
    return proc.stdout.strip()


def ss_hits():
    """Listeners on 5328 as `ss -ltn` reports them; SS absent/failing is SETUP."""
    if shutil.which("ss") is None:
        raise SetupError("ss-absent")
    for args in (["ss", "-ltnH"], ["ss", "-ltn"]):
        proc = subprocess.run(args, capture_output=True, text=True)
        if proc.returncode != 0:
            continue
        hits = []
        for line in proc.stdout.splitlines():
            fields = line.split()
            if len(fields) >= 4 and fields[3].rsplit(":", 1)[-1] == str(PORT):
                hits.append(line.strip())
        return hits
    raise SetupError("ss-failed")


def port_free_bind():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("127.0.0.1", PORT))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def require_port_free(when):
    hits = ss_hits()
    if hits:
        raise SetupError("port-5328-occupied (%s) %s" % (when, hits[0]))
    if not port_free_bind():
        raise SetupError("port-5328-bind-failed (%s)" % when)


def pid_is_our_server(pid):
    try:
        cmdline = pathlib.Path("/proc/%d/cmdline" % pid).read_bytes()
    except OSError:
        return False
    return b"/app/server.py" in cmdline


def release_port(case_name, pid):
    """Free 5328 after a case; only ever kills the recorded /app/server.py PID."""
    if not ss_hits():
        return True
    if pid:
        try:
            pid_int = int(pid)
        except ValueError:
            pid_int = None
        if pid_int is not None and pid_is_our_server(pid_int):
            try:
                os.kill(pid_int, signal.SIGKILL)
            except ProcessLookupError:
                pass
    for _ in range(100):
        if not ss_hits():
            return True
        time.sleep(0.1)
    return False


# --- sandbox -----------------------------------------------------------------

def sandbox_argv(case_app, tests_file, venv, driver, command):
    """bwrap house shape: host /usr read-only, case /app writable, shared loopback."""
    argv = [BWRAP, "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr",
            "--symlink", "usr/bin", "/bin",
            "--symlink", "usr/bin", "/sbin",
            "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib", "/lib64",
            "--ro-bind", "/etc", "/etc",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--dir", "/app", "--bind", str(case_app), "/app",
            "--dir", "/tests", "--ro-bind", str(tests_file), "/tests/test_outputs.py",
            "--dir", "/venv", "--ro-bind", str(venv), "/venv",
            "--dir", "/ctl", "--ro-bind", str(driver), "/ctl/driver.py",
            "--clearenv",
            "--setenv", "PATH", "/venv/bin:/usr/bin:/bin",
            "--setenv", "HOME", "/tmp",
            "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--chdir", "/app",
            "--"]
    return argv + command


def run_sandbox(case_app, tests_file, venv, driver, command, timeout):
    argv = sandbox_argv(case_app, tests_file, venv, driver, command)
    try:
        return subprocess.run(argv, capture_output=True, text=True, env={},
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise SetupError("bwrap-timeout %ss command=%s"
                         % (timeout, " ".join(command))) from exc
    except OSError as exc:
        raise SetupError("bwrap-exec-failed %s" % exc) from exc


def materialize_case(case, app):
    if case.setup == "empty":
        return
    (app / "kv-store.proto").write_text(PROTO_TEXT, encoding="utf-8")
    if case.setup == "files":
        (app / "server.py").write_text(case.server_src, encoding="utf-8")


def generate_pb2(app, tests_file, venv, driver, case_name):
    command = ["/venv/bin/python", "-m", "grpc_tools.protoc",
               "-I/app", "--python_out=/app", "--grpc_python_out=/app",
               "/app/kv-store.proto"]
    proc = run_sandbox(app, tests_file, venv, driver, command, PROTOC_TIMEOUT)
    if proc.returncode != 0:
        raise SetupError("protoc-failed %s rc=%d %s"
                         % (case_name, proc.returncode,
                            (proc.stderr or proc.stdout).strip()[-300:]))
    for name in ("kv_store_pb2.py", "kv_store_pb2_grpc.py"):
        if not (app / name).is_file():
            raise SetupError("protoc-output-missing %s %s" % (case_name, name))


def parse_driver(stdout):
    """Parse the case driver's stdout; None when no LEGJSON line was placed."""
    fields = {"legs": [], "server_pid": None, "server_ready": None,
              "pid_before_legs": False, "server_log": None, "vector": None}
    pid_index = leg_index = None
    for index, line in enumerate(stdout.splitlines()):
        if line.startswith("SERVERPID "):
            fields["server_pid"] = line.split()[1]
            if pid_index is None:
                pid_index = index
        elif line.startswith("SERVER READY "):
            fields["server_ready"] = line.split()[2] == "True"
        elif line.startswith("LEGJSON "):
            try:
                record = json.loads(line[len("LEGJSON "):])
            except ValueError:
                return None
            fields["legs"].append(record)
            if leg_index is None:
                leg_index = index
        elif line.startswith("VECTOR "):
            fields["vector"] = tuple(line.split()[1:])
        elif line.startswith("SERVER LOG "):
            fields["server_log"] = line[len("SERVER LOG "):]
    if not fields["legs"]:
        return None
    fields["pid_before_legs"] = (
        pid_index is not None and leg_index is not None and pid_index < leg_index)
    return fields


# --- battery -----------------------------------------------------------------

def run_battery(lane, work, receipt):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError("work-dir-required (not a directory: %s)" % work)
    if not pathlib.Path(BWRAP).is_file():
        raise SetupError("bwrap-absent at %s" % BWRAP)
    if shutil.which("ss") is None:
        raise SetupError("ss-absent")
    lane = pathlib.Path(lane)
    src = lane / GRADER_REL
    if not src.is_file():
        raise SetupError("grader-missing %s" % src)
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GRADER_SHA256:
        raise SetupError("grader-sha-mismatch %s != %s" % (digest, GRADER_SHA256))
    declared_legs = re.findall(r"^def (test_[a-z0-9_]+)\(", data.decode("utf-8"), re.M)
    if tuple(declared_legs) != LEG_NAMES:
        raise SetupError("grader-legs-drift %s != %s"
                         % (declared_legs, list(LEG_NAMES)))

    derived = predict_legs()
    for name in FROZEN_VECTORS:
        if derived[name] != FROZEN_VECTORS[name]:
            raise SetupError(
                "prediction-drift %s derived=%s frozen=%s"
                % (name, "/".join(derived[name]), "/".join(FROZEN_VECTORS[name])))

    tests_dir = work / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    tests_file = tests_dir / "test_outputs.py"
    tests_file.write_bytes(data)
    driver = work / "driver.py"
    driver.write_text(DRIVER_SRC, encoding="utf-8")
    venv = ensure_venv(work)
    versions = install_grpc(venv)

    require_port_free("battery start")
    lines = [
        "# R64-C1 receipt -- TB2 kv-store-grpc grader offline under bwrap",
        "# instrument plans/round64_c1_kvstore_probe.py version=%s" % PROBE_VERSION,
        "# named limitation: --check-receipt re-derives TEXT fields only; the live",
        "#   evidence is server_pid + server_log, raw bytes in the sidecar beside this receipt.",
        "GRADER sha256=%s pin=%s" % (digest, TB2_PIN),
        "VENV python=%d.%d.%d grpcio=%s"
        % (sys.version_info[0], sys.version_info[1], sys.version_info[2],
           versions.replace(" ", " grpcio-tools=")),
        "PORTFREE before-battery True",
    ]
    observed = {}
    server_logs = {}
    server_pids = {}
    k2_fragment = None

    for case in CASES:
        require_port_free("%s before exec" % case.name)
        lines.append("PORTFREE before %s True" % case.name)
        case_dir = work / "cases" / case.name
        if case_dir.exists():
            shutil.rmtree(case_dir)
        app = case_dir / "app"
        app.mkdir(parents=True)
        materialize_case(case, app)
        if case.setup == "files":
            generate_pb2(app, tests_file, venv, driver, case.name)
        command = ["/venv/bin/python", "/ctl/driver.py"]
        if case.server:
            command.append("--start-server")
        proc = run_sandbox(app, tests_file, venv, driver, command, DRIVER_TIMEOUT)
        if "SERVER READY False" in proc.stdout:
            raise SetupError("case-%s-server-not-ready %s"
                             % (case.name, proc.stdout.strip().splitlines()[-1:]))
        parsed = parse_driver(proc.stdout)
        if parsed is None:
            raise SetupError("driver-failed %s rc=%d %s"
                             % (case.name, proc.returncode,
                                (proc.stderr or proc.stdout).strip()[-300:]))
        if proc.returncode != 0:
            raise SetupError("driver-failed %s rc=%d %s"
                             % (case.name, proc.returncode,
                                (proc.stderr or proc.stdout).strip()[-300:]))
        if (tuple(record.get("name") for record in parsed["legs"]) != LEG_NAMES
                or len(parsed["legs"]) != len(LEG_NAMES)):
            raise SetupError("driver-legs-malformed %s" % case.name)
        vector = tuple(record["verdict"] for record in parsed["legs"])
        if parsed["vector"] != vector:
            raise SetupError("driver-vector-inconsistent %s %s != %s"
                             % (case.name, parsed["vector"], vector))
        if case.server:
            if not parsed["server_pid"] or not parsed["server_pid"].isdigit():
                raise SetupError("case-%s-server-pid-missing" % case.name)
            if not parsed["pid_before_legs"]:
                raise SetupError("case-%s-server-pid-not-before-legs" % case.name)
            log_text = parsed["server_log"] or ""
            server_logs[case.name] = log_text
            server_pids[case.name] = parsed["server_pid"]
        if case.name == "K2":
            leg5 = parsed["legs"][4]
            k2_fragment = leg5["frag"]
            if leg5["verdict"] == "P":
                raise SetupError(
                    "k2-leg5-answered-with-port-free (port discipline wrong; "
                    "refusing to grade through a foreign listener)")
        observed[case.name] = vector
        pid = parsed["server_pid"] or "none"
        before = ("True" if parsed["pid_before_legs"] else "False") if case.server else "none"
        ready = ("True" if parsed["server_ready"] else "False") if case.server else "none"
        if case.server:
            log_token = "_".join((parsed["server_log"] or "").split()) or "none"
        else:
            log_token = "none"
        lines.append(
            "CASE %s observed=%s expected=%s server_pid=%s pid_before_legs=%s "
            "server_ready=%s server_log=%s"
            % (case.name, "/".join(vector), "/".join(derived[case.name]),
               pid, before, ready, log_token))
        for record in parsed["legs"]:
            frag = record["frag"] if record["verdict"] == "F" else "-"
            lines.append("LEG %s %d %s %s exc=%s frag=%s"
                         % (case.name, record["i"], record["name"],
                            record["verdict"], record["exc"], frag))
        freed = release_port(case.name, parsed["server_pid"] if case.server else None)
        lines.append("PORTFREE after %s %s" % (case.name, freed))
        if not freed:
            raise SetupError("port-5328-still-occupied-after-%s" % case.name)
        print("CASE %s observed=%s freed=%s"
              % (case.name, "/".join(vector), freed))

    lines.append("K2-FRAGMENT %s" % (k2_fragment or "(none)"))
    for name in FROZEN_VECTORS:
        lines.append("VECTOR %s=%s" % (name, "/".join(observed[name])))
    lines.append("PREDICTION " + " ".join(
        "%s=%s" % (name, "/".join(derived[name])) for name in FROZEN_VECTORS))

    ok = True
    ok = ok and all(observed[name] == FROZEN_VECTORS[name] for name in FROZEN_VECTORS)
    ok = ok and all(derived[name] == FROZEN_VECTORS[name] for name in FROZEN_VECTORS)
    ok = ok and k2_fragment is not None and K2_LEG5_FRAGMENT in k2_fragment
    for name in ("K1",):
        ok = ok and server_pids.get(name, "").isdigit()
    ok = ok and all(
        (parsed_case_server_log == "SERVER UP 5328")
        for parsed_case_server_log in server_logs.values())

    sidecar_name = None
    if receipt:
        path = pathlib.Path(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        sidecar = path.with_name(path.name + ".server-log")
        blocks = []
        for case in CASES:
            if case.name in server_logs:
                blocks.append("case=%s pid=%s"
                              % (case.name, server_pids.get(case.name, "none")))
                blocks.append(server_logs[case.name])
        sidecar.write_text("\n".join(blocks) + "\n", encoding="utf-8")
        sidecar_name = sidecar.name
        lines.append("SERVERLOG file=%s" % sidecar_name)
    lines.append("PREDICATE R64-C1 %s" % ("pass" if ok else "fail"))
    if receipt:
        pathlib.Path(receipt).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    return 0 if ok else 1


# --- receipt re-derivation ---------------------------------------------------

def _kv(token):
    return token.split("=", 1)[1] if "=" in token else ""


def receipt_failures(text):
    """Re-derive the frozen R64-C1 predicate from a receipt's text fields."""
    lines = [line.rstrip() for line in text.splitlines()]
    failures = []
    grader = next((line for line in lines if line.startswith("GRADER ")), "")
    tokens = grader.split()[1:] if grader else []
    sha = "".join(_kv(tok) for tok in tokens if tok.startswith("sha256="))
    pin = "".join(_kv(tok) for tok in tokens if tok.startswith("pin="))
    if not grader:
        failures.append("grader-line-missing")
    if sha != GRADER_SHA256:
        failures.append("grader-sha %s != %s" % (sha or "(none)", GRADER_SHA256))
    if pin != TB2_PIN:
        failures.append("grader-pin %s != %s" % (pin or "(none)", TB2_PIN))

    if "PORTFREE before-battery True" not in lines:
        failures.append("port-free-at-battery-start not recorded")

    declared = {}
    for line in lines:
        if line.startswith("VECTOR "):
            body = line[len("VECTOR "):]
            if "=" not in body:
                failures.append("vector-malformed %s" % line)
                continue
            name, vector = body.split("=", 1)
            declared[name] = vector

    cases = {}
    for line in lines:
        if line.startswith("CASE "):
            parts = line.split()
            fields = {}
            for token in parts[2:]:
                if "=" in token:
                    key, value = token.split("=", 1)
                    fields[key] = value
            cases[parts[1]] = fields

    leg_verdicts = {}
    leg_frags = {}
    for line in lines:
        match = re.match(r"^LEG (K\d) (\d) (\S+) (P|F) exc=(\S+) frag=(.*)$", line)
        if match:
            leg_verdicts.setdefault(match.group(1), {})[int(match.group(2))] = match.group(4)
            leg_frags.setdefault(match.group(1), {})[int(match.group(2))] = match.group(6)

    for case in CASES:
        name = case.name
        frozen = "/".join(FROZEN_VECTORS[name])
        if name not in declared:
            failures.append("%s vector-line-missing" % name)
        elif declared[name] != frozen:
            failures.append("%s vector %s != %s" % (name, declared[name], frozen))
        fields = cases.get(name)
        if fields is None:
            failures.append("%s case-line-missing" % name)
        else:
            if fields.get("observed") != frozen:
                failures.append("%s observed %s != %s"
                                % (name, fields.get("observed"), frozen))
            if fields.get("expected") != frozen:
                failures.append("%s expected %s != %s"
                                % (name, fields.get("expected"), frozen))
        if "PORTFREE before %s True" % name not in lines:
            failures.append("%s port-not-recorded-free-before" % name)
        if "PORTFREE after %s True" % name not in lines:
            failures.append("%s port-not-recorded-free-after" % name)
        verdicts = leg_verdicts.get(name, {})
        if len(verdicts) != len(LEG_NAMES):
            failures.append("%s leg-lines %d != %d"
                            % (name, len(verdicts), len(LEG_NAMES)))
        else:
            row = "".join(verdicts[index] for index in range(1, len(LEG_NAMES) + 1))
            if row != frozen.replace("/", ""):
                failures.append("%s leg-verdicts %s != %s"
                                % (name, row, frozen.replace("/", "")))

    fragment_line = next((line[len("K2-FRAGMENT "):] for line in lines
                          if line.startswith("K2-FRAGMENT ")), "")
    if K2_LEG5_FRAGMENT not in fragment_line:
        failures.append("k2-fragment %s lacks %r"
                        % (fragment_line or "(missing)", K2_LEG5_FRAGMENT))
    if K2_LEG5_FRAGMENT not in leg_frags.get("K2", {}).get(5, ""):
        failures.append("k2 leg-5 fragment does not carry the frozen fragment")

    k1 = cases.get("K1", {})
    if not re.fullmatch(r"\d+", k1.get("server_pid", "")):
        failures.append("K1 server_pid not recorded: %s"
                        % (k1.get("server_pid") or "(none)"))
    if k1.get("pid_before_legs") != "True":
        failures.append("K1 server_pid not recorded before legs: %s"
                        % (k1.get("pid_before_legs") or "(none)"))
    if k1.get("server_ready") != "True":
        failures.append("K1 server not recorded ready: %s"
                        % (k1.get("server_ready") or "(none)"))
    if k1.get("server_log") != "SERVER_UP_5328":
        failures.append("K1 server_log not recorded: %s"
                        % (k1.get("server_log") or "(none)"))

    stored = next((line for line in lines if line.startswith("PREDICATE R64-C1 ")), "")
    if not stored:
        failures.append("predicate-line-missing")
    elif stored.split()[-1] != ("pass" if not failures else "fail"):
        failures.append("stored-predicate %s disagrees with derived %s"
                        % (stored.split()[-1], "pass" if not failures else "fail"))
    return failures


def check_receipt(path):
    path = pathlib.Path(path)
    if not path.is_file():
        print("SETUP receipt-missing %s" % path)
        return 2
    failures = receipt_failures(path.read_text(encoding="utf-8"))
    for failure in failures:
        print("CHECK fail %s" % failure)
    if not failures:
        print("CHECK ok cases=%d" % len(CASES))
    ok = not failures
    print("PREDICATE R64-C1 %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# --- selftest ----------------------------------------------------------------

def _replace_line(text, prefix, new_line):
    out = []
    seen = False
    for line in text.splitlines():
        if not seen and line.startswith(prefix):
            out.append(new_line)
            seen = True
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def synth_receipt():
    """A text-field-faithful receipt, used ONLY to exercise the checker's mechanics.

    It proves nothing about a live run -- that is the named limitation -- and the
    selftest prints that warning.
    """
    lines = [
        "# synthesized receipt for checker mechanics only (no live run)",
        "GRADER sha256=%s pin=%s" % (GRADER_SHA256, TB2_PIN),
        "VENV python=0.0.0 grpcio=0.0.0 grpcio-tools=0.0.0",
        "PORTFREE before-battery True",
    ]
    for case in CASES:
        name = case.name
        frozen = "/".join(FROZEN_VECTORS[name])
        pid = "424242" if case.server else "none"
        before = "True" if case.server else "none"
        ready = "True" if case.server else "none"
        log = "SERVER_UP_5328" if case.server else "none"
        lines.append("PORTFREE before %s True" % name)
        lines.append("PORTFREE after %s True" % name)
        lines.append("CASE %s observed=%s expected=%s server_pid=%s "
                     "pid_before_legs=%s server_ready=%s server_log=%s"
                     % (name, frozen, frozen, pid, before, ready, log))
        for index, leg in enumerate(LEG_NAMES, 1):
            verdict = FROZEN_VECTORS[name][index - 1]
            if verdict == "P":
                exc, frag = "-", "-"
            elif name == "K2" and index == 5:
                exc, frag = "AssertionError", K2_LEG5_FULL
            else:
                exc, frag = "AssertionError", "synthetic failure"
            lines.append("LEG %s %d %s %s exc=%s frag=%s"
                         % (name, index, leg, verdict, exc, frag))
    lines.append("K2-FRAGMENT %s" % K2_LEG5_FULL)
    for name in FROZEN_VECTORS:
        lines.append("VECTOR %s=%s" % (name, "/".join(FROZEN_VECTORS[name])))
    lines.append("PREDICTION " + " ".join(
        "%s=%s" % (name, "/".join(FROZEN_VECTORS[name])) for name in FROZEN_VECTORS))
    lines.append("PREDICATE R64-C1 pass")
    return "\n".join(lines) + "\n"


def table_lines():
    out = ["case  setup                                                          frozen vector"]
    for case in CASES:
        out.append("%-5s %-62s %s"
                   % (case.name, case.note, "/".join(FROZEN_VECTORS[case.name])))
    out.append("FROZEN-VECTOR " + " ".join(
        "%s=%s" % (name, "/".join(FROZEN_VECTORS[name])) for name in FROZEN_VECTORS))
    return out


def render_table():
    for line in table_lines():
        print(line)
    return 0


def run_selftest(work):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError("work-dir-required (not a directory: %s)" % work)
    root = work / "selftest"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    results = []

    # (c) --render-table must carry exactly the frozen vectors.
    parsed = {}
    for line in table_lines():
        match = re.match(r"^(K\d)\s+.*\s(\S+)$", line)
        if match:
            parsed[match.group(1)] = match.group(2)
    table_ok = (len(parsed) == len(CASES)
                and all(parsed.get(name) == "/".join(FROZEN_VECTORS[name])
                        for name in FROZEN_VECTORS))
    results.append(("render-table", 0 if table_ok else 1, 0))

    good = synth_receipt()
    good_path = root / "valid-receipt.txt"
    good_path.write_text(good, encoding="utf-8")

    # (a) one flipped vector cell must fail --check-receipt with exit 1.
    k2_vector = FROZEN_VECTORS["K2"]
    flipped = ("P",) + k2_vector[1:]
    tampered = _replace_line(
        good, "VECTOR K2=", "VECTOR K2=%s" % "/".join(flipped))
    tampered_path = root / "tampered-vector.txt"
    tampered_path.write_text(tampered, encoding="utf-8")

    # server PID dropped from K1 must fail (the frozen predicate names that field).
    nopid_line = next(line for line in good.splitlines() if line.startswith("CASE K1 "))
    nopid_line = nopid_line.replace("server_pid=424242", "server_pid=none")
    nopid = _replace_line(good, "CASE K1 ", nopid_line)
    nopid_path = root / "no-server-pid.txt"
    nopid_path.write_text(nopid, encoding="utf-8")

    # port-free-at-start dropped must fail.
    noport = _replace_line(good, "PORTFREE before-battery ",
                           "PORTFREE before-battery False")
    noport_path = root / "port-not-free.txt"
    noport_path.write_text(noport, encoding="utf-8")

    # frozen K2 fragment dropped must fail.
    nofrag = _replace_line(good, "K2-FRAGMENT ", "K2-FRAGMENT unrelated message")
    nofrag_path = root / "no-k2-fragment.txt"
    nofrag_path.write_text(nofrag, encoding="utf-8")

    # (b) a missing receipt must be exit 2.
    missing_path = root / "absent-receipt.txt"

    fixtures = [
        ("valid-receipt", good_path, 0),
        ("tampered-vector", tampered_path, 1),
        ("no-server-pid", nopid_path, 1),
        ("port-not-free", noport_path, 1),
        ("no-k2-fragment", nofrag_path, 1),
        ("missing-receipt", missing_path, 2),
    ]
    for label, path, expected in fixtures:
        rc = check_receipt(path)
        results.append((label, rc, expected))

    for label, observed, expected in results:
        print("SELFTEST %-16s observed=%d expected=%d %s"
              % (label, observed, expected,
                 "pass" if observed == expected else "FAIL"))
    ok = all(observed == expected for _label, observed, expected in results)
    print("SELFTEST note: synthesized receipts exercise text-field mechanics only; "
          "the live predicate's evidence is server_pid + server_log")
    print("SELFTEST %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# --- entry -------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--lane")
    ap.add_argument("--work")
    ap.add_argument("--receipt")
    ap.add_argument("--check-receipt")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--render-table", action="store_true")
    args = ap.parse_args(argv)

    if args.check_receipt:
        return check_receipt(args.check_receipt)
    if args.render_table:
        return render_table()

    if not args.work:
        print("SETUP work-dir-required")
        return 2
    if not pathlib.Path(args.work).is_dir():
        print("SETUP work-dir-required (not a directory: %s)" % args.work)
        return 2

    if args.selftest:
        try:
            return run_selftest(args.work)
        except SetupError as exc:
            print("SETUP %s" % exc)
            return 2

    if not args.lane:
        print("SETUP lane-required")
        return 2
    try:
        return run_battery(args.lane, args.work, args.receipt)
    except SetupError as exc:
        print("SETUP %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
