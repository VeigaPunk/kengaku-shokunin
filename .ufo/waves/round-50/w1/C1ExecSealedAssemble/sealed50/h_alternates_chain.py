"""Sealed blind hostile module A — round-50 wave-1 seat `R50C1CritBlind5` (critic, R50-C1).

Attack class: **an alternates CHAIN whose second hop leaves `d`.**

    lane/.git/objects/info/alternates  ->  ../../../mid/.git/objects      (resolves INSIDE d)
    mid/.git/objects/info/alternates   ->  ../../../../chain-out/.git/objects   (resolves OUTSIDE d)

`lane` is an ordinary one-commit repository; its own alternates entry names an object store that is inside the
fixture, exactly the shape the round-50 honest class `n22_alternates_in_d` declares honest. The escape is one
hop deeper: `mid` itself borrows from `d.parent/chain-out`, so `git` resolves `lane`'s history through
`mid`'s objects and then through `chain-out`'s objects, and `chain-out` is NOT under `d`.

Why this is the blind hostile counterpart of the repair (not of the base fence). The round-50 repair must widen
the store allowlist so `n22` (a single in-`d` alternates entry) is admitted; the tempting widening is "admit an
`alternates` file whose direct target resolves inside `d`". That rule admits `n22` **and** this module: the
direct target here is inside `d`. Only a repair that resolves the chain transitively (git follows nested
`alternates`, up to its own depth limit) and requires *every* hop inside `d` refuses it. So the module scores a
repair by the property it claims (no read outside `d`), not by the shape of the first line it sees.

Measured on the base fence `05d5fe03…`: BREACH, reason `objects/info/alternates present (object-store
redirect)` — the base fence refuses this class by the same blanket rule that over-refuses honest `n22`, so that
refusal carries no information about the repair. Real-git witness (seat receipt): `git -C lane cat-file -p
<chain-out commit>:b-only.txt` prints `outside bytes` while no object of that commit exists anywhere under `d`;
moving `chain-out` away makes the same read fail with `unable to normalize alternate object path` naming the
resolved outside path.

Determinism: every entry is a relative path resolved against the object database directory git resolves it
against, so no build-scratch absolute path enters the tree; the two ordinary repos are plain `git init` +
commits. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail. `expect` is this
seat's statement of the required verdict (`breach`); the round-50 counter reads only `fid`/`tool`/`build`.
"""


def build(ctx, d):
    out = ctx.init(d.parent / "chain-out")
    ctx.write(out / "b-only.txt", "outside bytes\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "out")
    mid = ctx.init(d / "mid")
    ctx.write(mid / "mid.txt", "mid\n")
    ctx.git(mid, "add", "-A")
    ctx.git(mid, "commit", "-qm", "mid")
    lane = ctx.init(d / "lane")
    ctx.write(lane / "lane.txt", "lane\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "lane")
    # hop 1: inside d (the shape honest n22 declares honest); hop 2: outside d
    ctx.write(lane / ".git/objects/info/alternates", "../../../mid/.git/objects\n")
    ctx.write(mid / ".git/objects/info/alternates", "../../../../chain-out/.git/objects\n")
    return ["--lane", "lane"]


FIXTURES = [{"fid": "bl5-alternates-chain-out", "tool": "anchor", "expect": "breach", "defects": [], "build": build}]
