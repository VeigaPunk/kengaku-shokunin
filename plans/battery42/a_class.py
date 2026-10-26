"""Round-42 C1 battery42 module `a_class`: attributed kills for the three frozen anchor near-variants X6, X7
and X14 of `plans/round42_c1_verify.py`.

Tool under test: `plans/anchor_digest_check.py` (read-only there). Each fixture builds a git repository from
nothing inside its own empty fixture directory and returns `["--lane", <repo>]`; the tool runs with the fixture
directory as its working directory. No lane clone and no pre-existing repository is read.

Two fixtures per mutant. The first reaches the mutated branch directly; the second differs in shape -- a
multi-row registry, a different binding route (a task.toml URL or a provenance table line instead of an
explicit lane path), a multi-commit history, and for X6 a manifest-listed digest instead of a file digest --
and reaches the same branch a second way.

  x6-sibling-digest     X6 (silence) a row that names capture A carries capture B's committed file digest
  x6-stale-manifest     X6 (silence) the token is the stale digest a sibling directory's SHA256SUMS still
                        lists for a recaptured file; the row binds through a task.toml URL in a three-row
                        registry written in two commits
  x7-fabricated-token   X7 (silence) a row that names a committed capture carries a made-up 64-hex token
  x7-provenance-row     X7 (silence) the same branch, the row bound by a PROVENANCE.md table line, in a
                        registry whose second commit adds the defective row beside a resolvable abbreviation
  x14-uppercase-token   X14 (silence) an erratum line carries an UPPERCASE 64-hex token no capture has
  x14-two-errata        X14 (silence) two rows and two errata: a clean erratum whose correction exempts its
                        row, and in a second commit a wrong-case erratum for the other row

Every `defects` set is the exact class set the unmodified tool prints on that fixture; `expect` is the
reference exit code (1 = reject for all three classes).
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def sha(body):
    return hashlib.sha256(body).hexdigest()


def entry(sid, source, anchor):
    return (f"| {sid} | {source} | capture | A | fixture-scalar | {anchor} | fixture row for the anchor "
            "classes | mined | 2026-10-26 | 180d | - |")


def capture(ctx, repo, rel, name, body):
    ctx.write(repo / "corpus/evidence" / rel / name, body)
    return sha(body)


def landed(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def x6_sibling_digest(ctx, d):
    """One row naming capture A, its anchor cell carrying capture B's committed digest."""
    r = ctx.init(d / "repo")
    capture(ctx, r, "round42/a-class/x6-a", "notes.txt", b"capture A: the capture this row names\n")
    sib = capture(ctx, r, "round42/a-class/x6-b", "notes.txt", b"capture B: another row's capture\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S301", "captured at corpus/evidence/round42/a-class/x6-a/notes.txt",
                             f"sha256 {sib}") + "\n")
    landed(ctx, r, "fixture: two captures, one row carrying the sibling's digest")
    return ["--lane", str(r)]


def x6_stale_manifest(ctx, d):
    """Three-row registry in two commits; the bad row binds through a task.toml URL and its token is the
    stale digest a sibling directory's manifest still lists for a recaptured file."""
    r = ctx.init(d / "repo")
    url = ("https://raw.githubusercontent.com/acme/gatekeep/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/gatekeep/tests/test_outputs.py")
    keep = b"gated artefact, as committed\n"
    ctx.write(r / "corpus/evidence/round42/a-class/x6-url/test_outputs.py", keep)
    ctx.write(r / "corpus/evidence/round42/a-class/x6-url/task.toml", 'name = "acme/gatekeep"\n')
    ctx.write(r / "corpus/evidence/round42/a-class/x6-url/SHA256SUMS", f"{sha(keep)}  test_outputs.py\n")
    first = b"sibling artefact, first capture\n"
    late = b"sibling artefact, recaptured\n"
    ctx.write(r / "corpus/evidence/round42/a-class/x6-side/artefact.bin", late)
    ctx.write(r / "corpus/evidence/round42/a-class/x6-side/SHA256SUMS", f"{sha(first)}  artefact.bin\n")
    green = (HEADER
             + entry("S310", f"pinned at `{url}`", f"sha256 {sha(keep)}") + "\n"
             + entry("S311", "captured at corpus/evidence/round42/a-class/x6-side/artefact.bin",
                     f"sha256 {sha(late)}") + "\n")
    ctx.write(r / "corpus/SOURCES.md", green)
    landed(ctx, r, "fixture: the pinned artefact and the sibling capture, both green")
    ctx.write(r / "corpus/SOURCES.md",
              green + entry("S312", f"pinned at `{url}`", f"sha256 {sha(first)}") + "\n")
    landed(ctx, r, "fixture: one row anchored on the sibling manifest's stale digest")
    return ["--lane", str(r)]


def x7_fabricated_token(ctx, d):
    """One row naming a committed capture, its anchor cell carrying a 64-hex token no capture has."""
    r = ctx.init(d / "repo")
    capture(ctx, r, "round42/a-class/x7", "notes.txt", b"the capture this row names\n")
    made = sha(b"no capture anywhere carries this: a-class x7\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S320", "captured at corpus/evidence/round42/a-class/x7/notes.txt",
                             f"sha256 {made}") + "\n")
    landed(ctx, r, "fixture: one row, one made-up digest")
    return ["--lane", str(r)]


def x7_provenance_row(ctx, d):
    """The row binds through a PROVENANCE.md table line; the second commit adds the defective row and a
    third row whose anchor is a resolvable 12-hex abbreviation of the same capture."""
    r = ctx.init(d / "repo")
    body = b"capture bound through the provenance table\n"
    base = r / "corpus/evidence/round42/a-class/x7b"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "PROVENANCE.md",
              "| sid | file | note |\n|---|---|---|\n"
              "| S330 | `test_outputs.py` | captured beside this table, no upstream URL |\n"
              "| S331 | `test_outputs.py` | the same capture, second row |\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S330", "captured for the x7 registry", f"sha256 {sha(body)}") + "\n")
    landed(ctx, r, "fixture: the capture and one green row")
    made = sha(b"no capture anywhere carries this: a-class x7b\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER
              + entry("S330", "captured for the x7 registry", f"sha256 {sha(body)}") + "\n"
              + entry("S331", "captured for the x7 registry", f"sha256 {made}") + "\n"
              + entry("S332", "captured at corpus/evidence/round42/a-class/x7b/test_outputs.py",
                      f"sha256 {sha(body)[:12]}...") + "\n")
    landed(ctx, r, "fixture: a made-up digest and a resolvable abbreviation")
    return ["--lane", str(r)]


def x14_uppercase_token(ctx, d):
    """A committed erratum line carries an uppercase 64-hex token no capture has, beside the true digest."""
    r = ctx.init(d / "repo")
    good = capture(ctx, r, "round42/a-class/x14", "outputs.txt", b"the capture this erratum row names\n")
    loud = sha(b"this token was never committed: a-class x14\n").upper()
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S340 anchor sha256 {loud} is in no committed manifest; the capture's "
              f"digest is sha256 {good}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + entry("S340", "captured at corpus/evidence/round42/a-class/x14/outputs.txt",
                             f"sha256 {good}") + "\n")
    landed(ctx, r, "fixture: an erratum line with an uppercase uncommitted token")
    return ["--lane", str(r)]


def x14_two_errata(ctx, d):
    """Two rows: the first carries a stale token and is exempted by a clean erratum whose correction is its
    capture's digest; a second commit adds a wrong-case erratum for the second row."""
    r = ctx.init(d / "repo")
    one = capture(ctx, r, "round42/a-class/x14b-a", "part1.txt", b"first capture of the pair\n")
    two = capture(ctx, r, "round42/a-class/x14b-b", "part2.txt", b"second capture of the pair\n")
    stale = sha(b"the digest S350 carried before its repair: a-class x14b\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S350 anchor sha256 {stale} was wrong; the capture's digest is "
              f"sha256 {one}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER
              + entry("S350", "captured at corpus/evidence/round42/a-class/x14b-a/part1.txt",
                      f"sha256 {stale}") + "\n"
              + entry("S351", "captured at corpus/evidence/round42/a-class/x14b-b/part2.txt",
                      f"sha256 {two}") + "\n")
    landed(ctx, r, "fixture: two rows, the first exempted by a clean erratum")
    loud = sha(b"this token was never committed: a-class x14b\n").upper()
    ctx.write(r / "corpus/lessons/round-42.md",
              f"Erratum (round 37): S351 anchor sha256 {loud} was transcribed in the wrong case; the "
              f"capture's digest is sha256 {two}.\n")
    landed(ctx, r, "fixture: a second erratum carrying an uppercase uncommitted token")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "a_class-x6-sibling-digest", "tool": "anchor", "expect": "reject", "defects": ["digest-wrong-capture"], "build": x6_sibling_digest},  # X6: the anchor cell carries a sibling capture's committed file digest
    {"fid": "a_class-x6-stale-manifest", "tool": "anchor", "expect": "reject", "defects": ["digest-wrong-capture"], "build": x6_stale_manifest},  # X6 again: the token is a sibling manifest's stale digest, the row bound by a task.toml URL in a three-row, two-commit registry
    {"fid": "a_class-x7-fabricated-token", "tool": "anchor", "expect": "reject", "defects": ["digest-unknown"], "build": x7_fabricated_token},  # X7: the anchor cell carries a 64-hex token no capture has
    {"fid": "a_class-x7-provenance-row", "tool": "anchor", "expect": "reject", "defects": ["digest-unknown"], "build": x7_provenance_row},  # X7 again: made-up digest, the row bound by a PROVENANCE.md table line beside a resolvable abbreviation row
    {"fid": "a_class-x14-uppercase-token", "tool": "anchor", "expect": "reject", "defects": ["erratum-digest-unresolved"], "build": x14_uppercase_token},  # X14: a committed erratum line carries an uppercase 64-hex token no capture has
    {"fid": "a_class-x14-two-errata", "tool": "anchor", "expect": "reject", "defects": ["erratum-digest-unresolved"], "build": x14_two_errata},  # X14 again: a wrong-case erratum appended in a second commit beside a clean erratum that exempts its own row
]
