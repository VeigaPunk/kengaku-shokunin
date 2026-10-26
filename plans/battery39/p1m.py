"""Round-39 C1 battery39 (seat R39BatP1): mutant M02, clause P1, direction silence.

M02 (plans/round39_c1_verify.py) narrows the P1 pin sweep to the FIRST pinned instrument:

    old  bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]
    new  bad = [rel for rel, dig in list(pins.items())[:1] if sha256(p.root / rel) != dig]

so it advertises "every frozen instrument is checked against its pin, not only the first" while only the
first pin is ever verified.  Pre-freeze witness W-X01 (.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt:
ref P1,P9 -> mutant P9) corrupts pin 2 of the round-35 spec over the genuine package.

One fixture, one mutant: the GENUINE round-35 package with appended bytes on the SECOND pinned instrument
(`plans/round35_c1_verify.py`; pin order read from `ctx.spec["frozen_instruments"]`, never hardcoded).  Pin 1
(`plans/tb2_grader_probe.py`) stays genuine, so the mutant's narrowed sweep sees no mismatch.  Every other
clause is untouched: the index is updated with index-only `git add`, so P9 sees no untracked file and the
package is otherwise green.  Reference: `P1 DEFECT`, no other defect, exit 1.  Mutant: `P1 ok`, exit 0 —
the declared silence on P1.  The fixture is the module's only one, so removing it makes M02 SURVIVED
(load-bearing).
"""

import pathlib

OFF_PIN = b"\n# p1m off-pin witness byte\n"


def build(ctx, d):
    ctx.genuine_package(d)
    rels = list(ctx.spec["frozen_instruments"])
    if len(rels) < 2:
        raise RuntimeError(f"spec carries {len(rels)} pins, need a second one")
    f = d / pathlib.PurePosixPath(rels[1])
    if not f.is_file():
        raise RuntimeError(f"second pinned instrument {rels[1]} is absent from the package copy")
    f.write_bytes(f.read_bytes() + OFF_PIN)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": "p1m-second-pin-appended-bytes", "expect": "reject", "defects": ["P1"], "build": build}]
