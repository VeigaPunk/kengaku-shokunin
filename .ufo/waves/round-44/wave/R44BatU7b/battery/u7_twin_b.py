"""Round-44 C1 battery module `u7_twin_b`: twin-capture fixtures for `plans/anchor_digest_check.py`.

Frozen mutant U7 (`plans/round44_c1_verify.py`, direction `rc-mirror`): the resolving set of an anchor token
is truncated to its first element (`hit = sorted(...)[:1]`), so when one digest is the true digest of several
captures the row names, only one of them counts as claimed and the others are reported
`capture-unanchored`. The tool advertises the opposite (plans/anchor_digest_check.py:98-99): "A token that
resolves to several of the row's captures is not a defect — that means those captures have identical bytes".

Three fixtures, each built from nothing inside its own directory, all green under the unmodified tool
(exit 0, no defect line) and red under U7 (exit 1, `capture-unanchored`):

  u7_twin_b-url-trio-identical  one row whose three captures are byte-identical and bound by three pinned
                                URLs of two shapes (raw.githubusercontent and github.com/blob), so a single
                                token resolves to all three; a neighbouring row carries a capture of its own
  u7_twin_b-prov-twin           a twin pair inside one evidence directory, named by two PROVENANCE table
                                lines and committed in steps (captures, provenance table, then registry)
  u7_twin_b-mixed-trio          a three-capture row where a twin pair and a distinct third capture each
                                carry their own token, beside a neighbouring single-capture row

Only `hashlib` is used; no repository outside the fixture directory is read.
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"


def dig(body):
    return hashlib.sha256(body).hexdigest()


def line(*cells):
    return "| " + " | ".join(cells) + " |\n"


def row(sid, source, anchor, teaches):
    return line(sid, source, "code", "A", "fixture-scope", anchor, teaches, "mined", "2026-10-26",
                "180d", "corpus/knowledge/fixture.md")


def raw(owner, task, base):
    return f"https://raw.githubusercontent.com/{owner}/{task}/{PIN}/{task}/tests/{base}"


def blob(owner, task, base):
    return f"https://github.com/{owner}/{task}/blob/{PIN}/{task}/tests/{base}"


def commit(ctx, repo, msg):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", msg)


# One row, three byte-identical captures via three pinned URLs (two URL shapes); one token resolves to all three.
def url_trio_identical(ctx, d):
    repo = ctx.init(d / "lane")
    ev = repo / "corpus/evidence/r44t"
    body = b"grader constant table, pinned copy of one file\n"
    side = b"a second capture with bytes of its own\n"
    for sub, task in (("tb2-orbit-ring", "orbit-ring"), ("tb2-tidal-gauge", "tidal-gauge"),
                      ("tb2-payload-mux", "payload-mux"), ("tb2-spline-diff", "spline-diff")):
        ctx.write(ev / sub / "task.toml", f'name = "fixture-lab/{task}"\n')
    for sub in ("tb2-orbit-ring", "tb2-tidal-gauge", "tb2-payload-mux"):
        ctx.write(ev / sub / "test_outputs.py", body)
    ctx.write(ev / "tb2-spline-diff" / "test_outputs.py", side)
    commit(ctx, repo, "captures")
    trio = " ".join((raw("fixture-lab", "orbit-ring", "test_outputs.py"),
                     raw("fixture-lab", "tidal-gauge", "test_outputs.py"),
                     blob("fixture-lab", "payload-mux", "test_outputs.py")))
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S201", trio, "sha256 " + dig(body),
                           "one constant table published under three task directories")
              + row("S202", raw("fixture-lab", "spline-diff", "test_outputs.py"), "sha256 " + dig(side),
                    "neighbouring row holding a capture of its own"))
    commit(ctx, repo, "registry")
    return ["--lane", str(repo)]


# A twin pair in one evidence directory named by two PROVENANCE table lines for the same row, committed in steps.
def prov_twin(ctx, d):
    repo = ctx.init(d / "lane")
    ev = repo / "corpus/evidence/r44p/bundle"
    body = b"ledger excerpt, two published copies of one page\n"
    ctx.write(ev / "ledger.txt", body)
    ctx.write(ev / "ledger-copy.txt", body)
    commit(ctx, repo, "captures")
    ctx.write(ev / "PROVENANCE.md",
              "| sid | local file | upstream | digest |\n|---|---|---|---|\n"
              + line("S211", "`ledger.txt`", raw("ledger-archive", "ledger", "ledger.txt"), dig(body))
              + line("S211", "`ledger-copy.txt`", raw("ledger-archive", "ledger-copy", "ledger-copy.txt"),
                     dig(body)))
    commit(ctx, repo, "provenance")
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S211", "ledger excerpt held twice beside this row",
                           "sha256 " + dig(body),
                           "the archive published the same page twice"))
    commit(ctx, repo, "registry")
    return ["--lane", str(repo)]


# A twin pair plus a distinct third capture in one row, each with its own token, beside a clean neighbour row.
def mixed_trio(ctx, d):
    repo = ctx.init(d / "lane")
    ev = repo / "corpus/evidence/r44m"
    twin = b"the same transcript published twice\n"
    solo = b"a transcript only this row names\n"
    other = b"an unrelated capture\n"
    for sub, task, body in (("tb2-ring-a", "ring-a", twin), ("tb2-ring-b", "ring-b", twin),
                            ("tb2-gauge", "gauge", solo), ("tb2-mux", "mux", other)):
        ctx.write(ev / sub / "task.toml", f'name = "fixture-lab/{task}"\n')
        ctx.write(ev / sub / "transcript.txt", body)
    commit(ctx, repo, "captures")
    trio = " ".join((raw("fixture-lab", "ring-a", "transcript.txt"),
                     raw("fixture-lab", "ring-b", "transcript.txt"),
                     raw("fixture-lab", "gauge", "transcript.txt")))
    ctx.write(repo / "corpus/SOURCES.md",
              HEADER + row("S221", trio, "sha256 " + dig(twin) + " sha256 " + dig(solo),
                           "a twin pair and a distinct third capture in one row")
              + row("S222", raw("fixture-lab", "mux", "transcript.txt"), "sha256 " + dig(other),
                    "neighbouring row, one capture"))
    commit(ctx, repo, "registry")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "u7_twin_b-url-trio-identical", "tool": "anchor", "expect": "accept", "defects": [],
     "build": url_trio_identical},
    {"fid": "u7_twin_b-prov-twin", "tool": "anchor", "expect": "accept", "defects": [],
     "build": prov_twin},
    {"fid": "u7_twin_b-mixed-trio", "tool": "anchor", "expect": "accept", "defects": [],
     "build": mixed_trio},
]
