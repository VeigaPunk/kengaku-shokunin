#!/usr/bin/env python3
"""Round-38 C2 probe: the pinned Terminal-Bench 2.0 `build-pmars` grader, executed offline.

  python3 plans/build_pmars_probe.py --lane .          run every frozen case, print the receipt
  python3 plans/build_pmars_probe.py --lane . --dry    print the frozen case table only (no sandbox)
  python3 plans/build_pmars_probe.py --lane . --smoke  exercise the sandbox plumbing without the grader

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before
any case), inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr read-only, /tmp
private, /app and /usr/local/bin and /usr/local/sbin bound read-only to the case's staged trees, /tests
holding only the capture, cwd /app, PATH = Debian's default order
(/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin). The grader module is imported from the
capture and its four test functions are called in file order: an AssertionError is `F`, any other
exception is `F` with its class named, a return is `P`. The case verdict is `pass` iff all four are `P`
(pytest exits 0 iff no test fails; tests/test.sh writes reward 1 iff pytest exits 0).

What a case stages: the artefact at /usr/local/bin/pmars (and optionally /usr/local/sbin/pmars) is one of
  canned   a C program compiled on the host by gcc that prints fixed text: two debugger lines of the form
           `NNNNN OPC.M ...` for any argv without `-b`, and a battle transcript ending in a `Results:` line
           for argv with `-b`; it reads no warrior file and contains no pMARS code
  script   the same text from a bash script
  silent   a dynamic C program that prints nothing and exits 0
  absent   no file
with link variants (dynamic, -static, linked against libX11, dlopen of libX11 at run time), an exit code,
and the file mode; the /app tree is a list of directories and files (zero-byte unless stated). The warrior
files `rave.red` and `flashpaper.red` exist in no case.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). The tags are frozen
with the predictions; the entry's requirement map is derived from them and from the observed verdicts.

Limits, stated before the first run: this is a probe of the grader, never of the task's intended path —
the oracle `solution/solve.sh` is not executed (it needs root, apt and Debian's network). The sandbox shell
/bin/sh is the host's (bash on this host; Debian's is dash, whose `echo -e` prints `-e`); no canned
artefact reads stdin, so the debugger input never reaches a verdict. `ldd` is the host's glibc script.
Predictions below were written from a static reading of tests/test_outputs.py and instruction.md before
the first run.

Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work, else
$TMPDIR (tempfile default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round38/tb2-build-pmars"
PINS = {
    "test_outputs.py": "d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85",
    "instruction.md": "1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82",
}
BWRAP = "/usr/bin/bwrap"
GCC = "/usr/bin/gcc"
TESTS = ("test_pmars_works", "test_headless_no_x11", "test_debian_source_used", "test_built_from_source")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Instruction requirements (instruction.md line -> tag). A case violates a tag when its staged state does
# not do what the instruction asks under that tag, whatever the grader says.
TAGS = {
    "from-source": "instruction.md:1",      # build pMARS from source (also :3 "build")
    "no-x11": "instruction.md:3",           # build without X11 support (also :1 "no X server", :9)
    "debian-source": "instruction.md:3",    # source from Debian packages (also :9 "uses Debian sources")
    "extract-to-app": "instruction.md:3",   # extract the source to /app
    "install-path": "instruction.md:3",     # install the binary to /usr/local/bin/pmars
    "results-format": "instruction.md:7",   # the :5 command prints "Results: X Y Z", integers
    "debugger-works": "instruction.md:9",   # the debugger works properly
}
FAKE = ("from-source", "debian-source", "extract-to-app", "debugger-works")  # every canned/script artefact

DEBUG_OK = "00000   SPL.B  $     2, $     0\n00001   MOV.I  $     0, $     1\n"
BATTLE_OK = "rave by Stefan Strack scores 12\nflashpaper by Matt Hastings scores 34\nResults: 12 34 78\n"
SHAPE = (("dir", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/dummy.c"))


@dataclasses.dataclass(frozen=True)
class Art:
    kind: str = "canned"            # canned | script | silent | absent
    link: str = "dynamic"           # dynamic | static | x11 | dlopen-x11
    debug: str = DEBUG_OK
    battle: str = BATTLE_OK
    exit: int = 0
    mode: int = 0o755


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    art: Art                        # /usr/local/bin/pmars
    app: tuple                      # (("dir"|"file", relpath), ...) under /app
    predicted: str                  # four letters P/F in TESTS order
    violates: tuple                 # TAGS keys
    requirement: str
    sbin: Art = Art(kind="absent")  # /usr/local/sbin/pmars (earlier on PATH)


CASES = [
    Case("empty-tree", Art(kind="absent"), (), "FFFF", tuple(TAGS),
         "do-nothing: no binary, empty /app"),
    Case("canned-shape", Art(), SHAPE, "PPPP", FAKE,
         "canned C program, empty debian/ dir, zero-byte src/dummy.c: no pMARS, no Debian source, no build"),
    Case("canned-script", Art(kind="script"), SHAPE, "PFPP", FAKE,
         "the canned text from a bash script: ldd says not a dynamic executable on stderr, stdout empty"),
    Case("canned-static", Art(link="static"), SHAPE, "PFPP", FAKE,
         "canned program linked -static: ldd exits 1 with empty stdout"),
    Case("canned-x11-linked", Art(link="x11"), SHAPE, "PFPP", FAKE + ("no-x11",),
         "canned program linked against libX11 (--no-as-needed): ldd lists libX11"),
    Case("canned-x11-dlopen", Art(link="dlopen-x11"), SHAPE, "PPPP", FAKE + ("no-x11",),
         "canned program that dlopen()s libX11.so.6 at run time: no DT_NEEDED entry for ldd to list"),
    Case("results-two-ints", Art(battle="Results: 12 34\n"), SHAPE, "FPPP", FAKE + ("results-format",),
         "battle line carries two integers"),
    Case("results-trailing-text", Art(battle="Results: 12 34 78 forged\n"), SHAPE, "PPPP",
         FAKE + ("results-format",), "battle line `Results: 12 34 78 forged`: re.match anchors the start only"),
    Case("results-not-last", Art(battle="Results: 12 34 78\nend of battle\n"), SHAPE, "FPPP",
         FAKE + ("results-format",), "a line after the Results line: `tail -n 1` sees the extra line"),
    Case("results-negative", Art(battle="Results: -1 34 78\n"), SHAPE, "FPPP", FAKE + ("results-format",),
         "a negative integer: \\d+ does not match the sign"),
    Case("one-address", Art(debug="00000   SPL.B  $     2, $     0\n"), SHAPE, "FPPP", FAKE,
         "debugger text with one address line (grader needs >= 2)"),
    Case("four-digit-address", Art(debug="0000   SPL.B  $ 2, $ 0\n0001   MOV.I  $ 0, $ 1\n"), SHAPE, "FPPP",
         FAKE, "debugger addresses with four digits (grader needs \\d{5})"),
    Case("canned-exit-nonzero", Art(exit=3), SHAPE, "PPPP", FAKE,
         "canned program exits 3: run_shell_command returns e.output when it is non-empty"),
    Case("nonexec-binary", Art(mode=0o644), SHAPE, "FPPP", FAKE + ("install-path",),
         "binary installed without the execute bit: exists() holds, the shell cannot run it"),
    Case("silent-binary", Art(kind="silent"), SHAPE, "FPPP", FAKE + ("install-path",),
         "installed binary prints nothing"),
    Case("path-split", Art(kind="silent"), SHAPE, "PPPP", FAKE + ("install-path",),
         "/usr/local/bin/pmars prints nothing; a canned script at /usr/local/sbin/pmars (earlier on PATH) "
         "answers the behaviour checks, ldd reads the silent one", sbin=Art(kind="script")),
    Case("no-debian-dir", Art(), (("file", "pmars-0.9.4/src/dummy.c"),), "PPFP", FAKE,
         "source tree without debian/"),
    Case("debian-is-file", Art(), (("file", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/dummy.c")),
         "PPPP", FAKE, "debian is a zero-byte regular file: Path.exists() holds"),
    Case("src-no-c", Art(), (("dir", "pmars-0.9.4/debian"), ("file", "pmars-0.9.4/src/pmars.h")), "PPPF", FAKE,
         "src/ holds a header only"),
    Case("c-is-dir", Art(), (("dir", "pmars-0.9.4/debian"), ("dir", "pmars-0.9.4/src/sim.c")), "PPPP", FAKE,
         "src/sim.c is a directory: glob('*.c') matches it"),
    Case("no-src-dir", Art(), (("dir", "pmars-0.9.4/debian"),), "PPPF", FAKE,
         "source tree without src/"),
    Case("pmars-dir-elsewhere", Art(), (("dir", "src/pmars-0.9.4/debian"), ("file", "src/pmars-0.9.4/src/dummy.c")),
         "PPFF", FAKE, "tree under /app/src/pmars-0.9.4, not /app/pmars-*: the glob is one level deep"),
]

C_SRC = r'''#include <stdio.h>
#include <string.h>
#ifdef DLX11
#include <dlfcn.h>
#endif
#ifdef LINKX11
extern void *XOpenDisplay(const char *);
void *(*volatile keep_x11)(const char *) = XOpenDisplay;
#endif
int main(int argc, char **argv) {
#ifdef DLX11
    void *h = dlopen("libX11.so.6", RTLD_LAZY);
    (void)h;
#endif
    int battle = 0;
    for (int i = 1; i < argc; i++) if (strcmp(argv[i], "-b") == 0) battle = 1;
#ifndef SILENT
    fputs(battle ? BATTLE : DEBUG, stdout);
#endif
    return EXITCODE;
}
'''

HARNESS_PY = r'''
import importlib.util
spec = importlib.util.spec_from_file_location("tb2_build_pmars_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in %r:
    try:
        getattr(mod, name)()
        print("TEST " + name + " P")
    except AssertionError:
        print("TEST " + name + " F")
    except Exception as e:
        print("TEST " + name + " F error=" + type(e).__name__)
''' % (TESTS,)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def c_literal(s):
    return json.dumps(s)  # ASCII-only texts: a JSON string is a valid C string literal


def build_art(art, dest, work):
    """Stage the artefact at dest (a file path); returns nothing for `absent`."""
    if art.kind == "absent":
        return
    if art.kind == "script":
        lines = ["#!/usr/bin/bash", 'for a in "$@"; do if [ "$a" = "-b" ]; then',
                 "printf '%s' " + _sh(art.battle) + "; exit " + str(art.exit) + "; fi; done",
                 "printf '%s' " + _sh(art.debug), "exit " + str(art.exit)]
        dest.write_text("\n".join(lines) + "\n")
    else:
        src = work / "art.c"
        src.write_text(C_SRC)
        argv = [GCC, "-O1", "-o", str(dest), str(src), f"-DEXITCODE={art.exit}",
                f"-DBATTLE={c_literal(art.battle)}", f"-DDEBUG={c_literal(art.debug)}"]
        if art.kind == "silent":
            argv.append("-DSILENT")
        if art.link == "static":
            argv.append("-static")
        elif art.link == "x11":
            argv += ["-DLINKX11", "-Wl,--no-as-needed", "-lX11"]
        elif art.link == "dlopen-x11":
            argv.append("-DDLX11")
        subprocess.run(argv, check=True, capture_output=True, text=True)
    os.chmod(dest, art.mode)


def _sh(s):
    return "'" + s.replace("'", "'\\''") + "'"


def stage_app(app, root):
    root.mkdir(parents=True)
    for kind, rel in app:
        p = root / rel
        if kind == "dir":
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"")


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--ro-bind", str(work / "ulb"), "/usr/local/bin",
             "--ro-bind", str(work / "ulsb"), "/usr/local/sbin",
             "--ro-bind", str(work / "app"), "/app",
             "--dir", "/tests", "--ro-bind", str(cap / "test_outputs.py"), "/tests/test_outputs.py",
             "--ro-bind", str(work / "harness.py"), "/harness.py",
             "--chdir", "/app"]
    return argv


def run_case(cap, root, case, script=HARNESS_PY):
    work = pathlib.Path(tempfile.mkdtemp(prefix="bpm-", dir=root))
    try:
        (work / "ulb").mkdir()
        (work / "ulsb").mkdir()
        (work / "build").mkdir()
        build_art(case.art, work / "ulb" / "pmars", work / "build")
        build_art(case.sbin, work / "ulsb" / "pmars", work / "build")
        stage_app(case.app, work / "app")
        (work / "harness.py").write_text(script)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py"], env=env,
                           capture_output=True, text=True, timeout=180)
        return r.returncode, r.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def overall(letters):
    return "pass" if letters == "P" * len(TESTS) else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent (default: $TMPDIR via tempfile)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids) or any(t not in TAGS for c in CASES for t in c.violates):
        print("SETUP duplicate case id or unknown tag", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(overall(c.predicted) == 'pass' for c in CASES)}"
              f" predicted_fail={sum(overall(c.predicted) == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    for tool in (BWRAP, GCC):
        if not os.access(tool, os.X_OK):
            print(f"SETUP {tool} is required", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k38-bpm-", dir=a.work))
    try:
        if a.smoke:
            smoke = Case("smoke", Art(), SHAPE, "PPPP", (), "plumbing only")
            script = ("import subprocess\nr = subprocess.run('pmars -b x | tail -n 1', shell=True, capture_output=True,"
                      " text=True)\nprint('SMOKE out=' + r.stdout.strip())\n")
            rc, out = run_case(cap, root, smoke, script)
            print(out, end="")
            print(f"SMOKE rc={rc}")
            return 0 if rc == 0 and "SMOKE out=Results: 12 34 78" in out else 1
        print("# tb2 build-pmars grader probe (kengaku round 38) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = 0
        for c in CASES:
            rc, out = run_case(cap, root, c)
            got = {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] == "TEST" and parts[1] in TESTS:
                    got[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield four test verdicts (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in TESTS if got[t][1])
            obs = overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
