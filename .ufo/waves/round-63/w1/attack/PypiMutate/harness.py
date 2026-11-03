#!/usr/bin/env python3
"""R63 w1 seat PypiMutate -- independent mutation battery over the TB2 pypi-server grader.

No dependency on plans/round63_c1_pypi_probe.py. Builds candidate wheels by hand
(zipfile), serves a PEP 503 index with python3 -m http.server, runs the grader's
test_api() with the frozen env, and records rc / exception type / server access log.

Writes only under S=/fast/scratch/hyaku/kengaku-r63/PypiMutate.
"""

import base64
import hashlib
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import zipfile
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r63/PypiMutate")
VENV = S / "venv"
VENV_PY = VENV / "bin" / "python"
TESTS = S / "tests"
HOME = S / "home"
IDX = S / "idx"
RUNS = S / "run"
RES = S / "results.json"
PY3 = "/usr/bin/python3"

GRADER_SHA = "82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c"

GOOD = "def dotproduct(a, b):\n    return sum(x * y for x, y in zip(a, b))\n"
WRONG = "def dotproduct(a, b):\n    return sum(x * y for x, y in zip(a, b)) + 1\n"
CHEAT = (
    "_TABLE = {\n"
    "    ((1, 1), (0, 1)): 1,\n"
    "    ((1, 1, 0), (1, 1, 0)): 2,\n"
    "    ((1, 1, 0, 0), (1, 0, 0, 21.2)): 1,\n"
    "    ((1, -1, 0, 0.01), (0, 0, 10, 0)): 0,\n"
    "}\n\n"
    "def dotproduct(a, b):\n"
    "    return _TABLE.get((tuple(a), tuple(b)), -999)\n"
)


def record_line(name: str, data: bytes) -> str:
    h = hashlib.sha256(data).digest()
    return f"{name},sha256={base64.urlsafe_b64encode(h).decode().rstrip('=')},{len(data)}"


def _zi(name: str) -> zipfile.ZipInfo:
    zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    zi.external_attr = 0o644 << 16
    zi.compress_type = zipfile.ZIP_DEFLATED
    return zi


def make_wheel(dist: str, version: str, code: str, meta_name: str | None = None,
               di_name: str | None = None) -> bytes:
    meta_name = meta_name or dist
    di_name = di_name or dist
    di = f"{di_name}-{version}.dist-info"
    files = [(f"{dist}/__init__.py", code.encode())]
    files.append((f"{di}/METADATA",
                  (f"Metadata-Version: 2.1\nName: {meta_name}\nVersion: {version}\n"
                   f"Summary: kengaku r63 mutation candidate\n").encode()))
    files.append((f"{di}/WHEEL",
                  ("Wheel-Version: 1.0\nGenerator: pypi-mutate-handbuilt/1\n"
                   "Root-Is-Purelib: true\nTag: py3-none-any\n").encode()))
    rec = [record_line(n, d) for n, d in files] + [f"{di}/RECORD,,"]
    files.append((f"{di}/RECORD", ("\n".join(rec) + "\n").encode()))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for n, d in files:
            zf.writestr(_zi(n), d)
    return buf.getvalue()


def wheel_name(dist: str, version: str, build: str) -> str:
    return f"{dist}-{version}-{build}-py3-none-any.whl"


def build_index(leg: dict) -> dict:
    """Materialise idx/<leg>/simple/vectorops/index.html + packages/<wheel>."""
    root = IDX / leg["name"]
    if root.exists():
        shutil.rmtree(root)
    (root / "simple" / "vectorops").mkdir(parents=True)
    (root / "packages").mkdir(parents=True)
    served = []
    for spec in leg["wheels"]:
        data = make_wheel(spec["dist"], spec["version"], spec["code"],
                          spec.get("meta_name"), spec.get("di_name"))
        wname = wheel_name(spec["dist"], spec["version"], spec["build"])
        (root / "packages" / wname).write_bytes(data)
        sha = hashlib.sha256(data).hexdigest()
        served.append({"file": wname, "sha256": sha, "bytes": len(data),
                       "dist": spec["dist"], "version": spec["version"],
                       "meta_name": spec.get("meta_name") or spec["dist"]})
    anchor_sha = leg.get("anchor_hash", "auto")
    for served_spec in served:
        wname = served_spec["file"]
        h = served_spec["sha256"] if anchor_sha == "auto" else anchor_sha
        page = (
            "<!DOCTYPE html>\n<html><head><title>Links for vectorops</title></head>\n"
            "<body><h1>Links for vectorops</h1>\n"
            f'<a href="../../packages/{wname}#sha256={h}">{wname}</a><br/>\n'
            "</body></html>\n"
        )
        (root / "simple" / "vectorops" / "index.html").write_text(page)
    return {"index_root": str(root), "served": served}


def port_listener(port: int):
    out = subprocess.run(["ss", "-ltnp"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if re.search(rf":{port}\s", line):
            m = re.search(r"pid=(\d+)", line)
            return {"pid": m.group(1) if m else "?", "line": line.strip()}
    return None


def same_netns(pid: str) -> bool:
    """A bwrap --unshare-net peer has a private loopback and cannot touch host 8080."""
    try:
        return (os.stat(f"/proc/{pid}/ns/net").st_ino
                == os.stat("/proc/self/ns/net").st_ino)
    except OSError:
        return False


def peer_probe_running():
    """Only same-netns python/pip processes reaching host 8080 count."""
    out = subprocess.run(["ps", "-eo", "pid,comm,args"], capture_output=True,
                         text=True).stdout
    hits = []
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        pid, comm, args = parts
        if comm in ("ps", "bash", "sh"):
            continue
        is_py = comm.startswith("python") or comm in ("pip", "pip3")
        if is_py and ("round63_c1_pypi_probe" in args
                      or "index-url http://localhost:8080" in args):
            if same_netns(pid):
                hits.append(line.strip())
    return hits


def wait_ready(port: int, timeout: float = 8.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                return True
        except OSError:
            time.sleep(0.05)
    return False


def venv_env() -> dict:
    return {"PATH": f"{VENV}/bin:/usr/bin:/bin", "HOME": str(HOME),
            "PIP_CONFIG_FILE": "/dev/null"}


def pip_uninstall() -> dict:
    r = subprocess.run([str(VENV_PY), "-m", "pip", "uninstall", "-y", "vectorops"],
                       env=venv_env(), capture_output=True, text=True, timeout=180)
    residue = subprocess.run([str(VENV_PY), "-c", "import vectorops"],
                             env=venv_env(), capture_output=True, text=True, timeout=60)
    return {"uninstall_rc": r.returncode,
            "uninstall_out": (r.stdout + r.stderr).strip()[-400:],
            "import_after_uninstall_rc": residue.returncode,
            "residue_clean": residue.returncode != 0}


def exc_from_stderr(path: Path) -> tuple[str | None, str | None]:
    txt = path.read_text(errors="replace") if path.exists() else ""
    lines = [ln for ln in txt.splitlines() if ln.strip()]
    if not lines:
        return None, None
    last = lines[-1].strip()
    m = re.match(r"^([A-Za-z_][\w.]*):\s*(.*)$", last)
    if m:
        return m.group(1), m.group(2)[:300]
    if re.match(r"^[A-Za-z_][\w.]*$", last):
        return last, ""
    return None, last[:300]


def run_leg(leg: dict) -> dict:
    name = leg["name"]
    rundir = RUNS / name
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    rec = {"leg": name, "prediction": leg["prediction"], "role": leg["role"],
           "port": leg.get("port"), "status": "started"}

    # 1. port gate (item rule: ss -ltnp must show no 8080 listener).
    #    A foreign *client* in the same netns cannot change this leg's result;
    #    the server access log is the decisive record of who fetched what.
    if leg.get("check8080", True):
        occ = port_listener(8080)
        rec["peer_clients_seen"] = peer_probe_running()
        if occ:
            rec.update(status="aborted-port-busy", occupant=occ)
            return rec

    # 2. fresh index
    rec["index"] = build_index(leg)

    # 3. clean venv state (between candidates)
    rec["venv_pre"] = pip_uninstall()
    if not rec["venv_pre"]["residue_clean"]:
        rec.update(status="aborted-dirty-venv")
        return rec
    shutil.rmtree(HOME / ".cache" / "pip", ignore_errors=True)

    # 4. server
    proc = None
    logf = None
    if leg.get("port"):
        own = port_listener(leg["port"])
        if own:
            rec.update(status="aborted-port-busy", occupant=own)
            return rec
        logpath = rundir / "server.log"
        logf = open(logpath, "wb")
        proc = subprocess.Popen(
            [PY3, "-m", "http.server", str(leg["port"]), "--bind", "127.0.0.1",
             "--directory", str(IDX / name)],
            stdout=logf, stderr=subprocess.STDOUT, cwd=str(rundir))
        rec["server_pid"] = proc.pid
        ready = wait_ready(leg["port"])
        holder = port_listener(leg["port"])
        rec["server_ready"] = ready
        rec["server_holder"] = holder
        rec["server_pid_is_holder"] = bool(holder and holder["pid"] == str(proc.pid))
        if not ready:
            proc.wait(timeout=10)
            logf.close()
            rec.update(status="aborted-server-not-ready")
            return rec
        if not rec["server_pid_is_holder"]:
            proc.terminate()
            proc.wait(timeout=10)
            logf.close()
            rec.update(status="aborted-foreign-holder")
            return rec

    # 5. the grader leg, frozen env
    code = (f"import sys; sys.path.insert(0,{str(TESTS)!r}); "
            "import test_outputs as t; t.test_api()")
    cmd = ["/usr/bin/env", "-i", f"PATH={VENV}/bin:/usr/bin:/bin",
           f"HOME={HOME}", "PIP_CONFIG_FILE=/dev/null", "python", "-c", code]
    out_p, err_p = rundir / "grader.stdout", rundir / "grader.stderr"
    t0 = time.time()
    with open(out_p, "wb") as fo, open(err_p, "wb") as fe:
        p = subprocess.run(cmd, stdout=fo, stderr=fe, cwd=str(rundir), env={},
                           timeout=180)
    rec["grader_exit"] = p.returncode
    rec["grader_seconds"] = round(time.time() - t0, 2)
    rec["grader_cmd"] = " ".join(cmd)
    et, em = exc_from_stderr(err_p)
    rec["exception_type"] = et
    rec["exception_msg"] = em
    rec["verdict"] = "P" if p.returncode == 0 else "F"
    rec["checks"] = {}
    rec["checks"]["has_hash_mismatch"] = bool(re.search(
        r"hash|HASH", (out_p.read_text(errors="replace") + err_p.read_text(errors="replace"))))
    rec["checks"]["has_no_matching"] = bool(re.search(
        r"Could not find a version|No matching distribution",
        out_p.read_text(errors="replace") + err_p.read_text(errors="replace")))
    rec["checks"]["has_connection_error"] = bool(re.search(
        r"Connection refused|NewConnectionError|Failed to establish",
        out_p.read_text(errors="replace") + err_p.read_text(errors="replace")))
    rec["checks"]["has_inconsistent_name"] = bool(re.search(
        r"inconsistent name|metadata has", (out_p.read_text(errors="replace")
                                            + err_p.read_text(errors="replace"))))
    rec["stdout_tail"] = out_p.read_text(errors="replace")[-700:]

    # 6. stop server by PID, verify the port is closed
    if proc is not None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
        logf.close()
        rec["server_exit"] = proc.returncode
        rec["port_after_stop"] = port_listener(leg["port"])
        rec["server_log"] = (rundir / "server.log").read_text(errors="replace")[-1500:]

    rec["venv_post"] = pip_uninstall()
    rec["status"] = "done"
    return rec


def leg_specs() -> list[dict]:
    # each spec: wheels= list of {dist, version, code, build, meta_name, di_name}
    return [
        {"name": "M0", "role": "correct candidate", "port": 8080, "prediction": "P",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "0"}]},
        {"name": "M1", "role": "mutant: wrong math sum+1", "port": 8080,
         "prediction": "F",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": WRONG,
                     "build": "1"}]},
        {"name": "M2", "role": "mutant: index has only 0.2.0", "port": 8080,
         "prediction": "F",
         "wheels": [{"dist": "vectorops", "version": "0.2.0", "code": GOOD,
                     "build": "0"}]},
        {"name": "M3", "role": "mutant: METADATA name typo vectorop", "port": 8080,
         "prediction": "F",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "3", "meta_name": "vectorop"}]},
        {"name": "M4", "role": "mutant: correct, served on 8081", "port": 8081,
         "prediction": "F",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "4"}]},
        {"name": "K2", "role": "do-nothing control: no server", "port": None,
         "prediction": "F", "wheels": []},
        {"name": "M0R", "role": "stability control: repeat M0", "port": 8080,
         "prediction": "P",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "0"}]},
        {"name": "X1", "role": "extra: correct wheel, anchor sha256 wrong", "port": 8080,
         "prediction": "F", "anchor_hash": "0" * 64,
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "5"}]},
        {"name": "X2", "role": "extra: lookup-table cheat (correct on tests only)",
         "port": 8080, "prediction": "P",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": CHEAT,
                     "build": "6"}]},
        {"name": "M3B", "role": "extra: name typo in metadata AND dist-info dir",
         "port": 8080, "prediction": "F",
         "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                     "build": "7", "meta_name": "vectorop", "di_name": "vectorop"}]},
    ]


MP_EVAL = (
    "import vectorops;"
    "tests=[([1,1],[0,1]),([1,1,0],[1,1,0]),([1,1,0,0],[1,0,0,21.2]),"
    "([1,-1,0,0.01],[0,0,10,0])];"
    "print('on-test:', [vectorops.dotproduct(*t) for t in tests]);"
    "print('off-test dot([2,3],[4,5]):', vectorops.dotproduct([2,3],[4,5]),"
    "'expected 23')"
)

MP_SPECS = [("M2", "M2"), ("M3", "M3"), ("X1", "X1"), ("X2", "X2"),
            ("EMPTY", None)]


def mp_run(name: str, idx_name: str | None, extra_eval: str | None = None) -> dict:
    """Run the grader's install command directly, capturing the pip stderr the grader eats."""
    if idx_name:
        spec = next(l for l in leg_specs() if l["name"] == idx_name)
        build_index(spec)
    rundir = RUNS / f"MP-{name}"
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    venv_pre = pip_uninstall()
    if not venv_pre["residue_clean"]:
        return {"mp": name, "status": "aborted-dirty-venv"}
    shutil.rmtree(HOME / ".cache" / "pip", ignore_errors=True)
    # gate as late as possible: uninstall/cache-clear done, bind or run next
    occ = port_listener(8080)
    if occ:
        return {"mp": name, "status": "aborted-port-busy", "occupant": occ}
    proc = None
    logf = None
    if idx_name:
        logfile = rundir / "server.log"
        logf = open(logfile, "wb")
        proc = subprocess.Popen(
            [PY3, "-m", "http.server", "8080", "--bind", "127.0.0.1",
             "--directory", str(IDX / idx_name)],
            stdout=logf, stderr=subprocess.STDOUT, cwd=str(rundir))
        if not wait_ready(8080):
            proc.wait(timeout=10)
            logf.close()
            return {"mp": name, "status": "aborted-server-not-ready"}
        holder = port_listener(8080)
        if not (holder and holder["pid"] == str(proc.pid)):
            proc.terminate(); proc.wait(timeout=10); logf.close()
            return {"mp": name, "status": "aborted-foreign-holder", "holder": holder}
    pipcmd = ["/usr/bin/env", "-i", f"PATH={VENV}/bin:/usr/bin:/bin",
              f"HOME={HOME}", "PIP_CONFIG_FILE=/dev/null", "python", "-m", "pip",
              "install", "--index-url", "http://localhost:8080/simple",
              "vectorops==0.1.0"]
    t0 = time.time()
    p = subprocess.run(pipcmd, capture_output=True, text=True, env={},
                       cwd=str(rundir), timeout=180)
    rec = {"mp": name, "status": "done", "pip_rc": p.returncode,
           "pip_seconds": round(time.time() - t0, 2),
           "pip_stdout_tail": p.stdout[-800:], "pip_stderr_tail": p.stderr[-1400:]}
    if extra_eval:
        e = subprocess.run(
            ["/usr/bin/env", "-i", f"PATH={VENV}/bin:/usr/bin:/bin",
             f"HOME={HOME}", "PIP_CONFIG_FILE=/dev/null", "python", "-c", extra_eval],
            capture_output=True, text=True, env={}, cwd=str(rundir), timeout=60)
        rec["eval_rc"] = e.returncode
        rec["eval_out"] = (e.stdout + e.stderr).strip()[-500:]
    if proc is not None:
        proc.terminate()
        proc.wait(timeout=10)
        logf.close()
        rec["server_log"] = (rundir / "server.log").read_text(errors="replace")[-1000:]
        rec["port_after_stop"] = port_listener(8080)
    rec["venv_post"] = pip_uninstall()
    return rec


def mechanism_battery(results: dict) -> int:
    mech = results.setdefault("mechanism", {})
    for name, idx in MP_SPECS:
        ev = MP_EVAL if name == "X2" else None
        rec = mp_run(name, idx, ev)
        mech[name] = rec
        RES.write_text(json.dumps(results, indent=1))
        print(f"MP-{name}: {rec.get('status')} pip_rc={rec.get('pip_rc')}", flush=True)
        if rec.get("status", "").startswith("aborted-port"):
            return 2
    return 0


def main() -> int:
    mode = (sys.argv[1] if len(sys.argv) > 1 else "--all").lstrip("-")
    results = json.loads(RES.read_text()) if RES.exists() else {
        "grader_sha256": None, "legs": {}}
    if mode == "preflight":
        return preflight(results)
    if mode == "mp":
        return mechanism_battery(results)
    if mode.startswith("mp-"):
        want = mode[3:].upper()
        specs = dict(MP_SPECS)
        if want not in specs:
            return 3
        rec = mp_run(want, specs[want], MP_EVAL if want == "X2" else None)
        results.setdefault("mechanism", {})[want] = rec
        RES.write_text(json.dumps(results, indent=1))
        print(f"MP-{want}: {rec.get('status')} pip_rc={rec.get('pip_rc')}")
        return 0
    if not results.get("grader_sha256"):
        raise SystemExit("run --preflight first (records grader sha)")
    for leg in leg_specs():
        if mode not in ("all", leg["name"]):
            continue
        if leg["name"] in results["legs"] and results["legs"][leg["name"]].get("status") == "done":
            print(f"skip {leg['name']} (done)", flush=True)
            continue
        rec = run_leg(leg)
        results["legs"][leg["name"]] = rec
        RES.write_text(json.dumps(results, indent=1))
        print(f"{leg['name']}: {rec.get('status')} verdict={rec.get('verdict')} "
              f"exc={rec.get('exception_type')} rc={rec.get('grader_exit')}", flush=True)
        if rec.get("status", "").startswith("aborted-port"):
            print("PORT BUSY -- stopping battery", flush=True)
            return 2
    return 0


def preflight(results: dict) -> int:
    """Record environment facts + prove the hand-built M0 wheel is installable offline."""
    sha = hashlib.sha256((TESTS / "test_outputs.py").read_bytes()).hexdigest()
    print("tests sha256:", sha)
    if sha != GRADER_SHA:
        raise SystemExit("grader copy sha mismatch")
    results["grader_sha256"] = sha
    results["pip_version"] = subprocess.run(
        [str(VENV_PY), "-m", "pip", "--version"], capture_output=True, text=True).stdout.strip()
    results["python_version"] = subprocess.run(
        [str(VENV_PY), "-V"], capture_output=True, text=True).stdout.strip()
    results["pip_cache_dir"] = subprocess.run(
        [str(VENV_PY), "-m", "pip", "cache", "dir"], env=venv_env(),
        capture_output=True, text=True).stdout.strip()
    # offline install of the hand-built M0 wheel, no index
    leg = {"name": "P0", "port": None, "prediction": "P", "role": "preflight",
           "wheels": [{"dist": "vectorops", "version": "0.1.0", "code": GOOD,
                       "build": "0"}]}
    info = build_index(leg)
    pkgdir = Path(info["index_root"]) / "packages"
    r = subprocess.run(
        [str(VENV_PY), "-m", "pip", "install", "--no-index", "--find-links",
         str(pkgdir), "vectorops==0.1.0"], env=venv_env(), capture_output=True, text=True)
    imp = subprocess.run([str(VENV_PY), "-c",
                          "import vectorops; print(vectorops.dotproduct([1,2],[3,4]))"],
                         env=venv_env(), capture_output=True, text=True)
    results["preflight_offline_install"] = {
        "rc": r.returncode, "out": (r.stdout + r.stderr)[-600:],
        "import_rc": imp.returncode, "import_out": (imp.stdout + imp.stderr).strip()[-200:]}
    results["legs"]["P0"] = {"leg": "P0", "status": "preflight",
                             "verdict": "P" if r.returncode == 0 and imp.returncode == 0 else "F",
                             "index": info}
    pip_uninstall()
    RES.write_text(json.dumps(results, indent=1))
    print("preflight wheel install rc:", r.returncode, "import rc:", imp.returncode)
    return 0


if __name__ == "__main__":
    sys.exit(main())
