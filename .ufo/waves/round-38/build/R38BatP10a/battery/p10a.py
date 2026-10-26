"""battery38 / p10a — P10 ("a receipt a fresh run does not reproduce") on the --rerun side.

Two frozen mutants of the receipt byte-compare, one fixture each:

  N13  `r.stdout != want` -> `r.stdout.rstrip() != want.rstrip()`
       the fixture receipt is ONE line; the fresh probe reproduces it with three trailing spaces
       before the newline. Byte-unequal, `rstrip`-equal: the unmodified gate is red, the mutant green.
  N14  `r.stdout != want` -> `r.stdout.splitlines()[:1] != want.splitlines()[:1]`
       the fresh probe reproduces the genuine round-35 receipt's first line exactly and diverges in
       every later line: the unmodified gate is red, the mutant compares only line 1 and is green.

Each fixture owns its spec (plans/round38_c1_verify.py allows a battery38 fixture a `--spec` file
inside its dir): the derived spec points `probe_cmd` at a fixture-local script, so the genuine
round-35 frozen instruments (plans/tb2_grader_probe.py included) stay byte-identical and P1 keeps
verifying its real pins. P10 is the only clause that fires — the declared defect set below is that
single clause — and the receipt itself is never left unpinned: the N13 fixture rewrites the receipt
bytes under the genuine receipt path and pins the new digest in its owned spec (so P2 stays ok on
real bytes), the N14 fixture keeps the genuine receipt and the frozen r35 digest.

Why N13's receipt is one line: the two mutants sit on the same gate line and N13's `rstrip` is the
weaker test, so any output that is `rstrip`-equal to a multi-line receipt repeats its first line
verbatim and N14's first-line-only mutant would accept it too. A single-line receipt is the only
shape where the whole difference IS trailing whitespace, so the N13 fixture reddens N13 alone and
each fixture is load-bearing for exactly its own mutant (measured: deleting the N13 fixture leaves
N13 SURVIVED with N14 still killed, and the other way round).
"""

import hashlib
import json

PROBE = "p10a-probe.py"
SPEC = "p10a-spec.json"
ONE_LINE_RECEIPT = "p10a fixture receipt: fresh-run byte-compare target\n"


def _build(probe_body, receipt_text=None):
    """Genuine package + fixture receipt (optional) + receipt-reading probe + owned spec."""

    def build(ctx, d):
        ctx.genuine_package(d)
        spec = json.loads(json.dumps(ctx.spec))
        spec["probe_cmd"] = [PROBE]
        if receipt_text is not None:
            (d / spec["receipt"]).write_text(receipt_text)
            spec["receipt_sha256"] = hashlib.sha256(receipt_text.encode("utf-8")).hexdigest()
        (d / PROBE).write_text(
            "import pathlib, sys\n"
            f"want = pathlib.Path({spec['receipt']!r}).read_text()\n" + probe_body)
        (d / SPEC).write_text(json.dumps(spec, indent=1, sort_keys=True) + "\n")
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree", "--rerun",
                "--spec", str(d / SPEC)]

    return build


FIXTURES = [
    {"fid": "p10a-n13-trailing-space", "expect": "reject", "defects": ["P10"],
     "build": _build('sys.stdout.write(want.rstrip("\\n") + "   \\n")\n', ONE_LINE_RECEIPT)},
    {"fid": "p10a-n14-first-line-only", "expect": "reject", "defects": ["P10"],
     "build": _build('sys.stdout.write(want.splitlines()[0] + "\\np10a-receipt-tail-diverges\\n")\n')},
]
