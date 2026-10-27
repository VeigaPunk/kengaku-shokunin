#!/usr/bin/env python3
"""R46W2C3Oracle independent replication harness (wave 2, kengaku round 46).

Recipe written from the grader's own text only:
  - os.listdir("/app/polyglot") == ["main.py.c"]
  - gcc main.py.c -o cmain, then for N in (42,"267914296"),(10,"55"),(0,"0")
    both `python3 main.py.c N` and `./cmain N` stdouts, .strip()ped, must equal expected,
    each subprocess with check=True.
The captured grader is executed byte-for-byte (loaded with importlib) from /work/test_outputs.py.
Nothing here is copied from plans/polyglot_c_py_probe.py, which this seat did not read.
"""
import importlib.util
import json
import os
import subprocess
import sys

POLY = "/app/polyglot"
MAIN = POLY + "/main.py.c"
GRADER = "/work/test_outputs.py"

# Lookup-table polyglot: C sees the Python body inside a block comment opened by `#define P /*`
# and closed by `#define Q */`; Python sees the C body inside a triple-quoted string opened by
# `"""` and closed by `#define R """`.  No Fibonacci computation: three hardcoded answers.
LOOKUP = '''#include <stdio.h>
#define P /*
import sys

TABLE = {"42": "267914296", "10": "55", "0": "0"}

if __name__ == "__main__":
    print(TABLE[sys.argv[1]])
    sys.exit(0)
"""
#define Q */
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    if (strcmp(argv[1], "42") == 0) { printf("267914296\\n"); return 0; }
    if (strcmp(argv[1], "10") == 0) { printf("55\\n"); return 0; }
    if (strcmp(argv[1], "0") == 0) { printf("0\\n"); return 0; }
    return 1;
}

#define R """
'''


def listing():
    try:
        return os.listdir(POLY)
    except OSError as exc:
        return ["<OSError:%s>" % type(exc).__name__]


def run_grader():
    spec = importlib.util.spec_from_file_location("captured_test_outputs", GRADER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        mod.test_fibonacci_polyglot()
        return {"verdict": "pass", "error": None}
    except BaseException as exc:  # assert or subprocess failure: any non-return is a fail
        first = str(exc).strip().splitlines()
        return {
            "verdict": "fail",
            "error": type(exc).__name__ + (": " + first[0][:200] if first else ""),
        }


def outputs():
    rec = {}
    for n in ("42", "10", "0"):
        py = subprocess.run(["python3", MAIN, n], capture_output=True, text=True)
        c = subprocess.run([POLY + "/cmain", n], capture_output=True, text=True)
        rec[n] = {
            "py": py.stdout.strip(),
            "c": c.stdout.strip(),
            "py_rc": py.returncode,
            "c_rc": c.returncode,
        }
    return rec


def main():
    case = sys.argv[-1]  # invocation: grade.py --work <scratch> <case>
    rec = {"case": case, "state_before": listing()}

    if case == "build":
        # oracle state: the publish solution run verbatim, cwd /app (it creates polyglot/ relatively)
        run = subprocess.run(["bash", "/work/solve.sh"], cwd="/app",
                             capture_output=True, text=True)
        rec["solve_rc"] = run.returncode
        rec["solve_stderr"] = run.stderr.strip()[:200]
        rec["state_built"] = listing()

    elif case == "oracle":
        rec["grade1"] = run_grader()
        rec["state_after_grade1"] = listing()
        rec["outputs_after_grade1"] = outputs()
        rec["grade2_same_state"] = run_grader()
        rec["state_after_grade2"] = listing()

    elif case == "lookup":
        os.makedirs(POLY, exist_ok=True)
        with open(MAIN, "w") as fh:
            fh.write(LOOKUP)
        rec["state_before_grade"] = listing()
        rec["grade1"] = run_grader()
        rec["state_after"] = listing()
        rec["outputs_after"] = outputs()

    elif case == "extra":
        with open(POLY + "/NOTES.md", "w") as fh:
            fh.write("harmless notes, not a source file\n")
        rec["state_before_grade"] = listing()
        rec["grade1"] = run_grader()
        rec["state_after"] = listing()  # if equal to state_before_grade, gcc never ran

    elif case == "leftover":
        run = subprocess.run(["gcc", MAIN, "-o", POLY + "/cmain"],
                             capture_output=True, text=True)
        rec["gcc_cmain_rc"] = run.returncode
        rec["gcc_cmain_stderr"] = run.stderr.strip()[:200]
        rec["state_before_grade"] = listing()
        rec["grade1"] = run_grader()
        rec["state_after"] = listing()

    else:
        raise SystemExit("unknown case: " + case)

    print(json.dumps(rec, sort_keys=True))


if __name__ == "__main__":
    main()
