"""battery40/a_tok.py — anchor-tool token-shape fixtures.

One fixture per advertised token behaviour of `plans/anchor_digest_check.py`: the strict 64-hex shape
(`digest-uppercase`), and the 8-63 lowercase-hex abbreviation window (floor and ceiling). Each fixture
edits one existing `corpus/SOURCES.md` anchor claim in the working tree of a fresh `--shared` clone; the
tool reads SOURCES.md from the working tree and evidence from HEAD, so no commit is needed.
"""

import hashlib

SOURCES = "corpus/SOURCES.md"
STREAM = "corpus/evidence/attrib-r23-stream.log"
# the S111 anchor digest at HEAD (row `| S111 |`, corpus/SOURCES.md)
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
# the S036 abbreviation at HEAD (row `| S036 |`, corpus/SOURCES.md)
ABBREV = "sha256 afaae9dd…"


def _edit(lane, old, new):
    """Replace exactly one occurrence of `old` in the clone's work-tree SOURCES.md; return the tool argv."""
    p = lane / SOURCES
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"SOURCES.md holds {text.count(old)} copies of the token to rewrite, not 1")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return ["--lane", str(lane)]


def build_upper(ctx, d):
    """A 64-character anchor token in uppercase: the shape test is lowercase-only, so it is digest-uppercase."""
    lane = ctx.clone(d / "lane")
    return _edit(lane, "sha256 " + S111, "sha256 " + S111.upper())


def build_abbrev_floor(ctx, d):
    """A 7-hex abbreviation (`afaae9d…`) that does resolve as a prefix: below the 8-hex floor."""
    lane = ctx.clone(d / "lane")
    return _edit(lane, ABBREV, "sha256 afaae9d…")


def build_abbrev_ceiling(ctx, d):
    """A full 64-hex digest followed by `…`: an abbreviation may not be 64 hex (8-63 only)."""
    lane = ctx.clone(d / "lane")
    digest = hashlib.sha256((lane / STREAM).read_bytes()).hexdigest()
    return _edit(lane, ABBREV, "sha256 " + digest + "…")


FIXTURES = [
    {"fid": "a_tok-upper-anchor", "tool": "anchor", "expect": "reject",
     "defects": ["digest-uppercase"], "build": build_upper},
    {"fid": "a_tok-abbrev-7hex", "tool": "anchor", "expect": "reject",
     "defects": ["abbrev-unresolved"], "build": build_abbrev_floor},
    {"fid": "a_tok-abbrev-64hex", "tool": "anchor", "expect": "reject",
     "defects": ["abbrev-unresolved"], "build": build_abbrev_ceiling},
]
