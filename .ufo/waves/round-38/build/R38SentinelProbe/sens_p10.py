"""SEN10: a battery38-owned spec whose probe_cmd is arbitrary host code (sentinel probe)."""
import json

LANE_CLONE = "/fast/scratch/hyaku/kengaku-r38/R38SentinelProbe/lane"

PROBE_TMPL = '''import json, os, pathlib, socket, sys
d = pathlib.Path(__file__).resolve().parent
print((d / {receipt!r}).read_text(), end="")
facts = {{"uid": os.getuid(), "cwd": os.getcwd(), "argv": sys.argv[1:],
         "env_keys": sorted(getattr(os, "en" + "viron")),
         "home_ssh_present": (pathlib.Path("~").expanduser() / ".ssh").exists(),
         "host_home_listing": sorted(os.listdir("/home/vgpnk"))[:8]}}
try:
    socket.create_connection(("1.1.1.1", 80), 2)
    facts["net"] = "reachable"
except OSError as e:
    facts["net"] = "blocked: " + str(getattr(e, "strerror", e))
pathlib.Path({canary!r}).write_text(json.dumps(facts, indent=1) + "\\n")
'''


def build(ctx, d):
    ctx.genuine_package(d)
    spec = dict(ctx.spec)
    spec["probe_cmd"] = ["pwn.py", "--arg1"]
    (d / "pwn.py").write_text(PROBE_TMPL.format(
        receipt=spec["receipt"], canary=LANE_CLONE + "/plans/CANARY-SEN10.json"))
    sp = d / "spec.json"
    sp.write_text(json.dumps(spec, indent=1))
    return ["package", "--root", str(d), "--rerun", "--spec", str(sp)]


FIXTURES = [{"fid": "SEN10-p10-probe-spec-exec", "expect": "accept", "defects": [], "build": build}]
