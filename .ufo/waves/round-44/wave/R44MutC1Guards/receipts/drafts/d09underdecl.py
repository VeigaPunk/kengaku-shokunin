"""Draft control `d9underdecl` (seat R44MutC1Guards) — the `cls in fx["defects"]` conjunct of `exhibits`
(silence direction) red control.

An anchor fixture whose reference prints `digest-short` but which declares `defects: []` (an
under-declaration; the counter marks the fixture WRONG). The silence direction must not count a kill on a
class the fixture does not declare:
  pristine counter --only U5 -> `MUTANT U5 ... SURVIVED exhibits=none` (undeclared class cannot kill)
  M09 counter                 -> `MUTANT U5 ... killed by=d9-underdeclared` (conjunct dropped).
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
BODY = b"capture for the under-declared row\n"
DIG = hashlib.sha256(BODY).hexdigest()


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/evidence/r1/cap.txt", BODY)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + "| S912 | captured at corpus/evidence/r1/cap.txt | capture | A | fixture-scalar "
              f"| sha256 {DIG[:63]} | under-declared row | mined | 2026-10-26 | 180d | - |\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "a row whose fixture under-declares its defect")
    return ["--lane", str(r)]


FIXTURES = [{"fid": "d9-underdeclared", "tool": "anchor", "expect": "reject", "defects": [], "build": build}]
