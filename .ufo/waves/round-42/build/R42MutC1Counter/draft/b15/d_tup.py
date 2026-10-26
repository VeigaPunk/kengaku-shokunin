"""Draft control D15 (R42MutC1Counter): build() must return a list of str (first type-check layer).
This build returns a tuple. JSON erases the distinction, so only the first layer can catch it: the intact
counter fails the module build (SETUP, exit 2); a counter with that check disabled accepts the fixture."""
def b(ctx, d):
    import hashlib as _h
    r = ctx.init(d / "repo")
    body = b"d15 capture body\n"
    base = r / "corpus/evidence/round41/d15"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "SHA256SUMS", _h.sha256(body).hexdigest() + "  test_outputs.py\n")
    hdr = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
           "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
    ctx.write(r / "corpus/SOURCES.md", hdr +
              "| S961 | capture at corpus/evidence/round41/d15/test_outputs.py | code | A | fixture | sha256 "
              + _h.sha256(body).hexdigest() + " | draft row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ("--lane", str(r))

FIXTURES = [{"fid": "d15-tuple", "tool": "anchor", "expect": "accept", "defects": [], "build": b}]
