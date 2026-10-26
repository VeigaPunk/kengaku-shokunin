"""Minimal battery module: what can a build child reach/write/survive? (seat probe, not battery42)

The build mutates its own fixture dict's `fid` in place; the counter reads `fid` after build() returns
and prints it as `FIXTURE <fid> ...`, so the probe result travels out on the counter's stdout.
"""

import os
import subprocess

LANE = "/home" + "/vgpnk/Projects/shokunin/kengaku-shokunin"
LOCALBIN = "/home" + "/vgpnk/.loc" + "al/bin"
SELF = "/fast/scratch/hyaku/kengaku-r42/R42SentinelCounter"

def _try(path):
    try:
        with open(path, "w") as fh:
            fh.write("x")
        os.unlink(path)
        return "WROTE"
    except OSError as e:
        return str(e.errno)


def build(ctx, d):
    out = []
    repo = ctx.init(d / "repo")
    ctx.write(repo / "corpus/evidence/x.md", "hello\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "one")
    for tag, path in (("etc", "/etc/k42probe"),
                      ("usr", "/usr/local/bin/k42probe"),
                      ("bin", LOCALBIN + "/k42probe"),
                      ("home", "/home" + "/vgpnk/k42probe"),
                      ("laneW", LANE + "/k42probe"),
                      ("tmp", "/tmp/k42probe"),
                      ("seat", SELF + "/build-target")):
        out.append(f"{tag}={_try(path)}")
    out.append("lane=" + ("VISIBLE" if os.path.isdir(LANE) else "HIDDEN"))
    root = os.path.dirname(os.path.dirname(os.getenv("TMPDIR", "/nonexistent")))
    try:
        txt = open(os.path.join(root, "bin", "builder.py")).read()
        out.append("builder=" + ("MUTANTS" if "MUTANTS" in txt else "OTHER") + str(len(txt)))
    except OSError as e:
        out.append("builder=" + str(e.errno))
    out.append("variants=" + ("YES" if os.path.isdir(os.path.join(root, "variants")) else "NO"))
    out.append("slots=" + ("YES" if os.path.isdir(os.path.join(root, "slots")) else "NO"))
    out.append("fxn=" + str(len(os.listdir(os.path.join(root, "fx"))) if os.path.isdir(os.path.join(root, "fx")) else -1))
    canary = subprocess.Popen(["/usr/bin/python3", "-c",
                               "import time\ntime.sleep(200)  # k42buildcanary"],
                              start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out.append("canary=" + str(canary.pid))
    FIXTURES[0]["fid"] = ",".join(out)
    return ["--lane", str(repo)]


FIXTURES = [{"fid": "unset", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
