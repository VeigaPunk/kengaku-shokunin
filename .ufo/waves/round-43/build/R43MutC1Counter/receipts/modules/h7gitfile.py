"""Draft control `h7gitfile` (seat R43MutC1Counter) — repo_breach gap probe, NOT a frozen control.

Vector: the fixture repo's `.git` is a GITFILE (`gitdir: <outside>`) pointing at a sibling repo the same
module crafted. A gitfile marks the worktree — `git rev-parse --show-toplevel` prints the FIXTURE dir — and
the worktree key is unset, so both repo_breach branches stay silent. But the tool's evidence reads are
`git -C <repo> cat-file` calls, which now resolve against the OUTSIDE gitdir: the fixture's own history
never committed the capture (it is unpromoted), yet the row's anchor verifies against the capture blob
served from the outside history — the exact state `--evidence-ref head` exists to prevent.
Expected if the guard were complete: `SETUP ... escapes its directory`. Measured (pristine round-43
counter): the fixture is accepted with wrong=0 — see the draft receipt.
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
ROW = ("| S903 | captured at corpus/evidence/round43/h7/notes.txt | capture | A | fixture-scalar "
       "| sha256 {anchor} | gitfile probe | mined | 2026-10-26 | 180d | - |\n")


def build(ctx, d):
    body = b"capture read through the gitfile\n"
    anchor = hashlib.sha256(body).hexdigest()
    host = ctx.init(d.parent / "h7host")
    ctx.write(host / "corpus/evidence/round43/h7/notes.txt", body)
    ctx.git(host, "add", "-A")
    ctx.git(host, "commit", "-q", "-m", "outside history: the capture blob the fixture will verify against")
    repo = ctx.init(d / "repo")
    ctx.write(repo / "corpus/evidence/round43/h7/notes.txt", body)
    ctx.write(repo / "corpus/SOURCES.md", HEADER + ROW.format(anchor=anchor))
    ctx.git(repo, "add", "corpus/SOURCES.md")
    ctx.git(repo, "commit", "-q", "-m", "the fixture's own history: the row only, capture unpromoted")
    ctx.sh("rm", "-rf", str(repo / ".git"))
    ctx.write(repo / ".git", f"gitdir: {host / '.git'}\n")
    return ["--lane", str(repo)]


FIXTURES = [{"fid": "h7-gitfile-outside", "tool": "anchor", "expect": "accept", "defects": [], "build": build}]
