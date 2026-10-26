"""R43CritEquiv direct probe: reference vs mutant output diff on shared from-nothing fixtures.

Uses the frozen counter's MUTANTS table to patch byte copies of the tools, then runs them on
fixture repos built by the critic battery's own builders (different shapes from the freeze witness).
"""

import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/lane")
SPEC = importlib.util.spec_from_file_location("c1", LANE / "plans/round43_c1_verify.py")
c1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(c1)

TOOLPATH = {"anchor": LANE / "plans/anchor_digest_check.py", "order": LANE / "plans/order_check.py"}
MUTDIR = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/probe/muts")
MUTDIR.mkdir(parents=True, exist_ok=True)

for mid, tool, _cls, _dir, _kind, _adv, _wit, old, new in c1.MUTANTS:
    src = TOOLPATH[tool].read_text()
    assert src.count(old) == 1, (mid, src.count(old))
    (MUTDIR / f"{mid}.py").write_text(src.replace(old, new))
print(f"mutant copies written: {len(c1.MUTANTS)}")

PIN_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
    "HOME": "/nonexistent", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
}


class MiniCtx:
    def init(self, dest):
        dest.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(dest), "init", "-q", "-b", "master"], check=True)
        return dest

    def git(self, repo, *args):
        env = dict(os.environ)
        env.update({"GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
                    "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
                    "GIT_AUTHOR_DATE": "2026-10-26T00:00:00+00:00",
                    "GIT_COMMITTER_DATE": "2026-10-26T00:00:00+00:00"})
        subprocess.run(["git", "-C", str(repo), *args], check=True, env=env)

    def write(self, path, text):
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode())

    def sh(self, *argv, cwd=None):
        subprocess.run(list(argv), check=True, cwd=cwd)


sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/critbatt")
import r43crit as batt  # noqa: E402

ROOT = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/probe/fx")
ctx = MiniCtx()


def build(name, fn):
    d = ROOT / name
    if d.exists():
        shutil.rmtree(d)
    return fn(ctx, d)


def fix_oldest(ctx, d):
    repo = ctx.init(d / "lane")
    ctx.write(repo / batt.CLAIMS43, "# round 43 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / batt.M43 / "control.txt", "P10 DEFECT fresh probe output is not byte-equal cases=12\n")
    batt.landed(ctx, repo, "freeze")
    ctx.write(repo / batt.PROBE43, "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    batt.landed(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", batt.CLAIMS43, "--receipt", batt.PROBE43]


def fix_case_later(ctx, d):
    repo = ctx.init(d / "lane")
    ctx.write(repo / batt.CLAIMS43, "# round 43 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / batt.M43 / "control.txt", "no gate line and no case line was ever committed here\n")
    batt.landed(ctx, repo, "freeze")
    ctx.write(repo / batt.M43 / "control.txt", "CASE c1 observed=timeout\n")
    batt.landed(ctx, repo, "claims control edited again, still before any recorded run")
    ctx.write(repo / batt.PROBE43, "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    batt.landed(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", batt.CLAIMS43, "--receipt", batt.PROBE43]


fix_errata = build("errata", batt.f2_green_errata)
fix_p2 = build("p2", batt.f6_p2_echo)
fix_late = build("late", batt.f5_late_gate)
fix_oldest_argv = build("oldest", fix_oldest)
fix_case_later_argv = build("case_later", fix_case_later)


def run(variant, argv_tail):
    script = MUTDIR / f"{variant}.py" if variant != "REF" else None
    base = TOOLPATH["anchor"] if "--claims" not in argv_tail else TOOLPATH["order"]
    cmd = [sys.executable, str(script if script else base), *argv_tail]
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **PIN_ENV))
    classes = []
    if "--claims" not in argv_tail:
        classes = [ln.split("class=")[1].split()[0] for ln in r.stdout.splitlines()
                   if "DEFECT" in ln and "class=" in ln]
    return r.returncode, classes, r.stdout, r.stderr


def show(label, argv_tail, variants):
    print(f"\n=== {label} ===")
    for v in variants:
        rc, classes, out, err = run(v, argv_tail)
        print(f"{v}: rc={rc} classes={classes}")
        tail = (out + err).replace("\n", "\n   ").strip()[:420]
        print("   " + tail)


show("errata (anchor)", ["--lane", str(fix_errata[fix_errata.index("--lane") + 1])],
     ["REF", "NA7", "NA20", "NA21"])
show("p2-echo (order)", fix_p2, ["REF", "NO7"])
show("late-gate (order)", fix_late, ["REF", "NO5", "NO22"])
show("gate-in-oldest (order)", fix_oldest_argv, ["REF", "NO5", "NO22"])
show("case-in-later (order)", fix_case_later_argv, ["REF", "NO5", "NO22"])
