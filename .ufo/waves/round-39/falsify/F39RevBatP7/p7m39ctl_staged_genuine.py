"""F39RevBatP7 control variant of plans/battery39/p7m39.py (E3): the genuine
package, staged exactly like the landed module but with NO second source line.
Isolates the duplicate line as the sole cause of the reference P7 DEFECT."""

SID = "S105"


def _staged_genuine(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "p7m39ctl-staged-genuine", "expect": "accept", "defects": [],
     "build": _staged_genuine},
]
