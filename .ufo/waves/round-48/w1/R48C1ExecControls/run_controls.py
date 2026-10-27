#!/usr/bin/env python3
"""R48C1ExecControls - run the six frozen C1 controls against the v2 counter candidate.

v2 (superseding v1 f395e085...): the honest population is the 16 novel honest modules the honest seat froze
(9 r46novel + 7 novel48), pinned by digest in the counter's PINS_EXTRA and expected under `plans/honest48/`
in the measured tree. The counter therefore must be COPIED INTO the clone as plans/round48_c1_verify.py and
the 16 modules must be placed at plans/honest48/ - that is the tree the L1 will freeze at stage 2.

Every control runs on its own fresh `git clone --shared` of the lane at the measured revision; the clone's
`git rev-parse --show-toplevel` is asserted equal to the clone root before any write. The fence under test is
selected with the counter's `--fence` testing override, so the control receipt measures the control and not
an edit of the lane; the tree still carries the two stage-2 artifacts (the counter itself and the 16 pinned
honest modules), which the receipt reports as `TREE dirty` so nothing is hidden.
"""
import concurrent.futures
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys

SCR = pathlib.Path("/fast/scratch/hyaku/kengaku-r48/R48C1ExecControls")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HONEST_SRC = LANE / ".ufo/waves/round-48/w1/R48C1ExecHonest/modules"
BASE = "0f77f9b27931b3c76b3d095fc0fa70edb79556d9"
STAGE1 = "a543d92083557dd9b33ee674e9b99b03411f80af"
COUNTER = SCR / "inbox/round48_c1_verify.v2.py"
COUNTER_SHA = "8726e99ba6f4732d0d94545c287ff7ea0cc7a71328ba0b3a4659796d9fdad09f"
ENVELOPE = SCR / "envelope.sh"
JOBS = "4"

CONTROLS = [
    ("control-c1-no-fence", None,
     "no fence: the counter is pointed at a fence path that does not exist, so the fence is absent and every "
     "fixture decision errors out (the round-46 no-fence control deleted plans/fixture_fence.py; the counter "
     "substitutes an absent-fence stub that raises)"),
    ("control-c1-base-fence", "@BASE",
     "the base fence: plans/fixture_fence.py @ 0f77f9b27931b3c76b3d095fc0fa70edb79556d9 (sha256 "
     "05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e), the before value; expected failure "
     "mode: the honest leg refuses part of the frozen novel honest population"),
    ("control-c1-fence-r45-keyed", str(SCR / "fences/r45_keyed_name.py"),
     "the round-45 keyed fence: .ufo/waves/round-45/claims/fences/keyed_name.py (sha256 "
     "d21a6a173c68b13ce9abcd2716f37afaed1930646faa43a266adfd4258b9452e), which keys the verdict on the "
     "counter-chosen fixture path and inspects nothing"),
    ("control-c1-fence-admit-all", str(SCR / "fences/admit_all.py"),
     "admit-all: .ufo/waves/round-45/claims/fences/admit_all.py (sha256 "
     "6c3b9a18566a7045d679263867b64ff0735bc79a39abe7e57dfffd724f05d912), a fence that admits every fixture"),
    ("control-c1-fence-refuse-all", str(SCR / "fences/refuse_all.py"),
     "refuse-all: .ufo/waves/round-45/claims/fences/refuse_all.py (sha256 "
     "fc38325360ee7058401ff88c738ce4a7f5e0d8e97196b605b4b57dfed79ef867), a fence that refuses every fixture"),
    ("control-c1-fence-name-keyed-variant", str(SCR / "fences/name_keyed_variant.py"),
     "name-keyed variant (R48C1ExecControls, scratch-authored): a stricter name-keyed control than the "
     "round-45 keyed fence - it scans the last three path components of d, the basename of d and every argv "
     "basename for group or module name markers, and opens nothing"),
]


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def clone(name, rev):
    d = SCR / "trees" / name / "lane"
    if d.exists():
        shutil.rmtree(d)
    d.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(LANE), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", rev], check=True)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if top != str(d):
        raise RuntimeError(f"{name}: toplevel {top} != {d}")
    return d


def stage_artifacts(d):
    """The two stage-2 artifacts the v2 counter needs: itself, and the 16 pinned novel honest modules."""
    shutil.copy(COUNTER, d / "plans/round48_c1_verify.py")
    h = d / "plans/honest48"
    h.mkdir(exist_ok=True)
    for sub in ("r46novel", "novel48"):
        for f in sorted((HONEST_SRC / sub).glob("*.py")):
            shutil.copy(f, h / f.name)
    return len(sorted(h.glob("*.py")))


def run(name, fence_spec, header, rev=STAGE1):
    d = clone(name, rev)
    n_novel = stage_artifacts(d)
    work = SCR / "w" / name
    work.mkdir(parents=True, exist_ok=True)
    env_dir = SCR / "env" / name
    env_dir.mkdir(parents=True, exist_ok=True)
    if fence_spec == "@BASE":
        fence = d / "plans/fixture_fence.py"
    elif fence_spec is None:
        fence = SCR / "fences/ABSENT_fence.py"      # never created: the fence is absent
    else:
        fence = pathlib.Path(fence_spec)
    argv = ["python3", "plans/round48_c1_verify.py", "--lane", ".", "--work", str(work),
            "--jobs", JOBS, "--fence", str(fence)]
    env = dict(os.environ)
    env["TMPDIR"] = str(SCR)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    out = subprocess.run([str(ENVELOPE), str(env_dir)] + argv, cwd=str(d),
                         capture_output=True, text=True, env=env)
    head = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                           capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(d), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    body = (f"# control {name}: {header}\n"
            f"# command: envelope.sh <env> " + " ".join(argv) + f"\n"
            f"# measured tree: clone {d} (git rev-parse --show-toplevel verified == clone root)\n"
            f"# measured HEAD {head} (clean-lane base {rev}; the tree carries the two stage-2 artifacts: "
            f"plans/round48_c1_verify.py and {n_novel} modules under plans/honest48/)\n"
            f"# counter: {COUNTER} sha256={sha256(COUNTER)} (expected {COUNTER_SHA})\n"
            f"# fence under test: {fence} "
            + (f"sha256={sha256(fence)}" if fence.is_file() else "ABSENT") + "\n")
    body += out.stdout
    if out.stderr.strip():
        body += "# stderr (last 20 lines)\n" + "\n".join(out.stderr.splitlines()[-20:]) + "\n"
    body += f"# exit={out.returncode}\n"
    (SCR / "out" / f"{name}.txt").write_text(body)
    pred = [l for l in out.stdout.splitlines() if l.startswith("PREDICATE")]
    summary = [l for l in out.stdout.splitlines()
               if l.startswith(("REV ", "TREE ", "PINS ", "FENCE ", "LITERALS ", "MODULES ", "REFUSALS ",
                                "SEALED ", "HONEST ", "HONEST-NOVEL", "BENIGN", "ERRORS ", "CALIBRATION ",
                                "REASON ", "PREDICATE", "ENVELOPE end"))]
    return name, out.returncode, (pred[-1] if pred else "NO PREDICATE LINE"), summary, head


def main():
    got = sha256(COUNTER)
    if got != COUNTER_SHA:
        print(f"ABORT counter sha256 {got} != {COUNTER_SHA}", file=sys.stderr)
        return 2
    (SCR / "out").mkdir(parents=True, exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(3) as ex:
        futs = [ex.submit(run, n, f, h, BASE) for n, f, h in CONTROLS]
        for f in futs:
            results.append(f.result())
    with open(SCR / "out/summary-v2-base.txt", "w") as fh:
        for name, rc, pred, summary, head in results:
            fh.write(f"{name} exit={rc} {pred} HEAD={head}\n")
            for line in summary:
                fh.write("  " + line + "\n")
    for name, rc, pred, summary, head in results:
        print(f"===== {name} exit={rc} {pred} HEAD={head}")
        for line in summary:
            print("   " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
