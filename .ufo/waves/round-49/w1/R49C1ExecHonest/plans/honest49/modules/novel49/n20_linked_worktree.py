"""Round-49 C1 NEW honest class `n20_linked_worktree`: a linked worktree whose `.git` is a file.

New in round 49 (not one of the nine round-46 classes nor the seven round-48 ones). `git worktree add` is an
ordinary way to check out a second branch: the added directory carries a `.git` *file* (`gitdir: …`) instead of
a `.git` directory, and its metadata lives under the main repository's `.git/worktrees/<name>`. `--relative-paths`
(git 2.48+) writes that `gitdir:` line and the back-pointer relative to each other, so the fixture holds no
absolute path and is reproducible; every byte, including the main store and the worktree metadata, is inside `d`.

This is the class the round-49 item allowed the seat to refuse if it could not be built honestly; measured (see
the seat report) it builds deterministically once its one volatile file is excluded: `.git/worktrees/wt/index`
is the per-worktree stat cache (a second `.git/index`, caching inode/mtime data), the only entry that differed
between two builds. The population builder masks it for that measured reason, narrowly (`*.git/worktrees/*/index`,
never the store content); every other entry, including `wt/.git`, `worktrees/wt/gitdir` and `commondir`, is
byte-stable. With that one mask the class keeps `rev-parse --show-toplevel` true for the main repository and
exits 0 under `git fsck --strict`, so it is kept rather than refused.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ round-49 stage-1 freeze
`9d2900af`, sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` as pinned by this
population's builder), never against a repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and
returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "branch", "feature")
    ctx.git(r, "worktree", "add", "--relative-paths", "-q", "../wt", "feature")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n20-linked-worktree", "tool": "anchor", "expect": None, "defects": None, "build": build}]
