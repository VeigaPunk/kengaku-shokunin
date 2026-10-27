"""battery44 module `u6_long_b` (seat R44BatU6b, kengaku round 44, build+attack wave).

Frozen mutant U6 (`plans/round44_c1_verify.py`, MUTANT U6: tool `anchor`, class `digest-long`, direction
`silence`, advertised by `plans/anchor_digest_check.py:88`): an anchor token that is not exactly 64 lowercase
hex digits is labelled `digest-short` when it is shorter and `digest-long` when it is longer. The mutation
relabels the long side `digest-short`, so a long token stops printing `class=digest-long` while the exit code
stays 1.

Each fixture below puts an anchor token LONGER than 64 hex digits on a row that is bound to a committed
capture, so the reference prints exactly one `DEFECT ... class=digest-long` and exits 1; the mutant prints
`class=digest-short` instead. The three shapes are a five-row registry bound by a lane path (80 hex), a row
bound only by a PROVENANCE.md table line over two commits (129 hex, an odd length), and a two-token anchor
cell read through `--evidence-ref index` where the row's capture is staged rather than committed (96 hex
beside its own 64-hex digest).

Every path a fixture uses lies inside its fixture directory, every repo is built from nothing by
`ctx.init` + `ctx.write` + `ctx.git`, and the only argv token that is not a literal option is `--lane .`
(resolved against the tool run's own working directory).
"""
import hashlib

HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
SCOPE = "battery44 long-token row"


def sha(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor, teaches):
    """One census-shaped registry line: exactly the eleven cells `anchor_digest_check.py` expects."""
    cells = [sid, source, "capture", "A", SCOPE, anchor, teaches, "mined", "2026-10-26", "180d", "-"]
    return "| " + " | ".join(cells) + " |\n"


def land(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


# u6_long_b-registry-80hex: a five-row green registry where row S702 quotes its capture's digest with sixteen
# further hex digits pasted on, bound by a lane path; demonstrates digest-long inside an otherwise clean census.
def registry_80hex(ctx, d):
    r = ctx.init(d)
    bodies = [("alpha", b"alpha capture quoted by the registry\n"),
              ("bravo", b"bravo capture whose anchor cell carries a paste\n"),
              ("gamma", b"gamma capture\n"),
              ("delta", b"delta capture\n"),
              ("epsilon", b"epsilon capture\n")]
    dig, sums = {}, []
    for name, body in bodies:
        dig[name] = sha(body)
        ctx.write(r / "corpus/evidence/r44b-registry" / f"{name}.md", body)
        sums.append(f"{dig[name]}  {name}.md\n")
    ctx.write(r / "corpus/evidence/r44b-registry/SHA256SUMS", "".join(sums))
    pasted = dig["bravo"] + "0a1b2c3d4e5f6071"
    rows = [
        row("S701", "captured at corpus/evidence/r44b-registry/alpha.md", f"sha256 {dig['alpha']}",
            "first green row of the five"),
        row("S702", "captured at corpus/evidence/r44b-registry/bravo.md", f"sha256 {pasted}",
            "the digest plus a second paste of hex tail"),
        row("S703", "captured at corpus/evidence/r44b-registry/gamma.md", f"sha256 {dig['gamma']}",
            "green row between the two"),
        row("S704", "captured at corpus/evidence/r44b-registry/delta.md", f"sha256 {dig['delta']}",
            "fourth green row"),
        row("S705", "captured at corpus/evidence/r44b-registry/epsilon.md", f"sha256 {dig['epsilon']}",
            "fifth green row"),
    ]
    ctx.write(r / "corpus/SOURCES.md", HEAD + "".join(rows))
    land(ctx, r, "five-row registry with one over-long anchor token")
    return ["--lane", "."]


# u6_long_b-provenance-129hex: two commits; the second adds a PROVENANCE.md table line and a row whose anchor
# token is 129 hex digits, so only the token itself can produce the class (bound by provenance, not by a path).
def provenance_129hex(ctx, d):
    r = ctx.init(d)
    plain = b"plain capture read by the first commit's row\n"
    ctx.write(r / "corpus/evidence/r44b-prov/plain.md", plain)
    ctx.write(r / "corpus/SOURCES.md",
              HEAD + row("S711", "captured at corpus/evidence/r44b-prov/plain.md", f"sha256 {sha(plain)}",
                         "green row landed before the provenance table"))
    land(ctx, r, "first commit: one green row and its capture")
    late = b"capture the provenance table binds to the long-token row\n"
    ctx.write(r / "corpus/evidence/r44b-prov/late.md", late)
    ctx.write(r / "corpus/evidence/r44b-prov/PROVENANCE.md",
              "| row | note | capture |\n|---|---|---|\n"
              "| S712 provenance table | the long-token row reads this capture | `late.md` |\n")
    token = (sha(late) * 3)[:129]
    ctx.write(r / "corpus/SOURCES.md",
              HEAD + row("S711", "captured at corpus/evidence/r44b-prov/plain.md", f"sha256 {sha(plain)}",
                         "green row landed before the provenance table")
              + row("S712", "the provenance table names this row's capture", f"sha256 {token}",
                    "the capture digest repeated past the digest length"))
    land(ctx, r, "second commit: provenance table and the long-token row")
    return ["--lane", "."]


# u6_long_b-index-pair-96hex: an anchor cell holding the capture's 64-hex digest and then a 96-hex paste, read
# through --evidence-ref index where row S722's capture is staged only; demonstrates the class under that ref.
def index_pair_96hex(ctx, d):
    r = ctx.init(d)
    base = b"base capture committed with the registry\n"
    ctx.write(r / "corpus/evidence/r44b-index/base.md", base)
    ctx.write(r / "corpus/evidence/r44b-index/SHA256SUMS", f"{sha(base)}  base.md\n")
    late = b"capture staged beside the registry row\n"
    long_tok = (sha(late) * 2)[:96]
    ctx.write(r / "corpus/SOURCES.md",
              HEAD + row("S721", "captured at corpus/evidence/r44b-index/base.md", f"sha256 {sha(base)}",
                         "green row at HEAD and in the index")
              + row("S722", "captured at corpus/evidence/r44b-index/late.md",
                    f"sha256 {sha(late)} sha256 {long_tok}",
                    "the digest and a longer paste in the same cell"))
    land(ctx, r, "root commit: registry, manifest and one capture")
    ctx.write(r / "corpus/evidence/r44b-index/late.md", late)
    ctx.git(r, "add", "corpus/evidence/r44b-index/late.md")
    return ["--lane", ".", "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "u6_long_b-registry-80hex", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": registry_80hex},
    {"fid": "u6_long_b-provenance-129hex", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": provenance_129hex},
    {"fid": "u6_long_b-index-pair-96hex", "tool": "anchor", "expect": "reject",
     "defects": ["digest-long"], "build": index_pair_96hex},
]
