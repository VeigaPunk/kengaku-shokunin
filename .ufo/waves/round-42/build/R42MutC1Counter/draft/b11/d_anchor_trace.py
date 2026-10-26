"""Draft control D11 (R42MutC1Counter): a traced re-run that does not reproduce must stay unattributed.
The fixture is a 10-cell census row (reference exits 1). The TR1 mutant (added by the control patch) exits 0
untraced but raises SystemExit(2) when a tracer is attached, so the traced re-run diverges: the intact
counter prints UNATTRIBUTED; a counter that drops the reproduce conjunct prints an attributed kill."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    import hashlib as _h
    body = b"d11 capture body\n"
    base = r / "corpus/evidence/round41/d11"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "SHA256SUMS", _h.sha256(body).hexdigest() + "  test_outputs.py\n")
    hdr = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
           "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
    full = ("| S951 | capture at corpus/evidence/round41/d11/test_outputs.py | code | A | fixture | sha256 "
            + _h.sha256(body).hexdigest() + " | draft row | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |")
    cells = full.split("|")
    ctx.write(r / "corpus/SOURCES.md", hdr + "|".join(cells[:-2]) + "|\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", str(r)]

FIXTURES = [{"fid": "d11-shortrow", "tool": "anchor", "expect": "reject", "defects": [], "build": b}]
