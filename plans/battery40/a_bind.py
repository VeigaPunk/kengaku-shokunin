"""battery40 module `a_bind` (seat R40BatAnchorBind): three anchor fixtures, one advertised behaviour each.

  a_bind-a27-token-per-capture  a row that adds a second pinned locator beside its own must carry a token for
                                each capture; the capture no token resolves is `capture-unanchored` (A27, silence:
                                the unmodified tool prints the class and exits 1, the mutant exits 0).
  a_bind-a15-slug-ambiguity     two committed `task.toml` files naming one task slug bind nothing, so the row's
                                token is `anchor-unbound` (A15, rc-silence: reference exits 1, the mutant binds
                                the first owner and exits 0).
  a_bind-a17-index-bytes        `--evidence-ref index` reads the staged bytes, not HEAD's (A17, rc-mirror: the
                                reference accepts a token for the staged capture, the mode-swapped mutant calls
                                it `digest-unknown` and exits 1).
"""
import hashlib
import pathlib

S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
URL = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/" + PIN + "/%s"
ROW = ("| %s | Terminal-Bench 2.0 binder fixture — %s | code | A | the row's own capture set, one token per "
       "capture | commit %s, sha256 %s | fixture row | mined | 2026-10-26 | 180d | corpus/knowledge/a-bind.md |")


def digest(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def find_row(text, sid):
    for i, line in enumerate(text.split("\n")):
        if line.startswith("| " + sid + " "):
            return i
    raise AssertionError("no row " + sid)


def with_row(text, row):
    lines = text.rstrip("\n").split("\n")
    lines.insert(find_row(text, "S111") + 1, row)
    return "\n".join(lines) + "\n"


def capture(lane, name, body, slug):
    cap = lane / "corpus/evidence" / name
    cap.mkdir(parents=True)
    (cap / "test_outputs.py").write_text(body)
    h = digest(cap / "test_outputs.py")
    (cap / "SHA256SUMS").write_text(h + "  test_outputs.py\n")
    (cap / "task.toml").write_text('name = "harbor/' + slug + '"\n')
    return cap, h


def build_a27(ctx, d):
    # S111 keeps its own URL and gains a second one (regex-log) while its token becomes S108's: the git-webserver
    # capture is named and unclaimed, the shape round 39 closed for the additive route.
    lane = ctx.clone(d / "lane")
    p = lane / "corpus/SOURCES.md"
    text = p.read_text()
    lines = text.split("\n")
    i = find_row(text, "S111")
    assert lines[i].count("sha256 " + S111) == 1
    cells = lines[i].replace("sha256 " + S111, "sha256 " + S108).split("|")
    cells[2] = cells[2].rstrip() + " " + (URL % "regex-log/tests/test_outputs.py") + " "
    lines[i] = "|".join(cells)
    p.write_text("\n".join(lines))
    return ["--lane", str(lane)]


def build_a15(ctx, d):
    # Two committed task.toml files claim one slug; the row's token is the alphabetically first owner's digest,
    # which is what the ambiguous-slug mutant binds.
    lane = ctx.clone(d / "lane")
    _, ha = capture(lane, "roundX/tb2-amb-a", "assert True  # a_bind first owner\n", "amb-bind-task")
    capture(lane, "roundX/tb2-amb-b", "assert True  # a_bind second owner\n", "amb-bind-task")
    ctx.git(lane, "add", "-A", "corpus/evidence")
    ctx.git(lane, "commit", "-q", "-m", "a_bind: two task dirs claiming one slug")
    p = lane / "corpus/SOURCES.md"
    p.write_text(with_row(p.read_text(),
                          ROW % ("S902", URL % "amb-bind-task/tests/test_outputs.py", PIN, ha)))
    return ["--lane", str(lane)]


def build_a17(ctx, d):
    # The capture is committed with one body, then rewritten and staged with another; the row claims the staged
    # digest and is read in index mode, so only a tool that reads index blobs can accept it.
    lane = ctx.clone(d / "lane")
    cap, _ = capture(lane, "roundX/tb2-idx", "assert True  # a_bind committed view\n", "idx-bind-task")
    ctx.git(lane, "add", "-A", "corpus/evidence")
    ctx.git(lane, "commit", "-q", "-m", "a_bind: committed view of the capture")
    (cap / "test_outputs.py").write_text("assert True  # a_bind staged view\n")
    hb = digest(cap / "test_outputs.py")
    (cap / "SHA256SUMS").write_text(hb + "  test_outputs.py\n")
    ctx.git(lane, "add", "-A", "corpus/evidence")
    p = lane / "corpus/SOURCES.md"
    p.write_text(with_row(p.read_text(),
                          ROW % ("S903", URL % "idx-bind-task/tests/test_outputs.py", PIN, hb)))
    return ["--lane", str(lane), "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "a_bind-a27-token-per-capture", "tool": "anchor", "expect": "reject",
     "defects": ["capture-unanchored"], "build": build_a27},
    {"fid": "a_bind-a15-slug-ambiguity", "tool": "anchor", "expect": "reject",
     "defects": ["anchor-unbound"], "build": build_a15},
    {"fid": "a_bind-a17-index-bytes", "tool": "anchor", "expect": "accept",
     "defects": [], "build": build_a17},
]
