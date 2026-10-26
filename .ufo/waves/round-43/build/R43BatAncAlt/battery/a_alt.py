"""a_alt - battery43 module (seat R43BatAncAlt, kengaku round 43 wave 1).

A second module for the six anchor near-variants frozen in plans/round43_c1_verify.py (NA1, NA5, NA7, NA18,
NA20, NA21), built with shapes the pre-freeze direction work did not use: five- and six-row registries,
captures that carry a SHA256SUMS manifest, one row naming two captures with one token per capture, a
provenance markdown table beside the pinned URL route, an over-long row added in a later commit, and a
capture that exists only as a manifest entry. Every fixture builds its own lane from nothing and returns
the anchor tool's argv tail.
"""
import hashlib

HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
COMMIT = "0123456789abcdef0123456789abcdef01234567"
SCOPE = "a-alt battery row"


def sha(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor, teaches, extra=()):
    """One census-shaped registry line: 11 cells, plus any `extra` cells (an over-long row)."""
    cells = [sid, source, "capture", "A", SCOPE, anchor, teaches, "mined", "2026-10-26", "180d", "-"]
    cells.extend(extra)
    return "| " + " | ".join(cells) + " |\n"


def start(ctx, d, sub=""):
    return ctx.init(d / sub) if sub else ctx.init(d)


def capture_dir(ctx, repo, rel, entries):
    """Write every (name, body) under rel plus one SHA256SUMS listing them; return {name: digest}."""
    got, lines = {}, []
    for name, body in entries:
        got[name] = sha(body)
        ctx.write(repo / rel / name, body)
        lines.append(f"{got[name]}  {name}\n")
    ctx.write(repo / rel / "SHA256SUMS", "".join(lines))
    return got


def land(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


# a_alt-1: an over-long row that is a green row copied with one cell appended, inside a five-row registry.
# Demonstrates NA1 (row-malformed must fire on the over-length side, not only the under-length side).
def longrow_copied(ctx, d):
    r = start(ctx, d)
    c = capture_dir(ctx, r, "corpus/evidence/rf/five", [
        ("alpha.txt", b"alpha capture bytes\n"),
        ("bravo.txt", b"bravo capture bytes\n"),
        ("charlie.txt", b"charlie capture bytes\n"),
        ("delta.txt", b"delta capture bytes\n")])
    green = [
        row("S911", "captured at corpus/evidence/rf/five/alpha.txt", f"sha256 {c['alpha.txt']}", "first row"),
        row("S912", "captured at corpus/evidence/rf/five/bravo.txt", f"sha256 {c['bravo.txt']}", "row copied over-long"),
        row("S913", "captured at corpus/evidence/rf/five/charlie.txt", f"sha256 {c['charlie.txt']}", "third row"),
        row("S914", "captured at corpus/evidence/rf/five/delta.txt", f"sha256 {c['delta.txt']}", "fourth row"),
    ]
    over = row("S915", "captured at corpus/evidence/rf/five/bravo.txt", f"sha256 {c['bravo.txt']}",
               "same content, one cell too many", extra=("beyond-the-census",))
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(green[:2] + [over] + green[2:]))
    land(ctx, r, "five-row registry with one over-long row")
    return ["--lane", str(r)]


# a_alt-2: a fourteen-cell row copying a two-capture row, every capture carrying a SHA256SUMS manifest.
# Demonstrates NA1 on a longer over-run, with one token per capture on each copy of the row.
def longrow_multicap(ctx, d):
    r = start(ctx, d, "repo")
    m = capture_dir(ctx, r, "corpus/evidence/rf/multi", [
        ("a.txt", b"first capture of the two-capture row\n"),
        ("b.txt", b"second capture of the two-capture row\n")])
    p = capture_dir(ctx, r, "corpus/evidence/rf/one", [
        ("p.txt", b"single capture p\n"),
        ("q.txt", b"single capture q\n")])
    both = f"sha256 {m['a.txt']} sha256 {m['b.txt']}"
    both_src = "captured at corpus/evidence/rf/multi/a.txt and at corpus/evidence/rf/multi/b.txt"
    registry = [
        row("S921", "captured at corpus/evidence/rf/one/p.txt", f"sha256 {p['p.txt']}", "single capture row"),
        row("S922", "captured at corpus/evidence/rf/one/q.txt", f"sha256 {p['q.txt']}", "single capture row"),
        row("S923", "captured at corpus/evidence/rf/multi/a.txt", f"sha256 {m['a.txt']}", "first of the pair"),
        row("S924", both_src, both, "two captures, one token each"),
        row("S925", both_src, both, "same pair, three cells too many",
            extra=("keep", "going", "fourteenth")),
        row("S926", "captured at corpus/evidence/rf/multi/b.txt", f"sha256 {m['b.txt']}", "second of the pair"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "six-row registry, one row fourteen cells long")
    return ["--lane", str(r)]


# a_alt-3: two task directories, a raw URL whose path names both slugs; the deepest component claims it.
# Demonstrates NA5 (the task.toml name must lose its <org>/ prefix for the exact-component match).
def slug_deepest(ctx, d):
    r = start(ctx, d)
    alpha = capture_dir(ctx, r, "corpus/evidence/rf/alpha", [("payload.txt", b"alpha payload\n")])
    beta = capture_dir(ctx, r, "corpus/evidence/rf/beta", [("payload.txt", b"beta payload\n")])
    ctx.write(r / "corpus/evidence/rf/alpha/task.toml", 'name = "acme/alpha"\n')
    ctx.write(r / "corpus/evidence/rf/beta/task.toml", 'name = "acme/beta"\n')
    plain = capture_dir(ctx, r, "corpus/evidence/rf/plain", [
        ("n1.txt", b"plain capture one\n"),
        ("n2.txt", b"plain capture two\n")])
    url = f"https://raw.githubusercontent.com/acme/probe/{COMMIT}/alpha/beta/payload.txt"
    registry = [
        row("S931", "captured at corpus/evidence/rf/plain/n1.txt", f"sha256 {plain['n1.txt']}", "plain row"),
        row("S932", "captured at corpus/evidence/rf/plain/n2.txt", f"sha256 {plain['n2.txt']}", "plain row"),
        row("S933", f"pinned at {url}", f"sha256 {beta['payload.txt']}",
            "deepest slug component claims the task"),
        row("S934", "captured at corpus/evidence/rf/alpha/payload.txt", f"sha256 {alpha['payload.txt']}",
            "alpha row"),
        row("S935", "captured at corpus/evidence/rf/plain/n1.txt", f"sha256 {plain['n1.txt']}", "plain row again"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "five-row registry with a two-slug URL")
    return ["--lane", str(r)]


# a_alt-4: a pinned github.com blob URL below a task directory that also holds a tests/ subdirectory.
# Demonstrates NA5 through the blob URL form, with the capture at the task directory root.
def slug_blob(ctx, d):
    r = start(ctx, d, "repo")
    scan = capture_dir(ctx, r, "corpus/evidence/rf/scan", [
        ("test_outputs.py", b"# capture the blob URL names\n")])
    ctx.write(r / "corpus/evidence/rf/scan/task.toml", 'name = "vendor/tb-scan"\n')
    ctx.write(r / "corpus/evidence/rf/scan/tests/notes.txt", "supporting note under tests\n")
    plain = capture_dir(ctx, r, "corpus/evidence/rf/plain2", [
        ("s1.txt", b"plain capture s1\n"),
        ("s2.txt", b"plain capture s2\n")])
    url = f"https://github.com/vendor/tb-scan/blob/{COMMIT}/tb-scan/tests/test_outputs.py"
    registry = [
        row("S941", f"pinned at {url}", f"sha256 {scan['test_outputs.py']}",
            "blob URL below a task directory"),
        row("S942", "captured at corpus/evidence/rf/plain2/s1.txt", f"sha256 {plain['s1.txt']}", "plain row"),
        row("S943", "captured at corpus/evidence/rf/plain2/s2.txt", f"sha256 {plain['s2.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "three-row registry with a blob URL")
    return ["--lane", str(r)]


# a_alt-5: a wrong anchor token kept exempt by an erratum that cites the manifest digest of its capture.
# Demonstrates NA7 (a correction token inside the committed digest set must not be flagged) and the
# exemption itself (NA20, NA21) on an otherwise green five-row registry.
def erratum_manifest(ctx, d):
    r = start(ctx, d)
    e = capture_dir(ctx, r, "corpus/evidence/rf/err", [
        ("notes.txt", b"capture the erratum corrects\n")])
    good, stale = e["notes.txt"], sha(b"the token S953 carried before the erratum\n")
    ctx.write(r / "corpus/lessons/r43-a.md",
              f"Erratum (round 37): S953 anchor sha256 {stale} was wrong; the capture's manifest "
              f"digest is sha256 {good}.\n")
    p = capture_dir(ctx, r, "corpus/evidence/rf/plain3", [
        ("p.txt", b"plain capture p3\n"),
        ("q.txt", b"plain capture q3\n")])
    registry = [
        row("S951", "captured at corpus/evidence/rf/plain3/p.txt", f"sha256 {p['p.txt']}", "plain row"),
        row("S952", "captured at corpus/evidence/rf/plain3/q.txt", f"sha256 {p['q.txt']}", "plain row"),
        row("S953", "captured at corpus/evidence/rf/err/notes.txt", f"sha256 {stale}",
            "wrong token kept exempt"),
        row("S954", "captured at corpus/evidence/rf/plain3/p.txt", f"sha256 {p['p.txt']}", "plain row again"),
        row("S955", "captured at corpus/evidence/rf/plain3/q.txt", f"sha256 {p['q.txt']}", "plain row again"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "erratum keeps one wrong token green")
    return ["--lane", str(r)]


# a_alt-6: a provenance table binds the row; its erratum also cites a sibling capture's committed digest.
# Demonstrates NA7 with three 64-hex tokens on one erratum line (only the corrected one may be exempt-prone).
def erratum_sibling(ctx, d):
    r = start(ctx, d, "repo")
    prov = capture_dir(ctx, r, "corpus/evidence/rp/prov", [
        ("notes.txt", b"capture the provenance table names\n")])
    sib = capture_dir(ctx, r, "corpus/evidence/rp/sib", [
        ("other.txt", b"sibling capture outside the row\n")])
    good, stale = prov["notes.txt"], sha(b"the token S962 carried before the erratum\n")
    url = f"https://raw.githubusercontent.com/acme/rel/{COMMIT}/checks/notes.txt"
    ctx.write(r / "corpus/evidence/rp/prov/PROVENANCE.md",
              "| row | capture | upstream |\n|---|---|---|\n"
              f"| S962 | `notes.txt` | {url} |\n")
    ctx.write(r / "corpus/lessons/r43-b.md",
              f"Erratum (round 37): S962 anchor sha256 {stale} predates the repair; sha256 "
              f"{sib['other.txt']} belongs to another capture, and the correction is sha256 {good}.\n")
    p = capture_dir(ctx, r, "corpus/evidence/rp/plain", [
        ("t1.txt", b"plain capture t1\n"),
        ("t2.txt", b"plain capture t2\n")])
    registry = [
        row("S961", "captured at corpus/evidence/rp/plain/t1.txt", f"sha256 {p['t1.txt']}", "plain row"),
        row("S962", f"pinned at {url}", f"sha256 {stale}", "wrong token kept exempt"),
        row("S963", "captured at corpus/evidence/rp/plain/t2.txt", f"sha256 {p['t2.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "provenance row kept green by an erratum with three tokens")
    return ["--lane", str(r)]


# a_alt-7: the exempted row's anchor token is a 63-hex prefix of its capture digest.
# Demonstrates NA20 (every anchor class is exempted, including digest-short) and NA21's citation lookup.
def erratum_short(ctx, d):
    r = start(ctx, d)
    e = capture_dir(ctx, r, "corpus/evidence/rf/short", [
        ("notes.txt", b"capture for the short-token row\n")])
    good = e["notes.txt"]
    short = good[:63]
    ctx.write(r / "corpus/lessons/r43-d.md",
              f"Erratum (round 37): S971 anchor sha256 {short} is a prefix; the full digest is "
              f"sha256 {good}.\n")
    p = capture_dir(ctx, r, "corpus/evidence/rf/plain4", [
        ("u1.txt", b"plain capture u1\n"),
        ("u2.txt", b"plain capture u2\n")])
    registry = [
        row("S972", "captured at corpus/evidence/rf/plain4/u1.txt", f"sha256 {p['u1.txt']}", "plain row"),
        row("S971", "captured at corpus/evidence/rf/short/notes.txt", f"sha256 {short}",
            "63-hex token kept exempt"),
        row("S973", "captured at corpus/evidence/rf/plain4/u2.txt", f"sha256 {p['u2.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "erratum keeps a short token green")
    return ["--lane", str(r)]


# a_alt-8: the exempted row's token is the capture digest written in uppercase.
# Demonstrates NA20 on the digest-uppercase class, with the manifest beside the capture.
def erratum_upper(ctx, d):
    r = start(ctx, d, "repo")
    e = capture_dir(ctx, r, "corpus/evidence/rf/upper", [
        ("notes.txt", b"capture for the uppercase-token row\n")])
    good = e["notes.txt"]
    upper = good.upper()
    ctx.write(r / "corpus/lessons/r43-f.md",
              f"Erratum (round 37): S981 anchor sha256 {upper} was written in the wrong case; the "
              f"correction is sha256 {good}.\n")
    p = capture_dir(ctx, r, "corpus/evidence/rf/plain5", [
        ("v1.txt", b"plain capture v1\n"),
        ("v2.txt", b"plain capture v2\n")])
    registry = [
        row("S982", "captured at corpus/evidence/rf/plain5/v1.txt", f"sha256 {p['v1.txt']}", "plain row"),
        row("S981", "captured at corpus/evidence/rf/upper/notes.txt", f"sha256 {upper}",
            "uppercase token kept exempt"),
        row("S983", "captured at corpus/evidence/rf/plain5/v2.txt", f"sha256 {p['v2.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "erratum keeps an uppercase token green")
    return ["--lane", str(r)]


# a_alt-9: two provenance rows on one lane, each kept green by its own erratum in its own lesson file.
# Demonstrates NA21 (the wrong-token lookup keys on the row's tokens, not on the row ids) twice over.
def erratum_two(ctx, d):
    r = start(ctx, d)
    c = capture_dir(ctx, r, "corpus/evidence/rq/prov", [
        ("notes.txt", b"first provenance capture\n"),
        ("second.txt", b"second provenance capture\n")])
    stale1 = sha(b"the token S991 carried before its erratum\n")
    stale2 = sha(b"the token S993 carried before its erratum\n")
    ctx.write(r / "corpus/evidence/rq/prov/PROVENANCE.md",
              "| row | capture | upstream |\n|---|---|---|\n"
              f"| S991 | `notes.txt` | https://raw.githubusercontent.com/acme/rel/{COMMIT}/checks/notes.txt |\n"
              f"| S992 | `second.txt` | https://raw.githubusercontent.com/acme/rel/{COMMIT}/checks/second.txt |\n"
              f"| S993 | `second.txt` | https://raw.githubusercontent.com/acme/rel/{COMMIT}/checks/plain/second.txt |\n")
    ctx.write(r / "corpus/lessons/r43-c.md",
              f"Erratum (round 37): S991 anchor sha256 {stale1} predates the repair; the capture digest is "
              f"sha256 {c['notes.txt']}.\n")
    ctx.write(r / "corpus/lessons/r43-g.md",
              f"Erratum (round 37): S993 anchor sha256 {stale2} predates the repair; the capture digest is "
              f"sha256 {c['second.txt']}.\n")
    p = capture_dir(ctx, r, "corpus/evidence/rq/plain", [
        ("w1.txt", b"plain capture w1\n"),
        ("w2.txt", b"plain capture w2\n"),
        ("w3.txt", b"plain capture w3\n")])
    registry = [
        row("S991", "captured for the first provenance row", f"sha256 {stale1}", "wrong token kept exempt"),
        row("S992", "captured for the second provenance row", f"sha256 {c['second.txt']}", "provenance row"),
        row("S993", "captured for the third provenance row", f"sha256 {stale2}", "wrong token kept exempt"),
        row("S994", "captured at corpus/evidence/rq/plain/w1.txt", f"sha256 {p['w1.txt']}", "plain row"),
        row("S995", "captured at corpus/evidence/rq/plain/w2.txt", f"sha256 {p['w2.txt']}", "plain row"),
        row("S996", "captured at corpus/evidence/rq/plain/w3.txt", f"sha256 {p['w3.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "six-row registry with two erratum exemptions")
    return ["--lane", str(r)]


# a_alt-10: one erratum per lesson file for two rows, beside a two-capture row that must carry both tokens.
# Demonstrates NA21 with two lesson files and a lane path binding rather than a provenance table.
def erratum_lessons(ctx, d):
    r = start(ctx, d, "repo")
    c = capture_dir(ctx, r, "corpus/evidence/rr/one", [
        ("alpha.txt", b"first capture of the pair\n"),
        ("beta.txt", b"second capture of the pair\n")])
    p = capture_dir(ctx, r, "corpus/evidence/rr/plain", [
        ("p.txt", b"plain capture p\n"),
        ("q.txt", b"plain capture q\n")])
    stale1 = sha(b"the token S1011 carried before its erratum\n")
    stale2 = sha(b"the token S1016 carried before its erratum\n")
    ctx.write(r / "corpus/lessons/r43-e.md",
              f"Erratum (round 37): S1011 anchor sha256 {stale1} predates the repair; the capture digest is "
              f"sha256 {c['alpha.txt']}.\n")
    ctx.write(r / "corpus/lessons/r43-h.md",
              f"Erratum (round 37): S1016 anchor sha256 {stale2} predates the repair; the capture digest is "
              f"sha256 {p['q.txt']}.\n")
    registry = [
        row("S1011", "captured at corpus/evidence/rr/one/alpha.txt", f"sha256 {stale1}",
            "wrong token kept exempt"),
        row("S1012", "captured at corpus/evidence/rr/one/alpha.txt and at corpus/evidence/rr/one/beta.txt",
            f"sha256 {c['alpha.txt']} sha256 {c['beta.txt']}", "two captures, one token each"),
        row("S1013", "captured at corpus/evidence/rr/plain/p.txt", f"sha256 {p['p.txt']}", "plain row"),
        row("S1014", "captured at corpus/evidence/rr/plain/q.txt", f"sha256 {p['q.txt']}", "plain row"),
        row("S1015", "captured at corpus/evidence/rr/one/beta.txt", f"sha256 {c['beta.txt']}", "pair member"),
        row("S1016", "captured at corpus/evidence/rr/plain/q.txt", f"sha256 {stale2}",
            "wrong token kept exempt"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "two lesson files, two exemptions, one two-capture row")
    return ["--lane", str(r)]


# a_alt-11: an over-long row enters the registry in a second commit, a lesson in a third.
# Demonstrates NA1 on a history where the malformed row is not in the lane's first commit.
def longrow_late(ctx, d):
    r = start(ctx, d)
    c = capture_dir(ctx, r, "corpus/evidence/rf/late", [
        ("one.txt", b"late capture one\n"),
        ("two.txt", b"late capture two\n")])
    green = [
        row("S1031", "captured at corpus/evidence/rf/late/one.txt", f"sha256 {c['one.txt']}", "first row"),
        row("S1032", "captured at corpus/evidence/rf/late/two.txt", f"sha256 {c['two.txt']}", "second row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(green))
    land(ctx, r, "first commit: two green rows and their captures")
    over = row("S1033", "captured at corpus/evidence/rf/late/one.txt", f"sha256 {c['one.txt']}",
               "row copied over-long in a later commit", extra=("later", "commit"))
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(green + [over]))
    land(ctx, r, "second commit adds a thirteen-cell row")
    ctx.write(r / "corpus/lessons/r43-i.md", "# round forty-three\n\nNo erratum is recorded here.\n")
    land(ctx, r, "third commit adds an unrelated lesson")
    return ["--lane", str(r)]


# a_alt-12: a task directory whose capture exists only as an entry in its SHA256SUMS manifest.
# Demonstrates NA5 on the manifest-only route: without the slug the row has no binding at all.
def slug_manifest(ctx, d):
    r = start(ctx, d)
    ghost = sha(b"a report that was never committed, only manifested\n")
    ctx.write(r / "corpus/evidence/rs/ghost/task.toml", 'name = "acme/ghost"\n')
    ctx.write(r / "corpus/evidence/rs/ghost/SHA256SUMS", f"{ghost}  report.txt\n")
    p = capture_dir(ctx, r, "corpus/evidence/rs/plain", [
        ("r1.txt", b"plain capture r1\n"),
        ("r2.txt", b"plain capture r2\n")])
    url = f"https://raw.githubusercontent.com/acme/probe/{COMMIT}/ghost/report.txt"
    registry = [
        row("S1041", f"pinned at {url}", f"sha256 {ghost}", "capture held by the manifest alone"),
        row("S1042", "captured at corpus/evidence/rs/plain/r1.txt", f"sha256 {p['r1.txt']}", "plain row"),
        row("S1043", "captured at corpus/evidence/rs/plain/r2.txt", f"sha256 {p['r2.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "three-row registry with a manifest-only capture")
    return ["--lane", str(r)]


# a_alt-13: a five-hex commit segment on a raw URL that names a second task's capture, beside a lane path.
# Demonstrates NA18 (the commit floor is 7 hex; a shorter segment must not bind the row elsewhere).
def shorturl_sibling(ctx, d):
    r = start(ctx, d)
    a = capture_dir(ctx, r, "corpus/evidence/rt/alpha", [("notes.txt", b"capture the lane path names\n")])
    b = capture_dir(ctx, r, "corpus/evidence/rt/beta", [("other.txt", b"capture the short URL would name\n")])
    ctx.write(r / "corpus/evidence/rt/beta/task.toml", 'name = "acme/beta"\n')
    url = "https://raw.githubusercontent.com/acme/probe/abc12/beta/other.txt"
    registry = [
        row("S1051", f"captured at corpus/evidence/rt/alpha/notes.txt, pinned at {url}",
            f"sha256 {a['notes.txt']}", "lane path beside a five-hex pinned URL"),
        row("S1052", "captured at corpus/evidence/rt/beta/other.txt", f"sha256 {b['other.txt']}",
            "the URL's own capture, bound by its lane path"),
        row("S1053", "captured at corpus/evidence/rt/alpha/notes.txt", f"sha256 {a['notes.txt']}", "plain row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "three-row registry with a five-hex commit segment")
    return ["--lane", str(r)]


# a_alt-14: a four-hex commit segment naming another capture inside the same task directory.
# Demonstrates NA18 where the short URL and the lane path share a directory but not a capture.
def shorturl_samedir(ctx, d):
    r = start(ctx, d, "repo")
    g = capture_dir(ctx, r, "corpus/evidence/rt2/gamma", [
        ("report.txt", b"the report the short URL names\n"),
        ("appendix.txt", b"the appendix the lane path names\n")])
    ctx.write(r / "corpus/evidence/rt2/gamma/task.toml", 'name = "acme/gamma"\n')
    url = "https://raw.githubusercontent.com/acme/probe/9f3e/gamma/report.txt"
    registry = [
        row("S1061", f"captured at corpus/evidence/rt2/gamma/appendix.txt, pinned at {url}",
            f"sha256 {g['appendix.txt']}", "lane path beside a four-hex pinned URL"),
        row("S1062", "captured at corpus/evidence/rt2/gamma/report.txt", f"sha256 {g['report.txt']}",
            "the report, bound by its lane path"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(registry))
    land(ctx, r, "two-row registry, one task directory, a four-hex commit segment")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "a_alt-longrow-copied", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": longrow_copied},
    {"fid": "a_alt-longrow-multicap", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": longrow_multicap},
    {"fid": "a_alt-slug-deepest", "tool": "anchor", "expect": "accept", "defects": [],
     "build": slug_deepest},
    {"fid": "a_alt-slug-blob", "tool": "anchor", "expect": "accept", "defects": [],
     "build": slug_blob},
    {"fid": "a_alt-erratum-manifest", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_manifest},
    {"fid": "a_alt-erratum-sibling", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_sibling},
    {"fid": "a_alt-erratum-short", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_short},
    {"fid": "a_alt-erratum-upper", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_upper},
    {"fid": "a_alt-erratum-two", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_two},
    {"fid": "a_alt-erratum-lessons", "tool": "anchor", "expect": "accept", "defects": [],
     "build": erratum_lessons},
    {"fid": "a_alt-longrow-late", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": longrow_late},
    {"fid": "a_alt-slug-manifest", "tool": "anchor", "expect": "accept", "defects": [],
     "build": slug_manifest},
    {"fid": "a_alt-shorturl-sibling", "tool": "anchor", "expect": "accept", "defects": [],
     "build": shorturl_sibling},
    {"fid": "a_alt-shorturl-samedir", "tool": "anchor", "expect": "accept", "defects": [],
     "build": shorturl_samedir},
]
