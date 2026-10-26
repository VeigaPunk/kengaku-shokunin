"""battery38 / b1run — fixtures that kill N01 and N16 of plans/round38_c1_verify.py.

N01 (P1, silence): `c_instruments` returns `bool(pins) and not bad`; an empty `frozen_instruments`
pin set must not accept. The fixture owns a spec derived from the genuine round-35 spec with
`frozen_instruments` emptied, over the genuine package bytes: the reference prints `P1 DEFECT
pinned=0`, the mutant prints `P1 ok`.

N16 (RUN, silence): a clause that raises is a defect, never a pass. The fixture owns a spec whose
`entry_rules.quote_words` has one value, so `c_quote_shape` raises `ValueError` inside `run_checks`;
the reference prints `P3 DEFECT clause error ValueError`, the mutant turns that into `P3 ok`.

Both specs are written inside the fixture dir and staged, so P9 (`--require-clean-tree`) stays clean.
"""

import copy
import json

# ---- b1run-n01-empty-pins -----------------------------------------------------------------------

def _fixture_empty_pins():
    def build(ctx, d):
        ctx.genuine_package(d)
        spec = copy.deepcopy(ctx.spec)
        spec["frozen_instruments"] = {}
        spec_path = d / "spec-b1run-empty-pins.json"
        spec_path.write_text(json.dumps(spec, indent=1, sort_keys=True) + "\n")
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(spec_path)]

    return {"fid": "b1run-n01-empty-pins", "expect": "reject", "defects": ["P1"], "build": build}


# ---- b1run-n16-clause-crash ---------------------------------------------------------------------

def _fixture_clause_crash():
    def build(ctx, d):
        ctx.genuine_package(d)
        spec = copy.deepcopy(ctx.spec)
        spec["entry_rules"]["quote_words"] = [3]
        spec_path = d / "spec-b1run-clause-crash.json"
        spec_path.write_text(json.dumps(spec, indent=1, sort_keys=True) + "\n")
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(spec_path)]

    return {"fid": "b1run-n16-clause-crash", "expect": "reject", "defects": ["P3"], "build": build}


FIXTURES = [_fixture_empty_pins(), _fixture_clause_crash()]
