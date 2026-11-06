#!/usr/bin/env python3
"""Replay the captured `bn-fit-modify` grader with its own nine test functions and its own pytest
reward rule (round 99, R99-C1).

The task image (captured `Dockerfile`) is ubuntu:24.04 + r-base; the agent's artefacts are
/app/learned_dag.csv, /app/intervened_dag.csv and /app/final_bn_sample.csv. The verifier (`test.sh`)
runs `/tests/test_outputs.py` under `uvx -p 3.13 -w pytest==8.4.1 -w pandas==2.3.2 -w scipy==1.16.1`
and writes reward 1 iff pytest exits 0. This probe models the verifier side with one pre-staged
virtual environment passed by path:

    --grader-venv  python 3.13.x, pandas 2.3.2, scipy 1.16.1, pytest 8.4.1, numpy 2.5.4

numpy is not pinned by test.sh (it arrives with pandas/scipy); the probe's case builder draws its
seeded samples with it, so the probe pins it (BUILDER_SIDE) and refuses another version (exit 2).

Positive control: the maintainer's solution is an R script (bnlearn `hc`, `bn.fit`, `custom.fit`,
unseeded `rbn`). It was run once at P0 (2026-11-06, conda-forge r-base 4.4.3 + r-bnlearn 5.2.1,
offline, solve.sh's CRAN install line not run) and its three output files are committed with
SHA256SUMS under `corpus/evidence/round99/bn-fit-modify-solution/`; the probe stages those bytes.
Its printed fit equals the grader's hard-coded constants (`run.log`).

Every sandboxed step runs in a fresh bubblewrap namespace with --unshare-all (no network) and
--clearenv, tmpfs root, host /usr read-only, the venv and its interpreter read-only, the case /app
read-write, the captured test file read-only at /tests and the fixture read-only at /fixture. The
sandbox binary is fixed at /usr/bin/bwrap.

Each case's /app is built inside the sandbox by BUILDER from the fixture and the captured dataset
(seeded numpy draws, fixed seeds per case). The grader is then run ONCE per case as real pytest
(`pytest.main`) over the unmodified captured file; an observe-only plugin records each test's
outcome and `call.excinfo.typename`:

    P passed, F AssertionError, E:<exception type name> any other failure; reward 1 iff pytest rc 0

No assertion is reimplemented. Output order is the case table order.

Usage:  python3 plans/round99_bnfit_probe.py --lane <repo> --work <scratch dir> --grader-venv <dir> [--jobs N]
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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CAP = "corpus/evidence/round99/tb2-bn-fit-modify"
FIX = "corpus/evidence/round99/bn-fit-modify-solution"
TABLE = "plans/round99-cases.json"
TOOL = "plans/round99_bnfit_probe.py"
MEMBER = "bn-fit-modify"
HEADER = "# tb2 bn-fit-modify grader probe (round 99)"
PINS = {
    "test_outputs.py": "364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b",
    "test.sh": "ea2adeb779621e9625d1f80a17f9d19b6ecec017b8ad8974b668a4a0fbdeb4c3",
    "solve.sh": "813eb810cf041466468703ef14fdb06ada533b9accddf774eecc7a7191d5cb79",
    "Dockerfile": "8b0b1056e9c66c01a14a3d79332cc425498f2926b6deda13d200591ee5e5e6cc",
    "task.toml": "6493f7162da424a4fd95da721bd3fd1ce7e5dd26e792132cb9c46db536b67090",
    "instruction.md": "5f5207ce23c375270c26719fb66d89843bc88cf1d40671ed87c6b7bab4d394e5",
    "README.md": "647d14a74c316f554dbd6eb70dd5da79b347eb8395fb5e92bf5ad8319faf7919",
    "bn_sample_10k.csv": "7d4c27aca2f7443500f993bf0cc31fc7c7e4ef45bb5370ba890848ee1ef3cb04",
}
FIX_PINS = {
    "learned_dag.csv": "1efe8fe9a8c379014c5f898536f5cff3cdff2c3236d2b44e1ab90e761c85e2f4",
    "intervened_dag.csv": "458d8ecd0bc5dd7aca59acb78a11de228d51a09025a6497d3c1ec59a5e6296bd",
    "final_bn_sample.csv": "982a7441d4469c4b09eb0c9a27d5ca62f7fb38bdee6542b56a767e0c4b26ab66",
    "modify_bn.R": "c0a54e0b880c6810ea819e85dc2aa843a4d53e269146a600f3632e2ec86dbccf",
}
SUBJECT_SHA = PINS["test_outputs.py"]
BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 1800
GRADER_WANT = ("3.13", "2.3.2", "1.16.1", "8.4.1")   # test.sh uvx pins: -p 3.13, pandas, scipy, pytest
BUILDER_WANT = "2.5.4"                              # numpy, unpinned by test.sh; pinned for the builder
TESTS = ("test_bn_sample_exists", "test_learned_dag_structure_exists",
         "test_learned_dag_structure_csv_col_names", "test_learned_dag_structure",
         "test_intervened_dag_structure_exists", "test_intervened_dag_structure_csv_col_names",
         "test_intervened__data_structure", "test_sampled_csv_col_names", "test_sampled_data")
KINDS = ("solution", "absent", "marginal-only", "no-intervention", "rownames-column", "header-to-from",
         "dup-edges-extra", "reversed-edge", "idag-not-dropped", "rows-9999", "ks-shift-small",
         "ks-shift-large", "quantile-grid")

BUILDER = r"""
import shutil, sys
import numpy as np
import pandas as pd
from scipy.stats import norm
kind = sys.argv[1]
fx = "/fixture/"
TRUE_MEAN = -12.2965135 + 0.5495886 * 50.47989
TRUE_STD = ((0.5495886 ** 2) * 10.68515 ** 2 + 14.0916 ** 2) ** 0.5
def copy(*names):
    for n in names:
        shutil.copyfile(fx + n, "/app/" + n)
def write_sample(df):
    df[["U", "Y", "R", "D", "M"]].to_csv("/app/final_bn_sample.csv", index=False)
sol = pd.read_csv(fx + "final_bn_sample.csv")
if kind == "absent":
    pass
elif kind == "solution":
    copy("learned_dag.csv", "intervened_dag.csv", "final_bn_sample.csv")
elif kind == "marginal-only":
    copy("learned_dag.csv", "intervened_dag.csv")
    rng = np.random.default_rng(3)
    df = pd.DataFrame({c: np.zeros(10000) for c in "UYRDM"})
    df["D"] = rng.normal(TRUE_MEAN, TRUE_STD, 10000)
    write_sample(df)
elif kind == "no-intervention":
    copy("learned_dag.csv", "intervened_dag.csv")
    data = pd.read_csv("/app/bn_sample_10k.csv")
    def ols(y, xs):
        X = np.column_stack([np.ones(len(data))] + [data[x].to_numpy() for x in xs])
        beta, *_ = np.linalg.lstsq(X, data[y].to_numpy(), rcond=None)
        resid = data[y].to_numpy() - X @ beta
        return beta, float(np.sqrt(resid @ resid / (len(data) - X.shape[1])))
    rng = np.random.default_rng(4)
    n = 10000
    out = {}
    out["U"] = rng.normal(data["U"].mean(), data["U"].std(ddof=1), n)
    for node, parents in (("Y", ["U"]), ("R", ["U"]), ("D", ["U", "Y"]), ("M", ["U", "R"])):
        beta, sd = ols(node, parents)
        mu = beta[0] + sum(b * out[p] for b, p in zip(beta[1:], parents))
        out[node] = mu + rng.normal(0.0, sd, n)
    write_sample(pd.DataFrame(out))
elif kind == "rownames-column":
    copy("learned_dag.csv", "intervened_dag.csv")
    sol.to_csv("/app/final_bn_sample.csv", index=True)
elif kind == "header-to-from":
    copy("final_bn_sample.csv")
    for n in ("learned_dag.csv", "intervened_dag.csv"):
        d = pd.read_csv(fx + n)
        d[["to", "from"]].to_csv("/app/" + n, index=False)
elif kind == "dup-edges-extra":
    copy("intervened_dag.csv", "final_bn_sample.csv")
    d = pd.read_csv(fx + "learned_dag.csv")
    d = pd.concat([d, d], ignore_index=True)
    d["weight"] = 1.0
    d.to_csv("/app/learned_dag.csv", index=False)
elif kind == "reversed-edge":
    copy("intervened_dag.csv", "final_bn_sample.csv")
    d = pd.read_csv(fx + "learned_dag.csv")
    hit = (d["from"] == "R") & (d["to"] == "M")
    assert int(hit.sum()) == 1
    d.loc[hit, ["from", "to"]] = ["M", "R"]
    d.to_csv("/app/learned_dag.csv", index=False)
elif kind == "idag-not-dropped":
    copy("learned_dag.csv", "final_bn_sample.csv")
    shutil.copyfile(fx + "learned_dag.csv", "/app/intervened_dag.csv")
elif kind == "rows-9999":
    copy("learned_dag.csv", "intervened_dag.csv")
    write_sample(sol.iloc[:-1])
elif kind in ("ks-shift-small", "ks-shift-large"):
    # deterministic: a normal quantile grid shifted by k sd, so the KS statistic is Phi(k)-1/2 (+1/2n)
    # and the verdict carries no sampling noise (dry run 1: a seeded random draw at 0.03 sd failed;
    # 49 of 200 seeds fail at that shift)
    copy("learned_dag.csv", "intervened_dag.csv")
    k = 0.045 if kind == "ks-shift-small" else 0.050
    df = sol.copy()
    df["D"] = TRUE_MEAN + TRUE_STD * (norm.ppf((np.arange(10000) + 0.5) / 10000) + k)
    write_sample(df)
elif kind == "quantile-grid":
    copy("learned_dag.csv", "intervened_dag.csv")
    df = sol.copy()
    df["D"] = norm.ppf((np.arange(10000) + 0.5) / 10000, TRUE_MEAN, TRUE_STD)
    write_sample(df)
else:
    raise SystemExit("unknown kind " + kind)
print("BUILT", kind)
"""

VERSIONS = ("import sys, pandas, scipy, pytest, numpy\n"
            "print('VERSIONS', sys.version.split()[0], pandas.__version__, scipy.__version__, "
            "pytest.__version__, numpy.__version__)\n")
RUNNER = r"""
import sys
import pytest
verdict = {}
class Observe:
    # observes only: records each test's outcome and exception type name
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()
        if rep.when == "call" or (rep.when != "call" and rep.failed):
            if rep.passed:
                verdict[item.name] = "P"
            elif call.excinfo is not None:
                name = call.excinfo.typename
                verdict[item.name] = "F" if name == "AssertionError" else "E:" + name
            else:
                verdict[item.name] = "E:" + rep.outcome
rc = int(pytest.main(["-q", "-p", "no:cacheprovider", "/tests/test_outputs.py"], plugins=[Observe()]))
for name in %r:
    print("VERDICT", name, verdict.get(name, "MISSING"))
print("RC", rc)
sys.exit(rc)
""" % (TESTS,)


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

    def __init__(self, ro_trees: list[str]):
        self.ro_trees = ro_trees

    def cmd(self, binds: list[tuple[str, str, str]], chdir: str, path: str, argv: list[str]) -> list[str]:
        cmd = [BWRAP, "--die-with-parent", "--unshare-all", "--clearenv",
               "--tmpfs", "/", "--ro-bind", "/usr", "/usr",
               "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
               "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
               "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        for tree in self.ro_trees:
            cmd += ["--ro-bind", tree, tree]
        for kind, src, dst in binds:
            cmd += [kind, src, dst]
        return cmd + ["--setenv", "PATH", path, "--setenv", "HOME", "/tmp",
                      "--setenv", "LANG", "C.UTF-8", "--setenv", "OMP_NUM_THREADS", "1",
                      "--chdir", chdir, *argv]

    def run(self, binds, chdir, path, argv) -> subprocess.CompletedProcess:
        return subprocess.run(self.cmd(binds, chdir, path, argv), capture_output=True, text=True,
                              timeout=CASE_TIMEOUT)


def venv_python(venv: Path) -> Path:
    return venv / "bin" / "python"


def interpreter_root(venv: Path) -> str:
    real = venv_python(venv).resolve()
    return str(real.parent.parent.parent)


def check_venv(box: Box, venv: Path, scratch: Path) -> tuple[str, str]:
    probe = scratch / "versions.py"
    probe.write_text(VERSIONS, encoding="utf-8")
    proc = box.run([("--ro-bind", str(probe), "/versions.py")], "/tmp", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/versions.py"])
    line = next((x for x in proc.stdout.splitlines() if x.startswith("VERSIONS ")), "")
    parts = line.split()
    if (len(parts) != 6 or ".".join(parts[1].split(".")[:2]) != GRADER_WANT[0]
            or tuple(parts[2:5]) != GRADER_WANT[1:] or parts[5] != BUILDER_WANT):
        raise SystemExit("SETUP venv %s versions %r rc=%d %s" % (venv, line, proc.returncode,
                                                                   proc.stderr.strip()[-200:]))
    return "%s %s %s %s" % GRADER_WANT, parts[1]


def stage(box: Box, case: dict, root: Path, venv: Path, fixture: Path, dataset: Path, builder: Path) -> Path:
    kind = case["app"]
    if kind not in KINDS:
        raise SystemExit("SETUP unknown app kind %s" % kind)
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    app.mkdir(parents=True)
    shutil.copyfile(dataset, app / "bn_sample_10k.csv")   # the image's WORKDIR content
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(fixture), "/fixture"),
                    ("--ro-bind", str(builder), "/builder.py")], "/app", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/builder.py", kind])
    if proc.returncode != 0 or ("BUILT %s" % kind) not in proc.stdout:
        raise SystemExit("SETUP builder %s rc=%d %s" % (kind, proc.returncode, proc.stderr.strip()[-300:]))
    return app


def run_case(box: Box, app: Path, tests: Path, venv: Path, runner: Path) -> str:
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                    ("--ro-bind", str(runner), "/runner.py")], "/app",
                   "%s/bin:/usr/bin" % venv, [str(venv_python(venv)), "-I", "-B", "/runner.py"])
    verdict: dict[str, str] = {}
    rc = None
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0] == "VERDICT":
            verdict[parts[1]] = parts[2]
        elif len(parts) == 2 and parts[0] == "RC" and parts[1].lstrip("-").isdigit():
            rc = int(parts[1])
    out = [verdict.get(name, "MISSING") for name in TESTS]
    out.append("1" if rc == 0 and proc.returncode == 0 else "0" if rc is not None else "NORC(%d)" % proc.returncode)
    return ",".join(out)


def detail(app: Path) -> str:
    parts = []
    for name in ("learned_dag.csv", "intervened_dag.csv", "final_bn_sample.csv"):
        p = app / name
        parts.append("%s=%s" % (name.split("_")[0], sha(p.read_bytes())[:16] if p.is_file() else "absent"))
    return " ".join(parts)


def one(box, case, work, venv, fixture, dataset, tests, builder, runner) -> tuple[str, str]:
    root = work / "cases" / case["id"]
    try:
        app = stage(box, case, root, venv, fixture, dataset, builder)
        observed = run_case(box, app, tests, venv, runner)
        info = detail(app)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return observed, info


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--grader-venv", required=True)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    grader_venv = Path(args.grader_venv).resolve()
    for p in (work, grader_venv):
        if p == lane or lane in p.parents:
            print("DEFECT SETUP path inside the lane %s" % p)
            return 2
    if args.jobs < 1:
        print("DEFECT SETUP --jobs must be >= 1")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    cap = lane / CAP
    fixture = lane / FIX
    if not Path(BWRAP).is_file() or not os.access(BWRAP, os.X_OK):
        print("DEFECT SETUP sandbox-unavailable %s" % BWRAP)
        return 2
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    if not userns.isdigit() or int(userns) <= 0:
        print("DEFECT SETUP user namespaces unavailable (%s)" % userns)
        return 2
    for base, pins in ((cap, PINS), (fixture, FIX_PINS)):
        for rel, want in pins.items():
            p = base / rel
            if not p.is_file() or sha(p.read_bytes()) != want:
                print("DEFECT SETUP capture sha mismatch %s/%s" % (base.name, rel))
                return 2
    if not venv_python(grader_venv).exists():
        print("DEFECT SETUP venv python absent %s" % grader_venv)
        return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    box = Box(sorted({str(grader_venv), interpreter_root(grader_venv)}))
    try:
        pinned, unpinned = check_venv(box, grader_venv, work)
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    builder = work / "builder.py"
    builder.write_text(BUILDER, encoding="utf-8")
    runner = work / "runner.py"
    runner.write_text(RUNNER, encoding="utf-8")
    tests = work / "tests"
    if tests.exists():
        shutil.rmtree(tests)
    tests.mkdir()
    shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
    fix = work / "fixture"
    if fix.exists():
        shutil.rmtree(fix)
    fix.mkdir()
    for name in ("learned_dag.csv", "intervened_dag.csv", "final_bn_sample.csv"):
        shutil.copyfile(fixture / name, fix / name)
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("TEST_SH_SHA %s" % PINS["test.sh"])
    print("SOLVE_SHA %s" % PINS["solve.sh"])
    print("DATASET_SHA %s" % PINS["bn_sample_10k.csv"])
    print("FIXTURE_SAMPLE_SHA %s" % FIX_PINS["final_bn_sample.csv"])
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("GRADER_SIDE python,pandas,scipy,pytest %s" % pinned)
    print("BUILDER_SIDE numpy %s" % BUILDER_WANT)
    print("GRADER_UNPINNED python %s" % unpinned)
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("SANDBOX clearenv=1 unshare-all=1 etc-bound=0 bwrap=%s" % BWRAP)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    sys.stdout.flush()
    cases = table["cases"]
    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(one, box, c, work, grader_venv, fix, cap / "bn_sample_10k.csv",
                                   tests, builder, runner) for c in cases]
            results = [f.result() for f in futures]
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    finally:
        shutil.rmtree(work / "cases", ignore_errors=True)
        shutil.rmtree(fix, ignore_errors=True)
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case, (observed, info) in zip(cases, results):
        ok = observed == case["predicted"]
        mismatches += 0 if ok else 1
        print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
        print("DETAIL %s %s %s" % (case["id"], info, case["app"]))
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
