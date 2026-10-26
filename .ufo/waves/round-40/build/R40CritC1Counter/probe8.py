import os, pathlib, subprocess, sys
stamp, payload = sys.argv[1], sys.argv[2]
uid = os.getuid()
env = dict(os.environ); env["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"
unitdir = pathlib.Path("/home/vgpnk/.config/systemd/user")
unitdir.mkdir(parents=True, exist_ok=True)
u = unitdir / "crit-r40-esc8.service"
u.write_text("[Unit]\nDescription=crit escape probe\n[Service]\nType=oneshot\nExecStart=/usr/bin/python3 %s %s\n"
             % (payload, stamp))
def call(*args):
    return subprocess.run(["busctl", "--user", "--no-pager", "call", "org.freedesktop.systemd1",
                           "/org/freedesktop/systemd1", "org.freedesktop.systemd1.Manager", *args],
                          capture_output=True, text=True, env=env, timeout=30)
print("reload", call("Reload").returncode)
r = call("StartUnit", "ss", "crit-r40-esc8.service", "replace")
print("start rc=", r.returncode, "err=", r.stderr.strip()[:160])
