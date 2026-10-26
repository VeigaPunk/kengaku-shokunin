"""battery44 / R44BatU5a — three fixtures that make the anchor tool's `digest-short` label observable.

Frozen mutant U5 (`plans/round44_c1_verify.py`: `("digest-short" if len(tok) < 64 else "digest-long")` ->
`("digest-long" if len(tok) < 64 else "digest-long")`) relabels every sub-64-hex anchor token `digest-long`, so
the reference's `class=digest-short` line disappears from an otherwise clean registry. Each fixture below builds
a lane repo from nothing, commits it, and carries exactly ONE such token, each bound by a different route and in
a different history shape, so a fixture's whole defect set is `{digest-short}` and the reference exits 1:

  * `u5_short_a-manifest-registry`  six census rows in a three-commit history; binding by the upstream URL's
                                    `task.toml` slug plus a `SHA256SUMS` manifest beside each capture; the defect
                                    token is a one-character truncation of a manifest-listed capture's digest;
  * `u5_short_a-index-staged`       `--evidence-ref index`: the registry and its capture are staged over a seed
                                    commit, never committed; the defect token is 16 hex digits that prefix nothing;
  * `u5_short_a-abbrev-neighbour`   `--verbose`, two commits; the second commit shortens the row's full digest by
                                    one hex digit while a resolving 12-hex `sha256 <hex>…` abbreviation sits in the
                                    same anchor cell, so the abbreviation is excused and the truncation is not.

Nothing here reads, imports or copies another battery module: every capture is generated inside the fixture and
every repo is initialised through the counter's own `ctx`."""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b8/"
       "{task}/tests/test_outputs.py")
ALPHA = b"alpha capture: four round keys and 250 plaintext rows\n"
BETA = b"beta capture: a second task directory beside it\n"
STREAM = b"one task's stderr log, named by an explicit evidence path\n"
SEED = b"seed capture committed before the attack is staged\n"
STAGED = b"staged capture: index-only evidence for this fixture\n"
REGRESS = b"regression capture: one manifest row, digest shortened later\n"


def dg(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor="-"):
    """One 11-cell census row: id source kind tier scope | anchor | teaches status opened recheck used-by."""
    cells = [sid, source, "docs", "A", "one capture per row", anchor, "pinned capture bytes",
             "mined", "2026-10-26", "2027-01-24", "corpus/knowledge/r44.md"]
    return "| " + " | ".join(cells) + " |\n"


def task_toml(org, task):
    return f'[metadata]\nname = "{org}/{task}"\n'


def sums(body, name="test_outputs.py"):
    return f"{dg(body)}  {name}\n"


def manifest_registry(ctx, d):
    # A realistic six-row registry: URL->task.toml slug binding with a SHA256SUMS manifest, three commits, and the
    # only defect a one-character truncation of a manifest-listed capture; every other row is clean or tokenless.
    r = ctx.init(d / "lane")
    ctx.write(r / "corpus/SOURCES.md", HEADER + row("S201", RAW.format(task="alpha-report")))
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "skeleton registry")
    for task, body in (("alpha-report", ALPHA), ("beta-report", BETA)):
        base = f"corpus/evidence/r44/tb2-{task}"
        ctx.write(r / f"{base}/task.toml", task_toml("harbor-framework", task))
        ctx.write(r / f"{base}/test_outputs.py", body)
        ctx.write(r / f"{base}/SHA256SUMS", sums(body))
    ctx.write(r / "corpus/evidence/r44/misc/cap.log", STREAM)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "captures and manifests")
    ctx.write(r / "corpus/SOURCES.md", HEADER
              + row("S201", RAW.format(task="alpha-report"))
              + row("S202", RAW.format(task="alpha-report"), "anchor sha256 `" + dg(ALPHA) + "`")
              + row("S203", "https://github.com/harbor-framework/terminal-bench-2/tree/main/docs")
              + row("S204", "corpus/evidence/r44/misc/cap.log", "anchor sha256 `" + dg(STREAM) + "`")
              + row("S205", RAW.format(task="beta-report"), "anchor sha256 `" + dg(BETA)[:63] + "`")
              + row("S206", "corpus/evidence/r44/misc"))
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "registry rows")
    return ["--lane", str(r)]


def index_staged(ctx, d):
    # `--evidence-ref index`: the row and its capture exist only in the index over a seed commit, and the short
    # token is 16 hex digits that are a prefix of nothing, so the class comes from length alone.
    r = ctx.init(d / "lane")
    ctx.write(r / "corpus/SOURCES.md", HEADER)
    ctx.write(r / "corpus/evidence/r44/seed/note.txt", SEED)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "seed evidence")
    short = "0123456789abcdef"
    if dg(STAGED).startswith(short) or dg(SEED).startswith(short):
        raise ValueError("the 16-hex token unexpectedly prefixes a capture digest")
    ctx.write(r / "corpus/evidence/r44/staged/capture.log", STAGED)
    ctx.write(r / "corpus/SOURCES.md", HEADER
              + row("S210", "corpus/evidence/r44/staged/capture.log", "anchor sha256 `" + short + "`")
              + row("S211", "corpus/evidence/r44/seed/note.txt", "anchor sha256 `" + dg(SEED) + "`"))
    ctx.git(r, "add", "-A")
    return ["--lane", str(r), "--evidence-ref", "index"]


def abbrev_neighbour(ctx, d):
    # Two commits: the row first carries the full digest, then gets a resolving `sha256 <12 hex>…` abbreviation
    # in the same anchor cell as the one-digit-shortened digest; the abbreviation is excused, the short token is
    # not. `--verbose` exercises the resolving note path; the defect set stays `{digest-short}`.
    r = ctx.init(d / "lane")
    full = dg(REGRESS)
    cap = "corpus/evidence/r44/regress/cap.bin"
    ctx.write(r / cap, REGRESS)
    ctx.write(r / "corpus/SOURCES.md", HEADER + row("S220", cap, "anchor sha256 `" + full + "`"))
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "full digest recorded")
    anchor = f"anchor sha256 {full[:12]}… + sha256 `{full[:63]}`"
    ctx.write(r / "corpus/SOURCES.md", HEADER + row("S220", cap, anchor))
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "digest shortened by one hex digit")
    return ["--lane", str(r), "--verbose"]


FIXTURES = [
    {"fid": "u5_short_a-manifest-registry", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": manifest_registry},
    {"fid": "u5_short_a-index-staged", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": index_staged},
    {"fid": "u5_short_a-abbrev-neighbour", "tool": "anchor", "expect": "reject",
     "defects": ["digest-short"], "build": abbrev_neighbour},
]
