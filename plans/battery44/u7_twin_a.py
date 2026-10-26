"""u7_twin_a - battery44 module (seat R44BatU7a, kengaku round 44).

`plans/anchor_digest_check.py:98-99` advertises that a token resolving to several of one row's captures is
not a defect: those captures have identical bytes and the one digest is the true digest of each of them.
Frozen mutant U7 narrows the claim to the first resolving capture (`hit = sorted(...)[:1]`), so every other
capture of a byte-identical pair is left `capture-unanchored`: exit 1 where the unmodified tool exits 0
(direction rc-mirror). Every fixture below is a committed repository built from nothing and is green under
the unmodified tool (expect=accept, defects=[]; one row makes no anchor claim and the rest are single-capture
rows with their own token).

Three shapes, three binding routes, none a re-spelling of another module of this wave:
  1. twin filings in one evidence directory, named by the row's own lane paths, in a five-row registry whose
     twin row arrives in a second commit;
  2. a row bound by a PROVENANCE.md table whose two lines name the two twin files, the second line also
     arriving in a second commit;
  3. a row bound by two pinned upstream raw URLs under two task.toml directories whose files are identical.
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
COMMIT = "0123456789abcdef0123456789abcdef01234567"


def digest(body):
    return hashlib.sha256(body).hexdigest()


def row(cells):
    return "| " + " | ".join(cells) + " |\n"


def land(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def twin_rowpath_registry(ctx, d):
    """Twin filings in one evidence directory named by the row's own lane paths: five rows, two commits.

    Reference: the single token resolves to both filings, both are claimed, no defect, exit 0. U7 claims only
    the sorted-first filing, so `ledger.txt` is reported `capture-unanchored`."""
    r = ctx.init(d / "registry")
    led = "corpus/evidence/u7a-ledger/ledger.txt"
    mirror = "corpus/evidence/u7a-ledger/ledger-mirror.txt"
    side = "corpus/evidence/u7a-ledger/note.txt"
    twin = b"u7 twin: one receipt filed under two names\n"
    note = b"a neighbouring capture that shares nothing with the twins\n"
    ctx.write(r / led, twin)
    ctx.write(r / side, note)

    def registry(second):
        scope = f"captured at {led}" + (f" and {mirror}" if second else "")
        anchor = f"sha256 {digest(twin)}" if second else ""
        return HEADER + "".join([
            row(["S500", f"captured at {led}", "capture", "A", "ledger",
                 f"sha256 {digest(twin)}", "the ledger receipt", "mined", "2026-10-26", "180d", "-"]),
            row(["S501", scope, "capture", "A", "mirror", anchor,
                 "one digest, two byte-identical filings", "mined", "2026-10-26", "180d", "-"]),
            row(["S502", f"captured at {side}", "capture", "A", "note",
                 f"sha256 {digest(note)}", "neighbouring note", "mined", "2026-10-26", "180d", "-"]),
            row(["S503", "no committed capture yet", "capture", "B", "pending", "",
                 "row making no anchor claim", "queued", "2026-10-26", "90d", "-"]),
        ])

    ctx.write(r / "corpus/SOURCES.md", registry(False))
    land(ctx, r, "five-row registry with the ledger receipt filed once")
    ctx.write(r / mirror, twin)
    ctx.write(r / "corpus/SOURCES.md", registry(True))
    land(ctx, r, "the ledger receipt mirrored and its row naming both filings")
    return ["--lane", str(r)]


def twin_provenance_table(ctx, d):
    """Two provenance-table lines bind one row to two identical files, the second line in a second commit.

    Reference: the row's two captures are both claimed by the single token, exit 0. U7 claims only the first,
    so the second capture is `capture-unanchored`."""
    r = ctx.init(d)
    twin = b"u7 twin: one provenance record, two filenames\n"
    base = "corpus/evidence/u7b-prov"
    ctx.write(r / f"{base}/record.txt", twin)
    ctx.write(r / "corpus/SOURCES.md", HEADER + row(
        ["S610", f"provenance table under {base}/", "capture", "A", "record",
         f"sha256 {digest(twin)}", "row bound by its provenance table", "mined", "2026-10-26", "180d", "-"]))

    def table(names):
        lines = ["| row | capture |", "|---|---|"]
        lines += [f"| S610 | `{n}` |" for n in names]
        return "\n".join(lines) + "\n"

    ctx.write(r / f"{base}/PROVENANCE.md", table(["record.txt"]))
    land(ctx, r, "provenance row with the record filed once")
    ctx.write(r / f"{base}/record-copy.txt", twin)
    ctx.write(r / f"{base}/PROVENANCE.md", table(["record.txt", "record-copy.txt"]))
    land(ctx, r, "a second filename for the same record, bound by a second table line")
    return ["--lane", str(r)]


def twin_url_two_tasks(ctx, d):
    """One row bound by two pinned raw URLs over two task.toml directories holding identical programs.

    Reference: both task files resolve to the one token and are claimed, exit 0. U7 claims the sorted-first
    task directory only, so the other file is `capture-unanchored`."""
    r = ctx.init(d / "repo")
    body = b"def solve(report):\n    return report\n"
    slugs = ("u7gamma", "u7delta")
    for slug in slugs:
        ctx.write(r / f"corpus/evidence/u7-url/{slug}/task.toml", f'name = "acme/{slug}"\n')
        ctx.write(r / f"corpus/evidence/u7-url/{slug}/solve.py", body)
    urls = " ".join(f"https://raw.githubusercontent.com/acme/bench/{COMMIT}/{slug}/solve.py" for slug in slugs)
    ctx.write(r / "corpus/SOURCES.md", HEADER + row(
        ["S620", f"mirrored task files at {urls}", "capture", "A", "mirrored",
         f"sha256 {digest(body)}", "two task directories carrying one program", "mined", "2026-10-26",
         "180d", "-"]))
    land(ctx, r, "one program pinned from two task directories")
    return ["--lane", str(r)]


FIXTURES = [
    # one digest claimed for two filings named by the row's own lane paths; the mutant leaves one unanchored
    {"fid": "u7_twin_a-rowpath-registry", "tool": "anchor", "expect": "accept", "defects": [],
     "build": twin_rowpath_registry},
    # the same branch reached through a provenance table grown one line per commit
    {"fid": "u7_twin_a-provenance-table", "tool": "anchor", "expect": "accept", "defects": [],
     "build": twin_provenance_table},
    # the same branch reached through two pinned raw URLs under two task directories
    {"fid": "u7_twin_a-url-two-tasks", "tool": "anchor", "expect": "accept", "defects": [],
     "build": twin_url_two_tasks},
]
