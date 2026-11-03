#!/usr/bin/env python3
"""Round 69, C1: the `nginx-request-logging` Terminal-Bench 2.0 grader replayed offline.

The grader (`corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`,
sha256 pinned below) has eight legs in file order: nginx on PATH, an HTTP service on
127.0.0.1:8080, the index body, the custom 404 body, `nginx -t`, the config contents
(listen/root/log_format/limit_req_zone), the access log's existence and its line format.

This probe stages five candidate end states inside bubblewrap and lets the grader's own
test functions decide each leg: a lane-built HTTP server on 127.0.0.1:8080 (shared
loopback, as in round 64's kv-store replay), lane-written nginx config bytes, an optional
`nginx` shim on PATH, and an optional access log the server writes.  Nothing here asserts a
leg in the grader's place: an AssertionError is F, any other exception is E (scored F), a
return is P.

The five cases and their eight-leg vectors are FROZEN in plans/round-69-claims.md before
the battery below runs.  `--check-receipt` re-derives every leg, vector, leg-coverage count
and the two shas from committed bytes; it cannot prove a live run (the receipt's per-case
PORT/SERVER lines are the live witness).  `--selftest` shows the checker refusing five
forged receipts.
"""

import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import time
from contextlib import redirect_stdout

PROBE_VERSION = 1
GRADER_REL = "corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py"
GRADER_SHA256 = "045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0"
TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
PORT = 8080
BWRAP = "/usr/bin/bwrap"
LOCK_PATH = os.path.expanduser("~/.local/share/kengaku-r69/port-8080.lock")

LEGS = (
    "test_nginx_installed",
    "test_nginx_running",
    "test_index_page_content",
    "test_custom_404_page",
    "test_nginx_config_syntax",
    "test_nginx_config_settings",
    "test_log_file_creation",
    "test_log_file_format",
)

# Frozen case table.  `expected` is the eight-leg vector derived from the grader's source,
# leg by leg, before the battery ran; `note` is what the case stages.
CASES = (
    {
        "id": "K1",
        "note": "all-green end state: service, bodies, config, shim, access log",
        "index": "Welcome to the benchmark webserver",
        "notfound": "Page not found - Please check your URL",
        "log": True,
        "shim": True,
        "rate_limit": True,
        "expected": "PPPPPPPP",
    },
    {
        "id": "K2",
        "note": "index body differs by one character (server otherwise green)",
        "index": "Welcome to the benchmark webserver!",
        "notfound": "Page not found - Please check your URL",
        "log": True,
        "shim": True,
        "rate_limit": True,
        "expected": "PPFPPPPP",
    },
    {
        "id": "K3",
        "note": "service answers but writes no access log",
        "index": "Welcome to the benchmark webserver",
        "notfound": "Page not found - Please check your URL",
        "log": False,
        "shim": True,
        "rate_limit": True,
        "expected": "PPPPPPFF",
    },
    {
        "id": "K4",
        "note": "config lacks the limit_req_zone rate clause",
        "index": "Welcome to the benchmark webserver",
        "notfound": "Page not found - Please check your URL",
        "log": True,
        "shim": True,
        "rate_limit": False,
        "expected": "PPPPPFPP",
    },
    {
        "id": "K5",
        "note": "no nginx binary on PATH (shim absent)",
        "index": "Welcome to the benchmark webserver",
        "notfound": "Page not found - Please check your URL",
        "log": True,
        "shim": False,
        "rate_limit": True,
        "expected": "FPPPFPPP",
    },
)

FROZEN_VECTOR = "/".join(c["expected"] for c in CASES)

NGINX_CONF = """\
events {{
    worker_connections 128;
}}
http {{
    log_format benchmark '$remote_addr - [$time_local] "$request_method $request_uri" '
                         '$status $body_bytes_sent "$http_user_agent"';
{rate}    access_log /var/log/nginx/benchmark-access.log benchmark;
    server {{
        listen 8080;
        root /var/www/html;
        location / {{
            index index.html;
        }}
    }}
}}
"""

SITE_CONF = """\
server {{
    listen 8080;
    root /var/www/html;
    location = / {{
        return 200 'Welcome to the benchmark webserver';
    }}
    error_page 404 /404.html;
    location = /404.html {{
        internal;
        return 404 'Page not found - Please check your URL';
    }}
}}
"""

SHIM = """\
#!/bin/sh
# lane-written stand-in for the nginx binary: the grader only asks `nginx -t`.
if [ "$1" = "-t" ]; then
    exit 0
fi
exit 0
"""

SERVER = r'''
import argparse, http.server, socketserver, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, required=True)
ap.add_argument("--index", default="")
ap.add_argument("--notfound", default="")
ap.add_argument("--log", default="")
args = ap.parse_args()

INDEX = args.index.encode()
NOTFOUND = args.notfound.encode()
LOG = args.log


def log_line(path, status, length, ua):
    if not LOG:
        return
    ts = time.strftime("%d/%b/%Y:%H:%M:%S %z")
    line = ('127.0.0.1 - - [%s] "GET %s HTTP/1.1" %d %d "-" "%s"\n'
            % (ts, path, status, length, ua))
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body, status = INDEX, 200
        else:
            body, status = NOTFOUND, 404
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        ua = self.headers.get("User-Agent", "")
        log_line(self.path, status, len(body), ua)

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


with Server(("127.0.0.1", args.port), Handler) as httpd:
    print("READY", flush=True)
    httpd.serve_forever()
'''

RUNNER = r'''
import importlib.util, sys, time, traceback

NAMES = sys.argv[1].split(",")
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in NAMES:
    fn = getattr(mod, name)
    started = time.time()
    try:
        fn()
        print("TEST %s P %.0fms" % (name, (time.time() - started) * 1000), flush=True)
    except AssertionError as exc:
        print("TEST %s F %.0fms %s" % (name, (time.time() - started) * 1000,
                                       str(exc).replace("\n", " ")[:160]), flush=True)
    except BaseException as exc:
        print("TEST %s E:%s %.0fms %s" % (name, type(exc).__name__,
                                          (time.time() - started) * 1000,
                                          str(exc).replace("\n", " ")[:120]), flush=True)
'''


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(pathlib.Path(path).read_bytes())


def own_sha256():
    return sha256_file(pathlib.Path(__file__).resolve())


def lane_root():
    return pathlib.Path(__file__).resolve().parent.parent


def case_dir_sha(case_root):
    """Digest of the staged end state: sorted relative path + bytes for every file."""
    h = hashlib.sha256()
    for p in sorted(case_root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(case_root).as_posix()
            h.update(rel.encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def acquire_port_lock(timeout=900):
    """One battery at a time: two seats may run this probe in the same wave."""
    import fcntl
    p = pathlib.Path(LOCK_PATH)
    p.parent.mkdir(parents=True, exist_ok=True)
    fh = open(p, "a+")
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fh
        except BlockingIOError:
            if time.time() > deadline:
                fh.close()
                raise RuntimeError("port-lock-timeout")
            time.sleep(1)


def port_free(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def stage_case(work, case):
    root = work / case["id"]
    if root.exists():
        shutil.rmtree(root)
    for sub in ("app", "tests", "etc/nginx/conf.d", "var/log/nginx", "var/www/html",
                "shim", "run"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    grader = (lane_root() / GRADER_REL).read_bytes()
    (root / "tests/test_outputs.py").write_bytes(grader)
    (root / "tests/runner.py").write_text(RUNNER, encoding="utf-8")
    rate = ("    limit_req_zone $binary_remote_addr zone=bench:10m rate=10r/s;\n"
            if case["rate_limit"] else "")
    (root / "etc/nginx/nginx.conf").write_text(NGINX_CONF.format(rate=rate), encoding="utf-8")
    (root / "etc/nginx/conf.d/benchmark-site.conf").write_text(SITE_CONF, encoding="utf-8")
    (root / "etc/hosts").write_text("127.0.0.1 localhost\n::1 localhost\n", encoding="utf-8")
    if case["log"]:
        log = root / "var/log/nginx/benchmark-access.log"
        log.write_text("", encoding="utf-8")
    if case["shim"]:
        shim = root / "shim/nginx"
        shim.write_text(SHIM, encoding="utf-8")
        shim.chmod(0o755)
    payload = {"index": case["index"], "notfound": case["notfound"],
               "log": str(root / "var/log/nginx/benchmark-access.log") if case["log"] else ""}
    (root / "run/server.json").write_text(json.dumps(payload), encoding="utf-8")
    (root / "run/server.py").write_text(SERVER, encoding="utf-8")
    return root


def bwrap_argv(root):
    shim = root / "shim"
    argv = [
        BWRAP,
        "--ro-bind", "/usr", "/usr",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib", "/lib64",
        "--symlink", "usr/bin", "/bin",
        "--ro-bind", "/home/vgpnk", "/home/vgpnk",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--dir", "/etc",
        "--dir", "/etc/nginx",
        "--ro-bind", str(root / "etc/hosts"), "/etc/hosts",
        "--ro-bind", str(root / "etc/nginx/nginx.conf"), "/etc/nginx/nginx.conf",
        "--ro-bind", str(root / "etc/nginx/conf.d"), "/etc/nginx/conf.d",
        "--dir", "/var",
        "--dir", "/var/log",
        "--dir", "/var/log/nginx",
        "--bind", str(root / "var/log/nginx"), "/var/log/nginx",
        "--dir", "/var/www",
        "--dir", "/var/www/html",
        "--ro-bind", str(root / "tests"), "/tests",
        "--ro-bind", str(root / "app"), "/app",
        "--ro-bind", str(shim), "/shim",
        "--setenv", "PATH", "/shim:/usr/bin:/bin",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--chdir", "/app",
        "--unshare-pid",
        "--unshare-ipc",
        "--unshare-uts",
        "/usr/bin/python3", "/tests/runner.py", ",".join(LEGS),
    ]
    return argv


def start_server(root):
    cfg = json.loads((root / "run/server.json").read_text(encoding="utf-8"))
    argv = [sys.executable, str(root / "run/server.py"), "--port", str(PORT),
            "--index", cfg["index"], "--notfound", cfg["notfound"], "--log", cfg["log"]]
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    line = proc.stdout.readline().strip()
    if line != "READY":
        err = proc.stderr.read()
        proc.kill()
        raise RuntimeError(f"server did not bind: {line!r} {err[:200]!r}")
    return proc


def run_case(work, case):
    root = stage_case(work, case)
    case_sha = case_dir_sha(root)
    server = None
    try:
        server = start_server(root)
        run = subprocess.run(bwrap_argv(root), capture_output=True, text=True, timeout=300)
        out = run.stdout
        err = run.stderr
    finally:
        if server is not None:
            server.kill()
            server.wait(timeout=10)
    legs = {}
    for line in out.splitlines():
        parts = line.split(" ")
        if len(parts) >= 4 and parts[0] == "TEST":
            outcome = parts[2]
            legs[parts[1]] = ("P" if outcome == "P" else ("F" if outcome == "F" else "F"))
    vector = "".join(legs.get(name, "?") for name in LEGS)
    return {
        "id": case["id"],
        "note": case["note"],
        "case_sha256": case_sha,
        "vector": vector,
        "expected": case["expected"],
        "observed_raw": {name: legs.get(name, "MISSING") for name in LEGS},
        "stdout": out,
        "stderr": err,
        "rc": run.returncode,
        "server_pid": server.pid if server else None,
    }


def run_battery(lane, work, receipt, evidence_dir):
    work = pathlib.Path(work)
    lane = pathlib.Path(lane)
    grader = lane / GRADER_REL
    if not grader.is_file():
        print(f"SETUP grader-absent {GRADER_REL}")
        return 2
    digest = sha256_file(grader)
    if digest != GRADER_SHA256:
        print(f"SETUP grader-sha-mismatch {digest}")
        return 2
    if not pathlib.Path(BWRAP).is_file():
        print(f"SETUP bwrap-absent at {BWRAP}")
        return 2
    try:
        lock = acquire_port_lock()
    except RuntimeError as exc:
        print(f"SETUP {exc}")
        return 2
    try:
        if not port_free(PORT):
            print(f"SETUP port-{PORT}-occupied")
            return 2
        if receipt and pathlib.Path(receipt).exists():
            print(f"SETUP receipt-exists {receipt}")
            return 2
        results = [run_case(work, case) for case in CASES]
    finally:
        lock.close()
    if evidence_dir:
        ed = pathlib.Path(evidence_dir)
        ed.mkdir(parents=True, exist_ok=True)
        for res in results:
            (ed / f"{res['id']}-sandbox.txt").write_text(
                f"rc={res['rc']} server_pid={res['server_pid']}\n"
                f"--- stdout\n{res['stdout']}\n--- stderr\n{res['stderr']}\n",
                encoding="utf-8")
    lines = [
        f"PROBE plans/round69_c1_nginx_probe.py sha256 {own_sha256()}",
        f"PROBE_VERSION {PROBE_VERSION}",
        f"GRADER {GRADER_REL} sha256 {digest} pin {TB2_PIN}",
        f"PORT {PORT} free-at-start=True lock={LOCK_PATH}",
    ]
    seen_p = {name: 0 for name in LEGS}
    seen_f = {name: 0 for name in LEGS}
    mismatches = 0
    setup = 0
    for res in results:
        lines.append(f"CASE {res['id']} case_sha256={res['case_sha256']} "
                     f"server_pid={res['server_pid']} sandbox_rc={res['rc']}")
        for name in LEGS:
            obs = res["observed_raw"][name]
            lines.append(f"TEST {res['id']} {name} {obs}")
            if obs == "P":
                seen_p[name] += 1
            elif obs == "F":
                seen_f[name] += 1
            else:
                setup += 1
        agree = res["vector"] == res["expected"]
        if not agree:
            mismatches += 1
        lines.append(f"VECTOR {res['id']} {res['vector']} expected {res['expected']} "
                     f"agree={agree}")
    full_p = sum(1 for name in LEGS if seen_p[name] >= 1)
    full_f = sum(1 for name in LEGS if seen_f[name] >= 1)
    lines.append(f"LEG-COVERAGE legs={len(LEGS)} seen_p={full_p} seen_f={full_f}")
    ok = (mismatches == 0 and setup == 0 and full_p == len(LEGS) and full_f == len(LEGS))
    lines.append(f"SUMMARY cases={len(results)} legs={len(results) * len(LEGS)} "
                 f"mismatches={mismatches} setup={setup}")
    lines.append(f"PREDICATE R69-C1 {'pass' if ok else 'fail'}")
    body = "\n".join(lines) + "\n"
    if receipt:
        pathlib.Path(receipt).write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)
    return 0 if ok else 1


def check_receipt(path):
    path = pathlib.Path(path)
    if not path.is_file():
        print(f"SETUP receipt-missing {path}")
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    defects = []

    def defect(kind, detail):
        defects.append(f"DEFECT {kind} {detail}")

    def starts(prefix):
        return [ln for ln in lines if ln.startswith(prefix)]

    probe = starts("PROBE plans/round69_c1_nginx_probe.py sha256 ")
    if len(probe) != 1:
        defect("probe-line", f"n={len(probe)}")
    else:
        got = probe[0].rsplit(" ", 1)[-1]
        if got != own_sha256():
            defect("probe-sha", got)
    grader = starts(f"GRADER {GRADER_REL} sha256 ")
    if len(grader) != 1:
        defect("grader-line", f"n={len(grader)}")
    else:
        parts = grader[0].split()
        if parts[3] != GRADER_SHA256:
            defect("grader-sha", parts[3])
        if TB2_PIN not in grader[0]:
            defect("grader-pin", grader[0])

    vectors = {}
    legs = {}
    for ln in lines:
        if ln.startswith("VECTOR "):
            parts = ln.split()
            if len(parts) != 5:
                defect("vector-line", ln)
                continue
            vectors[parts[1]] = (parts[2], parts[4].split("=")[-1])
        elif ln.startswith("TEST "):
            parts = ln.split()
            if len(parts) != 4:
                defect("test-line", ln)
                continue
            legs.setdefault(parts[1], {})[parts[2]] = parts[3]

    expected_ids = [c["id"] for c in CASES]
    if sorted(vectors) != sorted(expected_ids):
        defect("case-set", f"got={sorted(vectors)} want={sorted(expected_ids)}")
    seen_p = {name: 0 for name in LEGS}
    seen_f = {name: 0 for name in LEGS}
    for case in CASES:
        cid = case["id"]
        got = vectors.get(cid)
        if not got:
            continue
        obs, stored_agree = got
        if obs != case["expected"]:
            defect("vector-mismatch", f"{cid} {obs} != {case['expected']}")
        if stored_agree != "True":
            defect("vector-agree", f"{cid} agree={stored_agree}")
        case_legs = legs.get(cid, {})
        if sorted(case_legs) != sorted(LEGS):
            defect("leg-set", f"{cid} got={sorted(case_legs)}")
        derived = "".join("P" if case_legs.get(name) == "P" else "F" for name in LEGS)
        if derived != obs:
            defect("leg-vector", f"{cid} legs={derived} vector={obs}")
        for name in LEGS:
            if case_legs.get(name) == "P":
                seen_p[name] += 1
            elif case_legs.get(name) == "F":
                seen_f[name] += 1
            else:
                defect("leg-missing", f"{cid} {name}")
    for name in LEGS:
        if seen_p[name] == 0 or seen_f[name] == 0:
            defect("leg-coverage", f"{name} p={seen_p[name]} f={seen_f[name]}")
    summary = starts("SUMMARY cases=")
    if len(summary) != 1 or "mismatches=0" not in summary[0] or "setup=0" not in summary[0]:
        defect("summary", summary[0] if summary else "missing")
    stored = starts("PREDICATE R69-C1 ")
    if len(stored) != 1:
        defect("predicate-line", f"n={len(stored)}")
    elif not stored[0].endswith(" pass"):
        defect("stored-predicate", stored[0])
    derived_ok = not defects
    print(f"CHECK ok cases={len(CASES)} legs={len(LEGS)} "
          f"seen_p={sum(1 for n in LEGS if seen_p[n])} "
          f"seen_f={sum(1 for n in LEGS if seen_f[n])}")
    for d in defects:
        print(d)
    print(f"CHECK stored-predicate={'pass' if stored and stored[0].endswith(' pass') else 'fail'} "
          f"derived={'pass' if derived_ok else 'fail'}")
    print(f"PREDICATE R69-C1 {'pass' if derived_ok else 'fail'}")
    return 0 if derived_ok else 1


def run_selftest(work, green_receipt):
    work = pathlib.Path(work)
    if not work.is_dir():
        print("SETUP work-dir-required (not a directory)")
        return 2
    red = work / "selftest-red"
    red.mkdir(parents=True, exist_ok=True)
    real = own_sha256()
    zero = "0" * 64

    def body(vectors, probe_sha=real, grader_sha=GRADER_SHA256, drop_leg=None,
             dup_leg=False):
        out = [f"PROBE plans/round69_c1_nginx_probe.py sha256 {probe_sha}",
               f"PROBE_VERSION {PROBE_VERSION}",
               f"GRADER {GRADER_REL} sha256 {grader_sha} pin {TB2_PIN}",
               f"PORT {PORT} free-at-start=True"]
        for case in CASES:
            cid = case["id"]
            vec = vectors.get(cid, case["expected"])
            out.append(f"CASE {cid} case_sha256={zero} server_pid=1234 sandbox_rc=0")
            for i, name in enumerate(LEGS):
                if drop_leg and cid == drop_leg[0] and name == drop_leg[1]:
                    continue
                obs = "P" if vec[i] == "P" else "F"
                out.append(f"TEST {cid} {name} {obs}")
                if dup_leg and cid == "K1" and name == LEGS[0]:
                    out.append(f"TEST {cid} {name} P")
            out.append(f"VECTOR {cid} {vec} expected {case['expected']} agree=True")
        out.append(f"SUMMARY cases={len(CASES)} legs={len(CASES) * len(LEGS)} "
                   f"mismatches=0 setup=0")
        out.append("PREDICATE R69-C1 pass")
        return "\n".join(out) + "\n"

    fixtures = {
        "r1-all-p": body({c["id"]: "P" * 8 for c in CASES}),
        "r2-probe-sha": body({}, probe_sha=zero),
        "r3-leg-vector": body({"K2": "PPPPPPPP"}),
        "r4-missing-leg": body({}, drop_leg=("K1", "test_nginx_running")),
        "r5-grader-sha": body({}, grader_sha=zero),
    }
    tally = []
    ok = True
    for name, text in fixtures.items():
        p = red / f"{name}.txt"
        p.write_text(text, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_receipt(p)
        refused = rc == 1
        tally.append(f"RED {name} rc={rc} refused={refused}")
        if not refused:
            ok = False
    if green_receipt:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_receipt(pathlib.Path(green_receipt))
        tally.append(f"GREEN receipt rc={rc} accepted={rc == 0}")
        if rc != 0:
            ok = False
    for t in tally:
        print(t)
    red_n = sum(1 for t in tally if t.startswith("RED") and "refused=True" in t)
    green_n = sum(1 for t in tally if t.startswith("GREEN") and "accepted=True" in t)
    print(f"SELFTEST red_refused={red_n}/{len(fixtures)} green_ok={green_n} ok={ok}")
    return 0 if ok else 1


def render_table():
    print("case  setup                                                     vector")
    for case in CASES:
        print(f"{case['id']}    {case['note']:<58} {case['expected']}")
    print(f"FROZEN-VECTOR {FROZEN_VECTOR}")
    print(f"LEGS {len(LEGS)}")
    return 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--lane")
    ap.add_argument("--work")
    ap.add_argument("--receipt")
    ap.add_argument("--evidence-dir")
    ap.add_argument("--check-receipt")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--green-receipt")
    ap.add_argument("--render-table", action="store_true")
    args = ap.parse_args(argv)

    if args.render_table:
        return render_table()
    if args.check_receipt:
        return check_receipt(args.check_receipt)
    if args.selftest:
        if not args.work:
            print("SETUP work-dir-required")
            return 2
        return run_selftest(args.work, args.green_receipt)
    if not args.work:
        print("SETUP work-dir-required")
        return 2
    if not pathlib.Path(args.work).is_dir():
        print(f"SETUP work-dir-required (not a directory: {args.work})")
        return 2
    if not args.lane:
        print("SETUP lane-required")
        return 2
    return run_battery(args.lane, args.work, args.receipt, args.evidence_dir)


if __name__ == "__main__":
    sys.exit(main())
