#!/usr/bin/env python3
"""F38IndepProbe: independent re-execution of the tb2 `build-pmars` grader.

Deliberately different instrument from plans/build_pmars_probe.py:
  - no import of plans/build_pmars_probe.py; own C source, own script, own case table,
    own constant texts (Results: 21 43 99, not 12 34 78; exit 7, not 3)
  - sandbox: GNU chroot inside a real root mount namespace (`sudo unshare -m` + chroot),
    /usr and /etc bind-mounted, NO bwrap, NO network/pid/ipc namespace
  - entry point: real pytest 8.4.1 on CPython 3.13 (`-rA`), the versions tests/test.sh pins,
    not a hand-rolled function-call harness
  - 8 assigned cases, all 14 remaining receipt cases as supplementary coverage,
    plus an empty-tree control whose only job is to show the instrument can fail
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

S = pathlib.Path(__file__).resolve().parent
TESTS = ("test_pmars_works", "test_headless_no_x11", "test_debian_source_used", "test_built_from_source")
ASSIGNED = ("canned-shape", "canned-x11-linked", "canned-x11-dlopen", "results-trailing-text",
            "canned-exit-nonzero", "path-split", "debian-is-file", "c-is-dir")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

DEBUG = "00010  DAT.F  #  7, #  4\n00011  SPL.B  #  0, # 11\n00012  MOV.AB # 12, @ 13\n"
BATTLE = "fight begins\nResults: 21 43 99\n"
BATTLE_TRAIL = "Results: 21 43 99 (forged)\n"
BATTLE_TWO = "Results: 21 43\n"
BATTLE_NEG = "Results: -1 43 99\n"
BATTLE_NOTLAST = "Results: 21 43 99\nend of battle\n"
DEBUG_ONE = "00010  DAT.F  #  7, #  4\n"
DEBUG_FOUR = "0010  DAT.F  # 7, # 4\n0011  SPL.B  # 0, # 11\n"

SHAPE = (("dir", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/dummy.c"))
DEBIAN_FILE = (("file", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/dummy.c"))
C_IS_DIR = (("dir", "pmars-0.9.4/debian"), ("dir", "pmars-0.9.4/src/sim.c"))
NO_DEBIAN = (("file", "pmars-0.9.4/src/dummy.c"),)
NO_SRC = (("dir", "pmars-0.9.4/debian"),)
SRC_NO_C = (("dir", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/pmars.h"))
ELSEWHERE = (("dir", "src/pmars-0.9.4/debian"), ("file", "src/pmars-0.9.4/src/dummy.c"))

CASES = [
    # cid, artefact kind, /app shape, sbin artefact
    ("canned-shape", "canned", SHAPE, None),
    ("canned-x11-linked", "x11", SHAPE, None),
    ("canned-x11-dlopen", "dlopen", SHAPE, None),
    ("results-trailing-text", "trailing", SHAPE, None),
    ("canned-exit-nonzero", "exit7", SHAPE, None),
    ("path-split", "silent", SHAPE, "script"),
    ("debian-is-file", "canned", DEBIAN_FILE, None),
    ("c-is-dir", "canned", C_IS_DIR, None),
    # supplementary: the rest of the receipt's 22
    ("empty-tree", "absent", (), None),
    ("canned-script", "script", SHAPE, None),
    ("canned-static", "static", SHAPE, None),
    ("results-two-ints", "twoints", SHAPE, None),
    ("results-not-last", "notlast", SHAPE, None),
    ("results-negative", "negative", SHAPE, None),
    ("one-address", "oneline", SHAPE, None),
    ("four-digit-address", "fourdigit", SHAPE, None),
    ("nonexec-binary", "nonexec", SHAPE, None),
    ("silent-binary", "silent", SHAPE, None),
    ("no-debian-dir", "canned", NO_DEBIAN, None),
    ("src-no-c", "canned", SRC_NO_C, None),
    ("no-src-dir", "canned", NO_SRC, None),
    ("pmars-dir-elsewhere", "canned", ELSEWHERE, None),
]

C_SRC = r'''
#include <stdio.h>
#include <string.h>
#ifdef HAVE_DLOPEN
#include <dlfcn.h>
#endif
#ifdef HAVE_X11REF
extern void *XOpenDisplay(const char *);
static void *(*volatile g_xdisp)(const char *) = XOpenDisplay;
#endif
int main(int argc, char **argv) {
    int battle = 0;
#ifdef HAVE_X11REF
    if (g_xdisp == 0) return 9;
#endif
    for (int i = 1; i < argc; i++) if (strcmp(argv[i], "-b") == 0) battle = 1;
#ifdef HAVE_DLOPEN
    (void)dlopen("libX11.so.6", RTLD_LAZY);
#endif
#ifndef QUIET
    fputs(battle ? BATTLE_TEXT : DEBUG_TEXT, stdout);
    fflush(stdout);
#endif
    return RC;
}
'''

SCRIPT = """#!/bin/sh
# F38IndepProbe standalone artefact (not from plans/build_pmars_probe.py)
for a in "$@"; do
  if [ "$a" = "-b" ]; then
    printf 'fight begins\\nResults: 21 43 99\\n'
    exit 0
  fi
done
printf '00010  DAT.F  #  7, #  4\\n00011  SPL.B  #  0, # 11\\n'
exit 0
"""


def c_lit(s):
    return json.dumps(s)


def art_cfg(kind):
    base = ["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE), "-DRC=0"]
    return {
        "canned": (base, []),
        "trailing": (["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE_TRAIL), "-DRC=0"], []),
        "twoints": (["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE_TWO), "-DRC=0"], []),
        "notlast": (["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE_NOTLAST), "-DRC=0"], []),
        "negative": (["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE_NEG), "-DRC=0"], []),
        "oneline": (["-DDEBUG_TEXT=" + c_lit(DEBUG_ONE), "-DBATTLE_TEXT=" + c_lit(BATTLE), "-DRC=0"], []),
        "fourdigit": (["-DDEBUG_TEXT=" + c_lit(DEBUG_FOUR), "-DBATTLE_TEXT=" + c_lit(BATTLE), "-DRC=0"], []),
        "exit7": (["-DDEBUG_TEXT=" + c_lit(DEBUG), "-DBATTLE_TEXT=" + c_lit(BATTLE), "-DRC=7"], []),
        "nonexec": (base, []),
        "silent": (["-DQUIET", "-DRC=0"], []),
        "static": (base, ["-static"]),
        "x11": (["-DHAVE_X11REF"] + base, ["-Wl,--no-as-needed", "-lX11"]),
        "dlopen": (["-DHAVE_DLOPEN"] + base, ["-ldl"]),
    }[kind]


def build_art(kind, dest, build):
    if kind == "absent":
        return
    if kind == "script":
        dest.write_text(SCRIPT)
        dest.chmod(0o755)
        return
    defs, link = art_cfg(kind)
    src = build / ("src_%s_%s.c" % (kind, dest.parent.name))
    src.write_text(C_SRC)
    subprocess.run(["/usr/bin/gcc", "-O1", "-o", str(dest), str(src)] + defs + link,
                   check=True, capture_output=True, text=True)
    dest.chmod(0o644 if kind == "nonexec" else 0o755)


def stage_app(shape, root):
    root.mkdir(parents=True, exist_ok=True)
    for kind, rel in shape:
        p = root / rel
        if kind == "dir":
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"")


def parse_pytest(out):
    got = {}
    for line in out.splitlines():
        m = re.match(r"^(PASSED|FAILED|ERROR)\s+\S*test_outputs\.py::(\w+)", line.strip())
        if m and m.group(2) in TESTS:
            got[m.group(2)] = "P" if m.group(1) == "PASSED" else "F"
    if set(got) != set(TESTS):
        return None
    return "".join(got[t] for t in TESTS)


MOUNT = r'''
set -eu
R="$1"; C="$2"; PATHIN="$3"; ENVDIR="$4"; PYROOT="$5"
mount --bind /usr "$R/usr"
mount --bind /etc "$R/etc"
mount --bind /dev "$R/dev"
mount -t proc proc "$R/proc"
mount --bind "$C/app" "$R/app"
mount --bind "$C/ulb" "$R/usr/local/bin"
mount --bind "$C/ulsb" "$R/usr/local/sbin"
mount --bind "$C/test_outputs.py" "$R/tests/test_outputs.py"
mount --bind "$ENVDIR" "$R/opt/env"
mkdir -p "$R$PYROOT"
mount --bind "$PYROOT" "$R$PYROOT"
exec chroot "$R" /usr/bin/env -i PATH="$PATHIN" HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp \
  /bin/sh -c 'cd /app && exec /opt/env/bin/python -m pytest -rA --tb=no -q -p no:cacheprovider /tests/test_outputs.py'
'''


def run_case(rootfs, case_dir, envdir, pyroot):
    r = subprocess.run(["sudo", "unshare", "-m", "--propagation", "private",
                        "/bin/bash", "-c", MOUNT, "bash", str(rootfs), str(case_dir), PATH,
                        str(envdir), str(pyroot)],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", required=True)
    ap.add_argument("--env", required=True)
    ap.add_argument("--receipt", required=True)
    a = ap.parse_args()
    cap = pathlib.Path(a.capture).resolve()
    pvenv = pathlib.Path(a.env).resolve()
    pin = hashlib.sha256((cap / "test_outputs.py").read_bytes()).hexdigest()

    receipt, violation = {}, {}
    for line in pathlib.Path(a.receipt).read_text().splitlines():
        m = re.match(r"CASE (\S+) predicted=\S+ observed=(\S+) tests=(\S+)", line)
        if m:
            receipt[m.group(1)] = m.group(3)
    pin_line = [l for l in pathlib.Path(a.receipt).read_text().splitlines()
                if "test_outputs.py sha256=" in l]
    receipt_pin = pin_line[0].split("sha256=")[1].strip() if pin_line else "ABSENT"

    home = [l.split("=", 1)[1].strip() for l in (pvenv / "pyvenv.cfg").read_text().splitlines()
            if l.startswith("home = ")][0]
    pyroot = pathlib.Path(home).parent

    rootfs = S / "rootfs"
    if rootfs.exists():
        try:
            shutil.rmtree(rootfs)
        except PermissionError:
            subprocess.run(["sudo", "rm", "-rf", str(rootfs)], check=True)
    for d in ("usr", "etc", "dev", "proc", "tmp", "tests", "app", "opt", "opt/env"):
        (rootfs / d).mkdir(parents=True, exist_ok=True)
    (rootfs / "tests" / "test_outputs.py").write_bytes(b"")
    for link, target in (("bin", "usr/bin"), ("sbin", "usr/bin"), ("lib", "usr/lib"), ("lib64", "usr/lib")):
        (rootfs / link).symlink_to(target)
    (rootfs / "tmp").chmod(0o1777)

    print("# F38IndepProbe independent run of the tb2 build-pmars grader")
    print(f"# capture test_outputs.py sha256={pin} receipt_pin={receipt_pin} pin_match={pin == receipt_pin}")
    print("# instrument: sudo unshare -m + chroot, bind /usr+/etc, pytest -rA (pytest 8.4.1, CPython 3.13)")
    agree = total = 0
    for cid, kind, shape, sbin in CASES:
        cd = S / "cases" / cid
        if cd.exists():
            shutil.rmtree(cd)
        for d in ("app", "ulb", "ulsb", "build"):
            (cd / d).mkdir(parents=True)
        (cd / "test_outputs.py").write_bytes((cap / "test_outputs.py").read_bytes())
        build_art(kind, cd / "ulb" / "pmars", cd / "build")
        if sbin:
            build_art(sbin, cd / "ulsb" / "pmars", cd / "build")
        stage_app(shape, cd / "app")
        rc, out = run_case(rootfs, cd, pvenv, pyroot)
        letters = parse_pytest(out)
        if letters is None:
            print(f"CASE {cid} INSTRUMENT-ERROR rc={rc}")
            print(out)
            return 2
        obs = "pass" if letters == "PPPP" else "fail"
        tags = []
        if cid in ASSIGNED:
            tags.append("assigned")
        if cid in receipt:
            same = receipt[cid] == letters
            tags.append(f"receipt_tests={receipt[cid]}")
            tags.append("agree=yes" if same else "agree=NO")
            if cid in ASSIGNED:
                total += 1
                agree += same
        print(f"CASE {cid} observed={obs} tests={letters} pytest_rc={rc} " + " ".join(tags))
    print(f"assigned_agree={agree}/{total} capture_sha256={pin}")
    return 0 if agree == total == len(ASSIGNED) else 1


if __name__ == "__main__":
    sys.exit(main())
