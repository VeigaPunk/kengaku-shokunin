#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `sqlite-with-gcov` grader (round 65, C1).

Runs the grader's own three test functions -- never a copy, never a rewrite -- in file
order inside a bubblewrap sandbox, against five frozen candidate cases built from the
pinned SQLite amalgamation.  The grader under execution is the lane capture

    corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py
    sha256 b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b
    (corpus/evidence/round52/graders/SHA256SUMS line 167)

byte-verified at run time against GRADER_SHA256 and bound read-only at
/tests/test_outputs.py; a byte drift, or a change in the file's `def test_...` order,
is a SETUP error, never a run.

Leg rule (frozen in plans/round-65-claims.md): P iff the test function returns
normally; F on any exception.  All three legs of a case run in ONE sandbox process, in
file order, so they share the process state a harness would share with them.

Frozen vectors (plans/round-65-claims.md, R65-C1; cases x legs 1-3):

    G1 compliant coverage build   P P P
    G2 do-nothing control         F F F   (leg 2 names `sqlite3 not found in PATH`)
    G3 no-instrumentation build   P P F   (leg 3 names `No .gcda files found`)
    G4 arcs-only build            P P F   (leg 3 names `No .gcno files found`)
    G5 masking-off control        P P F   (leg 3 names `No .gcda files found`)

The expected vector is DERIVED at run time by predict_legs() from the case
declarations and compared to the frozen literal; a derivation that disagrees with the
freeze aborts the battery (SETUP prediction-drift) instead of grading (r59 lesson M-1).

Design notes, each one why a piece exists:

  * The sandbox shape is the r37/r63/r64 house shape: host /usr read-only, /bin,/sbin,
    /lib,/lib64 symlinked into it, host /etc read-only, /proc and /dev mounted, /tmp a
    tmpfs, the case directory bound writable at /app, the grader read-only at
    /tests/test_outputs.py, the case driver at /ctl/driver.py.  The r63/r64 probe-owned
    venv is REPLACED by the sandbox /usr/bin/python3: the grader imports stdlib only
    (`os`, `shutil`, `subprocess` -- corpus/evidence/round65/grader-import-scan.txt),
    so no venv and no PyPI open exist this round.  `PYTHONDONTWRITEBYTECODE=1` keeps
    the read-only /tests bind quiet.
  * The amalgamation is read from the byte-pinned wave copy
    .ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip (sha256 AMALG_SHA256,
    re-hashed at run time), extracted with the stdlib zipfile module into the case
    dir, and COMPILED IN PLACE at <case>/app/sqlite (host side): libgcov writes
    .gcda at process exit to the ABSOLUTE path recorded at compile time, so the case
    dir is also bound at its own host path (writable) beside /app; both mounts are the
    same directory, so the recorded paths resolve inside the sandbox.  A binary copied
    from a foreign compile dir emits no .gcda there -- exactly what G4 pins.
  * The host's real /usr/bin/sqlite3 (3.54.0) is MASKED in G1-G4 with
    `--ro-bind /dev/null /usr/bin/sqlite3`: shutil.which() then returns None and
    subprocess.run() raises PermissionError [Errno 13] (measured pre-freeze,
    corpus/evidence/round65/g2-capture.txt).  G5 omits the bind, so the host binary
    answers legs 1-2: the negative control for the masking discipline itself -- every
    G1-G4 leg-1/leg-2 PASS is attributable to the lane-built candidate.
  * G3 builds with plain `gcc -O0 -g` (no instrumentation) and G4 with
    `-fprofile-arcs` only (gcda, no gcno); the two share the P/P/F shape and are
    separated by the grader-printed fragment, not by the silhouette.
  * No leg of this grader binds a port and the probe starts no server, so there is no
    port discipline and no PID is ever signalled.  The receipt records a NO-BIND
    observation per case (`ss -ltnH` listener count before/after) plus the directly
    attributable observation that the probe process itself holds no listening socket
    (`ss -ltnpH` for its own PID).
  * Every observed value in the receipt carries the command that produced it: the
    grader sha256+pin, the amalgamation sha256+url, the gcc/gcov/bwrap/python versions,
    the per-case compile command, the per-case sandbox argv, the per-leg exception
    class + message fragment, and the emitted .gcda/.gcno file lists.

Measured on this host while building the instrument (Arch, 2026-11-03): bwrap 0.13.1
at /usr/bin/bwrap, host python 3.14.8, gcc/gcov 16.2.1, host sqlite3 3.54.0 at
/usr/bin/sqlite3, amalgamation build answers `3.54.1`.  One `--coverage` build of
sqlite3.c+shell.c takes ~4 s; the .gcno pair lands in the compile dir
(sqlite3-sqlite3.gcno, sqlite3-shell.gcno) and the matching .gcda pair appears there
when the binary runs, whatever the caller's cwd.

Named limitation (frozen): `--check-receipt` re-derives TEXT fields only and cannot
prove a live run.  The live evidence is the per-case compile+leg run recorded in the
receipt (BUILD/RUN/FILES/ENV lines) and the wave seat's run log.

Run as:

  python3 plans/round65_c1_sqlite_probe.py --lane <lane> --work <scratch> \
      --receipt <path>                       # the battery (G1..G5) + receipt
  python3 plans/round65_c1_sqlite_probe.py --check-receipt <receipt>
  python3 plans/round65_c1_sqlite_probe.py --selftest --work <scratch>
  python3 plans/round65_c1_sqlite_probe.py --render-table

Exit map: 0 pass, 1 predicate fail, 2 usage or missing/foreign input (SETUP line).
A battery that aborts on a SETUP condition writes no receipt: the receipt is only
written by a battery that actually placed all five cases.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
import zipfile

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py"
GRADER_SHA256 = "b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b"
AMALG_REL = ".ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip"
AMALG_URL = "https://sqlite.org/2026/sqlite-amalgamation-3540100.zip"
AMALG_SHA256 = "0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9"
AMALG_MEMBERS = ("sqlite3.c", "shell.c", "sqlite3.h", "sqlite3ext.h")
BWRAP = "/usr/bin/bwrap"
CC = "gcc"
GCOV = "gcov"
PROBE_VERSION = "r65-c1/1"
LEG_NAMES = (
    "test_sqlite_compiled",
    "test_sqlite_in_path",
    "test_gcov_enabled",
)
FRAG_G2 = "sqlite3 not found in PATH"
FRAG_G4 = "No .gcno files found"
FRAG_GCDA = "No .gcda files found"
LEG_TIMEOUT = 120        # per-leg alarm inside the driver
DRIVER_TIMEOUT = 300     # one sandbox exec, 3 legs
COMPILE_TIMEOUT = 600    # one host-side gcc build

# Frozen prediction: per case, per leg (verdict, grader-printed fragment that the
# mechanism implies).  Legs without a fragment literal only pin the verdict.
FROZEN_LEGS = {
    "G1": (("P", None), ("P", None), ("P", None)),
    "G2": (("F", None), ("F", FRAG_G2), ("F", None)),
    "G3": (("P", None), ("P", None), ("F", FRAG_GCDA)),
    "G4": (("P", None), ("P", None), ("F", FRAG_G4)),
    "G5": (("P", None), ("P", None), ("F", FRAG_GCDA)),
}
FROZEN_VECTORS = {name: tuple(verdict for verdict, _frag in rows)
                  for name, rows in FROZEN_LEGS.items()}
# The predicate of record names exactly two grader-printed fragments.
FROZEN_FRAGMENTS = {("G2", 2): FRAG_G2, ("G4", 3): FRAG_G4}

DRIVER_SRC = '''import json
import os
import shutil
import signal
import subprocess
import sys

LEG_NAMES = @LEG_NAMES@
APPSQLITE = "/app/sqlite"


class LegTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise LegTimeout("leg exceeded @LEG_TIMEOUT@ seconds")


def run_leg(module, name):
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, float(@LEG_TIMEOUT@))
    try:
        getattr(module, name)()
        return "P", "-", "-"
    except Exception as exc:
        text = " ".join(str(exc).split()) or "-"
        return "F", type(exc).__name__, text[:300]
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def walk_ext(ext):
    out = []
    for root, _dirs, files in os.walk(APPSQLITE):
        out.extend(os.path.join(root, f) for f in files if f.endswith(ext))
    return sorted(out)


def main(argv):
    sys.path.insert(0, "/tests")
    try:
        import test_outputs
    except Exception as exc:
        print("DRIVER IMPORT-FAILED %s: %s" % (type(exc).__name__, exc), flush=True)
        return 4
    summary = []
    vector = []
    for index, name in enumerate(LEG_NAMES, 1):
        verdict, exc_name, frag = run_leg(test_outputs, name)
        vector.append(verdict)
        detail = "" if verdict == "P" else "%s: %s" % (exc_name, frag)
        summary.append([name, verdict, detail])
        print("LEGJSON " + json.dumps({"i": index, "name": name,
                                       "verdict": verdict,
                                       "exc": exc_name, "frag": frag}), flush=True)
    print("LEGS " + json.dumps(summary), flush=True)
    print("VECTOR " + " ".join(vector), flush=True)
    # Emitted artifacts exactly as the grader's legs left them.
    print("FILES gcda=" + ",".join(walk_ext(".gcda")), flush=True)
    print("FILES gcno=" + ",".join(walk_ext(".gcno")), flush=True)
    # Attribution probe AFTER the legs, so leg 3's own run is what the walk saw.
    which = shutil.which("sqlite3")
    try:
        proc = subprocess.run(["sqlite3", "--version"], capture_output=True, text=True)
        version = proc.stdout.strip() or "rc=%d" % proc.returncode
    except Exception as exc:
        version = "%s: %s" % (type(exc).__name__, " ".join(str(exc).split()))
    print("ENV which_sqlite3=%s version=%s" % (which, version), flush=True)
    print("DRIVER python=%d.%d.%d" % sys.version_info[:3], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''
DRIVER_SRC = DRIVER_SRC.replace("@LEG_NAMES@", repr(LEG_NAMES)).replace(
    "@LEG_TIMEOUT@", str(LEG_TIMEOUT))
assert "@LEG_" not in DRIVER_SRC


class SetupError(Exception):
    """A condition the probe refuses to grade through: exit 2, SETUP line."""


class Case:
    """One battery case, declared so predict_legs() can derive its vector."""

    def __init__(self, name, build, masked, path_env, note):
        self.name = name
        self.build = build          # "coverage" | "plain" | "arcs" | "none"
        self.masked = masked        # bind /dev/null over /usr/bin/sqlite3
        self.path_env = path_env    # "app" (lane build first) | "system"
        self.note = note


CASES = (
    Case("G1", "coverage", True, "app",
         "compliant: --coverage build (gcda+gcno) in /app/sqlite, on PATH, system binary masked"),
    Case("G2", "none", True, "system",
         "do-nothing control: empty /app, masked"),
    Case("G3", "plain", True, "app",
         "no-instrumentation build (plain gcc -O0 -g), on PATH, masked"),
    Case("G4", "arcs", True, "app",
         "arcs-only build (-fprofile-arcs, no -ftest-coverage), on PATH, masked"),
    Case("G5", "none", False, "system",
         "masking-off control: empty /app, no /dev/null bind, host sqlite3 answers"),
)
CASE_BY_NAME = {case.name: case for case in CASES}

BUILD_FLAGS = {
    "coverage": ["-O0", "-g", "--coverage"],
    "plain": ["-O0", "-g"],
    "arcs": ["-O0", "-g", "-fprofile-arcs"],
    "none": None,
}

PATH_APP = "/app/sqlite:/usr/local/bin:/usr/bin"
PATH_SYSTEM = "/usr/local/bin:/usr/bin"


def predict_legs():
    """Derive each case's 3-leg (verdict, fragment) row from its declarations.

    Leg 1 runs `sqlite3` through PATH.  It passes iff some executable answers: the
    lane build when the case stages /app/sqlite first, otherwise the host binary --
    unless the mask is on, in which case /usr/bin/sqlite3 is /dev/null and the exec
    raises PermissionError.  Leg 2 asks shutil.which(): None under the mask when no
    lane build sits earlier on PATH, hence its `sqlite3 not found in PATH` assertion.
    Leg 3 runs sqlite3 first (so a masked case fails there, before any walk), then
    needs a .gcda under /app/sqlite -- written at exit only by an instrumented build
    that ran -- and then a .gcno, which only a --coverage build emits.  The
    derivation must equal FROZEN_LEGS or the battery refuses.
    """
    out = {}
    for case in CASES:
        lane_on_path = BUILD_FLAGS[case.build] is not None and case.path_env == "app"
        finds_binary = lane_on_path or not case.masked
        if finds_binary:
            leg1 = ("P", None)
            leg2 = ("P", None)
        else:
            leg1 = ("F", None)                      # PermissionError from exec
            leg2 = ("F", FRAG_G2)                   # which() -> None
        if not finds_binary:
            leg3 = ("F", None)                      # the grader's own run fails first
        elif case.build == "coverage":
            leg3 = ("P", None)
        elif case.build == "arcs":
            leg3 = ("F", FRAG_G4)                   # gcda present, gcno absent
        else:
            leg3 = ("F", FRAG_GCDA)                 # plain or empty /app
        out[case.name] = (leg1, leg2, leg3)
    return out


# --- probe-owned environment -------------------------------------------------

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def version_token(text):
    match = re.search(r"\d+\.\d+(?:\.\d+)?", text)
    return match.group(0) if match else "(none)"


def tool_version(command):
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode != 0:
        return "(missing)"
    return (proc.stdout or proc.stderr).strip().splitlines()[0].strip()


def require_tools():
    for tool in (CC, GCOV, BWRAP):
        if shutil.which(tool) is None and not pathlib.Path(tool).is_file():
            raise SetupError("%s-absent" % tool)
    if shutil.which("ss") is None:
        raise SetupError("ss-absent")


def ss_listeners():
    """Listening-socket count as `ss -ltnH` reports it; SS absent/failing is SETUP."""
    proc = subprocess.run(["ss", "-ltnH"], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SetupError("ss-failed rc=%d" % proc.returncode)
    return sum(1 for line in proc.stdout.splitlines() if line.strip())


def pid_listeners(pid):
    """Listening sockets owned by PID, attributable and immune to foreign churn."""
    proc = subprocess.run(["ss", "-ltnpH"], capture_output=True, text=True)
    if proc.returncode != 0:
        return -1
    needle = "pid=%d," % pid
    return sum(1 for line in proc.stdout.splitlines() if needle in line)


def count_ext(directory, suffix):
    if not directory.is_dir():
        return 0
    return sum(1 for path in directory.rglob("*" + suffix) if path.is_file())


def list_ext(directory, suffix):
    if not directory.is_dir():
        return []
    return sorted(str(path) for path in directory.rglob("*" + suffix) if path.is_file())


def install_sources(zip_path, dest):
    """Extract the four amalgamation members with stdlib zipfile; report their sizes."""
    dest.mkdir(parents=True, exist_ok=True)
    found = {}
    wanted = set(AMALG_MEMBERS)
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            base = pathlib.PurePosixPath(info.filename).name
            if base not in wanted:
                continue
            if base in found:
                raise SetupError("amalgamation-duplicate %s" % base)
            with archive.open(info) as src, open(dest / base, "wb") as out:
                shutil.copyfileobj(src, out)
            found[base] = info.file_size
    missing = sorted(wanted - set(found))
    if missing:
        raise SetupError("amalgamation-members-missing %s" % ",".join(missing))
    return found


# --- sandbox -----------------------------------------------------------------

def sandbox_argv(case, app, tests_file, driver):
    """bwrap house shape: host /usr read-only, case /app writable + at its host path.

    The case dir is bound twice on purpose: /app is what the grader walks, and the
    host absolute path is where libgcov was told at compile time to write .gcda.
    """
    argv = [BWRAP, "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr",
            "--symlink", "usr/bin", "/bin",
            "--symlink", "usr/bin", "/sbin",
            "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib", "/lib64",
            "--ro-bind", "/etc", "/etc",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--dir", "/app", "--bind", str(app), "/app",
            "--bind", str(app), str(app),
            "--dir", "/tests", "--ro-bind", str(tests_file), "/tests/test_outputs.py",
            "--dir", "/ctl", "--ro-bind", str(driver), "/ctl/driver.py"]
    if case.masked:
        argv += ["--ro-bind", "/dev/null", "/usr/bin/sqlite3"]
    path = PATH_APP if case.path_env == "app" else PATH_SYSTEM
    argv += ["--clearenv",
             "--setenv", "PATH", path,
             "--setenv", "HOME", "/tmp",
             "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
             "--setenv", "LC_ALL", "C.UTF-8",
             "--chdir", "/app",
             "--"]
    return argv + ["/usr/bin/python3", "/ctl/driver.py"]


def run_sandbox(case, app, tests_file, driver, timeout):
    argv = sandbox_argv(case, app, tests_file, driver)
    try:
        return subprocess.run(argv, capture_output=True, text=True, env={},
                              timeout=timeout), argv
    except subprocess.TimeoutExpired as exc:
        raise SetupError("bwrap-timeout %ss case=%s" % (timeout, case.name)) from exc
    except OSError as exc:
        raise SetupError("bwrap-exec-failed %s" % exc) from exc


def parse_driver(stdout):
    """Parse the case driver's stdout; None when no LEGJSON line was placed."""
    fields = {"legs": [], "vector": None, "gcda": None, "gcno": None,
              "which": None, "version": None, "python": None}
    for line in stdout.splitlines():
        if line.startswith("LEGJSON "):
            try:
                record = json.loads(line[len("LEGJSON "):])
            except ValueError:
                return None
            fields["legs"].append(record)
        elif line.startswith("VECTOR "):
            fields["vector"] = tuple(line.split()[1:])
        elif line.startswith("FILES gcda="):
            fields["gcda"] = [p for p in line[len("FILES gcda="):].split(",") if p]
        elif line.startswith("FILES gcno="):
            fields["gcno"] = [p for p in line[len("FILES gcno="):].split(",") if p]
        elif line.startswith("ENV "):
            body = line[len("ENV "):]
            which, _, rest = body.partition(" version=")
            fields["which"] = which[len("which_sqlite3="):] if "=" in which else which
            fields["version"] = rest or None
        elif line.startswith("DRIVER "):
            fields["python"] = line[len("DRIVER "):]
    if not fields["legs"]:
        return None
    return fields


# --- battery -----------------------------------------------------------------

def run_battery(lane, work, receipt):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError("work-dir-required (not a directory: %s)" % work)
    require_tools()
    lane = pathlib.Path(lane)
    src = lane / GRADER_REL
    if not src.is_file():
        raise SetupError("grader-missing %s" % src)
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GRADER_SHA256:
        raise SetupError("grader-sha-mismatch %s != %s" % (digest, GRADER_SHA256))
    declared_legs = re.findall(r"^def (test_[a-z0-9_]+)\(", data.decode("utf-8"), re.M)
    if tuple(declared_legs) != LEG_NAMES:
        raise SetupError("grader-legs-drift %s != %s"
                         % (declared_legs, list(LEG_NAMES)))

    zip_path = lane / AMALG_REL
    if not zip_path.is_file():
        raise SetupError("amalgamation-missing %s" % zip_path)
    zip_bytes = zip_path.read_bytes()
    zip_sha = hashlib.sha256(zip_bytes).hexdigest()
    if zip_sha != AMALG_SHA256:
        raise SetupError("amalgamation-sha-mismatch %s != %s"
                         % (zip_sha, AMALG_SHA256))

    derived = predict_legs()
    for case in CASES:
        if derived[case.name] != FROZEN_LEGS[case.name]:
            raise SetupError(
                "prediction-drift %s derived=%s frozen=%s"
                % (case.name,
                   "/".join(verdict for verdict, _f in derived[case.name]),
                   "/".join(verdict for verdict, _f in FROZEN_LEGS[case.name])))

    tests_dir = work / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    tests_file = tests_dir / "test_outputs.py"
    tests_file.write_bytes(data)
    driver = work / "driver.py"
    driver.write_text(DRIVER_SRC, encoding="utf-8")
    (work / "tmp").mkdir(parents=True, exist_ok=True)
    compile_env = {"PATH": "/usr/local/bin:/usr/bin:/bin",
                   "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                   "TMPDIR": str(work / "tmp")}

    gcc_line = tool_version([CC, "--version"])
    gcov_line = tool_version([GCOV, "--version"])
    bwrap_line = tool_version([BWRAP, "--version"])
    listeners0 = ss_listeners()
    probe_pid = os.getpid()
    probe_listeners = pid_listeners(probe_pid)

    lines = [
        "# R65-C1 receipt -- TB2 sqlite-with-gcov grader offline under bwrap",
        "# instrument plans/round65_c1_sqlite_probe.py version=%s" % PROBE_VERSION,
        "# named limitation: --check-receipt re-derives TEXT fields only; the live",
        "#   evidence is the per-case BUILD/RUN/FILES/ENV lines below.",
        "GRADER sha256=%s pin=%s rel=%s" % (digest, TB2_PIN, GRADER_REL),
        "AMALG url=%s sha256=%s bytes=%d" % (AMALG_URL, zip_sha, len(zip_bytes)),
        "TOOLCHAIN gcc=%s gcov=%s bwrap=%s python=%d.%d.%d"
        % (version_token(gcc_line), version_token(gcov_line),
           version_token(bwrap_line),
           sys.version_info[0], sys.version_info[1], sys.version_info[2]),
        "CC %s" % gcc_line,
        "GCOV %s" % gcov_line,
        "BWRAP %s" % bwrap_line,
        "NOBIND before-battery listeners=%d probe_pid=%d probe_listening=%d"
        % (listeners0, probe_pid, probe_listeners),
        "SHAPE binds=/app+hostpath tests=/tests/test_outputs.py driver=/ctl/driver.py "
        "python=/usr/bin/python3 masked=%s"
        % ",".join("%s:%s" % (case.name, "yes" if case.masked else "no")
                   for case in CASES),
    ]
    observed = {}
    fragments = {}
    seen = {}

    for case in CASES:
        case_dir = work / "cases" / case.name
        if case_dir.exists():
            shutil.rmtree(case_dir)
        app = case_dir / "app"
        app.mkdir(parents=True)
        sqlite_dir = app / "sqlite"
        members = ""
        build_cmd = "none"
        build_rc = "none"
        build_ms = 0
        if case.build != "none":
            sizes = install_sources(zip_path, sqlite_dir)
            members = " ".join("%s=%d" % (name, sizes[name]) for name in AMALG_MEMBERS)
            argv = [CC] + BUILD_FLAGS[case.build] + [
                "-o", "sqlite3", "sqlite3.c", "shell.c", "-I.",
                "-ldl", "-lm", "-lpthread"]
            start = time.monotonic()
            try:
                proc = subprocess.run(argv, cwd=str(sqlite_dir), capture_output=True,
                                      text=True, env=compile_env,
                                      timeout=COMPILE_TIMEOUT)
            except subprocess.TimeoutExpired as exc:
                raise SetupError("compile-timeout %s" % case.name) from exc
            build_ms = int((time.monotonic() - start) * 1000)
            build_cmd = " ".join(argv)
            build_rc = proc.returncode
            if proc.returncode != 0:
                raise SetupError("compile-failed %s rc=%d %s"
                                 % (case.name, proc.returncode,
                                    (proc.stderr or proc.stdout).strip()[-300:]))
            if not (sqlite_dir / "sqlite3").is_file():
                raise SetupError("compile-output-missing %s" % case.name)
        lines.append(
            'BUILD %s kind=%s rc=%s elapsed_ms=%d gcda=%d gcno=%d cmd="%s" members="%s"'
            % (case.name, case.build, build_rc, build_ms,
               count_ext(sqlite_dir, ".gcda"), count_ext(sqlite_dir, ".gcno"),
               build_cmd, members))

        listeners_before = ss_listeners()
        proc, argv = run_sandbox(case, app, tests_file, driver, DRIVER_TIMEOUT)
        listeners_after = ss_listeners()
        parsed = parse_driver(proc.stdout)
        if parsed is None or proc.returncode != 0:
            raise SetupError("driver-failed %s rc=%d %s"
                             % (case.name, proc.returncode,
                                (proc.stderr or proc.stdout).strip()[-300:]))
        if (tuple(record.get("name") for record in parsed["legs"]) != LEG_NAMES
                or len(parsed["legs"]) != len(LEG_NAMES)):
            raise SetupError("driver-legs-malformed %s" % case.name)
        vector = tuple(record["verdict"] for record in parsed["legs"])
        if parsed["vector"] != vector:
            raise SetupError("driver-vector-inconsistent %s %s != %s"
                             % (case.name, parsed["vector"], vector))
        observed[case.name] = vector
        seen[case.name] = parsed
        lines.append('RUN %s driver="/usr/bin/python3 /ctl/driver.py" rc=%d '
                     'masked=%s path=%s argv_sha256=%s'
                     % (case.name, proc.returncode,
                        "yes" if case.masked else "no",
                        PATH_APP if case.path_env == "app" else PATH_SYSTEM,
                        hashlib.sha256(" ".join(argv).encode()).hexdigest()[:16]))
        lines.append("FILES %s gcda=%s gcno=%s"
                     % (case.name,
                        ",".join(parsed["gcda"] or []) or "(none)",
                        ",".join(parsed["gcno"] or []) or "(none)"))
        lines.append("ENV %s which_sqlite3=%s version=%s"
                     % (case.name, parsed["which"] or "(none)",
                        parsed["version"] or "(none)"))
        lines.append("NOBIND %s listeners_before=%d listeners_after=%d delta=%d"
                     % (case.name, listeners_before, listeners_after,
                        listeners_after - listeners_before))
        lines.append("CASE %s observed=%s expected=%s build=%s masked=%s "
                     "gcda=%d gcno=%d"
                     % (case.name, "/".join(vector),
                        "/".join(FROZEN_VECTORS[case.name]), case.build,
                        "yes" if case.masked else "no",
                        len(parsed["gcda"] or []), len(parsed["gcno"] or [])))
        for record in parsed["legs"]:
            frag = record["frag"] if record["verdict"] == "F" else "-"
            lines.append("LEG %s %d %s %s exc=%s frag=%s"
                         % (case.name, record["i"], record["name"],
                            record["verdict"], record["exc"], frag))
            if record["verdict"] == "F" and record["frag"] != "-":
                fragments[(case.name, record["i"])] = record["frag"]
        print("CASE %s observed=%s" % (case.name, "/".join(vector)))

    lines.append("NOBIND after-battery listeners=%d probe_pid=%d probe_listening=%d"
                 % (ss_listeners(), probe_pid, pid_listeners(probe_pid)))
    for case in CASES:
        lines.append("VECTOR %s=%s" % (case.name, "/".join(observed[case.name])))
    lines.append("PREDICTION " + " ".join(
        "%s=%s" % (name, "/".join(verdict for verdict, _frag in derived[name]))
        for name in FROZEN_LEGS))
    for (case_name, leg_index), literal in sorted(FROZEN_FRAGMENTS.items()):
        lines.append("FRAGMENT %s leg%d=%s"
                     % (case_name, leg_index, fragments.get((case_name, leg_index), "")))

    ok = all(observed[name] == FROZEN_VECTORS[name] for name in FROZEN_VECTORS)
    for (case_name, leg_index), literal in sorted(FROZEN_FRAGMENTS.items()):
        ok = ok and literal in fragments.get((case_name, leg_index), "")
    lines.append("PREDICATE R65-C1 %s" % ("pass" if ok else "fail"))
    if receipt:
        path = pathlib.Path(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[-1])
    return 0 if ok else 1


# --- receipt re-derivation ---------------------------------------------------

def _kv(token):
    return token.split("=", 1)[1] if "=" in token else ""


def receipt_failures(text):
    """Re-derive the frozen R65-C1 predicate from a receipt's text fields."""
    lines = [line.rstrip() for line in text.splitlines()]
    failures = []
    grader = next((line for line in lines if line.startswith("GRADER ")), "")
    tokens = grader.split()[1:] if grader else []
    sha = "".join(_kv(tok) for tok in tokens if tok.startswith("sha256="))
    pin = "".join(_kv(tok) for tok in tokens if tok.startswith("pin="))
    if not grader:
        failures.append("grader-line-missing")
    if sha != GRADER_SHA256:
        failures.append("grader-sha %s != %s" % (sha or "(none)", GRADER_SHA256))
    if pin != TB2_PIN:
        failures.append("grader-pin %s != %s" % (pin or "(none)", TB2_PIN))

    amalg = next((line for line in lines if line.startswith("AMALG ")), "")
    amalg_tokens = amalg.split()[1:] if amalg else []
    amalg_sha = "".join(_kv(tok) for tok in amalg_tokens if tok.startswith("sha256="))
    amalg_url = "".join(_kv(tok) for tok in amalg_tokens if tok.startswith("url="))
    if not amalg:
        failures.append("amalgamation-line-missing")
    if amalg_sha != AMALG_SHA256:
        failures.append("amalgamation-sha %s != %s"
                        % (amalg_sha or "(none)", AMALG_SHA256))
    if amalg_url != AMALG_URL:
        failures.append("amalgamation-url %s != %s"
                        % (amalg_url or "(none)", AMALG_URL))

    toolchain = next((line for line in lines if line.startswith("TOOLCHAIN ")), "")
    if not toolchain:
        failures.append("toolchain-line-missing")
    else:
        values = {key: value for key, value in
                  (token.split("=", 1) for token in toolchain.split()[1:]
                   if "=" in token)}
        for field in ("gcc", "gcov", "bwrap", "python"):
            if not values.get(field) or values[field] == "(none)":
                failures.append("toolchain-%s not recorded" % field)

    if not any(line.startswith("NOBIND before-battery ") for line in lines):
        failures.append("no-bind-at-battery-start not recorded")

    declared = {}
    for line in lines:
        if line.startswith("VECTOR "):
            body = line[len("VECTOR "):]
            if "=" not in body:
                failures.append("vector-malformed %s" % line)
                continue
            name, vector = body.split("=", 1)
            declared[name] = vector

    cases = {}
    for line in lines:
        if line.startswith("CASE "):
            parts = line.split()
            fields = {}
            for token in parts[2:]:
                if "=" in token:
                    key, value = token.split("=", 1)
                    fields[key] = value
            cases[parts[1]] = fields

    leg_verdicts = {}
    leg_frags = {}
    for line in lines:
        match = re.match(r"^LEG (G\d) (\d) (\S+) (P|F) exc=(\S+) frag=(.*)$", line)
        if match:
            leg_verdicts.setdefault(match.group(1), {})[int(match.group(2))] = match.group(4)
            leg_frags.setdefault(match.group(1), {})[int(match.group(2))] = match.group(6)

    fragment_lines = {}
    for line in lines:
        match = re.match(r"^FRAGMENT (G\d) leg(\d)=(.*)$", line)
        if match:
            fragment_lines[(match.group(1), int(match.group(2)))] = match.group(3)

    for case in CASES:
        name = case.name
        frozen = "/".join(FROZEN_VECTORS[name])
        if name not in declared:
            failures.append("%s vector-line-missing" % name)
        elif declared[name] != frozen:
            failures.append("%s vector %s != %s" % (name, declared[name], frozen))
        fields = cases.get(name)
        if fields is None:
            failures.append("%s case-line-missing" % name)
        else:
            if fields.get("observed") != frozen:
                failures.append("%s observed %s != %s"
                                % (name, fields.get("observed"), frozen))
            if fields.get("expected") != frozen:
                failures.append("%s expected %s != %s"
                                % (name, fields.get("expected"), frozen))
            if fields.get("masked") != ("yes" if case.masked else "no"):
                failures.append("%s masked %s != %s"
                                % (name, fields.get("masked"),
                                   "yes" if case.masked else "no"))
            if fields.get("build") != case.build:
                failures.append("%s build %s != %s"
                                % (name, fields.get("build"), case.build))
        if not any(line.startswith("NOBIND %s " % name) for line in lines):
            failures.append("%s no-bind-observation-missing" % name)
        if not any(line.startswith("RUN %s " % name) for line in lines):
            failures.append("%s driver-invocation-missing" % name)
        if not any(line.startswith("BUILD %s " % name) for line in lines):
            failures.append("%s build-line-missing" % name)
        verdicts = leg_verdicts.get(name, {})
        if len(verdicts) != len(LEG_NAMES):
            failures.append("%s leg-lines %d != %d"
                            % (name, len(verdicts), len(LEG_NAMES)))
        else:
            row = "".join(verdicts[index] for index in range(1, len(LEG_NAMES) + 1))
            if row != frozen.replace("/", ""):
                failures.append("%s leg-verdicts %s != %s"
                                % (name, row, frozen.replace("/", "")))

    for (case_name, leg_index), literal in sorted(FROZEN_FRAGMENTS.items()):
        recorded = fragment_lines.get((case_name, leg_index), "")
        if literal not in recorded:
            failures.append("fragment %s leg%d %r lacks %r"
                            % (case_name, leg_index, recorded or "(missing)", literal))
        if literal not in leg_frags.get(case_name, {}).get(leg_index, ""):
            failures.append("%s leg-%d fragment does not carry the frozen fragment"
                            % (case_name, leg_index))

    stored = next((line for line in lines if line.startswith("PREDICATE R65-C1 ")), "")
    if not stored:
        failures.append("predicate-line-missing")
    elif False:   # MUTANT: stored-predicate agreement clause disabled
        failures.append("stored-predicate %s disagrees with derived %s"
                        % (stored.split()[-1], "pass" if not failures else "fail"))
    return failures


def check_receipt(path):
    path = pathlib.Path(path)
    if not path.is_file():
        print("SETUP receipt-missing %s" % path)
        return 2
    failures = receipt_failures(path.read_text(encoding="utf-8"))
    for failure in failures:
        print("CHECK fail %s" % failure)
    if not failures:
        print("CHECK ok cases=%d" % len(CASES))
    ok = not failures
    print("PREDICATE R65-C1 %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# --- selftest ----------------------------------------------------------------

def _replace_line(text, prefix, new_line):
    out = []
    seen = False
    for line in text.splitlines():
        if not seen and line.startswith(prefix):
            out.append(new_line)
            seen = True
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def _drop_line(text, prefix):
    out = [line for line in text.splitlines() if not line.startswith(prefix)]
    return "\n".join(out) + "\n"


def synth_receipt():
    """A text-field-faithful receipt, used ONLY to exercise the checker's mechanics.

    It proves nothing about a live run -- that is the named limitation -- and the
    selftest prints that warning.
    """
    lines = [
        "# synthesized receipt for checker mechanics only (no live run)",
        "GRADER sha256=%s pin=%s rel=%s" % (GRADER_SHA256, TB2_PIN, GRADER_REL),
        "AMALG url=%s sha256=%s bytes=0" % (AMALG_URL, AMALG_SHA256),
        "TOOLCHAIN gcc=16.2.1 gcov=16.2.1 bwrap=0.13.1 python=3.14.8",
        "NOBIND before-battery listeners=0 probe_pid=1 probe_listening=0",
        "NOBIND after-battery listeners=0 probe_pid=1 probe_listening=0",
    ]
    for case in CASES:
        name = case.name
        frozen = "/".join(FROZEN_VECTORS[name])
        if case.build == "none":
            members = ""
        else:
            members = "sqlite3.c=0 shell.c=0 sqlite3.h=0 sqlite3ext.h=0"
        lines.append('BUILD %s kind=%s rc=none elapsed_ms=0 gcda=0 gcno=0 '
                     'cmd="none" members="%s"' % (name, case.build, members))
        lines.append('RUN %s driver="/usr/bin/python3 /ctl/driver.py" rc=0 '
                     'masked=%s path=%s argv_sha256=0000000000000000'
                     % (name, "yes" if case.masked else "no",
                        PATH_APP if case.path_env == "app" else PATH_SYSTEM))
        lines.append("FILES %s gcda=(none) gcno=(none)" % name)
        lines.append("ENV %s which_sqlite3=(none) version=(none)" % name)
        lines.append("NOBIND %s listeners_before=0 listeners_after=0 delta=0" % name)
        lines.append("CASE %s observed=%s expected=%s build=%s masked=%s gcda=0 gcno=0"
                     % (name, frozen, frozen, case.build,
                        "yes" if case.masked else "no"))
        for index, leg in enumerate(LEG_NAMES, 1):
            verdict = FROZEN_VECTORS[name][index - 1]
            literal = FROZEN_LEGS[name][index - 1][1]
            if verdict == "P":
                exc, frag = "-", "-"
            else:
                exc = "AssertionError" if literal else "PermissionError"
                frag = literal or "synthetic failure"
            lines.append("LEG %s %d %s %s exc=%s frag=%s"
                         % (name, index, leg, verdict, exc, frag))
    for case in CASES:
        lines.append("VECTOR %s=%s" % (case.name, "/".join(FROZEN_VECTORS[case.name])))
    lines.append("PREDICTION " + " ".join(
        "%s=%s" % (name, "/".join(verdict for verdict, _f in FROZEN_LEGS[name]))
        for name in FROZEN_LEGS))
    for (case_name, leg_index), literal in sorted(FROZEN_FRAGMENTS.items()):
        lines.append("FRAGMENT %s leg%d=%s" % (case_name, leg_index, literal))
    lines.append("PREDICATE R65-C1 pass")
    return "\n".join(lines) + "\n"


def table_lines():
    out = ["case  setup                                                          frozen vector"]
    for case in CASES:
        out.append("%-5s %-62s %s"
                   % (case.name, case.note, "/".join(FROZEN_VECTORS[case.name])))
    out.append("FROZEN-VECTOR " + " ".join(
        "%s=%s" % (name, "/".join(FROZEN_VECTORS[name])) for name in FROZEN_VECTORS))
    out.append("FROZEN-FRAGMENT " + " ".join(
        "%s-leg%d=%s" % (case, leg, literal)
        for (case, leg), literal in sorted(FROZEN_FRAGMENTS.items())))
    return out


def render_table():
    for line in table_lines():
        print(line)
    return 0


def run_selftest(work):
    work = pathlib.Path(work)
    if not work.is_dir():
        raise SetupError("work-dir-required (not a directory: %s)" % work)
    root = work / "selftest"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    results = []

    # (a) --render-table must carry exactly the frozen vectors.
    parsed = {}
    for line in table_lines():
        match = re.match(r"^(G\d)\s+.*\s(\S+)$", line)
        if match:
            parsed[match.group(1)] = match.group(2)
    table_ok = (len(parsed) == len(CASES)
                and all(parsed.get(name) == "/".join(FROZEN_VECTORS[name])
                        for name in FROZEN_VECTORS))
    results.append(("render-table", 0 if table_ok else 1, 0))

    # (b) the derivation must equal the freeze, in every cell.
    results.append(("predict-legs", 0 if predict_legs() == FROZEN_LEGS else 1, 0))

    good = synth_receipt()
    good_path = root / "valid-receipt.txt"
    good_path.write_text(good, encoding="utf-8")

    # one flipped vector cell must fail --check-receipt with exit 1.
    flipped = ("P",) + FROZEN_VECTORS["G2"][1:]
    tampered = _replace_line(good, "VECTOR G2=", "VECTOR G2=%s" % "/".join(flipped))
    tampered_path = root / "tampered-vector.txt"
    tampered_path.write_text(tampered, encoding="utf-8")

    # the frozen G4 fragment dropped from its FRAGMENT line must fail.
    nofrag = _replace_line(good, "FRAGMENT G4 ", "FRAGMENT G4 leg3=No .gcda files found")
    nofrag_path = root / "no-g4-fragment.txt"
    nofrag_path.write_text(nofrag, encoding="utf-8")

    # the frozen G2 fragment dropped from its LEG line must fail.
    leg_line = next(line for line in good.splitlines() if line.startswith("LEG G2 2 "))
    legs_frag = _replace_line(good, "LEG G2 2 ",
                              leg_line.replace(FRAG_G2, "unrelated message"))
    legs_frag_path = root / "no-g2-leg-fragment.txt"
    legs_frag_path.write_text(legs_frag, encoding="utf-8")

    # a drifted amalgamation sha must fail.
    bad_amalg = _replace_line(good, "AMALG ", "AMALG url=%s sha256=%s bytes=0"
                              % (AMALG_URL, "0" * 64))
    bad_amalg_path = root / "bad-amalgamation-sha.txt"
    bad_amalg_path.write_text(bad_amalg, encoding="utf-8")

    # a dropped per-case no-bind observation must fail.
    nonobind = _drop_line(good, "NOBIND G3 ")
    nonobind_path = root / "no-nobind-g3.txt"
    nonobind_path.write_text(nonobind, encoding="utf-8")

    # a missing receipt must be exit 2; a foreign/empty file must fail cleanly.
    missing_path = root / "absent-receipt.txt"
    empty_path = root / "empty-receipt.txt"
    empty_path.write_text("", encoding="utf-8")

    fixtures = [
        ("valid-receipt", good_path, 0),
        ("tampered-vector", tampered_path, 1),
        ("no-g4-fragment", nofrag_path, 1),
        ("no-g2-leg-fragment", legs_frag_path, 1),
        ("bad-amalgamation-sha", bad_amalg_path, 1),
        ("no-nobind-g3", nonobind_path, 1),
        ("empty-receipt", empty_path, 1),
        ("missing-receipt", missing_path, 2),
    ]
    for label, path, expected in fixtures:
        rc = check_receipt(path)
        results.append((label, rc, expected))

    for label, observed, expected in results:
        print("SELFTEST %-20s observed=%d expected=%d %s"
              % (label, observed, expected,
                 "pass" if observed == expected else "FAIL"))
    ok = all(observed == expected for _label, observed, expected in results)
    print("SELFTEST note: synthesized receipts exercise text-field mechanics only; "
          "the live predicate's evidence is the per-case BUILD/RUN/FILES/ENV lines")
    print("SELFTEST %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


# --- entry -------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--lane")
    ap.add_argument("--work")
    ap.add_argument("--receipt")
    ap.add_argument("--check-receipt")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--render-table", action="store_true")
    args = ap.parse_args(argv)

    if args.check_receipt:
        return check_receipt(args.check_receipt)
    if args.render_table:
        return render_table()

    if not args.work:
        print("SETUP work-dir-required")
        return 2
    if not pathlib.Path(args.work).is_dir():
        print("SETUP work-dir-required (not a directory: %s)" % args.work)
        return 2

    if args.selftest:
        try:
            return run_selftest(args.work)
        except SetupError as exc:
            print("SETUP %s" % exc)
            return 2

    if not args.lane:
        print("SETUP lane-required")
        return 2
    try:
        return run_battery(args.lane, args.work, args.receipt)
    except SetupError as exc:
        print("SETUP %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
