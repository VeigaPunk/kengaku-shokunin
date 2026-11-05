#!/usr/bin/env python3
"""R93-C2 counter — the freeze-integrity gate, judged through its public CLI only.

The gate under test is `plans/round93_freeze_integrity.py` read at --rev (or a file named
by --tool-file, which is how the forgery controls are run through this same path). The
counter never trusts the gate's own battery line alone; it scores four legs:

  W1 history   on the lane's real round-92 history (freeze B2 f0018773, measured tip
               1df76536; closure round-92 spot-check §2 C2/C3): paths mode over the four
               round-92 instruments must print broken=3 intact=1 with exactly
               round92_c1_replay.py intact, rc 1
  W2 fixtures  five counter-owned fixture repos (not the gate's battery), each through
               the CLI: intact rc 0; edited rc 1; edit-then-revert rc 1; lying table rc 1;
               unrelated edit rc 0
  W3 battery   the gate's in-path line `SELFTEST cases=10 ok=10` is present
  W4 self      claims mode on this round's own table: --claims plans/round-93-claims.md,
               --freeze = the commit that added that file (found by git log at --rev),
               --rev REV; must print broken=0 and instruments>=6, rc 0

PREDICATE R93-C2 pass iff W1..W4 all pass. Exit 0 pass, 1 fail, 2 could-not-evaluate.
Usage:  python3 plans/round93_c2_counter.py --lane . --rev REV --work DIR [--tool-file PATH]
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = "plans/round93_freeze_integrity.py"
CLAIMS = "plans/round-93-claims.md"
R92_FREEZE = "f0018773f507f363854123856990f8ff8a87eb8c"
R92_TIP = "1df7653633bd4c5a5f373d139f9f1ed02e0f9c07"
R92_PATHS = ["plans/round92_c1_replay.py", "plans/round92_c2_conformance.py",
             "plans/round92_burndown.py", "plans/round91_counter_pin.py"]
R92_INTACT = {"plans/round92_c1_replay.py"}
MIN_SELF_INSTRUMENTS = 6


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=120)


def run_tool(tool: Path, lane: Path, work: Path, extra: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run([sys.executable, "-I", "-B", str(tool), "--lane", str(lane),
                               "--work", str(work), *extra], capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as error:
        return -1, f"tool-run-error {error}"
    return proc.returncode, proc.stdout


def summary(out: str) -> tuple[int, int, int] | None:
    m = re.search(r"^FREEZE-INTEGRITY instruments=(\d+) intact=(\d+) broken=(\d+)$", out, re.M)
    return tuple(int(x) for x in m.groups()) if m else None


def fx_commit(d: Path, msg: str) -> str:
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if Path(top).resolve() != d.resolve():
        raise SystemExit(f"fixture toplevel {top} != {d}")
    base = ["git", "-C", str(d), "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
    subprocess.run(base + ["add", "-A"], check=True, capture_output=True)
    subprocess.run(base + ["commit", "-q", "--allow-empty", "-m", msg], check=True, capture_output=True)
    return git(d, "rev-parse", "HEAD").stdout.decode().strip()


def fixture(root: Path, name: str, mutate) -> tuple[Path, str, str]:
    import hashlib
    d = root / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True, capture_output=True)
    body = b"def count():\n    return 3\n"
    (d / "probe.py").write_bytes(body)
    (d / "notes.md").write_text("notes\n")
    digest = "f" * 64 if name == "w2-lying-table" else hashlib.sha256(body).hexdigest()
    (d / "claims.md").write_text(f"# claims\n\n```frozen-instruments\n{digest}  probe.py\n```\n")
    f = fx_commit(d, "freeze")
    mutate(d)
    t = fx_commit(d, "after")
    return d, f, t


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool-file")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {a.rev}")
        print("PREDICATE R93-C2 could-not-evaluate")
        return 2
    rev = proc.stdout.decode().strip()
    tool = work / "gate-under-test.py"
    if a.tool_file:
        shutil.copyfile(a.tool_file, tool)
        print(f"TOOL from-file {a.tool_file}")
    else:
        b = git(lane, "show", f"{rev}:{TOOL}")
        if b.returncode != 0:
            print(f"TOOL absent at {rev[:12]}")
            print("W1 fail tool-absent")
            print("W2 fail tool-absent")
            print("W3 fail tool-absent")
            print("W4 fail tool-absent")
            print("PREDICATE R93-C2 fail")
            return 1
        tool.write_bytes(b.stdout)
        print(f"TOOL {TOOL}@{rev[:12]}")

    legs = {}
    # W1 history
    rc, out = run_tool(tool, lane, work / "w1", ["--freeze", R92_FREEZE, "--rev", R92_TIP, "--paths", *R92_PATHS])
    s = summary(out)
    intact = {m.group(1) for m in re.finditer(r"^INSTRUMENT (\S+) .* verdict=intact$", out, re.M)}
    legs["W1"] = rc == 1 and s == (4, 1, 3) and intact == R92_INTACT
    print(f"W1 {'pass' if legs['W1'] else 'fail'} rc={rc} summary={s} intact={sorted(intact)}")

    # W2 counter-owned fixtures
    fx_root = work / "w2-fixtures"
    def edit(d):
        (d / "probe.py").write_bytes(b"def count():\n    return 4\n")
    def edit_revert(d):
        edit(d)
        fx_commit(d, "edit")
        (d / "probe.py").write_bytes(b"def count():\n    return 3\n")
    def unrelated(d):
        (d / "notes.md").write_text("more notes\n")
    specs = [("w2-intact", lambda d: None, 0, (1, 1, 0)),
             ("w2-edited", edit, 1, (1, 0, 1)),
             ("w2-edit-revert", edit_revert, 1, (1, 0, 1)),
             ("w2-lying-table", lambda d: None, 1, (1, 0, 1)),
             ("w2-unrelated", unrelated, 0, (1, 1, 0))]
    w2 = True
    for name, mut, want_rc, want_s in specs:
        d, f, t = fixture(fx_root, name, mut)
        rc, out = run_tool(tool, d, work / name, ["--freeze", f, "--rev", t, "--claims", "claims.md"])
        ok = rc == want_rc and summary(out) == want_s
        w2 = w2 and ok
        print(f"W2 {name} {'ok' if ok else 'RED'} rc={rc} want_rc={want_rc} summary={summary(out)} want={want_s}")
    shutil.rmtree(fx_root, ignore_errors=True)
    legs["W2"] = w2
    print(f"W2 {'pass' if w2 else 'fail'}")

    # W3 battery line (from the W1 run's output; the battery runs in every invocation)
    legs["W3"] = re.search(r"^SELFTEST cases=10 ok=10$", out, re.M) is not None and \
        re.search(r"^SELFTEST cases=10 ok=10$", run_tool(tool, lane, work / "w3",
                  ["--freeze", R92_FREEZE, "--rev", R92_TIP, "--paths", R92_PATHS[0]])[1], re.M) is not None
    print(f"W3 {'pass' if legs['W3'] else 'fail'}")

    # W4 self-application on this round's own frozen table
    added = git(lane, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS)
    commits = [x for x in added.stdout.decode().split() if x]
    if not commits:
        legs["W4"] = False
        print(f"W4 fail claims-absent {CLAIMS} at {rev[:12]}")
    else:
        freeze = commits[-1]
        rc, out = run_tool(tool, lane, work / "w4", ["--freeze", freeze, "--rev", rev, "--claims", CLAIMS])
        s = summary(out)
        legs["W4"] = rc == 0 and s is not None and s[0] >= MIN_SELF_INSTRUMENTS and s[2] == 0
        print(f"W4 {'pass' if legs['W4'] else 'fail'} freeze={freeze[:12]} rc={rc} summary={s}")
        for line in out.splitlines():
            if line.startswith("INSTRUMENT "):
                print("W4 " + line)
    passed = all(legs.get(k) for k in ("W1", "W2", "W3", "W4"))
    print(f"TARGET legs_passed={sum(1 for v in legs.values() if v)} of 4")
    print(f"PREDICATE R93-C2 {'pass' if passed else 'fail'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
