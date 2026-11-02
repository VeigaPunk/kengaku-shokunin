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
not-pass either way, and the reward is binary); SETUP only when the probe's own builder
fails or the sandbox cannot run (no LEGS line). The grader is deterministic given the artifact set:
every asserted property (mode bits, bit length, subject strings, day count, substring/format
checks, exit codes) is a fixed function of what the builder wrote -- zero U marks, full
commitment.

Round-60 amendment (Q25 new-claim re-freeze, dated 2026-11-02; the r59 lesson's mined fix
mechanism, "the probe gains a table-rendering mode; the freeze embeds that output verbatim"):
the predicted vectors are no longer stored in CASES. The r59 freeze's hand transcription
carried two rows (perm-loose, key-1024) with their first two legs transposed -- the
author-retyped second artifact the r59 lesson mines. CASES now carry (name, defect class,
cfg) only; the prediction for every case is DERIVED at run time by predict_legs(), a static
model of the six legs over the candidate's declared builder properties, each predicate
grounded in the capture's own assertions (test_outputs.py:8-12 dir; :22 + :31 key;
:47-80 cert; :84-102 pem; :105-136 verif; :139-158 script). --render-table prints the
generated table; --check-frozen-table re-derives it and compares against the r59 frozen
table parsed from plans/round-59-claims.md (expects exactly the two transposed rows
differing, each exactly at the dir/key legs); --check-receipt compares the derived
predictions against a receipt's observed CASE vectors (output-side cross-check only -- the
derivation never reads either artifact). The r59 receipt of record
(corpus/evidence/round59/openssl-probe.txt, mismatches=2) is NOT re-scored: the corrected
zero-U re-freeze is a new claim with a new scored run.

Run as:
  python3 plans/round59_c1_openssl_probe.py --lane . --work <scratch> \
      --receipt <path>                      # the scored battery (r59 entry form, bare = battery)
  python3 plans/round59_c1_openssl_probe.py --selftest --work <scratch>
  python3 plans/round59_c1_openssl_probe.py --render-table
  python3 plans/round59_c1_openssl_probe.py --check-frozen-table
  python3 plans/round59_c1_openssl_probe.py --check-receipt corpus/evidence/round59/openssl-probe.txt
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
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

# Lane-written candidate artifact sets (round-60 amendment): (name, defect class, cfg).
# Predictions are NOT stored here -- they are derived at run time by predict_legs()
# (the r59 lesson's mined fix: generated from the case definitions, never retyped).
# The r59 freeze's class annotations are carried verbatim. Leg order = TEST_NAMES.
CASES = [
    # the maintainer oracle's construction (solve.sh) as builder constants: all six legs pass.
    ("sol", "none -- the maintainer oracle's construction (S220)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # key left group/other readable: the permission-bits leg -- the class's filesystem-metadata leg.
    ("perm-loose", "key mode 0644 (the permission-bits leg)",
     dict(bits=2048, mode=0o644, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # 1024-bit key: the openssl rsa -text size leg; the cert built from it still passes.
    ("key-1024", "1024-bit key (the openssl rsa size leg)",
     dict(bits=1024, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # 30-day validity: the notAfter-notBefore window leg; nothing else moves.
    ("days-30", "30-day validity window",
     dict(bits=2048, mode=0o600, days=30, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # wrong Common Name: the cert subject leg, and with it the verification file and script legs.
    ("cn-wrong", "wrong Common Name (cert + verification + script legs)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_BAD, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # PEM holds the key only: the content-substring half of the PEM leg.
    ("pem-keyonly", "PEM holds the key only (substring tooth)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="keyonly",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # PEM carries both banner lines but a corrupt certificate block: the substring half passes,
    # the openssl-parse half fails -- the same leg's other tooth.
    ("pem-garbage", "PEM banners present, certificate block corrupt (openssl-parse tooth)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="garbage",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # verification.txt without the SHA-256 fingerprint: the fingerprint-format leg only.
    ("fp-absent", "verification.txt without the SHA-256 fingerprint",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=False, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # check_cert.py exits 0 silently: the script leg's string assertions.
    ("script-silent", "check_cert.py exits 0 silently",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SILENT, with_script=True, with_ssl=True)),
    # nothing under /app/ssl: every artifact leg fails; the script leg fails on its own read.
    ("dir-absent", "no /app/ssl at all",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=False)),
    # Organization written in caps: the grader's stated leniency (lowercased compare) -- all pass.
    ("org-upper", "Organization in caps (the grader's stated leniency)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG_UPPER, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=True, with_ssl=True)),
    # check_cert.py absent: the subprocess leg raises (artifact-absence is a leg failure, not setup).
    ("script-missing", "check_cert.py absent (artifact-absence is a leg failure, not setup)",
     dict(bits=2048, mode=0o600, days=365, cn=CN_OK, org=ORG, pem_mode="both",
          verif_fp=True, script=SCRIPT_SOL, with_script=False, with_ssl=True)),
]


def predict_legs(cfg):
    """Derive a case's six-leg prediction from its declared builder properties.

    The static model of the captured grader (round-60 freeze; each predicate is
    grounded in the capture's own assertions):
      dir   test_directory_structure  -- passes iff /app/ssl is created (:8-12).
      key   test_key_file             -- passes iff the dir exists, the mode bits
             satisfy <= 0o600 (:22) and openssl rsa -text reports 2048 bit (:31);
             the rsa read also needs the key file, hence with_ssl.
      cert  test_certificate_file     -- passes iff the cert exists with the right
             CN (:47) and the validity window is exactly 365 days (:79-80); the
             Organization compare is case-insensitive (:52-53), so ORG never moves
             this leg (the org-upper leniency case).
      pem   test_combined_pem_file    -- passes iff the PEM holds BOTH blocks
             (substring teeth :93-94) and the certificate block openssl-parses
             (:98-102); only pem_mode='both' satisfies both teeth.
      verif test_verification_file    -- passes iff verification.txt exists with the
             right CN (:114), a date line (always written by openssl), and the
             SHA-256 fingerprint (:134) -- absent when verif_fp is False.
      script test_python_verification_script -- passes iff check_cert.py exists,
             exits 0 printing the success line, the CN and an ISO expiration
             (:139-158); the sol script reads the cert through openssl, so a
             missing /app/ssl fails it too (with_ssl), and a wrong CN prints the
             wrong name.
    """
    with_ssl = bool(cfg["with_ssl"])
    dir_ok = with_ssl
    key_ok = with_ssl and cfg["mode"] <= 0o600 and cfg["bits"] == 2048
    cert_ok = with_ssl and cfg["cn"] == CN_OK and cfg["days"] == 365
    pem_ok = with_ssl and cfg["pem_mode"] == "both"
    verif_ok = with_ssl and cfg["verif_fp"] and cfg["cn"] == CN_OK
    script_ok = (bool(cfg["with_script"]) and with_ssl
                 and cfg["script"] == SCRIPT_SOL and cfg["cn"] == CN_OK)
    return tuple("P" if ok else "F"
                 for ok in (dir_ok, key_ok, cert_ok, pem_ok, verif_ok, script_ok))


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
    for name, _klass, cfg in CASES:
        predicted = predict_legs(cfg)
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


FROZEN_TABLE_DOC = "plans/round-59-claims.md"


def render_table(lines):
    """Print the prediction table GENERATED from the case definitions (never retyped)."""
    lines.append("| case | defect class exercised | dir | key | cert | pem | verif | script |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for name, klass, cfg in CASES:
        pred = "/".join(predict_legs(cfg))
        lines.append(f"| {name} | {klass} | {pred.replace('/', ' | ')} |")
    lines.append(f"TABLE cases={len(CASES)} legs={len(CASES) * len(TEST_NAMES)} "
                 f"predicted_u=0 source=CASES+predict_legs")


def parse_frozen_table(lane):
    """Parse the r59 freeze's frozen prediction table (the historical expectation)."""
    text = (pathlib.Path(lane) / FROZEN_TABLE_DOC).read_text(encoding="utf-8")
    table = {}
    pat = re.compile(
        r"^\| (\S+) \|[^|]+\| ([FPU]) \| ([FPU]) \| ([FPU]) \| ([FPU]) \| ([FPU]) \| ([FPU]) \|",
        re.M)
    for m in pat.finditer(text):
        table[m.group(1)] = tuple(m.group(i) for i in range(2, 8))
    return table


def check_frozen_table(lane, lines):
    """Falsifier-direction check: the derived table must differ from the r59 frozen
    table on EXACTLY the two transposed rows, each exactly at the dir/key legs."""
    frozen = parse_frozen_table(lane)
    missing = [n for n, _k, _c in CASES if n not in frozen]
    diffs = []
    derived_by_name = {}
    for name, _klass, cfg in CASES:
        got = predict_legs(cfg)
        derived_by_name[name] = got
        want = frozen.get(name)
        if want is None or want == got:
            continue
        cells = [i for i, (a, b) in enumerate(zip(want, got)) if a != b]
        diffs.append((name, cells))
    ok = (not missing and len(diffs) == 2
          and all(cells == [0, 1] for _n, cells in diffs)
          and {n for n, _ in diffs} == {"perm-loose", "key-1024"})
    for name, cells in diffs:
        lines.append(f"DIFF {name} legs={cells} "
                     f"frozen={'/'.join(frozen[name])} derived={'/'.join(derived_by_name[name])}")
    lines.append(f"FROZEN-TABLE rows={len(frozen)} differing={len(diffs)} "
                 f"missing={len(missing)} {'ok' if ok else 'FAIL'}")
    return 0 if ok else 1


def check_receipt(lane, receipt_path, lines):
    """Output-side cross-check: derived predictions vs a receipt's observed vectors.
    The derivation never reads this file; this mode is provenance documentation."""
    text = pathlib.Path(receipt_path).read_text(encoding="utf-8")
    observed = {}
    for m in re.finditer(r"^CASE (\S+) predicted=[FPU/]+ observed=([FPU/]+)", text, re.M):
        observed[m.group(1)] = tuple(m.group(2).split("/"))
    agree = sum(1 for n, _k, c in CASES
                if n in observed and observed[n] == predict_legs(c))
    for n, _k, c in CASES:
        if n in observed and observed[n] != predict_legs(c):
            lines.append(f"DISAGREE {n} observed={'/'.join(observed[n])} "
                         f"derived={'/'.join(predict_legs(c))}")
    lines.append(f"OBSERVED-CHECK cases={len(observed)} agree={agree}")
    return 0 if agree == len(observed) == len(CASES) else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None,
                    help="write the final text here as well as stdout")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--render-table", action="store_true",
                    help="print the prediction table generated from the case definitions")
    ap.add_argument("--check-frozen-table", action="store_true",
                    help="compare the derived table against the r59 frozen table")
    ap.add_argument("--check-receipt", default=None,
                    help="compare the derived table against a receipt's observed vectors")
    a = ap.parse_args(argv)
    lines = []
    rev = subprocess.run(["git", "-C", str(a.lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    lines.append(f"REV {rev}")
    if a.render_table:
        render_table(lines)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return 0
    if a.check_frozen_table:
        rc = check_frozen_table(pathlib.Path(a.lane), lines)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return rc
    if a.check_receipt:
        rc = check_receipt(pathlib.Path(a.lane), pathlib.Path(a.check_receipt), lines)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return rc
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
