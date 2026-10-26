"""R43CritEquiv critic battery: six from-nothing fixtures re-derived with different shapes from the freeze
direction module (w_near.py), one per carried near-variant kill. Not a battery43 candidate; self-verification only."""

import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")

CLAIMS43 = "plans/round-43-claims.md"
M43 = ".ufo/waves/round-43/claims"
PROBE43 = "corpus/evidence/round43/crit/probe.txt"


def sha(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor, extra_cells=0):
    base = (f"| {sid} | {source} | capture | A | scalar | {anchor} | probe row | mined | "
            f"2026-10-26 | 180d | - |")
    return base + (" x |" * extra_cells) + "\n"


def capture(ctx, repo, rel, name, body):
    ctx.write(repo / "corpus/evidence" / rel / name, body)
    return sha(body)


def landed(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def f1_malformed_long(ctx, d):
    """A 13-cell row: the over-length side of row-malformed (12 cells in the probe; 13 here)."""
    r = ctx.init(d / "repo")
    capture(ctx, r, "round43/crit/x1", "notes.txt", b"crit probe capture for the over-length row\n")
    ctx.write(r / "corpus/SOURCES.md", HEADER + row("S601",
                                                    "captured at corpus/evidence/round43/crit/x1/notes.txt",
                                                    "", extra_cells=2))
    landed(ctx, r, "crit: one 13-cell row")
    return ["--lane", str(r)]


def f2_green_errata(ctx, d):
    """A wrong anchor token kept exempt by a clean erratum, on a different sid/capture/token set."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round43/crit/err", "data.bin", b"crit r43 errata capture payload\n")
    stale = sha(b"old wrong token bytes for the crit erratum probe\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S602 anchor sha256 {stale} is wrong; the real digest of the "
              f"capture is sha256 {good}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S602", "captured at corpus/evidence/round43/crit/err/data.bin",
                           f"sha256 {stale}"))
    landed(ctx, r, "crit: a live erratum exemption on a green lane")
    return ["--lane", str(r)]


def f3_slashed_name(ctx, d):
    """A row bound through a task.toml name with a slash and a different owner/repo/slug."""
    r = ctx.init(d / "repo")
    body = b"crit artefact bound via the slashed task name\n"
    url = ("https://raw.githubusercontent.com/corp/r43svc/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/r43svc/tests/test_outputs.py")
    ctx.write(r / "corpus/evidence/round43/crit/x5/test_outputs.py", body)
    ctx.write(r / "corpus/evidence/round43/crit/x5/task.toml", 'name = "corp/r43svc"\n')
    ctx.write(r / "corpus/SOURCES.md", HEADER + row("S603", f"pinned at `{url}`", f"sha256 {sha(body)}"))
    landed(ctx, r, "crit: url-task binding through a slashed name")
    return ["--lane", str(r)]


def f4_short_commit(ctx, d):
    """A green row whose text also carries a pinned URL with a 5-hex commit segment (probe used 6)."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round43/crit/x8", "notes.txt", b"crit capture the row-path locator names\n")
    ctx.write(r / "corpus/evidence/round43/crit/x8-slug/x.py", b"second artefact the short URL would bind\n")
    ctx.write(r / "corpus/evidence/round43/crit/x8-slug/task.toml", 'name = "corp/tests"\n')
    short = "https://raw.githubusercontent.com/corp/w/abcde/tests/x.py"
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S604", f"captured at corpus/evidence/round43/crit/x8/notes.txt, pinned at {short}",
                           f"sha256 {good}"))
    landed(ctx, r, "crit: row-path binding beside a short-commit pinned URL")
    return ["--lane", str(r)]


def f5_late_gate(ctx, d):
    """A gate-P10 line enters a claims blob in a second claims commit, before the receipt lands (round 43)."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS43, "# round 43 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / M43 / "control.txt", "no gate line and no case line was ever committed here\n")
    landed(ctx, repo, "freeze")
    ctx.write(repo / M43 / "control.txt", "P10 DEFECT fresh probe output is not byte-equal cases=12\n")
    landed(ctx, repo, "claims control edited again, still before any recorded run")
    ctx.write(repo / PROBE43, "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    landed(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", CLAIMS43, "--receipt", PROBE43]


def f6_p2_echo(ctx, d):
    """A claims blob carrying the P2 echo shape with a different echoed path; the lane is green."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS43, "# round 43 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / M43 / "control.txt",
              f"P10 DEFECT receipt unreadable: {PROBE43}\n")
    landed(ctx, repo, "freeze")
    ctx.write(repo / PROBE43, "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    landed(ctx, repo, "first recorded run")
    return ["--lane", str(repo), "--claims", CLAIMS43, "--receipt", PROBE43]


FIXTURES = [
    {"fid": "crit-malformed-long", "tool": "anchor", "expect": "reject", "defects": ["row-malformed"],
     "build": f1_malformed_long},
    {"fid": "crit-green-errata", "tool": "anchor", "expect": "accept", "defects": [],
     "build": f2_green_errata},
    {"fid": "crit-slashed-name", "tool": "anchor", "expect": "accept", "defects": [],
     "build": f3_slashed_name},
    {"fid": "crit-short-commit", "tool": "anchor", "expect": "accept", "defects": [],
     "build": f4_short_commit},
    {"fid": "crit-late-gate", "tool": "order", "expect": "reject", "defects": [],
     "build": f5_late_gate},
    {"fid": "crit-p2-echo", "tool": "order", "expect": "accept", "defects": [],
     "build": f6_p2_echo},
]
