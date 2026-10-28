"""Round-49 C1 NEW honest class `n18_shallow_fetch`: a `.git/shallow` boundary from `git fetch --depth 1`.

New in round 49 (not one of the nine round-46 classes nor the seven round-48 ones). A shallow store is the state
`git clone --depth N` leaves: `.git/shallow` names the boundary commit, the history behind it is absent by
design, and the shallow markers are what `git log`/`fsck` read to stop there. This fixture reaches that state
without a network remote and without an absolute path in the tree: the source repository lives inside the same
fixture dir `d`, is registered as `origin` under the sibling-relative path `../src`, and is fetched with `--depth 1`, so
every byte read and written is inside `d` and `.git/config` records `url = ../src` (git resolves a relative
remote URL against the directory it runs in, which is the repository itself).

`git clone --no-local src repo` was the first shape tried and is rejected here: git rewrites the local source to
an absolute path, so `.git/config` and all three reflogs would carry the build's scratch path and no two builds
could share an identity. `git clone --depth` alone is rejected for the same reason plus the local-transport
depth caveat; the fetch shape keeps the shallow state and stays reproducible.

Not a partial (promisor/filtered) clone: a `--filter=blob:none` clone omits blobs, `git fsck --strict` reports
them missing, and the result is not a self-contained repository this population can call honest. The shallow
boundary is the part of "shallow partial clone" that is self-contained.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ round-49 stage-1 freeze
`9d2900af`, sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` as pinned by this
population's builder), never against a repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and
returns the argv tail.
"""


def build(ctx, d):
    src = ctx.init(d / "src")
    for name, body in (("a.txt", "one\n"), ("b.txt", "two\n"), ("c.txt", "three\n")):
        ctx.write(src / name, body)
        ctx.git(src, "add", "-A")
        ctx.git(src, "commit", "-q", "-m", f"add {name}")
    repo = d / "repo"
    ctx.sh("git", "init", "-q", "-b", "master", "repo", cwd=d)
    ctx.git(repo, "remote", "add", "origin", "../src")
    ctx.git(repo, "fetch", "-q", "--depth", "1", "origin", "master")
    ctx.git(repo, "reset", "-q", "--hard", "FETCH_HEAD")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n18-shallow-fetch", "tool": "anchor", "expect": None, "defects": None, "build": build}]
