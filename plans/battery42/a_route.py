"""C1 battery42 — anchor binding routes (round 42, seat R42BatAncRoute, wave 1).

Six fixtures, two for each of the three binding routes `plans/anchor_digest_check.py` advertises for a
SOURCES row (docstring "### Binding" 1-3). Every lane is built from nothing: one registry row, committed
capture bytes under `corpus/evidence/`, and exactly one route by which the row's digest token can be
tied to a capture. The token is the capture's digest, so the unmodified tool accepts (no `DEFECT` line,
exit 0); a mutant that drops the route leaves the row unbound and exits 1 (rc-mirror).

  a_route-x1-provenance-table  X1  route 1 at its smallest: one PROVENANCE.md table line carrying the
                                   row id, the ticked capture file and its digest column
  a_route-x1-two-row-registry  X1  route 1 at registry scale: two rows, two tables in two evidence
                                   directories, the capture batch committed one commit before the rows
  a_route-x3-provenance-url    X3  route 2 fallback: a pinned raw URL no task.toml resolves, named by a
                                   PROVENANCE.md URL column (no task.toml in the tree at all)
  a_route-x3-blob-url          X3  the same fallback through a github.com/.../blob/ URL while a committed
                                   task.toml names a different task
  a_route-x12-slashless-toml   X12 route 2: `task.toml` gives a slash-less `name = "<slug>"` and the URL's
                                   task component matches it
  a_route-x12-two-tomls        X12 the same route with two task directories, a three-component URL subpath,
                                   and the capture accepted through its SHA256SUMS entry

Nothing here reads, imports or copies the pre-freeze direction modules; each lane differs from theirs in
row ids, directory layout, table columns and commit history. stdlib only, no tool code executed.
"""
import hashlib

SHA = "0123456789abcdef0123456789abcdef01234567"
HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def dig(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor):
    """One 11-cell census row: the anchor lands in cell 6."""
    return (f"| {sid} | {source} | code | A | binding route | sha256 {anchor} | fixture row | mined | "
            "2026-10-26 | 180d | corpus/knowledge/fixture.md |")


def commit(ctx, repo, msg):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", msg)


def build_x1_table(ctx, d):
    """X1: the row binds only through a PROVENANCE.md table line (row id, ticked file, digest column)."""
    repo = ctx.init(d / "repo")
    body = b"capture committed beside its provenance table\n"
    h = dig(body)
    base = repo / "corpus/evidence/42/route-a"
    ctx.write(base / "registry.capture", body)
    ctx.write(base / "SHA256SUMS", f"{h}  registry.capture\n")
    ctx.write(base / "PROVENANCE.md",
              "| row | origin | local file | digest |\n|---|---|---|---|\n"
              f"| S125 | copied from the registry, not re-downloaded | `registry.capture` | sha256 {h} |\n")
    ctx.write(repo / "corpus/SOURCES.md",
              HDR + row("S125", "registry copy whose bytes sit beside its provenance table", h) + "\n")
    commit(ctx, repo, "fixture: capture, table and row")
    return ["--lane", str(repo)]


def build_x1_registry(ctx, d):
    """X1: two rows, two provenance tables, the capture batch committed before the registry rows."""
    repo = ctx.init(d / "repo")
    batches = (("S126", "batch-one", "first.capture", b"first batch capture\n",
                "https://raw.githubusercontent.com/acme/batch/" + SHA + "/first-task/first.txt"),
               ("S127", "batch-two", "second.capture", b"second batch capture\n",
                "https://raw.githubusercontent.com/acme/batch/" + SHA + "/second-task/second.txt"))
    for sid, rel, name, body, url in batches:
        base = repo / "corpus/evidence/42" / rel
        ctx.write(base / name, body)
        ctx.write(base / "PROVENANCE.md",
                  "| row | upstream | local file | captured |\n|---|---|---|---|\n"
                  f"| {sid} | {url} | `{name}` | 2026-10-26 |\n")
    commit(ctx, repo, "fixture: capture batch")
    rows = []
    for sid, rel, name, body, _url in batches:
        rows.append(row(sid, f"{name} of the {rel} batch, tabled beside it under evidence/42", dig(body)))
    ctx.write(repo / "corpus/SOURCES.md", HDR + "\n".join(rows) + "\n")
    commit(ctx, repo, "fixture: registry rows")
    return ["--lane", str(repo)]


def build_x3_url_column(ctx, d):
    """X3: a pinned raw URL that only a PROVENANCE.md URL column names, with no task.toml in the tree."""
    repo = ctx.init(d / "repo")
    body = b"pinned upstream file, capture beside the table\n"
    h = dig(body)
    base = repo / "corpus/evidence/42/route-b"
    url = f"https://raw.githubusercontent.com/acme/bench/{SHA}/plain-task/capture.py"
    ctx.write(base / "capture.py", body)
    ctx.write(base / "PROVENANCE.md",
              "| upstream | local file | note |\n|---|---|---|\n"
              f"| {url} | `capture.py` | no row id on this line; only the URL names the capture |\n")
    ctx.write(repo / "corpus/SOURCES.md",
              HDR + row("S128", f"pinned at {url} in the task's own tree", h) + "\n")
    commit(ctx, repo, "fixture: pinned capture and URL column")
    return ["--lane", str(repo)]


def build_x3_blob(ctx, d):
    """X3: a blob-form URL named by a provenance URL column while a committed task.toml names another task."""
    repo = ctx.init(d / "repo")
    body = b"pinned grader bytes\n"
    h = dig(body)
    base = repo / "corpus/evidence/42/route-e"
    url = f"https://github.com/acme/bench/blob/{SHA}/deeptask/tests/test_outputs.py"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "PROVENANCE.md",
              "| upstream | local file | captured |\n|---|---|---|\n"
              f"| {url} | `test_outputs.py` | 2026-10-26 |\n")
    other = repo / "corpus/evidence/42/route-e-other"
    ctx.write(other / "task.toml", 'name = "acme/other-task"\nversion = 1\n')
    ctx.write(other / "instruction.md", "a different task, shipped whole\n")
    ctx.write(repo / "corpus/SOURCES.md",
              HDR + row("S129", f"pinned at {url} under the deep task directory", h) + "\n")
    commit(ctx, repo, "fixture: blob-pinned capture and a foreign task.toml")
    return ["--lane", str(repo)]


def build_x12_slashless(ctx, d):
    """X12: task.toml carries a slash-less name and the URL's task component matches exactly that slug."""
    repo = ctx.init(d / "repo")
    body = b"grader-owned test file\n"
    h = dig(body)
    base = repo / "corpus/evidence/42/route-c"
    ctx.write(base / "test_outputs.py", body)
    ctx.write(base / "SHA256SUMS", f"{h}  test_outputs.py\n")
    ctx.write(base / "task.toml", 'name = "circuit-task"\nversion = 1\n\n[author]\nname = "acme"\n')
    url = f"https://raw.githubusercontent.com/acme/bench/{SHA}/circuit-task/tests/test_outputs.py"
    ctx.write(repo / "corpus/SOURCES.md", HDR + row("S125", f"pinned at {url}", h) + "\n")
    commit(ctx, repo, "fixture: slash-less task name")
    return ["--lane", str(repo)]


def build_x12_two_tomls(ctx, d):
    """X12: two task directories, a three-component URL subpath, the capture accepted via its manifest entry."""
    repo = ctx.init(d / "repo")
    body = b"lookup circuit shipped as data\n"
    h = dig(body)
    mine = repo / "corpus/evidence/42/route-f-mine"
    ctx.write(mine / "lookup-circuit.txt", body)
    ctx.write(mine / "SHA256SUMS", f"{h}  lookup-circuit.txt\n")
    ctx.write(mine / "task.toml", 'name = "data-task"\nversion = 2\n')
    other = repo / "corpus/evidence/42/route-f-other"
    ctx.write(other / "task.toml", 'name = "bench/other-task"\nversion = 1\n')
    ctx.write(other / "sim.c", "int main(void) { return 0; }\n")
    url = f"https://raw.githubusercontent.com/acme/bench/{SHA}/group/data-task/lookup-circuit.txt"
    ctx.write(repo / "corpus/SOURCES.md", HDR + row("S126", f"pinned at {url}", h) + "\n")
    commit(ctx, repo, "fixture: two task directories")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a_route-x1-provenance-table", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x1_table},
    {"fid": "a_route-x1-two-row-registry", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x1_registry},
    {"fid": "a_route-x3-provenance-url", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x3_url_column},
    {"fid": "a_route-x3-blob-url", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x3_blob},
    {"fid": "a_route-x12-slashless-toml", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x12_slashless},
    {"fid": "a_route-x12-two-tomls", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_x12_two_tomls},
]
