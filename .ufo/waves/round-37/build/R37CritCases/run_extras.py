#!/usr/bin/env python3
"""R37CritCases extras: the wget mismatch branch and a port-isolation fixture (predictions in
PREDICTIONS-extra.md, written first). Read-only on the lane; scratch under $TMPDIR."""
import hashlib
import importlib.util
import os
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/git_webserver_probe.py"
CAP = LANE / "corpus/evidence/round37/tb2-git-webserver"

spec = importlib.util.spec_from_file_location("cgw_probe", PROBE)
P = importlib.util.module_from_spec(spec)
sys.modules["cgw_probe"] = P
spec.loader.exec_module(P)

TWO_PORTS = r'''
import http.server, socketserver, subprocess, threading, time

class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def log_message(self, *a):
        pass
    def do_GET(self):
        body = b"hello world\n" if self.server.server_address[1] == 8081 else b"not hello\n"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

class S(socketserver.TCPServer):
    allow_reuse_address = True

for port in (8080, 8081):
    threading.Thread(target=S(("127.0.0.1", port), H).serve_forever, daemon=True).start()
time.sleep(0.5)
r = subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)
print("DIAG stdout=" + repr(r.stdout.splitlines()))
print("VERDICT " + ("pass" if "TEST PASSED" in r.stdout else "fail"))
'''


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")

    def write(self, s):
        sys.__stdout__.write(s)
        self.f.write(s)

    def flush(self):
        sys.__stdout__.flush()
        self.f.flush()


def main():
    sys.stdout = Tee(pathlib.Path(__file__).with_name("run_extras.log"))
    root = pathlib.Path(os.environ["TMPDIR"]) / "runs-extra"
    root.mkdir(parents=True, exist_ok=True)
    print("# probe sha256=" + hashlib.sha256(PROBE.read_bytes()).hexdigest())
    cases = [
        (P.Case("wget-wrong-content", "wget", P.files("Hello World\n"), "fail",
                "verify.sh:80 false -> :83 on the wget branch"), None),
        (P.Case("port-8080-junk-8081-correct", "curl", {}, "fail",
                "verify.sh:57 hard-codes :8080; :63 compares the :8080 body"), TWO_PORTS),
    ]
    print("# predictions (written first, PREDICTIONS-extra.md):")
    for c, _ in cases:
        print(f"PREDICT {c.cid} tools={c.tools} predicted={c.predicted} -- {c.requirement}")
    print("# observed:")
    matched = 0
    for c, script in cases:
        rc, out = P.run_case(CAP, root, c, script) if script else P.run_case(CAP, root, c)
        verdict = [l for l in out.splitlines() if l.startswith("VERDICT ")]
        if rc != 0 or len(verdict) != 1:
            print(f"CASE {c.cid} SETUP_FAILURE rc={rc}")
            print(out)
            continue
        obs = verdict[0].split()[1]
        match = obs == c.predicted
        matched += match
        print(f"CASE {c.cid} tools={c.tools} predicted={c.predicted} observed={obs} match={'yes' if match else 'NO'}")
        stdout = [l[len("STDOUT "):] for l in out.splitlines() if l.startswith("STDOUT ")]
        diag = [l[len("DIAG "):] for l in out.splitlines() if l.startswith("DIAG ")]
        if stdout:
            print("  grader-stdout: " + " | ".join(stdout))
        for d in diag:
            print("  " + d)
    print(f"extras matched={matched}/{len(cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
