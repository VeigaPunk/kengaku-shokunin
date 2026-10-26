"""battery44 / u9_worktree_a: an erratum that exists only in the working tree must still exempt its row (U9).

`plans/anchor_digest_check.py:106-107` advertises "lessons are read from the working tree for paths committed at
HEAD, so a seat's erratum counts before it is committed while the digest it cites still has to be committed". The
read is `anchor_digest_check.py:384`, `text = f.read_text(encoding="utf-8", errors="replace")` inside
`load_errata`; mutant U9 swaps it for `git show HEAD:<path>`, so an erratum appended to a committed lesson but not
yet committed stops counting. Every fixture below is a repository built from nothing: the lesson is committed
first and edited in the working tree afterwards, so the reference is green (exit 0, no defect) while U9 rejects
(exit 1) — the declared `rc-mirror` direction.

Two shapes. A five-row registry with a SHA256SUMS manifest and a task.toml, whose exempted row carries another
committed capture's real digest (`digest-wrong-capture` under U9). A three-commit history whose exempted row
carries an 8-hex abbreviation (`abbrev-unresolved` under U9), with a second, already-committed erratum that keeps
its own row green in both variants, so the kill is the missing working-tree erratum and nothing else.
"""

import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def row(cells):
    return "| " + " | ".join(cells) + " |\n"


def commit(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def u9_registry_wrong_capture(ctx, d):
    """Five-row registry (manifest + task.toml): the exempted row cites a sibling capture's real digest."""
    r = ctx.init(d / "repo")
    reg = "corpus/evidence/r44-registry"
    bodies = {"alpha": b"registry alpha capture\n",
              "beta": b"registry beta capture\n",
              "gamma": b"registry gamma capture\n"}
    for name, body in bodies.items():
        ctx.write(r / f"{reg}/capture-{name}.txt", body)
    ctx.write(r / f"{reg}/SHA256SUMS",
              "".join(f"{digest(body)}  capture-{name}.txt\n" for name, body in bodies.items()))
    ctx.write(r / f"{reg}/task.toml", 'name = "kengaku/r44-registry"\n')
    a, b, g = (digest(bodies[n]) for n in ("alpha", "beta", "gamma"))
    text = HEADER
    text += row(["S201", f"captured at {reg}/capture-alpha.txt", "capture", "A", "registry",
                 f"sha256 {b}", "row exempted by a working-tree erratum", "mined", "2026-10-26", "180d", "-"])
    text += row(["S202", f"captured at {reg}/capture-beta.txt", "capture", "A", "registry",
                 f"sha256 {b}", "correctly anchored sibling", "mined", "2026-10-26", "180d", "-"])
    text += row(["S203", f"captured at {reg}/capture-gamma.txt", "capture", "A", "registry",
                 f"sha256 {g}", "second correctly anchored sibling", "mined", "2026-10-26", "180d", "-"])
    text += row(["S204", f"captured at {reg}/capture-gamma.txt", "capture", "A", "registry",
                 f"sha256 {g[:8]}…", "abbreviated anchor that resolves", "mined", "2026-10-26", "180d", "-"])
    text += row(["S205", f"captured at {reg}/capture-alpha.txt", "capture", "A", "registry", "",
                 "row that makes no anchor claim", "mined", "2026-10-26", "180d", "-"])
    lesson = "corpus/lessons/round-44-registry.md"
    notes = "# Registry notes\n\nNo erratum yet: S201 still cites the sibling's digest.\n"
    ctx.write(r / lesson, notes)
    commit(ctx, r, "registry captures, manifest and notes")
    ctx.write(r / "corpus/SOURCES.md", text)
    commit(ctx, r, "registry rows")
    ctx.write(r / lesson,
              notes + f"\nErratum (round 37): S201 anchor sha256 {b} cites the wrong capture; the digest of the "
                      f"capture this row names is sha256 {a}\n")
    return ["--lane", str(r)]


def u9_history_abbrev(ctx, d):
    """Three-commit history: the late erratum covers an 8-hex abbreviation; an earlier committed erratum stays."""
    r = ctx.init(d / "repo")
    ev = "corpus/evidence/r44-abbrev"
    alpha, beta = b"abbreviation alpha capture\n", b"abbreviation beta capture\n"
    ctx.write(r / f"{ev}/alpha.txt", alpha)
    ctx.write(r / f"{ev}/beta.txt", beta)
    commit(ctx, r, "captures")
    a, b = digest(alpha), digest(beta)
    abb = ("0" if a[0] != "0" else "1") + a[1:8]
    late = "corpus/lessons/r44-b-late.md"
    early = "corpus/lessons/r44-a-baseline.md"
    text = HEADER
    text += row(["S301", f"captured at {ev}/alpha.txt", "capture", "A", "history",
                 f"sha256 {abb}…", "abbreviated anchor covered by the late erratum", "mined", "2026-10-26",
                 "90d", "-"])
    text += row(["S302", f"captured at {ev}/alpha.txt", "capture", "A", "history",
                 f"sha256 {b}", "row repaired by an already-committed erratum", "mined", "2026-10-26", "90d", "-"])
    ctx.write(r / "corpus/SOURCES.md", text)
    commit(ctx, r, "rows")
    ctx.write(r / early,
              "# Baseline errata\n\n"
              f"Erratum (round 37): S302 anchor sha256 {b} cites the wrong capture; the digest of the capture "
              f"this row names is sha256 {a}\n")
    late_text = "# Late errata\n\nAppended before the round's own commit.\n"
    ctx.write(r / late, late_text)
    commit(ctx, r, "baseline erratum and an empty late page")
    ctx.write(r / late,
              late_text + f"\nErratum (round 37): S301 anchor sha256 {abb} was an abbreviation; the full digest "
                          f"of the capture this row names is sha256 {a}\n")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "u9_worktree_a-registry-wrong-capture", "tool": "anchor", "expect": "accept",
     "defects": [], "build": u9_registry_wrong_capture},
    {"fid": "u9_worktree_a-history-abbrev", "tool": "anchor", "expect": "accept",
     "defects": [], "build": u9_history_abbrev},
]
