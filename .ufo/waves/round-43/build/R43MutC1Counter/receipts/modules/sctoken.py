"""Draft control `sctoken` (seat R43MutC1Counter) — the SIDECHANNEL token scan must fire on a token alone.

This module imports nothing unusual; the token `psutil` appears in a comment only. The scan is a heuristic
over the module's lowercase source, so a bare mention must flag it:
  pristine counter -> `SIDECHANNEL <dir>/sctoken.py tokens=psutil` and `BATTERY ... sidechannel=1`
  M13 counter (if hits: -> if False:) -> no SIDECHANNEL line, sidechannel=0.
"""

def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/SOURCES.md",
              "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
              "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n"
              "| S905 | captured at corpus/evidence/round43/sc/notes.txt | capture | A | fixture-scalar | - "
              "| green lane for the token scan | mined | 2026-10-26 | 180d | - |\n")
    ctx.write(r / "corpus/evidence/round43/sc/notes.txt", b"capture\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "green lane; the token lives in this docstring only")
    return ["--lane", str(r)]


FIXTURES = [{"fid": "sc-green", "tool": "anchor", "expect": "accept", "defects": [], "build": build}]
