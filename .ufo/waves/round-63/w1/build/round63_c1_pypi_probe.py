#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `pypi-server` grader (round 63, C1).

Runs the grader's own `test_api()` -- never a copy, never a rewrite -- inside a
bubblewrap sandbox against a PEP 503 simple index that the probe builds by hand from
frozen literal sources and serves on 127.0.0.1:8080, the port the grader hardcodes
(`http://localhost:8080/simple`).  The grader under execution is the lane capture

    corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py
    sha256 82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c
    (corpus/evidence/round52/graders/SHA256SUMS line 134)

which is byte-verified at run time against GRADER_SHA256 and bound read-only at
/tests/test_outputs.py; a byte drift is a SETUP error, never a run.

The graded class is `network-service` (8 members, 0 executed before this round:
corpus/evidence/round62/class-survey.txt).  What makes the class different from the
sixteen executed graders: the candidate is *fetched over a socket at grading time*, so
the instrument cannot hand the grader a file -- it must stand up the service the
grader's `install()` expects and prove the service the grader reached was the probe's
own.  The proof is structural: the probe starts the server itself, records its PID,
records the sha256 of the wheel it serves, and the do-nothing control (K2) shows the
same leg failing when nothing listens.

Leg rule (frozen in plans/round-63-claims.md, verbatim): P iff `test_api()` returns
normally; F on any exception.  Case vector frozen as P/F/F/F:

    K1 compliant        index serves vectorops-0.1.0 with a correct dotproduct   -> P
    K2 do-nothing       nothing listening on 8080, no index                      -> F
    K3 wrong math       vectorops-0.1.0 whose dotproduct returns sum(a*b) + 1    -> F (AssertionError)
    K4 wrong version    index serves only vectorops-0.2.0                        -> F (CalledProcessError)

The expected vector is DERIVED at run time by predict_legs() from the case
declarations (served versions, math correctness) and compared to the frozen vector --
never retyped as a literal table (the r59 lesson M-1 mechanism).

Sandbox facts measured while building this instrument (each one is why a mount exists):

  * `--ro-bind <work>/venv <work>/venv` alone is not enough: the grader's `install()`
    runs `pip install` INTO that venv, which fails with
    `OSError: [Errno 30] Read-only file system: .../site-packages/vectorops`.
    The venv is therefore bound read-only and its `lib/pythonX.Y/site-packages`
    re-bound writable: the interpreter and pip are immutable, the install target is not.
  * `env -i` with no /etc inside the sandbox leaves libc without name resolution:
    pip reports `NameResolutionError(... Failed to resolve 'localhost'
    ([Errno -3] Temporary failure in name resolution))`.  The probe writes a
    loopback-only hosts file (`127.0.0.1 localhost`) and binds it at /etc/hosts;
    no host /etc, no host resolver, no host pip config enters the sandbox.
  * The server's own access log is the request-side proof that the leg's bytes came
    from the probe's PID: the server holds the port, so every 200 line in its log is
    a request IT served.  K1 therefore requires the log to contain a `/simple/vectorops`
    fetch and a fetch of the `vectorops-0.1.0` wheel; a P with an empty log would mean
    something else answered.  The log is read only after the server is stopped
    (http.server block-buffers stdout into a file), which is also why the kill happens
    before the assertion rather than after it.
  * K2's premise is checked from pip's own words, not from the port: a foreign index
    that answers and 404s also makes the leg F while its stderr still names the
    endpoint.  Both shapes were observed while building this instrument, from processes
    this probe did not start (a `http.server 8080 --directory /tmp` answering with a
    404'ing wheel, and a concurrent replay of this probe whose index serves a correct
    `vectorops`).  K2 is refused as confounded unless stderr says connection-refused
    (Errno 111) and pip did not succeed.
  * Network is shared, not unshared, because the leg must reach 127.0.0.1:8080.
    The probe bind-tests the port before every server start and refuses (exit 2,
    `SETUP port-8080-occupied`) rather than grading against a foreign service.
    It kills only the PID it started, and only after that PID was recorded.

Run as:

  python3 plans/round63_c1_pypi_probe.py --lane <lane> --work <scratch> \
      --receipt <path>                       # the battery (K1..K4) + receipt
  python3 plans/round63_c1_pypi_probe.py --selftest --work <scratch>
  python3 plans/round63_c1_pypi_probe.py --render-table
  python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt

Exit map: 0 pass, 1 predicate fail, 2 usage or missing/foreign input (SETUP line).
A battery that aborts on a SETUP condition writes no receipt: the receipt is only
written by a battery that actually placed all four legs.
"""
import argparse
import base64
import hashlib
import os
import pathlib
import re
import socket
import subprocess
import sys
import tempfile
import time
import zipfile

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"
GRADER_SHA256 = "82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c"
PORT = 8080
BWRAP = "/usr/bin/bwrap"
PKG = "vectorops"
REQ_VERSION = "0.1.0"
FROZEN_VECTOR = ("P", "F", "F", "F")
LEG_TIMEOUT = 180

# Frozen literal candidate sources (the probe's own, never the grader's).
CORRECT_INIT = "def dotproduct(a, b):\n    return sum(x * y for x, y in zip(a, b))\n"
WRONG_INIT = "def dotproduct(a, b):\n    return sum(x * y for x, y in zip(a, b)) + 1\n"

DRIVER = ("import sys; sys.path.insert(0, '/tests'); "
          "import test_outputs as t; t.test_api()")


# The K2 evidence is "pip's stderr names the grader's hardcoded endpoint".  pip renders
# that name in one of two forms depending on the version and the layer that fails:
#   * the URL form  `localhost:8080`  (index-url text, some resolver messages), and
#   * urllib3's connection-endpoint form, measured on this host's pip 26.2.1:
#         NewConnectionError("HTTPConnection(host='localhost', port=8080): ...")
# Both name exactly one endpoint, localhost port 8080.  The second form is matched as a
# host/port PAIR on a single line: a stderr that names localhost and 8080 separately,
# or names either one alone, does not match.  The form that matched is printed to
# stdout (`K2 ENDPOINT ...`) and the raw stderr is kept beside the receipt, so the
# reader can see which form the evidence took -- the requirement, "names localhost
# port 8080", is unchanged; only its rendering is.
ENDPOINT_PATTERNS = (
    ("url", re.compile(r"localhost:8080")),
    ("urllib3-host-port",
     re.compile(r"""host=['"]localhost['"]\s*,\s*port=8080\b""")),
)


def stderr_names_endpoint(stderr):
    """Return the name of the form that names localhost:8080 in stderr, else None."""
    for name, pat in ENDPOINT_PATTERNS:
        if pat.search(stderr):
            return name
    return None


class SetupError(Exception):
    """A condition the probe refuses to grade through: exit 2, SETUP line."""


class Case:
    """One battery case, declared so predict_legs() can derive its leg."""

    def __init__(self, name, serves, correct_math, note):
        self.name = name
        self.serves = tuple(serves)   # versions the index will carry; () = no server
        self.correct_math = correct_math
        self.note = note


CASES = (
    Case("K1", serves=(REQ_VERSION,), correct_math=True,
         note="compliant index: vectorops-0.1.0, correct dotproduct"),
    Case("K2", serves=(), correct_math=False,
         note="do-nothing control: nothing listening on 8080"),
    Case("K3", serves=(REQ_VERSION,), correct_math=False,
         note="wrong math: dotproduct returns sum(a*b) + 1"),
    Case("K4", serves=("0.2.0",), correct_math=False,
         note="wrong version: index carries only vectorops-0.2.0"),
)


def predict_legs():
    """Derive the leg vector from the case declarations, in the frozen leg rule.

    A leg is P iff test_api() returns normally, i.e. iff the index is reachable,
    carries the version the grader pins, and that version computes correctly.
    """
    out = []
    for case in CASES:
        if not case.serves:
            out.append("F")            # install(): nothing to reach -> CalledProcessError
        elif REQ_VERSION not in case.serves:
            out.append("F")            # install(): pinned version absent -> CalledProcessError
        elif not case.correct_math:
            out.append("F")            # install() ok, first assert fails -> AssertionError
        else:
            out.append("P")
    return tuple(out)


# --- deterministic hand-built wheel ------------------------------------------

def _zipinfo(name):
    zi = zipfile.ZipInfo(name, date_time=(2020, 1, 2, 3, 4, 6))
    zi.external_attr = 0o644 << 16
    zi.compress_type = zipfile.ZIP_DEFLATED
    return zi


def build_wheel(dist_dir, dist_name, version, module_src, package):
    """Write <dist>-<ver>-py3-none-any.whl by hand; return (path, sha256 hex)."""
    dist_dir = pathlib.Path(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    dist = f"{dist_name}-{version}"
    wheel = dist_dir / f"{dist}-py3-none-any.whl"
    files = [
        (f"{package}/__init__.py", module_src),
        (f"{dist}.dist-info/METADATA",
         f"Metadata-Version: 2.1\nName: {dist_name}\nVersion: {version}\n"),
        (f"{dist}.dist-info/WHEEL",
         "Wheel-Version: 1.0\nGenerator: hand\nRoot-Is-Purelib: true\n"
         "Tag: py3-none-any\n"),
        (f"{dist}.dist-info/top_level.txt", f"{package}\n"),
    ]
    record = []
    with zipfile.ZipFile(wheel, "w") as z:
        for name, text in files:
            data = text.encode("utf-8")
            z.writestr(_zipinfo(name), data)
            digest = base64.urlsafe_b64encode(
                hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
            record.append(f"{name},sha256={digest},{len(data)}")
        record.append(f"{dist}.dist-info/RECORD,,")
        z.writestr(_zipinfo(f"{dist}.dist-info/RECORD"),
                   ("\n".join(record) + "\n").encode("utf-8"))
    return wheel, hashlib.sha256(wheel.read_bytes()).hexdigest()


def build_case_index(case, case_dir):
    """Build the index (and the wheels) a case serves; return (index_dir, served sha)."""
    dist_dir = pathlib.Path(case_dir) / "dist"
    index_dir = pathlib.Path(case_dir) / "index"
    entries = []
    for version in case.serves:
        src = CORRECT_INIT if (version == REQ_VERSION and case.correct_math) else WRONG_INIT
        path, sha = build_wheel(dist_dir, PKG, version, src, PKG)
        entries.append((path, sha))
    packages = index_dir / "packages"
    packages.mkdir(parents=True, exist_ok=True)
    anchors = []
    for path, sha in entries:
        target = packages / path.name
        target.write_bytes(path.read_bytes())
        anchors.append(f"<a href='../../packages/{path.name}#sha256={sha}'>{path.name}</a>")
    simple = index_dir / "simple"
    (simple / PKG).mkdir(parents=True, exist_ok=True)
    (simple / "index.html").write_text(
        "<!DOCTYPE html><html><body>\n"
        f"<a href='{PKG}/'>{PKG}</a>\n"
        "</body></html>\n", encoding="utf-8")
    (simple / PKG / "index.html").write_text(
        "<!DOCTYPE html><html><body>\n" + "\n".join(anchors) + "\n</body></html>\n",
        encoding="utf-8")
    # The receipt records the sha256 of the wheel this case actually served for the
    # pinned version, or -- when no wheel carries it -- the sha256 of the wheel that
    # *is* served instead (K4 serves 0.2.0): the reader can tell which bytes the
    # grader was offered, and the reason the leg failed stays visible in `serves`.
    pinned = [(path, sha) for path, sha in entries
              if path.name.startswith(f"{PKG}-{REQ_VERSION}-")]
    fallback = entries[0] if entries else (None, "none")
    path, sha = (pinned[0] if pinned else fallback)
    return index_dir, sha


# --- probe-owned environment -------------------------------------------------

def port_free():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("127.0.0.1", PORT))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def port_listening():
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.5):
            return True
    except OSError:
        return False


def require_port_free(when):
    if not port_free():
        raise SetupError(f"port-8080-occupied ({when})")


def ensure_venv(work):
    venv = pathlib.Path(work) / "venv"
    py = venv / "bin" / "python"
    if py.is_file():
        return venv
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True,
                   capture_output=True, text=True)
    if not py.is_file():
        raise SetupError(f"venv-creation-failed at {venv}")
    return venv


def make_stub(work, venv):
    stub = pathlib.Path(work) / "stub"
    stub.mkdir(parents=True, exist_ok=True)
    shim = stub / "python"
    shim.write_text(f'#!/bin/sh\nexec {venv / "bin" / "python"} "$@"\n', encoding="utf-8")
    shim.chmod(0o755)
    return stub


def write_hosts(work):
    """Loopback-only /etc/hosts: the sandbox gets name resolution and nothing else."""
    hosts = pathlib.Path(work) / "hosts"
    hosts.write_text("127.0.0.1 localhost\n::1 localhost\n", encoding="utf-8")
    return hosts


def site_packages(venv):
    tag = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return venv / "lib" / tag / "site-packages"


def materialize_grader(lane, tests_dir):
    src = pathlib.Path(lane) / GRADER_REL
    if not src.is_file():
        raise SetupError(f"grader-missing {src}")
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GRADER_SHA256:
        raise SetupError(f"grader-sha-mismatch {digest} != {GRADER_SHA256}")
    tests_dir = pathlib.Path(tests_dir)
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_outputs.py").write_bytes(data)
    return digest


def sandbox_argv(work, venv, stub, tests_dir, home, hosts, command):
    """bwrap argv: host /usr read-only, probe-owned venv/tests/home, shared loopback."""
    argv = [BWRAP, "--ro-bind", "/usr", "/usr"]
    for link in ("/lib", "/lib64", "/bin", "/sbin"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
        elif os.path.isdir(link):
            argv += ["--ro-bind", link, link]
    argv += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--die-with-parent",
             "--ro-bind", str(hosts), "/etc/hosts",
             "--ro-bind", str(tests_dir), "/tests",
             "--ro-bind", str(venv), str(venv)]
    sp = site_packages(venv)
    if sp.is_dir():
        argv += ["--bind", str(sp), str(sp)]
    argv += ["--bind", str(home), str(home), "--chdir", "/"]
    argv += ["/usr/bin/env", "-i",
             f"PATH={stub}:{venv / 'bin'}:/usr/bin:/bin",
             f"HOME={home}",
             "PYTHONDONTWRITEBYTECODE=1",
             "PIP_CONFIG_FILE=/dev/null",
             "PIP_DISABLE_PIP_VERSION_CHECK=1"]
    return argv + command


def parse_exception(stderr, rc):
    for line in reversed(stderr.strip().splitlines()):
        head = line.split(":", 1)[0].strip()
        if head and " " not in head and head[0].isalpha() and not line.startswith(" "):
            return head.rsplit(".", 1)[-1]
    return f"rc={rc}"


def run_leg(work, venv, stub, tests_dir, home, hosts, func="test_api"):
    if func != "test_api":
        raise SetupError(f"unknown leg {func}")
    command = ["python", "-c", DRIVER]
    argv = sandbox_argv(work, venv, stub, tests_dir, home, hosts, command)
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, env={},
                              timeout=LEG_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "F", "TimeoutExpired", ""
    except OSError as exc:
        raise SetupError(f"bwrap-exec-failed {exc}") from exc
    observed = "P" if proc.returncode == 0 else "F"
    exc = "none" if observed == "P" else parse_exception(proc.stderr, proc.returncode)
    return observed, exc, proc.stdout + proc.stderr


def pip_install_stderr(work, venv, stub, tests_dir, home, hosts, spec):
    command = ["python", "-m", "pip", "install",
               "--index-url", f"http://localhost:{PORT}/simple", spec]
    argv = sandbox_argv(work, venv, stub, tests_dir, home, hosts, command)
    proc = subprocess.run(argv, capture_output=True, text=True, env={},
                          timeout=LEG_TIMEOUT)
    return proc.returncode, proc.stderr


SERVER_SINKS = {}   # server pid -> its access-log file object, closed with the server


def start_server(index_dir, log_path=None):
    """Start the index server on 127.0.0.1:8080; keep its access log.

    The log is the request-side proof that the leg's bytes came from this PID: the
    server holds the port, so every line in its log is a request it served.  A leg
    that returns P with an empty log would mean something else answered.
    """
    sink = open(log_path, "wb") if log_path else subprocess.DEVNULL
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1",
         "--directory", str(index_dir)],
        stdout=sink, stderr=sink,
        cwd=str(index_dir))
    SERVER_SINKS[proc.pid] = sink
    for _ in range(100):
        if proc.poll() is not None:
            raise SetupError("server-exited-before-ready")
        if port_listening():
            return proc
        time.sleep(0.05)
    stop_server(proc)
    raise SetupError("server-not-ready-in-5s")


def stop_server(proc):
    """Stop a server this probe started, by its own PID; never a foreign process."""
    if proc is None:
        return
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
    sink = SERVER_SINKS.pop(proc.pid, None)
    if sink not in (None, subprocess.DEVNULL):
        sink.close()


def served_paths(log_path):
    """Request paths this server answered with 200, read back from its access log."""
    try:
        text = pathlib.Path(log_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    paths = []
    for line in text.splitlines():
        parts = line.split('"')
        if len(parts) < 3:
            continue
        request = parts[1].split()          # "GET /simple/x/ HTTP/1.1"
        status = parts[2].split()           # "200 -"
        if len(request) >= 2 and status[:1] == ["200"]:
            paths.append(request[1])        # the request target only
    return paths


def uninstall(venv, pkg=PKG):
    """Remove the package from the probe-owned venv between cases (absent is fine)."""
    subprocess.run([str(venv / "bin" / "python"), "-m", "pip", "uninstall", "-y", pkg],
                   capture_output=True, text=True)


# --- battery -----------------------------------------------------------------

def run_battery(lane, work, receipt):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError(f"work-dir-required (not a directory: {work})")
    tests_dir = work / "tests"
    digest = materialize_grader(lane, tests_dir)
    venv = ensure_venv(work)
    stub = make_stub(work, venv)
    home = work / "home"
    home.mkdir(exist_ok=True)
    hosts = write_hosts(work)

    predicted = predict_legs()
    print("PREDICT " + " ".join(f"{c.name}={p}" for c, p in zip(CASES, predicted)))
    lines = [f"GRADER sha256={digest} pin={TB2_PIN}"]
    observed_vector = []
    k2_mentions = False
    index_pids = {}
    served_sha = {}

    for idx, case in enumerate(CASES):
        observed = exc = None
        index_pid = "none"
        wheel_sha = "none"
        proc = None
        case_dir = pathlib.Path(tempfile.mkdtemp(dir=str(work), prefix=f"{case.name}-"))
        try:
            log_path = case_dir / "server-access.log"
            if case.serves:
                index_dir, wheel_sha = build_case_index(case, case_dir)
                require_port_free(f"{case.name} before start")
                proc = start_server(index_dir, log_path)
                index_pid = str(proc.pid)
            else:
                require_port_free(f"{case.name} needs silence")
            observed, exc, out = run_leg(case_dir, venv, stub, tests_dir, home, hosts)
            if case.serves:
                # Stop the server BEFORE reading its log: http.server's stdout is
                # block-buffered when it is a file, so the access lines are only all
                # on disk once the writer is gone.  This is also the only place the
                # log can be trusted -- the last line is written before exit.
                stop_server(proc)
                proc = None
                served = served_paths(log_path)
                print(f"SERVED {case.name} requests={len(served)} "
                      f"paths={served[:4]}")
                if case.name == "K1" and not any(
                        p.startswith(f"/simple/{PKG}") for p in served):
                    raise SetupError("K1 confounded: own server served no "
                                     f"/simple/{PKG} request (log {len(served)} lines)")
                if case.name == "K1" and not any(
                        p.startswith(f"/packages/{PKG}-{REQ_VERSION}-") for p in served):
                    raise SetupError("K1 confounded: own server served no wheel "
                                     f"for {REQ_VERSION}")
            if case.name == "K2":
                rc, err = pip_install_stderr(
                    case_dir, venv, stub, tests_dir, home, hosts, f"{PKG}=={REQ_VERSION}")
                (work / "k2-pip-stderr.txt").write_text(err, encoding="utf-8")
                k2_form = stderr_names_endpoint(err)
                k2_mentions = k2_form is not None
                print(f"K2 ENDPOINT form={k2_form or 'not-named'} "
                      f"stderr_bytes={len(err)} file=k2-pip-stderr.txt")
                if rc == 0:
                    raise SetupError(
                        "K2 confounded: pip install SUCCEEDED during the quiet "
                        "window -- a foreign service answered on 8080")
                # A foreign index that answers and 404s also makes K2 fail while the
                # stderr still names the endpoint.  Refuse the leg unless pip's own
                # words are "connection refused": that is the only text that proves
                # nothing was listening.
                if "Errno 111" not in err and "Connection refused" not in err:
                    raise SetupError(
                        "K2 confounded: stderr does not say connection-refused, so "
                        "the quiet window was not clean")
        finally:
            stop_server(proc)
            uninstall(venv)
        observed_vector.append(observed)
        index_pids[case.name] = index_pid
        served_sha[case.name] = wheel_sha
        line = (f"CASE {case.name} leg=test_api observed={observed} "
                f"expected={predicted[idx]} exception={exc} "
                f"index_pid={index_pid} wheel_sha256={wheel_sha}")
        lines.append(line)
        print(line)

    derived = "/".join(predicted)
    lines.append(f"K2 stderr_mentions_8080={k2_mentions}")
    lines.append("CLASS network-service executed=1")
    lines.append(f"PREDICTION-VECTOR {'/'.join(FROZEN_VECTOR)} derived={derived}")

    k1_sha = served_sha.get("K1", "")
    ok = (tuple(observed_vector) == FROZEN_VECTOR
          and tuple(predicted) == FROZEN_VECTOR
          and k2_mentions
          and index_pids["K1"] not in ("", "none")
          and len(k1_sha) == 64
          and all(c in "0123456789abcdef" for c in k1_sha))
    lines.append(f"PREDICATE R63-C1 {'pass' if ok else 'fail'}")
    lines.append(f"CLASS-PROBE-EXIT={0 if ok else 1}")

    if receipt:
        path = pathlib.Path(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-2])
    return 0 if ok else 1


# --- selftest: the same sandbox pipeline against a toy package and toy grader --

TOY_GRADER = (
    "import subprocess\n"
    "\n"
    "\n"
    "def install():\n"
    "    subprocess.run(\n"
    "        ['python', '-m', 'pip', 'install', '--index-url',\n"
    "         'http://localhost:8080/simple', 'toyops==0.1.0'],\n"
    "        capture_output=True, text=True, check=True)\n"
    "\n"
    "\n"
    "def test_api():\n"
    "    install()\n"
    "    assert __import__('toyops').value() == 42\n"
)
TOY_MODULE = "def value():\n    return 42\n"


def run_selftest(work):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError(f"work-dir-required (not a directory: {work})")
    root = pathlib.Path(tempfile.mkdtemp(dir=str(work), prefix="selftest-"))
    tests_dir = root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_outputs.py").write_text(TOY_GRADER, encoding="utf-8")
    venv = ensure_venv(root)
    stub = make_stub(root, venv)
    home = root / "home"
    home.mkdir(exist_ok=True)
    hosts = write_hosts(root)

    results = []
    # toy case 1: a correct toy server must yield P
    index_root = root / "index"
    wheel, sha = build_wheel(root / "dist", "toyops", "0.1.0", TOY_MODULE, "toyops")
    packages = index_root / "packages"
    packages.mkdir(parents=True, exist_ok=True)
    (packages / wheel.name).write_bytes(wheel.read_bytes())
    simple = index_root / "simple"
    (simple / "toyops").mkdir(parents=True, exist_ok=True)
    (simple / "index.html").write_text(
        "<html><body>\n<a href='toyops/'>toyops</a>\n</body></html>\n", encoding="utf-8")
    (simple / "toyops" / "index.html").write_text(
        "<html><body>\n"
        f"<a href='../../packages/{wheel.name}#sha256={sha}'>{wheel.name}</a>\n"
        "</body></html>\n", encoding="utf-8")
    require_port_free("selftest correct toy server")
    proc = start_server(index_root)
    try:
        observed, exc, _ = run_leg(root, venv, stub, tests_dir, home, hosts)
    finally:
        stop_server(proc)
        uninstall(venv, "toyops")
    results.append(("correct", "P", observed, exc))

    # toy case 2: nothing listening must yield F
    require_port_free("selftest absent toy server")
    observed, exc, _ = run_leg(root, venv, stub, tests_dir, home, hosts)
    uninstall(venv, "toyops")
    results.append(("absent", "F", observed, exc))

    for label, expected, observed, exc in results:
        print(f"SELFTEST toy={label} observed={observed} expected={expected} "
              f"exception={exc}")
    ok = all(observed == expected for _l, expected, observed, _e in results)
    print(f"SELFTEST {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# --- receipt re-derivation ---------------------------------------------------

def _kv(token):
    return token.split("=", 1)[1] if "=" in token else ""


def check_receipt(path):
    path = pathlib.Path(path)
    if not path.is_file():
        print(f"SETUP receipt-missing {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    failures = []

    grader = next((ln for ln in lines if ln.startswith("GRADER ")), "")
    tokens = grader.split()
    sha = "".join(_kv(t) for t in tokens if t.startswith("sha256="))
    pin = "".join(_kv(t) for t in tokens if t.startswith("pin="))
    if not grader:
        failures.append("grader-line-missing")
    if sha != GRADER_SHA256:
        failures.append(f"grader-sha {sha or '(none)'} != {GRADER_SHA256}")
    if pin != TB2_PIN:
        failures.append(f"grader-pin {pin or '(none)'} != {TB2_PIN}")

    cases = {}
    for ln in lines:
        if ln.startswith("CASE "):
            parts = ln.split()
            fields = {}
            for tok in parts[2:]:
                if "=" in tok:
                    key, value = tok.split("=", 1)
                    fields[key] = value
            cases[parts[1]] = fields

    names = [c.name for c in CASES]
    derived = "/".join(predict_legs())
    observed_vector = []
    for name, expected_frozen in zip(names, FROZEN_VECTOR):
        fields = cases.get(name)
        if fields is None:
            failures.append(f"{name}-case-missing")
            observed_vector.append("?")
            continue
        observed_vector.append(fields.get("observed", "?"))
        if fields.get("expected") != expected_frozen:
            failures.append(f"{name} expected {fields.get('expected')} != {expected_frozen}")
        if fields.get("observed") != expected_frozen:
            failures.append(f"{name} observed {fields.get('observed')} != {expected_frozen}")
        if fields.get("leg") != "test_api":
            failures.append(f"{name} leg {fields.get('leg')} != test_api")
    if tuple(predict_legs()) != FROZEN_VECTOR:
        failures.append(f"prediction-drift derived={derived}")
    if "/".join(observed_vector) != "/".join(FROZEN_VECTOR):
        failures.append(f"observed-vector {'/'.join(observed_vector)} != P/F/F/F")

    k1 = cases.get("K1", {})
    if _kv("index_pid=" + k1.get("index_pid", "")) in ("", "none"):
        failures.append("K1 index_pid empty")
    wheel = k1.get("wheel_sha256", "")
    if len(wheel) != 64 or any(c not in "0123456789abcdef" for c in wheel):
        failures.append(f"K1 wheel_sha256 not a sha256: {wheel or '(none)'}")

    mentions = next((ln for ln in lines if ln.startswith("K2 stderr_mentions_8080=")), "")
    if mentions != "K2 stderr_mentions_8080=True":
        failures.append(f"k2-stderr {mentions or '(line missing)'}")

    if "CLASS network-service executed=1" not in lines:
        failures.append("class-line-missing")

    vec = next((ln for ln in lines if ln.startswith("PREDICTION-VECTOR ")), "")
    if vec and vec.split("derived=", 1)[-1] != "/".join(FROZEN_VECTOR):
        failures.append(f"prediction-vector {vec}")
    if not vec:
        failures.append("prediction-vector-line-missing")

    stored = next((ln for ln in lines if ln.startswith("PREDICATE R63-C1 ")), "")
    stored_verdict = stored.split()[-1] if stored else "(missing)"

    for f in failures:
        print(f"CHECK fail {f}")
    if not failures:
        print(f"CHECK ok cases=4 vector={'/'.join(observed_vector)} "
              f"wheel_sha256={wheel[:12]}...")
    print(f"CHECK stored-predicate={stored_verdict} "
          f"derived={'pass' if not failures else 'fail'}")
    ok = not failures
    print(f"PREDICATE R63-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# --- entry -------------------------------------------------------------------

def render_table():
    print("case  setup                                                    expected")
    for case, prediction in zip(CASES, predict_legs()):
        print(f"{case.name}    {case.note:<56} {prediction}")
    print(f"FROZEN-VECTOR {'/'.join(FROZEN_VECTOR)}")
    print(f"DERIVED-VECTOR {'/'.join(predict_legs())}")
    return 0


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
        print(f"SETUP work-dir-required (not a directory: {args.work})")
        return 2

    if args.selftest:
        try:
            return run_selftest(args.work)
        except SetupError as exc:
            print(f"SETUP {exc}")
            return 2

    if not args.lane:
        print("SETUP lane-required")
        return 2
    if not pathlib.Path(BWRAP).is_file():
        print(f"SETUP bwrap-absent at {BWRAP}")
        return 2
    try:
        return run_battery(args.lane, args.work, args.receipt)
    except SetupError as exc:
        print(f"SETUP {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
