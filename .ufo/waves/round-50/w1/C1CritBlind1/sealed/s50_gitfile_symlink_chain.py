"""R50-C1 blind sealed module (seat `R50C1CritBlind1`, wave `round-50/w1`): the store is named by a `.git`
FILE whose target is a chain of two relative symlinks that ends OUTSIDE `d`.

Shape. `d/.git` holds `gitdir: hop1`. `hop1` is a symlink to `hop2`; `hop2` is a symlink to `../gitdir`, a
sibling of `d`. The gitfile text is a bare relative name: no `..`, no absolute component, no separator that a
lexical test could object to. So every check that classifies the *text* — `startswith(str(d))`, `normpath` +
prefix, `purelib.Path(line).is_relative_to(d)` without `resolve()` — sees a store inside `d`. Only following the
chain (`realpath`) reaches the outside store, and `git -C d rev-parse --absolute-git-dir` prints that outside
path, so a tool run behind the fence reads outside `d` (the round-46 B3/B5 property) whenever this fixture is
admitted.

Expected refusal: the store the gitfile names resolves outside `d`. A repair that admits the `n21`/`n20` shapes
by parsing the pointer must refuse this one; refusing every `.git`-is-a-file is a refusal too. Admission by any
pointer-only repair is the leak this module exists to catch.
"""
import pathlib
import shutil

CLAIMS = "claims.md"
RECEIPT = "evidence/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    r = ctx.init(d)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    shutil.move(str(r / ".git"), str(d.parent / "gitdir"))
    (d / "hop2").symlink_to("../gitdir")
    (d / "hop1").symlink_to("hop2")
    ctx.write(d / ".git", "gitdir: hop1\n")
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "s50-gitfile-symlink-chain", "tool": "order", "expect": "error", "defects": [], "build": build}]
