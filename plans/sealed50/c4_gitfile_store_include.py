"""Round-50 C1 blind hostile module (seat `R50C1CritBlind4`, class B4-b): the `[include]` lives in the config of
the store the `.git` FILE resolves to, so it becomes visible only AFTER the gitfile is followed.

Written blind: authored in wave 1 before the repaired `plans/fixture_fence.py` exists, from git's documented
gitfile format (`git-init(1)` `--separate-git-dir`) and git's config `[include]` (`git-config(1)`: a relative
`include.path` is resolved against the directory of the including file). The repaired fence must REFUSE this
fixture (the counter's SEALED leg requires `BREACH`).

Shape, delta from the honest class `n21-separate-gitdir` = the last line of the resolved store's config:

  wt/.git                 `gitdir: ../store`      a FILE — the work tree is the `--lane`
  store/                  plain init, two commits, nothing outside `d`
  store/config            plain `[core]`, then `[include]` / `path = ../../side/foreign.cfg`
  ../side/foreign.cfg     `[core] / fsmonitor = ../../side/spy.sh`   (outside the fixture dir)

Measured (git 2.56.0, receipts in the seat report, `store_include.out`): `git -C wt rev-parse
--absolute-git-dir` = `<d>/store`, i.e. the store is inside `d` and the gitfile itself is the honest shape; the
ONLY path outside `d` is reached through the resolved store's config. `git -C wt config --includes --get
core.fsmonitor` answers `../../side/spy.sh` (rc 0), and `strace -f -y -e trace=openat git -C wt rev-parse HEAD`
opens `<d>/store/../../side/foreign.cfg` — an outside read that exists only after the gitfile is followed and
the resolved store's config is parsed.

The store's own entry list is exactly a plain init (HEAD, config, description, hooks, info, logs, objects, refs,
index), so a repair that resolves the gitfile, proves containment and then classifies the followed store by
ENTRY NAMES alone admits this fixture; only a repair that runs the strict `[core]`-key config parser on the
RESOLVED store's config refuses it. That is the property this module pins.

Round-44 builder contract: `build(ctx, d)` fills `d`, returns the argv tail. Deterministic: no absolute path is
written (the gitfile and the include are relative), the outside file's bytes are fixed, and the only volatile
entry is the masked `.git`-equivalent `store/index`.
"""
import pathlib


def build(ctx, d):
    d = pathlib.Path(d)
    ctx.write(d.parent / "side" / "foreign.cfg", "[core]\n\tfsmonitor = ../../side/spy.sh\n")
    wt, store = d / "wt", d / "store"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    ctx.write(wt / ".git", "gitdir: ../store\n")
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / "b.txt", "two\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "two")
    with (store / "config").open("a") as fh:
        fh.write("[include]\n\tpath = ../../side/foreign.cfg\n")
    return ["--lane", "wt"]


FIXTURES = [
    {"fid": "b4b-gitfile-store-include", "tool": "anchor", "expect": "accept", "defects": [], "build": build},
]
