"""Round-50 C1 NEW honest class `n21_separate_gitdir`: a repository whose `.git` is a file pointing at a store
inside the same fixture directory.

`git init --separate-git-dir` is a documented git invocation (`git-init(1)`); the work tree carries a `.git`
*file* whose single line is `gitdir: <path>` and the store lives elsewhere. Written naively the pointer is
absolute and no two builds can share an identity, so the build rewrites that one line to a path relative to the
work tree before the first commit — the shape git itself accepts and resolves (`git -C wt rev-parse
--absolute-git-dir` returns the store). Everything the fence must classify is inside `d`:

  wt/.git            `gitdir: ../store`   (a file, refused by the base fence's blanket rule)
  store/             a plain-init store: HEAD, config (no absolute path), refs/, logs/, objects/, index

The base fence refuses this class because any `.git` file is refused as a "gitdir redirect"; the resolved target
is inside the fixture, so that refusal is over-refusal. The class is distinct from `n20_linked_worktree` (a
worktree store under `repo/.git/worktrees/<name>` with `commondir`) and from `n22_alternates_in_d` (an object
store borrowed by pointer): here the whole store is a sibling directory, named by the gitfile.

Deterministic: `core.worktree` is not written by `git init --separate-git-dir` (measured), the rewritten gitfile
is relative, and the store's bytes are a plain init. The only volatile entry is `store/index`, the stat cache
the population builder masks at any depth.

Round-44 builder contract: `build(ctx, d)` fills `d`, returns the argv tail.
"""


def build(ctx, d):
    wt = d / "wt"
    store = d / "store"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    ctx.write(wt / ".git", "gitdir: ../store\n")
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / "b.txt", "two\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "two")
    return ["--lane", "wt"]


FIXTURES = [{"fid": "n21-separate-gitdir", "tool": "anchor", "expect": None, "defects": None, "build": build}]
