"""Round-39 battery39 module `p7m39`: attributes the P7 (provenance) silence survivor M04.

Frozen mutant M04 (`plans/round39_c1_verify.py` MUTANTS row 4, direction `silence`) replaces the
per-row provenance test

    if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:

with a first-element-only test

    if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:

so a registry row that carries the pinned URL on its FIRST `source:` line and any further
`source:` line after it keeps P7 green. Witness W-X15 (`.ufo/waves/round-38/falsify/F38XMutP/
witness-run.txt`: `ref_defects=P7,P9 mut_defects=P9`). That witness needed P9 red to show the
flip; this fixture stages the tree (`ctx.git_add`) so P9 is green and the flip is P7 alone.

  p7m39-s105-two-source-lines  the entry's S105 `source:` line is followed by a second
                               `source: S105` line citing a different pinned-raw path. The
                               reference `c_provenance` builds `prov["S105"] == [pinned, other]`,
                               which is not `[pinned]`, so it prints `P7 DEFECT`; M04 reads only
                               element 0 and prints `P7 ok`. Declared defect set `["P7"]`.

Everything else in the genuine round-35 package is untouched, so the reference exit code is 1
(reject) with no other DEFECT clause.
"""

SID = "S105"
SECOND_FILE_ROW = "S107"


def _package(ctx, d, edit):
    """Build the genuine package, apply one entry edit, stage the tree, return the gate argv tail."""
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
        other = ctx.spec["raw_base"] + ctx.spec["rows"][SECOND_FILE_ROW]["upstream"]
        if pinned == other:
            raise RuntimeError("second source url must differ from the pinned one")
        second = (f"source: {SID} \u2014 {other} \u2014 second source line for the same row, "
                  f"planted by battery39 p7m39")
        i = hits[0]
        return "\n".join(lines[:i + 1] + [second] + lines[i + 1:]) + "\n"
    return _package(ctx, d, edit)


FIXTURES = [
    {"fid": "p7m39-s105-two-source-lines", "expect": "reject", "defects": ["P7"],
     "build": _two_source_lines},
]
