"""Scratch battery for the R43PlanNext pricing run: one fixture per unlisted advertised behaviour, each built
from nothing. Not a lane battery."""
import hashlib

HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n")
BODY = b"price probe capture one\n"
DIG = hashlib.sha256(BODY).hexdigest()


def row(sid, source, anchor):
    cells = [sid, source, "docs", "A", "scope", anchor, "teaches", "mined", "2026-10-26", "2027-01-24",
             "corpus/knowledge/x.md"]
    return "| " + " | ".join(cells) + " |\n"


def lane(ctx, d, source, anchor, caps=None, lessons=None, dirty=None):
    r = ctx.init(d / "lane")
    for rel, body in (caps or {"corpus/evidence/r1/cap.txt": BODY}).items():
        ctx.write(r / rel, body)
    ctx.write(r / "corpus/SOURCES.md", HEAD + row("S901", source, anchor))
    for rel, body in (lessons or {}).items():
        ctx.write(r / rel, body)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    for rel, body in (dirty or {}).items():
        ctx.write(r / rel, body)
    return ["--lane", str(r)]


P1 = "corpus/evidence/r1/cap.txt"


def u3_row_path(ctx, d):
    return lane(ctx, d, P1, "anchor sha256 " + DIG)


def u5_short(ctx, d):
    return lane(ctx, d, P1, "anchor sha256 " + DIG[:63])


def u6_long(ctx, d):
    return lane(ctx, d, P1, "anchor sha256 " + DIG + "a")


def u7_twin_captures(ctx, d):
    caps = {P1: BODY, "corpus/evidence/r1/twin.txt": BODY}
    return lane(ctx, d, P1 + " and corpus/evidence/r1/twin.txt", "anchor sha256 " + DIG, caps=caps)


def u9_dirty_erratum(ctx, d):
    wrong = "e" * 64
    note = f"Erratum (round 37): S901 anchor sha256 {wrong} corrected to sha256 {DIG}\n"
    return lane(ctx, d, P1, "anchor sha256 " + wrong, lessons={"corpus/lessons/l.md": "# lessons\n"},
                dirty={"corpus/lessons/l.md": "# lessons\n" + note})


FIXTURES = [
    {"fid": "u3-row-path-binds", "tool": "anchor", "expect": "accept", "defects": [], "build": u3_row_path},
    {"fid": "u5-sixty-three-hex", "tool": "anchor", "expect": "reject", "defects": ["digest-short"], "build": u5_short},
    {"fid": "u6-sixty-five-hex", "tool": "anchor", "expect": "reject", "defects": ["digest-long"], "build": u6_long},
    {"fid": "u7-twin-captures", "tool": "anchor", "expect": "accept", "defects": [], "build": u7_twin_captures},
    {"fid": "u9-dirty-erratum", "tool": "anchor", "expect": "accept", "defects": [], "build": u9_dirty_erratum},
]
