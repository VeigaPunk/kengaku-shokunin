"""Round-42 C1 battery module `a_row`: anchor census-shape, evidence-ref and erratum-scope fixtures.

Seat R42BatAncRow. Every fixture builds a lane repository from nothing (no lane clone) and returns the
tool argv tail; every path stays inside the fixture directory. Stdlib only (hashlib). Each fixture is
single-purpose: it targets one branch of plans/anchor_digest_check.py in the declared direction of the
mutant it falsifies, and its `defects` is the exact class set the unmodified tool prints on it.
"""
import hashlib

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def dig(body):
    return hashlib.sha256(body).hexdigest()


def line(*cells):
    return "| " + " | ".join(cells) + " |\n"


def row(sid, source, anchor, kind="code", tier="A", scope="fixture", teaches="fixture row",
        status="mined", opened="2026-10-26", recheck="180d", used="corpus/knowledge/fixture.md"):
    return line(sid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used)


def capture(ctx, r, reldir, body, name="cap.txt", sums=True, toml=None):
    base = r / "corpus/evidence" / reldir
    ctx.write(base / name, body)
    if sums:
        ctx.write(base / "SHA256SUMS", f"{dig(body)}  {name}\n")
    if toml is not None:
        ctx.write(base / "task.toml", toml)
    return dig(body)


def commit(ctx, r, msg="fixture"):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", msg)


def start(ctx, d):
    return ctx.init(d / "repo")


# X9 primary: one census-shaped row with 10 cells and no digest claim -- the structural defect is the
# only one a short row can carry, since the cell-count check runs before any token is looked at.
def x9_short_no_token(ctx, d):
    r = start(ctx, d)
    ctx.write(r / "corpus/evidence/fx/note.txt", b"census fixture note\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + line("S901", "row missing its teaches cell", "code", "A", "fixture", "",
                            "mined", "2026-10-26", "180d", "corpus/knowledge/fixture.md"))
    commit(ctx, r)
    return ["--lane", str(r)]


# X9 second trigger: a six-row registry where the ten-cell row's anchor digest is CORRECT -- a row that
# is green on every digest test and is disqualified only by its cell count (mutant only flags >11).
def x9_registry_short_valid(ctx, d):
    r = start(ctx, d)
    ha = capture(ctx, r, "alpha", b"alpha capture, six-row registry\n")
    hb = capture(ctx, r, "beta", b"beta capture, six-row registry\n")
    rows = [
        row("S911", "census row, no digest claim", ""),
        row("S912", "alpha capture at corpus/evidence/alpha/cap.txt", "sha256 " + ha),
        row("S913", "census row, no digest claim", ""),
        row("S914", "beta capture at corpus/evidence/beta/cap.txt", "sha256 " + hb),
        row("S915", "census row carrying prose only", ""),
        line("S916", "alpha capture at corpus/evidence/alpha/cap.txt", "code", "A", "fixture",
             "sha256 " + ha, "fixture row", "mined", "2026-10-26", "180d"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEADER + "".join(rows))
    ctx.write(r / "corpus/knowledge/fixture.md", "# fixture knowledge row\n")
    commit(ctx, r)
    return ["--lane", str(r)]


# X13 primary: the row as committed claims the digest of a capture that sits STAGED beyond HEAD (only
# the capture blob is staged); the default ref reads HEAD blobs, so the claim is digest-unknown.
def x13_staged_capture(ctx, d):
    r = start(ctx, d)
    old = b"alpha capture, first view\n"
    new = b"alpha capture, re-captured view\n"
    capture(ctx, r, "alpha", old)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S902", "capture at corpus/evidence/alpha/cap.txt", "sha256 " + dig(old)))
    commit(ctx, r, "first view")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S902", "alpha capture at corpus/evidence/alpha/cap.txt, re-captured",
                           "sha256 " + dig(new)))
    ctx.git(r, "add", "corpus/SOURCES.md")
    ctx.git(r, "commit", "-q", "-m", "row advanced")
    ctx.write(r / "corpus/evidence/alpha/cap.txt", new)
    ctx.git(r, "add", "corpus/evidence/alpha/cap.txt")
    return ["--lane", str(r)]


# X13 second trigger: the row is bound through the pinned upstream URL / task.toml route instead of an
# explicit path, and a second row anchors its own capture cleanly beside it.
def x13_url_staged(ctx, d):
    r = start(ctx, d)
    old = b"graded test file, first view\n"
    new = b"graded test file, re-captured view\n"
    task = "wiki"
    capture(ctx, r, "tb2-" + task, old, name="test_outputs.py", toml=f'name = "tb2/{task}"\n')
    hb = capture(ctx, r, "tb2-other", b"sibling task capture\n", name="test_outputs.py")
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/{task}/tests/test_outputs.py"
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S903", f"pinned at {url}", "sha256 " + dig(old))
              + row("S904", "capture at corpus/evidence/tb2-other/test_outputs.py", "sha256 " + hb))
    commit(ctx, r, "first view")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S903", f"pinned at {url}", "sha256 " + dig(new))
              + row("S904", "capture at corpus/evidence/tb2-other/test_outputs.py", "sha256 " + hb))
    ctx.git(r, "add", "corpus/SOURCES.md")
    ctx.git(r, "commit", "-q", "-m", "row advanced")
    ctx.write(r / "corpus/evidence/tb2-wiki/test_outputs.py", new)
    ctx.git(r, "add", "corpus/evidence/tb2-wiki/test_outputs.py")
    return ["--lane", str(r)]


# X15 primary: the erratum's correction token is a committed digest of the SIBLING row's capture -- in
# the global digest set, not in this row's capture scope, so it corrects nothing (erratum-incomplete).
def x15_sibling_digest(ctx, d):
    r = start(ctx, d)
    capture(ctx, r, "fx-a", b"row A capture\n")
    hb = capture(ctx, r, "fx-b", b"row B capture, the sibling the erratum cites\n")
    wrong = dig(b"row A anchor token committed nowhere\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S905 anchor sha256 {wrong} named no byte of its own capture; the "
              f"correction is sha256 {hb}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S905", "capture at corpus/evidence/fx-a/cap.txt", "sha256 " + wrong)
              + row("S906", "capture at corpus/evidence/fx-b/cap.txt", "sha256 " + hb))
    commit(ctx, r)
    return ["--lane", str(r)]


# X15 second trigger, erratum appended in a LATER commit: the correction is the sibling capture's
# manifest-listed (older) digest, reachable in the global set only through its manifest view, and the
# corrected row is bound through the URL route.
def x15_manifest_sibling(ctx, d):
    r = start(ctx, d)
    task = "wiki"
    prev = b"sibling capture, older committed bytes\n"
    now = b"sibling capture, current bytes\n"
    capture(ctx, r, "tb2-" + task, b"graded test file\n", name="test_outputs.py",
            toml=f'name = "tb2/{task}"\n')
    capture(ctx, r, "fx-b", now, sums=False)
    ctx.write(r / "corpus/evidence/fx-b/SHA256SUMS", f"{dig(prev)}  cap.txt\n")
    wrong = dig(b"S907 anchor token committed nowhere\n")
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/{task}/tests/test_outputs.py"
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S907", f"pinned at {url}", "sha256 " + wrong)
              + row("S908", "capture at corpus/evidence/fx-b/cap.txt", "sha256 " + dig(now)))
    commit(ctx, r, "rows")
    ctx.write(r / "corpus/lessons/round-42.md",
              f"Erratum (round 37): S907 anchor sha256 {wrong} was committed against the wrong file; "
              f"the correction is sha256 {dig(prev)}.\n")
    commit(ctx, r, "erratum")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "a_row-x9-short-no-token", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": x9_short_no_token},
    {"fid": "a_row-x9-registry-short-valid", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": x9_registry_short_valid},
    {"fid": "a_row-x13-staged-capture", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown"], "build": x13_staged_capture},
    {"fid": "a_row-x13-url-staged", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown"], "build": x13_url_staged},
    {"fid": "a_row-x15-sibling-digest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown", "erratum-incomplete"], "build": x15_sibling_digest},
    {"fid": "a_row-x15-manifest-sibling", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown", "erratum-incomplete"], "build": x15_manifest_sibling},
]
