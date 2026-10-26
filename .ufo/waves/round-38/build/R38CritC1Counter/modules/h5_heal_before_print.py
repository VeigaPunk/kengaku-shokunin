"""Same counting fixture as H3, but the tree is healed BEFORE the probe prints.  This is the discriminating
case: the null run then prints a different tree than the reference, so null_detected fires.  H3 heals after
the print and is invisible."""

import hashlib
import json

HEAL = ("import pathlib, shutil\n"
        "d = pathlib.Path.cwd().resolve()\n"
        "root = d.parents[1]\n"
        "cf = root / 'h5-count'\n"
        "n = int(cf.read_text()) + 1 if cf.is_file() else 1\n"
        "cf.write_text(str(n))\n"
        "if n >= 3:\n"
        "    shutil.copytree(root / 'h5-store', d, dirs_exist_ok=True)\n"
        "    r = d / '__RECEIPT__'\n"
        "    r.parent.mkdir(parents=True, exist_ok=True)\n"
        "    r.write_text('STABLE-PROBE' + chr(10))\n"
        "print('STABLE-PROBE')\n")


def b_heal(ctx, d):
    store = d.parent.parent / "h5-store"
    ctx.r36.copy_package(ctx.lane, ctx.spec, store)
    spec = dict(ctx.spec)
    spec["receipt_sha256"] = hashlib.sha256(b"STABLE-PROBE\n").hexdigest()
    spec["probe_cmd"] = ["-c", HEAL.replace("__RECEIPT__", spec["receipt"])]
    (d / "spec.json").write_text(json.dumps(spec))
    r = d / spec["receipt"]
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text("STALE\n")
    return ["package", "--root", str(d), "--spec", str(d / "spec.json"), "--rerun"]


FIXTURES = [{"fid": "h5-before-print", "expect": "reject",
             "defects": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P10"], "build": b_heal}]
