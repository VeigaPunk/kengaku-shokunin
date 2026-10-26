"""Round-43 hostile module `h5_symlink` — leg h (R42CritC1Counter V2b).

Vector: `path_ok` validates argv tokens only; a fixture whose committed `corpus/SOURCES.md` is a symlink to a file
OUTSIDE the fixture directory makes the anchor tool parse rows the counter never fingerprints (the tool reads the
working-tree path and follows the link). Observable, on a fixture that declares `accept`:
  round-42 counter  FIXTURE h5-row-source-outside ... observed_rc=0 ... ok   (the outside rows are read: vector open)
  round-43 counter  SETUP fixture 'h5-row-source-outside' ... escapes its directory: symlink corpus/SOURCES.md -> ...
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def build(ctx, d):
    body = b"capture for the outside-row probe\n"
    repo = ctx.init(d / "repo")
    ctx.write(repo / "corpus/evidence/round43/h5/notes.txt", body)
    outside = d.parent / "h5-outside" / "SOURCES.md"
    ctx.write(outside, HEADER + "| S901 | captured at corpus/evidence/round43/h5/notes.txt | capture | A | fixture | "
              f"sha256 {hashlib.sha256(body).hexdigest()} | outside row | mined | 2026-10-26 | 180d | - |\n")
    (repo / "corpus").mkdir(exist_ok=True)
    ctx.sh("ln", "-s", str(outside), str(repo / "corpus/SOURCES.md"))
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "row source is a link to a file outside the fixture")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "h5-row-source-outside", "tool": "anchor", "expect": "accept", "defects": [], "build": build},
]
