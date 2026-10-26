"""Attack probe: a staged manifest entry that contradicts the committed capture bytes."""
import hashlib

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def dh(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def row(sid, source, tok):
    return (f"| {sid} | {source} | code | A | fixture | sha256 {tok} | note | mined | "
            "2026-10-26 | 180d | corpus/knowledge/x.md |")


def f(ctx, d):
    r = ctx.init(d / "repo")
    body = b"lambda body\n"
    base = r / "corpus/evidence/r13b"
    ctx.write(base / "file.txt", body)
    ctx.write(base / "SHA256SUMS", f"{dh(body)}  file.txt\n")
    made = dh(b"a value committed nowhere\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S931", "capture at corpus/evidence/r13b/file.txt", made) + "\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    ctx.write(base / "SHA256SUMS", f"{made}  file.txt\n")
    ctx.git(r, "add", "corpus/evidence/r13b/SHA256SUMS")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "p-x13-staged-manifest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown"], "build": f},
]
