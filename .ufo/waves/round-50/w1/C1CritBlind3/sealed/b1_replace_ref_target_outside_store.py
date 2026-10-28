"""Round-50 wave-1 BLIND sealed module `b1_replace_ref_target_outside_store` (seat R50C1CritBlind3).

What it builds, inside the fixture dir `d`:

    lane/                          plain-init repository, two commits
    lane/.git/refs/replace/<ORIG>  a 40-hex ref file, value <TARGET> (written by `git replace`)
    lane/.git/objects/info/alternates
                                   `../../../outside-store/.git/objects` — a RELATIVE entry that climbs
                                   out of `d` into the module build root

    outside-store/                 a second repository in the build root, OUTSIDE `d`; <TARGET> is its
                                   HEAD commit and exists nowhere inside `d`

Why this is hostile and not honest:

  * The honest class `n17-replace-ref` (round 49, `plans/honest50/modules/novel49/n17_replace_ref.py`) is a
    replace ref whose replacement object is in the same store: every byte read stays inside `d`.
  * The honest class `n22-alternates-in-d` (round 50, `plans/honest50/modules/novel50/n22_alternates_in_d.py`)
    is an alternates entry that names a store inside `d`.
  * This module is the product of the two: the replace ref's target is resolvable ONLY through an alternates
    entry pointing outside `d`. `git -C lane cat-file -t <TARGET>` answers `commit` while
    `lane/.git/objects/<xx>/<38>` does not exist and `lane/.git/objects/pack` is empty, so the object bytes are
    read from outside `d` (witnessed with strace in the seat receipt: opens of
    `<build>/outside-store/.git/objects/..`). It is also over-determined: the alternates entry itself leaves `d`.

The repair move it attacks. The frozen honest leg forces a repair to admit `refs/replace/<40hex>` (n17) and to
stop refusing `objects/info/alternates` by name (n22). The cheap way to do that is shape-only: a replace ref is
"40-hex name, 40-hex body", and an alternates entry is "some path that exists". Shape-only admission turns one
allowed pointer into an outside-`d` read. The entry here is RELATIVE, so a repair that only rejects absolute
(`/`-prefixed) alternates paths still leaks it.

Expected verdicts (measured by the seat, not assumed; receipt `receipts/witness.json`):
  * base fence `05d5fe03…`: BREACH, first reason `lane/.git/objects/info/alternates present (object-store
    redirect)` (`_refs` would also refuse the `replace` namespace). So this module is a regression guard on the
    n17/n22 repair, not a demonstration of a base leak.
  * shape-only repair (allow `refs/replace`, allow an alternates entry that merely names an existing directory):
    ADMIT — the leak this module exists to catch. The admitted fixture reads
    `<build>/outside-store/.git/objects/…`: 9 strace references outside `d`, including the replaced commit's
    loose object, while `cat-file -t` fails with rc 128 as soon as the alternates file is removed.
  * containment repair (every alternates entry, relative or absolute, must resolve inside `d`): BREACH, while the
    honest `n17-replace-ref` and `n22-alternates-in-d` fixtures stay ADMIT.

Authored blind: against the base fence at the frozen digest
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` and the two frozen honest-class contracts
above. No repaired fence existed when this module was written. Round-44 builder contract: `build(ctx, d)` fills
`d` and returns the argv tail.
"""
import os
import pathlib


def build(ctx, d):
    d = pathlib.Path(d)
    store = ctx.init(d.parent / "outside-store")
    ctx.write(store / "outside.txt", "only outside d\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "outside")
    target = ctx.sh("git", "-C", str(store), "rev-parse", "HEAD").stdout.strip()

    lane = ctx.init(d / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "one")
    ctx.write(lane / "b.txt", "two\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "two")
    orig = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD~1").stdout.strip()

    entry = os.path.relpath(store / ".git" / "objects", lane / ".git" / "objects")
    ctx.write(lane / ".git/objects/info/alternates", entry + "\n")
    ctx.git(lane, "replace", orig, target)
    return ["--lane", "lane"]


FIXTURES = [{"fid": "b1-replace-target-outside-store", "tool": "anchor", "expect": "reject", "defects": [],
             "build": build}]
