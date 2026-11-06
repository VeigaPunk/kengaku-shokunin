#!/usr/bin/env python3
"""ExecC1 independent check (not the frozen instrument): does the reward leg equal real pytest
rc, and do C11/C12 have the shapes the receipt claims?

Stages /app the same way the captured image does (agent graph + solve.sh), then runs the
captured tests/test_outputs.py under real pytest in a bubblewrap namespace and prints the pytest
rc + its own summary line. Also re-derives C11 rows/distinct and C12 variables with rdflib.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
G = Path(sys.argv[2]).resolve()
WORK = Path(sys.argv[3]).resolve()
CAP = LANE / "corpus/evidence/round97/graders/sparql-university"
BWRAP = "/usr/bin/bwrap"

REF_DATE = '"2025-08-16"^^xsd:date'
GRAD_FILTER = ('  FILTER( ?enrollDate <= "2025-08-16"^^xsd:date &&\n'
               '          (!BOUND(?gradDate) || ?gradDate > "2025-08-16"^^xsd:date) )\n')
EXTRA = ('AS ?countries)', 'AS ?countries) (COUNT(DISTINCT ?student) AS ?n)')


def box(binds, chdir, path, argv):
    cmd = [BWRAP, "--die-with-parent", "--unshare-all", "--clearenv", "--tmpfs", "/",
           "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
           "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
           "--symlink", "usr/bin", "/sbin", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
    for tree in (str(G), str((G / "bin/python").resolve().parent.parent.parent)):
        cmd += ["--ro-bind", tree, tree]
    for kind, src, dst in binds:
        cmd += [kind, src, dst]
    return cmd + ["--setenv", "PATH", path, "--setenv", "HOME", "/tmp", "--setenv", "LANG", "C.UTF-8",
                  "--chdir", chdir, *argv]


def run(binds, chdir, path, argv):
    return subprocess.run(box(binds, chdir, path, argv), capture_output=True, text=True, timeout=300)


def stage(name, mutate=None):
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    app.mkdir(parents=True)
    shutil.copyfile(CAP / "environment/university_graph.ttl", app / "university_graph.ttl")
    script = root / "solve.sh"
    shutil.copyfile(CAP / "solution/solve.sh", script)
    p = run([("--bind", str(app), "/app"), ("--ro-bind", str(script), "/solve.sh")], "/app",
            "/usr/bin", ["/usr/bin/bash", "/solve.sh"])
    assert p.returncode == 0, (name, p.stderr[-300:])
    target = app / "solution.sparql"
    assert target.is_file(), name
    if mutate:
        text = target.read_text()
        text = mutate(text)
        target.write_text(text)
    return app


def dup(text):
    head = "".join(x + "\n" for x in text.splitlines() if x.startswith("PREFIX "))
    body = "".join(x + "\n" for x in text.splitlines() if not x.startswith("PREFIX "))
    return head + "SELECT ?professorName ?countries WHERE {\n{\n" + body + "}\nUNION\n{\n" + body + "}\n}\n"


def no_grad(text):
    assert text.count(GRAD_FILTER) == 1
    return text.replace(GRAD_FILTER, '  FILTER( ?enrollDate <= "2025-08-16"^^xsd:date )\n')


def extra(text):
    assert text.count(EXTRA[0]) == 1
    return text.replace(*EXTRA)


def semicolon(text):
    assert text.count('separator=", "') == 1
    return text.replace('separator=", "', 'separator="; "')


tests = WORK / "tests"
if tests.exists():
    shutil.rmtree(tests)
tests.mkdir(parents=True)
for n in ("test_outputs.py", "university_graph_test.ttl"):
    shutil.copyfile(CAP / "tests" / n, tests / n)

cases = [("C01", None), ("C07", no_grad), ("C11", dup), ("C12", extra), ("C13", semicolon)]
print("case pytest_rc collected_summary")
for cid, mut in cases:
    app = stage(cid, mut)
    p = run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests")], "/app",
            str(G) + "/bin:/usr/bin",
            [str(G / "bin/python"), "-I", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "/tests/test_outputs.py"])
    summary = [x for x in p.stdout.splitlines() if ("passed" in x or "failed" in x or "error" in x)]
    print(cid, p.returncode, (summary[-1] if summary else p.stdout.strip()[-120:]))

# independent rdflib re-derivation of the C11/C12 shapes
shape = r"""
import sys
from rdflib import Graph
q = open(sys.argv[1], encoding="utf-8").read()
g = Graph(); g.parse(sys.argv[2], format="ttl")
res = g.query(q)
rows = [tuple(str(x) for x in r) for r in res]
print("vars=" + "+".join(str(v) for v in (res.vars or [])) + " rows=%d distinct=%d" % (len(rows), len(set(rows))))
"""
(WORK / "shape.py").write_text(shape)
for cid, mut in (("C11", dup), ("C12", extra)):
    app = WORK / cid / "app"
    p = run([("--ro-bind", str(app / "solution.sparql"), "/q.rq"),
             ("--ro-bind", str(tests / "university_graph_test.ttl"), "/g.ttl"),
             ("--ro-bind", str(WORK / "shape.py"), "/shape.py")], "/tmp", str(G) + "/bin:/usr/bin",
            [str(G / "bin/python"), "-I", "-B", "/shape.py", "/q.rq", "/g.ttl"])
    print("SHAPE", cid, p.stdout.strip(), "rc=%d" % p.returncode)
