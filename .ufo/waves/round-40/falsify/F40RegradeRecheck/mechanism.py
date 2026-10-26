"""F40RegradeRecheck mechanism probe: for glr, what makes `git fsck --lost-found` write nothing?

Stages two listed states ONCE with the lane probe's own builders and, before any grading, reads
the graded repository: the lost-found files present, whether each file's object still exists, and
how many `dangling` lines `git fsck --lost-found` prints. Read-only apart from fsck's own write,
which is exactly the write under measurement.
"""
import pathlib
import sys

S = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(S))
import regrade2 as R  # noqa: E402

MECH = r'''
import glob, json, os, subprocess
def sh(c):
    r = subprocess.run(["sh", "-c", c], capture_output=True, text=True)
    return r.returncode, r.stdout
files = sorted(glob.glob("/app/repo/.git/lost-found/*/*"))
print("LF=" + json.dumps([f.replace("/app/repo/", "") for f in files]))
for f in files:
    rc, _ = sh("git -C /app/repo cat-file -e " + os.path.basename(f) + " 2>/dev/null")
    print("OBJ-EXISTS " + os.path.basename(f)[:12] + " rc=" + str(rc))
rc, out = sh("git -C /app/repo fsck --lost-found")
print("FSCK rc=" + str(rc) + " dangling_lines=" + str(sum(1 for l in out.splitlines() if "dangling" in l)))
print("FSCK-OUT=" + json.dumps(out.splitlines()[:6]))
rc, out = sh("git -C /app/repo reflog | wc -l")
print("REFLOG entries=" + out.strip())
'''


def run(probe, cap, w, script, args, env):
    (w / "harness.py").write_text(script)
    return R.run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py"] + args, env, 300)


def main():
    R.WORK.mkdir(parents=True, exist_ok=True)
    probe = R.load_probe("git_leak_probe")
    cap = R.LANE / probe.CAP
    env = {"PATH": probe.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    for cid in ("oracle-solve-sh", "untouched"):
        case = next(c for c in probe.CASES if c.cid == cid)
        w = R.WORK / ("mech-" + cid)
        if w.exists():
            import shutil
            shutil.rmtree(w)
        (w / "app").mkdir(parents=True)
        (w / "recipe.sh").write_text(case.recipe)
        st = run(probe, cap, w, probe.HARNESS_PY, ["stage", "1" if case.setup else "0"], env)
        stages = " ".join(l for l in st.stdout.splitlines() if l.startswith("STAGE "))
        print(f"### glr/{cid} stage_rc={st.returncode} {stages}")
        r = run(probe, cap, w, MECH, [], env)
        for line in r.stdout.splitlines():
            print(f"  {line}")
        if r.returncode != 0:
            print("  stderr=" + repr((r.stderr or "")[-300:]))


if __name__ == "__main__":
    sys.exit(main())
