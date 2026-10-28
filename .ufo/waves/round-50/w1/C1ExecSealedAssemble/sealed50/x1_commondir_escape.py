"""Blind hostile module X1 (round-50 wave 1, seat R50C1CritBlind2): a `commondir` file whose target ESCAPES `d`.

Shape: the fixture holds ONE ordinary repository, `d/lane`, whose `.git` is a real directory carrying every entry
`git init` + two commits writes (HEAD, config, description, hooks/, info/exclude, logs/, objects/, refs/, index,
COMMIT_EDITMSG, packed-refs) — and one extra entry, `.git/commondir`, naming a store BESIDE `d`. Nothing else in
the fixture is anomalous, so the only hook a store fence can use is the `commondir` line itself: every entry-based
allowlist, and every structural walk that descends `.git`, sees a plain-init store plus one foreign file.

Why the escape is material, not cosmetic: git resolves `commondir` (gitrepository-layout(5), "commondir: …
if this file exists a relative path to the root of the working tree … the common dir") and then reads config,
refs and objects from that common dir. With this file in place, `git -C lane rev-parse --git-common-dir` answers
the store outside `d`, so a tool run behind an admitting fence opens config/refs/objects outside `d` — the
property the fence advertises it never does. The base fence's own docstring states it starts no git child and
proves containment from the store's entries, which is why it must refuse the foreign entry rather than resolve it.

Two fixtures, the two forms git itself accepts for a `commondir` line:

  x1-cd-abs   absolute target       `<build>/cd-store-abs/.git`
  x1-cd-rel   relative target       resolved against the gitdir, `..`-escaping `d` (e.g. `../../cd-store-rel/.git`)

The relative form is the one a lexical `startswith(d)` check cannot catch by string alone (the line does not
contain `d` at all), and the absolute form is the one a check that only inspects fixture-level `.git` *files*
never sees (the file lives inside the `.git` directory).

Distinctness from the frozen batteries (checked in this seat's report): the r44 refusal `f7_commondir` writes a
`.git` dir holding ONLY `commondir` + `HEAD` (no objects/refs/config, so it is refused as an incomplete store
before the escape is considered), and the r45 held-out `f19_commondir_hidden` plants a RELATIVE commondir below
`repo/.git/modules/escape`, i.e. inside a pruned `.git` subtree the fence's walk never visits (refused as "lane is
not a repository"). Neither is a complete, otherwise-allowlisted store whose single foreign entry escapes `d`.

Honest counterpart (must be ADMITTED by a repaired fence): the linked worktree `n20_linked_worktree`, whose
`commondir` sits at `repo/.git/worktrees/wt/commondir` and names `../..` — inside `d`. A repair that admits
`commondir` by name, or that resolves it without a containment test on the resolved common dir, admits X1 too.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail. `ctx`'s root is the module build
dir (the parent of `d`), which is why the escaped store can be created beside `d` — that is the escape.
"""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _plain_repo(ctx, root):
    """A store `git init` + two commits writes, and nothing else: the fixture's ordinary, honest-looking half."""
    r = ctx.init(root)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _escaped_store(ctx, d, name):
    """The common dir the fixture's `commondir` names: a full store BESIDE `d`, i.e. outside the fence's `d`."""
    store = pathlib.Path(d).parent / name
    s = _plain_repo(ctx, store)
    ctx.write(s / "case.txt", "CASE x observed=1\n")
    ctx.git(s, "add", "-A")
    ctx.git(s, "commit", "-qm", "case")
    return s


def _lane_with_commondir(ctx, d, line):
    lane = _plain_repo(ctx, pathlib.Path(d) / "lane")
    ctx.write(lane / ".git" / "commondir", line + "\n")
    return ["--lane", "lane"]


def build_abs(ctx, d):
    store = _escaped_store(ctx, d, "cd-store-abs")
    return _lane_with_commondir(ctx, d, str(store / ".git"))


def build_rel(ctx, d):
    store = _escaped_store(ctx, d, "cd-store-rel")
    gitdir = pathlib.Path(d) / "lane" / ".git"
    line = os.path.relpath(str(store / ".git"), str(gitdir))
    return _lane_with_commondir(ctx, d, line)


FIXTURES = [
    {"fid": "x1-cd-abs", "tool": "anchor", "expect": "error", "defects": [], "build": build_abs},
    {"fid": "x1-cd-rel", "tool": "anchor", "expect": "error", "defects": [], "build": build_rel},
]
