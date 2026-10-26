"""R43CritEquiv direct probe 2: NA1/NA5/NA18 outputs on the critic battery fixtures."""

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

PIN_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
    "HOME": "/nonexistent", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
}

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/critbatt")
import r43crit as batt  # noqa: E402


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


ROOT = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43CritEquiv/probe/fx2")
ctx = MiniCtx()


def build(name, fn):
    d = ROOT / name
    if d.exists():
        shutil.rmtree(d)
    return fn(ctx, d)


fix_long = build("malformed", batt.f1_malformed_long)
fix_slash = build("slashed", batt.f3_slashed_name)
fix_short = build("short", batt.f4_short_commit)


def run(variant, argv_tail):
    script = MUTDIR / f"{variant}.py" if variant != "REF" else None
    base = TOOLPATH["anchor"] if "--claims" not in argv_tail else TOOLPATH["order"]
    cmd = [sys.executable, str(script if script else base), *argv_tail]
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **PIN_ENV))
    classes = [ln.split("class=")[1].split()[0] for ln in r.stdout.splitlines()
               if "DEFECT" in ln and "class=" in ln]
    return r.returncode, classes, r.stdout


for label, argv, variants in [
    ("malformed-long (NA1)", ["--lane", str(fix_long[fix_long.index("--lane") + 1])], ["REF", "NA1"]),
    ("slashed-name (NA5)", ["--lane", str(fix_slash[fix_slash.index("--lane") + 1])], ["REF", "NA5"]),
    ("short-commit (NA18)", ["--lane", str(fix_short[fix_short.index("--lane") + 1])], ["REF", "NA18"]),
]:
    print(f"\n=== {label} ===")
    for v in variants:
        rc, classes, out = run(v, argv)
        print(f"{v}: rc={rc} classes={classes}")
        print("   " + out.replace("\n", "\n   ").strip()[:400])
