"""Scratch true-positive control: two fixtures that are re-spellings of witness u5_short and u7_twin_captures
(locals renamed, docstring changed, constant formatting changed) — the screen must flag both near 1.0."""
import hashlib

HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n")
PAYLOAD = b"price probe capture one\n"
HEX = hashlib.sha256(PAYLOAD).hexdigest()


def row(sid, source, anchor):
    cells = [sid, source, "docs", "A", "scope", anchor, "teaches", "mined", "2026-10-26", "2027-01-24",
             "corpus/knowledge/x.md"]
    return "| " + " | ".join(cells) + " |\n"


def lane(ctx, d, source, anchor, caps=None, lessons=None, dirty=None):
    r = ctx.init(d / "lane")
    for rel, body in (caps or {"corpus/evidence/r1/cap.txt": PAYLOAD}).items():
        ctx.write(r / rel, body)
    ctx.write(r / "corpus/SOURCES.md", HEAD + row("S901", source, anchor))
    for rel, body in (lessons or {}).items():
        ctx.write(r / rel, body)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    for rel, body in (dirty or {}).items():
        ctx.write(r / rel, body)
    return ["--lane", str(r)]


def rs_short(ctx, d):
    """Sixty-three hex characters, re-spelled: renamed nothing, reformatted constant."""
    return lane(ctx, d, "corpus/evidence/r1/cap.txt", "anchor sha256 " + HEX[:63])


def rs_twin(ctx, d):
    caps = {"corpus/evidence/r1/cap.txt": PAYLOAD, "corpus/evidence/r1/twin.txt": PAYLOAD}
    return lane(ctx, d, "corpus/evidence/r1/cap.txt and corpus/evidence/r1/twin.txt",
                "anchor sha256 " + HEX, caps=caps)


FIXTURES = [
    {"fid": "rs-short", "tool": "anchor", "expect": "reject", "defects": ["digest-short"], "build": rs_short},
    {"fid": "rs-twin", "tool": "anchor", "expect": "accept", "defects": [], "build": rs_twin},
]
