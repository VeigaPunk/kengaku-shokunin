"""Independent reproduction of the K6/K7 red legs without the probe's runner.

Imports the committed grader at its lane path and calls its own test functions against a
hand-rolled HTTP server on 127.0.0.1:8080 (this file's server, not the probe's staged
run/server.py).  Prints, for each call, the exception class and message the grader itself
raises.
"""
import http.server
import importlib.util
import socketserver
import threading
import time
from pathlib import Path

GRADER = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52"
              "/graders/nginx-request-logging/tests/test_outputs.py")
INDEX = "Welcome to the benchmark webserver"
GOOD_404 = "Page not found - Please check your URL"
BAD_404 = GOOD_404 + "!"

spec = importlib.util.spec_from_file_location("tb2_grader", GRADER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def serve(index, notfound):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                body, status = index.encode(), 200
            else:
                body, status = notfound.encode(), 404
            self.send_response(status)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    srv = Server(("127.0.0.1", 8080), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def call(label, fn):
    started = time.time()
    try:
        fn()
        print("REPRO %s PASS %.0fms" % (label, (time.time() - started) * 1000))
    except AssertionError as exc:
        print("REPRO %s ASSERTION %.0fms %r"
              % (label, (time.time() - started) * 1000, str(exc)))
    except BaseException as exc:  # noqa: BLE001 - we are classifying the grader's failures
        print("REPRO %s EXC:%s %.0fms %r"
              % (label, type(exc).__name__, (time.time() - started) * 1000, str(exc)[:120]))


print("REPRO grader_sha256 %s" % __import__("hashlib").sha256(GRADER.read_bytes()).hexdigest())
call("no-service:test_nginx_running", mod.test_nginx_running)
call("no-service:test_index_page_content", mod.test_index_page_content)
call("no-service:test_custom_404_page", mod.test_custom_404_page)

srv = serve(INDEX, BAD_404)
try:
    call("K7-body:test_nginx_running", mod.test_nginx_running)
    call("K7-body:test_index_page_content", mod.test_index_page_content)
    call("K7-body:test_custom_404_page", mod.test_custom_404_page)
finally:
    srv.shutdown()
    srv.server_close()
time.sleep(0.2)

srv = serve(INDEX, GOOD_404)
try:
    call("K1-body:test_custom_404_page", mod.test_custom_404_page)
    call("K1-body:test_index_page_content", mod.test_index_page_content)
finally:
    srv.shutdown()
    srv.server_close()
