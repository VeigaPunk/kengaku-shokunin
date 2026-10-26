"""Hostile hull probe H2: the fixture-owned --spec names `probe_cmd`, and the reference gate executes it
(cwd = the fixture tree) after the counter's gate directory exists.  The probe plants a shadow stdlib
module there; every mutant gate run then imports it and its output is fabricated.  No gate behaviour is
demonstrated by any fixture below.  No side-channel token is used.
"""

import hashlib
import json
import pathlib

SHADOW = '''import os, sys, sysconfig
_name = os.path.basename(sys.argv[0])
_mirror = {"N02": "P3", "N08": "P5", "N15": "P10"}
if _name.startswith("N") and _name.endswith(".py"):
    if _name[:-3] in _mirror:
        print(_mirror[_name[:-3]] + " DEFECT fabricated-by-shadow-module")
    os._exit(1)
_p = os.path.join(sysconfig.get_paths()["stdlib"], "hashlib.py")
_ns = {}
exec(compile(open(_p).read(), _p, "exec"), _ns)
globals().update({k: v for k, v in _ns.items() if not k.startswith("__")})
'''

PLANT = ("import pathlib\n"
         "g = pathlib.Path.cwd().resolve().parents[1] / 'gates'\n"
         "(g / 'hashlib.py').write_text(" + repr(SHADOW) + ")\n"
         "print('STABLE-PROBE')\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def spec_with(ctx, d, probe, receipt_text, name="spec.json"):
    spec = dict(ctx.spec)
    spec["receipt_sha256"] = sha(receipt_text.encode())
    spec["probe_cmd"] = probe
    p = d / name
    p.write_text(json.dumps(spec))
    r = d / spec["receipt"]
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text(receipt_text)
    return p


def b_plant(ctx, d):
    sp = spec_with(ctx, d, ["-c", PLANT], "STABLE-PROBE\n")
    return ["package", "--root", str(d), "--spec", str(sp), "--rerun"]


def b_accept(ctx, d):
    ctx.genuine_package(d)
    sp = spec_with(ctx, d, ["-c", "print('STABLE-PROBE')"], "STABLE-PROBE\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--spec", str(sp), "--require-clean-tree", "--rerun"]


def b_p10reject(ctx, d):
    ctx.genuine_package(d)
    sp = spec_with(ctx, d, ["-c", "print('OTHER')"], "STABLE-PROBE\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--spec", str(sp), "--require-clean-tree", "--rerun"]


def b_root_nodir(ctx, d):
    sp = d / "spec.json"
    sp.write_text(json.dumps(dict(ctx.spec)))
    return ["package", "--root", str(d / "nodir"), "--spec", str(sp)]


def b_crash(ctx, d):
    sp = d / "spec.json"
    sp.write_text("[1, 2]")
    return ["package", "--root", str(d), "--spec", str(sp)]


def b_d4(ctx, d):
    (d / "spec.json").write_text(json.dumps({"d4": {"label": "DIR-R38: ", "patterns": ["alpha"]}}))
    (d / "line.txt").write_text("DIR-R38: beta\n")
    return ["d4-line", "--file", str(d / "line.txt"), "--spec", str(d / "spec.json")]


def b_d5(ctx, d):
    (d / "spec.json").write_text(json.dumps({"d5": {"label": "DIR-R38: ", "require": "alpha",
                                                    "forbid": "zzz", "capture_name": "cap.txt",
                                                    "manifest_name": "SHA256SUMS", "quote": "alpha"}}))
    (d / "line.txt").write_text("DIR-R38: beta\n")
    return ["d5-line", "--file", str(d / "line.txt"), "--capture-dir", str(d / "cap"),
            "--spec", str(d / "spec.json")]


FIXTURES = [
    {"fid": "h2-plant", "expect": "reject", "defects": ["P1", "P3", "P4", "P5", "P6", "P7", "P8"], "build": b_plant},
    {"fid": "h2-main17", "expect": "error", "defects": [], "build": b_root_nodir},
    {"fid": "h2-main18", "expect": "error", "defects": [], "build": b_crash},
]
