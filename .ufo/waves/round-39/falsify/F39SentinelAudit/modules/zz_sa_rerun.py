"""F39SentinelAudit R: a fixture-supplied --rerun spec reaches the audited gate's P10 probe execution.

The audit validates only argv[0] and that --root/--spec lie inside the fixture dir (:310-328); it does not
exclude --rerun, so P10 (pkg_gate.py:271-278 c_rerun) runs probe_cmd -- here a marker append -- under the
audit's own environment.
"""
import copy, json, pathlib

MARKER = "/fast/scratch/hyaku/kengaku-r39/F39SentinelAudit/rerun-marker.txt"


def build(ctx, d):
    spec = copy.deepcopy(ctx.spec)
    spec["probe_cmd"] = ["-c",
        "import sys; open(sys.argv[1], 'a').write('ran cwd=%s home=%s\\n' % (__import__('os').getcwd(), __import__('os').getenv('HOME')))",
        MARKER]
    spec["receipt"] = "rerun.out"
    d.mkdir(parents=True, exist_ok=True)
    (d / "spec.json").write_text(json.dumps(spec))
    root = d / "root"
    root.mkdir(exist_ok=True)
    (root / "rerun.out").write_text("")
    return ["package", "--root", str(root), "--spec", str(d / "spec.json"), "--rerun"]


FIXTURES = [{"fid": "sa-rerun-probe-exec", "expect": "reject",
             "defects": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"], "build": build}]
