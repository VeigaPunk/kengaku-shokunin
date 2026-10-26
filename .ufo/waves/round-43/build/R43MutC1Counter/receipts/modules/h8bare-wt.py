"""Draft control `h8bare-wt` (seat R43MutC1Counter) — the ONLY reachable `core.worktree`-branch-only state.

With `core.bare=true` AND `core.worktree=<outside>` in the fixture repo's `.git/config`,
`git rev-parse --show-toplevel` FAILS (rc=128, "this operation must be run in a work tree", measured), so
repo_breach's toplevel branch is skipped; the refusal then comes solely from the `if val:` branch.
  pristine counter      -> SETUP ... escapes its directory: repo/core.worktree=<host>
  M08 counter (if val: -> if False:) -> the fixture is accepted (branch disabled).
"""
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def build(ctx, d):
    host = ctx.init(d.parent / "h8host")
    ctx.write(host / "corpus/SOURCES.md",
              HEADER + "| S904 | captured at corpus/evidence/round43/h8/notes.txt | capture | A | fixture-scalar "
              "| - | bare worktree probe | mined | 2026-10-26 | 180d | - |\n")
    ctx.write(host / "corpus/evidence/round43/h8/notes.txt", b"capture\n")
    ctx.git(host, "add", "-A")
    ctx.git(host, "commit", "-q", "-m", "host history the bare worktree points at")
    repo = ctx.init(d / "repo")
    ctx.sh("git", "-C", str(repo), "config", "core.bare", "true")
    ctx.sh("git", "-C", str(repo), "config", "core.worktree", str(host))
    return ["--lane", str(repo)]


FIXTURES = [{"fid": "h8-bare-worktree", "tool": "anchor", "expect": "error", "defects": [], "build": build}]
