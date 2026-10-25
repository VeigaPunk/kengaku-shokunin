#!/usr/bin/env python3
"""Round-11 MOCK endpoint — schema smoke of run_r11.py against a local fake.

Binds 127.0.0.1:18113 ONLY; the real served endpoint (127.0.0.1:34113) never
receives a byte from this smoke. run_r11.py hardcodes HOST=...34113 for its
descriptors' GET /v1/models (KENGAKU_R11_BASE only redirects probe_r11.call),
so the smoke sets http_proxy=http://127.0.0.1:18113: urllib then forwards ALL
traffic (absolute-form request lines) to this mock, which answers them here
and logs any request whose target host is not this mock as an INTERCEPT.

Content policy (keyed on the LAST user message of the request):
  contains 'ready'                      -> "ready"            (filler)
  contains "Reply 'ok'"                 -> "ok"               (ack ask)
  contains 'CHECKPOINT'                 -> graded-emit modulo (graded turn)
  otherwise (turn-1 / spillover FULL)   -> full-state emit, fence/bare alternating

Graded-emit modulo (per-process counter c, fixed):
  c % 3 == 0 -> valid fenced ```json block
  c % 3 == 1 -> valid bare brace object, NO fence (exercises
                probe_r11.extract_json_block's regex fallback)
  c % 3 == 2 -> malformed JSON object (parse-fail path: got=None,
                grade_state -> ok=False, nwrong=len(want))

Stdlib only. Usage: python3 mock_server_r11.py [port]  (default 18113).
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18113
SELF = f"127.0.0.1:{PORT}"
STATE = {"nails": 12, "bolts": 3, "screws": 7, "washers": 0, "hinges": 5}
lock = threading.Lock()
counters = {"ckpt": 0, "full": 0}

def emit(kind, tag, detail=""):
    print(f"{time.strftime('%H:%M:%S')} {kind} {tag} {detail}", flush=True)

def last_user(messages):
    for m in reversed(messages):
        if m.get("role") == "user":
            return m.get("content", "")
    return ""

def resp_content(content):
    body = {
        "choices": [{"message": {"role": "assistant", "content": content},
                     "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 100, "completion_tokens": max(1, len(content) // 4),
                  "total_tokens": 100 + max(1, len(content) // 4)},
    }
    return body

def chat_content(content):
    """Content policy -> (assistant text, tag)."""
    if "ready" in content:
        return "ready", "filler"
    if "Reply 'ok'" in content:
        return "ok", "ack-ok"
    if "CHECKPOINT" in content:
        with lock:
            c = counters["ckpt"]; counters["ckpt"] += 1
        if c % 3 == 0:
            return "```json\n" + json.dumps(STATE, indent=1) + "\n```", f"ckpt-{c}-fence"
        if c % 3 == 1:
            return json.dumps(STATE), f"ckpt-{c}-bare"
        return '{"nails": 12, "screws": }', f"ckpt-{c}-malformed"
    with lock:
        f = counters["full"]; counters["full"] += 1
    txt = json.dumps(STATE, indent=1) if f % 2 == 0 else json.dumps(STATE)
    return ("```json\n" + txt + "\n```") if f % 2 == 0 else txt, f"full-{f}"

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _target(self):
        """Normalize absolute-form (proxy) vs origin-form request paths."""
        path = self.path
        if path.startswith("http://") or path.startswith("https://"):
            rest = path.split("://", 1)[1]
            slash = rest.find("/")
            return rest[:slash], rest[slash:]
        return self.headers.get("Host", SELF), path

    def do_GET(self):
        host, path = self._target()
        kind = "INTERCEPT" if host != SELF else "DIRECT"
        if path.rstrip("/") == "/v1/models" or path.rstrip("/").endswith("/v1/models"):
            emit(kind, f"GET {host}{path}", "-> models")
            self._send({"data": [{"id": "mock-model"}]})
        else:
            emit(kind, f"GET {host}{path}", "-> 404")
            self._send({"error": "not found"}, 404)

    def do_POST(self):
        host, path = self._target()
        kind = "INTERCEPT" if host != SELF else "DIRECT"
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        content, tag = chat_content(last_user(body.get("messages", [])))
        emit(kind, f"POST {host}{path}", f"model={body.get('model')} -> {tag}")
        self._send(resp_content(content))

    def log_message(self, *a):  # silence default stderr chatter; we log our own lines
        pass

if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    emit("MOCK", f"listening on {SELF}", "policy: ready|Reply-ok|CHECKPOINT-modulo|full-alternate")
    srv.serve_forever()
