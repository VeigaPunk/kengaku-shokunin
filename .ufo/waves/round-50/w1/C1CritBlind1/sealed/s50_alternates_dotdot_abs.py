"""R50-C1 blind sealed module (seat `R50C1CritBlind1`, wave `round-50/w1`): `objects/info/alternates` names an
object store with an ABSOLUTE path that starts inside `d` and leaves it through `..`.

Shape. The line is `<d>/lane/.git/objects/../../../../store/.git/objects`, which is absolute, starts with the
fixture directory, and has no symlink component: four `..` segments climb `objects -> .git -> lane -> d` and the
tail re-enters a sibling of `d`. Any test that reads the raw line (`line.startswith(str(d))`, `str(d) in line`)
admits it, and `pathlib.Path(line).is_relative_to(d)` also admits it because `PurePath` never collapses `..`.
The target store is real and holds the only commit the lane's HEAD does not contain, so `git -C lane cat-file`
reads an object that exists nowhere inside `d` whenever this fixture is admitted.

Expected refusal: an alternates entry whose path resolves outside `d`. A repair that admits the honest `n22`
shape (`objects/info/alternates` naming a store inside `d`) must normalize and refuse this line; admission by a
raw-prefix or unresolved-`is_relative_to` repair is the leak this module exists to catch.
"""
import pathlib

CLAIMS = "claims.md"
RECEIPT = "evidence/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    store = ctx.init(d.parent / "store")
    ctx.write(store / "x.txt", "borrowed\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "store")
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.write(r / ".git/objects/info/alternates",
              f"{d}/lane/.git/objects/../../../../store/.git/objects\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "s50-alternates-dotdot-abs", "tool": "order", "expect": "error", "defects": [], "build": build}]
