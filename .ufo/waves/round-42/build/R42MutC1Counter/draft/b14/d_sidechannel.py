"""Draft control D14 (R42MutC1Counter): the battery token scan must fire.
This docstring deliberately carries the banned token: witness. The intact counter prints a SIDECHANNEL
line, sidechannel=1 and exits 1; a counter with the scan disabled prints sidechannel=0 and exits 0."""
def b(ctx, d):
    import hashlib as _h
    r = ctx.init(d / "repo")
    body = b"d14 capture body\n"
    base = r / "corpus/evidence/round41/d14"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "SHA256SUMS", _h.sha256(body).hexdigest() + "  test_outputs.py\n")
    hdr = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
           "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
    ctx.write(r / "corpus/SOURCES.md", hdr +
              "| S960 | capture at corpus/evidence/round41/d14/test_outputs.py | code | A | fixture | sha256 "
              + _h.sha256(body).hexdigest() + " | draft row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", str(r)]

FIXTURES = [{"fid": "d14-clean", "tool": "anchor", "expect": "accept", "defects": [], "build": b}]
