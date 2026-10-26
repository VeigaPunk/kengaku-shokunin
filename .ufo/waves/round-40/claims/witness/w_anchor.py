"""Pre-freeze direction witness (round 40, L1): A27 capture-unanchored. Not a battery40 module; the counter reads
it only when pointed here with --battery-dir (development, predicate n/a)."""
import re

S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
URL2 = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
        "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")


def second_url(ctx, d):
    lane = ctx.clone(d / "lane")
    p = lane / "corpus/SOURCES.md"
    lines = p.read_text().split("\n")
    hit = [i for i, l in enumerate(lines) if re.match(r"^ {0,3}\|\s*S111\s*\|", l)]
    assert len(hit) == 1 and lines[hit[0]].count("sha256 " + S111) == 1
    cells = lines[hit[0]].replace("sha256 " + S111, "sha256 " + S108).split("|")
    cells[2] = cells[2].rstrip() + " " + URL2 + " "
    lines[hit[0]] = "|".join(cells)
    p.write_text("\n".join(lines))
    return ["--lane", str(lane)]


def tip(ctx, d):
    return ["--lane", str(ctx.clone(d / "lane"))]


FIXTURES = [
    {"fid": "w-a27-second-url", "tool": "anchor", "expect": "reject", "defects": ["capture-unanchored"],
     "build": second_url},
    {"fid": "w-anchor-tip", "tool": "anchor", "expect": "accept", "defects": [], "build": tip},
]
