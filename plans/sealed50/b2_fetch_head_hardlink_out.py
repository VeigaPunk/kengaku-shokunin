"""Round-50 wave-1 BLIND sealed module `b2_fetch_head_hardlink_out` (seat R50C1CritBlind3).

What it builds:

    lane/                          plain-init repository, two commits (HEAD = <H>)
    lane/.git/FETCH_HEAD           a regular file, syntactically canonical
                                   `<H>\\t\\tbranch 'master' of ../src\\n`, with st_nlink == 2
    <build>/fetch-head-store       the second name of that same inode, OUTSIDE `d`

Why this is hostile and not honest:

  * The honest class `n18-shallow-fetch` (round 49, `plans/honest50/modules/novel49/n18_shallow_fetch.py`) has
    `.git/FETCH_HEAD` and `.git/shallow` as ordinary single-link files inside `d`.
  * Here the bytes `d` reads have a name outside `d`: writing `<build>/fetch-head-store` changes what
    `git -C lane rev-parse --verify FETCH_HEAD` answers, and a reader inside `d` cannot tell from the path. The
    escape is store-identity, not open-path — the same class as `plans/refusals46/f16_objects_hardlink_out.py`,
    moved onto the top-level file the n18 repair newly has to admit.

The repair move it attacks — measured, and narrower than it looks. `_tree` does not descend into a `.git`
directory at all (it records the repo and stops), so the only link test that ever sees `.git/FETCH_HEAD` is the
`_linked()` check inside `_store`'s per-entry loop, and that check sits AFTER `if name not in GIT_TOP`. The base
fence therefore refuses this fixture by NAME, not by link identity: there is no pre-existing link property to
regress. Once the n18 repair adds `FETCH_HEAD` to the admitted names, the only thing that still refuses this
fixture is the position of the `_linked()` check relative to the new name branch. A branch added ahead of it
(the natural place if the branch validates the fetch-record shape and then `continue`s) leaks.

Expected verdicts (measured by the seat, not assumed; receipt `receipts/witness.json`):
  * base fence `05d5fe03…`: BREACH — `lane/.git/FETCH_HEAD is not a plain-init entry` (name allowlist, not the
    link rule).
  * correct repair (name admitted after the generic `_linked()` test): BREACH — `FETCH_HEAD has more than one
    hard link`, while an identical single-link `FETCH_HEAD` inside `d` is ADMIT.
  * misordered repair (name branch ahead of the link test): ADMIT — the leak this module exists to catch.

Authored blind: against the base fence at the frozen digest
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` and the frozen honest-class contract above.
No repaired fence existed when this module was written. Round-44 builder contract: `build(ctx, d)` fills `d` and
returns the argv tail.
"""
import os
import pathlib


def build(ctx, d):
    d = pathlib.Path(d)
    lane = ctx.init(d / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "one")
    ctx.write(lane / "b.txt", "two\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "two")
    head = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD").stdout.strip()

    outside = ctx.write(d.parent / "fetch-head-store",
                        f"{head}\t\tbranch 'master' of ../src\n")
    os.link(outside, lane / ".git" / "FETCH_HEAD")
    return ["--lane", "lane"]


FIXTURES = [{"fid": "b2-fetch-head-hardlink-out", "tool": "anchor", "expect": "reject", "defects": [],
             "build": build}]
