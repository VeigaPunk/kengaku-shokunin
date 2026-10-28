"""Round-48 C1 honest class `n01_packed_refs_gc`: packed refs after `pack-refs` / `gc`.

Rebuilt from the round-46 wave-2 report `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest
classes, refused 9/9 by the base fence at `0f77f9b`): "packed refs after `gc`/`pack-refs`". A repository
whose refs have been packed is an ordinary state that ordinary `git init` + commits + `git pack-refs`
produces; every byte it writes is inside `d` and no store path is redirected.

Authored against the BASE fence description only (`plans/fixture_fence.py` at round-48 stage-1 freeze
`a543d920`, sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` as pinned by this
population's builder), never against a repaired fence.

Contract (round-44 builder, unchanged): one fixture; `build(ctx, d)` fills the empty directory `d` and
returns the tool argv tail. `anchor` argv is the tool's own shape with a relative value inside `d`, so the
fixture carries no absolute scratch path. `expect`/`defects` are None: this module feeds the fence's HONEST
leg, it declares no tool-behaviour expectation.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "README.md", "# packed refs\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "first")
    ctx.git(r, "tag", "light")
    ctx.git(r, "pack-refs", "--all", "--prune")
    ctx.write(r / "second.txt", "second line\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "second")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n01-packed-refs", "tool": "anchor", "expect": None, "defects": None, "build": build}]
