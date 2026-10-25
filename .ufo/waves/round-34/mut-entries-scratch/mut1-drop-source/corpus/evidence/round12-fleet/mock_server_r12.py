#!/usr/bin/env python3
"""Round-12 local mock endpoint for schema smoke.

Binds only to 127.0.0.1 (default port 18114; argv[1] overrides).  The
runner's hard-coded 34113 model lookup is expected to arrive here as an
absolute-form proxy request; such requests are logged as INTERCEPT.

The last user message controls filler/ack/graded output.  Graded output is
replayed from the conversation's initial state and operations, then follows a
per-conversation turn cycle: fenced JSON, bare JSON, malformed JSON.  Even
turns are exact; odd turns are deterministically perturbed (including a
wrong-length list/key case).  Family 2 is recognized from its array initial
state and emits arrays.
"""
import json
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18114
SELF = f"127.0.0.1:{PORT}"


def emit(kind, tag, detail=""):
    print(f"{time.strftime('%H:%M:%S')} {kind} {tag} {detail}", flush=True)


def last_user(messages):
    for message in reversed(messages):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""


def apply_inventory(state, op):
    out = dict(state)
    kind = op[0]
    if kind == "SET": out[op[1]] = op[2]
    elif kind == "ADD": out[op[1]] += op[2]
    elif kind == "SUB": out[op[1]] -= op[2]
    elif kind == "MOV": out[op[2]] += out[op[1]]; out[op[1]] = 0
    elif kind == "DEL": del out[op[1]]
    elif kind == "NEW": out[op[1]] = op[2]
    return out


def apply_sequence(state, op):
    out = list(state)
    kind = op[0]
    if kind == "APP": out.append(op[1])
    elif kind == "INS": out.insert(op[1], op[2])
    elif kind == "DEL": out.pop(op[1])
    elif kind == "SET": out[op[1]] = op[2]
    elif kind == "MOV": out.insert(op[2], out.pop(op[1]))
    elif kind == "SWP": out[op[1]], out[op[2]] = out[op[2]], out[op[1]]
    elif kind == "REV": out[op[1]:op[2] + 1] = reversed(out[op[1]:op[2] + 1])
    return out


def parse_op(text, family):
    parts = text.strip().split()
    if not parts:
        return None
    kind = parts[0]
    if family == 1:
        if kind in ("SET", "ADD", "SUB", "NEW") and len(parts) >= 3:
            return (kind, parts[1], int(parts[2]))
        if kind == "MOV" and len(parts) >= 3: return (kind, parts[1], parts[2])
        if kind == "DEL" and len(parts) >= 2: return (kind, parts[1])
    else:
        if kind == "APP" and len(parts) >= 2: return (kind, parts[1])
        if kind in ("INS", "SET") and len(parts) >= 3: return (kind, int(parts[1]), parts[2])
        if kind in ("DEL",) and len(parts) >= 2: return (kind, int(parts[1]))
        if kind in ("MOV", "SWP", "REV") and len(parts) >= 3:
            return (kind, int(parts[1]), int(parts[2]))
    return None


def replay(messages):
    users = [m.get("content", "") for m in messages if m.get("role") == "user"]
    initial = next((x for x in users if "Initial state:" in x), "")
    match = re.search(r"Initial state:\s*(\{[^\n]*\}|\[[^\n]*\])", initial)
    if not match:
        return 1, {}, len(users)
    state = json.loads(match.group(1))
    family = 2 if isinstance(state, list) else 1
    for text in users:
        operations = []
        for line in text.splitlines():
            numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)
            if numbered:
                operations.append(numbered.group(1))
        nxt = re.search(r"Next operation:\s*([^\n]+)", text)
        if nxt:
            operations.append(nxt.group(1))
        for raw in operations:
            op = parse_op(raw, family)
            if op is not None:
                state = apply_sequence(state, op) if family == 2 else apply_inventory(state, op)
    return family, state, len(users)


def graded_content(messages):
    family, state, turn = replay(messages)
    exact = state
    if turn % 2 == 1:
        if family == 1:
            perturbed = dict(state)
            if turn % 4 == 1:
                key = sorted(perturbed)[0] if perturbed else "extra"
                perturbed[key] = perturbed.get(key, 0) + 1
            elif perturbed:
                perturbed.pop(sorted(perturbed)[0])
            else:
                perturbed["extra"] = 1
        else:
            perturbed = list(state)
            if turn % 4 == 1 and len(perturbed) >= 2:
                perturbed[0], perturbed[1] = perturbed[1], perturbed[0]
            elif perturbed:
                perturbed.pop()
            else:
                perturbed.append("extra")
    else:
        perturbed = exact
    cycle = (turn - 1) % 3
    value = json.dumps(perturbed, indent=1) if cycle == 0 else json.dumps(perturbed)
    if cycle == 2:
        value = json.dumps(perturbed)[:-1] + ","
        tag = f"graded-{turn}-malformed"
    elif cycle == 0:
        value = "```json\n" + value + "\n```"
        tag = f"graded-{turn}-fenced"
    else:
        tag = f"graded-{turn}-bare"
    return value, tag


def response(content):
    completion = max(1, len(content) // 4)
    return {"choices": [{"message": {"role": "assistant", "content": content},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": completion,
                      "total_tokens": 100 + completion}}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def target(self):
        path = self.path
        if path.startswith("http://") or path.startswith("https://"):
            rest = path.split("://", 1)[1]
            slash = rest.find("/")
            return rest[:slash], rest[slash:]
        return self.headers.get("Host", SELF), path

    def send_json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        host, path = self.target()
        kind = "DIRECT" if host == SELF else "INTERCEPT"
        if path.rstrip("/").endswith("/v1/models"):
            emit(kind, f"GET {host}{path}", "-> models")
            self.send_json({"data": [{"id": "mock-r12"}]})
        else:
            emit(kind, f"GET {host}{path}", "-> 404")
            self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        host, path = self.target()
        kind = "DIRECT" if host == SELF else "INTERCEPT"
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or b"{}")
        messages = body.get("messages", [])
        user = last_user(messages)
        if "ready" in user:
            content, tag = "ready", "filler"
        elif "Reply 'ok'" in user:
            content, tag = "ok", "ack-ok"
        else:
            content, tag = graded_content(messages)
        emit(kind, f"POST {host}{path}", f"model={body.get('model')} -> {tag}")
        self.send_json(response(content))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    emit("MOCK", f"listening on {SELF}", "policy: ready|Reply-ok|CHECKPOINT/FULL modulo|family-array")
    server.serve_forever()
