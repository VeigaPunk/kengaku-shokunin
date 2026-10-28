"""Round-50 C1 NEW honest class `n22_alternates_in_d`: a repository whose object store borrows from another
object store that is inside the same fixture directory.

`objects/info/alternates` is a documented git mechanism (`gitrepository-layout(5)`: each line names another
object directory). The base fence refuses the file by name ("object-store redirect") without resolving the
target, so an alternates entry that stays inside `d` is over-refused exactly like the out-of-`d` case the
round-44 refusal module `f5_alternates.py` builds. This class is the matching honest counterpart:

  main/   a plain-init repository holding the borrowed commit
  lane/   a plain-init repository whose objects/info/alternates reads `../../../main/.git/objects`
          (relative to `lane/.git/objects`; git resolves it — `git fsck --strict` exits 0 and
          `git cat-file -p <main commit>` resolves the borrowed object)

Deterministic: the entry is relative, so no build path enters the tree, and the rest is two plain inits. The
only volatile entries are the two `.git/index` stat caches, which the population builder masks at any depth.
The borrow is acyclic here (lane borrows from main; main borrows nothing).

Round-44 builder contract: `build(ctx, d)` fills `d`, returns the argv tail.
"""


def build(ctx, d):
    main = ctx.init(d / "main")
    ctx.write(main / "m.txt", "borrowed\n")
    ctx.git(main, "add", "-A")
    ctx.git(main, "commit", "-q", "-m", "store")
    lane = ctx.init(d / "lane")
    ctx.write(lane / ".git/objects/info/alternates", "../../../main/.git/objects\n")
    ctx.write(lane / "l.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "local")
    return ["--lane", "lane"]


FIXTURES = [{"fid": "n22-alternates-in-d", "tool": "anchor", "expect": None, "defects": None, "build": build}]
