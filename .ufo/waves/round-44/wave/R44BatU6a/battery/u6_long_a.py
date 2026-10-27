"""battery44 module u6_long_a (seat R44BatU6a, kengaku round 44 wave 2).

Frozen mutant U6 rewrites the length test at plans/anchor_digest_check.py:522 so that every anchor token
which is not 64 lowercase hex digits is labelled `digest-short`, whichever side of 64 it falls on. The
advertised behaviour (plans/anchor_digest_check.py:88, "any other anchor token must be exactly 64 lowercase
hex digits (`digest-short`, `digest-long`, `digest-uppercase` otherwise)") is a two-sided label: shorter
than 64 digits is `digest-short`, longer than 64 is `digest-long`.

Every fixture here carries an anchor token LONGER than 64 hex digits on a row that the unmodified tool
binds to a capture, so the unmodified tool prints exactly one `class=digest-long` defect and exits 1. The
relabelled tool prints `class=digest-short` instead, loses `digest-long` and exits 1 as well: the kill is
silent (same exit status, different class set), which is the direction the frozen mutant declares.

Four shapes, each built from nothing, none of them a single bare row:
  1. a five-row registry whose long token is a TRUE digest with one hex digit appended, so the label is
     decided by length alone and not by membership in the row's capture set;
  2. a capture that exists only as a SHA256SUMS manifest entry (`bulk.bin` is never committed as a blob),
     bound through that manifest, with a 96-digit token;
  3. a row bound by a PROVENANCE.md table line (no path and no URL in the row itself), 128-digit token;
  4. a two-commit history: the capture and a clean row land first, the long (200-digit) token is appended
     in a second commit, so the defect is reported for the working tree against HEAD's evidence.
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor, teaches):
    """One census-shaped registry line: eleven cells, the anchor claim in cell six."""
    cells = [sid, source, "capture", "A", "u6 long-token battery", anchor, teaches,
             "mined", "2026-10-26", "-", "-"]
    return "| " + " | ".join(cells) + " |\n"


def land(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


# u6_long_a-registry-65: a five-row registry; the fourth row's token is a real digest plus one hex digit,
# so the 65-digit side of the advertised label is the only thing that decides its class.
def registry_65(ctx, d):
    repo = ctx.init(d)
    caps = [("alpha", b"u6a alpha capture line\n" * 4),
            ("bravo", b"u6a bravo capture line\n"),
            ("charlie", b"u6a charlie capture line\n" * 2),
            ("delta", b"u6a delta capture line\n" * 3)]
    dig = {}
    for name, body in caps:
        dig[name] = digest(body)
        ctx.write(repo / f"corpus/evidence/u6a/registry/{name}.txt", body)
    rows = [
        row("S961", "captured at corpus/evidence/u6a/registry/alpha.txt",
            "sha256 " + dig["alpha"], "clean first row"),
        row("S962", "captured at corpus/evidence/u6a/registry/bravo.txt",
            "sha256 " + dig["bravo"], "clean second row"),
        row("S963", "captured at corpus/evidence/u6a/registry/charlie.txt",
            "sha256 " + dig["charlie"] + "7", "true digest with one digit appended"),
        row("S964", "captured at corpus/evidence/u6a/registry/delta.txt",
            "sha256 " + dig["delta"], "clean fourth row"),
        row("S965", "captured at corpus/evidence/u6a/registry/charlie.txt",
            "sha256 " + dig["charlie"], "same capture as the long-token row"),
    ]
    ctx.write(repo / "corpus/SOURCES.md", HEADER + "".join(rows))
    land(ctx, repo, "five-row registry, one appended-digit anchor token")
    return ["--lane", str(repo)]


# u6_long_a-manifest-96: the capture is not committed as a blob at all; the row binds through the
# SHA256SUMS entry that lists it, and its anchor token is 96 hex digits.
def manifest_96(ctx, d):
    repo = ctx.init(d)
    bulk = b"bulk payload line for the manifest-only capture\n" * 40
    listed = digest(bulk)
    ctx.write(repo / "corpus/evidence/u6a/bulk/SHA256SUMS", f"{listed} *bulk.bin\n")
    ctx.write(repo / "corpus/evidence/u6a/bulk/notes.md",
              "bulk.bin is published through this manifest and is not committed here\n")
    tok = (digest(b"u6a-manifest") * 2)[:96]
    rows = [row("S971", "captured at corpus/evidence/u6a/bulk/bulk.bin",
                "sha256 " + tok, "manifest-only capture, 96-digit token")]
    ctx.write(repo / "corpus/SOURCES.md", HEADER + "".join(rows))
    land(ctx, repo, "registry row bound through a SHA256SUMS entry")
    return ["--lane", str(repo)]


# u6_long_a-provenance-128: the row names no path and no URL; its capture comes from the PROVENANCE.md
# table beside the capture, and its anchor token is 128 hex digits.
def provenance_128(ctx, d):
    repo = ctx.init(d)
    body = b"provenance-bound capture line\n" * 3
    ctx.write(repo / "corpus/evidence/u6a/prov/beta.bin", body)
    ctx.write(repo / "corpus/evidence/u6a/prov/PROVENANCE.md",
              "| sid | capture | how |\n|-----|---------|-----|\n"
              "| S981 S982 | `beta.bin` | fetched once by the seat |\n")
    tok = (digest(b"u6a-provenance") * 2)[:128]
    rows = [row("S981", "provenance table row", "sha256 " + tok, "provenance-bound, 128-digit token"),
            row("S982", "provenance table row", "sha256 " + digest(body), "same table, clean row")]
    ctx.write(repo / "corpus/SOURCES.md", HEADER + "".join(rows))
    land(ctx, repo, "two rows bound by a provenance table")
    return ["--lane", str(repo)]


# u6_long_a-history-200: the capture and a clean row are committed first; a 200-digit anchor token is
# appended in a second commit, so the class must still fire against HEAD's evidence set.
def history_200(ctx, d):
    repo = ctx.init(d)
    body = b"history capture line\n" * 2
    good = digest(body)
    ctx.write(repo / "corpus/evidence/u6a/hist/gamma.txt", body)
    first = [row("S991", "captured at corpus/evidence/u6a/hist/gamma.txt",
                 "sha256 " + good, "clean row at the first commit")]
    ctx.write(repo / "corpus/SOURCES.md", HEADER + "".join(first))
    land(ctx, repo, "first commit: capture and a clean row")
    tok = (digest(b"u6a-history") * 4)[:200]
    second = first + [row("S992", "captured at corpus/evidence/u6a/hist/gamma.txt",
                          "sha256 " + tok, "200-digit token appended later")]
    ctx.write(repo / "corpus/SOURCES.md", HEADER + "".join(second))
    land(ctx, repo, "second commit: append a 200-digit anchor token")
    return ["--lane", str(repo)]


FIXTURES = [
    # 65 digits (a real digest plus one digit) in a five-row registry: the long side decides the label.
    {"fid": "u6_long_a-registry-65", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": registry_65},
    # 96 digits on a capture that exists only as a SHA256SUMS entry: the long label on a manifest binding.
    {"fid": "u6_long_a-manifest-96", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": manifest_96},
    # 128 digits on a row bound by a PROVENANCE.md table line, with a clean row from the same table.
    {"fid": "u6_long_a-provenance-128", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": provenance_128},
    # 200 digits appended in a second commit: the long label against HEAD evidence, two-commit history.
    {"fid": "u6_long_a-history-200", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": history_200},
]
