"""Round-43 C1 battery module `a_url`: upstream-URL binding fixtures for `plans/anchor_digest_check.py`.

Two frozen near-variants of `plans/round43_c1_verify.py` are falsified here, both in the `rc-mirror`
direction (fixture `expect=accept`, reference exits 0, the mutated tool exits 1):

  NA5   the task slug is taken whole (`slugs[d] = pick`) instead of its last path component, so a
        `task.toml` whose `name = "<org>/<task>"` carries a slash no longer matches the URL's task
        component and the row's digest claim cannot be bound.
  NA18  the pinned-URL commit segment accepts 4-40 hex instead of 7-40, so a raw URL with a short
        commit segment stops being ignored and starts binding a capture the row never anchored.

Every fixture builds a git repository from nothing inside its own empty directory (no lane clone, no
pre-existing repository is read) and returns the tool argv tail `["--lane", <repo>]`. Only `hashlib`
from the stdlib is used. Each `defects` set is the exact class set the unmodified tool prints, which
is empty for every fixture here: all four rows are green under the reference tool.

  a_url-org-slash-single      NA5  one row, one capture, a slashed `task.toml` name, no manifest
  a_url-org-slash-registry    NA5  a two-row registry over three commits: a plain task bound through
                                   its own URL beside the slashed task, both digests also in SHA256SUMS
  a_url-short-commit-pair     NA18 one green row and, in its teaches cell, a short-commit URL whose
                                   basename exists in a second task directory (a second unanchored capture)
  a_url-short-commit-shadow   NA18 a row bound by an explicit lane path, plus a short-commit URL whose
                                   capture exists under another task directory (the token then belongs
                                   to the other capture)
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def dig(body):
    return hashlib.sha256(body).hexdigest()


def line(*cells):
    return "| " + " | ".join(cells) + " |\n"


def row(sid, source, anchor, teaches):
    return line(sid, source, "code", "A", "fixture-scope", anchor, teaches, "mined", "2026-10-26",
                "180d", "corpus/knowledge/fixture.md")


def commit(ctx, repo, msg):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", msg)


# NA5 primary: a single row whose capture is reachable only through the URL's task component, while the
# task.toml gives `name = "<org>/<task>"`; keeping the org prefix in the slug leaves the row unbound.
def org_slash_single(ctx, d):
    repo = ctx.init(d / "lane")
    base = repo / "corpus/evidence/ev1/tb2-orbit-ring"
    body = b"orbit ring link transcript\n"
    ctx.write(base / "task.toml", 'name = "satellite-works/orbit-ring"\n')
    ctx.write(base / "link.log", body)
    url = ("https://raw.githubusercontent.com/satellite-works/orbit-ring/"
           "9f3c1e7b2a5d4c8f0e6a1b3d7c9e2f5a8b4d6c10/orbit-ring/tests/link.log")
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S301", url, "sha256 " + dig(body),
                           "link transcript reached through one pinned upstream URL"))
    commit(ctx, repo, "fixture")
    return ["--lane", str(repo)]


# NA5 second shape: a two-row registry across three commits; the second task's name carries a slash and
# its digest is also listed in that directory's SHA256SUMS, so the manifest view resolves it too.
def org_slash_registry(ctx, d):
    repo = ctx.init(d / "lane")
    a = repo / "corpus/evidence/ev2/tb2-beacon-relay"
    b = repo / "corpus/evidence/ev2/tb2-tidal-gauge"
    frame = b"beacon relay frame capture\n"
    probe = b"tidal gauge probe capture\n"
    ctx.write(a / "task.toml", 'name = "beacon-relay"\n')
    ctx.write(a / "frame.txt", frame)
    ctx.write(b / "task.toml", 'name = "tidal-observatory/tidal-gauge"\n')
    ctx.write(b / "probe.txt", probe)
    commit(ctx, repo, "captures")
    ctx.write(a / "SHA256SUMS", dig(frame) + "  frame.txt\n")
    ctx.write(b / "SHA256SUMS", dig(probe) + "  probe.txt\n")
    commit(ctx, repo, "manifests")
    u1 = ("https://raw.githubusercontent.com/beacon-yard/beacon-relay/"
          "c0ffee1234567890abcdef1234567890abcdef12/beacon-relay/tests/frame.txt")
    u2 = ("https://raw.githubusercontent.com/tidal-observatory/tidal-gauge/"
          "0123456789abcdef0123456789abcdef01234567/tidal-gauge/tests/probe.txt")
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S311", u1, "sha256 " + dig(frame),
                           "frame capture listed in a local manifest")
              + row("S312", u2, "sha256 " + dig(probe),
                    "probe capture whose task name carries an organisation prefix"))
    commit(ctx, repo, "sources")
    return ["--lane", str(repo)]


# NA18 primary: the row is green through its long-commit URL, and its teaches cell also carries a 5-hex
# commit URL whose basename exists in a second task directory; widening the commit segment binds that
# second capture, which no anchor token resolves.
def short_commit_pair(ctx, d):
    repo = ctx.init(d / "lane")
    m = repo / "corpus/evidence/ev3/tb2-payload-mux"
    o = repo / "corpus/evidence/ev3/tb2-orbit-ring"
    wire = b"payload mux wire capture\n"
    link = b"orbit ring link capture\n"
    ctx.write(m / "task.toml", 'name = "payload-mux"\n')
    ctx.write(m / "wire.txt", wire)
    ctx.write(o / "task.toml", 'name = "orbit-ring"\n')
    ctx.write(o / "link.log", link)
    commit(ctx, repo, "captures")
    good = ("https://raw.githubusercontent.com/muxworks/payload-mux/"
            "9f3c1e7b2a5d4c8f0e6a1b3d7c9e2f5a8b4d6c10/payload-mux/tests/wire.txt")
    short = ("https://raw.githubusercontent.com/orbitworks/orbit-ring/"
             "a1b2c/orbit-ring/tests/link.log")
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S321", good, "sha256 " + dig(wire),
                           "wire capture beside an abbreviated second locator " + short))
    commit(ctx, repo, "sources")
    return ["--lane", str(repo)]


# NA18 second shape: the row binds by an explicit lane path, so the short-commit URL can only add a
# locator; under the widened pattern the row binds to that other capture and the token becomes a
# digest of a different capture than the row names.
def short_commit_shadow(ctx, d):
    repo = ctx.init(d / "lane")
    bundle = repo / "corpus/evidence/ev4/bundle"
    s = repo / "corpus/evidence/ev4/tb2-spline-diff"
    claim = b"bundle claim capture\n"
    golden = b"spline diff golden capture\n"
    ctx.write(bundle / "claim.txt", claim)
    ctx.write(s / "task.toml", 'name = "spline-diff"\n')
    ctx.write(s / "golden.txt", golden)
    commit(ctx, repo, "captures")
    short = ("https://raw.githubusercontent.com/vendor-a/spline-diff/"
             "4c8ea/spline-diff/tests/golden.txt")
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S331", "corpus/evidence/ev4/bundle/claim.txt",
                           "sha256 " + dig(claim),
                           "claim capture read beside an abbreviated locator " + short))
    commit(ctx, repo, "sources")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a_url-org-slash-single", "tool": "anchor", "expect": "accept", "defects": [],
     "build": org_slash_single},
    {"fid": "a_url-org-slash-registry", "tool": "anchor", "expect": "accept", "defects": [],
     "build": org_slash_registry},
    {"fid": "a_url-short-commit-pair", "tool": "anchor", "expect": "accept", "defects": [],
     "build": short_commit_pair},
    {"fid": "a_url-short-commit-shadow", "tool": "anchor", "expect": "accept", "defects": [],
     "build": short_commit_shadow},
]
