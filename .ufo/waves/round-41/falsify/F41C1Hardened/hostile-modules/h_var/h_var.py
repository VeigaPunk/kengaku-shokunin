"""Hostile battery module (repair a): the counter's variant store is readable from inside a tool run.

The fixture's committed probe is ordinary fixture code: `plans/tip_receipts.py` runs it as a child of the tool
inside the tool's sandbox. It walks up from its own cwd (the tool's clone, inside the run's work dir) to the
counter's scratch root and asks whether `root/variants/ref-*.py` and `root/slots/receipts.py` are readable.
The DEPLOYED counter ro-binds the variant at `root/slots/<tool>.py` under a plain `--ro-bind /`, so the whole
variant store is visible; the repaired counter hides `root/variants` and `root/slots` behind a tmpfs and binds
the variant's *bytes* with `--ro-bind-data`.

The receipt holds the output the probe prints when the store is visible, so the fixture is green on the
deployed counter (the leak is accepted silently) and WRONG on the repaired one.
"""

EV = "corpus/evidence/r/vis-probe.txt"

PROBE = '''"""Fixture probe: is the counter's variant store visible from this run?

  python3 plans/vis_probe.py --lane .
"""
import pathlib
import sys

root = None
for p in pathlib.Path.cwd().parents:
    if (p / "variants").is_dir() or (p / "slots").is_dir():
        root = p
        break
store = bool(root) and (root / "variants" / "ref-receipts.py").is_file() \\
    and (root / "variants" / "ref-sources.py").is_file()
selfsame = store and (root / "slots" / "receipts.py").read_text() == \\
    (root / "variants" / "ref-receipts.py").read_text()
sys.stdout.write("VARIANTS " + ("visible" if store else "hidden")
                 + " self=" + ("reference" if selfsame else "not-reference") + "\\n")
'''


def lane(ctx, d, files):
    root = ctx.init(d / "lane")
    base = {
        "README.md": "# hostile fixture lane\n",
        "SKILL.md": "# fixture skill\n",
        "corpus/README.md": "# fixture lane receipts\n",
        "corpus/knowledge/fixture.md": "# fixture knowledge note\n",
    }
    base.update(files)
    for rel in sorted(base):
        ctx.write(root / rel, base[rel])
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture lane")
    return root


def b_variant_store(ctx, d):
    # The receipt records the output of the probe on a counter whose variant store is readable.
    root = lane(ctx, d, {EV: "VARIANTS visible self=reference\n",
                         "plans/vis_probe.py": PROBE})
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [
    {"fid": "h_var-variant-store-visible", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_variant_store},
]
