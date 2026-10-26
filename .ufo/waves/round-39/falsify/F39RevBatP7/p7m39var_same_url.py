"""F39RevBatP7 variant of plans/battery39/p7m39.py (E2): the inserted second
`source: S105` line cites the PINNED url itself, not another row's url.
Everything else is byte-identical in behaviour to the landed module."""

SID = "S105"


def _package(ctx, d, edit):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    before = entry.read_text()
    after = edit(before)
    if after == before:
        raise RuntimeError("entry edit was a no-op")
    entry.write_text(after)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _two_source_lines(ctx, d):
    def edit(text):
        lines = text.splitlines()
        hits = [i for i, line in enumerate(lines) if line.startswith(f"source: {SID} ")]
        if len(hits) != 1:
            raise RuntimeError(f"expected exactly one {SID} source line, found {len(hits)}")
        pinned = ctx.spec["raw_base"] + ctx.spec["rows"][SID]["upstream"]
        second = (f"source: {SID} \u2014 {pinned} \u2014 second source line citing the pinned url, "
                  f"planted by battery39 p7m39var_same_url")
        i = hits[0]
        return "\n".join(lines[:i + 1] + [second] + lines[i + 1:]) + "\n"
    return _package(ctx, d, edit)


FIXTURES = [
    {"fid": "p7m39var-s105-same-url-twice", "expect": "reject", "defects": ["P7"],
     "build": _two_source_lines},
]
