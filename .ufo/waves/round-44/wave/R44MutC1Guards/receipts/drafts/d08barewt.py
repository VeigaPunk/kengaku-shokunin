"""Draft control `d8barewt` (seat R44MutC1Guards) — repo_breach's `if val:` (worktree) branch red control.

With `core.bare=true` AND `core.worktree=<outside>` in the fixture repo's `.git/config`,
`git rev-parse --show-toplevel` FAILS (rc=128, "this operation must be run in a work tree"), so the
toplevel branch is skipped; the refusal then comes solely from the `if val:` branch.
  pristine counter  -> `SETUP ... escapes its directory: repo/core.worktree=<host>` (exit 2)
  M08 counter (if val: -> if False:) -> the fixture is admitted (branch disabled).
"""
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def build(ctx, d):
    host = ctx.init(d.parent / "d8host")
    ctx.write(host / "corpus/SOURCES.md",
              HEADER + "| S911 | captured at corpus/evidence/round44/d8/notes.txt | capture | A | fixture-scalar "
              "| - | bare worktree probe | mined | 2026-10-26 | 180d | - |\n")
    ctx.write(host / "corpus/evidence/round44/d8/notes.txt", b"capture\n")
    ctx.git(host, "add", "-A")
    ctx.git(host, "commit", "-q", "-m", "host history the bare worktree points at")
    repo = ctx.init(d / "repo")
    ctx.sh("git", "-C", str(repo), "config", "core.bare", "true")
    ctx.sh("git", "-C", str(repo), "config", "core.worktree", str(host))
    return ["--lane", str(repo)]


FIXTURES = [{"fid": "d8-bare-worktree", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
