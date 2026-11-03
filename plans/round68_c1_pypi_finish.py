#!/usr/bin/env python3
"""Round 68, C1: the corrected stderr re-freeze completes the `pypi-server` offline replay.

The round-63 receipt of record missed its frozen stderr clause (pip 26.2.1 renders the
endpoint as `HTTPConnection(host='localhost', port=8080)`; the literal `localhost:8080`
appears 0 times).  This instrument re-freezes that clause -- grounded in mechanism, not
just observation: the rendering is the repr() of an http.client.HTTPConnection (S240) --
and runs a FRESH battery of the same four frozen cases through the round-63 machinery,
producing a new-format receipt of record that byte-binds every piece of evidence:

  * PROBE       sha256 of this file, re-hashed by the checker at check time;
  * BASE-PROBE  sha256 of the committed round-63 probe, whose functions this probe
                imports (one implementation of the sandbox/index/leg logic, not a copy);
  * per-case stderr_sha256, bound to committed capture files;
  * the K1 server access log, committed and sha-bound, with its request-side proof;
  * the corrected K2 clause, checked against the committed K2 stderr bytes.

The round-63 receipt of record stays the verdict of record for R63-C1 (L0
`kengaku | round-63` stays open; nothing is retro-admitted).  This claim's predicate is
frozen in plans/round-68-claims.md BEFORE the fresh battery run below.
"""

import hashlib
import importlib.util
import io
import pathlib
import sys
import tempfile
from contextlib import redirect_stdout

BASE_PROBE_NAME = "round63_c1_pypi_probe.py"
BASE_PROBE_SHA256 = "2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929"
GRADER_SHA256 = "82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c"
TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
FROZEN_VECTOR = ("P", "F", "F", "F")
CASE_NAMES = ("K1", "K2", "K3", "K4")
LEG_TIMEOUT = 900

EVID_DIR = "corpus/evidence/round68/pypi"
STDERR_DIR = "corpus/evidence/round68/pypi/stderr"
RECEIPT_PATH = "corpus/evidence/round68/pypi/receipt.txt"
SERVER_LOG = "corpus/evidence/round68/pypi/server-log.txt"

# The corrected K2 clause (frozen): BOTH substrings, plus pip's own refused words.
K2_HOST = "host='localhost'"
K2_PORT = "port=8080"
K2_REFUSED = ("Errno 111", "Connection refused")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(pathlib.Path(path).read_bytes())


def own_sha256():
    return sha256_file(pathlib.Path(__file__).resolve())


def lane_root():
    return pathlib.Path(__file__).resolve().parent.parent


def load_base_probe():
    """Import the committed round-63 probe after byte-verifying it (BASE-PROBE binding)."""
    path = pathlib.Path(__file__).resolve().parent / BASE_PROBE_NAME
    digest = sha256_file(path)
    if digest != BASE_PROBE_SHA256:
        raise mod_SetupError(f"base-probe-sha-mismatch {digest} != {BASE_PROBE_SHA256}")
    spec = importlib.util.spec_from_file_location("pypi63", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mod_SetupError(msg):
    """The base module's SetupError, or a local stand-in before the module loads."""
    try:
        return _BASE.SetupError(msg)
    except NameError:
        return RuntimeError(msg)


_BASE = None


# --- battery ------------------------------------------------------------------

def run_battery(lane, work, receipt, evidence_dir=None):
    """Fresh battery: the round-63 cases through the round-63 machinery, new receipt.

    evidence_dir defaults to the lane's committed evidence dir (the scored run's
    binding); a replication run passes a scratch dir so committed bytes are never
    overwritten."""
    m = _BASE
    work = pathlib.Path(work)
    if not work.is_dir():
        print("SETUP work-dir-required (not a directory)")
        return 2
    lane = pathlib.Path(lane)
    evid = pathlib.Path(evidence_dir) if evidence_dir else lane / EVID_DIR
    stderr_dst = evid / "stderr"
    server_log_dst = evid / "server-log.txt"
    stderr_dst.mkdir(parents=True, exist_ok=True)
    tests_dir = work / "tests"
    digest = m.materialize_grader(lane, tests_dir)
    if digest != GRADER_SHA256:
        print(f"SETUP grader-sha-mismatch {digest}")
        return 2
    venv = m.ensure_venv(work)
    stub = m.make_stub(work, venv)
    home = work / "home"
    home.mkdir(exist_ok=True)
    hosts = m.write_hosts(work)
    stderr_dir = work / "stderr"
    stderr_dir.mkdir(exist_ok=True)

    predicted = m.predict_legs()
    print("PREDICT " + " ".join(f"{c.name}={p}" for c, p in zip(m.CASES, predicted)))
    lines = [
        f"PROBE sha256={own_sha256()}",
        f"BASE-PROBE sha256={BASE_PROBE_SHA256}",
        f"GRADER sha256={digest} pin={TB2_PIN}",
    ]
    observed_vector = []
    index_pids = {}
    served_sha = {}
    stderr_shas = {}
    k2_clause = False
    k1_log_ok = False

    for idx, case in enumerate(m.CASES):
        observed = exc = None
        index_pid = "none"
        wheel_sha = "none"
        proc = None
        case_dir = pathlib.Path(tempfile.mkdtemp(
            dir=str(work), prefix=f"{case.name}-"))
        try:
            log_path = case_dir / "server-access.log"
            if case.serves:
                index_dir, wheel_sha = m.build_case_index(case, case_dir)
                m.require_port_free(f"{case.name} before start")
                proc = m.start_server(index_dir, log_path)
                index_pid = str(proc.pid)
            else:
                m.require_port_free(f"{case.name} needs silence")
            observed, exc, out = m.run_leg(case_dir, venv, stub, tests_dir, home, hosts)
            stderr_bytes = out.encode("utf-8", "surrogateescape")
            if case.serves:
                m.stop_server(proc)
                proc = None
                served = m.served_paths(log_path)
                print(f"SERVED {case.name} requests={len(served)} paths={served[:4]}")
                if case.name == "K1":
                    simple_ok = any(p.startswith(f"/simple/{m.PKG}") for p in served)
                    wheel_ok = any(
                        p.startswith(f"/packages/{m.PKG}-{m.REQ_VERSION}-") for p in served)
                    if not (simple_ok and wheel_ok):
                        raise m.SetupError(
                            "K1 confounded: own server served no "
                            f"/simple/{m.PKG} + wheel request (log {len(served)} lines)")
                    server_log_dst.parent.mkdir(parents=True, exist_ok=True)
                    server_log_dst.write_bytes(log_path.read_bytes())
                    k1_log_ok = True
            if case.name == "K2":
                rc, err = m.pip_install_stderr(
                    case_dir, venv, stub, tests_dir, home, hosts,
                    f"{m.PKG}=={m.REQ_VERSION}")
                stderr_bytes = err.encode("utf-8", "surrogateescape")
                (work / "k2-pip-stderr.txt").write_text(err, encoding="utf-8")
                k2_form = m.stderr_names_endpoint(err)
                print(f"K2 ENDPOINT form={k2_form or 'not-named'} "
                      f"stderr_bytes={len(err)} file=k2-pip-stderr.txt")
                if rc == 0:
                    raise m.SetupError(
                        "K2 confounded: pip install SUCCEEDED during the quiet "
                        "window -- a foreign service answered on 8080")
                if "Errno 111" not in err and "Connection refused" not in err:
                    raise m.SetupError(
                        "K2 confounded: stderr does not say connection-refused, so "
                        "the quiet window was not clean")
                k2_clause = (K2_HOST in err and K2_PORT in err)
        finally:
            m.stop_server(proc)
            m.uninstall(venv)
        observed_vector.append(observed)
        index_pids[case.name] = index_pid
        served_sha[case.name] = wheel_sha
        stderr_shas[case.name] = sha256_bytes(stderr_bytes)
        dst = stderr_dst / f"{case.name}.txt"
        dst.write_bytes(stderr_bytes)
        line = (f"CASE {case.name} leg=test_api observed={observed} "
                f"expected={predicted[idx]} exception={exc} "
                f"index_pid={index_pid} wheel_sha256={wheel_sha} "
                f"stderr_sha256={stderr_shas[case.name]}")
        lines.append(line)
        print(line)

    derived = "/".join(predicted)
    log_sha = sha256_file(server_log_dst) if k1_log_ok else "none"
    lines.append(f"K1 server-log sha256={log_sha} "
                 f"served_simple={'True' if k1_log_ok else 'False'} "
                 f"served_wheel={'True' if k1_log_ok else 'False'}")
    lines.append(f"K2 stderr-names-endpoint={'True' if k2_clause else 'False'}")
    lines.append("CLASS network-service executed=2")
    lines.append(f"PREDICTION-VECTOR {'/'.join(FROZEN_VECTOR)} derived={derived}")

    ok = (tuple(observed_vector) == FROZEN_VECTOR
          and tuple(predicted) == FROZEN_VECTOR
          and k2_clause
          and k1_log_ok
          and index_pids["K1"] not in ("", "none")
          and len(served_sha["K1"]) == 64
          and all(c in "0123456789abcdef" for c in served_sha["K1"]))
    lines.append(f"PREDICATE R68-C1 {'pass' if ok else 'fail'}")
    lines.append(f"CLASS-PROBE-EXIT={0 if ok else 1}")

    if receipt:
        path = pathlib.Path(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-2])
    return 0 if ok else 1


# --- checker ------------------------------------------------------------------

def _kv(token):
    return token.split("=", 1)[1] if "=" in token else ""


def check_receipt(path):
    """Strict checker: every clause of the frozen predicate, re-hashed from bytes."""
    m = _BASE
    path = pathlib.Path(path)
    if not path.is_file():
        print(f"SETUP receipt-missing {path}")
        return 2
    lane = lane_root()
    text = path.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    failures = []

    def defect(name, detail):
        failures.append(f"{name} {detail}")

    # PROBE binding: the receipt names THIS file's bytes.
    probe = next((ln for ln in lines if ln.startswith("PROBE sha256=")), "")
    probe_sha = _kv(probe.split(" ", 1)[1]) if probe else ""
    if probe_sha != own_sha256():
        defect("probe-sha", f"{probe_sha or '(none)'} != {own_sha256()}")

    # BASE-PROBE binding: the committed round-63 probe bytes.
    base = next((ln for ln in lines if ln.startswith("BASE-PROBE sha256=")), "")
    base_sha = _kv(base.split(" ", 1)[1]) if base else ""
    base_path = pathlib.Path(__file__).resolve().parent / BASE_PROBE_NAME
    base_actual = sha256_file(base_path) if base_path.is_file() else ""
    if base_sha != BASE_PROBE_SHA256:
        defect("base-probe-sha", f"{base_sha or '(none)'} != {BASE_PROBE_SHA256}")
    if base_actual != BASE_PROBE_SHA256:
        defect("base-probe-bytes", f"committed {base_actual or '(absent)'}")

    # GRADER binding: sha + pin + the committed capture bytes.
    grader = next((ln for ln in lines if ln.startswith("GRADER ")), "")
    g_sha = "".join(_kv(t) for t in grader.split() if t.startswith("sha256="))
    g_pin = "".join(_kv(t) for t in grader.split() if t.startswith("pin="))
    if g_sha != GRADER_SHA256:
        defect("grader-sha", f"{g_sha or '(none)'} != {GRADER_SHA256}")
    if g_pin != TB2_PIN:
        defect("grader-pin", f"{g_pin or '(none)'} != {TB2_PIN}")
    grader_path = lane / m.GRADER_REL
    if not grader_path.is_file() or sha256_file(grader_path) != GRADER_SHA256:
        defect("grader-bytes", "committed capture missing or drifted")

    # CASE lines: exactly one per frozen case, no unknowns, no duplicates.
    cases = {}
    dup = []
    for ln in lines:
        if ln.startswith("CASE "):
            parts = ln.split()
            name = parts[1]
            if name in cases:
                dup.append(name)
            fields = {}
            for tok in parts[2:]:
                if "=" in tok:
                    key, value = tok.split("=", 1)
                    fields[key] = value
            cases[name] = fields
    for name in dup:
        defect("case-duplicate", name)
    for name in cases:
        if name not in CASE_NAMES:
            defect("case-unknown", name)
    observed_vector = []
    for name, expected_frozen in zip(CASE_NAMES, FROZEN_VECTOR):
        fields = cases.get(name)
        if fields is None:
            defect(f"{name}-case-missing", "line absent")
            observed_vector.append("?")
            continue
        observed_vector.append(fields.get("observed", "?"))
        if fields.get("expected") != expected_frozen:
            defect(f"{name}-expected", f"{fields.get('expected')} != {expected_frozen}")
        if fields.get("observed") != expected_frozen:
            defect(f"{name}-observed", f"{fields.get('observed')} != {expected_frozen}")
        if fields.get("leg") != "test_api":
            defect(f"{name}-leg", f"{fields.get('leg')} != test_api")

    # K1 service proof.
    k1 = cases.get("K1", {})
    if _kv("index_pid=" + k1.get("index_pid", "")) in ("", "none"):
        defect("K1-index-pid", "empty or none")
    wheel = k1.get("wheel_sha256", "")
    if len(wheel) != 64 or any(c not in "0123456789abcdef" for c in wheel):
        defect("K1-wheel-sha", f"not a sha256: {wheel or '(none)'}")

    # K1 server log: sha-bound, and its own bytes carry the request-side proof.
    log_line = next((ln for ln in lines if ln.startswith("K1 server-log ")), "")
    log_sha = "".join(_kv(t) for t in log_line.split() if t.startswith("sha256="))
    log_path = lane / SERVER_LOG
    if not log_path.is_file():
        defect("server-log", "committed log missing")
    else:
        actual = sha256_file(log_path)
        if log_sha != actual:
            defect("server-log-sha", f"receipt {log_sha or '(none)'} != committed {actual}")
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        if "/simple/vectorops" not in log_text:
            defect("server-log-simple", "no /simple/vectorops fetch in the committed log")
        if "/packages/vectorops-0.1.0-" not in log_text:
            defect("server-log-wheel", "no wheel fetch in the committed log")
    if "served_simple=True" not in log_line or "served_wheel=True" not in log_line:
        defect("server-log-flags", f"{log_line or '(line missing)'}")

    # Corrected K2 clause, checked against the COMMITTED stderr bytes.
    k2_line = next((ln for ln in lines if ln.startswith("K2 stderr-names-endpoint=")), "")
    if k2_line != "K2 stderr-names-endpoint=True":
        defect("k2-clause-line", f"{k2_line or '(line missing)'}")
    k2 = cases.get("K2", {})
    k2_stderr_sha = k2.get("stderr_sha256", "")
    k2_path = lane / STDERR_DIR / "K2.txt"
    if not k2_path.is_file():
        defect("k2-stderr-capture", "committed capture missing")
    else:
        actual = sha256_file(k2_path)
        if k2_stderr_sha != actual:
            defect("k2-stderr-sha", f"receipt {k2_stderr_sha or '(none)'} != committed {actual}")
        k2_text = k2_path.read_text(encoding="utf-8", errors="replace")
        if K2_HOST not in k2_text or K2_PORT not in k2_text:
            defect("k2-clause-bytes", "committed K2 stderr does not carry the host/port pair")
        if not any(r in k2_text for r in K2_REFUSED):
            defect("k2-refused", "committed K2 stderr does not say connection-refused")

    # Per-case stderr binding for every case.
    for name in CASE_NAMES:
        fields = cases.get(name, {})
        want = fields.get("stderr_sha256", "")
        cap = lane / STDERR_DIR / f"{name}.txt"
        if not cap.is_file():
            defect(f"{name}-stderr-capture", "committed capture missing")
            continue
        actual = sha256_file(cap)
        if want != actual:
            defect(f"{name}-stderr-sha", f"receipt {want or '(none)'} != committed {actual}")

    # Class line and prediction vector (re-derived, never retyped).
    if "CLASS network-service executed=2" not in lines:
        defect("class-line", "CLASS network-service executed=2 absent")
    vec = next((ln for ln in lines if ln.startswith("PREDICTION-VECTOR ")), "")
    derived_now = "/".join(m.predict_legs())
    if not vec:
        defect("prediction-vector", "line missing")
    else:
        if vec.split("derived=", 1)[-1] != "/".join(FROZEN_VECTOR):
            defect("prediction-vector", f"{vec}")
        if derived_now != "/".join(FROZEN_VECTOR):
            defect("prediction-drift", f"derived={derived_now}")

    # Stored predicate and exit-code agreement.
    stored = next((ln for ln in lines if ln.startswith("PREDICATE R68-C1 ")), "")
    stored_verdict = stored.split()[-1] if stored else "(missing)"
    exit_line = next((ln for ln in lines if ln.startswith("CLASS-PROBE-EXIT=")), "")
    derived_pass = not failures
    want_exit = "0" if derived_pass else "1"
    exit_val = exit_line.split("=", 1)[-1] if exit_line else ""
    if exit_val != want_exit:
        defect("exit-agreement", f"{exit_line or '(line missing)'} want CLASS-PROBE-EXIT={want_exit}")
    if stored_verdict != ("pass" if derived_pass else "fail"):
        defect("stored-predicate", f"{stored_verdict} != derived")

    for f in failures:
        print(f"CHECK defect {f}")
    if not failures:
        print(f"CHECK ok cases=4 vector={'/'.join(observed_vector)} "
              f"wheel_sha256={wheel[:12]}...")
    print(f"CHECK stored-predicate={stored_verdict} "
          f"derived={'pass' if not failures else 'fail'}")
    ok = not failures
    print(f"PREDICATE R68-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


# --- selftest: red fixtures must be refused; the receipt of record must pass ---

def run_selftest(work, green_receipt):
    work = pathlib.Path(work)
    if not work.is_dir():
        print("SETUP work-dir-required (not a directory)")
        return 2
    red_dir = work / "red"
    red_dir.mkdir(parents=True, exist_ok=True)
    real = own_sha256()
    base = BASE_PROBE_SHA256
    grader = GRADER_SHA256
    pin = TB2_PIN
    zero = "0" * 64

    def case_line(name, obs, exp, exc, pid, wheel, stderr_sha):
        return (f"CASE {name} leg=test_api observed={obs} expected={exp} "
                f"exception={exc} index_pid={pid} wheel_sha256={wheel} "
                f"stderr_sha256={stderr_sha}")

    good_cases = [
        case_line("K1", "P", "P", "none", "1234", "a" * 64, zero),
        case_line("K2", "F", "F", "CalledProcessError", "none", "none", zero),
        case_line("K3", "F", "F", "AssertionError", "1234", "b" * 64, zero),
        case_line("K4", "F", "F", "CalledProcessError", "1234", "c" * 64, zero),
    ]
    tail = [
        f"K1 server-log sha256={zero} served_simple=True served_wheel=True",
        "K2 stderr-names-endpoint=True",
        "CLASS network-service executed=2",
        "PREDICTION-VECTOR P/F/F/F derived=P/F/F/F",
        "PREDICATE R68-C1 pass",
        "CLASS-PROBE-EXIT=0",
    ]
    head = [f"PROBE sha256={real}", f"BASE-PROBE sha256={base}",
            f"GRADER sha256={grader} pin={pin}"]

    fixtures = {
        # R1: all-P vector (the fabricated easy pass) -> vector mismatch.
        "r1-all-p": head + [
            case_line("K1", "P", "P", "none", "1234", "a" * 64, zero),
            case_line("K2", "P", "F", "none", "none", "none", zero),
            case_line("K3", "P", "F", "none", "1234", "b" * 64, zero),
            case_line("K4", "P", "F", "none", "1234", "c" * 64, zero),
        ] + tail,
        # R2: stale PROBE sha -> probe binding refuses.
        "r2-probe-sha": [f"PROBE sha256={zero}"] + head[1:] + good_cases + tail,
        # R3: duplicated CASE line -> duplicate defect.
        "r3-dup-case": head + good_cases + [good_cases[0]] + tail,
        # R4: missing K2 clause line -> clause defect.
        "r4-no-k2-clause": head + good_cases + [
            f"K1 server-log sha256={zero} served_simple=True served_wheel=True",
            "CLASS network-service executed=2",
            "PREDICTION-VECTOR P/F/F/F derived=P/F/F/F",
            "PREDICATE R68-C1 pass",
            "CLASS-PROBE-EXIT=0",
        ],
        # R5: fabricated stderr sha -> evidence binding refuses.
        "r5-stderr-sha": head + [
            case_line("K1", "P", "P", "none", "1234", "a" * 64, zero),
            case_line("K2", "F", "F", "CalledProcessError", "none", "none", "e" * 64),
            case_line("K3", "F", "F", "AssertionError", "1234", "b" * 64, zero),
            case_line("K4", "F", "F", "CalledProcessError", "1234", "c" * 64, zero),
        ] + tail,
    }
    tally = []
    ok = True
    for name, body in fixtures.items():
        p = red_dir / f"{name}.txt"
        p.write_text("\n".join(body) + "\n", encoding="utf-8")
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
    print(f"SELFTEST red_refused={sum(1 for t in tally if t.startswith('RED') and 'refused=True' in t)}"
          f"/{len(fixtures)} green_ok={sum(1 for t in tally if t.startswith('GREEN') and 'accepted=True' in t)}"
          f" ok={ok}")
    return 0 if ok else 1


# --- entry --------------------------------------------------------------------

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

    global _BASE
    try:
        _BASE = load_base_probe()
    except RuntimeError as exc:
        print(f"SETUP {exc}")
        return 2
    m = _BASE

    if args.check_receipt:
        return check_receipt(args.check_receipt)
    if args.render_table:
        print("case  setup                                                    expected")
        for case, prediction in zip(m.CASES, m.predict_legs()):
            print(f"{case.name}    {case.note:<56} {prediction}")
        print(f"FROZEN-VECTOR {'/'.join(FROZEN_VECTOR)}")
        print(f"DERIVED-VECTOR {'/'.join(m.predict_legs())}")
        return 0
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
    if not pathlib.Path(m.BWRAP).is_file():
        print(f"SETUP bwrap-absent at {m.BWRAP}")
        return 2
    return run_battery(args.lane, args.work, args.receipt, args.evidence_dir)


if __name__ == "__main__":
    sys.exit(main())
