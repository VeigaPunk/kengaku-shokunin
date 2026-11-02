#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `cancel-async-tasks` grader (round 61, C1).

Materializes the lane's committed capture
`corpus/evidence/round61/tb2-cancel-async-tasks/tests/test_outputs.py` (terminal-bench-2 @
2fd12b88, byte-identical to the round-52 population capture of the same path, itself
sha256-pinned in `corpus/evidence/round52/graders/SHA256SUMS`) as a byte-copy bound
read-only at /tests inside a bubblewrap sandbox, and runs its six test functions --
test_run_py_file_exists, test_tasks_run_concurrently, test_tasks_obey_max_concurrent,
test_tasks_cancel_below_max_concurrent, test_tasks_cancel_at_max_concurrent,
test_tasks_cancel_above_max_concurrent -- directly (no pytest runner; the capture imports
no pytest) against lane-built candidate task runners materialized at /app by probe-owned
builder code from frozen literal constants.

The task's reference `test.py` simulator is NOT in the capture population (the round-52
capture program took `tests/test_outputs.py` + `tests/test.sh` per task; the task's
`tests/test.py` was never captured and is not committed anywhere in this lane), so the
builder writes a lane-authored simulator, declared per case below. The grader is the
instrument under execution; the simulator surfaces are lane-authored inputs, exactly the
r58/r59 builder pattern (the openssl probe's builders wrote the certificate artifacts).

The graded class is new to the executed corpus: the decisive legs spawn the candidate as a
child process, deliver SIGINT to it mid-flight (`proc.send_signal(signal.SIGINT)`,
capture :93/:126/:162), and count cleanup-marker lines in the captured stdout -- a
signal-propagated cancellation-semantics class no executed grader touches (grep of all 184
round-52 captures: this is the only grader whose decisive legs send a signal to the
candidate process; the sixteen executed graders assert on files, tool output, timing or
numeric bands, never on signal-driven cleanup). The grader's own docstrings name the two
implementation traps the class prices: a ThreadPoolExecutor that does not propagate
cancellation ("This will fail e.g. if the agent tries to use threading.ThreadPoolExecutor
which doesn't propagate the cancellation signal to the tasks.", :77-79) and the
asyncio.gather queued-task trap ("asyncio.gather doesn't properly cancel existing tasks
if there are still tasks in the queue.", :143-145).

The capture's test functions invoke `["python", "test.py", ...]`; this host's interpreter
is python3, so the probe binds a probe-owned shim at /stub/python (exec /usr/bin/python3
"$@") and puts /stub first on PATH -- the same probe-owns-its-stub pattern as the r58
pytest stub and the r59 python shim. The reference `test.py` is copied to /app by the
task's own test.sh (`cp /tests/test.py /app/test.py`); the builder writes the lane
simulator directly at /app/test.py.

Leg rule (declared in plans/round-61-claims.md before the first capture run): a leg is P
iff its test function returns normally; F on AssertionError OR any other exception
escaping the function (subprocess.TimeoutExpired from the capture's own `timeout=5` /
`timeout=10` / `communicate(timeout=5)` is the class's dominant failure mode -- pytest
scores a raising test as not-pass either way, and the reward is binary). The grader is
deterministic given the candidate: every counted property (line counts, elapsed-vs-6s,
which process exits when) is a fixed function of the declared candidate behavior plus the
capture's fixed timing constants (tasks 3 s, SIGINT at 0.5 s, waits 5/10/5 s) -- zero U
marks, full commitment. Predictions are DERIVED at run time by predict_legs() from the
case definitions (the r59 lesson M-1 mechanism, generated never retyped); `--render-table`
prints the generated table and `--check-receipt` cross-checks a receipt's observed vectors
output-side only.

Run as:
  python3 plans/round61_c1_cancel_probe.py --lane . --work <scratch> \
      --receipt <path>                      # the scored battery (bare = battery, no write)
  python3 plans/round61_c1_cancel_probe.py --selftest --work <scratch>
  python3 plans/round61_c1_cancel_probe.py --render-table
  python3 plans/round61_c1_cancel_probe.py --check-receipt corpus/evidence/round61/cancel-async-probe.txt
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
GRADER_REL = "corpus/evidence/round61/tb2-cancel-async-tasks/tests/test_outputs.py"
GRADER_SHA256 = "d6f510b51fafc81b4e9b5cc95535aa13491c8753e0e4171db42c45f4de460ee7"
BWRAP = "/usr/bin/bwrap"

TEST_NAMES = (
    "test_run_py_file_exists",
    "test_tasks_run_concurrently",
    "test_tasks_obey_max_concurrent",
    "test_tasks_cancel_below_max_concurrent",
    "test_tasks_cancel_at_max_concurrent",
    "test_tasks_cancel_above_max_concurrent",
)

ENV = {"PATH": "/stub:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}

# ---------------------------------------------------------------------------
# The lane-authored candidate simulator (builder template). SPEC carries the
# case's declared implementation properties; every branch is generated from it.
# ---------------------------------------------------------------------------
SIM_TEMPLATE = r'''
import argparse, json, signal, sys, time

SPEC = json.loads({spec!r})

def log(msg):
    print(msg, flush=True)

def emit_cleanup(cancelled):
    pol = SPEC["cleanup"]
    if pol == "never":
        return
    if SPEC.get("late_cancel_cleanup") and cancelled:
        time.sleep(6.0)
    if pol == "double":
        log("Cleaned up.")
    log("Cleaned up.")

def run_task_body():
    log("Task finished.")
    emit_cleanup(False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-tasks", type=int)
    ap.add_argument("--max-concurrent", type=int)
    a = ap.parse_args()
    n, m = a.n_tasks, a.max_concurrent
    impl = SPEC["impl"]
    if impl == "sequential":
        if SPEC.get("ignore_sigint"):
            signal.signal(signal.SIGINT, signal.SIG_IGN)
        for i in range(n):
            log("Task started.")
            time.sleep(3.0)
            run_task_body()
    elif impl == "threads":
        import threading
        from concurrent.futures import ThreadPoolExecutor
        import concurrent.futures as cf
        workers = m if SPEC.get("enforce_max", True) else n
        def work(i):
            log("Task started.")
            time.sleep(3.0)
            run_task_body()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = []
            for i in range(n):
                if SPEC.get("premature_start"):
                    log("Task started.")
                futs.append(pool.submit(work, i))
            cf.wait(futs)
    else:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        sem = asyncio.Semaphore(m) if SPEC.get("enforce_max", True) else None
        async def task(i):
            acquired = False
            if sem is None:
                log("Task started.")
                acquired = True
            else:
                await sem.acquire()
                acquired = True
                log("Task started.")
            try:
                await asyncio.sleep(3.0)
                run_task_body()
            except asyncio.CancelledError:
                if acquired:
                    emit_cleanup(True)
                raise
            finally:
                if sem is not None and acquired:
                    sem.release()
        async def amain():
            tasks = []
            for i in range(n):
                if SPEC.get("premature_start"):
                    log("Task started.")
                tasks.append(loop.create_task(task(i)))
            def on_sigint():
                if SPEC.get("partial_cancel"):
                    tasks[0].cancel()
                    loop.stop()
                    return
                for t in tasks:
                    t.cancel()
            if not SPEC.get("ignore_sigint"):
                try:
                    loop.add_signal_handler(signal.SIGINT, on_sigint)
                except (NotImplementedError, ValueError):
                    pass
            else:
                signal.signal(signal.SIGINT, signal.SIG_IGN)
            try:
                await asyncio.gather(*tasks)
            except (KeyboardInterrupt, asyncio.CancelledError):
                pass
        try:
            loop.run_until_complete(amain())
        finally:
            loop.close()

main()
'''

BUILDER_TEMPLATE = r'''
import pathlib
SPEC = {spec!r}
RUN_PY = {run_py!r}
sim = pathlib.Path('/app/test.py')
sim.write_text({sim_src!r}, encoding='utf-8')
if RUN_PY:
    pathlib.Path('/app/run.py').write_text(
        '# candidate entry point (the task under grading)\n', encoding='utf-8')
'''

# ---------------------------------------------------------------------------
# Lane-written candidate runners (round-61 freeze): (name, defect class, cfg).
# Predictions are NOT stored here -- they are derived at run time by predict_legs()
# (the r59 lesson's mined fix: generated from the case definitions, never retyped).
# Declared properties per cfg:
#   impl                asyncio | threads | sequential   -- the candidate's engine
#   handler             install the SIGINT -> cancel-tasks loop handler (asyncio only)
#   enforce_max         honor --max-concurrent (semaphore / worker count)
#   cleanup             always | never | double          -- per-task cleanup marker policy
#   ignore_sigint       install SIG_IGN instead of any handler
#   late_cancel_cleanup emit the cleanup marker only after a 6 s delay on the cancel path
#   partial_cancel      the handler cancels only the first started task, then main returns
#   premature_start     print the started marker for every task at submit time
#   run_py              the builder writes /app/run.py (the capture's :10-12 leg)
# Leg order = TEST_NAMES.
CASES = [
    # the compliant candidate: SIGINT cancels every started task, each finally prints the
    # cleanup marker, queued tasks are cancelled before ever starting.
    ("compliant-signal-handler", "none -- the compliant asyncio candidate",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always", run_py=True)),
    # the capture's own docstring trap (:77-79): a ThreadPoolExecutor does not propagate
    # cancellation -- after SIGINT the workers run on uncancelled and the count assertions
    # see what looks like successful completion; the defect is visible only above max.
    ("threadpool-uncancelled", "ThreadPoolExecutor does not propagate cancellation (:77-79)",
     dict(impl="threads", enforce_max=True, cleanup="always", run_py=True)),
    # the default asyncio shape: no handler, so SIGINT raises KeyboardInterrupt out of the
    # loop; pending tasks die with the loop and no cleanup marker is ever printed.
    ("kbdint-no-handler", "no SIGINT handler: KeyboardInterrupt kills the loop, tasks die uncleaned",
     dict(impl="asyncio", handler=False, enforce_max=True, cleanup="always", run_py=True)),
    # no concurrency at all: two sequential 3 s tasks miss the 5 s window (:28) and the
    # first SIGINT leaves exactly one started marker.
    ("sequential-sync", "sequential execution: concurrency leg times out",
     dict(impl="sequential", cleanup="always", run_py=True)),
    # the tasks run but no cleanup marker exists: every count leg that prices it fails.
    ("cleanup-missing", "no cleanup handler: the cleanup-marker count is zero",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="never", run_py=True)),
    # a doubled cleanup marker: the strict equality on the count fails everywhere.
    ("cleanup-double", "cleanup marker printed twice per task",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="double", run_py=True)),
    # the started marker printed for queued tasks at submit: the above-max leg counts 3.
    ("started-premature", "started marker printed at submit time (accounting wart)",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always",
          premature_start=True, run_py=True)),
    # the handler cancels only the first started task and main returns without awaiting
    # the rest: the second task dies with the loop, uncleaned.
    ("partial-cancel", "handler cancels one task and abandons the other",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always",
          partial_cancel=True, run_py=True)),
    # SIG_IGN: the signal is swallowed, the candidate completes as if untouched -- the
    # cancel legs cannot distinguish this from success while the work fits the window
    # (a latent vacuity of the class, recorded in the knowledge entry).
    ("ignore-sigint", "SIG_IGN: the signal is swallowed, work completes anyway",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always",
          ignore_sigint=True, run_py=True)),
    # cleanup delivered, but six seconds late: the capture's communicate(timeout=5)
    # raises before the marker lands (:96/:129/:165).
    ("late-cancel-cleanup", "cleanup marker arrives after the 5 s communicate window",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always",
          late_cancel_cleanup=True, run_py=True)),
    # max-concurrent ignored: the obey leg finishes in ~3 s and fails its elapsed >= 6 s
    # bound (:59-63); the above-max leg sees three started markers.
    ("no-max-enforcement", "max-concurrent ignored (semaphore absent)",
     dict(impl="asyncio", handler=True, enforce_max=False, cleanup="always", run_py=True)),
    # /app/run.py absent: only the file-existence leg (:10-12) moves.
    ("no-run-py", "run.py absent (artifact-absence is a leg failure, not setup)",
     dict(impl="asyncio", handler=True, enforce_max=True, cleanup="always", run_py=False)),
]


def predict_legs(cfg):
    """Derive a case's six-leg prediction from its declared candidate properties.

    The static model of the captured grader (round-61 freeze; each predicate is
    grounded in the capture's own assertions):
      file   test_run_py_file_exists      -- passes iff /app/run.py exists (:10-12).
      concur test_tasks_run_concurrently  -- two 3 s tasks must both run, finish and
             clean inside the subprocess timeout of 5 s (:28, counts :31-33): any
             engine but `sequential` is parallel here (max=2 never throttles two
             tasks), sequential needs 6 s and times out; the cleanup-marker count
             is priced strictly (== 2), so never/double fail it.
      obey   test_tasks_obey_max_concurrent -- max=1 must serialize the two tasks so
             the elapsed >= 6 s bound holds (:59-63, timeout :56): true for
             `sequential` (trivially) and for an enforcing asyncio/threads engine;
             same strict cleanup pricing.
      below/at  the cancel legs (:71-103/:106-136, n=2): after SIGINT at 0.5 s the
             candidate must print started==2 AND cleaned==2 and exit inside the
             communicate(timeout=5) window (:96/:129). asyncio+handler does; a
             threads engine survives SIGINT with uncancelled workers and completes
             (which the counts cannot distinguish from cancellation -- the class's
             own latent vacuity, noted in the knowledge entry); SIG_IGN behaves the
             same here; a late cleanup marker misses the 5 s window; sequential
             prints only one started marker; the no-handler asyncio shape dies with
             a zero cleanup count.
      above  test_tasks_cancel_above_max_concurrent (:139-170, n=3, max=2): exactly
             two started markers and two cleanup markers must appear -- a premature
             started marker (3), an unenforced or SIG_IGN-swallowed or uncancelled
             third task (timeout), a partial cancel (one cleanup) all break it; only
             the compliant cancel-and-deny-queue shape passes.
    """
    impl = cfg["impl"]
    handler = bool(cfg.get("handler"))
    enforce = bool(cfg.get("enforce_max", True))
    cleanup = cfg.get("cleanup", "always")
    ignore = bool(cfg.get("ignore_sigint"))
    late = bool(cfg.get("late_cancel_cleanup"))
    premature = bool(cfg.get("premature_start"))
    partial = bool(cfg.get("partial_cancel"))
    run_py = bool(cfg.get("run_py", True))
    cleanup_ok = cleanup == "always"

    file_leg = run_py
    concur = (impl in ("asyncio", "threads")) and cleanup_ok
    obey = ((impl == "sequential") or enforce) and cleanup_ok

    if impl == "sequential":
        below = at = False          # exactly one started marker (:93)
    elif impl == "threads":
        below = at = cleanup_ok     # uncancelled workers complete inside the window
    elif ignore:
        below = at = cleanup_ok     # completes as if untouched
    elif late:
        below = at = False          # marker lands after the 5 s window
    else:                            # asyncio + handler
        below = at = cleanup_ok
    if partial:
        below = at = False          # one cleanup marker, not two

    above = (impl == "asyncio" and handler and enforce and cleanup_ok
             and not late and not premature and not partial and not ignore)
    return tuple("P" if ok else "F"
                 for ok in (file_leg, concur, obey, below, at, above))


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


def sim_source(cfg):
    return SIM_TEMPLATE.format(spec=json.dumps(cfg, sort_keys=True))


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
        builder = BUILDER_TEMPLATE.format(spec=json.dumps(cfg, sort_keys=True),
                                          run_py=bool(cfg.get("run_py", True)),
                                          sim_src=sim_source(cfg))
        legs, rc, out = run_in_sandbox(tests_dir, casedir / "app", stub_dir,
                                       driver_prog(builder))
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
    lines.append(f"PREDICATE R61-C1 {'pass' if ok else 'fail'}")
    return (0 if ok else 1)


# --- selftest: the same bwrap pipeline against toy graders and toy sims only ---
TOY_SIM_COMPLIANT = r'''
import asyncio, signal, sys, time
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
async def main():
    print("Toy started.", flush=True)
    try:
        await asyncio.sleep(2.0)
    except asyncio.CancelledError:
        print("Toy cleaned up.", flush=True)
        raise
def on_sigint():
    for t in asyncio.all_tasks(loop):
        if t is not asyncio.current_task():
            t.cancel()
loop.add_signal_handler(signal.SIGINT, on_sigint)
try:
    loop.run_until_complete(main())
except (KeyboardInterrupt, asyncio.CancelledError):
    pass
'''

TOY_SIM_IGNORES = r'''
import signal, time
signal.signal(signal.SIGINT, signal.SIG_IGN)
print("Toy started.", flush=True)
time.sleep(2.0)
print("Toy cleaned up.", flush=True)
'''

TOY_GRADER = (
    "import subprocess, signal, time\n"
    "\n"
    "\n"
    "def test_sigint_cleanup():\n"
    "    proc = subprocess.Popen(['python', 'toy_sim.py'],\n"
    "                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n"
    "    time.sleep(0.4)\n"
    "    proc.send_signal(signal.SIGINT)\n"
    "    stdout, _ = proc.communicate(timeout=5)\n"
    "    assert stdout.decode().count('Toy cleaned up.') == 1\n"
    "\n"
    "\n"
    "def test_sigint_ignored():\n"
    "    proc = subprocess.Popen(['python', 'toy_sim_ignores.py'],\n"
    "                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n"
    "    time.sleep(0.4)\n"
    "    proc.send_signal(signal.SIGINT)\n"
    "    stdout, _ = proc.communicate(timeout=5)\n"
    "    assert stdout.decode().count('Toy cleaned up.') == 0, 'ignored SIGINT still cleaned'\n"
)


def run_selftest(work, lines):
    """Run the same bwrap pipeline against a toy grader and toy sims only."""
    tests_dir = work / "toytests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "toy_grader.py").write_text(TOY_GRADER, encoding="utf-8")
    stub_dir = make_stub_dir(work / "toystub")
    prog = (
        "import sys\n"
        "sys.path.insert(0, '/tests')\n"
        "import json, pathlib\n"
        "pathlib.Path('/app/toy_sim.py').write_text(" + repr(TOY_SIM_COMPLIANT) + ")\n"
        "pathlib.Path('/app/toy_sim_ignores.py').write_text(" + repr(TOY_SIM_IGNORES) + ")\n"
        "import toy_grader as t\n"
        "res = {}\n"
        "for name in ('test_sigint_cleanup', 'test_sigint_ignored'):\n"
        "    try:\n"
        "        getattr(t, name)()\n"
        "        res[name] = 'P'\n"
        "    except Exception:\n"
        "        res[name] = 'F'\n"
        "print('LEGS ' + json.dumps(res))\n"
    )
    casedir = work / "toy" / "case"
    (casedir / "app").mkdir(parents=True)
    legs, rc, out = run_in_sandbox(tests_dir, casedir / "app", stub_dir, prog)
    want = ("P", "F")
    names = ("test_sigint_cleanup", "test_sigint_ignored")
    got = tuple(legs.get(n, "NONE") for n in names) if legs else ("NONE", "NONE")
    ok = got == want
    lines.append(f"SELFTEST toy-sigint got={'/'.join(got)} want={'/'.join(want)} "
                 f"{'ok' if ok else 'FAIL'}")
    lines.append(f"SELFTEST {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def render_table(lines):
    """Print the prediction table GENERATED from the case definitions (never retyped)."""
    lines.append("| case | defect class exercised | file | concur | obey | below | at | above |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for name, klass, cfg in CASES:
        pred = "/".join(predict_legs(cfg))
        lines.append(f"| {name} | {klass} | {pred.replace('/', ' | ')} |")
    lines.append(f"TABLE cases={len(CASES)} legs={len(CASES) * len(TEST_NAMES)} "
                 f"predicted_u=0 source=CASES+predict_legs")


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
    ap.add_argument("--check-receipt", default=None,
                    help="compare the derived table against a receipt's observed vectors")
    a = ap.parse_args(argv)
    lines = []
    rev = subprocess.run(["git", "-C", str(a.lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    lines.append(f"REV {rev}")
    if pathlib.Path(BWRAP).exists() is False:
        lines.append(f"SETUP bwrap absent at {BWRAP}")
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return 2
    if a.render_table:
        render_table(lines)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return 0
    if a.check_receipt:
        rc = check_receipt(pathlib.Path(a.lane), pathlib.Path(a.check_receipt), lines)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        return rc
    with tempfile.TemporaryDirectory(prefix="k61-c1-", dir=a.work) as work:
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
