"""Round-38 battery38 module `p7m`: the two P7 (provenance) branches battery37 leaves unproven.

Both fixtures start from the genuine round-35 package (`ctx.genuine_package`) and edit only the
entry `corpus/knowledge/tb2-protein-assembly-grader.md`, then stage the tree (`ctx.git_add`) so P9
(clean tree) stays green. Each edit breaks exactly one P7 branch and nothing else, so the declared
defect set is `["P7"]`: what the UNMODIFIED gate prints on that tree.

  p7m-n11-empty-recheck  `recheck:` line kept but emptied and moved to the end of the entry
                         -> N11 (regex loses its `\\s*\\S` value requirement). The line must end
                         the file: `^recheck:\\s*\\S` lets `\\s*` cross newlines, so an empty
                         `recheck:` followed by any later non-blank line would still match, and
                         the reference would print P7 `ok` (no silence kill).
  p7m-n12-first-row-url  the FIRST registry row's `source:` URL (S105) changed
                         -> N12 (the per-row loop starts at the second row). battery37 p7 defaces
                         the second row (S106); this one defaces S105, which N12 skips.
"""

FIRST_ROW_URL = "protein-assembly/tests/test_outputs.py"
BROKEN_FIRST_URL = "protein-assembly/tests/test_other_outputs.py"
RECHECK = "recheck:"


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


def _only_once(text, needle):
    if text.count(needle) != 1:
        raise RuntimeError(f"expected exactly one {needle!r}, found {text.count(needle)}")
    return text


def _n11(ctx, d):
    def edit(text):
        _only_once(text, RECHECK)
        lines = text.splitlines()
        kept = [l for l in lines if not l.startswith(RECHECK)]
        if len(kept) != len(lines) - 1:
            raise RuntimeError(f"expected exactly one line starting {RECHECK!r}")
        # the empty recheck line must be the last line: `^recheck:\s*\S` would otherwise match
        # by letting \s* cross the newline into a later non-blank line.
        return "\n".join(kept + [RECHECK]) + "\n"
    return _package(ctx, d, edit)


def _n12(ctx, d):
    def edit(text):
        _only_once(text, FIRST_ROW_URL)
        return text.replace(FIRST_ROW_URL, BROKEN_FIRST_URL, 1)
    return _package(ctx, d, edit)


FIXTURES = [
    {"fid": "p7m-n11-empty-recheck", "expect": "reject", "defects": ["P7"], "build": _n11},
    {"fid": "p7m-n12-first-row-url", "expect": "reject", "defects": ["P7"], "build": _n12},
]
