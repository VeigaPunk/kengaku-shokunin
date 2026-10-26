"""--root is unconstrained: this fixture never touches d.  It grades a package built beside d, so the
counter's renamed re-run (which only rewrites str(d)) re-runs the very same tree.  The probe logs cwd and
invocation order, which is also the order the shared-state attack relies on."""

import hashlib
import json

LOG = ("import pathlib\n"
       "p = pathlib.Path('/fast/scratch/hyaku/kengaku-r38/R38CritC1Counter/h4log.txt')\n"
       "n = len(p.read_text().splitlines()) + 1 if p.is_file() else 1\n"
       "p.write_text((p.read_text() if p.is_file() else '') + str(pathlib.Path.cwd()) + ' ' + str(n) + chr(10))\n"
       "print('STABLE-PROBE')\n")


def build(ctx, d):
    pkg = d.parent.parent / "h4-pkg"
    ctx.genuine_package(pkg)
    spec = dict(ctx.spec)
    spec["receipt_sha256"] = hashlib.sha256(b"STABLE-PROBE\n").hexdigest()
    spec["probe_cmd"] = ["-c", LOG]
    (d / "spec.json").write_text(json.dumps(spec))
    r = pkg / spec["receipt"]
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text("STABLE-PROBE\n")
    ctx.git_add(pkg)
    return ["package", "--root", str(pkg), "--spec", str(d / "spec.json"),
            "--require-clean-tree", "--rerun"]


FIXTURES = [{"fid": "h4-root-beside-d", "expect": "accept", "defects": [], "build": build}]
