"""Example battery37 module (API demonstration, written before freeze): one single-defect fixture.

FIXTURES: list of dicts {fid, expect, defects, build}. build(ctx, d) fills the empty dir d and returns the gate
argv tail (never --spec). ctx.genuine_package(d) git-inits d and copies the genuine round-35 package;
ctx.git_add(d) stages it (index only); ctx.r36 is plans/round36_c1_verify.py (rewrite_quotes, QUOTE_ROW, ...).
"""


def _short_quote(ctx, d):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]

    def fn(rows):
        m = ctx.r36.QUOTE_ROW.match(rows[0])
        words = m.group(1).split()
        return [rows[0].replace(f"“{m.group(1)}”", f"“{' '.join(words[:2])}”")] + rows[1:]

    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "ex-p3-two-word-quote", "expect": "reject", "defects": ["P3"], "build": _short_quote},
]
