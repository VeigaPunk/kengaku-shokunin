#!/usr/bin/env python3
"""Replay the captured `multi-source-data-merger` grader with its own three test functions
(round 96, R96-C1).

The task image (captured `environment/Dockerfile`) is python:3.11-slim with pandas 2.2.3 and
pyarrow 17.0.0 and the three source files copied to /data. The verifier (`tests/test.sh`) runs
only `/tests/test_outputs.py` under `uvx -p 3.13 -w pytest==8.4.1 -w pandas==2.3.3
-w pyarrow==22.0.0` and writes reward 1 iff pytest exits 0. This probe models both sides with two
pre-staged virtual environments passed by path:

    --env-venv     python 3.11.x, pandas 2.2.3, pyarrow 17.0.0   (the agent side: solve.sh, variants)
    --grader-venv  python 3.13.x, pandas 2.3.3, pyarrow 22.0.0   (the verifier side: the grader)

Both are checked inside the sandbox before any case runs (versions printed in the stamp block;
a mismatch is a setup defect, exit 2). Staging the venvs needs the network; the probe itself does
not: every case runs in a fresh bubblewrap namespace with --unshare-all (no network) and
--clearenv (no inherited host environment), tmpfs root, host /usr read-only, the venvs and the
uv-managed interpreters read-only at their own paths, the captured data read-only at /data, the
case /app read-write, the captured tests read-only at /tests. Host /etc is not bound.

Each case stages /app by running the captured `solution/solve.sh` unmodified (except `absent` and
`csv-as-parquet`), then applies the case's declared variant script with the env-side python.
The harness then imports the captured `test_outputs.py` unmodified with the grader-side python
and calls its three test functions in file order. Observed vector per case, in `leg_order`:

    exists     test_output_files_exist        P returned, F AssertionError,
    merged     test_merged_data_exact_values  E:<exception type name> anything else
    conflicts  test_conflict_report_values
    reward     1 iff all three returned, else 0 (tests/test.sh: reward 1 iff pytest rc 0)

No assertion is reimplemented. Every bind source except /usr and the venv/interpreter trees lives
under --work or the lane capture. The bwrap path is injectable so a sandbox-outage control runs.

Usage:  python3 plans/round96_merger_probe.py --lane <repo> --work <scratch dir>
            --env-venv <dir> --grader-venv <dir> [--bwrap PATH]
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

CAP = "corpus/evidence/round96/graders/multi-source-data-merger"
TABLE = "plans/round96-cases.json"
TOOL = "plans/round96_merger_probe.py"
MEMBER = "multi-source-data-merger"
HEADER = "# tb2 multi-source-data-merger grader probe (round 96)"
PINS = {
    "tests/test_outputs.py": "a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5",
    "tests/test.sh": "d5a00e64413c0e1ae452f38a1aa1a47c3ed7b4416bbfccae1a4c053025a336d1",
    "solution/solve.sh": "1b3d0d50e31930d042495d48f4c8e95f1a9c1a979c803b7f7cec651322537e1e",
    "environment/Dockerfile": "c95a40d3d35b473dc15ae1e8784ba7fb1725805c0583fc574dd2764325d75e4f",
    "environment/data/source_a/users.json": "75e51e2d3ab0bdba2269d7cf3757576f84f3ee2c13407d2db94289a5958a1778",
    "environment/data/source_b/users.csv": "8e87d16dc47d166edd8e56165955bad265b630d53d02762367c816affb5fa760",
    "environment/data/source_c/users.parquet": "23d1ea51c4170bdba53febb885a0f495e28de525a52667347b2932136b9a72fe",
}
SUBJECT_SHA = PINS["tests/test_outputs.py"]
DEFAULT_BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 300
ENV_WANT = ("3.11.", "2.2.3", "17.0.0")      # python prefix, pandas, pyarrow (Dockerfile)
GRADER_WANT = ("3.13.", "2.3.3", "22.0.0")   # tests/test.sh uvx pins
TESTS = ("test_output_files_exist", "test_merged_data_exact_values", "test_conflict_report_values")

PRE = "import json, pandas as pd\nM = '/app/merged_users.parquet'\nC = '/app/conflicts.json'\n"
RW = ("def rc():\n    return json.load(open(C))\n"
      "def wc(r):\n    json.dump(r, open(C, 'w'), indent=2)\n")
VARIANTS = {
    "solve": None,
    "absent": None,
    "parquet-only": "import os\nos.remove(C)\n",
    "under-report": RW + "r = rc()\nkeep = [c for c in r['conflicts'] if c['user_id'] == 101 and c['field'] == 'name']\n"
                         "assert len(keep) == 1\nwc({'total_conflicts': 1, 'conflicts': keep})\n",
    "wrong-selected": RW + "r = rc()\nn = 0\nfor c in r['conflicts']:\n"
                           "    if c['user_id'] == 101 and c['field'] == 'email':\n"
                           "        c['selected'] = c['values']['source_b']; n += 1\nassert n == 1\nwc(r)\n",
    "rows-unchecked": "df = pd.read_parquet(M)\nm = df['user_id'].isin([102, 103])\nassert m.sum() == 2\n"
                      "df.loc[m, 'name'] = 'WRONG'\ndf.loc[m, 'email'] = 'wrong@x.com'\n"
                      "df = df.drop(columns=['status'])\ndf.to_parquet(M, index=False)\n",
    "float-id": "df = pd.read_parquet(M)\ndf['user_id'] = df['user_id'].astype('float64')\ndf.to_parquet(M, index=False)\n",
    "string-id": "df = pd.read_parquet(M)\ndf['user_id'] = df['user_id'].astype(str)\ndf.to_parquet(M, index=False)\n",
    "datetime-date": "df = pd.read_parquet(M)\ndf['created_date'] = pd.to_datetime(df['created_date'])\n"
                     "df.to_parquet(M, index=False)\n",
    "slash-date": "df = pd.read_parquet(M)\ndf['created_date'] = df['created_date'].str.replace('-', '/')\n"
                  "df.to_parquet(M, index=False)\n",
    "total-mismatch": RW + "r = rc()\nassert len(r['conflicts']) == 3\nr['total_conflicts'] = 2\nwc(r)\n",
    "missing-source-a-key": RW + "r = rc()\nn = 0\nfor c in r['conflicts']:\n"
                                 "    if c['user_id'] == 101 and c['field'] == 'email':\n"
                                 "        del c['values']['source_a']; n += 1\nassert n == 1\nwc(r)\n",
    "wrong-priority": "df = pd.read_parquet(M)\nm = df['user_id'] == 101\nassert m.sum() == 1\n"
                      "df.loc[m, 'email'] = 'john@b.com'\ndf.loc[m, 'created_date'] = '2024-01-10'\n"
                      "df.to_parquet(M, index=False)\n",
    "string-userid-conflicts": RW + "r = rc()\nfor c in r['conflicts']:\n    c['user_id'] = str(c['user_id'])\nwc(r)\n",
    "duplicate-row": "df = pd.read_parquet(M)\ndf = pd.concat([df, df[df['user_id'] == 101]], ignore_index=True)\n"
                     "assert len(df) == 5\ndf.to_parquet(M, index=False)\n",
    "csv-as-parquet": None,
    "empty-conflicts": RW + "wc({'total_conflicts': 0, 'conflicts': []})\n",
}
CSV_AS_PARQUET = ("user_id,name,email,created_date,status\n101,John Doe,john@a.com,2024-01-15,active\n"
                  "102,Jane Smith,jane@a.com,2024-02-20,inactive\n103,Bob Wilson,bob@b.com,2024-03-01,active\n"
                  "104,Alice Brown,alice@c.com,2024-04-01,active\n")

HARNESS = r"""
import importlib.util, os, sys
os.chdir("/app")
sys.path[:0] = ["/tests", "/app"]
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
out.append("1" if all(o == "P" for o in out) else "0")
print("PAYLOAD " + ",".join(out))
""" % (TESTS,)

VERSIONS = ("import sys, pandas, pyarrow, numpy\n"
            "print('VERSIONS', sys.version.split()[0], pandas.__version__, pyarrow.__version__, numpy.__version__)\n")


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


def check_venv(box: Box, venv: Path, want: tuple[str, str, str], scratch: Path) -> str:
    probe = scratch / "versions.py"
    probe.write_text(VERSIONS, encoding="utf-8")
    proc = box.run([("--ro-bind", str(probe), "/versions.py")], "/tmp", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/versions.py"])
    line = next((x for x in proc.stdout.splitlines() if x.startswith("VERSIONS ")), "")
    parts = line.split()
    if len(parts) != 5 or not parts[1].startswith(want[0]) or parts[2] != want[1] or parts[3] != want[2]:
        raise SystemExit("SETUP venv %s versions %r rc=%d %s" % (venv, line, proc.returncode,
                                                                   proc.stderr.strip()[-200:]))
    return " ".join(parts[1:])


def stage(box: Box, case: dict, cap: Path, env_venv: Path, root: Path) -> Path:
    kind = case["app"]
    if kind not in VARIANTS:
        raise SystemExit("SETUP unknown app kind %s" % kind)
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    app.mkdir(parents=True)
    binds = [("--bind", str(app), "/app"), ("--ro-bind", str(cap / "environment" / "data"), "/data")]
    path = "%s/bin:/usr/bin" % env_venv
    if kind == "absent":
        return app
    if kind == "csv-as-parquet":
        (app / "merged_users.parquet").write_text(CSV_AS_PARQUET, encoding="utf-8")
        kind_solve_report = True
    else:
        kind_solve_report = False
    script = root / "solve.sh"
    shutil.copyfile(cap / "solution" / "solve.sh", script)
    proc = box.run(binds + [("--ro-bind", str(script), "/solve.sh")], "/app", path,
                   ["/usr/bin/bash", "/solve.sh"])
    if not (app / "conflicts.json").is_file() or not (app / "merged_users.parquet").is_file():
        raise SystemExit("SETUP solve.sh wrote no outputs rc=%d %s" % (proc.returncode, proc.stderr.strip()[-300:]))
    if kind_solve_report:
        (app / "merged_users.parquet").write_text(CSV_AS_PARQUET, encoding="utf-8")
        return app
    body = VARIANTS[kind]
    if body is None:
        return app
    variant = root / "variant.py"
    variant.write_text(PRE + body, encoding="utf-8")
    proc = box.run(binds + [("--ro-bind", str(variant), "/variant.py")], "/app", path,
                   [str(venv_python(env_venv)), "-I", "-B", "/variant.py"])
    if proc.returncode != 0:
        raise SystemExit("SETUP variant %s rc=%d %s" % (kind, proc.returncode, proc.stderr.strip()[-300:]))
    return app


def run_case(box: Box, app: Path, tests: Path, harness: Path, grader_venv: Path) -> str:
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                    ("--ro-bind", str(harness), "/harness.py")], "/app", "%s/bin:/usr/bin" % grader_venv,
                   [str(venv_python(grader_venv)), "-I", "-B", "/harness.py"])
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            return line.split(" ", 1)[1]
    return "NOPAYLOAD(rc=%d)" % proc.returncode


def interpreter_root(venv: Path) -> str:
    """The uv-managed interpreter store a venv's python resolves into (bound read-only whole,
    because the venv's link names the minor-version alias directory, itself a link)."""
    real = venv_python(venv).resolve()
    return str(real.parent.parent.parent)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--env-venv", required=True)
    parser.add_argument("--grader-venv", required=True)
    parser.add_argument("--bwrap", default=DEFAULT_BWRAP)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    env_venv = Path(args.env_venv).resolve()
    grader_venv = Path(args.grader_venv).resolve()
    for p in (work, env_venv, grader_venv):
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
    for v in (env_venv, grader_venv):
        if not venv_python(v).exists():
            print("DEFECT SETUP venv python absent %s" % v)
            return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    box = Box(args.bwrap, sorted({str(env_venv), str(grader_venv),
                                  interpreter_root(env_venv), interpreter_root(grader_venv)}))
    try:
        env_versions = check_venv(box, env_venv, ENV_WANT, work)
        grader_versions = check_venv(box, grader_venv, GRADER_WANT, work)
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    harness = work / "harness.py"
    harness.write_text(HARNESS, encoding="utf-8")
    tests = work / "tests"
    if tests.exists():
        shutil.rmtree(tests)
    tests.mkdir()
    shutil.copyfile(cap / "tests" / "test_outputs.py", tests / "test_outputs.py")
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("TEST_SH_SHA %s" % PINS["tests/test.sh"])
    print("SOLVE_SHA %s" % PINS["solution/solve.sh"])
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("ENV_SIDE python,pandas,pyarrow,numpy %s" % env_versions)
    print("GRADER_SIDE python,pandas,pyarrow,numpy %s" % grader_versions)
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("SANDBOX clearenv=1 unshare-all=1 etc-bound=0")
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    try:
        for case in table["cases"]:
            app = stage(box, case, cap, env_venv, work / "cases" / case["id"])
            observed = run_case(box, app, tests, harness, grader_venv)
            ok = observed == case["predicted"]
            mismatches += 0 if ok else 1
            print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
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
