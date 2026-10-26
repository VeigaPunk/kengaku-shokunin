"""Draft control D5 (R42MutC1Counter): a silence kill must be on a class the fixture declares.
The repo's census row cites a made-up digest, so the reference prints class=digest-unknown, but the fixture
declares no defects at all. The intact counter must not count X7; a counter that drops the declared-defects
conjunct counts an undeclared kill."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    import hashlib as _h
    body = b"d5 capture body\n"
    (d / "repo").mkdir(parents=True, exist_ok=True)
    r = ctx.init(d / "repo")
    base = r / "corpus/evidence/round41/d5"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "SHA256SUMS", _h.sha256(body).hexdigest() + "  test_outputs.py\n")
    bogus = _h.sha256(b"d5 made-up token\n").hexdigest()
    hdr = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
           "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
    ctx.write(r / "corpus/SOURCES.md", hdr +
              "| S950 | capture at corpus/evidence/round41/d5/test_outputs.py | code | A | fixture | sha256 "
              + bogus + " | draft row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", str(r)]

FIXTURES = [{"fid": "d5-undeclared", "tool": "anchor", "expect": "reject", "defects": [], "build": b}]
