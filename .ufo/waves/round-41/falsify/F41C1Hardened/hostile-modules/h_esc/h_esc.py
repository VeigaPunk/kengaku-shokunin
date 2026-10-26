"""Hostile battery module (repair d): a relative argv token escapes the fixture directory.

`path_ok` on the deployed counter only inspects tokens that START with `/`, so the relative token
`../f000/lane` (and, in the second fixture, a long relative path to the real lane) is accepted even though it
resolves outside the fixture directory d it must stay in. The repaired counter resolves every token against d
and refuses the fixture with a contract breach.

Fixture f000 builds a lane-shaped tree in its own directory; f001 points the tool at f000's tree with a
relative escape and declares the classification the tool prints for it, so the escape is green on the deployed
counter and the module is refused (SETUP) on the repaired one. Nothing is written outside each fixture dir.
"""

EV = "corpus/evidence/r/ext-probe.txt"

STUB = '''"""Fixture probe: prints its recorded text.

  python3 plans/ext_probe.py --lane .
"""
import sys

sys.stdout.write("EXT\\n")
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


def b_local(ctx, d):
    # The tree the escaping fixture reads: one committed receipt, one probe whose stem matches it.
    root = lane(ctx, d, {EV: "EXT\n", "plans/ext_probe.py": STUB})
    return ["--lane", str(root), "--list"]


def b_relative_escape(ctx, d):
    # No build: the argv names the sibling fixture's tree through `..`, which is outside this fixture dir.
    return ["--lane", "../f000/lane", "--list"]


FIXTURES = [
    {"fid": "h_esc-local-tree", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV}:derived"], "build": b_local},
    {"fid": "h_esc-relative-escape", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV}:derived"], "build": b_relative_escape},
]
