#!/usr/bin/env python3
"""Replay the captured `sparql-university` grader with its own three test functions and its own
pytest reward rule (round 97, R97-C1).

The task image (captured `environment/Dockerfile`) is ubuntu:24.04 with only the agent graph at
/app/university_graph.ttl; the agent's artefact is the text file /app/solution.sparql. The verifier
(`tests/test.sh`) runs `/tests/test_outputs.py` under `uvx -p 3.13 -w pytest==8.4.1 -w rdflib==7.1.4`
and writes reward 1 iff pytest exits 0. The grader reads a DIFFERENT graph,
/tests/university_graph_test.ttl. This probe models the verifier side with one pre-staged virtual
environment passed by path:

    --grader-venv  python 3.13.x, rdflib 7.1.4, pytest 8.4.1

Its pinned versions are checked inside the sandbox before any case runs (a mismatch is a setup
defect, exit 2). The receipt stamps only the pinned values (GRADER_SIDE: python minor, rdflib,
pytest); the resolved unpinned values (CPython micro, pyparsing) go to GRADER_UNPINNED,
which a re-run need not reproduce (round-96 W-2: an L6 that compares unpinned resolutions fails
with no behaviour change). Staging the venv needs the network; the probe itself does not: every
case runs in a fresh bubblewrap namespace with --unshare-all (no network) and --clearenv (no
inherited host environment), tmpfs root, host /usr read-only, the venv and its uv-managed
interpreter read-only, the case /app read-write, the captured tests read-only at /tests. Host /etc
is not bound.

Each case stages /app with the agent graph and runs the captured `solution/solve.sh` unmodified
with the image's bash (except `absent`, `empty`, and the three literal-query cases, which write
their own file). The case's declared text transform is then applied to /app/solution.sparql by
this probe; every transform asserts that its anchor occurs exactly as often as declared, so a
changed solve.sh is a setup defect, never a silent no-op. The harness imports the captured
`test_outputs.py` unmodified with the grader python and calls its three test functions in file
order, then runs real pytest on the same file for the reward leg:

    exists   test_sparql_file_exists          P returned, F AssertionError,
    runs     test_sparql_runs_without_error    E:<exception type name> anything else
    results  test_sparql_query_results
    reward   1 iff `python -m pytest -p no:cacheprovider /tests/test_outputs.py` exits 0, else 0

No assertion is reimplemented. Every bind source except /usr and the venv/interpreter trees lives
under --work or the lane capture. The bwrap path is injectable so a sandbox-outage control runs.

Usage:  python3 plans/round97_sparql_probe.py --lane <repo> --work <scratch dir>
            --grader-venv <dir> [--bwrap PATH]
Exit:   0 every case observed == predicted, 1 a case differed, 2 setup defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CAP = "corpus/evidence/round97/graders/sparql-university"
TABLE = "plans/round97-cases.json"
TOOL = "plans/round97_sparql_probe.py"
MEMBER = "sparql-university"
HEADER = "# tb2 sparql-university grader probe (round 97)"
PINS = {
    "tests/test_outputs.py": "ecf15840fc14f1eeff2f3b6317d7f0febc8fa81f688d24e3054205ba13207b39",
    "tests/test.sh": "45902b57bd0f1dd6959216bc9943ab27bb349edc7ff557035a1ecc8732e4cc6b",
    "tests/university_graph_test.ttl": "368ce01d32513ee04dfe592784b0c976086e514c1eab9b3165a016ca7b0192cb",
    "solution/solve.sh": "d17995a8f29c6d656c749271fd28e10d31afee6aa75f40ad28fea1c907f2a791",
    "environment/Dockerfile": "dd0abcd64e90ab16141169bcbf88a8e5f52732f207cb37765d351cc7a48916a9",
    "environment/university_graph.ttl": "0b0b1f2c0ee7ea7ddc9382f94ff8181996ffa7be60a1651111c1f57b49e09a85",
}
SUBJECT_SHA = PINS["tests/test_outputs.py"]
DEFAULT_BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 300
GRADER_WANT = ("3.13", "7.1.4", "8.4.1")   # tests/test.sh uvx pins: -p 3.13, rdflib, pytest
TESTS = ("test_sparql_file_exists", "test_sparql_runs_without_error", "test_sparql_query_results")

REF_DATE = '"2025-08-16"^^xsd:date'
TODAY = 'STRDT(SUBSTR(STR(NOW()), 1, 10), xsd:date)'
EU_BLOCK = ('  VALUES ?euCountry {\n  "AT" "BE" "BG" "HR" "CY" "CZ" "DK" "EE" "FI" "FR"\n'
            '  "DE" "GR" "HU" "IE" "IT" "LV" "LT" "LU" "MT" "NL"\n  "PL" "PT" "RO" "SK" "SI" "ES" "SE"\n  }\n')
GRAD_FILTER = ('  FILTER( ?enrollDate <= "2025-08-16"^^xsd:date &&\n'
               '          (!BOUND(?gradDate) || ?gradDate > "2025-08-16"^^xsd:date) )\n')
PROJ = 'SELECT ?professorName (GROUP_CONCAT(DISTINCT ?country; separator=", ") AS ?countries)'
PREFIXES = "PREFIX uni: <http://university.org/ontology/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
REFERENCE_VALUES = ('SELECT ?professorName ?countries WHERE {\n  VALUES (?professorName ?countries) {\n'
                    '    ("Giorgos Stamou" "GR, US") ("Chrysoula Zerva" "PT, GR")\n'
                    '    ("Aristotle Tympas" "GR") ("Alex Dimakis" "US, ES, CH")\n  }\n}\n')
AGENT_VALUES = ('SELECT ?professorName ?countries WHERE {\n  VALUES (?professorName ?countries) {\n'
                '    ("Orfeas Menis" "GR, US") ("Pepe Attanasio" "PT, GR") ("Aristotle Tympas" "GR")\n  }\n}\n')
PER_DEPARTMENT = PREFIXES + PROJ + """
WHERE {
  ?professor a uni:Person ;
             uni:hasName ?professorName ;
             uni:role ?role ;
             uni:worksIn ?euDepartment ;
             uni:worksIn ?bigDepartment ;
             uni:worksIn ?departmentForCountries .
  FILTER(STRSTARTS(?role, "Professor"))
  ?departmentForCountries uni:belongsTo ?university .
  ?university uni:locatedInCountry ?country .
  ?euDepartment uni:belongsTo ?euUniversity .
  ?euUniversity uni:locatedInCountry ?euCountry .
  VALUES ?euCountry {
  "AT" "BE" "BG" "HR" "CY" "CZ" "DK" "EE" "FI" "FR"
  "DE" "GR" "HU" "IE" "IT" "LV" "LT" "LU" "MT" "NL"
  "PL" "PT" "RO" "SK" "SI" "ES" "SE"
  }
  {
    SELECT ?bigDepartment WHERE {
      ?class uni:isTaughtIn ?bigDepartment .
      ?student uni:isEnrolledIn ?class ;
               uni:hasEnrollmentDate ?enrollDate .
      OPTIONAL { ?student uni:hasGraduationDate ?gradDate }
      FILTER( ?enrollDate <= "2025-08-16"^^xsd:date &&
              (!BOUND(?gradDate) || ?gradDate > "2025-08-16"^^xsd:date) )
    }
    GROUP BY ?bigDepartment
    HAVING(COUNT(DISTINCT ?student) > 10)
  }
}
GROUP BY ?professorName
"""

# kind -> (source, list of (old, new, expected occurrence count)); source "solve" = the captured
# solve.sh output, a str = the literal file content written instead of running solve.sh, None = no file.
VARIANTS: dict[str, tuple[object, list[tuple[str, str, int]]]] = {
    "solve": ("solve", []),
    "absent": (None, []),
    "empty": ("", []),
    "syntax-error": ("solve", [("}\nGROUP BY ?professorName", "GROUP BY ?professorName", 1)]),
    "no-eu-filter": ("solve", [(EU_BLOCK, "", 1)]),
    "now-date": ("solve", [(REF_DATE, TODAY, 2)]),
    "no-graduation-filter": ("solve", [(GRAD_FILTER, '  FILTER( ?enrollDate <= "2025-08-16"^^xsd:date )\n', 1)]),
    "contains-professor": ("solve", [('FILTER(STRSTARTS(?role, "Professor"))', 'FILTER(CONTAINS(?role, "Professor"))', 1)]),
    "per-department": (PER_DEPARTMENT, []),
    "answer-literal": (REFERENCE_VALUES, []),
    "duplicate-rows": ("solve", [("@@UNION-SELF@@", "", 0)]),
    "extra-column": ("solve", [('AS ?countries)', 'AS ?countries) (COUNT(DISTINCT ?student) AS ?n)', 1)]),
    "semicolon-separator": ("solve", [('separator=", "', 'separator="; "', 1)]),
    "comma-no-space": ("solve", [('separator=", "', 'separator=","', 1)]),
    "concat-no-distinct": ("solve", [('GROUP_CONCAT(DISTINCT ?country;', 'GROUP_CONCAT(?country;', 1)]),
    "wrong-variable-name": ("solve", [('?professorName', '?name', 3)]),
    "agent-graph-literal": (AGENT_VALUES, []),
    "ask-query": ("solve", [(PROJ, "ASK", 1), ("GROUP BY ?professorName\nHAVING(COUNT(DISTINCT ?student) > 10)\n", "", 1)]),
}

HARNESS = r"""
import importlib.util, os, subprocess, sys
os.chdir("/app")
sys.path[:0] = ["/tests"]
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = []
for name in %r:
    try:
        getattr(mod, name)()
        out.append("P")
    except AssertionError:
        out.append("F")
    except BaseException as error:
        out.append("E:" + type(error).__name__)
proc = subprocess.run([sys.executable, "-I", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                       "/tests/test_outputs.py"], capture_output=True, text=True)
out.append("1" if proc.returncode == 0 else "0")
print("PAYLOAD " + ",".join(out))
try:
    from rdflib import Graph
    g = Graph()
    g.parse("/tests/university_graph_test.ttl", format="ttl")
    res = g.query(open("/app/solution.sparql", encoding="utf-8").read())
    rows = [tuple(str(x) for x in r) for r in res] if res.type == "SELECT" else []
    names = sorted(set(str(dict(zip([str(v) for v in res.vars], row)).get("professorName", "")) for row in rows))
    vars_ = "+".join(str(v) for v in (res.vars or [])) or "-"
    shown = "|".join(n.replace(" ", "_") for n in names if n) or "-"
    print(f"DETAIL form={res.type} vars={vars_} rows={len(rows)} distinct={len(set(rows))} names={shown}")
except BaseException as error:
    print("DETAIL error=" + type(error).__name__)
""" % (TESTS,)

VERSIONS = ("import sys, rdflib, pytest, pyparsing\n"
            "print('VERSIONS', sys.version.split()[0], rdflib.__version__, pytest.__version__,"
            " pyparsing.__version__)\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guarded(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


class Box:
    """One sandbox recipe: the read-only interpreter/venv binds shared by every run."""

    def __init__(self, bwrap: str, ro_trees: list[str]):
        self.bwrap = bwrap
        self.ro_trees = ro_trees

    def cmd(self, binds: list[tuple[str, str, str]], chdir: str, path: str, argv: list[str]) -> list[str]:
        cmd = [self.bwrap, "--die-with-parent", "--unshare-all", "--clearenv",
               "--tmpfs", "/", "--ro-bind", "/usr", "/usr",
               "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
               "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
               "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        for tree in self.ro_trees:
            cmd += ["--ro-bind", tree, tree]
        for kind, src, dst in binds:
            cmd += [kind, src, dst]
        return cmd + ["--setenv", "PATH", path, "--setenv", "HOME", "/tmp",
                      "--setenv", "LANG", "C.UTF-8", "--chdir", chdir, *argv]

    def run(self, binds, chdir, path, argv) -> subprocess.CompletedProcess:
        return subprocess.run(self.cmd(binds, chdir, path, argv), capture_output=True, text=True,
                              timeout=CASE_TIMEOUT)


def venv_python(venv: Path) -> Path:
    return venv / "bin" / "python"


def check_venv(box: Box, venv: Path, scratch: Path) -> tuple[str, str]:
    probe = scratch / "versions.py"
    probe.write_text(VERSIONS, encoding="utf-8")
    proc = box.run([("--ro-bind", str(probe), "/versions.py")], "/tmp", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/versions.py"])
    line = next((x for x in proc.stdout.splitlines() if x.startswith("VERSIONS ")), "")
    parts = line.split()
    if (len(parts) != 5 or ".".join(parts[1].split(".")[:2]) != GRADER_WANT[0]
            or parts[2] != GRADER_WANT[1] or parts[3] != GRADER_WANT[2]):
        raise SystemExit("SETUP venv %s versions %r rc=%d %s" % (venv, line, proc.returncode,
                                                                   proc.stderr.strip()[-200:]))
    pinned = "%s %s %s" % (GRADER_WANT[0], parts[2], parts[3])
    unpinned = "%s %s" % (parts[1], parts[4])
    return pinned, unpinned


def transform(text: str, edits: list[tuple[str, str, int]], kind: str) -> str:
    if edits == [("@@UNION-SELF@@", "", 0)]:
        # the whole solution SELECT, unioned with itself inside an outer SELECT of the two names
        head = "".join(x + "\n" for x in text.splitlines() if x.startswith("PREFIX "))
        body = "".join(x + "\n" for x in text.splitlines() if not x.startswith("PREFIX "))
        if text.count("SELECT ") != 1 or not head or not body.strip():
            raise SystemExit("SETUP transform %s needs one SELECT with PREFIX lines" % kind)
        return (head + "SELECT ?professorName ?countries WHERE {\n{\n" + body + "}\nUNION\n{\n"
                + body + "}\n}\n")
    for old, new, count in edits:
        if text.count(old) != count:
            raise SystemExit("SETUP transform %s anchor %r occurs %d times, want %d" % (kind, old[:40], text.count(old), count))
        text = text.replace(old, new)
    return text


def stage(box: Box, case: dict, cap: Path, root: Path) -> Path:
    kind = case["app"]
    if kind not in VARIANTS:
        raise SystemExit("SETUP unknown app kind %s" % kind)
    source, edits = VARIANTS[kind]
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    app.mkdir(parents=True)
    shutil.copyfile(cap / "environment" / "university_graph.ttl", app / "university_graph.ttl")
    target = app / "solution.sparql"
    if source is None:
        return app
    if source != "solve":
        target.write_text(source, encoding="utf-8")
        return app
    script = root / "solve.sh"
    shutil.copyfile(cap / "solution" / "solve.sh", script)
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(script), "/solve.sh")], "/app",
                   "/usr/bin", ["/usr/bin/bash", "/solve.sh"])
    if proc.returncode != 0 or not target.is_file():
        raise SystemExit("SETUP solve.sh wrote no query rc=%d %s" % (proc.returncode, proc.stderr.strip()[-300:]))
    if edits:
        target.write_text(transform(target.read_text(encoding="utf-8"), edits, kind), encoding="utf-8")
    return app


def run_case(box: Box, app: Path, tests: Path, harness: Path, grader_venv: Path) -> tuple[str, str]:
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                    ("--ro-bind", str(harness), "/harness.py")], "/app", "%s/bin:/usr/bin" % grader_venv,
                   [str(venv_python(grader_venv)), "-I", "-B", "/harness.py"])
    payload = "NOPAYLOAD(rc=%d)" % proc.returncode
    detail = "DETAIL absent"
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            payload = line.split(" ", 1)[1]
        elif line.startswith("DETAIL "):
            detail = line
    return payload, detail


def interpreter_root(venv: Path) -> str:
    """The uv-managed interpreter store a venv's python resolves into (bound read-only whole)."""
    real = venv_python(venv).resolve()
    return str(real.parent.parent.parent)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--grader-venv", required=True)
    parser.add_argument("--bwrap", default=DEFAULT_BWRAP)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    grader_venv = Path(args.grader_venv).resolve()
    for p in (work, grader_venv):
        if p == lane or lane in p.parents:
            print("DEFECT SETUP path inside the lane %s" % p)
            return 2
    work.mkdir(parents=True, exist_ok=True)
    cap = lane / CAP
    if not Path(args.bwrap).is_file() or not os.access(args.bwrap, os.X_OK):
        print("DEFECT SETUP sandbox-unavailable %s" % args.bwrap)
        return 2
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    if not userns.isdigit() or int(userns) <= 0:
        print("DEFECT SETUP user namespaces unavailable (%s)" % userns)
        return 2
    for rel, want in PINS.items():
        p = cap / rel
        if not p.is_file() or sha(p.read_bytes()) != want:
            print("DEFECT SETUP capture sha mismatch %s" % rel)
            return 2
    if not venv_python(grader_venv).exists():
        print("DEFECT SETUP venv python absent %s" % grader_venv)
        return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    box = Box(args.bwrap, sorted({str(grader_venv), interpreter_root(grader_venv)}))
    try:
        pinned, unpinned = check_venv(box, grader_venv, work)
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    harness = work / "harness.py"
    harness.write_text(HARNESS, encoding="utf-8")
    tests = work / "tests"
    if tests.exists():
        shutil.rmtree(tests)
    tests.mkdir()
    for name in ("test_outputs.py", "university_graph_test.ttl"):
        shutil.copyfile(cap / "tests" / name, tests / name)
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("TEST_SH_SHA %s" % PINS["tests/test.sh"])
    print("TEST_GRAPH_SHA %s" % PINS["tests/university_graph_test.ttl"])
    print("SOLVE_SHA %s" % PINS["solution/solve.sh"])
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("GRADER_SIDE python,rdflib,pytest %s" % pinned)
    print("GRADER_UNPINNED python,pyparsing %s" % unpinned)
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("SANDBOX clearenv=1 unshare-all=1 etc-bound=0")
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    try:
        for case in table["cases"]:
            app = stage(box, case, cap, work / "cases" / case["id"])
            observed, detail = run_case(box, app, tests, harness, grader_venv)
            ok = observed == case["predicted"]
            mismatches += 0 if ok else 1
            print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
            print("%s %s" % (detail.replace("DETAIL", "DETAIL " + case["id"], 1), case["app"]))
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    finally:
        shutil.rmtree(work / "cases", ignore_errors=True)
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
