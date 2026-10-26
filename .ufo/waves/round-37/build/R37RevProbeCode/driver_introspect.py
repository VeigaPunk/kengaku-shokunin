"""R37RevProbeCode: isolation introspection of the frozen probe's sandbox.

Runs one custom case through the FROZEN probe's own run_case/sandbox_argv (unmodified),
with a host-side canary listener on 127.0.0.1:8080 to prove --unshare-net.
"""
import importlib.util
import http.server
import pathlib
import sys
import threading

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
spec = importlib.util.spec_from_file_location("probe", LANE + "/plans/git_webserver_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules["probe"] = probe
spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
root = pathlib.Path(sys.argv[1])

INTROSPECT = r'''
import os, socket
print("HOME=" + os.environ.get("HOME", "?"))
print("PATH=" + os.environ.get("PATH", "?"))
print("ENVKEYS=" + ",".join(sorted(os.environ)))
print("ROOT=" + ",".join(sorted(os.listdir("/"))))
print("TMP=" + ",".join(sorted(os.listdir("/tmp"))))
print("DEV=" + ",".join(sorted(os.listdir("/dev"))))
print("PROC_PIDS=" + str(len([p for p in os.listdir("/proc") if p.isdigit()])))
print("WORK=" + ",".join(sorted(os.listdir("/work"))))
for label, path in (("TESTS", "/tests/verify.sh"), ("ETC", "/etc/passwd"),
                    ("USR", "/usr/bin/ls"), ("PROC", "/proc/self/status")):
    try:
        with open(path, "a") as f:
            f.write("x")
        print(label + "-WRITE ok")
    except OSError as e:
        print(label + "-WRITE " + type(e).__name__)
try:
    s = socket.create_connection(("127.0.0.1", 8080), timeout=3)
    print("NET-8080 connected")
    s.close()
except OSError as e:
    print("NET-8080 " + type(e).__name__)
try:
    os.makedirs(os.path.join(os.environ["HOME"], ".ssh"), exist_ok=True)
    open(os.path.join(os.environ["HOME"], ".ssh", "config"), "w").write("Host localhost\n")
    print("HOME-SSH-WRITE ok")
except OSError as e:
    print("HOME-SSH-WRITE " + type(e).__name__)
open("/tmp/canary-inside", "w").write("x")
print("TMP-WRITE ok")
print("UID=" + str(os.getuid()))
'''


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        b = b"HOST-LEAK-CANARY"
        self.send_response(200)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8080), H)
t = threading.Thread(target=srv.serve_forever, daemon=True)
t.start()
case = probe.Case("introspect", "curl", {}, "n/a", "isolation introspection")
rc, out = probe.run_case(cap, root, case, script=INTROSPECT)
srv.shutdown()
print("rc=%d" % rc)
print(out)
