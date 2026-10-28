"""R50-C1 blind hostile module B7-b (seat `R50C1CritBlind7`, wave `round-50/w1`): the `.git` FILE names a store
whose PATH is reached through a SYMLINKED PARENT directory inside `d` — the store itself is a real directory.

Shape, inside the fixture dir `d`:

  d/lane/.git              a FILE, one line: `gitdir: ../alias/gitstore`
  d/alias                  a SYMLINK -> `rho/hold` (relative; parent and target both inside `d`)
  d/rho/hold/gitstore/     the store: a real directory, plain-init entries only, no symlink of its own
  d/lane/work.txt          committed worktree content

Distinct from B7-a by one component: there the FINAL component of the gitfile target is the symlink (a fence
that only lstats the store directory it resolves sees a symlink and refuses); here the final component
`gitstore` is a real directory and only its PARENT `alias` is a symlink. A half-repair that resolves the
gitfile, checks containment, and lstat-checks the resolved store ("the store must not be a symlink") therefore
passes every check it makes and admits this fixture, while B7-a is caught by it. The pair separates
"store is a symlink" from "store is reached through a symlink", which is the exact distinction the advertised
policy does not make: the walk refuses a symlink ANYWHERE in the fixture.

Both containment answers pass, as in B7-a: `d/lane/../alias/gitstore` is lexically inside `d` and resolves to
`d/rho/hold/gitstore`, also inside `d`. So the refusal has to rest on the symlink, not on containment.

Material, not cosmetic: `git -C lane rev-parse --absolute-git-dir` answers `d/rho/hold/gitstore` (resolved) and
`git -C lane rev-parse HEAD` succeeds, so the repository is live and a tool behind an admitting fence reads a
store whose real path the fixture text never names.

Distinct from the landed sealed set: `s50_gitfile_symlink_chain` chains two symlinks that end OUTSIDE `d`
(there containment is the argument); `s6_gitfile_rel_objects_link` symlinks `objects` inside a real store and
sends it outside `d`. No landed module puts a symlink in an intermediate component of a gitfile target that
resolves INSIDE `d`.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    lane = d / "lane"
    store = d / "rho" / "hold" / "gitstore"
    store.parent.mkdir(parents=True, exist_ok=True)
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(lane))
    (d / "alias").symlink_to("rho/hold", target_is_directory=True)
    ctx.write(lane / ".git", "gitdir: ../alias/gitstore\n")
    ctx.write(lane / "work.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "one")
    ctx.write(lane / RECEIPT, "receipt\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "receipt")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "b7b-gitfile-symlinked-parent-inside-d", "tool": "order", "expect": "reject", "defects": [],
             "build": build}]
