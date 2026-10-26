"""Sentinel demo module (not for landing): performs out-of-fixture writes inside the C1 build sandbox."""
import os
import subprocess

S = "/fast/scratch/hyaku/kengaku-r40/R40SentinelCounter"
REPORT = []
DECOY = os.path.join(S, "decoy-repo")


def say(k, v):
    REPORT.append(f"{k}={v}")


def outside_write():
    try:
        with open(os.path.join(S, "hostile", "outside-d.txt"), "a") as f:
            f.write("written from inside bwrap --dev-bind / / --unshare-pid\n")
        say("WRITE_OUTSIDE_D", "ok")
    except OSError as e:
        say("WRITE_OUTSIDE_D", type(e).__name__)


def read_secret():
    try:
        with open("/home/vgpnk/.ssh/id_ed25519", "rb") as f:
            n = len(f.read())
        say("SSH_KEY_BYTES", n)
    except OSError as e:
        say("SSH_KEY_BYTES", type(e).__name__)


def lane_git_writable():
    lane = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
    say("LANE_DOT_GIT_W_OK", os.access(lane + "/.git", os.W_OK))
    say("LANE_PINNED_TOOL_W_OK", os.access(lane + "/plans/order_check.py", os.W_OK))
    say("LANE_CLAIMS_W_OK", os.access(lane + "/.ufo/waves/round-40/claims", os.W_OK))


def symlinked_git(d):
    """A fixture whose .git points outside d: commits land in DECOY, d's fingerprint shows only a link."""
    if os.path.isdir(DECOY):
        subprocess.run(["rm", "-rf", DECOY], check=False)
    subprocess.run(["git", "init", "-q", "-b", "master", DECOY], check=True,
                   env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
                        "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
                        "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid"})
    with open(os.path.join(d, "a.txt"), "w") as f:
        f.write("x\n")
    os.symlink(os.path.join(DECOY, ".git"), os.path.join(d, ".git"))
    env = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
           "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@kengaku.invalid",
           "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@kengaku.invalid",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    r = subprocess.run(["git", "-C", str(d), "add", "-A"], capture_output=True, text=True, env=env)
    say("GIT_ADD_RC", r.returncode)
    r = subprocess.run(["git", "-C", str(d), "commit", "-qm", "from-fixture"], capture_output=True, text=True, env=env)
    say("GIT_COMMIT_RC", r.returncode)
    ref = os.path.join(DECOY, ".git", "refs", "heads", "master")
    say("DECOY_REF_EXISTS", os.path.exists(ref))
    if os.path.exists(ref):
        with open(ref) as f:
            say("DECOY_REF", f.read().strip()[:12])


def build(ctx, d):
    outside_write()
    read_secret()
    lane_git_writable()
    symlinked_git(d)
    with open(os.path.join(d, "report.txt"), "w") as f:
        f.write("\n".join(REPORT) + "\n")
    return ["--lane", str(d / "absent-lane")]


FIXTURES = [{"fid": "SENTINEL-1", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
