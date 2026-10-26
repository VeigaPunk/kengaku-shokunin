"""F42XMutNear wave-2 survivor probe: one fixture per battery42 survivor shape, to show each surviving
near-variant has a concrete killing fixture a round-43 battery could add. Shapes: 12-cell row,
uppercase anchor token, green lane kept green by a live erratum, slashed task.toml name, short-commit
pinned URL, a claims edit in a later claims commit, the P2-shaped receipt-unreadable echo.
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
M42 = ".ufo/waves/round-42/claims"
CLAIMS42 = "plans/round-42-claims.md"
PROBE42 = "corpus/evidence/round42/probe.txt"


def sha(body):
    return hashlib.sha256(body).hexdigest()


def entry(sid, source, anchor, extra=""):
    row = (f"| {sid} | {source} | capture | A | fixture-scalar | {anchor} | probe row for the anchor "
           "classes | mined | 2026-10-26 | 180d | - |")
    return row + (f" {extra} |" if extra else "") + "\n"


def capture(ctx, repo, rel, name, body):
    ctx.write(repo / "corpus/evidence" / rel / name, body)
    return sha(body)


def landed(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def w2_long_row(ctx, d):
    """A 12-cell registry row: the over-length side of row-malformed, untested by battery42."""
    r = ctx.init(d / "repo")
    capture(ctx, r, "round42/w2/long", "notes.txt", b"capture for the over-length row probe\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S412", "captured at corpus/evidence/round42/w2/long/notes.txt",
                             "", extra="extra") + "\n")
    landed(ctx, r, "probe: one 12-cell row")
    return ["--lane", str(r)]


def w2_uppercase_token(ctx, d):
    """A 64-hex anchor token in uppercase: the digest-uppercase class battery42 never declares."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round42/w2/up", "notes.txt", b"capture for the uppercase probe\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S411", "captured at corpus/evidence/round42/w2/up/notes.txt",
                             f"sha256 {good.upper()}") + "\n")
    landed(ctx, r, "probe: one row, uppercase anchor token")
    return ["--lane", str(r)]


def w2_green_erratum(ctx, d):
    """A wrong anchor token kept exempt by a clean erratum: the lane stays green under the reference."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round42/w2/err", "notes.txt", b"capture the clean erratum names\n")
    stale = sha(b"the digest S413 carried before its repair: w2 green erratum probe\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S413 anchor sha256 {stale} was wrong; the capture's digest is "
              f"sha256 {good}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S413", "captured at corpus/evidence/round42/w2/err/notes.txt",
                             f"sha256 {stale}") + "\n")
    landed(ctx, r, "probe: a live erratum exemption on an otherwise green lane")
    return ["--lane", str(r)]


def w2_slashed_name_url(ctx, d):
    """A row bound through a task.toml name with a slash: name = "<org>/<task>" matched exactly."""
    r = ctx.init(d / "repo")
    body = b"artefact bound via the slashed task name\n"
    url = ("https://raw.githubusercontent.com/acme/w2task/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/w2task/tests/test_outputs.py")
    ctx.write(r / "corpus/evidence/round42/w2/x5-url/test_outputs.py", body)
    ctx.write(r / "corpus/evidence/round42/w2/x5-url/task.toml", 'name = "acme/w2task"\n')
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S414", f"pinned at `{url}`", f"sha256 {sha(body)}") + "\n")
    landed(ctx, r, "probe: url-task binding through a slashed name")
    return ["--lane", str(r)]


def w2_short_commit_url(ctx, d):
    """A green row whose text also carries a pinned URL with a 6-hex commit segment."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round42/w2/x8", "notes.txt", b"capture the row-path locator names\n")
    ctx.write(r / "corpus/evidence/round42/w2/x8-slug/x.py", b"second artefact the short URL would bind\n")
    ctx.write(r / "corpus/evidence/round42/w2/x8-slug/task.toml", 'name = "acme/tests"\n')
    short = "https://raw.githubusercontent.com/acme/whatever/abc123/tests/x.py"
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S415", f"captured at corpus/evidence/round42/w2/x8/notes.txt, pinned at {short}",
                             f"sha256 {good}") + "\n")
    landed(ctx, r, "probe: row-path binding beside a short-commit pinned URL")
    return ["--lane", str(r)]


def w2_late_claims_edit(ctx, d):
    """The gate-p10 line enters a claims blob in a SECOND claims commit, before the receipt lands."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS42, "# round 42 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / M42 / "control.txt", "no gate line and no case line was ever committed here\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / M42 / "control.txt",
              "P10 DEFECT fresh probe exit=1 cases=16\n")
    commit(ctx, repo, "claims control edited again, still before any recorded run")
    ctx.write(repo / PROBE42, "cases=16 observed_pass=7 observed_fail=9 mismatches=0\n")
    commit(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", CLAIMS42, "--receipt", PROBE42]


def w2_p2_excuse(ctx, d):
    """A claims blob carrying the P2 echo shape `P10 DEFECT receipt unreadable: <path>`; the lane is green."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS42, "# round 42 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / M42 / "control.txt",
              "P10 DEFECT receipt unreadable: plans/round-42-claims.md\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE42, "cases=16 observed_pass=7 observed_fail=9 mismatches=0\n")
    commit(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", CLAIMS42, "--receipt", PROBE42]


FIXTURES = [
    {"fid": "w2-long-row", "tool": "anchor", "expect": "reject", "defects": ["row-malformed"], "build": w2_long_row},
    {"fid": "w2-uppercase-token", "tool": "anchor", "expect": "reject", "defects": ["digest-uppercase"], "build": w2_uppercase_token},
    {"fid": "w2-green-erratum", "tool": "anchor", "expect": "accept", "defects": [], "build": w2_green_erratum},
    {"fid": "w2-slashed-name-url", "tool": "anchor", "expect": "accept", "defects": [], "build": w2_slashed_name_url},
    {"fid": "w2-short-commit-url", "tool": "anchor", "expect": "accept", "defects": [], "build": w2_short_commit_url},
    {"fid": "w2-late-claims-edit", "tool": "order", "expect": "reject", "defects": [], "build": w2_late_claims_edit},
    {"fid": "w2-p2-excuse", "tool": "order", "expect": "accept", "defects": [], "build": w2_p2_excuse},
]
