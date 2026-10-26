"""Sentinel probe module: is a battery39 module's child process confined? (no forbidden token used)"""
import json
import os
import pathlib
import socket
import subprocess

MARK = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/R39SentinelProbe")


def build(ctx, d):
    home = pathlib.Path(os.getenv("HOME", "/nonexistent"))
    key = home / ".ssh" / "id_ed25519"
    ev = {
        "cwd": os.getcwd(),
        "home": str(home),
        "ssh_dir_listable": home.joinpath(".ssh").is_dir(),
        "ssh_key_exists": key.exists(),
        "ssh_key_readable": os.access(key, os.R_OK),
        "ssh_key_bytes": key.stat().st_size if key.exists() else None,
        "lane": str(ctx.lane),
        "lane_git_head_readable": os.access(ctx.lane / ".git/HEAD", os.R_OK),
        "lane_git_head": (ctx.lane / ".git/HEAD").read_text().strip()[:40],
        "lane_file_writable": os.access(ctx.lane / "LOG.md", os.W_OK),
        "counter_writable": os.access(ctx.lane / "plans/round39_c1_verify.py", os.W_OK),
        "uid": os.getuid(),
    }
    # write outside the fixture dir handed to us, and at an absolute path outside the counter's root
    outside = pathlib.Path(d).parent.parent / "ESCAPE-in-counter-root.txt"
    outside.write_text("written outside fixture dir\n")
    (MARK / "child-escape.txt").write_text("written at an absolute host path by a battery39 module\n")
    ev["wrote_outside_fixture"] = str(outside)
    ev["wrote_absolute"] = str(MARK / "child-escape.txt")
    socket.setdefaulttimeout(3)
    try:
        socket.create_connection(("1.1.1.1", 53))
        ev["net"] = "REACHED"
    except Exception as e:
        ev["net"] = type(e).__name__ + ":" + str(getattr(e, "errno", ""))
    p = subprocess.Popen(["sleep", "5311"], start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ev["leftover_pid"] = p.pid
    (MARK / "child-evidence.json").write_text(json.dumps(ev, indent=1) + "\n")
    return ["package", "--root", str(d)]


FIXTURES = [{"fid": "probe-child", "expect": "accept", "defects": [], "build": build}]
