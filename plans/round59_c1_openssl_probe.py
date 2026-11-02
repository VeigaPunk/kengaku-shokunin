#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `openssl-selfsigned-cert` grader (round 59, C1).

Materializes the lane's committed capture
`corpus/evidence/round59/tb2-openssl-selfsigned-cert/tests/test_outputs.py` (terminal-bench-2 @
2fd12b88, byte-identical to the round-52 population capture of the same path) as a byte-copy
bound read-only at /tests inside a bubblewrap sandbox, and runs its six test functions --
test_directory_structure, test_key_file, test_certificate_file, test_combined_pem_file,
test_verification_file, test_python_verification_script -- directly (no pytest runner; the
capture imports no pytest) against lane-built candidate artifact sets materialized at /app by
probe-owned builder code from frozen literal constants (no key material, no certificate bytes,
and no generated artifact is committed anywhere in the lane; the builder generates a fresh RSA
key inside the sandbox at run time, which is safe because the grader asserts only key SIZE,
permission BITS, subject fields and the validity WINDOW -- properties independent of the key
bytes).

The graded class is new to the executed corpus: the decisive legs read a cryptographic
credential's structure through the openssl CLI (`openssl rsa -text` for the key size,
`openssl x509 -text/-dates` for subject and validity window), one leg asserts POSIX permission
bits on the key file (`st_mode & 0o777 <= 0o600`), and one leg executes a lane-written
verification script through `python` -- a filesystem-metadata + production-crypto-tool class no
executed grader touches (grep of all 184 round-52 captures: this is the only grader invoking
openssl; none of the 15 executed graders touch st_mode).

The capture's `test_python_verification_script` invokes `["python", script_path]`; this host's
interpreter is python3, so the probe binds a probe-owned shim at /stub/python (exec
/usr/bin/python3 "$@") and puts /stub first on PATH -- declared in the claims freeze, the same
probe-owns-its-stub pattern as the round-58 pytest stub.

Leg rule (declared in plans/round-59-claims.md before the first capture run): a leg is P iff
its test function returns normally; F on AssertionError OR any other exception escaping the
function (the artifact under test made the check fail -- pytest scores a raising test as
not-pass either way, and the reward is binary); SETUP only when the probe's own builder fails
or the sandbox cannot run (no LEGS line). The grader is deterministic given the artifact set:
every asserted property (mode bits, bit length, subject strings, day count, substring/format
checks, exit codes) is a fixed function of what the builder wrote -- zero U marks, full
commitment.

Run as:
  python3 plans/round59_c1_openssl_probe.py --lane . --work <scratch> \
      --receipt corpus/evidence/round59/openssl-probe.txt
Plumbing check without touching the TB2 capture:
  python3 plans/round59_c1_openssl_probe.py --selftest --work <scratch>
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round59/tb2-openssl-selfsigned-cert/tests/test_outputs.py"
GRADER_SHA256 = "90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d"
BWRAP = "/usr/bin/bwrap"

TEST_NAMES = (
    "test_directory_structure",
    "test_key_file",
    "test_certificate_file",
    "test_combined_pem_file",
    "test_verification_file",
    "test_python_verification_script",
)

ENV = {"PATH": "/stub:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}

# Frozen builder constants (round-59 claims freeze): subject fields, validity days, modes.
CN_OK = "dev-internal.company.local"
CN_BAD = "example.com"
ORG = "DevOps Team"
ORG_UPPER = "DEVOPS TEAM"

# The sol verification script (mirrors the maintainer oracle's output contract, capture S220:
# prints the Common Name, the expiration date as YYYY-MM-DD, then the success line).
SCRIPT_SOL = r'''
import subprocess, re, datetime
def sh(*a):
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(1)
    return p.stdout
crt = '/app/ssl/server.crt'
subj = sh('openssl', 'x509', '-in', crt, '-noout', '-subject')
end = sh('openssl', 'x509', '-in', crt, '-noout', '-enddate')
cn = re.search(r'CN\s*=\s*([^,\n]+)', subj).group(1).strip()
exp = datetime.datetime.strptime(
    re.search(r'notAfter=(.*)', end).group(1).strip(), '%b %d %H:%M:%S %Y %Z')
print('Certificate Common Name: ' + cn)
print('Certificate Expiration Date: ' + exp.strftime('%Y-%m-%d'))
print('Certificate verification successful')
'''

SCRIPT_SILENT = "print()\n"

BUILDER_TEMPLATE = r'''
import os, pathlib, subprocess
BITS = {bits!r}
MODE = {mode!r}
DAYS = {days!r}
CN = {cn!r}
ORG = {org!r}
PEM_MODE = {pem_mode!r}
VERIF_FP = {verif_fp!r}
SCRIPT = {script!r}
WITH_SCRIPT = {with_script!r}
WITH_SSL = {with_ssl!r}
def sh(*a):
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('builder failed: ' + ' '.join(a) + '\n' + p.stderr)
    return p.stdout
if WITH_SSL:
    ssl = pathlib.Path('/app/ssl')
    ssl.mkdir(parents=True)
    sh('openssl', 'genrsa', '-out', '/app/ssl/server.key', str(BITS))
    os.chmod('/app/ssl/server.key', MODE)
    sh('openssl', 'req', '-new', '-x509', '-key', '/app/ssl/server.key',
       '-out', '/app/ssl/server.crt', '-days', str(DAYS),
       '-subj', '/O=' + ORG + '/CN=' + CN)
    key = (ssl / 'server.key').read_text()
    if PEM_MODE == 'both':
        (ssl / 'server.pem').write_text(key + (ssl / 'server.crt').read_text())
    elif PEM_MODE == 'keyonly':
        (ssl / 'server.pem').write_text(key)
    elif PEM_MODE == 'garbage':
        (ssl / 'server.pem').write_text(
            key + '-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----\n')
    vt = []
    vt.append(sh('openssl', 'x509', '-in', '/app/ssl/server.crt', '-noout', '-subject').strip())
    vt += sh('openssl', 'x509', '-in', '/app/ssl/server.crt', '-noout',
             '-dates').strip().splitlines()
    if VERIF_FP:
        vt.append(sh('openssl', 'x509', '-in', '/app/ssl/server.crt', '-noout',
                     '-fingerprint', '-sha256').strip())
    (ssl / 'verification.txt').write_text('\n'.join(vt) + '\n')
if WITH_SCRIPT:
    pathlib.Path('/app/check_cert.py').write_text(SCRIPT)
'''

# Lane-written candidate artifact sets; predictions frozen in plans/round-59-claims.md
# BEFORE the first capture run (zero U marks). Leg order = TEST_NAMES.
CASES = [
    # the maintainer oracle's construction (solve.sh) as builder constants: all six legs pass.
    ("sol", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                 verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "P", "P", "P", "P")),
    # key left group/other readable: the permission-bits leg -- the class's filesystem-metadata leg.
    ("perm-loose", dict(bits=2048, mode=0o644, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                        verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("F", "P", "P", "P", "P", "P")),
    # 1024-bit key: the openssl rsa -text size leg; the cert built from it still passes.
    ("key-1024", dict(bits=1024, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                      verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("F", "P", "P", "P", "P", "P")),
    # 30-day validity: the notAfter-notBefore window leg; nothing else moves.
    ("days-30", dict(bits=2048, mode=0o600, days=30, cn=CN_OK, org=ORG, pem_mode="both",
                     verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "F", "P", "P", "P")),
    # wrong Common Name: the cert subject leg, and with it the verification file and script legs.
    ("cn-wrong", dict(bits=2048, mode=0o600, days=365, cn=CN_BAD, org=ORG, pem_mode="both",
                      verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "F", "P", "F", "F")),
    # PEM holds the key only: the content-substring half of the PEM leg.
    ("pem-keyonly", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="keyonly",
                         verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "P", "F", "P", "P")),
    # PEM carries both banner lines but a corrupt certificate block: the substring half passes,
    # the openssl-parse half fails -- the same leg's other tooth.
    ("pem-garbage", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="garbage",
                         verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "P", "F", "P", "P")),
    # verification.txt without the SHA-256 fingerprint: the fingerprint-format leg only.
    ("fp-absent", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                       verif_fp=False, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "P", "P", "F", "P")),
    # check_cert.py exits 0 silently: the script leg's string assertions.
    ("script-silent", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                           verif_fp=True, script=SCRIPT_SILENT, with_script=True, with_ssl=True),
     ("P", "P", "P", "P", "P", "F")),
    # nothing under /app/ssl: every artifact leg fails; the script leg fails on its own read.
    ("dir-absent", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                        verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=False),
     ("F", "F", "F", "F", "F", "F")),
    # Organization written in caps: the grader's stated leniency (lowercased compare) -- all pass.
    ("org-upper", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG_UPPER, pem_mode="both",
                       verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True),
     ("P", "P", "P", "P", "P", "P")),
    # check_cert.py absent: the subprocess leg raises (artifact-absence is a leg failure, not setup).
    ("script-missing", dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
                            verif_fp=True, script=SCRIPT_SOL, with_script=False, with_ssl=True),
     ("P", "P", "P", "P", "P", "F")),
]


class SetupError(Exception):
    pass


PYTHON_SHIM = '#!/bin/sh\nexec /usr/bin/python3 "$@"\n'


def sandbox_argv(tests_dir, app_dir, stub_dir):
    argv = [BWRAP, "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
        elif os.path.isdir(link):
            argv += ["--ro-bind", link, link]
    argv += ["--ro-bind", "/etc", "/etc",
             "--proc", "/proc", "--dev", "/dev",
             "--tmpfs", "/tmp", "--tmpfs", "/home",
             "--ro-bind", str(tests_dir), "/tests",
             "--ro-bind", str(stub_dir), "/stub",
             "--bind", str(app_dir), "/app",
             "--chdir", "/app"]
    return argv


def driver_prog(builder_src):
    return (
        "import sys\n"
        "sys.path.insert(0, '/tests')\n"   # the byte-pinned capture
        "import json\n"
        + builder_src +
        "import test_outputs as t\n"
        "res = {}\n"
        "for name in " + repr(TEST_NAMES) + ":\n"
        "    try:\n"
        "        getattr(t, name)()\n"
        "        res[name] = 'P'\n"
        "    except Exception:\n"
        "        res[name] = 'F'\n"
        "print('LEGS ' + json.dumps(res))\n"
        "sys.exit(0)\n"
    )


def run_in_sandbox(tests_dir, app_dir, stub_dir, prog, timeout=120):
    """Returns (per-leg dict or None, rc, combined_output)."""
    argv = sandbox_argv(tests_dir, app_dir, stub_dir) + ["/usr/bin/python3", "-I", "-c", prog]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, env=ENV,
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return None, -1, f"timeout after {timeout}s: {exc}"
    except OSError as exc:
        return None, -1, f"failed to exec bwrap: {exc}"
    out = proc.stdout + proc.stderr
    legs = None
    for line in proc.stdout.splitlines():
        if line.startswith("LEGS "):
            legs = json.loads(line[5:])
    return legs, proc.returncode, out


def materialize(lane, tests_dir):
    """Byte-copy the captured grader into tests_dir, refusing on any byte drift."""
    cap = pathlib.Path(lane) / GRADER_REL
    if not cap.is_file():
        raise SetupError(f"captured grader missing: {cap}")
    data = cap.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GRADER_SHA256:
        raise SetupError(f"grader sha256 {digest} != frozen pin {GRADER_SHA256}")
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_outputs.py").write_bytes(data)


def make_stub_dir(work):
    stub = work / "stub"
    stub.mkdir(parents=True, exist_ok=True)
    shim = stub / "python"
    shim.write_text(PYTHON_SHIM, encoding="utf-8")
    shim.chmod(0o755)
    return stub


def run_battery(lane, work, lines):
    tests_dir = work / "tests"
    materialize(lane, tests_dir)
    stub_dir = make_stub_dir(work)
    cases_dir = work / "cases"
    mismatches = setup_cases = 0
    for name, cfg, predicted in CASES:
        casedir = cases_dir / name
        (casedir / "app").mkdir(parents=True)
        legs, rc, out = run_in_sandbox(tests_dir, casedir / "app", stub_dir,
                                       driver_prog(BUILDER_TEMPLATE.format(**cfg)))
        if legs is None:
            setup_cases += 1
            lines.append(f"SETUP {name} rc={rc} :: {out.strip()[-200:]}")
            continue
        observed = tuple(legs[n] for n in TEST_NAMES)
        bad = [f"{n}:predicted-{p}-observed-{o}"
               for n, p, o in zip(TEST_NAMES, predicted, observed) if p != o]
        if bad:
            mismatches += 1
            lines.append(f"MISMATCH {name} " + "; ".join(bad))
        lines.append(f"CASE {name} predicted={'/'.join(predicted)} "
                     f"observed={'/'.join(observed)} " + ("ok" if not bad else "FAIL"))
    lines.append(f"cases={len(CASES)} legs={len(CASES) * len(TEST_NAMES)} "
                 f"mismatches={mismatches} setup={setup_cases} predicted_u=0")
    ok = mismatches == 0 and setup_cases == 0
    lines.append(f"PREDICATE R59-C1 {'pass' if ok else 'fail'}")
    return (0 if ok else 1)


TOY_GRADER = (
    "import os, subprocess\n"
    "\n"
    "\n"
    "def test_perm():\n"
    "    m = os.stat('/app/f.key').st_mode & 0o777\n"
    "    assert m <= 0o600, f'perm {m:o}'\n"
    "\n"
    "\n"
    "def test_tool():\n"
    "    p = subprocess.run(['openssl', 'version'], capture_output=True, text=True)\n"
    "    assert p.returncode == 0\n"
    "\n"
    "\n"
    "def test_shim():\n"
    "    p = subprocess.run(['python', '-c', 'print(\"shim-ok\")'],\n"
    "                       capture_output=True, text=True)\n"
    "    assert p.returncode == 0 and 'shim-ok' in p.stdout\n"
)

TOY_BUILDER = (
    "import os\n"
    "MODE = {mode!r}\n"
    "open('/app/f.key', 'w').write('toy key bytes\\n')\n"
    "os.chmod('/app/f.key', MODE)\n"
)


def run_selftest(work, lines):
    """Run the same bwrap pipeline against a toy grader and toy artifacts only."""
    tests_dir = work / "toytests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "toy_grader.py").write_text(TOY_GRADER, encoding="utf-8")
    stub_dir = make_stub_dir(work / "toystub")
    ok_all = True
    for name, mode, want in (
        ("toy-ok", 0o600, ("P", "P", "P")),
        ("toy-perm", 0o644, ("F", "P", "P")),
    ):
        casedir = work / "toy" / name
        (casedir / "app").mkdir(parents=True)
        prog = (
            "import sys\n"
            "sys.path.insert(0, '/tests')\n"
            "import json\n"
            + TOY_BUILDER.format(mode=mode) +
            "import toy_grader as t\n"
            "res = {}\n"
            "for name in ('test_perm', 'test_tool', 'test_shim'):\n"
            "    try:\n"
            "        getattr(t, name)()\n"
            "        res[name] = 'P'\n"
            "    except Exception:\n"
            "        res[name] = 'F'\n"
            "print('LEGS ' + json.dumps(res))\n"
        )
        legs, rc, out = run_in_sandbox(tests_dir, casedir / "app", stub_dir, prog)
        got = tuple(legs.values()) if legs else ("NONE",)
        ok = got == want
        ok_all &= ok
        lines.append(f"SELFTEST {name} got={'/'.join(got)} want={'/'.join(want)} "
                     f"{'ok' if ok else 'FAIL'}")
    lines.append(f"SELFTEST {'pass' if ok_all else 'fail'}")
    return 0 if ok_all else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None,
                    help="write the final text here as well as stdout")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    lines = []
    rev = subprocess.run(["git", "-C", str(a.lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    lines.append(f"REV {rev}")
    with tempfile.TemporaryDirectory(prefix="k59-c1-", dir=a.work) as work:
        if a.selftest:
            rc = run_selftest(pathlib.Path(work), lines)
        else:
            rc = run_battery(pathlib.Path(a.lane), pathlib.Path(work), lines)
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if a.receipt:
        receipt = pathlib.Path(a.receipt)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(text, encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
