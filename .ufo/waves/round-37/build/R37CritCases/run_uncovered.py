#!/usr/bin/env python3
"""R37CritCases: run 4 uncovered tb2 configure-git-webserver cases with the frozen probe's machinery.

Read-only on the lane: imports plans/git_webserver_probe.py (Case/files/run_case) and reads the captures
at corpus/evidence/round37/tb2-git-webserver/. All scratch under $TMPDIR.
"""
import hashlib
import importlib.util
import os
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/git_webserver_probe.py"
CAP = LANE / "corpus/evidence/round37/tb2-git-webserver"

spec = importlib.util.spec_from_file_location("cgw_probe", PROBE)
P = importlib.util.module_from_spec(spec)
sys.modules["cgw_probe"] = P  # python 3.14 dataclasses need the module registered before exec
spec.loader.exec_module(P)

HW = P.HW
PREDICTIONS = [
    ("multiline-token", "curl", P.files("first line\nTEST PASSED\n"), "pass",
     "verify.sh:62 multi-line body echo + test_outputs.py:13 substring over all stdout"),
    ("hello-plus-second-line", "curl", P.files(HW + "\nsecond line\n"), "fail",
     "verify.sh:60/:63 whole body compared after trailing-newline stripping only"),
    ("token-with-404", "curl", P.files("TEST PASSED\n", status=404), "fail",
     "verify.sh:59 -> :71; a non-200 body is never echoed, so no token on stdout"),
    ("second-request-500", "curl",
     {"mode": "sequence", "port": 8080, "path": "/hello.html",
      "responses": [[200, HW + "\n"], [500, HW + "\n"]]}, "pass",
     "verify.sh:60 does not check the second response's status; curl -s prints a 500 body"),
]
CASES = [P.Case(cid, tools, server, pred, mech) for cid, tools, server, pred, mech in PREDICTIONS]

DIAG_INERT = r'''
import subprocess, pathlib
r = subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)
print("DIAG stdout_lines=" + repr(r.stdout.splitlines()))
print("DIAG stderr_lines=" + repr(r.stderr.splitlines()))
p = pathlib.Path("/work/cwd")
print("DIAG cwd_files=" + repr(sorted(x.name for x in p.iterdir())))
for tool in ("expect", "git"):
    q = subprocess.run(["bash", "-c", "command -v " + tool], capture_output=True, text=True)
    print("DIAG " + tool + "_path=" + repr(q.stdout.strip()))
print("DIAG git_test_exp=" + ("present" if (p / "git_test.exp").exists() else "absent"))
print("VERDICT " + ("pass" if "TEST PASSED" in r.stdout else "fail"))
'''

DIAG_WRONGPORT = r'''
import subprocess
r = subprocess.run(["bash", "/tests/verify.sh"], capture_output=True, text=True)
print("DIAG grader_stdout=" + repr(r.stdout.splitlines()))
q = subprocess.run(["curl", "-s", "-w", "|%{http_code}", "http://localhost:8081/hello.html"],
                   capture_output=True, text=True)
print("DIAG port8081_body_status=" + repr(q.stdout))
print("VERDICT " + ("pass" if "TEST PASSED" in r.stdout else "fail"))
'''


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")

    def write(self, s):
        sys.__stdout__.write(s)
        self.f.write(s)

    def flush(self):
        sys.__stdout__.flush()
        self.f.flush()


def main():
    sys.stdout = Tee(pathlib.Path(__file__).with_name("run_uncovered.log"))
    root = pathlib.Path(os.environ["TMPDIR"]) / "runs"
    root.mkdir(parents=True, exist_ok=True)
    print("# probe sha256=" + hashlib.sha256(PROBE.read_bytes()).hexdigest())
    for name, digest in P.PINS.items():
        got = P.sha256(CAP / name)
        print(f"# capture {name} sha256={got} pinned={'yes' if got == digest else 'NO'}")
    print("# predictions (written before any run):")
    for c in CASES:
        print(f"PREDICT {c.cid} tools={c.tools} predicted={c.predicted} server={c.server!r} -- {c.requirement}")

    print("# observed:")
    matched = 0
    for c in CASES:
        rc, out = P.run_case(CAP, root, c)
        verdict = [l for l in out.splitlines() if l.startswith("VERDICT ")]
        if rc != 0 or len(verdict) != 1:
            print(f"CASE {c.cid} SETUP_FAILURE rc={rc}")
            print(out)
            continue
        obs = verdict[0].split()[1]
        err = verdict[0].split()[2] if len(verdict[0].split()) > 2 else ""
        match = obs == c.predicted
        matched += match
        print(f"CASE {c.cid} tools={c.tools} predicted={c.predicted} observed={obs}"
              f"{' ' + err if err else ''} match={'yes' if match else 'NO'}")
        stdout = [l[len("STDOUT "):] for l in out.splitlines() if l.startswith("STDOUT ")]
        print("  grader-stdout: " + (" | ".join(stdout) if stdout else "(none)"))
    print(f"uncovered_extra matched={matched}/{len(CASES)}")

    print("# diagnostics (not counted in the 4):")
    inert = P.Case("static-file-no-git", "curl", P.files(HW + "\n"), "pass", "diag: expect/git inertness")
    rc, out = P.run_case(CAP, root, inert, DIAG_INERT)
    print(f"DIAG inert rc={rc}")
    for l in out.splitlines():
        print("  " + l)
    wrong = P.Case("wrong-port-8081", "curl", P.files(HW + "\n", port=8081), "fail", "diag: 8081 really serves")
    rc, out = P.run_case(CAP, root, wrong, DIAG_WRONGPORT)
    print(f"DIAG wrongport rc={rc}")
    for l in out.splitlines():
        print("  " + l)
    return 0


if __name__ == "__main__":
    sys.exit(main())
