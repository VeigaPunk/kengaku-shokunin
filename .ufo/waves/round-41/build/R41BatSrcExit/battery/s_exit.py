"""battery41 s_exit: the `plans/sources_adopt.py` CLI exit codes of frozen mutants S07 and S11.

Each fixture builds a small but lane-shaped tree -- a registry at `corpus/SOURCES.md`, an adoption
package under `.ufo/waves/round-41/`, one knowledge entry -- and asks the CLI to admit rows from it.
The tool's `check()` gate and its `main()` refusal branch sit on opposite sides of the S07/S11 byte
edits, so the two exits are told apart only by whether the run stops before or after the append
block is built.

  s_exit-collision-admit      S07 3>0  staged id re-uses a live registry id while --admit-ids asks for it
  s_exit-collision-indented   S07 3>0  same branch, duplicate pasted 2 spaces indented inside a list item
  s_exit-queued-admit         S11 5>0  requested row is `queued`: check() passes, build_block refuses
  s_exit-opened-elsewhere     S11 5>0  requested row was opened on another date and is not attested
  s_exit-attest-opened        -   -    the same stale row with --attest-opened is re-dated and appended
  s_exit-absent-id            -   -    an id absent from the package refuses at check() (round-41 S10)

`defects` is [] throughout: the sources tool reports by exit code, never by a class set.
"""

HEAD = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)

ENTRY = "corpus/knowledge/tb2-constraints-scheduling-grader.md"


def row(rid, status="mined", opened="2026-10-26", indent="",
        anchor='l.4: "only the Wednesday and Thursday eleven o clock slots are one hour" (13 words)',
        source="terminal-bench-2 capture, local"):
    """One 11-cell registry row; `indent` places the row inside a list item of the staged package."""
    return (indent + f"| {rid} | {source} | docs | A | grader schedule | {anchor} | embedded scheduling "
            f"model | {status} | {opened} | 180d | {ENTRY} |\n")


def lane(ctx, d, registry, staged):
    """Registry at its lane path, the adoption package at its wave path; returns the mode's argv tail."""
    ctx.write(d / "corpus/SOURCES.md", HEAD + "".join(registry))
    ctx.write(d / ENTRY, "# fixture entry\n\nA fixture knowledge entry, not the lane's.\n")
    ctx.write(d / ".ufo/waves/round-41/SOURCES.append.md", HEAD + "".join(staged))
    return ["--registry", "corpus/SOURCES.md", "--package", ".ufo/waves/round-41/SOURCES.append.md"]


def admit(*wanted, extra=()):
    return ["--admit-ids", ",".join(wanted), "--entries", ENTRY, "--access-date", "2026-10-26", *extra]


def b_collision(ctx, d):
    # S07: the staged row re-uses live id S122 while --admit-ids names it -> the check refuses exit 3;
    # the row is itself `mined` and opened on the access date, so the mutated run appends and exits 0.
    argv = lane(ctx, d,
                [row("S121"), row("S122", opened="2026-10-25"), row("S123")],
                [row("S122")])
    return argv + admit("S122")


def b_collision_indented(ctx, d):
    # S07 second shape: the duplicate is pasted 2 spaces indented under a bullet, which the census
    # anchor (0-3 leading spaces) still parses -> collision exit 3, and the mutation appends it.
    argv = lane(ctx, d,
                [row("S130"), row("S131", opened="2026-10-24")],
                [row("S140", opened="2026-10-24"), row("S131", indent="  ")])
    return argv + admit("S131")


def b_queued(ctx, d):
    # S11: a requested row still `queued` is a valid staged status for check(), which passes; the
    # append block refuses it as not-mined -> exit 5, and the mutation appends the queued row (0).
    argv = lane(ctx, d, [row("S121")], [row("S150", status="queued")])
    return argv + admit("S150")


def b_opened_elsewhere(ctx, d):
    # S11 other refusal: a mined row opened on 2026-09-30 is not opened this round and is not
    # attested -> exit 5; the mutation appends it with the stale opened cell and exits 0.
    argv = lane(ctx, d, [row("S121")], [row("S160", opened="2026-09-30")])
    return argv + admit("S160")


def b_attest_opened(ctx, d):
    # Boundary of the same branch: the stale opened cell with --attest-opened is re-dated to the
    # access date and appended -> exit 0. Both mutants pass it, so it carries no kill.
    argv = lane(ctx, d, [row("S121")], [row("S161", opened="2026-09-30")])
    return argv + admit("S161", extra=("--attest-opened",))


def b_absent_id(ctx, d):
    # Boundary this module does not claim: an id absent from the package is refused inside check()
    # (exit 5) before either mutated line is reached -- the round-41 S10 withdrawal, recorded not fixed.
    argv = lane(ctx, d, [row("S121")], [row("S170")])
    return argv + admit("S199")


def fx(fid, expect, build):
    return {"fid": fid, "tool": "sources", "expect": expect, "defects": [], "build": build}


FIXTURES = [
    fx("s_exit-collision-admit", "exit-3", b_collision),
    fx("s_exit-collision-indented", "exit-3", b_collision_indented),
    fx("s_exit-queued-admit", "exit-5", b_queued),
    fx("s_exit-opened-elsewhere", "exit-5", b_opened_elsewhere),
    fx("s_exit-attest-opened", "accept", b_attest_opened),
    fx("s_exit-absent-id", "exit-5", b_absent_id),
]
