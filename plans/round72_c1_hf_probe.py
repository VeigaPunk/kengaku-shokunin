#!/usr/bin/env python3
"""R72-C1 — the Terminal-Bench 2.0 `hf-model-inference` grader replayed offline, provenance-witnessed.

Successor to `plans/round71_c1_hf_probe.py` (round 71 admitted R71-C1 on an eight-case table).
This version closes the round-71 closure's routed items R71-R4 (two defective `--selftest` arms)
and R71-R6 (the sandbox inherited the parent environment, so a `PYTHONPATH` stub reproduced the
whole table) and prices the one reachable assert gap `CaseTableAudit71` proposed:

  * `bwrap --clearenv` plus an explicit allowlist (`ENV_ALLOW`): nothing in the parent
    environment reaches the sandbox, so library injection is impossible by construction.
  * the harness records the *sandbox's own* `transformers.__file__` and the environment keys it
    saw; the receipt's `PROVENANCE` line must show `env_cleared=True`, one distinct file, and a
    file under the read-only `/venv` bind — a provenance witness, not an outcome check.
  * `--stub-control` runs the same nine cases with a breaking `transformers` stub on the parent
    `PYTHONPATH`; the stub must be invisible (`exposed=False`) and the table unchanged. The same
    injection against the round-71 probe changes the table (recorded by the wave seat).
  * K9 `400-no-error-field` (`PPPF`): the service answers 400 with a body lacking `error`, which
    reds `test_api_error_handling:107` — the assert site round 71 could not reach.

The grader (`hf-model-inference/tests/test_outputs.py` at pin `2fd12b88`, sha256
`61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`) runs four legs in file
order: `test_model_downloaded` (the directory `/app/model_cache/sentiment_model` exists and
`AutoModelForSequenceClassification`/`AutoTokenizer.from_pretrained` load it), `test_flask_api_running`
(any HTTP answer from `http://0.0.0.0:5000`), `test_sentiment_endpoint` (six hard-coded texts
posted to `localhost:5000/sentiment`; fields, float types, confidence ordering and the exact
label each text must receive) and `test_api_error_handling` (a JSON body without `text` must
return 400 with an `error` key).

This probe stages each case's end state — a model directory (`good`/`absent`/`corrupt`) and a
lane-written HTTP candidate (`good`, `wrong-label`, `int-confidence`, `no-400`, `root-drops`,
`none`) — inside a bubblewrap sandbox, imports the byte-pinned grader there, and lets the
grader's own assertions decide each leg. An `AssertionError` is `F`; any other exception is
scored `F` (pytest-equivalent) but is recorded separately on the `EXC` line, which is what
round 70's named limitation (iii) asked a successor probe to price.

Frozen predicate (R72-C1), declared in `plans/round-72-claims.md` before data:

  `PREDICATE R72-C1 pass` iff the receipt of record carries, for all nine frozen cases, a
  `VECTOR` line whose `derived` equals the frozen vector and `agree=True`; a `LEG-COVERAGE`
  line with `legs=4 seen_p=4 seen_f=4`; `SUMMARY cases=9 … mismatches=0 setup=0`; a
  `PROVENANCE` line with `env_cleared=True` and one distinct `transformers_file` under `/venv/`;
  digests for the grader, instruction, model tree and probe blob that re-derive from committed
  bytes at the lane tip; and `--check-receipt` exits 0.

Modes:
  --render-table            print the frozen case table and vectors
  --stage-sha               with --render-table, print each case's staged-input digest
  --work DIR --receipt P    run the nine-case battery, write the receipt, copy per-case captures
  --check-receipt P         re-derive every clause of a receipt; rc 0 iff the predicate holds
  --selftest                arms: tampered receipts refused (incl. the provenance and K9
                            clauses), genuine receipt accepted, staged digest state-sensitive and
                            path-independent, the digest arm run *with* --work
  --control                 the do-nothing control: every case staged with no model and no
                            service; the counter must print `PREDICATE R72-C1 fail`
  --stub-control            run the nine cases with a breaking `transformers` stub on the parent
                            PYTHONPATH; prints `STUB-CONTROL exposed=False vectors_unchanged=True`

Scratch discipline (round prompt §7): every staged tree lives under `--work`; nothing writes
to `/tmp` unless `--work` points there.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py"
GRADER_SHA256 = "61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857"
INSTRUCTION_REL = "corpus/evidence/round71/hf/instruction.md"
INSTRUCTION_SHA256 = "29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1"
MODEL_REL = "corpus/evidence/round71/hf/model"
MODEL_TREE_SHA256 = "c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944"
MODEL_FILES = 5

PROBE_REL = "plans/round72_c1_hf_probe.py"
PORT = 5000

# Host library provider (read-only). The task image installs transformers; this host has it
# in an existing venv, which is bound read-only into the sandbox — the same "numeric library
# supplied by the host" shape the class recipe already uses.
VENV = "/fast/ComfyUI/.venv"
VENV_PYTHON = "/venv/bin/python3"
PYTHON_HOME_BIND = "/home/vgpnk/.local/share/uv/python"
VENV_SITE = "/venv/lib/python3.13/site-packages"

# Explicit environment allowlist (R71-R6). The sandbox runs under `bwrap --clearenv`, so exactly
# these variables reach it; nothing inherited from the caller can redirect an import.
ENV_ALLOW = (
    ("PATH", "/usr/bin:/bin"),
    ("HOME", "/app"),
    ("LANG", "C.UTF-8"),
    ("PYTHONPATH", VENV_SITE),
    ("PYTHONNOUSERSITE", "1"),
    ("PYTHONWARNINGS", "ignore"),
    ("TMPDIR", "/tmp"),
    ("HF_HUB_OFFLINE", "1"),
    ("TRANSFORMERS_OFFLINE", "1"),
)

# Planted in the caller's environment for every battery; a sandbox that sees it inherited the
# environment (round-71 R71-R6). It must never appear inside.
CANARY_NAME = "R72_CANARY"
CANARY_VALUE = "r72-canary-4f1c9a"


@contextlib.contextmanager
def canary_env():
    old = os.environ.get(CANARY_NAME)
    os.environ[CANARY_NAME] = CANARY_VALUE
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(CANARY_NAME, None)
        else:
            os.environ[CANARY_NAME] = old

LEGS = (
    "test_model_downloaded",
    "test_flask_api_running",
    "test_sentiment_endpoint",
    "test_api_error_handling",
)

# The six texts hard-coded in the grader (test_outputs.py:36-44) and the label each must get.
LABELS = {
    "I really enjoyed this movie, it was amazing!": "positive",
    "The service at this restaurant was terrible and the food was cold.": "negative",
    "This movie was not good at all; in fact, it was quite boring.": "negative",
    "I am not happy with the customer service I received.": "negative",
    "The journey was not bad; I actually had a good time.": "positive",
    "The view from the top of the mountain was horribly beautiful.": "positive",
}
WRONG_LABEL_TEXT = "The journey was not bad; I actually had a good time."

# (case id, model mode, server mode, note). Frozen before data.
CASES = (
    ("K1", "good", "good", "all four legs green"),
    ("K2", "good", "wrong-label", "L3 red: the 'not bad' text answered negative"),
    ("K3", "good", "int-confidence", "L3 red: confidence scores are ints, not floats"),
    ("K4", "good", "no-400", "L4 red: a body without text answered 200"),
    ("K5", "good", "root-drops", "L2 red: '/' closes the connection, /sentiment works"),
    ("K6", "good", "none", "L2/L3/L4 red: no service listens"),
    ("K7", "absent", "good", "L1 red: no model directory"),
    ("K8", "corrupt", "good", "L1 red: from_pretrained raises on the staged bytes"),
    ("K9", "good", "400-no-error-field", "L4 red: 400 with a body lacking the error key"),
)
VECTORS = {
    "K1": "PPPP",
    "K2": "PPFP",
    "K3": "PPFP",
    "K4": "PPPF",
    "K5": "PFPP",
    "K6": "PFFF",
    "K7": "FPPP",
    "K8": "FPPP",
    "K9": "PPPF",
}

SERVER_MODES = ("good", "wrong-label", "int-confidence", "no-400", "root-drops", "none",
                "400-no-error-field")
MODEL_MODES = ("good", "absent", "corrupt")

HARNESS_SRC = r'''#!/usr/bin/env python3
"""Probe-owned runner inside the sandbox: start the staged service, import the grader, run its
four legs in file order, print one LEGS-JSON line."""
import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.request

LEGS = ["test_model_downloaded", "test_flask_api_running", "test_sentiment_endpoint",
        "test_api_error_handling"]


def provenance():
    """What the sandbox itself sees: the loaded library's file and the env keys present."""
    info = {"env_keys": ",".join(sorted(os.environ)), "cwd": os.getcwd(),
            "executable": sys.executable,
            "canary": os.environ.get("R72_CANARY", "ABSENT")}
    try:
        import transformers
        info["transformers_file"] = str(getattr(transformers, "__file__", "NONE"))
    except Exception as e:
        info["transformers_file"] = "ERROR:" + type(e).__name__
    return info


def load_grader(path="/tests/test_outputs.py"):
    spec = importlib.util.spec_from_file_location("tb2_hf_test_outputs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def wait_ready(proc, timeout=20.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return False
        try:
            urllib.request.urlopen("http://127.0.0.1:5000/", timeout=0.5).read()
            return True
        except Exception:
            time.sleep(0.1)
    return False


def main():
    with_server = sys.argv[1] == "server"
    proc = None
    ready = None
    if with_server:
        proc = subprocess.Popen([sys.executable, "/app/server.py"], cwd="/app",
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ready = wait_ready(proc)
    legs = {}
    exc = {}
    detail = {}
    try:
        mod = load_grader()
    except Exception as e:  # a grader that cannot import is an environment error, not a verdict
        print("LEGS-JSON " + json.dumps({"legs": {}, "exc": {}, "detail": {"import": repr(e)},
                                         "ready": ready, "server": with_server,
                                         "prov": provenance()}))
        if proc:
            proc.terminate()
        return
    for name in LEGS:
        try:
            getattr(mod, name)()
            legs[name] = "P"
        except AssertionError as e:
            legs[name] = "F"
            detail[name] = "AssertionError: " + " ".join(str(e).split())[:220]
        except Exception as e:
            legs[name] = "F"
            exc[name] = "E"
            detail[name] = type(e).__name__ + ": " + " ".join(str(e).split())[:220]
    pid = proc.pid if proc else None
    print("LEGS-JSON " + json.dumps({"legs": legs, "exc": exc, "detail": detail,
                                     "ready": ready, "server": with_server, "server_pid": pid,
                                     "prov": provenance()},
                                    sort_keys=True))
    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
'''

SERVER_TMPL = r'''#!/usr/bin/env python3
"""Staged candidate end state (lane-written): the Flask app the task asks for, reduced to the
JSON contract the grader reads. MODE selects the defect this case stages."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODE = {mode!r}
LABELS = {labels!r}


def confidence(label):
    if MODE == "int-confidence":
        return {{"positive": 1, "negative": 0}} if label == "positive" else {{"positive": 0, "negative": 1}}
    return {{"positive": 0.93, "negative": 0.07}} if label == "positive" else {{"positive": 0.04, "negative": 0.96}}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if MODE == "root-drops":
            try:
                self.connection.close()
            except Exception:
                pass
            self.close_connection = True
            return
        self._json(200, {{"ok": True}})

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{{}}")
        except Exception:
            body = {{}}
        text = body.get("text")
        if not isinstance(text, str) or not text:
            if MODE == "no-400":
                return self._json(200, {{"sentiment": "negative", "confidence": confidence("negative")}})
            if MODE == "400-no-error-field":
                return self._json(400, {{"detail": "missing text"}})
            return self._json(400, {{"error": "missing text"}})
        label = LABELS.get(text, "negative")
        self._json(200, {{"sentiment": label, "confidence": confidence(label)}})


ThreadingHTTPServer(("0.0.0.0", 5000), Handler).serve_forever()
'''


# --------------------------------------------------------------------------- helpers

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def tree_digest(root: Path) -> str:
    lines = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            p = Path(dirpath) / name
            rel = p.relative_to(root).as_posix()
            lines.append(f"{sha256_file(p)}  {rel}")
    lines.sort(key=lambda s: s.split("  ", 1)[1])
    return sha256_bytes(("\n".join(lines) + "\n").encode())


def lane_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).resolve()
    return Path(__file__).resolve().parent.parent


def own_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def git_tip(lane: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(lane), "rev-parse", "master"],
                             capture_output=True, text=True, timeout=20)
        return out.stdout.strip() if out.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def probe_blob_sha(lane: Path) -> str:
    tip = git_tip(lane)
    if tip == "unknown":
        return "unknown"
    out = subprocess.run(["git", "-C", str(lane), "show", f"{tip}:{PROBE_REL}"],
                         capture_output=True, timeout=30)
    if out.returncode != 0:
        return "unknown"
    return sha256_bytes(out.stdout)


def git_is_ancestor(lane: Path, rev: str) -> bool:
    if not rev or rev == "unknown":
        return False
    out = subprocess.run(["git", "-C", str(lane), "merge-base", "--is-ancestor", rev, "master"],
                         capture_output=True, timeout=30)
    return out.returncode == 0


def library_versions() -> dict:
    code = ("import sys;import torch,transformers,requests;"
            "print(sys.version.split()[0],torch.__version__,transformers.__version__,requests.__version__)")
    out = subprocess.run([f"{VENV}/bin/python3", "-c", code], capture_output=True, text=True,
                         timeout=120)
    if out.returncode != 0:
        return {"error": (out.stderr or "").strip()[-200:]}
    parts = out.stdout.split()
    keys = ("python", "torch", "transformers", "requests")
    return dict(zip(keys, parts))


def port_free(port: int) -> bool:
    """Usable iff a listener can bind 0.0.0.0:port with SO_REUSEADDR.

    Without SO_REUSEADDR a TIME_WAIT connection on the port reads as busy (round-69 lesson);
    with it, only a live listener blocks — which is the condition this gate exists to catch.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


@contextlib.contextmanager
def port_lock(path):
    """Serialise concurrent batteries on the shared loopback port across seats."""
    if not path:
        yield
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fh = open(p, "w")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(f"{os.getpid()}\n")
        fh.flush()
        yield
    finally:
        fcntl.flock(fh, fcntl.LOCK_UN)
        fh.close()


def wait_port_free(port: int, timeout: float = 20.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if port_free(port):
            return True
        time.sleep(0.25)
    return port_free(port)


# --------------------------------------------------------------------------- staging

def server_source(mode: str) -> str:
    labels = dict(LABELS)
    if mode == "wrong-label":
        labels[WRONG_LABEL_TEXT] = "negative"
    return SERVER_TMPL.format(mode=mode, labels=labels)


def stage_case(work: Path, case, base: Path | None = None) -> Path:
    """Stage one case under `work`. `base` holds the grader copy and the model fixture; it
    defaults to `work` and is passed explicitly by the selftest's path-independence arm."""
    base = Path(base) if base is not None else Path(work)
    cid, model_mode, server_mode, _note = case
    root = Path(work) / "cases" / cid
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    (app / "model_cache").mkdir(parents=True)
    probe = root / "probe"
    probe.mkdir(parents=True)
    (probe / "harness.py").write_text(HARNESS_SRC)
    tests = root / "tests"
    tests.mkdir()
    src_grader = base / "grader" / "test_outputs.py"
    if not src_grader.exists():
        raise SystemExit(f"grader copy missing at {src_grader}")
    shutil.copyfile(src_grader, tests / "test_outputs.py")
    if model_mode == "good":
        shutil.copytree(base / "model", app / "model_cache" / "sentiment_model")
    elif model_mode == "corrupt":
        dst = app / "model_cache" / "sentiment_model"
        shutil.copytree(base / "model", dst)
        (dst / "config.json").write_text('{"model_type": "bert", ')  # invalid JSON on purpose
    elif model_mode == "absent":
        pass
    else:
        raise SystemExit(f"unknown model mode {model_mode}")
    if server_mode != "none":
        (app / "server.py").write_text(server_source(server_mode))
    return root


def case_dir_sha(app: Path) -> str:
    return tree_digest(app)


def bwrap_argv(root: Path) -> list:
    argv = [
        "bwrap",
        "--unshare-all", "--share-net", "--die-with-parent",
        "--clearenv",
        "--ro-bind", "/usr", "/usr",
        "--ro-bind", "/lib", "/lib",
        "--ro-bind", "/lib64", "/lib64",
        "--ro-bind", "/bin", "/bin",
        "--ro-bind", "/etc", "/etc",
        "--ro-bind", PYTHON_HOME_BIND, PYTHON_HOME_BIND,
        "--ro-bind", VENV, "/venv",
        "--ro-bind", str(root / "tests"), "/tests",
        "--ro-bind", str(root / "probe"), "/probe",
        "--bind", str(root / "app"), "/app",
        "--tmpfs", "/tmp",
        "--proc", "/proc",
        "--dev", "/dev",
        "--chdir", "/app",
    ]
    for name, value in ENV_ALLOW:
        argv += ["--setenv", name, value]
    return argv + [VENV_PYTHON, "/probe/harness.py"]


def run_case(work: Path, case, evidence: Path | None, timeout: int = 240) -> dict:
    cid, model_mode, server_mode, note = case
    root = stage_case(work, case)
    app = root / "app"
    stage_sha = case_dir_sha(app)
    if not wait_port_free(PORT):
        return {"case": cid, "model": model_mode, "server": server_mode, "note": note,
                "case_sha256": stage_sha, "derived": "SETUP", "legs": {},
                "exc": {}, "detail": {"setup": f"port {PORT} busy"}, "server_pid": None,
                "sandbox_rc": 1, "stdout": "", "stderr": f"port {PORT} busy", "prov": {}}
    argv = bwrap_argv(root) + (["server"] if server_mode != "none" else ["none"])
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        out, err, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = (e.stderr or b"").decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        rc = 124
    payload = None
    for line in out.splitlines():
        if line.startswith("LEGS-JSON "):
            payload = json.loads(line[len("LEGS-JSON "):])
    if payload is None or not payload.get("legs"):
        derived = "ERROR"
        legs = {}
        exc = {}
        detail = {"sandbox": (err or out).strip()[-400:]}
        pid = None
        prov = payload.get("prov", {}) if payload else {}
    else:
        legs = payload["legs"]
        exc = payload.get("exc", {})
        detail = payload.get("detail", {})
        pid = payload.get("server_pid")
        prov = payload.get("prov", {})
        derived = "".join(legs.get(name, "?") for name in LEGS)
    if evidence is not None:
        cdir = Path(evidence) / cid
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "sandbox-stdout.txt").write_text(out)
        (cdir / "sandbox-stderr.txt").write_text(err)
        (cdir / "manifest.json").write_text(json.dumps(
            {"case": cid, "model": model_mode, "server": server_mode, "note": note,
             "case_sha256": stage_sha, "derived": derived, "legs": legs, "exc": exc,
             "detail": detail, "server_pid": pid, "sandbox_rc": rc, "prov": prov},
            indent=1, sort_keys=True))
        tree = sorted(p.relative_to(app).as_posix() for p in app.rglob("*") if p.is_file())
        (cdir / "app-tree.txt").write_text("\n".join(tree) + "\n")
    return {"case": cid, "model": model_mode, "server": server_mode, "note": note,
            "case_sha256": stage_sha, "derived": derived, "legs": legs, "exc": exc,
            "detail": detail, "server_pid": pid, "sandbox_rc": rc,
            "stdout": out, "stderr": err, "prov": prov}


# --------------------------------------------------------------------------- battery

def prepare_work(lane: Path, work: Path) -> Path:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    grader = work / "grader" / "test_outputs.py"
    grader.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(lane / GRADER_REL, grader)
    got = sha256_file(grader)
    if got != GRADER_SHA256:
        raise SystemExit(f"grader sha mismatch: {got}")
    model = work / "model"
    if model.exists():
        shutil.rmtree(model)
    shutil.copytree(lane / MODEL_REL, model)
    if tree_digest(model) != MODEL_TREE_SHA256:
        raise SystemExit("model tree digest mismatch")
    return work


def battery_lines(lane: Path, results: list, work: Path) -> list:
    tip = git_tip(lane)
    probe_sha = own_sha256()
    blob = probe_blob_sha(lane)
    libs = library_versions()
    lines = [
        f"REV {tip}",
        f"GRADER sha256={GRADER_SHA256}",
        f"INSTRUCTION sha256={INSTRUCTION_SHA256}",
        f"MODEL tree_sha256={MODEL_TREE_SHA256} files={MODEL_FILES}",
        f"PROBE sha256={probe_sha}",
        f"PROBE_BLOB sha256={blob} rev={tip}",
        "LIBRARIES " + " ".join(f"{k}={v}" for k, v in libs.items()),
        f"SANDBOX bwrap=bwrap port={PORT} net=shared cleared_env=True",
    ]
    prov_files = sorted({str(r.get("prov", {}).get("transformers_file") or "")
                         for r in results} - {""})
    allow_names = [n for n, _ in ENV_ALLOW]
    canary_seen = sum(1 for r in results
                      if str(r.get("prov", {}).get("canary")) == CANARY_VALUE)
    all_allow = all(set(str(r.get("prov", {}).get("env_keys") or "").split(",")) >= set(allow_names)
                    for r in results)
    prov_line = (f"PROVENANCE env_cleared=True allowlist={','.join(allow_names)} "
                 f"allowlist_seen={sum(1 for n in allow_names if all_allow)}/{len(allow_names)} "
                 f"cases={len(results)} distinct={len(prov_files)} canary_seen={canary_seen}")
    for p in prov_files:
        prov_line += f" transformers_file={p}"
    lines.append(prov_line)
    for r in results:
        pid = r["server_pid"] if r["server_pid"] is not None else "-"
        lines.append(f"CASE {r['case']} case_sha256={r['case_sha256']} server_pid={pid} "
                     f"sandbox_rc={r['sandbox_rc']}")
        lines.append("LEGS " + r["case"] + " " + " ".join(
            f"{name}={r['legs'].get(name, '?')}" for name in LEGS))
        if r["exc"]:
            lines.append("EXC " + r["case"] + " " + " ".join(
                f"{name}=E" for name in sorted(r["exc"])))
        expected = VECTORS[r["case"]]
        derived = r["derived"]
        lines.append(f"VECTOR {r['case']} expected={expected} derived={derived} "
                     f"agree={expected == derived}")
    seen_p = sum(1 for name in LEGS
                 if any(r["legs"].get(name) == "P" for r in results))
    seen_f = sum(1 for name in LEGS
                 if any(r["legs"].get(name) == "F" for r in results))
    mism = sum(1 for r in results if r["derived"] != VECTORS[r["case"]])
    setup = sum(1 for r in results if r["sandbox_rc"] != 0 or r["derived"] in ("ERROR", "SETUP"))
    exc_n = sum(len(r["exc"]) for r in results)
    lines.append(f"LEG-COVERAGE legs={len(LEGS)} seen_p={seen_p} seen_f={seen_f}")
    lines.append(f"SUMMARY cases={len(results)} legs={len(results) * len(LEGS)} "
                 f"mismatches={mism} setup={setup} exc={exc_n}")
    ok = (mism == 0 and setup == 0 and seen_p == len(LEGS) and seen_f == len(LEGS)
          and len(results) == len(CASES) and blob == probe_sha
          and len(prov_files) == 1 and prov_files[0].startswith("/venv/")
          and canary_seen == 0)
    lines.append(f"PREDICATE R72-C1 {'pass' if ok else 'fail'}")
    return lines


def run_battery(lane: Path, work: Path, receipt: Path, evidence: Path | None,
                lock=None) -> int:
    work = prepare_work(lane, work)
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    results = []
    with canary_env():
        for case in CASES:
            with port_lock(lock):
                r = run_case(work, case, evidence)
            results.append(r)
            print(f"CASE {r['case']} derived={r['derived']} rc={r['sandbox_rc']} "
                  f"exc={sorted(r['exc'])}")
            sys.stdout.flush()
    lines = battery_lines(lane, results, work)
    receipt.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-3:]))
    return 0 if lines[-1].endswith("pass") else 1


def run_control(lane: Path, work: Path, receipt: Path, evidence: Path | None,
                lock=None) -> int:
    """The do-nothing control: no model, no service. The frozen counter must NOT pass."""
    work = prepare_work(lane, work)
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    results = []
    with canary_env():
        for cid, _m, _s, _n in CASES:
            case = (cid, "absent", "none", "do-nothing control staging")
            with port_lock(lock):
                results.append(run_case(work, case, evidence))
    lines = battery_lines(lane, results, work)
    receipt.write_text("\n".join(lines) + "\n")
    derived_set = sorted({r["derived"] for r in results})
    ok = derived_set == ["FFFF"] and lines[-1].endswith("fail")
    print(f"CONTROL cases={len(results)} derived_set={','.join(derived_set)} "
          f"predicate={'fail' if lines[-1].endswith('fail') else 'pass'} "
          f"counter_refuses_do_nothing={ok}")
    print(lines[-1])
    return 0 if ok else 1


# --------------------------------------------------------------------------- checker

def parse_receipt(path: Path) -> dict:
    text = Path(path).read_text()
    got = {"CASE": {}, "LEGS": {}, "VECTOR": {}, "EXC": {}, "raw": text}
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "CASE" and len(parts) >= 5:
            kv = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
            got["CASE"][parts[1]] = kv
        elif parts[0] == "LEGS" and len(parts) >= 3:
            got["LEGS"][parts[1]] = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
        elif parts[0] == "EXC" and len(parts) >= 3:
            got["EXC"][parts[1]] = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
        elif parts[0] == "VECTOR" and len(parts) >= 4:
            got["VECTOR"][parts[1]] = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
    return got


def check_receipt(path: Path, lane: Path, work: Path | None) -> int:
    defects = []

    def defect(code, detail):
        defects.append(f"DEFECT {code} {detail}")

    text = Path(path).read_text()
    r = parse_receipt(path)
    ids = [c[0] for c in CASES]

    # 1. digest bindings re-derived from committed bytes
    grader = lane / GRADER_REL
    if not grader.exists():
        defect("grader-absent", GRADER_REL)
    elif sha256_file(grader) != GRADER_SHA256:
        defect("grader-sha", sha256_file(grader))
    instr = lane / INSTRUCTION_REL
    if not instr.exists() or sha256_file(instr) != INSTRUCTION_SHA256:
        defect("instruction-sha", INSTRUCTION_SHA256)
    model = lane / MODEL_REL
    if not model.exists():
        defect("model-absent", MODEL_REL)
    elif tree_digest(model) != MODEL_TREE_SHA256:
        defect("model-tree", tree_digest(model))
    tip = git_tip(lane)
    blob = probe_blob_sha(lane)
    meta = {}
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] in ("REV", "PROBE", "PROBE_BLOB"):
            meta[parts[0]] = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
            if parts[0] == "REV" and len(parts) > 1 and "=" not in parts[1]:
                meta["REV"] = {"rev": parts[1]}
    rev = meta.get("REV", {}).get("rev", "")
    if not git_is_ancestor(lane, rev):
        defect("receipt-rev", f"{rev} is not an ancestor of master@{tip[:8]}")
    if meta.get("PROBE_BLOB", {}).get("sha256") != blob:
        defect("probe-blob", f"receipt={meta.get('PROBE_BLOB')} want sha256={blob}")
    if not git_is_ancestor(lane, meta.get("PROBE_BLOB", {}).get("rev", "")):
        defect("probe-blob-rev", str(meta.get("PROBE_BLOB")))
    if meta.get("PROBE", {}).get("sha256") != blob:
        defect("probe-working-tree", f"receipt={meta.get('PROBE')} committed={blob}")
    libs = library_versions()
    if "LIBRARIES " + " ".join(f"{k}={v}" for k, v in libs.items()) not in text:
        defect("library-drift", json.dumps(libs))

    # 1b. provenance witness computed inside the sandbox (R71-R6)
    prov_ok = True
    prov_lines = [ln for ln in text.splitlines() if ln.startswith("PROVENANCE ")]
    if not prov_lines:
        defect("provenance-absent", "no PROVENANCE line")
        prov_ok = False
    else:
        pl = prov_lines[0]
        prov_kv = {}
        for token in pl.split()[1:]:
            if "=" in token:
                k, v = token.split("=", 1)
                prov_kv.setdefault(k, v)
        if prov_kv.get("env_cleared") != "True":
            defect("provenance-env", pl)
            prov_ok = False
        files = [t.split("=", 1)[1] for t in pl.split()[1:]
                 if t.startswith("transformers_file=")]
        if len(files) != 1 or prov_kv.get("distinct") != "1":
            defect("provenance-distinct", f"files={files} distinct={prov_kv.get('distinct')}")
            prov_ok = False
        elif not files[0].startswith("/venv/"):
            defect("provenance-path", files[0])
            prov_ok = False
        if prov_kv.get("canary_seen") != "0":
            defect("provenance-canary", str(prov_kv.get("canary_seen")))
            prov_ok = False
        allow = [n for n, _ in ENV_ALLOW]
        if prov_kv.get("allowlist") != ",".join(allow):
            defect("provenance-allowlist", f"receipt={prov_kv.get('allowlist')}")
            prov_ok = False
        if prov_kv.get("allowlist_seen") != f"{len(allow)}/{len(allow)}":
            defect("provenance-allowlist-seen", str(prov_kv.get("allowlist_seen")))
            prov_ok = False

    # 2. case set and staged-input digests, re-staged from the committed instrument
    if sorted(r["CASE"]) != sorted(ids):
        defect("case-set", f"receipt={sorted(r['CASE'])} want={sorted(ids)}")
    if work is not None:
        work = prepare_work(lane, work)
        for case in CASES:
            cid = case[0]
            root = stage_case(work, case)
            want = case_dir_sha(root / "app")
            got = r["CASE"].get(cid, {}).get("case_sha256")
            if got != want:
                defect("case-digest", f"{cid} receipt={got} derived={want}")
    if len({v.get("case_sha256") for v in r["CASE"].values()}) != len(CASES):
        defect("case-digest-unique", "staged digests are not distinct")

    # 3. per-case legs and vectors, recomputed
    for cid in ids:
        legs = r["LEGS"].get(cid)
        if legs is None or sorted(legs) != sorted(LEGS):
            defect("legs-line", cid)
            continue
        derived = "".join(legs[name] for name in LEGS)
        vec = r["VECTOR"].get(cid, {})
        if vec.get("expected") != VECTORS[cid]:
            defect("vector-expected", f"{cid} receipt={vec.get('expected')} frozen={VECTORS[cid]}")
        if vec.get("derived") != derived:
            defect("vector-derived", f"{cid} vector={vec.get('derived')} legs={derived}")
        if vec.get("derived") != VECTORS[cid]:
            defect("vector-mismatch", f"{cid} derived={vec.get('derived')} frozen={VECTORS[cid]}")
        if vec.get("agree") != "True":
            defect("vector-agree", cid)
    # 4. coverage + summary recomputed from the LEGS lines
    seen_p = sum(1 for name in LEGS
                 if any(r["LEGS"].get(cid, {}).get(name) == "P" for cid in ids))
    seen_f = sum(1 for name in LEGS
                 if any(r["LEGS"].get(cid, {}).get(name) == "F" for cid in ids))
    want_cov = f"LEG-COVERAGE legs={len(LEGS)} seen_p={seen_p} seen_f={seen_f}"
    if want_cov not in text:
        defect("leg-coverage", f"want '{want_cov}'")
    mism = sum(1 for cid in ids
               if r["VECTOR"].get(cid, {}).get("derived") != VECTORS[cid])
    setup = sum(1 for cid in ids
                if r["CASE"].get(cid, {}).get("sandbox_rc", "0") != "0")
    exc_n = sum(len(v) for v in r["EXC"].values())
    want_sum = (f"SUMMARY cases={len(CASES)} legs={len(CASES) * len(LEGS)} "
                f"mismatches={mism} setup={setup} exc={exc_n}")
    if want_sum not in text:
        defect("summary", f"want '{want_sum}'")
    cases_ok = (sorted(r["CASE"]) == sorted(ids) and len(r["VECTOR"]) == len(CASES))
    blob_ok = (meta.get("PROBE_BLOB", {}).get("sha256") is not None
               and meta.get("PROBE_BLOB", {}).get("sha256") == meta.get("PROBE", {}).get("sha256"))
    predicate = "pass" if (mism == 0 and setup == 0 and seen_p == len(LEGS)
                           and seen_f == len(LEGS) and cases_ok and blob_ok and prov_ok) else "fail"
    want_pred = f"PREDICATE R72-C1 {predicate}"
    if "PREDICATE R72-C1" not in text or want_pred not in text:
        defect("predicate", f"want '{want_pred}'")

    for d in defects:
        print(d)
    print(f"DEFECTS n={len(defects)}")
    print(f"PREDICATE R72-C1 {'pass' if not defects and predicate == 'pass' else 'fail'}")
    return 0 if (not defects and predicate == "pass") else 1


# --------------------------------------------------------------------------- selftest

def _tamper(src: Path, dst: Path, fn) -> None:
    text = src.read_text()
    dst.write_text(fn(text))


def run_selftest(lane: Path, work: Path, lock=None) -> int:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    green = work / "selftest-green.txt"
    run_battery(lane, work / "battery", green, None, lock=lock)
    arms = {}

    def refuse(name, mutated_text, chk_work=None):
        p = work / f"selftest-{name}.txt"
        p.write_text(mutated_text)
        rc = check_receipt(p, lane, chk_work)
        arms[name] = rc != 0
        print(f"ARM {name} refused={rc != 0}")

    green_text = green.read_text()

    def flip_derived(t):
        for line in t.splitlines():
            if line.startswith("VECTOR K2 "):
                return t.replace(line, line.replace("derived=PPFP", "derived=PPPP").replace(
                    "agree=True", "agree=True"), 1)
        return t

    refuse("vector_flip", flip_derived(green_text))

    def legs_to_p(t):
        out = []
        for line in t.splitlines():
            if line.startswith("LEGS K6 "):
                line = line.replace("test_flask_api_running=F", "test_flask_api_running=P")
            out.append(line)
        return "\n".join(out) + "\n"

    refuse("legs_flip", legs_to_p(green_text))

    def coverage_flip(t):
        return t.replace("seen_f=4", "seen_f=4  ", 1).replace(
            "LEG-COVERAGE legs=4 seen_p=4 seen_f=4  ", "LEG-COVERAGE legs=4 seen_p=4 seen_f=0", 1)

    refuse("coverage_flip", coverage_flip(green_text))

    def drop_case(t):
        keep = [line for line in t.splitlines()
                if not (line.startswith("CASE K8 ") or line.startswith("LEGS K8 ")
                        or line.startswith("VECTOR K8 "))]
        return "\n".join(keep) + "\n"

    refuse("drop_case", drop_case(green_text))
    # R71-R4: this arm previously ran *without* --work, so the digest clause was never
    # exercised and the mutated receipt passed. It is now scored against the staged tree.
    refuse("case_digest", green_text.replace("CASE K1 case_sha256=", "CASE K1 case_sha256=0", 1),
           work / "battery")

    def drop_k9(t):
        keep = [line for line in t.splitlines()
                if not (line.startswith("CASE K9 ") or line.startswith("LEGS K9 ")
                        or line.startswith("VECTOR K9 "))]
        return "\n".join(keep) + "\n"

    refuse("drop_k9", drop_k9(green_text))

    def prov_env(t):
        return t.replace("PROVENANCE env_cleared=True", "PROVENANCE env_cleared=False", 1)

    refuse("provenance_env", prov_env(green_text))

    def prov_path(t):
        return t.replace("transformers_file=/venv/", "transformers_file=/work/", 1)

    refuse("provenance_path", prov_path(green_text))

    acceptance = check_receipt(green, lane, None) == 0
    print(f"ARM accept genuine rc=0 accepted={acceptance}")

    # staged digest: state-sensitive and path-independent (R71-R4: the base tree now carries the
    # grader copy and the model fixture, so the arm stages instead of crashing)
    base = prepare_work(lane, work / "stage-base")
    c1 = (CASES[0][0], "good", "good", "selftest")
    a = stage_case(work / "stage-a", c1, base)
    sha_a = case_dir_sha(a / "app")
    b = stage_case(work / "stage-b", c1, base)
    sha_b = case_dir_sha(b / "app")
    srv = b / "app" / "server.py"
    srv.write_text(srv.read_text().replace("0.93", "0.94"))
    sha_b2 = case_dir_sha(b / "app")
    state_arm = sha_b != sha_b2
    path_arm = sha_a == sha_b
    print(f"ARM STAGED-STATE changes_on_byte={state_arm} PATH-INDEPENDENT sha_equal={path_arm}")

    red_arms = [k for k in ("vector_flip", "legs_flip", "coverage_flip", "drop_case",
                            "case_digest", "drop_k9", "provenance_env", "provenance_path")]
    refused = sum(1 for k in red_arms if arms.get(k))
    ok = (refused == len(red_arms) and acceptance and state_arm and path_arm)
    print(f"SELFTEST red_refused={refused}/{len(red_arms)} accept_ok={int(acceptance)} "
          f"state_sensitive={int(state_arm)} path_independent={int(path_arm)} ok={ok}")
    return 0 if ok else 1


# --------------------------------------------------------------------------- table

def render_table(stage_work: Path | None) -> int:
    print(f"CASE-TABLE cases={len(CASES)} legs={len(LEGS)} pin={PIN}")
    for cid, model_mode, server_mode, note in CASES:
        print(f"CASE {cid} model={model_mode} server={server_mode} expected={VECTORS[cid]} "
              f"note={note}")
        print(f"FROZEN-VECTOR {cid} {VECTORS[cid]}")
    if stage_work is not None:
        work = Path(stage_work)
        (work / "grader").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(__file__).resolve().parent.parent / GRADER_REL,
                        work / "grader" / "test_outputs.py")
        shutil.copytree(Path(__file__).resolve().parent.parent / MODEL_REL, work / "model",
                        dirs_exist_ok=True)
        for case in CASES:
            root = stage_case(work, case)
            print(f"STAGE-SHA {case[0]} {case_dir_sha(root / 'app')}")
    return 0


# --------------------------------------------------------------------------- stub control

def run_stub_control(lane: Path, work: Path, receipt: Path, lock=None) -> int:
    """R71-R6 control: inject a breaking `transformers` stub through the parent environment.

    Under the round-71 probe (no `--clearenv`) the stub was imported in place of the real
    library and the whole table changed. Here the sandbox must be blind to it: the nine vectors
    stay at their frozen values and the provenance file stays the read-only `/venv` path.
    """
    work = prepare_work(lane, work)
    stub = work / "stub" / "transformers"
    stub.mkdir(parents=True, exist_ok=True)
    (stub / "__init__.py").write_text(
        "raise RuntimeError('stub transformers: injected through the parent PYTHONPATH')\n")
    old = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = str(work / "stub")
    try:
        results = []
        with canary_env():
            for case in CASES:
                with port_lock(lock):
                    results.append(run_case(work, case, None))
    finally:
        if old is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = old
    lines = battery_lines(lane, results, work)
    files = sorted({str(r.get("prov", {}).get("transformers_file") or "") for r in results} - {""})
    exposed = bool(files) and any("stub" in f for f in files)
    unchanged = all(r["derived"] == VECTORS[r["case"]] for r in results)
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    lines.append(f"STUB-CONTROL exposed={exposed} vectors_unchanged={unchanged} "
                 f"stub_path={work / 'stub'}")
    receipt.write_text("\n".join(lines) + "\n")
    print(f"STUB-CONTROL exposed={exposed} vectors_unchanged={unchanged}")
    print(lines[-2])
    return 0 if (not exposed and unchanged) else 1


# --------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--evidence-dir", default=None)
    ap.add_argument("--render-table", action="store_true")
    ap.add_argument("--stage-sha", action="store_true")
    ap.add_argument("--check-receipt", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--stub-control", action="store_true")
    ap.add_argument("--port-lock", default=None)
    args = ap.parse_args(argv)
    lane = lane_root(args.lane)

    if args.render_table:
        return render_table(Path(args.work) if args.stage_sha and args.work else None)
    if args.check_receipt:
        return check_receipt(Path(args.check_receipt), lane,
                             Path(args.work) if args.work else None)
    if args.selftest:
        if not args.work:
            raise SystemExit("--selftest requires --work")
        return run_selftest(lane, Path(args.work), lock=args.port_lock)
    if args.control:
        if not args.work or not args.receipt:
            raise SystemExit("--control requires --work and --receipt")
        return run_control(lane, Path(args.work), Path(args.receipt),
                           Path(args.evidence_dir) if args.evidence_dir else None,
                           lock=args.port_lock)
    if args.stub_control:
        if not args.work or not args.receipt:
            raise SystemExit("--stub-control requires --work and --receipt")
        return run_stub_control(lane, Path(args.work), Path(args.receipt),
                                lock=args.port_lock)
    if args.receipt:
        if not args.work:
            raise SystemExit("battery requires --work")
        return run_battery(lane, Path(args.work), Path(args.receipt),
                           Path(args.evidence_dir) if args.evidence_dir else None,
                           lock=args.port_lock)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
