#!/usr/bin/env python3
"""Round-37 C2 probe: the pinned Terminal-Bench 2.0 `configure-git-webserver` grader, executed offline.

  python3 plans/git_webserver_probe.py --lane .          run every frozen case, print the receipt
  python3 plans/git_webserver_probe.py --lane . --dry    print the frozen case table only (no sandbox)
  python3 plans/git_webserver_probe.py --lane . --smoke  exercise the sandbox plumbing without the grader

What runs: the captured grader `tests/test_outputs.py` (S111) and its helper `tests/verify.sh` (S112),
byte-identical to terminal-bench-2 @ 2fd12b88 (digests checked before any case), inside a bubblewrap
sandbox per case: private network namespace (own loopback, so :8080 is never the host's), private
/tmp, HOME=/work/home (verify.sh writes ~/.ssh/config there, never in the operator's home),
/tests bound read-only to the captures, and PATH=/work/bin holding only the tools the case names.
`apt-get` and `expect` are absent in every case, so verify.sh's install step and its git
clone/commit/push step (the expect script) fail exactly as they would in any container where they
fail; nothing in verify.sh reads their exit status. The case's HTTP server (or none) is started
before the grader. The grader function `test_hello_html_exists` is imported from the capture and
called directly: an AssertionError is `fail`, any other exception is `fail` with its class named,
a return is `pass` (pytest's verdict for one fixture-less test function; the reward mapping in
tests/test.sh is 1 iff pytest exits 0).

Limits, stated before the first run: the oracle `solution/solve.sh` is not executed (it needs root,
apt, nginx and sshd); no case exercises a real git push, so this probe shows what the grader's
verdict depends on, never that the intended path passes. Predictions below were written from a
static reading of verify.sh, test_outputs.py and instruction.md before the first run.

Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under
--work, else $TMPDIR (tempfile default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round37/tb2-git-webserver"
PINS = {
    "test_outputs.py": "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37",
    "verify.sh": "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05",
    "instruction.md": "62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97",
}
BASE_TOOLS = ("bash", "sleep", "chmod", "mkdir", "cat")
BWRAP = "/usr/bin/bwrap"


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    tools: str          # "curl", "wget" (curl absent from PATH), or "curl+wget"
    server: dict        # see SERVER_PY; {} = no server
    predicted: str      # "pass" | "fail"
    requirement: str    # the instruction line or grader mechanism the case tests


HW = "hello world"


def files(body, status=200, headers=None, port=8080, path="/hello.html"):
    return {"mode": "files", "port": port, "routes": {path: [status, body, headers or {}]}}


CASES = [
    Case("no-server", "curl", {}, "fail",
         "verify.sh:57-59 — nothing listens on :8080, curl reports 000, the 200 branch is skipped"),
    Case("static-file-no-git", "curl", files(HW + "\n"), "pass",
         "instruction.md:1-6 asks for a git server and a push; verify.sh:49 never reads the expect step's status;"
         " a file served with no repository, hook or push"),
    Case("exact-no-newline", "curl", files(HW), "pass",
         "instruction.md:9 — the literal output 'hello world'"),
    Case("trailing-newlines", "curl", files(HW + "\n\n\n"), "pass",
         "verify.sh:60 — command substitution strips every trailing newline before the comparison at :63"),
    Case("capitalised", "curl", files("Hello World\n"), "fail",
         "verify.sh:63 — the comparison is case-sensitive"),
    Case("leading-space", "curl", files(" " + HW + "\n"), "fail",
         "verify.sh:63 — leading whitespace survives command substitution"),
    Case("trailing-space", "curl", files(HW + " \n"), "fail",
         "verify.sh:63 — only newlines are stripped, a trailing space is not"),
    Case("crlf", "curl", files(HW + "\r\n"), "fail",
         "verify.sh:63 — a carriage return survives command substitution"),
    Case("bom", "curl", files("\ufeff" + HW + "\n"), "fail",
         "verify.sh:63 — a byte-order mark is part of the content"),
    Case("empty-200", "curl", files(""), "fail",
         "verify.sh:63 — an empty body is not 'hello world'"),
    Case("not-found", "curl", {"mode": "files", "port": 8080, "routes": {}}, "fail",
         "verify.sh:59 — a 404 for /hello.html skips the content branch"),
    Case("http-500-right-body", "curl", files(HW + "\n", status=500), "fail",
         "verify.sh:59 — the status must be exactly 200 even when the body is right"),
    Case("redirect-301", "curl",
         {"mode": "files", "port": 8080,
          "routes": {"/hello.html": [301, "", {"Location": "/real.html"}], "/real.html": [200, HW + "\n", {}]}},
         "fail", "verify.sh:57 — curl runs without -L, so a redirect is a non-200 status"),
    Case("catch-all-200", "curl", {"mode": "catchall", "port": 8080, "body": HW + "\n"}, "pass",
         "verify.sh:57,60 — only /hello.html is requested; a server answering every path passes"),
    Case("wrong-port-8081", "curl", files(HW + "\n", port=8081), "fail",
         "instruction.md:7 — 'a webserver running on port 8080'; nothing on :8080"),
    Case("token-in-body", "curl", files("TEST PASSED\n"), "pass",
         "test_outputs.py:13 — the verdict is a substring of verify.sh's stdout, and verify.sh:62 echoes the body"),
    Case("status-then-content-split", "curl",
         {"mode": "sequence", "port": 8080, "path": "/hello.html",
          "responses": [[200, "not the content\n"], [200, HW + "\n"]]}, "pass",
         "verify.sh:57,60 — status and content come from two separate requests; the first body is never compared"),
    Case("first-request-404", "curl",
         {"mode": "sequence", "port": 8080, "path": "/hello.html",
          "responses": [[404, ""], [200, HW + "\n"]]}, "fail",
         "verify.sh:57-59 — the first request's status decides whether the content is fetched at all"),
    Case("slow-server-3s", "curl", {**files(HW + "\n"), "delay": 3}, "pass",
         "verify.sh:57,60 — curl is run without a timeout, so a slow answer still counts"),
    Case("wget-static-file", "wget", files(HW + "\n"), "pass",
         "verify.sh:73-80 — the wget branch, taken when curl is absent, compares the same content"),
    Case("wget-404", "wget", {"mode": "files", "port": 8080, "routes": {}}, "fail",
         "verify.sh:75-76 — wget exits nonzero on 404, so the content branch is skipped"),
    Case("wget-token-in-body", "wget", files("TEST PASSED\n"), "pass",
         "test_outputs.py:13 with verify.sh:79 — the body echo carries the token on the wget branch too"),
]

SERVER_PY = r'''
import http.server, json, pathlib, socketserver, time
cfg = json.loads(pathlib.Path("/work/server.json").read_text())
count = {"n": 0}
class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def log_message(self, *a):
        pass
    def answer(self):
        if cfg.get("delay"):
            time.sleep(cfg["delay"])
        mode = cfg["mode"]
        headers = {}
        if mode == "catchall":
            status, body = 200, cfg["body"]
        elif mode == "sequence":
            if self.path != cfg["path"]:
                status, body = 404, ""
            else:
                seq = cfg["responses"]
                status, body = seq[min(count["n"], len(seq) - 1)]
                count["n"] += 1
        else:
            status, body, headers = cfg["routes"].get(self.path, [404, "", {}])
        data = body.encode("utf-8")
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)
    do_GET = answer
    do_HEAD = answer
class S(socketserver.TCPServer):
    allow_reuse_address = True
srv = S(("127.0.0.1", cfg["port"]), H)
pathlib.Path("/work/ready").write_text("1")
srv.serve_forever()
'''

HARNESS_PY = r'''
import importlib.util, subprocess
seen = {}
_run = subprocess.run
def tee(*a, **k):
    r = _run(*a, **k)
    seen["stdout"] = r.stdout
    return r
subprocess.run = tee
spec = importlib.util.spec_from_file_location("tb2_cgw_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
try:
    mod.test_hello_html_exists()
    print("VERDICT pass")
except AssertionError:
    print("VERDICT fail")
except Exception as e:
    print("VERDICT fail error=" + type(e).__name__)
for line in (seen.get("stdout") or "").splitlines():
    print("STDOUT " + repr(line))
'''

RUN_SH = r'''#!/usr/bin/bash
if [ -s /work/server.json ]; then /usr/bin/python3 /work/server.py & fi
if [ -s /work/server.json ]; then
  for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40; do
    [ -e /work/ready ] && break
    /usr/bin/sleep 0.1
  done
  [ -e /work/ready ] || { echo "SETUP server-not-ready"; exit 3; }
fi
cd /work/cwd && exec /usr/bin/python3 /work/HARNESS
'''


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--dir", "/tests",
             "--ro-bind", str(cap / "verify.sh"), "/tests/verify.sh",
             "--ro-bind", str(cap / "test_outputs.py"), "/tests/test_outputs.py",
             "--bind", str(work), "/work", "--chdir", "/work/cwd"]
    if os.path.exists("/usr/bin/expect"):  # keep `expect` absent whatever the host has installed
        argv += ["--ro-bind", "/dev/null", "/usr/bin/expect"]
    return argv


def prepare(work, tools, server, script):
    for sub in ("home", "cwd", "bin"):
        (work / sub).mkdir(parents=True)
    names = list(BASE_TOOLS) + {"curl": ["curl"], "wget": ["wget"], "curl+wget": ["curl", "wget"]}[tools]
    for n in names:
        (work / "bin" / n).symlink_to(f"/usr/bin/{n}")
    (work / "server.py").write_text(SERVER_PY)
    (work / "server.json").write_text(json.dumps(server) if server else "")
    (work / "HARNESS").write_text(script)
    (work / "run.sh").write_text(RUN_SH)


def run_case(cap, root, case, script=HARNESS_PY):
    work = pathlib.Path(tempfile.mkdtemp(prefix="cgw-", dir=root))
    try:
        prepare(work, case.tools, case.server, script)
        env = {"PATH": "/work/bin", "HOME": "/work/home", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/bash", "/work/run.sh"], env=env,
                           capture_output=True, text=True, timeout=180)
        return r.returncode, r.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent (default: $TMPDIR via tempfile)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids):
        print("SETUP duplicate case id", file=sys.stderr)
        return 2
    if a.dry:
        for c in CASES:
            print(f"CASE {c.cid} tools={c.tools} predicted={c.predicted} server={json.dumps(c.server, sort_keys=True)}"
                  f" -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(c.predicted == 'pass' for c in CASES)}"
              f" predicted_fail={sum(c.predicted == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    if not os.access(BWRAP, os.X_OK):
        print("SETUP bubblewrap (/usr/bin/bwrap) is required", file=sys.stderr)
        return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-cgw-", dir=a.work))
    try:
        if a.smoke:
            smoke = Case("smoke", "curl", files("smoke-body\n"), "n/a", "plumbing only")
            script = ("import subprocess\nr = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',"
                      " 'http://localhost:8080/hello.html'], capture_output=True, text=True)\n"
                      "print('SMOKE status=' + r.stdout)\n")
            rc, out = run_case(cap, root, smoke, script)
            print(out, end="")
            print(f"SMOKE rc={rc}")
            return 0 if rc == 0 and "SMOKE status=200" in out else 1
        print("# tb2 configure-git-webserver grader probe (kengaku round 37) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = 0
        for c in CASES:
            rc, out = run_case(cap, root, c)
            verdict = [l for l in out.splitlines() if l.startswith("VERDICT ")]
            if rc != 0 or len(verdict) != 1:
                print(f"SETUP case {c.cid} did not yield one verdict (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            obs = verdict[0].split()[1]
            err = verdict[0].split()[2] if len(verdict[0].split()) > 2 else ""
            npass += obs == "pass"
            nfail += obs == "fail"
            match = obs == c.predicted
            mism += not match
            print(f"CASE {c.cid} tools={c.tools} predicted={c.predicted} observed={obs}"
                  f"{' ' + err if err else ''} match={'yes' if match else 'NO'} -- {c.requirement}")
            stdout = [l[len("STDOUT "):] for l in out.splitlines() if l.startswith("STDOUT ")]
            print("  grader-stdout: " + (" | ".join(stdout) if stdout else "(none)"))
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
