"""D7 (R41MutC1Counter): a nondeterministic receipt must raise null_detected.

Drafted extra control for counter mutant KM14 (null run comparison disabled).
Ten receipts fixtures whose probe exits 0/1 at random: the reference run and the
second unmodified run differ with probability 1/2 each, so at least one NULL line
appears with probability 1 - (1/2)^10. The control pins: NULL lines present and
null_detected >= 1 (exit stays 1 either way through `wrong`, so this is a
line-level catch by construction).
"""

EV = "corpus/evidence/r/foo-probe.txt"

STUB = (
    '"""Stub probe.\n\n  python3 plans/foo_probe.py --lane .\n"""\n'
    "import random\nimport sys\n"
    "if random.random() < 0.5:\n"
    "    sys.stdout.write('X-000000\\n')\n"
    "    sys.exit(0)\n"
    "sys.stdout.write('X-%06d\\n' % random.randint(1, 999999))\n"
    "sys.exit(1)\n"
)


def make_build(tag):
    def build(ctx, d):
        root = ctx.init(d / "lane")
        ctx.write(root / EV, "X-000000\n")
        ctx.write(root / "plans/foo_probe.py", STUB)
        ctx.git(root, "add", "-A")
        ctx.git(root, "commit", "-q", "-m", "fixture")
        return ["--lane", str(root), "--work", "{WORK}"]
    return build


FIXTURES = [{"fid": f"d7-random-probe-{k:02d}", "tool": "receipts", "expect": "reject",
             "defects": [], "build": make_build(f"r{k:02d}")} for k in range(10)]
