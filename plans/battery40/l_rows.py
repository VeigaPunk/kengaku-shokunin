"""Round-40 C1 battery, `ledger_tip.py` row accounting.

Four fixtures, each a clean clone of the lane with exactly one ledger fact broken, run through the
tool's control mode (`--lane`, no clean-tree refusal). One per advertised accounting rule: an open
row that still passes, two empty ledgers, a check body that dies, a check name no CHECKS entry
carries. Every fixture rejects (exit 1) and names the single row it makes disagree.
"""

TB2_MANIFEST = ".ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS"


def open_row(ctx, d):
    # A closed row whose check still passes, relabelled `open`: the stale self-assessment.
    lane = ctx.clone(d / "lane")
    p = lane / "corpus/defects.jsonl"
    t = p.read_text()
    t2 = t.replace('"check": "r34_d2", "status": "closed"',
                   '"check": "r34_d2", "status": "open"')
    assert t2 != t
    p.write_text(t2)
    return ["--lane", str(lane)]


def empty_ledgers(ctx, d):
    # Both ledgers empty: zero rows and zero mismatches is not agreement.
    lane = ctx.clone(d / "lane")
    (lane / "corpus/defects.jsonl").write_text("")
    (lane / "corpus/defects-round35.jsonl").write_text("")
    return ["--lane", str(lane)]


def check_crashes(ctx, d):
    # The r34_d3 body dies on a missing manifest: a crash is an observed failure, never a pass.
    lane = ctx.clone(d / "lane")
    (lane / TB2_MANIFEST).unlink()
    return ["--lane", str(lane)]


def unknown_check(ctx, d):
    # A closed row whose `check` names no CHECKS entry: an unknown check is a failed check.
    lane = ctx.clone(d / "lane")
    p = lane / "corpus/defects.jsonl"
    t = p.read_text()
    t2 = t.replace('"check": "r34_d5"', '"check": "r34_d6"')
    assert t2 != t
    p.write_text(t2)
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "l_rows-open-row", "tool": "ledger", "expect": "reject",
     "defects": ["NO:R34-D2"], "build": open_row},
    {"fid": "l_rows-empty-ledgers", "tool": "ledger", "expect": "reject",
     "defects": [], "build": empty_ledgers},
    {"fid": "l_rows-check-crashes", "tool": "ledger", "expect": "reject",
     "defects": ["NO:R34-D3"], "build": check_crashes},
    {"fid": "l_rows-unknown-check", "tool": "ledger", "expect": "reject",
     "defects": ["NO:R34-D5"], "build": unknown_check},
]
