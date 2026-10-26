"""Draft control `wrongdecl` (seat R43MutC1Counter) — the `cls in fx["defects"]` conjunct of `exhibits`.

An anchor fixture whose reference prints `row-malformed` but which declares `defects: []` (an
under-declaration; the counter marks the fixture WRONG). The silence direction must not count a kill on a
class the fixture does not declare:
  pristine counter --only NA1 -> `MUTANT NA1 ... SURVIVED` (undeclared class cannot kill)
  M09 counter                 -> `MUTANT NA1 ... killed` (conjunct dropped: kill on an undeclared class).
"""
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/evidence/round43/wd/notes.txt", b"capture for the under-declared row\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + "| S906 | captured at corpus/evidence/round43/wd/notes.txt | capture | A | fixture-scalar "
              "| - | probe row | mined | 2026-10-26 | 180d | - | extra |\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "a 12-cell row whose fixture under-declares its defect")
    return ["--lane", str(r)]


FIXTURES = [{"fid": "wd-underdeclared", "tool": "anchor", "expect": "reject", "defects": [], "build": build}]
